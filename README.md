# AetherCore Patches

Colecao de patches MCP para o AetherCore, com exemplos prontos para uso e um patch instalador que gerencia downloads, instalacao e atualizacao. O repositorio tambem inclui o script de build do registro remoto e os artefatos de distribuicao (ZIPs).

## Destaques

- Patches MCP via STDIO (JSON-RPC) prontos para uso no AetherCore.
- Patch installer para listar, instalar, atualizar e remover patches a partir do registro remoto.
- Script de build que gera `generated/patches.json` e empacota zips em `dist/`.

## Patches incluidos

| Pasta | Nome (manifest) | Namespace | Descricao curta |
| --- | --- | --- | --- |
| `patches/echo/` | `echo` | `debug` | Ecoa texto recebido via `debug.echo`. |
| `patches/notes/` | `notes` | `notes` | CRUD simples de notas locais em JSON. |
| `patches/mqtt/` | `mqtt` | `mqtt` | Bridge MQTT com publish e subscribe_once. |
| `patches/installer/` | `installer` | `installer` | Gerenciador de patches via registro remoto. |

## Estrutura do repositorio

- `patches/` - Patches MCP (cada patch contem `manifest.yaml` e `server.py`).
- `scripts/build_registry.py` - Gera ZIPs e o registro `generated/patches.json`.
- `generated/patches.json` - Lista remota consumida pelo patch `installer`.
- `dist/` - Artefatos ZIP gerados para distribuicao.

## Requisitos gerais

- Python 3.x para executar os patches (cada patch define seu entrypoint em `manifest.yaml`).
- Dependencias por patch:
  - `installer`: `requests` e `PyYAML`.
  - `mqtt`: `paho-mqtt`.

## Como usar no AetherCore

1) Instale o patch (manual ou via installer).
2) Inicie o AetherCore com o patch habilitado.
3) Liste tools e chame via namespace.

Exemplo no REPL do AetherCore:

```bash
# listar tools do patch
AetherCore> tools notes

# chamar tool
AetherCore> run notes notes.add title="Ideias" content="Lembrar de revisar o patch installer"
```

## Patch installer

O patch `installer` consulta o registro remoto em `generated/patches.json` e baixa os ZIPs publicados em `dist/`.

Ferramentas:

- `list_remote`
- `list_installed`
- `install` (`patch_name=...`)
- `uninstall` (`patch_name=...`)
- `update` (`patch_name=...`)
- `sync` (`patch_name=...`)

Exemplos:

```bash
AetherCore> run installer list_remote
AetherCore> run installer install patch_name="notes"
AetherCore> run installer list_installed
AetherCore> run installer update patch_name="notes"
AetherCore> run installer uninstall patch_name="notes"
```

Observacoes:

- O `installer` usa `PATCHES_REPO_URL` em `patches/installer/server.py`.
- Se precisar apontar para outro repositorio, ajuste essa URL e regenere o ZIP.

## Patch echo

Tool disponivel:

- `debug.echo` -> recebe `{ "text": "..." }` e devolve o mesmo texto.

Exemplo:

```bash
AetherCore> run debug debug.echo text="teste"
```

## Patch notes

Armazena notas como JSON em `data/notes_storage/` (criada automaticamente).

Ferramentas:

- `notes.add` (title, content)
- `notes.list`
- `notes.search` (query)

Exemplo:

```bash
AetherCore> run notes notes.add title="Checklist" content="Revisar README"
AetherCore> run notes notes.list
AetherCore> run notes notes.search query="README"
```

## Patch mqtt

Configurar o broker no arquivo `patches/mqtt/server.py`:

```python
BROKER_HOST = "192.168.0.10"
BROKER_PORT = 1883
MQTT_CLIENT_ID = "aethercore_mqtt_client"
```

Ferramentas:

- `mqtt_publish` (topic, payload, qos?, retain?)
- `mqtt_subscribe_once` (topic, timeout?)

Exemplo:

```bash
AetherCore> run mqtt mqtt_publish topic="esp32/cmd" payload="LED_ON"
AetherCore> run mqtt mqtt_subscribe_once topic="esp32/sensores" timeout=5
```

## Registry remoto e distribuicao

O script `scripts/build_registry.py`:

- Varre `patches/*`.
- Le `manifest.yaml` e opcionalmente a descricao do README do patch.
- Gera ZIPs em `dist/` com a estrutura `patches/<nome>/...`.
- Atualiza `generated/patches.json` com nome, versao, descricao e URL de download.

Para gerar:

```bash
python scripts/build_registry.py
```

Variaveis de ambiente suportadas:

- `AETHERCORE_REPO_USER`
- `AETHERCORE_REPO_NAME`
- `AETHERCORE_REPO_BRANCH`

## Criando um novo patch

1) Crie uma pasta em `patches/<meu_patch>/`.
2) Adicione `manifest.yaml` com `name`, `version`, `transport`, `entrypoint` e `tools_namespace`.
3) Implemente `server.py` com JSON-RPC via STDIO (methods `tools/list` e `tools/call`).
4) Opcional: adicione `README.md` para descricao curta.
5) Rode `python scripts/build_registry.py` para gerar ZIP e atualizar o registro.

Exemplo de `manifest.yaml`:

```yaml
name: "meu_patch"
version: "0.1.0"
transport: "stdio"
entrypoint:
  command: "python3"
  args:
    - "patches/meu_patch/server.py"
tools_namespace: "meu"
```

## Troubleshooting

- Confirme que o `entrypoint` no `manifest.yaml` aponta para o Python correto (em Windows pode ser `.venv/Scripts/python.exe`).
- Se o `installer` falhar ao baixar, verifique conectividade e a URL em `PATCHES_REPO_URL`.
- No `mqtt`, valide host, porta e permissao de rede para o broker.

## Licenca

Nao especificada neste repositorio.
