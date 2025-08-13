# backend/app/models/database_models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Country(Base):
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(3), nullable=False, unique=True)
    gdp_usd_billion = Column(Float)
    currency = Column(String(3))
    exchange_rate_to_inr = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dealers = relationship("Dealer", back_populates="country")
    trade_routes = relationship("TradeRoute", back_populates="destination_country")
    country_tariffs = relationship("CountryTariff", back_populates="country")

class ProductCategory(Base):
    __tablename__ = "product_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Relationships
    products = relationship("Product", back_populates="category")
    country_tariffs = relationship("CountryTariff", back_populates="product_category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("product_categories.id"))
    description = Column(Text)
    base_price_usd = Column(Float)
    weight_kg = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("ProductCategory", back_populates="products")
    dealer_products = relationship("DealerProduct", back_populates="product")

class Dealer(Base):
    __tablename__ = "dealers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    business_type = Column(String(100))
    country_id = Column(Integer, ForeignKey("countries.id"))
    city = Column(String(100))
    contact_email = Column(String(200))
    contact_phone = Column(String(50))
    quality_score = Column(Float, default=0.0)
    reliability_score = Column(Float, default=0.0)
    delivery_performance = Column(Float, default=0.0)
    overall_rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    country = relationship("Country", back_populates="dealers")
    dealer_products = relationship("DealerProduct", back_populates="dealer")
    trade_transactions = relationship("TradeTransaction", back_populates="dealer")

class DealerProduct(Base):
    __tablename__ = "dealer_products"
    
    id = Column(Integer, primary_key=True, index=True)
    dealer_id = Column(Integer, ForeignKey("dealers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    cost_per_unit = Column(Float, nullable=False)
    minimum_order_quantity = Column(Integer, default=1)
    maximum_supply_capacity = Column(Integer)
    average_delivery_days = Column(Integer)
    quality_rating = Column(Float, default=0.0)
    defect_rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dealer = relationship("Dealer", back_populates="dealer_products")
    product = relationship("Product", back_populates="dealer_products")

class CountryTariff(Base):
    __tablename__ = "country_tariffs"
    
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    product_category_id = Column(Integer, ForeignKey("product_categories.id"))
    import_duty_rate = Column(Float, default=0.0)
    export_duty_rate = Column(Float, default=0.0)
    gst_rate = Column(Float, default=18.0)  # India's GST
    additional_cess = Column(Float, default=0.0)
    effective_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    country = relationship("Country", back_populates="country_tariffs")
    product_category = relationship("ProductCategory", back_populates="country_tariffs")

class TradeRoute(Base):
    __tablename__ = "trade_routes"
    
    id = Column(Integer, primary_key=True, index=True)
    destination_country_id = Column(Integer, ForeignKey("countries.id"))
    transport_mode = Column(String(50))  # sea, air, land
    base_cost_per_kg = Column(Float)
    transit_days = Column(Integer)
    delay_probability = Column(Float, default=0.1)
    carbon_footprint_kg_co2 = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    destination_country = relationship("Country", back_populates="trade_routes")

class TradeTransaction(Base):
    __tablename__ = "trade_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    dealer_id = Column(Integer, ForeignKey("dealers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    destination_country_id = Column(Integer, ForeignKey("countries.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_product_value = Column(Float, nullable=False)
    logistics_cost = Column(Float)
    tariff_cost = Column(Float)
    total_cost = Column(Float, nullable=False)
    profit_margin_percentage = Column(Float)
    order_date = Column(DateTime, nullable=False)
    expected_delivery_date = Column(DateTime)
    actual_delivery_date = Column(DateTime)
    status = Column(String(50), default="completed")  # pending, shipped, delivered, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    dealer = relationship("Dealer", back_populates="trade_transactions")

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    from_currency = Column(String(3), nullable=False)
    to_currency = Column(String(3), nullable=False)
    rate = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
