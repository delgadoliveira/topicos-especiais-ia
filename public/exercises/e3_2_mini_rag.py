# Tutorial 3.2: mini-RAG executavel no navegador
#
# Objetivo: completar o retriever aos poucos.
# Nao ha LLM real aqui: o foco e entender retrieval + grounding.

import re

knowledge_base = [
    "RAG recupera documentos relevantes antes de gerar a resposta.",
    "Embeddings representam textos como vetores para busca semantica.",
    "Function calling permite que o LLM invoque ferramentas externas.",
    "Memoria episodica registra eventos e interacoes passadas.",
    "MCP padroniza a conexao entre agentes, dados e ferramentas.",
]


def tokenize(texto: str) -> list[str]:
    # TODO 1: normalize melhor o texto.
    # Dica: use re.findall(r"[a-zA-Z0-9_]+", texto.lower())
    return texto.lower().split()


def similarity(query: str, doc: str) -> float:
    q_tokens = set(tokenize(query))
    d_tokens = set(tokenize(doc))
    if not q_tokens or not d_tokens:
        return 0.0

    # TODO 2: calcule Jaccard = intersecao / uniao.
    # Troque o retorno fixo abaixo pela formula.
    return 0.0


def retrieve(query: str, top_k: int = 2) -> list[tuple[str, float]]:
    scores = [(doc, similarity(query, doc)) for doc in knowledge_base]
    # TODO 3: ordene do maior score para o menor.
    # Dica: scores.sort(key=lambda item: item[1], reverse=True)
    return scores[:top_k]


def answer(query: str, docs: list[tuple[str, float]]) -> str:
    melhor_doc, melhor_score = docs[0]
    # TODO 4: se o score for muito baixo, responda "nao sei".
    # Dica: teste melhor_score < 0.10
    return f"Com base no contexto: {melhor_doc}"


def validar():
    pergunta = "como o agente usa ferramentas externas?"
    docs = retrieve(pergunta, top_k=3)
    resposta = answer(pergunta, docs)

    checks = [
        (
            "tokenize remove pontuacao",
            "rag" in tokenize("RAG, funciona?"),
            "use regex para separar palavras",
        ),
        (
            "similarity detecta sobreposicao",
            similarity("ferramentas externas", knowledge_base[2]) > 0,
            "implemente Jaccard em similarity()",
        ),
        (
            "retrieve coloca function calling no topo",
            docs[0][0].startswith("Function calling"),
            "ordene scores em ordem decrescente",
        ),
        (
            "pegadinha retorna nao sei",
            "nao sei" in answer("qual a capital da Islandia?", retrieve("qual a capital da Islandia?")).lower(),
            "adicione limiar de confianca em answer()",
        ),
    ]

    print("=== Query ===")
    print(pergunta)
    print("\n=== Documentos recuperados ===")
    for i, (doc, score) in enumerate(docs, 1):
        print(f"{i}. score={score:.2f} | {doc}")
    print("\n=== Resposta grounded ===")
    print(resposta)

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
