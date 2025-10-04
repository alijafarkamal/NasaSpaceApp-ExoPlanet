# ???? NASA Exoplanet Prediction System

**Team AstroVenture** ????????????????????????

Advanced AI-powered system for detecting and classifying exoplanets using NASA's Kepler data with beautiful React frontend and FastAPI backend.

## ???? Features

- **Real-time Exoplanet Classification**: CONFIRMED, CANDIDATE, or FALSE POSITIVE
- **Modern Web Interface**: Beautiful, responsive React frontend with NASA-themed UI
- **FastAPI Backend**: High-performance Python API with automatic documentation
- **CSV Batch Processing**: Upload multiple exoplanet data points for batch predictions
- **PDF Report Generation**: Automatic generation of professional prediction reports
- **Interactive Visualizations**: Pie charts and progress bars for prediction results
- **Machine Learning Pipeline**: Intelligent prediction system with confidence scores

## ??????? Technology Stack

- **Frontend**: React 18, TypeScript, Material-UI, Recharts, Axios
- **Backend**: FastAPI, Pydantic, Uvicorn, ReportLab
- **ML**: Scikit-learn, XGBoost, Custom prediction algorithms
- **Styling**: NASA-themed dark UI with space gradients and animations

## ???? Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/alijafarkamal/NasaSpaceApp-ExoPlanet.git
cd NasaSpaceApp-ExoPlanet
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt --break-system-packages
```

3. **Install frontend dependencies**
```bash
cd frontend
npm install
cd ..
```

### Running the Application

**Option 1: Use the startup script (Recommended)**
```bash
./start_nasa_app.sh
```

**Option 2: Manual startup**
```bash
# Terminal 1 - Backend
python3 app.py

# Terminal 2 - Frontend
cd frontend
npm start
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## ???? How to Use

### Single Prediction
1. Open http://localhost:3000 in your browser
2. Fill in the exoplanet data form with the 15 required parameters
3. Click "Predict Exoplanet Classification" to get instant classification
4. View results with confidence levels and interactive charts

### Batch CSV Processing
1. Click the "Batch CSV Upload" tab
2. Upload a CSV file with the required columns (see format below)
3. Click "Process CSV" to run batch predictions
4. Download the PDF report with detailed results

## ???? Required CSV Format

Your CSV file must contain these exact columns:
```
koi_period, koi_duration, koi_depth, koi_prad, koi_teq, koi_insol, koi_model_snr, koi_steff, koi_slogg, koi_srad, koi_kepmag, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec
```

## ???? Test Data

Use the provided `sample_exoplanet_data.csv` file for testing, or try these sample inputs:

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
All Flags: 0,0,0,0
```

## ???? API Endpoints

- `POST /api/predict` - Make single exoplanet predictions
- `POST /api/upload-csv` - Batch CSV processing
- `GET /download-pdf/{filename}` - Download PDF reports
- `GET /health` - Health check
- `GET /` - Main application page
- `GET /docs` - Interactive API documentation

## ???? Prediction Classes

- **??? CONFIRMED**: Verified exoplanets (High confidence)
- **?????? CANDIDATE**: Potential exoplanets requiring further study
- **??? FALSE POSITIVE**: Non-planetary objects or stellar variability

## ???? Scientific Impact

This system helps astronomers:
- Prioritize follow-up observations
- Reduce false positives in exoplanet surveys
- Accelerate exoplanet discovery process
- Democratize space science through accessible AI tools

## ???? Team AstroVenture

**Countries**: Pakistan ????????, Azerbaijan ???????? & Kazakhstan ????????  
**Mission**: Advancing exoplanet detection through AI  
**Challenge**: NASA Space App Challenge 2025

## ???? Development Tools

This project was developed and enhanced using **Cursor AI**, an advanced AI-powered code editor that significantly accelerated the development process through intelligent code generation, debugging, and optimization.

## ???? License

Developed for NASA Space App Challenge 2025

---

**???? Exploring the cosmos, one prediction at a time!** ???
