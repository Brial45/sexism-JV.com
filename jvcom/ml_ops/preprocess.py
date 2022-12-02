from jvcom.ml_ops.encoder import tokenize , label


def preprocess(data):
    #get the data and preprocess it by throwing it into the encoder


    data = data.map(tokenize, batched=True)

    # !!!!!! il faut changer le nom des colonnes a removes
    # pour coller a nos data !!!!
    remove_columns = ['id', 'text', 'type']

    data = data.map(label, remove_columns=remove_columns)

    return data

def train_val_split(data):
    #train_dataset = data['train'].shuffle(seed=10).select(range(6875))
    #eval_dataset = data['train'].shuffle(seed=10).select(range(6875,8593))
    train_dataset = data['train'].select(range(10))
    eval_dataset = data['train'].select(range(10,20))
    return train_dataset , eval_dataset
