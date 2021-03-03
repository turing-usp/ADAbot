from transformers import AutoTokenizer, AutoModel

# downloads everything on docker build time

AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=False)
AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')
