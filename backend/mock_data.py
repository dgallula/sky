"""
Données mock pour les offres de vols.
Ces données simulent les réponses d'API réelles (Skyscanner, Kiwi, Amadeus).
"""

from typing import List, Dict
import random
from datetime import datetime, timedelta


def generate_mock_flights(
    origin: str,
    destination: str,
    date: str,
    airline: str = None
) -> List[Dict]:
    """
    Génère des données de vols mock basées sur les critères de recherche.
    
    Args:
        origin: Aéroport d'origine (ex: "TLV", "Paris")
        destination: Aéroport de destination (ex: "NYC", "London")
        date: Date du vol (format: YYYY-MM-DD)
        airline: Compagnie aérienne (optionnel)
    
    Returns:
        Liste de dictionnaires contenant les informations de vols
    """
    
    # Liste de compagnies aériennes
    airlines = [
        "Air France",
        "El Al",
        "Lufthansa",
        "Emirates",
        "British Airways",
        "Turkish Airlines",
        "KLM",
        "Ryanair",
        "EasyJet",
        "Wizz Air"
    ]
    
    # Si une compagnie spécifique est demandée, l'utiliser en priorité
    if airline and airline.strip():
        selected_airlines = [airline] + random.sample(
            [a for a in airlines if a.lower() != airline.lower()], 
            min(4, len(airlines) - 1)
        )
    else:
        selected_airlines = airlines
    
    # Générer entre 8 et 15 vols
    num_flights = random.randint(8, 15)
    flights = []
    
    # Parser la date de départ
    try:
        departure_date = datetime.strptime(date, "%Y-%m-%d")
    except:
        departure_date = datetime.now() + timedelta(days=30)
    
    for i in range(num_flights):
        # Heure de départ aléatoire
        departure_hour = random.randint(0, 23)
        departure_minute = random.choice([0, 15, 30, 45])
        departure_time = departure_date.replace(
            hour=departure_hour, 
            minute=departure_minute
        )
        
        # Durée du vol (entre 2h et 15h)
        flight_duration_hours = random.randint(2, 15)
        flight_duration_minutes = random.choice([0, 15, 30, 45])
        
        # Calculer l'heure d'arrivée
        arrival_time = departure_time + timedelta(
            hours=flight_duration_hours,
            minutes=flight_duration_minutes
        )
        
        # Prix (entre 150 et 1200 EUR)
        base_price = random.randint(150, 1200)
        
        # Nombre d'escales (0, 1 ou 2)
        stops = random.choices([0, 1, 2], weights=[50, 35, 15])[0]
        
        # Sièges disponibles
        available_seats = random.randint(1, 150)
        
        # Type de cabine
        cabin_class = random.choice(["Economy", "Economy", "Economy", "Premium Economy", "Business", "First Class"])
        
        # Ajuster le prix selon la classe
        if cabin_class == "Premium Economy":
            base_price = int(base_price * 1.5)
        elif cabin_class == "Business":
            base_price = int(base_price * 2.5)
        elif cabin_class == "First Class":
            base_price = int(base_price * 4)
        
        # Compagnie aérienne
        airline_name = random.choice(selected_airlines)
        
        # Bagages inclus
        checked_baggage = random.choice([0, 1, 2])
        carry_on = 1
        
        flight = {
            "id": f"FL{1000 + i}",
            "airline": airline_name,
            "flight_number": f"{airline_name[:2].upper()}{random.randint(100, 999)}",
            "origin": origin,
            "destination": destination,
            "departure_time": departure_time.strftime("%Y-%m-%d %H:%M"),
            "arrival_time": arrival_time.strftime("%Y-%m-%d %H:%M"),
            "duration": f"{flight_duration_hours}h {flight_duration_minutes}m",
            "price": base_price,
            "currency": "EUR",
            "stops": stops,
            "cabin_class": cabin_class,
            "available_seats": available_seats,
            "baggage": {
                "carry_on": carry_on,
                "checked": checked_baggage
            },
            "amenities": generate_amenities(),
            "booking_url": f"https://booking.example.com/flight/{1000 + i}"
        }
        
        flights.append(flight)
    
    # Trier par prix
    flights.sort(key=lambda x: x["price"])
    
    return flights


def generate_amenities() -> List[str]:
    """Génère une liste aléatoire d'équipements disponibles dans l'avion."""
    all_amenities = [
        "WiFi gratuit",
        "Divertissement à bord",
        "Prise électrique",
        "USB",
        "Repas inclus",
        "Snacks gratuits",
        "Boissons incluses",
        "Espace pour les jambes étendu",
        "Siège inclinable"
    ]
    
    # Sélectionner 3-7 équipements aléatoires
    num_amenities = random.randint(3, 7)
    return random.sample(all_amenities, num_amenities)


# Exemples de destinations populaires avec codes IATA
POPULAR_DESTINATIONS = {
    "Paris": "CDG",
    "New York": "JFK",
    "London": "LHR",
    "Tokyo": "NRT",
    "Dubai": "DXB",
    "Barcelona": "BCN",
    "Rome": "FCO",
    "Amsterdam": "AMS",
    "Berlin": "BER",
    "Istanbul": "IST",
    "Tel Aviv": "TLV",
    "Los Angeles": "LAX",
    "Bangkok": "BKK",
    "Singapore": "SIN",
    "Sydney": "SYD"
}


def get_airport_code(city_name: str) -> str:
    """Convertit un nom de ville en code IATA d'aéroport."""
    return POPULAR_DESTINATIONS.get(city_name, city_name.upper()[:3])
