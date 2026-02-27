/**
 * Advanced App with All Components
 * Exemplo completo de como integrar todos os 10 componentes
 */

import { useState, useEffect } from 'react';
import LoginComponent from './components/LoginComponent';
import TradingComponent from './components/TradingComponent';
import SignalsComponent from './components/SignalsComponent';
import AlertsNotifications from './components/AlertsNotifications';
import PricingComponent from './components/PricingComponent';
import AIChat from './components/AIChat';
import TradeHistory from './components/TradeHistory';
import ReportsAnalytics from './components/ReportsAnalytics';
import DashboardExample from './DashboardExample';

const APP_PAGES = {
  DASHBOARD: 'dashboard',
  TRADING: 'trading',
  SIGNALS: 'signals',
  ALERTS: 'alerts',
  HISTORY: 'history',
  ANALYTICS: 'analytics',
  CHAT: 'chat',
  PRICING: 'pricing',
  ACCOUNT: 'account',
};

function AppAdvanced() {
  const [currentPage, setCurrentPage] = useState(APP_PAGES.DASHBOARD);
  const [userEmail, setUserEmail] = useState(
    localStorage.getItem('userEmail') || 'User'
  );
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem('token')
  );
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    setIsLoggedIn(false);
    setCurrentPage(APP_PAGES.DASHBOARD);
  };

  if (!isLoggedIn) {
    return <LoginComponent />;
  }

  const renderPage = () => {
    switch (currentPage) {
      case APP_PAGES.DASHBOARD:
        return <DashboardExample />;
      case APP_PAGES.TRADING:
        return <TradingComponent />;
      case APP_PAGES.SIGNALS:
        return <SignalsComponent />;
      case APP_PAGES.ALERTS:
        return <AlertsNotifications />;
      case APP_PAGES.HISTORY:
        return <TradeHistory />;
      case APP_PAGES.ANALYTICS:
        return <ReportsAnalytics />;
      case APP_PAGES.CHAT:
        return <AIChat />;
      case APP_PAGES.PRICING:
        return <PricingComponent />;
      case APP_PAGES.ACCOUNT:
        return (
          <div
            style={{
              background: '#1a1a2e',
              borderRadius: '12px',
              padding: '30px',
              margin: '20px',
              color: '#fff',
            }}
          >
            <h2 style={{ color: '#00d4ff', marginBottom: '20px' }}>
              👤 Minha Conta
            </h2>
            <div
              style={{
                background: '#0f0f1a',
                padding: '20px',
                borderRadius: '8px',
                border: '1px solid #333',
              }}
            >
              <p>
                <strong>Email:</strong> {userEmail}
              </p>
              <p>
                <strong>Status:</strong> <span style={{ color: '#00ff88' }}>✓ Ativo</span>
              </p>
              <p>
                <strong>Plano:</strong> <span style={{ color: '#ffd700' }}>Premium</span>
              </p>
              <button
                onClick={handleLogout}
                style={{
                  marginTop: '20px',
                  padding: '10px 20px',
                  background: '#ff6b6b',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '5px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                }}
              >
                Logout
              </button>
            </div>
          </div>
        );
      default:
        return <DashboardExample />;
    }
  };

  const navItems = [
    { icon: '📊', label: 'Dashboard', page: APP_PAGES.DASHBOARD },
    { icon: '🎯', label: 'Trading', page: APP_PAGES.TRADING },
    { icon: '📈', label: 'Sinais', page: APP_PAGES.SIGNALS },
    { icon: '🔔', label: 'Alertas', page: APP_PAGES.ALERTS },
    { icon: '📋', label: 'Histórico', page: APP_PAGES.HISTORY },
    { icon: '📊', label: 'Análises', page: APP_PAGES.ANALYTICS },
    { icon: '💬', label: 'Chat IA', page: APP_PAGES.CHAT },
    { icon: '💰', label: 'Planos', page: APP_PAGES.PRICING },
    { icon: '👤', label: 'Conta', page: APP_PAGES.ACCOUNT },
  ];

  const containerStyle = {
    display: 'flex',
    minHeight: '100vh',
    background: '#0f0f1a',
    color: '#fff',
  };

  const sidebarStyle = {
    width: sidebarOpen ? '250px' : '70px',
    background: '#1a1a2e',
    borderRight: '1px solid #333',
    padding: '20px',
    transition: 'width 0.3s ease',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  const logoStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#00d4ff',
    marginBottom: '30px',
    whiteSpace: 'nowrap',
    cursor: 'pointer',
    textAlign: 'center',
  };

  const navItemStyle = (isActive) => ({
    padding: '12px',
    margin: '8px 0',
    background: isActive ? '#0f4c75' : 'transparent',
    color: isActive ? '#00d4ff' : '#888',
    border: isActive ? '1px solid #00d4ff' : '1px solid #333',
    borderRadius: '5px',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    whiteSpace: 'nowrap',
    transition: 'all 0.2s ease',
  });

  const mainContentStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'auto',
  };

  const headerStyle = {
    background: '#1a1a2e',
    borderBottom: '1px solid #333',
    padding: '15px 30px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  };

  const toggleButtonStyle = {
    background: '#0f4c75',
    color: '#00d4ff',
    border: '1px solid #00d4ff',
    borderRadius: '5px',
    padding: '8px 12px',
    cursor: 'pointer',
    fontWeight: 'bold',
  };

  const contentStyle = {
    flex: 1,
    overflow: 'auto',
    padding: '20px',
  };

  return (
    <div style={containerStyle}>
      {/* Sidebar */}
      <div style={sidebarStyle}>
        <div
          style={logoStyle}
          onClick={() => setCurrentPage(APP_PAGES.DASHBOARD)}
          title="Voltar para Dashboard"
        >
          {sidebarOpen ? '📊 SMC Analysis' : '📊'}
        </div>

        <nav style={{ flex: 1 }}>
          {navItems.map((item) => (
            <div
              key={item.page}
              onClick={() => setCurrentPage(item.page)}
              style={navItemStyle(currentPage === item.page)}
              title={sidebarOpen ? '' : item.label}
            >
              <span style={{ fontSize: '18px' }}>{item.icon}</span>
              {sidebarOpen && <span>{item.label}</span>}
            </div>
          ))}
        </nav>

        {/* Sidebar Footer */}
        {sidebarOpen && (
          <div
            style={{
              paddingTop: '20px',
              borderTop: '1px solid #333',
              fontSize: '12px',
              color: '#888',
              textAlign: 'center',
            }}
          >
            <p style={{ margin: '0 0 10px 0' }}>v1.0.0</p>
            <p style={{ margin: '0' }}>© 2025 SMC Trading</p>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div style={mainContentStyle}>
        {/* Header */}
        <div style={headerStyle}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              style={toggleButtonStyle}
            >
              {sidebarOpen ? '◀' : '▶'}
            </button>
            <h1 style={{ margin: '0', color: '#00d4ff' }}>
              {navItems.find((n) => n.page === currentPage)?.label ||
                'Dashboard'}
            </h1>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <div style={{ textAlign: 'right' }}>
              <p style={{ margin: '0', fontSize: '12px', color: '#888' }}>
                Bem-vindo,
              </p>
              <p style={{ margin: '0', fontWeight: 'bold' }}>{userEmail}</p>
            </div>

            <button
              onClick={handleLogout}
              style={{
                padding: '8px 16px',
                background: '#ff6b6b',
                color: '#fff',
                border: 'none',
                borderRadius: '5px',
                fontWeight: 'bold',
                cursor: 'pointer',
              }}
            >
              Logout
            </button>
          </div>
        </div>

        {/* Page Content */}
        <div style={contentStyle}>{renderPage()}</div>
      </div>
    </div>
  );
}

export default AppAdvanced;
