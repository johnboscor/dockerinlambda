import uuid
import uvicorn

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
import os
from mangum import Mangum

from app.single_inclusivity_rating import create_gender_tag
from app.batch_inclusivity_rating import do_batch_inclusivity_rating
from app.female_applicant_prediction import predict_female_applicants_pct
from app.technical_flag import create_tech_flags

from app.monitoring import logging_config
from app.middlewares.correlation_id_middleware import CorrelationIdMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.handlers.exception_handler import exception_handler
from app.handlers.http_exception_handler import http_exception_handler

###############################################################################
#   Application object for the API                                                #
###############################################################################

inclusivity_rating_api = FastAPI(title="Equitable Postings Tool",
                                docs_url='/docs',
                                redoc_url="/redoc",
                                openapi_url='/openapi.json')


###############################################################################
#   Logging configuration                                                     #
###############################################################################

logging_config.configure_logging(level='DEBUG', service='Helloworld', instance=str(uuid.uuid4()))

###############################################################################
#   Error handlers configuration                                              #
###############################################################################

inclusivity_rating_api.add_exception_handler(Exception, exception_handler)
inclusivity_rating_api.add_exception_handler(HTTPException, http_exception_handler)

###############################################################################
#   Middlewares configuration                                                 #
###############################################################################

# Tip : middleware order : CorrelationIdMiddleware > LoggingMiddleware -> reverse order
inclusivity_rating_api.add_middleware(LoggingMiddleware)
inclusivity_rating_api.add_middleware(CorrelationIdMiddleware)



class JobDescription(BaseModel):
    job_description: str

@inclusivity_rating_api.get("/")
async def welcome_page():
      return {"message": "Equitable Postings Tool"}

@inclusivity_rating_api.get(path="/gettest")
async def gettest():
        return {"message": "Get Test Works!"}

@inclusivity_rating_api.post(path="/single_inclusivity_rating", response_class=JSONResponse)
async def single_inclusivity_rating(job_description: JobDescription):
    """
    Example of how to call this API

    curl --request POST 'http://localhost:8000/single_inclusivity_rating' \
        --location \
        --header 'Accept: application/json' \
        --header 'Content-Type: application/json' \
        --data '{
        "job_description": "put your job description here"
        }'

    Args:\n
        job_description (JobDescription): job description as string\n

    Returns:\n
        JSON: {
            "gender_decoder_result": {
                "gender_tag": "Netural",
                "gender_word_count": {
                    "male": 0,
                    "female": 0
                    },
                "masculine_words": [],
                "feminine_words": []
            }
    """
    result = create_gender_tag(job_description.job_description)
    return {'gender_decoder_result': result}


@inclusivity_rating_api.post(path="/batch_inclusivity_rating", response_class=FileResponse)
async def batch_inclusivity_rating(
    input_file: UploadFile = File(...),
    job_description_col: str = Form(...)
    ):
    """
    Example of how to call this API

    curl --request POST 'http://localhost:8000/batch_inclusivity_rating' \
        --location \
        --header 'accept: */*' \
        --form 'input_file=@"data/input/sample_job_descriptions.csv"' \
        --form 'job_description_col="Job Description"'

    Args:\n
        input_file (UploadFile): input_file to be uploaded. Must include a job_description column.\n
        job_description_col (str): the job description column name\n

    Returns:\n
        FILE: input_file with 4 extra output columns: gender_tag, gender_word_count, masculine_words, and feminine_words.
    """
    # upload the input_file
    contents = await input_file.read()

    # write the content of the uploaded input_file and save as a temp input_file
    temp_file = NamedTemporaryFile('wb', delete=False)
    f = None
    try:
        with temp_file as f:
            f.write(contents)
        # now the temp input_file can be re-opened as many times as needed
        # get input and output file path
        input_file_path = temp_file.name
        output_file_path = f'/tmp/sample_batch_gender_decoder_output.csv'

        # do batch processing for multiple job descriptions
        do_batch_inclusivity_rating(
            input_file_path=input_file_path,
            output_file_path=output_file_path,
            job_description_col=f'{job_description_col}'
        )

    finally:
        if f is not None:
            f.close()
        os.unlink(temp_file.name)

    return FileResponse(output_file_path)


@inclusivity_rating_api.post(path="/technical_flag", response_class=FileResponse)
async def technical_flag(
    input_file: UploadFile = File(...),
    job_title_col_name: str = Form(...),
    job_description_col_name: str = Form(...)
    ):
    """
    Example of how to call this API

    curl -X 'POST' \
        'http://localhost:8000/technical_flag' \
        -H 'accept: */*' \
        -H 'Content-Type: multipart/form-data' \
        -F 'input_file=@data/input/sample_job_descriptions.csv;type=text/csv' \
        -F 'job_title_col_name="Job Title"' \
        -F 'job_description_col_name="Job Description"'

    Args:\n
        input_file (UploadFile): input_file to be uploaded. Must include columns: Job Title, Job Description.\n
        job_title_col_name (str): job title column name\n
        job_description_col_name (str): job description column name\n

    Returns:\n
        FILE: input_file with 1 extra column: Tech_Flag
    """
    # Upload the input file
    contents = await input_file.read()

    # write the content of the uploaded input_file and save as a temp input file
    temp_file = NamedTemporaryFile('wb', delete=False)
    f = None
    try:
        with temp_file as f:
            f.write(contents)
        # now the temp input_file can be re-opened as many times as needed
        # get input and output file path
        input_file_path = temp_file.name
        output_file_path = f'/tmp/sample_technical_flag_output.csv'

        # process the input file
        create_tech_flags(
            input_file_path=input_file_path,
            output_file_path=output_file_path,
            job_title_col_name=job_title_col_name,
            job_description_col_name=job_description_col_name
        )
    finally:
        if f is not None:
            f.close()
        os.unlink(temp_file.name)

    return FileResponse(output_file_path)


@inclusivity_rating_api.post(path="/female_applicant_prediction", response_class=FileResponse)
async def female_applicant_prediction(
    input_file: UploadFile = File(...),
    job_title_col_name: str = Form(...),
    tech_col_name: str = Form(...),
    gender_tag_col_name: str = Form(...)
    ):
    """
    Example of how to call this API

    curl -X 'POST' \
        'http://localhost:8000/female_applicant_prediction' \
        -H 'accept: */*' \
        -H 'Content-Type: multipart/form-data' \
        -F 'input_file=@data/input/sample_female_applicant_prediction_input.csv;type=text/csv' \
        -F 'job_title_col_name="External Job Title"' \
        -F 'tech_col_name=Tech' \
        -F 'gender_tag_col_name="Gender Tag"'

    Args:\n
        input_file (UploadFile): input_file to be uploaded. Must include columns: Job Title, Tech, Gender Tag.\n
        job_title_col_name (str): job title column name\n
        tech_col_name (str): tech column name\n
        gender_tag_col_name (str): gender tag column name\n

    Returns:\n
        FILE: input_file with 1 extra column: female_applicant_prediction
    """
    # Upload the input file
    contents = await input_file.read()

    # write the content of the uploaded input_file and save as a temp input file
    temp_file = NamedTemporaryFile('wb', delete=False)
    f = None
    try:
        with temp_file as f:
            f.write(contents)
        # now the temp input_file can be re-opened as many times as needed
        # get input and output file path
        input_file_path = temp_file.name
        output_file_path = f'/tmp/sample_female_applicant_prediction_output.csv'

        # process the input file
        predict_female_applicants_pct(
            input_file_path=input_file_path,
            job_title_col_name=job_title_col_name,
            tech_col_name=tech_col_name,
            gender_tag_col_name=gender_tag_col_name,
            output_file_path=output_file_path
        )
    finally:
        if f is not None:
            f.close()
        os.unlink(temp_file.name)

    return FileResponse(output_file_path)


###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(inclusivity_rating_api)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(inclusivity_rating_api, host="0.0.0.0", port=5000)
