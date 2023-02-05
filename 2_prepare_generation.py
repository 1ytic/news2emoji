import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

CHANNEL = os.getenv("CHANNEL")

df = pd.read_csv(f"data/{CHANNEL}/messages.csv", index_col="id")

print("Downloaded message:", len(df))

df = df.dropna()

df["len"] = df["text"].str.split().apply(len)

df["len"].hist(bins=50).get_figure().savefig("len_hist.png")

df = df[(df.len > 10) & (df.len < 100)]

print("Filtered messages:", len(df))

completion_mapping = {
    "❤": "heart",
    "👍": "positive",
    "👎": "negative",
    "🤔": "thinking",
    "😢": "cry",
    "🤣": "laughing",
    "😱": "scream",
    "🤬": "symbols",
    "🤡": "clown",
    "💩": "shit",
}

completion_values = list(completion_mapping.values())


def convert(row):
    idx = row.argsort()[::-1]
    non_zero_idx = idx[row[idx] != 0]
    text = " ".join([completion_values[int(x)] for x in non_zero_idx])
    return f" {text} END"


prompts = df["text"].apply(lambda x: x + "\n\n###\n\n")
completions = df[completion_mapping.keys()].apply(convert, axis=1)

df = pd.concat([prompts.rename("prompt"), completions.rename("completion")], axis=1)

df = df.drop_duplicates(subset=["prompt"])

stats = df["completion"].value_counts()
print(stats)

df.to_json(f"data/{CHANNEL}/generation/dataset.jsonl", orient="records", lines=True, force_ascii=False)

print("Done", len(df))
