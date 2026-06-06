import gradio as gr
from src.query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    sources = "\n".join(f"• {source}" for source in result["sources"])

    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide")
    gr.Markdown("Ask questions about SFSU CS professors, courses, electives, and student experiences.")

    question = gr.Textbox(label="Your question", placeholder="Example: What do students say about Robert Bierman and CSC 415?")
    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=6)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()