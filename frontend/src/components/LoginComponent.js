/**
 * Login Component
 * Exemplo de componente com autenticação
 */
import { useState } from "react";
import { useLogin } from "../hooks";

function LoginComponent() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, loading, error } = useLogin();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await login(email, password);
      // access_token já foi salvo pelo hook useLogin
      // salva também como 'token' que é o que App.js verifica
      localStorage.setItem("token", response.access_token);
      localStorage.setItem("userEmail", email);
      // redireciona recarregando a página — App.js vai detectar o token
      window.location.reload();
    } catch (err) {
      console.error("❌ Erro de login:", err);
    }
  };

  const containerStyle = {
    maxWidth: "400px",
    margin: "50px auto",
    padding: "30px",
    background: "#1a1a2e",
    borderRadius: "10px",
    border: "1px solid #333",
    color: "#fff",
  };

  const inputStyle = {
    width: "100%",
    padding: "10px",
    margin: "10px 0",
    background: "#0f0f1a",
    border: "1px solid #333",
    borderRadius: "5px",
    color: "#fff",
    boxSizing: "border-box",
  };

  const buttonStyle = {
    width: "100%",
    padding: "12px",
    background: "#00d4ff",
    color: "#000",
    border: "none",
    borderRadius: "5px",
    fontWeight: "bold",
    cursor: "pointer",
    marginTop: "20px",
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ textAlign: "center", color: "#00d4ff", margin: "0 0 20px 0" }}>
        🔐 Login
      </h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label style={{ display: "block", marginBottom: "5px" }}>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="seu@email.com"
            required
            style={inputStyle}
          />
        </div>
        <div>
          <label style={{ display: "block", marginBottom: "5px" }}>Senha:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="sua senha"
            required
            style={inputStyle}
          />
        </div>
        {error && (
          <p style={{ color: "#ff6b6b", marginTop: "10px", textAlign: "center" }}>
            ❌ {error}
          </p>
        )}
        <button type="submit" style={buttonStyle} disabled={loading}>
          {loading ? "⏳ Entrando..." : "🚀 Entrar"}
        </button>
      </form>
    </div>
  );
}

export default LoginComponent;