#!/bin/bash
DEPLOY_URL=154769901104.dkr.ecr.sa-east-1.amazonaws.com
REPO_NAME=turing/ada
API_FUNCTION=turing-ada-api
APP_FUNCTION=turing-ada-app

# update api
zip $API_FUNCTION.zip api.py
aws lambda update-function-code --function-name $API_FUNCTION --zip-file fileb://$API_FUNCTION.zip
rm $API_FUNCTION.zip

# update main app
sudo docker build . -t $REPO_NAME -q
aws ecr get-login-password --region sa-east-1 | sudo docker login --username AWS --password-stdin $DEPLOY_URL
sudo docker tag $REPO_NAME:latest $DEPLOY_URL/$REPO_NAME:latest
sudo docker push $DEPLOY_URL/$REPO_NAME:latest -q
aws lambda update-function-code --function-name $APP_FUNCTION --image-uri $DEPLOY_URL/$REPO_NAME:latest
