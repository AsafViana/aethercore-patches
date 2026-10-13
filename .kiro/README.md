# .kiro — Starter Kit (.NET)

Este diretório contém a configuração do Kiro IDE para um projeto .NET/C#.

## Estrutura

```
.kiro/
├── steering/
│   ├── product.md          → Contexto do projeto
│   ├── tech.md             → Regras técnicas da stack .NET
│   ├── rules.md            → Regras absolutas (NUNCA/SEMPRE)
│   ├── code-review.md      → Processo de review
│   ├── git-conventions.md  → Branching, commits, PRs
│   └── quality-gates.md    → Gates de qualidade progressivos
├── hooks/
│   ├── on-save.json        → Feedback ao salvar arquivos .cs
│   └── pre-commit.json     → Validação antes de escrever código
└── README.md               → Este arquivo
```

## Como usar

1. Copie a pasta `.kiro/` para a raiz do seu repositório .NET
2. Edite `steering/product.md` com o contexto do seu projeto
3. Revise `steering/tech.md` e ajuste libs/padrões se necessário
4. Revise `steering/rules.md` e adicione/remova regras do seu time
5. Abra o projeto no Kiro IDE — pronto!

## Customização

### Steering files
Os arquivos `.md` em `steering/` são lidos pelo Kiro como contexto. 
Escreva em linguagem natural, seja específico e direto.

### Hooks
Os hooks em `hooks/` disparam ações automáticas:
- `on-save.json` → roda quando você salva um arquivo
- `pre-commit.json` → roda quando o Kiro vai escrever código

Edite os `outputPrompt` para ajustar o que o Kiro verifica.

## Evolução

As regras devem evoluir com o time:
1. Abra um PR alterando o arquivo relevante
2. Justifique a mudança
3. Após aprovação, merge normalmente
