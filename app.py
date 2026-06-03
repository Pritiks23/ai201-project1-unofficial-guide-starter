import gradio as gr
from query import ask


def handle_query(question):
    result = ask(question)

    sources_text = "\n".join([f"• {s}" for s in result["sources"]])

    return result["answer"], sources_text


with gr.Blocks() as demo:
    gr.Markdown("# 🔍 RAG Assistant (Grounded QA System)")

    inp = gr.Textbox(label="Ask a question")
    btn = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Sources", lines=5)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()