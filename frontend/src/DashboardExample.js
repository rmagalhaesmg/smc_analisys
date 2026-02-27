/**
 * Example Dashboard Component
 * Demonstra como usar os hooks e a API do backend
 */

import { useState, useEffect } from "react";
import { useProcessBar, useLastSignal } from "./hooks";
import { systemAPI } from "./api";

function DashboardExample() {
  const { processBar, loading: barLoading, result } = useProcessBar();
  const { fetch: fetchSignal, signal, loading: signalLoading } = useLastSignal("WDOH1");
  const [status, setStatus] = useState(null);
  const [statusLoading, setStatusLoading] = useState(false);

  // Buscar status do sistema
  useEffect(() => {
    const loadStatus = async () => {
      setStatusLoading(true);
      try {
        const response = await systemAPI.getRoot();
        setStatus(response.data);
      } catch (error) {
        console.error("Erro ao carrega status:", error);
      } finally {
        setStatusLoading(false);
      }
    };

    loadStatus();
    // Atualizar a cada 5 segundos
    const interval = setInterval(loadStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  // Carregar último sinal
  useEffect(() => {
    fetchSignal();
    const interval = setInterval(fetchSignal, 10000); // Atualizar a cada 10 segundos
    return () => clearInterval(interval);
  }, [fetchSignal]);

  // Exemplo de processamento de barra
  const handleProcessExampleBar = async () => {
    const exampleBar = {
      open: 105.50,
      high: 106.20,
      low: 105.30,
      close: 106.00,
      volume: 2500000,
      time: "2026-02-27T15:30:00Z",
      symbol: "WDOH1",
    };

    try {
      const result = await processBar(exampleBar);
      console.log("Resultado da análise:", result);
    } catch (error) {
      console.error("Erro ao processar barra:", error);
    }
  };

  // Styled components
  const containerStyle = {
    backgroundColor: "#0f0f1a",
    color: "#ffffff",
    minHeight: "100vh",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  };

  const cardStyle = {
    background: "#1a1a2e",
    borderRadius: "12px",
    padding: "20px",
    border: "1px solid #333",
    marginBottom: "20px",
  };

  const headingStyle = {
    color: "#00d4ff",
    marginTop: 0,
  };

  const statusBadge = (online) => ({
    display: "inline-block",
    padding: "5px 10px",
    borderRadius: "5px",
    backgroundColor: online ? "#00ff88" : "#ff6b6b",
    color: "#000",
    fontWeight: "bold",
    fontSize: "12px",
  });

  const buttonStyle = {
    background: "#00d4ff",
    color: "#000",
    border: "none",
    padding: "10px 20px",
    borderRadius: "5px",
    cursor: "pointer",
    fontWeight: "bold",
    marginRight: "10px",
  };

  const loadingText = "⏳ Carregando...";
  const errorColor = "#ff6b6b";

  return (
    <div style={containerStyle}>
      <h1 style={{ color: "#00d4ff", textAlign: "center" }}>
        🚀 SMC SaaS - Dashboard
      </h1>

      {/* Status do Sistema */}
      <div style={cardStyle}>
        <h2 style={headingStyle}>📊 Status do Sistema</h2>

        {statusLoading ? (
          <p>{loadingText}</p>
        ) : status ? (
          <div>
            <p>
              <strong>App:</strong> {status.app}
              <span style={statusBadge(status.status === "online")}>
                {status.status}
              </span>
            </p>
            <p>
              <strong>Versão:</strong> {status.versao}
            </p>
            <p>
              <strong>Horário do Servidor:</strong> {status.timestamp}
            </p>
            <p>
              <strong>API URL:</strong> {process.env.REACT_APP_API_URL}
            </p>
          </div>
        ) : (
          <p style={{ color: errorColor }}>
            Erro ao carrega status do servidor
          </p>
        )}
      </div>

      {/* Último Sinal */}
      <div style={cardStyle}>
        <h2 style={headingStyle}>📈 Último Sinal</h2>

        {signalLoading ? (
          <p>{loadingText}</p>
        ) : signal ? (
          <div>
            <p>
              <strong>Símbolo:</strong> {signal.symbol || "N/A"}
            </p>
            <p>
              <strong>Score:</strong>{" "}
              <span style={{ color: "#ffd700", fontWeight: "bold" }}>
                {((signal.score || 0) * 100).toFixed(0)}%
              </span>
            </p>
            <p>
              <strong>Direção:</strong>{" "}
              <span style={{ color: signal.direction === 1 ? "#00ff88" : "#ff6b6b" }}>
                {signal.direction === 1 ? "📈 ALTA" : signal.direction === -1 ? "📉 BAIXA" : "➡️ NEUTRA"}
              </span>
            </p>
            <p>
              <strong>Qualidade:</strong> {signal.qualidade || "N/A"}
            </p>
            <p>
              <strong>Horário:</strong> {signal.time || "N/A"}
            </p>
          </div>
        ) : (
          <p style={{ color: errorColor }}>Nenhum sinal disponível ainda</p>
        )}
      </div>

      {/* Processar Barra */}
      <div style={cardStyle}>
        <h2 style={headingStyle}>🔧 Testar Processamento de Barra</h2>
        <p>
          Clique no botão abaixo para enviar uma barra de exemplo para o backend
          processar:
        </p>

        <button
          style={buttonStyle}
          onClick={handleProcessExampleBar}
          disabled={barLoading}
        >
          {barLoading ? "⏳ Processando..." : "🚀 Processar Barra"}
        </button>

        {result && (
          <div
            style={{
              background: "#0f0f1a",
              padding: "15px",
              borderRadius: "8px",
              marginTop: "15px",
              borderLeft: "4px solid #00d4ff",
            }}
          >
            <h3 style={{ margin: "0 0 10px 0", color: "#00d4ff" }}>
              ✅ Resultado da Análise
            </h3>
            <pre
              style={{
                overflow: "auto",
                color: "#00ff88",
                fontSize: "12px",
                margin: 0,
              }}
            >
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>

      {/* Informações de Teste */}
      <div style={cardStyle}>
        <h2 style={headingStyle}>ℹ️ Informações de Teste</h2>
        <p>
          <strong>Frontend Origin:</strong> {window.location.origin}
        </p>
        <p>
          <strong>Backend URL:</strong> {process.env.REACT_APP_API_URL}
        </p>
        <p>
          <strong>Token no localStorage:</strong>{" "}
          {localStorage.getItem("access_token") ? "✅ Existe" : "❌ Não existe"}
        </p>
        <p>
          <strong>React Version:</strong> {require("react").version}
        </p>

        <details>
          <summary style={{ cursor: "pointer", color: "#00d4ff" }}>
            📋 Ver Todas as Variáveis de Ambiente
          </summary>
          <pre
            style={{
              background: "#0f0f1a",
              padding: "10px",
              borderRadius: "5px",
              overflow: "auto",
              marginTop: "10px",
            }}
          >
            {Object.entries(process.env)
              .filter(([key]) => key.startsWith("REACT_APP_"))
              .map(([key, value]) => `${key}=${value}`)
              .join("\n")}
          </pre>
        </details>
      </div>

      {/* Próximos Passos */}
      <div style={cardStyle}>
        <h2 style={headingStyle}>🎯 Próximos Passos</h2>
        <ol>
          <li>
            Verificar se o backend está rodando em{" "}
            <code
              style={{
                background: "#0f0f1a",
                padding: "2px 6px",
                borderRadius: "3px",
              }}
            >
              http://127.0.0.1:8000
            </code>
          </li>
          <li>
            Acessar a documentação interativa:{" "}
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: "#00d4ff" }}
            >
              /docs
            </a>
          </li>
          <li>Integrar os hooks (`useProcessBar`, `useLastSignal`, etc) nos componentes reais</li>
          <li>Implementar autenticação com `useLogin` e `useRegister`</li>
          <li>Adicionar loading states e error handling</li>
        </ol>
      </div>
    </div>
  );
}

export default DashboardExample;
