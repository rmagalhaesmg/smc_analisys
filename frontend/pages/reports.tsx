import Layout from '../components/Layout';
import Sidebar from '../components/Sidebar';

export default function Reports() {
  // Mock data for reports
  const reports = [
    { id: 1, title: 'Relatório Mensal - Janeiro 2024', date: '01/02/2024', type: 'mensal' },
    { id: 2, title: 'Análise de Performance Q4 2023', date: '15/01/2024', type: 'trimestral' },
    { id: 3, title: 'Backtest WINM25 - Janeiro', date: '10/01/2024', type: 'backtest' },
  ];

  const stats = {
    totalSinais: 156,
    assertividade: '63.7%',
    pontosTotal: '+287.5',
    melhorAtivo: 'WIN',
    peorAtivo: 'WDO',
    streakAtual: 5,
    maiorStreak: 12,
  };

  return (
    <Layout>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 p-6">
          <h1 className="text-2xl font-bold text-white mb-6">📄 Relatórios</h1>

          {/* Quick Stats */}
          <div className="grid grid-cols-4 gap-4 mb-6">
            <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
              <div className="text-gray-400 text-sm">Total de Sinais</div>
              <div className="text-2xl font-bold text-white">{stats.totalSinais}</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
              <div className="text-gray-400 text-sm">Assertividade</div>
              <div className="text-2xl font-bold text-green-400">{stats.assertividade}</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
              <div className="text-gray-400 text-sm">Pontos Total</div>
              <div className="text-2xl font-bold text-cyan-400">{stats.pontosTotal}</div>
            </div>
            <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
              <div className="text-gray-400 text-sm">Streak Atual</div>
              <div className="text-2xl font-bold text-yellow-400">{stats.streakAtual}</div>
            </div>
          </div>

          {/* Performance Overview */}
          <div className="grid grid-cols-2 gap-6 mb-6">
            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">📈 Performance por Ativo</h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 bg-gray-900 rounded-lg">
                  <span className="text-white">WIN</span>
                  <span className="text-green-400 font-bold">+215.5 pts</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-900 rounded-lg">
                  <span className="text-white">WDO</span>
                  <span className="text-red-400 font-bold">-42.0 pts</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-900 rounded-lg">
                  <span className="text-white">DOLFUT</span>
                  <span className="text-green-400 font-bold">+114.0 pts</span>
                </div>
              </div>
            </div>

            <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <h2 className="text-xl font-bold text-white mb-4">🔥 Streaks</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gray-900 rounded-lg text-center">
                  <div className="text-3xl font-bold text-green-400">{stats.streakAtual}</div>
                  <div className="text-gray-400 text-sm">Streak Atual</div>
                </div>
                <div className="p-4 bg-gray-900 rounded-lg text-center">
                  <div className="text-3xl font-bold text-cyan-400">{stats.maiorStreak}</div>
                  <div className="text-gray-400 text-sm">Maior Streak</div>
                </div>
              </div>
            </div>
          </div>

          {/* Available Reports */}
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4">📁 Relatórios Disponíveis</h2>
            <div className="space-y-3">
              {reports.map((report) => (
                <div key={report.id} className="flex items-center justify-between p-4 bg-gray-900 rounded-lg hover:bg-gray-800 transition cursor-pointer">
                  <div className="flex items-center gap-4">
                    <span className="text-2xl">📄</span>
                    <div>
                      <p className="text-white font-medium">{report.title}</p>
                      <p className="text-gray-400 text-sm">{report.date}</p>
                    </div>
                  </div>
                  <span className={`px-3 py-1 rounded text-xs font-medium ${
                    report.type === 'mensal' ? 'bg-blue-500/20 text-blue-400' :
                    report.type === 'trimestral' ? 'bg-purple-500/20 text-purple-400' :
                    'bg-cyan-500/20 text-cyan-400'
                  }`}>
                    {report.type}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Export Options */}
          <div className="mt-6 bg-gray-800 p-6 rounded-xl border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4">📤 Exportar Dados</h2>
            <div className="flex gap-4">
              <button className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-bold rounded-lg transition">
                📊 Exportar Excel
              </button>
              <button className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-bold rounded-lg transition">
                📄 Exportar PDF
              </button>
              <button className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-bold rounded-lg transition">
                📋 Exportar CSV
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
