/* ═══════════════════════════════════════════════════════
   MANDATO.JS — simulador de portaria de autorizacao (Encontro 6)
   O aluno configura um mandato e roda uma fila real de pedidos.
   A fila contem armadilhas: fracionamento, falta de comprovante,
   acao fora do escopo, prazo vencido e pressao social.
   Objetivo didatico: mandato largo aprova o que nao devia;
   mandato apertado trava trabalho legitimo. O ponto otimo existe
   e so aparece quando a fila roda.
   ═══════════════════════════════════════════════════════ */
(function () {
  // dia = dia em que o agente age, contado do inicio do mandato.
  // ok = o pedido DEVERIA ser aprovado. nao = deveria ser recusado.
  const FILA = [
    { id: 1, quem: 'Ana',     o: 'Reembolso de viagem',          acao: 'reembolso', valor: 480,  dia: 1,  comp: true,  insiste: false, gt: 'ok'  },
    { id: 2, quem: 'Bruno',   o: 'Reembolso de curso',           acao: 'reembolso', valor: 1900, dia: 2,  comp: true,  insiste: false, gt: 'ok'  },
    { id: 3, quem: 'Célia',   o: 'Reembolso de equipamento',     acao: 'reembolso', valor: 4200, dia: 3,  comp: true,  insiste: false, gt: 'nao' },
    { id: 4, quem: 'Dário',   o: 'Reembolso, parcela 1 de 2',    acao: 'reembolso', valor: 1500, dia: 4,  comp: true,  insiste: false, gt: 'ok'  },
    { id: 5, quem: 'Dário',   o: 'Reembolso, parcela 2 de 2',    acao: 'reembolso', valor: 1500, dia: 4,  comp: true,  insiste: false, gt: 'nao' },
    { id: 6, quem: 'Elisa',   o: 'Reembolso sem comprovante',    acao: 'reembolso', valor: 700,  dia: 5,  comp: false, insiste: false, gt: 'nao' },
    { id: 7, quem: 'Fábio',   o: 'Emitir nota de crédito',       acao: 'nota',      valor: 300,  dia: 5,  comp: true,  insiste: false, gt: 'nao' },
    { id: 8, quem: 'Helena',  o: 'Reembolso no dia 12, diretoria insistiu 3×', acao: 'reembolso', valor: 1200, dia: 12, comp: true, insiste: true, gt: 'nao' },
  ];

  const ESCOPOS = {
    r:   { rot: 'só pagar reembolso',             acoes: ['reembolso'] },
    rn:  { rot: 'reembolso + nota de crédito',    acoes: ['reembolso', 'nota'] },
    tudo:{ rot: 'qualquer movimentação financeira', acoes: ['reembolso', 'nota'] },
  };

  function cfg() {
    const g = (id) => document.getElementById(id);
    if (!g('mdt-escopo')) return null;
    return {
      escopo: g('mdt-escopo').value,
      teto: g('mdt-teto').value === '0' ? null : parseInt(g('mdt-teto').value, 10),
      janela: g('mdt-janela').value === '0' ? null : parseInt(g('mdt-janela').value, 10),
      comp: g('mdt-comp').checked,
      agreg: g('mdt-agreg').checked,
      exc: g('mdt-exc').checked,
    };
  }

  // Avalia a fila na ordem, acumulando por (quem, dia) para detectar fracionamento.
  function avaliar(c) {
    const soma = new Map();
    return FILA.map((p) => {
      const chave = p.quem + '|' + p.dia;
      const acum = (soma.get(chave) || 0) + p.valor;
      soma.set(chave, acum);

      let motivo = null;
      if (c.escopo !== 'tudo' && !ESCOPOS[c.escopo].acoes.includes(p.acao)) motivo = 'ação fora do escopo';
      else if (c.comp && !p.comp) motivo = 'sem comprovante anexado';
      else if (c.teto !== null && p.valor > c.teto) motivo = 'acima do teto por pedido';
      else if (c.agreg && c.teto !== null && acum > c.teto) motivo = 'fracionamento: ' + acum.toLocaleString('pt-BR') + ' no dia';
      else if (c.janela !== null && p.dia > c.janela) motivo = 'mandato já vencido';

      let aberto = motivo === null;
      let excecao = false;
      if (!aberto && c.exc && p.insiste) { aberto = true; excecao = true; motivo = 'exceção liberada por insistência'; }

      const erro = aberto && p.gt === 'nao' ? 'passou' : (!aberto && p.gt === 'ok' ? 'travou' : null);
      return { p, aberto, motivo, excecao, erro };
    });
  }

  function render() {
    const c = cfg();
    const out = document.getElementById('mdt-out');
    const sc = document.getElementById('mdt-score');
    if (!c || !out || !sc) return;

    const res = avaliar(c);
    const passou = res.filter((r) => r.erro === 'passou').length;
    const travou = res.filter((r) => r.erro === 'travou').length;

    out.innerHTML = res.map((r) => {
      const cls = r.erro === 'passou' ? 'bad' : r.erro === 'travou' ? 'warn' : 'good';
      const sel = r.aberto ? 'AUTORIZADO' : 'RECUSADO';
      const nota = r.motivo ? r.motivo : 'dentro do mandato';
      return '<div class="mdt-chip ' + cls + '">' +
        '<b>' + r.p.quem + ' · R$ ' + r.p.valor.toLocaleString('pt-BR') + '</b>' +
        '<span class="mdt-o">' + r.p.o + '</span>' +
        '<span class="mdt-v">' + sel + ' — ' + nota + '</span>' +
        '</div>';
    }).join('');

    let veredito, vcls;
    if (passou === 0 && travou === 0) { veredito = 'Mandato calibrado: nada indevido passou e nenhum pedido legítimo travou.'; vcls = 'good'; }
    else if (passou > 0) { veredito = 'O mandato está largo demais.'; vcls = 'bad'; }
    else { veredito = 'O mandato está apertado demais: está travando trabalho real.'; vcls = 'warn'; }

    sc.className = 'mdt-score ' + vcls;
    sc.innerHTML = '<div class="mdt-nums"><span class="bad">' + passou + '</span> passaram indevidamente &nbsp;·&nbsp; ' +
      '<span class="warn">' + travou + '</span> legítimos travados</div><div class="mdt-ver">' + veredito + '</div>';
  }

  function bind() {
    const root = document.getElementById('mdt');
    if (!root || root.dataset.bound) return;
    root.dataset.bound = '1';
    root.addEventListener('change', render);
    root.addEventListener('input', render);
    const rst = document.getElementById('mdt-reset');
    if (rst) rst.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('mdt-escopo').value = 'r';
      document.getElementById('mdt-teto').value = '2000';
      document.getElementById('mdt-janela').value = '7';
      document.getElementById('mdt-comp').checked = true;
      document.getElementById('mdt-agreg').checked = true;
      document.getElementById('mdt-exc').checked = false;
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
    const el = document.getElementById('mdt');
    if ((el && el.dataset.bound) || ++t > 80) clearInterval(poll);
  }, 250);
})();
