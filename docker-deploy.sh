#!/bin/bash
# Docker Deployment Helper Script

set -e

echo "🐳 Pet Sitting Website - Docker Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    print_status "Docker and Docker Compose are installed."
}

# Build and start the application
deploy() {
    print_status "Building Docker images..."
    docker-compose build

    print_status "Starting services..."
    docker-compose up -d

    print_status "Waiting for services to be healthy..."
    sleep 10

    print_status "Checking application health..."
    if curl -f http://localhost/health &> /dev/null; then
        print_status "✅ Application is running successfully!"
        print_status "🌐 Access your application at: http://localhost"
        print_status "📊 Health check: http://localhost/health"
    else
        print_error "❌ Application health check failed. Check logs with: docker-compose logs"
        exit 1
    fi
}

# Stop the application
stop() {
    print_status "Stopping services..."
    docker-compose down
    print_status "✅ Services stopped."
}

# View logs
logs() {
    print_status "Showing application logs..."
    docker-compose logs -f web
}

# Initialize database
init_db() {
    print_status "Initializing database..."
    docker-compose exec web python deploy.py init-db
    print_status "✅ Database initialized."
}

# Show status
status() {
    print_status "Service Status:"
    docker-compose ps

    print_status "Health Check:"
    if curl -f http://localhost/health &> /dev/null; then
        echo -e "${GREEN}✅ Application is healthy${NC}"
    else
        echo -e "${RED}❌ Application is not responding${NC}"
    fi
}

# Main menu
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy    Build and start the application"
    echo "  stop      Stop the application"
    echo "  restart   Restart the application"
    echo "  logs      Show application logs"
    echo "  status    Show service status"
    echo "  init-db   Initialize the database"
    echo "  cleanup   Remove containers and images"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Deploy the application"
    echo "  $0 logs      # View logs"
    echo "  $0 stop      # Stop everything"
}

# Cleanup function
cleanup() {
    print_warning "This will remove all containers and images. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Cleaning up..."
        docker-compose down -v --rmi all
        print_status "✅ Cleanup completed."
    else
        print_status "Cleanup cancelled."
    fi
}

# Restart function
restart() {
    print_status "Restarting services..."
    docker-compose restart
    print_status "✅ Services restarted."
}

# Main logic
case "${1:-help}" in
    deploy)
        check_docker
        deploy
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    init-db)
        init_db
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac