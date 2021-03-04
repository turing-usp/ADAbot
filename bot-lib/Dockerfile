FROM public.ecr.aws/lambda/python:3.8

WORKDIR /var/task

COPY requirements.txt requirements.txt

RUN ["pip", "install", "-r", "requirements.txt", "--no-cache-dir"]

#instances wanted model so it is cached for docker runs

COPY . .

CMD ["app.lambda_handler"]
 
