from flask import Flask, render_template, redirect
import json
import random
from collections import Counter
import requests

from ai_model import detect_anomalies

app = Flask(__name__)

LOG_FILE = "honeypot_logs.json"
BLOCK_FILE = "blocked_ips.json"


def load_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)[-100:]
    except:
        return []


def get_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
        return {
            "lat": res.get("lat", 0),
            "lon": res.get("lon", 0),
            "country": res.get("country", "Unknown")
        }
    except:
        return {"lat": 0, "lon": 0, "country": "Unknown"}


# -------- BLOCK IP -------- #
def block_ip(ip):
    try:
        with open(BLOCK_FILE, "r") as f:
            blocked = json.load(f)
    except:
        blocked = []

    if ip not in blocked:
        blocked.append(ip)

    with open(BLOCK_FILE, "w") as f:
        json.dump(blocked, f, indent=4)


# -------- ATTACK SIMULATION -------- #
def simulate_attack(rounds=10):
    ips = ["8.8.8.8", "1.1.1.1", "45.33.32.156", "104.244.42.1"]
    services = ["SSH", "HTTP", "FTP"]
    statuses = ["failed", "login_attempt", "request"]

    logs = load_logs()

    for _ in range(rounds):
        logs.append({
            "ip": random.choice(ips),
            "service": random.choice(services),
            "status": random.choice(statuses),
            "severity": random.choice(["LOW", "MEDIUM", "HIGH"])
        })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


# -------- DASHBOARD -------- #
@app.route("/")
def dashboard():
    logs = detect_anomalies()

    # Add Geo + Block logic
    for log in logs:
        loc = get_location(log.get("ip", ""))

        log["lat"] = loc["lat"]
        log["lon"] = loc["lon"]
        log["country"] = loc["country"]

        # 🚨 AUTO BLOCK
        if "🚨" in log.get("ai_flag", ""):
            block_ip(log["ip"])

    ip_counts = Counter(log["ip"] for log in logs)
    service_counts = Counter(log["service"] for log in logs)

    return render_template(
        "index.html",
        logs=logs,
        ip_counts=dict(ip_counts),
        service_counts=dict(service_counts)
    )


@app.route("/attack")
def attack():
    simulate_attack(10)
    return redirect("/")


@app.route("/heavy_attack")
def heavy_attack():
    simulate_attack(50)
    return redirect("/")


@app.route("/reset")
def reset():
    with open(LOG_FILE, "w") as f:
        json.dump([], f)
    return redirect("/")


if __name__ == "__main__":
    print("🔥 Starting Flask...")
    app.run(host="0.0.0.0", port=5000, debug=True)
