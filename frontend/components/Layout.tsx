import React from "react";
import { Link, useLocation } from "react-router-dom";

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  const isLandingPage = location.pathname === '/';

  // Landing page and login don't use sidebar
  if (isLandingPage || isLoginPage) {
    return (
      <div className="min-h-screen bg-gray-900">
        {children}
      </div>
    );
  }

  return (
    <div className="min-h-screen flex bg-gray-900">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
        {/* Logo */}
        <div className="p-4 border-b border-gray-800">
        <Link to="/dashboard" className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-2xl">📊</span>
            </div>
            <span className="text-xl font-bold text-white">SMC Analysys</span>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {[
              { to: '/dashboard', label: 'Dashboard', icon: '📊' },
              { to: '/history', label: 'Histórico / Backtest', icon: '📈' },
              { to: '/datasources', label: '📥 Fontes de Dados', icon: '📥' },
              { to: '/alerts', label: 'Alertas', icon: '🔔' },
              { to: '/assistant', label: 'Assistente IA', icon: '🤖' },
              { to: '/reports', label: 'Relatórios', icon: '📄' },
              { to: '/billing', label: 'Assinatura', icon: '💳' },
              { to: '/settings', label: 'Configurações', icon: '⚙️' },
            ].map((item) => {
              const isActive = location.pathname === item.to;
              return (
              <li key={item.to}>
                  <Link
                    to={item.to}
                    className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                        : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                    }`}
                  >
                    <span className="text-lg">{item.icon}</span>
                    <span className="font-medium">{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* User Info */}
        <div className="p-4 border-t border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center">
              <span className="text-lg">👤</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">Usuário</p>
              <p className="text-xs text-gray-400 truncate">Plano Premium</p>
            </div>
          </div>
          <button
            onClick={() => {
              localStorage.removeItem('token');
              window.location.href = '/login';
            }}
            className="mt-3 w-full px-4 py-2 text-sm text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors text-left"
          >
            🚪 Sair
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6 overflow-auto">
        {children}
      </main>
    </div>
  );
};

export default Layout;
