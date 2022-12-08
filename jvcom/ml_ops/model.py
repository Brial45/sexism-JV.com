from jvcom.ml_ops.preprocess import preprocess , train_val_split
from jvcom.ml_ops.registry import load_hf_model,load_hf_model, load_local_model , save_model
from transformers import Trainer ,TrainingArguments
from jvcom.interface.csvFile import load_local_data
from datasets import Dataset
#Here we load the model preprocess the data and train the model save the trained one and do some


#the trainer is the model loaded with the data to train once it has been train once we can load it with data to evaluate
def make_trainer(model=None, num_train_epochs :int = 3):
    #load the huggingface model and the data to train it if we dont have any model
    if not model:
        model = load_hf_model()
        print("loading dataset")
        data = load_local_data()
        training_args = TrainingArguments("test_trainer", num_train_epochs=num_train_epochs)
        print("preprocessing data")
        data = preprocess(data)
        print("making split")
        train_dataset , eval_dataset = train_val_split(data)
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset)
        print("training model")
        trainer.train()
        print("saving_model")
        save_model(trainer)
        return trainer
    #when we want to predict with the train model

    trainer = Trainer(model=model)
    return trainer



def predict(text,trainer):
    #Load and make ther trainer for predict data
    data = [{'id': 0, 'text': text, 'type': ''}]
    data = Dataset.from_list(data)
    data = preprocess(data)
    return trainer.predict(data)
