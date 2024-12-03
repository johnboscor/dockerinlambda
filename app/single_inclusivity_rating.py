import re
import numpy as np
import sys
import os
# append current working directory to system so app.wordlists is recognized
sys.path.append(os.getcwd())
from app.wordlists import *


def tokenize_text(text):
    """
    Tokenize a blob of text into a list of words

    Args:
        text (str): long text such as job description

    Returns:
        list(str)
    """

    # Gender Decoder Version
    cleaner_text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    cleaner_text = re.sub("[\\s]", " ", cleaner_text, 0, 0)
    cleaned_word_list = re.sub(u"[\.\t\,“”‘’<>\*\?\!\"\[\]\@\':;\(\)\./&]"," ", cleaner_text, 0, 0)
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

def handle_duplicates(word_list):
    """ 
    When there is duplicate words, show the word and the number of times it repeats
    For example, "understanding (2 times)" when understanding appears twice
    When the word is not duplicate, just show it as is

    Args:
        word_list (list(str)): list of words

    Returns:
        list(str)
    """
    word_count_dict = {}
    gender_words_list = []
    for item in word_list:
        if item not in word_count_dict.keys():
            word_count_dict[item] = 1
        else:
            word_count_dict[item] += 1
    for key, value in word_count_dict.items():
        if value == 1:
            gender_words_list.append(key)
        else:
            gender_words_list.append(f"{key} ({value} times)")
    return gender_words_list

def find_and_count_coded_words(advert_word_list, gendered_word_list):
    """
    Return a list of unique gendered words, and the words count in that list

    Args:
        advert_word_list (list(str)): tokenized text from job description
        gendered_word_list (list(str)): gendered word list

    Returns:
        (list(str), int)
    """
    gender_coded_words = [word for word in advert_word_list
        for coded_word in gendered_word_list 
        if (word.startswith(coded_word) and word not in non_coded_exceptions)]
    gender_coded_words_unique = handle_duplicates(gender_coded_words)
    return gender_coded_words_unique, len(gender_coded_words)

def calculate_gender_words(tokenized_text):
    """
    Returns the count of masculine and feminine words found from tokenized words
    and return the founded feminine and masculine coded words

    Args:
        tokenized_text (list(str)): tokenized words

    Returns:
        (dict, list(str), list(str))
    """
    gendered_words = []
    masculine_words_list = []
    feminine_words_list = []
    gender_words_count = {'male': 0, 'female': 0}
    if tokenized_text == np.nan or tokenized_text == 'nan':
        gendered_words.append({'male': np.nan, 'female': np.nan})
        masculine_words_list.append(np.nan)
        feminine_words_list.append(np.nan)
    else:
        masculine_words, masculine_count = find_and_count_coded_words(tokenized_text,masculine_coded_words)
        gender_words_count['male'] = masculine_count
        feminine_words, feminine_count = find_and_count_coded_words(tokenized_text,feminine_coded_words)
        gender_words_count['female'] = feminine_count
            
    return gender_words_count, masculine_words, feminine_words

def determine_gender_tag(x, strong_cutoff = 3):
    """
    Return gender tag in the following categories: 
    strongly feminine, feminine, netural, masculine and strongly masculine tag based on the cutoff threshold.
    By default, the cutoff is 3 words  

    Args:
        x (int): number of ferminine words - number of masculine words
        strong_cutoff (int, optional): threshold used to get into the strong categories. Defaults to 3.

    Returns:
        str
    """
    if x == 0:
        return 'Neutral'
    elif x > 0 and x <= strong_cutoff:
        return 'Feminine'
    elif x > strong_cutoff:
        return 'Strongly Feminine'
    elif x < 0 and x >= -strong_cutoff:
        return 'Masculine'
    elif x < -strong_cutoff:
        return 'Strongly Masculine'
    else:
        return None

def create_gender_tag(job_description, verbose=False):
    """
    A final gender tagging function that takes job description and return
    {gender_tag, masculine words, ferminine words}

    Args:
        job_description (list(str)): job description
        verbose (bool, optional): verbose flag. Defaults to False.

    Returns:
        {gender_tag, masculine words, ferminine words}
    """
    result = {}
    tokenized_text = tokenize_text(job_description)
    gender_words_count, masculine_words, feminine_words = calculate_gender_words(tokenized_text)
    gender_tag = determine_gender_tag(gender_words_count['female'] - gender_words_count['male'])
    result['gender_tag'], result['gender_word_count'], result['masculine_words'], result['feminine_words'] = \
         gender_tag, gender_words_count, masculine_words, feminine_words
    if verbose:
        print(result)

    return result

def main():
    job_description = "Slalom is a purpose-driven consulting firm that helps companies solve business problems and build for the future, with solutions spanning business advisory, customer experience, technology, and analytics. We partner with companies to push the boundaries of what?s possible?together. Founded in 2001 and headquartered in Seattle, WA, Slalom has organically grown to nearly 6,000 employees. We were named one of Fortune?s 100 Best Companies to Work For in 2018 and are regularly recognized by our employees as a best place to work. You can find us in 27 cities across the U.S., U.K., and Canada. Job Title: .NET Developer As a consultant, you will be involved in designing and delivering quality solutions. Your duties may include interacting with the user or business group to help define the client*s needs and translating those needs into a solution of value. As a partner to our client, you will help them be successful by working within their framework or bringing an appropriate framework and structure to the process that works well with the client. Responsibilities: Design, develop, test, support, and deploy desktop, custom web, and mobile applications in a .NET environment Develop system architecture, design, and code in accordance with the clients' requirements Help architect and design solutions, or act in a lead position responsible for the productivity of the development team Help clients implement software development methodologies Produce applications that provide measurable business value to our clients Qualifications: 3+ years of development experience, and a minimum of 2 years of experience with Microsoft Visual Studio, C# or Visual Basic, andÂ  ASP.Net Experience with object-oriented design and development techniques; solid understanding of basic development best practices Ability to work well in a team and individually Azure experience strongly preferred Formal training or experience in project management and building a rapport with clients Demonstrated ability around decision-making, delegation, and building trust and credibility Understanding of how software development projects are organized, including how work is prioritized, scope-managed, and risk-assessed and mitigated Slalom is an equal opportunity employer and all qualified applicants will receive consideration for employment without regard to race, color, religion, sex, national origin, disability status, protected veteran status, or any other characteristic protected by law."
    result = create_gender_tag(job_description, verbose=True)
    return result

if __name__ == "__main__":
    main()