import os
import sys
import time
import json
from .client import NexusClient

# 🚀 THE MASTER ALIAS MAP: Full listing of supported infrastructure engines
MODEL_ALIASES = {
    # OpenAI Standard
    "gpt": "gpt-3.5-turbo",
    "gpt3": "gpt-3.5-turbo",
    "gpt4": "gpt-4o",
    "gpt4o": "gpt-4o",
    "mini": "gpt-4o-mini",
    
    # Groq (Ultra-Fast)
    "llama": "llama-3.3-70b-versatile",
    "groq": "llama-3.3-70b-versatile",
    "fast": "llama-3.1-8b-instant",
    "mixtral": "mixtral-8x7b-32768",
    
    # Google (Adaptive)
    "gemini": "gemini-1.5-flash",
    "google": "gemini-1.5-flash",
    "gemini-pro": "gemini-1.5-pro",
    
    # Anthropic (Reasoning)
    "claude": "claude-3-5-sonnet-latest",
    "opus": "claude-3-opus-20240229",
    "sonnet": "claude-3-5-sonnet-latest",
    
    # Aliases
    "pro": "gpt-4o",
    "dev": "llama-3.3-70b-versatile"
}

def main():
    # --- 1. INDUSTRIAL HEADER ---
    print("\n\033[1;34m============================================")
    print("    NEXUS GATEWAY - SOVEREIGN CLI v3.1.3")
    print("    Inference.Control.Plane.Active")
    print("============================================\033[0m")

    # 2. KEY PROVISIONING
    api_key = os.getenv("NEXUS_API_KEY")
    if not api_key:
        try:
            api_key = input("🔑 \033[1mEnter Nexus API Key:\033[0m ").strip()
        except KeyboardInterrupt:
            sys.exit(0)

    # 3. HANDSHAKE
    print("Establishing connection...", end="\r")
    client = NexusClient(api_key=api_key)
    
    if not client.validate_key():
        print("\n\033[1;31m❌ Access Denied: Invalid Infrastructure Key.")
        print("Provision a key at: https://nexus-gateway.org/dashboard\033[0m")
        return

    print("✅ \033[1;32mGateway Connected! Protocol v3.1 Active.\033[0m")
    print("\033[90mShortcuts: model=llama, /key [sk-...], /clear, /exit\033[0m\n")

    # 4. SESSION STATE
    active_model = "llama-3.3-70b-versatile" # 🚀 Default to high-speed Groq
    current_provider_key = None

    # 5. INTERACTIVE COMMAND LOOP
    while True:
        try:
            # Dynamic Prompt Status
            status_line = f"[ {active_model} ]"
            if current_provider_key:
                status_line += " [ 🔐 BYOK ]"
            
            user_input = input(f"\033[1;32m{status_line} > \033[0m").strip()
            if not user_input: continue

            # --- 🚀 1. HIGH-PRIORITY COMMAND PARSER ---
            cmd = user_input.lower()
            
            # A. Handle BYOK Key (/key sk-...)
            if cmd.startswith("/key"):
                parts = user_input.split(" ")
                if len(parts) > 1:
                    current_provider_key = parts[1].strip()
                    print("🔐 \033[1;33mProvider Key Injected. Bypassing Nexus credits...\033[0m\n")
                else:
                    current_provider_key = None
                    print("🔓 \033[1;33mProvider Key Removed. Using Nexus credits...\033[0m\n")
                continue

            # B. Handle Model Switch (model=name, /model name)
            if ("=" in cmd and "model" in cmd) or cmd.startswith("/model"):
                val = ""
                if "=" in cmd:
                    val = cmd.split("=")[1].strip()
                else:
                    parts = cmd.split(" ")
                    if len(parts) > 1: val = parts[1].strip()
                
                if val:
                    active_model = MODEL_ALIASES.get(val.lower(), val)
                    print(f"🔄 \033[1;36mEngine Switched -> {active_model}\033[0m\n")
                continue

            # C. System Commands
            if cmd in ["exit", "quit", "/exit"]:
                print("\033[1;34mTerminating Session. Secure Data Plane Closed. 👋\033[0m")
                break
            if cmd in ["/clear", "clear"]:
                os.system('cls' if os.name == 'nt' else 'clear')
                continue

            # --- 🚀 2. INFERENCE EXECUTION ---
            print("\033[1;34mNexus:\033[0m ", end="", flush=True)
            
            start_time = time.time()
            full_response = ""
            has_received_data = False

            try:
                # Direct Stream from Sovereign Bridge
                for chunk in client.chat(
                    user_input, 
                    model=active_model, 
                    stream=True, 
                    provider_key=current_provider_key
                ):
                    print(chunk, end="", flush=True)
                    full_response += chunk
                    has_received_data = True
                
                if not has_received_data:
                    print("\033[33mNo response data received from provider.\033[0m")

                # 📊 TELEMETRY LEDGER
                latency = int((time.time() - start_time) * 1000)
                tokens = len(full_response) // 4
                print(f"\n\n\033[90m[ {latency}ms | {tokens} tokens | Layer: Infrastructure ]\033[0m\n")
                
            except Exception as e:
                print(f"\n\033[1;31m{e}\033[0m\n")

        except KeyboardInterrupt:
            print("\n\033[1;34mEmergency Shutdown. Goodbye! 👋\033[0m")
            break

if __name__ == "__main__":
    main()