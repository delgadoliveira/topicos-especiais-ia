# Tutorial 3.4: MCP em miniatura - registro de tools
#
# MCP real conecta clientes a servidores de tools.
# Aqui simulamos o padrao dentro do navegador: schema -> dispatch -> resultado.

arquivos_fake = {
    "app.py": "print('hello')\nprint('agents')\n",
    "README.md": "# Projeto\nEste agente usa MCP.\n",
    "data.csv": "id,valor\n1,10\n2,20\n",
}


def listar_arquivos(diretorio: str = ".") -> list[str]:
    # TODO 1: retorne apenas os nomes dos arquivos disponiveis.
    # Dica: list(arquivos_fake.keys())
    return []


def contar_linhas(caminho_arquivo: str) -> int:
    # TODO 2: conte as linhas do arquivo solicitado.
    # Dica: arquivos_fake[caminho_arquivo].splitlines()
    return 0


tool_registry = {
    "listar_arquivos": {
        "description": "Lista arquivos de um diretorio",
        "function": listar_arquivos,
    },
    "contar_linhas": {
        "description": "Conta linhas de um arquivo",
        "function": contar_linhas,
    },
}


def chamar_tool(nome: str, **kwargs):
    # TODO 3: valide se a tool existe e chame a funcao correta.
    # Dica: tool_registry[nome]["function"](**kwargs)
    return None


def plano_do_agente(pergunta: str) -> list[tuple[str, dict]]:
    # Este plano simula o que um LLM faria antes de chamar tools.
    return [
        ("listar_arquivos", {"diretorio": "."}),
        ("contar_linhas", {"caminho_arquivo": "app.py"}),
    ]


def validar():
    plano = plano_do_agente("quantas linhas tem app.py?")
    resultados = []
    for nome, args in plano:
        resultados.append((nome, chamar_tool(nome, **args)))

    try:
        desconhecida = chamar_tool("apagar_tudo")
    except Exception as exc:
        desconhecida = f"ERRO: {type(exc).__name__}"

    checks = [
        (
            "listar_arquivos retorna app.py",
            "app.py" in listar_arquivos("."),
            "retorne list(arquivos_fake.keys())",
        ),
        (
            "contar_linhas calcula 2 linhas para app.py",
            contar_linhas("app.py") == 2,
            "use splitlines() no conteudo do arquivo",
        ),
        (
            "dispatcher chama tools registradas",
            resultados[-1][1] == 2,
            "implemente chamar_tool() usando tool_registry",
        ),
        (
            "tool desconhecida falha de forma clara",
            desconhecida is None,
            "mantenha bloqueio para tools fora do registry",
        ),
    ]

    print("=== Tools expostas ===")
    for nome, meta in tool_registry.items():
        print(f"- {nome}: {meta['description']}")

    print("\n=== Plano simulado do agente ===")
    for nome, args in plano:
        print(f"- chamar {nome}({args})")

    print("\n=== Resultados ===")
    for nome, resultado in resultados:
        print(f"- {nome}: {resultado}")

    print("\n=== Checklist ===")
    ok = 0
    for nome, passou, dica in checks:
        if passou:
            ok += 1
            print(f"[OK] {nome}")
        else:
            print(f"[TODO] {nome} -> {dica}")
    print(f"\nProgresso: {ok}/{len(checks)}")


validar()
