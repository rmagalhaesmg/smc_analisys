# 🔍 Como Encontrar suas URLs no Railway

## 1️⃣ Acessar Railway

Vá para: **https://railway.app**

---

## 2️⃣ Encontrar URL do Backend

1. Clique no seu **Projeto** (smc-analysis ou similar)
2. No painel à esquerda, clique em **backend** (ou o serviço Python/FastAPI)
3. Clique em **Deployments** ou **Overview**
4. Procure por uma seção tipo **"Service URL"** ou **"Domain"**
5. Copie a URL completa (algo como `https://smc-api-prod.railway.app`)

**✅ Pronto! Você tem sua URL da API**

---

## 3️⃣ Atualizar Frontend com essa URL

1. Clique em **frontend** (serviço Node.js/React)
2. Vá para **Variables** (em Settings ou Environment)
3. Procure por `REACT_APP_API_URL`
4. Cole sua URL do backend **SEM `/api` no final**

**Exemplo correto:**
```
REACT_APP_API_URL=https://smc-api-prod.railway.app
```

**Exemplo errado:**
```
REACT_APP_API_URL=https://smc-api-prod.railway.app/api  ❌
```

5. Clique em **Save**
6. Clique em **Trigger Deploy** ou **Redeploy**
7. Aguarde 2-5 minutos
8. Pronto! 🎉

---

## 📱 Teste Rápido

Abra a URL do frontend no navegador → Clique em "Dashboard" ou navegue → F12 (DevTools)

**Network**: Você deve ver requisições para sua URL do backend com status 200 ou 201

Se ver **CORS error**: Avise que o backend precisa de ajuste na configuração CORS

---

## 💡 Dica

Se não conseguir encontrar a URL, procure por:
- **"Domains"** na seção do serviço
- **"Generated Domain"** em railway.app
- Qualquer coisa como `*.railway.app`

---

**Compartilhe sua URL do backend aqui e vou validar se está correta!** ✅
