# 🚀 GUIDE DE DÉMARRAGE RAPIDE - Sky Travel

## ⚡ Démarrage en 5 minutes

### Étape 1 : Backend (Terminal 1)

```powershell
# Aller dans le dossier backend
cd backend

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
.\venv\Scripts\Activate

# Installer les dépendances
pip install -r requirements.txt

# Copier et configurer les variables d'environnement
cp .env.example .env
# ⚠️ IMPORTANT : Éditez .env et ajoutez votre clé OpenAI !

# Démarrer le serveur
python main.py
```

✅ Le backend tourne sur `http://localhost:8000`

---

### Étape 2 : Frontend (Terminal 2 - NOUVEAU terminal)

```powershell
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Copier les variables d'environnement (déjà configuré)
cp .env.example .env

# Démarrer le frontend
npm run dev
```

✅ Le frontend tourne sur `http://localhost:3000`

---

### Étape 3 : Utilisation

1. Ouvrez votre navigateur : `http://localhost:3000`
2. Remplissez le formulaire :
   - Départ : Paris
   - Destination : New York
   - Date : (choisir une date future)
   - Compagnie : (optionnel) Air France
3. Cliquez sur "Rechercher avec l'IA"
4. Profitez des recommandations ! 🎉

---

## 🔑 Configuration de la clé OpenAI

### Obtenir une clé API OpenAI :
1. Allez sur https://platform.openai.com/api-keys
2. Créez un compte ou connectez-vous
3. Cliquez sur "Create new secret key"
4. Copiez la clé (elle commence par `sk-...`)

### L'ajouter au projet :
1. Ouvrez le fichier `backend/.env`
2. Remplacez `your_openai_api_key_here` par votre clé
3. Sauvegardez le fichier
4. Redémarrez le serveur backend

**Exemple** :
```env
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

---

## 🔥 Commandes Utiles

### Backend
```powershell
# Vérifier la santé de l'API
curl http://localhost:8000/health

# Voir les logs en direct
python main.py
```

### Frontend
```powershell
# Build pour production
npm run build

# Démarrer en production
npm start
```

---

## ❓ Problèmes Courants

### ❌ "OPENAI_API_KEY not found"
➡️ Vérifiez que le fichier `backend/.env` existe et contient votre clé

### ❌ "Cannot connect to server"
➡️ Vérifiez que le backend tourne sur le port 8000

### ❌ "Module not found"
➡️ Backend : `pip install -r requirements.txt`
➡️ Frontend : `npm install`

---

## 📦 Dépendances Principales

### Backend
- FastAPI : Framework web moderne
- LangChain : Framework pour IA
- OpenAI : API ChatGPT
- Socket.IO : Communication temps réel

### Frontend
- Next.js 14 : Framework React
- TypeScript : Typage statique
- Tailwind CSS : Styles utilitaires
- Socket.IO Client : WebSocket client

---

**Bon développement ! 🚀**
