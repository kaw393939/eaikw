# Eleventy Portfolio - Docker Setup

Complete Docker setup with development and production profiles, live reload, and nginx hosting.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose V2+
- Make (optional, recommended)

### Setup

1. **Create environment file:**
```bash
make setup
# or manually: cp .env.example .env
```

2. **Edit `.env` with your Docker Hub username:**
```bash
DOCKER_USERNAME=your-dockerhub-username
```

3. **Start development:**
```bash
make dev
# Access at http://localhost:8080
```

4. **Start production:**
```bash
make prod
# Access at http://localhost:80
```

## 📦 Available Commands

### Using Make (Recommended)

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make dev` | Start development with live reload |
| `make prod` | Start production with nginx |
| `make build` | Build production image |
| `make push` | Build and push to Docker Hub |
| `make test-prod` | Test production locally on port 8081 |
| `make stop` | Stop all containers |
| `make clean` | Stop and remove containers + volumes |
| `make logs` | Show all logs |
| `make logs-dev` | Show development logs |
| `make logs-prod` | Show production logs |
| `make shell-dev` | Open shell in dev container |
| `make shell-prod` | Open shell in prod container |

### Using NPM Scripts

```bash
npm run docker:dev      # Start development
npm run docker:prod     # Start production
npm run docker:stop     # Stop all containers
npm run docker:clean    # Clean up containers and volumes
```

### Using Docker Compose Directly

```bash
# Development
docker compose --profile dev up --build
docker compose --profile dev down

# Production
docker compose --profile production up -d
docker compose --profile production down
```

## 🔧 Development Environment

**Features:**
- ✅ Live reload on file changes
- ✅ Source files mounted as volumes
- ✅ Fast incremental builds
- ✅ Accessible at `http://localhost:8080`

**What's watched:**
- All files in `src/` directory
- Configuration changes in `.eleventy.js`
- Template changes auto-trigger rebuild

## 🏭 Production Environment

**Features:**
- ✅ Multi-stage optimized build
- ✅ Nginx web server with best practices
- ✅ Gzip compression enabled
- ✅ Static asset caching
- ✅ Security headers configured
- ✅ Health check endpoint at `/health`
- ✅ Accessible at `http://localhost:80`

## 🐳 Publishing to Docker Hub

### 1. Login
```bash
docker login
```

### 2. Build and Push
```bash
# Using Make
make push

# With version tag
VERSION=1.0.0 make push

# Using Docker Compose
docker compose build web
docker compose push web
```

### 3. Pull and Run
```bash
# Pull your published image
docker pull your-username/eleventy-portfolio:latest

# Run it
docker run -d -p 80:80 your-username/eleventy-portfolio:latest
```

## 📁 Docker Files Overview

- **Dockerfile** - Multi-stage production build with nginx
- **Dockerfile.dev** - Development with live reload
- **docker-compose.yml** - Orchestration with profiles
- **nginx.conf** - Production web server configuration
- **.dockerignore** - Exclude unnecessary files from build
- **Makefile** - Convenience commands
- **DOCKER.md** - Comprehensive documentation

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Development (8080)
lsof -ti:8080 | xargs kill -9

# Production (80)
sudo lsof -ti:80 | xargs kill -9
```

### Live Reload Not Working
```bash
# Enable polling
CHOKIDAR_USEPOLLING=true make dev
```

### View Logs
```bash
make logs           # All logs
make logs-dev       # Development logs
make logs-prod      # Production logs
```

### Clean Everything
```bash
make clean          # Remove containers and volumes
docker system prune -a  # Clean entire Docker system
```

## 📚 Documentation

See [DOCKER.md](./DOCKER.md) for comprehensive documentation including:
- Detailed command reference
- CI/CD integration examples
- Advanced configuration options
- Best practices
- Troubleshooting guide

## 🏗️ Architecture

### Development Flow
```
Source Files → Docker Volume → Eleventy --serve → Live Reload → Browser
     ↓
  File Watch
     ↓
  Auto Rebuild
```

### Production Flow
```
Source Files → Docker Build → Eleventy Build → Static Files → Nginx → Port 80
                    ↓
              Optimization
                    ↓
         Gzip + Cache Headers
```

## 🔐 Environment Variables

Configure in `.env`:

```bash
# Docker Hub username (required for publishing)
DOCKER_USERNAME=your-dockerhub-username

# Image version tag (default: latest)
VERSION=latest

# Node environment (default: production)
NODE_ENV=production
```

## 🎯 Best Practices

1. **Development:** Always use `make dev` for local work
2. **Testing:** Run `make test-prod` before pushing to Docker Hub
3. **Versioning:** Tag production images with semantic versions
4. **Security:** Never commit `.env` file with credentials
5. **Cleanup:** Run `make clean` periodically to free disk space

## 📊 Health Checks

Production container includes health monitoring:

```bash
# Check health status
docker compose --profile production ps

# Test health endpoint
curl http://localhost/health
```

## 🚢 Deployment Options

The Docker setup supports deployment to:
- Docker Hub
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Kubernetes
- Any container orchestration platform

## 📖 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Profiles](https://docs.docker.com/compose/profiles/)
- [Eleventy Documentation](https://www.11ty.dev/)
- [Nginx Configuration](https://nginx.org/en/docs/)
