import { useState, useEffect } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid
} from "recharts";
import {
  Activity, Bell, Settings, TrendingUp,
  AlertTriangle, CheckCircle
} from "lucide-react";
import axios from "axios";

const API = "https://smcanalisys-production.up.railway.app";

const cardStyle = {
  background: "#1a1a2e",
  borderRadius: "12px",
  padding: "20px",
  border: "1px solid #333"
};

function StatusCard({ label, value, icon, color }) {
  return (
    <div style={cardStyle}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
        <span style={{ color: "#888", fontSize: "13px" }}>{label}</span>
        <span style={{ color }}>{icon}</span>
      </div>
      <div style={{ fontSize: "24px", fontWeight: "bold", color }}>{value}</div>
    </div>
  );
}

function Dashboard({ signals, candles, alerts, status }) {
  return (
    <>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginBottom: "24px" }}>
        <StatusCard label="Engine" value={status.engine || "..."} icon={<Activity size={20} />} color="#00ff88" />
        <StatusCard label="Sinais Hoje" value={status.signals_today || "..."} icon={<TrendingUp size={20} />} color="#00d4ff" />
        <StatusCard
          label="Win Rate"
          value={status.win_rate ? `${(status.win_rate * 100).toFixed(0)}%` : "..."}
          icon={<CheckCircle size={20} />}
          color="#ffd700"
        />
        <StatusCard label="Uptime" value={status.uptime || "..."} icon={<Activity size={20} />} color="#ff6b6b" />
      </div>

      <div style={{ ...cardStyle, marginBottom: "24px" }}>
        <h3 style={{ margin: "0 0 16px", color: "#00d4ff" }}>📈 Preço em Tempo Real</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={candles}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey="time" stroke="#555" />
            <YAxis stroke="#555" domain={["auto", "auto"]} />
            <Tooltip contentStyle={{ background: "#1a1a2e", border: "1px solid #333" }} />
            <Line type="monotone" dataKey="close" stroke="#00d4ff" dot={false} strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
        <div style={cardStyle}>
          <h3 style={{ margin: "0 0 16px", color: "#00d4ff" }}>🎯 Últimos Sinais</h3>
          {signals.map(s => (
            <div key={s.id} style={{
              display: "flex", justifyContent: "space-between",
              padding: "10px", borderRadius: "8px",
              background: "#0f0f1a", marginBottom: "8px"
            }}>
              <span style={{ color: "#ffd700", fontWeight: "bold" }}>{s.type}</span>
              <span style={{ color: "#00d4ff" }}>{s.price}</span>
              <span style={{ color: "#00ff88" }}>{(s.score * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>

        <div style={cardStyle}>
          <h3 style={{ margin: "0 0 16px", color: "#ff6b6b" }}>🔔 Alertas</h3>
          {alerts.map(a => (
            <div key={a.id} style={{
              display: "flex", gap: "10px",
              padding: "10px", borderRadius: "8px",
              background: "#0f0f1a", marginBottom: "8px"
            }}>
              <AlertTriangle size={16} color={a.level === "high" ? "#ff6b6b" : "#ffd700"} />
              <span style={{ fontSize: "13px" }}>{a.message}</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

function SignalsPage({ signals }) {
  return (
    <div style={cardStyle}>
      <h2 style={{ color: "#00d4ff", marginTop: 0 }}>🎯 Todos os Sinais</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid #333" }}>
            {["ID", "Tipo", "Preço", "Score", "Timestamp"].map(h => (
              <th key={h} style={{ padding: "10px", color: "#888", textAlign: "left" }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {signals.map(s => (
            <tr key={s.id} style={{ borderBottom: "1px solid #222" }}>
              <td style={{ padding: "10px", color: "#555" }}>#{s.id}</td>
              <td style={{ padding: "10px", color: "#ffd700", fontWeight: "bold" }}>{s.type}</td>
              <td style={{ padding: "10px", color: "#00d4ff" }}>{s.price}</td>
              <td style={{ padding: "10px", color: "#00ff88" }}>{(s.score * 100).toFixed(0)}%</td>
              <td style={{ padding: "10px", color: "#555", fontSize: "12px" }}>
                {new Date(s.timestamp).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function AlertsPage({ alerts }) {
  return (
    <div style={cardStyle}>
      <h2 style={{ color: "#ff6b6b", marginTop: 0 }}>🔔 Central de Alertas</h2>
      {alerts.map(a => (
        <div key={a.id} style={{
          display: "flex", gap: "16px", alignItems: "center",
          padding: "16px", borderRadius: "8px", background: "#0f0f1a",
          marginBottom: "12px",
          border: `1px solid ${a.level === "high" ? "#ff6b6b44" : "#ffd70044"}`
        }}>
          <AlertTriangle size={24} color={a.level === "high" ? "#ff6b6b" : "#ffd700"} />
          <div>
            <div style={{ fontWeight: "bold", marginBottom: "4px" }}>{a.message}</div>
            <div style={{ fontSize: "12px", color: "#555" }}>
              {new Date(a.timestamp).toLocaleString()}
            </div>
          </div>
          <span style={{
            marginLeft: "auto",
            background: a.level === "high" ? "#ff6b6b22" : "#ffd70022",
            color: a.level === "high" ? "#ff6b6b" : "#ffd700",
            padding: "4px 10px", borderRadius: "20px", fontSize: "12px"
          }}>
            {a.level}
          </span>
        </div>
      ))}
    </div>
  );
}

function SettingsPage() {
  return (
    <div style={cardStyle}>
      <h2 style={{ color: "#888", marginTop: 0 }}>⚙️ Configurações</h2>
      <div style={{ color: "#555" }}>API URL: {API}</div>
      <div style={{ color: "#555", marginTop: "8px" }}>Versão: 1.0.0</div>
    </div>
  );
}

function App() {
  const [signals, setSignals] = useState([]);
  const [candles, setCandles] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [status, setStatus] = useState({});
  const [page, setPage] = useState("dashboard");

  useEffect(() => {
    fetchAll();
    const interval = setInterval(fetchAll, 10000);
    return () => clearInterval(interval);
  }, []);

  async function fetchAll() {
    try {
      const [s, c, a, st] = await Promise.all([
        axios.get(`${API}/api/signals`),
        axios.get(`${API}/api/candles`),
        axios.get(`${API}/api/alerts`),
        axios.get(`${API}/api/status`),
      ]);
      setSignals(s.data.signals);
      setCandles(c.data.candles);
      setAlerts(a.data.alerts);
      setStatus(st.data);
    } catch (e) {
      console.error(e);
    }
  }

  const pages = ["dashboard", "signals", "alerts", "settings"];

  return (
    <div style={{ background: "#0f0f1a", minHeight: "100vh", color: "#e0e0e0", fontFamily: "monospace" }}>
      <div style={{
        background: "#1a1a2e", padding: "12px 24px",
        display: "flex", alignItems: "center", gap: "24px",
        borderBottom: "1px solid #333"
      }}>
        <span style={{ color: "#00d4ff", fontWeight: "bold", fontSize: "18px" }}>⚡ SMC Analysys</span>
        {pages.map(p => (
          <button key={p} onClick={() => setPage(p)} style={{
            background: page === p ? "#00d4ff22" : "transparent",
            color: page === p ? "#00d4ff" : "#888",
            border: "none", padding: "6px 14px",
            borderRadius: "6px", cursor: "pointer",
            textTransform: "capitalize"
          }}>
            {p}
          </button>
        ))}
        <div style={{ marginLeft: "auto" }}>
          <span style={{
            background: "#00ff8822", color: "#00ff88",
            padding: "4px 10px", borderRadius: "20px", fontSize: "12px"
          }}>
            ● LIVE
          </span>
        </div>
      </div>

      <div style={{ padding: "24px" }}>
        {page === "dashboard" && <Dashboard signals={signals} candles={candles} alerts={alerts} status={status} />}
        {page === "signals" && <SignalsPage signals={signals} />}
        {page === "alerts" && <AlertsPage alerts={alerts} />}
        {page === "settings" && <SettingsPage />}
      </div>
    </div>
  );
}

export default App;