import { useState } from 'react';
import Layout from '../components/Layout';
import Sidebar from '../components/Sidebar';

export default function Alerts() {
  const [telegramChatId, setTelegramChatId] = useState('');
  const [telegramBotToken, setTelegramBotToken] = useState('');
  const [email, setEmail] = useState('');
  const [whatsapp, setWhatsapp] = useState('');
  const [testing, setTesting] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<string | null>(null);

  const handleTest = async (type: string) => {
    setTesting(type);
    setTestResult(null);

    // Simulate test
    setTimeout(() => {
      setTesting(null);
      setTestResult(type === 'telegram' 
        ? '✅ Mensagem de teste enviada com sucesso!'
        : type === 'email'
        ? '✅ E-mail de teste enviado com sucesso!'
        : '✅ WhatsApp de teste enviado com sucesso!'
      );
    }, 1500);
  };

  return (
    <Layout>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 p-6">
          <h1 className="text-2xl font-bold text-white mb-6">🔔 Configuração de Alertas</h1>

          {/* Telegram */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">📱</span>
              <h2 className="text-xl font-bold text-white">Telegram</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-gray-400 mb-2">Chat ID:</label>
                <input
                  type="text"
                  value={telegramChatId}
                  onChange={(e) => setTelegramChatId(e.target.value)}
                  placeholder="Seu Chat ID do Telegram"
                  className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                />
              </div>
              
              <div>
                <label className="block text-gray-400 mb-2">Bot Token:</label>
                <input
                  type="password"
                  value={telegramBotToken}
                  onChange={(e) => setTelegramBotToken(e.target.value)}
                  placeholder="Token do seu Bot"
                  className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                />
              </div>

              <button
                onClick={() => handleTest('telegram')}
                disabled={testing !== null}
                className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-600 disabled:cursor-not-allowed text-gray-900 font-bold rounded-lg transition"
              >
                {testing === 'telegram' ? '⏳ Enviando...' : '🧪 Testar'}
              </button>

              {testResult && testing === null && (
                <p className="text-green-400 mt-2">{testResult}</p>
              )}
            </div>
          </div>

          {/* Email */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">📧</span>
              <h2 className="text-xl font-bold text-white">E-mail</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-gray-400 mb-2">E-mail de destino:</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="seu@email.com"
                  className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                />
              </div>

              <button
                onClick={() => handleTest('email')}
                disabled={testing !== null}
                className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-600 disabled:cursor-not-allowed text-gray-900 font-bold rounded-lg transition"
              >
                {testing === 'email' ? '⏳ Enviando...' : '🧪 Testar'}
              </button>

              {testResult && testing === null && (
                <p className="text-green-400 mt-2">{testResult}</p>
              )}
            </div>
          </div>

          {/* WhatsApp */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-6">
            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl">💬</span>
              <h2 className="text-xl font-bold text-white">WhatsApp</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-gray-400 mb-2">Número:</label>
                <input
                  type="text"
                  value={whatsapp}
                  onChange={(e) => setWhatsapp(e.target.value)}
                  placeholder="+55 (11) 99999-9999"
                  className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                />
              </div>

              <button
                onClick={() => handleTest('whatsapp')}
                disabled={testing !== null}
                className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-600 disabled:cursor-not-allowed text-gray-900 font-bold rounded-lg transition"
              >
                {testing === 'whatsapp' ? '⏳ Enviando...' : '🧪 Testar'}
              </button>

              {testResult && testing === null && (
                <p className="text-green-400 mt-2">{testResult}</p>
              )}
            </div>
          </div>

          {/* Alert Preferences */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4">⚙️ Preferências de Alertas</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-gray-400 mb-2">Score mínimo para alerta:</label>
                <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                  <option value="0.7">70%</option>
                  <option value="0.75" selected>75%</option>
                  <option value="0.8">80%</option>
                  <option value="0.85">85%</option>
                  <option value="0.9">90%</option>
                </select>
              </div>

              <div>
                <label className="block text-gray-400 mb-2">Ativos para monitorar:</label>
                <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                  <option>WIN (Índice WIN)</option>
                  <option>WDO (Dólar)</option>
                  <option>WIN + WDO</option>
                  <option>Todos</option>
                </select>
              </div>

              <div>
                <label className="block text-gray-400 mb-2">Horários de alerta:</label>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-gray-500 text-sm">Início</label>
                    <input
                      type="time"
                      defaultValue="09:00"
                      className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="text-gray-500 text-sm">Fim</label>
                    <input
                      type="time"
                      defaultValue="17:00"
                      className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                </div>
              </div>

              <button className="w-full px-6 py-3 bg-green-500 hover:bg-green-400 text-gray-900 font-bold rounded-lg transition">
                💾 Salvar Configurações
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
