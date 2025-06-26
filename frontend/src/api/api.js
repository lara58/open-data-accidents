// src/api/api.js
import axios from 'axios';

const API_URL = 'http://localhost:5000/api'; // Ajout du préfixe /api

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Ajouter le token JWT aux requêtes
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Gestion des réponses d'erreur globale
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Rediriger vers login si 401 (non autorisé)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;