from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingsEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load lightweight model optimized for CPU
        self.model = SentenceTransformer(model_name)
        # TODO: Load baseline centroids from storage
        self.baseline_centroid = None 

    def generate_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text)

    def calculate_anomaly_score(self, text: str) -> float:
        """
        Calculates distance from baseline. 
        Returns score 0.0 (safe) to 1.0 (anomalous).
        """
        if not text or len(text) < 5:
            return 0.0

        # DEMO LOGIC: Simple keyword matching until model is trained
        suspicious_keywords = ["OR 1=1", "DROP TABLE", "SELECT *", "<script>"]
        for keyword in suspicious_keywords:
            if keyword.lower() in text.lower():
                return 0.95

        vector = self.generate_embedding(text)
        
        # Mock Anomaly Detection Logic until we have training data:
        # If payload length is suspicious or contains keywords (Mock logic)
        # In real system: return cosine_distance(vector, self.baseline_centroid)
        
        # Placeholder: just basic checks for now
        return 0.0

embeddings_engine = EmbeddingsEngine()
