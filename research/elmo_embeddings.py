import pandas as pd
import seaborn as sns
from allennlp.modules.elmo import Elmo, batch_to_ids
import numpy as np
import matplotlib.pyplot as plt

def cossine_sim(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)* np.linalg.norm(b))

def main():
    options_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway_5.5B/elmo_2x4096_512_2048cnn_2xhighway_5.5B_options.json"
    weight_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway_5.5B/elmo_2x4096_512_2048cnn_2xhighway_5.5B_weights.hdf5"

    elmo = Elmo(options_file, weight_file, 1, dropout=0)

    frases = ['Posso participar do grupo sendo da pós graduação?',
              'Sou da pós graduação posso participar do grupo?',
               'Sou da pós e queria participar do turing, pode?',
                'Quanto custa esta escola?',
                'Qual é a mensalidade dessa instituição de ensino?',
                'Quando abre o processo seletivo?',
                'A partir de quando eu posso participar do processo seletivo?']

    frases_tokenizadas = [frase.lower().split(" ") for frase in frases]

    character_ids = batch_to_ids(frases_tokenizadas)

    embeddings = elmo(character_ids)

    embs = np.array([emb.detach().numpy() for emb in embeddings['elmo_representations']])
    embs = embs[0]
    embs[embs == 0] = np.nan
    means = np.nanmean(embs, axis=1)

    similarity_matrix = np.zeros((len(frases), len(frases)))

    for i, frase1 in enumerate(means):
        for j, frase2 in enumerate(means):
            similarity_matrix[i,j] = cossine_sim(frase1,frase2)

    similaridades = pd.DataFrame(similarity_matrix, index=frases, columns=frases)
    plt.figure(figsize=(10,10))
    sns.heatmap(similaridades, annot=True, vmin=0, vmax=1, cmap='hot')
    plt.tight_layout()
    plt.savefig("elmo_sim.png")

    return embs



if __name__ == '__main__':
    main()