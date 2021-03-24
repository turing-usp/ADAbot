#!/bin/bash
DEPLOY_URL="035554315566.dkr.ecr.sa-east-1.amazonaws.com"
docker build . -t turing-chatbot-nlp -q
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin $DEPLOY_URL
docker tag turing-chatbot-nlp:latest $DEPLOY_URL/turing-chatbot-nlp:latest
docker push $DEPLOY_URL/turing-chatbot-nlp:latest -q
# latest: digest: sha256:e9d84c9810f1c0f2fe3234c02476b57e6b23290d4f3f81810430327930261d04 size: 2420
# aws lambda update-function-code --function-name turing-chatbot-nlp --image-uri $DEPLOY_URL/turing-chatbot-nlp:latest