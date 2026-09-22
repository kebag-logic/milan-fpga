[A10] Residue of #295, filed on the maintainer decision of 2026-09-07 to close that ledger

## Objective and evidence

Pin the content of the recognised non-gate steps in the four non-RTL required-context carriers (`docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`), so that a step's script rewritten under its recorded name, or a finding swallowed beside its call, is refused naming the step and the first differing line, the way the four gate steps already are.

- `docs/testing/CI_WORKFLOWS.md` lines 538 to 545 (item 12) record the residue at dev 7fd04d45: the content of the recognised non-gate steps in the four carriers can still be rewritten or swallowed with the context green, `docs-check`'s gates other than the ci_events step included (`docs_check`, `check_feature_status`, the traceability matrix, the builder gates and the rest), and the second runner (`full-ci-gate`'s contract step, `rtl.yml` line 91) backs up only `ci_events --check`. The page says a sequence-and-content pin on every job closes it and that it is #295's widened acceptance row.
- `scripts/ci_events.py` `check_carrier_steps` (lines 2745 to 2807, PR #335 merged 2026-09-02, b16cb470) holds identity and key set only: lines 2777 to 2778 accept any string `run` under the recorded name. Content is held for the gate steps, the builder setup and the act self-test alone: `check_carrier_gate_step` (2627), `check_named_carrier_gate_step` (2659), `check_scope_step` (2685), `check_builder_dependencies` (2525, the builder checkout, submodule fetch and builder call), `_check_builder_sv2v` (2496, the sv2v install) and the act self-test step (2824 to 2835), wired from `check_docs` (2810 to 2857) and `check_elaborate` (2860 to 2869). Every other `run:` step is recognised by its name and nothing else.
- The unpinned scripts, by step name: `.github/workflows/docs.yml` lines 21 to 82 (the HDL reference build, the link, audience, diagram, product, submodule, timing-diagram, PNG, feature-status and traceability gates) and 105 to 344 less the steps the functions above hold (the code-quality self-tests, the bare-metal scope gate, the NVM and saved-state gates, the source-list, naming, port-contract, fail-fast, TODO, test-evidence, hygiene and idiom ratchets, the cited-path, archive, per-page, sweep-shape and entity-shape gates), line 371 (`wire-accountability`'s submodule fetch), and `.github/workflows/elaborate.yml` lines 100 to 246 less the builder steps (the dependency fetch, the LiteX, sbt and VexiiRiscv installs, the patch series, the elaboration gates, the standalone LiteX aggregate and the cache write-back).

## Authority and scope

- `docs/testing/CI_WORKFLOWS.md` items 1, 2, 4, 11 and 12; #295 (widened acceptance row); PR #293 ([R3] round 9) and PR #335; #261.
- Context: `scripts/ci_events.py` (`normalize_script`, `script_difference` at line 1855, `GatePin`, `CARRIER_STEP_LISTS`, `pinned_step_keys`), `docs.yml`, `elaborate.yml`.
- In scope: a canonical normalised script per recognised `run:` step in the four carriers, held the way the gate steps are (item 1: verbatim after whitespace normalisation) and refused by name with the first differing line; the `uses:` steps stay held by their recorded `with`; one reason-pinned arm per lever per step class; the policy page restated with the cost (every legitimate script edit updates the table) and the remedy.
- Out of scope: the seven RTL jobs (the sibling residue issue filed with this one); changing what any gate runs; the gate steps and the scope step, already held.

## Acceptance and validation

1. Every recognised `run:` step of the four carriers is pinned to a canonical normalised script in `scripts/ci_events.py`; a refusal names the job, the step and the first differing line.
2. Arms in `--selftest`, for at least one step of each carrier and for every gate class in `docs-check` (a python gate, a ratchet with a bound, a builder gate, the reference build): `|| true` appended to the call, the script replaced by `true` under the recorded name, one command of a multi-command script dropped, a `--self-test` or `--check` flag dropped, and the step made `continue-on-error`; each is refused naming the step, and the vacuity control fails every arm.
3. `python3 scripts/ci_events.py --selftest` PASSes with the new arms counted, and `python3 scripts/ci_events.py --check` is green on the pristine tree.
4. `docs/testing/CI_WORKFLOWS.md` item 12 (lines 538 to 545) no longer names the non-gate content as open, item 11 states the carriers' scripts as pinned, and the cost row names the remedy (update the canonical script beside a mutation entry). `python3 -B scripts/docs_check.py`, `python3 scripts/gen_toc.py --check` and `python3 scripts/check_doc_paths.py` pass.
5. Measured under act: a `|| true` on `docs-check`'s Python idiom gate step leaves that tampered step green, while both `docs-check`'s own CI contract step and `full-ci-gate`'s contract step refuse the tree naming the Python idiom step. Both required exhaustive aggregates fail closed on the second runner. The whole `docs-check` job must fail too; it cannot legitimately stay green when its own mandatory contract check refuses the tree.

## Lane and review

Executor: [A155] Codex (separate author context). Independent reviewers: [R219] Codex (cleared-context internal) and [R220] Opus (cleared-context external). Manager: [A10].

Dependencies: none open; PR #335 is the precedent. Lane conflicts: any branch editing `scripts/ci_events.py`, `docs.yml`, `elaborate.yml` or `docs/testing/CI_WORKFLOWS.md`; every lane that adds or edits a docs.yml gate step must update the canonical table, so land this after the sibling sequence-pin issue or in the same lane.
