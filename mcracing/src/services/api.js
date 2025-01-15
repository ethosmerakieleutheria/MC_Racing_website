// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const raceAPI = {
  get_all_races: () => api.get('/races'),
  getRaceById: (id) => api.get(`/races/${id}`),
  registerForRace: (raceId, userData) => api.post(`/races/${raceId}/register`, userData),
  createPaymentIntent: (raceId) => api.post(`/payment/create-intent`, { raceId }),
};

export const trainingAPI = {
  getPrograms: () => api.get('/training/slots'), // Ensure this matches your FastAPI route
  registerForTraining: (slotId, userData) =>
    api.post('/training/register', { slotId, ...userData }),
};


export const leaderboardAPI = {
  getLeaderboard: () => api.get('/leaderboard/top'),
};

export const contactAPI = {
  sendMessage: (messageData) => api.post('/contact', messageData),
};

export default api;