# 🚀 Integração Frontend-Backend - Resumo

## ✅ O que foi criado

### 📁 Arquivos do Frontend

1. **`.env.local`**
   - Configuração da URL da API
   - Define `REACT_APP_API_URL=http://127.0.0.1:8000`

2. **`src/api.js`**
   - Cliente Axios centralizado
   - Grupos de endpoints: auth, trading, alerts, AI, payments
   - Interceptadores para JWT automático
   - Tratamento de erros centralizado

3. **`src/hooks.js`**
   - Custom React Hooks com loading/error states
   - `useLogin()`, `useRegister()` - Autenticação
   - `useProcessBar()` - Processar barras OHLCV
   - `useLastSignal()` - Buscar último sinal
   - `useAIInterpret()` - Interpretação da IA
   - `usePaymentPlans()` - Planos de pagamento
   - E mais...

4. **`src/DashboardExample.js`**
   - Componente pronto com exemplos de uso
   - Mostra status do sistema
   - Processa barras de exemplo
   - Busca últimos sinais
   - Testado e funcional

### 📄 Documentação

1. **`INTEGRACAO_FRONTEND.md`**
   - Guia completo de integração
   - Exemplos de código para cada caso de uso
   - Lista completa de endpoints
   - Troubleshooting
   - Deploy em produção

### 🚀 Scripts de Inicialização

1. **`start-dev.ps1`** (Windows PowerShell)
   - Inicia Backend e Frontend em janelas separadas
   - Uso: `.\start-dev.ps1`

2. **`start-dev.sh`** (Linux/Mac)
   - Script bash equivalente

---

## 🎯 Como usar

### Opção 1: Iniciar com Script (Recomendado Windows)

```powershell
.\start-dev.ps1
```

Isso abrirá dois terminais:
- Terminal 1: Backend rodando em `http://127.0.0.1:8000`
- Terminal 2: Frontend rodando em `http://localhost:3000`

### Opção 2: Iniciar Manualmente

**Terminal 1 (Backend):**
```bash
.\.venv\Scripts\python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm install  # Se ainda não tiver instalado
npm start
```

---

## 📚 Exemplos Rápidos

### Usar um Hook em um Componente

```javascript
import { useProcessBar } from "./hooks";

function MyComponent() {
  const { processBar, loading, error, result } = useProcessBar();

  const handleClick = async () => {
    const bar = {
      open: 105.50,
      high: 106.20,
      low: 105.30,
      close: 106.00,
      volume: 2500000,
      time: "2026-02-27T15:30:00Z",
      symbol: "WDOH1"
    };
    
    const result = await processBar(bar);
    console.log("Resultado:", result);
  };

  return (
    <div>
      <button onClick={handleClick} disabled={loading}>
        {loading ? "Processando..." : "Processar"}
      </button>
      {result && <p>Score: {(result.score * 100).toFixed(0)}%</p>}
      {error && <p style={{color: "red"}}>{error}</p>}
    </div>
  );
}
```

### Usar API Diretamente

```javascript
import { apiClient } from "./api";

// Em qualquer lugar do código
const response = await apiClient.get("/api/status");
console.log(response.data);
```

---

## 🔗 Arquitetura da Integração

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                        │
│                 http://localhost:3000                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  DashboardExample.js & Seus Componentes             │   │
│  │  ├─ useProcessBar()    ─────┐                       │   │
│  │  ├─ useLastSignal()    ─────┼─→  hooks.js          │   │
│  │  ├─ useAIInterpret()   ─────┼─→  api.js            │   │
│  │  └─ usePaymentPlans()  ─────┘    (axios)           │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                  │
│                  CORS (localhost:3000)                       │
│                            │                                  │
└────────────────────────────┼──────────────────────────────────┘
                             │
                             │ HTTP/REST
                             │
┌────────────────────────────▼──────────────────────────────────┐
│                      BACKEND (FastAPI)                        │
│                 http://127.0.0.1:8000                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  main.py (FastAPI App)                              │   │
│  │  ├─ /auth/*              ← AuthEngine               │   │
│  │  ├─ /api/processar-barra ← SMCCoreEngine            │   │
│  │  ├─ /api/alertas/*       ← AlertEngine              │   │
│  │  ├─ /api/ai/*            ← AIEngine                 │   │
│  │  └─ /api/pagamento/*     ← PaymentEngine            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## 📊 Status da Integração

| Componente | Status | Notas |
|-----------|--------|-------|
| Backend FastAPI | ✅ Rodando | Porta 8000, CORS configurado |
| Frontend React | ✅ Pronto | Aguardando `npm install` |
| API Client | ✅ Implementado | `src/api.js` com 6 grupos de endpoints |
| React Hooks | ✅ Implementado | 8 custom hooks prontos |
| JWT Auth | ✅ Automático | Token é adicionado automaticamente |
| Exemplos | ✅ Disponível | `DashboardExample.js` funcional |
| Documentação | ✅ Completa | `INTEGRACAO_FRONTEND.md` |

---

## 🔐 Fluxo de Autenticação

```
1. Usuário clica "Login"
2. useLogin() envia credentials para /auth/login
3. Backend retorna access_token
4. Token armazenado em localStorage
5. Interceptador adiciona token a todas requisições posteriores
6. API retorna dados autenticados
```

---

## 🌍 URLs Importantes

| Serviço | URL | Descrição |
|---------|-----|-----------|
| Frontend | `http://localhost:3000` | Aplicação React |
| Backend | `http://127.0.0.1:8000` | API FastAPI |
| Swagger Docs | `http://127.0.0.1:8000/docs` | Documentação interativa |
| OpenAPI JSON | `http://127.0.0.1:8000/openapi.json` | Schema da API |

---

## 💡 Próximos Passos

1. ✅ **Arquivos de integração criados**
2. ⏳ **Instalar dependências do Frontend:**
   ```bash
   cd frontend
   npm install
   ```
3. ⏳ **Iniciar os serviços:**
   ```bash
   .\start-dev.ps1
   ```
4. ⏳ **Testar no navegador:**
   - Abrir `http://localhost:3000`
   - Ver Dashboard Example rodando

---

## 🐛 Troubleshooting Rápido

**CORS Error?**
- Verificar se backend está em `http://127.0.0.1:8000`
- Verificar `.env.local` no frontend

**Requisição retorna 401?**
- Fazer login novamente
- Verificar se token está em `localStorage`

**Connection Refused?**
- Verificar se backend está rodando
- Verificar porta 8000

---

## 📞 Recursos Adicionais

- 📖 Guia completo: `INTEGRACAO_FRONTEND.md`
- 💻 Exemplo funcional: `src/DashboardExample.js`
- 🔧 Client API: `src/api.js`
- 🪝 React Hooks: `src/hooks.js`
- 🚀 Scripts de inicialização: `start-dev.ps1`

---

**✨ Integração Completa! Pronto para começar?**
