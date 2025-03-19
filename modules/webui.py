import argparse
import json
import os
import gradio as gr
from _func import *
from thema import ThemaManager
from dataset import DatasetManager
from history import ChatHistory


thema_manager = ThemaManager()
dataset_manager = DatasetManager()
chat_history = ChatHistory()
history = []
current_question = None
current_expected_answer = None


def parse_args():
    parser = argparse.ArgumentParser(description='Web UI Startup Arguments')
    parser.add_argument('--api-key', nargs='?', const=True, default=False,
                        help='Use API response handler. Optionally provide an API key.')
    parser.add_argument('--api-endpoint', nargs='?', const=True, default="http://192.168.1.187:8080",
                        help='Use API response handler. Provide an IP address.')
    return parser.parse_args()


def handle_theme_selection(theme, subtopic=None):
    thema_manager.set_thema(theme)
    #print(f"selected theme: {thema_manager.thema}")

    # If subtopic is provided, include it in the dataset name
    if subtopic:
        dataset_name = f"{theme} - {subtopic}"
    else:
        dataset_name = theme

    dataset_manager.set_dataset(dataset_name)
    return dataset_name


def custom_label():
    return thema_manager.thema if thema_manager.thema in ["Thema 1", "Thema 2", "Thema 3"] else "gog"


def load_question_from_dataset(dataset_name):
    global current_question, current_expected_answer

    # Check for dataset file with the combined name first
    dataset_filename = f"{dataset_name}.json"
    dataset_path = os.path.join(".\\dataset", dataset_filename)

    # If the combined file doesn't exist, fall back to the main theme file
    if not os.path.exists(dataset_path):
        main_theme = dataset_name.split(" - ")[0] if " - " in dataset_name else dataset_name
        dataset_filename = f"{main_theme}.json"
        dataset_path = os.path.join(".\\dataset", dataset_filename)

    if os.path.exists(dataset_path):
        try:
            with open(dataset_path, "r", encoding="utf-8") as file:
                dataset_data = json.load(file)

            if len(dataset_data) < 1:
                print("Error: Dataset is empty.")
                return "No question available", ""
            else:
                # Assuming the dataset now contains a question and expected answer
                for item in dataset_data:
                    if item.get("type") == "question":
                        current_question = item.get("content", "No question available")
                        current_expected_answer = item.get("expected_answer", "")
                        return current_question, current_expected_answer

                # If no question type found, use the first item's content as question
                message = dataset_data[0]
                current_question = message.get("content", "No question available")
                current_expected_answer = message.get("expected_answer", "")
                return current_question, current_expected_answer

        except Exception as e:
            print(f"Error loading dataset: {e}")
            return f"Error loading question: {e}", ""
    else:
        print(f"Warning: Dataset file {dataset_path} not found.")
        return "Dataset not found", ""

def evaluate_answer_with_llm(user_answer, expected_answer, question):
    # Check if the answer is minimal (like "..." or just a few characters)
    is_minimal_answer = len(user_answer.strip()) <= 5

    # Create a prompt for the LLM to evaluate the answer
    evaluation_prompt = [
        {
            "role": "system",
            "content": "Du bist ein Prüfer, der Antworten auf Aufgaben bewertet. Bewerte die Antwort auf einer Skala von 0 bis 10 und gib eine kurze Begründung. Auch minimale oder unvollständige Antworten müssen bewertet werden."
        },
        {
            "role": "user",
            "content": f"Hier ist die Aufgabenstellung: {question}\n\n"
                       f"Hier die erwartete Antwort: {expected_answer}\n\n"
                       f"Und zuletzt die Benutzerantwort: {user_answer}\n\n"
                       +
                       (
                           f"Hinweis: Dies scheint eine sehr kurze oder minimale Benutzerantwort zu sein (zur Referenz lautet die zu bewertende Benutzerantwort: {user_answer}). Bewerte sie trotzdem im kompletten Umfang.\n\n" if is_minimal_answer else ""
                       )
                       +
                       f"Bewerte diese Benutzerantwort auf einer Skala von 0 bis 10 und erkläre kurz, warum du diese Bewertung gibst. Beziehe dich dabei auf die erwartete Antwort und falls nötig auch weitere Randinformationen. Antworte IMMER im folgenden Format:\nPunkte: [0-10]\nBegründung: [Deine Begründung]"
        }
    ]

    # Get response from LLM
    response = respond(evaluation_prompt)

    #TODO: Maybe add a tool for symantic analysis to check if the answer is identidcal to the expected answer?

    # Extract score and feedback from the response
    try:
        # Find the score in the response
        score_line = [line for line in response[-1]['content'].split('\n') if line.startswith('Punkte:')]
        if score_line:
            score_text = score_line[0].replace('Punkte:', '').strip()
            # Extract the number from the score text
            import re
            score_match = re.search(r'\d+', score_text)
            if score_match:
                score = int(score_match.group())  # Convert to integer
                # Ensure score is within 0-10 range
                score = max(0, min(10, score))
            else:
                score = -1  # Default if no number found
        else:
            score = -1  # Default if no score line found

        # Get the feedback
        feedback_parts = [line for line in response[-1]['content'].split('\n') if line.startswith('Begründung:')]
        if feedback_parts:
            feedback = feedback_parts[0].replace('Begründung:', '').strip()
            # If there are additional lines after "Begründung:", include them
            start_idx = response[-1]['content'].find('Begründung:')
            if start_idx != -1:
                feedback = response[-1]['content'][start_idx:].replace('Begründung:', '').strip()
        else:
            feedback = response[-1]['content']  # Use the whole response if no specific feedback found

        return score, feedback
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        print(f"Raw response: {response}")
        return -1, "Error evaluating answer. Please try again."


def get_score_bar_color(score):
    # Convert score to integer if it's a string
    if isinstance(score, str):
        try:
            score = int(score)
        except ValueError:
            # If conversion fails, default to a middle score
            return "#37134A"  # Amber for unknown scores

    # Now compare with integers
    if score <= 3:
        return "#FF5252"  # Red for low scores
    elif score <= 6:
        return "#FFC107"  # Amber for medium scores
    elif score <= 8:
        return "#4CAF50"  # Green for good scores
    else:
        return "#2196F3"  # Blue for excellent scores

def get_available_datasets():
    """
    Scans the dataset directory and organizes files into themes and subtopics.
    Returns a dictionary with themes as keys and lists of subtopics as values.
    """
    dataset_dir = ".\\dataset"
    themes = {}

    # Check if directory exists
    if not os.path.exists(dataset_dir):
        print(f"Warning: Dataset directory {dataset_dir} not found.")
        return themes

    # List all JSON files in the dataset directory
    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json'):
            # Parse the filename to extract theme and subtopic
            parts = filename.replace('.json', '').split(' - ')

            if len(parts) == 1:
                # If there's only one part, it's a main theme without subtopic
                theme = parts[0]
                if theme not in themes:
                    themes[theme] = []
            elif len(parts) >= 2:
                # If there are two parts, first is theme, second is subtopic
                theme = parts[0]
                subtopic = ' - '.join(parts[1:])

                if theme not in themes:
                    themes[theme] = []
                themes[theme].append(subtopic)

    return themes


def interface():
    with gr.Blocks(css=css_func) as demo:
        demo.load(fn=None, inputs=None, outputs=None, js=js_func)

        # Get available datasets
        available_datasets = get_available_datasets()

        # Initial theme selection screen
        with gr.Group() as theme_screen:
            gr.Markdown("## Informatik -- Projektarbeit", elem_classes="topic-label")
            with gr.Accordion("Automatentheorie", open=True, elem_classes="accordion"):
                # Dynamically create accordions for each theme
                theme_accordions = {}
                theme_buttons = {}

                for theme, subtopics in available_datasets.items():
                    with gr.Accordion(theme, open=False, elem_classes="accordion") as theme_accordion:
                        theme_accordions[theme] = theme_accordion
                        theme_buttons[theme] = {}

                        with gr.Column(elem_classes="section"):
                            if subtopics:
                                # Create buttons for each subtopic
                                for subtopic in subtopics:
                                    btn = gr.Button(subtopic)
                                    theme_buttons[theme][subtopic] = btn
                            else:
                                # If there are no subtopics, create a button for the theme itself
                                btn = gr.Button("Allgemein")
                                theme_buttons[theme]["Allgemein"] = btn

        # Quiz interface (initially hidden)
        with gr.Group(visible=False) as quiz_interface:
            # Question box at the top
            with gr.Column(elem_classes="section"):
                question_box = gr.HTML(
                    "Question will appear here",
                    elem_classes="question-container"
                )

            with gr.Column(elem_classes="section"):
                answer_input = gr.Textbox(
                    label="Antwort:",
                    placeholder="Antwort hier eingeben...",
                    lines=3
                )

            with gr.Column(visible=False) as feedback_container:
                result_box = gr.HTML(
                    "Feedback will appear here",
                    elem_classes="feedback-container"
                )

            with gr.Column(visible=False, elem_classes="section") as expected_answer_container:
                expected_answer_box = gr.Markdown("Expected answer will appear here")

            with gr.Column(visible=False, elem_classes="section") as score_display:
                score_value = gr.HTML('<div class="score-value">0 / 10</div>')
                score_bar_container = gr.HTML(
                    """<div class="score-bar-container">
                        <div class="score-bar" style="width: 0%; background-color: #FF5252;"></div>
                    </div>"""
                )

            # Add a new row for buttons at the bottom, split into two columns
            with gr.Row(elem_classes="section button-row"):
                with gr.Column(scale=1):
                    back_to_topics_btn = gr.Button(
                        "zurück zur Themenauswahl",
                        elem_classes=["theme-button", "back-button"]
                    )

                with gr.Column(scale=1):
                    submit_button = gr.Button(
                        "Antwort abgeben",
                        elem_classes=["theme-button", "submit-button"]
                    )

        def update_interface_with_subtopic(theme, subtopic):
            dataset_name = handle_theme_selection(theme, subtopic)
            question, expected = load_question_from_dataset(dataset_name)

            # Format the question with the topic in the header
            if subtopic:
                formatted_question = f"""
                <div class="integrated-question">
                    <div class="question-header">
                        <div class="question-title">Aufgabe ({theme} - {subtopic}):</div>
                    </div>
                    <div>{question}</div>
                </div>
                """
            else:
                formatted_question = f"""
                <div class="integrated-question">
                    <div class="question-header">
                        <div class="question-title">Aufgabe ({theme}):</div>
                    </div>
                    <div>{question}</div>
                </div>
                """

            return [
                gr.update(visible=True),
                gr.update(visible=False),
                formatted_question,  # Use the formatted question HTML with topic
                gr.update(value="", interactive=True),  # Clear answer input AND make it interactive
                gr.update(visible=False),  # Hide result
                gr.update(visible=False),  # Hide expected answer
                gr.update(visible=False),  # Hide score display
                gr.update(visible=False),  # Hide feedback container
                gr.update(interactive=True, elem_classes=["theme-button", "submit-button"])  # Reset submit button state
            ]

        # Set up event handlers for dynamically created buttons
        for theme, subtopic_buttons in theme_buttons.items():
            for subtopic, btn in subtopic_buttons.items():
                # For the "Allgemein" button, we don't pass a subtopic
                if subtopic == "Allgemein":
                    btn.click(
                        fn=update_interface_with_subtopic,
                        inputs=[gr.State(theme), gr.State(None)],
                        outputs=[
                            quiz_interface,
                            theme_screen,
                            question_box,
                            answer_input,
                            result_box,
                            expected_answer_box,
                            score_display,
                            feedback_container,
                            submit_button
                        ]
                    )
                else:
                    btn.click(
                        fn=update_interface_with_subtopic,
                        inputs=[gr.State(theme), gr.State(subtopic)],
                        outputs=[
                            quiz_interface,
                            theme_screen,
                            question_box,
                            answer_input,
                            result_box,
                            expected_answer_box,
                            score_display,
                            feedback_container,
                            submit_button
                        ]
                    )

        def submit_answer(answer):
            # Check if answer is empty and handle accordingly
            if not answer or answer.strip() == "":
                # Option 1: Return without submitting to LLM
                return [
                    gr.update(visible=True,
                              value="<div class='integrated-question'><div class='question-header'><div class='question-title'>Fehler:</div></div><div>Bitte geben Sie eine Antwort ein, bevor Sie fortfahren.</div></div>"),
                    gr.update(visible=False),  # Hide expected answer
                    gr.update(visible=False),  # Hide score display
                    "",  # Empty score value
                    "",  # Empty score bar
                    gr.update(interactive=True),  # Keep submit button active
                    gr.update(visible=True),  # Show feedback container
                    gr.update(interactive=True)  # Keep answer input interactive
                ]

            # Use LLM to evaluate the answer
            score, feedback = evaluate_answer_with_llm(answer, current_expected_answer, current_question)

            # Ensure score is an integer
            if isinstance(score, str):
                try:
                    score = int(score)
                except ValueError:
                    score = -1  # Default if conversion fails

            # Get color based on score
            bar_color = get_score_bar_color(score)

            # Create HTML for the score bar
            bar_width = f"{score * 10}%"

            # Create integrated feedback HTML with score and bar - using the same structure as question
            integrated_feedback = f"""
            <div class="integrated-question">
                <div class="question-header">
                    <div class="question-title">Feedback:</div>
                    <div class="score-value-inline" style="color: {bar_color};">{score}/10</div>
                </div>

                <div class="score-bar-container" style="margin-bottom: 16px;">
                    <div class="score-bar" style="width: {bar_width}; background-color: {bar_color};"></div>
                </div>

                <div>{feedback}</div>
            </div>
            """

            expected_answer_md = f"## Expected Answer\n{current_expected_answer}"

            return [
                gr.update(visible=True, value=integrated_feedback),
                gr.update(visible=True, value=expected_answer_md),
                gr.update(visible=False),  # Hide score display since it's now in the feedback
                "",  # Empty score value
                "",  # Empty score bar
                gr.update(interactive=False, elem_classes=["theme-button", "submit-button", "disabled-button"]),
                # Disable submit button instead of hiding
                gr.update(visible=True),  # Show feedback container
                gr.update(interactive=False)  # Make answer input field non-interactive
            ]

        submit_button.click(
            fn=submit_answer,
            inputs=[answer_input],
            outputs=[
                result_box,
                expected_answer_box,
                score_display,
                score_value,
                score_bar_container,
                submit_button,
                feedback_container,
                answer_input  # Add this line to include answer_input in outputs
            ]
        )

        back_to_topics_btn.click(
            fn=lambda: [gr.update(visible=False), gr.update(visible=True)],
            inputs=[],
            outputs=[quiz_interface, theme_screen]
        )

    return demo

if __name__ == "__main__":
    args = parse_args()
    if args.api_key and args.api_endpoint:
        from chat_logic_api import respond
        import chat_logic_api
        chat_logic_api.API_KEY = args.api_key
        chat_logic_api.API_ENDPOINT = f"{args.api_endpoint}/v1/chat/completions"
    else:
        from chat_logic_local import respond

    demo = interface()
    demo.launch(
        #share=True,
        #auth=("gog", "sigma")
    )
