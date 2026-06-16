# Memoria de longo prazo simples (key-value + busca)
from datetime import datetime

class MemoriaAgente:
    def __init__(self):
        self.episodica = []
        self.semantica = {}

    def salvar_episodio(self, evento: str):
        self.episodica.append((datetime.now().isoformat(), evento))

    def salvar_fato(self, chave: str, valor: str):
        self.semantica[chave] = valor

    def buscar_episodios(self, termo: str, limit: int = 3) -> list:
        resultados = [(ts, ev) for ts, ev in self.episodica if termo.lower() in ev.lower()]
        return resultados[-limit:]

    def recall(self, chave: str) -> str:
        return self.semantica.get(chave, 'Nao encontrado')

# Uso
mem = MemoriaAgente()

mem.salvar_fato('nome_usuario', 'Maria')
mem.salvar_fato('preferencia_linguagem', 'Python')
mem.salvar_episodio('Usuaria perguntou sobre RAG')
mem.salvar_episodio('Agente buscou docs sobre embeddings')
mem.salvar_episodio('Usuaria pediu exemplo de RAG em Python')
mem.salvar_episodio('Agente gerou codigo de RAG')

print('=== Memoria Semantica ===')
print(f'  Nome: {mem.recall("nome_usuario")}')
print(f'  Linguagem: {mem.recall("preferencia_linguagem")}')
print(f'  Cor favorita: {mem.recall("cor_favorita")}')

print('\n=== Memoria Episodica (busca: "RAG") ===')
for ts, ev in mem.buscar_episodios('RAG'):
    print(f'  [{ts[11:19]}] {ev}')

print(f'\nTotal: {len(mem.episodica)} episodios, {len(mem.semantica)} fatos')
