(() => {
  const stage = document.getElementById('deck-stage');
  const deck = document.getElementById('deck');
  const slides = [...document.querySelectorAll('.slide')];
  let index = 0;

  function fit() {
    const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    stage.style.transform = `scale(${scale})`;
  }

  function go(next, animate = true) {
    index = Math.max(0, Math.min(slides.length - 1, next));
    deck.style.transition = animate && !document.body.classList.contains('motion-off') ? '' : 'none';
    deck.style.transform = `translateX(${-index * 1920}px)`;
    document.body.dataset.slide = String(index + 1);
    history.replaceState(null, '', `#${slides[index]?.id || `slide-${index + 1}`}`);
  }

  function fromHash() {
    const id = location.hash.slice(1);
    const found = slides.findIndex(s => s.id === id);
    if (found >= 0) index = found;
    go(index, false);
  }

  addEventListener('resize', fit);
  addEventListener('hashchange', fromHash);
  addEventListener('keydown', (e) => {
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); go(index + 1); }
    if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); go(index - 1); }
    if (e.key === 'Home') go(0);
    if (e.key === 'End') go(slides.length - 1);
    if (e.key.toLowerCase() === 'b') document.body.classList.toggle('motion-off');
  });

  window.__deck = { go, fit, slides, get index() { return index; } };
  fit();
  fromHash();
})();
