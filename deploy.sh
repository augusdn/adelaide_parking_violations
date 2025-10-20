#!/bin/bash

# Adelaide Parking Violations Map - Deployment Script
# This script builds and prepares the application for deployment

echo "🚀 Starting deployment build process..."

# Check if we're in the right directory
if [ ! -f "vite.config.ts" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Process data if CSV exists
if [ -f "data/Parking_Expiations.csv" ]; then
    echo "📊 Processing parking violations data..."
    if [ -d ".venv" ]; then
        echo "Using virtual environment..."
        source .venv/bin/activate
        python scripts/process_data.py
    else
        echo "⚠️  Virtual environment not found. Make sure Python dependencies are installed."
        python3 scripts/process_data.py
    fi
else
    echo "ℹ️  Using existing sample data (data/Parking_Expiations.csv not found)"
fi

# Build the application
echo "🔨 Building application for production..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo ""
    echo "🧪 Testing the production build..."
    npm run preview &
    PREVIEW_PID=$!
    sleep 2
    
    # Test if data files are accessible
    if curl -s -f http://localhost:4173/adelaide_parking_violations/data/streets.json > /dev/null; then
        echo "✅ Data files are accessible in preview"
    else
        echo "⚠️  Warning: Data files may not be accessible in preview"
    fi
    
    # Stop preview server
    kill $PREVIEW_PID 2>/dev/null
    
    echo ""
    echo "📁 Built files are in the 'dist' directory"
    echo "🌐 Deploy the 'dist' folder to your hosting service"
    echo ""
    echo "For GitHub Pages:"
    echo "  1. git add ."
    echo "  2. git commit -m 'Deploy parking violations map'"
    echo "  3. git push origin main"
    echo "  4. Enable GitHub Pages in repository settings"
    echo ""
    echo "🎉 Your Adelaide Parking Violations Map is ready for deployment!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi