css_func = """
<style>
    /* Import a more modern font */
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

    /* Apply base typography */
    body, .gradio-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        line-height: 1.5;
        letter-spacing: 0.015em;
    }

    /* Heading styling */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        letter-spacing: -0.01em;
        margin-bottom: 0.8em;
        margin-top: 0.5em;
    }

    h2 {
        font-size: 1.75rem;
        letter-spacing: -0.02em;
    }

    h3 {
        font-size: 1.35rem;
        margin-bottom: 0.6em;
    }

    /* Accordion styling */
    .accordion {
        margin-bottom: 12px;
    }

    .accordion-header {
        font-weight: 500;
        letter-spacing: 0.01em;
    }

    /* Content spacing */
    .gradio-container .prose {
        max-width: none;
    }

    /* Better textbox styling */
    textarea, input[type="text"] {
        font-size: 1rem;
        line-height: 1.5;
        padding: 12px 16px !important;
        border-radius: 6px !important;
    }

    /* Label styling */
    label {
        font-weight: 500;
        margin-bottom: 6px;
        font-size: 0.95rem;
    }

    /* Button styling */
    button {
        font-weight: 500 !important;
        letter-spacing: 0.01em;
        padding: 8px 16px !important;
        border-radius: 6px !important;
        transition: all 0.2s ease;
    }

    /* Improved markdown rendering */
    .markdown p {
        margin-bottom: 1em;
        line-height: 1.6;
    }

    /* Hide clear button */
    button[aria-label="Clear"] {
        display: none !important;
    }

    /* Score bar styling */
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

    /* Improved score value display */
    .score-value {
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 18px;
        color: #ffffff;
        text-align: center;
        letter-spacing: 0.02em;
    }

    /* Feedback container styling */
    .feedback-container {
        margin-top: 0px;
        padding: 16px;
        border-left: 4px solid #3a3a3a;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0 6px 6px 0;
    }

    /* Topic and question styling */
    .topic-label {
        text-align: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 12px;
        margin-bottom: 0px;
    }

    .question-container {
        margin-top: 0px;
        padding: 16px;
        border-left: 4px solid #3a3a3a;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0 6px 6px 0;
    }

    /* Section spacing */
    .section {
        margin-bottom: 10px;  # Reduce from 32px
    }

    # First, let's update the CSS to add styling for the integrated feedback container
# Add these styles to the css_func string:

    /* Integrated feedback container with score */
    .integrated-feedback {
        margin-top: 0;  # Reduce from 24px
        padding: 16px;
        border: 1px solid #3a3a3a;
        border-left: 4px solid #3a3a3a;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0 6px 6px 0;
    }

    .score-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .score-title {
        font-weight: 600;
        font-size: 1.1rem;
    }

    .score-value-inline {
        font-size: 1.2rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 12px;
        background-color: rgba(0, 0, 0, 0.2);
    }

    # First, add a new CSS class for the question container to match the feedback style
# Add this to the css_func string:

    /* Question container styling to match feedback */
    .integrated-question {
        margin-top: 0;  # Reduce from 24px
        padding: 16px;
        border: 1px solid #3a3a3a;
        border-left: 4px solid #3a3a3a;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 0 6px 6px 0;
    }

    .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .question-title {
        font-weight: 600;
        font-size: 1.1rem;
    }

    # First, add these CSS rules to the css_func string to style the buttons:

    /* Theme-colored buttons that fill their container */
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

    .submit-button:hover {
        background-color: #1976D2 !important;
    }

    .back-button {
        background-color: #424242 !important;
        border-color: #616161 !important;
    }

    .back-button:hover {
        background-color: #616161 !important;
    }

    # Add this to the css_func string:

    /* Button row styling */
    .button-row {
        margin-top: 0px;
        gap: 0px;
    }

    /* Ensure columns in button row have equal width */
    .button-row > div {
        flex: 1;
    }

    /* Button row styling with consistent padding */
    .button-row {
        margin-top: 0px;
        margin-bottom: 12px;
        gap: 16px;
        padding-top: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Ensure columns in button row have equal width */
    .button-row > div {
        flex: 1;
    }

    /* Disabled button styling */
    .disabled-button {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
        pointer-events: none !important;
    }

    # Update the CSS to add consistent spacing between elements and the button row:

    /* Add consistent bottom margin to sections before the button row */
    .section {
        margin-bottom: 12px;
    }

    /* Ensure feedback container has proper spacing */
    .feedback-container {
        margin-bottom: 12px;
    }

</style>
"""
