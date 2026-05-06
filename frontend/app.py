import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/ask"


def respond(message, history):

    try:
        response = requests.post(
            API_URL,
            json={"query": message}
        )

        data = response.json()

        answer = data.get(
            "answer",
            "No response from backend."
        )

        return answer

    except Exception as e:
        return f"Error: {str(e)}"


demo = gr.ChatInterface(
    fn=respond,
    title="🧠 Internal Knowledge Support",
    description="Ask questions from your knowledge base."
)

demo.launch()