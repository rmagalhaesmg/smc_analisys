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
      localStorage.setItem("token", response.access_token);
      localStorage.setItem("userEmail", email);
      window.location.reload();
    } catch (err) {
      console.error("Erro de login:", err);
    }
  };
  const s = { maxWidth:"400px",margin:"50px auto",padding:"30px",background:"#1a1a2e",borderRadius:"10px",border:"1px solid #333",color:"#fff" };
  const i = { width:"100%",padding:"10px",margin:"10px 0",background:"#0f0f1a",border:"1px solid #333",borderRadius:"5px",color:"#fff",boxSizing:"border-box" };
  const b = { width:"100%",padding:"12px",background:"#00d4ff",color:"#000",border:"none",borderRadius:"5px",fontWeight:"bold",cursor:"pointer",marginTop:"20px" };
  return (
    <div style={s}>
      <h2 style={{textAlign:"center",color:"#00d4ff"}}>🔐 Login</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="email" required style={i}/>
        <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="senha" required style={i}/>
        {error && <p style={{color:"#ff6b6b"}}>❌ {error}</p>}
        <button type="submit" style={b} disabled={loading}>{loading?"⏳ Entrando...":"🚀 Entrar"}</button>
      </form>
    </div>
  );
}
export default LoginComponent;
