// Widgets of the distractor page (teaching/distractor_location). Uses the shared helpers of demo.js.
//
//   <div class="dl-intro"></div>     the search display, pinned, three scroll steps
//   <div class="dl-story"></div>     three designs and what each keeps and gives up; pinned, three scroll steps
(function () {
  const PLACES = 8, USUAL = 0;                       // eight places on a ring; the distractor's usual place is on top
  const pct = (x) => Math.round(100 * x) + "%";

  document.addEventListener("DOMContentLoaded", () => {
    const kit = window.mpKit;
    if (!kit) return;
    const { el, flash, scrollSteps, stepControls, captionOf } = kit;

    // A ring of eight places. draw(items) sets what is at each place.
    function ring(cls) {
      const box = el("div", "dl-ring " + (cls || "")), spots = [];
      for (let k = 0; k < PLACES; k += 1) {
        const angle = (2 * Math.PI * k) / PLACES - Math.PI / 2;
        const spot = el("i", "dl-spot");
        spot.style.left = 50 + 38 * Math.cos(angle) + "%"; spot.style.top = 50 + 38 * Math.sin(angle) + "%";
        box.append(spot); spots.push(spot);
      }
      return { box, spots };
    }
    const kindOf = (distractor) => (distractor === null ? "none" : distractor === USUAL ? "usual" : "other");
    const KIND = { none: "no distractor", usual: "distractor at its usual place", other: "distractor at another place" };

    // ---- The task, the usual place, the question ------------------------------------------------
    function intro(root) {
      const steps = [
        { title: "The task", usual: false, coded: false,
          text: "Find the diamond among eight shapes and report whether its line is upright or flat. On most trials one circle is red. It is irrelevant, and it distracts." },
        { title: "The usual place", usual: true, coded: false,
          text: "The red circle is at one place far more often than anywhere else. People learn to ignore that place." },
        { title: "The question", usual: true, coded: true,
          text: "Does a distractor at its usual place still slow the search? Compared: trials with the distractor there against trials with no distractor." },
      ];
      const trials = [[null, 3, "|"], [USUAL, 5, "—"], [USUAL, 2, "|"], [4, 6, "—"], [null, USUAL, "|"], [USUAL, 7, "—"]];
      const head = captionOf(steps);
      const stage = el("div", "mp-demo dl-demo");
      const display = ring("dl-display"); const cross = el("span", "dl-cross", "+"); display.box.append(cross);
      const names = ["fixation", "search", "response"];
      const phases = el("div", "mp-steps"); names.forEach((n) => phases.append(el("span", "", n)));
      const record = el("div", "mp-record dl-record");
      const boxes = ["Distractor", "Target", "Response"].map((n) => {
        const d = el("div"); d.append(el("small", "", n), el("b", "", ""), el("em", "", "")); record.append(d); return d;
      });
      const controls = el("div", "mp-controls");
      const back = el("button", "", "◀ Back"), play = el("button", "", "Play"), stop = el("button", "", "Pause"), next = el("button", "", "Next ▶");
      const where = el("span", "mp-where", "");
      controls.append(back, play, stop, next, where);
      stage.append(display.box, phases, record, controls);

      let i = 0, phase = 0, timer = null, playing = true, showUsual = false, coded = false;
      const durations = [700, 1700, 1500];
      function draw() {
        const [distractor, target, line] = trials[i], kind = kindOf(distractor), shown = phase >= 1;
        [...phases.children].forEach((s, n) => s.classList.toggle("on", n === phase));
        cross.style.visibility = "visible";
        display.spots.forEach((spot, k) => {
          spot.className = "dl-spot" + (shown ? (k === target ? " dl-target" : k === distractor ? " dl-distractor" : " dl-circle") : "")
            + (showUsual && k === USUAL ? " dl-usual" : "");
          spot.textContent = "";
          if (shown && k === target) spot.append(el("span", "dl-line", line));   // the diamond is a turned square; the line is turned back
        });
        boxes[0].children[1].textContent = shown ? (distractor === null ? "none" : "red circle") : "";
        boxes[0].children[2].textContent = shown && showUsual && distractor !== null ? (distractor === USUAL ? "at its usual place" : "at another place") : "";
        boxes[1].children[1].textContent = shown ? "diamond" : "";
        boxes[1].children[2].textContent = shown && showUsual ? (target === USUAL ? "at the distractor's usual place" : "at another place") : "";
        boxes[2].children[1].textContent = phase === 2 ? (line === "|" ? "upright" : "flat") : "";
        stage.dataset.kind = coded && shown ? kind : "";
        where.textContent = `Trial ${i + 1} of ${trials.length}`;
      }
      function move(by) {
        phase += by;
        if (phase === names.length) { phase = 0; i = (i + 1) % trials.length; }
        if (phase < 0) { phase = names.length - 1; i = (i - 1 + trials.length) % trials.length; }
      }
      function tick() { draw(); timer = setTimeout(() => { move(1); tick(); }, durations[phase]); }
      function mark() { play.classList.toggle("on", playing); stop.classList.toggle("on", !playing); }
      function pause() { playing = false; clearTimeout(timer); mark(); }
      play.addEventListener("click", () => { if (!playing) { playing = true; mark(); tick(); } });
      stop.addEventListener("click", pause);
      next.addEventListener("click", () => { pause(); move(1); draw(); });
      back.addEventListener("click", () => { pause(); move(-1); draw(); });

      const track = el("div", "mp-track"), pin = el("div", "mp-pin"), inner = el("div", "mp-inner");
      let current = -1; const scroller = { go: () => {} };
      const row = stepControls(steps.length, (n) => scroller.go(n), () => current);
      inner.append(head.caption, stage, row.controls); pin.append(inner); track.append(pin); root.append(track);
      function show(n) {
        if (n === current) return;
        const first = current === -1; current = n;
        head.show(n, !first);
        showUsual = steps[n].usual; coded = steps[n].coded;
        draw(); row.show(n);
      }
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { pause(); draw(); } else { mark(); tick(); }
      scroller.go = scrollSteps(track, pin, steps.length, show).go;
    }

    // ---- Three designs, one step each: what each keeps and what it gives up ----------------------
    function story(root) {
      const OK = "✓", NO = "✗";
      const EVEN = 1 / 8;
      // Trials of one block by kind of trial: [target elsewhere, target at the distractor's usual place].
      // "more" raises the target's share at the usual place only on trials with the distractor at another
      // place (10 to 7 there), which gives an even spread over all trials and leaves the baseline as it was.
      const DESIGNS = {
        original: { none: [7, 1], usual: [28, 0], other: [42, 7] },
        never: { none: [7, 0], usual: [28, 0], other: [42, 0] },
        more: { none: [49, 7], usual: [196, 0], other: [294, 70] },
      };
      const rates = (name) => {
        const c = DESIGNS[name], share = ([e, u]) => u / (e + u);
        const all = ["none", "usual", "other"].reduce((a, k) => [a[0] + c[k][0], a[1] + c[k][1]], [0, 0]);
        return { none: share(c.none), usual: 0, other: share(c.other), all: share(all) };
      };
      const WISHES = ["Every place holds the target equally often", "A distractor elsewhere says nothing about the target", "The baseline can use all its trials"];
      const steps = [
        { title: "The original design", design: "original",
          text: "The target goes to any free place, equally often. But two things cannot be in one place: with the distractor at its usual place, the target is never there.",
          gives: [[NO, `the usual place holds it on ${pct(rates("original").all)} of the trials; an even spread is 1 in 8`], [OK, "the target is about as likely at the usual place as anywhere"], [NO, "1 trial in 8 has its target where the other condition never has it"]] },
        { title: "Never there", design: "never",
          text: "Exclude it: the target is never at the distractor's usual place. Now both conditions have the same seven target places.",
          gives: [[NO, "the usual place never holds it, which can be learned"], [NO, "the target is never at the usual place"], [OK, "every trial has the target elsewhere"]] },
        { title: "More often elsewhere", design: "more",
          text: "Or make up for it, but only on the trials with the distractor at another place: there the target is at the usual place more often. Trials without a distractor are the baseline and stay as they were.",
          gives: [[OK, "every place on 1 trial in 8"], [NO, "with a distractor elsewhere, the target is likelier at the usual place"], [NO, "as in the original: 1 trial in 8 has its target where the other condition never has it"]] },
      ];
      const head = captionOf(steps);

      const kinds = el("div", "dl-kinds");
      const rings = ["none", "usual", "other"].map((kind) => {
        const card = el("div", "dl-kind"); const r = ring("dl-small"); const label = el("b", "", KIND[kind]), sub = el("span", "dl-sub", "");
        card.dataset.kind = kind; card.append(label, r.box, sub); kinds.append(card);
        return { kind, card, spots: r.spots, sub };
      });
      kinds.dataset.focus = "usual";
      const legend = el("div", "mp-legend dl-legend");
      legend.innerHTML = '<span><i class="dl-key dl-free"></i>the target can be here</span><span><i class="dl-key dl-distractor"></i>the distractor is here</span><span><i class="dl-key dl-usual-key"></i>the distractor’s usual place</span>';

      const lower = el("div", "mp-lower");
      const chart = el("div", "mp-panel"); chart.append(el("h5", "", "Target at the distractor’s usual place"));
      const chartBox = el("div", "sm-chart on");
      const ROWS = [["none", KIND.none], ["usual", KIND.usual], ["other", KIND.other], ["all", "all trials"]];
      const bars = ROWS.map(([key, label]) => {
        const r = el("div", "sm-chart-row dl-chart-row"), trackEl = el("div", "sm-chart-track"), fill = el("div", "sm-chart-fill"), tick = el("i", "sm-chart-tick"), value = el("span", "sm-chart-value", "");
        tick.style.left = 100 * EVEN * 3 + "%"; trackEl.append(fill, tick);   // the bar spans 0 to one third
        r.append(el("span", "", label), trackEl, value); chartBox.append(r);
        return { key, fill, value };
      });
      const note = el("div", "sm-note on", "The line marks an even spread: 1 trial in 8."); chart.append(chartBox, note);
      const gives = el("div", "mp-panel"); gives.append(el("h5", "", "What this design keeps, and what it gives up"));
      const lines = WISHES.map((name) => {
        const r = el("div", "mp-balance-row"), icon = el("span", "mp-icon", ""), what = el("span", "mp-what", name), how = el("span", "mp-how", "");
        r.append(icon, what, how); gives.append(r); return { row: r, icon, how };
      });
      lower.append(chart, gives);

      const track = el("div", "mp-track"), pin = el("div", "mp-pin"), inner = el("div", "mp-inner");
      let current = -1; const scroller = { go: () => {} };
      const row = stepControls(steps.length, (n) => scroller.go(n), () => current);
      inner.append(head.caption, kinds, legend, lower, row.controls); pin.append(inner); track.append(pin); root.append(track);

      const EXAMPLE_OTHER = 3;                         // the place of the distractor in the "another place" picture
      function show(n) {
        if (n === current) return;
        const first = current === -1; current = n;
        const s = steps[n], R = rates(s.design);
        head.show(n, !first);
        rings.forEach((r) => {
          const distractor = r.kind === "none" ? null : r.kind === "usual" ? USUAL : EXAMPLE_OTHER, x = R[r.kind];
          r.spots.forEach((spot, k) => {
            spot.className = "dl-spot " + (k === distractor ? "dl-distractor" : "dl-free") + (k === USUAL ? " dl-usual" : "")
              + (k === USUAL && k !== distractor && x === 0 ? " dl-never" : "") + (k === USUAL && k !== distractor && x > 0.15 ? " dl-more" : "");
          });
          r.sub.textContent = r.kind === "usual" ? "target there: impossible" : x === 0 ? "target there: never" : `target there: ${pct(x)}`;
          if (!first) flash(r.sub);
        });
        bars.forEach((b) => {
          const x = R[b.key];
          b.fill.style.width = Math.min(100, 100 * x * 3) + "%"; b.fill.classList.toggle("sm-off", Math.abs(x - EVEN) > 0.02);
          b.value.textContent = b.key === "usual" ? "impossible" : x === 0 ? "never" : pct(x);
        });
        lines.forEach((line, k) => {
          const entry = s.gives[k];
          line.icon.textContent = entry[0]; line.how.textContent = entry[1]; line.row.classList.toggle("mp-not", entry[0] === NO);
          if (!first) flash(line.row);
        });
        row.show(n);
      }
      scroller.go = scrollSteps(track, pin, steps.length, show).go;
    }

    document.querySelectorAll(".dl-intro").forEach(intro);
    document.querySelectorAll(".dl-story").forEach(story);
  });
})();
