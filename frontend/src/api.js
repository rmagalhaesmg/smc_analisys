/**
 * API Configuration
 * Centralized API client for all backend requests
 */

import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
const API_TIMEOUT = parseInt(process.env.REACT_APP_API_TIMEOUT || "30000", 10);

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// ==================== Auth API ====================
export const authAPI = {
  register: (data) => apiClient.post("/auth/register", data),
  login: (username, password) =>
    apiClient.post("/auth/login", { username, password }),
  refresh: () => apiClient.post("/auth/refresh"),
  verifyEmail: (token) => apiClient.get(`/auth/verify-email?token=${token}`),
  forgotPassword: (email) => apiClient.post("/auth/forgot-password", { email }),
  resetPassword: (token, password) =>
    apiClient.post("/auth/reset-password", { token, password }),
  getProfile: () => apiClient.get("/auth/me"),
};

// ==================== Trading API ====================
export const tradingAPI = {
  processBar: (bar) => apiClient.post("/api/processar-barra", bar),
  getLastSignal: (symbol) => apiClient.get(`/api/ultimo-sinal/${symbol}`),
};

// ==================== Alerts API ====================
export const alertsAPI = {
  getLog: () => apiClient.get("/api/alertas/log"),
  getStats: () => apiClient.get("/api/alertas/stats"),
};

// ==================== AI API ====================
export const aiAPI = {
  interpret: (symbol) => apiClient.get(`/api/ai/interpretar/${symbol}`),
  chat: (message) => apiClient.post("/api/ai/chat", { message }),
  getReport: (symbol) => apiClient.get(`/api/ai/relatorio/${symbol}`),
};

// ==================== Payment API ====================
export const paymentAPI = {
  getPlans: () => apiClient.get("/api/planos"),
  checkout: (planId) => apiClient.post("/api/pagamento/checkout", { plan_id: planId }),
  getPaymentStatus: () => apiClient.get("/api/pagamento/status"),
  getPaymentHistory: () => apiClient.get("/api/pagamento/historico"),
  cancelPayment: (paymentId) =>
    apiClient.post("/api/pagamento/cancelar", { payment_id: paymentId }),
};

// ==================== System API ====================
export const systemAPI = {
  getStatus: () => apiClient.get("/api/status"),
  getRoot: () => apiClient.get("/"),
};

export default apiClient;
