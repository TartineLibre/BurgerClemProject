# LLM Council - Local Deployment

**Team Members:** [Your Names Here]  
**TD Group:** [Your TD Group Number]

## Project Overview

This project implements a distributed LLM Council system where multiple AI models collaborate to answer queries through a three-stage process:

1. **Stage 1 - First Opinions**: Multiple LLMs independently answer the query
2. **Stage 2 - Reviews & Rankings**: LLMs anonymously review and rank each other's answers
3. **Stage 3 - Chairman Synthesis**: A Chairman LLM synthesizes all responses into a final answer

All LLMs run locally using Ollama, with services distributed across 3 separate machines.

## Architecture

```
┌─────────────────┐
│   Frontend      │  ← Any PC on WiFi hotspot
│  (Flask + UI)   │     (e.g., 192.168.137.1:8080)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──────┐ ┌───▼──────┐ ┌────────────┐
│ Member 1 │ │ Member 2 │ │  Chairman  │
│  PC #1   │ │  PC #2   │ │   PC #3    │
│  :5001   │ │  :5002   │ │   :5000    │
└──────────┘ └──────────┘ └────────────┘
```

## Team Setup (3 Students, 3 PCs)

### PC Assignment
- **Student 1 (PC #1)**: Council Member 1 + Frontend
- **Student 2 (PC #2)**: Council Member 2
- **Student 3 (PC #3)**: Chairman

## Prerequisites

### All PCs Need:
1. **Python 3.8+** installed
2. **Ollama** installed ([Download here](https://ollama.ai))
3. Connected to **same WiFi hotspot**

### Install Ollama
```bash
# Windows: Download installer from ollama.ai
# Mac: 
curl -fsSL https://ollama.ai/install.sh | sh
# Linux:
curl -fsSL https://ollama.ai/install.sh | sh
```

### Pull Models (on each PC)
```bash
# On all PCs, download at least one model:
ollama pull llama2
# or
ollama pull mistral
# or
ollama pull phi
```

## Installation Steps

### Step 1: Get IP Addresses

On the **WiFi hotspot host PC**, open Command Prompt (Windows) or Terminal (Mac/Linux):

```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
# or
ip addr show
```

Look for the **WiFi adapter** IP address (usually starts with 192.168.x.x)

**Example scenario:**
- PC #1 (Member 1): 192.168.137.101
- PC #2 (Member 2): 192.168.137.102
- PC #3 (Chairman): 192.168.137.103

### Step 2: Setup on Each PC

#### On ALL PCs:

1. Clone or download this project
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

#### On PC #1 (Council Member 1 + Frontend):

3. **Start Ollama** (if not running):
```bash
ollama serve
```

4. **Run Council Member 1**:
```bash
# Open terminal 1
set MODEL_NAME=llama2
set MEMBER_ID=member1
set PORT=5001
python council_member.py
```

5. **Run Frontend** (in a new terminal):
```bash
# Open terminal 2
# Edit these IPs to match your actual IPs!
set MEMBER1_URL=http://192.168.137.101:5001
set MEMBER2_URL=http://192.168.137.102:5002
set CHAIRMAN_URL=http://192.168.137.103:5000
set PORT=8080
python app.py
```

#### On PC #2 (Council Member 2):

3. **Start Ollama**:
```bash
ollama serve
```

4. **Run Council Member 2**:
```bash
set MODEL_NAME=mistral
set MEMBER_ID=member2
set PORT=5002
python council_member.py
```

#### On PC #3 (Chairman):

3. **Start Ollama**:
```bash
ollama serve
```

4. **Run Chairman**:
```bash
set MODEL_NAME=llama2
set PORT=5000
python chairman.py
```

### Step 3: Test the System

1. On **any PC** connected to the same WiFi, open a browser
2. Go to: `http://192.168.137.101:8080` (replace with PC #1's IP)
3. Click **"Refresh Status"** - all services should show "healthy"
4. Enter a question and click **"Submit to Council"**

## Troubleshooting

### Services Show "Unreachable"

**Problem**: Firewall blocking connections

**Solution**:
```bash
# Windows: Allow Python through firewall
# Go to: Windows Defender Firewall → Allow an app

# Or temporarily disable firewall for testing (not recommended for production)
```

### "Connection refused" errors

**Problem**: Service not running or wrong IP

**Solution**:
1. Verify service is running: `netstat -an | findstr :5001`
2. Double-check IP addresses with `ipconfig`
3. Make sure Ollama is running: `ollama list`

### Slow responses

**Problem**: Models are large and computation-intensive

**Solution**:
- Use smaller models: `ollama pull phi` (2GB) instead of llama2 (7GB)
- Be patient - first run downloads models
- Expect 30-60 seconds per stage

### "Model not found"

**Problem**: Model not downloaded on that PC

**Solution**:
```bash
ollama pull llama2
```

## Quick Reference: Command Cheat Sheet

```bash
# Check if Ollama is running
ollama list

# Download a model
ollama pull llama2

# Test Ollama directly
ollama run llama2 "Hello"

# Check what's using port 5001
netstat -an | findstr :5001

# Find your IP address
ipconfig              # Windows
ifconfig              # Mac/Linux
```

## Models We Used

- **Council Member 1**: llama2 (7B parameters)
- **Council Member 2**: mistral (7B parameters)
- **Chairman**: llama2 (7B parameters)

## Key Design Decisions

1. **Flask for Services**: Lightweight, easy to deploy, standard Python web framework
2. **Ollama for Local LLMs**: Best tool for running LLMs locally with simple API
3. **REST API Communication**: Standard HTTP makes debugging and monitoring easy
4. **Tabbed UI**: Allows inspection of individual model responses
5. **Health Checks**: Real-time monitoring of all services

## Improvements Over Original

1. ✅ **Fully Local**: No cloud APIs, complete privacy
2. ✅ **Distributed Architecture**: Real multi-machine deployment
3. ✅ **Health Monitoring**: Visual status dashboard
4. ✅ **Better UI**: Modern, responsive design with tabs
5. ✅ **Error Handling**: Graceful failures and timeouts
6. ✅ **Easy Configuration**: Environment variables for all settings

## Network Configuration Details

### WiFi Hotspot Setup

The WiFi hotspot creator's PC typically gets IP: `192.168.137.1`

Other devices get IPs like:
- `192.168.137.101`
- `192.168.137.102`
- `192.168.137.103`

### Port Usage

- **Frontend**: 8080
- **Council Member 1**: 5001
- **Council Member 2**: 5002
- **Chairman**: 5000
- **Ollama**: 11434 (default, runs on each PC)

## Testing Checklist

Before the demo:

- [ ] All PCs connected to same WiFi
- [ ] Ollama installed and models downloaded on all PCs
- [ ] Python dependencies installed on all PCs
- [ ] IP addresses identified for all PCs
- [ ] Environment variables set correctly
- [ ] All services start without errors
- [ ] Health check shows all services "healthy"
- [ ] Test query completes successfully through all 3 stages

## Demo Script

1. Show the network setup (3 PCs)
2. Open browser to frontend
3. Click "Refresh Status" → show all healthy
4. Enter query: "What is machine learning?"
5. Show Stage 1: Different answers from each model
6. Show Stage 2: Each model's review/ranking
7. Show Stage 3: Chairman's synthesized answer
8. Optional: Show logs on each PC running

## Generative AI Usage Statement

We used Claude (Anthropic) for:
- Initial code structure and Flask setup
- Debugging network connection issues
- Documentation formatting
- Explaining Ollama API usage

We wrote ourselves:
- Network architecture decisions
- Testing and troubleshooting
- Team coordination
- Final integration and demo preparation

## License

MIT License - Educational Project

## Contact

[Your contact information]

---

**Note**: Remember to replace all example IP addresses with your actual IP addresses!