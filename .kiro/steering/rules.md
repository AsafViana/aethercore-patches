# Regras Absolutas — .NET

> Violação de qualquer regra abaixo = PR rejeitado. Sem exceções.

## NUNCA

- ❌ NUNCA usar `var` quando o tipo não é óbvio pelo lado direito da atribuição
- ❌ NUNCA usar `.Result`, `.Wait()` ou `GetAwaiter().GetResult()` em código async
- ❌ NUNCA fazer `catch (Exception ex) { }` vazio (engolir exceções)
- ❌ NUNCA hardcodar connection strings, secrets ou tokens no código
- ❌ NUNCA commitar `appsettings.Development.json` com dados reais
- ❌ NUNCA usar `DateTime.Now` — usar `DateTime.UtcNow` ou `IDateTimeProvider`
- ❌ NUNCA retornar `null` de métodos que retornam coleções (retornar lista vazia)
- ❌ NUNCA expor entidades de domínio diretamente na API (usar DTOs)
- ❌ NUNCA usar `public` em campos de classe (usar propriedades)
- ❌ NUNCA fazer query N+1 (carregar coleções em loop)
- ❌ NUNCA usar `Thread.Sleep()` — usar `Task.Delay()` se necessário
- ❌ NUNCA ignorar CancellationToken em métodos async
- ❌ NUNCA commitar código comentado
- ❌ NUNCA deixar `Console.WriteLine` ou `Debug.WriteLine` em código de produção
- ❌ NUNCA usar `dynamic` sem justificativa documentada
- ❌ NUNCA criar controller com mais de 7 actions (dividir por responsabilidade)

## SEMPRE

- ✅ SEMPRE usar `async/await` para operações de I/O
- ✅ SEMPRE propagar `CancellationToken` do controller até o repositório
- ✅ SEMPRE validar input com FluentValidation antes de processar
- ✅ SEMPRE retornar tipos tipados nos controllers (`ActionResult<T>`)
- ✅ SEMPRE usar injeção de dependência (nunca `new` para serviços)
- ✅ SEMPRE documentar endpoints públicos com XML comments ou Swagger annotations
- ✅ SEMPRE usar `ILogger<T>` com structured logging
- ✅ SEMPRE criar migration para alterações de schema (nunca alterar DB manualmente)
- ✅ SEMPRE ter pelo menos um teste unitário por use case/service público
- ✅ SEMPRE usar `sealed` em classes que não foram projetadas para herança
- ✅ SEMPRE tratar erros com Result Pattern ou exceções tipadas (nunca string de erro)
- ✅ SEMPRE usar records para DTOs imutáveis
- ✅ SEMPRE configurar EF com Fluent API (não Data Annotations para mapeamento)
- ✅ SEMPRE paginar listagens (nunca retornar coleção inteira sem limite)
- ✅ SEMPRE usar `ConfigureAwait(false)` em libraries (não em controllers/endpoints)
