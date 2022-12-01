from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from main import pred

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?tweet=
@app.get("/predict")
def predict(tweet: str):

    X_pred = pd.DataFrame({'text': tweet})
    y_pred = pred(X_pred)

    return dict({'type': int(y_pred[0][0])})


@app.get("/")
def root():
    return {'greeting': 'Hello'}
