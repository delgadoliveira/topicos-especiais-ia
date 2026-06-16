/* ═══════════════════════════════════════════════════════
   SUBMISSION.JS — Student exercise submission via FormSubmit
   Sends to: delgado.oliveira@gmail.com
   Subject tag: [TOPICOS-IA-E{encontro}] for easy filtering
   ═══════════════════════════════════════════════════════ */

window.Submission = (() => {
  const EMAIL = 'delgado.oliveira@gmail.com';
  const FORMSUBMIT_URL = `https://formsubmit.co/${EMAIL}`;

  function createForm(encontroNum, exerciseTitle) {
    return `
    <div class="submission-container">
      <div class="submission-header">
        <div class="submission-icon">📝</div>
        <h3>Exercício Final — Encontro ${encontroNum}</h3>
        <p class="submission-subtitle">${exerciseTitle}</p>
      </div>
      <form class="submission-form" action="${FORMSUBMIT_URL}" method="POST" data-encontro="${encontroNum}">
        <!-- FormSubmit config -->
        <input type="hidden" name="_subject" value="[TOPICOS-IA-E${encontroNum}] Submissão de Exercício — Encontro ${encontroNum}">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="true">
        <input type="hidden" name="_next" value="${window.location.href}#/submission-success">
        <input type="text" name="_honey" style="display:none">
        
        <div class="form-grid">
          <div class="form-group">
            <label for="nome-e${encontroNum}">👤 Nome completo</label>
            <input type="text" id="nome-e${encontroNum}" name="Nome" required placeholder="Seu nome completo">
          </div>
          <div class="form-group">
            <label for="email-e${encontroNum}">📧 Email institucional</label>
            <input type="email" id="email-e${encontroNum}" name="Email" required placeholder="aluno@universidade.edu.br">
          </div>
          <div class="form-group">
            <label for="carteirinha-e${encontroNum}">🎓 Matrícula / Carteirinha</label>
            <input type="text" id="carteirinha-e${encontroNum}" name="Matricula" required placeholder="Ex: 2024001234">
          </div>
          <div class="form-group">
            <label for="encontro-e${encontroNum}">📚 Encontro</label>
            <input type="text" id="encontro-e${encontroNum}" name="Encontro" value="Encontro ${encontroNum}" readonly>
          </div>
        </div>
        
        <div class="form-group form-full">
          <label for="resposta-e${encontroNum}">💡 Sua Resposta</label>
          <textarea id="resposta-e${encontroNum}" name="Resposta" rows="10" required 
            placeholder="Cole aqui sua resposta completa. Inclua código, explicações e conclusões."></textarea>
        </div>
        
        <div class="form-group form-full">
          <label for="reflexao-e${encontroNum}">🤔 Reflexão (opcional)</label>
          <textarea id="reflexao-e${encontroNum}" name="Reflexao" rows="3" 
            placeholder="O que você aprendeu? Que dificuldades encontrou?"></textarea>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn-submit">
            <span class="btn-icon">🚀</span>
            <span class="btn-text">Enviar Exercício</span>
          </button>
          <p class="form-note">Ao enviar, o professor receberá seu exercício por email com a tag <code>[TOPICOS-IA-E${encontroNum}]</code></p>
        </div>
      </form>
    </div>`;
  }

  function initAll() {
    document.querySelectorAll('[data-submission]').forEach(el => {
      const encontro = el.dataset.submission;
      const title = el.dataset.title || 'Exercício Final';
      if (!el.querySelector('.submission-container')) {
        el.innerHTML = createForm(encontro, title);
      }
    });
  }

  return { initAll, createForm };
})();
