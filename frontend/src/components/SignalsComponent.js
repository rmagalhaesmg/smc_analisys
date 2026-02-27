/**
 * Signals Component
 * Monitora sinais em tempo real
 */

import { useState, useEffect } from "react";
import { useLastSignal } from "../hooks";

function SignalsComponent() {
  const [symbols] = useState(["WDOH1", "WDOM1", "WINM26"]);
  const [activeSymbol, setActiveSymbol] = useState("WDOH1");
  const [allSignals, setAllSignals] = useState({});
  const { fetch, signal, loading, error } = useLastSignal(activeSymbol);

  // Carregar sinal quando mudar símbolo
  useEffect(() => {
    fetch();
    const interval = setInterval(fetch, 10000); // Atualizar a cada 10 segundos
    return () => clearInterval(interval);
  }, [activeSymbol, fetch]);

  // Armazenar sinais
  useEffect(() => {
    if (signal) {
      setAllSignals((prev) => ({
        ...prev,
        [activeSymbol]: signal,
      }));
    }
  }, [signal, activeSymbol]);

  const containerStyle = {
    background: "#1a1a2e",
    borderRadius: "12px",
    padding: "20px",
    border: "1px solid #333",
    color: "#fff",
    maxWidth: "600px",
    margin: "20px auto",
  };

  const tabsStyle = {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
    flexWrap: "wrap",
  };

  const tabButtonStyle = (isActive) => ({
    padding: "10px 16px",
    background: isActive ? "#00d4ff" : "#0f0f1a",
    color: isActive ? "#000" : "#fff",
    border: "1px solid #333",
    borderRadius: "5px",
    cursor: "pointer",
    fontWeight: isActive ? "bold" : "normal",
  });

  const signalCardStyle = {
    background: "#0f0f1a",
    padding: "15px",
    borderRadius: "8px",
    borderLeft: "4px solid #00d4ff",
    marginTop: "20px",
  };

  const scoreBarStyle = {
    width: "100%",
    height: "30px",
    background: "#333",
    borderRadius: "5px",
    overflow: "hidden",
    marginTop: "10px",
  };

  const getScoreColor = (score) => {
    if (score > 0.75) return "#00ff88";
    if (score > 0.6) return "#ffd700";
    if (score > 0.4) return "#ff9d00";
    return "#ff6b6b";
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ color: "#00d4ff", margin: "0 0 20px 0" }}>📊 Sinais em Tempo Real</h2>

      {/* Symbol Tabs */}
      <div style={tabsStyle}>
        {symbols.map((sym) => (
          <button
            key={sym}
            onClick={() => setActiveSymbol(sym)}
            style={tabButtonStyle(activeSymbol === sym)}
          >
            {sym}
          </button>
        ))}
      </div>

      {/* Loading/Error */}
      {loading && <p style={{ color: "#888" }}>⏳ Carregando sinal de {activeSymbol}...</p>}
      {error && <p style={{ color: "#ff6b6b" }}>❌ {error}</p>}

      {/* Signal Display */}
      {signal && (
        <div style={signalCardStyle}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "15px" }}>
            {/* Score */}
            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Score</p>
              <p
                style={{
                  fontSize: "28px",
                  fontWeight: "bold",
                  margin: "5px 0 0 0",
                  color: getScoreColor(signal.score || 0),
                }}
              >
                {((signal.score || 0) * 100).toFixed(0)}%
              </p>
              <div style={scoreBarStyle}>
                <div
                  style={{
                    width: `${(signal.score || 0) * 100}%`,
                    height: "100%",
                    background: getScoreColor(signal.score || 0),
                    transition: "width 0.3s ease",
                  }}
                />
              </div>
            </div>

            {/* Direction */}
            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Direção</p>
              <p style={{ fontSize: "28px", margin: "5px 0 0 0" }}>
                {signal.direction === 1
                  ? "📈 ALTA"
                  : signal.direction === -1
                  ? "📉 BAIXA"
                  : "➡️ NEUTRA"}
              </p>
            </div>

            {/* Quality */}
            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Qualidade</p>
              <p style={{ fontSize: "20px", margin: "5px 0 0 0", color: "#ffd700" }}>
                {signal.qualidade || "N/A"}⭐
              </p>
            </div>

            {/* Time */}
            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Horário</p>
              <p style={{ fontSize: "14px", margin: "5px 0 0 0", color: "#00d4ff" }}>
                {signal.time ? new Date(signal.time).toLocaleTimeString("pt-BR") : "N/A"}
              </p>
            </div>
          </div>

          {/* Modules Score */}
          <div style={{ marginTop: "20px", paddingTop: "20px", borderTop: "1px solid #333" }}>
            <p style={{ margin: "0 0 10px 0", color: "#888", fontSize: "12px" }}>
              📊 Scores dos Módulos
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "10px" }}>
              <div style={{ background: "#0f0f1a", padding: "10px", borderRadius: "5px" }}>
                <p style={{ margin: "0", color: "#888", fontSize: "11px" }}>HFZ</p>
                <p style={{ fontSize: "16px", margin: "5px 0 0 0", color: "#00ff88" }}>
                  {signal.hfz?.score?.toFixed(0) || "—"}
                </p>
              </div>
              <div style={{ background: "#0f0f1a", padding: "10px", borderRadius: "5px" }}>
                <p style={{ margin: "0", color: "#888", fontSize: "11px" }}>FBI</p>
                <p style={{ fontSize: "16px", margin: "5px 0 0 0", color: "#ffd700" }}>
                  {signal.fbi?.score?.toFixed(0) || "—"}
                </p>
              </div>
              <div style={{ background: "#0f0f1a", padding: "10px", borderRadius: "5px" }}>
                <p style={{ margin: "0", color: "#888", fontSize: "11px" }}>DTM</p>
                <p style={{ fontSize: "16px", margin: "5px 0 0 0", color: "#ff6b6b" }}>
                  {signal.dtm?.score?.toFixed(0) || "—"}
                </p>
              </div>
              <div style={{ background: "#0f0f1a", padding: "10px", borderRadius: "5px" }}>
                <p style={{ margin: "0", color: "#888", fontSize: "11px" }}>SDA</p>
                <p style={{ fontSize: "16px", margin: "5px 0 0 0", color: "#00d4ff" }}>
                  {signal.sda?.score?.toFixed(0) || "—"}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Summary */}
      {Object.keys(allSignals).length > 0 && (
        <div style={{ marginTop: "20px", paddingTop: "20px", borderTop: "1px solid #333" }}>
          <p style={{ margin: "0 0 10px 0", color: "#888", fontSize: "12px" }}>
            📈 Resumo de Todos os Sinais
          </p>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "10px" }}>
            {Object.entries(allSignals).map(([sym, sig]) => (
              <div
                key={sym}
                onClick={() => setActiveSymbol(sym)}
                style={{
                  background: activeSymbol === sym ? "#0f0f1a" : "transparent",
                  padding: "10px",
                  borderRadius: "5px",
                  cursor: "pointer",
                  borderLeft: `4px solid ${getScoreColor(sig.score || 0)}`,
                }}
              >
                <p style={{ margin: "0", fontWeight: "bold", color: "#fff" }}>{sym}</p>
                <p style={{ margin: "5px 0 0 0", color: getScoreColor(sig.score || 0) }}>
                  {((sig.score || 0) * 100).toFixed(0)}%
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default SignalsComponent;
