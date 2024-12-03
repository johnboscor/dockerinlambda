# Steps to deploy the entire stack into an AWS account with SAM CLI

## Prerequisites
- **Make sure you have aws and sam cli's installed**
- **Make sure you have admin access(to deploy all resources) to the aws account**
- **Clone this repository and change directory into it**

## Deployment with default parameters:
- **Environment**: 'dev'
- **API Token**: <Use the API token from api gateway>

- **Issue the following set of commands:**
    - sam build
    - sam deploy --resolve-image-repos
      ```
      This will go ahead and start creating the resources using cloudformation stacks.
      SAM will also take of building the docker iamge for the lambda function and upload the image 
      to ECR. Once the build is done(you may have to press 'y' when it asks you to confirm the resources),
      the functional URL(to access the docs page) and the API gateway URL(which is the actual rest API) 
      will be printed as output. You can use them with curl (sample curl commands listed below) along with 
      authorizationToken header to access the APIs. Or you could use postman app to access them.
      Example output:
      -------------------------------------------------
        Outputs                                                                                                                                              
      ----------------------------------------------------
        Key                 EPToolApi                                                                                                                        
        Description         API Gateway endpoint URL                                                                                                         
        Value               https://he7j5altn4.execute-api.us-east-1.amazonaws.com/dev/                                                                      

        Key                 EPToolFunction                                                                                                                   
        Description         EP Tool Lambda Function ARN                                                                                                      
        Value               arn:aws:lambda:us-east-1:497031296963:function:ept-EPToolFunction-3IQmC2T98oEM                                                   

        Key                 EPToolFunctionUrlEndpoint                                                                                                        
        Description         Functional docs URL(for internal use only)                                                                                       
        Value               https://k64oug4snkj2scze7yoiwtfwou0thzyq.lambda-url.us-east-1.on.aws/docs                                                        
      ------------------------------------------

      ```
    - sam delete (if you want to destroy the stack and delete all the resources from AWS)

## Deployment with input parameters:
    You can override the enviroment(stage) and apitoken value by using the following parameters in 
    the deploy command:

    - sam deploy --resolve-image-repos --parameter-overrides DeployStage=dev SecretToken=mysecrettoken
    
    The above command will deploy the stack in dev stage and use the specified API token for 
    authentication
    

## Sample curl commands to test the APIs
```
The command assumes that the files needed for the form data is present in the data/input folder
```
    1. single_inclusivity_rating

    curl --location 'https://he7j5altn4.execute-api.us-east-1.amazonaws.com/dev/single_inclusivity_rating' \
    --header 'authorizationToken: <API token value>' \
    --header 'Content-Type: application/json' \
    --data '{
    "job_description": "Company is a purpose-driven consulting firm that helps companies solve business problems and build for the future, with solutions spanning business advisory, customer experience, technology and analytics. We partnet with companies to push the buoundaries of what'\''s possible together. Founded in 2001 and headquartered in Seattle, WA, Company has organically grown to nearly 6,000 employess. We were names one of Fortune'\''s 100 best companies to work for in 2018 and are regularly recognized by our employees as a best place to work."
    }'

    2. batch_inclusivity_rating

    curl --location 'https://he7j5altn4.execute-api.us-east-1.amazonaws.com/dev/batch_inclusivity_rating' \
    --header 'authorizationToken: <api token>' \
    --form 'input_file=@"/Users/john.br/inclusive-recruiting-john/data/input/sample_job_descriptions.csv"' \
    --form 'job_description_col="Job Description"'

    3. female_applicant_prediction

    curl --location 'https://he7j5altn4.execute-api.us-east-1.amazonaws.com/dev/female_applicant_prediction' \
    --header 'authorizationToken: API token value' \
    --form 'job_title_col_name="External Job Title"' \
    --form 'tech_col_name="Tech"' \
    --form 'gender_tag_col_name="Gender Tag"' \
    --form 'input_file=@"/Users/john.br/inclusive-recruiting-john/data/input/sample_female_applicant_pred_small.csv"'

    4. technical_flag

    curl --location 'https://he7j5altn4.execute-api.us-east-1.amazonaws.com/dev/technical_flag' \
    --header 'authorizationToken: API token value' \
    --form 'job_title_col_name="Job Title"' \
    --form 'job_description_col_name="Job Description"' \
    --form 'input_file=@"/Users/john.br/inclusive-recruiting-john/data/input/sample_job_descriptions.csv"'
