import pandas as pd
from tqdm import tqdm


def predict_female_applicants_pct(
    input_file_path,
    job_title_col_name,
    tech_col_name,
    gender_tag_col_name,
    output_file_path,
    reference_data_path='data/input/female_applicant_prediction_reference_data.csv'
    ):
    """
    Make female applicants percentage predictions 
    by looking up to a reference data with the combo keys (Job Title, Tech and Gender Tag)
    Input file must contain the following columns: Job Title, Tech, and Gender Tag.

    Args:
        input_file_path (directory): input file path
        job_title_col_name (str): job title column name
        tech_col_name (str): tech column name
        gender_tag_col_name (str): gender tag column name
        output_file_path (directory): output file path
        reference_data_path (directory, optional): reference data path. 
            Defaults to 'data/input/female_applicant_prediction_reference_data.csv'.

    Returns:
        Action: Wrote a output CSV file to output_file_path
        Return (pd.DataFrame): Output data
    """

    # Read in both the reference and input data
    reference = pd.read_csv(reference_data_path)
    input_data = pd.read_csv(input_file_path)

    # Create a female_applicant_prediction column
    input_data['female_applicant_prediction']=''

    # Loop through each row of the input_data
    # look up reference_data using the keys (Job Title, Tech and Gender Tag) to get female_applicant_predictions
    for index, row_data in tqdm(input_data.iterrows(), total=input_data.shape[0]):
        try: # add a very simple error catching
            if (row_data[job_title_col_name] not in reference['Job Title']) and row_data[tech_col_name]==1:
                [prediction1] = reference[(reference['Job Title']=="Other Technical") & (reference['Gender Tag']==row_data[gender_tag_col_name])]['Estimated Percent Female Applicants']
                input_data.loc[index ,"female_applicant_prediction"]=prediction1
                
            elif (row_data[job_title_col_name] not in reference['Job Title']) and row_data[tech_col_name]==0:
                [prediction2] = reference[(reference['Job Title']=="Non-Technical") & (reference['Gender Tag']==row_data[gender_tag_col_name])]['Estimated Percent Female Applicants']
                input_data.loc[index ,"female_applicant_prediction"]=prediction2
                
            else:
                [prediction3] = reference[(reference['Job Title']== row_data[job_title_col_name]) & (reference['Gender Tag']==row_data[gender_tag_col_name]) & (reference[tech_col_name]==1)]['Estimated Percent Female Applicants']
                input_data.loc[index ,"female_applicant_prediction"]=prediction3
        except:
            input_data.loc[index ,"female_applicant_prediction"]=''
            
    output_data = input_data
    output_data.to_csv(output_file_path, index=False)
    print(f'INFO: Wrote the output file to: {output_file_path}')

    return output_data

def main():
    input_file_path = 'data/input/sample_female_applicant_prediction_input.csv'
    job_title_col_name = 'External Job Title'
    tech_col_name = 'Tech'
    gender_tag_col_name = 'Gender Tag'
    output_file_path = 'data/output/sample_female_applicant_prediction_output.csv'

    predict_female_applicants_pct(
        input_file_path=input_file_path,
        job_title_col_name=job_title_col_name,
        tech_col_name=tech_col_name,
        gender_tag_col_name=gender_tag_col_name,
        output_file_path=output_file_path
    )

if __name__ == "__main__":
    main()
