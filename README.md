# 🚀 NASA Exoplanet Prediction System
**Team AstroVenture** 🇵🇰🇦🇿

Advanced AI-powered system for detecting and classifying exoplanets using NASA's Kepler data.

## 🌟 Features

- **Real-time Exoplanet Classification**: CONFIRMED, CANDIDATE, or FALSE POSITIVE
- **Modern Web Interface**: Beautiful, responsive React frontend
- **FastAPI Backend**: High-performance Python API
- **Machine Learning Pipeline**: Intelligent prediction system
- **Space-themed UI**: Immersive cosmic experience

## 🛠️ Technology Stack

- **Frontend**: React 18, Tailwind CSS, Lucide Icons
- **Backend**: FastAPI, Pydantic, Uvicorn
- **ML**: Custom prediction algorithms
- **Styling**: Space-themed animations and effects

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Nasa-Space-App-Challenge
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

### Running the Application

1. **Start the backend**
```bash
python app.py
```

2. **Start the frontend** (in a new terminal)
```bash
./start_frontend.sh
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📊 How to Use

1. **Open** http://localhost:3000 in your browser
2. **Fill in the exoplanet data form** with the 15 required parameters
3. **Click "Predict Exoplanet"** to get instant classification
4. **View results** with confidence levels and recommendations

## 🧪 Test Data

Use these sample inputs to test the system:

### Earth-like Planet (CANDIDATE)
```
Orbital Period: 365.25 days
Transit Duration: 13.0 hours
Transit Depth: 0.000085
Planet Radius: 1.0 Earth radii
Equilibrium Temperature: 288K
Stellar Insolation: 1.0
Model SNR: 15.2
Stellar Temperature: 5778K
Stellar Surface Gravity: 4.44
Stellar Radius: 1.0 Solar radii
Kepler Magnitude: 12.5
All Flags: 0,0,0,1
```

## 🎯 API Endpoints

- `POST /api/predict` - Make exoplanet predictions
- `GET /health` - Health check
- `GET /` - Main application page

## 🌍 Team AstroVenture

**Countries**: Pakistan 🇵🇰, Azerbaijan 🇦🇿 & Kazakhstan 🇰🇿  
**Mission**: Advancing exoplanet detection through AI  
**Challenge**: NASA Space App Challenge 2025  

## 🤖 Development Tools

This project was developed and enhanced using **Cursor AI**, an advanced AI-powered code editor that significantly accelerated the development process through intelligent code generation, debugging, and optimization.  

## 📈 Prediction Classes

- **✅ CONFIRMED**: Verified exoplanets
- **⚠️ CANDIDATE**: Potential exoplanets requiring further study
- **❌ FALSE POSITIVE**: Non-planetary objects

## 🔬 Scientific Impact

This system helps astronomers:
- Prioritize follow-up observations
- Reduce false positives
- Accelerate exoplanet discovery
- Democratize space science

## 📝 License

Developed for NASA Space App Challenge 2025

---

**🚀 Exploring the cosmos, one prediction at a time!** ✨
