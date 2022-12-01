from transformers import AutoModelForSequenceClassification
import os


def load_model():
#load model online only if there is no model on the architecture
#else load the model locally
    if os.path.isfile("model/"):
        model = AutoModelForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=2)
    else:
        model = AutoModelForSequenceClassification.from_pretrained("model/", num_labels=2)
    return model


def save_model(trainer):
    trainer.save_model(f'model/')
