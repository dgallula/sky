"""
Script de test simple pour vérifier le fonctionnement du backend.
Lance quelques requêtes de test pour valider la configuration.
"""

from mock_data import generate_mock_flights, POPULAR_DESTINATIONS
from flight_analyzer import flight_analyzer
from config import settings


def test_mock_data():
    """Teste la génération de données mock."""
    print("\n" + "="*60)
    print("TEST 1: Génération de données mock")
    print("="*60)
    
    flights = generate_mock_flights(
        origin="Paris",
        destination="New York",
        date="2025-12-25",
        airline="Air France"
    )
    
    print(f"✅ {len(flights)} vols générés")
    print(f"Prix min: {min(f['price'] for f in flights)}€")
    print(f"Prix max: {max(f['price'] for f in flights)}€")
    
    # Afficher un exemple de vol
    print("\nExemple de vol:")
    print(f"  Compagnie: {flights[0]['airline']}")
    print(f"  Prix: {flights[0]['price']}€")
    print(f"  Départ: {flights[0]['departure_time']}")
    print(f"  Arrivée: {flights[0]['arrival_time']}")
    print(f"  Escales: {flights[0]['stops']}")
    
    return flights


def test_flight_analyzer(flights):
    """Teste l'analyse des vols avec LangChain."""
    print("\n" + "="*60)
    print("TEST 2: Analyse avec LangChain/OpenAI")
    print("="*60)
    
    if not settings.openai_api_key or settings.openai_api_key == "":
        print("⚠️  ATTENTION: Clé OpenAI non configurée !")
        print("   Ajoutez votre clé dans backend/.env")
        print("   Le système utilisera les recommandations de secours")
    
    result = flight_analyzer.analyze_flights(
        flights=flights,
        origin="Paris",
        destination="New York",
        date="2025-12-25",
        airline="Air France"
    )
    
    if result['success']:
        print(f"✅ Analyse réussie")
        print(f"   {len(result['recommendations'])} recommandations générées")
        
        # Afficher la première recommandation
        if result['recommendations']:
            rec = result['recommendations'][0]
            print("\nMeilleure recommandation:")
            print(f"  Vol: {rec['airline']} - {rec['flight_number']}")
            print(f"  Prix: {rec['price']}€")
            
            if 'ai_analysis' in rec:
                print(f"  Rang: #{rec['ai_analysis']['rank']}")
                print(f"  Raison: {rec['ai_analysis']['reason']}")
    else:
        print("❌ Échec de l'analyse")


def test_configuration():
    """Teste la configuration du système."""
    print("\n" + "="*60)
    print("TEST 3: Vérification de la configuration")
    print("="*60)
    
    checks = {
        "OpenAI configuré": bool(settings.openai_api_key),
        "Port configuré": settings.port == 8000,
        "Host configuré": settings.host == "0.0.0.0",
    }
    
    for check, status in checks.items():
        symbol = "✅" if status else "❌"
        print(f"{symbol} {check}")
    
    print(f"\nDestinations disponibles: {len(POPULAR_DESTINATIONS)}")
    print("Exemples:", ", ".join(list(POPULAR_DESTINATIONS.keys())[:5]))


def main():
    """Fonction principale de test."""
    print("\n" + "🧪 " * 20)
    print("     TEST DU BACKEND SKY TRAVEL")
    print("🧪 " * 20)
    
    # Test 1: Mock data
    flights = test_mock_data()
    
    # Test 2: Configuration
    test_configuration()
    
    # Test 3: Flight analyzer
    test_flight_analyzer(flights[:10])  # Tester avec 10 vols
    
    print("\n" + "="*60)
    print("TESTS TERMINÉS")
    print("="*60)
    print("\n💡 Si tous les tests sont ✅, votre backend est prêt !")
    print("   Lancez-le avec: python main.py\n")


if __name__ == "__main__":
    main()
