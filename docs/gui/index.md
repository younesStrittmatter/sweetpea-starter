# SweetPea Designer: a preview

Screenshots of a graphical editor for SweetPea designs. You build the design
by clicking, and the Python code is written next to it; change either side
and the other follows. The four steps at the top are the same as in the
tutorial: factors, blocks, constraints, generate.

Click a picture to see it in full size.

## 1. Factors

Three panes side by side: the designer, the block structure as a picture, and
the Python code. Here a Stroop design is loaded: colour and word as factors,
congruency as a derived factor.

[![The three panes with the factors of a Stroop design](01-overview-factors.png)](01-overview-factors.png){ target=_blank }

The designer pane on its own. A factor is a list of levels, each with a
weight. A derived factor says which factors it is based on and when each of
its levels applies.

[![The factors pane on its own](02-factors-pane.png)](02-factors-pane.png){ target=_blank }

The condition of a level is a short Python expression. The editor suggests
the levels of the factors it is based on.

[![A derived level written as a condition, with suggestions](03-derived-factor-python-condition.png)](03-derived-factor-python-condition.png){ target=_blank }

A derived factor can also look back across trials: here the response is
compared with the response two trials before.

[![A derived factor that compares values across trials](05-derived-factor-lag.png)](05-derived-factor-lag.png){ target=_blank }

## 2. Blocks

A block crosses factors. Blocks can be put inside one another (nest), run
over the same trials (merge) or repeated. The timeline at the top left shows
which block covers which trials.

[![The blocks step with a nested, a merged and a repeated block](06-overview-blocks-nest-merge-repeat.png)](06-overview-blocks-nest-merge-repeat.png){ target=_blank }

The block structure as a picture: a frame runs its contents once for each of
its levels, a plus joins merged blocks, an arrow repeats a block, and a link
marks a constraint.

[![The block structure on its own](07-block-structure.png)](07-block-structure.png){ target=_blank }

The blocks editor on its own. For every block you tick which factors are in
the design and which are crossed.

[![The blocks editor on its own](08-blocks-editor.png)](08-blocks-editor.png){ target=_blank }

## 3. Constraints

Each constraint belongs to a block, which sets where it applies: within each
run of the block, or across everything inside it.

[![The constraints step](09-constraints.png)](09-constraints.png){ target=_blank }

## 4. Generate

Choose how many sequences and which sampler, generate, look at the trials as
a table, and download them.

[![The generate step with a sequence as a table](10-generate-results.png)](10-generate-results.png){ target=_blank }

## Dark theme

[![The blocks step in the dark theme](12-overview-dark-theme.png)](12-overview-dark-theme.png){ target=_blank }
