import sys
import os
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.utils import load_object

class RealPredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # Load the actual trained model and scaler
            model_path = 'notebooks/best_model.pkl'
            scaler_path = 'notebooks/scaler.pkl'
            
            model = load_object(file_path=model_path)
            scaler = load_object(file_path=scaler_path)
            
            # Apply the same transformations as in training
            # Apply log transformation to skewed columns (same as training)
            skewed_columns = ['koi_prad', 'koi_depth', 'koi_teq', 'koi_insol', 'koi_model_snr']
            features_transformed = features.copy()
            
            for col in skewed_columns:
                if col in features_transformed.columns:
                    features_transformed[col + '_log'] = np.log1p(features_transformed[col])
            
            # Drop original skewed columns
            features_transformed = features_transformed.drop(columns=skewed_columns, errors='ignore')
            
            # Ensure features are in the exact order the scaler expects
            feature_order = [
                'koi_period', 'koi_duration', 'koi_fpflag_nt', 'koi_fpflag_ss',
                'koi_fpflag_co', 'koi_fpflag_ec', 'koi_steff', 'koi_slogg', 'koi_srad',
                'koi_kepmag', 'koi_prad_log', 'koi_depth_log', 'koi_teq_log', 'koi_insol_log',
                'koi_model_snr_log'
            ]
            
            # Reorder features to match training order
            features_ordered = features_transformed[feature_order]
            
            # Apply the same preprocessing as during training
            data_scaled = scaler.transform(features_ordered)
            
            # Make prediction using the actual trained model
            predictions = model.predict(data_scaled)
            
            return predictions
            
        except Exception as e:
            raise CustomException(e, sys)
