import os
import json
import httpx
import re
from typing import Any, Dict, List

INFERENCE_ENDPOINT = "https://inference.do-ai.run/v1/chat/completions"
DEFAULT_MODEL = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")
AUTH_TOKEN = os.getenv("DIGITALOCEAN_INFERENCE_KEY")

def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

def _coerce_unstructured_payload(raw_text: str) -> Dict[str, Any]:
    compact = raw_text.strip()
    tags = [part.strip(" -•\t") for part in re.split(r",|\\n", compact) if part.strip(" -•\t")]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact,
        "tags": tags[:6],
    }


async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=90.0) as client:
        try:
            resp = await client.post(INFERENCE_ENDPOINT, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Assume the LLM returns a 'content' field with possible markdown
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not content:
                raise ValueError("Empty content from inference")
            json_str = _extract_json(content)
            return json.loads(json_str)
        except Exception as e:
            # Fallback payload
            return {"note": f"AI service unavailable: {str(e)}"}

async def generate_coaching_suggestion(habit_name: str, recent_checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    system_prompt = (
        "You are an AI habit‑coach. Provide a concise coaching suggestion for the given habit. "
        "Include a short reason and a confidence score (0‑1). Return a JSON object with keys: "
        "'suggestion', 'reason', 'confidence_score'."
    )
    user_prompt = json.dumps({"habit": habit_name, "recent_checks": recent_checks})
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return await _call_inference(messages)

async def generate_weekly_insights(summary: List[Dict[str, Any]]) -> Dict[str, Any]:
    system_prompt = (
        "You are an AI analyst for habit tracking. Based on the weekly summary, produce a short insight text "
        "that highlights trends, strengths, and suggestions. Return JSON with keys: 'insight', 'recommendation'."
    )
    user_prompt = json.dumps({"weekly_summary": summary})
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return await _call_inference(messages)
