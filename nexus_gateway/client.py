import requests
import json

class NexusClient:
    def __init__(self, api_key: str, base_url: str = "https://nexusgateway.onrender.com/api"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def validate_key(self) -> bool:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            res = requests.get(f"{self.base_url}/stats", headers=headers, timeout=5)
            return res.status_code == 200
        except: return False

    def chat(self, message: str, model: str = "llama-3.3-70b-versatile", stream: bool = True, provider_key: str = None):
        endpoint = "/chat/stream" if stream else "/chat"
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # 🔐 BYOK AUTO-MAPPING
        if provider_key:
            m = model.lower()
            if "gpt" in m: headers["x-nexus-openai-key"] = provider_key
            elif "llama" in m or "mixtral" in m: headers["x-nexus-groq-key"] = provider_key
            elif "gemini" in m: headers["x-nexus-gemini-key"] = provider_key
            elif "claude" in m: headers["x-nexus-anthropic-key"] = provider_key

        payload = {"message": message, "model": model, "stream": stream}

        if stream:
            return self._handle_stream(url, payload, headers)
        
        response = requests.post(url, json=payload, headers=headers)
        self._check_error(response)
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

    def _handle_stream(self, url, payload, headers):
        response = requests.post(url, json=payload, headers=headers, stream=True)
        self._check_error(response)

        for line in response.iter_lines():
            if not line: continue
            line_str = line.decode('utf-8')
            
            if line_str.startswith("data: "):
                content_raw = line_str[6:].strip()
                if content_raw == "[DONE]": break
                
                try:
                    chunk = json.loads(content_raw)
                    # 🚀 UNIVERSAL PARSING (OpenAI/Groq/Gemini)
                    content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "") or \
                              chunk.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    if content: yield content
                except:
                    if "error" in content_raw.lower(): yield f"\n[Nexus Error]: {content_raw}"

    def _check_error(self, response):
        if response.status_code == 401: raise Exception("❌ Unauthorized: Invalid Nexus API Key")
        if response.status_code == 402: raise Exception("⛔ Quota Exceeded. Upgrade at nexus-gateway.org")
        if response.status_code == 403: raise Exception("🛡️ Sovereign Shield: Request blocked by governance policy.")
        if response.status_code >= 400: raise Exception(f"🚨 API Error {response.status_code}: {response.text}")