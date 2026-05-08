import time
from typing import Generator

import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/ask"

CSS = """
#app-shell {
    max-width: 980px;
    margin: 0 auto;
}
#brand {
    padding: 18px 20px 8px 20px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(59,130,246,0.14), rgba(99,102,241,0.10));
    border: 1px solid rgba(148,163,184,0.18);
    margin-bottom: 14px;
}
#brand h1 {
    margin: 0;
    font-size: 34px;
    line-height: 1.1;
}
#brand p {
    margin: 8px 0 0 0;
    color: #64748b;
    font-size: 15px;
}
#chatbot {
    border-radius: 24px;
    overflow: hidden;
}
footer {
    display: none !important;
}
"""

def fetch_answer(message: str) -> str:
    response = requests.post(API_URL, json={"query": message}, timeout=60)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict):
        return data.get("answer") or str(data)
    return str(data)

def stream_reply(message: str, history) -> Generator[str, None, None]:
    try:
        full_answer = fetch_answer(message)
    except requests.exceptions.RequestException as e:
        full_answer = f"Request Error: {e}"
    except ValueError:
        full_answer = "Backend returned invalid JSON."
    except Exception as e:
        full_answer = f"Unexpected Error: {e}"

    partial = ""
    for ch in full_answer:
        partial += ch
        yield partial
        time.sleep(0.008)

with gr.Blocks(css=CSS, title="IKS Assistant") as demo:
    with gr.Column(elem_id="app-shell"):
        with gr.Group(elem_id="brand"):
            gr.Markdown(
                "# 🧠 IKS Assistant\n"
                "**Internal Knowledge Support** for employees, onboarding, and policy questions."
            )
            gr.Markdown(
                "Search your uploaded documents through the RAG backend and get grounded answers with citations."
            )

        chatbot = gr.Chatbot(
            layout="bubble",
            height=560,
            show_label=False,
            render_markdown=True,
            avatar_images=(None, None),
            elem_id="chatbot",
            placeholder=(
                "### Welcome to IKS Assistant\n"
                "Ask a question about policies, benefits, onboarding, or company docs."
            ),
        )

        gr.ChatInterface(
            fn=stream_reply,
            chatbot=chatbot,
            textbox=gr.Textbox(
                placeholder="Ask your knowledge base...",
                show_label=False,
                lines=1,
                max_lines=1,
                submit_btn="Send",
                stop_btn="Stop",
            ),
            title=None,
            description=None,
            submit_btn="Send",
            stop_btn="Stop",
            autofocus=True,
            fill_height=True,
            fill_width=True,
            flagging_mode="never",
            examples=[
                "How do I enroll in retirement plans?",
                "What leave options are available?",
            ],
        )

demo.queue()
demo.launch()