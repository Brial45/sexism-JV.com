from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jvcom.ml_ops.model import predict , make_trainer
from jvcom.ml_ops.registry import load_local_model
from google.cloud import storage
import os
from zipfile import ZipFile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load model.zip from Google Storage

client = storage.Client()
bucket = client.bucket(os.environ.get('BUCKET_NAME'))
blob = bucket.blob("model/" + f"model.zip")
blob.download_to_filename(f"model.zip")
print(blob)

with ZipFile("model.zip", 'r') as zObject:

    # Extracting all the members of the zip into a specific location.
    zObject.extractall(path="model/")

TRAINER = make_trainer(load_local_model())

# http://0.0.0.0:8000/pred?text=
@app.get("/pred")
def pred(text: str):

    y_pred = predict(text,TRAINER).predictions[0]
    response = {'proba': y_pred.tolist(),
                'type': y_pred.tolist().index(max(y_pred.tolist()))}
    print(response)
    return response


@app.get("/")
def root():
    return {'greeting': 'Hello'}
