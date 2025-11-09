# Deployment Guide

## Docker Deployment

### Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

### Local Docker Development

1. **Build and run with Docker Compose:**

```bash
# Make sure .env file exists with your OPENAI_API_KEY
cp .env.example .env
# Edit .env and add your API key

# Build and start the container
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

2. **Access the application:**
   - Backend API: `http://localhost:5001`
   - Health check: `http://localhost:5001/api/health`

3. **Test the API:**

```bash
curl http://localhost:5001/api/health
```

### Build Docker Image Manually

```bash
# Build the image
docker build -t literature-assistant .

# Run the container
docker run -d \
  -p 5001:5001 \
  -e OPENAI_API_KEY=your_key_here \
  --name literature-assistant \
  literature-assistant

# View logs
docker logs -f literature-assistant

# Stop and remove
docker stop literature-assistant
docker rm literature-assistant
```

## Deploying to Render

### Method 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**

```bash
git add .
git commit -m "Add Docker deployment configuration"
git push origin main
```

2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables:**
   - In the Render dashboard, go to your service
   - Navigate to "Environment" tab
   - Add:
     - Key: `OPENAI_API_KEY`
     - Value: Your OpenAI API key
   - Click "Save Changes"

4. **Deploy:**
   - Render will automatically build and deploy
   - Wait for deployment to complete
   - Your backend will be available at: `https://literature-assistant-backend.onrender.com`

### Method 2: Manual Web Service Setup

1. **Create New Web Service:**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service:**
   - **Name:** `literature-assistant-backend`
   - **Environment:** `Docker`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Dockerfile Path:** `./Dockerfile`

3. **Set Environment Variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PORT`: 5001 (auto-set by Render)

4. **Deploy:**
   - Click "Create Web Service"
   - Wait for build and deployment

### Update Frontend with Backend URL

After deploying to Render, update your frontend to use the new backend URL:

1. **Edit `frontend/app.js`:**

```javascript
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001'
    : 'https://literature-assistant-backend.onrender.com'; // Your Render URL
```

2. **Push the update:**

```bash
git add frontend/app.js
git commit -m "Update backend URL for production"
git push origin main
```

3. **GitHub Pages will auto-deploy the frontend**

## Render Free Tier Notes

⚠️ **Important for Free Tier Users:**

- Free tier services **spin down after 15 minutes of inactivity**
- First request after spin-down takes 30-60 seconds to wake up
- Consider upgrading to Starter ($7/month) for always-on service
- Free tier includes:
  - 750 hours/month
  - Automatic SSL
  - Global CDN

## Monitoring and Logs

### View Logs on Render

1. Go to your service dashboard
2. Click "Logs" tab
3. View real-time logs

### Health Check

Your service includes a health check endpoint:

```bash
curl https://your-app.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "openai_configured": true
}
```

## Troubleshooting

### Build Fails

1. **Check Dockerfile syntax:**
```bash
docker build -t test .
```

2. **Check requirements.txt:**
- Ensure all packages are available
- Pin specific versions

### Service Won't Start

1. **Check environment variables:**
   - Verify `OPENAI_API_KEY` is set
   - Check Render dashboard → Environment tab

2. **Check logs:**
   - Look for Python errors
   - Verify imports work

### CORS Issues

If you get CORS errors:

1. **Verify CORS is enabled in app.py:**
```python
from flask_cors import CORS
CORS(app)
```

2. **Check your frontend URL is correct**

### Slow Response Times

**For Free Tier:**
- Service spins down after inactivity
- First request takes longer (cold start)
- Consider upgrading to Starter tier

**For All Tiers:**
- OpenAI API calls take 30-60 seconds
- This is normal for GPT-4 analysis

## Scaling

### Horizontal Scaling

In `Dockerfile`, adjust workers:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "--timeout", "120", "backend.api.app:app"]
```

Workers recommendation:
- Free tier: 1-2 workers
- Starter tier: 2-4 workers
- Pro tier: 4-8 workers

### Vertical Scaling

Upgrade Render plan for more resources:
- **Starter**: $7/month, 512MB RAM
- **Standard**: $25/month, 2GB RAM
- **Pro**: $85/month, 4GB RAM

## Alternative Deployment Options

### Railway

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Deploy:
```bash
railway login
railway init
railway up
```

### Heroku

1. Create `Procfile`:
```
web: gunicorn backend.api.app:app
```

2. Deploy:
```bash
heroku create literature-assistant
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### DigitalOcean App Platform

1. Connect GitHub repository
2. Select Dockerfile
3. Set environment variables
4. Deploy

## Security Best Practices

1. **Never commit API keys:**
   - Keep `.env` in `.gitignore`
   - Use environment variables in Render

2. **HTTPS only:**
   - Render provides free SSL
   - Always use HTTPS URLs in production

3. **Rate limiting:**
   - Consider adding rate limiting for production
   - Use packages like `flask-limiter`

4. **Monitor costs:**
   - Track OpenAI API usage
   - Set spending limits in OpenAI dashboard

## Cost Estimation

### Render Costs
- Free tier: $0 (750 hours/month)
- Starter: $7/month (always-on)

### OpenAI API Costs
- GPT-4 Turbo: ~$0.01 per analysis
- 100 analyses: ~$1
- 1000 analyses: ~$10

### Total Monthly Cost (Estimate)
- **Light usage** (Free tier): $5-10/month (OpenAI only)
- **Medium usage** (Starter): $15-25/month
- **Heavy usage** (Pro): $50-100/month

## Support

For deployment issues:
- Render docs: https://render.com/docs
- Docker docs: https://docs.docker.com
- Open GitHub issue for project-specific problems

---

# Production Deployment (Render + GitHub Pages)

This guide walks you through deploying the Literature Assistant with GitHub Pages (frontend) and Render (backend).

## Prerequisites

- GitHub account
- Render account (free tier is fine)
- OpenAI API key
- Your code pushed to a GitHub repository

## Part 1: Deploy Backend to Render

### Step 1: Push Code to GitHub

1. **IMPORTANT**: Verify `.env` files are NOT committed (they're in `.gitignore`)
2. Commit and push all code:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

### Step 2: Set Up Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository:
   - Select `literature-assistant` repository
   - Click **"Connect"**

4. Configure the service:
   - **Name**: `literature-assistant-backend` (or any name you prefer)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: **Docker**
   - **Instance Type**: **Free** (or Starter for $7/month - no sleep)

5. **Environment Variables** - Click "Advanced" and add:
   - **OPENAI_API_KEY**: `sk-your-actual-api-key-here`
   - **ALLOWED_ORIGINS**: `https://YOURUSERNAME.github.io,http://localhost:5001`
     (Replace `YOURUSERNAME` with your actual GitHub username)
   - **PORT**: `10000`

6. Click **"Create Web Service"**

7. Wait for deployment (~5-10 minutes)
   - Watch the logs for any errors
   - Once deployed, note your backend URL: `https://literature-assistant-backend.onrender.com`

### Step 3: Test Backend

Visit: `https://YOUR-APP-NAME.onrender.com/api/health`

You should see: `{"openai_configured":true,"status":"healthy"}`

---

## Part 2: Update Frontend with Backend URL

### Step 4: Update Frontend Configuration

**YOU NEED TO DO THIS STEP:**

1. Open `frontend/app.js`
2. Find line 6 (around there)
3. Replace `https://literature-assistant.onrender.com` with **YOUR actual Render URL**
   ```javascript
   : (window.BACKEND_URL || 'https://YOUR-ACTUAL-APP-NAME.onrender.com');
   ```

4. Commit and push:
   ```bash
   git add frontend/app.js
   git commit -m "Update backend URL for production"
   git push origin main
   ```

---

## Part 3: Deploy Frontend to GitHub Pages

### Step 5: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** → **Pages** (in left sidebar)
3. Under "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: Select `main`
   - **Folder**: Select `/frontend`
4. Click **Save**

5. Wait ~2 minutes, then refresh the page
6. Your site URL will appear at the top: `https://YOURUSERNAME.github.io/literature-assistant/`

### Step 6: Update CORS in Render

1. Go back to Render dashboard
2. Open your web service
3. Go to **Environment** tab
4. Update `ALLOWED_ORIGINS` to include your actual GitHub Pages URL:
   ```
   https://YOURUSERNAME.github.io,http://localhost:5001,http://127.0.0.1:5001
   ```
5. Click **Save Changes**
6. Wait for automatic redeployment

---

## Part 4: Test the Deployed Application

1. Visit your GitHub Pages URL: `https://YOURUSERNAME.github.io/literature-assistant/`
2. Upload a PDF research paper
3. Click "Analyze Paper"
4. Verify it works!

---

## Troubleshooting

### CORS Errors
**Error**: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Fix**:
1. Check `ALLOWED_ORIGINS` in Render dashboard
2. Make sure it exactly matches your GitHub Pages URL (no trailing slash)
3. Redeploy backend after changing

### Backend Not Responding
**Error**: "Cannot connect to backend server"

**Fix**:
1. Check backend is running: visit `https://your-app.onrender.com/api/health`
2. Free tier sleeps after 15min - first request takes 30-50 seconds to wake up
3. Check Render logs for errors

### OpenAI API Errors
**Error**: "OpenAI API error" or "Unknown error"

**Fix**:
1. Verify `OPENAI_API_KEY` is set correctly in Render
2. Check you have credits in your OpenAI account
3. Verify model name is correct (`gpt-4o-mini` or `gpt-4o`)

### GitHub Pages 404
**Error**: 404 Page Not Found

**Fix**:
1. Make sure you selected `/frontend` folder, not root
2. Wait 2-3 minutes after enabling Pages
3. Check that `index.html` exists in `frontend/` folder

---

## Cost Breakdown

- **GitHub Pages**: Free
- **Render Free Tier**: Free (sleeps after 15min, wakes in ~30s)
- **Render Starter**: $7/month (always-on, faster)
- **OpenAI API**: ~$0.15-0.60 per document (GPT-4o-mini)

---

## Security Checklist

✅ API key stored only in Render environment variables (not in code)
✅ `.env` files are in `.gitignore`
✅ CORS configured to only allow your GitHub Pages domain
✅ HTTPS enabled on both platforms

---

## Next Steps

- Test thoroughly with different PDFs
- Monitor OpenAI usage at https://platform.openai.com/usage
- Consider upgrading Render to Starter plan for better performance
- Add custom domain (optional)

---

## Updating Your App

When you make code changes:

1. **Backend changes**:
   ```bash
   git add backend/
   git commit -m "Update backend"
   git push
   ```
   Render auto-deploys from main branch

2. **Frontend changes**:
   ```bash
   git add frontend/
   git commit -m "Update frontend"
   git push
   ```
   GitHub Pages auto-updates

---

Good luck! 🚀
