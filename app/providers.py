# Placeholder for app/providers.py
import os
import httpx


class LLMProvider:
    def __init__(self):
        self.mode = os.getenv("LLM_MODE") #, "local")
        self.session = httpx.Client(timeout=60.0)

    def chat(self, messages):
        if self.mode == "local":
            return self._chat_ollama(messages)
        return self._chat_hosted(messages)

    def _chat_ollama(self, messages):
        base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        prompt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
        r = self.session.post(
            f"{base}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
        )
        r.raise_for_status()
        return r.json().get("response", "")

    def _hosted_headers(self):
        if os.getenv("OPENROUTER_API_KEY"):
            
            return (
                {
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    "HTTP-Referer": "https://localhost",
                    "X-Title": "ARC RAG",
                },
                "https://openrouter.ai/api/v1/chat/completions",
                os.getenv("OPENROUTER_MODEL"),
            )
        if os.getenv("TOGETHER_API_KEY"):
            
            return (
                {"Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}"},
                "https://api.together.xyz/v1/chat/completions",
                os.getenv(
                    "TOGETHER_MODEL", "meta-llama/Llama-3-8b-Instruct-Turbo"
                ),
            )
        if os.getenv("HF_API_KEY"):
            return (
                {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"},
                f"https://api-inference.huggingface.co/models/{os.getenv('HF_MODEL','HuggingFaceH4/zephyr-7b-beta')}",
                None,
            )
        raise RuntimeError("No hosted LLM credentials found")

    def _chat_hosted(self, messages):
        headers, url, model = self._hosted_headers()
        if "openrouter.ai" in url or "together.xyz" in url:
            payload = {"model": model, "messages": messages, "temperature": 0.2}
            r = self.session.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]

        # HF simple endpoint expects single prompt
        prompt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
        r = self.session.post(
            url,
            headers=headers,
            json={"inputs": prompt, "parameters": {"temperature": 0.2}},
        )
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data:
            return data[0].get("generated_text", "")
        return str(data)
