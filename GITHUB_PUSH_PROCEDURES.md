# GitHub Push & Deployment Procedures

## Quick Reference: Protecting Your API Key

Your OpenAI API key is **PROTECTED** by:
1. `.gitignore` - prevents `.env` files from being committed
2. `.env.example` - template without real keys
3. Render environment variables - secure storage for production

**NEVER commit `.env` files!**

---

## Pre-Push Checklist

Before pushing to GitHub, verify:

- [ ] `.env` file is NOT staged for commit
- [ ] API keys are only in local `.env` file (not in code)
- [ ] `.gitignore` includes all `.env` variations
- [ ] `.env.example` exists but contains NO real keys

### Quick Check Command:
```bash
# This should show NO .env files (except .env.example)
git status | grep -E "\.env$"

# This should return empty (no API keys in code)
grep -r "sk-" frontend/ backend/ --exclude-dir=node_modules
```

---

## Step-by-Step: Push to GitHub

### 1. Verify API Key Protection

```bash
# Check what files will be committed
git status

# If you see .env files (NOT .env.example), DO NOT COMMIT
# If .env appears, remove it:
git reset .env
```

### 2. Stage Your Changes

```bash
# Add all files (gitignore will protect .env)
git add .

# Or add specific files
git add frontend/ backend/ requirements.txt
```

### 3. Commit Changes

```bash
git commit -m "Prepare for deployment"
```

### 4. Push to GitHub

```bash
git push origin main
```

---

## Deployment Procedures

### Part 1: Deploy Backend to Render

#### Before You Start:
1. Create account at [Render](https://render.com)
2. Have your OpenAI API key ready
3. Know your GitHub username

#### Steps:

**1. Push code to GitHub** (see above)

**2. Create Render Web Service**
- Go to [Render Dashboard](https://dashboard.render.com/)
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repository

**3. Configure Service**
- **Name**: `literature-assistant-backend`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Runtime**: `Docker`
- **Instance Type**: `Free` (or `Starter` for $7/mo - no sleep)

**4. Set Environment Variables**
Click "Advanced" and add these variables:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `sk-your-actual-api-key-here` |
| `ALLOWED_ORIGINS` | `https://YOUR_USERNAME.github.io,http://localhost:5001` |
| `PORT` | `10000` |

**Replace `YOUR_USERNAME` with your actual GitHub username!**

**5. Deploy**
- Click **"Create Web Service"**
- Wait 5-10 minutes for build
- Note your URL: `https://YOUR-APP-NAME.onrender.com`

**6. Test Backend**
Visit: `https://YOUR-APP-NAME.onrender.com/api/health`

Should see: `{"status":"healthy","openai_configured":true}`

---

### Part 2: Update Frontend Configuration

**REQUIRED STEP - Don't Skip!**

**1. Update Backend URL in Code**

Edit `frontend/app.js` line 7:

**Change from:**
```javascript
: (window.BACKEND_URL || 'https://YOUR-APP-NAME.onrender.com');
```

**Change to:**
```javascript
: (window.BACKEND_URL || 'https://literature-assistant-backend.onrender.com');
```
*(Use YOUR actual Render service name)*

**2. Commit and Push**
```bash
git add frontend/app.js
git commit -m "Update production backend URL"
git push origin main
```

---

### Part 3: Deploy Frontend to GitHub Pages

**1. Enable GitHub Pages**
- Go to your repository on GitHub
- Click **Settings** → **Pages**
- Under "Build and deployment":
  - **Source**: `GitHub Actions`
- Click **Save**

**2. Trigger Deployment**
The GitHub Actions workflow (`.github/workflows/deploy.yml`) will automatically deploy on push to `main`.

**3. Get Your URL**
- Wait ~2-3 minutes
- Your site: `https://YOUR_USERNAME.github.io/literature-assistant.github.io/`

**4. Update CORS in Render**
- Go back to Render Dashboard
- Open your service → **Environment** tab
- Update `ALLOWED_ORIGINS`:
  ```
  https://YOUR_USERNAME.github.io,http://localhost:5001
  ```
- Click **Save Changes**
- Wait for auto-redeploy (~3-5 min)

---

### Part 4: Test Everything

**1. Test Backend**
```bash
curl https://YOUR-APP-NAME.onrender.com/api/health
```

**2. Test Frontend**
- Visit: `https://YOUR_USERNAME.github.io/literature-assistant.github.io/`
- Upload a test PDF
- Click "Analyze Paper"
- Verify it works!

---

## Configuration Checklist

Before deployment, update these files with YOUR information:

### 1. `render.yaml`
```yaml
repo: https://github.com/YOUR_USERNAME/literature-assistant.github.io
```

### 2. `frontend/app.js`
```javascript
: (window.BACKEND_URL || 'https://YOUR-APP-NAME.onrender.com');
```

### 3. Render Environment Variables
```
ALLOWED_ORIGINS=https://YOUR_USERNAME.github.io,http://localhost:5001
```

---

## Common Issues & Solutions

### Issue: CORS Error
**Error**: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solution**:
1. Check `ALLOWED_ORIGINS` in Render matches your GitHub Pages URL exactly
2. No trailing slash in URL
3. Redeploy backend after changes

### Issue: Backend Not Responding
**Error**: "Cannot connect to backend server"

**Solution**:
1. Free tier sleeps after 15min inactivity
2. First request after sleep takes 30-50 seconds
3. Check Render logs for errors
4. Verify health endpoint works

### Issue: OpenAI API Error
**Error**: "OpenAI API error" or rate limits

**Solution**:
1. Verify `OPENAI_API_KEY` in Render dashboard
2. Check OpenAI account has credits
3. Verify model name in backend code

### Issue: Accidentally Committed API Key
**URGENT FIX**:
```bash
# Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (ONLY if you haven't shared the repo)
git push origin --force --all

# IMPORTANT: Rotate your API key at OpenAI immediately!
```

Then:
1. Go to OpenAI platform
2. Revoke the exposed key
3. Generate new key
4. Update Render environment variable

---

## Security Best Practices

✅ **DO:**
- Keep API keys in environment variables
- Use `.gitignore` for sensitive files
- Rotate keys if exposed
- Use HTTPS only in production
- Monitor API usage regularly

❌ **DON'T:**
- Commit `.env` files
- Hardcode API keys in source code
- Share API keys in chat/email
- Use API keys in frontend JavaScript
- Push to public repos without checking

---

## File Structure Reference

```
literature-assistant.github.io/
├── .env                    # LOCAL ONLY - NEVER COMMIT
├── .env.example            # Template - SAFE to commit
├── .gitignore              # Protects .env files
├── .github/
│   └── workflows/
│       └── deploy.yml      # Auto-deploys to GitHub Pages
├── frontend/
│   ├── index.html
│   └── app.js              # UPDATE: Backend URL
├── backend/
│   └── api/
│       └── app.py
├── Dockerfile              # Uses PORT env var
├── render.yaml             # UPDATE: GitHub repo URL
├── requirements.txt
└── DEPLOYMENT.md           # Full deployment guide
```

---

## Cost Summary

| Service | Free Tier | Paid |
|---------|-----------|------|
| **GitHub Pages** | ✅ Free forever | N/A |
| **Render** | ✅ Free (sleeps after 15min) | $7/mo (always-on) |
| **OpenAI API** | Pay-per-use | ~$0.15-0.60/document |

**Estimated Monthly Cost**: $5-15 (mostly OpenAI usage)

---

## Quick Commands Reference

### Local Development
```bash
# Start backend
python main.py server

# Start frontend (new terminal)
cd frontend && python -m http.server 8000
```

### Git Operations
```bash
# Check for sensitive files
git status | grep "\.env"

# Stage and commit
git add .
git commit -m "Your message"
git push origin main
```

### Docker
```bash
# Build and run locally
docker-compose up --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **GitHub Pages**: https://docs.github.com/pages
- **OpenAI API**: https://platform.openai.com/docs
- **Project Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/literature-assistant.github.io/issues)

---

## Next Steps After Deployment

1. ✅ Test with multiple PDFs
2. ✅ Monitor OpenAI usage: https://platform.openai.com/usage
3. ✅ Set spending limits in OpenAI dashboard
4. ✅ Star the repo (optional)
5. ✅ Share with colleagues!

---

**Last Updated**: 2025-11-09
**Status**: ✅ Ready for deployment
