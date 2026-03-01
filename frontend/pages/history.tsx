import Layout from "../components/Layout";
import SignalsTable from "../components/SignalsTable";

export default function History() {
  return (
    <Layout>
      <div className="p-6">
        <h1 className="text-2xl font-bold text-white mb-6">📈 Histórico de Sinais</h1>
        
        {/* Filters */}
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 mb-6">
          <div className="grid grid-cols-4 gap-4">
            <div>
              <label className="block text-gray-400 mb-2">Data Inicial</label>
              <input
                type="date"
                className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
              />
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Data Final</label>
              <input
                type="date"
                className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white"
              />
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Ativo</label>
              <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                <option>Todos</option>
                <option>WIN</option>
                <option>WDO</option>
              </select>
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Resultado</label>
              <select className="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg text-white">
                <option>Todos</option>
                <option>Win</option>
                <option>Loss</option>
              </select>
            </div>
          </div>
        </div>

        {/* Signals Table */}
        <SignalsTable />
      </div>
    </Layout>
  );
}
