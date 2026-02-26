# SMC Web App - Docker Deployment Guide

## Overview

This guide explains how to containerize and deploy the SMC Web App using Docker.

## Prerequisites

- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)
- `.env` file configured with your settings

## Quick Start

### 1. Build and Run with Docker Compose (Recommended)

```powershell
cd c:\Users\Usuário\Documents\smc_analysys\backend

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f smc-api

# Stop the service
docker-compose down
```

### 2. Build Docker Image Manually

```powershell
cd c:\Users\Usuário\Documents\smc_analysys\backend

# Build the image
docker build -t smc-api:latest .

# Run the container
docker run -d `
  --name smc-api `
  -p 8000:8000 `
  -v smc-data:/app/smc.db `
  -v smc-uploads:/app/uploads `
  --env-file .env `
  smc-api:latest

# View logs
docker logs -f smc-api

# Stop the container
docker stop smc-api
docker rm smc-api
```

## Access the Application

After deployment:

- **API Swagger UI**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Configuration

### Environment Variables

Create/edit `.env` file in the backend directory:

```env
# Application
APP_NAME=SMC - Sistema de Monitoramento Contínuo
APP_VERSION=2.3.0
DEBUG=False

# API
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=sqlite:///./smc.db

# Notifications (optional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_IDS=
SENDGRID_API_KEY=
TWILIO_ACCOUNT_SID=
OPENAI_API_KEY=
```

## Docker Compose Services

### Current Setup

- **smc-api**: FastAPI backend service on port 8000

### Optional Services (Commented)

Uncomment in `docker-compose.yml` to enable:

**PostgreSQL Database**
```yaml
db:
  image: postgres:16-alpine
  environment:
    - POSTGRES_DB=smc_db
    - POSTGRES_USER=smc_user
    - POSTGRES_PASSWORD=your_password
```

**Nginx Reverse Proxy**
```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
```

## Volume Management

### Named Volumes

```powershell
# List volumes
docker volume ls

# Inspect volume
docker volume inspect smc-data

# Remove unused volumes
docker volume prune
```

### Persistent Data Locations

- **Database**: `smc-data` volume → `/app/smc.db`
- **Uploads**: `smc-uploads` volume → `/app/uploads`

## Common Commands

```powershell
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Check container logs
docker logs smc-api
docker logs -f smc-api  # Follow logs

# Execute command in container
docker exec -it smc-api bash

# Restart service
docker-compose restart smc-api

# Rebuild image
docker-compose build --no-cache

# Remove containers and volumes
docker-compose down -v
```

## Health Checks

The container includes a built-in health check:

```powershell
# Check container health
docker ps --format "{{.Names}}\t{{.Status}}"

# Should show: "smc-api (healthy)" if running correctly
```

## Production Deployment

### AWS ECS

```bash
# Tag image
docker tag smc-api:latest YOUR_AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/smc-api:latest

# Push to ECR
docker push YOUR_AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/smc-api:latest
```

### Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT/smc-api
gcloud run deploy smc-api --image gcr.io/YOUR_PROJECT/smc-api
```

### Azure Container Instances

```bash
az acr build --registry YOUR_REGISTRY --image smc-api:latest .
az container create --resource-group YOUR_RG --name smc-api \
  --image YOUR_REGISTRY.azurecr.io/smc-api:latest --ports 8000 \
  --dns-name-label smc-api
```

### Docker Hub

```bash
# Tag image
docker tag smc-api:latest YOUR_USERNAME/smc-api:latest

# Login to Docker Hub
docker login

# Push image
docker push YOUR_USERNAME/smc-api:latest
```

## Kubernetes Deployment

### Create k8s manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smc-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: smc-api
  template:
    metadata:
      labels:
        app: smc-api
    spec:
      containers:
      - name: smc-api
        image: smc-api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: smc-config
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: smc-api-service
spec:
  selector:
    app: smc-api
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Deploy to Kubernetes

```bash
kubectl apply -f deployment.yaml
kubectl get services
```

## Troubleshooting

### Container won't start

```powershell
# Check logs
docker logs smc-api

# Check image exists
docker images

# Verify .env file
cat .env
```

### Port already in use

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (if needed)
taskkill /PID <PID> /F

# Or use different port in docker-compose.yml
# Change "8000:8000" to "8001:8000"
```

### Database connection issues

```powershell
# Verify volume
docker volume inspect smc-data

# Check database file permissions
docker exec smc-api ls -la smc.db
```

### Performance issues

```powershell
# Check resource usage
docker stats smc-api

# Increase memory in docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

## Files Reference

- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration
- `.dockerignore` - Files to exclude from build
- `.env` - Environment variables (not committed)
- `requirements.txt` - Python dependencies

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [Best Practices for Node.js/Python Containers](https://snyk.io/blog/10-best-practices-for-nodejs-docker/)

## Support

For issues or questions:
1. Check container logs: `docker logs smc-api`
2. Verify configuration: `cat .env`
3. Test API endpoint: `curl http://localhost:8000/health`
4. Review this guide's troubleshooting section
