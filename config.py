# PC #1 - Council Member 1 (+ Frontend)
MEMBER1_IP = "10.15.57.177"
MEMBER1_PORT = 5001

# PC #2 - Council Member 2
MEMBER2_IP = "10.15.57.142"
MEMBER2_PORT = 5002

# PC #3 - Chairman
CHAIRMAN_IP = "10.15.57.84"
CHAIRMAN_PORT = 5000

# Frontend Port (runs on PC #1)
FRONTEND_PORT = 8080

# Download the models with : ollama pull <model_name>

MEMBER1_MODEL = "llama2:7b"
MEMBER2_MODEL = "mistral:7b"
CHAIRMAN_MODEL = "phi"

# Default Ollama host (usually doesn't need to change)
OLLAMA_HOST = "http://localhost:11434"

MEMBER1_URL = f"http://{MEMBER1_IP}:{MEMBER1_PORT}"
MEMBER2_URL = f"http://{MEMBER2_IP}:{MEMBER2_PORT}"
CHAIRMAN_URL = f"http://{CHAIRMAN_IP}:{CHAIRMAN_PORT}"

COUNCIL_MEMBERS = [
    {
        'id': 'member1',
        'url': MEMBER1_URL,
        'model': MEMBER1_MODEL
    },
    {
        'id': 'member2',
        'url': MEMBER2_URL,
        'model': MEMBER2_MODEL
    }
]

def print_config():
    """Print current configuration for verification"""
    print("=" * 60)
    print("LLM COUNCIL CONFIGURATION")
    print("=" * 60)
    print(f"\nCouncil Member 1:")
    print(f"  IP:    {MEMBER1_IP}")
    print(f"  Port:  {MEMBER1_PORT}")
    print(f"  Model: {MEMBER1_MODEL}")
    print(f"  URL:   {MEMBER1_URL}")
    
    print(f"\nCouncil Member 2:")
    print(f"  IP:    {MEMBER2_IP}")
    print(f"  Port:  {MEMBER2_PORT}")
    print(f"  Model: {MEMBER2_MODEL}")
    print(f"  URL:   {MEMBER2_URL}")
    
    print(f"\nChairman:")
    print(f"  IP:    {CHAIRMAN_IP}")
    print(f"  Port:  {CHAIRMAN_PORT}")
    print(f"  Model: {CHAIRMAN_MODEL}")
    print(f"  URL:   {CHAIRMAN_URL}")
    
    print(f"\nFrontend:")
    print(f"  Port:  {FRONTEND_PORT}")
    print(f"  Access: http://{MEMBER1_IP}:{FRONTEND_PORT}")
    print("=" * 60)

if __name__ == "__main__":
    print_config()