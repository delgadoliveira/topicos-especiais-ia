# Context management: sliding window com resumo
def contar_tokens(msgs: list) -> int:
    return sum(len(m['content']) // 4 for m in msgs)

def sliding_window(msgs: list, max_tokens: int = 50) -> list:
    system = [msgs[0]] if msgs[0]['role'] == 'system' else []
    historico = msgs[1:] if system else msgs

    resultado = []
    tokens_usados = contar_tokens(system)

    for msg in reversed(historico):
        msg_tokens = len(msg['content']) // 4
        if tokens_usados + msg_tokens <= max_tokens:
            resultado.insert(0, msg)
            tokens_usados += msg_tokens
        else:
            break

    return system + resultado

# Teste
mensagens = [
    {'role': 'system', 'content': 'Voce e um assistente.'},
    {'role': 'user', 'content': 'Ola, me chamo Joao'},
    {'role': 'assistant', 'content': 'Prazer, Joao!'},
    {'role': 'user', 'content': 'Qual a capital do Brasil?'},
    {'role': 'assistant', 'content': 'A capital do Brasil e Brasilia.'},
    {'role': 'user', 'content': 'E a populacao?'},
]

print(f'Original: {len(mensagens)} msgs, ~{contar_tokens(mensagens)} tokens')
resultado = sliding_window(mensagens, max_tokens=30)
print(f'Apos window: {len(resultado)} msgs, ~{contar_tokens(resultado)} tokens')
print()
for m in resultado:
    print(f'  [{m["role"]}] {m["content"][:50]}')
