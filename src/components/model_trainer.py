import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from xgboost import XGBClassifier
import pickle
from dataclasses import dataclass
import sys
import os  # Make sure to import os

from src.exception import CustomException
from src.logger import logging

pd.set_option('display.max_columns', None)

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = 'artifacts/model.pkl'
    best_model_info_path: str = 'artifacts/best_model_info.pkl'  # Fixed: added colon

class ModelTrainer:
    def __init__(self):  # Fixed: was __init_(self)
        self.model_trainer_config = ModelTrainerConfig()
        # Create artifacts directory if it doesn't exist
        os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path), exist_ok=True)

    def initiate_model_trainer(self, train_data, test_data):
        try:
            logging.info("Starting model training process")
            
            # Split train and test data into features and target
            # Assuming the last column is the target variable
            X_train = train_data[:, :-1]
            y_train = train_data[:, -1]
            X_test = test_data[:, :-1]
            y_test = test_data[:, -1]
            
            logging.info(f"Training data shape: X_train {X_train.shape}, y_train {y_train.shape}")
            logging.info(f"Test data shape: X_test {X_test.shape}, y_test {y_test.shape}")
            
            # === Define Models & Hyperparameters ===
            models = {
                "Random Forest": RandomForestClassifier(random_state=42),
                "Decision Tree": DecisionTreeClassifier(random_state=42),
                "Gradient Boosting": GradientBoostingClassifier(random_state=42),
                "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
                "AdaBoost": AdaBoostClassifier(random_state=42),
                "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
            }

            params = {
                "Random Forest": {
                    'n_estimators': [100, 200],
                    'max_depth': [None, 20],
                    'max_features': ['sqrt', 'log2']
                },

                "Decision Tree": {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 10, 20],
                    'min_samples_split': [2, 5]
                },

                "Gradient Boosting": {
                    'n_estimators': [100, 200],
                    'learning_rate': [0.1, 0.05],
                    'max_depth': [3, 5]
                },

                "AdaBoost": {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.1, 1.0]
                },

                "Logistic Regression": {
                    'C': [0.1, 1.0, 10.0],
                    'solver': ['lbfgs', 'liblinear']
                },

                "XGBoost": {
                    'n_estimators': [100, 200],
                    'learning_rate': [0.1, 0.05],
                    'max_depth': [3, 5, 7]
                }
            }

            # === Train and Evaluate ===
            best_model = None
            best_score = 0
            best_model_name = ""
            model_scores = {}

            logging.info("Starting model training with GridSearchCV")

            for name, model in models.items():
                print(f"\n🔧 Training {name}...")
                logging.info(f"Training {name} with GridSearchCV")
                
                grid = GridSearchCV(model, params[name], cv=5, scoring='accuracy', n_jobs=-1)
                grid.fit(X_train, y_train)

                y_pred = grid.predict(X_test)

                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred, average='macro')
                rec = recall_score(y_test, y_pred, average='macro')
                f1 = f1_score(y_test, y_pred, average='macro')

                print(f"✅ {name} Results:")
                print(f"Accuracy:  {acc:.4f}")
                print(f"Precision: {prec:.4f}")
                print(f"Recall:    {rec:.4f}")
                print(f"F1-Score:  {f1:.4f}")
                print(f"Best Params: {grid.best_params_}")
                
                print("Confusion Matrix:")
                print(confusion_matrix(y_test, y_pred))
                print("Classification Report:")
                print(classification_report(y_test, y_pred))

                model_scores[name] = {
                    'accuracy': acc,
                    'precision': prec,
                    'recall': rec,
                    'f1_score': f1,
                    'best_params': grid.best_params_
                }

                if acc > best_score:
                    best_score = acc
                    best_model = grid.best_estimator_
                    best_model_name = name

                logging.info(f"{name} completed with accuracy: {acc:.4f}")

            # === Save Best Model ===
            print(f"\n🏆 Best Model: {best_model_name} with Accuracy: {best_score:.4f}")
            logging.info(f"Best model: {best_model_name} with accuracy: {best_score:.4f}")
            
            # Save the best model
            with open(self.model_trainer_config.trained_model_file_path, 'wb') as f:
                pickle.dump(best_model, f)
            
            # Save model scores and info for future reference
            best_model_info = {
                'best_model_name': best_model_name,
                'best_score': best_score,
                'best_params': model_scores[best_model_name]['best_params'],
                'all_model_scores': model_scores
            }
            
            with open(self.model_trainer_config.best_model_info_path, 'wb') as f:
                pickle.dump(best_model_info, f)
            
            logging.info(f"Best model saved to {self.model_trainer_config.trained_model_file_path}")
            logging.info(f"Model info saved to {self.model_trainer_config.best_model_info_path}")

            # Print summary of all models
            print("\n" + "="*50)
            print("📊 MODEL PERFORMANCE SUMMARY")
            print("="*50)
            for name, scores in model_scores.items():
                print(f"{name:20} | Accuracy: {scores['accuracy']:.4f} | F1-Score: {scores['f1_score']:.4f}")
            
            print(f"\n🎯 BEST MODEL: {best_model_name} (Accuracy: {best_score:.4f})")

            return best_score, best_model_name, model_scores

        except Exception as e:
            logging.error("Error in model training")
            raise CustomException(e, sys)


# For testing the class directly
if __name__ == "__main__":
    try:
        # Example usage - you'll need to load your actual train and test data
        # train_data = np.loadtxt('artifacts/train.csv', delimiter=',')
        # test_data = np.loadtxt('artifacts/test.csv', delimiter=',')
        
        # For now, we'll create dummy data for testing
        train_data=pd.read_csv('artifacts/train.csv').to_numpy()
        test_data=pd.read_csv('artifacts/test.csv').to_numpy()
        model_trainer = ModelTrainer()
        best_score, best_model_name, model_scores = model_trainer.initiate_model_trainer(train_data, test_data)
        
        print(f"\nTraining completed! Best model: {best_model_name} with accuracy: {best_score:.4f}")
        
    except Exception as e:
        print(f"Error during model training: {e}")
        import traceback
        traceback.print_exc()