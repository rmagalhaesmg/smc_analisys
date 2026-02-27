/**
 * AlertsNotifications Component
 * Mostra alertas e notificações do sistema
 */

import { useState, useEffect } from "react";
import { alertsAPI } from "../api";

function AlertsNotifications() {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("recent"); // recent || stats

  useEffect(() => {
    loadAlerts();
    const interval = setInterval(loadAlerts, 30000); // Atualizar a cada 30s
    return () => clearInterval(interval);
  }, []);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      const [alertsRes, statsRes] = await Promise.all([
        alertsAPI.getLog(),
        alertsAPI.getStats(),
      ]);
      setAlerts(alertsRes.data || []);
      setStats(statsRes.data || {});
    } catch (error) {
      console.error("Erro ao carregar alertas:", error);
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
    maxWidth: "700px",
    margin: "20px auto",
  };

  const tabsStyle = {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
    borderBottom: "1px solid #333",
    paddingBottom: "10px",
  };

  const tabButtonStyle = (isActive) => ({
    padding: "8px 16px",
    background: isActive ? "#00d4ff" : "transparent",
    color: isActive ? "#000" : "#888",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontWeight: isActive ? "bold" : "normal",
  });

  const alertItemStyle = {
    background: "#0f0f1a",
    padding: "12px",
    borderRadius: "5px",
    marginBottom: "10px",
    borderLeft: "4px solid #00d4ff",
  };

  const statCardStyle = {
    background: "#0f0f1a",
    padding: "15px",
    borderRadius: "5px",
    textAlign: "center",
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ color: "#00d4ff", margin: "0 0 20px 0" }}>🔔 Alertas e Notificações</h2>

      {/* Tabs */}
      <div style={tabsStyle}>
        <button
          style={tabButtonStyle(activeTab === "recent")}
          onClick={() => setActiveTab("recent")}
        >
          📋 Recentes
        </button>
        <button
          style={tabButtonStyle(activeTab === "stats")}
          onClick={() => setActiveTab("stats")}
        >
          📊 Estatísticas
        </button>
        <button
          style={{ marginLeft: "auto", ...tabButtonStyle(false) }}
          onClick={loadAlerts}
          disabled={loading}
        >
          {loading ? "⏳" : "🔄"} Atualizar
        </button>
      </div>

      {/* Recent Alerts */}
      {activeTab === "recent" && (
        <div>
          {alerts.length > 0 ? (
            alerts.slice(0, 10).map((alert, idx) => (
              <div key={idx} style={alertItemStyle}>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span style={{ fontWeight: "bold", color: "#ffd700" }}>
                    {alert.type || "ALERTA"}
                  </span>
                  <span style={{ color: "#888", fontSize: "12px" }}>
                    {alert.timestamp
                      ? new Date(alert.timestamp).toLocaleTimeString("pt-BR")
                      : "---"}
                  </span>
                </div>
                <p style={{ margin: "5px 0 0 0", color: "#888", fontSize: "14px" }}>
                  {alert.message || alert.description || "Sem mensagem"}
                </p>
              </div>
            ))
          ) : (
            <p style={{ color: "#888" }}>📭 Nenhum alerta recente</p>
          )}
        </div>
      )}

      {/* Stats */}
      {activeTab === "stats" && stats && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "15px" }}>
          <div style={statCardStyle}>
            <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Total de Alertas</p>
            <p style={{ fontSize: "24px", fontWeight: "bold", color: "#00d4ff", margin: "10px 0 0 0" }}>
              {stats.total_alerts || 0}
            </p>
          </div>
          <div style={statCardStyle}>
            <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Hoje</p>
            <p style={{ fontSize: "24px", fontWeight: "bold", color: "#ffd700", margin: "10px 0 0 0" }}>
              {stats.today || 0}
            </p>
          </div>
          <div style={statCardStyle}>
            <p style={{ margin: "0", color: "#888", fontSize: "12px" }}>Taxa de Sucesso</p>
            <p style={{ fontSize: "24px", fontWeight: "bold", color: "#00ff88", margin: "10px 0 0 0" }}>
              {stats.success_rate ? `${(stats.success_rate * 100).toFixed(0)}%` : "--"}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default AlertsNotifications;
