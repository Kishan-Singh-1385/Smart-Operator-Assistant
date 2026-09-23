import axios from 'axios';

const API_URL = 'http://localhost:8001/api';

const api = axios.create({
  baseURL: API_URL,
});

export const getOperators = () => api.get('/operators/');
export const getOperator = (id) => api.get(`/operators/${id}`);

export const getMachines = () => api.get('/machines/');
export const getMachine = (id) => api.get(`/machines/${id}`);

export const getTasks = () => api.get('/tasks/');
export const getTask = (id) => api.get(`/tasks/${id}`);

export const getTelemetry = (machineId) => api.get(`/telemetry/${machineId}`);

export default api;
