# Tutorial 3.3: memoria semantica + episodica
#
# Objetivo: simular "lembrar entre sessoes" sem banco real.
# A primeira sessao salva fatos; a segunda carrega um snapshot.

from datetime import datetime


class MemoriaAgente:
    def __init__(self):
        self.episodica = []
        self.semantica = {}

    def salvar_episodio(self, evento: str):
        self.episodica.append((datetime.now().isoformat(), evento))

    def salvar_fato(self, chave: str, valor: str):
        # TODO 1: normalize a chave antes de salvar.
        # Dica: chave.strip().lower()
        self.semantica[chave] = valor

    def recall(self, chave: str) -> str:
        # TODO 2: use a mesma normalizacao de salvar_fato().
        return self.semantica.get(chave, "Nao encontrado")

    def buscar_episodios(self, termo: str, limit: int = 3) -> list:
        resultados = []
        # TODO 3: filtre episodios que contem o termo, ignorando maiusculas.
        for ts, evento in self.episodica:
            if termo in evento:
                resultados.append((ts, evento))
        return resultados[-limit:]

    def exportar_snapshot(self) -> dict:
        # TODO 4: retorne uma copia de semantica e episodica.
        # Isso simula gravar em disco entre execucoes.
        return {}

    def importar_snapshot(self, snapshot: dict):
        # TODO 5: restaure semantica e episodica a partir do snapshot.
        self.semantica = {}
        self.episodica = []


def validar():
    sessao_1 = MemoriaAgente()
    sessao_1.salvar_fato(" Nome_Usuario ", "Maria")
    sessao_1.salvar_fato("profissao", "engenheira de dados")
    sessao_1.salvar_fato("preferencia_linguagem", "Python")
    sessao_1.salvar_episodio("Usuario perguntou sobre RAG")
    sessao_1.salvar_episodio("Agente buscou docs sobre embeddings")
    sessao_1.salvar_episodio("Usuario pediu exemplo de RAG em Python")

    snapshot = sessao_1.exportar_snapshot()

    sessao_2 = MemoriaAgente()
    sessao_2.importar_snapshot(snapshot)

    checks = [
        (
            "normaliza chave com espacos/maiusculas",
            sessao_1.recall("nome_usuario") == "Maria",
            "normalize a chave em salvar_fato() e recall()",
        ),
        (
            "busca episodica ignora maiusculas",
            len(sessao_1.buscar_episodios("rag")) == 2,
            "compare termo.lower() com evento.lower()",
        ),
        (
            "exporta snapshot com fatos",
            "semantica" in snapshot and snapshot["semantica"],
            "retorne {'semantica': dict(...), 'episodica': list(...)}",
        ),
        (
            "importa snapshot em nova sessao",
            sessao_2.recall("profissao") == "engenheira de dados",
            "restaure self.semantica e self.episodica",
        ),
    ]

    print("=== Sessao 2: pergunta ===")
    print("Qual minha profissao?")
    print("Resposta da memoria:", sessao_2.recall("profissao"))

    print("\n=== Episodios sobre RAG ===")
    for ts, evento in sessao_1.buscar_episodios("rag"):
        print(f"- [{ts[11:19]}] {evento}")

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
