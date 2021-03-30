
from transformers import AutoTokenizer  
from transformers import AutoModel 
import torch
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def cossine_sim(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)* np.linalg.norm(b))

def get_embs_bertinbau(frase):
    input_ids = tokenizer.encode(frase, return_tensors='pt')
    with torch.no_grad():
        outs = model(input_ids)
        encoded = outs[0][0, 1:-1] 
    return encoded

def get_sentence_embs(frase):
    frase_embs = get_embs_bertinbau(frase.lower()).numpy()
    final = np.mean(frase_embs, axis=0)
    return final

tokenizer = AutoTokenizer.from_pretrained('../bot-lib/model', do_lower_case=False)
model = AutoModel.from_pretrained('../bot-lib/model')

frases = ['Posso participar do grupo sendo da pós graduação?',
              'Sou da pós graduação posso participar do grupo?',
               'Sou da pós e queria participar do turing, pode?',
                'Quanto custa esta escola?',
                'Qual é a mensalidade dessa instituição de ensino?',
                'Quando abre o processo seletivo?',
                'A partir de quando eu posso participar do processo seletivo?']

embeddings = [get_sentence_embs(frase) for frase in frases]

similarity_matrix = np.zeros((len(frases), len(frases)))

for i, frase1 in enumerate(embeddings):
    for j, frase2 in enumerate(embeddings):
        similarity_matrix[i,j] = cossine_sim(frase1,frase2)

similaridades = pd.DataFrame(similarity_matrix, index=frases, columns=frases)
plt.figure(figsize=(10,10))
sns.heatmap(similaridades, annot=True, vmin=0, vmax=1, cmap='hot')
plt.tight_layout()
plt.savefig("bert_sim.png")