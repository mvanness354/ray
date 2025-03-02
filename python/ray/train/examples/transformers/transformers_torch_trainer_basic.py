# Minimal Example adapted from https://huggingface.co/docs/transformers/training
from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
import numpy as np
import evaluate

from ray.train.huggingface.transformers import (
    prepare_trainer,
    RayTrainReportCallback,
)
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer


# [1] Define a training function that includes all your training logics
# =====================================================================
def train_func(config):
    # Datasets
    dataset = load_dataset("yelp_review_full")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    tokenized_ds = dataset.map(tokenize_function, batched=True)

    small_train_ds = tokenized_ds["train"].shuffle(seed=42).select(range(1000))
    small_eval_ds = tokenized_ds["test"].shuffle(seed=42).select(range(1000))

    # Model
    model = AutoModelForSequenceClassification.from_pretrained(
        "bert-base-cased", num_labels=5
    )

    # Evaluation Metrics
    metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    # HuggingFace Trainer
    training_args = TrainingArguments(
        output_dir="test_trainer", evaluation_strategy="epoch", report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_ds,
        eval_dataset=small_eval_ds,
        compute_metrics=compute_metrics,
    )

    # [2] Report metrics and checkpoints to Ray Train
    # ===============================================
    trainer.add_callback(RayTrainReportCallback())

    # [3] Prepare your trainer for Ray Data Integration
    # =================================================
    trainer = prepare_trainer(trainer)

    # Start Training
    trainer.train()


# [4] Build a Ray TorchTrainer to launch `train_func` on all workers
# ==================================================================
trainer = TorchTrainer(
    train_func, scaling_config=ScalingConfig(num_workers=4, use_gpu=True)
)

trainer.fit()
