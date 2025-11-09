# Render Quick Start - Start Command Info

## ✅ Your Start Command is Already Configured!

**Location**: `Dockerfile` line 23
```bash
CMD gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 2 --timeout 120 backend.api.app:app
```

---

## 🚀 Deploy Now (3 Steps)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Create Render Service

Go to [Render Dashboard](https://dashboard.render.com/)

**Quick Setup**:
- Click **"New +"** → **"Blueprint"**
- Connect repository: `literature-assistant.github.io`
- Render auto-detects `render.yaml`
- Click **"Apply"**

**OR Manual Setup**:
- Click **"New +"** → **"Web Service"**
- Connect repository
- **Runtime**: `Docker`
- **Dockerfile Path**: `./Dockerfile`
- **NO need to set start command** (uses Dockerfile CMD)

### Step 3: Add Environment Variable

In Render dashboard → **Environment**:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | Your actual OpenAI API key |
| `ALLOWED_ORIGINS` | `https://bobaba99.github.io,http://localhost:5001` |
| `PORT` | `10000` |

Click **"Save Changes"** → Auto-deploys!

---

## 📋 Start Command Reference

### What Render Uses (from Dockerfile):
```bash
gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 2 --timeout 120 backend.api.app:app
```

### What Each Part Does:
- `gunicorn` - Production WSGI server
- `--bind 0.0.0.0:${PORT:-5001}` - Listen on all interfaces, use $PORT or default to 5001
- `--workers 2` - 2 worker processes (good for free tier)
- `--timeout 120` - 2 minutes timeout (for AI processing)
- `backend.api.app:app` - Your Flask app location

---

## 🔍 Verify Deployment

### 1. Check Health Endpoint
```bash
curl https://YOUR-APP-NAME.onrender.com/api/health
```

**Expected Response**:
```json
{"status":"healthy","openai_configured":true}
```

### 2. Check Logs

Render Dashboard → Your Service → **Logs** tab

**Look for**:
```
==> Starting service with 'gunicorn --bind 0.0.0.0:10000...'
Starting server on 0.0.0.0:10000
```

---

## 🛠️ Alternative Start Commands

### If Using Python Runtime (not Docker):

**In Render Dashboard** → Build & Deploy:
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 backend.api.app:app
```

### If Using start.sh Script:
```
Start Command: ./start.sh
```

---

## ⚙️ Configuration Files

| File | Purpose | Status |
|------|---------|--------|
| `Dockerfile` | Contains start command (line 23) | ✅ Ready |
| `render.yaml` | Render blueprint (Docker) | ✅ Ready |
| `render-python.yaml` | Alternative (Python runtime) | 📄 Optional |
| `start.sh` | Standalone start script | 📄 Optional |

---

## 🆘 Troubleshooting

### Issue: Service won't start
**Check**: Render logs for errors
**Fix**: Verify `OPENAI_API_KEY` is set

### Issue: "Module not found"
**Check**: `backend/` directory exists in repo
**Fix**: Ensure `COPY backend ./backend` in Dockerfile

### Issue: Timeout errors
**Fix**: Increase timeout to 180-300 seconds in start command

### Issue: "Address already in use"
**Check**: PORT is set to 10000 in Render
**Fix**: Render sets PORT automatically, don't override

---

## 📊 Performance Tuning

### Free Tier (Recommended):
```bash
--workers 2 --timeout 120
```

### Paid Tier ($7/mo Starter):
```bash
--workers 4 --timeout 120
```

---

## ✅ Deployment Checklist

- [x] Start command configured in Dockerfile
- [x] `render.yaml` ready for Blueprint deployment
- [x] `.gitignore` protects `.env` files
- [ ] Push code to GitHub
- [ ] Create Render web service
- [ ] Add `OPENAI_API_KEY` environment variable
- [ ] Test health endpoint
- [ ] Update frontend with Render URL

---

## 🎯 Summary

**You don't need to configure a start command manually!**

Your project uses Docker, and the start command is already in the Dockerfile. 

**Just**:
1. Push to GitHub
2. Connect to Render
3. Add API key
4. Deploy!

**Full guide**: See [RENDER_SETUP.md](RENDER_SETUP.md) for detailed information.

---

**Ready to deploy?** → [Render Dashboard](https://dashboard.render.com/)
