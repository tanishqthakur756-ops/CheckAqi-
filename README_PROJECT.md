# India AQI Tracker 🌍

A comprehensive web application for tracking and analyzing Air Quality Index (AQI) data across Indian districts. Built with **Astro** frontend and **FastAPI** backend.

## ✨ Features

- **Real-time AQI Data**: Track air quality across all Indian districts
- **District Comparison**: Compare AQI levels between different regions
- **Forecasting**: View AQI trends and predictions
- **Historical Analysis**: Analyze historical data patterns
- **Seasonal Insights**: Understand seasonal pollution variations
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Interactive Visualizations**: Charts and gauges for easy data interpretation

## 🛠️ Tech Stack

### Frontend
- **Astro 7.x** - Fast, static-first site builder
- **Tailwind CSS 4.x** - Utility-first CSS framework
- **JavaScript/TypeScript** - For interactivity

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite/PostgreSQL** - Database
- **Python 3.12+** - Backend runtime

## 📋 Prerequisites

- Node.js 22+ (for frontend)
- Python 3.12+ (for backend)
- npm or yarn (package manager)

## 🚀 Getting Started

### Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The frontend will be available at `http://localhost:4321`

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

## 📁 Project Structure

```
├── src/
│   ├── components/        # Reusable Astro components
│   ├── layouts/          # Page layouts
│   ├── pages/            # Route pages
│   └── styles/           # Global styles
├── public/               # Static assets
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── main.py      # FastAPI app entry
│   │   ├── api/         # API routes
│   │   ├── models/      # SQLAlchemy models
│   │   └── data/        # Database scripts
│   └── requirements.txt
├── netlify.toml          # Netlify configuration
└── package.json          # Node dependencies
```

## 🌐 Deployment

### Netlify (Frontend)

This project is pre-configured for Netlify deployment:

1. Push code to GitHub
2. Connect repository to Netlify
3. Build command: `npm run build`
4. Publish directory: `dist`
5. Node version: 22

Your site will be live in minutes!

### Backend Deployment

Backend can be deployed to:
- Vercel (Python support)
- Railway
- Render
- AWS (EC2, Lambda)
- Heroku

## 📊 API Documentation

Once the backend is running, visit: `http://localhost:8000/docs`

This provides interactive API documentation powered by Swagger UI.

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root (frontend) and `backend/.env`:

```env
# Frontend
PUBLIC_API_URL=https://your-api-domain.com

# Backend
DATABASE_URL=sqlite:///aqi_tracker.db
# or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/aqi_db
```

## 📝 Available Scripts

### Frontend
- `npm run dev` - Start dev server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run check` - TypeScript type checking
- `npm run astro` - Astro CLI commands

### Backend
- `uvicorn app.main:app --reload` - Start with hot reload
- `pytest` - Run tests
- `python -m alembic upgrade head` - Database migrations

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙋 Support

Have questions or found a bug? 
- Open an [Issue](https://github.com/tanishqthakur756-ops/CheckAqi-/issues)
- Start a [Discussion](https://github.com/tanishqthakur756-ops/CheckAqi-/discussions)

## 📚 Learn More

- [Astro Documentation](https://docs.astro.build)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Netlify Docs](https://docs.netlify.com)

---

**Built with ❤️ by Tanish Thakur**
