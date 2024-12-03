These tests are applicable for containers built for aws lamba. To build and test the container locally:

Build the container:
docker build -t inclusive_recruiting_lambda . -f Dockerfile.lambda

Run the container:
docker run -p 8000:8080 inclusive_recruiting_lambda:latest

To test the endpoints, see the example text files for individual curl commands
