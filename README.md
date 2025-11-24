# 🌍 Sky Travel - Plateforme de Recherche de Vols avec IA

Plateforme web complète de recherche et recommandation de vols utilisant l'intelligence artificielle (ChatGPT/OpenAI) pour fournir des suggestions personnalisées en temps réel.

## 🚀 Technologies Utilisées

### Frontend
- **Next.js 14** - Framework React pour applications web modernes
- **TypeScript** - Typage statique pour un code robuste
- **Tailwind CSS** - Framework CSS utilitaire
- **Socket.IO Client** - Communication temps réel avec le backend

### Backend
- **FastAPI** - Framework Python moderne et rapide
- **Python Socket.IO** - Gestion des WebSockets
- **LangChain** - Framework pour applications IA
- **OpenAI GPT-3.5** - Analyse intelligente des offres de vols
- **Uvicorn** - Serveur ASGI haute performance

## 📁 Structure du Projet

```
sky/
├── backend/
│   ├── main.py              # Application FastAPI principale
│   ├── config.py            # Configuration et variables d'environnement
│   ├── flight_analyzer.py   # Service d'analyse IA avec LangChain
│   ├── mock_data.py         # Générateur de données de vols mock
│   ├── requirements.txt     # Dépendances Python
│   ├── .env.example         # Exemple de fichier d'environnement
│   └── .gitignore
│
└── frontend/
    ├── app/
    │   ├── page.tsx         # Page principale
    │   ├── layout.tsx       # Layout de l'application
    │   └── globals.css      # Styles globaux
    ├── components/
    │   ├── SearchForm.tsx   # Formulaire de recherche
    │   ├── FlightCard.tsx   # Carte d'affichage d'un vol
    │   └── SearchResults.tsx # Affichage des résultats
    ├── hooks/
    │   └── useSocket.ts     # Hook pour Socket.IO
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── .env.example
    └── .gitignore
```

## 🔧 Installation et Configuration

### Prérequis
- **Node.js** (version 18 ou supérieure)
- **Python** (version 3.9 ou supérieure)
- **pip** (gestionnaire de paquets Python)
- **Clé API OpenAI** ([Obtenir une clé](https://platform.openai.com/api-keys))

### Configuration du Backend

1. **Naviguer dans le dossier backend**
```powershell
cd backend
```

2. **Créer un environnement virtuel Python (recommandé)**
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. **Installer les dépendances**
```powershell
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```powershell
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env et ajouter votre clé OpenAI
# OPENAI_API_KEY=votre_clé_api_openai_ici
```

**⚠️ IMPORTANT**: Éditez le fichier `.env` et remplacez `your_openai_api_key_here` par votre vraie clé API OpenAI.

5. **Démarrer le serveur backend**
```powershell
python main.py
```

Le serveur sera accessible sur `http://localhost:8000`

### Configuration du Frontend

1. **Ouvrir un nouveau terminal et naviguer dans le dossier frontend**
```powershell
cd frontend
```

2. **Installer les dépendances**
```powershell
npm install
```

3. **Configurer les variables d'environnement**
```powershell
# Copier le fichier d'exemple
cp .env.example .env
```

Le fichier `.env` contient déjà la bonne configuration par défaut :
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Démarrer le serveur de développement**
```powershell
npm run dev
```

Le frontend sera accessible sur `http://localhost:3000`

## 🎯 Utilisation

1. **Accédez au frontend** : Ouvrez votre navigateur sur `http://localhost:3000`

2. **Remplissez le formulaire** :
   - Ville de départ (ex: Paris, Tel Aviv)
   - Destination (ex: New York, London)
   - Date de départ
   - Compagnie aérienne préférée (optionnel)

3. **Lancez la recherche** : Cliquez sur "Rechercher avec l'IA"

4. **Visualisez les résultats** :
   - L'IA analyse les offres disponibles
   - Affichage des 5 meilleures recommandations
   - Chaque vol inclut une analyse détaillée de l'IA

## 🤖 Comment fonctionne l'IA ?

Le système utilise **LangChain** avec **OpenAI GPT-3.5** pour analyser les vols selon plusieurs critères :

1. **Rapport qualité/prix** - Meilleure valeur pour l'argent
2. **Durée de vol optimale** - Temps de trajet le plus court
3. **Nombre d'escales** - Privilégie les vols directs
4. **Horaires convenables** - Évite les heures extrêmes
5. **Réputation de la compagnie** - Compagnies fiables
6. **Services inclus** - Bagages, repas, WiFi, etc.

L'analyse est effectuée en temps réel via Socket.IO pour une expérience utilisateur fluide.

## 📊 Données Mock

Le projet utilise des **données mock réalistes** pour les tests. Le fichier `backend/mock_data.py` génère des vols avec :

- Prix variés (150€ - 1200€)
- Différentes compagnies aériennes
- Horaires réalistes
- Escales (0, 1 ou 2)
- Classes de cabine (Economy, Business, First)
- Équipements (WiFi, repas, bagages, etc.)

## 🔌 Intégration d'API Réelles

Pour passer aux données réelles, vous pouvez intégrer :

### APIs de vols disponibles :
- **Skyscanner API** - [Documentation](https://developers.skyscanner.net/)
- **Kiwi.com API** - [Documentation](https://docs.kiwi.com/)
- **Amadeus API** - [Documentation](https://developers.amadeus.com/)

### Étapes pour intégrer une API réelle :

1. **Obtenir les clés API** auprès du fournisseur

2. **Ajouter les clés dans `backend/.env`** :
```env
SKYSCANNER_API_KEY=votre_clé_ici
KIWI_API_KEY=votre_clé_ici
```

3. **Créer un nouveau fichier** `backend/flight_api.py` :
```python
import requests
from config import settings

def fetch_real_flights(origin, destination, date):
    # Exemple avec Kiwi.com API
    url = "https://api.tequila.kiwi.com/v2/search"
    headers = {"apikey": settings.kiwi_api_key}
    params = {
        "fly_from": origin,
        "fly_to": destination,
        "date_from": date,
        "date_to": date
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

4. **Modifier `backend/main.py`** pour utiliser l'API réelle :
```python
# Remplacer cette ligne :
flights = generate_mock_flights(...)

# Par :
flights = fetch_real_flights(origin, destination, date)
```

## 🛠️ Scripts Disponibles

### Backend
```powershell
# Démarrer le serveur
python main.py

# Démarrer avec rechargement automatique
uvicorn main:socket_app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```powershell
# Développement
npm run dev

# Build pour production
npm run build

# Démarrer en production
npm start

# Linter
npm run lint
```

## 🧪 Tests

### Tester le backend
```powershell
# Health check
curl http://localhost:8000/health

# Vérifier la connexion Socket.IO (via le frontend)
```

### Tester le frontend
1. Ouvrez `http://localhost:3000`
2. Vérifiez le statut de connexion (point vert)
3. Effectuez une recherche de test

## 📈 Évolutions Futures

Le projet est conçu pour être facilement extensible :

- ✅ **Filtres avancés** : Budget, préférences de voyage, allergies
- ✅ **Multi-destinations** : Recherche de vols avec plusieurs escales
- ✅ **Comparaison de prix** : Graphiques d'évolution des prix
- ✅ **Alertes de prix** : Notifications quand le prix baisse
- ✅ **Historique de recherches** : Sauvegarder les recherches favorites
- ✅ **Authentification utilisateur** : Profils personnalisés
- ✅ **Système de réservation** : Réservation directe dans l'application
- ✅ **Mode multi-langues** : Support de plusieurs langues

## 🐛 Résolution de Problèmes

### Le backend ne démarre pas
- Vérifiez que Python 3.9+ est installé : `python --version`
- Vérifiez que toutes les dépendances sont installées : `pip list`
- Vérifiez que le fichier `.env` existe et contient la clé OpenAI

### Le frontend ne se connecte pas au backend
- Vérifiez que le backend est démarré sur le port 8000
- Vérifiez la variable `NEXT_PUBLIC_API_URL` dans `.env`
- Vérifiez les logs de la console du navigateur (F12)

### Erreur "OpenAI API Key not found"
- Assurez-vous d'avoir créé le fichier `backend/.env`
- Vérifiez que la clé API est correcte et active
- La clé doit être au format : `OPENAI_API_KEY=sk-...`

### Les résultats ne s'affichent pas
- Ouvrez les outils de développement (F12)
- Vérifiez les messages d'erreur dans la console
- Vérifiez les événements Socket.IO dans l'onglet Network

## 📝 Licences et Crédits

- **Développement** : Sky Travel Team
- **Framework Frontend** : Next.js (MIT License)
- **Framework Backend** : FastAPI (MIT License)
- **IA** : OpenAI GPT-3.5 / LangChain

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation des APIs utilisées
- Vérifiez les logs du serveur pour les erreurs détaillées

---

**Bon développement avec Sky Travel ! ✈️🌍**
