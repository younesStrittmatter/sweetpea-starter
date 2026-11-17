"""Builds skills/sweetpea/paradigms.md: for a research topic, which paradigms published studies used.

Run:  python dev/build_paradigm_index.py <folder with */metadata.yaml> [<another folder> ...]

Reads the title and abstract of each paper and looks for the names of paradigms and of topics, by
keyword. It writes titles, years and DOIs only; no abstract text is copied. A paper that does not
name its paradigm in the title or abstract is not found, so the index is a floor, not a survey.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

PARADIGMS = {
    "Stroop task": r"\bstroop\b", "flanker task": r"\bflanker", "Simon task": r"\bsimon (task|effect)",
    "task switching": r"task[- ]switch|switch cost", "n-back": r"\bn-?back\b|\b[123]-back\b",
    "go/no-go": r"go[/ -]no-?go", "stop-signal task": r"stop[- ]signal", "AX-CPT": r"\bax-?cpt\b",
    "demand selection task": r"demand selection", "effort discounting": r"effort[- ](based )?(discounting|choice|cost)|effort discount",
    "Sternberg task": r"\bsternberg\b", "change detection": r"change detection", "delayed estimation": r"delayed estimation|continuous report",
    "visual search": r"visual search", "additional singleton search": r"additional singleton|singleton distractor",
    "attentional blink": r"attentional blink", "spatial cueing": r"(spatial|posner|exogenous|endogenous) cue?ing|cueing (task|paradigm)",
    "dual task / PRP": r"dual[- ]task|psychological refractory", "priming": r"\bpriming\b", "masked priming": r"masked prim",
    "serial reaction time task": r"serial reaction time|\bsrt task", "statistical learning": r"statistical learning",
    "old/new recognition": r"recognition memory|old[/-]new", "free recall": r"free recall", "paired associates": r"paired[- ]associate",
    "prospective memory task": r"prospective memory", "lexical decision": r"lexical decision", "picture-word interference": r"picture[- ]word interference",
    "random dot motion": r"random[- ]dot|motion (discrimination|coherence)", "perceptual decision task": r"perceptual decision",
    "multi-armed bandit": r"\bbandit\b", "two-step task": r"two-step task|two-stage task", "reversal learning": r"reversal learning",
    "Iowa gambling task": r"iowa gambling", "delay discounting": r"delay discounting|intertemporal choice", "risky choice / gambles": r"risky (choice|decision)|gambl|lotter",
    "ultimatum / dictator game": r"ultimatum|dictator game", "trust / public goods game": r"trust game|public goods|prisoner'?s dilemma",
    "category learning": r"category learning|categori[sz]ation task", "foraging task": r"\bforaging\b", "confidence rating task": r"confidence (rating|judg)",
    "temporal reproduction / timing": r"time (perception|estimation)|interval timing|temporal (reproduction|bisection)", "mental rotation": r"mental rotation",
    "emotion recognition": r"emotion recognition|facial expression", "fear conditioning": r"fear conditioning|pavlovian", "moral dilemmas": r"moral (dilemma|judg)",
    "reading / eye tracking": r"eye[- ]track|eye movements? during reading", "working memory span": r"(operation|reading|complex) span|working memory span",
}
TOPICS = {
    "cognitive control and conflict": r"cognitive control|conflict (adaptation|monitoring|processing)|interference control|executive (control|function)|inhibitory control|congruency",
    "mental effort": r"mental effort|cognitive effort|effort (cost|avers|allocation|expenditure)|effortful",
    "cognitive flexibility and task switching": r"cognitive flexibility|task[- ]switch|set[- ]shifting|multitask",
    "response inhibition": r"response inhibition|inhibit(ion|ory)|impulsiv",
    "working memory": r"working memory|short[- ]term memory",
    "long-term memory": r"episodic memory|long[- ]term memory|recognition memory|recall|forgetting|retrieval",
    "attention": r"\battention|attentional",
    "learning from reward": r"reinforcement learning|reward learning|value[- ]based|exploration|exploitation",
    "decision making under risk and time": r"risk|uncertainty|discounting|intertemporal|loss aversion",
    "perceptual decisions and confidence": r"perceptual decision|confidence|metacognit|psychophys",
    "implicit and statistical learning": r"implicit learning|statistical learning|sequence learning",
    "language": r"language|sentence|lexical|semantic|reading|word recognition",
    "social cognition and decisions": r"social|cooperat|fairness|theory of mind|trust|moral",
    "emotion and motivation": r"emotion|affect|mood|anxiety|motivation|reward prospect",
    "time and action": r"time perception|timing|motor|action control|sensorimotor",
}

papers = []
for folder in sys.argv[1:]:
    for path in sorted(Path(folder).glob("*/metadata.yaml")):
        try:
            d = yaml.safe_load(path.read_text())
        except Exception:
            continue
        text = f"{d.get('title') or ''} {d.get('abstract') or ''}".lower()
        if len(text) < 50:
            continue
        papers.append({"title": (d.get("title") or "").strip().rstrip("."), "year": d.get("year"), "doi": (d.get("paper_doi") or "").replace("https://doi.org/", ""),
                       "paradigms": [p for p, rx in PARADIGMS.items() if re.search(rx, text)],
                       "topics": [t for t, rx in TOPICS.items() if re.search(rx, text)]})

index = defaultdict(lambda: defaultdict(list))
for paper in papers:
    for topic in paper["topics"]:
        for paradigm in paper["paradigms"]:
            index[topic][paradigm].append(paper)
named = sum(1 for p in papers if p["paradigms"])
lines = ["# Paradigms by research topic", "",
         f"Which paradigms published studies with open data used for a topic. Built from the titles and abstracts of {len(papers)}",
         f"papers by keyword; {named} of them name a paradigm from the list. Generated by `dev/build_paradigm_index.py`; do not edit by hand.", "",
         "How to use it: when a user names a topic and has no task yet, look the topic up, offer the two or three most",
         "used paradigms, and say what each one measures and what it typically compares, from your own knowledge.",
         "The counts say how often a paradigm was used here, not how good it is. Papers that do not name their paradigm",
         "in the abstract are missing, so absence from this list means nothing. Details of single experiments are in `tasks.md`.", ""]
for topic in TOPICS:
    if topic not in index:
        continue
    lines += [f"## {topic.capitalize()}", ""]
    for paradigm, found in sorted(index[topic].items(), key=lambda kv: -len(kv[1])):
        examples = "; ".join(f"{p['title'][:90]} ({p['year']}, doi:{p['doi']})" for p in found[:2])
        lines.append(f"- **{paradigm}** ({len(found)}): {examples}")
    lines.append("")
out = Path(__file__).resolve().parents[1] / "skills" / "sweetpea" / "paradigms.md"
out.write_text("\n".join(lines))
print(len(papers), "papers,", named, "name a paradigm,", len(index), "topics ->", out.name)
for topic in ("cognitive control and conflict", "mental effort"):
    print(topic, "->", [(p, len(f)) for p, f in sorted(index[topic].items(), key=lambda kv: -len(kv[1]))][:8])
