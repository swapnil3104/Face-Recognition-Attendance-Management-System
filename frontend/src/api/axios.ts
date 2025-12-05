import axios from 'axios';

export const backendApi = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const faceApi = axios.create({
  baseURL: 'http://localhost:9001',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add interceptor to include token in backend requests
backendApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
