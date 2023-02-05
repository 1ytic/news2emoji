import openai
import numpy as np
import streamlit as st
from streamlit_confetti import confetti


# Assign credentials from streamlit secrets dict
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Completions are cut because sometimes the model predicts the non-training words
completion_mapping = {
    " hea": "\u2764\uFE0F", # correct black heart with additional code
    " pos": "👍",
    " neg": "👎",
    " thi": "🤔",
    " cry": "😢",
    " lau": "🤣",
    " scr": "😱",
    " sym": "🤬",
    " clo": "🤡",
    " shi": "💩",
}

models = {
    "ada, varlamov_news, 4 epochs": "ada:ft-personal-2023-02-04-16-19-14",
    "curie, varlamov_news, 4 epochs": "curie:ft-personal-2023-02-04-17-15-22",
    "davinci, varlamov_news, 1 epoch": "davinci:ft-personal-2023-02-02-22-55-48",
}


def show_chart(values:dict):

    """
    Example of values: [
        {"emoji": "🍊", "score": 0.7},
        {"emoji": "🍇", "score": 0.2},
        {"emoji": "🍏", "score": 0.1},
    ]
    """

    chart = {
        "data": {
            "values": values,
        },
        "config": {
            "legend": {"disable": True},
        },
        "encoding": {
            "x": {
                "field": "score",
                "type": "quantitative",
                "scale": {"domain": [0, 1]},
                "axis": {"grid": False, "labels": False},
                "title": None,
            },
            "y": {
                "field": "emoji",
                "type": "nominal",
                "sort": "-x",
                "title": None,
            },
        },
        "layer": [
            {
                # Main bar chart
                "mark": {"type": "bar", "cornerRadiusEnd": 15},
                "encoding": {"color": {"field": "score", "type": "quantitative"}},
            },
            {
                # Label text displayed on top of each bar line
                "mark": {
                    "type": "text",
                    "align": "right",
                    "xOffset": -4,
                    "aria": False,
                },
                "encoding": {
                    "text": {
                        "field": "score",
                        "type": "quantitative",
                        "format": ".1%",
                    },
                    "color": {
                        "value": "black",
                        "condition": {
                            "test": {"field": "score", "gt": 0.15},
                            "value": "white",
                        },
                    },
                },
            },
        ],
    }

    placeholder.vega_lite_chart(spec=chart, use_container_width=True)


@st.cache(show_spinner=False)  # Don't waste 💸 the OpenAI requests
def do_request(written_text: str, selected_model: str):
    # The function `do_request` created, because
    # @st.cache can't handle st.session_state
    response = openai.Completion.create(
        model=models[selected_model],
        prompt=written_text + "\n\n###\n\n",
        temperature=0,
        max_tokens=1,
        logprobs=5,
    )
    choices: list = response["choices"]
    logprobs: list = choices[0]["logprobs"]
    top_logprobs: dict = logprobs["top_logprobs"][0]
    gpt_result = []
    for key, logprob in top_logprobs.items():
        emoji = completion_mapping[key.lower()[:4]]
        probability = np.exp(logprob)
        if probability > 0.04:
            gpt_result.append({"emoji": emoji, "score": probability})
    gpt_result.sort(key=lambda x: x["score"], reverse=True)
    return gpt_result


def predict_reactions(written_text: str, selected_model: str, text_limit: int = 1000):
    with placeholder:
        with st.spinner("Please wait while the model predicts the reactions..."):
            try:
                # Don't waste 💸 the OpenAI tokens quote
                assert len(written_text) < text_limit, f"The text length {len(written_text)} exceeds the {text_limit} characters limit."
                st.session_state.gpt_result = do_request(written_text, selected_model)
            except Exception as e:
                st.session_state.gpt_result = None
                st.session_state.gpt_error = e


st.set_page_config(page_title="news❤️emoji", page_icon="🤖", initial_sidebar_state="collapsed")

st.markdown("""
## Predict news reactions
This app predicts emoji reactions using OpenAI's based [models](https://platform.openai.com/docs/models/overview) for the news messages. 
The models fine tunes on [@varlamov_news](http://t.me/varlamov_news) corpus messages 2022-2023 with emoji reactions. 
You can find more details on GitHub [news2emoji](https://github.com/1ytic/news2emoji) project.
""")

with st.sidebar:
    model = st.radio(label="Choose a fine-tune model:", options=models.keys())

value = "Британский художник Бэнкси опубликовал видео со своими работами, созданными на территории Украины, в том числе на стенах поврежденных домов."
placeholder = "Введите текст новости на русском языке."

text = st.text_area(
    label="News message",
    height=100,
    value=value,
    placeholder=placeholder,
    label_visibility="collapsed",
)

st.button(label="Predict", on_click=predict_reactions, args=(text, model))

placeholder = st.empty()

if st.session_state.get("gpt_error"):
    placeholder.error(f"OpenAI API error: {st.session_state.gpt_error}")

if st.session_state.get("gpt_result"):
    show_chart(st.session_state.get("gpt_result"))

# We use the special "key" argument to assign a fixed identity to this
# component instance. By default, when a component's arguments change,
# it is considered a new instance and will be re-mounted on the frontend
# and lose its current state. In this case, we want to vary the component's
# "name" argument without having it get recreated.
confetti(emojis=st.session_state.get("gpt_result"), key="confetti")

st.session_state.gpt_result = None
