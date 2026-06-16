# Simulando Chain-of-Thought com parsing estruturado
def cot_resolver(problema: str) -> dict:
    steps = []
    if 'desconto' in problema.lower():
        steps.append('Passo 1: Identificar o valor original')
        steps.append('Passo 2: Calcular o percentual de desconto')
        steps.append('Passo 3: Subtrair o desconto do original')
        valor = 200
        desconto = 0.15
        final = valor * (1 - desconto)
        steps.append(f'Calculo: {valor} x (1 - {desconto}) = {final}')
        return {'steps': steps, 'answer': final}
    return {'steps': ['Problema nao reconhecido'], 'answer': None}

resultado = cot_resolver('Qual o preco com 15% de desconto em R$200?')
print('=== Chain-of-Thought ===')
for step in resultado['steps']:
    print(f'  -> {step}')
print(f'\nResposta final: R${resultado["answer"]:.2f}')
