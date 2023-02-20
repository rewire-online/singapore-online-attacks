import torch
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
from transformers import AutoTokenizer, TrainingArguments
from transformers import AutoModelForSequenceClassification, Trainer
import numpy as np
import pandas as pd
import json
from datasets import Dataset
from torch import nn
from transformers import EarlyStoppingCallback
from torch import from_numpy
import os
import argparse

pd.set_option('display.max_columns', None)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(torch.cuda.get_device_name(0))

PREPROC_DIR = "."
TOKENIZER_MAX = 256
RESUME_FROM_CHECKPOINT = False

# HF-compatible function to calculate test metrics from output prediction object.
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='macro', zero_division=0)
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1_macro': f1,
        'precision': precision,
        'recall': recall
    }


# Train transformer model
def finetune(model_identifier, conf):
    train_data = pd.read_csv('data/dso_dataset/rewire_dso_2022-12-05-1404_train_multilingual.csv', index_col=0)
    valid_data = pd.read_csv('data/dso_dataset/rewire_dso_2022-12-05-1404_val_multilingual.csv', index_col=0)
    test_data = pd.read_csv('data/dso_dataset/rewire_dso_2022-12-05-1404_test_multilingual.csv', index_col=0)

    model_name = model_identifier.split("/")[-1]
    tokenizer = AutoTokenizer.from_pretrained(model_identifier, use_fast=False, do_lower_case=True)
    model_loaded = AutoModelForSequenceClassification.from_pretrained(model_identifier, num_labels=2).to('cuda')

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=TOKENIZER_MAX)

    ds = {'train': (Dataset.from_pandas(train_data)).map(tokenize_function).remove_columns(["rewire_id", "text"]),
          'valid': (Dataset.from_pandas(valid_data)).map(tokenize_function).remove_columns(["rewire_id", "text"])}

    # Using a linear batch-size to LR relation: BS of 32 and LR 1e-05 (0.00001) or BS of 4 and LR 1.25e-06 (0.00000125)
    # Save checkpoints in non-task specific folder as to not clutter the output model folder.
    training_args = TrainingArguments(output_dir='models/training_cache/' + model_name,
                                      per_device_train_batch_size=conf['batch_size'],
                                      per_device_eval_batch_size=conf['batch_size'],
                                      evaluation_strategy="epoch", 
                                      save_strategy="epoch",
                                      # eval_steps=5000,
                                      # save_steps=400, 
                                      save_total_limit=1,
                                      gradient_accumulation_steps=1, 
                                      metric_for_best_model='eval_loss',
                                      load_best_model_at_end=True,
                                      num_train_epochs=conf['max_epochs'],
                                      learning_rate=conf['learning_rate'],
                                      warmup_steps=500,
                                      weight_decay=0.01,
                                      logging_steps=10,
                                      seed=10,
                                      data_seed=123)

    trainer = Trainer(
        model=model_loaded,
        args=training_args,
        train_dataset=ds['train'],
        eval_dataset=ds['valid'],
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=conf['patience'])]
    )

    training_results = trainer.train(resume_from_checkpoint=RESUME_FROM_CHECKPOINT)

    try:
        os.makedirs('outputs/evaluation/' + model_name)
    except FileExistsError:
       # directory already exists
       pass

    trainer.save_model('outputs/' + model_name)
    trainer.save_state()
    tokenizer.save_pretrained('outputs/' + model_name)

    # compute train results
    metrics = training_results.metrics
    metrics["train_samples"] = len(ds['train'])

    # save train results
    trainer.log_metrics("train", metrics)
    with open('outputs/evaluation/' + model_name + "/train_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4, sort_keys=True)

    # compute validation results
    metrics = trainer.evaluate()
    metrics["eval_samples"] = len(ds['valid'])

    # save validation results
    trainer.log_metrics("valid", metrics)
    with open('outputs/evaluation/' + model_name + "/validation_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4, sort_keys=True)


    tokenizer = AutoTokenizer.from_pretrained('outputs/' + model_name, use_fast=False, do_lower_case=True)
    ds = (Dataset.from_pandas(test_data)).map(tokenize_function).remove_columns(["rewire_id", "text"])
    model_loaded = AutoModelForSequenceClassification.from_pretrained('outputs/' + model_name)
    model_loaded.eval()
    model_loaded.to(device)
    evaluator = Trainer(model=model_loaded, compute_metrics=compute_metrics)
    preds = evaluator.predict(ds).predictions
    probabilities = nn.functional.softmax(from_numpy(preds), dim=-1)
    test_data[model_name] = probabilities[:, 1]
    test_data.to_csv('outputs/evaluation/' + model_name + "/test_set_predictions.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Finetunes a Model and saves the resulting model files to s3')
    parser.add_argument('-n','--model_identifier', help='Model Identifier', required=True)
    parser.add_argument('-e','--max_epochs', help='Max Number of Epochs', nargs='?', required=False, const=20, default=20, type=int)
    parser.add_argument('-l','--learning_rate', help='Model Folder', nargs='?', required=False, const=1e-05, default=1e-05, type=float)
    parser.add_argument('-p','--patience', help='Patience', nargs='?', required=False, const=3, default=3, type=int)
    parser.add_argument('-b','--batch_size', help='Batch Size', nargs='?', required=False, const=16, default=16, type=int)

    args = vars(parser.parse_args())
    finetune(args['model_identifier'], args)
