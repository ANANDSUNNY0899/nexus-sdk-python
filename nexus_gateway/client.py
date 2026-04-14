import requests
import json
import time
from typing import Generator, Optional, Union

class NexusClient:
    """
    NEXUS GATEWAY - SOVEREIGN PYTHON SDK
    Inference Control Plane | v3.2.0
    """
    
    def __init__(self, api_key: str, base_url: str = "https://nexusgateway-production.up.railway.app/api"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def validate_key(self) -> bool:
        """Handshake with the Sovereign Registry to verify infrastructure access."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            res = requests.get(f"{self.base_url}/stats", headers=headers, timeout=5)
            return res.status_code == 200
        except Exception:
            return False

    def chat(
        self, 
        message: str, 
        model: str = "llama-3.3-70b-versatile", 
        stream: bool = True, 
        provider_key: Optional[str] = None
    ) -> Union[Generator[str, None, None], str]:
        endpoint = "/chat/stream" if stream else "/chat"
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-Nexus-SDK": "python-v3.2.0"
        }

        if provider_key:
            m = model.lower()
            if any(x in m for x in ["gpt", "o1", "o3"]): 
                headers["x-nexus-openai-key"] = provider_key
            elif any(x in m for x in ["llama", "mixtral", "gemma"]): 
                headers["x-nexus-groq-key"] = provider_key
            elif "gemini" in m: 
                headers["x-nexus-gemini-key"] = provider_key
            elif "claude" in m: 
                headers["x-nexus-anthropic-key"] = provider_key

        # 🚨 THE FIX: Format the payload exactly how the Go Gateway expects it
        payload = {
            "model": model,
            "stream": stream,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        if stream:
            return self._handle_stream(url, payload, headers, model)
        
        response = requests.post(url, json=payload, headers=headers)
        self._check_error(response)
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    def _handle_stream(self, url: str, payload: dict, headers: dict, active_model: str) -> Generator[str, None, None]:
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=60)
        self._check_error(response)

        has_received_any_data = False

        # iter_lines is better now that we know the Go backend is flushing \n\n
        for line in response.iter_lines():
            if not line:
                continue
            
            line_str = line.decode('utf-8', errors='ignore')

            # 1. 🛡️ SILENT HANDSHAKE: Ignore the wakeup comment
            if line_str.startswith(": nexus-handshake-active"):
                continue

            # 2. 🚨 THE RAW ERROR INTERCEPTOR (NEW)
            # Catch upstream provider rejections that bypass the 200 OK
            if not line_str.startswith("data: ") and line_str.startswith("{"):
                try:
                    err_chunk = json.loads(line_str)
                    if "error" in err_chunk:
                        yield f"\n\n[🚨 UPSTREAM PROVIDER REJECTION]: {json.dumps(err_chunk['error'], indent=2)}"
                        return
                except:
                    pass

            # 3. 🛰️ DATA PROCESSING
            if line_str.startswith("data: "):
                content_raw = line_str[6:].strip()
                if content_raw == "[DONE]":
                    break

                try:
                    chunk = json.loads(content_raw)
                    
                    # Search for standard content
                    content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                    
                    # Fallback for Groq/Gemini variants
                    if not content:
                        content = chunk.get("content", "")

                    if content:
                        has_received_any_data = True
                        yield str(content)
                except json.JSONDecodeError:
                    # If it's valid text but not JSON, yield it
                    yield f"\n[RAW_TEXT]: {content_raw}"
        
        if not has_received_any_data:
            yield "\n[Sovereign Note: Connection established, but stream was empty or aborted.]"

    def _check_error(self, response: requests.Response):
        if response.status_code == 401:
            raise Exception("❌ Unauthorized: Invalid Nexus API Key.")
        if response.status_code == 402:
            raise Exception("⛔ Quota Exceeded. Upgrade at dashboard.")
        if response.status_code == 403:
            raise Exception("🛡️ Sovereign Shield: Blocked by governance.")
        if response.status_code >= 400:
            raise Exception(f"🚨 Gateway Error {response.status_code}: {response.text}")