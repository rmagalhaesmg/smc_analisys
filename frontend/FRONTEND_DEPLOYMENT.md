# Frontend Deployment Guide

This document describes how to build and deploy the React dashboard for the SMC SaaS application.

## Prerequisites

- Node.js (v18+ recommended)
- npm or yarn
- (Optional) Docker if you want to containerize the frontend

## Local Development

```bash
cd frontend
npm install      # or `yarn`
npm start        # starts development server on http://localhost:3000
```

The app reads `REACT_APP_API_URL` from your environment to know where the backend lives. You can create a `.env` file at the `frontend` root:

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000
```

## Production Build

```bash
cd frontend
npm run build   # outputs to `build/`
```

### Serve Locally

You can test the production bundle with a simple static server:

```bash
npm install -g serve
serve -s build -l 3000
```

## Docker Container

The included `Dockerfile.txt` shows a minimal container. To build and run:

```bash
cd frontend
cp Dockerfile.txt Dockerfile
# build image
docker build -t smc-frontend:latest .
# run container
docker run -d --name smc-frontend -p 3000:3000 smc-frontend:latest
```

Volume mounting is unnecessary since the build is baked into the image. Ensure the backend URL is injected via `REACT_APP_API_URL` at build time or via environment variables if using a multi‑stage build.

## Deployment Options

- **Vercel/Netlify**: Connect the Git repository and set environment variables; the platform will handle building and hosting automatically.
- **GitHub Pages**: Run `npm run build` and push the contents of `build/` to the `gh-pages` branch.
- **Static server**: Host the `build/` directory on any web server (NGINX, Apache, S3, etc.).

## Continuous Integration

Consider adding a CI pipeline (GitHub Actions, GitLab CI) to lint, test, and build the frontend on each push. A simple workflow could:

```yaml
name: Frontend CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - run: npm run build
      - run: echo "Build complete"
```

## Environment Variables

The frontend currently honors the following variables:

- `REACT_APP_API_URL` – backend base URL (required)
- `REACT_APP_API_TIMEOUT` – HTTP request timeout in milliseconds

Make sure these are configured in whichever hosting platform you choose.

---

With the UI built and the backend endpoints in place, users can log in, view plans, start checkout flows, and monitor/cancel subscriptions directly from the dashboard.