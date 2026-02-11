# ⚡ Quick Start Guide

Get the Content Intelligence Platform running in 5 minutes!

---

## 🎯 What You Need

1. **Python 3.9+** installed
2. **One API key** (choose one):
   - Groq API (recommended for speed) → [Get it here](https://console.groq.com/keys)
   - Google Gemini API → [Get it here](https://makersuite.google.com/app/apikey)

---

## 🚀 5-Minute Setup

### Step 1: Install (1 minute)

```bash
# Extract the ZIP file
# Navigate to folder
cd genai-content-intelligence

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API key
# You only need ONE of these:
```

**Option A: Using Groq (Recommended)**
```env
GROQ_API_KEY=gsk_your_actual_key_here
GOOGLE_API_KEY=
```

**Option B: Using Gemini**
```env
GROQ_API_KEY=
GOOGLE_API_KEY=AIza_your_actual_key_here
```

### Step 3: Run (30 seconds)

```bash
streamlit run app.py
```

✅ **Done!** App opens at `http://localhost:8501`

---

## 🎮 First Usage

### Try These Examples:

1. **YouTube Video Summary**
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

2. **Article Summary**
   ```
   https://example.com/some-article
   ```

### Steps:
1. Paste URL in input box
2. Click "🔍 Analyze"
3. Wait 10-20 seconds
4. View results in tabs!

---

## 🎛️ Quick Settings

**Sidebar → Settings:**

- **Mode**: 
  - Fast = Quick results
  - Balanced = Good quality (recommended)
  - Accurate = Best quality

- **Summary Depth**:
  - TL;DR = 1-2 lines
  - Executive Summary = 2-3 paragraphs (recommended)
  - Detailed = Full summary

- **Style**:
  - Executive Tone (professional)
  - Simple Explanation (easy to read)
  - Technical (for experts)

---

## 📤 Export Your Results

1. Go to "Export" tab
2. Choose format:
   - Markdown (best for docs)
   - Plain Text
   - PDF (coming soon)
3. Click "Download"

---

## 🐛 Troubleshooting

### "No API keys configured"
→ Make sure you edited `.env` file with your actual API key

### "Module not found"
→ Run: `pip install -r requirements.txt`

### "Transcript not available"
→ Try another YouTube video (some don't have transcripts)

### App won't start
→ Make sure you're using Python 3.9 or higher

---

## 🎯 Next Steps

### Deploy Online (Free!)

1. Push to GitHub:
   ```bash
   git init
   git add .
   git commit -m "My content intelligence app"
   git push
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add API keys in "Secrets"
5. Deploy!

**Full guide:** See `DEPLOYMENT.md`

---

## 💡 Tips

1. **Start with "Balanced" mode** - Good speed + quality
2. **Use Executive Summary depth** - Best for most cases
3. **Try different styles** - See what fits your need
4. **Export everything** - Save your summaries
5. **Compare multiple URLs** - Great for research

---

## 📚 Learn More

- Full documentation: `README.md`
- Deployment guide: `DEPLOYMENT.md`
- API docs: See links in README

---

## 🆘 Need Help?

1. Check `README.md` troubleshooting section
2. Verify API keys are correct
3. Test with example URLs first
4. Make sure dependencies installed

---

**You're all set! 🎉**

Start analyzing content with AI!
