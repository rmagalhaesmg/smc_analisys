import React, { useState } from 'react';
import Layout from '../components/Layout';
import Sidebar from '../components/Sidebar';

type DataSource = {
  name: string;
  status: 'active' | 'delayed' | 'offline';
  lastUpdate: string;
  latency?: string;
};

type TabType = 'status' | 'csv' | 'rtd' | 'dll' | 'api';

export default function DataSources() {
  const [activeTab, setActiveTab] = useState<TabType>('status');
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [csvType, setCsvType] = useState<'trades' | 'book' | 'volume'>('trades');
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<string | null>(null);

  // Mock data sources
  const dataSources: DataSource[] = [
    { name: 'CSV Profit', status: 'active', lastUpdate: '10:42' },
    { name: 'RTD', status: 'active', lastUpdate: '10:43', latency: '120ms' },
    { name: 'DLL', status: 'offline', lastUpdate: '-' },
    { name: 'API Neológica', status: 'active', lastUpdate: '10:43', latency: '85ms' },
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setCsvFile(e.target.files[0]);
      setUploadResult(null);
    }
  };

  const handleUpload = async () => {
    if (!csvFile) return;
    
    setUploading(true);
    setUploadResult(null);

    // Simulate upload
    setTimeout(() => {
      setUploading(false);
      setUploadResult('✔ Arquivo validado\n✔ 125.000 ticks carregados\n✔ Replay disponível\n✔ Backtest recalculado');
    }, 2000);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'delayed': return 'bg-yellow-500';
      case 'offline': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <Layout>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 p-6">
          <h1 className="text-2xl font-bold text-white mb-6">📥 Fontes de Dados</h1>

          {/* Tabs */}
          <div className="flex gap-2 mb-6 border-b border-gray-700 pb-2">
            {(['status', 'csv', 'rtd', 'dll', 'api'] as TabType[]).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-t-lg font-medium transition ${
                  activeTab === tab
                    ? 'bg-cyan-500 text-gray-900'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                }`}
              >
                {tab === 'status' && '📊 Status'}
                {tab === 'csv' && '📁 CSV'}
                {tab === 'rtd' && '⚡ RTD'}
                {tab === 'dll' && '🔌 DLL'}
                {tab === 'api' && '🌐 API'}
              </button>
            ))}
          </div>

          {/* Status Tab */}
          {activeTab === 'status' && (
            <div className="space-y-6">
              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-4">STATUS DAS FONTES</h2>
                <div className="grid gap-4">
                  {dataSources.map((source) => (
                    <div key={source.name} className="flex items-center justify-between p-4 bg-gray-900 rounded-lg">
                      <div className="flex items-center gap-4">
                        <div className={`w-3 h-3 rounded-full ${getStatusColor(source.status)}`} />
                        <span className="text-white font-medium">{source.name}</span>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          source.status === 'active' ? 'bg-green-500/20 text-green-400' :
                          source.status === 'delayed' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-red-500/20 text-red-400'
                        }`}>
                          {source.status === 'active' ? '● Ativo' :
                           source.status === 'delayed' ? '● Atrasado' : '● Offline'}
                        </span>
                      </div>
                      <div className="text-gray-400 text-sm">
                        {source.latency && <span className="mr-4">Latência: {source.latency}</span>}
                        <span>Última: {source.lastUpdate}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Pipeline Visual */}
              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <h2 className="text-xl font-bold text-white mb-4">🔄 PIPELINE DE DADOS</h2>
                <div className="flex items-center justify-between gap-4">
                  <div className="flex gap-2">
                    <span className="px-3 py-2 bg-gray-700 text-cyan-400 rounded-lg text-sm">CSV</span>
                    <span className="px-3 py-2 bg-gray-700 text-cyan-400 rounded-lg text-sm">RTD</span>
                    <span className="px-3 py-2 bg-gray-700 text-cyan-400 rounded-lg text-sm">DLL</span>
                    <span className="px-3 py-2 bg-gray-700 text-cyan-400 rounded-lg text-sm">API</span>
                  </div>
                  <span className="text-gray-500">→</span>
                  <div className="px-3 py-2 bg-gray-700 text-yellow-400 rounded-lg text-sm">Normalização</div>
                  <span className="text-gray-500">→</span>
                  <div className="px-3 py-2 bg-gray-700 text-yellow-400 rounded-lg text-sm">Cálculo SMC</div>
                  <span className="text-gray-500">→</span>
                  <div className="px-3 py-2 bg-gray-700 text-green-400 rounded-lg text-sm">Scores</div>
                  <span className="text-gray-500">→</span>
                  <div className="px-3 py-2 bg-cyan-500 text-gray-900 font-bold rounded-lg text-sm">Alerta</div>
                </div>
              </div>
            </div>
          )}

          {/* CSV Tab */}
          {activeTab === 'csv' && (
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">📁 IMPORTAR CSV (Profit / Replay / Backtest)</h2>
              
              <div className="space-y-6">
                <div className="border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-cyan-500 transition">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    className="hidden"
                    id="csv-upload"
                  />
                  <label htmlFor="csv-upload" className="cursor-pointer">
                    <div className="text-4xl mb-4">📄</div>
                    <p className="text-white mb-2">
                      {csvFile ? csvFile.name : 'Selecionar Arquivo CSV'}
                    </p>
                    <p className="text-gray-400 text-sm">Arraste ou clique para selecionar</p>
                  </label>
                </div>

                <div>
                  <p className="text-white mb-3">Tipo de dado:</p>
                  <div className="flex gap-4">
                    {(['trades', 'book', 'volume'] as const).map((type) => (
                      <label key={type} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="radio"
                          name="csvType"
                          value={type}
                          checked={csvType === type}
                          onChange={(e) => setCsvType(e.target.value as typeof csvType)}
                          className="text-cyan-500"
                        />
                        <span className="text-gray-300">
                          {type === 'trades' && 'Times & Trades'}
                          {type === 'book' && 'Livro de Ofertas'}
                          {type === 'volume' && 'Volume / Agressão'}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>

                <button
                  onClick={handleUpload}
                  disabled={!csvFile || uploading}
                  className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-600 disabled:cursor-not-allowed text-gray-900 font-bold rounded-lg transition"
                >
                  {uploading ? '⏳ Enviando e Processando...' : '📤 Enviar e Processar'}
                </button>

                {uploadResult && (
                  <div className="p-4 bg-green-500/20 border border-green-500/30 rounded-lg">
                    <pre className="text-green-400 whitespace-pre-line">{uploadResult}</pre>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* RTD Tab */}
          {activeTab === 'rtd' && (
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">⚡ RTD - PROFIT</h2>
              
              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-gray-900 rounded-lg">
                  <span className="text-white font-medium">Status:</span>
                  <span className="text-green-400 font-bold">● Conectado</span>
                </div>

                <div>
                  <label className="block text-white mb-2">Símbolo:</label>
                  <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                    <option>WIN / WDO</option>
                    <option>WINM25</option>
                    <option>WDOM25</option>
                  </select>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-900 rounded-lg">
                  <span className="text-white font-medium">Frequência:</span>
                  <span className="text-cyan-400">100ms</span>
                </div>

                <div>
                  <p className="text-white mb-3">Campos recebidos:</p>
                  <div className="grid grid-cols-2 gap-2">
                    {['✓ Preço', '✓ Volume', '✓ Agressão', '✓ Delta'].map((field) => (
                      <span key={field} className="text-green-400">{field}</span>
                    ))}
                  </div>
                </div>

                <button className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-bold rounded-lg transition">
                  🧪 Testar Conexão
                </button>
              </div>
            </div>
          )}

          {/* DLL Tab */}
          {activeTab === 'dll' && (
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">🔌 DLL BRIDGE</h2>
              
              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-gray-900 rounded-lg">
                  <span className="text-white font-medium">Status:</span>
                  <span className="text-red-400 font-bold">● Desconectado</span>
                </div>

                <div>
                  <label className="block text-white mb-2">Porta:</label>
                  <input
                    type="text"
                    defaultValue="127.0.0.1:9001"
                    className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                  />
                </div>

                <div className="flex gap-4">
                  <button className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-bold rounded-lg transition">
                    ▶ Iniciar Listener
                  </button>
                  <button className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-bold rounded-lg transition">
                    🧪 Testar
                  </button>
                </div>

                <div className="p-4 bg-gray-900 rounded-lg">
                  <p className="text-gray-400 text-sm">Ideal para:</p>
                  <ul className="text-gray-300 mt-2 space-y-1">
                    <li>• Ambientes proprietários</li>
                    <li>• Servidores locais</li>
                    <li>• Mesas proprietárias</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* API Tab */}
          {activeTab === 'api' && (
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">🌐 API DE DADOS</h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-white mb-2">Provider:</label>
                  <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                    <option>Neológica</option>
                    <option>Other Provider</option>
                  </select>
                </div>

                <div>
                  <label className="block text-white mb-2">API Key:</label>
                  <input
                    type="password"
                    placeholder="*********************"
                    className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
                  />
                </div>

                <div>
                  <p className="text-white mb-3">Endpoints:</p>
                  <div className="grid grid-cols-3 gap-2">
                    {['✓ Times & Trades', '✓ Book', '✓ Volume'].map((endpoint) => (
                      <span key={endpoint} className="text-green-400 text-sm">{endpoint}</span>
                    ))}
                  </div>
                </div>

                <button className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-bold rounded-lg transition">
                  ✅ Validar Credenciais
                </button>
              </div>
            </div>
          )}

          {/* Alert Destinations */}
          <div className="mt-6 bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4">🔔 DESTINOS DE ALERTA</h2>
            <div className="flex gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" defaultChecked className="text-cyan-500" />
                <span className="text-gray-300">Telegram</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" defaultChecked className="text-cyan-500" />
                <span className="text-gray-300">E-mail</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="text-cyan-500" />
                <span className="text-gray-300">WhatsApp</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
