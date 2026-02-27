/**
 * AIChat Component
 * Componente de chat com integração de IA
 */

import { useState } from "react";
import { aiAPI } from "../api";

function AIChat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Olá! Como posso ajudá-lo com análise de trading? 📊",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    // Adicionar mensagem do usuário
    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      // Enviar para API
      const response = await aiAPI.chat(input);

      // Adicionar resposta da IA
      const assistantMessage = {
        role: "assistant",
        content:
          response.data?.response ||
          response.data?.message ||
          "Desculpe, não consegui processar sua pergunta.",
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      // Erro
      const errorMessage = {
        role: "assistant",
        content: `❌ Erro ao processar sua pergunta: ${error.message}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
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
    height: "600px",
    display: "flex",
    flexDirection: "column",
  };

  const messagesContainerStyle = {
    flex: 1,
    overflowY: "auto",
    marginBottom: "20px",
    paddingRight: "10px",
  };

  const messageStyle = (role) => ({
    margin: "10px 0",
    padding: "12px 15px",
    borderRadius: "8px",
    background:
      role === "user"
        ? "#0f4c75" // Azul escuro para usuário
        : "#2a2a3e", // Cinza escuro para IA
    color: "#fff",
    textAlign: role === "user" ? "right" : "left",
    alignSelf: role === "user" ? "flex-end" : "flex-start",
    maxWidth: "80%",
    wordWrap: "break-word",
  });

  const formStyle = {
    display: "flex",
    gap: "10px",
  };

  const inputStyle = {
    flex: 1,
    padding: "12px",
    background: "#0f0f1a",
    border: "1px solid #333",
    borderRadius: "5px",
    color: "#fff",
    resize: "none",
  };

  const buttonStyle = {
    padding: "12px 20px",
    background: "#00d4ff",
    color: "#000",
    border: "none",
    borderRadius: "5px",
    fontWeight: "bold",
    cursor: "pointer",
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ color: "#00d4ff", margin: "0 0 20px 0" }}>🤖 Chat com IA</h2>

      {/* Messages */}
      <div style={messagesContainerStyle}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              display: "flex",
              justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
              margin: "10px 0",
            }}
          >
            <div
              style={{
                ...messageStyle(msg.role),
                background:
                  msg.role === "user"
                    ? "#00d4ff"
                    : "#0f0f1a",
                color: msg.role === "user" ? "#000" : "#fff",
                borderLeft: msg.role !== "user" ? "4px solid #00d4ff" : "none",
              }}
            >
              {msg.role === "assistant" && <span>🤖 </span>}
              {msg.role === "user" && <span>👤 </span>}
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div style={{ display: "flex", justifyContent: "flex-start", margin: "10px 0" }}>
            <div
              style={{
                background: "#0f0f1a",
                padding: "12px 15px",
                borderRadius: "8px",
                color: "#888",
                borderLeft: "4px solid #ffd700",
              }}
            >
              ⏳ IA está digitando...
            </div>
          </div>
        )}
      </div>

      {/* Form */}
      <form onSubmit={handleSendMessage} style={formStyle}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSendMessage(e);
            }
          }}
          placeholder="Digite sua pergunta... (Shift+Enter para quebra de linha)"
          style={{ ...inputStyle, minHeight: "50px", maxHeight: "100px" }}
          disabled={loading}
        />
        <button type="submit" style={buttonStyle} disabled={loading}>
          {loading ? "⏳" : "📤"}
        </button>
      </form>
    </div>
  );
}

export default AIChat;
