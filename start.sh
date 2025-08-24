#!/bin/bash
echo "🚀 DXowy Bot starting on Railway..."
echo "📅 Date: $(date)"
echo "🔧 Python version: $(python --version)"
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "▶️ Starting bot..."
python dxowy_bot.py
