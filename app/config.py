import os
from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    APP_NAME: str = "AegisGate AI Firewall"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Server
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Upstream (Default Fallback)
    UPSTREAM_URL: str = "http://localhost:8080"
    
    # Path Routing: Map URL prefixes to upstream Services
    API_ROUTES: Dict[str, str] = {}
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    ADMIN_API_KEY: str = "secret"
    JWT_SECRET: str = "secret"
    
    # AI Config
    ENABLE_EMBEDDINGS: bool = True
    ENABLE_ANOMALY_DETECTION: bool = True

    class Config:
        env_file = ".env"

    def load_routes_from_yaml(self):
        import yaml
        import os
        
        yaml_path = "routes.yaml"
        if os.path.exists(yaml_path):
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                if data and "routes" in data:
                    for route in data["routes"]:
                        # Convert to dict format expected by lookup
                        # Ensure upstream doesn't have trailing slash
                        upstream = route["upstream"].rstrip("/")
                        self.API_ROUTES[route["prefix"]] = upstream
                        print(f"Loaded Route: {route['name']} ({route['prefix']} -> {upstream})")

settings = Settings()
settings.load_routes_from_yaml()
