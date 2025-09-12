#!/bin/bash
# Docker Deployment Script for Pet Sitting Website

set -e

echo "🐱 Pet Sitting Website - Docker Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    print_warning "Please edit .env file with your actual configuration before proceeding."
    exit 1
fi

# Build and start the application
print_status "Building Docker images..."
if command -v docker-compose &> /dev/null; then
    docker-compose build
    print_status "Starting services with docker-compose..."
    docker-compose up -d
else
    docker compose build
    print_status "Starting services with docker compose..."
    docker compose up -d
fi

# Wait for services to be healthy
print_status "Waiting for services to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost/health &> /dev/null; then
    print_status "Application is running successfully!"
    echo ""
    echo "🌐 Access your application at: http://localhost"
    echo "🔍 Health check: http://localhost/health"
    echo ""
    echo "📊 View logs:"
    if command -v docker-compose &> /dev/null; then
        echo "   docker-compose logs -f"
    else
        echo "   docker compose logs -f"
    fi
    echo ""
    echo "🛑 Stop application:"
    if command -v docker-compose &> /dev/null; then
        echo "   docker-compose down"
    else
        echo "   docker compose down"
    fi
else
    print_error "Application failed to start. Check logs:"
    if command -v docker-compose &> /dev/null; then
        docker-compose logs
    else
        docker compose logs
    fi
    exit 1
fi
