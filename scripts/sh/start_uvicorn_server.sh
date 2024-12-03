# turn on the API inside docker with uvicorn
# conda activate job_ads
uvicorn app.main:gender_decoder_api --host "0.0.0.0" --port 8000
