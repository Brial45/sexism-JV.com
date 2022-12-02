from ml_ops.preprocess import preprocess , train_val_test_split
from ml_ops.registry import load_model , save_model
from transformers import Trainer ,TrainingArguments
from interface.csvFile import load_file
#Here we load the model preprocess the data and train the model save the trained one and do some


#the trainer is the model loaded with the data to train once it has been train once we can load it with data to evaluate
def make_trainer( num_train_epochs :int = 5):
    #load the mode and the data
    model = load_model()
    data = load_file()

    training_args = TrainingArguments("test_trainer", num_train_epochs=num_train_epochs)


    data = preprocess(data)
    train_dataset , eval_dataset, test_dataset = train_val_test_split(data)


    trainer = Trainer(
    model=model, args=training_args, train_dataset=train_dataset, eval_dataset=eval_dataset
    )

    return trainer, train_dataset , eval_dataset, test_dataset

def train_model(trainer):
    trainer.train()


def load_save_train_model():

    #load the model and load the trainer
    print("load the model")
    trainer = make_trainer

    #train the model
    print("train the model")
    train_model(trainer)

    #save the model
    print("save model ")
    save_model(trainer)

def predict(dataset):
    trainer, train_dataset , eval_dataset, test_dataset = make_trainer()
    pred = trainer.predict(test_dataset)
    return pred

'''if __name__ == '__main__':
    print("blabla")
    load_save_train_model()
'''
