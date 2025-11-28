# Progresso do projeto CalcWeb

## Histórico (checklist)
- [x] Estrutura Flask com app factory, blueprints (auth, sizing), modelos SQLAlchemy (User, Company, Sizing, Asset), templates Jinja e layout base.
- [x] CRUD de sizings/ativos com arredondamento p/ múltiplos de 1000, export HTML, autenticação e sessão.
- [x] Ajuste do `main.py` para usar app factory e manter blueprint de API.
- [x] SQLite em `/tmp` para ambiente serverless (`DATABASE_URL`/`SQLITE_PATH` configuráveis).
- [x] README revisado com visão geral, stack, fluxos, execução local, variáveis e deploy.
- [x] Fluxo Git: branch `develop`, feature `feature/brainstorm-mvp`, merges em `develop` e `main`, remoção da feature.
- [x] Convenção: sempre criar features a partir de `develop`; criada e mergeada `feature/readme-profissional` em `develop`.
