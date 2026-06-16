# Tracing: registra cada passo do agente para debug
import json
from datetime import datetime

class AgentTracer:
    def __init__(self):
        self.spans = []
        self.current_trace_id = 'trace_001'

    def start_span(self, name: str, input_data: str):
        span = {
            'trace_id': self.current_trace_id,
            'name': name,
            'start': datetime.now().isoformat(),
            'input': input_data[:100],
            'status': 'running'
        }
        self.spans.append(span)
        return len(self.spans) - 1

    def end_span(self, idx: int, output: str, status: str = 'ok'):
        self.spans[idx]['output'] = output[:100]
        self.spans[idx]['status'] = status
        self.spans[idx]['end'] = datetime.now().isoformat()

    def print_trace(self):
        print(f'Trace: {self.current_trace_id}')
        print(f'  Total spans: {len(self.spans)}')
        print()
        for i, span in enumerate(self.spans):
            icon = 'OK' if span['status'] == 'ok' else 'ERRO'
            print(f'  [{icon}] {span["name"]}')
            print(f'     Input:  {span["input"]}')
            print(f'     Output: {span.get("output", "...")}')
            print()

# Simula execucao de agente
tracer = AgentTracer()

s1 = tracer.start_span('user_input', 'Quanto custa um iPhone 15?')
tracer.end_span(s1, 'parsed: buscar preco iPhone 15')

s2 = tracer.start_span('planning', 'Objetivo: buscar preco')
tracer.end_span(s2, 'Plano: [buscar_produto, formatar_resposta]')

s3 = tracer.start_span('tool:buscar_produto', '{"nome": "iPhone 15"}')
tracer.end_span(s3, '{"preco": 5999, "loja": "TechStore"}')

s4 = tracer.start_span('generate_response', 'Contexto: iPhone 15 R$5999')
tracer.end_span(s4, 'O iPhone 15 custa R$5.999 na TechStore.', 'ok')

tracer.print_trace()
