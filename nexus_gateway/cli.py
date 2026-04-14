import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.table import Table
from rich.status import Status
from .client import NexusClient

# Initialize Rich Console
console = Console()

MODEL_ALIASES = {
    "r1": "deepseek-reasoner",
    "llama": "llama-3.3-70b-versatile",
    "gpt4": "gpt-4o",
    "gemini": "gemini-1.5-flash", 
    "google": "gemini-1.5-flash"
}

def print_header():
    header_text = Text("NEXUS GATEWAY | SOVEREIGN CONTROL PLANE v3.2.0", style="bold cyan")
    console.print(Panel(header_text, subtitle="Inference.Protocol.Active", border_style="blue", expand=False))

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header()

    # 1. API Key Handshake
    api_key = os.getenv("NEXUS_API_KEY") or console.input("[bold yellow]🔑 Enter Nexus API Key: [/bold yellow]")
    
    with console.status("[bold blue]Establishing Secure Data Plane connection...", spinner="dots"):
        client = NexusClient(api_key=api_key)
        if not client.validate_key():
            console.print("[bold red]❌ Access Denied: Invalid Infrastructure Key.[/bold red]")
            return
    
    console.print("[bold green]✅ Gateway Connected! Protocol v3.2 Active.[/bold green]\n")

    active_model = "llama-3.3-70b-versatile"

    # 2. Interactive Loop
    while True:
        try:
            # Styled Prompt
            prompt_label = Text(f" nexus@{active_model} ", style="black on green")
            user_input = console.input(f"{prompt_label} [bold white]> [/bold white]").strip()

            if not user_input: continue
            if user_input.lower() in ["exit", "quit"]: break

            # --- 🚀 THE FIX: AGGRESSIVE MODEL COMMAND PARSING ---
            # Handles /model name, /model=name, model=name, or even just /model
            if user_input.startswith("/model") or user_input.startswith("model="):
                # Strip out the command prefixes completely
                parts = user_input.replace("/model", "").replace("model=", "").strip()
                # Clean up any lingering spaces or equals signs
                parts = parts.lstrip(" =")
                
                active_model = MODEL_ALIASES.get(parts.lower(), parts)
                console.print(f"[italic cyan]🔄 Engine Switched -> {active_model}[/italic cyan]\n")
                continue

            # --- INFERENCE EXECUTION ---
            console.print(f"\n[bold blue]Nexus_Node:[/bold blue] ", end="")

            start_time = time.time()
            full_response = ""

            # Unified Streaming Loop (Cleaned of flush=True)
            try:
                for chunk in client.chat(user_input, model=active_model):
                    # Rich handles the streaming automatically without 'flush'
                    console.print(chunk, end="") 
                    full_response += chunk
            except Exception as e:
                console.print(f"\n[bold red]🚨 Streaming Error: {e}[/bold red]")

            # --- TELEMETRY DATA ---
            latency = int((time.time() - start_time) * 1000)
            tokens = len(full_response) // 4
            
            telemetry_table = Table(show_header=False, box=None, padding=(0, 2))
            telemetry_table.add_row(
                f"[dim]Latency: {latency}ms[/dim]",
                f"[dim]Tokens: ~{tokens}[/dim]",
                f"[dim]Layer: Infrastructure[/dim]"
            )
            console.print("\n")
            console.print(telemetry_table)
            console.print("[dim]────────────────────────────────────────────────[/dim]\n")

        except KeyboardInterrupt:
            console.print("\n[bold red]Emergency Shutdown. Secure Data Plane Closed.[/bold red]")
            break

if __name__ == "__main__":
    main()