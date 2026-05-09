#!/bin/bash

echo "🛑 Stopping Net Hunt System..."

# Kill honeypot, attack, dashboard
sudo pkill -f Honeypot.py
sudo pkill -f attack.py
sudo pkill -f app.py

# Kill ngrok (if running)
sudo pkill -f ngrok

# Free common ports (extra safety)
for port in 5000 2222 8080 2121 2323 2525 3389
do
    pid=$(sudo lsof -t -i:$port)
    if [ ! -z "$pid" ]; then
        echo "Killing process on port $port (PID $pid)"
        sudo kill -9 $pid
    fi
done

echo "✅ All processes stopped."
