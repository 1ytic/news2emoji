import os
import typer
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

CHANNEL = os.getenv("CHANNEL")
TASK = os.getenv("TASK")

def main(input_path: Path = typer.Argument(..., exists=True, dir_okay=False)):
    df = pd.read_json(input_path, lines=True)

    print(len(df))
    print(df.completion.value_counts())

    train = df.sample(frac=0.8, random_state=37)
    valid = df.drop(train.index)

    print(len(train), len(valid))

    train.to_json(f"data/{CHANNEL}/{TASK}/dataset_prepared_train.jsonl", orient="records", lines=True, force_ascii=False)
    valid.to_json(f"data/{CHANNEL}/{TASK}/dataset_prepared_valid.jsonl", orient="records", lines=True, force_ascii=False)


if __name__ == "__main__":
    typer.run(main)
