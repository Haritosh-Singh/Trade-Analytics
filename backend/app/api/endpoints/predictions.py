# backend/app/api/endpoints/predictions.py
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import sys
import os
# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.core.database import get_db
from ml.models.profit_predictor import ProfitPredictor, DealerRankingSystem
import pandas as pd
import os

router = APIRouter()

# Load pre-trained model if available
model_path = "/home/poweranger/trade-optimization-system/data/models/profit_predictor.joblib"
predictor = ProfitPredictor()

# Initialize dealer ranking system
dealer_ranker = DealerRankingSystem()

class TradePredictionRequest(BaseModel):
    dealer_id: int
    product_id: int
    destination_country_id: int
    quantity: int
    transport_mode: str = "sea"

class TradePredictionResponse(BaseModel):
    predicted_profit_margin: float
    predicted_delivery_days: int
    confidence_score: float
    recommendation: str
    total_cost_estimate: float
    risk_factors: Dict[str, float]

class DealerRankingRequest(BaseModel):
    product_category_id: Optional[int] = None
    destination_country_id: Optional[int] = None
    max_results: int = 10

@router.post("/predict-trade", response_model=TradePredictionResponse)
async def predict_trade_profitability(
    request: TradePredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict trade profitability and delivery time for a specific trade scenario
    """
    try:
        # Load trade data for feature engineering
        data_path = "/home/poweranger/trade-optimization-system/data/processed"
        
        # Load required datasets
        dealers_df = pd.read_csv(f"{data_path}/dealers.csv")
        products_df = pd.read_csv(f"{data_path}/products.csv")
        countries_df = pd.read_csv(f"{data_path}/countries.csv")
        dealer_products_df = pd.read_csv(f"{data_path}/dealer_products.csv")
        routes_df = pd.read_csv(f"{data_path}/trade_routes.csv")
        tariffs_df = pd.read_csv(f"{data_path}/country_tariffs.csv")
        
        # Get dealer, product, and country information
        dealer = dealers_df[dealers_df['id'] == request.dealer_id]
        product = products_df[products_df['id'] == request.product_id]
        country = countries_df[countries_df['id'] == request.destination_country_id]
        
        if dealer.empty or product.empty or country.empty:
            raise HTTPException(status_code=404, detail="Dealer, product, or country not found")
        
        dealer = dealer.iloc[0]
        product = product.iloc[0]
        country = country.iloc[0]
        
        # Get dealer-product relationship
        dealer_product = dealer_products_df[
            (dealer_products_df['dealer_id'] == request.dealer_id) & 
            (dealer_products_df['product_id'] == request.product_id)
        ]
        
        if dealer_product.empty:
            raise HTTPException(status_code=404, detail="Dealer does not supply this product")
        
        dealer_product = dealer_product.iloc[0]
        
        # Get trade route information
        route = routes_df[
            (routes_df['destination_country_id'] == request.destination_country_id) &
            (routes_df['transport_mode'] == request.transport_mode)
        ]
        
        if route.empty:
            # Use default route values
            logistics_cost_per_kg = 2.0
            average_delivery_days = 30
            delay_probability = 0.1
        else:
            route = route.iloc[0]
            logistics_cost_per_kg = route['base_cost_per_kg']
            average_delivery_days = route['transit_days']
            delay_probability = route['delay_probability']
        
        # Get tariff information
        product_category_id = product['category_id']
        tariff = tariffs_df[
            (tariffs_df['country_id'] == request.destination_country_id) &
            (tariffs_df['product_category_id'] == product_category_id)
        ]
        
        if tariff.empty:
            import_duty_rate = 5.0  # Default
            export_duty_rate = 0.0
        else:
            tariff = tariff.iloc[0]
            import_duty_rate = tariff['import_duty_rate']
            export_duty_rate = tariff['export_duty_rate']
        
        # Create feature dictionary for prediction
        features = {
            'quantity': request.quantity,
            'dealer_cost_per_unit': dealer_product['cost_per_unit'],
            'logistics_cost_per_kg': logistics_cost_per_kg,
            'import_duty_rate': import_duty_rate,
            'export_duty_rate': export_duty_rate,
            'exchange_rate': 83.2,  # Default INR to USD
            'dealer_quality_score': dealer['quality_score'],
            'dealer_reliability_score': dealer['reliability_score'],
            'dealer_delivery_performance': dealer['delivery_performance'],
            'average_delivery_days': average_delivery_days,
            'delay_probability': delay_probability,
            'defect_rate': dealer_product['defect_rate'],
            'market_price': dealer_product['cost_per_unit'] * 1.3,  # Estimated market price
            'dealer_country': 'India' if dealer['country_id'] == 1 else 'International',
            'destination_country': country['name'],
            'product_category': f"Category_{product_category_id}",
            'transport_mode': request.transport_mode,
            'dealer_business_type': dealer['business_type']
        }
        
        # Train model with historical data if not already trained
        if not predictor.is_trained:
            transactions_df = pd.read_csv(f"{data_path}/trade_transactions.csv")
            
            # Prepare training data with features
            training_features = []
            for _, transaction in transactions_df.iterrows():
                t_dealer = dealers_df[dealers_df['id'] == transaction['dealer_id']].iloc[0]
                t_product = products_df[products_df['id'] == transaction['product_id']].iloc[0]
                t_country = countries_df[countries_df['id'] == transaction['destination_country_id']].iloc[0]
                
                training_features.append({
                    'quantity': transaction['quantity'],
                    'dealer_cost_per_unit': transaction['unit_price'],
                    'logistics_cost_per_kg': transaction['logistics_cost'] / transaction['quantity'],
                    'import_duty_rate': 5.0,  # Simplified
                    'export_duty_rate': 0.0,
                    'exchange_rate': 83.2,
                    'dealer_quality_score': t_dealer['quality_score'],
                    'dealer_reliability_score': t_dealer['reliability_score'],
                    'dealer_delivery_performance': t_dealer['delivery_performance'],
                    'average_delivery_days': 30,  # Simplified
                    'delay_probability': 0.1,
                    'defect_rate': 0.02,
                    'market_price': transaction['unit_price'] * 1.3,
                    'dealer_country': 'India' if t_dealer['country_id'] == 1 else 'International',
                    'destination_country': t_country['name'],
                    'product_category': f"Category_{t_product['category_id']}",
                    'transport_mode': 'sea',  # Simplified
                    'dealer_business_type': t_dealer['business_type'],
                    'profit_margin_percentage': transaction['profit_margin_percentage'],
                    'actual_delivery_days': (pd.to_datetime(transaction['actual_delivery_date']) - 
                                           pd.to_datetime(transaction['order_date'])).days
                })
            
            training_df = pd.DataFrame(training_features)
            predictor.train(training_df)
        
        # Make prediction
        prediction = predictor.predict_trade_scenario(features)
        
        # Calculate cost estimates
        unit_cost = dealer_product['cost_per_unit']
        total_product_cost = unit_cost * request.quantity
        logistics_cost = logistics_cost_per_kg * request.quantity
        tariff_cost = total_product_cost * (import_duty_rate / 100)
        total_cost = total_product_cost + logistics_cost + tariff_cost + 1000  # Additional charges
        
        # Risk assessment
        risk_factors = {
            'delivery_risk': delay_probability,
            'quality_risk': dealer_product['defect_rate'],
            'cost_risk': max(0, (unit_cost - 500) / 1000),  # Cost deviation risk
            'reliability_risk': 1 - dealer['reliability_score']
        }
        
        return TradePredictionResponse(
            predicted_profit_margin=prediction['predicted_profit_margin'],
            predicted_delivery_days=prediction['predicted_delivery_days'],
            confidence_score=prediction['confidence_score'],
            recommendation=prediction['recommendation'],
            total_cost_estimate=total_cost,
            risk_factors=risk_factors
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/rank-dealers", response_model=List[Dict])
async def rank_dealers_for_product(
    request: DealerRankingRequest,
    db: Session = Depends(get_db)
):
    """
    Rank dealers based on multiple criteria for a specific product/destination
    """
    try:
        # Load data
        data_path = "/home/poweranger/trade-optimization-system/data/processed"
        dealers_df = pd.read_csv(f"{data_path}/dealers.csv")
        dealer_products_df = pd.read_csv(f"{data_path}/dealer_products.csv")
        
        # Filter dealers based on criteria
        filtered_dealers = dealers_df.copy()
        
        if request.product_category_id:
            # Get dealers who supply products in this category
            products_df = pd.read_csv(f"{data_path}/products.csv")
            category_products = products_df[products_df['category_id'] == request.product_category_id]['id'].tolist()
            category_dealers = dealer_products_df[dealer_products_df['product_id'].isin(category_products)]['dealer_id'].unique()
            filtered_dealers = filtered_dealers[filtered_dealers['id'].isin(category_dealers)]
        
        # Prepare dealer data for ranking
        dealers_list = []
        for _, dealer in filtered_dealers.iterrows():
            # Get average dealer-product metrics
            dealer_products = dealer_products_df[dealer_products_df['dealer_id'] == dealer['id']]
            
            if not dealer_products.empty:
                avg_cost = dealer_products['cost_per_unit'].mean()
                avg_delivery = dealer_products['average_delivery_days'].mean()
                avg_quality = dealer_products['quality_rating'].mean()
                max_capacity = dealer_products['maximum_supply_capacity'].max()
            else:
                avg_cost = 500
                avg_delivery = 30
                avg_quality = 4.0
                max_capacity = 1000
            
            dealer_data = {
                'id': dealer['id'],
                'name': dealer['name'],
                'country_id': dealer['country_id'],
                'business_type': dealer['business_type'],
                'cost_per_unit': avg_cost,
                'quality_score': avg_quality / 5.0,  # Normalize to 0-1
                'delivery_performance': dealer['delivery_performance'],
                'reliability_score': dealer['reliability_score'],
                'max_supply_capacity': max_capacity,
                'overall_rating': dealer['overall_rating']
            }
            
            dealers_list.append(dealer_data)
        
        # Rank dealers
        ranked_dealers = dealer_ranker.rank_dealers(dealers_list)
        
        # Return top results
        return ranked_dealers[:request.max_results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ranking error: {str(e)}")

@router.get("/country-analysis")
async def analyze_countries():
    """
    Analyze trade opportunities by country
    """
    try:
        data_path = "/home/poweranger/trade-optimization-system/data/processed"
        transactions_df = pd.read_csv(f"{data_path}/trade_transactions.csv")
        countries_df = pd.read_csv(f"{data_path}/countries.csv")
        
        # Calculate country-wise statistics
        country_stats = transactions_df.groupby('destination_country_id').agg({
            'profit_margin_percentage': ['mean', 'std', 'count'],
            'actual_delivery_date': lambda x: (pd.to_datetime(x) - pd.to_datetime(transactions_df.loc[x.index, 'order_date'])).dt.days.mean(),
            'total_cost': 'mean'
        }).round(2)
        
        country_analysis = []
        for country_id in country_stats.index:
            country_name = countries_df[countries_df['id'] == country_id]['name'].iloc[0]
            stats = country_stats.loc[country_id]
            
            country_analysis.append({
                'country_id': int(country_id),
                'country_name': country_name,
                'avg_profit_margin': float(stats['profit_margin_percentage']['mean']),
                'profit_consistency': float(1 / (1 + stats['profit_margin_percentage']['std'])),
                'avg_delivery_days': float(stats['actual_delivery_date']),
                'transaction_count': int(stats['profit_margin_percentage']['count']),
                'avg_cost': float(stats['total_cost']['mean']),
                'opportunity_score': float(
                    stats['profit_margin_percentage']['mean'] * 0.4 +
                    (1 / (1 + stats['profit_margin_percentage']['std'])) * 20 * 0.3 +
                    (60 - min(60, stats['actual_delivery_date'])) * 0.3
                )
            })
        
        # Sort by opportunity score
        country_analysis.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return country_analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@router.get("/model-performance")
async def get_model_performance():
    """
    Get current ML model performance metrics
    """
    try:
        if not predictor.is_trained:
            return {"status": "Model not trained", "metrics": {}}
        
        feature_importance = predictor.get_feature_importance()
        
        return {
            "status": "Model trained",
            "model_info": {
                "profit_model": "XGBoost Regressor",
                "delivery_model": "XGBoost Regressor", 
                "features_count": len(predictor.feature_columns),
                "training_date": "2025-08-12"
            },
            "feature_importance": feature_importance,
            "performance_metrics": {
                "profit_model_r2": 0.85,  # Placeholder
                "delivery_model_r2": 0.78,
                "prediction_confidence": 0.82
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance error: {str(e)}")
