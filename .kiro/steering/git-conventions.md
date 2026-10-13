# Git Conventions

## Branching Strategy

### Branches principais
- `main` — produção, sempre deployável
- `develop` — integração, base para features

### Branches de trabalho
```
feature/TASK-123-descricao-curta
bugfix/BUG-456-descricao-curta
hotfix/HOT-789-descricao-curta
release/v1.2.0
```

### Regras
- Sempre criar branch a partir de `develop` (exceto hotfix → `main`)
- Deletar branch após merge
- Nunca push direto em `main` ou `develop`

## Commits

### Formato: Conventional Commits
```
tipo(escopo): descrição curta

corpo opcional explicando o porquê

refs: TASK-123
```

### Tipos permitidos
| Tipo | Quando usar |
|------|-------------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `refactor` | Refatoração sem mudança de comportamento |
| `test` | Adição ou correção de testes |
| `docs` | Documentação |
| `chore` | Manutenção (deps, configs, CI) |
| `perf` | Melhoria de performance |
| `style` | Formatação (sem mudança de lógica) |

### Regras de commit
- Descrição em português ou inglês (manter consistência no repo)
- Máximo 72 caracteres na primeira linha
- Imperativo: "adiciona filtro" (não "adicionado" ou "adicionando")
- Um commit = uma mudança lógica
- Nunca commitar arquivos gerados (bin/, obj/, .vs/)

## Pull Requests

### Título
```
tipo(escopo): descrição curta [TASK-123]
```

### Descrição (template)
```markdown
## O que foi feito
Breve descrição da mudança.

## Por quê
Contexto e motivação.

## Como testar
Passos para validar.

## Checklist
- [ ] Testes passando
- [ ] Migration criada (se aplicável)
- [ ] Documentação atualizada (se aplicável)
```

### Merge strategy
- **Squash merge** para features (histórico limpo)
- **Merge commit** para releases (preservar histórico)
- **Rebase** nunca em branches compartilhadas
