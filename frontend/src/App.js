/**
 * Main App Component
 * Versão profissional com todos os 10 componentes
 * Tema customizado para brand SMC Analysis
 */

import { useState, useEffect } from 'react';
import { COLORS } from './theme';
import LoginComponent from './components/LoginComponent';
import TradingComponent from './components/TradingComponent';
import SignalsComponent from './components/SignalsComponent';
import AlertsNotifications from './components/AlertsNotifications';
import PricingComponent from './components/PricingComponent';
import AIChat from './components/AIChat';
import TradeHistory from './components/TradeHistory';
import ReportsAnalytics from './components/ReportsAnalytics';
import DashboardExample from './DashboardExample';
import { useSubscriptionStatus, useCancelSubscription } from './hooks';

// account page component used inside main App
function AccountPage({ userEmail, handleLogout }) {
  const { fetch, status, loading, error } = useSubscriptionStatus();
  const { cancel, loading: cancelLoading } = useCancelSubscription();

  useEffect(() => {
    fetch();
  }, [fetch]);

  return (
    <div
      style={{
        background: COLORS.bgSecondary,
        borderRadius: '12px',
        padding: '30px',
        margin: '20px',
        color: COLORS.textPrimary,
      }}
    >
      <h2 style={{ color: COLORS.primary, marginBottom: '20px' }}>
        👤 Minha Conta
      </h2>
      <div
        style={{
          background: COLORS.bgPrimary,
          padding: '20px',
          borderRadius: '8px',
          border: `1px solid ${COLORS.border}`,
        }}
      >
        <p>
          <strong>Email:</strong> {userEmail}
        </p>
        <p>
          <strong>Status:</strong>{' '}
          {loading ? (
            '⏳ Carregando...'
          ) : status?.ativa ? (
            <span style={{ color: COLORS.success }}>✓ Ativo</span>
          ) : (
            <span style={{ color: COLORS.danger }}>✗ Inativo</span>
          )}
        </p>
        {status && status.plan && (
          <p>
            <strong>Plano:</strong>{' '}
            <span style={{ color: COLORS.warning }}>{status.plan}</span>
          </p>
        )}
        {status && status.expires_at && (
          <>
            <p>
              <strong>Expira em:</strong>{' '}
              {new Date(status.expires_at).toLocaleString()}
            </p>
            {status.days_remaining !== undefined && (
              <p>
                <strong>Dias restantes:</strong>{' '}
                {status.days_remaining}
              </p>
            )}
          </>
        )}

        {error && (
          <p style={{ color: COLORS.danger }}>Erro: {error}</p>
        )}

        <div style={{ marginTop: '20px' }}>
          <button
            onClick={handleLogout}
            style={{
              padding: '10px 20px',
              background: COLORS.danger,
              color: COLORS.textPrimary,
              border: 'none',
              borderRadius: '5px',
              fontWeight: 'bold',
              cursor: 'pointer',
              marginRight: '10px',
            }}
          >
            Logout
          </button>
          {status?.ativa && (
            <button
              onClick={() => cancel().then(() => fetch())}
              style={{
                padding: '10px 20px',
                background: COLORS.warning,
                color: COLORS.textPrimary,
                border: 'none',
                borderRadius: '5px',
                fontWeight: 'bold',
                cursor: 'pointer',
              }}
              disabled={cancelLoading}
            >
              {cancelLoading ? '⏳ Cancelando...' : 'Cancelar Assinatura'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}



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

function App() {
  const [currentPage, setCurrentPage] = useState(APP_PAGES.DASHBOARD);
  const userEmail =
    localStorage.getItem('userEmail') || 'User';
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
        return <AccountPage userEmail={userEmail} handleLogout={handleLogout} />;
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
    background: COLORS.bgPrimary,
    color: COLORS.textPrimary,
  };

  const sidebarStyle = {
    width: sidebarOpen ? '250px' : '70px',
    background: COLORS.bgSecondary,
    borderRight: `1px solid ${COLORS.border}`,
    padding: '20px',
    transition: 'width 0.3s ease',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  };

  const logoStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    color: COLORS.primary,
    marginBottom: '30px',
    whiteSpace: 'nowrap',
    cursor: 'pointer',
    textAlign: 'center',
  };

  const navItemStyle = (isActive) => ({
    padding: '12px',
    margin: '8px 0',
    background: isActive ? COLORS.primaryDark : 'transparent',
    color: isActive ? COLORS.primary : COLORS.textSecondary,
    border: isActive ? `1px solid ${COLORS.primary}` : `1px solid ${COLORS.border}`,
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
    background: COLORS.bgSecondary,
    borderBottom: `1px solid ${COLORS.border}`,
    padding: '15px 30px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  };

  const toggleButtonStyle = {
    background: COLORS.primaryDark,
    color: COLORS.primary,
    border: `1px solid ${COLORS.primary}`,
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
              borderTop: `1px solid ${COLORS.border}`,
              fontSize: '12px',
              color: COLORS.textSecondary,
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
            <h1 style={{ margin: '0', color: COLORS.primary }}>
              {navItems.find((n) => n.page === currentPage)?.label ||
                'Dashboard'}
            </h1>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <div style={{ textAlign: 'right' }}>
              <p style={{ margin: '0', fontSize: '12px', color: COLORS.textSecondary }}>
                Bem-vindo,
              </p>
              <p style={{ margin: '0', fontWeight: 'bold' }}>{userEmail}</p>
            </div>

            <button
              onClick={handleLogout}
              style={{
                padding: '8px 16px',
                background: COLORS.danger,
                color: COLORS.textPrimary,
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

export default App;