import os
import pandas as pd
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from datetime import datetime, timedelta, timezone


load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CHANNEL = os.getenv("CHANNEL")

START_DATE = datetime(2022, 2, 1, tzinfo=timezone(timedelta(hours=3), name="Europe/Moscow"))
END_DATE = datetime(2023, 2, 1, tzinfo=timezone(timedelta(hours=3), name="Europe/Moscow"))

client = TelegramClient("credentials", API_ID, API_HASH)

emoticons = ["❤", "👍", "👎", "🤔", "😢", "🤣", "😱", "🤬", "🤡", "💩"]
# removed emoji ["🔥", "😁", "🍌", "🤯", "🤩", "🤮", "🥰", "🎉", "👏"]
emoticons2id = {e: i for i, e in enumerate(emoticons)}

data = []


def flatten_reactions(results):
    counts = [0] * len(emoticons)
    for reaction_count in results:
        e = reaction_count.reaction.emoticon
        if e not in emoticons2id:
            return None
        i = emoticons2id[e]
        counts[i] = reaction_count.count
    return counts


async def main():
    async for message in client.iter_messages(CHANNEL, offset_date=END_DATE):
        if message is None:
            break
        offset_date = message.date
        if offset_date < START_DATE:
            break
        if not message.message:
            continue
        if message.reactions is None:
            continue
        counts = flatten_reactions(message.reactions.results)
        if counts is None:
            print("This message with old reaction schema")
            break
        if sum(counts) == 0:
            continue
        data.append([message.id, message.date] + counts + [message.message])
        if len(data) % 100 == 0:
            print(len(data), message.date)

with client:
    client.loop.run_until_complete(main())

os.makedirs(f"data/{CHANNEL}", exist_ok=True)

df = pd.DataFrame(data, columns=["id", "date"] + emoticons + ["text"])
df.to_csv(f"data/{CHANNEL}/messages.csv", encoding="utf-8", index=False)

print("Done", len(df))
