import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

CHANNEL = os.getenv("CHANNEL")

df = pd.read_csv(f"data/{CHANNEL}/messages.csv", index_col="id")

print("Downloaded message:", len(df))

df = df.dropna()

df["len"] = df["text"].str.split().apply(len)

df["len"].hist(bins=50).get_figure().savefig("data/{CHANNEL}/len_hist.png")

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

historical_completion_mapping = {
    "🔥": "fire",
    "😁": "grin",
    "🍌": "banana",
    "🤯": "exploding",
    "🤮": "vomiting",
    "🤩": "star",
    "🥰": "hearts",
    "🎉": "celebrating",
    "👏": "applause",
}


prompts = df["text"].apply(lambda x: x + "\n\n###\n\n")
targets = df[completion_mapping.keys()].idxmax(axis="columns")
completions = targets.apply(lambda x: " " + completion_mapping[x] + "\n")

stats = targets.value_counts()
print(stats)

df = pd.concat([prompts.rename("prompt"), completions.rename("completion")], axis=1)

df = df.drop_duplicates(subset=["prompt"])

df = df.sample(frac=1, random_state=37)

df = df.groupby("completion").apply(lambda x: x.sample(min(len(x), 400), random_state=37))

stats = df["completion"].value_counts()
print(stats)

df.to_json(f"data/{CHANNEL}/classification/dataset.jsonl", orient="records", lines=True, force_ascii=False)

print("Done", len(df))
