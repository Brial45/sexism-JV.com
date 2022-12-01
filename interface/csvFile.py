import pandas as pd
import os
from datasets import load_dataset

def save(data : pd.DataFrame,
         file_name : str):
    with open(f"{os.environ['CSV_FILE_PATH']}/{file_name}", 'a') as f:
        data.to_csv(f, mode='a', header=f.tell()==0)



def load_file(file_name : str):
    return load_dataset(f'../raw_data/{file_name}')
