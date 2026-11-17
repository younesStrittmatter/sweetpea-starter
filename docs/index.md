# SweetPea Starter

An AI assistant for designing experiments with
[SweetPea](https://sweetpea-org.github.io).

<div class="join">
<div class="join-item">
<a href="assets/qr_site.svg"><img src="assets/qr_site.svg" alt="QR code for this website"></a>
<strong>This website</strong>
<span class="join-url">younesstrittmatter.github.io/<wbr>sweetpea-starter</span>
</div>
<div class="join-item">
<a href="assets/qr_repo.svg"><img src="assets/qr_repo.svg" alt="QR code for the repository"></a>
<strong>The repository: open it in a Codespace to work with an assistant</strong>
<a class="join-url" href="https://github.com/younesStrittmatter/sweetpea-starter-template" target="_blank">github.com/<wbr>younesStrittmatter/<wbr>sweetpea-starter-template</a>
</div>
</div>

You say what you want to find out. The assistant states the hypothesis,
suggests a paradigm, proposes a design, and counts what the design leaves
unequal between the conditions you compare. Where a choice has a cost, it
puts the options to you.

## How it works

The assistant is not a separate program. It is a general AI coding assistant
that reads a few plain text files (`*.md`) in the repository's
[`skills/`](https://github.com/younesStrittmatter/sweetpea-starter-template/tree/main/skills){ target=_blank }
folder before it works with you.

- [`skills/sweetpea/SKILL.md`](https://github.com/younesStrittmatter/sweetpea-starter-template/blob/main/skills/sweetpea/SKILL.md){ target=_blank }
  helps it understand SweetPea: the current API, a working method that starts
  from your analysis, the paradigms, and the worked examples.
- [`skills/sweetpea-tutor/SKILL.md`](https://github.com/younesStrittmatter/sweetpea-starter-template/blob/main/skills/sweetpea-tutor/SKILL.md){ target=_blank }
  tells it how to teach.

**Teaching mode.** Say that you want to learn SweetPea, or ask for the guided
tutorial, and the assistant switches to teaching: it writes all the code,
explains each decision before making it, and walks you through the result
step by step. You decide; you never have to write code.

The files are ordinary text. You can read them, and change them to change how
the assistant works.

## What it is built on

**The SweetPea project.** 100 published papers, re-analysed with the trial
order taken into account: 11 flips and many shifts. The assistant learned from
these which side effects a design can have, and its worked examples come from
them.
[Slides: Avoidable by design](Avoidable%20by%20design%20-%20Slides.pdf){ target=_blank }.

**The [psyche](https://huggingface.co/spaces/ystrittm/psyche){ target=_blank } project.** A database of published experiments with open
trial-level data: 1,544 experiments from 790 studies. The assistant uses it to
suggest which paradigm fits a research question and what such studies
compare.

**SweetPea itself.** It turns a description of an experiment (its factors,
what must be balanced, what must not happen) into trial sequences that
satisfy it.

## Teaching examples

One experiment each, walked through with pictures: what is compared, what the
design leaves unequal, and what can be done about it.

1. [Masked number priming](teaching/masked_number_priming/index.md): a side effect of crossing two stimuli from the same set.
2. [The trial before](teaching/simon_previous_trial/index.md): a side effect of shuffling in small sets.
3. [Two things in one place](teaching/distractor_location/index.md): no design without a cost, only a choice between costs.

## Tutorial

One Stroop experiment grown in four questions, with an assistant or as
notebooks: [start here](tutorial/index.md).

## Example library

The same kind of experiment in a fixed, short format: the reference the
assistant reads when it works with you.

- [All examples](library/index.md)
