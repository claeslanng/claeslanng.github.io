(() => {
  const canvas = document.getElementById("scope");
  const ctx = canvas.getContext("2d");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  // One bar of 4/4 at 128 BPM: a kick on every beat, and a bass that ducks under it
  const bpm = 128, beats = 4, rate = 6000;
  const beatSec = 60 / bpm, barSec = beatSec * beats;
  const n = Math.round(barSec * rate);
  const kick = new Float32Array(n), bass = new Float32Array(n);
  let kickPhase = 0, bassPhase = 0;
  for (let i = 0; i < n; i++) {
    const t = i / rate, tb = t % beatSec;
    if (tb < 1 / rate) kickPhase = 0;
    const f = 48 + 130 * Math.exp(-tb * 32);
    kickPhase += 2 * Math.PI * f / rate;
    kick[i] = 0.92 * Math.sin(kickPhase) * Math.exp(-tb * 6.5);
    bassPhase += 2 * Math.PI * 49 / rate;
    let saw = 0;
    for (let h = 1; h <= 4; h++) saw += Math.sin(bassPhase * h) / h;
    const duck = 1 - Math.exp(-Math.max(0, tb - 0.02) * 9);
    bass[i] = 0.42 * saw * duck;
  }

  let cols = 0, kHi, kLo, bHi, bLo, w = 0, h = 0, dpr = 1;
  function measure() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    const r = canvas.getBoundingClientRect();
    w = r.width; h = r.height;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    cols = Math.max(1, Math.round(w));
    kHi = new Float32Array(cols); kLo = new Float32Array(cols);
    bHi = new Float32Array(cols); bLo = new Float32Array(cols);
    for (let c = 0; c < cols; c++) {
      const s0 = Math.floor(c * n / cols), s1 = Math.min(n - 1, Math.floor((c + 1) * n / cols));
      let a = -9, b = 9, x = -9, y = 9;
      for (let s = s0; s <= s1; s++) {
        a = Math.max(a, kick[s]); b = Math.min(b, kick[s]);
        x = Math.max(x, bass[s]); y = Math.min(y, bass[s]);
      }
      kHi[c] = a; kLo[c] = b; bHi[c] = x; bLo[c] = y;
    }
  }

  const css = getComputedStyle(document.documentElement);
  const ink = css.getPropertyValue("--ink").trim();
  const orange = css.getPropertyValue("--orange").trim();
  const faint = css.getPropertyValue("--ink-faint").trim();

  // Filled min/max envelope, drawn for columns [from, to)
  function envelope(hi, lo, from, to, colour, alpha) {
    if (to - from < 2) return;
    const mid = h / 2, amp = h * 0.46;
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    ctx.moveTo(from + 0.5, mid - hi[from] * amp);
    for (let c = from + 1; c < to; c++) ctx.lineTo(c + 0.5, mid - hi[c] * amp);
    for (let c = to - 1; c >= from; c--) ctx.lineTo(c + 0.5, mid - lo[c] * amp);
    ctx.closePath();
    ctx.fillStyle = colour; ctx.fill();
    ctx.lineWidth = 1.2; ctx.strokeStyle = colour; ctx.stroke();
    ctx.globalAlpha = 1;
  }

  function draw(progress) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = faint;
    for (let b = 1; b < beats; b++) ctx.fillRect(Math.round(b * w / beats), 0, 1, h);
    ctx.fillRect(0, Math.round(h / 2), w, 1);

    const head = Math.round(progress * cols);
    // The part not yet redrawn this pass stays as a faint copy of the last one
    envelope(bHi, bLo, Math.max(0, head - 1), cols, orange, 0.22);
    envelope(kHi, kLo, Math.max(0, head - 1), cols, ink, 0.22);
    envelope(bHi, bLo, 0, Math.min(cols, head + 1), orange, 1);
    envelope(kHi, kLo, 0, Math.min(cols, head + 1), ink, 1);

    if (progress < 1) {
      ctx.fillStyle = orange;
      ctx.fillRect(head, 0, 2, h);
    }
  }

  let raf = 0, start = 0, visible = true;
  function frame(now) {
    if (!start) start = now;
    draw(((now - start) / 1000 % barSec) / barSec);
    raf = requestAnimationFrame(frame);
  }
  function update() {
    cancelAnimationFrame(raf);
    if (reduceMotion.matches || !visible) { draw(1); return; }
    start = 0;
    raf = requestAnimationFrame(frame);
  }

  measure(); update();
  window.addEventListener("resize", () => { measure(); update(); });
  reduceMotion.addEventListener?.("change", update);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; update(); }).observe(canvas);
})();
