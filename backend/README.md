# Task Manager API

## 📌 Visão Geral

API Django REST Framework para gerenciamento de tarefas com:

- Autenticação JWT (em breve)
- CRUD completo de tasks
- Filtros e paginação (em breve)

## 🛠️ Tecnologias

### Backend Principal
- **Django** - Framework web Python
- **Django REST Framework** - Construção de APIs RESTful
- **MySQL 8.4** - Banco de dados relacional

### Testes & Qualidade
- **pytest + coverage** - Testes unitários e medição de cobertura de código
- **pyright** - Verificação estática de tipos

### Desenvolvimento
- **Docker** - Containers isolados para desenvolvimento
- **uv** - Gerenciador de pacotes ultra-rápido

### Documentação
- **DRF Spectacular** - Geração automática de documentação OpenAPI
- **Swagger UI** - Interface interativa para testar endpoints

## 🚀 Começando

### Pré-requisitos

- Python 3.13+
- MySQL 8.4
- UV (https://github.com/astral-sh/uv)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-user/task-manager.git

# Configure o ambiente
cd backend
cp .env.example .env

# Instale as dependências
uv sync --locked --all-extras --dev
```

## 🛠️ Comandos Úteis

```bash
# Rodar testes
make test

# Verificar tipos
make typecheck

# Aplicar migrações
make migrate
```

## 🌐 Endpoints

| Método   | Endpoint        | Descrição              |
| -------- | --------------- | ---------------------- |
| GET      | /api/tasks/     | Lista todas tasks      |
| POST     | /api/tasks/     | Cria nova task         |
| PATCH    | /api/tasks/{id} | Altera task de id `id` |
| DELETE   | /api/tasks/{id} | Deleta task de id `id` |


## 📄 Licença

MIT
