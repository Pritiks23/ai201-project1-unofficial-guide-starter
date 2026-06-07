import gradio as gr

def test(x):
    print("CLICK")
    return "OK"

demo = gr.Interface(test, "text", "text")

demo.launch(
    server_name="127.0.0.1",
    server_port=7861,
    show_error=True,
    quiet=False
)