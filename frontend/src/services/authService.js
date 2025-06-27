// src/services/authService.js
import api from '../api/api';

export const authService = {
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  login: async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      // Stocker les informations utilisateur si elles sont incluses dans la réponse
      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
    }
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
  
  getProfile: async () => {
    const response = await api.get('/auth/profile');
    // Stocker les informations utilisateur à jour
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },
  
  updateProfile: async (userData) => {
    const response = await api.put('/auth/update-profile', userData);
    // Mettre à jour les informations utilisateur dans localStorage
    if (response.data.user) {
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },
  
  // Nouvelle fonction pour récupérer l'utilisateur courant
  getCurrentUser: () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        return null;
      }
      
      // Récupérer l'utilisateur du localStorage
      const userStr = localStorage.getItem('user');
      if (userStr) {
        return JSON.parse(userStr);
      }
      
      // Si pas d'utilisateur stocké mais un token existe,
      // on pourrait décoder le token ou appeler getProfile()
      return null;
    } catch (error) {
      console.error("Erreur lors de la récupération de l'utilisateur", error);
      return null;
    }
  }
};