# Deployment Steps for Streamlit Cloud

## Prerequisites

- GitHub account
- Groq API key from https://console.groq.com

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure these files exist:
- ✅ `app.py` - Streamlit application
- ✅ `requirements.txt` - Dependencies
- ✅ `rag/` - Backend logic
- ✅ `data/` - Documents (doc1.md, doc2.md, doc3.md)
- ✅ `.streamlit/config.toml` - Streamlit config
- ✅ `.gitignore` - Excludes `.env` and artifacts

### 2. Push to GitHub

```bash
# If not already initialized
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create repo on GitHub (github.com/new), then:
git remote add origin https://github.com/YOUR_USERNAME/rag-construction.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Streamlit Cloud

1. **Go to**: https://share.streamlit.io

2. **Sign in** with GitHub

3. **Click "New app"**

4. **Configure**:
   - Repository: `YOUR_USERNAME/rag-construction`
   - Branch: `main`
   - Main file path: `app.py`

5. **Add Secrets** (Advanced settings → Secrets):
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   LLM_PROVIDER = "groq"
   GROQ_MODEL = "llama-3.1-8b-instant"
   EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
   ```

6. **Click "Deploy"**

7. **Wait** 2-5 minutes for build

8. **Your app is live!** You'll get a URL like:
   `https://YOUR_USERNAME-rag-construction.streamlit.app`

### 4. Test Your Deployment

1. Visit your Streamlit URL
2. Click "Build Index" in sidebar
3. Wait ~30 seconds for index to build
4. Try a sample question
5. Verify you get answers with retrieved context

### 5. Share for Assignment

Include in your submission:

```
🚀 Live Demo: https://YOUR_USERNAME-rag-construction.streamlit.app

Instructions:
1. Visit the URL
2. Click "Build Index" in sidebar (first time only)
3. Try sample questions or ask your own
4. Expand context sections to see retrieved chunks

GitHub Repository: https://github.com/YOUR_USERNAME/rag-construction
```

## Updating Your Deployment

After making changes:

```bash
git add .
git commit -m "Update features"
git push
```

Streamlit Cloud auto-redeploys when you push!

## Troubleshooting

**Build fails:**
- Check `requirements.txt` has all dependencies
- Verify `.streamlit/config.toml` exists

**"Index not found" error:**
- Click "Build Index" button
- Wait for success message

**API errors:**
- Check secrets are correctly set in Streamlit Cloud
- Verify GROQ_API_KEY is valid

**Slow loading:**
- First deployment downloads ~80MB embedding model
- Cached for subsequent loads

## Alternative: Keep It Private

If you don't want public deployment:
- Set repository to private on GitHub
- Share with specific accounts only
- Or just submit GitHub link (grader can run locally)
