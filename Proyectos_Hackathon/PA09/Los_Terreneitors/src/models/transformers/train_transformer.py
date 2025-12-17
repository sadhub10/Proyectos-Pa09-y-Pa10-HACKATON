from pathlib import Path
import json
import numpy as np
import pandas as pd
import inspect

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


# ================================
# CONFIG
# ================================
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_dataset.csv"

# Guardaremos el transformer dentro de src/models/transformers/checkpoints/
OUT_DIR = PROJECT_ROOT / "src" / "models" / "transformers" / "checkpoints" / "distilbert"

MODEL_NAME = "distilbert-base-uncased"

TEXT_COL = "text"
LABEL_COL = "label"

LABELS = ["Anxiety", "Depression", "Stress", "Suicidal"]
label2id = {l: i for i, l in enumerate(LABELS)}
id2label = {i: l for l, i in label2id.items()}


def _compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average="weighted"),
        "precision": precision_score(labels, preds, average="weighted", zero_division=0),
        "recall": recall_score(labels, preds, average="weighted", zero_division=0),
    }


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No encontré el dataset en: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Si tus etiquetas vienen en español, normalizamos a inglés
    mapping_es = {
        "Ansiedad": "Anxiety",
        "Depresión": "Depression",
        "Estrés": "Stress",
        "Ideación suicida": "Suicidal",
    }
    if LABEL_COL in df.columns:
        df[LABEL_COL] = df[LABEL_COL].replace(mapping_es)

    if TEXT_COL not in df.columns or LABEL_COL not in df.columns:
        raise ValueError(
            f"Tu CSV debe tener columnas '{TEXT_COL}' y '{LABEL_COL}'. "
            f"Columnas actuales: {list(df.columns)}"
        )

    df = df.dropna(subset=[TEXT_COL, LABEL_COL]).copy()
    df = df[df[LABEL_COL].isin(LABELS)].copy()
    df["label_id"] = df[LABEL_COL].map(label2id)

    dataset = Dataset.from_pandas(df[[TEXT_COL, "label_id"]])
    dataset = dataset.train_test_split(test_size=0.2, seed=42)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenize(batch):
        return tokenizer(
            batch[TEXT_COL],
            truncation=True,
            padding="max_length",
            max_length=256
        )

    tokenized = dataset.map(tokenize, batched=True)
    tokenized = tokenized.rename_column("label_id", "labels")
    tokenized.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABELS),
        id2label=id2label,
        label2id=label2id,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ================================
    # TrainingArguments (compatibilidad)
    # ================================
    base_args = dict(
        output_dir=str(OUT_DIR / "runs"),
        save_strategy="epoch",
        logging_strategy="steps",
        logging_steps=50,
        num_train_epochs=2,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        learning_rate=2e-5,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        report_to="none",
    )

    sig = inspect.signature(TrainingArguments.__init__)

    # Transformers nuevos: eval_strategy
    if "eval_strategy" in sig.parameters:
        base_args["eval_strategy"] = "epoch"
    # Transformers viejos: evaluation_strategy
    elif "evaluation_strategy" in sig.parameters:
        base_args["evaluation_strategy"] = "epoch"

    args = TrainingArguments(**base_args)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
        compute_metrics=_compute_metrics,
    )

    trainer.train()

    trainer.save_model(str(OUT_DIR))
    tokenizer.save_pretrained(str(OUT_DIR))

    # Guardar métricas en reports/metrics
    metrics = trainer.evaluate()
    metrics_path = PROJECT_ROOT / "reports" / "metrics" / "transformer_metrics.json"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Transformer guardado en: {OUT_DIR}")
    print(f"Métricas guardadas en: {metrics_path}")


if __name__ == "__main__":
    main()
