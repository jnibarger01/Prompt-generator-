# 🚀 Quick Start Deployment Guide

## Fastest Path to Production: Render + Netlify (5 minutes)

### Step 1: Deploy Backend to Render (2 min)

1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo or upload directly
4. Configure:
   ```
   Name: prompt-generator-api
   Environment: Python 3
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Click **"Create Web Service"**
6. **Copy your Render URL** (e.g., `https://prompt-generator-api.onrender.com`)

### Step 2: Deploy Frontend to Netlify (2 min)

1. Go to [netlify.com](https://netlify.com) and sign up/login
2. Drag and drop the `frontend` folder onto Netlify dashboard
3. **Edit `frontend/index.html`**:
   - Find line: `const API_URL = window.location.hostname === 'localhost'`
   - Replace with your Render URL:
   ```javascript
   const API_URL = 'https://your-render-url.onrender.com'
   ```
4. Re-upload to Netlify
5. Done! Your app is live at `https://your-app.netlify.app`

### Step 3: Test Your Deployment (1 min)

1. Visit your Netlify URL
2. Click "Generate Prompts"
3. Select options and click "🚀 Generate Prompts"
4. Try "Optimize Prompt" tab with: "Give me a bowl cut"

---

## Alternative: One-Command Local Deployment

```bash
# Install dependencies
cd backend && pip install -r requirements.txt

# Start backend (Terminal 1)
uvicorn main:app --reload --port 8000

# Start frontend (Terminal 2)
cd ../frontend && python -m http.server 3000

# Visit: http://localhost:3000
```

---

## Alternative: Docker Deployment

```bash
# Start everything
docker-compose up

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

---

## Alternative: Railway (One Click)

1. Install CLI: `npm i -g @railway/cli`
2. Deploy:
   ```bash
   railway login
   railway init
   railway up
   ```

---

## Production Checklist

After deployment, update these in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.netlify.app",  # Your actual domain
        "http://localhost:3000"  # For local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Troubleshooting

**Backend not responding:**
- Check Render logs: Dashboard → Logs
- Verify Start Command uses `$PORT` variable
- Ensure requirements.txt is in backend/ folder

**Frontend can't reach backend:**
- Verify API_URL in frontend/index.html matches your Render URL
- Check browser console for CORS errors
- Confirm Render app is running (not sleeping)

**Render free tier sleeps after inactivity:**
- First request takes 30-60s to wake up
- Consider upgrading for always-on service
- Or use Railway/Vercel for better free tier

---

## Testing Production API

```bash
# Test backend health
curl https://your-render-url.onrender.com/

# Test generate
curl -X POST https://your-render-url.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt_type":"image","count":5,"specificity":"high"}'

# Test optimize
curl -X POST https://your-render-url.onrender.com/optimize \
  -H "Content-Type: application/json" \
  -d '{"vague_prompt":"Give me a bowl cut"}'
```

---

## Cost Breakdown

| Service | Free Tier | Limits | Upgrade Cost |
|---------|-----------|--------|-------------|
| Render  | ✅ Yes    | 750 hrs/mo, sleeps after 15 min | $7/mo |
| Netlify | ✅ Yes    | 100GB bandwidth/mo | $19/mo |
| Railway | ✅ Yes    | $5 free credit/mo | $5/mo per $5 |
| Vercel  | ✅ Yes    | 100GB bandwidth/mo | $20/mo |

**Recommended:** Render + Netlify = $0/month (perfect for MVP)

---

## Next Steps

1. Add authentication (Auth0, Clerk)
2. Add rate limiting (Redis + FastAPI middleware)
3. Add analytics (PostHog, Plausible)
4. Add monitoring (Sentry, LogRocket)
5. Custom domain (Namecheap, GoDaddy)

---

**Total deployment time: < 10 minutes**
**Total cost: $0/month (free tier)**

Now go build something awesome! 🚀
