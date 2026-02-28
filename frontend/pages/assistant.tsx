import { useState, useRef, useEffect } from 'react';
import Layout from '../components/Layout';
import Sidebar from '../components/Sidebar';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

const quickQuestions = [
  'Último sinal foi bom?',
  'Qual a assertividade hoje?',
  'Me explica o último backtest',
  'Qual ativo está mais favorável?',
];

export default function Assistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Olá! Sou o assistente IA do SMC Analysys. Posso te ajudar com:\n\n• Análise do último sinal\n• Estatísticas de performance\n• Resultados de backtest\n• Insights sobre o mercado\n\nComo posso ajudar?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    // Simulate AI response
    setTimeout(() => {
      let response = '';
      
      if (userMessage.toLowerCase().includes('sinal') && userMessage.toLowerCase().includes('bom')) {
        response = 'Historicamente, sinais com score acima de 0.80 têm 72% de assertividade. O último sinal (COMPRA em WIN) teve score de 0.82, o que indica uma oportunidade interessante.';
      } else if (userMessage.toLowerCase().includes('assertividade')) {
        response = 'Hoje sua assertividade está em 63.7% (47 acertos em 74 operações). Na última semana: 61.2%. No último mês: 58.9%.';
      } else if (userMessage.toLowerCase().includes('backtest')) {
        response = 'O último backtest realizado com dados do último mês mostrou:\n\n• Profit Factor: 1.42\n• Sharpe Ratio: 1.18\n• Drawdown máximo: -3.2%\n• Total de operações: 156\n\nPosso detalhar mais algum ponto?';
      } else if (userMessage.toLowerCase().includes('ativo') || userMessage.toLowerCase().includes('favorável')) {
        response = 'Analisando os ativos:\n\n• WIN: Tendência de ALTA, fluxo comprador forte\n• WDO: Lateralização, aguardar rompimento\n\nRecomendo atenção ao WIN nos próximos 15 minutos.';
      } else {
        response = `Entendi sua pergunta: "${userMessage}"\n\nCom base nos dados atuais, posso te dizer que o sistema está processando sinais em tempo real. Posso analisar com mais detalhes se você especificar sobre qual ativo ou período gostaria de informações.`;
      }

      setMessages(prev => [...prev, { role: 'assistant', content: response }]);
      setLoading(false);
    }, 1500);
  };

  const handleQuickQuestion = (question: string) => {
    setInput(question);
    handleSend();
  };

  return (
    <Layout>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 p-6 flex flex-col h-[calc(100vh-48px)]">
          <h1 className="text-2xl font-bold text-white mb-4">🤖 Assistente IA</h1>

          {/* Quick Questions */}
          <div className="mb-4">
            <p className="text-gray-400 text-sm mb-2">Pergunte sobre:</p>
            <div className="flex flex-wrap gap-2">
              {quickQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickQuestion(question)}
                  className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-cyan-400 text-sm rounded-lg transition border border-gray-700"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>

          {/* Chat Area */}
          <div className="flex-1 bg-gray-800 rounded-xl border border-gray-700 overflow-hidden flex flex-col">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-4 rounded-xl ${
                      message.role === 'user'
                        ? 'bg-cyan-500 text-gray-900'
                        : 'bg-gray-700 text-white'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      <span className="text-lg">
                        {message.role === 'user' ? '👤' : '🤖'}
                      </span>
                      <p className="whitespace-pre-line">{message.content}</p>
                    </div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-700 text-white p-4 rounded-xl">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">🤖</span>
                      <span className="animate-pulse">Pensando...</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-700">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Digite sua pergunta..."
                  className="flex-1 p-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  disabled={loading}
                />
                <button
                  onClick={handleSend}
                  disabled={loading || !input.trim()}
                  className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-600 disabled:cursor-not-allowed text-gray-900 font-bold rounded-lg transition"
                >
                  {loading ? '⏳' : '➤'}
                </button>
              </div>
            </div>
          </div>

          {/* Info Box */}
          <div className="mt-4 p-4 bg-blue-500/20 border border-blue-500/30 rounded-lg">
            <p className="text-blue-400 text-sm">
              💡 <strong>Nota:</strong> A IA não indica entrada ou saída. Ela fornece informações e contexto 
              para auxiliar suas decisões. Sempre utilize gestão de risco adequada.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
