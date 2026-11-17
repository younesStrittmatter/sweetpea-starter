// Widgets of the teaching pages. No dependencies.
//
//   <div class="mp-intro" data-trials="4>1, 9>4"></div>       the task animation, pinned, three scroll steps
//   <div class="mp-story" data-numbers="1,4,6,9" data-mapping="1>6,4>9,6>1,9>4"></div>
//                                                              all pairs, pinned, five scroll steps
(function () {
  const side = (n) => (Number(n) < 5 ? "smaller" : "larger");
  const kind = (p, t) => (p === t ? "same" : side(p) === side(t) ? "congruent" : "incongruent");
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const mask = () => Array.from({ length: 7 }, () => "abcdefghkmnpqrstuvwxyzABCDEFGHKMNPQRSTUVWXYZ"[Math.floor(Math.random() * 44)]).join("");
  const flash = (node) => { node.classList.remove("mp-changed"); void node.offsetWidth; node.classList.add("mp-changed"); };

  // A pinned block with `count` scroll steps. The page scrolls normally; once the scrolling has
  // stopped, it glides to the fixed position of the next or the previous step.
  // Returns { go(i) }. `draw(i)` is called whenever the step changes.
  function scrollSteps(track, pin, count, draw) {
    const last = count - 1;
    const stepLength = () => Math.round(window.innerHeight * 0.5);
    const offset = () => parseFloat(getComputedStyle(pin).top) || 0;
    // Room before the first and after the last step: the block is already (or still) pinned there,
    // but nothing changes yet, so scrolling into or out of it does not start a step at once.
    const room = () => Math.round(window.innerHeight * 0.35);
    const scrolled = () => offset() - track.getBoundingClientRect().top - room();
    let anchor = 0, settling = false, quiet = null;
    function size() {
      // the block fills the window below the page header; if its content is taller, it is scaled down to fit
      const available = window.innerHeight - offset();
      const inner = pin.firstElementChild;
      inner.style.zoom = 1;
      if (inner.offsetHeight > available) inner.style.zoom = available / inner.offsetHeight;
      pin.style.height = available + "px";
      track.style.height = 2 * room() + last * stepLength() + available + "px";
    }
    function onScroll() { draw(Math.max(0, Math.min(last, Math.round(scrolled() / stepLength())))); }
    function go(i) {
      anchor = Math.max(0, Math.min(last, i)); settling = true;
      window.scrollTo({ top: window.scrollY + anchor * stepLength() - scrolled(), behavior: "smooth" });
    }
    function settle() {
      if (settling) { settling = false; return; }
      const at = scrolled(), length = stepLength();
      if (at < -length * 0.5 || at > last * length + length * 0.5) { anchor = at < 0 ? 0 : last; return; }  // outside the block
      const moved = at - anchor * length;
      if (Math.abs(moved) < 3) return;
      // a scroll of any size moves exactly to the next or the previous step (or further, if it went further)
      const target = Math.abs(moved) < 24 ? anchor : anchor + Math.sign(moved) * Math.max(1, Math.round(Math.abs(moved) / length));
      if (target < 0 || target > last) { anchor = Math.max(0, Math.min(last, target)); return; }      // leaving the block
      go(target);
    }
    window.addEventListener("scroll", () => {
      requestAnimationFrame(onScroll);
      clearTimeout(quiet); quiet = setTimeout(settle, 130);
    }, { passive: true });
    window.addEventListener("resize", () => { size(); onScroll(); });
    size(); onScroll();
    return { go };
  }

  // The caption of a pinned block: the titles of all steps on a rail that slides, with the current
  // one in the middle and the others fainter the further away they are; below it the text of the step.
  function captionOf(steps) {
    const caption = el("div", "mp-caption"), frame = el("div", "mp-titles"), rail = el("div", "mp-rail"), text = el("span", "mp-text", "");
    const titles = steps.map((s) => { const t = el("b", "", s.title); rail.append(t); return t; });
    frame.append(rail); caption.append(frame, text);
    const FAINT = [1, 0.4, 0.2, 0.1];
    let current = 0;
    function place() {
      const t = titles[current];
      rail.style.transform = `translateX(${frame.clientWidth / 2 - (t.offsetLeft + t.offsetWidth / 2)}px)`;
    }
    function show(i, animate) {
      current = i;
      titles.forEach((t, k) => { t.style.opacity = FAINT[Math.min(Math.abs(k - i), FAINT.length - 1)]; t.classList.toggle("on", k === i); });
      place();
      text.textContent = steps[i].text;
      if (animate) flash(text);
    }
    window.addEventListener("resize", place);
    window.addEventListener("load", place);
    return { caption, show };
  }

  // The row under a pinned block: previous step, next step, and where we are.
  function stepControls(count, go, current) {
    const controls = el("div", "mp-controls mp-step-controls");
    const up = el("button", "mp-wide", "↑ Previous step"), down = el("button", "mp-wide", "↓ Next step"), where = el("span", "mp-where", "");
    up.addEventListener("click", () => go(current() - 1));
    down.addEventListener("click", () => go(current() + 1));
    controls.append(up, down, where);
    return { controls, show: (i) => { where.textContent = `Step ${i + 1} of ${count}`; } };
  }

  // The task animation: fixation, mask, prime, mask, target, response; with a record of the trial below.
  // setCoded(true) also names and colours the trial as congruent or incongruent.
  function demo(root, trialSpec) {
    const trials = trialSpec.split(",").map((s) => s.trim().split(">"));
    const screen = el("div", "mp-screen", "+");
    const names = ["fixation", "mask", "prime", "mask", "target", "response"];
    const steps = el("div", "mp-steps"); names.forEach((n) => steps.append(el("span", "", n)));
    const record = el("div", "mp-record");
    const boxes = ["Prime", "Target", "Response", "Trial type"].map((n) => {
      const d = el("div"); d.append(el("small", "", n), el("b", "", ""), el("em", "", "")); record.append(d); return d;
    });
    const cells = boxes.map((d) => d.children[1]), hints = boxes.map((d) => d.children[2]);
    // A number line from 1 to 9 with five in the middle: where the prime and the target are.
    const line = el("div", "mp-line");
    const ticks = [];
    for (let n = 1; n <= 9; n += 1) {
      const tick = el("div", "mp-tick" + (n === 5 ? " mp-five" : ""));
      const above = el("span", "mp-mark mp-mark-prime", "prime"), below = el("span", "mp-mark mp-mark-target", "target");
      tick.append(above, el("b", "", String(n)), below); line.append(tick); ticks.push({ n: String(n), above, below });
    }
    const sides = el("div", "mp-sides"); sides.append(el("span", "", "smaller than 5"), el("span", "", "larger than 5"));
    const scale = el("div", "mp-scale"); scale.append(line, sides);
    boxes[3].classList.add("mp-type");
    const controls = el("div", "mp-controls");
    const back = el("button", "", "◀ Back"), play = el("button", "", "Play"), stop = el("button", "", "Pause"), next = el("button", "", "Next ▶");
    const where = el("span", "mp-where", "");
    controls.append(back, play, stop, next, where);
    const note = el("div", "mp-note", "Slowed down. In the experiment the prime is on screen for 10 to 80 ms.");
    root.append(screen, steps, record, scale, controls, note);

    let i = 0, step = 0, timer = null, playing = true, coded = false;
    const durations = [700, 450, 1000, 450, 1300, 1700];
    function draw() {
      const [p, t] = trials[i]; const k = kind(p, t) === "incongruent" ? "incongruent" : "congruent";
      [...steps.children].forEach((s, n) => s.classList.toggle("on", n === step));
      screen.classList.toggle("mp-dim", step === 2);
      screen.textContent = ["+", mask(), p, mask(), t, t][step];
      cells[0].textContent = step >= 2 ? p : "";
      cells[1].textContent = step >= 4 ? t : "";
      cells[2].textContent = step === 5 ? side(t) + " than 5" : "";
      const typed = coded && step >= 4;
      cells[3].textContent = typed ? k : "";
      // with the question asked, say for prime and target on which side of five they are
      hints[0].textContent = coded && step >= 2 ? side(p) + " than 5" : "";
      hints[1].textContent = coded && step >= 4 ? side(t) + " than 5" : "";
      hints[3].textContent = typed ? (k === "congruent" ? "same side of 5" : "opposite sides of 5") : "";
      ticks.forEach((tick) => {
        tick.above.classList.toggle("on", coded && step >= 2 && tick.n === p);
        tick.below.classList.toggle("on", coded && step >= 4 && tick.n === t);
      });
      root.classList.toggle("mp-is-congruent", typed && k === "congruent");
      root.classList.toggle("mp-is-incongruent", typed && k === "incongruent");
      where.textContent = `Trial ${i + 1} of ${trials.length}`;
    }
    function move(by) {
      step += by;
      if (step === names.length) { step = 0; i = (i + 1) % trials.length; }
      if (step < 0) { step = names.length - 1; i = (i - 1 + trials.length) % trials.length; }
    }
    function tick() { draw(); timer = setTimeout(() => { move(1); tick(); }, durations[step]); }
    function mark() {
      play.classList.toggle("on", playing); stop.classList.toggle("on", !playing);
      play.setAttribute("aria-pressed", playing); stop.setAttribute("aria-pressed", !playing);
    }
    function pause() { playing = false; clearTimeout(timer); mark(); }
    play.addEventListener("click", () => { if (!playing) { playing = true; mark(); tick(); } });
    stop.addEventListener("click", pause);
    next.addEventListener("click", () => { pause(); move(1); draw(); });
    back.addEventListener("click", () => { pause(); move(-1); draw(); });
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { pause(); draw(); }
    else { mark(); tick(); }
    return { setCoded(on) { coded = on; root.classList.toggle("mp-coded", on); draw(); } };
  }

  // The task, then the question: the same animation, first plain, then with every trial named
  // and coloured as congruent or incongruent.
  function intro(root) {
    const steps = [
      { title: "The task", coded: false,
        text: "A number is flashed between two masks, too briefly to be seen (the prime). A visible number follows (the target). Is the target smaller or larger than five?" },
      { title: "The question", coded: true,
        text: "Are responses faster when prime and target are on the same side of five (congruent) than when they are on opposite sides (incongruent)?" },
      { title: "The assumption", coded: true,
        text: "If so, the unseen prime was processed. That only follows if congruent and incongruent trials differ in nothing else." },
    ];
    const track = el("div", "mp-track"), pin = el("div", "mp-pin");
    const head = captionOf(steps), caption = head.caption;
    const stage = el("div", "mp-demo");
    const player = demo(stage, root.dataset.trials);
    let current = -1;
    const scroller = { go: () => {} };
    const row = stepControls(steps.length, (i) => scroller.go(i), () => current);
    const inner = el("div", "mp-inner"); inner.append(caption, stage, row.controls);
    pin.append(inner); track.append(pin); root.append(track);
    function draw(i) {
      if (i === current) return;
      const first = current === -1; current = i;
      head.show(i, !first);
      player.setCoded(steps[i].coded);
      row.show(i);
    }
    scroller.go = scrollSteps(track, pin, steps.length, draw).go;
  }

  // All pairs in two panels, how often each target follows each prime, and a list of what is balanced.
  // Colour, marks and list rows appear only in the step they belong to, so no state gives away a later one.
  function story(root) {
    const numbers = root.dataset.numbers.split(",");
    const mapped = new Set(root.dataset.mapping.split(","));
    const once = () => 1;
    const doubled = (k) => ({ same: 0, congruent: 2, incongruent: 1 }[k]);
    const design = (k, p, t) => (k === "same" ? 0 : k === "congruent" ? 1 : mapped.has(p + ">" + t) ? 1 : 0);
    const OK = "✓", NO = "✗";
    // balance: one entry per row of "What is balanced"; a row stays hidden until its first entry.
    const steps = [
      { title: "The original design", text: "Primes and targets are 1, 4, 6 or 9. Every pair is shown equally often, in random order.",
        count: once, mark: () => false, colour: "none",
        balance: [[OK, "equally often"], null, null] },
      { title: "The problem", text: "4 of the 8 congruent pairs repeat the number. No incongruent pair can. Congruent trials may be faster because the number repeats.",
        count: once, mark: (k) => k === "same", hatch: true, colour: "same",
        balance: [[OK, "equally often"], [NO, "only on congruent trials"], null] },
      { title: "A first idea", text: "Remove the same-number pairs and show the other congruent pairs twice, so that half of the trials stay congruent.",
        count: doubled, mark: () => false, colour: "none",
        balance: [[OK, "equally often"], [OK, "on no trial"], null] },
      { title: "A new problem", text: "Now the prime tells which number is coming: after a 1, a 4 is twice as likely as a 6 or a 9. The congruent target is the expected one.",
        count: doubled, mark: (k) => k === "congruent", bars: true, colour: "all",
        balance: [[OK, "equally often"], [OK, "on no trial"], [NO, "congruent target 50%, each incongruent target 25%"]] },
      { title: "The design", text: "Give every prime one congruent and one fixed incongruent target. No number repeats, half of the trials are congruent, and both targets are equally expected.",
        count: design, mark: () => false, colour: "all",
        balance: [[OK, "equally often"], [OK, "on no trial"], [OK, "50% for the target of every trial"]] },
    ];
    const BALANCE = ["Congruent and incongruent trials", "Number repetition", "How expected the target number is after its prime"];

    const track = el("div", "mp-track"), pin = el("div", "mp-pin");
    const head = captionOf(steps), caption = head.caption;

    const columns = el("div", "mp-columns"); const chips = [];
    ["congruent", "incongruent"].forEach((name) => {
      const column = el("div", "mp-column mp-col-" + name);
      column.append(el("h5", "", name === "congruent" ? "Congruent: same side of five" : "Incongruent: opposite sides"));
      const box = el("div", "mp-chips");
      numbers.forEach((p) => numbers.forEach((t) => {
        if ((side(p) === side(t)) !== (name === "congruent")) return;
        const chip = el("div", "mp-chip"); const n = el("span", "mp-count", "");
        chip.append(el("span", "mp-box mp-prime", p), el("span", "mp-arrow", "→"), el("span", "mp-box", t), n);
        box.append(chip); chips.push({ chip, n, p, t, k: kind(p, t), last: null });
      }));
      column.append(box); columns.append(column);
    });

    const lower = el("div", "mp-lower");
    const follow = el("div", "mp-panel");
    follow.append(el("h5", "", "After each prime: how often each target follows"));
    const bars = numbers.map((p) => {
      const row = el("div", "mp-stack-row"), stack = el("div", "mp-stack");
      const segments = numbers.map((t) => {
        const seg = el("div", "mp-seg mp-" + kind(p, t)); const label = el("span", "", "");
        seg.append(label); stack.append(seg); return { t, seg, label };
      });
      row.append(el("span", "mp-stack-label", `prime ${p}`), stack); follow.append(row);
      return { p, segments };
    });
    const balance = el("div", "mp-panel");
    balance.append(el("h5", "", "What is balanced"));
    const lines = BALANCE.map((name) => {
      const row = el("div", "mp-balance-row"), icon = el("span", "mp-icon", ""), what = el("span", "mp-what", name), how = el("span", "mp-how", "");
      row.append(icon, what, how); balance.append(row); return { row, icon, how, last: null };
    });
    lower.append(follow, balance);

    let current = -1, barTimer = null;
    const scroller = { go: () => {} };
    const row = stepControls(steps.length, (i) => scroller.go(i), () => current);
    const inner = el("div", "mp-inner"); inner.append(caption, columns, lower, row.controls);
    pin.append(inner); track.append(pin); root.append(track);

    const LATER = 750;   // a count that goes up appears this long after the crosses
    function draw(i) {
      if (i === current) return;
      const first = current === -1; current = i;
      const s = steps[i];
      head.show(i, !first);
      const anyMark = chips.some((c) => s.mark(c.k));
      let raised = false;
      chips.forEach((c) => {
        const n = s.count(c.k, c.p, c.t);
        const up = !first && c.last !== null && n > c.last;
        clearTimeout(c.timer);
        const badge = () => {
          c.n.textContent = n ? n + "×" : "";
          c.n.classList.toggle("mp-strong", n === 2);
          if (!first && n === 2) flash(c.n);
        };
        if (up) { raised = true; c.timer = setTimeout(badge, LATER); } else badge();
        c.chip.classList.toggle("mp-removed", n === 0);
        c.chip.classList.toggle("mp-marked", s.mark(c.k) && !s.hatch);
        c.chip.classList.toggle("mp-chip-same", !!s.hatch && s.mark(c.k));
        c.chip.classList.toggle("mp-faded", anyMark && !s.mark(c.k) && n > 0);
        if (!first && c.last !== n && !up) flash(c.chip);
        c.last = n;
      });
      const drawBars = () => bars.forEach((b) => {
        const counts = b.segments.map((g) => s.count(kind(b.p, g.t), b.p, g.t));
        const total = counts.reduce((x, y) => x + y, 0);
        b.segments.forEach((g, k) => {
          const share = (100 * counts[k]) / total;
          g.seg.style.width = share + "%";
          g.seg.classList.toggle("mp-empty", counts[k] === 0);
          // colour only what the current step is about, so the chart does not give away a later step
          const k2 = kind(b.p, g.t);
          g.seg.classList.toggle("mp-neutral", !(s.colour === "all" || (s.colour === "same" && k2 === "same")));
          g.label.textContent = counts[k] ? `${g.t}: ${Math.round(share)}%` : "";
        });
      });
      clearTimeout(barTimer);
      if (raised) barTimer = setTimeout(drawBars, LATER); else drawBars();   // the chart follows the counts
      follow.classList.toggle("mp-marked", !!s.bars);
      lines.forEach((line, k) => {
        const entry = s.balance[k];
        line.row.classList.toggle("mp-hidden", !entry);
        if (entry) {
          line.icon.textContent = entry[0]; line.how.textContent = entry[1];
          line.row.classList.toggle("mp-not", entry[0] === NO);
        }
        const key = entry ? entry.join() : null;
        if (!first && key && line.last !== key) flash(line.row);
        line.last = key;
      });
      row.show(i);
    }
    scroller.go = scrollSteps(track, pin, steps.length, draw).go;
  }

  // Shared with the widgets of other teaching pages.
  window.mpKit = { el, flash, scrollSteps, stepControls, captionOf };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".mp-intro").forEach(intro);
    document.querySelectorAll(".mp-story").forEach(story);
  });
})();
