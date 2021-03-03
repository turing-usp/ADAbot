FROM python:3.8

WORKDIR "/lambda_function"

COPY requirements.txt requirements.txt

RUN ["pip", "install", "-r", "requirements.txt", "--no-cache-dir"]

#instances wanted model so it is cached for docker runs

COPY aux/download_nlp_assets.py aux/download_nlp_assets.py

RUN ["python", "aux/download_nlp_assets.py"]

COPY . .