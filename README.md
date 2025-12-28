# 🐍 Nexus Gateway Python SDK

The official Python client for **Nexus Gateway**.

This library provides a simple interface to interact with the Nexus Gateway API, enabling semantic caching, multi-model routing, and automated cost optimization for LLM applications.

<br>

## 📦 Installation

You can install the package via pip:

```bash
pip install nexus-gateway
(For local development, you can run pip install . in the root directory)
<br>
🔑 Authentication
To use this SDK, you require a valid API Key.
Get your Free API Key here
<br>
🚀 Usage
Basic Example
Initialize the client with your API key and send a message. By default, requests are routed to gpt-3.5-turbo.
code
Python
from nexus_gateway import NexusClient

# 1. Initialize the Client
# Replace 'nk-...' with your actual key from the dashboard
client = NexusClient(api_key="nk-your-key-here")

# 2. Send request
try:
    response = client.chat("Explain quantum computing in one sentence.")
    print(response)
except Exception as e:
    print(f"Error: {e}")
<br>
🤖 Advanced Usage
Switching Models (Universal Router)
Nexus Gateway acts as a unified interface for multiple AI providers. You can specify the model parameter to switch providers dynamically without changing your client logic.
Using Anthropic (Claude 3):
code
Python
response = client.chat(
    message="Write a Python script to sort a list.", 
    model="claude-3-opus-20240229"
)
Using OpenAI (GPT-4):
code
Python
response = client.chat(
    message="Explain the theory of relativity.", 
    model="gpt-4"
)
<br>
✨ Key Features
Semantic Caching: Responses are cached using vector embeddings. Similar queries return cached results instantly.
Unified Interface: Switch between OpenAI and Anthropic models without changing your underlying code.
Rate Limiting: Built-in protection against API abuse.
Automated Billing: Usage is tracked automatically via the gateway.
<br>
License
MIT License © 2025 Sunny Anand
code
Code
5.  Click **"Commit changes"**.

**This version uses `<br>` tags to force spacing.** It will look clean and structured like a real Google Doc or professional library. 📄✨