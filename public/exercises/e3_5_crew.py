# Tutorial 3.5: dois agentes - pesquisador e critico
#
# Sem chamadas web/LLM reais. O foco e praticar handoff:
# pesquisador produz fatos -> critico marca riscos -> sintese usa apenas fatos confiaveis.


def agente_pesquisador(tema: str) -> list[dict]:
    return [
        {
            "texto": "RAG reduz alucinacao ao ancorar respostas em documentos.",
            "fonte": "artigo RAG 2020",
            "confianca": 0.82,
        },
        {
            "texto": "Agentes sempre superam workflows deterministas.",
            "fonte": "",
            "confianca": 0.35,
        },
        {
            "texto": "MCP padroniza como agentes acessam tools e dados externos.",
            "fonte": "modelcontextprotocol.io",
            "confianca": 0.78,
        },
    ]


def agente_critico(fatos: list[dict]) -> list[dict]:
    avaliados = []
    for fato in fatos:
        novo = dict(fato)
        # TODO 1: marque como duvidoso se nao tiver fonte.
        # TODO 2: marque como duvidoso se confianca < 0.60.
        # Dica: novo["status"] = "duvidoso" ou "confiavel"
        novo["status"] = "confiavel"
        novo["motivo"] = "ok"
        avaliados.append(novo)
    return avaliados


def sintetizar(avaliados: list[dict]) -> str:
    # TODO 3: use apenas fatos confiaveis na sintese.
    usados = avaliados
    linhas = ["Sintese:"]
    for fato in usados:
        linhas.append(f"- {fato['texto']} (fonte: {fato['fonte'] or 'sem fonte'})")
    return "\n".join(linhas)


def custo_estimado(fatos: list[dict], avaliados: list[dict]) -> int:
    # TODO 4: estime custo como numero de fatos lidos pelos dois agentes.
    return 0


def validar():
    fatos = agente_pesquisador("RAG, MCP e agentes")
    avaliados = agente_critico(fatos)
    sintese = sintetizar(avaliados)

    checks = [
        (
            "critico marca fato sem fonte como duvidoso",
            avaliados[1]["status"] == "duvidoso",
            "verifique fonte vazia em agente_critico()",
        ),
        (
            "critico marca baixa confianca como duvidoso",
            any(f["status"] == "duvidoso" and f["confianca"] < 0.60 for f in avaliados),
            "adicione regra de confianca < 0.60",
        ),
        (
            "sintese remove fato duvidoso",
            "sempre superam" not in sintese,
            "filtre avaliados por status == 'confiavel'",
        ),
        (
            "custo estima dois passes sobre os fatos",
            custo_estimado(fatos, avaliados) == 6,
            "retorne len(fatos) + len(avaliados)",
        ),
    ]

    print("=== Pesquisador: fatos ===")
    for fato in fatos:
        print(f"- {fato['texto']} | fonte={fato['fonte'] or 'sem fonte'} | conf={fato['confianca']}")

    print("\n=== Critico: avaliacao ===")
    for fato in avaliados:
        print(f"- {fato['status']}: {fato['texto']} ({fato['motivo']})")

    print("\n=== Sintese final ===")
    print(sintese)

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
