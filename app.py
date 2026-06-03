import gradio as gr
from query import ask


def handle_query(question):
    result = ask(question)

    sources = "\n".join([f"• {s}" for s in result["sources"]])

    return result["answer"], sources


# ----------------------------
# MODERN GRADIO (NO deprecated APIs)
# ----------------------------
with gr.Blocks() as demo:
    gr.Markdown("# RAG Assistant")

    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()