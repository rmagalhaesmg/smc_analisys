import axios from "axios";

// URL da API - configure via variável de ambiente ou use localhost
const API_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para adicionar token JWT
api.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// Funções de API reutilizáveis
export const auth = {
  login: async (email: string, password: string) => {
    const response = await api.post("/auth/login", { email, password });
    if (response.data.access_token) {
      localStorage.setItem("token", response.data.access_token);
    }
    return response.data;
  },
  register: async (email: string, password: string, name: string) => {
    const response = await api.post("/auth/register", { email, password, name });
    return response.data;
  },
  logout: () => {
    localStorage.removeItem("token");
  },
};

export const data = {
  uploadCsv: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await api.post("/data/upload-csv", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  },
  getSources: async () => {
    const response = await api.get("/data/sources");
    return response.data;
  },
};

export const signals = {
  getAll: async () => {
    const response = await api.get("/signals");
    return response.data;
  },
  getById: async (id: string) => {
    const response = await api.get(`/signals/${id}`);
    return response.data;
  },
};

export const analysis = {
  run: async (params: any) => {
    const response = await api.post("/analysis/run", params);
    return response.data;
  },
  getHistory: async () => {
    const response = await api.get("/analysis/history");
    return response.data;
  },
};

export const alerts = {
  getConfig: async () => {
    const response = await api.get("/alerts/config");
    return response.data;
  },
  saveConfig: async (config: any) => {
    const response = await api.post("/alerts/config", config);
    return response.data;
  },
};

export const billing = {
  getPlans: async () => {
    const response = await api.get("/billing/plans");
    return response.data;
  },
  getSubscription: async () => {
    const response = await api.get("/billing/subscription");
    return response.data;
  },
};
