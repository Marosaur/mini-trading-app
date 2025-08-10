# Mini Trading App

A containerized mock trading simulator built to explore DevOps methodologies and CI/CD practices. This full-stack application demonstrates modern deployment patterns with Docker and Kubernetes.

## 🏗️ Architecture

- **Frontend**: React + Vite (JavaScript/CSS)
- **Backend**: FastAPI with SQLAlchemy ORM (Python)  
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes single-node cluster

## ✨ Features

- Create and manage trading orders (buy/sell)
- Execute pending orders
- RESTful API with FastAPI
- Responsive React frontend
- PostgreSQL persistence
- Health checks and database connectivity

## 🚀 Deployment Options

### Docker Compose (Development)
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Kubernetes (Production-like)
```bash
kubectl apply -f k8s/
```
- Frontend: http://localhost:30080
- Backend API: http://localhost:30081

## 📁 Project Structure

```
├── frontend/          # React application
│   ├── src/
│   └── frontend.Dockerfile
├── backend/           # FastAPI application  
│   ├── main.py
│   ├── requirements.txt
│   └── backend.Dockerfile
├── k8s/              # Kubernetes manifests
│   ├── frontend.yaml
│   ├── backend.yaml
│   └── postgres.yaml
└── docker-compose.yml
```

## 🎯 Current DevOps Implementation

- ✅ **Containerization**: Multi-stage Docker builds
- ✅ **Container Orchestration**: Kubernetes deployment with services
- ✅ **Service Communication**: Inter-container networking
- ✅ **Database Integration**: PostgreSQL with persistent storage
- ✅ **Health Checks**: Application readiness probes

## 🔄 Next Steps

### Phase 1: GitOps & Multi-Environment
- [ ] Implement GitOps workflow with ArgoCD/Flux
- [ ] Multi-cluster setup (dev/staging/prod)
- [ ] Terraform Infrastructure as Code

### Phase 2: Observability & Monitoring  
- [ ] Prometheus + Grafana monitoring stack
- [ ] Centralized logging with ELK/Loki
- [ ] Distributed tracing implementation

### Phase 3: DevSecOps Integration
- [ ] Container vulnerability scanning
- [ ] SAST/DAST security testing
- [ ] Policy enforcement with OPA Gatekeeper

### Phase 4: Advanced Automation
- [ ] Advanced CI/CD pipelines with Jenkins/GitLab
- [ ] Automated testing and quality gates
- [ ] Service mesh with Istio

---

*This project serves as a hands-on learning platform for enterprise-grade DevOps practices in financial technology environments.*