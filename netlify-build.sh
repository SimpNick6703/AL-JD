#!/usr/bin/env bash

# Install Rust toolchain so pydantic-core can compile if no prebuilt wheel exists
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

echo "Installing Node.js dependencies..."
npm install

echo "Building frontend..."
npm run build

echo "Frontend build complete!"
