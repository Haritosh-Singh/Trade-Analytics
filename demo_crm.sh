#!/bin/bash

# Demo script for Trade Optimization System Sales CRM
# This script demonstrates the key features and API endpoints

echo "🌍 Welcome to Trade Optimization System - Sales CRM Demo"
echo "========================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_BASE="http://localhost:8000/api"

echo -e "${BLUE}📊 SALES CRM FEATURES DEMO${NC}"
echo "============================"
echo ""

echo -e "${YELLOW}1. Dealer Database Management${NC}"
echo "   • Complete dealer information with performance metrics"
echo "   • Filtering by country, product, and performance"
echo "   • Contact management and transaction history"
echo ""

echo -e "${YELLOW}2. Country Tariff & Tax Dashboard${NC}"
echo "   • Real-time tariff and tax rates"
echo "   • Country-wise duty information"
echo "   • Historical tariff trends"
echo ""

echo -e "${YELLOW}3. Interactive Analytics & Charts${NC}"
echo "   • Profit vs Time by Country (Line Chart)"
echo "   • Cost Breakdown per Product (Bar Chart)"
echo "   • Dealer Performance Comparison"
echo "   • Advanced cost analysis"
echo ""

echo -e "${YELLOW}4. AI-Powered Trade Recommendations${NC}"
echo "   • Increase sales strategies"
echo "   • Cost reduction opportunities"
echo "   • Market opportunity identification"
echo "   • Risk assessment and mitigation"
echo ""

echo -e "${YELLOW}5. Data Upload & Management${NC}"
echo "   • Manual data entry interface"
echo "   • CSV file upload functionality"
echo "   • Real-time data synchronization"
echo ""

echo -e "${BLUE}🔗 API ENDPOINTS OVERVIEW${NC}"
echo "=========================="
echo ""
echo "Dealer Management:"
echo "  GET  /api/data/dealers           - Get all dealers"
echo "  GET  /api/data/dealers?country=1 - Filter by country"
echo ""
echo "Analytics & Data:"
echo "  GET  /api/data/countries         - Country information"
echo "  GET  /api/data/tariffs          - Tariff rates"
echo "  GET  /api/data/analytics        - Profit & cost data"
echo "  GET  /api/data/dashboard-summary - Complete metrics"
echo ""
echo "Data Management:"
echo "  POST /api/data/upload-csv       - Upload CSV files"
echo "  POST /api/data/manual-entry     - Manual data entry"
echo ""

echo -e "${BLUE}🌐 ACCESS URLS${NC}"
echo "=============="
echo ""
echo -e "${GREEN}Sales CRM:${NC}      http://localhost:3000/crm"
echo -e "${GREEN}AI Dashboard:${NC}   http://localhost:3000/dashboard"
echo -e "${GREEN}API Docs:${NC}       http://localhost:8000/docs"
echo -e "${GREEN}Backend API:${NC}    http://localhost:8000/api"
echo ""

echo -e "${BLUE}🎯 KEY BENEFITS${NC}"
echo "==============="
echo ""
echo "✅ Comprehensive dealer management"
echo "✅ Real-time tariff and tax tracking"
echo "✅ Interactive data visualizations"
echo "✅ AI-powered trade recommendations"
echo "✅ Easy data import and management"
echo "✅ Responsive design for all devices"
echo "✅ RESTful API for third-party integration"
echo ""

echo -e "${YELLOW}🚀 Quick Start:${NC}"
echo "1. Start Backend:  uvicorn backend.app.main:app --reload"
echo "2. Start Frontend: npm start (in frontend/frontend/)"
echo "3. Open Browser:   http://localhost:3000/crm"
echo ""

echo -e "${GREEN}✨ Demo complete! Ready to optimize your trade operations!${NC}"
