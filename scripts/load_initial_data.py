#!/usr/bin/env python3
"""
Load Initial Trade Data for AI-Powered Import-Export Optimization System
Generates comprehensive dummy data for system testing and demonstration
"""

import pandas as pd
import numpy as np
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List
import os

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

class TradeDataGenerator:
    """
    Generate comprehensive dummy trade data
    """
    
    def __init__(self):
        # Top 10 GDP Countries data
        self.countries = [
            {'name': 'India', 'code': 'IN', 'gdp_rank': 5, 'currency': 'INR', 'base_import_duty': 0.0, 'base_export_duty': 0.0},
            {'name': 'United States', 'code': 'US', 'gdp_rank': 1, 'currency': 'USD', 'base_import_duty': 2.5, 'base_export_duty': 0.0},
            {'name': 'China', 'code': 'CN', 'gdp_rank': 2, 'currency': 'CNY', 'base_import_duty': 7.5, 'base_export_duty': 0.0},
            {'name': 'Germany', 'code': 'DE', 'gdp_rank': 4, 'currency': 'EUR', 'base_import_duty': 4.2, 'base_export_duty': 0.0},
            {'name': 'Japan', 'code': 'JP', 'gdp_rank': 3, 'currency': 'JPY', 'base_import_duty': 3.8, 'base_export_duty': 0.0},
            {'name': 'United Kingdom', 'code': 'GB', 'gdp_rank': 6, 'currency': 'GBP', 'base_import_duty': 3.2, 'base_export_duty': 0.0},
            {'name': 'France', 'code': 'FR', 'gdp_rank': 7, 'currency': 'EUR', 'base_import_duty': 4.1, 'base_export_duty': 0.0},
            {'name': 'Italy', 'code': 'IT', 'gdp_rank': 8, 'currency': 'EUR', 'base_import_duty': 4.0, 'base_export_duty': 0.0},
            {'name': 'Brazil', 'code': 'BR', 'gdp_rank': 9, 'currency': 'BRL', 'base_import_duty': 8.2, 'base_export_duty': 0.0},
            {'name': 'Canada', 'code': 'CA', 'gdp_rank': 10, 'currency': 'CAD', 'base_import_duty': 2.8, 'base_export_duty': 0.0},
        ]
        
        # Product categories with HS codes
        self.product_categories = [
            {'name': 'Textiles & Garments', 'hs_code_prefix': '50-63', 'description': 'Cotton, silk, wool textiles and ready-made garments'},
            {'name': 'Agricultural Products', 'hs_code_prefix': '01-24', 'description': 'Rice, spices, tea, coffee, fruits'},
            {'name': 'Pharmaceuticals', 'hs_code_prefix': '30', 'description': 'Generic medicines and APIs'},
            {'name': 'Chemicals', 'hs_code_prefix': '28-38', 'description': 'Organic and inorganic chemicals'},
            {'name': 'Machinery', 'hs_code_prefix': '84-85', 'description': 'Industrial machinery and electrical equipment'},
            {'name': 'Automotive Parts', 'hs_code_prefix': '87', 'description': 'Auto components and parts'},
            {'name': 'Jewelry & Gems', 'hs_code_prefix': '71', 'description': 'Precious stones and jewelry'},
            {'name': 'IT Hardware', 'hs_code_prefix': '85', 'description': 'Computer hardware and telecom equipment'},
            {'name': 'Leather Products', 'hs_code_prefix': '41-43', 'description': 'Leather goods and footwear'},
            {'name': 'Handicrafts', 'hs_code_prefix': '95-96', 'description': 'Traditional handicrafts and art items'}
        ]
        
        # Exchange rates (INR to other currencies) as of August 2025
        self.exchange_rates = {
            'USD': 83.2, 'CNY': 11.8, 'EUR': 91.5, 'JPY': 0.57,
            'GBP': 105.8, 'BRL': 15.2, 'CAD': 61.4, 'INR': 1.0
        }
        
        # Transport modes with characteristics
        self.transport_modes = [
            {'mode': 'sea', 'cost_multiplier': 1.0, 'time_multiplier': 1.0, 'reliability': 0.95},
            {'mode': 'air', 'cost_multiplier': 4.5, 'time_multiplier': 0.15, 'reliability': 0.98},
            {'mode': 'road', 'cost_multiplier': 2.0, 'time_multiplier': 0.8, 'reliability': 0.85},
            {'mode': 'rail', 'cost_multiplier': 1.5, 'time_multiplier': 0.9, 'reliability': 0.90}
        ]
    
    def generate_countries_data(self) -> pd.DataFrame:
        """Generate countries master data"""
        countries_with_id = []
        for i, country in enumerate(self.countries):
            country_dict = country.copy()
            country_dict['id'] = i + 1
            countries_with_id.append(country_dict)
        return pd.DataFrame(countries_with_id)
    
    def generate_product_categories_data(self) -> pd.DataFrame:
        """Generate product categories data"""
        categories_with_id = []
        for i, category in enumerate(self.product_categories):
            category_dict = category.copy()
            category_dict['id'] = i + 1
            categories_with_id.append(category_dict)
        return pd.DataFrame(categories_with_id)
    
    def generate_products_data(self, num_products: int = 50) -> pd.DataFrame:
        """Generate products data"""
        products = []
        
        # Sample product names by category
        product_templates = {
            'Textiles & Garments': ['Cotton T-Shirt', 'Silk Saree', 'Denim Jeans', 'Wool Sweater', 'Linen Shirt'],
            'Agricultural Products': ['Basmati Rice', 'Black Pepper', 'Cardamom', 'Turmeric Powder', 'Darjeeling Tea'],
            'Pharmaceuticals': ['Paracetamol Tablets', 'Antibiotic Capsules', 'Diabetes Medicine', 'Blood Pressure Pills', 'Vitamin D3'],
            'Chemicals': ['Organic Dye', 'Industrial Acid', 'Fertilizer', 'Pesticide', 'Paint Pigment'],
            'Machinery': ['CNC Machine', 'Industrial Motor', 'Pump System', 'Conveyor Belt', 'Generator'],
            'Automotive Parts': ['Brake Pads', 'Engine Parts', 'Transmission System', 'Suspension Kit', 'Exhaust System'],
            'Jewelry & Gems': ['Gold Ring', 'Diamond Necklace', 'Silver Bracelet', 'Emerald Earrings', 'Pearl Set'],
            'IT Hardware': ['Laptop', 'Smartphone', 'Server', 'Router', 'Memory Chip'],
            'Leather Products': ['Leather Jacket', 'Handbag', 'Sports Shoes', 'Wallet', 'Belt'],
            'Handicrafts': ['Wooden Sculpture', 'Brass Statue', 'Ceramic Vase', 'Embroidered Cushion', 'Metal Art']
        }
        
        units = ['kg', 'pieces', 'liters', 'meters', 'sets']
        
        product_id = 1
        for category in self.product_categories:
            category_name = category['name']
            templates = product_templates.get(category_name, ['Generic Product'])
            
            for i in range(5):  # 5 products per category
                template = random.choice(templates)
                variant = random.choice(['Premium', 'Standard', 'Economy', 'Export', 'Bulk'])
                
                products.append({
                    'id': product_id,
                    'name': f"{variant} {template}",
                    'sku': f"PRD{product_id:04d}",
                    'category_id': self.product_categories.index(category) + 1,
                    'hs_code': f"{category['hs_code_prefix'].split('-')[0]}{random.randint(10, 99)}",
                    'unit_of_measure': random.choice(units),
                    'is_raw_material': random.choice([True, False]),
                    'is_finished_good': True,
                    'manufacturing_cost_per_unit': round(random.uniform(10, 500), 2),
                    'requires_license': random.choice([True, False]),
                    'restricted_countries': json.dumps(random.sample(['CN', 'US'], k=random.randint(0, 2)))
                })
                product_id += 1
        
        return pd.DataFrame(products)
    
    def generate_dealers_data(self, num_dealers: int = 30) -> pd.DataFrame:
        """Generate dealers data"""
        dealers = []
        
        business_types = ['manufacturer', 'wholesaler', 'retailer', 'distributor']
        indian_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Hyderabad']
        
        for i in range(num_dealers):
            # 70% Indian dealers, 30% international
            is_indian = random.random() < 0.7
            
            if is_indian:
                country_id = 1  # India
                city = random.choice(indian_cities)
                state = random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'West Bengal'])
            else:
                country = random.choice([c for c in self.countries if c['name'] != 'India'])
                country_id = self.countries.index(country) + 1
                city = random.choice(['New York', 'Shanghai', 'Berlin', 'Tokyo', 'London', 'Paris', 'Milan', 'São Paulo', 'Toronto'])
                state = 'International'
            
            dealers.append({
                'id': i + 1,
                'name': f"Dealer {i+1:02d} {'India' if is_indian else 'Intl'}",
                'email': f"dealer{i+1:02d}@{'indiansupplier' if is_indian else 'global'}.com",
                'phone': f"+91-{random.randint(7000000000, 9999999999)}" if is_indian else f"+{random.randint(1, 999)}-{random.randint(1000000, 9999999)}",
                'country_id': country_id,
                'state': state,
                'city': city,
                'address': f"{random.randint(1, 999)} Business Street, {city}",
                'business_type': random.choice(business_types),
                'registration_number': f"REG{random.randint(100000, 999999)}",
                'gst_number': f"GST{random.randint(10000000000, 99999999999)}" if is_indian else None,
                'overall_rating': round(random.uniform(3.0, 5.0), 2),
                'reliability_score': round(random.uniform(0.6, 1.0), 3),
                'quality_score': round(random.uniform(0.7, 1.0), 3),
                'delivery_performance': round(random.uniform(0.6, 0.95), 3),
                'is_active': True,
                'created_at': datetime.now() - timedelta(days=random.randint(30, 730))
            })
        
        return pd.DataFrame(dealers)
    
    def generate_dealer_products_data(self, dealers_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
        """Generate dealer-product relationships with pricing"""
        dealer_products = []
        
        for _, dealer in dealers_df.iterrows():
            # Each dealer supplies 3-8 products
            num_products = random.randint(3, 8)
            dealer_product_ids = random.sample(list(products_df['id']), num_products)
            
            for product_id in dealer_product_ids:
                product = products_df[products_df['id'] == product_id].iloc[0]
                base_cost = product['manufacturing_cost_per_unit']
                
                # Add margin and variability based on dealer location and type
                cost_multiplier = 1.2 if dealer['country_id'] == 1 else random.uniform(1.5, 2.5)
                
                dealer_products.append({
                    'id': len(dealer_products) + 1,
                    'dealer_id': dealer['id'],
                    'product_id': product_id,
                    'cost_per_unit': round(base_cost * cost_multiplier, 2),
                    'minimum_order_quantity': random.randint(10, 1000),
                    'maximum_supply_capacity': random.randint(1000, 50000),
                    'average_delivery_days': random.randint(5, 60),
                    'delivery_reliability': round(random.uniform(0.7, 1.0), 3),
                    'quality_rating': round(random.uniform(3.0, 5.0), 2),
                    'defect_rate': round(random.uniform(0.0, 0.1), 3),
                    'is_available': True,
                    'last_updated': datetime.now()
                })
        
        return pd.DataFrame(dealer_products)
    
    def generate_country_tariffs_data(self, countries_df: pd.DataFrame, categories_df: pd.DataFrame) -> pd.DataFrame:
        """Generate tariff data for country-category combinations"""
        tariffs = []
        
        for _, country in countries_df.iterrows():
            if country['name'] == 'India':
                continue  # Skip India for import duties
                
            for _, category in categories_df.iterrows():
                # Tariff rates vary by country and product category
                base_rate = country['base_import_duty']
                category_modifier = random.uniform(0.5, 2.0)
                
                tariffs.append({
                    'id': len(tariffs) + 1,
                    'country_id': country['id'],
                    'product_category_id': category['id'],
                    'import_duty_rate': round(base_rate * category_modifier, 2),
                    'export_duty_rate': round(random.uniform(0, 2), 2),
                    'additional_taxes': json.dumps({'vat': round(random.uniform(5, 20), 1)}),
                    'requires_certification': random.choice([True, False]),
                    'certification_cost': round(random.uniform(100, 2000), 2),
                    'processing_days': random.randint(1, 15),
                    'effective_from': datetime.now() - timedelta(days=365),
                    'effective_to': datetime.now() + timedelta(days=365)
                })
        
        return pd.DataFrame(tariffs)
    
    def generate_trade_routes_data(self, countries_df: pd.DataFrame) -> pd.DataFrame:
        """Generate trade routes data"""
        routes = []
        
        # India to all other countries
        for _, country in countries_df.iterrows():
            if country['name'] == 'India':
                continue
                
            for transport in self.transport_modes:
                base_distance_cost = random.uniform(0.5, 3.0)  # per kg
                
                routes.append({
                    'id': len(routes) + 1,
                    'origin_country_id': 1,  # India
                    'destination_country_id': country['id'],
                    'transport_mode': transport['mode'],
                    'base_cost_per_kg': round(base_distance_cost * transport['cost_multiplier'], 2),
                    'base_cost_per_cbm': round(base_distance_cost * transport['cost_multiplier'] * 200, 2),
                    'transit_days': int(random.uniform(3, 45) * transport['time_multiplier']),
                    'delay_probability': round(1 - transport['reliability'], 3),
                    'average_delay_days': random.randint(0, 7),
                    'origin_port': f"India Port {random.randint(1, 5)}",
                    'destination_port': f"{country['name']} Port {random.randint(1, 3)}",
                    'is_active': True
                })
        
        return pd.DataFrame(routes)
    
    def generate_historical_transactions(self, dealers_df: pd.DataFrame, products_df: pd.DataFrame, 
                                       countries_df: pd.DataFrame, num_transactions: int = 200) -> pd.DataFrame:
        """Generate historical trade transaction data for ML training"""
        transactions = []
        
        for i in range(num_transactions):
            # Random transaction
            dealer = dealers_df.sample(1).iloc[0]
            product = products_df.sample(1).iloc[0]
            dest_country = countries_df[countries_df['name'] != 'India'].sample(1).iloc[0]
            
            # Get dealer-product relationship
            dealer_product_cost = random.uniform(100, 1000)  # Simplified
            
            # Transaction details
            quantity = random.randint(100, 10000)
            unit_price = dealer_product_cost
            total_product_value = quantity * unit_price
            
            # Calculate costs
            logistics_cost = random.uniform(0.5, 5.0) * quantity  # per unit logistics
            tariff_rate = random.uniform(2, 15)  # percentage
            tariff_cost = total_product_value * (tariff_rate / 100)
            other_charges = random.uniform(500, 5000)
            total_cost = total_product_value + logistics_cost + tariff_cost + other_charges
            
            # Selling price and profit
            profit_margin = random.uniform(5, 25)  # percentage
            selling_price = total_cost * (1 + profit_margin / 100)
            profit_amount = selling_price - total_cost
            profit_margin_percentage = (profit_amount / total_cost) * 100
            
            # Delivery times
            expected_delivery_days = random.randint(7, 60)
            actual_delivery_days = expected_delivery_days + random.randint(-5, 15)
            
            order_date = datetime.now() - timedelta(days=random.randint(1, 365))
            
            transactions.append({
                'id': i + 1,
                'transaction_id': f"TXN{i+1:06d}",
                'dealer_id': dealer['id'],
                'product_id': product['id'],
                'destination_country_id': dest_country['id'],
                'quantity': quantity,
                'unit_price': round(unit_price, 2),
                'total_product_value': round(total_product_value, 2),
                'logistics_cost': round(logistics_cost, 2),
                'tariff_cost': round(tariff_cost, 2),
                'other_charges': round(other_charges, 2),
                'total_cost': round(total_cost, 2),
                'selling_price': round(selling_price, 2),
                'profit_amount': round(profit_amount, 2),
                'profit_margin_percentage': round(profit_margin_percentage, 2),
                'order_date': order_date,
                'expected_delivery_date': order_date + timedelta(days=expected_delivery_days),
                'actual_delivery_date': order_date + timedelta(days=actual_delivery_days),
                'status': random.choice(['delivered', 'shipped', 'pending']),
                'predicted_profit': round(profit_margin_percentage + random.uniform(-2, 2), 2),
                'predicted_delivery_days': expected_delivery_days + random.randint(-3, 3),
                'prediction_accuracy': round(random.uniform(0.7, 0.95), 3)
            })
        
        return pd.DataFrame(transactions)
    
    def generate_exchange_rates_data(self) -> pd.DataFrame:
        """Generate exchange rates data"""
        rates = []
        
        for currency, rate in self.exchange_rates.items():
            if currency == 'INR':
                continue
                
            # Generate historical rates for last 30 days
            for i in range(30):
                date = datetime.now() - timedelta(days=i)
                fluctuation = random.uniform(0.95, 1.05)  # ±5% daily fluctuation
                
                rates.append({
                    'id': len(rates) + 1,
                    'from_currency': 'INR',
                    'to_currency': currency,
                    'rate': round(rate * fluctuation, 4),
                    'date': date,
                    'source': 'RBI_API'
                })
        
        return pd.DataFrame(rates)
    
    def save_all_data(self, output_dir: str = '/home/poweranger/trade-optimization-system/data/processed'):
        """Generate and save all datasets"""
        os.makedirs(output_dir, exist_ok=True)
        
        print("🏭 Generating Trade Optimization System Data...")
        
        # Generate all datasets
        countries_df = self.generate_countries_data()
        categories_df = self.generate_product_categories_data()
        products_df = self.generate_products_data()
        dealers_df = self.generate_dealers_data()
        dealer_products_df = self.generate_dealer_products_data(dealers_df, products_df)
        tariffs_df = self.generate_country_tariffs_data(countries_df, categories_df)
        routes_df = self.generate_trade_routes_data(countries_df)
        transactions_df = self.generate_historical_transactions(dealers_df, products_df, countries_df)
        exchange_rates_df = self.generate_exchange_rates_data()
        
        # Save to CSV files
        datasets = {
            'countries': countries_df,
            'product_categories': categories_df,
            'products': products_df,
            'dealers': dealers_df,
            'dealer_products': dealer_products_df,
            'country_tariffs': tariffs_df,
            'trade_routes': routes_df,
            'trade_transactions': transactions_df,
            'exchange_rates': exchange_rates_df
        }
        
        for name, df in datasets.items():
            filepath = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(filepath, index=False)
            print(f"✅ Saved {len(df)} records to {name}.csv")
        
        # Generate summary statistics
        self.generate_summary_report(datasets, output_dir)
        
        print(f"\n🎉 Data generation complete! Files saved to {output_dir}")
        return datasets
    
    def generate_summary_report(self, datasets: Dict[str, pd.DataFrame], output_dir: str):
        """Generate a summary report of the generated data"""
        report = {
            'generation_date': datetime.now().isoformat(),
            'datasets': {
                name: {
                    'records': len(df),
                    'columns': list(df.columns),
                    'file_size_mb': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
                }
                for name, df in datasets.items()
            },
            'business_insights': {
                'total_dealers': len(datasets['dealers']),
                'indian_dealers': len(datasets['dealers'][datasets['dealers']['country_id'] == 1]),
                'international_dealers': len(datasets['dealers'][datasets['dealers']['country_id'] != 1]),
                'total_products': len(datasets['products']),
                'product_categories': len(datasets['product_categories']),
                'target_countries': len(datasets['countries']) - 1,  # Excluding India
                'historical_transactions': len(datasets['trade_transactions']),
                'avg_profit_margin': round(datasets['trade_transactions']['profit_margin_percentage'].mean(), 2),
                'avg_delivery_days': round(datasets['trade_transactions']['actual_delivery_date'].subtract(datasets['trade_transactions']['order_date']).dt.days.mean(), 1)
            }
        }
        
        # Save report
        report_path = os.path.join(output_dir, 'data_summary.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📊 Summary report saved to data_summary.json")

if __name__ == "__main__":
    generator = TradeDataGenerator()
    datasets = generator.save_all_data()
    
    print("\n📈 Sample Data Preview:")
    print("Countries:", len(datasets['countries']))
    print("Products:", len(datasets['products']))
    print("Dealers:", len(datasets['dealers']))
    print("Historical Transactions:", len(datasets['trade_transactions']))
    
    print("\n🔍 Quick Stats:")
    print(f"Average Profit Margin: {datasets['trade_transactions']['profit_margin_percentage'].mean():.2f}%")
    print(f"Average Delivery Time: {datasets['trade_transactions']['actual_delivery_date'].subtract(datasets['trade_transactions']['order_date']).dt.days.mean():.1f} days")
    print(f"Top Countries by Transaction Volume:")
    country_stats = datasets['trade_transactions']['destination_country_id'].value_counts().head()
    for country_id, count in country_stats.items():
        country_name = datasets['countries'][datasets['countries']['id'] == country_id]['name'].iloc[0]
        print(f"  {country_name}: {count} transactions")
