import json
import gradio as gr
from thema import ThemaManager
from dataset import DatasetManager
from chat_logic import respond
from history import ChatHistory

js_func = """
function refresh() {
    const url = new URL(window.location);
    if (!document.documentElement.hasAttribute('__theme')) {
        document.documentElement.setAttribute('__theme', 'dark');
    }
}
refresh();
"""

css_func = """
<style>
    :root {
        --block-background: #1f1f1f;
        --block-label-background: #2b2b2b;
        --input-background-fill: #2b2b2b;
        --body-background-fill: #1f1f1f;
        --color-background-primary: #2b2b2b;
        --background-fill-primary: #2b2b2b;
        --text-color: #ffffff;
    }
    button[aria-label="Clear"] {
        display: none !important;
    }
</style>
"""

thema_manager = ThemaManager()
dataset_manager = DatasetManager()
chat_history = ChatHistory()
history = []

def handle_theme_selection(choice):
    thema_manager.set_thema(choice)
    print(f"selected theme: {thema_manager.thema}")
    dataset_manager.set_dataset(choice)

def custom_label():
    return thema_manager.thema if thema_manager.thema in ["Thema 1", "Thema 2", "Thema 3"] else "gog"

def handle_dataset_selection(choice):
    chat_history.clear()
    if thema_manager.thema in ["Thema 1", "Thema 2", "Thema 3"]:
        with open(f"E:\\Pra\\dataset\\{dataset_manager.dataset}.json", "r") as file:
            dataset_data = json.load(file)
        if len(dataset_data) < 1:
            print("Error: Dataset is empty.")
        if len(dataset_data) > 1:
            print("Error: Dataset contains more than one element.")
        if len(dataset_data) == 1:
            message = dataset_data[0]
            chat_history.add_message(role=f"{message['role']}", content=f"{message['content']}")
            dataset_manager.set_dataset(choice)
        else:
            print("Error: Dataset does not contain exactly one element.")

def interface():
    with gr.Blocks(css=css_func) as demo:
        demo.load(fn=None, inputs=None, outputs=None, js=js_func)
        # Initial theme selection screen
        with gr.Group() as theme_screen:
            thema_auswahl = gr.Dropdown(
                label="Themenauswahl",
                choices=["Thema 1", "Thema 2", "Thema 3"],
                interactive=True
            )
            start_button = gr.Button("Select")

        # Chat interface (initially hidden)
        with gr.Group(visible=False) as chat_interface:
            with gr.Row():
                chatbox = gr.Chatbot(
                    scale=5,
                    label=custom_label(),
                    type="messages"
                )
            with gr.Row():
                inputbox = gr.Textbox(
                    scale=1,
                    show_label=False,
                )
            with gr.Row():
                print_history = gr.Button("Print History")
                clear_history = gr.ClearButton([inputbox, chatbox])

        def update_interface(choice):
            handle_theme_selection(choice)
            handle_dataset_selection(choice)
            new_label = custom_label()
            return [gr.update(visible=True), gr.update(visible=False), gr.update(label=new_label)]

        def send_message(message, history):
            chat_history.add_message(role='user', content=message)
            response = respond(chat_history.messages)
            return "", response

        start_button.click(
            fn=update_interface,
            inputs=[thema_auswahl],
            outputs=[chat_interface, theme_screen, chatbox]
        )

        print_history.click(
            fn=lambda: print(chat_history.messages),
            inputs=None,
            outputs=None
        )

        clear_history.click(
            fn=lambda: chat_history.clear(),
        )

        inputbox.submit(
            fn=send_message,
            inputs=[inputbox, chatbox],
            outputs=[inputbox, chatbox],
        )

    return demo


if __name__ == "__main__":
    demo = interface()
    demo.launch(
        #share=True,
        #auth=[("test", "test")],
        #pwa=True
                )