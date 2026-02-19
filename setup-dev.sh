#!/bin/bash
# Development environment setup

echo "🚀 Setting up Fingerprint Enhancer Development Environment..."

# Backend setup
echo "📦 Setting up backend..."
cd backend
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
fi

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd fingerprint-web/client
npm install
cd ../../

# Final message
echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "To start developing:"
echo "  1. Backend: cd backend && python run.py"
echo "  2. Frontend: cd fingerprint-web/client && npm start"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up"
