// src/services/accidentService.js
import api from '../api/api';

export const accidentService = {
  getAllAccidents: async () => {
    try {
      const response = await api.get('/accidents');
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des accidents:", error);
      throw error;
    }
  },
  
  getUserAccidents: async () => {
    try {
      const response = await api.get('/accidents/user');
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la récupération des accidents de l'utilisateur:", error);
      throw error;
    }
  },
  
  getAccidentById: async (id) => {
    try {
      const response = await api.get(`/accidents/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la récupération de l'accident #${id}:`, error);
      throw error;
    }
  },
  
  createAccident: async (accidentData) => {
    try {
      const response = await api.post('/accidents', accidentData);
      return response.data; // Cette réponse contient l'ID et potentiellement la gravité prédite
    } catch (error) {
      console.error("Erreur lors de la création de l'accident:", error);
      throw error;
    }
  },
  
  updateAccident: async (id, accidentData) => {
    try {
      const response = await api.put(`/accidents/${id}`, accidentData);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la mise à jour de l'accident #${id}:`, error);
      throw error;
    }
  },
  
  deleteAccident: async (id) => {
    try {
      const response = await api.delete(`/accidents/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la suppression de l'accident #${id}:`, error);
      throw error;
    }
  }
};