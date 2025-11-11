#!/bin/bash
# Netlify build script - frontend only
echo "Installing Node.js dependencies..."
npm install

echo "Building frontend..."
npm run build

echo "Frontend build complete!"
