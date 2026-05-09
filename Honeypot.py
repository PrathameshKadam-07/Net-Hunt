import socket
import threading
import json
from datetime import datetime

LOG_FILE = "honeypot_logs.json"

# ---------------- COMMON LOG FUNCTION ----------------
def log_event(ip, service, status, severity):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append({
        "ip": ip,
        "service": service,
        "status": status,
        "severity": severity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


# ---------------- SSH HONEYPOT ----------------
def ssh_honeypot():
    HOST, PORT = "0.0.0.0", 2222
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"🛡️ SSH Honeypot running on {PORT}")

    while True:
        client, addr = server.accept()
        ip = addr[0]

        print(f"[SSH] Connection from {ip}")
        log_event(ip, "SSH", "login_attempt", "HIGH")

        client.send(b"SSH-2.0-OpenSSH_7.4\r\n")
        client.close()


# ---------------- HTTP HONEYPOT ----------------
def http_honeypot():
    HOST, PORT = "0.0.0.0", 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"🌐 HTTP Honeypot running on {PORT}")

    while True:
        client, addr = server.accept()
        ip = addr[0]

        print(f"[HTTP] Request from {ip}")
        log_event(ip, "HTTP", "request", "LOW")

        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nWelcome"
        client.send(response)
        client.close()


# ---------------- FTP HONEYPOT ----------------
def ftp_honeypot():
    HOST, PORT = "0.0.0.0", 2121
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"📁 FTP Honeypot running on {PORT}")

    while True:
        client, addr = server.accept()
        ip = addr[0]

        print(f"[FTP] Connection from {ip}")
        log_event(ip, "FTP", "login_attempt", "MEDIUM")

        client.send(b"220 FTP Server Ready\r\n")
        client.close()


# ---------------- TELNET HONEYPOT ----------------
def telnet_honeypot():
    HOST, PORT = "0.0.0.0", 2323
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"📡 TELNET Honeypot running on {PORT}")

    while True:
        client, addr = server.accept()
        ip = addr[0]

        print(f"[TELNET] Connection from {ip}")
        log_event(ip, "TELNET", "login_attempt", "MEDIUM")

        client.send(b"login: ")
        client.close()


# ---------------- SMTP HONEYPOT ----------------
def smtp_honeypot():
    HOST, PORT = "0.0.0.0", 2525
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"📧 SMTP Honeypot running on {PORT}")

    while True:
        client, addr = server.accept()
        ip = addr[0]

        print(f"[SMTP] Connection from {ip}")
        log_event(ip, "SMTP", "spam_attempt", "HIGH")

        client.send(b"220 Fake SMTP Server\r\n")
        client.close()


# ---------------- RDP HONEYPOT ----------------
def rdp_honeypot():
    HOST, PORT = "0.0.0.0", 3389
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"🖥️ RDP Honeypot running on {PORT}")

    while True:
        client, addr = server.accept()
        ip = addr[0]

        print(f"[RDP] Connection from {ip}")
        log_event(ip, "RDP", "connection_attempt", "HIGH")

        client.close()


# ---------------- START ALL SERVICES ----------------
if __name__ == "__main__":
    print("🚀 Starting Multi-Service Honeypot...\n")

    threading.Thread(target=ssh_honeypot).start()
    threading.Thread(target=http_honeypot).start()
    threading.Thread(target=ftp_honeypot).start()
    threading.Thread(target=telnet_honeypot).start()
    threading.Thread(target=smtp_honeypot).start()
    threading.Thread(target=rdp_honeypot).start()

    while True:
        pass
