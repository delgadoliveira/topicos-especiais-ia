/* ═══════════════════════════════════════════════════════
   HANDOFF.JS — simulador de travessia de reset (Encontro 5)
   O aluno escolhe o que o agente deixa gravado antes da sessao
   morrer. O simulador mata a sessao e mostra o que o agente
   seguinte consegue (ou nao) retomar.
   Cenario ancorado na fila de 400 reembolsos do inicio do encontro:
   no momento do reset, 90 pedidos ja decididos, 30 e-mails enviados
   e 310 pedidos ainda por decidir (90 + 310 = 400).
   ═══════════════════════════════════════════════════════ */
(function () {
  const DECIDIDOS = 90, ENVIADOS = 30, RESTANTES = 310;

  // pena: artefatos que PIORAM a travessia quando marcados.
  const ART = [
    { id: 'obj',    pena: false },
    { id: 'crit',   pena: false },
    { id: 'feito',  pena: false },
    { id: 'just',   pena: false },
    { id: 'mail',   pena: false },
    { id: 'passo',  pena: false },
    { id: 'transc', pena: true  },
    { id: 'cred',   pena: true  },
  ];

  function estado() {
    const s = {};
    for (const a of ART) {
      const el = document.getElementById('hnd-' + a.id);
      if (!el) return null;
      s[a.id] = el.checked;
    }
    return s;
  }

  function render() {
    const s = estado();
    const out = document.getElementById('hnd-out');
    const sc = document.getElementById('hnd-score');
    if (!s || !out || !sc) return;

    const reproc = s.feito ? 0 : DECIDIDOS;
    const dup = s.mail ? 0 : ENVIADOS;
    const incons = s.crit ? 0 : RESTANTES;
    const parou = !s.obj;

    const achados = [];
    if (parou) achados.push(['bad', 'A fila para', 'O agente seguinte n&atilde;o sabe o que estava fazendo. Nenhum pedido avan&ccedil;a at&eacute; algu&eacute;m voltar na segunda.']);
    if (!s.crit) achados.push(['bad', incons + ' decis&otilde;es com outro crit&eacute;rio', 'Os ' + DECIDIDOS + ' primeiros seguiram uma r&eacute;gua; os ' + RESTANTES + ' restantes seguem outra. &Eacute; a&iacute; que nascem os 60 aprovados sem comprovante.']);
    if (!s.feito) achados.push(['bad', reproc + ' pedidos reprocessados', 'Sem a lista do que j&aacute; foi decidido, o agente novo recome&ccedil;a por pedidos que j&aacute; tinham resposta.']);
    if (!s.mail) achados.push(['bad', dup + ' e-mails duplicados', 'Quem j&aacute; tinha recebido o pedido de documento recebe de novo. &Eacute; o erro de s&aacute;bado &agrave;s 3h.']);
    if (!s.just) achados.push(['warn', 'N&atilde;o audit&aacute;vel', 'D&aacute; para dizer quantos foram decididos, n&atilde;o por qu&ecirc;. Descobrir quais conferir vira trabalho manual.']);
    if (!s.passo) achados.push(['warn', 'Recome&ccedil;a do in&iacute;cio', 'Sem o ponto de parada, o agente refaz o percurso at&eacute; achar onde estava.']);
    if (s.transc) achados.push(['warn', 'A transcri&ccedil;&atilde;o entope a sess&atilde;o nova', 'Hist&oacute;rico n&atilde;o &eacute; handoff. Ele volta inteiro para o contexto e a sess&atilde;o seguinte estoura mais cedo.']);
    if (s.cred) achados.push(['bad', 'O token sobrevive &agrave; tarefa', 'A permiss&atilde;o passa a viver mais que o trabalho que a justificava. &Eacute; a chave que o agente guarda.']);

    if (!achados.length) {
      achados.push(['good', 'A tarefa atravessou', 'O agente seguinte retoma no pedido certo, com a mesma r&eacute;gua, sem reenviar nada.']);
      achados.push(['good', 'E d&aacute; para auditar', 'Cada decis&atilde;o tem motivo gravado. Conferir uma amostra &eacute; quest&atilde;o de minutos.']);
    }

    out.innerHTML = achados.map(([c, t, d]) =>
      '<div class="mdt-chip ' + c + '"><b>' + t + '</b><span class="mdt-o">' + d + '</span></div>'
    ).join('');

    let vcls, ver;
    if (parou) { vcls = 'bad'; ver = 'A tarefa n&atilde;o atravessou: o reset apagou o trabalho.'; }
    else if (achados[0][0] === 'good') { vcls = 'good'; ver = 'A tarefa atravessou o reset sem dano.'; }
    else { vcls = achados.some((a) => a[0] === 'bad') ? 'bad' : 'warn'; ver = 'Atravessou, mas com dano &mdash; e ningu&eacute;m vai perceber at&eacute; segunda.'; }

    sc.className = 'mdt-score ' + vcls;
    sc.innerHTML = '<div class="mdt-nums"><span class="bad">' + reproc + '</span> reprocessados &nbsp;·&nbsp; ' +
      '<span class="bad">' + dup + '</span> e-mails duplicados &nbsp;·&nbsp; ' +
      '<span class="warn">' + incons + '</span> fora do crit&eacute;rio</div><div class="mdt-ver">' + ver + '</div>';
  }

  function bind() {
    const root = document.getElementById('hnd');
    if (!root || root.dataset.bound) return;
    root.dataset.bound = '1';
    root.addEventListener('change', render);
    const rst = document.getElementById('hnd-reset');
    if (rst) rst.addEventListener('click', (e) => {
      e.preventDefault();
      for (const a of ART) {
        const el = document.getElementById('hnd-' + a.id);
        if (el) el.checked = !a.pena;
      }
      render();
    });
    render();
  }

  if (document.readyState !== 'loading') bind();
  else document.addEventListener('DOMContentLoaded', bind);
  document.addEventListener('ready', bind);
  if (window.Reveal && Reveal.on) Reveal.on('slidechanged', bind);
  window.addEventListener('load', bind);
  // As secoes sao injetadas por fetch depois do load: tenta ate o no existir.
  let t = 0;
  const poll = setInterval(() => {
    bind();
    const el = document.getElementById('hnd');
    if ((el && el.dataset.bound) || ++t > 80) clearInterval(poll);
  }, 250);
})();
