import Head from 'next/head';
import Link from 'next/link';
import { useState } from 'react';

export default function Landing() {
  const [loading, setLoading] = useState(false);

  const handleGetStarted = () => {
    setLoading(true);
    // Simulate redirect to login
    setTimeout(() => {
      window.location.href = '/login';
    }, 500);
  };

  return (
    <>
      <Head>
        <title>SMC Analysys - Leitura de Fluxo com Estatística Real</title>
        <meta name="description" content="Plataforma de análise de fluxo com inteligência artificial para trader" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800">
        {/* Header */}
        <header className="flex justify-between items-center px-8 py-4 bg-gray-900/80 backdrop-blur-sm fixed w-full z-50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-2xl">📊</span>
            </div>
            <span className="text-2xl font-bold text-white">SMC Analysys</span>
          </div>
          <div className="flex gap-4">
            <Link href="/login" className="px-5 py-2 text-cyan-400 hover:text-cyan-300 transition font-medium">
              Entrar
            </Link>
            <Link 
              href="/login" 
              className="px-5 py-2 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-bold rounded-lg transition"
            >
              Começar Agora
            </Link>
          </div>
        </header>

        {/* Hero Section */}
        <section className="pt-32 pb-20 px-8 text-center">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
              Leitura de Fluxo com
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500"> Estatística Real</span>
            </h1>
            <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
              Identifique padrões de fluxo, receba alertas em tempo real e tome decisões 
              baseadas em dados estatísticos reais do mercado.
            </p>
            <button 
              onClick={handleGetStarted}
              disabled={loading}
              className="px-10 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white text-xl font-bold rounded-xl hover:from-cyan-400 hover:to-blue-500 transition-all transform hover:scale-105 shadow-lg shadow-cyan-500/25"
            >
              {loading ? '⏳ Redirecionando...' : '🚀 Começar Agora'}
            </button>
          </div>
        </section>

        {/* How It Works */}
        <section className="py-20 px-8 bg-gray-800/50">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-white text-center mb-16">Como Funciona</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {/* Step 1 */}
              <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700 hover:border-cyan-500/50 transition">
                <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <span className="text-3xl">📥</span>
                </div>
                <h3 className="text-xl font-bold text-white text-center mb-4">1. Conecte seus Dados</h3>
                <p className="text-gray-400 text-center">
                  Conecte via CSV, RTD (Profit), DLL ou API Neológica. 
                  Nossa engine processa Times & Trades, Livro de Ofertas e Volume.
                </p>
              </div>

              {/* Step 2 */}
              <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700 hover:border-cyan-500/50 transition">
                <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <span className="text-3xl">🧠</span>
                </div>
                <h3 className="text-xl font-bold text-white text-center mb-4">2. Análise com IA</h3>
                <p className="text-gray-400 text-center">
                  Nossos módulos (HFZ, FBI, DTM, SDA, MTV) analisam o fluxo e 
                  calculam scores de probabilidade em tempo real.
                </p>
              </div>

              {/* Step 3 */}
              <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700 hover:border-cyan-500/50 transition">
                <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <span className="text-3xl">🔔</span>
                </div>
                <h3 className="text-xl font-bold text-white text-center mb-4">3. Receba Alertas</h3>
                <p className="text-gray-400 text-center">
                  Receba alertas no Telegram, E-mail ou WhatsApp quando 
                  uma oportunidade de alta probabilidade surge.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Plans Section */}
        <section className="py-20 px-8">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold text-white text-center mb-4">Escolha seu Plano</h2>
            <p className="text-gray-400 text-center mb-12">Tenha acesso a todos os recursos e inicie hoje mesmo</p>
            
            <div className="grid md:grid-cols-3 gap-8">
              {/* Monthly Plan */}
              <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700">
                <h3 className="text-2xl font-bold text-white mb-2">Mensal</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold text-cyan-400">R$199,90</span>
                  <span className="text-gray-400">/mês</span>
                </div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Dashboard em tempo real
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Alertas (Telegram/Email)
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Histórico completo
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Backtester
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Assistente IA
                  </li>
                </ul>
                <Link 
                  href="/login" 
                  className="block w-full py-3 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-bold text-center rounded-lg transition"
                >
                  Assinar
                </Link>
              </div>

              {/* Semester Plan - Recommended */}
              <div className="bg-gradient-to-b from-gray-800 to-gray-900 p-8 rounded-2xl border-2 border-cyan-500 relative transform scale-105">
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-cyan-500 text-gray-900 font-bold px-4 py-1 rounded-full text-sm">
                  MAIS POPULAR
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Semestral</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold text-cyan-400">R$999,90</span>
                  <span className="text-gray-400">/6 meses</span>
                  <div className="text-green-400 text-sm mt-1">Equivale a R$166,65/mês</div>
                </div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Dashboard em tempo real
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Alertas (Telegram/Email)
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Histórico completo
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Backtester
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Assistente IA
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Suporte prioritário
                  </li>
                </ul>
                <Link 
                  href="/login" 
                  className="block w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-center rounded-lg transition"
                >
                  Assinar
                </Link>
              </div>

              {/* Annual Plan */}
              <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700">
                <h3 className="text-2xl font-bold text-white mb-2">Anual</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold text-cyan-400">R$1.799,90</span>
                  <span className="text-gray-400">/ano</span>
                  <div className="text-green-400 text-sm mt-1">Equivale a R$149,99/mês</div>
                </div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Dashboard em tempo real
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Alertas (Telegram/Email)
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Histórico completo
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Backtester
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Assistente IA
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Suporte VIP
                  </li>
                  <li className="flex items-center gap-3 text-gray-300">
                    <span className="text-green-400">✓</span> Treinamento exclusivo
                  </li>
                </ul>
                <Link 
                  href="/login" 
                  className="block w-full py-3 bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-bold text-center rounded-lg transition"
                >
                  Assinar
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="py-20 px-8 bg-gray-800/50">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-white text-center mb-16">Recursos Principais</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="flex gap-4 items-start">
                <div className="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">📈</span>
                </div>
                <div>
                  <h4 className="text-lg font-bold text-white mb-2">Análise em Tempo Real</h4>
                  <p className="text-gray-400">Processamento de dados em milissegundos para identificar oportunidades instantaneamente.</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">🎯</span>
                </div>
                <div>
                  <h4 className="text-lg font-bold text-white mb-2">Múltiplos Indicadores SMC</h4>
                  <p className="text-gray-400">HFZ, FBI, DTM, SDA e MTV trabalhando em conjunto para maior precisão.</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">🔄</span>
                </div>
                <div>
                  <h4 className="text-lg font-bold text-white mb-2">Backtest Completo</h4>
                  <p className="text-gray-400">Teste suas estratégias com dados históricos e analise a assertividade.</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">🤖</span>
                </div>
                <div>
                  <h4 className="text-lg font-bold text-white mb-2">Assistente com IA</h4>
                  <p className="text-gray-400">Tire dúvidas sobre sinais, estatísticas e estratégias com nossa IA especializada.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-12 px-8 bg-gray-900 border-t border-gray-800">
          <div className="max-w-5xl mx-auto">
            <div className="flex flex-col md:flex-row justify-between items-center gap-6">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center">
                  <span className="text-xl">📊</span>
                </div>
                <span className="text-xl font-bold text-white">SMC Analysys</span>
              </div>
              <div className="flex gap-6 text-gray-400">
                <Link href="#" className="hover:text-cyan-400 transition">Termos de Uso</Link>
                <Link href="#" className="hover:text-cyan-400 transition">Privacidade</Link>
                <Link href="#" className="hover:text-cyan-400 transition">Contato</Link>
              </div>
              <div className="text-gray-500 text-sm">
                © 2024 SMC Analysys. Todos os direitos reservados.
              </div>
            </div>
            <div className="mt-8 pt-8 border-t border-gray-800 text-center text-gray-500 text-sm">
              <p>Este produto é para fins educacionais. Negociar envolve riscos.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
