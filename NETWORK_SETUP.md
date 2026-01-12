# Quick Start Guide - WiFi Hotspot Setup

## 🚀 For Your 3-Person Team

### Before You Start

**One person creates a WiFi hotspot**, the other two connect to it.

---

## Step 1: Create WiFi Hotspot (Friend's PC)

### On Windows:
1. Go to **Settings** → **Network & Internet** → **Mobile hotspot**
2. Turn on **Mobile hotspot**
3. Note the **network name** and **password**
4. Share these with your teammates

### On Mac:
1. Go to **System Preferences** → **Sharing**
2. Enable **Internet Sharing**
3. Share connection via **Wi-Fi**

---

## Step 2: Connect Everyone

1. **All 3 PCs** connect to the same WiFi hotspot
2. The hotspot creator's PC is usually at `192.168.137.1`

---

## Step 3: Find IP Addresses

On **each PC**, open Command Prompt (Windows) or Terminal (Mac):

```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

Look for the **WiFi adapter** IP address.

**Write them down:**
- PC #1: _________________ (Will run Member 1 + Frontend)
- PC #2: _________________ (Will run Member 2)
- PC #3: _________________ (Will run Chairman)

---

## Step 4: Install Everything (On ALL PCs)

### 4.1 Install Ollama

Go to https://ollama.ai and download the installer for your OS.

After installation, open a terminal and download models:

```bash
ollama pull llama2
# Wait 5-10 minutes for download
```

Optional - download more models:
```bash
ollama pull mistral
ollama pull phi
```

### 4.2 Install Python Dependencies

In your project folder:

```bash
pip install -r requirements.txt
```

---

## Step 5: Edit Configuration

**IMPORTANT**: On PC #1 (where you'll run the frontend), edit `config.py`:

```python
# Replace with YOUR actual IP addresses!
MEMBER1_IP = "192.168.137.101"  # PC #1's IP
MEMBER2_IP = "192.168.137.102"  # PC #2's IP
CHAIRMAN_IP = "192.168.137.103"  # PC #3's IP
```

Save the file!

---

## Step 6: Start Services

### On PC #1 (Student 1):

**Terminal 1** - Start Council Member 1:
```bash
python council_member.py
```
When prompted, or if you need to set manually:
```bash
# Windows
set MODEL_NAME=llama2
set MEMBER_ID=member1
set PORT=5001
python council_member.py

# Mac/Linux
export MODEL_NAME=llama2
export MEMBER_ID=member1
export PORT=5001
python council_member.py
```

**Terminal 2** - Start Frontend:
```bash
python app_with_config.py
```

### On PC #2 (Student 2):

**Terminal 1** - Start Council Member 2:
```bash
python council_member.py
```
Or manually:
```bash
# Windows
set MODEL_NAME=mistral
set MEMBER_ID=member2
set PORT=5002
python council_member.py

# Mac/Linux
export MODEL_NAME=mistral
export MEMBER_ID=member2
export PORT=5002
python council_member.py
```

### On PC #3 (Student 3):

**Terminal 1** - Start Chairman:
```bash
python chairman.py
```
Or manually:
```bash
# Windows
set MODEL_NAME=llama2
set PORT=5000
python chairman.py

# Mac/Linux
export MODEL_NAME=llama2
export PORT=5000
python chairman.py
```

---

## Step 7: Test It!

1. On **ANY PC** (even your phone!), open a web browser
2. Go to: `http://192.168.137.101:8080` (replace with PC #1's IP)
3. Click **"Refresh Status"**
   - All services should show **"healthy"** (green)
4. Type a question: **"What is artificial intelligence?"**
5. Click **"Submit to Council"**
6. Wait 30-60 seconds
7. See the results! 🎉

---

## Troubleshooting

### ❌ Service shows "Unreachable"

**Solution 1**: Check firewall
- Windows: Allow Python through Windows Firewall
- Temporarily disable firewall for testing

**Solution 2**: Verify service is running
```bash
# Check if service is listening
netstat -an | findstr :5001
```

**Solution 3**: Double-check IP addresses
- Run `ipconfig` again
- Make sure IPs in `config.py` match

### ❌ "Model not found"

**Solution**: Download the model
```bash
ollama pull llama2
```

### ❌ Very slow responses

**Solution**: This is normal!
- First request takes longer (loading model)
- Large models take time to think
- Expected: 30-60 seconds per stage

### ❌ Can't access frontend from other PC

**Solution**: 
1. Check if PC #1's firewall allows incoming connections
2. Try accessing from PC #1 first: `http://localhost:8080`
3. If that works, it's a firewall issue

---

## Quick Commands Reference

```bash
# Check if Ollama is running
ollama list

# Test Ollama
ollama run llama2 "Say hello"

# Find your IP
ipconfig              # Windows
ifconfig              # Mac/Linux

# Check if port is in use
netstat -an | findstr :5001    # Windows
lsof -i :5001                  # Mac/Linux

# Stop a Python process (if stuck)
Ctrl + C
```

---

## Demo Day Checklist

Before your presentation:

- [ ] All 3 PCs connected to same WiFi
- [ ] All IPs confirmed and written down
- [ ] `config.py` edited with correct IPs
- [ ] Ollama installed on all PCs
- [ ] Models downloaded (llama2, mistral)
- [ ] Python dependencies installed
- [ ] All services started and showing "healthy"
- [ ] Test query runs successfully
- [ ] Browser bookmarked to frontend URL

---

## Example Test Questions

- "What is machine learning?"
- "Explain neural networks in simple terms"
- "What are the benefits of renewable energy?"
- "How does encryption work?"
- "What is the difference between AI and ML?"

---

## Need Help?

Common issues and solutions:

| Problem | Solution |
|---------|----------|
| Port already in use | Change PORT in environment variable |
| Ollama not responding | Restart: `ollama serve` |
| Connection timeout | Check firewall settings |
| Wrong IP | Re-run `ipconfig` and update `config.py` |

---

**Remember**: The first run always takes longer because models need to load into memory. Be patient! ⏰

Good luck with your demo! 🚀