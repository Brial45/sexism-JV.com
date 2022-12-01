from transformers import AutoTokenizer

def load_tokenizer():
    #Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-cased')
    return tokenizer

def label(data):
    #get the data and create the label columns for the model
    label = label['type']

    return {'labels': label}

def tokenize(data):
    #receive the data and tokenize our text return 3 different column
    tokenizer = load_tokenizer()
    return tokenizer(data['text'], padding='max_length')