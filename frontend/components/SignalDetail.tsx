type ScoreBarProps = {
  name: string;
  score: number;
  description: string;
};

export default function SignalDetail() {
  const scoreBars: ScoreBarProps[] = [
    { name: 'HFZ', score: 0.78, description: 'High Frequency Zone' },
    { name: 'FBI', score: 0.85, description: 'Fair Value Gap' },
    { name: 'DTM', score: 0.70, description: 'Depth Market Analysis' },
    { name: 'SDA', score: 0.88, description: 'Supply & Demand' },
    { name: 'MTV', score: 0.75, description: 'Market Trend Velocity' },
  ];

  const finalScore = 0.82;
  const direction = 'COMPRA';
  const time = '10:32';
  const asset = 'WINM25';
  const points = '+1.2 pts';
  const status = 'EM ANDAMENTO';

  const aiContext = 'Alta absorção com falha de rompimento, favorece retorno ao ponto de equilíbrio. O fluxo de compra está predominante nos últimos 5 minutos.';

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <div className={`px-4 py-2 rounded-lg font-bold ${
            direction === 'COMPRA' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
          }`}>
            🚀 ALERTA FINAL: {direction}
          </div>
          <div className="text-2xl font-bold text-white">
            Score final: {finalScore.toFixed(2)}
          </div>
        </div>
        <div className="text-gray-400">
          {time} - {asset}
        </div>
      </div>

      {/* Score Bars */}
      <div className="mb-6">
        <h3 className="text-white font-bold mb-4">Scores por Indicador:</h3>
        <div className="space-y-3">
          {scoreBars.map((item) => (
            <div key={item.name} className="flex items-center gap-4">
              <div className="w-16 text-gray-400 font-medium">{item.name}</div>
              <div className="flex-1 bg-gray-900 rounded-full h-4 overflow-hidden">
                <div 
                  className={`h-full rounded-full ${
                    item.score >= 0.8 ? 'bg-green-500' : item.score >= 0.7 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${item.score * 100}%` }}
                />
              </div>
              <div className="w-12 text-right">
                <span className={`font-bold ${
                  item.score >= 0.8 ? 'text-green-400' : item.score >= 0.7 ? 'text-yellow-400' : 'text-red-400'
                }`}>
                  {item.score.toFixed(2)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AI Context */}
      <div className="p-4 bg-blue-500/20 border border-blue-500/30 rounded-lg mb-6">
        <h4 className="text-blue-400 font-bold mb-2">🧠 Contexto IA:</h4>
        <p className="text-gray-300">{aiContext}</p>
      </div>

      {/* Result */}
      <div className="flex items-center justify-between p-4 bg-gray-900 rounded-lg">
        <div>
          <span className="text-gray-400">Resultado Parcial:</span>
          <span className={`ml-2 font-bold ${points.startsWith('+') ? 'text-green-400' : 'text-red-400'}`}>
            {points}
          </span>
        </div>
        <div>
          <span className="text-gray-400">Status:</span>
          <span className="ml-2 px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded text-sm">
            {status}
          </span>
        </div>
      </div>

      {/* Historical Stats */}
      <div className="mt-6 p-4 bg-gray-900 rounded-lg">
        <h4 className="text-white font-bold mb-3">📊 Estatísticas Históricas</h4>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-green-400">64%</div>
            <div className="text-gray-400 text-sm">Assertividade</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-cyan-400">+2.1</div>
            <div className="text-gray-400 text-sm">Pontos Médios</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-white">156</div>
            <div className="text-gray-400 text-sm">Sinais Semelhantes</div>
          </div>
        </div>
      </div>
    </div>
  );
}
