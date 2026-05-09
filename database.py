#!/usr/bin/env python3
"""
NETHUNT DATABASE LAYER (NDJSON VERSION)
- Reads JSON Lines logs
- Processes attack data
- Stores into SQLite database
"""

import json
import sqlite3
from collections import Counter

LOG_FILE = "honeypot_logs.json"
DB_FILE = "honeypot.db"


# ---------------- LOAD LOGS (UPDATED) ----------------
def load_logs():
    logs = []

    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    continue  # skip broken lines safely

        return logs

    except Exception as e:
        print(f"[ERROR] Failed to load logs: {e}")
        return []


# ---------------- PROCESS LOGS ----------------
def process_logs(logs):
    ip_counter = Counter()
    service_counter = Counter()
    severity_counter = Counter()

    detailed_records = []

    for log in logs:
        ip = log.get("ip", "unknown")
        service = log.get("service", "unknown")
        severity = log.get("severity", "LOW")

        ip_counter[ip] += 1
        service_counter[service] += 1
        severity_counter[severity] += 1

        detailed_records.append((
            log.get("timestamp", ""),
            ip,
            service,
            severity,
            log.get("action", ""),
            log.get("payload", "")
        ))

    return ip_counter, service_counter, severity_counter, detailed_records


# ---------------- DATABASE SETUP ----------------
def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        timestamp TEXT,
        ip TEXT,
        service TEXT,
        severity TEXT,
        action TEXT,
        payload TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ip_stats (
        ip TEXT PRIMARY KEY,
        attempts INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS service_stats (
        service TEXT PRIMARY KEY,
        count INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS severity_stats (
        severity TEXT PRIMARY KEY,
        count INTEGER
    )
    """)

    conn.commit()
    return conn, cursor


# ---------------- INSERT DATA ----------------
def insert_data(cursor, records, ip_counter, service_counter, severity_counter):

    # Clear old data (optional but recommended)
    cursor.execute("DELETE FROM logs")
    cursor.execute("DELETE FROM ip_stats")
    cursor.execute("DELETE FROM service_stats")
    cursor.execute("DELETE FROM severity_stats")

    # Insert raw logs
    cursor.executemany("""
    INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)
    """, records)

    # Insert stats
    for ip, count in ip_counter.items():
        cursor.execute("INSERT INTO ip_stats VALUES (?, ?)", (ip, count))

    for service, count in service_counter.items():
        cursor.execute("INSERT INTO service_stats VALUES (?, ?)", (service, count))

    for sev, count in severity_counter.items():
        cursor.execute("INSERT INTO severity_stats VALUES (?, ?)", (sev, count))


# ---------------- PRINT SUMMARY ----------------
def print_summary(ip_counter, service_counter, severity_counter):
    print("\n" + "=" * 50)
    print("      NETHUNT DATABASE SUMMARY")
    print("=" * 50)

    print("\nTop Attacking IPs:")
    for ip, count in ip_counter.most_common():
        print(f"  {ip} → {count}")

    print("\nServices Targeted:")
    for service, count in service_counter.items():
        print(f"  {service} → {count}")

    print("\nSeverity Distribution:")
    for sev, count in severity_counter.items():
        print(f"  {sev} → {count}")


# ---------------- MAIN ----------------
def main():
    logs = load_logs()

    if not logs:
        print("[!] No logs found.")
        return

    ip_counter, service_counter, severity_counter, records = process_logs(logs)

    conn, cursor = setup_database()

    insert_data(cursor, records, ip_counter, service_counter, severity_counter)

    conn.commit()
    conn.close()

    print("[+] Data stored in honeypot.db")

    print_summary(ip_counter, service_counter, severity_counter)


if __name__ == "__main__":
    main()

