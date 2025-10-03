import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        # Create artifacts directory if it doesn't exist
        os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

    def load_koi_dataset(self):
        """Load Kepler Objects of Interest dataset"""
        try:
            df = pd.read_csv('Data/cumulative_2025.09.22_16.04.13.csv')
            logging.info('Read the KOI dataset as dataframe')
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def get_dataset_info(self, df):
        """Get basic information about the KOI dataset"""
        try:
            info = {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.value_counts().to_dict(),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'missing_values': df.isnull().sum().to_dict(),
                'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict()
            }
            logging.info("Dataset info collected successfully")
            return info
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Load KOI dataset
            df = self.load_koi_dataset()
            logging.info(f"Dataset loaded with shape: {df.shape}")

            # Get dataset information
            dataset_info = self.get_dataset_info(df)
            
            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info(f"Raw data saved to: {self.ingestion_config.raw_data_path}")

            logging.info("Data ingestion completed successfully")

            return df, dataset_info
            
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    raw_data, dataset_info = obj.initiate_data_ingestion()
    
    # Print dataset information
    print("\n" + "="*50)
    print("KOI DATASET INFORMATION")
    print("="*50)
    print(f"Shape: {dataset_info['shape']}")
    print(f"Memory Usage: {dataset_info['memory_usage_mb']:.2f} MB")
    print(f"Total Missing Values: {sum(dataset_info['missing_values'].values())}")
    print(f"Number of Columns: {len(dataset_info['columns'])}")
    
    print("\nData Types:")
    for dtype, count in dataset_info['dtypes'].items():
        print(f"  {dtype}: {count}")
    
    print("\nFirst 5 rows of the dataset:")
    print(raw_data.head())
    
    print("\nDataset info summary:")
    print(f"DataFrame type: {type(raw_data)}")
    print(f"DataFrame shape: {raw_data.shape}")