import numpy as np

class Chatbot():
    """Class that generate ADA's answer considering set of frequent questions. 
    """
    def __init__(self, question_embeddings, similarity_threshold=0.8):
        self.similarity_threshold = similarity_threshold
        self.question_embeddings = question_embeddings
    
    def semelhanca_cossenos(self, a,b):
        return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
    
    def get_most_similar_phrase(self, frase):
        mais_similar = ""
        maior_score_similaridade = -999

        sentence_emb = self.question_embeddings.get_sentence_embs(frase)
        perguntas_frequentes_emb = self.question_embeddings.get_perguntas_frequentes()
        for i, row in perguntas_frequentes_emb.iterrows():
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
