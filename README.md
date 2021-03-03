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

### Deploy
O deploy do chatbot, é feito num AWS Lambda, com a utlilização de um container/Docker. A nossa aplicação recebe requests do webhook do facebook e depois faz um request para a API do Facebook para responder;
![](https://scontent.fcgh23-1.fna.fbcdn.net/v/t39.8562-6/64382845_2370704119653345_4919414098698960896_n.png?_nc_cat=102&ccb=3&_nc_sid=6825c5&_nc_eui2=AeGaGeFX-pksjtuKlgyURw191getXIdIojrWB61ch0iiOq-Dq04DAKbtcmGDofpqECOp6aVjENmV_wP6XyIa1u2V&_nc_ohc=ywyKBdmIIhsAX-LytVe&_nc_ht=scontent.fcgh23-1.fna&oh=bca95ff1a34a38f0e0d0a63ca250c98b&oe=6064E07B)

```
docker build -t turing-bot-v1 .
```


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
- [Julia Pocciotti | @juliapocciotti](https://github.com/juliapocciotti)
- [Luísa Heise | @luisaheise](https://github.com/luisaheise)
- [Vitoria Rodrigues | @vitoriars](https://github.com/vitoriars)
- [Noel Eliezer | @anorak](https://github.com/anorak)
- [Lucas Leme | @lucas_leme](https://github.com/lucas_leme)
