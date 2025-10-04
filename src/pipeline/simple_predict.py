import sys
import os
import pandas as pd
import numpy as np
from src.exception import CustomException

class SimplePredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # Simple rule-based prediction for demonstration
            # This is a placeholder - in production you'd load a trained model
            
            # Extract key features for simple rules
            koi_period = features['koi_period'].iloc[0]
            koi_prad = features['koi_prad'].iloc[0]
            koi_model_snr = features['koi_model_snr'].iloc[0]
            koi_fpflag_nt = features['koi_fpflag_nt'].iloc[0]
            koi_fpflag_ss = features['koi_fpflag_ss'].iloc[0]
            koi_fpflag_co = features['koi_fpflag_co'].iloc[0]
            koi_fpflag_ec = features['koi_fpflag_ec'].iloc[0]
            
            # Simple rule-based classification
            # Check for false positive flags
            if koi_fpflag_nt == 1 or koi_fpflag_ss == 1 or koi_fpflag_co == 1:
                return [0]  # FALSE POSITIVE
            
            # Check for good signal quality
            if koi_model_snr > 15 and koi_fpflag_ec == 1:
                if koi_period < 50 and koi_prad > 0.5:  # Short period, reasonable size
                    return [1]  # CANDIDATE
                elif koi_period < 20 and koi_prad > 1.0:  # Very short period, large planet
                    return [2]  # CONFIRMED
                else:
                    return [1]  # CANDIDATE
            elif koi_model_snr > 10:
                return [1]  # CANDIDATE
            else:
                return [0]  # FALSE POSITIVE
                
        except Exception as e:
            raise CustomException(e, sys)
