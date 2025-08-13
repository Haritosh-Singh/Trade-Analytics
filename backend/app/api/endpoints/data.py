# backend/app/api/endpoints/data.py
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import os

router = APIRouter()

DATA_PATH = "/home/poweranger/trade-optimization-system/data/processed"

@router.get("/countries")
async def get_countries():
    """Get list of all countries"""
    try:
        df = pd.read_csv(f"{DATA_PATH}/countries.csv")
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading countries: {str(e)}")

@router.get("/products")
async def get_products(category_id: Optional[int] = Query(None)):
    """Get list of products, optionally filtered by category"""
    try:
        df = pd.read_csv(f"{DATA_PATH}/products.csv")
        if category_id:
            df = df[df['category_id'] == category_id]
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading products: {str(e)}")

@router.get("/dealers")
async def get_dealers(country_id: Optional[int] = Query(None)):
    """Get list of dealers with enhanced information for CRM"""
    try:
        dealers_df = pd.read_csv(f"{DATA_PATH}/dealers.csv")
        countries_df = pd.read_csv(f"{DATA_PATH}/countries.csv")
        transactions_df = pd.read_csv(f"{DATA_PATH}/trade_transactions.csv")
        
        if country_id:
            dealers_df = dealers_df[dealers_df['country_id'] == country_id]
        
        result = []
        for _, dealer in dealers_df.iterrows():
            # Get country name
            country_name = countries_df[countries_df['id'] == dealer['country_id']]['name'].iloc[0]
            
            # Calculate dealer performance metrics
            dealer_transactions = transactions_df[transactions_df['dealer_id'] == dealer['id']]
            if not dealer_transactions.empty:
                avg_profit = dealer_transactions['profit_margin_percentage'].mean()
                total_transactions = len(dealer_transactions)
                avg_cost = dealer_transactions['total_cost'].mean()
            else:
                avg_profit = 0
                total_transactions = 0
                avg_cost = 0
            
            # Determine main product (placeholder logic)
            main_products = ['Electronics', 'Textiles', 'Automotive', 'Agriculture', 'Chemicals']
            main_product = main_products[dealer['id'] % len(main_products)]
            
            # Calculate performance rating
            performance_rating = min(100, max(0, avg_profit * 5))  # Scale profit to 0-100
            performance_category = 'High' if performance_rating >= 80 else 'Medium' if performance_rating >= 60 else 'Low'
            
            result.append({
                'id': dealer['id'],
                'name': dealer['name'],
                'country': country_name,
                'contact_email': dealer['email'],  # Fixed column name
                'main_product': main_product,
                'performance_rating': round(performance_rating, 1),
                'performance_category': performance_category,
                'avg_profit': round(avg_profit, 2),
                'total_transactions': int(total_transactions),
                'avg_cost': round(avg_cost, 2),
                'overall_rating': dealer['overall_rating'],
                'is_active': dealer['is_active']
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading dealers: {str(e)}")

@router.get("/product-categories")
async def get_product_categories():
    """Get list of product categories"""
    try:
        df = pd.read_csv(f"{DATA_PATH}/product_categories.csv")
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading categories: {str(e)}")

@router.get("/transactions")
async def get_transactions(limit: int = Query(50, le=200)):
    """Get recent transactions"""
    try:
        df = pd.read_csv(f"{DATA_PATH}/trade_transactions.csv")
        df = df.sort_values('order_date', ascending=False).head(limit)
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading transactions: {str(e)}")

@router.get("/dashboard-summary")
async def get_dashboard_summary():
    """Get summary data for dashboard"""
    try:
        # Load all required data
        transactions_df = pd.read_csv(f"{DATA_PATH}/trade_transactions.csv")
        dealers_df = pd.read_csv(f"{DATA_PATH}/dealers.csv")
        countries_df = pd.read_csv(f"{DATA_PATH}/countries.csv")
        products_df = pd.read_csv(f"{DATA_PATH}/products.csv")
        
        # Calculate summary metrics
        total_transactions = len(transactions_df)
        avg_profit = transactions_df['profit_margin_percentage'].mean()
        total_trade_value = transactions_df['total_product_value'].sum()
        
        # Top countries by transaction volume
        top_countries = transactions_df.groupby('destination_country_id').size().sort_values(ascending=False).head(5)
        top_countries_data = []
        for country_id, count in top_countries.items():
            country_name = countries_df[countries_df['id'] == country_id]['name'].iloc[0]
            top_countries_data.append({
                'country': country_name,
                'transactions': int(count),
                'avg_profit': round(transactions_df[transactions_df['destination_country_id'] == country_id]['profit_margin_percentage'].mean(), 2)
            })
        
        # Recent transactions
        recent_transactions = transactions_df.sort_values('order_date', ascending=False).head(10)
        recent_data = []
        for _, transaction in recent_transactions.iterrows():
            dealer_name = dealers_df[dealers_df['id'] == transaction['dealer_id']]['name'].iloc[0]
            country_name = countries_df[countries_df['id'] == transaction['destination_country_id']]['name'].iloc[0]
            
            recent_data.append({
                'transaction_id': transaction['transaction_id'],
                'dealer': dealer_name,
                'country': country_name,
                'profit_margin': round(transaction['profit_margin_percentage'], 2),
                'status': transaction['status'],
                'order_date': transaction['order_date']
            })
        
        # Dealer performance
        dealer_performance = []
        for _, dealer in dealers_df.head(10).iterrows():
            dealer_transactions = transactions_df[transactions_df['dealer_id'] == dealer['id']]
            if not dealer_transactions.empty:
                avg_profit = dealer_transactions['profit_margin_percentage'].mean()
                transaction_count = len(dealer_transactions)
            else:
                avg_profit = 0
                transaction_count = 0
                
            dealer_performance.append({
                'name': dealer['name'],
                'country': 'India' if dealer['country_id'] == 1 else 'International',
                'avg_profit': round(avg_profit, 2),
                'transactions': transaction_count,
                'rating': dealer['overall_rating']
            })
        
        return {
            "summary": {
                "total_transactions": total_transactions,
                "avg_profit_margin": round(avg_profit, 2),
                "total_trade_value": round(total_trade_value, 2),
                "active_dealers": len(dealers_df[dealers_df['is_active'] == True]),
                "countries_served": len(countries_df) - 1,  # Excluding India
                "products_available": len(products_df)
            },
            "top_countries": top_countries_data,
            "recent_transactions": recent_data,
            "dealer_performance": dealer_performance,
            "trends": {
                "monthly_growth": 12.5,  # Placeholder
                "profit_trend": "increasing",
                "volume_trend": "stable"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard summary: {str(e)}")

@router.get("/tariffs")
async def get_tariffs():
    """Get country tariff and tax information"""
    try:
        df = pd.read_csv(f"{DATA_PATH}/country_tariffs.csv")
        countries_df = pd.read_csv(f"{DATA_PATH}/countries.csv")
        
        # Merge with country names and aggregate by country
        result = []
        country_tariffs = df.groupby('country_id').agg({
            'import_duty_rate': 'mean',
            'export_duty_rate': 'mean',
            'additional_taxes': 'first'
        }).reset_index()
        
        for _, tariff in country_tariffs.iterrows():
            try:
                country_name = countries_df[countries_df['id'] == tariff['country_id']]['name'].iloc[0]
                
                # Parse VAT from additional_taxes if it's a JSON string
                vat_rate = 0
                try:
                    import json
                    additional_taxes = json.loads(tariff['additional_taxes'].replace("'", '"'))
                    vat_rate = additional_taxes.get('vat', 0)
                except:
                    vat_rate = 0
                
                result.append({
                    'id': int(tariff['country_id']),
                    'country': country_name,
                    'tariff_rate': round(tariff['import_duty_rate'], 2),
                    'tax_rate': round(vat_rate, 2),
                    'export_duty': round(tariff['export_duty_rate'], 2)
                })
            except:
                continue
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading tariffs: {str(e)}")

@router.get("/analytics")
async def get_analytics():
    """Get analytics data for charts and graphs"""
    try:
        transactions_df = pd.read_csv(f"{DATA_PATH}/trade_transactions.csv")
        dealers_df = pd.read_csv(f"{DATA_PATH}/dealers.csv")
        countries_df = pd.read_csv(f"{DATA_PATH}/countries.csv")
        products_df = pd.read_csv(f"{DATA_PATH}/products.csv")
        
        # Profit data by country over time
        profit_data = []
        country_profits = transactions_df.groupby('destination_country_id')['profit_margin_percentage'].mean()
        for country_id, avg_profit in country_profits.items():
            country_name = countries_df[countries_df['id'] == country_id]['name'].iloc[0]
            profit_data.append({
                'country': country_name,
                'avg_profit': round(avg_profit, 2),
                'total_transactions': len(transactions_df[transactions_df['destination_country_id'] == country_id])
            })
        
        # Cost data by product
        cost_data = []
        product_costs = transactions_df.groupby('product_id')['total_cost'].mean()
        for product_id, avg_cost in product_costs.items():
            try:
                product_name = products_df[products_df['id'] == product_id]['name'].iloc[0]
                cost_data.append({
                    'product': product_name,
                    'avg_cost': round(avg_cost, 2),
                    'volume': len(transactions_df[transactions_df['product_id'] == product_id])
                })
            except:
                continue
        
        return {
            "profit_data": profit_data,
            "cost_data": cost_data,
            "monthly_trends": {
                "profit_growth": 15.0,
                "cost_reduction": -5.0,
                "volume_increase": 8.0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating analytics: {str(e)}")

from fastapi import UploadFile, File
from pydantic import BaseModel

class ManualDataEntry(BaseModel):
    data: str

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV file"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Save uploaded file temporarily
        file_path = f"{DATA_PATH}/uploaded_{file.filename}"
        content = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Read and validate CSV
        df = pd.read_csv(file_path)
        
        return {
            "message": f"File {file.filename} uploaded successfully",
            "rows": len(df),
            "columns": list(df.columns)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.post("/manual-entry")
async def manual_data_entry(data: ManualDataEntry):
    """Process manual data entry"""
    try:
        # For now, just log the data - in production you'd process and store it
        print(f"Manual data received: {data.data}")
        
        return {
            "message": "Data received successfully",
            "data_length": len(data.data),
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing manual data: {str(e)}")
