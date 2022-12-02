import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


def connection():
    credentials = service_account.Credentials.from_service_account_file('../.keys/sexism-jv-forum-7c9b63f34ed4.json')

    project_id = 'sexism-jv-forum'
    return  bigquery.Client(credentials= credentials,project=project_id)

#query_job = client.query("""
#   SELECT *
#   FROM dataset.my_table
#  LIMIT 1000 """)

def save_data(data ,
              is_first: bool):

    client = connection()

    table = "SexismJvForum"
    table = f"{'sexism-jv-forum'}.{table}.data_test_monthly"

    # define write mode and schema
    write_mode = "WRITE_TRUNCATE" if is_first else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    print(f"\n{'Write' if is_first else 'Append'} {table} ({data.shape[0]} rows)")

    # save data on bq
    job = client.load_table_from_dataframe(data, table, job_config=job_config)
    return job.result()  # wait for the job to complete

def load_data_from_cloud(table_name : str):

    client = connection()
    dataset_ref = bigquery.DatasetReference("sexism-jv-forum", "SexismJvForum")
    table_ref = dataset_ref.table(table_name)
    table = client.get_table(table_ref)

    return client.list_rows(table).to_dataframe()



if __name__ == '__main__':
    print(load_data_from_cloud("data_test_monthly"))
