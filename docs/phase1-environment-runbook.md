# Cognitive Platform

## Phase 1 Runbook --- AI Accelerated Development Environment

This document describes the complete setup and verification process for
Phase 1 of the Cognitive Platform roadmap.

Phase 1 establishes a fully functional AI systems engineering
workstation and prepares the local infrastructure required to build the
platform.

------------------------------------------------------------------------

# Objective

Prepare a development workstation capable of building and running the
Cognitive Platform locally.

The environment must support:

-   AI-assisted development
-   containerized services
-   local infrastructure
-   Python ML workloads
-   Java distributed systems components

------------------------------------------------------------------------

# Development Environment Architecture

    Developer Machine
    │
    ├── WSL Linux
    │
    ├── Development Tools
    │   ├ VS Code
    │   ├ Git
    │   ├ GitHub
    │   ├ GitHub Copilot
    │   └ Claude Code
    │
    ├── Language Runtimes
    │   ├ Python
    │   └ Java
    │
    ├── Container Runtime
    │   └ Docker
    │
    └── Platform Infrastructure
        ├ Postgres + pgvector
        ├ Redis
        ├ Prometheus
        └ Grafana

------------------------------------------------------------------------

# Phase 1 Stages

    Stage 1  WSL Linux Environment
    Stage 2  Development Workspace
    Stage 3  Git Repository Initialization
    Stage 4  IDE + AI Coding Tools
    Stage 5  Runtime Stack
    Stage 6  Infrastructure Containers

------------------------------------------------------------------------

# Stage 1 --- WSL Linux Environment

Install Windows Subsystem for Linux.

Verify installation:

``` bash
wsl -l -v
```

Expected output:

    Ubuntu    Running    2

Enter the Linux shell:

``` bash
wsl
```

Update packages:

``` bash
sudo apt update
sudo apt upgrade
```

------------------------------------------------------------------------

# Stage 2 --- Development Workspace

Create a consistent development workspace.

Recommended structure:

    ~/dev
    └── git
        └── cognitive-platform

Create directories:

``` bash
mkdir -p ~/dev/git
cd ~/dev/git
```

------------------------------------------------------------------------

# Stage 3 --- Git Repository Initialization

Create the repository:

``` bash
mkdir cognitive-platform
cd cognitive-platform
git init
```

Initial project structure:

    cognitive-platform
    ├ core
    ├ services
    ├ infra
    ├ models
    ├ datasets
    ├ docker
    ├ scripts
    ├ docs
    └ README.md

Initial commit:

``` bash
git add .
git commit -m "initial project structure"
```

Create GitHub repository and add remote:

``` bash
git remote add origin <repo-url>
git push -u origin main
```

------------------------------------------------------------------------

# Stage 4 --- IDE + AI Development Tools

Install Visual Studio Code.

Required extensions:

-   Python
-   Java Extension Pack
-   Docker
-   GitLens
-   Thunder Client
-   Remote WSL

Optional extensions:

-   Continue.dev
-   Error Lens

AI tools used:

-   GitHub Copilot
-   Claude Code
-   OpenAI tooling

Verify Copilot:

Create test file:

    scripts/test_copilot.py

Add prompt:

``` python
# write a fibonacci function
```

Copilot should suggest code.

------------------------------------------------------------------------

# Stage 5 --- Runtime Stack

Install language runtimes required by the platform.

## Python

Verify installation:

``` bash
python3 --version
```

Create virtual environment:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Verify pip:

``` bash
pip --version
```

------------------------------------------------------------------------

## Java

Install OpenJDK:

``` bash
sudo apt install openjdk-21-jdk
```

Verify:

``` bash
java -version
javac -version
```

------------------------------------------------------------------------

## Docker

Install Docker Engine:

``` bash
curl -fsSL https://get.docker.com | sudo sh
```

Allow current user to run Docker:

``` bash
sudo usermod -aG docker $USER
```

Restart WSL.

Start Docker service:

``` bash
sudo service docker start
```

Verify installation:

``` bash
docker --version
docker compose version
```

Test container runtime:

``` bash
docker run hello-world
```

------------------------------------------------------------------------

# Stage 6 --- Infrastructure Containers

Create the platform infrastructure stack using Docker Compose.

Create file:

    docker-compose.yml

Example configuration:

``` yaml
version: "3.9"

services:

  postgres:
    image: pgvector/pgvector:pg16
    container_name: cognitive-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: cognitive
      POSTGRES_PASSWORD: cognitive
      POSTGRES_DB: cognitive
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    container_name: cognitive-redis
    restart: unless-stopped
    ports:
      - "6379:6379"

  prometheus:
    image: prom/prometheus
    container_name: cognitive-prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    container_name: cognitive-grafana
    ports:
      - "3000:3000"

volumes:
  postgres_data:
```

Start infrastructure:

``` bash
docker compose up -d
```

Verify containers:

``` bash
docker ps
```

Expected:

-   cognitive-postgres
-   cognitive-redis
-   cognitive-prometheus
-   cognitive-grafana

------------------------------------------------------------------------

# Infrastructure Verification

## Postgres

``` bash
docker exec -it cognitive-postgres psql -U cognitive -d cognitive
```

Enable vector:

``` sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Create example table:

``` sql
CREATE TABLE cognitive_embeddings (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(384)
);
```

Exit:

    \q

------------------------------------------------------------------------

## Redis

``` bash
docker exec -it cognitive-redis redis-cli
```

Test:

    PING

Expected:

    PONG

Exit:

    exit

------------------------------------------------------------------------

## Prometheus

Open:

http://localhost:9090

------------------------------------------------------------------------

## Grafana

Open:

http://localhost:3000

Default credentials:

admin / admin

------------------------------------------------------------------------

# Phase 1 Completion Criteria

Phase 1 is complete when:

-   WSL Linux environment works
-   Git repository initialized
-   VS Code + AI tools configured
-   Python virtual environment active
-   Java installed
-   Docker installed
-   Postgres running
-   Redis running
-   Prometheus running
-   Grafana running
-   pgvector enabled

------------------------------------------------------------------------

# Result of Phase 1

The developer now has:

-   AI platform development workstation
-   Containerized local infrastructure
-   Vector database capability
-   Monitoring stack
-   Reproducible development environment

------------------------------------------------------------------------

# Next Phase

Phase 2 --- Platform Engineering

First service to implement:

    services/rag-service

This service will integrate:

-   FastAPI
-   Postgres + pgvector
-   Redis
-   Observability
