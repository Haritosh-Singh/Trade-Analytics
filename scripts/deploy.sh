#!/bin/bash

# AI-Powered Import-Export Optimization System - Deployment Script
# This script deploys the complete trade optimization system

set -e

echo "🌍 Deploying AI-Powered Import-Export Optimization System..."

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[DEPLOY]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Set up environment
print_header "Setting up environment..."

# Create necessary directories
mkdir -p data/processed data/models logs

# Generate sample data if it doesn't exist
if [ ! -f "data/processed/countries.csv" ]; then
    print_status "Generating sample trade data..."
    cd backend
    source venv/bin/activate 2>/dev/null || true
    python ../scripts/load_initial_data.py
    cd ..
fi

# Build and start services using Docker Compose
print_header "Building and starting services..."

# Use docker compose or docker-compose based on availability
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Stop any existing containers
print_status "Stopping existing containers..."
$DOCKER_COMPOSE down --remove-orphans

# Build and start services
print_status "Building and starting services..."
$DOCKER_COMPOSE up --build -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 10

# Check if backend is healthy
print_status "Checking backend health..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health &> /dev/null; then
        print_status "Backend is healthy ✅"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Backend failed to start properly"
        $DOCKER_COMPOSE logs backend
        exit 1
    fi
    sleep 2
done

# Check if frontend is accessible
print_status "Checking frontend accessibility..."
for i in {1..30}; do
    if curl -f http://localhost:3000 &> /dev/null; then
        print_status "Frontend is accessible ✅"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Frontend failed to start properly"
        $DOCKER_COMPOSE logs frontend
        exit 1
    fi
    sleep 2
done

# Display service status
print_header "Service Status:"
$DOCKER_COMPOSE ps

# Display access information
print_header "🎉 Deployment Complete!"
echo ""
echo "📊 Trade Optimization Dashboard: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "🏭 Sample Data Loaded:"
echo "   • 10 Countries (Top GDP)"
echo "   • 50 Products across 10 categories"
echo "   • 30 Dealers (India + International)"
echo "   • 200+ Historical transactions"
echo ""
echo "🤖 AI Features Available:"
echo "   • Profit Prediction ML Models"
echo "   • Dealer Performance Ranking"
echo "   • Country Trade Analysis"
echo "   • Risk Assessment"
echo ""
echo "📱 Usage:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Navigate through Overview, Predictions, Analytics tabs"
echo "   3. Test AI predictions with sample dealer/product IDs (1-30, 1-50)"
echo "   4. Explore country analysis and dealer rankings"
echo ""

# Optional: Show logs
read -p "📖 Do you want to view live logs? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Showing live logs (Press Ctrl+C to exit)..."
    $DOCKER_COMPOSE logs -f
fi

echo "🚀 Trade Optimization System is ready for use!"
#!/bin/bash

# AWS EC2 Deployment Script
echo "Starting deployment to AWS EC2..."

# Step 1: Build and push Docker images
docker build -t trade-backend ./backend
docker build -t trade-frontend ./frontend

# Step 2: Deploy to EC2 instance
ssh -i "your-key.pem" ec2-user@your-ec2-ip << 'EOF'
  # Update system
  sudo yum update -y
  
  # Install Docker
  sudo yum install -y docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user
  
  # Install Docker Compose
  sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  
  # Clone repository and start services
  git clone https://github.com/your-username/trade-optimization-system.git
  cd trade-optimization-system
  docker-compose up -d
EOF

echo "Deployment completed!"
