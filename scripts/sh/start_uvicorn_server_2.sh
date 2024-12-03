# in case if conda activate job_ads does not work
conda run --name job_ads uvicorn app.main:gender_decoder_api --host "0.0.0.0" --port 8000