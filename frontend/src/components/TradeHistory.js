/**
 * Trade History Component
 * Componente para exibir histórico de análises e trades
 */

import { useState, useEffect } from "react";
import { tradingAPI } from "../api";

function TradeHistory() {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all"); // all, hfz, fbi, dtm
  const [sortBy, setSortBy] = useState("recent"); // recent, score, symbol

  useEffect(() => {
    loadTrades();
    // Auto-refresh a cada 30 segundos
    const interval = setInterval(loadTrades, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadTrades = async () => {
    try {
      setLoading(true);
      // Tenta chamar API real, se não existir, usa dados vazios
      let trades = [];
      try {
        const response = await tradingAPI.getHistory?.();
        trades = response?.data?.trades || [];
      } catch (apiError) {
        // Fallback: dados vazios quando API não está disponível
        console.log('getHistory não implementado, usando array vazio');
        trades = [];
      }
      setTrades(trades);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "#00ff88";
    if (score >= 60) return "#00d4ff";
    if (score >= 40) return "#ffd700";
    return "#ff6b6b";
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return "🟢 Excelente";
    if (score >= 60) return "🔵 Bom";
    if (score >= 40) return "🟡 Moderado";
    return "🔴 Baixo";
  };

  const filteredTrades = trades.filter((trade) => {
    if (filter === "all") return true;
    return trade.analysis_type?.toLowerCase() === filter.toLowerCase();
  });

  const sortedTrades = [...filteredTrades].sort((a, b) => {
    if (sortBy === "recent")
      return new Date(b.timestamp) - new Date(a.timestamp);
    if (sortBy === "score") return (b.score || 0) - (a.score || 0);
    if (sortBy === "symbol") return (a.symbol || "").localeCompare(b.symbol);
    return 0;
  });

  const containerStyle = {
    background: "#1a1a2e",
    borderRadius: "12px",
    padding: "20px",
    border: "1px solid #333",
    color: "#fff",
    margin: "20px",
  };

  const headerStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "20px",
    flexWrap: "wrap",
    gap: "10px",
  };

  const filterButtonStyle = (isActive) => ({
    padding: "8px 16px",
    background: isActive ? "#00d4ff" : "#333",
    color: isActive ? "#000" : "#fff",
    border: "none",
    borderRadius: "5px",
    fontWeight: isActive ? "bold" : "normal",
    cursor: "pointer",
  });

  const selectStyle = {
    padding: "8px 12px",
    background: "#0f0f1a",
    border: "1px solid #333",
    borderRadius: "5px",
    color: "#fff",
  };

  const tableStyle = {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: "20px",
  };

  const cellStyle = {
    padding: "12px",
    borderBottom: "1px solid #333",
    textAlign: "left",
  };

  const headerCellStyle = {
    ...cellStyle,
    background: "#0f0f1a",
    fontWeight: "bold",
    color: "#00d4ff",
  };

  const scoreBarStyle = (score) => ({
    width: "100%",
    height: "20px",
    background: "#333",
    borderRadius: "3px",
    overflow: "hidden",
    position: "relative",
  });

  const scoreBarFillStyle = (score) => ({
    width: `${Math.min(score || 0, 100)}%`,
    height: "100%",
    background: getScoreColor(score),
    transition: "width 0.3s ease",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "10px",
    fontWeight: "bold",
    color: "#000",
  });

  if (loading && trades.length === 0) {
    return (
      <div style={containerStyle}>
        <h2 style={{ color: "#00d4ff", margin: "0 0 20px 0" }}>
          📊 Histórico de Trades
        </h2>
        <p style={{ color: "#888" }}>⏳ Carregando dados...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={containerStyle}>
        <h2 style={{ color: "#00d4ff", margin: "0 0 20px 0" }}>
          📊 Histórico de Trades
        </h2>
        <p style={{ color: "#ff6b6b" }}>❌ Erro: {error}</p>
        <button
          onClick={loadTrades}
          style={{
            padding: "10px 20px",
            background: "#00d4ff",
            color: "#000",
            border: "none",
            borderRadius: "5px",
            fontWeight: "bold",
            cursor: "pointer",
          }}
        >
          Tentar novamente
        </button>
      </div>
    );
  }

  return (
    <div style={containerStyle}>
      <h2 style={{ color: "#00d4ff", margin: "0 0 20px 0" }}>
        📊 Histórico de Trades
      </h2>

      {/* Filtros e Controles */}
      <div style={headerStyle}>
        <div style={{ display: "flex", gap: "10px" }}>
          {["all", "hfz", "fbi", "dtm"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={filterButtonStyle(filter === f)}
            >
              {f === "all" ? "Todos" : f.toUpperCase()}
            </button>
          ))}
        </div>

        <div style={{ display: "flex", gap: "10px" }}>
          <label style={{ color: "#888" }}>
            Ordenar por:
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              style={{
                ...selectStyle,
                marginLeft: "8px",
              }}
            >
              <option value="recent">Mais recente</option>
              <option value="score">Maior score</option>
              <option value="symbol">Símbolo</option>
            </select>
          </label>
        </div>

        <button
          onClick={loadTrades}
          style={{
            padding: "8px 16px",
            background: "#0f4c75",
            color: "#00d4ff",
            border: "1px solid #00d4ff",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          🔄 Atualizar
        </button>
      </div>

      {/* Tabela */}
      {sortedTrades.length === 0 ? (
        <p style={{ color: "#888", marginTop: "20px", textAlign: "center" }}>
          Nenhum trade encontrado para os filtros selecionados.
        </p>
      ) : (
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={headerCellStyle}>Data/Hora</th>
              <th style={headerCellStyle}>Símbolo</th>
              <th style={headerCellStyle}>Tipo</th>
              <th style={headerCellStyle}>Score</th>
              <th style={headerCellStyle}>Estado</th>
            </tr>
          </thead>
          <tbody>
            {sortedTrades.slice(0, 20).map((trade, idx) => (
              <tr
                key={idx}
                style={{
                  background: idx % 2 === 0 ? "#1a1a2e" : "#0f0f1a",
                }}
              >
                <td style={cellStyle}>
                  {new Date(trade.timestamp || Date.now()).toLocaleString()}
                </td>
                <td style={cellStyle}>
                  <strong>{trade.symbol || "N/A"}</strong>
                </td>
                <td style={cellStyle}>
                  <span
                    style={{
                      background: "#0f4c75",
                      padding: "4px 8px",
                      borderRadius: "3px",
                      fontSize: "12px",
                    }}
                  >
                    {trade.analysis_type || "N/A"}
                  </span>
                </td>
                <td style={cellStyle}>
                  <div style={scoreBarStyle(trade.score)}>
                    <div style={scoreBarFillStyle(trade.score)}>
                      {trade.score ? `${Math.round(trade.score)}%` : "N/A"}
                    </div>
                  </div>
                </td>
                <td style={cellStyle}>
                  <span style={{ color: getScoreColor(trade.score || 0) }}>
                    {getScoreLabel(trade.score || 0)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Rodapé */}
      <p style={{ color: "#888", fontSize: "12px", marginTop: "20px" }}>
        ℹ️ Exibindo últimos {Math.min(sortedTrades.length, 20)} de{" "}
        {sortedTrades.length} trades. Auto-atualiza a cada 30 segundos.
      </p>
    </div>
  );
}

export default TradeHistory;
