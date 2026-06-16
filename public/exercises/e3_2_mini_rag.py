# Mini-RAG: busca por similaridade de palavras (Jaccard)
def tokenize(text: str) -> list:
    return text.lower().split()

def similarity(query: str, doc: str) -> float:
    q_tokens = set(tokenize(query))
    d_tokens = set(tokenize(doc))
    if not q_tokens or not d_tokens:
        return 0.0
    intersection = q_tokens & d_tokens
    union = q_tokens | d_tokens
    return len(intersection) / len(union)

# Base de conhecimento (chunks)
knowledge_base = [
    'Agentes de IA usam LLMs para raciocinar e tomar decisoes.',
    'O padrao ReAct combina reasoning e acting em um loop.',
    'Function calling permite que o LLM invoque ferramentas externas.',
    'RAG recupera documentos relevantes antes de gerar a resposta.',
    'Memoria episodica armazena interacoes passadas do agente.',
    'LangGraph permite criar grafos de estado para agentes complexos.',
]

# Busca
query = 'como o agente usa ferramentas?'
print(f'Query: "{query}"\n')

scores = [(doc, similarity(query, doc)) for doc in knowledge_base]
scores.sort(key=lambda x: x[1], reverse=True)

print('Top 3 documentos relevantes:')
for i, (doc, score) in enumerate(scores[:3], 1):
    print(f'  {i}. [{score:.2f}] {doc}')

context = '\n'.join(doc for doc, _ in scores[:2])
print(f'\nContexto enviado ao LLM:\n  {context}')
