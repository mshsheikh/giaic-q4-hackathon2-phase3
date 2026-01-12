# Deployment Scripts

This directory contains scripts for building, testing, and deploying the Todo AI Chatbot system.

## Available Scripts

### `build-all.sh`
Builds Docker images for all services in the system.

```bash
./scripts/build-all.sh
```

### `test-all.sh`
Runs tests for all components of the system (backend, MCP server, frontend).

```bash
./scripts/test-all.sh
```

### `deploy-dev.sh`
Deploys the system to a development environment using docker-compose.dev.yml.

```bash
./scripts/deploy-dev.sh
```

### `deploy-prod.sh`
Deploys the system to a production environment using docker-compose.prod.yml.

> **Note**: Set `DEPLOY_ENV=production` before running this script.

```bash
DEPLOY_ENV=production ./scripts/deploy-prod.sh
```

## Environment Variables

The deployment scripts rely on environment variables defined in `.env` files. Make sure to set up your environment variables before running deployment scripts.

## Docker Compose Files

- `docker/docker-compose.yml` - Default configuration for local development
- `docker/docker-compose.dev.yml` - Configuration optimized for development
- `docker/docker-compose.prod.yml` - Configuration for production deployment