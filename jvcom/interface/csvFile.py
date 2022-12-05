import pandas as pd
import os
from datasets import load_dataset


def save(data : pd.DataFrame,
         file_name : str):
    with open(f"{os.environ['CSV_FILE_PATH']}/{file_name}", 'a') as f:
        data.to_csv(f, mode='a', header=f.tell()==0)


def load_local_data():
    return load_dataset(f'jvcom/data')
