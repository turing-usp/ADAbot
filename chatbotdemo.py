from utils.languageprocessing import doc_embeddings as de
from transformers import AutoTokenizer  
from transformers import AutoModel 
import torch
import numpy as np
import pandas as pd
import nltk
from nltk import word_tokenize
import os

def main():
    # https://drive.google.com/file/d/1d7zI16_UnKQIpTIr_hcg-p6P_5mziA_n/view?usp=sharing
    FILENAME = "q_and_a.xlsx"
    #os.system(f"wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1d7zI16_UnKQIpTIr_hcg-p6P_5mziA_n' -O {FILENAME}") 

    qe = de.QuestionEmbeddings(question_path=FILENAME, greeting="Olá, tudo bem?", no_answer="Em breve, alguns dos nossos membros te responderá!")

    while True:
        question = input("Faça uma pergunta: \n")
        ans = qe.get_response(question)
        print(ans)

if __name__ == '__main__':
    main()