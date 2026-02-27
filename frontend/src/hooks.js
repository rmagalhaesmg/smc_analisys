/**
 * Custom React Hooks for API calls with loading/error states
 */

import { useState, useCallback } from "react";
import { tradingAPI, authAPI, aiAPI, paymentAPI } from "./api";

/**
 * Generic hook for API calls with loading, error, and data states
 * Usage: const { data, loading, error, execute } = useApi();
 */
export const useApi = (apiFunction) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(
    async (...args) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiFunction(...args);
        setData(response.data);
        return response.data;
      } catch (err) {
        const errorMessage =
          err.response?.data?.message || err.message || "Erro desconhecido";
        setError(errorMessage);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [apiFunction]
  );

  return { data, loading, error, execute, setData };
};

// ==================== Auth Hooks ====================
export const useLogin = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const login = useCallback(async (username, password) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authAPI.login(username, password);
      localStorage.setItem("access_token", response.data.access_token);
      return response.data;
    } catch (err) {
      const errorMessage =
        err.response?.data?.message || "Falha no login";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { login, loading, error };
};

export const useRegister = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const register = useCallback(async (data) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authAPI.register(data);
      return response.data;
    } catch (err) {
      const errorMessage =
        err.response?.data?.message || "Falha no registro";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { register, loading, error };
};

// ==================== Trading Hooks ====================
export const useProcessBar = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const processBar = useCallback(async (bar) => {
    setLoading(true);
    setError(null);
    try {
      const response = await tradingAPI.processBar(bar);
      setResult(response.data);
      return response.data;
    } catch (err) {
      const errorMessage =
        err.response?.data?.message || "Erro ao processar barra";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { processBar, loading, error, result };
};

export const useLastSignal = (symbol) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [signal, setSignal] = useState(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await tradingAPI.getLastSignal(symbol);
      setSignal(response.data);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.message || "Erro ao buscar sinal");
      throw err;
    } finally {
      setLoading(false);
    }
  }, [symbol]);

  return { fetch, loading, error, signal };
};

// ==================== AI Hooks ====================
export const useAIInterpret = (symbol) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [interpretation, setInterpretation] = useState(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await aiAPI.interpret(symbol);
      setInterpretation(response.data);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.message || "Erro na interpretação da IA");
      throw err;
    } finally {
      setLoading(false);
    }
  }, [symbol]);

  return { fetch, loading, error, interpretation };
};

// ==================== Payment Hooks ====================
export const usePaymentPlans = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [plans, setPlans] = useState([]);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await paymentAPI.getPlans();
      setPlans(response.data);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.message || "Erro ao buscar planos");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { fetch, loading, error, plans };
};

export const useCheckout = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const checkout = useCallback(async (planId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await paymentAPI.checkout(planId);
      return response.data;
    } catch (err) {
      const errorMessage =
        err.response?.data?.message || "Erro no checkout";
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { checkout, loading, error };
};
