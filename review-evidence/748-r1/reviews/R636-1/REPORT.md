[R636] POSITIVE - exact head c48bfe38b25f002d24898cec265520b9fc1a7111

# R636-1: internal cleared-context review of PR #749 (issue #748)

- Head under review: `c48bfe38b25f002d24898cec265520b9fc1a7111`, tree `33e999cb842593dbbd9d2e97cfeea587d581b63a`. Branch `748-elab-race` and `refs/pull/749/head` both resolve to it (`git ls-remote`).
- Source base: `9ef717727e6fdac11ee7f01672fefae948452343`. The delta is three one-line commits with no trailers, touching 5 files (+412/-41): `.github/ci-templates/elaborate.yml`, `.github/workflows/elaborate.yml`, `scripts/ci_events.py`, `scripts/ci_toolcache_isolation.py` (new), `docs/testing/CI_WORKFLOWS.md`.
- Scope reconstructed from AGENTS.md and CONTRIBUTING.md, and from the issue #748 body. The assignment comment (decision: job-private toolchain, shared tool cache read-only; items 1 to 4), TAKEN and REVIEW READY were read, along with the PR body, the diff, history and the public evidence tree `9ae6b8b2:review-evidence/748-r1` (author control logs and JSON, the apply race summary, docs-gate TSV and the elaboration-leg tails).
- Private author material was not used. That includes `author/HANDOFF.md` in the evidence tree, which was not opened.
- No prior review findings exist on this PR. The only PR comments are the two review-start notices, so nothing had to be resolved or retained.

## Verdict basis

Every claim in the six focus checks was confirmed at this head, either from the author's published receipts or by my own falsification runs.

- **(1) Inventory.** `actions/setup-python` occurs only in `elaborate` (2 of 2 occurrences, both legs).
  - The act runner image's own `PATH` contains no tool-cache entry, so `python3` in the other three workflows is the image's interpreter, not the tool cache's. I read the registry config of `catthehacker/ubuntu:full-latest` (amd64, created 2026-09-16), which `scripts/act_ci.py:85` names (`receipts/runner_image_env.txt`).
  - Every other install, fetch or patch step writes job- or image-private paths: workspace, `$RUNNER_TEMP`, `/tmp`, `$HOME`, `/usr/local/bin`, `/opt/verilator`, `/opt/yosys`, `/opt/sbt`, apt.
  - The PR table has one wording gap, recorded as F1 (RESIDUE).
- **(2) The new step.** It sits immediately after setup-python in both legs, before every later `python3` user:
  - template `.github/ci-templates/elaborate.yml:148-162`;
  - generated `.github/workflows/elaborate.yml:111-117` (leg 0) and `:346-352` (leg 1).

  Covered steps: the LiteX install, the VexiiRiscv placement (`scripts/ci_litex_env.py` clones into `pythondata_cpu_vexiiriscv.data_location`), the metadata copy, `apply.sh` (`PY="${PYTHON:-python3}"`; `PYTHON` is never set in the workflow), the gate legs and Scala generation (`test_builder._litex_python` uses `sys.executable`), and the leg-1 aggregate (`run_litex_sims.sh` uses `command -v python3`).

  Template, generator and workflow are consistent. `ci_gate_workflows.py --check` gives rc 0, and probe M4 (template edited, workflow not regenerated) gives rc 1. The derived id shifts (`gate_14_*` to `gate_15_*`, `gate_18` to `gate_19`, `ci_packages_16` to `ci_packages_17`) are not referenced anywhere outside the generated workflows.
- **(3) Contract.** `scripts/ci_events.py:569` (recorded writer, canonical script), `:1217` (pinned position, `BUILDER_IF`) and `:7453-7469` (three arms).
  - `--check` gives OK over 2199 items.
  - `--selftest` gives PASS (2199 items, 5233 arms), including all three `#748` arms.
  - My independent template-level mutations were all caught by `--check` after regeneration:
    - M1, the step moved after the install: 3 findings;
    - M2, the venv placed inside the tool-cache interpreter's prefix: 2 findings;
    - M3, the step's `if` dropped: 2 findings.
- **(4) Native control.** I reran it with a different planted interpreter (standalone CPython 3.12.13, 5386 planted paths).
  - At the head: every step of both legs rc 0, gate 23h rc 0 in each leg, `5386 planted paths, 0 changed`, ISOLATED, rc 0.
  - `--shared`: NOT ISOLATED, rc 1, 9296 paths changed. Leg 0's placement failed with `fatal: destination path ... already exists and is not an empty directory`.
  - `--rev 9ef71772`: NOT ISOLATED, rc 1, 9296 changed. Leg 1's placement failed the same way.
  - The control also rejects a partial fix (probe M1, venv after the install): NOT ISOLATED, rc 1, 3399 cache paths changed.
  - This matches the author's receipts at all three commits: 6303 planted / 0 changed with the fix, and 9296 changed for `--shared` and for dev.
- **(5) Cache keys and cost.**
  - No key formula and no template `path` changed (diff). The RV32 SDK key does not hash workflows, so it still hits. The apt entry's path moved with its index, and its key already misses once.
  - The venv step measured 2.0 s per leg in my runs, against 2.3 to 2.4 s in the author's. Install 30 to 34 s, placement 11 to 13 s, patches 0.3 to 0.4 s, all consistent with the author's.
  - The #737 projections (`docs/testing/CI_WORKFLOWS.md:2809-2810`, 1475/1353 of 1620) stay inside budget at about 1478/1356.
- **(6) Comment rule.** I scanned every added line of the raw diff (417 lines, `receipts/head.diff`) for lane labels, bracketed role IDs, review rounds, reviewer IDs, issue-comment IDs and local paths. The only hits were two Python `round()` calls, so there is no new instance.

## Findings

### F1 - RESIDUE - lenses: Conformance, Docs - artifact: PR #749 body, "Inventory" table, row `docs, rtl-fast, rtl | python3 -m pip install (...)`

- **Evidence.** The row enumerates the installed packages as "pyyaml, behave, renderer, HDL reference, wavedrom, evidence reader". It omits the LiteX pin install in `rtl-fast` job `firmware-boundary`, at `.github/workflows/rtl-fast.yml:993`: `python3 -m pip install --quiet pyyaml -r sw/litex/litex_pins.txt`.
- **Why the classification still holds.** The row is still correct for that step. It writes the image's own interpreter (the image `PATH` has no tool-cache entry), and nothing in that job patches or clones into it.
- **Impact.** Wording only. No measurement, verdict, code, generated artifact or conformance claim changes.
- **Exact fix.** In that row's parenthesis, replace "(pyyaml, behave, renderer, HDL reference, wavedrom, evidence reader)" with "(pyyaml, behave, renderer, HDL reference, wavedrom, evidence reader, and the LiteX pins in `rtl-fast` `firmware-boundary`)".
- **Verification.** The PR body text.

### F2 - SUGGESTION - lenses: Tests - artifact: `scripts/ci_toolcache_isolation.py:50-52,70-86`

- **Evidence.** The committed control runs the setup window up to the patch series. The steps after it (gate legs with the Scala generation, the leg-1 aggregate, "Keep the generated CPU netlist arguments") are covered by construction: the control's probe proves `sys.prefix`, `litex.__file__` and `data_location` are under the leg's `RUNNER_TEMP`.
- **The gap.** The author's statement that the planted cache was still byte-equal after both gate legs ran concurrently ("0 of 6299 paths differ") has no comparison receipt in the evidence tree. Only the leg rc files and log tails are there.
- **Optional outcome.** Publish that comparison receipt, or let the control optionally run the gate legs before its final manifest. Not required by acceptance item 2, which concerns the setup.

No BLOCKER, MAJOR or MINOR finding is open.

## Lens results (clean-lens evidence)

- **[R636] PASS Conformance** — issue #748 items 1 to 4 against the head:
  - item 1: inventory checked against all four workflows and `receipts/runner_image_env.txt`; template-only edit, then `receipts/gate_workflows_check.rc` 0;
  - item 2: `receipts/control_{fix,shared,dev}.{log,json}`;
  - item 3: `receipts/head.diff` is confined to CI template, workflow, contract, control and doc, with no arm weakened; the 20 to 21 step-count updates are consistent; cost stated;
  - item 4: comment scan clean.
- **[R636] PASS RTL** — `receipts/head.diff`: no HDL, constraint or synthesis file in the delta. Applied as: the workflow-level ordering and interpreter-resolution contract of the steps that feed elaboration, at `.github/workflows/elaborate.yml:105-206,340-352`, `sw/builder/test_builder.py:22634-22656`, `scripts/run_litex_sims.sh:130-143`, `sw/litex/patches/apply.sh:28`. Module and interface contracts are unchanged.
- **[R636] PASS Robustness**:
  - The step's `if` is pinned (M3).
  - With `rtl=false` the step and every consumer skip together.
  - The `always()` record steps import no yaml (`scripts/ci_gate_receipts.py`, `scripts/ci_runtime_evidence.py`).
  - Nothing deletes `$RUNNER_TEMP/litex-venv`.
  - The concurrent legs pass under barriers (`receipts/control_fix.log`).
  - A partial fix fails (`receipts/mutations/M1.summary`, `M1.control.log`).
  - The act tool-cache volume is per run but shared by every job of a run (`docs/testing/CI_WORKFLOWS.md:2096-2101`), which is exactly the sharing the fix removes.
- **[R636] PASS Tests**:
  - `receipts/events_selftest.log` (5233 arms, three `#748` arms caught).
  - `receipts/mutations/` M1 to M4 (independent template-level mutations all caught).
  - `receipts/control_*` (the control fails without the fix at `--shared` and at dev, and passes at the head with a second planted interpreter).
  - `receipts/gate_workflows_selftest.log` PASS.
- **[R636] PASS Docs** — `docs/testing/CI_WORKFLOWS.md:1422-1454` checked against the template and the control code (pass criteria, `--shared`, prerequisites).
  - Docs gates at the head: `receipts/docgates/` (em-dash 0 findings over 33 added lines, cited paths OK, TOC and anchors OK, doc style OK, docs_check 0 findings, Python idiom 54/54) all rc 0.
  - F1 is RESIDUE and does not leave this lens unclean.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #748 body and assignment items 1 to 4; PR inventory against all four workflows and the runner image config; `receipts/control_*` | R636-1 | c48bfe38b25f002d24898cec265520b9fc1a7111 |
| RTL | CLEAN | `receipts/head.diff` (no HDL); elaborate step order and interpreter resolution (`elaborate.yml:105-206,340-352`, `test_builder.py:22634-22656`, `run_litex_sims.sh:130-143`, `apply.sh:28`) | R636-1 | c48bfe38b25f002d24898cec265520b9fc1a7111 |
| Robustness | CLEAN | skip and always() paths, venv lifetime, concurrent legs under barriers, partial-fix probe M1 | R636-1 | c48bfe38b25f002d24898cec265520b9fc1a7111 |
| Tests | CLEAN | `ci_events.py` arms and selftest, `ci_gate_workflows` check and selftest, mutations M1 to M4, native control fix/shared/dev | R636-1 | c48bfe38b25f002d24898cec265520b9fc1a7111 |
| Docs | CLEAN (F1 RESIDUE carried) | `CI_WORKFLOWS.md:1422-1454`, template comments `elaborate.yml:148-156`, `ci_events.py:565-568`, control docstrings, docs gates | R636-1 | c48bfe38b25f002d24898cec265520b9fc1a7111 |

## Commands run (all foreground, concurrency inside one command)

- `scripts/run_checks_and_controls.sh` ran 7 jobs at once: the four contract and generator checks and the three control runs. Result: control_fix 0, control_shared 1, control_dev 1; gate_workflows_check 0, gate_workflows_selftest 0, events_check 0, events_selftest 0.
- `scripts/mutation_probes.sh` ran M1 to M4 in disposable clones under `scratch/`. Every mutation was caught.
- `scripts/run_doc_gates.sh` ran six docs gates, all rc 0. The first attempt (em-dash and TOC) returned rc 2 because the pinned Markdown renderer was not installed. After installing `tools/markdown/requirements.txt` into the review venv, the rerun gave rc 0. The rerun overwrote the first attempt's logs, so that attempt's outcome is recorded only in this sentence; the published logs are the rerun's.
- The review interpreter is a venv from standalone CPython 3.12.13 with `ci/requirements-evidence.txt` (hash-pinned) installed.
- After the probes the clone is at the exact head with no tracked, untracked or ignored changes, and the required gitlinks match their checkouts (`receipts/clone_state_after_probes.txt`). The checks had created ignored `__pycache__` directories, which were removed.
- Pinned Verilator was not used, since there is no RTL in the delta.
- Local paths in published receipts are redacted to `$PACKET`, `$CLONE` and `$HOME`.

## Real limits

- No Docker or act was run. The isolation under act is shown natively: the author's control, my rerun, and the image config read from the registry. The four-job act replay at this head is not yet posted on the PR (only the two review-start notices exist), so I cite no act receipt.
- Planted interpreters were local CPython 3.12.3 (author) and standalone 3.12.13 (mine), not the image's 3.12.14. If an image stdlib module lacked compiled bytecode, the venv step could write `__pycache__` into the shared cache. Such writes are atomic and are not a race, but they would not be byte-unchanged. Not observed with either planted interpreter.
- The control skips the cache restores and `Install sbt` (named in its `SKIP` table). Isolation of the steps after the patch series rests on construction plus the author's unreceipted post-gate comparison (F2).
- Hosted runs at the head were still queued or in progress at my snapshot (`receipts/hosted_checkruns_snapshot.txt`; `elaborate-gates-1` in progress, `docs-check-no-git`, `bdd-conformance`, `changes` and `wire-accountability` succeeded, the physical gPTP context skipped). This is not hosted acceptance.
- No manager source bank exists at this head, and none is claimed. Physical calibration NOT RUN; not applicable to this delta, and field skips are not hardware proof.

## Pending manager duties

- Publish the four-job act replay at this head. Its elaborate legs should show each leg's placement and patches under its own `RUNNER_TEMP` and no tool-cache Python in any log line.
- Hosted exact-head acceptance: `elaborate-gates-0/1` and the full gate set.
- Build and validate the current-dev merge candidate at the merge turn: source base `9ef71772`, live dev `973e681b`.
- Carry F1 to the residue checklist.
- External review (R637) is separate and still required.

R636-1 FINISHED
