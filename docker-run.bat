@echo off
echo 🐳 Docker Commands for Pet Sitting Website
echo ==========================================
echo.
echo Available commands:
echo   build     - Build the Docker image
echo   up        - Start the services
echo   down      - Stop the services
echo   logs      - View logs
echo   init-db   - Initialize the database
echo   shell     - Access container shell
echo   clean     - Remove containers and volumes
echo.
echo Usage: docker-run.bat [command]
echo.

if "%1"=="build" (
    echo Building Docker image...
    docker-compose build
    goto end
)

if "%1"=="up" (
    echo Starting services...
    docker-compose up -d
    echo.
    echo 🌐 Access your site at: http://localhost:5000
    goto end
)

if "%1"=="down" (
    echo Stopping services...
    docker-compose down
    goto end
)

if "%1"=="logs" (
    echo Showing logs...
    docker-compose logs -f
    goto end
)

if "%1"=="init-db" (
    echo Initializing database...
    docker-compose exec web python docker-init-db.py
    goto end
)

if "%1"=="shell" (
    echo Accessing container shell...
    docker-compose exec web /bin/bash
    goto end
)

if "%1"=="clean" (
    echo Cleaning up containers and volumes...
    docker-compose down -v
    docker system prune -f
    goto end
)

echo Please specify a command:
echo   docker-run.bat build
echo   docker-run.bat up
echo   docker-run.bat init-db
echo etc.

:end
pause