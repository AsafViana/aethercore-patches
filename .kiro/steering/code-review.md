# Code Review Process

## Princípios

1. **Review é sobre o código, não sobre a pessoa**
2. **Seja específico** — aponte a linha, sugira a correção
3. **Priorize**: bugs > segurança > performance > legibilidade > estilo
4. **Aprove quando "bom o suficiente"** — perfeição não é o objetivo

## SLAs

| Tipo de PR | Tempo máximo para primeiro review |
|-----------|----------------------------------|
| Hotfix | 2 horas |
| Bug fix | 4 horas |
| Feature (< 300 linhas) | 8 horas |
| Feature (> 300 linhas) | 24 horas |

## Tamanho de PR

- **Ideal**: até 300 linhas alteradas
- **Máximo aceitável**: 500 linhas
- **Acima de 500**: dividir em PRs menores (exceto refactors mecânicos)

## Checklist do reviewer

### Obrigatório verificar
- [ ] Testes existem e cobrem o cenário principal
- [ ] Sem secrets ou dados sensíveis
- [ ] Migrations estão corretas e reversíveis
- [ ] Sem breaking changes não documentados
- [ ] Endpoints novos têm autorização configurada

### Desejável verificar
- [ ] Nomenclatura segue padrões do projeto
- [ ] Sem código morto ou comentado
- [ ] Logging adequado para troubleshooting
- [ ] Performance: sem N+1, sem carregamento desnecessário
- [ ] Error handling adequado

## Etiqueta

### Para quem abre o PR
- Descrição clara do que foi feito e por quê
- Link para a task/issue
- Screenshots se houver mudança visual
- Marcar se é WIP (draft PR)

### Para quem revisa
- Comentários construtivos com sugestão de melhoria
- Usar prefixos:
  - `[blocker]` — precisa corrigir antes de aprovar
  - `[suggestion]` — melhoria opcional
  - `[question]` — preciso entender melhor
  - `[nit]` — detalhe cosmético, não bloqueia
- Aprovar com comentários menores (não bloquear por nits)

## Aprovação

- Mínimo **1 aprovação** para merge
- PRs que alteram infra/segurança: **2 aprovações**
- Auto-merge habilitado após aprovação + CI verde
