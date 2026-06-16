# Exercício: Complete a função decidir_acao
def decidir_acao(pergunta: str) -> str:
    '''Retorna "buscar" se a pergunta precisa de dados externos,
    ou "responder" se pode responder direto.'''
    palavras_busca = ['clima', 'preco', 'cotacao', 'noticia', 'hoje']
    # TODO: verifique se alguma palavra_busca esta na pergunta
    for palavra in palavras_busca:
        if palavra in pergunta.lower():
            return 'buscar'
    return 'responder'

# Teste
perguntas = [
    'Qual o clima em SP hoje?',
    'O que e machine learning?',
    'Qual o preco do Bitcoin?',
]
for p in perguntas:
    print(f'{p} -> {decidir_acao(p)}')
