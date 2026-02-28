import { useState } from 'react';
import Layout from '../components/Layout';
import Sidebar from '../components/Sidebar';

export default function Settings() {
  const [activeTab, setActiveTab] = useState('profile');

  return (
    <Layout>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 p-6">
          <h1 className="text-2xl font-bold text-white mb-6">⚙️ Configurações</h1>

          {/* Tabs */}
          <div className="flex gap-2 mb-6 border-b border-gray-700 pb-2">
            {['profile', 'account', 'preferences'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-t-lg font-medium transition ${
                  activeTab === tab
                    ? 'bg-cyan-500 text-gray-900'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
              >
                {tab === 'profile' && '👤 Perfil'}
                {tab === 'account' && '🔐 Conta'}
                {tab === 'preferences' && '⚡ Preferências'}
              </button>
            ))}
          </div>

          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">Informações do Perfil</h2>
              
              <div className="space-y-4">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-20 h-20 bg-gray-700 rounded-full flex items-center justify-center text-3xl">
                    👤
                  </div>
                  <button className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-medium rounded-lg transition">
                    Alterar Foto
                  </button>
                </div>

                <div>
                  <label className="block text-gray-400 mb-2">Nome:</label>
                  <input
                    type="text"
                    defaultValue="Usuário"
                    className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                  />
                </div>

                <div>
                  <label className="block text-gray-400 mb-2">E-mail:</label>
                  <input
                    type="email"
                    defaultValue="usuario@email.com"
                    className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                  />
                </div>

                <div>
                  <label className="block text-gray-400 mb-2">Telefone:</label>
                  <input
                    type="tel"
                    placeholder="+55 (11) 99999-9999"
                    className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                  />
                </div>

                <button className="px-6 py-3 bg-green-500 hover:bg-green-400 text-gray-900 font-bold rounded-lg transition">
                  💾 Salvar Alterações
                </button>
              </div>
            </div>
          )}

          {/* Account Tab */}
          {activeTab === 'account' && (
            <div className="space-y-6">
              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-4">Segurança</h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-gray-400 mb-2">Senha atual:</label>
                    <input
                      type="password"
                      className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                    />
                  </div>

                  <div>
                    <label className="block text-gray-400 mb-2">Nova senha:</label>
                    <input
                      type="password"
                      className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                    />
                  </div>

                  <div>
                    <label className="block text-gray-400 mb-2">Confirmar nova senha:</label>
                    <input
                      type="password"
                      className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                    />
                  </div>

                  <button className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-bold rounded-lg transition">
                    🔒 Alterar Senha
                  </button>
                </div>
              </div>

              <div className="bg-gray-800 rounded-xl p-6 border border-red-500/30">
                <h2 className="text-xl font-bold text-red-400 mb-4">Zona de Perigo</h2>
                <p className="text-gray-400 mb-4">
                  Ao excluir sua conta, todos os dados serão permanentemente removidos.
                </p>
                <button className="px-6 py-3 bg-red-500 hover:bg-red-400 text-white font-bold rounded-lg transition">
                  🗑️ Excluir Conta
                </button>
              </div>
            </div>
          )}

          {/* Preferences Tab */}
          {activeTab === 'preferences' && (
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">Preferências do Sistema</h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-gray-400 mb-2">Tema:</label>
                  <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                    <option>Escuro (Padrão)</option>
                    <option>Claro</option>
                    <option>Automático</option>
                  </select>
                </div>

                <div>
                  <label className="block text-gray-400 mb-2">Idioma:</label>
                  <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                    <option>Português (Brasil)</option>
                    <option>English</option>
                    <option>Español</option>
                  </select>
                </div>

                <div>
                  <label className="block text-gray-400 mb-2">Fuso horário:</label>
                  <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                    <option>America/Sao_Paulo (GMT-3)</option>
                    <option>America/New_York (GMT-5)</option>
                    <option>Europe/London (GMT+0)</option>
                  </select>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-900 rounded-lg">
                  <div>
                    <p className="text-white font-medium">Notificações sonoras</p>
                    <p className="text-gray-400 text-sm">Som ao receber novos alertas</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" defaultChecked className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-500"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-900 rounded-lg">
                  <div>
                    <p className="text-white font-medium">Modo econômico</p>
                    <p className="text-gray-400 text-sm">Reduz consumo de recursos</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" />
                    <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-cyan-500"></div>
                  </label>
                </div>

                <button className="w-full px-6 py-3 bg-green-500 hover:bg-green-400 text-gray-900 font-bold rounded-lg transition">
                  💾 Salvar Preferências
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
