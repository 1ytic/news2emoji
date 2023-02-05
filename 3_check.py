import typer
import pandas as pd
from pathlib import Path


def main(input_path: Path = typer.Argument(..., exists=True, dir_okay=False)):
    df = pd.read_json(input_path, lines=True)
    print(len(df))
    print(df.completion.value_counts())
    assert len(df.completion.value_counts()) == 10


if __name__ == "__main__":
    typer.run(main)
