from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jvcom.ml_ops.model import predict
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?tweet=
@app.get("/pred")
def pred(tweet: str):

    y_pred = predict(tweet).predictions[0]
    print(y_pred)
    return y_pred.tolist()


@app.get("/")
def root():
    return {'greeting': 'Hello'}
