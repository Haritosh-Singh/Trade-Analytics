# tests/test_ml_models/test_profit_predictor.py
import pytest
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.ml.models.profit_predictor import ProfitPredictor

class TestProfitPredictor:
    def setup_method(self):
        self.predictor = ProfitPredictor()
        self.sample_data = pd.DataFrame({
            'cost_per_unit': [100, 200, 150],
            'customs_duty_rate': [10, 15, 12],
            'shipping_cost_per_kg': [5, 8, 6],
            'weight_per_unit': [2, 3, 2.5],
            'country': ['USA', 'Germany', 'UK'],
            'category': ['Electronics', 'Machinery', 'Textiles'],
            'dealer_location': ['India', 'China', 'India'],
            'profit_per_unit': [50, 80, 60]
        })
    
    def test_feature_preparation(self):
        features = self.predictor.prepare_features(self.sample_data)
        assert 'total_duty_cost' in features.columns
        assert 'gst_cost' in features.columns
        assert 'shipping_cost' in features.columns
    
    def test_model_training(self):
        score = self.predictor.train(self.sample_data)
        assert score >= 0  # R² score should be non-negative
        assert hasattr(self.predictor.model, 'predict')
    
    def test_predictions(self):
        self.predictor.train(self.sample_data)
        predictions = self.predictor.predict(self.sample_data.iloc[:2])
        assert len(predictions) == 2
        assert all(isinstance(p, (int, float)) for p in predictions)
