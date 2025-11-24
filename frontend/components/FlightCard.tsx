/**
 * Composant pour afficher un vol individuel.
 * Affiche toutes les informations du vol avec l'analyse IA.
 */

'use client';

import { Flight } from '@/hooks/useSocket';

interface FlightCardProps {
  flight: Flight;
}

export default function FlightCard({ flight }: FlightCardProps) {
  const {
    airline,
    flight_number,
    departure_time,
    arrival_time,
    duration,
    price,
    currency,
    stops,
    cabin_class,
    available_seats,
    baggage,
    amenities,
    booking_url,
    ai_analysis,
  } = flight;

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow p-6 border-l-4 border-primary-500">
      {/* En-tête avec rang IA */}
      {ai_analysis && (
        <div className="flex items-center justify-between mb-4">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-primary-100 text-primary-800">
            🏆 Recommandation #{ai_analysis.rank}
          </span>
          <span className="text-sm text-gray-500">{flight_number}</span>
        </div>
      )}

      {/* Informations principales */}
      <div className="mb-4">
        <h3 className="text-xl font-bold text-gray-800 mb-2">{airline}</h3>
        
        {/* Horaires */}
        <div className="flex items-center justify-between mb-3">
          <div>
            <p className="text-2xl font-bold text-gray-900">
              {new Date(departure_time).toLocaleTimeString('fr-FR', {
                hour: '2-digit',
                minute: '2-digit',
              })}
            </p>
            <p className="text-sm text-gray-600">Départ</p>
          </div>

          <div className="flex-1 mx-4">
            <div className="flex items-center">
              <div className="flex-1 border-t-2 border-gray-300"></div>
              <span className="px-2 text-sm text-gray-500">
                {duration}
              </span>
              <div className="flex-1 border-t-2 border-gray-300"></div>
            </div>
            <p className="text-center text-xs text-gray-500 mt-1">
              {stops === 0 ? 'Vol direct' : `${stops} escale${stops > 1 ? 's' : ''}`}
            </p>
          </div>

          <div>
            <p className="text-2xl font-bold text-gray-900">
              {new Date(arrival_time).toLocaleTimeString('fr-FR', {
                hour: '2-digit',
                minute: '2-digit',
              })}
            </p>
            <p className="text-sm text-gray-600">Arrivée</p>
          </div>
        </div>

        {/* Prix */}
        <div className="bg-primary-50 rounded-lg p-3 mb-3">
          <p className="text-3xl font-bold text-primary-700">
            {price} {currency}
          </p>
          <p className="text-sm text-gray-600">{cabin_class}</p>
        </div>
      </div>

      {/* Analyse IA */}
      {ai_analysis && (
        <div className="bg-green-50 rounded-lg p-4 mb-4 border border-green-200">
          <p className="text-sm font-semibold text-green-800 mb-2">
            🤖 Analyse IA:
          </p>
          <p className="text-sm text-gray-700 mb-2">{ai_analysis.reason}</p>
          {ai_analysis.highlights.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {ai_analysis.highlights.map((highlight, index) => (
                <span
                  key={index}
                  className="inline-block px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full"
                >
                  ✓ {highlight}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Détails supplémentaires */}
      <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
        <div>
          <p className="text-gray-600">Bagages:</p>
          <p className="font-semibold">
            {baggage.carry_on} bagage cabine, {baggage.checked} bagage(s) en soute
          </p>
        </div>
        <div>
          <p className="text-gray-600">Sièges disponibles:</p>
          <p className="font-semibold">{available_seats}</p>
        </div>
      </div>

      {/* Équipements */}
      {amenities.length > 0 && (
        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-2">Équipements:</p>
          <div className="flex flex-wrap gap-2">
            {amenities.slice(0, 4).map((amenity, index) => (
              <span
                key={index}
                className="inline-block px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
              >
                {amenity}
              </span>
            ))}
            {amenities.length > 4 && (
              <span className="inline-block px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                +{amenities.length - 4} autres
              </span>
            )}
          </div>
        </div>
      )}

      {/* Bouton de réservation */}
      <a
        href={booking_url}
        target="_blank"
        rel="noopener noreferrer"
        className="block w-full text-center bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        Réserver ce vol
      </a>
    </div>
  );
}
