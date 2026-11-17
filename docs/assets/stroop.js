/* A playable block of the Stroop experiment for the tutorial pages.
   <div class="stroop-demo" data-trials='[{"colour":"red","word":"green","congruency":"incongruent", ...}]'></div> */
(function () {
  var INK = { red: "#e5484d", green: "#30a46c", blue: "#3e8bff", yellow: "#e2b100" };
  var LABELS = [["congruency", "this trial"], ["trial_before", "trial before"], ["transition", "task"], ["context", "context"]];

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function build(root) {
    var trials;
    try { trials = JSON.parse(root.getAttribute("data-trials")); } catch (e) { return; }
    if (!trials || !trials.length || root.dataset.built) return;
    root.dataset.built = "1";
    var i = 0, timer = null, blank = false;

    var screen = el("div", "st-screen");
    var cue = el("div", "st-cue"), word = el("div", "st-word"), keys = el("div", "st-keys");
    screen.append(cue, word, keys);
    var chips = el("div", "st-chips");
    var strip = el("div", "st-strip");
    var tiles = trials.map(function (t, n) {
      var tile = el("button", "st-tile st-" + (t.congruency || "none"), t.congruency ? t.congruency[0] : "");
      tile.type = "button";
      tile.title = "trial " + (n + 1);
      if (n > 0 && t.block !== undefined && t.block !== trials[n - 1].block) tile.classList.add("st-newblock");
      tile.addEventListener("click", function () { stop(); i = n; show(); });
      strip.append(tile);
      return tile;
    });
    var controls = el("div", "st-controls");
    var prev = el("button", null, "‹ back"), play = el("button", "st-play", "▶ play"), next = el("button", null, "next ›");
    var count = el("span", "st-count");
    [prev, play, next].forEach(function (b) { b.type = "button"; });
    controls.append(prev, play, next, count);
    root.append(screen, chips, strip, controls);

    function show() {
      var t = trials[i];
      var reading = t.task === "read the word";
      cue.textContent = t.task ? t.task.toUpperCase() : "NAME THE COLOUR";
      cue.classList.toggle("st-cue-read", reading);
      word.textContent = blank ? "+" : t.word.toUpperCase();
      word.style.color = blank ? "" : INK[t.colour] || t.colour;
      keys.textContent = blank ? "" : "correct answer: " + (reading ? t.word : t.colour);
      screen.classList.toggle("st-context-b", t.context === "mostly incongruent");
      chips.textContent = "";
      LABELS.forEach(function (pair) {
        var value = t[pair[0]];
        if (value === undefined || value === "") return;
        var chip = el("span", "st-chip");
        chip.append(el("small", null, pair[1]), el("b", null, value));
        chips.append(chip);
      });
      tiles.forEach(function (tile, n) { tile.classList.toggle("on", n === i); });
      count.textContent = "trial " + (i + 1) + " of " + trials.length + (t.block !== undefined ? ", block " + t.block : "");
    }
    function stop() {
      clearTimeout(timer); timer = null; blank = false;
      play.textContent = "▶ play"; play.classList.remove("on");
    }
    function tick() {
      if (blank) { blank = false; i = (i + 1) % trials.length; show(); timer = setTimeout(tick, 1100); }
      else { blank = true; show(); timer = setTimeout(tick, 350); }
    }
    play.addEventListener("click", function () {
      if (timer) { stop(); show(); return; }
      play.textContent = "❚❚ pause"; play.classList.add("on");
      timer = setTimeout(tick, 1100);
    });
    prev.addEventListener("click", function () { stop(); i = (i - 1 + trials.length) % trials.length; show(); });
    next.addEventListener("click", function () { stop(); i = (i + 1) % trials.length; show(); });
    show();
  }

  function init() { document.querySelectorAll(".stroop-demo").forEach(build); }
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(init);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
