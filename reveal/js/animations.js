/* ═══════════════════════════════════════════════════════
   ANIMATIONS.JS — GSAP-powered slide animations
   ═══════════════════════════════════════════════════════ */

const Animations = {
  /** Animate counter elements on a slide */
  animateCounters(slide) {
    const counters = slide.querySelectorAll('.counter');
    counters.forEach(counter => {
      const target = parseInt(counter.dataset.target, 10);
      if (!target) return;
      const duration = 2;
      const obj = { val: 0 };
      gsap.to(obj, {
        val: target,
        duration,
        ease: 'power2.out',
        onUpdate() {
          if (target >= 1000000) {
            counter.textContent = (obj.val / 1000000).toFixed(1) + 'M';
          } else if (target >= 1000) {
            counter.textContent = Math.round(obj.val / 1000) + 'k';
          } else {
            counter.textContent = Math.round(obj.val);
          }
        }
      });
    });
  },

  /** Stagger-animate cards within a container */
  staggerCards(slide) {
    const cards = slide.querySelectorAll('.stagger-in > *');
    if (!cards.length) return;
    gsap.fromTo(cards,
      { opacity: 0, y: 30, scale: 0.95 },
      { opacity: 1, y: 0, scale: 1, duration: 0.5, stagger: 0.12, ease: 'back.out(1.4)' }
    );
  },

  /** Animate flow diagram nodes */
  animateFlow(slide) {
    const nodes = slide.querySelectorAll('.flow-node');
    const arrows = slide.querySelectorAll('.flow-arrow');
    if (!nodes.length) return;
    
    const tl = gsap.timeline();
    nodes.forEach((node, i) => {
      tl.fromTo(node, 
        { opacity: 0, scale: 0.7 },
        { opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2)' },
        i * 0.15
      );
      if (arrows[i]) {
        tl.fromTo(arrows[i],
          { opacity: 0, x: -10 },
          { opacity: 1, x: 0, duration: 0.2 },
          i * 0.15 + 0.1
        );
      }
    });
  },

  /** Typewriter effect on elements */
  typewriter(slide) {
    const els = slide.querySelectorAll('.typewriter-js');
    els.forEach(el => {
      const text = el.dataset.text || el.textContent;
      el.textContent = '';
      el.style.visibility = 'visible';
      let i = 0;
      const speed = parseInt(el.dataset.speed, 10) || 40;
      const interval = setInterval(() => {
        el.textContent += text[i];
        i++;
        if (i >= text.length) clearInterval(interval);
      }, speed);
    });
  },

  /** Animate agent trace lines one by one */
  animateTrace(slide) {
    const lines = slide.querySelectorAll('.agent-trace .trace-line');
    if (!lines.length) return;
    gsap.fromTo(lines,
      { opacity: 0, x: -20 },
      { opacity: 1, x: 0, duration: 0.3, stagger: 0.2, ease: 'power2.out' }
    );
  },

  /** Parallax depth effect on cards */
  enableParallax(slide) {
    const cards = slide.querySelectorAll('.parallax-card');
    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `perspective(800px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(800px) rotateY(0) rotateX(0)';
        card.style.transition = 'transform 0.4s ease';
      });
      card.addEventListener('mouseenter', () => {
        card.style.transition = 'none';
      });
    });
  },

  /** Run all animations for a slide */
  onSlideEnter(slide) {
    this.animateCounters(slide);
    this.staggerCards(slide);
    this.animateFlow(slide);
    this.typewriter(slide);
    this.animateTrace(slide);
    this.enableParallax(slide);
  }
};

// Export for use in main.js
window.Animations = Animations;
