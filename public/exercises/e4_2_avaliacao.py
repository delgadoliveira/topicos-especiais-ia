# Avaliacao de agentes: metricas simples
def avaliar_resposta(esperado: str, obtido: str) -> dict:
    exact = esperado.strip().lower() == obtido.strip().lower()

    tokens_esp = set(esperado.lower().split())
    tokens_obt = set(obtido.lower().split())

    if not tokens_esp or not tokens_obt:
        precision = recall = f1 = 0.0
    else:
        common = tokens_esp & tokens_obt
        precision = len(common) / len(tokens_obt)
        recall = len(common) / len(tokens_esp)
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {'exact_match': exact, 'precision': precision, 'recall': recall, 'f1': f1}

# Dataset de avaliacao
test_cases = [
    ('A capital do Brasil e Brasilia.', 'Brasilia e a capital do Brasil.'),
    ('Python e uma linguagem interpretada.', 'Python e interpretada e de alto nivel.'),
    ('O agente deve usar a tool de busca.', 'Nao sei responder essa pergunta.'),
]

print('=== Avaliacao de Respostas ===\n')
total_f1 = 0
for i, (esperado, obtido) in enumerate(test_cases, 1):
    metrics = avaliar_resposta(esperado, obtido)
    total_f1 += metrics['f1']
    print(f'Case {i}:')
    print(f'  Esperado: "{esperado[:50]}"')
    print(f'  Obtido:   "{obtido[:50]}"')
    print(f'  F1={metrics["f1"]:.2f} | Precision={metrics["precision"]:.2f} | Recall={metrics["recall"]:.2f}')
    print()

print(f'F1 medio: {total_f1/len(test_cases):.2f}')
