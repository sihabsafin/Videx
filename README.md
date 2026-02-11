# 🧠 Content Intelligence Platform

A production-ready GenAI platform for extracting, analyzing, and summarizing content from YouTube videos and websites. Built with Streamlit, LangChain, and modern AI models.

## ✨ Features

### 🎯 Core Capabilities
- **YouTube Video Analysis** - Extract transcripts with timestamps
- **Website Content Extraction** - Clean article extraction from any URL
- **Multi-Level Summarization** - TL;DR, Bullet Points, Executive, Detailed, Structured
- **Style Customization** - Simple, Technical, Academic, Executive, Casual, LinkedIn, Twitter
- **Insight Extraction** - Key ideas, arguments, evidence, implications
- **Question Generation** - Study, Discussion, Interview, MCQ questions
- **Content Transformation** - Blog posts, LinkedIn posts, Emails, Meeting notes
- **Multi-Source Comparison** - Compare up to 5 URLs side-by-side

### 🎨 User Experience
- Modern, professional dark-themed UI
- Real-time processing with progress indicators
- Session-based history tracking
- Export to Markdown, Plain Text, and PDF
- Responsive design for all devices

### 🚀 Technical Features
- Intelligent text chunking with overlap
- Multiple summarization strategies (Stuff, Refine, Map-Reduce)
- Free-tier optimized (Groq + Gemini)
- No database required (session-based)
- Production-ready error handling
- Rate limiting protection

---

## 📋 Prerequisites

- Python 3.9+
- API keys (at least one):
  - [Groq API Key](https://console.groq.com/keys) (Free tier: 30 req/min)
  - [Google Gemini API Key](https://makersuite.google.com/app/apikey) (Free tier: 60 req/min)

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd genai-content-intelligence
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Get from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Get from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here
```

**Note:** You only need ONE API key to get started!

### 4. Run Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Deploy to Streamlit Cloud

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository
4. Set main file path: `app.py`
5. Add secrets in "Advanced settings" → "Secrets":

```toml
GROQ_API_KEY = "your_groq_key"
GOOGLE_API_KEY = "your_gemini_key"
```

6. Click "Deploy"!

Your app will be live at: `https://your-app-name.streamlit.app`

---

## 📖 Usage Guide

### Single URL Analysis

1. Enter a YouTube or website URL
2. Click "🔍 Analyze"
3. View results in tabs:
   - **Summary** - Main summarization
   - **Insights** - Key ideas and arguments
   - **Questions** - Generated questions
   - **Transform** - Convert to different formats
   - **Export** - Download results

### Compare Multiple URLs

1. Switch to "Compare Multiple URLs" mode
2. Add 2-5 URLs
3. Click "🔍 Compare All"
4. View comparison analysis

### Customize Output

Use sidebar settings:
- **Mode** - Fast, Balanced, or Accurate
- **Summary Depth** - TL;DR to Structured Outline
- **Writing Style** - Simple to Academic

---

## 🏗️ Project Structure

```
genai-content-intelligence/
├── app.py                      # Main application entry
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── src/
    ├── config.py              # App configuration
    ├── orchestrator.py        # Main orchestration logic
    ├── extractors/
    │   ├── youtube_extractor.py    # YouTube content extraction
    │   └── website_extractor.py    # Website content extraction
    ├── processors/
    │   └── text_processor.py       # Text chunking and processing
    ├── engines/
    │   └── summarization.py        # Summarization strategies
    ├── llm/
    │   └── provider.py             # LLM provider abstraction
    ├── utils/
    │   ├── session.py              # Session management
    │   └── url_validator.py        # URL validation
    └── ui/
        ├── theme.py                # Custom styling
        ├── sidebar.py              # Sidebar component
        ├── pages.py                # Main page component
        └── export.py               # Export functionality
```

---

## 🔧 Configuration

### Model Settings

Edit `src/config.py` to customize:

```python
# Default processing mode
DEFAULT_MODEL = "groq"  # or "gemini"

# Model selection per mode
GROQ_MODELS = {
    "fast": "llama-3.1-8b-instant",
    "balanced": "llama-3.1-70b-versatile",
    "accurate": "llama-3.1-70b-versatile"
}

# Text processing
MAX_CHUNK_SIZE = 8000
CHUNK_OVERLAP = 500
```

### Rate Limits

```python
MAX_URLS_PER_SESSION = 10
MAX_COMPARISON_URLS = 5
```

---

## 🎯 Use Cases

### For Students
- Summarize lecture videos
- Extract key concepts from articles
- Generate study questions
- Create study outlines

### For Researchers
- Quickly digest research papers
- Compare multiple sources
- Extract key arguments
- Generate discussion points

### For Professionals
- Executive summaries of reports
- Transform content for LinkedIn
- Meeting notes from recordings
- Compare industry articles

### For Content Creators
- Research topic summaries
- Extract key talking points
- Generate content ideas
- Analyze competitor content

---

## 🚦 API Limits

### Groq (Free Tier)
- 30 requests/minute
- Best for: Fast processing

### Google Gemini (Free Tier)
- 60 requests/minute
- Best for: Longer content

**Tip:** The app automatically uses whichever API key you provide!

---

## 🔒 Privacy & Security

- No data is stored permanently
- Session-based only (resets on browser close)
- API keys stored in environment variables
- No third-party analytics
- All processing happens in real-time

---

## 🐛 Troubleshooting

### "No API keys configured"
- Check `.env` file exists
- Verify API keys are correct
- Restart the app after adding keys

### "Transcript not available"
- Not all YouTube videos have transcripts
- Try another video with captions enabled

### "Failed to extract content"
- Some websites block scrapers
- Try another URL
- Check if website is accessible

### Rate Limit Errors
- Wait a minute and try again
- Switch to different processing mode
- Use alternative API key

---

## 🛠️ Development

### Add New Features

1. **New Summarization Style**
   - Edit `src/engines/summarization.py`
   - Add to `style_modifiers` dict

2. **New Export Format**
   - Edit `src/ui/export.py`
   - Add new format function

3. **New Processing Mode**
   - Edit `src/config.py`
   - Add to `PROCESSING_MODES`

### Testing

```bash
# Test URL extraction
python -c "from src.extractors.youtube_extractor import YouTubeExtractor; print(YouTubeExtractor.get_transcript('dQw4w9WgXcQ'))"

# Test website extraction
python -c "from src.extractors.website_extractor import WebsiteExtractor; print(WebsiteExtractor.extract_content('https://example.com'))"
```

---

## 📊 Performance

### Processing Times (Approximate)

| Content Length | Fast Mode | Balanced | Accurate |
|---------------|-----------|----------|----------|
| Short (< 5 min video) | 5-10s | 10-15s | 15-20s |
| Medium (15 min video) | 15-20s | 20-30s | 30-45s |
| Long (1 hour video) | 30-45s | 45-60s | 60-90s |

---

## 🎨 Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#6366f1"  # Change accent color
backgroundColor = "#0f172a"  # Change background
```

### Modify UI

Edit files in `src/ui/`:
- `theme.py` - Custom CSS
- `pages.py` - Main content layout
- `sidebar.py` - Settings panel

---

## 📝 License

This project is open source and available for educational and commercial use.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Check troubleshooting section
- Review configuration docs

---

## 🚀 Roadmap

### V1 (Current)
- ✅ YouTube & Website extraction
- ✅ Multi-level summarization
- ✅ Insight extraction
- ✅ Export functionality

### V2 (Planned)
- User authentication
- Save projects
- Shareable links
- Team workspaces
- Search & Summarize mode
- Playlist support
- Advanced analytics

---

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io) - Web framework
- [LangChain](https://langchain.com) - LLM orchestration
- [Groq](https://groq.com) - Fast inference
- [Google Gemini](https://ai.google.dev) - Advanced AI
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Web scraping
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) - YouTube transcripts

---

**Made with ❤️ for the AI community**
