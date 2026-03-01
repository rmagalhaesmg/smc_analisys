# ⚡ Update Rápido no Railway

Seu código foi feito push! Agora Railway está redeployando automaticamente.

## 🔄 O que está acontecendo agora

1. **GitHub**: ✅ Código atualizado no main
2. **Railway**: 🔄 Build e deploy automático em andamento
3. **Backend**: Deploy será concluído em 2-5 minutos
4. **Frontend**: Deploy será concluído logo depois

---

## 🎯 Próximo Passo: Atualizar URL da API

### 1. Acesse o painel Railway
- Vá para [railway.app](https://railway.app)
- Faça login
- Clique no seu **projeto smc-analysis**

### 2. Vá para o serviço Frontend
- Clique em **frontend** (o serviço Node.js/React)
- Clique em **Variables** (ou Settings → Variables)

### 3. Atualize a variável de ambiente

**Procure por**: `REACT_APP_API_URL`

**Mude para**: A URL do seu backend (Exemplo: `https://smc-api-prod.railway.app`)

⚠️ **Não inclua `/api` no final! Deve ser apenas a URL base**

### 4. Redeploy

- Clique em **Trigger Deploy** ou **Redeploy**
- Aguarde 2-5 minutos
- Pronto! Frontend será redeployado com a nova URL

---

## 📋 Checklist de Verificação

Após redeploy completar:

### 1. Testar Backend
```bash
curl https://seu-url-backend.railway.app/api/system/status
```
Deve retornar JSON com status

### 2. Testar Frontend
- Abra URL do frontend no navegador
- Tela de login deve aparecer
- Tente fazer login com qualquer email/senha
- Dashboard deve carregar
- F12 → Console (não deve ter erros vermelhos)

### 3. Testar Conexão API
- No dashboard, abra DevTools (F12)
- Aba Network
- Clique em qualquer componente
- Deve ver requisições para sua API (status 200)

---

## 🆘 Se algo falhar

| Problema | Solução |
|----------|---------|
| **Frontend em branco** | Aguarde 5 min, faça F5 refresh |
| **Erro "Cannot connect"** | URL da API errada - verifique formato |
| **404 nas requisições API** | Endpoints não implementados no backend |
| **CORS error** | Backend precisa de ajuste CORS |

---

## ⏱️ Timeline Esperada

```
Agora          → Git push ✅
+0 min         → Railway detecta mudança
+2 min         → Build backend
+4 min         → Build frontend
+6 min         → Deploy completo
+7 min         → Você atualiza URL API
+10 min        → Redeploy frontend
+12 min        → Tudo online! 🎉
```

---

**Qual é sua URL do backend no Railway?** Preciso dela para completar a configuração! 🚀
