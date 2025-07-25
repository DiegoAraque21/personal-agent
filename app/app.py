from chat.controller import ChatController
import gradio as gr

# make the chatbot have a better UI



def main():
    controller = ChatController()

    with gr.Blocks(theme=gr.themes.Monochrome(), css="""
.gradio-container { background: #181a20 !important; }
#main-title, #footer, #sidebar-info { color: #e0e0e0 !important; }
.gr-chatbot { background: #23262f !important; }
.gr-textbox textarea { background: #23262f !important; color: #e0e0e0 !important; }
""") as ui:
        gr.Markdown(
            """
            # 👋 Diego Araque's AI Assistant
            Welcome! Ask me anything about Diego's professional background, projects, or experience.
            """,
            elem_id="main-title"
        )
        with gr.Row():
            with gr.Column(scale=1, min_width=120):
                gr.Image(
                    value="https://media.licdn.com/dms/image/v2/D4D03AQEmLX_SGf-wBQ/profile-displayphoto-shrink_800_800/B4DZbGu7chG8Ac-/0/1747090914455?e=1756339200&v=beta&t=a-Wg3VIb8VcfauNnoyuMdAd-w1HO8wvPwTRNJmZ9Q0Y",  # Replace with Diego's avatar if available
                    show_label=False,
                    show_download_button=False,
                    height=100,
                    width=100,
                )
                gr.Markdown(
                    """
                    **Diego Araque**  
                    Software Engineer | Capital One, Tec de Monterrey
                    [LinkedIn](https://www.linkedin.com/in/diegoaraque21/)
                    """,
                    elem_id="sidebar-info"
                )
            with gr.Column(scale=4):
                chat = gr.Chatbot(
                    type="messages",
                    min_height=400,
                    label="💬 Chat with Diego's AI",
                    bubble_full_width=False,
                )
                msg = gr.Textbox(
                    label="Your message",
                    placeholder="Ask about Diego's skills, experience, or projects...",
                    autofocus=True,
                    submit_btn=True
                )
                history_state = gr.State([])
                emails_sent = gr.State([])

                def add_user_message(message, history):
                    history.append({"role": "user", "content": message})
                    return history, history

                def respond(history, emails_state):
                    message = history[-1]["content"]
                    reply, emails = controller.get_response(msg=message, history=history, emails_sent=set(emails_state))
                    history.append({"role": "assistant", "content": reply})
                    return history, list(emails)

                msg.submit(add_user_message, inputs=[msg, history_state], outputs=[history_state, chat])
                msg.submit(respond, inputs=[history_state, emails_sent], outputs=[chat, emails_sent])
                msg.submit(lambda: "", None, msg)

        gr.Markdown(
            """
            <div style='text-align: center; color: #888; font-size: 0.9em; margin-top: 2em;'>
                Powered by OpenAI & Gradio | © 2024 Diego Araque
            </div>
            """,
            elem_id="footer"
        )

    ui.launch(share=True)