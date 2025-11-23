#!/bin/bash

# WRXS Quick Start Script

echo "🏋️  WRXS - Workout & Fitness Tracker"
echo "====================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env

    # Generate a random secret key
    if command -v openssl &> /dev/null; then
        SECRET_KEY=$(openssl rand -hex 32)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/your-secret-key-here-generate-a-random-string/$SECRET_KEY/" .env
        else
            # Linux
            sed -i "s/your-secret-key-here-generate-a-random-string/$SECRET_KEY/" .env
        fi
        echo "✅ Generated secure SECRET_KEY"
    else
        echo "⚠️  Please set a secure SECRET_KEY in .env file"
    fi

    echo "📄 .env file created. You may want to customize it."
fi

# Build and start containers
echo ""
echo "🐳 Building and starting Docker containers..."
docker-compose up -d --build

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if backend is healthy
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running"
else
    echo "⚠️  Backend may still be starting up"
fi

# Seed the database
echo ""
echo "🌱 Seeding database with sample exercises..."
docker-compose exec -T backend python -m app.seed_data

echo ""
echo "✅ WRXS is ready!"
echo ""
echo "📱 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📚 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Create an account"
echo "   3. Update your fitness profile"
echo "   4. Start logging workouts!"
echo ""
echo "🛑 To stop: docker-compose down"
echo "🔄 To view logs: docker-compose logs -f"
