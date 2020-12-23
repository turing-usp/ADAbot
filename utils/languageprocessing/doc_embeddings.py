from transformers import AutoTokenizer  
from transformers import AutoModel 
import torch
import numpy as np
import pandas as pd
import nltk
from nltk import word_tokenize

class QuestionEmbeddings():
    def __init__(self, question_path, greeting, no_answer, similarity_threshold=0.69, count_stops=False, media=True):
        self.no_answer = no_answer
        self.similarity_threshold = similarity_threshold
        self.greeting = greeting
        self.count_stops = count_stops
        self.media = media
        self.tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=False)
        self.model = AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
        perguntas_frequentes_int = pd.read_excel(question_path)
        self.perguntas_frequentes = self.get_database_embs(perguntas_frequentes_int)

    def get_database_embs(self, perguntas_frequentes):
        embs = []
        for i, row in perguntas_frequentes.iterrows():
            emb = self.get_sentence_embs(row['PERGUNTAS'])
            embs.append(emb)
        perguntas_frequentes['Sentence Embedding'] = embs
        return perguntas_frequentes

    def get_embs_bertinbau(self, frase):
        input_ids = self.tokenizer.encode(frase, return_tensors='pt')
        with torch.no_grad():
            outs = self.model(input_ids)
            encoded = outs[0][0, 1:-1] 
        return encoded

    def get_sentence_embs(self, frase):
        frase_embs = self.get_embs_bertinbau(frase.lower()).numpy()
        frase_embs_considerados = []
        palavras = word_tokenize(frase.lower())
        for palavra, embedding in zip(palavras, frase_embs):
            if not(self.count_stops):
                if not(palavra in self.stopwords):
                    frase_embs_considerados.append(embedding)
            else:
                frase_embs_considerados.append(embedding)
        frase_embs_considerados = np.array(frase_embs_considerados)
        if self.media:
            final = np.mean(frase_embs_considerados, axis=0)
        else:
            final = np.sum(frase_embs_considerados, axis=0)
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
        return mais_similar, maior_score_similaridade
    
    def get_response(self, frase):
        question, similaridade = self.get_most_similar_phrase(frase)
        anwser = self.perguntas_frequentes[self.perguntas_frequentes['PERGUNTAS']  ==  question]['RESPOSTAS'].values[0]
        print(f"Pergunta mais similar na base de dados: \n{question}\nsimilaridade = {similaridade*100}%")
        if similaridade < self.similarity_threshold:
            anwser = self.no_answer
        full_answer = self.greeting + "\n" + anwser
        return full_answer
