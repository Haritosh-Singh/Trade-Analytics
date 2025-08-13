#!/bin/bash

# Test script for Trade Optimization System API endpoints

API_BASE="http://localhost:8000/api"

echo "🧪 Testing Trade Optimization System API Endpoints"
echo "=================================================="

echo ""
echo "📊 Testing /data/dealers endpoint..."
curl -s "$API_BASE/data/dealers" | jq '.[0:2]' || echo "❌ Failed to get dealers data"

echo ""
echo "🏛️ Testing /data/countries endpoint..."
curl -s "$API_BASE/data/countries" | jq '.[0:3]' || echo "❌ Failed to get countries data"

echo ""
echo "💰 Testing /data/tariffs endpoint..."
curl -s "$API_BASE/data/tariffs" | jq '.[0:3]' || echo "❌ Failed to get tariffs data"

echo ""
echo "📈 Testing /data/analytics endpoint..."
curl -s "$API_BASE/data/analytics" | jq '.profit_data[0:2]' || echo "❌ Failed to get analytics data"

echo ""
echo "📋 Testing /data/dashboard-summary endpoint..."
curl -s "$API_BASE/data/dashboard-summary" | jq '.summary' || echo "❌ Failed to get dashboard summary"

echo ""
echo "✅ API Testing Complete!"
