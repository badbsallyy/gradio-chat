import os
from typing import Dict, List

import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

import config

load_dotenv()


def get_client(model_id: str) -> InferenceClient:
    token = os.getenv("HF_TOKEN")
    return InferenceClient(model=model_id, token=token)


def to_chatbot(messages: List[Dict[str, str]]) -> List[List[str]]:
    chat_pairs = []
    user_message = None
    for message in messages:
        if message["role"] == "user":
            user_message = message["content"]
        elif message["role"] == "assistant":
            if user_message is None:
                user_message = ""
            chat_pairs.append([user_message, message["content"]])
            user_message = None
    if user_message is not None:
        chat_pairs.append([user_message, ""])
    return chat_pairs


def build_prompt(messages: List[Dict[str, str]], system_prompt: str) -> str:
    prompt = ""
    first_user = True
    for message in messages:
        if message["role"] == "user":
            if first_user:
                sys_block = f"<<SYS>>\n{system_prompt}\n<</SYS>>\n\n"
                prompt += f"<s>[INST] {sys_block}{message['content']} [/INST]"
                first_user = False
            else:
                prompt += f"<s>[INST] {message['content']} [/INST]"
        elif message["role"] == "assistant":
            prompt += f" {message['content']} </s>"
    return prompt


def respond(
    message: str,
    history: List[Dict[str, str]],
    system_prompt: str,
    temperature: float,
    top_p: float,
    max_new_tokens: int,
):
    if not message:
        return

    conversation = list(history or [])
    conversation.append({"role": "user", "content": message})
    yield to_chatbot(conversation), conversation, ""

    prompt = build_prompt(conversation, system_prompt)
    try:
        client = get_client(config.DEFAULT_MODEL)
        stream = client.text_generation(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=config.REPETITION_PENALTY,
            stream=True,
        )
        assistant_message = ""
        for chunk in stream:
            assistant_message += chunk.token.text
            updated = conversation + [
                {"role": "assistant", "content": assistant_message}
            ]
            yield to_chatbot(updated), updated, ""
        conversation.append({"role": "assistant", "content": assistant_message})
        yield to_chatbot(conversation), conversation, ""
    except Exception as exc:
        error_message = (
            "⚠️ The model could not be reached. "
            "Please verify your HF_TOKEN or try again later.\n\n"
            f"Details: {exc}"
        )
        conversation.append({"role": "assistant", "content": error_message})
        yield to_chatbot(conversation), conversation, ""


def clear_chat():
    return [], [], ""


with gr.Blocks(title="AI Chat App") as demo:
    gr.Markdown("# AI Chat App")
    gr.Markdown(
        "Chat with an AI model hosted on Hugging Face using the Inference API."
    )

    state = gr.State([])

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(height=420)
            user_input = gr.Textbox(
                label="Your message",
                placeholder="Type a message and press Send",
                lines=2,
            )
            with gr.Row():
                send_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("Clear")
        with gr.Column(scale=1):
            with gr.Accordion("Settings", open=False):
                system_prompt_input = gr.Textbox(
                    label="System prompt",
                    value=config.SYSTEM_PROMPT,
                    lines=4,
                )
                temperature_input = gr.Slider(
                    label="Temperature",
                    minimum=0.0,
                    maximum=1.5,
                    step=0.05,
                    value=config.TEMPERATURE,
                )
                top_p_input = gr.Slider(
                    label="Top-p",
                    minimum=0.0,
                    maximum=1.0,
                    step=0.05,
                    value=config.TOP_P,
                )
                max_tokens_input = gr.Slider(
                    label="Max new tokens",
                    minimum=32,
                    maximum=2048,
                    step=32,
                    value=config.MAX_NEW_TOKENS,
                )

    send_btn.click(
        respond,
        inputs=[
            user_input,
            state,
            system_prompt_input,
            temperature_input,
            top_p_input,
            max_tokens_input,
        ],
        outputs=[chatbot, state, user_input],
    )
    user_input.submit(
        respond,
        inputs=[
            user_input,
            state,
            system_prompt_input,
            temperature_input,
            top_p_input,
            max_tokens_input,
        ],
        outputs=[chatbot, state, user_input],
    )
    clear_btn.click(clear_chat, outputs=[chatbot, state, user_input])


if __name__ == "__main__":
    demo.launch()
