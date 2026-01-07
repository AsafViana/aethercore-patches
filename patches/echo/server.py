#!/usr/bin/env python3
import sys
import json

def send(msg: dict):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def handle_request(req: dict):
    method = req.get("method")
    req_id = req.get("id")

    # Resposta padrão de erro
    def error(message: str):
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": message}}

    # tools/list
    if method == "tools/list":
        result = {
            "tools": [
                {
                    "name": "debug.echo",
                    "description": "Ecoa o texto recebido.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Texto a ser ecoado"}
                        },
                        "required": ["text"],
                        "additionalProperties": False
                    }
                }
            ]
        }
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    # tools/call
    if method == "tools/call":
        params = req.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}

        if name != "debug.echo":
            return error(f"Tool desconhecida: {name}")

        text = arguments.get("text")
        if not isinstance(text, str):
            return error("Campo 'text' é obrigatório e deve ser string.")

        result = {
            "content": [
                {
                    "type": "text",
                    "text": text,
                }
            ]
        }
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

    return error(f"Método não suportado: {method}")

def main():
    # Loop lendo uma linha JSON por vez
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"JSON inválido: {e}"}})
            continue

        resp = handle_request(req)
        send(resp)

if __name__ == "__main__":
    main()