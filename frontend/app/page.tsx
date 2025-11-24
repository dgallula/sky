/**
 * Page principale de l'application Sky Travel.
 * Gère le formulaire de recherche et l'affichage des résultats en temps réel.
 */

'use client';

import { useSocket, useFlightSearch } from '@/hooks/useSocket';
import SearchForm from '@/components/SearchForm';
import SearchResults from '@/components/SearchResults';

export default function Home() {
  // Connexion Socket.IO
  const { socket, isConnected, error: connectionError } = useSocket();

  // Gestion de la recherche de vols
  const {
    searchFlights,
    isSearching,
    searchStatus,
    results,
    error: searchError,
    clearResults,
  } = useFlightSearch(socket);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* En-tête */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🌍 Sky Travel
          </h1>
          <p className="text-xl text-gray-700 mb-2">
            Trouvez les meilleurs vols avec l'intelligence artificielle
          </p>
          <p className="text-sm text-gray-600">
            Recommandations personnalisées par ChatGPT
          </p>

          {/* Statut de connexion */}
          <div className="mt-4 inline-block">
            {isConnected ? (
              <span className="flex items-center text-green-600 text-sm">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                Connecté au serveur
              </span>
            ) : (
              <span className="flex items-center text-red-600 text-sm">
                <span className="w-2 h-2 bg-red-500 rounded-full mr-2"></span>
                {connectionError || 'Connexion au serveur...'}
              </span>
            )}
          </div>
        </div>

        {/* Contenu principal */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Formulaire de recherche */}
          <div className="lg:col-span-1">
            <SearchForm onSearch={searchFlights} isSearching={isSearching} />

            {/* Statut de recherche en cours */}
            {isSearching && searchStatus && (
              <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center">
                  <svg
                    className="animate-spin h-5 w-5 text-blue-600 mr-3"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  <p className="text-sm text-blue-800">{searchStatus}</p>
                </div>
              </div>
            )}

            {/* Erreur de recherche */}
            {searchError && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-800">❌ {searchError}</p>
              </div>
            )}

            {/* Informations sur le projet */}
            <div className="mt-8 bg-white rounded-lg shadow-md p-6">
              <h3 className="font-bold text-gray-800 mb-3">
                💡 Comment ça marche ?
              </h3>
              <ol className="text-sm text-gray-600 space-y-2">
                <li>1️⃣ Remplissez vos critères de voyage</li>
                <li>2️⃣ Notre IA analyse les offres disponibles</li>
                <li>3️⃣ Recevez les 5 meilleures recommandations</li>
                <li>4️⃣ Réservez directement le vol de votre choix</li>
              </ol>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-500">
                  🔒 Données mock pour démonstration
                  <br />
                  🚀 Prêt pour intégration API réelle
                </p>
              </div>
            </div>
          </div>

          {/* Résultats */}
          <div className="lg:col-span-2">
            {results ? (
              <SearchResults
                results={results}
                searchStatus={searchStatus}
                onNewSearch={clearResults}
              />
            ) : (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <div className="text-6xl mb-4">✈️</div>
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                  Prêt à partir ?
                </h2>
                <p className="text-gray-600">
                  Remplissez le formulaire pour commencer votre recherche.
                  <br />
                  Notre IA vous trouvera les meilleures offres !
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-600 text-sm">
          <p>
            Développé avec ❤️ par Sky Travel Team
            <br />
            React + Next.js • FastAPI • Socket.IO • LangChain • OpenAI
          </p>
        </footer>
      </div>
    </main>
  );
}
