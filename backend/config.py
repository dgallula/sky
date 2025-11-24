"""
Configuration centralisée de l'application.
Charge les variables d'environnement et fournit les paramètres de configuration.
"""

from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

# Charger explicitement le fichier .env
load_dotenv()


class Settings(BaseSettings):
    """
    Configuration de l'application utilisant Pydantic pour la validation.
    Les valeurs sont chargées depuis le fichier .env
    """
    
    # OpenAI Configuration
    openai_api_key: str = ""
    
    # API Keys pour les services de vols (optionnel)
    skyscanner_api_key: Optional[str] = None
    kiwi_api_key: Optional[str] = None
    amadeus_api_key: Optional[str] = None
    amadeus_api_secret: Optional[str] = None
    
    # Serveur Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS Configuration
    allowed_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignorer les champs supplémentaires


# Instance globale des paramètres
settings = Settings()
