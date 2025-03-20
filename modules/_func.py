#Style für die Gradio Benutzeroberfläche
css_func = """
<style>
    /* Schriftart importieren und Basisvariablen festlegen */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --block-background: #1f1f1f;
        --block-label-background: #2b2b2b;
        --input-background-fill: #2b2b2b;
        --body-background-fill: #1f1f1f;
        --color-background-primary: #2b2b2b;
        --background-fill-primary: #2b2b2b;
        --text-color: #ffffff;
    }

    /* Basis-Typografie */
    body, .gradio-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.5;
        letter-spacing: 0.015em;
    }

    /* Überschriften */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        letter-spacing: -0.01em;
        margin: 0.5em 0 0.8em;
    }
    h2 { font-size: 1.75rem; letter-spacing: -0.02em; }
    h3 { font-size: 1.35rem; margin-bottom: 0.6em; }

    /* Layout-Elemente */
    .accordion { margin-bottom: 12px; }
    .accordion-header { font-weight: 500; letter-spacing: 0.01em; }
    .gradio-container .prose { max-width: none; }
    .section { margin-bottom: 12px; }

    /* Form Elemente */
    textarea, input[type="text"] {
        font-size: 1rem;
        line-height: 1.5;
        padding: 12px 16px !important;
        border-radius: 6px !important;
    }
    label {
        font-weight: 500;
        margin-bottom: 6px;
        font-size: 0.95rem;
    }
    button[aria-label="Clear"] { display: none !important; }

    /* Buttons */
    button {
        font-weight: 500 !important;
        letter-spacing: 0.01em;
        padding: 8px 16px !important;
        border-radius: 6px !important;
        transition: all 0.2s ease;
    }
    .theme-button {
        width: 100% !important;
        background-color: #2b2b2b !important;
        border: 1px solid #3a3a3a !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        transition: all 0.2s ease !important;
    }
    .theme-button:hover {
        background-color: #3a3a3a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
    }
    .submit-button {
        background-color: #2196F3 !important;
        border-color: #1976D2 !important;
    }
    .submit-button:hover { background-color: #1976D2 !important; }
    .back-button {
        background-color: #424242 !important;
        border-color: #616161 !important;
    }
    .back-button:hover { background-color: #616161 !important; }
    .disabled-button {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
        pointer-events: none !important;
    }

    /* Inhaltscontainer */
    .markdown p {
        margin-bottom: 1em;
        line-height: 1.6;
    }
    .topic-label {
        text-align: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 12px;
        margin-bottom: 0px;
    }
    .question-container, .feedback-container {
        margin-top: 0px;
        padding: 16px;
        border-left: 4px solid #3a3a3a;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0 6px 6px 0;
    }
    .feedback-container { margin-bottom: 12px; }

    /* Integrierte Container */
    .integrated-question, .integrated-feedback {
        margin-top: 0;
        padding: 16px;
        border: 1px solid #3a3a3a;
        border-left: 4px solid #3a3a3a;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0 6px 6px 0;
    }
    .question-header, .score-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .question-title, .score-title {
        font-weight: 600;
        font-size: 1.1rem;
    }

    /* Bewertungselemente */
    .score-bar-container {
        height: 24px;
        background-color: #3a3a3a;
        border-radius: 12px;
        overflow: hidden;
        margin: 16px 0;
        position: relative;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
    }
    .score-bar {
        height: 100%;
        border-radius: 12px;
        transition: width 0.8s ease-in-out, background-color 0.8s ease-in-out;
    }
    .score-value {
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 18px;
        color: #ffffff;
        text-align: center;
        letter-spacing: 0.02em;
    }
    .score-value-inline {
        font-size: 1.2rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 12px;
        background-color: rgba(0, 0, 0, 0.2);
    }

    /* Button-Zeile */
    .button-row {
        margin-top: 0px;
        margin-bottom: 12px;
        gap: 16px;
        padding-top: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    .button-row > div { flex: 1; }

    /* Bewertungsbuttons style */
    .button-with-score {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .button-score {
        font-weight: bold;
        margin-left: 10px;
    }
    .theme-with-percentage {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .theme-percentage-container {
        display: flex;
        align-items: center;
        width: 150px;
        margin-left: 10px;
    }
    .theme-percentage-bar {
        height: 10px;
        border-radius: 5px;
        margin-right: 5px;
    }
    .theme-percentage-value {
        font-weight: bold;
        min-width: 50px;
        text-align: right;
    }
    .score-button {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        text-align: left !important;
    }
</style>
"""
