from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import numpy as np
import pandas as pd
from src.pipeline.real_predict import RealPredictPipeline
from typing import Optional

# Create FastAPI app
app = FastAPI(title="NASA Exoplanet Prediction API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Pydantic model for data validation
class ExoplanetData(BaseModel):
    koi_period: float
    koi_duration: float
    koi_depth: float
    koi_prad: float
    koi_teq: float
    koi_insol: float
    koi_model_snr: float
    koi_steff: float
    koi_slogg: float
    koi_srad: float
    koi_kepmag: float
    koi_fpflag_nt: int
    koi_fpflag_ss: int
    koi_fpflag_co: int
    koi_fpflag_ec: int

    @field_validator('koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 
                    'koi_teq', 'koi_insol', 'koi_model_snr', 'koi_steff',
                    'koi_slogg', 'koi_srad', 'koi_kepmag')
    @classmethod
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('Value must be positive')
        return v

    @field_validator('koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec')
    @classmethod
    def check_binary_flags(cls, v):
        if v not in [0, 1]:
            raise ValueError('Value must be 0 or 1')
        return v

# Custom data class to convert Pydantic model to DataFrame
class CustomData:
    def __init__(self, data: ExoplanetData):
        self.data = data
    
    def get_data_as_data_frame(self):
        data_dict = self.data.dict()
        return pd.DataFrame([data_dict])

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predictdata", response_class=HTMLResponse)
async def predict_datapoint_get(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predictdata", response_class=HTMLResponse)
async def predict_datapoint_post(
    request: Request,
    koi_period: float = Form(...),
    koi_duration: float = Form(...),
    koi_depth: float = Form(...),
    koi_prad: float = Form(...),
    koi_teq: float = Form(...),
    koi_insol: float = Form(...),
    koi_model_snr: float = Form(...),
    koi_steff: float = Form(...),
    koi_slogg: float = Form(...),
    koi_srad: float = Form(...),
    koi_kepmag: float = Form(...),
    koi_fpflag_nt: int = Form(...),
    koi_fpflag_ss: int = Form(...),
    koi_fpflag_co: int = Form(...),
    koi_fpflag_ec: int = Form(...)
):
    try:
        # Create Pydantic model from form data
        exoplanet_data = ExoplanetData(
            koi_period=koi_period,
            koi_duration=koi_duration,
            koi_depth=koi_depth,
            koi_prad=koi_prad,
            koi_teq=koi_teq,
            koi_insol=koi_insol,
            koi_model_snr=koi_model_snr,
            koi_steff=koi_steff,
            koi_slogg=koi_slogg,
            koi_srad=koi_srad,
            koi_kepmag=koi_kepmag,
            koi_fpflag_nt=koi_fpflag_nt,
            koi_fpflag_ss=koi_fpflag_ss,
            koi_fpflag_co=koi_fpflag_co,
            koi_fpflag_ec=koi_fpflag_ec
        )
        
        # Convert to DataFrame
        custom_data = CustomData(exoplanet_data)
        pred_df = custom_data.get_data_as_data_frame()
        
        print("Input Data:")
        print(pred_df)
        print("Before Prediction")

        # Make prediction using the actual trained model
        predict_pipeline = RealPredictPipeline()
        print("Mid Prediction")
        results = predict_pipeline.predict(pred_df)
        print("After Prediction")
        
        # Map prediction to human-readable labels
        prediction_label = {0: "FALSE POSITIVE", 1: "CANDIDATE", 2: "CONFIRMED"}.get(results[0], "UNKNOWN")
        
        return templates.TemplateResponse("home.html", {
            "request": request, 
            "results": prediction_label,
            "input_data": exoplanet_data.dict()
        })
        
    except Exception as e:
        return templates.TemplateResponse("home.html", {
            "request": request, 
            "error": f"Prediction error: {str(e)}"
        })

# API endpoint for programmatic access (JSON)
@app.post("/api/predict")
async def api_predict(data: ExoplanetData):
    try:
        custom_data = CustomData(data)
        pred_df = custom_data.get_data_as_data_frame()
        
        predict_pipeline = RealPredictPipeline()
        results = predict_pipeline.predict(pred_df)
        
        prediction_label = {0: "FALSE POSITIVE", 1: "CANDIDATE", 2: "CONFIRMED"}.get(results[0], "UNKNOWN")
        
        return {
            "prediction": prediction_label,
            "prediction_code": int(results[0]),
            "input_data": data.dict()
        }
        
    except Exception as e:
        return {"error": str(e)}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "NASA Exoplanet Prediction API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
