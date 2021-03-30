from gensim.models import KeyedVectors
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 


def get_phrase_embeddings(frase, model):
    embs_words = []
    for palavra in frase.lower().split(" "):
        try:
            embs_words.append(model[palavra])
        except KeyError:
            pass
    if len(embs_words)>1:
        phrase_emb = np.mean(np.array(embs_words),axis=0)
    else:
        phrase_emb = np.array(embs_words)
    return phrase_emb

def cossine_sim(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)* np.linalg.norm(b))

model = KeyedVectors.load_word2vec_format('/home/luisa/Documents/Turing/NLP/NILC-embeddings/skip_s100.txt')

frases = ['Posso participar do grupo sendo da pós graduação?',
        'Sou da pós graduação posso participar do grupo?',
        'Sou da pós e queria participar do turing, pode?',
            'Quanto custa esta escola?',
            'Qual é a mensalidade dessa instituição de ensino?',
            'Quando abre o processo seletivo?',
            'A partir de quanto eu posso participar do processo seletivo?']

embeddings = [get_phrase_embeddings(frase, model) for frase in frases]
similarity_matrix = np.zeros((len(frases), len(frases)))

for i, frase1 in enumerate(embeddings):
    for j, frase2 in enumerate(embeddings):
        similarity_matrix[i,j] = cossine_sim(frase1,frase2)

similaridades = pd.DataFrame(similarity_matrix, index=frases, columns=frases)
plt.figure(figsize=(10,10))
plt.tight_layout()
sns.heatmap(similaridades, annot=True, vmin=0, vmax=1, cmap='hot')
plt.tight_layout()

plt.savefig("word2vec_sim.png")
