# backend/ml/models/profit_predictor.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import joblib
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

class ProfitPredictor:
    """
    ML Model for predicting trade profitability and delivery times
    """
    
    def __init__(self):
        self.profit_model = None
        self.delivery_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.is_trained = False
        
        # Model configurations
        self.profit_model_params = {
            'n_estimators': 200,
            'max_depth': 15,
            'learning_rate': 0.1,
            'random_state': 42
        }
        
        self.delivery_model_params = {
            'n_estimators': 150,
            'max_depth': 12,
            'learning_rate': 0.1,
            'random_state': 42
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer features for the ML models
        """
        features = data.copy()
        
        # Categorical features to encode
        categorical_features = [
            'dealer_country', 'destination_country', 'product_category',
            'transport_mode', 'dealer_business_type'
        ]
        
        # Encode categorical variables
        for feature in categorical_features:
            if feature in features.columns:
                if feature not in self.label_encoders:
                    self.label_encoders[feature] = LabelEncoder()
                    features[f'{feature}_encoded'] = self.label_encoders[feature].fit_transform(features[feature].astype(str))
                else:
                    features[f'{feature}_encoded'] = self.label_encoders[feature].transform(features[feature].astype(str))
        
        # Create derived features
        features['cost_per_unit_ratio'] = features['dealer_cost_per_unit'] / features['market_price']
        features['tariff_burden'] = features['import_duty_rate'] + features['export_duty_rate']
        features['dealer_performance_score'] = (
            features['dealer_quality_score'] * 0.3 +
            features['dealer_reliability_score'] * 0.3 +
            features['dealer_delivery_performance'] * 0.4
        )
        
        # Distance and logistics features
        features['logistics_cost_ratio'] = features['logistics_cost_per_kg'] / features['dealer_cost_per_unit']
        features['delivery_speed_score'] = 1 / (1 + features['average_delivery_days'] / 30)
        
        # Economic indicators
        features['exchange_rate_impact'] = features['exchange_rate'] * features['dealer_cost_per_unit']
        
        # Risk factors
        features['total_risk_score'] = (
            features['delay_probability'] * 0.5 +
            features['defect_rate'] * 0.3 +
            (1 - features['dealer_reliability_score']) * 0.2
        )
        
        # Seasonal factors (if date available)
        if 'order_date' in features.columns:
            features['order_month'] = pd.to_datetime(features['order_date']).dt.month
            features['order_quarter'] = pd.to_datetime(features['order_date']).dt.quarter
        
        return features
    
    def select_features(self, data: pd.DataFrame) -> List[str]:
        """
        Select relevant features for model training
        """
        numeric_features = [
            'quantity', 'dealer_cost_per_unit', 'logistics_cost_per_kg',
            'import_duty_rate', 'export_duty_rate', 'exchange_rate',
            'dealer_quality_score', 'dealer_reliability_score', 'dealer_delivery_performance',
            'average_delivery_days', 'delay_probability', 'defect_rate',
            'cost_per_unit_ratio', 'tariff_burden', 'dealer_performance_score',
            'logistics_cost_ratio', 'delivery_speed_score', 'exchange_rate_impact',
            'total_risk_score'
        ]
        
        categorical_encoded = [
            'dealer_country_encoded', 'destination_country_encoded',
            'product_category_encoded', 'transport_mode_encoded',
            'dealer_business_type_encoded'
        ]
        
        seasonal_features = ['order_month', 'order_quarter'] if 'order_month' in data.columns else []
        
        all_features = numeric_features + categorical_encoded + seasonal_features
        
        # Filter features that actually exist in the data
        available_features = [f for f in all_features if f in data.columns]
        
        self.feature_columns = available_features
        return available_features
    
    def train(self, data: pd.DataFrame, target_profit: str = 'profit_margin_percentage', 
              target_delivery: str = 'actual_delivery_days') -> Dict[str, float]:
        """
        Train both profit and delivery prediction models
        """
        self.logger.info("Starting model training...")
        
        # Prepare features
        features_df = self.prepare_features(data)
        feature_columns = self.select_features(features_df)
        
        X = features_df[feature_columns]
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=feature_columns)
        
        metrics = {}
        
        # Train profit prediction model
        if target_profit in data.columns:
            y_profit = data[target_profit].fillna(data[target_profit].mean())
            
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled_df, y_profit, test_size=0.2, random_state=42
            )
            
            self.profit_model = xgb.XGBRegressor(**self.profit_model_params)
            self.profit_model.fit(X_train, y_train)
            
            # Evaluate profit model
            y_pred = self.profit_model.predict(X_test)
            metrics['profit_r2'] = r2_score(y_test, y_pred)
            metrics['profit_rmse'] = np.sqrt(mean_squared_error(y_test, y_pred))
            metrics['profit_mae'] = mean_absolute_error(y_test, y_pred)
            
            self.logger.info(f"Profit Model - R²: {metrics['profit_r2']:.3f}, RMSE: {metrics['profit_rmse']:.3f}")
        
        # Train delivery prediction model
        if target_delivery in data.columns:
            y_delivery = data[target_delivery].fillna(data[target_delivery].mean())
            
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled_df, y_delivery, test_size=0.2, random_state=42
            )
            
            self.delivery_model = xgb.XGBRegressor(**self.delivery_model_params)
            self.delivery_model.fit(X_train, y_train)
            
            # Evaluate delivery model
            y_pred = self.delivery_model.predict(X_test)
            metrics['delivery_r2'] = r2_score(y_test, y_pred)
            metrics['delivery_rmse'] = np.sqrt(mean_squared_error(y_test, y_pred))
            metrics['delivery_mae'] = mean_absolute_error(y_test, y_pred)
            
            self.logger.info(f"Delivery Model - R²: {metrics['delivery_r2']:.3f}, RMSE: {metrics['delivery_rmse']:.3f}")
        
        self.is_trained = True
        self.logger.info("Model training completed successfully!")
        
        return metrics
    
    def predict_profit(self, features: Dict) -> float:
        """
        Predict profit margin for a trade scenario
        """
        if not self.is_trained or self.profit_model is None:
            raise ValueError("Profit model is not trained yet!")
        
        # Convert features to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Prepare features
        feature_df = self.prepare_features(feature_df)
        
        # Select and scale features
        X = feature_df[self.feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.profit_model.predict(X_scaled)[0]
        
        return float(prediction)
    
    def predict_delivery_time(self, features: Dict) -> int:
        """
        Predict delivery time in days
        """
        if not self.is_trained or self.delivery_model is None:
            raise ValueError("Delivery model is not trained yet!")
        
        # Convert features to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Prepare features
        feature_df = self.prepare_features(feature_df)
        
        # Select and scale features
        X = feature_df[self.feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.delivery_model.predict(X_scaled)[0]
        
        return int(max(1, prediction))  # Ensure at least 1 day
    
    def predict_trade_scenario(self, features: Dict) -> Dict[str, float]:
        """
        Predict both profit and delivery for a complete trade scenario
        """
        try:
            profit_prediction = self.predict_profit(features)
            delivery_prediction = self.predict_delivery_time(features)
            
            # Calculate confidence scores based on feature similarity to training data
            confidence_score = self._calculate_confidence(features)
            
            return {
                'predicted_profit_margin': profit_prediction,
                'predicted_delivery_days': delivery_prediction,
                'confidence_score': confidence_score,
                'recommendation': self._generate_recommendation(profit_prediction, delivery_prediction)
            }
        except Exception as e:
            self.logger.error(f"Prediction error: {str(e)}")
            raise
    
    def _calculate_confidence(self, features: Dict) -> float:
        """
        Calculate prediction confidence based on feature similarity to training data
        """
        # Simplified confidence calculation
        # In practice, you'd compare with training data distribution
        base_confidence = 0.8
        
        # Reduce confidence for extreme values or missing data
        if any(v is None for v in features.values()):
            base_confidence *= 0.9
        
        return base_confidence
    
    def _generate_recommendation(self, profit: float, delivery_days: int) -> str:
        """
        Generate a recommendation based on predictions
        """
        if profit > 15 and delivery_days <= 30:
            return "Highly Recommended - High profit with fast delivery"
        elif profit > 10 and delivery_days <= 45:
            return "Recommended - Good profit with reasonable delivery time"
        elif profit > 5:
            return "Consider - Moderate profit potential"
        else:
            return "Not Recommended - Low profit margin"
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from trained models
        """
        if not self.is_trained:
            return {}
        
        importance_dict = {}
        
        if self.profit_model:
            profit_importance = dict(zip(self.feature_columns, self.profit_model.feature_importances_))
            importance_dict['profit_model'] = profit_importance
        
        if self.delivery_model:
            delivery_importance = dict(zip(self.feature_columns, self.delivery_model.feature_importances_))
            importance_dict['delivery_model'] = delivery_importance
        
        return importance_dict
    
    def save_model(self, filepath: str) -> None:
        """
        Save trained model to disk
        """
        if not self.is_trained:
            raise ValueError("No trained model to save!")
        
        model_data = {
            'profit_model': self.profit_model,
            'delivery_model': self.delivery_model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'timestamp': datetime.now().isoformat()
        }
        
        joblib.dump(model_data, filepath)
        self.logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """
        Load trained model from disk
        """
        model_data = joblib.load(filepath)
        
        self.profit_model = model_data['profit_model']
        self.delivery_model = model_data['delivery_model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_columns = model_data['feature_columns']
        self.is_trained = True
        
        self.logger.info(f"Model loaded from {filepath}")

class DealerRankingSystem:
    """
    System for ranking dealers based on multiple criteria
    """
    
    def __init__(self):
        self.weights = {
            'cost_efficiency': 0.25,
            'quality_score': 0.25,
            'delivery_performance': 0.25,
            'reliability': 0.15,
            'capacity': 0.10
        }
    
    def calculate_dealer_score(self, dealer_data: Dict) -> float:
        """
        Calculate comprehensive dealer score
        """
        # Normalize cost efficiency (lower cost = higher score)
        max_cost = dealer_data.get('max_market_cost', dealer_data['cost_per_unit'] * 1.5)
        cost_score = (max_cost - dealer_data['cost_per_unit']) / max_cost
        
        # Other scores (0-1 scale)
        quality_score = dealer_data.get('quality_score', 0.8)
        delivery_score = dealer_data.get('delivery_performance', 0.8)
        reliability_score = dealer_data.get('reliability_score', 0.8)
        
        # Capacity score based on supply capability
        capacity_score = min(1.0, dealer_data.get('max_supply_capacity', 1000) / 10000)
        
        # Calculate weighted score
        total_score = (
            cost_score * self.weights['cost_efficiency'] +
            quality_score * self.weights['quality_score'] +
            delivery_score * self.weights['delivery_performance'] +
            reliability_score * self.weights['reliability'] +
            capacity_score * self.weights['capacity']
        )
        
        return round(total_score, 3)
    
    def rank_dealers(self, dealers_list: List[Dict]) -> List[Dict]:
        """
        Rank dealers and return sorted list
        """
        for dealer in dealers_list:
            dealer['ranking_score'] = self.calculate_dealer_score(dealer)
        
        # Sort by ranking score (descending)
        ranked_dealers = sorted(dealers_list, key=lambda x: x['ranking_score'], reverse=True)
        
        # Add rank position
        for i, dealer in enumerate(ranked_dealers):
            dealer['rank'] = i + 1
        
        return ranked_dealers
