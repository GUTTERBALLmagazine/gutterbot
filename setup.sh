#!/bin/bash
# setup script for gutterbot conda environment

echo "🚀 Setting up gutterbot conda environment..."

# create conda environment
conda env create -f environment.yml

# activate environment
echo "✅ Environment created! To activate:"
echo "conda activate gutterbot"
echo ""
echo "📝 Don't forget to:"
echo "1. Copy env.example to .env"
echo "2. Add your LASTFM_API_KEY to .env"
echo "3. Add usernames to LASTFM_USERS in .env"
echo ""
echo "🎵 Then run: python main.py"
