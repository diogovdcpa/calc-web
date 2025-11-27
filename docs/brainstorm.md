# Plataforma CalcWeb — Brainstorm Estruturado

## Visão geral
Plataforma para auxiliar arquitetos de soluções e engenheiros de pré-vendas a dimensionar BPS, GBS e EPS por projeto. Foco em cadastro rápido de sizings com geração de PDF e ações de edição/exclusão.

## Objetivo
- Permitir que usuários criem sizings contendo ativos detalhados.
- Padronizar arredondamento de quantidades para múltiplos de 1000.
- Oferecer exportação em PDF e manutenção (editar/excluir) dos sizings.

## Escopo (MVP)
- Fluxo de autenticação (cadastro/login) associado a uma empresa.
- Dashboard pós-login com CTA para criar novo sizing.
- Formulário de sizing com ativos (nome, quantidade, descrição) e arredondamento automático para cima em múltiplos de 1000.
- Ações após salvar: imprimir PDF, editar, excluir.

## Fora de escopo (por enquanto)
- Pagamentos, multi-idioma, permissões avançadas, integrações externas, automação de e-mail.

## Stack e padrões
- Flask com blueprints para controllers.
- ORM: SQLAlchemy + SQLite (arquivo local). Avaliar Alembic se surgirem migrações.
- MVC adaptado: controllers (regras e rotas), models (ORM), views (templates Jinja), static (assets).
- Deploy alvo: Vercel (WSGI). Manter inicialização minimalista no entrypoint.

## Estrutura de pastas proposta
```
app/
  __init__.py           # cria app, configura DB, registra blueprints
  settings.py           # configs de ambiente (DB path, secrets mínimos)
  db.py                 # instância do SQLAlchemy e helper de sessão
  models/
    __init__.py
    user.py
    company.py
    sizing.py
    asset.py
  controllers/
    __init__.py
    auth.py             # signup/login/logout
    sizing.py           # CRUD de sizing + exportação
  views/
    layout.html         # base
    auth/
      login.html
      signup.html
    sizing/
      index.html        # lista de sizings
      form.html         # criação/edição
      show.html         # exibição + ações
  static/
    css/, js/, imgs/
main.py                 # entrypoint Vercel importando app
```

## Modelo de domínio (rascunho)
- Usuario: nome, email, senha (hash), empresa_id.
- Empresa: nome.
- Sizing: titulo, descricao, empresa_id, usuario_id (criador), criado_em, atualizado_em.
- Ativo: sizing_id, nome, quantidade (arredondada para múltiplos de 1000), descricao.

## Fluxo principal do usuário
1) Cadastro com nome, email, senha e empresa.  
2) Login.  
3) Dashboard com opção de “Criar sizing”.  
4) Formulário de sizing: título, descrição e lista de ativos (nome, quantidade, descrição) com arredondamento automático da quantidade para cima em múltiplos de 1000.  
5) Salvar sizing.  
6) Tela de sizing com opções: Imprimir PDF, Editar, Excluir.

## Requisitos funcionais (MVP)
- RF01: Cadastro de usuário com vínculo a empresa.
- RF02: Login e sessão autenticada.
- RF03: Criar sizing com título/descrição.
- RF04: Adicionar/editar/remover ativos do sizing.
- RF05: Arredondar quantidade de ativo para múltiplos de 1000 (sempre para cima).
- RF06: Listar sizings do usuário/empresa.
- RF07: Exportar sizing em PDF.
- RF08: Editar/excluir sizing.

## Requisitos não funcionais
- RNF01: Persistência local via SQLite; fácil troca futura.
- RNF02: Organização MVC com blueprints.
- RNF03: Pronto para Vercel (WSGI, inicialização leve).
- RNF04: Templates Jinja simples; assets estáticos básicos (pode usar Tailwind CDN inicialmente).

## Backlog sugerido (ordem)
1) Setup Flask, SQLAlchemy, estrutura de pastas e settings.  
2) Models + migração inicial (ou script de criação).  
3) Autenticação básica (signup/login/logout).  
4) CRUD de sizing + ativos com arredondamento.  
5) Listagem/dashboard pós-login.  
6) Exportação PDF.  
7) Estilização mínima e validações.  
8) Deploy em Vercel.

## Perguntas em aberto
- Precisamos multi-empresa (usuários de empresas diferentes sem enxergar dados)?  
- Quem pode excluir sizings? Apenas criador ou qualquer usuário da empresa?  
- Template de PDF: layout esperado? Logo da empresa do usuário?  
- Há necessidade de papéis (admin vs comum)?

## Próximos passos
- Validar regras de permissão e escopo multi-empresa.  
- Fechar layout do PDF.  
- Definir se Alembic será adotado já no MVP.  
- Criar mockup rápido das telas (login, dashboard, form de sizing, show).
