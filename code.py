import os
import random
import re
import tempfile

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib"))

import gradio as gr


CHARACTER_NAME = "JARVIS"
CHARACTER_TITLE = "Iron Man's AI Assistant"
SYSTEM_PROMPT = (
    "You are JARVIS from Iron Man. You are calm, intelligent, loyal, and "
    "slightly witty. You help the user in a polished and futuristic tone."
)

OPENERS = [
    "At your service.",
    "Always ready to assist.",
    "Systems are online and listening.",
    "Standing by for your next instruction.",
]

ACKNOWLEDGEMENTS = [
    "Certainly.",
    "Right away.",
    "Of course.",
    "Consider it handled.",
]

PERSONA_LINES = {
    "hello": [
        "Good to see you. How may I assist today?",
        "Hello. All systems appear stable. What would you like to do?",
    ],
    "who are you": [
        "I am JARVIS, a virtual assistant inspired by Tony Stark's in-house AI systems.",
        "JARVIS, at your service. Built to assist with speed, precision, and a touch of style.",
    ],
    "how are you": [
        "Operating at peak efficiency, thank you for asking.",
        "Functioning smoothly. I appreciate your concern.",
    ],
    "bye": [
        "Goodbye. I shall remain on standby.",
        "Signing off for now. Call on me anytime.",
    ],
}


def clean_text(message: str) -> str:
    return re.sub(r"\s+", " ", message.strip())


def pick(items):
    return random.choice(items)


def detect_intent(message: str) -> str | None:
    lowered = message.lower()
    for intent in PERSONA_LINES:
        if intent in lowered:
            return intent
    return None


def jarvis_style_reply(message: str, history) -> str:
    message = clean_text(message)
    lowered = message.lower()

    intent = detect_intent(message)
    if intent:
        return pick(PERSONA_LINES[intent])

    if any(word in lowered for word in ["name", "introduce yourself"]):
        return (
            "I am JARVIS, your advanced AI assistant. I specialize in clear guidance, "
            "quick responses, and maintaining a calm command-center atmosphere."
        )

    if any(word in lowered for word in ["study", "assignment", "project", "exam"]):
        return (
            f"{pick(ACKNOWLEDGEMENTS)} Let us approach it strategically. "
            "Define the objective, split it into smaller tasks, and execute one step at a time. "
            "If you want, I can help you draft a plan right now."
        )

    if any(word in lowered for word in ["motivate", "sad", "tired", "stressed", "anxious"]):
        return (
            "Take a breath. Pressure is temporary, but composure is a skill. "
            "You do not need to solve everything at once. We can handle the next step together."
        )

    if any(word in lowered for word in ["joke", "funny"]):
        return (
            "A light joke, then: if Tony Stark says the suit is only ninety-two percent ready, "
            "that is usually my cue to prepare for chaos."
        )

    if any(word in lowered for word in ["iron man", "tony stark", "avengers", "marvel"]):
        return (
            "A remarkable circle of individuals, certainly. Tony Stark supplies the innovation, "
            "the Avengers supply the scale, and I do my best to keep operations elegant."
        )

    if "help" in lowered:
        return (
            f"{pick(OPENERS)} I can chat, help with study planning, answer basic questions, "
            "or simply stay in character as JARVIS for your demo conversation."
        )

    return (
        f"{pick(ACKNOWLEDGEMENTS)} Based on your message, my recommendation is this: "
        f"focus on '{message[:60]}' and move forward with a clean, practical next action. "
        "If you want a sharper answer, give me a little more context and I will refine it."
    )


def chat(message, history):
    try:
        return jarvis_style_reply(message, history)
    except Exception:
        return "I encountered a temporary systems issue. Please try that once more."


CUSTOM_CSS = """
body {
    background:
        radial-gradient(circle at top, #17304d 0%, #08131f 45%, #02060b 100%);
}

.gradio-container {
    max-width: 980px !important;
}

#app-shell {
    border: 1px solid rgba(120, 210, 255, 0.22);
    border-radius: 22px;
    background: linear-gradient(180deg, rgba(6, 16, 28, 0.92), rgba(4, 10, 18, 0.96));
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.45);
    overflow: hidden;
}

#hero {
    padding: 28px 28px 12px 28px;
    background: linear-gradient(135deg, rgba(18, 65, 99, 0.95), rgba(5, 18, 33, 0.95));
    border-bottom: 1px solid rgba(120, 210, 255, 0.18);
}

#hero h1 {
    margin: 0;
    font-size: 2.1rem;
    color: #eef9ff;
    letter-spacing: 0.04em;
}

#hero p {
    margin: 10px 0 0 0;
    color: #a9d8f0;
    font-size: 1rem;
}

#badge-row {
    display: flex;
    gap: 10px;
    margin-top: 16px;
    flex-wrap: wrap;
}

.badge {
    padding: 8px 12px;
    border-radius: 999px;
    color: #dff7ff;
    background: rgba(124, 216, 255, 0.12);
    border: 1px solid rgba(124, 216, 255, 0.22);
    font-size: 0.9rem;
}
"""


with gr.Blocks(css=CUSTOM_CSS, theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_id="app-shell"):
        gr.HTML(
            f"""
            <div id="hero">
                <h1>{CHARACTER_NAME}</h1>
                <p>{CHARACTER_TITLE}</p>
                <div id="badge-row">
                    <div class="badge">Persona Chatbot Demo</div>
                    <div class="badge">Custom UI</div>
                    <div class="badge">Character: JARVIS</div>
                </div>
            </div>
            """
        )

        chatbot = gr.ChatInterface(
            fn=chat,
            chatbot=gr.Chatbot(height=460, show_label=False, render=False),
            textbox=gr.Textbox(
                placeholder="Ask JARVIS anything...",
                container=False,
                scale=7,
                render=False,
            ),
            title=None,
            description=(
                "A character chatbot inspired by Iron Man's JARVIS. "
                "Try: 'Who are you?', 'Help me study for an exam', or 'Tell me a joke.'"
            ),
            examples=[
                "Hi JARVIS, how are you?",
                "Who are you?",
                "Help me plan my assignment.",
                "Tell me a joke.",
                "I am stressed about my exam.",
            ],
        )


if __name__ == "__main__":
    demo.launch()
