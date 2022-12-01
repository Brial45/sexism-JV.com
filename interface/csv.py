import pandas as pd
import os
def save(data : pd.DataFrame):
    with open(os.environ['CSV_FILE_PATH'], 'a') as f:
        data.to_csv(f, mode='a', header=f.tell()==0)
