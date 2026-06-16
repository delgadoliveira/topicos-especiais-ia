# Mini-agente ReAct (sem LLM real, logica fixa para aprendizado)

def tool_calculadora(expr: str) -> str:
    try:
        return str(eval(expr))
    except:
        return 'Erro na expressao'

def tool_clima(cidade: str) -> str:
    dados = {'SP': '28C, ensolarado', 'RJ': '32C, nublado'}
    return dados.get(cidade, 'Cidade nao encontrada')

# Simulacao do loop ReAct
steps = [
    ('Thought', 'Preciso calcular 15% de 200'),
    ('Action', 'calculadora("200 * 0.15")'),
    ('Observation', tool_calculadora('200 * 0.15')),
    ('Thought', 'Agora sei: 15% de 200 = 30'),
    ('Action', 'responder("15% de 200 e 30")'),
]

for tipo, conteudo in steps:
    print(f'[{tipo}] {conteudo}')
