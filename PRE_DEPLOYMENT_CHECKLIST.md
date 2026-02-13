# Pre-GitHub Checklist

## ✅ Files to Verify

### Required Files
- [x] `app.py` - Streamlit application
- [x] `requirements.txt` - Dependencies (streamlit included)
- [x] `.env.example` - Environment template
- [x] `README.md` - Project documentation
- [x] `DEPLOY.md` - Deployment guide
- [x] `.gitignore` - Excludes sensitive files
- [x] `rag/` folder - Core RAG logic
- [x] `data/` folder - Documents (doc1.md, doc2.md, doc3.md)
- [x] `.streamlit/config.toml` - Streamlit configuration

### Files to EXCLUDE (check .gitignore)
- [ ] `.env` - Contains your API key (MUST NOT commit!)
- [ ] `.venv/` - Virtual environment
- [ ] `__pycache__/` - Python cache
- [ ] `artifacts/` - Generated at runtime

## 🧪 Pre-Deployment Tests

### 1. Test Locally

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install/update dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

**Verify**:
- [ ] App opens at http://localhost:8501
- [ ] "Build Index" button works
- [ ] Sample questions work
- [ ] Context sections expand properly
- [ ] No errors in console

### 2. Check Files

```bash
# Make sure .env is NOT tracked
git status

# .env should NOT appear in the list
# If it does, make sure .gitignore includes .env
```

## 📤 Push to GitHub

### First Time

```bash
# Initialize git
git init

# Add all files
git add .

# Check what's being added (should NOT include .env)
git status

# Commit
git commit -m "Initial commit - RAG system with Streamlit"

# Create repository on GitHub: https://github.com/new
# Name it: rag-construction (or your preferred name)

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/rag-construction.git

# Push
git branch -M main
git push -u origin main
```

### Already Have a Git Repo

```bash
# Add changes
git add .

# Commit
git commit -m "Streamlit deployment ready"

# Push
git push
```

## 🚀 Deploy to Streamlit Cloud

Follow steps in `DEPLOY.md`:

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Add secrets (GROQ_API_KEY)
7. Deploy!

## 🎯 Final Checks Before Submission

- [ ] GitHub repository is public (or shared with evaluator)
- [ ] Streamlit app is deployed and accessible
- [ ] App URL works without errors
- [ ] README has clear setup instructions
- [ ] All documents are in `data/` folder
- [ ] Screenshots folder has demo images (optional)

## 📝 Submission Template

Include this in your assignment submission:

```
# RAG System Submission

## Live Demo
🚀 https://YOUR_USERNAME-rag-construction.streamlit.app

## GitHub Repository
📦 https://github.com/YOUR_USERNAME/rag-construction

## Quick Start
1. Visit the live demo URL
2. Click "Build Index" in sidebar
3. Try sample questions or ask your own
4. Expand context sections to see retrieved chunks

## Local Setup (Optional)
```bash
git clone https://github.com/YOUR_USERNAME/rag-construction.git
cd rag-construction
pip install -r requirements.txt
cp .env.example .env
# Add GROQ_API_KEY to .env
streamlit run app.py
```

## Technologies Used
- Streamlit (UI)
- FAISS (Vector Database)
- Sentence Transformers (Embeddings)
- Groq API (LLM)
- Python 3.11+
```

## 🆘 Troubleshooting

**Git refusing to push:**
```bash
git pull origin main --rebase
git push
```

**.env accidentally committed:**
```bash
# Remove from git but keep local file
git rm --cached .env
git commit -m "Remove .env from tracking"
git push

# Make sure .gitignore includes .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore"
git push
```

**Large files warning:**
- Remove `artifacts/` if accidentally added
- Clear `__pycache__/` folders

## ✨ You're Ready!

Once all checks pass:
1. ✅ Code on GitHub
2. ✅ App deployed on Streamlit Cloud  
3. ✅ Documentation complete
4. ✅ No sensitive data committed

**Submit your live URLs and you're done!** 🎉
