# Domain-Specific AI Chatbot

A domain-aware chatbot built with Streamlit, integrating **Gemma 3**, **TinyLLaMA**, and **Qwen 3** language models to answer questions only within a selected knowledge domain.

## Problem Statement

Most general-purpose AI chatbots respond to all types of user inputs, often without understanding the intended subject area. This results in off-topic answers, hallucinated facts, and reduced trust in AI-generated content—especially in sensitive or specialized domains such as science, medicine, or the arts.

## Solution

This project implements a **domain-restricted chatbot** that responds **only to questions within a selected subject area**. It uses custom prompting techniques and domain guardrails to ensure:

- No off-topic responses
- Clear and concise domain-specific reasoning
- Proper refusal for out-of-domain queries
- A structured and safe answer format

The chatbot is wrapped in a visually appealing, responsive **Streamlit interface**, including:

- Model selector (Gemma 3, TinyLLaMA, Qwen 3)
- Domain selector (e.g., Science, IT, Medical, Arts)
- Styled background and UI elements
- On-device model serving via `ollama` or any local LLM endpoint

## Features

- Strict domain-aligned behavior with in-prompt refusal logic
- Support for multiple LLMs through a unified backend
- Modular and easily extendable codebase
- Optional OpenAI zero-shot classification for domain-checking
- Customized prompt templates for each model
- Light/dark themed interface with modern CSS styling

## Requirements

- Python 3.8+
- `streamlit`
- `requests`
- `Pillow` (for image handling)
- Local Ollama server or endpoint compatible with your selected models
- Optional: OpenAI key if using GPT-3.5 for off-topic classification

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
