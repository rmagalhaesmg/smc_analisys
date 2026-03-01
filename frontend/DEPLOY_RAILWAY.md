# 🚀 Deploy via Railway (Guia Completo)

Railway é a melhor opção para deploy fácil! Aqui está o passo a passo.

## 📋 Pré-requisitos

- [ ] Conta GitHub (gratuita em github.com)
- [ ] Conta Railway (gratuita em railway.app)
- [ ] Git instalado localmente

---

## 🔧 Etapa 1: Preparar Repositório Git

### 1.1 Inicializar Git (se não tiver)
```bash
cd c:\Users\Usuário\Documents\smc_analysys
git init
git add .
git commit -m "Deploy inicial - SMC Analysis"
```

### 1.2 Criar Repositório no GitHub
1. Vá para [github.com/new](https://github.com/new)
2. Nome: `smc-analysis`
3. Descrição: `SMC Trading Analysis Platform`
4. Deixar **Público**
5. Criar repositório

### 1.3 Push para GitHub
```bash
git remote add origin https://github.com/SEU-USERNAME/smc-analysis.git
git branch -M main
git push -u origin main
```

---

## 🌐 Etapa 2: Deploy do Backend no Railway

### 2.1 Iniciar Railway
1. Vá para [railway.app](https://railway.app)
2. Faça login com GitHub (clique em "Login with GitHub")
3. Autorize Railway
4. Clique em **"Create Project"**

### 2.2 Selecionar Repositório
1. Escolha **"Deploy from GitHub repo"**
2. Selecione seu repositório `smc-analysis`
3. Clique em **Connect**

### 2.3 Configurar Variáveis de Ambiente
Railway detectará `Procfile` automaticamente.

Adicione as variáveis no painel Railway:

**Environment Variables** (copie-cole):
```
DATABASE_URL=postgresql://...  [OPCIONAL]
CORS_ORIGINS=https://seu-frontend.railway.app,http://localhost:3000
SECRET_KEY=sua-chave-secreta-aqui
LOG_LEVEL=INFO
```

### 2.4 Deploy
Railway fará deploy automaticamente quando você der push ao GitHub!

**Saída esperada** (no painel Railway):
```
✅ Build successful
✅ Deployment successful  
🌐 Service URL: https://smc-api-prod.railway.app
```

---

## 🔗 Etapa 3: Obter URL da API

1. Abra "Deployments" no painel Railway
2. Clique no seu backend
3. Copie a URL do tipo: `https://smc-api-prod.railway.app`

⚠️ **Importante**: Essa é sua URL da API em produção!

---

## 🎨 Etapa 4: Deploy do Frontend no Railway

### 4.1 Criar Nova Instância para Frontend

1. No painel Railway, clique **"New Project"**
2. Escolha **"Empty Project"**
3. Clique em **"Add Service"** → **"GitHub Repo"**
4. Selecione `smc-analysis` novamente

### 4.2 Configurar para Node.js/React

1. Clique em **"Generate from template"** (se aparecer)
2. Ou configure manualmente:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm install -g serve && serve -s build`

### 4.3 Configurar Variáveis de Ambiente

**Environment Variables**:
```
REACT_APP_API_URL=https://smc-api-prod.railway.app
REACT_APP_API_TIMEOUT=30000
NODE_ENV=production
```

⚠️ **Substitua `smc-api-prod.railway.app` pela URL real da sua API!**

### 4.4 Deploy
Railway fará deploy automaticamente ao novo push GitHub!

---

## ✅ Verificar Deploy

### 1. Testar Backend
```bash
curl https://smc-api-prod.railway.app/api/system/status
```

Esperado:
```json
{
  "status": "online",
  "version": "1.0.0"
}
```

### 2. Testar Frontend
Abra a URL do frontend no navegador (fornecida por Railway)

Esperado:
- Login aparece
- Pode fazer login
- Dashboard carrega
- Todos os componentes funcionam

### 3. Verificar Console (F12)
Não deve haver erros vermelhos

---

## 🚨 Solução de Problemas

### Erro: "Cannot GET /"
**Causa**: Frontend não foi compilado corretamente  
**Solução**:
```bash
cd frontend
npm install
npm run build
git add .
git commit -m "Fix: rebuild frontend"
git push
```

### Erro: "API connection failed"
**Causa**: REACT_APP_API_URL incorreta  
**Solução**:
1. Vá para painel Railway do frontend
2. Edite variável `REACT_APP_API_URL`
3. Copie URL exata do backend
4. Salve e redeploy

### Erro: "CORS error"
**Causa**: Backend bloqueando requisições do frontend  
**Solução**: No painel Railway do backend, ajuste:
```
CORS_ORIGINS=https://seu-frontend-url.railway.app
```

---

## 📊 Pipeline Completo

```
1. GitHub Repo
   ↓
2. Railroad detecta Procfile/package.json
   ↓
3. Build automático
   ├─ Backend (Python + FastAPI)
   └─ Frontend (Node.js + React)
   ↓
4. Deploy em produção
   ├─ Backend: https://smc-api-prod.railway.app
   └─ Frontend: https://smc-app-prod.railway.app
   ↓
5. Disponível 24/7! 🎉
```

---

## 📈 Monitorar em Produção

### Dashboard Railway
- Status dos serviços
- Logs em tempo real
- Uso de CPU/Memória
- Histórico de deploys

### Ativar Alertas (opcional)
Railway → Settings → Notifications

---

## 🔐 Segurança em Produção

### ✅ Fazer Isso:
- [ ] Usar HTTPS (Railway faz automaticamente)
- [ ] Usar variáveis de ambiente (não .env commited)
- [ ] Regular commits (Pipeline automático)
- [ ] Limpar dados sensíveis antes de commit
- [ ] Usar chaves secretas fortes

### ❌ NÃO fazer:
- Não commitar .env com senhas
- Não usar `localhost` em produção
- Não exposar chaves de API
- Não deixar debug=True

---

## 💡 Dicas Railway

### 1. **Auto-Deploy**
Cada push ao `main` redeploy automaticamente

### 2. **Rollback**
Se algo quebrar, Railway permite voltar versão anterior

### 3. **Custom Domain**
Em "Settings" → "Domain", adicione seu domínio próprio:
```
smc-api.seudominio.com
smc-app.seudominio.com
```

### 4. **Suporte Database**
Railway também hospeda PostgreSQL/MongoDB se precisar

---

## 📞 Se Precisar de Ajuda

| Problema | Link |
|----------|------|
| Status Railway | https://status.railway.app |
| Docs Railway | https://docs.railway.app |
| Discord Railway | https://discord.gg/railway |
| GitHub Issues | https://github.com/seu-repo/issues |

---

## 🎉 Próximas Etapas

1. ✅ Deploy backend → obter URL
2. ✅ Deploy frontend com URL correta
3. ✅ Testar login e navegação
4. ✅ Monitorar logs em tempo real
5. ✅ Ativar alertas
6. ✅ Configurar domínio customizado (opcional)

---

## 📋 Checklist Final

- [ ] GitHub repo criado
- [ ] Backend deployado no Railway
- [ ] API URL obtida
- [ ] Frontend deployado com URL correta
- [ ] Login funciona
- [ ] Todos componentes carregam
- [ ] F12 console sem erros
- [ ] 2-3 testes de navegação passaram
- [ ] Logs monitorados

---

**Pronto?** Comece pelo [resgistro no Railway](https://railway.app) e siga Etapa 1! 🚀
