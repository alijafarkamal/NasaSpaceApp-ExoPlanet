# NASA Exoplanet Prediction System (Kepler AI Classifier)

An end-to-end **AI-powered exoplanet classification system** built for the **NASA Space Apps Challenge 2025** by **Team AstroVenture (Pakistan, Azerbaijan & Kazakhstan)**.

This project uses **NASA Kepler Objects of Interest (KOI)** features to predict whether a target is:

- **CONFIRMED** (verified exoplanet)
- **CANDIDATE** (likely exoplanet, needs confirmation)
- **FALSE POSITIVE** (not an exoplanet)

It includes:
- A **FastAPI backend** (REST API + CSV batch prediction + PDF report generation)
- A **React frontend** for interactive use

---

## Demo / What It Does

### 1) Single Prediction (UI or API)
Provide 15 KOI parameters → model predicts the exoplanet class.

### 2) Batch Prediction via CSV Upload
Upload a CSV file → backend returns:
- per-row predictions
- summary counts for each class
- a downloadable **PDF report**

### 3) PDF Report Generation
A PDF report is generated automatically for CSV batch runs and stored under `temp/`.

---

## Project Structure

```text
.
├── app.py                      # FastAPI backend entry point
├── requirements.txt            # Python dependencies
├── src/
│   ├── pipeline/
│   │   ├── real_predict.py     # Loads trained model + scaler, applies transformations, predicts
│   │   └── simple_predict.py   # (Alternative/simple pipeline - if used)
│   ├── utils.py                # load_object() and utilities
│   ├── exception.py            # CustomException wrapper
│   └── logger.py               # Logging helpers
├── notebooks/
│   ├── best_model.pkl          # Trained model (loaded at runtime)
│   └── scaler.pkl              # Trained scaler (loaded at runtime)
└── frontend/                   # React frontend (Create React App)
```

---

## Tech Stack

### Backend
- **FastAPI** (API server)
- **Uvicorn** (ASGI server)
- **Pydantic** (validation)
- **Pandas / NumPy** (data handling)
- **scikit-learn + XGBoost** (ML)
- **ReportLab** (PDF reports)

### Frontend
- **React 18**
- **Tailwind CSS**
- **Axios**

---

## How The Prediction Works (High Level)

The backend uses `RealPredictPipeline` (`src/pipeline/real_predict.py`) which:

1. Loads:
   - `notebooks/best_model.pkl`
   - `notebooks/scaler.pkl`
2. Applies the same transformations used during training:
   - `log1p()` on skewed features:
     - `koi_prad`, `koi_depth`, `koi_teq`, `koi_insol`, `koi_model_snr`
   - Drops original skewed columns and keeps `*_log`
3. Reorders the features to the exact training order
4. Scales them with the saved scaler
5. Predicts class using the saved trained model

Output mapping used in the API/UI:
- `0 → FALSE POSITIVE`
- `1 → CANDIDATE`
- `2 → CONFIRMED`

---

## Getting Started (Local Setup)

### Prerequisites
- **Python 3.8+**
- **Node.js 16+** (or newer)
- npm

---

## Backend Setup (FastAPI)

### 1) Clone
```bash
git clone https://github.com/alijafarkamal/NasaSpaceApp-ExoPlanet.git
cd NasaSpaceApp-ExoPlanet
```

### 2) Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3) Run backend
```bash
python app.py
```

Backend will run at:
- API: `http://localhost:8000`
- Docs (Swagger): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

> Note: Make sure these files exist because the predictor loads them at runtime:
> - `notebooks/best_model.pkl`
> - `notebooks/scaler.pkl`

---

## Frontend Setup (React)

### 1) Install dependencies
```bash
cd frontend
npm install
```

### 2) (Optional) Configure API URL
Create `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000
```

### 3) Run frontend
```bash
npm start
```

Frontend will run at:
- `http://localhost:3000`

---

## Run Full App (Scripts)

This repo includes startup scripts:
- `./start_nasa_app.sh` (recommended, starts full system)
- `./start_app.sh`
- `./start_frontend.sh`

If needed, make them executable:
```bash
chmod +x start_nasa_app.sh start_app.sh start_frontend.sh
./start_nasa_app.sh
```

---

## API Reference

### `POST /api/predict` (Single Prediction)
**Request body (JSON):**
```json
{
  "koi_period": 365.25,
  "koi_duration": 13.0,
  "koi_depth": 0.000085,
  "koi_prad": 1.0,
  "koi_teq": 288,
  "koi_insol": 1.0,
  "koi_model_snr": 15.2,
  "koi_steff": 5778,
  "koi_slogg": 4.44,
  "koi_srad": 1.0,
  "koi_kepmag": 12.5,
  "koi_fpflag_nt": 0,
  "koi_fpflag_ss": 0,
  "koi_fpflag_co": 0,
  "koi_fpflag_ec": 0
}
```

**Response (example):**
```json
{
  "prediction": "CANDIDATE",
  "prediction_code": 1,
  "input_data": { "...": "..." }
}
```

---

### `POST /api/upload-csv` (Batch Prediction + PDF)
Upload a CSV (multipart/form-data). The backend will:
- validate required columns
- return prediction results + summary
- generate a PDF report in `temp/`
- provide `pdf_download_url`

---

### `GET /download-pdf/{filename}`
Downloads the generated PDF report.

---

## Required CSV Format

Your CSV must include these exact columns:

```text
koi_period, koi_duration, koi_depth, koi_prad, koi_teq, koi_insol, koi_model_snr,
koi_steff, koi_slogg, koi_srad, koi_kepmag, koi_fpflag_nt, koi_fpflag_ss, koi_fpflag_co, koi_fpflag_ec
```

---

## Common Issues / Troubleshooting

### Model files missing
If you get errors during prediction, confirm these exist:
- `notebooks/best_model.pkl`
- `notebooks/scaler.pkl`

### CORS / frontend can’t call backend
Backend CORS is currently configured for common local ports (3000, 5173).  
If your frontend runs somewhere else, update `allow_origins` in `app.py`.

---

## Contributing

Contributions are welcome:
1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-change`
3. Commit changes
4. Open a Pull Request

Suggested improvements:
- Add tests for `/api/predict` and `/api/upload-csv`
- Add Docker support (backend + frontend)
- Improve error responses (use proper HTTP status codes)

---

## Team AstroVenture

**Countries:** Pakistan, Azerbaijan & Kazakhstan  
**Event:** NASA Space Apps Challenge 2025  
**Mission:** Accelerate exoplanet discovery & classification using accessible AI tools.

---

## License

Developed for **NASA Space Apps Challenge 2025** (check repository for any additional licensing notes).

---

Exploring the cosmos, one prediction at a time.
