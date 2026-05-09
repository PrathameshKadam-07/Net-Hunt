#!/bin/bash

echo "🚀 Starting NetHunt Full System..."

# Activate venv if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ensure required files exist
[ -f honeypot_logs.json ] || echo "[]" > honeypot_logs.json
[ -f blocked_ips.json ] || echo "[]" > blocked_ips.json

# Kill old processes (optional safety)
echo "🧹 Cleaning old processes..."
pkill -f honeypot.py
pkill -f app.py

# 1. Start Honeypot (background)
echo "🛡️ Starting Honeypot..."
python3 Honeypot.py &
sleep 2

# 2. Run attack simulation
echo "⚔️ Launching attack simulation..."
python3 attack.py &
sleep 2

# 3. Start Dashboard
echo "📊 Starting Dashboard..."
python3 app.py &

# 4. Open browser (optional)
sleep 2
xdg-open http://localhost:5000

echo "✅ SYSTEM RUNNING"
