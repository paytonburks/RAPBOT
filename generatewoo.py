from transformers import pipeline

generator1 = pipeline('text-generation', model="gpt2")
res = generator1("I can't believe you did such a ", do_sample=False)
print(res)

generator = pipeline('text-generation', model='./thug-bertweet-output', tokenizer='vinai/bertweet-base')
res = generator('I push p ', do_sample=False)
print(res)