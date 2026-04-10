import axios from 'axios';


const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5001/api';


const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});



export const getDeployments = async (type = null, limit = 50) => {
  try {
    const params = { limit };
    if (type) params.type = type;
    
    const response = await api.get('/deployments', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching deployments:', error);
    throw error;
  }
};


export const getDeployment = async (id) => {
  try {
    const response = await api.get(`/deployments/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching deployment:', error);
    throw error;
  }
};



export const createDeployment = async (deploymentData) => {
  try {
    const response = await api.post('/deployments', deploymentData);
    return response.data;
  } catch (error) {
    console.error('Error creating deployment:', error);
    throw error;
  }
};

export const getStatistics = async () => {
  try {
    const response = await api.get('/statistics');
    return response.data;
  } catch (error) {
    console.error('Error fetching statistics:', error);
    throw error;
  }
};


export const getSummary = async () => {
  try {
    const response = await api.get('/statistics/summary');
    return response.data;
  } catch (error) {
    console.error('Error fetching summary:', error);
    throw error;
  }
};


export const getFullAnalysis = async () => {
  try {
    const response = await api.get('/analysis/full');
    return response.data;
  } catch (error) {
    console.error('Error fetching analysis:', error);
    throw error;
  }
};



export const simulateManualDeployment = async () => {
  try {
    const response = await api.post('/simulate/manual');
    return response.data;
  } catch (error) {
    console.error('Error simulating deployment:', error);
    throw error;
  }
};
export const simulateBatchDeployments = async (count = 10, spreadDays = 30) => {
  try {
    const response = await api.post('/simulate/manual/batch', {
      count,
      spread_days: spreadDays,
    });
    return response.data;
  } catch (error) {
    console.error('Error simulating batch deployments:', error);
    throw error;
  }
};
export const getSimulationSummary = async () => {
  try {
    const response = await api.get('/simulate/summary');
    return response.data;
  } catch (error) {
    console.error('Error fetching simulation summary:', error);
    throw error;
  }
};


export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking API health:', error);
    throw error;
  }
};