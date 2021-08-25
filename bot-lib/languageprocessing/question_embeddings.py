from transformers import AutoTokenizer  
from transformers import AutoModel 
import torch
import numpy as np
import pandas as pd

class QuestionEmbeddings():
    """Class that embeds questions and holds all the frequent questions embeddings.
    """
    def __init__(self, question_path, no_answer):
        self.no_answer = no_answer
        self.tokenizer = AutoTokenizer.from_pretrained('./model', do_lower_case=False)
        self.model = AutoModel.from_pretrained('./model')
        perguntas_frequentes_int = pd.read_csv(question_path, sep = ';')
        self.perguntas_frequentes = self.get_database_embs(perguntas_frequentes_int)

    def get_database_embs(self, perguntas_frequentes):
        perguntas_frequentes['Sentence Embedding'] = perguntas_frequentes['PERGUNTAS'].apply(self.get_sentence_embs)
        perguntas_frequentes['SAUDACAO'] = perguntas_frequentes['SAUDACAO'].fillna(0).astype(int)
        return perguntas_frequentes

    def get_embs_bertinbau(self, frase):
        input_ids = self.tokenizer.encode(frase, return_tensors='pt')
        with torch.no_grad():
            outs = self.model(input_ids)
            encoded = outs[0][0, 1:-1] 
        return encoded

    def get_sentence_embs(self, frase):
        frase_embs = self.get_embs_bertinbau(frase.lower()).numpy()
        final = np.mean(frase_embs, axis=0)
        return final

    def get_perguntas_frequentes(self):
        return self.perguntas_frequentes
