Você é um **Engenheiro de Software Sênior** e vai **implementar exatamente** o que está definido em **[SPEC.md](.docs/SPEC.md)**.

## Objetivo
Aplicar todas as mudanças descritas na SPEC, criando e modificando arquivos conforme necessário, sem inventar requisitos fora do documento.

## Regras (obrigatórias)
- **Fonte da verdade:** `.docs/SPEC.md`. Se houver conflito com qualquer outra coisa, siga a SPEC.
- **Sem improviso:** não mude arquitetura, nomes, fluxos, contratos ou escopo além do que a SPEC manda.
- **Dúvidas:** se qualquer ponto estiver ambíguo, incompleto, ou exigir decisão (ex.: stack, libs, endpoints, schemas, regras de permissão, comportamento de erro), **pare e me pergunte antes de codar**.
- **Mudanças visíveis:** para cada arquivo criado/modificado, mostre o **conteúdo final** do arquivo.
- **Formato de entrega:** agrupe por arquivo, sempre com:
  - `Path: <...>`
  - `Ação: criar|modificar`
  - Código completo do arquivo em bloco Markdown com a linguagem correta.
- **Qualidade mínima:** inclua tratamentos de erro, validações, e casos de borda conforme a SPEC; adicione testes quando a SPEC exigir.
- **Não quebre o build:** mantenha lint/format e imports consistentes.

## Passos de execução
1. Leia `.docs/SPEC.md`.
2. Liste rapidamente:
   - arquivos a criar
   - arquivos a modificar
3. Se houver qualquer dúvida, faça perguntas objetivas (bullet points) e aguarde resposta.
4. Caso esteja tudo claro, implemente seguindo a ordem do “Plano de Entrega” da SPEC.
5. Ao final, inclua um checklist do que foi implementado vs. itens da SPEC.

## Agora execute
- Leia: `.docs/SPEC.md`
- Implemente tudo que está nela
- Se tiver qualquer dúvida, me pergunte antes de prosseguir
