# 🚀 Deployment Guide

Complete guide for deploying Content Intelligence Platform to Streamlit Cloud.

---

## 📋 Pre-Deployment Checklist

- [ ] All code committed to GitHub
- [ ] `.env` file is in `.gitignore`
- [ ] API keys obtained (Groq and/or Gemini)
- [ ] README.md is complete
- [ ] requirements.txt is up to date
- [ ] Tested locally

---

## 🌐 Deploy to Streamlit Cloud (Recommended)

### Step 1: Prepare GitHub Repository

1. **Create GitHub repository**
   ```bash
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit: Content Intelligence Platform"
   
   # Create main branch
   git branch -M main
   
   # Add remote (replace with your repo URL)
   git remote add origin https://github.com/yourusername/content-intelligence.git
   
   # Push to GitHub
   git push -u origin main
   ```

2. **Verify `.gitignore` includes:**
   ```
   .env
   __pycache__/
   *.pyc
   .streamlit/secrets.toml
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with GitHub

3. **Click "New app"**

4. **Configure app:**
   - Repository: `yourusername/content-intelligence`
   - Branch: `main`
   - Main file path: `app.py`

5. **Add secrets** (Click "Advanced settings" → "Secrets"):
   ```toml
   GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxx"
   GOOGLE_API_KEY = "AIzaSyxxxxxxxxxxxxxxxxxx"
   ```
   
   **Note:** You only need ONE API key to start!

6. **Click "Deploy"**

7. **Wait** for deployment (2-5 minutes)

8. **Your app is live!** 🎉
   - URL: `https://your-app-name.streamlit.app`

---

## 🔧 Alternative: Deploy to Heroku

### Requirements
- Heroku account
- Heroku CLI installed

### Steps

1. **Create `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`:**
   ```bash
   mkdir -p ~/.streamlit/
   
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Update `Procfile`:**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

4. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku config:set GROQ_API_KEY="your_key"
   heroku config:set GOOGLE_API_KEY="your_key"
   ```

---

## 🐳 Alternative: Deploy with Docker

### 1. Create `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - ./src:/app/src
```

### 3. Run

```bash
docker-compose up
```

---

## 🌍 Alternative: Deploy to Railway

1. **Go to** [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Add environment variables:**
   - `GROQ_API_KEY`
   - `GOOGLE_API_KEY`
4. **Deploy automatically**

---

## 🔒 Security Best Practices

### Environment Variables
- ✅ Never commit API keys to Git
- ✅ Use `.env` for local development
- ✅ Use platform secrets for production
- ✅ Rotate keys regularly

### Rate Limiting
```python
# Already implemented in config.py
MAX_URLS_PER_SESSION = 10
MAX_COMPARISON_URLS = 5
```

### Input Validation
```python
# Already implemented in url_validator.py
- URL format validation
- Domain checking
- Malicious URL blocking
```

---

## 📊 Monitoring

### Streamlit Cloud
- Built-in logs in dashboard
- Usage metrics available
- Error tracking

### Custom Monitoring
Add to `app.py`:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log usage
logger.info(f"URL processed: {url}")
logger.error(f"Error: {error}")
```

---

## 🚀 Performance Optimization

### 1. Enable Caching

Add to functions:
```python
@st.cache_data
def expensive_function(param):
    # Your code
    pass
```

### 2. Optimize Chunk Size

Edit `src/config.py`:
```python
MAX_CHUNK_SIZE = 6000  # Reduce for faster processing
CHUNK_OVERLAP = 300    # Reduce overlap
```

### 3. Use Fast Mode Default

Edit `src/config.py`:
```python
DEFAULT_MODEL = "groq"  # Groq is faster
```

---

## 🐛 Common Deployment Issues

### Issue: App won't start

**Solution:**
1. Check requirements.txt syntax
2. Verify Python version (3.9+)
3. Check Streamlit Cloud logs

### Issue: "Module not found"

**Solution:**
1. Verify all imports in requirements.txt
2. Check file paths are correct
3. Ensure `src/` structure is correct

### Issue: API errors

**Solution:**
1. Verify API keys in secrets
2. Check key format (no quotes in Streamlit secrets)
3. Test keys locally first

### Issue: Slow performance

**Solution:**
1. Use "Fast" mode
2. Reduce MAX_CHUNK_SIZE
3. Enable caching
4. Use Groq for speed

---

## 📈 Scaling Considerations

### Free Tier Limits

**Streamlit Cloud:**
- 1 app per account (free)
- Unlimited visitors
- Automatic sleep after inactivity

**API Limits:**
- Groq: 30 requests/min
- Gemini: 60 requests/min

### If You Need More:

1. **Multiple API keys** - Rotate between keys
2. **Paid tiers** - Upgrade Groq or Gemini
3. **Custom deployment** - Use AWS/GCP/Azure
4. **Add caching** - Reduce redundant API calls

---

## 🎯 Production Checklist

Before going live:

- [ ] Test all features locally
- [ ] Verify all URLs work
- [ ] Test with long content
- [ ] Test with multiple users
- [ ] Check error handling
- [ ] Verify exports work
- [ ] Test on mobile
- [ ] Update README
- [ ] Add usage examples
- [ ] Set up monitoring

---

## 📞 Support & Resources

### Streamlit Resources
- [Documentation](https://docs.streamlit.io)
- [Community Forum](https://discuss.streamlit.io)
- [Deploy Guides](https://docs.streamlit.io/streamlit-community-cloud)

### API Documentation
- [Groq Docs](https://console.groq.com/docs)
- [Gemini Docs](https://ai.google.dev/docs)

### Troubleshooting
- Check Streamlit Cloud logs
- Test locally first
- Review API usage limits
- Check GitHub Issues

---

## 🎉 Post-Deployment

### Share Your App
```
https://your-app-name.streamlit.app
```

### Get Feedback
- Share with target users
- Collect feedback
- Iterate based on usage

### Monitor Usage
- Check Streamlit analytics
- Monitor API usage
- Track popular features

---

**Your app is now live! 🚀**

Share the URL and start helping users analyze content with AI!
