# India AQI Tracker 🌍

A comprehensive web application for tracking and analyzing Air Quality Index (AQI) data across Indian districts. Built with **Astro** frontend and **FastAPI** backend.

> For detailed project information, see [README_PROJECT.md](README_PROJECT.md)

## ✨ Quick Start

### Frontend
```bash
npm install
npm run dev        # Development server at localhost:4321
npm run build      # Production build
npm run preview    # Preview production build
```

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📋 Documentation

- **[README_PROJECT.md](README_PROJECT.md)** - Complete project documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guides
- **[LICENSE](LICENSE)** - MIT License
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community guidelines

## 🚀 Deploy to Netlify

The project is pre-configured for Netlify:

1. Push to GitHub: `git push origin main`
2. Connect to Netlify at [netlify.com](https://netlify.com)
3. Configure build: `npm run build` → `dist`
4. Site goes live! 🎉

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment options.

## 🛠️ Tech Stack

- **Frontend**: Astro 7.x + Tailwind CSS 4.x
- **Backend**: FastAPI + SQLite/PostgreSQL
- **Hosting**: Netlify (Frontend) + Railway/Render/AWS (Backend)

## 📊 Features

- Real-time AQI tracking across districts
- District comparison tools
- Historical data analysis
- Forecasting & trends
- Responsive design
- Interactive visualizations

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by Tanish Thakur**
