from __future__ import annotations

import json
from typing import Any, Dict, List

import requests

from .config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    LLM_PROVIDER,
    OLLAMA_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    USE_OLLAMA,
)


def build_rag_prompt(question: str, contexts: List[Dict[str, Any]]) -> str:
    """Construct a prompt that forces grounding in retrieved chunks."""
    context_blocks = []
    for i, c in enumerate(contexts, start=1):
        context_blocks.append(
            f"[Chunk {i} | source={c.get('source')} | score={c.get('score'):.3f}]\n{c.get('text')}"
        )
    context_text = "\n\n".join(context_blocks) if context_blocks else "No context retrieved."

    instructions = (
        "You are an AI assistant for a construction marketplace.\n"
        "You must answer ONLY using the information in the provided document chunks.\n"
        "If the answer is not present in the context, say you don't know based on the documents.\n"
        "Do not invent policies, facts, or numbers not supported by the context.\n"
        "Provide a clear, concise answer without suggesting follow-up questions.\n"
    )

    prompt = f"{instructions}\n\nContext:\n{context_text}\n\nQuestion: {question}\n\nAnswer:"
    return prompt


def call_openrouter(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        return "[Error] OPENROUTER_API_KEY not configured."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    body: Dict[str, Any] = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful, grounded assistant."},
            {"role": "user", "content": prompt},
        ],
    }
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(body))
    if resp.status_code != 200:
        return f"[Error] OpenRouter API error: {resp.status_code} {resp.text}"
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "[Error] Unexpected OpenRouter response format."


def call_groq(prompt: str) -> str:
    """Call Groq API for ultra-fast inference."""
    if not GROQ_API_KEY:
        return "[Error] GROQ_API_KEY not configured."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    body: Dict[str, Any] = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful, grounded assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 1024,
    }
    try:
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body, timeout=30)
    except requests.exceptions.RequestException as e:
        return f"[Error] Could not reach Groq API: {e}"
    
    if resp.status_code != 200:
        return f"[Error] Groq API error: {resp.status_code} {resp.text}"
    
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "[Error] Unexpected Groq response format."


def call_ollama(prompt: str) -> str:
    if not USE_OLLAMA:
        return "[Error] Offline LLM (Ollama) not enabled. Set USE_OLLAMA=true in .env."

    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=60,
        )
    except Exception as e:  # noqa: BLE001
        return f"[Error] Could not reach Ollama: {e}"

    if resp.status_code != 200:
        return f"[Error] Ollama error: {resp.status_code} {resp.text}"

    data = resp.json()
    return data.get("response", "[Error] Unexpected Ollama response format.")


def generate_answer(question: str, contexts: List[Dict[str, Any]], mode: str = "online") -> str:
    """Generate answer using configured LLM provider."""
    prompt = build_rag_prompt(question, contexts)
    
    if mode == "offline":
        return call_ollama(prompt)
    
    # Online mode - use configured provider
    if LLM_PROVIDER == "groq":
        return call_groq(prompt)
    elif LLM_PROVIDER == "openrouter":
        return call_openrouter(prompt)
    else:
        # Default to Groq
        return call_groq(prompt)

