---
title: AI Chat App
sdk: gradio
sdk_version: "4.0"
app_file: app.py
pinned: true
---

# AI Chat App

A fully deployable Gradio AI chat application that streams responses from the
Hugging Face Inference API.

[![Deploy to Hugging Face Spaces](https://img.shields.io/badge/Deploy-HF%20Spaces-blue)](https://huggingface.co/new-space?template=gradio)

## Features

- Streaming, token-by-token chat responses.
- Conversation history preserved across turns.
- Runtime controls for temperature, top-p, and max tokens.
- Editable system prompt.
- Clear button to reset the conversation.
- Friendly error handling that keeps the UI responsive.

## Local Development

1. Clone the repository and create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file (see `.env.example`) and add your Hugging Face token if
   needed for gated models.
4. Run the app:
   ```bash
   python app.py
   ```
5. Open the local URL shown in the terminal.

## Hugging Face Spaces Deployment

1. Create a Space with **SDK: Gradio**.
2. Add `HF_TOKEN` under **Settings → Secrets** if you plan to use gated models.
3. Push this repository to the Space—no additional configuration required.

## Functional Requirements Checklist

- [x] Chat is fully streamed token by token.
- [x] Conversation history is maintained across turns in a session.
- [x] User can adjust temperature, top-p, and max tokens live.
- [x] System prompt is editable at runtime.
- [x] Clear button resets the full conversation.
- [x] Errors are caught and displayed in the UI.
- [x] App reads `HF_TOKEN` from environment (dotenv locally, HF Secrets in prod).
- [x] Repo can be pushed to HF Spaces and works immediately.

## Notes

- No external database or persistent storage is used.
- The app relies solely on the Hugging Face Inference API (no local model load).
- Default model: `mistralai/Mistral-7B-Instruct-v0.3` (free-tier compatible).
