docker run -it --rm \
	-v $PWD/app:/usr/local/job_ads/app/ \
	-v $PWD/data:/usr/local/job_ads/data/ \
	-v $PWD/scripts:/usr/local/job_ads/scripts/ \
	-v $PWD/.vscode:/usr/local/job_ads/.vscode \
	-p 80:8000 \
	kevin_tran_inclusive_job_ads bash
