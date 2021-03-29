from transformers import AutoTokenizer  
from transformers import AutoModel 
import torch
import numpy as np
import pandas as pd

class QuestionEmbeddings():
    def __init__(self, question_path, no_answer, similarity_threshold=0.8):
        self.no_answer = no_answer
        self.similarity_threshold = similarity_threshold
        self.tokenizer = AutoTokenizer.from_pretrained('./model', do_lower_case=False)
        self.model = AutoModel.from_pretrained('./model')
        perguntas_frequentes_int = pd.read_csv(question_path)
        self.perguntas_frequentes = self.get_database_embs(perguntas_frequentes_int)

    def get_database_embs(self, perguntas_frequentes):
        perguntas_frequentes['Sentence Embedding'] = perguntas_frequentes['PERGUNTAS'].apply(self.get_sentence_embs)
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
    
    def semelhanca_cossenos(self, a,b):
        return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
    
    def get_most_similar_phrase(self, frase):
        mais_similar = ""
        maior_score_similaridade = -999

        sentence_emb = self.get_sentence_embs(frase)
        for i, row in self.perguntas_frequentes.iterrows():
            similaridade = self.semelhanca_cossenos(sentence_emb,row['Sentence Embedding'])
            if similaridade > maior_score_similaridade:
                maior_score_similaridade = similaridade
                mais_similar = row['PERGUNTAS']
                is_greeting = row['SAUDACAO']
                answer = row['RESPOSTAS']
        return mais_similar, maior_score_similaridade, answer, is_greeting
    
    def get_response(self, frase):
        found_answer = True
        question, similaridade, anwser, is_greeting = self.get_most_similar_phrase(frase)
        is_greeting = bool(is_greeting)
        print(f"mensagem: {frase} \nPergunta mais similar na base de dados: \n{question}\nsimilaridade = {similaridade*100}%")
        if similaridade < self.similarity_threshold:
            anwser = self.no_answer
            found_answer = False
            is_greeting = False
        return anwser, found_answer, is_greeting
