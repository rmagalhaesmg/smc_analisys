/**
 * Trading Component
 * Análise de barras OHLCV em tempo real
 */

import { useState } from "react";
import { useProcessBar } from "../hooks";

function TradingComponent() {
  const { processBar, loading, error, result } = useProcessBar();
  const [symbol, setSymbol] = useState("WDOH1");
  const [barData, setBarData] = useState({
    open: 105.5,
    high: 106.2,
    low: 105.3,
    close: 106.0,
    volume: 2500000,
  });

  const handleInputChange = (field, value) => {
    setBarData((prev) => ({
      ...prev,
      [field]: isNaN(value) ? value : parseFloat(value),
    }));
  };

  const handleProcessBar = async () => {
    const bar = {
      ...barData,
      symbol,
      time: new Date().toISOString(),
    };

    try {
      const analysis = await processBar(bar);
      console.log("✅ Análise Completa:", analysis);
    } catch (err) {
      console.error("❌ Erro na análise:", error);
    }
  };

  const containerStyle = {
    background: "#1a1a2e",
    borderRadius: "12px",
    padding: "20px",
    border: "1px solid #333",
    color: "#fff",
    maxWidth: "600px",
    margin: "20px auto",
  };

  const gridStyle = {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "15px",
    marginBottom: "20px",
  };

  const inputStyle = {
    padding: "10px",
    background: "#0f0f1a",
    border: "1px solid #333",
    borderRadius: "5px",
    color: "#fff",
    width: "100%",
    boxSizing: "border-box",
  };

  const buttonStyle = {
    padding: "12px 24px",
    background: "#00d4ff",
    color: "#000",
    border: "none",
    borderRadius: "5px",
    fontWeight: "bold",
    cursor: "pointer",
    fontSize: "14px",
  };

  const resultCardStyle = {
    background: "#0f0f1a",
    padding: "15px",
    borderRadius: "8px",
    borderLeft: "4px solid #00d4ff",
    marginTop: "20px",
  };

  const scoreStyle = {
    fontSize: "24px",
    fontWeight: "bold",
    color: result?.score > 0.7 ? "#00ff88" : result?.score > 0.5 ? "#ffd700" : "#ff6b6b",
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ color: "#00d4ff", margin: "0 0 20px 0" }}>📈 Análise de Barra</h2>

      {/* Symbol */}
      <div style={{ marginBottom: "15px" }}>
        <label style={{ display: "block", marginBottom: "5px", color: "#888" }}>
          Símbolo:
        </label>
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          placeholder="WDOH1"
          style={inputStyle}
        />
      </div>

      {/* OHLCV Inputs */}
      <div style={gridStyle}>
        <div>
          <label style={{ display: "block", marginBottom: "5px", color: "#888" }}>Open:</label>
          <input
            type="number"
            value={barData.open}
            onChange={(e) => handleInputChange("open", e.target.value)}
            step="0.01"
            style={inputStyle}
          />
        </div>
        <div>
          <label style={{ display: "block", marginBottom: "5px", color: "#888" }}>High:</label>
          <input
            type="number"
            value={barData.high}
            onChange={(e) => handleInputChange("high", e.target.value)}
            step="0.01"
            style={inputStyle}
          />
        </div>
        <div>
          <label style={{ display: "block", marginBottom: "5px", color: "#888" }}>Low:</label>
          <input
            type="number"
            value={barData.low}
            onChange={(e) => handleInputChange("low", e.target.value)}
            step="0.01"
            style={inputStyle}
          />
        </div>
        <div>
          <label style={{ display: "block", marginBottom: "5px", color: "#888" }}>Close:</label>
          <input
            type="number"
            value={barData.close}
            onChange={(e) => handleInputChange("close", e.target.value)}
            step="0.01"
            style={inputStyle}
          />
        </div>
        <div style={{ gridColumn: "1 / -1" }}>
          <label style={{ display: "block", marginBottom: "5px", color: "#888" }}>Volume:</label>
          <input
            type="number"
            value={barData.volume}
            onChange={(e) => handleInputChange("volume", e.target.value)}
            style={inputStyle}
          />
        </div>
      </div>

      {/* Error */}
      {error && (
        <p style={{ color: "#ff6b6b", marginBottom: "10px" }}>❌ {error}</p>
      )}

      {/* Process Button */}
      <button onClick={handleProcessBar} style={buttonStyle} disabled={loading}>
        {loading ? "⏳ Processando..." : "🚀 Processar Barra"}
      </button>

      {/* Result */}
      {result && (
        <div style={resultCardStyle}>
          <h3 style={{ margin: "0 0 15px 0", color: "#00d4ff" }}>
            ✅ Resultado da Análise
          </h3>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "15px" }}>
            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Score</p>
              <p style={{ ...scoreStyle, margin: "5px 0 0 0" }}>
                {((result.score || 0) * 100).toFixed(0)}%
              </p>
            </div>

            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Direção</p>
              <p style={{ fontSize: "20px", margin: "5px 0 0 0" }}>
                {result.direction === 1 ? "📈 ALTA" : result.direction === -1 ? "📉 BAIXA" : "➡️ NEUTRA"}
              </p>
            </div>

            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>HFZ</p>
              <p style={{ color: "#00d4ff", margin: "5px 0 0 0" }}>
                {result.hfz?.score?.toFixed(0) || "N/A"}
              </p>
            </div>

            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>FBI</p>
              <p style={{ color: "#ffd700", margin: "5px 0 0 0" }}>
                {result.fbi?.score?.toFixed(0) || "N/A"}
              </p>
            </div>

            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>DTM</p>
              <p style={{ color: "#ff6b6b", margin: "5px 0 0 0" }}>
                {result.dtm?.score?.toFixed(0) || "N/A"}
              </p>
            </div>

            <div>
              <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Qualidade</p>
              <p style={{ color: "#00ff88", margin: "5px 0 0 0" }}>
                {result.qualidade || "N/A"}
              </p>
            </div>
          </div>

          <details style={{ marginTop: "15px" }}>
            <summary style={{ cursor: "pointer", color: "#00d4ff" }}>
              📋 Ver dados completos
            </summary>
            <pre
              style={{
                background: "#0f0f1a",
                padding: "10px",
                borderRadius: "5px",
                overflow: "auto",
                marginTop: "10px",
                fontSize: "11px",
                color: "#00ff88",
              }}
            >
              {JSON.stringify(result, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

export default TradingComponent;
