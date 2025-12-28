from nexus_gateway import NexusClient

print("--- Initializing Nexus Client ---")
client = NexusClient(api_key="nk-3e1778da37c8bfe19dd0c3a8b2ebcb70")

print("Sending request to AI...")
try:
    response = client.chat("Explain quantum computing in one sentence and speed of photon.")
    print("\n✅ AI Response:")
    print(response)
except Exception as e:
    print("\n❌ Error:", e)