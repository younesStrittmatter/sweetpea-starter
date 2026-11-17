// Widgets of the Simon page (teaching/simon_previous_trial). Uses the shared helpers of demo.js
// and the generated blocks in window.SIMON (data.js next to the page).
//
//   <div class="sm-intro"></div>     the task animation, pinned, three scroll steps
//   <div class="sm-switch"></div>    choose sets of two, four or twelve
//   <div class="sm-story"></div>     one block of trials, pinned, four scroll steps
(function () {
  const pct = (x) => Math.round(100 * x) + "%";

  document.addEventListener("DOMContentLoaded", () => {
    const kit = window.mpKit, data = window.SIMON;
    if (!kit || !data) return;
    const { el, flash, scrollSteps, stepControls, captionOf } = kit;
    const KEY = data.key;
    const kind = (side, colour) => (KEY[colour] === side ? "congruent" : "incongruent");

    // A small screen with a coloured square on the left or the right.
    function square(side, colour, cls) {
      const s = el("div", cls); const dot = el("i", "sm-dot sm-" + colour + " sm-at-" + side); s.append(dot); return s;
    }

    // ---- The task, the question, the trial before ----------------------------------------------
    function intro(root) {
      const steps = [
        { title: "The task", coded: false, before: false,
          text: "A red or a green square appears on the left or on the right. Press the key of its colour. Where it appears does not matter." },
        { title: "The question", coded: true, before: false,
          text: "Are responses faster when the square is on the side of its key (congruent) than on the other side (incongruent)? That difference is the Simon effect." },
        { title: "The trial before", coded: true, before: true,
          text: "The Simon effect depends on the trial before: it is smaller right after an incongruent trial. So both trial types should have the same kinds of trial before them." },
      ];
      const trials = [["right", "red"], ["left", "red"], ["left", "green"], ["right", "green"], ["left", "red"], ["right", "red"]];
      const head = captionOf(steps);
      const stage = el("div", "mp-demo sm-demo");
      const screen = el("div", "mp-screen sm-screen"); const cross = el("span", "", "+"); const dot = el("i", "sm-dot");
      screen.append(cross, dot);
      const keys = el("div", "sm-keys");
      const keyOf = {};
      ["left", "right"].forEach((sideName) => {
        const colour = Object.keys(KEY).find((c) => KEY[c] === sideName);
        const k = el("div", "sm-key"); k.append(el("i", "sm-dot sm-" + colour), el("span", "", `${sideName} key: ${colour}`));
        keys.append(k); keyOf[sideName] = k;
      });
      const names = ["fixation", "square", "response"];
      const phases = el("div", "mp-steps"); names.forEach((n) => phases.append(el("span", "", n)));
      const record = el("div", "mp-record");
      const boxes = ["Square", "Correct key", "Trial type", "Trial before"].map((n) => {
        const d = el("div"); d.append(el("small", "", n), el("b", "", ""), el("em", "", "")); record.append(d); return d;
      });
      boxes[2].classList.add("mp-type"); boxes[3].classList.add("sm-before");
      const controls = el("div", "mp-controls");
      const back = el("button", "", "◀ Back"), play = el("button", "", "Play"), stop = el("button", "", "Pause"), next = el("button", "", "Next ▶");
      const where = el("span", "mp-where", "");
      controls.append(back, play, stop, next, where);
      stage.append(screen, keys, phases, record, controls);

      let i = 0, phase = 0, timer = null, playing = true, coded = false, before = false;
      const durations = [700, 1300, 1700];
      function draw() {
        const [side, colour] = trials[i], k = kind(side, colour);
        const [pSide, pColour] = trials[(i - 1 + trials.length) % trials.length];
        [...phases.children].forEach((s, n) => s.classList.toggle("on", n === phase));
        cross.style.visibility = phase === 0 ? "visible" : "hidden";
        dot.className = "sm-dot" + (phase >= 1 ? ` sm-${colour} sm-at-${side} on` : "");
        Object.entries(keyOf).forEach(([name, node]) => node.classList.toggle("on", phase === 2 && KEY[colour] === name));
        const shown = phase >= 1, typed = coded && shown;
        boxes[0].children[1].textContent = shown ? colour : ""; boxes[0].children[2].textContent = shown ? "on the " + side : "";
        boxes[1].children[1].textContent = phase === 2 ? KEY[colour] : ""; boxes[1].children[2].textContent = phase === 2 ? "the key of " + colour : "";
        boxes[2].children[1].textContent = typed ? k : "";
        boxes[2].children[2].textContent = typed ? (k === "congruent" ? "square on the side of its key" : "square on the other side") : "";
        boxes[3].children[1].textContent = before && shown ? kind(pSide, pColour) : "";
        boxes[3].children[2].textContent = before && shown ? "the trial just before" : "";
        stage.classList.toggle("mp-is-congruent", typed && k === "congruent");
        stage.classList.toggle("mp-is-incongruent", typed && k === "incongruent");
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
        coded = steps[n].coded; before = steps[n].before;
        stage.classList.toggle("mp-coded", coded); stage.classList.toggle("sm-with-before", before);
        draw(); row.show(n);
      }
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { pause(); draw(); } else { mark(); tick(); }
      scroller.go = scrollSteps(track, pin, steps.length, show).go;
    }

    // ---- Which sets: two, four, or the twelve of the original experiment -------------------------
    const NAMES = { 2: "two", 4: "four", 12: "twelve" };
    let variant = "4";
    try { variant = localStorage.getItem("sm-sets") || "4"; } catch (e) { /* no storage */ }
    if (!data.variants[variant]) variant = "4";
    const listeners = [];
    function choose(v) {
      variant = v; document.documentElement.dataset.smSets = v;
      try { localStorage.setItem("sm-sets", v); } catch (e) { /* no storage */ }
      listeners.forEach((f) => f());
    }
    function switcher(root) {
      root.append(el("span", "sm-switch-label", "Sets of"));
      const buttons = ["2", "4", "12"].map((v) => {
        const b = el("button", "", v === "12" ? "twelve (the original experiment)" : NAMES[v]);
        b.addEventListener("click", () => choose(v)); root.append(b); return { v, b };
      });
      listeners.push(() => buttons.forEach(({ v, b }) => b.classList.toggle("on", v === variant)));
    }

    // ---- One block of trials: the original sets, the problem, the design -------------------------
    function story(root) {
      const OK = "✓", NO = "✗", NOTE = "!";
      const CONTENT = { 2: "one congruent and one incongruent trial", 4: "two congruent and two incongruent trials", 12: "six congruent and six incongruent trials" };
      const PRICE = {
        2: [NOTE, "every border is a repeat, so only one order of trial types is left"],
        4: [NOTE, "every border is a repeat: a set starts with the very square that ended the last one"],
        12: [OK, "none found"],
      };
      // why the design reaches its balance the way it does, for each set size
      const WHY = {
        2: " A set of two always holds a switch, so every border has to be a repeat.",
        4: " A square occurs once per set, so it can repeat only across a border, and every border has to be one.",
        12: "",
      };
      const ROWS = [["inside", "Inside a set", 0.5], ["border", "At the border", 0.5], ["total", "In total", 0.5]];   // repeats of the trial type
      function stepsFor(v) {
        const V = data.variants[v], name = NAMES[V.size], L = V.long_run;
        const lead = V.size === 12 ? "Trials" : "A smaller version of the original. Trials";
        return [
          { title: "The original design", block: "original", coded: true, marks: false, chart: null,
            text: `${lead} come in sets of ${name}: ${CONTENT[V.size]}, in random order. The authors' reason: showing every combination equally often avoids contingency learning.`,
            balance: [[OK, `${CONTENT[V.size]} in every set`], null, null] },
          { title: "Inside a set", block: "original", coded: true, marks: true, focus: "inside",
            chart: { inside: L.type_inside }, chartNote: "Expected: the rate over many blocks of shuffled sets. A single block varies around it.",
            text: `Inside a set, the type just shown is scarcer among the trials that are left. A switch is more likely than a repeat: the same type follows ${V.size === 2 ? "never" : "in " + pct(L.type_inside) + " of cases"}.`,
            balance: [[OK, `${CONTENT[V.size]} in every set`], [NO, "inside a set: more switches than repeats"], null] },
          { title: "At the border", block: "original", coded: true, marks: true, focus: "border",
            chart: { inside: L.type_inside, border: L.type_border, total: L.type }, chartNote: "Expected: the rate over many blocks of shuffled sets. A single block varies around it.",
            text: `From the last trial of a set to the first of the next, repeat and switch are equally likely. That is fair, but it cannot make up for the sets. In total the same type follows in ${pct(L.type)} of cases.`,
            balance: [[OK, `${CONTENT[V.size]} in every set`], [NO, `in total: a repeat in ${pct(L.type)} of cases, not in half`], null] },
          { title: "The design", block: "design", coded: true, marks: true, focus: "all",
            // with sets of twelve a block on the page has only four borders, too few to show as a rate
            chart: V.size === 12 ? { total: V.design_rates.type } : { inside: V.design_same_type_inside, border: V.design_same_type_at_borders, total: V.design_rates.type },
            chartNote: V.size === 12 ? "Counted in the block shown. The total is the same in every block." : "Counted in the block shown, and the same in every block: with sets this small the design leaves no other way.",
            text: "Keep the sets and make the trial before part of the design: each trial type follows each trial type equally often." + WHY[V.size],
            balance: [[OK, `${CONTENT[V.size]} in every set`], [OK, "in total: a repeat in exactly half of the cases"], PRICE[V.size]] },
        ];
      }
      const BALANCE = ["How often each trial type is shown", "The trial before", "The price"];
      let steps = stepsFor(variant);
      const head = captionOf(steps);   // the titles are the same for every variant; the texts are set in show()

      const SLOTS = 49;
      const strip = el("div", "sm-strip sm-plain"); const tiles = [];
      for (let n = 0; n < SLOTS; n += 1) {
        const tile = el("div", "sm-tile"); const dot = el("i", "sm-dot"); const mark = el("span", "sm-mark", "");
        tile.append(dot, mark); strip.append(tile); tiles.push({ tile, dot, mark });
      }
      const legend = el("div", "mp-legend sm-legend");
      legend.innerHTML = '<span><i class="mp-congruent"></i>congruent</span><span><i class="mp-incongruent"></i>incongruent</span><span class="sm-arrow-key"><i class="sm-key-line sm-arc-repeat"></i>repeat: same type as the trial before</span><span class="sm-arrow-key"><i class="sm-key-line sm-arc-switch"></i>switch: the other type</span>';

      const lower = el("div", "mp-lower");
      const chart = el("div", "mp-panel"); chart.append(el("h5", "", "How often the same trial type follows (a repeat)"));
      const chartBox = el("div", "sm-chart");
      const bars = ROWS.map(([key, label, target]) => {
        const r = el("div", "sm-chart-row"), trackEl = el("div", "sm-chart-track"), fill = el("div", "sm-chart-fill"), tick = el("i", "sm-chart-tick"), value = el("span", "sm-chart-value", "");
        tick.style.left = 100 * target + "%"; trackEl.append(fill, tick);
        r.append(el("span", "", label), trackEl, value); chartBox.append(r);
        return { key, target, fill, value, row: r };
      });
      const note = el("div", "sm-note", "");
      chart.append(chartBox, note);
      const balance = el("div", "mp-panel"); balance.append(el("h5", "", "What is balanced"));
      const lines = BALANCE.map((name) => {
        const r = el("div", "mp-balance-row"), icon = el("span", "mp-icon", ""), what = el("span", "mp-what", name), how = el("span", "mp-how", "");
        r.append(icon, what, how); balance.append(r); return { row: r, icon, how, last: null };
      });
      lower.append(chart, balance);

      const track = el("div", "mp-track"), pin = el("div", "mp-pin"), inner = el("div", "mp-inner");
      let current = -1, shown = null, grouped = null; const scroller = { go: () => {} };
      const row = stepControls(steps.length, (n) => scroller.go(n), () => current);
      inner.append(head.caption, strip, legend, lower, row.controls); pin.append(inner); track.append(pin); root.append(track);

      // A short curved arrow from each trial to the next, above the tiles and centred on the gap
      // between the two: one colour and a solid line for a repeat, another colour and a dashed line for a switch.
      const SVG = "http://www.w3.org/2000/svg";
      function arrows() {
        const W = 22, H = 12;
        tiles.forEach((t, k) => {
          const kindOf = t.mark.dataset.kind; t.mark.textContent = "";
          if (!kindOf || t.tile.classList.contains("sm-absent")) return;
          const before = k > 0 ? tiles[k - 1].tile : null, sameRow = !!before && before.offsetTop === t.tile.offsetTop;
          // When the trial before is at the end of the row above (or is the extra trial in front of
          // the first set), a faint copy of it is shown in front of this trial, so that the arrow has
          // something to start from.
          const GHOST_GAP = 8, w = t.tile.offsetWidth;
          const gap = sameRow ? t.tile.offsetLeft - (before.offsetLeft + before.offsetWidth) : GHOST_GAP;
          if (!sameRow) {
            const type = t.mark.dataset.before === "congruent" ? "c" : "i";
            const ghost = el("span", "sm-ghost sm-" + type, type);
            ghost.style.width = w + "px"; ghost.style.left = -(w + GHOST_GAP) + "px";
            t.mark.append(ghost);
          }
          const svg = document.createElementNS(SVG, "svg");
          svg.setAttribute("width", W); svg.setAttribute("height", H); svg.setAttribute("class", "sm-arc sm-arc-" + kindOf);
          svg.style.left = -gap / 2 - W / 2 + "px";
          const path = document.createElementNS(SVG, "path"), head = document.createElementNS(SVG, "path");
          path.setAttribute("d", `M 2 ${H - 1} Q ${W / 2} -3 ${W - 3} ${H - 3}`);
          head.setAttribute("d", `M ${W - 8} ${H - 4} L ${W - 2} ${H - 1} L ${W - 2} ${H - 8}`); head.setAttribute("class", "sm-head");
          svg.append(path, head); t.mark.append(svg);
        });
      }
      window.addEventListener("resize", () => requestAnimationFrame(arrows));

      function show(n, force) {
        if (n === current && !force) return;
        const first = current === -1; current = n;
        const V = data.variants[variant], s = steps[n];
        // The design has one extra trial in front of the first set. It is not shown as a trial of
        // its own, only as the faint "trial before" of the first one.
        const lead = s.block === "design" ? kind(...V.design[0]) : null;
        const block = lead ? V.design.slice(1) : V[s.block], kinds = block.map(([side, colour]) => kind(side, colour));
        head.show(n, !first);
        head.caption.querySelector(".mp-text").textContent = s.text;
        const key = variant + s.block;
        if (shown !== key && !first) flash(strip);
        shown = key;
        strip.classList.toggle("sm-coded", s.coded); strip.classList.toggle("sm-marks", s.marks);
        strip.dataset.size = V.size;
        // one container per set, so that a row never breaks in the middle of a set
        if (grouped !== variant + block.length) {
          grouped = variant + block.length; strip.textContent = "";
          let group = null;
          tiles.forEach((t, k) => {
            if (k % V.size === 0) { group = el("div", "sm-set"); strip.append(group); }
            group.append(t.tile);
          });
        }
        legend.classList.toggle("on", s.coded);
        legend.classList.toggle("sm-with-arrows", s.marks);
        tiles.forEach((t, k) => {
          const present = k < block.length;
          t.tile.classList.toggle("sm-absent", !present);
          t.tile.classList.toggle("sm-set-end", present && (k + 1) % V.size === 0);
          t.tile.classList.toggle("sm-after-border", present && k % V.size === 0 && (k > 0 || !!lead));   // its trial before is in the previous set
          if (!present) return;
          const [side, colour] = block[k];
          t.dot.className = `sm-dot sm-${colour} sm-at-${side}`;
          t.tile.classList.toggle("sm-c", kinds[k] === "congruent"); t.tile.classList.toggle("sm-i", kinds[k] === "incongruent");
          const beforeKind = k === 0 ? lead : kinds[k - 1];
          t.mark.dataset.kind = !beforeKind ? "" : kinds[k] === beforeKind ? "repeat" : "switch";
          t.mark.dataset.before = beforeKind || "";
        });
        // a set container without any trial takes no room, so that every row is laid out alike
        strip.querySelectorAll(".sm-set").forEach((g) => g.classList.toggle("sm-gone", ![...g.children].some((c) => !c.classList.contains("sm-absent"))));
        requestAnimationFrame(arrows);
        chartBox.classList.toggle("on", !!s.chart); note.classList.toggle("on", !!s.chart); note.textContent = s.chartNote || "";
        chart.classList.toggle("mp-marked", s.focus === "inside" || s.focus === "border");
        chart.classList.toggle("sm-not-yet", !s.chart);   // the panel itself stays out of sight until it has something to show
        strip.dataset.focus = s.focus || "";
        bars.forEach((b) => {
          const has = !!s.chart && s.chart[b.key] !== undefined, x = has ? s.chart[b.key] : 0, off = Math.abs(x - b.target) > 0.005;
          b.row.classList.toggle("sm-row-hidden", !has);
          b.fill.style.width = 100 * x + "%"; b.fill.classList.toggle("sm-off", off);
          b.value.textContent = has ? pct(x) : "";
        });
        lines.forEach((line, k) => {
          const entry = s.balance[k];
          line.row.classList.toggle("mp-hidden", !entry);
          if (entry) {
            line.icon.textContent = entry[0]; line.how.textContent = entry[1];
            line.row.classList.toggle("mp-not", entry[0] === NO); line.row.classList.toggle("sm-price", entry[0] === NOTE);
          }
          const id = entry ? entry.join() : null;
          if (!first && id && line.last !== id) flash(line.row);
          line.last = id;
        });
        row.show(n);
      }
      scroller.go = scrollSteps(track, pin, steps.length, show).go;
      listeners.push(() => { steps = stepsFor(variant); show(Math.max(0, current), true); window.dispatchEvent(new Event("resize")); });
    }

    document.querySelectorAll(".sm-switch").forEach(switcher);
    document.querySelectorAll(".sm-intro").forEach(intro);
    document.querySelectorAll(".sm-story").forEach(story);
    choose(variant);
  });
})();
