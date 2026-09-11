# Deployment Guide

This guide covers deploying India AQI Tracker to various platforms.

## Frontend Deployment (Netlify)

### Initial Setup

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Create Netlify Account**
   - Visit [netlify.com](https://netlify.com)
   - Sign up with GitHub

3. **Connect Repository**
   - Click "Add new site"
   - Select "Import an existing project"
   - Choose GitHub and authorize
   - Select `tanishqthakur756-ops/CheckAqi-` repository

4. **Configure Build Settings**
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
   - **Node version**: Add `22` to Environment variables

5. **Deploy**
   - Click "Deploy site"
   - Wait for build to complete
   - Your site will have a Netlify URL

### Custom Domain

1. Go to Site settings → Domain management
2. Add your custom domain
3. Update DNS records with Netlify nameservers
4. SSL certificate will be auto-generated

### Environment Variables

In Netlify dashboard:
1. Go to Site settings → Build & deploy → Environment
2. Add build environment variables:
   ```
   PUBLIC_API_URL=https://your-api-domain.com
   NODE_VERSION=22
   ```

## Backend Deployment

### Option 1: Railway (Recommended for Beginners)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set DATABASE_URL=your_database_url

# Deploy
railway up
```

### Option 2: Render

1. Push code to GitHub
2. Create Render account at [render.com](https://render.com)
3. Create new "Web Service"
4. Connect GitHub repository
5. Configure:
   - **Runtime**: Python 3.12
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Add environment variables
7. Deploy

### Option 3: Vercel with Python

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts
4. Configure `vercel.json`:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "functions": {
    "api/**": {
      "runtime": "python3.12"
    }
  }
}
```

### Option 4: AWS EC2

```bash
# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update
sudo yum install python3.12 python3.12-venv nodejs npm

# Clone repository
git clone https://github.com/tanishqthakur756-ops/CheckAqi-.git
cd CheckAqi-/backend

# Setup
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run with systemd
sudo tee /etc/systemd/system/aqi-tracker.service > /dev/null <<EOF
[Unit]
Description=AQI Tracker API
After=network.target

[Service]
Type=notify
User=ec2-user
WorkingDirectory=/home/ec2-user/CheckAqi-/backend
ExecStart=/home/ec2-user/CheckAqi-/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable aqi-tracker
sudo systemctl start aqi-tracker
```

## Database Setup

### SQLite (Development)
- Comes pre-configured
- Data stored in `aqi_tracker.db`

### PostgreSQL (Production)

```bash
# Install PostgreSQL
# On Ubuntu:
sudo apt-get install postgresql postgresql-contrib

# Create database
createdb aqi_tracker

# Set connection string
export DATABASE_URL="postgresql://user:password@localhost/aqi_tracker"

# Run migrations
python -m alembic upgrade head
```

## CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Frontend
        run: |
          npm install
          npm run build
          
      - name: Deploy to Netlify
        uses: nflick/actions-netlify@v1.2
        with:
          publish-dir: './dist'
          github-token: ${{ secrets.GITHUB_TOKEN }}
          netlify-config-path: './netlify.toml'
        env:
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
      
      - name: Deploy Backend
        if: github.ref == 'refs/heads/main'
        run: |
          cd backend
          # Your backend deployment script
```

## Monitoring

### Netlify Logs
- Netlify Dashboard → Deploys → Deploy logs

### Backend Logs
- Railway/Render dashboards have built-in log viewers
- For self-hosted: Use systemd journal or Docker logs

## Health Checks

Test your deployment:

```bash
# Frontend
curl https://your-netlify-domain.com

# Backend API
curl https://your-api-domain.com/docs
```

## Rollback

### Frontend (Netlify)
- Dashboard → Deploys → Select previous deploy → "Restore"

### Backend (Railway/Render)
- Dashboard → Deployments → Previous version

## Support

For deployment issues:
- Check platform-specific documentation
- Review GitHub Issues
- Open a Discussion
