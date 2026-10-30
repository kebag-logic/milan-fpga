[R736] POSITIVE - exact head 0c45ebf28e2c11352aa4ad40d46780143b1a77ab

Independent verdict and ledger, written before any PR or issue comment list
other than the reviewer's own round-1 reports was read (written 2026-10-30,
after the hosted check-run snapshot at 19:11:26Z).

Delta f99405af..0c45ebf2: three documents only (CHANGELOG.md,
docs/design/AREA_BUDGET.md, docs/reference/SUBMODULES.md), all mode 100644,
7 insertions and 3 deletions; gitlinks identical; no RTL, test, script,
record or generated file changed. cf3ef596..0c45ebf2 is also documentation
only, so the synthesis checkpoint reused by the directive runs is from
executable inputs equal to this head.

Findings at the independent checkpoint:
- R736-2-S1 SUGGESTION Docs: the three pages say "the best directive" without
  naming it or its worst-corner figures.
- R736-2-S2 SUGGESTION Docs: AREA_BUDGET.md:148-149 (dev text) reads, after
  this change's route sentences, as if it described the adopted route.
- Prior R736-1-R1 (RESIDUE, Docs): resolved at this head in source and PR body.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta sentences vs #814 and #818 bodies; build floor docs/integration/BUILDING.md:712, docs/testing/RUNNING_TESTS.md:209; executable basis R736-1 at f99405af (tree equal outside the three pages) | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
| RTL | CLEAN | git diff --raw f99405af..0c45ebf2 (no HDL); directive scripts vs PP_SHADOW_BASELINE_RECIPE.md:142-185; gate parser on both utilization reports | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
| Robustness | CLEAN | four per-corner negative-slack reports and route status per directive; worst-hold corner check (Fast +0.011 ns >= 0); diff --raw (no executable change) | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
| Tests | CLEAN | receipts/directive-probe.txt (gate verdict_for and utilization parser); author docs-0c45ebf2/all.out; own docs gates receipts/docs/*; diff --raw (no test change) | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
| Docs | CLEAN | CHANGELOG.md:76-77, docs/design/AREA_BUDGET.md:144-145, docs/reference/SUBMODULES.md:429-431, PR body lines 28-31, 99-111, 162, 177-193 | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
