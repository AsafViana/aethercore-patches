# Technical Standards — .NET

## Arquitetura

### Padrão: Clean Architecture
```
src/
├── Domain/              # Entidades, Value Objects, Interfaces de repositório
├── Application/         # Use Cases, DTOs, Validators, Interfaces de serviço
├── Infrastructure/      # EF Core, Repositórios, Serviços externos
└── WebApi/              # Controllers, Middlewares, Filters, Program.cs
```

### Regras de dependência
- Domain não referencia nenhum outro projeto
- Application referencia apenas Domain
- Infrastructure referencia Application e Domain
- WebApi referencia todos (composition root)

## Convenções de código

### Nomenclatura
- Classes e métodos: PascalCase
- Variáveis locais e parâmetros: camelCase
- Interfaces: prefixo `I` (ex: `IUserRepository`)
- Constantes: PascalCase (não UPPER_SNAKE)
- Arquivos: mesmo nome da classe principal que contém

### Organização de classes
```csharp
public class MinhaClasse
{
    // 1. Campos privados
    // 2. Construtor
    // 3. Propriedades públicas
    // 4. Métodos públicos
    // 5. Métodos privados
}
```

### Async/Await
- Todo método que faz I/O deve ser async
- Sufixo `Async` em métodos async (ex: `GetUserAsync`)
- Nunca usar `.Result` ou `.Wait()` — sempre `await`
- Propagar CancellationToken em toda a cadeia

### Dependency Injection
- Registrar serviços por interface (não por classe concreta)
- Usar extension methods para organizar registros: `services.AddApplicationServices()`
- Scoped para serviços com estado por request
- Singleton para serviços stateless e thread-safe
- Transient apenas quando necessário criar nova instância a cada uso

## Entity Framework Core

### Configuração
- Usar Fluent API (não Data Annotations) para mapeamento
- Uma classe de configuração por entidade: `UserConfiguration : IEntityTypeConfiguration<User>`
- Migrations nomeadas descritivamente: `AddUserEmailIndex`

### Queries
- Usar projeção (`.Select()`) sempre que não precisar da entidade completa
- Nunca carregar coleções inteiras sem paginação
- Usar `.AsNoTracking()` para queries read-only
- Split queries para includes múltiplos: `.AsSplitQuery()`

## Testes

### Framework: xUnit + FluentAssertions + NSubstitute
```csharp
public class UserServiceTests
{
    [Fact]
    public async Task CreateUser_WithValidData_ShouldReturnSuccess()
    {
        // Arrange
        // Act
        // Assert
    }

    [Theory]
    [InlineData("", "email@test.com")]  // nome vazio
    [InlineData("John", "")]            // email vazio
    public async Task CreateUser_WithInvalidData_ShouldReturnValidationError(
        string name, string email)
    {
        // ...
    }
}
```

### Convenções de teste
- Nome: `MetodoSobTeste_Cenario_ResultadoEsperado`
- Arrange/Act/Assert separados por linha em branco
- Um assert lógico por teste (múltiplos asserts no mesmo objeto é ok)
- Testes de integração em projeto separado (`*.IntegrationTests`)
- Usar `WebApplicationFactory<Program>` para testes de API

## Performance

### Caching
- Usar `IMemoryCache` para dados que mudam raramente
- Usar `IDistributedCache` (Redis) para dados compartilhados entre instâncias
- Sempre definir expiração (nunca cache infinito)

### Paginação
- Toda listagem deve ser paginada por padrão
- Padrão: `pageSize=20`, máximo: `pageSize=100`
- Retornar metadata: `totalCount`, `pageSize`, `currentPage`, `totalPages`

## Logging

### Structured logging com Serilog
```csharp
_logger.LogInformation("User {UserId} created order {OrderId}", userId, orderId);
```
- Nunca interpolar strings em logs (usar placeholders)
- Levels: Debug (dev), Information (fluxo normal), Warning (recuperável), Error (falha)
- Nunca logar dados sensíveis (senhas, tokens, CPF completo)

## Segurança

- Validar todo input com FluentValidation
- Usar parameterized queries (EF Core já faz por padrão)
- Nunca expor stack traces em produção
- Usar `[Authorize]` explicitamente (não depender de filtro global sem entender)
- Secrets via Azure Key Vault ou User Secrets (nunca em appsettings.json)
