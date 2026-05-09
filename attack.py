import json
import random
import time
from datetime import datetime

LOG_FILE = "honeypot_logs.json"

# 🌍 Realistic attacker IPs
ips = [
    "8.8.8.8", "1.1.1.1", "45.33.32.156",
    "185.220.101.1", "103.21.244.0",
    "91.198.174.192", "172.217.160.78"
]

# 🎯 ALL SERVICES (UPDATED)
services = ["SSH", "HTTP", "FTP", "TELNET", "SMTP", "RDP"]

# ⚙️ Status types per service
status_map = {
    "SSH": ["failed", "login_attempt", "bruteforce"],
    "HTTP": ["request", "scan", "dir_scan"],
    "FTP": ["login_attempt", "upload_attempt"],
    "TELNET": ["login_attempt", "bruteforce"],
    "SMTP": ["spam_attempt", "relay_attempt"],
    "RDP": ["connection_attempt", "bruteforce"]
}

print("⚔️ Multi-service attack simulation started...")

while True:
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    ip = random.choice(ips)
    service = random.choice(services)
    status = random.choice(status_map[service])

    # 🎯 Smarter severity logic
    if service in ["SSH", "RDP"] and status in ["failed", "bruteforce"]:
        severity = "HIGH"
    elif service in ["SMTP", "TELNET"]:
        severity = random.choice(["MEDIUM", "HIGH"])
    elif service == "FTP":
        severity = random.choice(["MEDIUM", "HIGH"])
    else:
        severity = random.choice(["LOW", "MEDIUM"])

    log = {
        "ip": ip,
        "service": service,
        "status": status,
        "severity": severity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    logs.append(log)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    print(f"[{log['timestamp']}] {ip} → {service} → {status} → {severity}")

    # ⏱️ Random delay (more realistic traffic)
    time.sleep(random.uniform(1, 3))
