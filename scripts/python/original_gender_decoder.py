import pandas as pd
import re
import spacy
from spacy.tokenizer import Tokenizer
from spacy.tokens import Token
from nltk.stem.snowball import SnowballStemmer
#from wordcloud import WordCloud
#from matplotlib import pyplot as plt
#import os
import numpy as np
#%matplotlib inline
from original_wordlists import *
nlp = spacy.load("en_core_web_sm") #
tokenizer = Tokenizer(nlp.vocab)
stemmer = SnowballStemmer(language='english')

# Gender Decoder Version
def format_text(data):
    """ Returns a processed version of the input text, either the tokenized text or full spacy 
    NLP objects. NLP objects contain much more functionality and take longer to process"""
    cleaner_text = ''.join([i if ord(i) < 128 else ' '
        for i in data])
    cleaner_text = re.sub("[\\s]", " ", cleaner_text, 0, 0)
    cleaned_word_list = re.sub(u"[\.\t\,“”‘’<>\*\?\!\"\[\]\@\':;\(\)\./&]"," ", cleaner_text, 0, 0)
    #string_word_list = cleaned_word_list.strip().lower().replace('\n', '')
    # de_hyphen_non_coded_words
    data_cleaned = cleaned_word_list.strip().lower().replace('\n', '').split(" ")
    for word in data_cleaned:
        if word.find("-"):
            is_coded_word = False
            for coded_word in hyphenated_coded_words:
                if word.startswith(coded_word):
                    is_coded_word = True
            if not is_coded_word:
                word_index = data_cleaned.index(word)
                data_cleaned.remove(word)
                split_words = word.split("-")
                data_cleaned = (data_cleaned[:word_index] + split_words +data_cleaned[word_index:])
    return data_cleaned

def de_hyphen_non_coded_words(word_list):
    for word in word_list:
        if word.find("-"):
            is_coded_word = False
            for coded_word in hyphenated_coded_words:
                if word.startswith(coded_word):
                    is_coded_word = True
            if not is_coded_word:
                word_index = word_list.index(word)
                word_list.remove(word)
                split_words = word.split("-")
                word_list = (word_list[:word_index] + split_words +
                    word_list[word_index:])
    return word_list

def get_lemmas(row):
    """Returns a processed version of the input text;
    This function will remove inflectional endings only and to return the base or dictionary form of a word
    """
    result = []
    if row:
        for elem in row:
            #lemma = lemmatizer(elem.text, elem.pos_)
            result.append(elem.lemma_)
    return result

def get_stem(row):
    """Returns a processed version of the input text;
    This function will reducing the word to its core root, e.g. stemming --> stem
    """
    result = []
    if row:
        for elem in row:
            result.append(stemmer.stem(elem))
    return result

def handle_duplicates(word_list):
    d = {}
    l = []
    for item in word_list:
        if item not in d.keys():
            d[item] = 1
        else:
            d[item] += 1
    for key, value in d.items():
        if value == 1:
            l.append(key)
        else:
            l.append("{0} ({1} times)".format(key, value))
    return l

def find_and_count_coded_words(advert_word_list, gendered_word_list):
    gender_coded_words = [word for word in advert_word_list
        for coded_word in gendered_word_list 
        if (word.startswith(coded_word) and word not in non_coded_exceptions)]
    gender_coded_words_unique = handle_duplicates(gender_coded_words)
    return gender_coded_words_unique, len(gender_coded_words)
    #return (",").join(gender_coded_words), len(gender_coded_words)

def cal_mas_fem(data, col = "NLP STEM"):
    """
    Returns the count of masculine and feminine words that found from the input text column
    and return the founded feminine and masculine coded words that found from the input text column
    """
    gendered_words = []
    masculine_words_list = []
    feminine_words_list = []
    for r in data[col].values: 
        count_dict = {'male': 0, 'female': 0}
        if r == np.nan or r == 'nan':
            gendered_words.append({'male': np.nan, 'female': np.nan})
            masculine_words_list.append(np.nan)
            feminine_words_list.append(np.nan)
            continue
        else:
            masculine_words, masculine_count = find_and_count_coded_words(r,masculine_coded_words)
            count_dict['male'] = masculine_count
            feminine_words, feminine_count = find_and_count_coded_words(r,feminine_coded_words)
            count_dict['female'] = feminine_count
            # append the values
            gendered_words.append(count_dict)
            masculine_words_list.append(masculine_words)
            feminine_words_list.append(feminine_words)
            
    return gendered_words, masculine_words_list, feminine_words_list

# compute the gender tag
def val_gender_tag(x,strong_cutoff = 3):
    """
    Return the data with the strong feminine, feminine, netural, masculine and strongly masculine tag based on the strongly cutoff percentage.
    By default, the cutoff is 3 words    
    """
    if x == 0:
        return 'Netural'
    elif x > 0 and x <= strong_cutoff:
        return 'Feminine'
    elif x > strong_cutoff:
        return 'Strongly Feminine'
    elif x < 0 and x >= -strong_cutoff:
        return 'Masculine'
    elif x < -strong_cutoff:
        return 'Strongly Masculine'
    else:
        return np.nan

# 
def gender_tag(data ,input_col = 'NLP STEM', col = 'Inferred Gender'):
    """
    Return the data with the gender tag [Female, Male, Tie, Unkown] based on the feminine and masculine pronouns.
    """
    feminine_pronouns = ("she", "her")
    masculine_pronouns = ("he", "his")
    gendered_counts = []
    for r in data[input_col].values: 
        count_dict = {'male': 0, 'female': 0}
        if r is np.nan:
            gendered_counts.append(count_dict)
            continue
        else:
            for elem in r:
                if elem in masculine_pronouns:
                    count_dict['male'] += 1
                elif elem in feminine_pronouns:
                    count_dict['female'] += 1
            gendered_counts.append(count_dict)
    pct_female = []
    pct_male = []
    for score in gendered_counts:
        m = score['male']
        f = score['female']
        total = m  +f
        if total == 0:
            pct_female.append(0)
            pct_male.append(0)
        else:
            pct_female.append(f/total)
            pct_male.append(m/total)

    # add gender percentages to data
    data['female%'] = pct_female
    data['male%'] = pct_male
    data.loc[data['male%'] > 0.50, col] = 'Male'
    data.loc[(data['male%'] == 0.50), col] = 'Tie'
    data.loc[(data['female%'] > 0.50), col] = 'Female'
    data.loc[(data['female%'] == 0) & (data['male%'] == 0), col] = 'Unknown'
    data.drop(columns=['female%', 'male%'], inplace = True)
    return data

# Read data
jobs = pd.read_csv('data/input/jobs_to_rate_2017-2018.csv',encoding='ISO-8859-1')
input_col = 'Text Description'
#jobs = jobs[jobs[input_col].notnull()].reset_index(drop=True)

jobs[jobs[input_col].isnull()]

# make sure the column is string datatype
jobs[input_col] = jobs[input_col].astype(str)
# apply the format_text function
jobs['NLP'] = jobs[input_col].apply(format_text)

gendered_words, masculine_words_list, feminine_words_list = cal_mas_fem(jobs, col="NLP")
jobs = pd.concat([jobs, pd.DataFrame(gendered_words)], axis=1)
jobs['Masculine Words'] = masculine_words_list
jobs['Feminine Words'] = feminine_words_list

# create gender tag
jobs['Gender_Tag'] = (jobs['female']-jobs['male']).apply(val_gender_tag)

# keep null as null not Netural
jobs.loc[jobs[input_col] =='nan', 'Gender_Tag'] = np.nan

jobs.to_csv('data/output/jobs_ads_to_add_tech_flag_2017-2018.csv', index=False)
