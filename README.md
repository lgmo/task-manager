# FullStack Task Manager (Django + Vue)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Vue](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)
![Vuetify](https://img.shields.io/badge/Vuetify-1867C0?style=for-the-badge&logo=vuetify&logoColor=white)

## 📌 Overview

Complete task management application featuring:

- **Backend**: Django REST Framework API
- **Frontend**: Vue.js interface
- **Key Features**:
  - [ ] JWT Authentication
  - [x] Full CRUD task operations
  - [ ] OpenAI integration for smart suggestions
  - [ ] Automated Render deployment

## 🛠️ Tech Stack

### Backend
- **Django** - Python web framework
- **DRF** - REST API construction
- **MySQL 8.4** - Relational database
- **OpenAI SDK** - AI integration

### Frontend
- **Vue 3** - JavaScript framework
- **Axios** - API communication
- **Tailwind CSS** - Styling

### DevOps
- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **Render** - Deployment platform

## 🚀 Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.8.6+
- [Node.js](https://nodejs.org/en/download) 22+
- [MySQL](https://dev.mysql.com/doc/refman/8.4/en/installing.html) 8.4
- [bun](https://bun.com/docs/installation) 1.2.19+ (or other **javasript** package manager)

### Installation

Clone repository
```bash
git clone https://github.com/your-user/task-manager.git
```
Backend Setup
```bash
# Inside /backend
cp .env.example .env
uv sync --locked --all-extras --dev
```
Frontend setup (bun)
```bash 
# Inside /frontend
bun install --no-save
```
Frontend setup (alternatives)
```bash
# Inside /frontend
npm install
```
```bash
# Inside /frontend
yarn
```
```bash
# Inside /frontend
pnpm install
```

## 🌐 Live Access (coming soon)

- **API Documentation**: [Swagger UI]()
- **Live Demo**: [Frontend on Render]()

## 📄 License

MIT