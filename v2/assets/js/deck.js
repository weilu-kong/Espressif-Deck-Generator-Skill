(() => {
  const stage = document.getElementById('deck-stage');
  const deck = document.getElementById('deck');
  const slides = [...document.querySelectorAll('.slide')];
  const overviewModal = document.getElementById('overview-modal');
  const overviewGrid = document.getElementById('overview-grid');
  const overviewClose = document.getElementById('overview-close');
  let index = 0;
  let overviewOpen = false;
  let overviewFocusIndex = 0;

  function fit() {
    const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    stage.style.transform = `scale(${scale})`;
  }

  function cleanText(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function clip(value, max = 96) {
    const text = cleanText(value);
    return text.length > max ? text.slice(0, max - 1) + '…' : text;
  }

  function slideTitle(slide) {
    const el = slide.querySelector('.hero-title,.slide-title,.section-title,.ending-title,.card-title');
    return clip(el?.textContent || slide.id || 'Untitled slide', 72);
  }

  function slideDesc(slide) {
    const el = slide.querySelector('.hero-subtitle,.slide-subtitle,.section-subtitle,.card-positioning,.ending-subtitle');
    return clip(el?.textContent || '', 104);
  }

  function slideTag(slide) {
    const raw = slide.dataset.slideType || 'slide';
    return raw.replace(/_/g, '-').toUpperCase();
  }

  function overviewCards() {
    return overviewGrid ? [...overviewGrid.querySelectorAll('.overview-card')] : [];
  }

  function buildOverview() {
    if (!overviewGrid) return;
    overviewGrid.innerHTML = '';
    slides.forEach((slide, i) => {
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'overview-card';
      card.dataset.index = String(i);
      card.setAttribute('aria-label', `${i + 1}: ${slideTitle(slide)}`);

      const top = document.createElement('div');
      top.className = 'overview-card-top';
      const tag = document.createElement('span');
      tag.className = 'overview-card-tag';
      tag.textContent = slideTag(slide);
      const num = document.createElement('span');
      num.className = 'overview-card-num';
      num.textContent = `${String(i + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
      top.append(tag, num);

      const title = document.createElement('div');
      title.className = 'overview-card-title';
      title.textContent = slideTitle(slide);

      const desc = document.createElement('div');
      desc.className = 'overview-card-desc';
      desc.textContent = slideDesc(slide);

      card.append(top, title, desc);
      card.addEventListener('click', () => {
        go(i);
        closeOverview();
      });
      card.addEventListener('focus', () => { overviewFocusIndex = i; });
      overviewGrid.appendChild(card);
    });
  }

  function updateOverviewState() {
    overviewCards().forEach((card, i) => card.classList.toggle('current', i === index));
  }

  function go(next, animate = true) {
    index = Math.max(0, Math.min(slides.length - 1, next));
    deck.style.transition = animate && !document.body.classList.contains('motion-off') ? '' : 'none';
    deck.style.transform = `translateX(${-index * 1920}px)`;
    document.body.dataset.slide = String(index + 1);
    slides.forEach((slide, i) => slide.classList.toggle('active', i === index));
    updateOverviewState();
    history.replaceState(null, '', `#${slides[index]?.id || `slide-${index + 1}`}`);
  }

  function fromHash() {
    const id = location.hash.slice(1);
    const found = slides.findIndex(s => s.id === id);
    if (found >= 0) index = found;
    go(index, false);
  }

  function openOverview() {
    if (!overviewModal) return;
    overviewOpen = true;
    overviewFocusIndex = index;
    overviewModal.classList.add('active');
    overviewModal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('overview-open');
    updateOverviewState();
    requestAnimationFrame(() => overviewCards()[overviewFocusIndex]?.focus());
  }

  function closeOverview() {
    if (!overviewModal) return;
    overviewOpen = false;
    overviewModal.classList.remove('active');
    overviewModal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('overview-open');
  }

  function toggleOverview() {
    overviewOpen ? closeOverview() : openOverview();
  }

  function focusOverview(next) {
    const cards = overviewCards();
    if (!cards.length) return;
    overviewFocusIndex = (next + cards.length) % cards.length;
    cards[overviewFocusIndex].focus();
  }

  addEventListener('resize', fit);
  addEventListener('hashchange', fromHash);

  overviewClose?.addEventListener('click', closeOverview);
  overviewModal?.addEventListener('click', (e) => {
    if (e.target === overviewModal) closeOverview();
  });

  addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      toggleOverview();
      return;
    }

    if (overviewOpen) {
      const cols = window.innerWidth <= 980 ? 2 : 4;
      if (e.key === 'ArrowRight') { e.preventDefault(); focusOverview(overviewFocusIndex + 1); return; }
      if (e.key === 'ArrowLeft') { e.preventDefault(); focusOverview(overviewFocusIndex - 1); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); focusOverview(overviewFocusIndex + cols); return; }
      if (e.key === 'ArrowUp') { e.preventDefault(); focusOverview(overviewFocusIndex - cols); return; }
      if (e.key === 'Home') { e.preventDefault(); focusOverview(0); return; }
      if (e.key === 'End') { e.preventDefault(); focusOverview(slides.length - 1); return; }
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        go(overviewFocusIndex);
        closeOverview();
      }
      return;
    }

    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); go(index + 1); }
    else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); go(index - 1); }
    else if (e.key === 'Home') { e.preventDefault(); go(0); }
    else if (e.key === 'End') { e.preventDefault(); go(slides.length - 1); }
    else if (e.key.toLowerCase() === 'b') { document.body.classList.toggle('motion-off'); }
  });

  let touchStartX = 0;
  addEventListener('touchstart', (e) => {
    if (!overviewOpen) touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });
  addEventListener('touchend', (e) => {
    if (overviewOpen) return;
    const dx = touchStartX - e.changedTouches[0].screenX;
    if (Math.abs(dx) < 50) return;
    go(index + (dx > 0 ? 1 : -1));
  }, { passive: true });

  function seededRandom(seed) {
    let s = seed >>> 0;
    return () => {
      s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }

  class ParticleSystem {
    constructor(canvas, seed) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.rand = seededRandom(seed);
      this.particles = [];
      this.w = 0;
      this.h = 0;
      this.dpr = 1;
      this.last = 0;
      this.init();
    }

    init() {
      this.resize();
      this.particles = [];
      for (let i = 0; i < 58; i++) {
        const r = this.rand();
        this.particles.push({
          x: this.rand() * this.w,
          y: this.rand() * this.h,
          vx: (this.rand() - .5) * .34,
          vy: (this.rand() - .5) * .34,
          radius: 1.0 + this.rand() * 2.1,
          alpha: .22 + this.rand() * .48,
          phase: this.rand() * Math.PI * 2,
          spark: r > .86
        });
      }
    }

    resize() {
      this.w = this.canvas.clientWidth || 1920;
      this.h = this.canvas.clientHeight || 1080;
      this.dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.canvas.width = Math.round(this.w * this.dpr);
      this.canvas.height = Math.round(this.h * this.dpr);
      this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    }

    update(dt, t) {
      const k = Math.min(dt / 16.67, 2);
      for (const p of this.particles) {
        p.x += p.vx * k;
        p.y += p.vy * k + Math.sin(t * .0007 + p.phase) * .035;
        if (p.x < -8) p.x = this.w + 8;
        if (p.x > this.w + 8) p.x = -8;
        if (p.y < -8) p.y = this.h + 8;
        if (p.y > this.h + 8) p.y = -8;
      }
    }

    draw(t) {
      const ctx = this.ctx;
      ctx.clearRect(0, 0, this.w, this.h);
      const maxDist = 150;

      for (let i = 0; i < this.particles.length; i++) {
        const a = this.particles[i];
        for (let j = i + 1; j < this.particles.length; j++) {
          const b = this.particles[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const d = Math.hypot(dx, dy);
          if (d >= maxDist) continue;
          const alpha = (1 - d / maxDist) * .075;
          ctx.strokeStyle = `rgba(255,255,255,${alpha})`;
          ctx.lineWidth = .8;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }

      for (const p of this.particles) {
        const pulse = .76 + Math.sin(t * .0014 + p.phase) * .24;
        const alpha = p.alpha * pulse;
        ctx.save();
        if (p.spark) {
          ctx.shadowBlur = 16;
          ctx.shadowColor = 'rgba(255,196,218,.9)';
          ctx.fillStyle = `rgba(255,205,224,${Math.min(.92, alpha + .18)})`;
        } else {
          ctx.fillStyle = `rgba(255,255,255,${alpha})`;
        }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius * (p.spark ? 1.25 : 1), 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }

    frame = (t) => {
      const parent = this.canvas.closest('.slide');
      const active = !parent || parent.classList.contains('active');
      if (active) {
        const frozen = document.body.classList.contains('motion-off') ||
          window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const dt = this.last ? t - this.last : 16.67;
        if (!frozen) this.update(dt, t);
        this.draw(t);
      }
      this.last = t;
      requestAnimationFrame(this.frame);
    }
  }

  const particleSystems = [...document.querySelectorAll('canvas.tech-particles-bg')]
    .map((canvas, i) => new ParticleSystem(canvas, 0x51f15e + i * 97));
  addEventListener('resize', () => particleSystems.forEach(p => p.resize()));
  particleSystems.forEach(p => requestAnimationFrame(p.frame));

  window.__deck = {
    go,
    fit,
    slides,
    openOverview,
    closeOverview,
    get index() { return index; }
  };

  fit();
  buildOverview();
  fromHash();
})();
