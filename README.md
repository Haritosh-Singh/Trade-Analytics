# AI-Powered Import-Export Optimization System

## 🌍 Multi-Country Trade Analytics for India-Based Import-Export Business

### Project Overview
An end-to-end ML-powered platform that optimizes trade operations with the top 10 GDP countries. It analyzes dealer performance, logistics costs, tariffs, and historical transactions to recommend profitable, time-efficient trade strategies. The system provides a FastAPI backend with ML models, a React dashboard, and a CSV-based data lake backed by a lightweight database for local development.

### 🎯 Key Features
- Profit and delivery-time prediction using gradient-boosted trees (XGBoost)
- Dealer performance analytics and multi-criteria ranking
- Country opportunity analysis with risk-adjusted scoring
- Interactive React dashboard with CRM-style views and charts
- CSV ingestion, upload endpoints, and scripted data loading

### 🏗️ Architecture
```
├── backend/            # FastAPI backend, ML models, and API endpoints
│   ├── app/
│   │   ├── main.py                         # App entrypoint (Uvicorn driven)
│   │   ├── api/endpoints/                  # REST endpoints
│   │   │   ├── predictions.py              # ML predictions & analytics
│   │   │   └── data.py                     # Data/CRM endpoints
│   │   └── core/database.py                # SQLAlchemy (SQLite by default)
│   └── ml/models/profit_predictor.py       # XGBoost profit & delivery models
├── frontend/           # React dashboard (Create React App)
├── data/               # Processed CSV datasets used by API
├── monitoring/         # Prometheus client metrics utilities
└── scripts/            # Data loading and deploy helpers
```

### 🔧 Technology Stack (as implemented)
- Backend: FastAPI, SQLAlchemy, Uvicorn
- Database: SQLite (development default via `DATABASE_URL`), PostgreSQL optional via env
- ML/AI: XGBoost Regressor (profit & delivery), scikit-learn, Pandas, joblib
- Frontend: React, Chart.js/Plotly (components), Fetch/XHR to FastAPI
- Monitoring: Prometheus Python client (custom counters, histograms, gauges)

> Note: The backend currently defaults to SQLite (`sqlite:///./trade_optimization.db`). Provide a `DATABASE_URL` to switch engines (e.g., PostgreSQL) without code changes.

---

## 🚀 Quick Start

### 1) Backend API
```bash
cd backend
pip install -r ../requirements.txt
python app/main.py          # Starts FastAPI at http://localhost:8000 (auto-reload)
```

Docs: http://localhost:8000/docs  |  Health: http://localhost:8000/health

Environment variables:
- `DATABASE_URL` (optional): override DB connection (default: `sqlite:///./trade_optimization.db`)

### 2) Frontend (React)
```bash
cd frontend/frontend
npm install
npm start                    # Starts CRA dev server on http://localhost:3000
```

### 3) Load Sample Data
```bash
python scripts/load_initial_data.py
```

Data files are read by the API from `data/processed/*.csv`.

---

## � API Overview

Base URL: `http://localhost:8000`

### Predictions & Analytics (prefix: `/api/predictions`)
- `POST /predict-trade` — Predict profit margin and delivery days for a scenario
	- Request body:
		- `dealer_id` (int), `product_id` (int), `destination_country_id` (int),
			`quantity` (int), `transport_mode` ("sea" | "air" | "road" | "rail")
	- Response: `{ predicted_profit_margin, predicted_delivery_days, confidence_score, recommendation, total_cost_estimate, risk_factors }`
- `POST /rank-dealers` — Rank dealers using multi-criteria scoring
	- Request body: `{ product_category_id?, destination_country_id?, max_results=10 }`
- `GET /country-analysis` — Opportunity scoring by country (profitability + delivery)
- `GET /model-performance` — Current model types, features, and metrics

### Data & CRM (prefix: `/api/data`)
- `GET /countries` — Countries list
- `GET /products?category_id=` — Products, optional filter
- `GET /dealers?country_id=` — Dealers with calculated performance metrics
- `GET /product-categories` — Product categories
- `GET /transactions?limit=` — Recent transactions
- `GET /dashboard-summary` — Aggregated metrics for the dashboard
- `GET /tariffs` — Import/export tariffs and taxes by country
- `GET /analytics` — Data for charts (profit by country, cost by product, trends)
- `POST /upload-csv` — Upload a CSV and get basic validation summary
- `POST /manual-entry` — Accept manual data entries (echo service)

Explore all endpoints interactively at `/docs`.

---

## � ML Models (implemented)
1. Profit Predictor — XGBoost Regressor trained on engineered features
2. Delivery Time Estimator — XGBoost Regressor on logistics and risk features
3. Dealer Ranking System — Weighted scoring (cost, quality, delivery, reliability, capacity)

Model training lifecycle (see `backend/ml/models/profit_predictor.py`):
- Feature engineering: categorical encodings, tariff burden, cost/logistics ratios, risk scores, seasonal features
- Scaling: StandardScaler on selected numeric features
- Models: `xgboost.XGBRegressor` for profit and delivery
- Persistence: `joblib` save/load with scaler, encoders, and feature list
- Feature importance: surfaced via `/api/predictions/model-performance`

> When the server receives the first prediction request and no model is loaded, it trains on `data/processed/trade_transactions.csv` and caches the model in memory.

---

## �️ Data & Storage
- Processed CSVs: `data/processed/` (countries, dealers, products, transactions, routes, tariffs, etc.)
- Database: SQLAlchemy engine configured via `app/core/database.py`
	- Default: SQLite file `trade_optimization.db` in repo root
	- Override with `DATABASE_URL` (e.g., `postgresql+psycopg2://user:pass@host:5432/db`)

---

## 🖥️ Monitoring
- Prometheus metrics utilities in `monitoring/metrics_collector.py`
- Metrics include API request counts/latency, model prediction counters, active users, CPU and memory gauges
- Start a metrics HTTP server from your own runner:
	- Example: `MetricsCollector().start_metrics_server(port=8001)` (choose a port different from the API)

---

## ✅ Testing
- ML tests: `tests/test_ml_models/test_profit_predictor.py`
- Run tests with `pytest` from repo root:
```bash
pytest -q
```

---

## 📈 Dashboard Features
- Real-time analytics fed by `/api/data/*` endpoints
- Dealer comparison, country profitability views, ROI scenarios, alerts (UI components in `frontend/frontend/src/components`)

---

## � Security & Compliance
Foundational endpoints are public in development. For production, add:
- JWT auth middleware for protected routes
- TLS termination at reverse proxy
- Audit logging and data retention policies
- GST/IGST compliance tracking integrations

---

## 🧩 Environment & Configuration
- `DATABASE_URL` — SQLAlchemy database URL (optional; defaults to SQLite)
- Frontend CORS is allowed for `http://localhost:3000` by default in `main.py`

---

## 🚧 Roadmap / Next Steps
- Add Dockerfiles for backend and a docker-compose for full local stack
- Persist trained models to `data/models/*.joblib` and load on startup if present
- Add authentication/authorization and per-user dashboards
- Expand CI (lint, type-check, tests) and add synthetic data generator

---

**Author**: Trade Optimization Team

**Version**: 1.0.0

**License**: MIT