# CalcWeb — Plataforma de dimensionamento BPS/GBS/EPS

Plataforma web para arquitetos de soluções e pré-vendas criarem sizings com ativos, aplicando arredondamento de quantidades para múltiplos de 1000, com exportação em HTML/PDF-ready.

## Principais funcionalidades
- Autenticação com vínculo a empresa (signup/login/logout).
- CRUD de sizings com título, descrição e lista de ativos.
- Arredondamento automático de quantidade de ativos para múltiplos de 1000.
- Exportação simples em HTML (base para PDF) e ações de editar/excluir.

## Stack e arquitetura
- Flask (blueprints), Jinja2 para views.
- SQLAlchemy + SQLite (padrão) — `create_all()` na inicialização.
- Estilo custom no layout base; pronto para WSGI (Gunicorn/Vercel).

Estrutura resumida:
```
app/
  controllers/ (auth, sizing)
  models/ (user, company, sizing, asset)
  templates/ (auth, sizing, layout)
  settings.py / db.py / __init__.py (app factory)
main.py (entrypoint WSGI)
```

## Pré-requisitos
- Python 3.9+.
- pip ou uv para instalar dependências.

## Configuração e execução local
```bash
python -m venv .venv
source .venv/bin/activate
pip install flask flask-sqlalchemy gunicorn

# Variáveis de ambiente (opcional, veja abaixo)
export SECRET_KEY="sua-chave"
# export DATABASE_URL="postgresql+psycopg://user:pass@host/db"
# export SQLITE_PATH="/tmp/calcweb.sqlite"

# Executar em modo dev
flask --app main run --reload
# ou em modo WSGI
gunicorn main:app
```
A aplicação sobe em `http://127.0.0.1:5000` (Flask) ou `http://127.0.0.1:8000` (Gunicorn).

## Variáveis de ambiente
- `SECRET_KEY`: chave de sessão/flash (obrigatória em produção).
- `DATABASE_URL`: URL de banco (use Postgres/MySQL para produção).
- `SQLITE_PATH`: caminho do SQLite quando `DATABASE_URL` não for fornecida (default: `/tmp/calcweb.sqlite`, ideal para ambientes serverless).

## Deploy (Vercel ou WSGI)
- O entrypoint é `main:app`.
- Em ambientes serverless, o SQLite usa `/tmp` (armazenamento efêmero). Para persistência, configure `DATABASE_URL` para um banco gerenciado.

## Fluxos principais
- `/auth/signup` · Cadastro com empresa.
- `/auth/login` · Autenticação.
- `/sizings` · Dashboard e CRUD de sizings/ativos, exportação HTML para impressão/PDF.
