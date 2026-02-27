/**
 * App.js - Versão com Componentes Integrados
 * Use este arquivo para integrar seus componentes
 */

import { useState } from "react";
import LoginComponent from "./components/LoginComponent";
import TradingComponent from "./components/TradingComponent";
import SignalsComponent from "./components/SignalsComponent";
import DashboardExample from "./DashboardExample";

const APP_PAGES = {
  DASHBOARD: "dashboard",
  LOGIN: "login",
  TRADING: "trading",
  SIGNALS: "signals",
};

function App() {
  const [currentPage, setCurrentPage] = useState(APP_PAGES.DASHBOARD);
  const userEmail = localStorage.getItem("user_email");

  // Estilos
  const appStyle = {
    background: "#0f0f1a",
    color: "#fff",
    minHeight: "100vh",
    fontFamily: "Arial, sans-serif",
  };

  const navbarStyle = {
    background: "#1a1a2e",
    borderBottom: "1px solid #333",
    padding: "15px 20px",
    position: "sticky",
    top: 0,
    zIndex: 1000,
  };

  const navContainerStyle = {
    maxWidth: "1200px",
    margin: "0 auto",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  };

  const navBrandStyle = {
    fontSize: "24px",
    fontWeight: "bold",
    color: "#00d4ff",
    cursor: "pointer",
    margin: 0,
  };

  const navLinksStyle = {
    display: "flex",
    gap: "20px",
    alignItems: "center",
    listStyle: "none",
    margin: 0,
    padding: 0,
  };

  const navLinkStyle = (isActive) => ({
    color: isActive ? "#00d4ff" : "#888",
    cursor: "pointer",
    textDecoration: "none",
    fontWeight: isActive ? "bold" : "normal",
    transition: "color 0.3s",
  });

  const contentStyle = {
    maxWidth: "1200px",
    margin: "20px auto",
    padding: "0 20px",
  };

  const getPageTitle = () => {
    switch (currentPage) {
      case APP_PAGES.DASHBOARD:
        return "🏠 Dashboard";
      case APP_PAGES.LOGIN:
        return "🔐 Login";
      case APP_PAGES.TRADING:
        return "📈 Trading";
      case APP_PAGES.SIGNALS:
        return "📊 Sinais";
      default:
        return "App";
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case APP_PAGES.DASHBOARD:
        return <DashboardExample />;
      case APP_PAGES.LOGIN:
        return <LoginComponent />;
      case APP_PAGES.TRADING:
        return <TradingComponent />;
      case APP_PAGES.SIGNALS:
        return <SignalsComponent />;
      default:
        return <DashboardExample />;
    }
  };

  return (
    <div style={appStyle}>
      {/* Navbar */}
      <nav style={navbarStyle}>
        <div style={navContainerStyle}>
          <h1 style={navBrandStyle} onClick={() => setCurrentPage(APP_PAGES.DASHBOARD)}>
            🚀 SMC SaaS
          </h1>

          <ul style={navLinksStyle}>
            <li>
              <a
                style={navLinkStyle(currentPage === APP_PAGES.DASHBOARD)}
                onClick={() => setCurrentPage(APP_PAGES.DASHBOARD)}
              >
                Dashboard
              </a>
            </li>
            <li>
              <a
                style={navLinkStyle(currentPage === APP_PAGES.TRADING)}
                onClick={() => setCurrentPage(APP_PAGES.TRADING)}
              >
                Trading
              </a>
            </li>
            <li>
              <a
                style={navLinkStyle(currentPage === APP_PAGES.SIGNALS)}
                onClick={() => setCurrentPage(APP_PAGES.SIGNALS)}
              >
                Sinais
              </a>
            </li>
            <li>
              <a
                style={navLinkStyle(currentPage === APP_PAGES.LOGIN)}
                onClick={() => setCurrentPage(APP_PAGES.LOGIN)}
              >
                Login
              </a>
            </li>
            {userEmail && (
              <li style={{ color: "#00ff88", fontSize: "12px" }}>
                ✅ {userEmail.split("@")[0]}
              </li>
            )}
          </ul>
        </div>
      </nav>

      {/* Content */}
      <div style={contentStyle}>
        <h2 style={{ color: "#00d4ff", marginBottom: "20px" }}>{getPageTitle()}</h2>
        {renderPage()}
      </div>

      {/* Footer */}
      <footer
        style={{
          background: "#1a1a2e",
          borderTop: "1px solid #333",
          padding: "20px",
          textAlign: "center",
          color: "#888",
          marginTop: "40px",
        }}
      >
        <p style={{ margin: 0 }}>
          🔧 SMC SaaS - Frontend & Backend Integrados
        </p>
        <p style={{ margin: "5px 0 0 0", fontSize: "12px" }}>
          📖 Backend API: <a href="http://127.0.0.1:8000/docs" style={{ color: "#00d4ff" }}>
            /docs
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
