import sqlite3
import json
import logging
from datetime import datetime
from app.models.logs import LogEntry
from typing import List, Dict, Any

DB_PATH = "data/aegis.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            ip TEXT,
            request_path TEXT,
            method TEXT,
            decision TEXT,
            score REAL,
            reasons TEXT,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()

class SqliteLogger:
    def log(self, ip: str, path: str, method: str, decision: str, score: float, reasons: str, metadata: Dict[str, Any]):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO access_logs (timestamp, ip, request_path, method, decision, score, reasons, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (datetime.utcnow(), ip, path, method, decision, score, reasons, json.dumps(metadata)))
        conn.commit()
        conn.close()

    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM access_logs ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_stats(self) -> Dict:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), AVG(score) FROM access_logs")
        total, avg_score = cursor.fetchone()
        
        cursor.execute("SELECT decision, COUNT(*) FROM access_logs GROUP BY decision")
        decisions = dict(cursor.fetchall())
        
        conn.close()
        return {
            "total_requests": total,
            "avg_threat_score": avg_score or 0,
            "decisions": decisions
        }

db_logger = SqliteLogger()
