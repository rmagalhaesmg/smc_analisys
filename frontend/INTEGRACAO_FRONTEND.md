# Guia de Integração Frontend-Backend

## 📋 Resumo

O frontend React está integrado com o backend FastAPI rodando em `http://127.0.0.1:8000`. Este guia explica como usar a API do backend no frontend.

---

## 🚀 Início Rápido

### 1. Instalar Dependências do Frontend

```bash
cd frontend
npm install
```

### 2. Iniciar o Frontend

```bash
npm start
```

O React abrirá em `http://localhost:3000`

### 3. Certificar que o Backend está Rodando

```bash
# Terminal separado
.\.venv\Scripts\python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

---

## 🔧 Arquivos de Integração

### `.env.local` (Frontend)

Define a URL da API:

```env
REACT_APP_API_URL=http://127.0.0.1:8000
REACT_APP_API_TIMEOUT=30000
```

**Mude para produção (Railway):**
```env
REACT_APP_API_URL=https://smcanalisys-production.up.railway.app
```

### `src/api.js`

Cliente Axios centralizado com suporte a:
- Interceptadores de request/response
- Autenticação JWT automática
- Grupos de endpoints (auth, trading, AI, payments)

### `src/hooks.js`

Custom React Hooks com estados (loading, error, data):
- `useApi()` - Hook genérico
- `useLogin()` - Autenticação
- `useProcessBar()` - Processar barras OHLCV
- `useLastSignal()` - Último sinal
- `useAIInterpret()` - Interpretação da IA
- `usePaymentPlans()` - Planos de pagamento

---

## 📚 Exemplos de Uso

### Exemplo 1: Login

```javascript
import { useLogin } from "./hooks";

function LoginPage() {
  const { login, loading, error } = useLogin();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await login("usuario@example.com", "senha123");
      console.log("Login bem-sucedido!", response);
      // Redirecionar para dashboard
    } catch (err) {
      console.error("Erro de login:", error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input type="email" placeholder="Email" required />
      <input type="password" placeholder="Senha" required />
      <button disabled={loading}>{loading ? "Entrando..." : "Login"}</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}

export default LoginPage;
```

### Exemplo 2: Processar uma Barra OHLCV

```javascript
import { useProcessBar } from "./hooks";

function TradingPanel() {
  const { processBar, loading, error, result } = useProcessBar();

  const handleProcessBar = async () => {
    const bar = {
      open: 105.50,
      high: 106.20,
      low: 105.30,
      close: 106.00,
      volume: 2500000,
      time: "2026-02-27T15:30:00Z",
      symbol: "WDOH1"
    };

    try {
      const signal = await processBar(bar);
      console.log("Resultado da análise:", signal);
      // signal contém: score, direction, filters, hfz, fbi, dtm, sda, mtv, etc.
    } catch (err) {
      console.error("Erro ao processar barra:", error);
    }
  };

  return (
    <div>
      <button onClick={handleProcessBar} disabled={loading}>
        {loading ? "Processando..." : "Processar Barra"}
      </button>
      {result && (
        <div>
          <p>Score: {(result.score * 100).toFixed(0)}%</p>
          <p>Direção: {result.direction === 1 ? "📈 ALTA" : "📉 BAIXA"}</p>
        </div>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default TradingPanel;
```

### Exemplo 3: Buscar Último Sinal

```javascript
import { useLastSignal } from "./hooks";
import { useEffect } from "react";

function SignalDisplay() {
  const { fetch, loading, error, signal } = useLastSignal("WDOH1");

  useEffect(() => {
    fetch(); // Buscar ao montar componente
  }, []);

  if (loading) return <p>Carregando sinal...</p>;
  if (error) return <p style={{ color: "red" }}>Erro: {error}</p>;

  return signal ? (
    <div>
      <h3>Último Sinal - {signal.symbol}</h3>
      <p>Score: {(signal.score * 100).toFixed(0)}%</p>
      <p>Qualidade: {signal.qualidade}</p>
      <p>Time: {signal.time}</p>
    </div>
  ) : (
    <p>Nenhum sinal disponível</p>
  );
}

export default SignalDisplay;
```

### Exemplo 4: Planos de Pagamento

```javascript
import { usePaymentPlans, useCheckout } from "./hooks";
import { useEffect } from "react";

function PricingPage() {
  const { fetch, plans, loading } = usePaymentPlans();
  const { checkout } = useCheckout();

  useEffect(() => {
    fetch();
  }, []);

  if (loading) return <p>Carregando planos...</p>;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "20px" }}>
      {plans.map((plan) => (
        <div key={plan.id} style={{ border: "1px solid #ccc", padding: "20px" }}>
          <h3>{plan.name}</h3>
          <p>R$ {plan.price}</p>
          <p>{plan.description}</p>
          <button
            onClick={() => {
              checkout(plan.id);
            }}
          >
            Contratar
          </button>
        </div>
      ))}
    </div>
  );
}

export default PricingPage;
```

### Exemplo 5: Usar API Diretamente (sem hook)

```javascript
import { apiClient, tradingAPI, authAPI } from "./api";

// Qualquer lugar no código
async function verificarStatus() {
  try {
    const response = await apiClient.get("/api/status");
    console.log("Status:", response.data);
  } catch (error) {
    console.error("Erro:", error);
  }
}

// Ou usar os grupos de API
async function obterPerfil() {
  try {
    const perfil = await authAPI.getProfile();
    console.log("Perfil do usuário:", perfil.data);
  } catch (error) {
    console.error("Erro ao buscar perfil:", error);
  }
}
```

---

## 🔐 Autenticação JWT

O sistema usa JWT (JSON Web Tokens) para autenticação:

1. **Login** → Sistema retorna `access_token`
2. **Token é armazenado** em `localStorage`
3. **Interceptador automático** adiciona token a toda requisição: `Authorization: Bearer <token>`
4. **Token expirado?** Usuário é redirecionado para `/login`

```javascript
// O token é automaticamente adicionado a todas as requisições
// Nenhuma ação adicional necessária!
```

---

## 📡 Endpoints Disponíveis

### Auth (Autenticação)
```
POST   /auth/register              - Registrar novo usuário
POST   /auth/login                 - Login
POST   /auth/refresh               - Atualizar token
GET    /auth/verify-email          - Verificar email
POST   /auth/forgot-password       - Recuperação de senha
POST   /auth/reset-password        - Resetar senha
GET    /auth/me                    - Obter perfil do usuário
```

### Trading (Análise)
```
POST   /api/processar-barra        - Processar uma barra OHLCV
GET    /api/ultimo-sinal/{ativo}   - Último sinal do ativo
```

### Alerts (Alertas)
```
GET    /api/alertas/log            - Log de alertas
GET    /api/alertas/stats          - Estatísticas de alertas
```

### AI (Inteligência Artificial)
```
GET    /api/ai/interpretar/{ativo} - Interpretação da IA para ativo
POST   /api/ai/chat                - Chat com IA
GET    /api/ai/relatorio/{ativo}   - Relatório da IA
```

### Payments (Pagamentos)
```
GET    /api/planos                 - Lista de planos
POST   /api/pagamento/checkout     - Iniciar checkout
GET    /api/pagamento/status       - Status do pagamento
GET    /api/pagamento/historico    - Histórico de pagamentos
POST   /api/pagamento/cancelar     - Cancelar pagamento
```

---

## 🛠️ Troubleshooting

### ❌ CORS Error
**Problema:** `Access to XMLHttpRequest blocked by CORS`

**Solução:** O backend já tem CORS configurado. Certifique-se que:
1. Backend está rodando em `http://127.0.0.1:8000`
2. `.env.local` aponta para a URL correta

### ❌ 401 Unauthorized
**Problema:** Requisição retorna 401

**Solução:** 
1. Verificar se o token está no `localStorage`
2. Fazer login novamente
3. Verificar se o token não expirou

### ❌ Network Error
**Problema:** `Network Error` ou `Connection Refused`

**Solução:**
1. Verificar se o backend está rodando: `http://127.0.0.1:8000`
2. Verificar porta (deve ser 8000)
3. Verificar firewall

### ❌ Timeout
**Problema:** Requisição demora muito (timeout)

**Solução:**
1. Aumentar `REACT_APP_API_TIMEOUT` em `.env.local`
2. Verificar se o backend está processando corretamente

---

## 📦 Variáveis de Ambiente Disponíveis

```env
# Backend URL
REACT_APP_API_URL=http://127.0.0.1:8000

# Timeout das requisições (ms)
REACT_APP_API_TIMEOUT=30000

# Para adicionar mais variáveis:
# 1. Adicionar em .env.local
# 2. Iniciar com REACT_APP_
# 3. Acessar em JavaScript via process.env.REACT_APP_NOME
```

---

## 🚀 Deployment

### Produção (Railway)

1. **Backend já está deployado** em: `https://smcanalisys-production.up.railway.app`

2. **Deploy Frontend:**

```bash
# 1. Build para produção
npm run build

# 2. Deploy no Railway (ou outro serviço)
# Ver instruções no painel do Railway
```

3. **Atualizar URL da API:**

```env
REACT_APP_API_URL=https://smcanalisys-production.up.railway.app
```

---

## 📞 Suporte

- **Documentação Interativa**: http://127.0.0.1:8000/docs
- **Schema OpenAPI**: http://127.0.0.1:8000/openapi.json

---

**✅ Integração Completa! Backend e Frontend estão prontos para funcionar juntos.**
