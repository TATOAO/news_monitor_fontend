// API Configuration
export const API_CONFIG = {
  // Base URL for the API
  BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1',
  
  // Endpoints
  ENDPOINTS: {
    NEWS: '/news',
    MARKET: '/market',
    HEALTH: '/api/health',
    VERSION: '/api/version',
  },
  
  // API request configuration
  REQUEST_CONFIG: {
    headers: {
      'Content-Type': 'application/json',
    },
    timeout: 10000, // 10 seconds
  },
};

// Feature flags
export const FEATURES = {
  USE_REAL_API: process.env.REACT_APP_USE_REAL_API === 'true',
  USE_MOCK_DATA: process.env.REACT_APP_USE_MOCK_DATA === 'true',
}; 