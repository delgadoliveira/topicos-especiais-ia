# Plan-and-Execute: decompor objetivo em sub-tarefas
class SimplePlanner:
    def __init__(self):
        self.plan = []
        self.results = {}

    def decompose(self, objetivo: str):
        if 'comparar' in objetivo.lower():
            self.plan = [
                {'id': 1, 'action': 'buscar_preco', 'args': {'produto': 'A'}},
                {'id': 2, 'action': 'buscar_preco', 'args': {'produto': 'B'}},
                {'id': 3, 'action': 'comparar', 'deps': [1, 2]},
            ]
        print(f'Plano com {len(self.plan)} etapas:')
        for step in self.plan:
            deps = f" (depende de {step.get('deps', [])})" if 'deps' in step else ''
            print(f"   {step['id']}. {step['action']}({step.get('args', {})}){deps}")

    def execute(self):
        for step in self.plan:
            deps = step.get('deps', [])
            if all(d in self.results for d in deps):
                if step['action'] == 'buscar_preco':
                    self.results[step['id']] = {'A': 99, 'B': 149}[step['args']['produto']]
                elif step['action'] == 'comparar':
                    a, b = self.results[deps[0]], self.results[deps[1]]
                    self.results[step['id']] = f'A=R${a} vs B=R${b} -> {"A" if a < b else "B"} mais barato'
                print(f'  OK Step {step["id"]}: {self.results[step["id"]]}')

planner = SimplePlanner()
planner.decompose('Comparar precos dos produtos A e B')
print()
planner.execute()
