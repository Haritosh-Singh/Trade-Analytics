# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Import routers
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.endpoints import predictions, data
from app.core.database import init_db

app = FastAPI(
    title="AI-Powered Import-Export Trade Optimization API",
    description="Machine Learning-based system for optimizing India's international trade operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predictions.router, prefix="/api/predictions", tags=["ML Predictions"])
app.include_router(data.router, prefix="/api/data", tags=["Data Management"])

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/")
async def root():
    return {
        "message": "🌍 AI-Powered Import-Export Trade Optimization API v1.0.0",
        "features": [
            "Profit Prediction ML Models",
            "Dealer Performance Ranking",
            "Country Trade Analysis", 
            "Route Optimization",
            "Risk Assessment"
        ],
        "endpoints": {
            "predictions": "/api/predictions/",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "trade-optimization-api",
        "version": "1.0.0"
    }

@app.get("/api/stats")
async def get_system_stats():
    """Get system statistics"""
    import pandas as pd
    
    data_path = "/home/poweranger/trade-optimization-system/data/processed"
    
    try:
        # Load data for statistics
        countries_df = pd.read_csv(f"{data_path}/countries.csv")
        dealers_df = pd.read_csv(f"{data_path}/dealers.csv")
        products_df = pd.read_csv(f"{data_path}/products.csv")
        transactions_df = pd.read_csv(f"{data_path}/trade_transactions.csv")
        
        return {
            "data_summary": {
                "countries": len(countries_df),
                "dealers": len(dealers_df),
                "products": len(products_df),
                "historical_transactions": len(transactions_df)
            },
            "business_metrics": {
                "avg_profit_margin": round(transactions_df['profit_margin_percentage'].mean(), 2),
                "total_trade_value": round(transactions_df['total_product_value'].sum(), 2),
                "avg_delivery_days": round((pd.to_datetime(transactions_df['actual_delivery_date']) - 
                                          pd.to_datetime(transactions_df['order_date'])).dt.days.mean(), 1),
                "active_dealers": len(dealers_df[dealers_df['is_active'] == True])
            },
            "top_countries": transactions_df.groupby('destination_country_id').size().sort_values(ascending=False).head().to_dict(),
            "system_status": "operational"
        }
    except Exception as e:
        return {"error": f"Failed to load statistics: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
