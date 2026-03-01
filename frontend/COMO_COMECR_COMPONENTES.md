# 🚀 Como Integrar Seus Próprios Componentes

## 📁 Estrutura de Componentes Criada

```
frontend/src/
├── components/
│   ├── LoginComponent.js        ← Login com autenticação
│   ├── TradingComponent.js      ← Análise de barras OHLCV
│   ├── SignalsComponent.js      ← Monitoramento de sinais
│   └── ...seus componentes
├── App.js                        ← Seu App atual
├── App-example.js                ← Exemplo com todos os componentes
├── DashboardExample.js           ← Dashboard de teste
├── api.js                        ← Cliente API
├── hooks.js                      ← Hooks reutilizáveis
└── ...
```

---

## ✅ Passo 1: Ver os Componentes Criados

### 1. **LoginComponent** (`src/components/LoginComponent.js`)
- Formulário de login completo
- Usa `useLogin()` hook
- Suporta validação de email
- Armazena email no `localStorage`

### 2. **TradingComponent** (`src/components/TradingComponent.js`)
- Interface para processar barras OHLCV
- Inputs para Open, High, Low, Close, Volume
- Mostra resultados detalhados da análise
- Exibe scores HFZ, FBI, DTM, etc.

### 3. **SignalsComponent** (`src/components/SignalsComponent.js`)
- Monitora sinais em tempo real
- Suporta múltiplos símbolos (tabs)
- Auto-atualiza a cada 10 segundos
- Mostra barra de progresso do score

---

## 🎯 Passo 2: Usar o App com Todos os Componentes

### Opção A: Substituir App.js (Mais Rápido)

```bash
# Terminal no frontend
cp src/App-example.js src/App.js
```

Isso abrirá seu app com navegação entre:
- 📊 Dashboard
- 📈 Trading
- 📊 Sinais
- 🔐 Login

### Opção B: Copiar do App-example.js Manualmente

Abra `src/App-example.js` e copie:
- O navbar
- A lógica de páginas
- A estrutura de roteamento manual

---

## 📝 Passo 3: Criar Seus Próprios Componentes

### Template Básico

```javascript
/**
 * MyCustomComponent.js
 * Descrição do que faz
 */

import { useTermoDoHook } from "../hooks";

function MyCustomComponent() {
  const { fetch, loading, error, data } = useTermoDoHook();

  return (
    <div style={{ background: "#1a1a2e", padding: "20px", borderRadius: "10px" }}>
      <h2 style={{ color: "#00d4ff" }}>🎯 Meu Componente</h2>
      
      {loading && <p>⏳ Carregando...</p>}
      {error && <p style={{ color: "#ff6b6b" }}>❌ {error}</p>}
      {data && <p style={{ color: "#00ff88" }}>✅ {JSON.stringify(data)}</p>}
    </div>
  );
}

export default MyCustomComponent;
```

### Exemplo: Novo Componente com useProcessBar

```javascript
/**
 * MyTradingAnalyzer.js
 * Analisador customizado
 */

import { useState } from "react";
import { useProcessBar } from "../hooks";

function MyTradingAnalyzer() {
  const { processBar, loading, result } = useProcessBar();
  const [symbol, setSymbol] = useState("WDOH1");
  const [price, setPrice] = useState(105.50);

  const handleAnalyze = async () => {
    const bar = {
      open: price - 0.50,
      high: price + 0.20,
      low: price - 1.00,
      close: price,
      volume: 2000000,
      symbol,
      time: new Date().toISOString(),
    };

    const analysis = await processBar(bar);
    if (analysis.score > 0.7) {
      console.log("🎯 Signal encontrado!");
      // Aqui você pode enviar um alerta, salvar, etc
    }
  };

  return (
    <div style={{ background: "#1a1a2e", padding: "20px" }}>
      <h3>🎯 Meu Analisador</h3>
      
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="Symbol"
        style={{ padding: "10px", marginRight: "10px" }}
      />
      
      <input
        type="number"
        value={price}
        onChange={(e) => setPrice(parseFloat(e.target.value))}
        placeholder="Price"
        step="0.01"
        style={{ padding: "10px", marginRight: "10px" }}
      />
      
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analisando..." : "Analisar"}
      </button>

      {result && (
        <p>
          Score: <strong>{((result.score || 0) * 100).toFixed(0)}%</strong>
        </p>
      )}
    </div>
  );
}

export default MyTradingAnalyzer;
```

---

## 🪝 Passo 4: Usar os Hooks Disponíveis

### Hooks Disponíveis em `src/hooks.js`

#### Autenticação
```javascript
import { useLogin, useRegister } from "./hooks";

const { login, loading, error } = useLogin();
const { register } = useRegister();
```

#### Trading
```javascript
import { useProcessBar, useLastSignal } from "./hooks";

const { processBar, loading, result } = useProcessBar();
const { fetch, signal } = useLastSignal("WDOH1");
```

#### AI & Payments
```javascript
import { useAIInterpret, usePaymentPlans } from "./hooks";

const { fetch: fetchInterpretation } = useAIInterpret("WDOH1");
const { fetch: fetchPlans, plans } = usePaymentPlans();
```

---

## 🎨 Passo 5: Estilos e Temas

### Paleta de Cores do Projeto

```javascript
const THEME = {
  background: "#0f0f1a",      // Fundo escuro
  card: "#1a1a2e",             // Fundo dos cards
  border: "#333",              // Bordas
  primary: "#00d4ff",          // Azul claro (ativo)
  success: "#00ff88",          // Verde
  warning: "#ffd700",          // Ouro
  danger: "#ff6b6b",           // Vermelho
  muted: "#888",               // Texto cinzento
};
```

### Exemplo de Uso

```javascript
const containerStyle = {
  background: THEME.card,
  borderRadius: "10px",
  padding: "20px",
  border: `1px solid ${THEME.border}`,
  color: "#fff",
};
```

---

## 📚 Passo 6: Boas Práticas

### ✅ Faça

```javascript
// ✅ Use hooks para state management
import { useProcessBar } from "./hooks";

function MyComponent() {
  const { processBar, loading, error, result } = useProcessBar();
  // ...
}

// ✅ Sempre trate loading e error
{loading && <p>⏳</p>}
{error && <p style={{ color: "#ff6b6b" }}>{error}</p>}
{result && <p style={{ color: "#00ff88" }}>✅</p>}

// ✅ Use a paleta de cores consistente
style={{ color: "#00d4ff" }}  // Para destaque
style={{ color: "#888" }}      // Para labels

// ✅ Organize componentes em pastas
src/components/
  ├── LoginComponent.js
  ├── TradingComponent.js
  └── custom/
      └── MyComponent.js
```

### ❌ Evite

```javascript
// ❌ Não use URL da API diretamente
fetch("http://127.0.0.1:8000/api/...")  // ❌

// ✅ Use os hooks ou api.js
const { processBar } = useProcessBar();

// ❌ Não ignore loading/error states
{result && <p>{result}</p>}  // ❌

// ✅ Sempre trate todos os states
{loading && <p>Loading...</p>}
{error && <p>{error}</p>}
{result && <p>{result}</p>}
```

---

## 🔄 Passo 7: Adicionar ao App.js

Depois de criar seu componente, adicione ao App:

```javascript
// 1. Importe
import MyCustomComponent from "./components/MyCustomComponent";

// 2. Adicione à navegação (se usar roteamento manual)
const APP_PAGES = {
  MY_PAGE: "mypage",
  // ...
};

// 3. Adicione link na navbar
<a onClick={() => setCurrentPage(APP_PAGES.MY_PAGE)}>
  Minha Página
</a>

// 4. Renderize
{currentPage === APP_PAGES.MY_PAGE && <MyCustomComponent />}
```

---

## 📦 Passo 8: Integração com Backend

### Endpoints Disponíveis

```javascript
// Trading
POST /api/processar-barra          // Processar OHLCV
GET  /api/ultimo-sinal/{symbol}    // Último sinal

// Auth
POST /auth/login                    // Login
POST /auth/register                 // Registro
GET  /auth/me                       // Perfil

// Alerts
GET  /api/alertas/log               // Log de alertas
GET  /api/alertas/stats             // Estatísticas

// AI
GET  /api/ai/interpretar/{symbol}   // Interpretação
POST /api/ai/chat                   // Chat com IA

// Payments
GET  /api/planos                    // Planos
POST /api/pagamento/checkout        // Checkout
```

### Usar Diretamente

```javascript
import { apiClient, tradingAPI } from "./api";

// Via hooks (Recomendado)
const { processBar } = useProcessBar();
await processBar(barData);

// Ou direto
const result = await tradingAPI.processBar(barData);

// Ou com apiClient
const response = await apiClient.post("/api/processar-barra", barData);
```

---

## 🧪 Passo 9: Testar Localmente

```bash
# 1. Garantir que backend está rodando
# Terminal 1: Backend
.\.venv\Scripts\python -m uvicorn backend.main:app --reload

# 2. Garantir que frontend está rodando
# Terminal 2: Frontend
cd frontend && npm start

# 3. Abrir no navegador
# http://localhost:3000
```

---

## 🚀 Passo 10: Deploy

### Build para Produção

```bash
cd frontend
npm run build
```

Isso cria a pasta `build/` pronta para deploy.

### Deploy no Railway (Exemplo)

1. Commit suas mudanças
2. Push para Git
3. Railway detecta automaticamente e deploya

---

## 📖 Arquivos de Referência

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `App-example.js` | App completo com navegação | Copie ou use como referência |
| `components/LoginComponent.js` | Login funcional | Copie ou customize |
| `components/TradingComponent.js` | Trading com OHLCV | Use ou customize |
| `components/SignalsComponent.js` | Signals em tempo real | Use ou customize |
| `hooks.js` | Todos os hooks | Importe nos seus componentes |
| `api.js` | Client Axios | Use para chamadas diretas |

---

## 💡 Dicas Finais

1. **Comece simples** - Copie LoginComponent e customize
2. **Reutilize hooks** - Não faça axios calls direto
3. **Siga a paleta de cores** - Manter consistência visual
4. **Teste no navegador** - F12 para ver erros
5. **Use localStorage** - Para dados persistentes (tokens, preferências)
6. **Documente seu código** - Comments ajudam no futuro

---

## 🎉 Próximo Passo

```bash
# 1. Visualizar o App-example
# 2. Copiar App-example.js para App.js
# 3. Navegar entre as página no localhost:3000
# 4. Customizar os componentes para suas necessidades
# 5. Criar novos componentes seguindo o padrão
```

**Pronto para começar! 🚀**
