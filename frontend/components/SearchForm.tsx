/**
 * Composant de formulaire de recherche de vols.
 * Permet à l'utilisateur de saisir ses critères de voyage.
 */

'use client';

import { useState, FormEvent } from 'react';
import { FlightSearchParams } from '@/hooks/useSocket';

interface SearchFormProps {
  onSearch: (params: FlightSearchParams) => void;
  isSearching: boolean;
}

export default function SearchForm({ onSearch, isSearching }: SearchFormProps) {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [date, setDate] = useState('');
  const [airline, setAirline] = useState('');

  // Obtenir la date minimale (aujourd'hui)
  const today = new Date().toISOString().split('T')[0];

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (!origin || !destination || !date) {
      alert('Veuillez remplir tous les champs obligatoires');
      return;
    }

    onSearch({
      origin: origin.trim(),
      destination: destination.trim(),
      date,
      airline: airline.trim(),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        ✈️ Rechercher un vol
      </h2>

      {/* Origine */}
      <div>
        <label htmlFor="origin" className="block text-sm font-medium text-gray-700 mb-2">
          Ville de départ *
        </label>
        <input
          type="text"
          id="origin"
          value={origin}
          onChange={(e) => setOrigin(e.target.value)}
          placeholder="Ex: Paris, Tel Aviv, New York"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
          disabled={isSearching}
          required
        />
      </div>

      {/* Destination */}
      <div>
        <label htmlFor="destination" className="block text-sm font-medium text-gray-700 mb-2">
          Destination *
        </label>
        <input
          type="text"
          id="destination"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          placeholder="Ex: London, Tokyo, Barcelona"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
          disabled={isSearching}
          required
        />
      </div>

      {/* Date */}
      <div>
        <label htmlFor="date" className="block text-sm font-medium text-gray-700 mb-2">
          Date de départ *
        </label>
        <input
          type="date"
          id="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          min={today}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
          disabled={isSearching}
          required
        />
      </div>

      {/* Compagnie aérienne (optionnel) */}
      <div>
        <label htmlFor="airline" className="block text-sm font-medium text-gray-700 mb-2">
          Compagnie aérienne préférée (optionnel)
        </label>
        <input
          type="text"
          id="airline"
          value={airline}
          onChange={(e) => setAirline(e.target.value)}
          placeholder="Ex: Air France, El Al, Emirates"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
          disabled={isSearching}
        />
        <p className="mt-1 text-sm text-gray-500">
          L'IA privilégiera cette compagnie si possible
        </p>
      </div>

      {/* Bouton de soumission */}
      <button
        type="submit"
        disabled={isSearching}
        className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
          isSearching
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-primary-600 hover:bg-primary-700 active:scale-95'
        }`}
      >
        {isSearching ? (
          <span className="flex items-center justify-center">
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
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
            Recherche en cours...
          </span>
        ) : (
          '🔍 Rechercher avec l\'IA'
        )}
      </button>
    </form>
  );
}
