# 🛡️ AegisGate — AI API Firewall

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg?logo=docker)](https://www.docker.com/)

**AegisGate** is a next-generation AI-powered firewall designed to protect modern APIs from semantic attacks, abuse, and anomalies. Unlike traditional WAFs that rely on static regex rules, AegisGate understands the **intent** of a request using vector embeddings and LLM analysis.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Real-time+Threat+Dashboard) 
*(Replace with actual screenshot of your dashboard)*

## 🚀 Key Features

*   **🧠 Semantic Anomaly Detection**: Detects "SQL Injection" or "Toxic Comments" even if they bypass regex filters, by analyzing vector similarity.
*   **🚦 Adaptive Rate Limiting**: Token-bucket algorithm backed by Redis to stop denial-of-service attacks.
*   **🛣️ Multi-API Routing**: Protect multiple backend services (Microservices) with a single firewall instance using `routes.yaml`.
*   **📊 Real-time Dashboard**: Live visualization of traffic, blocked threats, and attack types.
*   **⚡ High Performance**: Built on FastAPI and Async I/O for minimal latency overhead.
*   **🐋 Production Ready**: Includes Docker Compose setup and structured JSON logging.

---

## 🛠️ Quick Start

### Prerequisites
-   Docker & Docker Compose
-   Python 3.11+ (for local dev)

### 1. Installation

Clone the repository and enter the directory:
```bash
git clone https://github.com/yourusername/aegis-gate.git
cd aegis-gate
```

### 2. Configuration

Create a `.env` file (copy from example):
```bash
cp .env.example .env
```
Edit `.env` to set your `UPSTREAM_URL` (where your actual API lives).

**(Optional) Configure Routes**:
Edit `routes.yaml` to map specific paths to different services:
```yaml
routes:
  - name: "User Service"
    prefix: "/users"
    upstream: "http://user-service:3000"
```

### 3. Run with Docker (Recommended)

```bash
docker-compose up --build -d
```
The firewall is now running at **http://localhost:8000**.

### 4. Run Locally (Dev Mode)

Use the helper script to start Redis, a Mock Upstream, and the Firewall:
```bash
./run_dev.sh
```

---

## 🖥️ Dashboard

Access the real-time dashboard at:
👉 **[http://localhost:8000/dashboard](http://localhost:8000/dashboard)**

---

## 🛡️ How it Works

1.  **Intercept**: AegisGate sits as a reverse proxy in front of your API.
2.  **Analyze**:
    *   **Level 1**: Checks IP Reputation and Rate Limits (Redis).
    *   **Level 2**: Converts payload to Vector Embeddings (SentenceTransformer).
    *   **Level 3**: Calculates Anomaly Score against baseline.
3.  **Decide**:
    *   **Allow**: Forwards request to Upstream.
    *   **Block**: Returns `403 Forbidden` with a JSON breakdown.
4.  **Learn**: Logs every interaction to SQLite/JSON for audit and retraining.

---

## 🧪 Testing

You can use `curl` to simulate attacks:

**SQL Injection Attack:**
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"user": "admin", "pass": "'\'' OR 1=1 --"}'
```
> **Response**: `403 Forbidden` (Semantic Anomaly Detected)

**XSS Attack:**
```bash
curl -X POST http://localhost:8000/api/comment \
  -d '{"msg": "<script>alert(1)</script>"}'
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
