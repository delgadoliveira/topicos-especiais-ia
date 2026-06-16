import json

# Schema das tools (como enviamos ao LLM)
tools_schema = [
    {
        'name': 'buscar_produto',
        'description': 'Busca info de um produto pelo nome',
        'parameters': {
            'type': 'object',
            'properties': {
                'nome': {'type': 'string'},
                'categoria': {'type': 'string', 'enum': ['eletro', 'roupa', 'comida']}
            },
            'required': ['nome']
        }
    }
]

# Simula resposta do LLM (function_call)
llm_response = {
    'role': 'assistant',
    'content': None,
    'tool_calls': [{
        'id': 'call_123',
        'function': {
            'name': 'buscar_produto',
            'arguments': json.dumps({'nome': 'iPhone 15', 'categoria': 'eletro'})
        }
    }]
}

# Dispatcher
def buscar_produto(nome: str, categoria: str = 'geral') -> dict:
    db = {'iPhone 15': {'preco': 5999, 'estoque': 42}}
    return db.get(nome, {'erro': 'nao encontrado'})

# Parse e executa
for call in llm_response['tool_calls']:
    fn_name = call['function']['name']
    args = json.loads(call['function']['arguments'])
    print(f'Chamando: {fn_name}({args})')
    result = buscar_produto(**args)
    print(f'Resultado: {result}')
