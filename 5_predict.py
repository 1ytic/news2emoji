import srsly
import spacy
import typer
from pathlib import Path


def main(
    model_path: Path = typer.Argument(..., exists=True, file_okay=False),
    valid_path: Path = typer.Argument(..., exists=True, dir_okay=False),
):
    nlp = spacy.load(model_path)

    data = ((eg["prompt"], eg) for eg in srsly.read_jsonl(valid_path))

    result = []
    for doc, eg in nlp.pipe(data, as_tuples=True):
        label = eg["completion"].strip()
        prediction = max(doc.cats, key=doc.cats.get)
        result.append(prediction == label)

    print(sum(result) / len(result))


if __name__ == "__main__":
    typer.run(main)
