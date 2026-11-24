/* Plays a quiet sine at a given frequency for a few seconds.
   Any <button data-tone="46.25"> on the page becomes a listen button. */
(function () {
  var ctx = null, current = null;

  function stop() {
    if (!current) return;
    var c = current; current = null;
    var t = ctx.currentTime;
    c.gain.gain.cancelScheduledValues(t);
    c.gain.gain.setTargetAtTime(0, t, 0.04);
    c.osc.stop(t + 0.3);
    c.button.setAttribute("aria-pressed", "false");
  }

  function play(button, hz) {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state === "suspended") ctx.resume();
    var osc = ctx.createOscillator(), gain = ctx.createGain(), t = ctx.currentTime;
    osc.type = "sine";
    osc.frequency.value = hz;
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(0.25, t + 0.05);
    gain.gain.setValueAtTime(0.25, t + 2.6);
    gain.gain.linearRampToValueAtTime(0, t + 3);
    osc.connect(gain).connect(ctx.destination);
    osc.start(t);
    osc.stop(t + 3.05);
    current = { osc: osc, gain: gain, button: button };
    button.setAttribute("aria-pressed", "true");
    osc.onended = function () {
      if (current && current.osc === osc) { current = null; button.setAttribute("aria-pressed", "false"); }
    };
  }

  document.addEventListener("click", function (e) {
    var button = e.target.closest("[data-tone]");
    if (!button) return;
    var wasThis = current && current.button === button;
    stop();
    if (!wasThis) play(button, parseFloat(button.getAttribute("data-tone")));
  });
})();
