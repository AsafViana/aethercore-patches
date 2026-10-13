# Quality Gates

## Gate 1: PR (antes do merge)

### Automático (CI)
- [ ] Build compila sem erros
- [ ] Todos os testes unitários passam
- [ ] Análise estática (SonarQube/Roslyn analyzers) sem bloqueadores
- [ ] Sem vulnerabilidades críticas em dependências (Snyk/Dependabot)
- [ ] Code coverage não diminuiu (mínimo 70% em código novo)

### Manual (reviewer)
- [ ] Pelo menos 1 aprovação
- [ ] Sem comentários `[blocker]` pendentes
- [ ] PR segue template e convenções

## Gate 2: Develop → Main (release candidate)

### Automático
- [ ] Todos os testes de integração passam
- [ ] Smoke tests passam no ambiente de staging
- [ ] Nenhum TODO crítico no código
- [ ] Migrations executam sem erro em banco limpo

### Manual
- [ ] QA validou os cenários principais
- [ ] Release notes documentadas
- [ ] Aprovação do Tech Lead

## Gate 3: Main → Produção (deploy)

### Automático
- [ ] Health check do serviço responde 200
- [ ] Métricas de erro não aumentaram nos primeiros 5 min
- [ ] Rollback automático se error rate > 5%

### Manual
- [ ] GMUD aprovada (se aplicável)
- [ ] Comunicação ao time feita
- [ ] Monitoramento ativo por 30 min pós-deploy

## Exceções

- **Hotfix crítico**: pode pular Gate 2 com aprovação de 2 seniors
- **Rollback**: não precisa de PR, mas precisa de post-mortem em 24h

## Métricas monitoradas

| Métrica | Threshold | Ação se violado |
|---------|-----------|-----------------|
| Code coverage (novo código) | < 70% | PR bloqueado |
| Vulnerabilidades críticas | > 0 | PR bloqueado |
| Build time | > 10 min | Investigar |
| Testes flaky | > 2% | Fix obrigatório na sprint |
| Tempo médio de review | > 24h | Escalar |
