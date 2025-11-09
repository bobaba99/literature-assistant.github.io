# Render Deployment Guide

## Current Configuration

Your project is configured to use **Docker runtime** on Render (recommended).

### Start Command Location

The start command is defined in the **Dockerfile**:
```dockerfile
CMD gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 2 --timeout 120 backend.api.app:app
```

This command:
- Uses `gunicorn` production WSGI server
- Binds to `0.0.0.0` (allows external connections)
- Uses the `PORT` environment variable (Render sets this to 10000)
- Runs 2 worker processes
- 120 second timeout for long-running AI requests
- Starts the Flask app at `backend.api.app:app`

---

## Deployment Options

### Option 1: Docker Runtime (Current - Recommended)

**File**: `render.yaml` (current configuration)

**Pros**:
- Consistent environment across local and production
- Includes system dependencies
- Better isolation
- Matches local Docker setup

**Start Command**: Defined in Dockerfile, no manual configuration needed

**To Deploy**:
1. Push code to GitHub
2. Render detects `render.yaml` and `Dockerfile`
3. Automatically builds and deploys

---

### Option 2: Python Runtime (Alternative)

**File**: `render-python.yaml` (alternative provided)

**Pros**:
- Faster builds (no Docker layer)
- Simpler configuration
- Uses less resources

**Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 backend.api.app:app`

**To Use**:
1. Backup current `render.yaml`
2. Rename `render-python.yaml` to `render.yaml`
3. Push to GitHub

---

## Manual Configuration (Web Dashboard)

If you prefer to configure via Render dashboard instead of `render.yaml`:

### 1. Create New Web Service

Go to [Render Dashboard](https://dashboard.render.com/) → **New +** → **Web Service**

### 2. Configure Basic Settings

| Setting | Value |
|---------|-------|
| **Name** | `literature-assistant-backend` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | (leave empty) |

### 3. Choose Runtime

#### For Docker:
| Setting | Value |
|---------|-------|
| **Runtime** | `Docker` |
| **Dockerfile Path** | `./Dockerfile` |

**Build Command**: (empty - Docker handles it)
**Start Command**: (empty - uses Dockerfile CMD)

#### For Python:
| Setting | Value |
|---------|-------|
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 backend.api.app:app` |

### 4. Environment Variables

Click **Advanced** → Add environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `OPENAI_API_KEY` | `sk-your-key-here` | **REQUIRED** - Get from OpenAI dashboard |
| `ALLOWED_ORIGINS` | `https://bobaba99.github.io,http://localhost:5001` | Update with YOUR GitHub username |
| `PORT` | `10000` | Render's default port |
| `PYTHONUNBUFFERED` | `1` | Real-time log output |

**PYTHON_VERSION** (Python runtime only): `3.12.0`

### 5. Instance Type

- **Free**: Spins down after 15 min inactivity, takes ~30-50s to wake
- **Starter ($7/mo)**: Always on, faster

### 6. Advanced Settings

| Setting | Value |
|---------|-------|
| **Health Check Path** | `/api/health` |
| **Auto-Deploy** | `Yes` (deploys on every push to main) |

---

## Start Command Variations

### Basic (Current)
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 backend.api.app:app
```

### With Logging
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - backend.api.app:app
```

### More Workers (for paid plans)
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 backend.api.app:app
```

### Using start.sh Script
```bash
./start.sh
```

---

## Verifying Your Configuration

### 1. Check Local Docker Build

```bash
# Build locally to verify Dockerfile works
docker build -t test-backend .

# Run locally
docker run -p 5001:5001 -e OPENAI_API_KEY=your-key-here test-backend
```

### 2. Test Start Command Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Test gunicorn command
gunicorn --bind 0.0.0.0:5001 --workers 2 --timeout 120 backend.api.app:app
```

### 3. Check Health Endpoint

```bash
# Should return: {"status":"healthy","openai_configured":true}
curl http://localhost:5001/api/health
```

---

## Troubleshooting Start Command Issues

### Issue: "Address already in use"

**Solution**: Port 10000 is occupied
```bash
# Find process using port
lsof -i :10000

# Kill process (if safe)
kill -9 <PID>
```

### Issue: "ModuleNotFoundError: No module named 'backend'"

**Solution**: Python can't find backend module

**For Docker**: Ensure `COPY backend ./backend` is in Dockerfile
**For Python runtime**: Ensure `backend/` directory is in repository

### Issue: "Application timeout"

**Solution**: Increase timeout in start command
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 300 backend.api.app:app
```

### Issue: Logs show "Worker timeout"

**Solution**: 
- OpenAI API calls are slow (30-60s) - this is normal
- Increase timeout to 120-180 seconds
- Use fewer workers on free tier (1-2 workers max)

### Issue: "Cannot bind to port"

**Solution**: Check PORT environment variable
```bash
# In Render dashboard, verify PORT=10000
# Render automatically sets PORT, but you can override
```

---

## Render Build & Deploy Process

### What Happens When You Push to GitHub:

1. **Render detects push** (via webhook)
2. **Build phase**:
   - Docker: Runs `docker build` using Dockerfile
   - Python: Runs build command (`pip install -r requirements.txt`)
3. **Deploy phase**:
   - Docker: Runs `CMD` from Dockerfile
   - Python: Runs start command
4. **Health check**: Pings `/api/health` endpoint
5. **Live**: Service is publicly available

### Build Logs

Check Render dashboard → Your service → **Logs** tab

Look for:
```
==> Building...
==> Deploying...
==> Starting service with 'gunicorn --bind 0.0.0.0:10000...'
Starting server on 0.0.0.0:10000
```

---

## Performance Tuning

### Workers Configuration

**Free Tier** (512 MB RAM):
```bash
--workers 2  # Recommended
```

**Starter** (512 MB RAM):
```bash
--workers 2-4
```

**Standard+** (2+ GB RAM):
```bash
--workers 4-8
```

**Formula**: `workers = (2 x CPU cores) + 1`

### Timeout Settings

**Default**: 120 seconds (good for most cases)

**For complex PDFs**: 180-300 seconds
```bash
--timeout 180
```

**For simple PDFs**: 60 seconds
```bash
--timeout 60
```

---

## Alternative: Using Procfile

Create `Procfile` in project root:
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 backend.api.app:app
```

Then in `render.yaml`, remove `startCommand` (Render auto-detects Procfile).

---

## Quick Reference

| File | Purpose | Current Status |
|------|---------|----------------|
| `Dockerfile` | Docker build & start command | ✅ Configured |
| `render.yaml` | Render Blueprint (Docker) | ✅ Configured |
| `render-python.yaml` | Alternative Python runtime | ⚠️ Optional |
| `start.sh` | Standalone start script | ⚠️ Optional |
| `requirements.txt` | Python dependencies | ✅ Complete |

---

## Current Start Command Summary

**Your project uses**: Docker runtime with Dockerfile CMD

**Start command**:
```bash
gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 2 --timeout 120 backend.api.app:app
```

**This means**:
- ✅ No manual start command configuration needed in Render
- ✅ Same command works locally and in production
- ✅ PORT automatically set by Render (10000)
- ✅ Defaults to 5001 for local development

**To deploy**: Just push to GitHub, Render handles the rest!

---

## Next Steps

1. ✅ Your start command is already configured
2. Push code to GitHub: `git push origin main`
3. Create Render web service (use `render.yaml` blueprint)
4. Add `OPENAI_API_KEY` in Render dashboard
5. Deploy! 🚀

---

**Questions?** Check the [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment guide.
