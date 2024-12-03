import pandas as pd
import itertools
import re
from nltk.corpus import stopwords

def getAllKeywords(techTagOp):
    """
        :getAllKeywords: Get all the keywords from technical/non-technical job description.

        :param techTagOp: The input of the funcation is dataframe with just tech or non-tech jobs
        :type techTagOp: pandas.core.frame.DataFrame

        :returns: Set of unique keywords excluding special characters, stopwords and ignoring case sensitive.
    """
        
    # Tokenize
    techTagTokens = [sub.split() for sub in set(techTagOp['Text Description'].fillna(""))]
    # convert list of list to list
    techTagUnqList = set(list(itertools.chain(*techTagTokens)))
    # Remove special characters
    techTagUnqListSpl = set([re.sub('[^a-zA-Z0-9]+', '', _) for _ in techTagUnqList])
    # Remove stop words
    techTagUnqListSplStop = [word for word in techTagUnqListSpl if word not in stopwords.words('english')]
    # case insensitive
    techTagUnqListSplStopCase = set({v.casefold(): v for v in techTagUnqListSplStop}.values())
    # Non-integers only
    techTagUnq = set(sorted([item for item in techTagUnqListSplStopCase if not item.isdigit()]))
    
    return (techTagUnq)


# Convert long string as list of strings
def stringToList(string):
    if not pd.isnull(string):
        listRes = list(string.split(" "))
        return [re.sub('[^a-zA-Z0-9]+', '', _) for _ in listRes]
    else:
        return " "


# Upon looping, The mappedTokens will contain list of sets, where len(list) = len(total jobs)
# Example: [ set(),{'ARM','Agile','Agilebased'},......... ] 
# implies the first job ad contains zero tech words, the second job ad contains 'ARM','Agile','Agilebased' technical words..
def mapTokens(job_ads_attribute, tech_words_list):
    """
        :mapTokens: Get all the keywords from technical/non-technical job description. The input of the funcation is dataframe with just tech or non-tech jobs

        :param job_ads_attribute: 'Text Description' or 'Job Order: External Job Title'
        :type job_ads_attribute: pandas.core.series.Series

        :returns: List of words in 'tech_words_list' are mapped with 'Text Description' or 'Job Order: External Job Title'
    """
    mappedTokens = [] 
    for i, role in enumerate (job_ads_attribute):
        mappedTokens.append(set(stringToList(job_ads_attribute[i])) & set(tech_words_list))
    return mappedTokens


def tech_tag(inputFile, jobDescriptionCol, mappedTokensText, mappedTokensTitle):
    """
        :tech_tag: Tag the tech and non-tech based on the 'Text Description' or 'Job Order: External Job Title'

        :param mappedTokensText: List of words in 'tech_words_list' are mapped with 'Text Description'
        :type mappedTokensText: list
        
        :param mappedTokensTitle: List of words in 'tech_words_list' are mapped with 'Job Order: External Job Title'
        :type mappedTokensTitle: list

        :returns: job_ads dataframe with additional column 'Tech_Flag'
    """
    # The dummy job descriptions/ templates have this sentence in common
    dummyJD = 'Avoid using a laundry list of technologies and/or skills'

    job_ads = pd.read_csv(inputFile)

    for i in range(len(job_ads)):
        # if the job 'Text Description' is empty or dummy -- Tag it based on the Job Title ; else use 'Text Description' to tag tech and non-tech.
        if not pd.isnull(job_ads[jobDescriptionCol][i]) and dummyJD not in job_ads[jobDescriptionCol][i]:
            # If we have mapped tokens between 'Text Description' and tech_words_list -> Tag 'Tech' else 'Non-Tech'
            if len(mappedTokensText[i]):
                job_ads.at[i,'Tech_Flag'] = 'Tech'
            else:
                job_ads.at[i,'Tech_Flag'] = 'Non-Tech'
        else:
            if len(mappedTokensTitle[i]):
                job_ads.at[i,'Tech_Flag'] = 'Tech'
            else:
                job_ads.at[i,'Tech_Flag'] = 'Non-Tech'
    
    return job_ads


def create_tech_flags(
    input_file_path,
    output_file_path,
    job_title_col_name,
    job_description_col_name,
    reference_tech_words_path='data/input/technical_flag_reference_tech_words.xlsx'
    ):
    """ Create technical flag based on job description or job title
        append the results to a new Tech_Flag column in the input_file

    Args:
        input_file_path (directory): input file path
        output_file_path (directory): output file path
        job_title_col_name (str): job title column name
        job_description_col_name (str): job description column name
        reference_tech_words_path (str, optional): technical_flag_reference_tech_words file path. 
            Defaults to 'data/input/technical_flag_reference_tech_words.xlsx'.

    Returns:
        Action: Wrote a output CSV file to output_file_path
        Return (pd.DataFrame): Output data
    """
    tech_words = pd.read_excel(reference_tech_words_path).dropna()
    tech_words_list = tech_words['Words'].tolist()

    # What words in 'tech_words_list' are mapped with 'Text Description'
    input_data = pd.read_csv(input_file_path)
    mappedTokenText = mapTokens(input_data[job_description_col_name], tech_words_list)
    # mappedTokensText = mapTokens(job_ads['Text Description'])

    # What words in 'tech_words_list' are mapped with 'Job title'
    mappedTokenTitle = mapTokens(input_data[job_title_col_name], tech_words_list)
    # mappedTokensTitle = mapTokens(job_ads['Job Order: External Job Title'])

    output_data = tech_tag(input_file_path, job_description_col_name, mappedTokenText, mappedTokenTitle)
    
    output_data.to_csv(output_file_path, index=False)
    print(f'INFO: Wrote the output file to: {output_file_path}')

    return output_data


def main():
    input_file_path = 'data/input/sample_job_descriptions.csv'
    output_file_path = 'data/output/sample_job_descriptions_tech_flag_output.csv'
    job_title_col_name = 'Job Title'
    job_description_col_name = 'Job Description'
    result = create_tech_flags(input_file_path, output_file_path, job_title_col_name, job_description_col_name)
    return result

if __name__ == "__main__":
    main()
