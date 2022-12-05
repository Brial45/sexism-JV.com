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

# http://127.0.0.1:8000/predict?text=
@app.get("/pred")
def pred(text: str):

    y_pred = predict(text).predictions[0]
    response = {'proba': y_pred.tolist(),
                'type': y_pred.tolist().index(max(y_pred.tolist()))}
    print(response)
    return response


@app.get("/")
def root():
    return {'greeting': 'Hello'}
