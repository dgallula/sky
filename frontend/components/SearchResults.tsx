/**
 * Composant pour afficher les résultats de recherche.
 * Affiche la liste des vols recommandés par l'IA.
 */

'use client';

import { SearchResult } from '@/hooks/useSocket';
import FlightCard from './FlightCard';

interface SearchResultsProps {
  results: SearchResult;
  searchStatus: string;
  onNewSearch: () => void;
}

export default function SearchResults({
  results,
  searchStatus,
  onNewSearch,
}: SearchResultsProps) {
  return (
    <div className="space-y-6">
      {/* En-tête des résultats */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              🎯 Résultats de la recherche
            </h2>
            <p className="text-gray-600 mt-1">
              {results.total_flights_analyzed} vols analysés -{' '}
              {results.recommendations.length} recommandations
            </p>
            {results.note && (
              <p className="text-sm text-amber-600 mt-2">ℹ️ {results.note}</p>
            )}
          </div>
          <button
            onClick={onNewSearch}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors"
          >
            🔄 Nouvelle recherche
          </button>
        </div>

        {searchStatus && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-sm text-blue-800">{searchStatus}</p>
          </div>
        )}
      </div>

      {/* Liste des vols */}
      {results.recommendations.length > 0 ? (
        <div className="space-y-4">
          {results.recommendations.map((flight) => (
            <FlightCard key={flight.id} flight={flight} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <p className="text-gray-500 text-lg">
            Aucun vol trouvé pour ces critères.
          </p>
          <button
            onClick={onNewSearch}
            className="mt-4 px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors"
          >
            Essayer une autre recherche
          </button>
        </div>
      )}
    </div>
  );
}
