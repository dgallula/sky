"""
Service d'analyse de vols utilisant LangChain et OpenAI.
Analyse les offres de vols et fournit des recommandations intelligentes.
"""

from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from config import settings
import json


class FlightAnalyzerService:
    """
    Service pour analyser les offres de vols avec LangChain et OpenAI.
    Fournit des recommandations basées sur plusieurs critères.
    """
    
    def __init__(self):
        """Initialise le modèle OpenAI et le pipeline LangChain."""
        
        # Initialiser le modèle ChatGPT
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,  # Température basse pour des réponses plus déterministes
            openai_api_key=settings.openai_api_key
        )
        
        # Créer le prompt template pour l'analyse
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Tu es un expert en voyage et conseiller en réservation de vols.
            Ta mission est d'analyser les offres de vols et de recommander les 5 meilleures options.
            
            Critères de sélection:
            1. Meilleur rapport qualité/prix
            2. Durée de vol optimale
            3. Nombre d'escales (privilégier les vols directs)
            4. Horaires convenables (éviter les départs très tôt ou très tard sauf si avantageux)
            5. Compagnie aérienne réputée
            6. Services inclus (bagages, repas, WiFi)
            
            Fournis une analyse concise et utile pour chaque recommandation."""),
            ("user", """Voici les critères de recherche:
            - Origine: {origin}
            - Destination: {destination}
            - Date: {date}
            - Compagnie préférée: {airline}
            
            Voici les offres de vols disponibles:
            {flights_json}
            
            Recommande les 5 meilleures offres avec une brève explication (2-3 phrases) pour chacune.
            Format de réponse attendu (JSON):
            {{
                "recommendations": [
                    {{
                        "flight_id": "FL1001",
                        "rank": 1,
                        "reason": "Explication courte et claire",
                        "highlights": ["point fort 1", "point fort 2"]
                    }}
                ]
            }}""")
        ])
        
        # Créer la chaîne LangChain
        self.chain = self.prompt_template | self.llm | StrOutputParser()
    
    
    def analyze_flights(
        self,
        flights: List[Dict],
        origin: str,
        destination: str,
        date: str,
        airline: str = "Aucune préférence"
    ) -> Dict:
        """
        Analyse les vols et retourne les 5 meilleures recommandations.
        
        Args:
            flights: Liste des vols disponibles
            origin: Ville d'origine
            destination: Ville de destination
            date: Date du voyage
            airline: Compagnie préférée (optionnel)
        
        Returns:
            Dictionnaire contenant les recommandations et l'analyse
        """
        
        try:
            # Convertir les vols en JSON pour le prompt
            flights_json = json.dumps(flights, indent=2, ensure_ascii=False)
            
            # Exécuter la chaîne LangChain
            response = self.chain.invoke({
                "origin": origin,
                "destination": destination,
                "date": date,
                "airline": airline if airline else "Aucune préférence",
                "flights_json": flights_json
            })
            
            # Parser la réponse JSON
            try:
                # Extraire le JSON de la réponse
                response_clean = response.strip()
                if "```json" in response_clean:
                    response_clean = response_clean.split("```json")[1].split("```")[0]
                elif "```" in response_clean:
                    response_clean = response_clean.split("```")[1].split("```")[0]
                
                analysis = json.loads(response_clean)
                
                # Enrichir les recommandations avec les données complètes des vols
                enriched_recommendations = []
                for rec in analysis.get("recommendations", [])[:5]:
                    flight_id = rec.get("flight_id")
                    # Trouver le vol correspondant
                    flight_data = next(
                        (f for f in flights if f["id"] == flight_id),
                        None
                    )
                    
                    if flight_data:
                        enriched_recommendations.append({
                            **flight_data,
                            "ai_analysis": {
                                "rank": rec.get("rank"),
                                "reason": rec.get("reason"),
                                "highlights": rec.get("highlights", [])
                            }
                        })
                
                return {
                    "success": True,
                    "recommendations": enriched_recommendations,
                    "total_flights_analyzed": len(flights)
                }
                
            except json.JSONDecodeError as e:
                # Si le parsing JSON échoue, retourner les 5 meilleurs vols par prix
                print(f"Erreur de parsing JSON: {e}")
                print(f"Réponse brute: {response}")
                return self._fallback_recommendations(flights)
        
        except Exception as e:
            print(f"Erreur lors de l'analyse: {e}")
            return self._fallback_recommendations(flights)
    
    
    def _fallback_recommendations(self, flights: List[Dict]) -> Dict:
        """
        Recommandations de secours si l'analyse IA échoue.
        Sélectionne simplement les 5 vols les moins chers avec vols directs prioritaires.
        """
        
        # Trier par nombre d'escales puis par prix
        sorted_flights = sorted(
            flights,
            key=lambda x: (x["stops"], x["price"])
        )
        
        top_5 = sorted_flights[:5]
        
        # Ajouter une analyse basique
        for i, flight in enumerate(top_5):
            reasons = []
            if flight["stops"] == 0:
                reasons.append("Vol direct")
            if flight["price"] < 300:
                reasons.append("Prix très compétitif")
            elif flight["price"] < 500:
                reasons.append("Bon rapport qualité/prix")
            
            flight["ai_analysis"] = {
                "rank": i + 1,
                "reason": f"Recommandé pour: {', '.join(reasons) if reasons else 'Bon choix général'}",
                "highlights": reasons
            }
        
        return {
            "success": True,
            "recommendations": top_5,
            "total_flights_analyzed": len(flights),
            "note": "Recommandations basées sur le prix et les escales (mode de secours)"
        }


# Instance globale du service
flight_analyzer = FlightAnalyzerService()
