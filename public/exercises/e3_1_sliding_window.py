# Tutorial 3.1: janela de contexto com sliding window
#
# Objetivo: completar pequenas partes e executar varias vezes.
# O checklist no final mostra o que ja esta correto.

mensagens = [
    {"role": "system", "content": "Voce e um tutor de IA. Responda de forma curta."},
    {"role": "user", "content": "Meu nome e Joao e eu estudo agentes."},
    {"role": "assistant", "content": "Prazer, Joao. Vamos estudar agentes."},
    {"role": "user", "content": "Explique RAG com um exemplo simples."},
    {"role": "assistant", "content": "RAG busca documentos antes de responder."},
    {"role": "user", "content": "Agora explique memoria de longo prazo."},
]


def contar_tokens(texto: str) -> int:
    # TODO 1: troque por uma estimativa melhor.
    # Dica: em ingles/portugues, uma aproximacao comum e len(texto) // 4.
    return len(texto.split())


def tokens_da_mensagem(msg: dict) -> int:
    return contar_tokens(msg["content"])


def separar_system(msgs: list) -> tuple[list, list]:
    # TODO 2: preserve a mensagem system fora do corte da janela.
    # Retorne: ([system], historico_sem_system) quando a primeira mensagem for system.
    return [], msgs


def sliding_window(msgs: list, max_tokens: int = 32) -> list:
    system, historico = separar_system(msgs)
    resultado = []
    tokens_usados = sum(tokens_da_mensagem(m) for m in system)

    # TODO 3: percorra o historico de tras para frente.
    # Dica: reversed(historico)
    for msg in historico:
        custo = tokens_da_mensagem(msg)
        if tokens_usados + custo <= max_tokens:
            # TODO 4: mantenha a ordem original das mensagens selecionadas.
            resultado.append(msg)
            tokens_usados += custo

    return system + resultado


def validar():
    compactado = sliding_window(mensagens, max_tokens=32)
    checks = []

    checks.append((
        "preserva a mensagem system",
        compactado and compactado[0]["role"] == "system",
        "implemente separar_system()",
    ))
    checks.append((
        "remove alguma mensagem antiga",
        len(compactado) < len(mensagens),
        "a janela deve cortar historico quando ultrapassar max_tokens",
    ))
    checks.append((
        "mantem a ultima pergunta do usuario",
        compactado[-1]["content"].startswith("Agora explique memoria"),
        "percorra de tras para frente para priorizar o contexto recente",
    ))
    checks.append((
        "mantem ordem cronologica",
        [m["role"] for m in compactado] == [m["role"] for m in sorted(compactado, key=lambda m: mensagens.index(m))],
        "use insert(0, msg) ou inverta no final",
    ))
    checks.append((
        "estimativa de tokens esta razoavel",
        contar_tokens("12345678901234567890") == 5,
        "use max(1, len(texto) // 4)",
    ))

    print("=== Resultado da janela ===")
    print(f"Original: {len(mensagens)} mensagens")
    print(f"Compactado: {len(compactado)} mensagens")
    for msg in compactado:
        print(f"- {msg['role']}: {msg['content'][:58]}")

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
