import requests
import os
import json
import pandas as pd
import re
import numpy as np

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url(start_index:int, stop_index:int):
    tweet_fields = ""
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    annotated_tweets_df = pd.read_csv('https://raw.githubusercontent.com/patriChiril/An-Annotated-Corpus-for-Sexism-Detection-in-French-Tweets/master/corpus_SexistContent.csv', sep="\t", header=None, names=['id', 'type'])
    ids_as_list = list(annotated_tweets_df.id)[start_index:stop_index]
    ids_as_string = ','.join(list(map(str, ids_as_list)))
    ids = f"ids={ids_as_string}"
    # You can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response


def main():
    annotated_tweets_df = pd.read_csv(
        'https://raw.githubusercontent.com/patriChiril/An-Annotated-Corpus-for-Sexism-Detection-in-French-Tweets/master/corpus_SexistContent.csv',
        sep="\t", header=0, names=['id', 'type'])
    step=100
    iterations = np.arange(0,len(annotated_tweets_df)/step, dtype=int)
    #iterations_test = np.arange(16,17)
    tweets_df = pd.DataFrame()

    for i in iterations:
        print(f"---Iteration #{i}---")
        url = create_url(i*step,i*step+step)
        response = connect_to_endpoint(url)
        response_df = pd.DataFrame(response.json()['data'])
        print(f"Number of tweets collected: {len(response_df)}")
        if 'withheld' in response_df:
            response_df = response_df[response_df['withheld'].isna()]
            response_df = response_df.drop(columns='withheld')
        print(response_df)
        if response.status_code != 200:
            break
        tweets_df = pd.concat([tweets_df, response_df], axis=0)

    tweets_df['text'] =  tweets_df['text'].apply(
                    lambda x: ' '.join(re.sub("(\w+:\/\/\S+)", " ", x).split()))
    annotated_tweets_df['id'] = annotated_tweets_df['id'].astype(str)
    annotated_tweets_df = annotated_tweets_df.drop_duplicates('id')
    annotated_tweets_df = annotated_tweets_df.set_index('id')
    tweets_df = tweets_df.drop_duplicates('id')
    tweets_df = tweets_df.set_index('id')
    concat_tweets_df = pd.concat([tweets_df, annotated_tweets_df], axis=1)
    concat_tweets_df = concat_tweets_df.drop(columns='edit_history_tweet_ids')
    concat_tweets_df = concat_tweets_df.dropna()
    concat_tweets_df['type'] = concat_tweets_df['type'].astype(int)
    #pd.set_option('display.max_rows', None)
    #print(concat_tweets_df)
    concat_tweets_df.to_csv('raw_data/corpus_SexistContent_with_text.csv', mode='w')

if __name__ == "__main__":
    main()
