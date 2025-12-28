# 🐍 Nexus Gateway Python SDK

The official Python client for **Nexus Gateway** – The High-Performance AI Semantic Caching Layer.

Use this SDK to integrate OpenAI/Anthropic capabilities into your Python apps with **90% lower costs** and **sub-millisecond latency**.

---

##  Installation

```bash
pip install nexus-gateway
(Note: If installing locally from source, run pip install . in the root directory)
🔑 Getting an API Key
You need a valid API Key to use this client.
Get your Free API Key here
🚀 Quick Start
code
Python
from nexus_gateway import NexusClient

# 1. Initialize the Client
client = NexusClient(api_key="nk-your-key-here")

# 2. Chat with AI (Defaults to GPT-3.5)
response = client.chat("Explain quantum computing in one sentence.")

print(response)
# Output: "Quantum computing uses qubits to perform calculations..."
🤖 Switching Models (The Universal Router)
Nexus Gateway supports multiple AI providers. You can switch models instantly without changing your code structure.
Use Claude 3:
code
Python
response = client.chat(
    message="Write a poem about rust.", 
    model="claude-3-opus-20240229"
)
Use GPT-4:
code
Python
response = client.chat(
    message="Complex math problem...", 
    model="gpt-4"
)
✨ Features
⚡ Semantic Caching: Automatically caches responses in Vector DB. Identical or similar queries return instantly.
🔌 Universal API: One interface for OpenAI and Anthropic.
🛡️ Rate Limiting: Built-in protection against spam.
💸 Cost Savings: Reduces API bills by serving cached hits.
License
MIT License © 2025 Sunny Anand