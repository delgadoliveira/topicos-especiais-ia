"""
Portal Multi-Agente — UI Gradio (roda local e no Hugging Face Spaces).

Descobre automaticamente todos os agentes em agents/, mostra um menu e
conversa com o agente selecionado. Se um agente falhar, o portal continua
de pé (a falha vira uma mensagem, não uma queda).

Rodar local:   python app.py
Rodar offline: MOCK_LLM=1 python app.py
"""
import os
import pathlib
import sys

# Garante que 'portal' e 'agents' sejam importáveis ao rodar de qualquer lugar.
sys.path.insert(0, str(pathlib.Path(__file__).parent))

try:  # .env é opcional
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

import gradio as gr

from portal import llm, registry, runner, submissions

AGENTS, ERRORS = registry.discover("agents")


def _make_chatbot(**kwargs):
    # gradio 4/5 usam type="messages"; gradio 6 já é messages por padrão.
    try:
        return gr.Chatbot(type="messages", **kwargs)
    except TypeError:
        return gr.Chatbot(**kwargs)


def _choices():
    return [(f"{a.emoji} {a.name}", slug) for slug, a in AGENTS.items()]


def responder(slug, message, history):
    history = history or []
    if not slug:
        history.append({"role": "assistant", "content": "Selecione um agente no menu."})
        return history, ""
    if not (message or "").strip():
        return history, ""

    agent = AGENTS[slug]
    history.append({"role": "user", "content": message})
    result, latency, status = runner.safe_run(agent, message, history[:-1])

    partes = [result.answer]
    if result.steps:
        partes.append("\n\n🔎 **Passos:** " + " → ".join(result.steps))
    if result.citations:
        partes.append("\n\n📎 **Fontes:** " + "; ".join(result.citations))
    partes.append(
        f"\n\n<sub>⏱️ {latency:.1f}s · modelo: {llm.get_model()} · "
        f"{llm.usage_summary()} · status: {status}</sub>"
    )
    history.append({"role": "assistant", "content": "".join(partes)})
    return history, ""


def avaliar_entrega(package):
    if not package:
        raise gr.Error("Selecione um arquivo ZIP.")
    try:
        result, report = submissions.evaluate_submission(package)
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc
    return submissions.format_result(result), str(report)


with gr.Blocks(title="Portal Multi-Agente") as demo:
    gr.Markdown(
        "# 🤖 Portal Multi-Agente\n"
        "Cada agente foi construído por um aluno. Escolha um e converse."
    )

    with gr.Tab("Experimentar agentes"):
        if ERRORS:
            with gr.Accordion(
                f"⚠️ {len(ERRORS)} agente(s) com erro de carga", open=False
            ):
                gr.Markdown("\n".join(f"- `{e.module}`: {e.reason}" for e in ERRORS))

        if not AGENTS:
            gr.Markdown(
                "### Nenhum agente carregado ainda.\n"
                "Crie `agents/<seu-slug>.py` a partir de `agents/_template_agent.py`."
            )
        else:
            first = list(AGENTS)[0]
            slug = gr.Dropdown(choices=_choices(), value=first, label="Agente")
            desc = gr.Markdown(f"_{AGENTS[first].description}_")
            chat = _make_chatbot(height=380)
            msg = gr.Textbox(placeholder="Digite sua mensagem...", label="Mensagem")
            with gr.Row():
                enviar = gr.Button("Enviar", variant="primary")
                limpar = gr.Button("Limpar")

            slug.change(lambda s: f"_{AGENTS[s].description}_", slug, desc)
            enviar.click(responder, [slug, msg, chat], [chat, msg])
            msg.submit(responder, [slug, msg, chat], [chat, msg])
            limpar.click(lambda: [], None, chat)

    with gr.Tab("Entregar trabalho"):
        gr.Markdown(
            "Envie o ZIP criado por `prepare_submission.py`. A avaliacao aplica "
            "uma politica restrita, roda **somente offline** e registra o conceito "
            "localmente.\n\n"
            "⚠️ O professor deve abrir esta funcao apenas em um computador de aula: "
            "a protecao por subprocesso e timeout nao substitui uma sandbox completa."
        )
        package = gr.File(
            label="Entrega (.zip)", file_types=[".zip"], type="filepath"
        )
        evaluate = gr.Button("Avaliar e registrar", variant="primary")
        result = gr.Markdown()
        report = gr.File(label="Planilha CSV consolidada")
        evaluate.click(avaliar_entrega, package, [result, report])


if __name__ == "__main__":
    demo.launch()
