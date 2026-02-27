/**
 * TEMPLATE: Componente Básico Reutilizável
 * 
 * Use este arquivo como base para criar novos componentes
 * Copie, renomeie e customize!
 */

import { useState } from "react";
import { useProcessBar } from "../hooks"; // Importe os hooks que precisa

/**
 * MyComponent
 * @description Descrição do que seu componente faz
 * @example
 * <MyComponent symbol="WDOH1" />
 */
function MyComponent({ symbol = "WDOH1" }) {
  // ==================== STATE ====================
  const [value, setValue] = useState("");
  
  // Hooks
  const { processBar, loading, error, result } = useProcessBar();

  // ==================== HANDLERS ====================
  const handleAction = async () => {
    try {
      // Fazer algo aqui
      console.log("Ação executada!");
    } catch (err) {
      console.error("Erro:", err);
    }
  };

  // ==================== STYLES ====================
  const containerStyle = {
    background: "#1a1a2e",
    borderRadius: "12px",
    padding: "20px",
    border: "1px solid #333",
    color: "#fff",
    maxWidth: "600px",
    margin: "20px auto",
  };

  const headingStyle = {
    color: "#00d4ff",
    margin: "0 0 20px 0",
  };

  const inputStyle = {
    padding: "10px",
    background: "#0f0f1a",
    border: "1px solid #333",
    borderRadius: "5px",
    color: "#fff",
    width: "100%",
    boxSizing: "border-box",
    marginBottom: "10px",
  };

  const buttonStyle = {
    padding: "12px 24px",
    background: "#00d4ff",
    color: "#000",
    border: "none",
    borderRadius: "5px",
    fontWeight: "bold",
    cursor: "pointer",
    marginRight: "10px",
  };

  const alertStyle = {
    padding: "10px",
    borderRadius: "5px",
    marginTop: "10px",
  };

  // ==================== RENDER ====================
  return (
    <div style={containerStyle}>
      <h2 style={headingStyle}>🚀 Meu Componente</h2>

      {/* Inputs */}
      <div>
        <label style={{ display: "block", marginBottom: "5px", color: "#888" }}>
          Digite algo:
        </label>
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Digite aqui..."
          style={inputStyle}
        />
      </div>

      {/* Loading */}
      {loading && (
        <p style={{ ...alertStyle, background: "#0f0f1a", color: "#888" }}>
          ⏳ Carregando...
        </p>
      )}

      {/* Error */}
      {error && (
        <p style={{ ...alertStyle, background: "#ff6b6b", color: "#fff" }}>
          ❌ {error}
        </p>
      )}

      {/* Success */}
      {result && (
        <p style={{ ...alertStyle, background: "#00ff88", color: "#000" }}>
          ✅ Sucesso! Score: {((result.score || 0) * 100).toFixed(0)}%
        </p>
      )}

      {/* Button */}
      <button
        style={buttonStyle}
        onClick={handleAction}
        disabled={loading}
      >
        {loading ? "⏳ Processando..." : "🚀 Executar"}
      </button>
    </div>
  );
}

export default MyComponent;
