from transformers import AutoModelForSequenceClassification


def load_hf_model():
    #Load model from Huggingface
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=2)
    return model

def load_local_model():
#else load the model locally
    model = AutoModelForSequenceClassification.from_pretrained("model/", local_files_only=True)
    return model

#used only once when we want to download train and save the model
def save_model(trainer):
    trainer.save_model(f'model/')
