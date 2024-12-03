import pandas as pd
import sys
import os
sys.path.append(os.getcwd())
from app.single_inclusivity_rating import create_gender_tag
from tqdm import tqdm


def do_batch_inclusivity_rating(input_file_path, output_file_path, job_description_col='job_description'):
    """
    create a batch process for gender decoder to handle many job descriptions all at once
    there is also a dynamic progress bar indicating number of job descriptions processed and % completion

    Args:
        input_file_path (directory): input file path
        output_file_path (directory): output file path
        job_description_col (str, optional): job description column name. Defaults to 'job_description'.

    Returns:
        Action: generated an output_file in the output_file_path
    """
    data = pd.read_csv(input_file_path, encoding='ISO-8859-1')
    job_descriptions = data[job_description_col].values

    # use generator for speed
    # use error handling when job description value is not a string
    gender_decoder_results = (
        create_gender_tag(job_description, verbose=False) 
        if type(job_description)==str \
        else {
            'gender_tag': None, 
            'gender_word_count': {'male': 0, 'female': 0}, 
            'masculine_words': list(), 
            'feminine_words': list()
            } 
        for job_description in tqdm(job_descriptions)
    )

    gender_decoder_results_df = pd.DataFrame(gender_decoder_results)

    # output a file with gender decoder results merged to the right side
    output = pd.merge(left=data, right=gender_decoder_results_df, left_index=True, right_index=True)
    output.to_csv(output_file_path, index=False)
    print(f'INFO: Wrote the output file to: {output_file_path}')

def main():
    input_file_path = 'data/input/sample_job_descriptions.csv'
    output_file_path = 'data/output/sample_job_descriptions_output.csv'
    do_batch_gender_decoder(input_file_path, output_file_path, 'Job Description')

if __name__ == "__main__":
    main()
