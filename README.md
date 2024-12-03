# Inclusivity Rating APIs

## There are 4 API endpoints
- **Single Inclusivity Rating**
- **Batch Inclusivity Rating**
- **Technical Flag**
- **Female Applicant Prediction**

![API endpoints](/images/API%20endpoints.png)

## How to start the API server locally
```
uvicorn app.main:inclusivity_rating_api --reload
```

![Start API](/images/Start%20API.png)

*--reload flag will make server reloading automatically*

## Below is an example of using one of the API endpoints

## How to query the API interactively

### The optimal way is to use Postman app

![Postman Example](/images/Postman%20example.png)

### Second way is to use internet browser
- **Note that this can be a bit laggy sometimes**

- Go to the browser
- Type ```localhost:8000/docs```

![FastAPI Swagger UI](/images/FastAPI%20-%20Swagger%20UI.png)

## Input
- Click on **Post /Single_Inclusivity_Rating**
- Click on **Try it out**
- You would see an image as follow
- Provide the job description to **job_description** in the body in JSON format
- Click **Execute** at the bottom
![Input to API](/images/Input%20to%20API.png)

## Results
Results are automatically generated with the following information:

- **Curl command** so you can copy/paste and run it in a terminal
- **Server response** with a **response body** and **response headers**
- **Response body** contains a JSON object that currently holds 2 keys: **gender_decoder_result** and **job description**
- **gender_decoder_result** currently holds 4 keys: **gender_tag**, **gendered_word_count**, **masculine words** and **feminine words**

![Results from API](/images/Results%20from%20API.png)
