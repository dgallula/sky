/**
 * Hook personnalisé pour gérer la connexion Socket.IO avec le backend.
 * Gère la connexion, déconnexion et les événements en temps réel.
 */

import { useEffect, useState, useCallback } from 'react';
import io, { Socket } from 'socket.io-client';

const SOCKET_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface UseSocketReturn {
  socket: Socket | null;
  isConnected: boolean;
  error: string | null;
}

export const useSocket = (): UseSocketReturn => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Créer la connexion Socket.IO
    const socketInstance = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    // Événements de connexion
    socketInstance.on('connect', () => {
      console.log('Connecté au serveur Socket.IO');
      setIsConnected(true);
      setError(null);
    });

    socketInstance.on('disconnect', () => {
      console.log('Déconnecté du serveur Socket.IO');
      setIsConnected(false);
    });

    socketInstance.on('connect_error', (err) => {
      console.error('Erreur de connexion:', err);
      setError('Impossible de se connecter au serveur');
      setIsConnected(false);
    });

    socketInstance.on('connection_response', (data) => {
      console.log('Réponse de connexion:', data);
    });

    setSocket(socketInstance);

    // Nettoyage lors du démontage du composant
    return () => {
      socketInstance.disconnect();
    };
  }, []);

  return { socket, isConnected, error };
};

/**
 * Interface pour les paramètres de recherche de vol
 */
export interface FlightSearchParams {
  origin: string;
  destination: string;
  date: string;
  airline?: string;
}

/**
 * Interface pour un vol
 */
export interface Flight {
  id: string;
  airline: string;
  flight_number: string;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  duration: string;
  price: number;
  currency: string;
  stops: number;
  cabin_class: string;
  available_seats: number;
  baggage: {
    carry_on: number;
    checked: number;
  };
  amenities: string[];
  booking_url: string;
  ai_analysis?: {
    rank: number;
    reason: string;
    highlights: string[];
  };
}

/**
 * Interface pour le résultat de recherche
 */
export interface SearchResult {
  success: boolean;
  recommendations: Flight[];
  total_flights_analyzed: number;
  note?: string;
}

/**
 * Hook pour gérer la recherche de vols
 */
export const useFlightSearch = (socket: Socket | null) => {
  const [isSearching, setIsSearching] = useState(false);
  const [searchStatus, setSearchStatus] = useState<string>('');
  const [results, setResults] = useState<SearchResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!socket) return;

    // Écouter les événements de recherche
    socket.on('search_status', (data: { status: string; message: string }) => {
      setSearchStatus(data.message);
    });

    socket.on('search_complete', (data: { status: string; data: SearchResult }) => {
      setResults(data.data);
      setIsSearching(false);
      setSearchStatus('Recherche terminée');
    });

    socket.on('search_error', (data: { error: string; message: string }) => {
      setError(data.message);
      setIsSearching(false);
      setSearchStatus('');
    });

    // Nettoyage
    return () => {
      socket.off('search_status');
      socket.off('search_complete');
      socket.off('search_error');
    };
  }, [socket]);

  const searchFlights = useCallback(
    (params: FlightSearchParams) => {
      if (!socket) {
        setError('Pas de connexion au serveur');
        return;
      }

      setIsSearching(true);
      setError(null);
      setResults(null);
      setSearchStatus('Démarrage de la recherche...');

      socket.emit('search_flights', params);
    },
    [socket]
  );

  const clearResults = useCallback(() => {
    setResults(null);
    setError(null);
    setSearchStatus('');
  }, []);

  return {
    searchFlights,
    isSearching,
    searchStatus,
    results,
    error,
    clearResults,
  };
};
