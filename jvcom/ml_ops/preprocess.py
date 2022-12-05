from ml_ops.encoder import tokenize , label
import re
import pandas as pd


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
    train_dataset = data['train'].shuffle(seed=10).select(range(5))
    eval_dataset = data['train'].shuffle(seed=10).select(range(5,7))
    return train_dataset , eval_dataset


def convert_date(date : str):
    # Converts date in scraped post from french format to Timestamp.

    dict = {
        'janvier': '01',
        'février': '02',
        'mars': '03',
        'avril': '04',
        'mai': '05',
        'juin': '06',
        'juillet': '07',
        'août': '08',
        'septembre': '09',
        'octobre': '10',
        'novembre': '11',
        'décembre': '12',
        'à': ''
        }

    pattern = re.compile(r'\b(' + '|'.join(
        re.escape(key) for key in dict.keys()) + r')\b')

    result = pattern.sub(lambda x: dict[x.group()], date)

    return pd.to_datetime(result)
