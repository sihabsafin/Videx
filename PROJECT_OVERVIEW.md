# 🧠 Content Intelligence Platform - Project Overview

## 📑 Table of Contents

1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Key Technologies](#key-technologies)
7. [Configuration](#configuration)
8. [Deployment](#deployment)

---

## Introduction

The Content Intelligence Platform is a production-ready SaaS application that uses advanced AI to extract, analyze, and summarize content from YouTube videos and websites. Built with modern technologies and best practices.

### Key Differentiators

✅ Multi-level summarization (5 depths)
✅ Multi-style output (7 styles)  
✅ Timestamp-aware video summaries
✅ Intelligent chunking strategies
✅ Multi-source comparison
✅ Content transformation
✅ Free-tier optimized
✅ Production-ready architecture

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│                 Streamlit UI                     │
│  (Pages, Sidebar, Theme, Export)                │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│          Content Orchestrator                    │
│  (Main coordination layer)                       │
└───┬─────────┬─────────┬─────────┬───────────────┘
    │         │         │         │
    ▼         ▼         ▼         ▼
┌─────┐  ┌────────┐ ┌──────┐ ┌────────────┐
│YouTu│  │Website │ │ Text │ │Summariza-  │
│ be  │  │Extract │ │Proces│ │tion Engine │
│Extr │  │or      │ │sor   │ │            │
└─────┘  └────────┘ └──────┘ └─────┬──────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │  LLM Provider │
                            │  (Groq/Gemini)│
                            └───────────────┘
```

### Processing Pipeline

```
URL Input → Validation → Source Detection
                             ↓
                    ┌────────┴────────┐
                    ▼                 ▼
              YouTube          Website
              Extractor        Extractor
                    ↓                 ↓
                    └────────┬────────┘
                             ▼
                    Text Preprocessing
                             ↓
                    Intelligent Chunking
                             ↓
                    Strategy Selection
                   (Stuff/Refine/MapReduce)
                             ↓
                    LLM Processing
                             ↓
                    Post-Processing
                             ↓
                    Output Formatting
```

---

## File Structure

```
genai-content-intelligence/
│
├── 📄 app.py                       # Main application entry
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 LICENSE                      # MIT License
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # Quick start guide
├── 📄 DEPLOYMENT.md                # Deployment guide
├── 📄 FEATURES.md                  # Features documentation
├── 📄 PROJECT_OVERVIEW.md          # This file
├── 📄 setup.sh                     # Automated setup script
├── 📄 verify_setup.py              # Setup verification
│
├── 📁 .streamlit/
│   └── config.toml                 # Streamlit configuration
│
└── 📁 src/                         # Source code
    ├── __init__.py
    ├── 📄 config.py                # App configuration
    ├── 📄 orchestrator.py          # Main orchestrator
    │
    ├── 📁 extractors/              # Content extraction
    │   ├── __init__.py
    │   ├── youtube_extractor.py    # YouTube API
    │   └── website_extractor.py    # Web scraping
    │
    ├── 📁 processors/              # Text processing
    │   ├── __init__.py
    │   └── text_processor.py       # Chunking, cleaning
    │
    ├── 📁 engines/                 # AI engines
    │   ├── __init__.py
    │   └── summarization.py        # Summarization logic
    │
    ├── 📁 llm/                     # LLM integration
    │   ├── __init__.py
    │   └── provider.py             # Provider abstraction
    │
    ├── 📁 utils/                   # Utilities
    │   ├── __init__.py
    │   ├── session.py              # Session management
    │   └── url_validator.py        # URL validation
    │
    └── 📁 ui/                      # User interface
        ├── __init__.py
        ├── theme.py                # Custom CSS
        ├── sidebar.py              # Sidebar component
        ├── pages.py                # Main page
        └── export.py               # Export functionality
```

---

## Core Components

### 1. Content Extractors

**YouTubeExtractor** (`src/extractors/youtube_extractor.py`)
- Uses `youtube-transcript-api`
- Extracts transcripts with timestamps
- Creates sectioned breakdowns
- Handles multiple URL formats

**WebsiteExtractor** (`src/extractors/website_extractor.py`)
- Uses BeautifulSoup + lxml
- Removes ads, scripts, navigation
- Extracts main content only
- Preserves article structure

### 2. Text Processor

**TextProcessor** (`src/processors/text_processor.py`)
- Token counting (tiktoken)
- Text cleaning and normalization
- Intelligent chunking
- Section-aware splitting
- Overlap strategy

### 3. LLM Provider

**LLMProvider** (`src/llm/provider.py`)
- Unified interface for Groq and Gemini
- Automatic provider selection
- Mode-based model selection
- Error handling

### 4. Summarization Engine

**SummarizationEngine** (`src/engines/summarization.py`)
- Three strategies:
  - **Stuff**: Single-pass (< 4K tokens)
  - **Refine**: Iterative (4K-15K tokens)
  - **Map-Reduce**: Parallel (> 15K tokens)
- Multi-level depths
- Multi-style outputs
- Insight extraction
- Question generation
- Content transformation

### 5. Content Orchestrator

**ContentOrchestrator** (`src/orchestrator.py`)
- Coordinates all components
- Manages processing pipeline
- Handles errors gracefully
- Returns structured results

### 6. UI Components

**Theme** (`src/ui/theme.py`)
- Custom CSS styling
- Dark theme
- Modern design
- Responsive layout

**Sidebar** (`src/ui/sidebar.py`)
- Settings panel
- API status
- Usage stats
- Recent history

**Pages** (`src/ui/pages.py`)
- Input section
- Tab navigation
- Content display
- Export interface

---

## Data Flow

### 1. URL Processing

```
User Input URL
    ↓
Validation (url_validator.py)
    ↓
Source Type Detection (youtube/website)
    ↓
Content Extraction
    ↓
Text Cleaning & Processing
    ↓
Session State Storage
```

### 2. Summarization

```
Content from Session State
    ↓
Token Count Check
    ↓
Strategy Selection (Stuff/Refine/MapReduce)
    ↓
Depth & Style Configuration
    ↓
LLM Processing
    ↓
Result Formatting
    ↓
Session State Update
```

### 3. Export

```
Session State Data
    ↓
Format Selection (MD/TXT/PDF)
    ↓
Template Application
    ↓
File Generation
    ↓
Download to User
```

---

## Key Technologies

### Backend
- **Python 3.9+**: Core language
- **LangChain**: LLM orchestration
- **Groq API**: Fast inference
- **Google Gemini**: Advanced AI
- **tiktoken**: Token counting

### Content Extraction
- **youtube-transcript-api**: YouTube transcripts
- **BeautifulSoup4**: Web scraping
- **lxml**: HTML parsing
- **requests**: HTTP client

### Frontend
- **Streamlit**: Web framework
- **Custom CSS**: Modern UI
- **Session State**: State management

### DevOps
- **dotenv**: Environment variables
- **Git**: Version control
- **Streamlit Cloud**: Deployment

---

## Configuration

### Environment Variables

```env
# Required (at least one)
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=AIza...
```

### Application Config

**`src/config.py`**:

```python
# Model Selection
DEFAULT_MODEL = "groq"

# Processing Limits
MAX_CHUNK_SIZE = 8000
CHUNK_OVERLAP = 500
MAX_VIDEO_LENGTH = 10800

# Rate Limits
MAX_URLS_PER_SESSION = 10
MAX_COMPARISON_URLS = 5

# UI Options
SUMMARY_STYLES = [...]
SUMMARY_DEPTHS = [...]
PROCESSING_MODES = [...]
```

### Streamlit Config

**`.streamlit/config.toml`**:

```toml
[theme]
primaryColor = "#6366f1"
backgroundColor = "#0f172a"

[server]
headless = true
port = 8501
```

---

## Deployment

### Local Development

```bash
# Setup
cp .env.example .env
# Add API keys to .env

# Install
pip install -r requirements.txt

# Run
streamlit run app.py
```

### Streamlit Cloud

```bash
# Push to GitHub
git push origin main

# Deploy on share.streamlit.io
# Add secrets in dashboard:
GROQ_API_KEY = "..."
GOOGLE_API_KEY = "..."
```

### Docker (Optional)

```bash
docker build -t content-intelligence .
docker run -p 8501:8501 content-intelligence
```

---

## Best Practices

### Code Organization
✅ Modular architecture
✅ Clear separation of concerns
✅ Type hints where applicable
✅ Comprehensive docstrings

### Error Handling
✅ Graceful degradation
✅ User-friendly messages
✅ Logging for debugging
✅ Validation at entry points

### Performance
✅ Efficient chunking
✅ Strategy selection
✅ Token optimization
✅ Caching opportunities

### Security
✅ API key protection
✅ Input validation
✅ Rate limiting
✅ No data persistence

---

## Extension Points

### Add New Provider

1. Create provider class in `src/llm/`
2. Implement standard interface
3. Add to `LLMProvider`
4. Update config

### Add New Summarization Style

1. Edit `src/engines/summarization.py`
2. Add to `style_modifiers` dict
3. Add to `src/config.py` SUMMARY_STYLES
4. Test thoroughly

### Add New Source Type

1. Create extractor in `src/extractors/`
2. Implement extract method
3. Add to orchestrator
4. Update URL validator

---

## Monitoring & Maintenance

### Logs
- Check Streamlit Cloud dashboard
- Review error messages
- Monitor API usage

### Updates
- Keep dependencies updated
- Monitor API changes
- Review user feedback

### Scaling
- Monitor rate limits
- Consider caching
- Upgrade API tiers if needed

---

## Support Resources

- **Documentation**: See all .md files
- **Setup**: `QUICKSTART.md`
- **Deployment**: `DEPLOYMENT.md`
- **Features**: `FEATURES.md`

---

**Last Updated**: 2024
**Version**: 1.0
**License**: MIT
