# FullStack Task Manager (Django + Vue)

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)](https://vuejs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Overview

Complete task management application featuring:

- **Backend**: Django REST Framework API
- **Frontend**: Vue.js 3 with Vuetify
- **Key Features**:
  - [x] Full CRUD task operations
  - [ ] JWT Authentication (in progress)
  - [ ] OpenAI integration
  - [ ] Automated Render deployment

## 🛠️ Tech Stack

### Backend
- **Django 5.2** - Python web framework
- **DRF** - REST API construction
- **MySQL 8.4** - Database (Docker recommended)
- **DRF Spectacular** - Swagger/OpenAPI docs
- **Pytest** - Test coverage >90%

### Frontend
- **Vue 3** - Composition API
- **Vuetify 3** - Material Design components
- **Axios** - API communication

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **Render** - Cloud deployment

## 🛠️ Prerequisites

### For Docker Setup (Recommended)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### For Hybrid Setup (Optional)
- **Backend**:
  - [uv](https://docs.astral.sh/uv/getting-started/installation) (alternative to pip)
  
- **Frontend**:
  - [Node.js](https://nodejs.org/) 22+
  - [bun](https://bun.sh/) (or npm/yarn/pnpm)

- **Database**:
  - MySQL 8.4 (via Docker recommended)

## 🚀 Getting Started

### Option 1: Full Docker Setup (Recommended)
```bash
git clone https://github.com/your-user/task-manager.git
cd task-manager
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
docker compose up -d
```

### Option 2: Hybrid Setup (DB in Docker Container)
General Setup
```bash
git clone https://github.com/your-user/task-manager.git
cd task-manager
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
docker compose up -d db

```
**Backend Setup**\
Change `MYSQL_HOST` to `0.0.0.0` in `backend/.env`\
Then run
```bash
# Inside /backend
uv sync --all-extras --dev
uv run src/manage.py migrate
uv run src/manage.py runserver
```

**Frontend setup (with `bun`)**
```bash
# Inside /frontend (in another terminal)
bun install --no-save
bun run dev
```

**Frontend setup with other package managers**
```bash
# Inside /frontend (in another terminal)

# With npm
npm install
npm run dev

# With yarn
yarn install
yarn run dev

# With pnpm
pnpm install
pnpm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Troubleshooting

### "Having trouble installing mysqlclient?"
Refer to the official installation guide for your platform:
- [mysqlclient PyPI documentation](https://pypi.org/project/mysqlclient/)
- [MySQL official connectors](https://dev.mysql.com/doc/connector-python/en/)

For most Linux systems, you'll need to install system dependencies first.

## 🌐 Coming Soon
- [ ] Live Demo on Render
- [ ] JWT Auth implementation guide
- [ ] OpenAI integration tutorial

## 📄 License

MIT