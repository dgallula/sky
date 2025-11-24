"""
Application principale FastAPI avec intégration Socket.IO.
Gère les connexions WebSocket et les recherches de vols en temps réel.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from typing import Dict
import asyncio

from config import settings
from mock_data import generate_mock_flights, get_airport_code
from flight_analyzer import flight_analyzer


# Créer l'application FastAPI
app = FastAPI(
    title="Sky Travel API",
    description="API de recherche et recommandation de vols avec IA",
    version="1.0.0"
)

# Configurer CORS pour permettre les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer le serveur Socket.IO
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.allowed_origins
)

# Combiner FastAPI et Socket.IO
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app
)


# ==================== Routes HTTP ====================

@app.get("/")
async def root():
    """Route de base pour vérifier que l'API fonctionne."""
    return {
        "message": "Sky Travel API is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "websocket": "Socket.IO connection available"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint pour vérifier la santé de l'API."""
    return {
        "status": "healthy",
        "openai_configured": bool(settings.openai_api_key),
        "services": {
            "fastapi": "running",
            "socketio": "running",
            "langchain": "configured"
        }
    }


# ==================== Socket.IO Events ====================

@sio.event
async def connect(sid, environ):
    """
    Événement déclenché quand un client se connecte.
    
    Args:
        sid: Session ID du client
        environ: Informations sur l'environnement de connexion
    """
    print(f"Client connecté: {sid}")
    await sio.emit('connection_response', {
        'message': 'Connecté au serveur Sky Travel',
        'sid': sid
    }, room=sid)


@sio.event
async def disconnect(sid):
    """
    Événement déclenché quand un client se déconnecte.
    
    Args:
        sid: Session ID du client
    """
    print(f"Client déconnecté: {sid}")


@sio.event
async def search_flights(sid, data: Dict):
    """
    Événement principal pour rechercher des vols.
    Reçoit les critères de recherche, génère des vols mock,
    les analyse avec IA, et renvoie les recommandations en temps réel.
    
    Args:
        sid: Session ID du client
        data: Dictionnaire contenant origin, destination, date, airline
    """
    
    try:
        print(f"Recherche de vols reçue de {sid}: {data}")
        
        # Extraire les paramètres de recherche
        origin = data.get('origin', '')
        destination = data.get('destination', '')
        date = data.get('date', '')
        airline = data.get('airline', '')
        
        # Valider les données
        if not origin or not destination or not date:
            await sio.emit('search_error', {
                'error': 'Paramètres manquants',
                'message': 'Veuillez fournir l\'origine, la destination et la date'
            }, room=sid)
            return
        
        # Étape 1: Notifier que la recherche commence
        await sio.emit('search_status', {
            'status': 'searching',
            'message': f'Recherche de vols de {origin} vers {destination}...'
        }, room=sid)
        
        # Simuler un délai de recherche (pour l'effet temps réel)
        await asyncio.sleep(1)
        
        # Étape 2: Générer les vols mock
        flights = generate_mock_flights(
            origin=origin,
            destination=destination,
            date=date,
            airline=airline
        )
        
        await sio.emit('search_status', {
            'status': 'analyzing',
            'message': f'{len(flights)} vols trouvés. Analyse en cours avec l\'IA...'
        }, room=sid)
        
        # Simuler un délai d'analyse
        await asyncio.sleep(1.5)
        
        # Étape 3: Analyser avec LangChain/OpenAI
        analysis_result = flight_analyzer.analyze_flights(
            flights=flights,
            origin=origin,
            destination=destination,
            date=date,
            airline=airline
        )
        
        # Étape 4: Envoyer les résultats
        await sio.emit('search_complete', {
            'status': 'completed',
            'data': analysis_result,
            'search_params': {
                'origin': origin,
                'destination': destination,
                'date': date,
                'airline': airline
            }
        }, room=sid)
        
        print(f"Recherche complétée pour {sid}")
        
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")
        await sio.emit('search_error', {
            'error': 'Erreur serveur',
            'message': str(e)
        }, room=sid)


@sio.event
async def get_flight_details(sid, data: Dict):
    """
    Récupère les détails complets d'un vol spécifique.
    
    Args:
        sid: Session ID du client
        data: Dictionnaire contenant flight_id
    """
    
    try:
        flight_id = data.get('flight_id')
        
        if not flight_id:
            await sio.emit('flight_details_error', {
                'error': 'ID de vol manquant'
            }, room=sid)
            return
        
        # En production, récupérer les détails depuis une base de données ou une API
        # Pour le moment, on renvoie une confirmation
        await sio.emit('flight_details_response', {
            'flight_id': flight_id,
            'message': 'Détails du vol disponibles',
            'booking_ready': True
        }, room=sid)
        
    except Exception as e:
        print(f"Erreur lors de la récupération des détails: {e}")
        await sio.emit('flight_details_error', {
            'error': str(e)
        }, room=sid)


# ==================== Lancement de l'application ====================

if __name__ == "__main__":
    import uvicorn
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║          Sky Travel API - Serveur de développement       ║
    ╠══════════════════════════════════════════════════════════╣
    ║  🚀 Serveur démarré sur: http://{settings.host}:{settings.port}       ║
    ║  📡 Socket.IO actif                                      ║
    ║  🤖 LangChain/OpenAI configuré                          ║
    ╚══════════════════════════════════════════════════════════╝
    
    Pour tester l'API:
    - Health check: http://localhost:{settings.port}/health
    - WebSocket: Connectez-vous via le frontend
    
    Appuyez sur CTRL+C pour arrêter le serveur.
    """)
    
    uvicorn.run(
        "main:socket_app",
        host=settings.host,
        port=settings.port,
        reload=True,  # Rechargement automatique en développement
        log_level="info"
    )
