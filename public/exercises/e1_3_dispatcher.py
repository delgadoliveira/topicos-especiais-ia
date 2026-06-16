# Agente com dispatch de tools
tools = {}

def register_tool(name):
    def decorator(func):
        tools[name] = func
        return func
    return decorator

@register_tool('somar')
def somar(a: int, b: int) -> int:
    return a + b

@register_tool('multiplicar')
def multiplicar(a: int, b: int) -> int:
    return a * b

# TODO: registre uma tool 'subtrair'
@register_tool('subtrair')
def subtrair(a: int, b: int) -> int:
    return a - b

# Dispatcher do agente
def executar(tool_name: str, **kwargs):
    if tool_name in tools:
        resultado = tools[tool_name](**kwargs)
        print(f'OK {tool_name}({kwargs}) = {resultado}')
    else:
        print(f'ERRO Tool "{tool_name}" nao encontrada')

executar('somar', a=5, b=3)
executar('multiplicar', a=4, b=7)
executar('subtrair', a=10, b=3)
executar('dividir', a=10, b=2)  # Tool nao existe!
