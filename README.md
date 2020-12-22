# NLP-fb-chatbot
Repositório contendo os conteúdos relativos ao projeto de chatbot do Grupo Turing.

----
## Escopo do projeto
- Responder mensagens frequentes enviadas para o Facebook do Grupo Turing
 - Responder perguntas escritas em linguagem natural e de forma não robótica, não sendo sensível a variações de léxico ou sintaxe.
 - Realizar o deploy do modelo e sua integração com o FB messager do Grupo Turing

## Abordagem
### Similaridade de documentos
Para que perguntas de mesmo conteúdo fossem respondidas da mesma maneira, foi aplicado um algorítimo para encontrar a similaridade entre duas perguntas. As perguntas serão respondidas pelas respostass registradas para as perguntas com maior similaridade dentro da base pré-definida.

### Embeddings contextuais
A similaridade entre perguntas foi calculada utilizando embeddings do modelo BERT pré-treinado em Português, o [Bertimbau](https://github.com/neuralmind-ai/portuguese-bert), disponibilizado na biblioteca `transformers` - [HuggingFace](https://huggingface.co/neuralmind/bert-base-portuguese-cased).

### References
```
@inproceedings{souza2020bertimbau,
  author    = {F{\'a}bio Souza and
               Rodrigo Nogueira and
               Roberto Lotufo},
  title     = {{BERT}imbau: pretrained {BERT} models for {B}razilian {P}ortuguese},
  booktitle = {9th Brazilian Conference on Intelligent Systems, {BRACIS}, Rio Grande do Sul, Brazil, October 20-23 (to appear)},
  year      = {2020}
}
```
----
Made with :heart: by: <br>
- [Alex Koji Misumi| @kojimisumi](https://github.com/kojimisumi)
- [Julia Pocciotti | @juliapocciotti](https://github.com/juliapocciotti)
- [Luísa Heise | @luisaheise](https://github.com/luisaheise)
- [Vitoria Rodrigues | @vitoriars](https://github.com/vitoriars)
- [William Liaw | @willfliaw](https://github.com/willfliaw)
