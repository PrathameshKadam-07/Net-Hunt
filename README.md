# 🛡️ Net Hunt – Honeypot-Based Network Intrusion Detection System

## 📌 Overview

Net Hunt is a web-based honeypot-driven Network Intrusion Detection System designed to detect, analyze, and visualize cyber attacks in real time. The system simulates vulnerable network services to attract attackers, logs their activities, and applies machine learning techniques to identify anomalous behavior.

Unlike traditional IDS systems, Net Hunt generates **near-zero false positives**, as any interaction with the honeypot is treated as malicious.

---

## 🎯 Key Features

* 🔐 Multi-service honeypot (SSH, HTTP, FTP, Telnet)
* 📊 Real-time attack logging in structured JSON format
* 🤖 Machine Learning-based anomaly detection (Isolation Forest)
* 🌐 Web-based dashboard for visualization
* 📍 GeoIP and attack pattern analysis
* 🚨 Detection of brute-force, scanning, and exploitation attempts

---

## 🧠 Machine Learning Integration

Net Hunt uses the **Isolation Forest algorithm** to detect anomalies in attacker behavior.

### ✔ Why Isolation Forest?

* Works on unlabeled data (unsupervised learning)
* Detects unknown / zero-day attacks
* Efficient and fast for real-time systems

### ✔ How it Works

* Logs are converted into numerical features
* Model builds random trees
* Anomalies are isolated faster (short path length)
* High anomaly score = suspicious activity

---

## 🏗️ System Architecture

```text
Attacker → Honeypot (SSH/HTTP/FTP/Telnet)
        → Log Collection (JSON)
        → Data Processing (Feature Extraction)
        → Isolation Forest (ML Model)
        → Dashboard (Flask Web App)
```

---

## ⚙️ Tech Stack

### 👨‍💻 Backend

* Python
* Socket Programming
* JSON Logging

### 🤖 Machine Learning

* Scikit-learn (Isolation Forest)
* Pandas, NumPy

### 🌐 Frontend

* Flask
* HTML, CSS, JavaScript

### 🛠️ Tools

* Nmap (Scanning)
* Hydra (Brute-force attacks)
* Kali Linux (Attack simulation)

---

## 📂 Project Structure

```text
net-hunt-honeypot-ids/
│
├── honeypot/
│   └── multi_service_honeypot.py
│
├── attacker/
│   └── attack.py
│
├── ml/
│   └── isolation_forest.py
│
├── dashboard/
│   └── app.py
│
├── logs/
├── README.md
├── requirements.txt
```

---

## 🚀 Installation & Setup

### 🔹 1. Clone Repository

```bash
git clone https://github.com/Pranav-prc/net-hunt-honeypot-ids.git
cd net-hunt-honeypot-ids
```

### 🔹 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔹 3. Run Honeypot

```bash
python honeypot/multi_service_honeypot.py
```

### 🔹 4. Run Dashboard

```bash
python dashboard/app.py
```

---

## 🧪 Testing the System

### 🔹 Run Attack Simulation

```bash
python attacker/attack.py
```

### 🔹 Or Use Tools

```bash
nmap -sS -p 22,23,80,21 <target-ip>
hydra -l admin -P passwords.txt ssh://<target-ip>
```

---

## 📊 Sample Log Format

```json
{
  "timestamp": "2026-04-25T10:23:45Z",
  "ip": "192.168.1.10",
  "service": "SSH",
  "event": "login_attempt",
  "status": "failed"
}
```

---

## 📈 Results

* ✔ Successfully captured attacker interactions
* ✔ Detected anomalies using ML
* ✔ Real-time visualization of attacks
* ✔ Near-zero false positives due to honeypot approach

---

## 🔄 Development Methodology

The project follows an **Agile Model**, with development divided into multiple sprints:

* Sprint 1: Setup & Planning
* Sprint 2: Honeypot Development
* Sprint 3: Dashboard & Data Processing
* Sprint 4: ML Integration & Testing

---

## 📚 Applications

* Cybersecurity monitoring
* Research and education
* Threat intelligence gathering
* SOC (Security Operations Center) support

---

## 🔮 Future Enhancements

* Malware sandbox integration
* Multi-region honeypot deployment
* Automated alert system (Email/SMS)
* Advanced ML models for classification
* Integration with threat intelligence platforms

---

## 👨‍💻 Team Members

* Pranav Chaudhari
* Prathmesh Kadam
* Soham Chaukaskar

---

## 📄 Research Contribution

This project has been successfully published as a research paper, validating its design, implementation, and contribution to cybersecurity.

---

## 📜 License

This project is for academic and research purposes.

---

## ⭐ Acknowledgment

We thank our mentors and institution for supporting this project.

---
