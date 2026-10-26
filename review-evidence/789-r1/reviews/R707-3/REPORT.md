[R707] POSITIVE - exact head 1c9a3e8e54fc746f95ab89e074346904ba49f3e0

# R707-3: internal cleared-context re-review of PR #794 (issue #789)

- **Head:** `1c9a3e8e54fc746f95ab89e074346904ba49f3e0`, tree `4012f6af307939213c6d6eaec3c070e1d2cc9ddf`, source base and live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`.
- **Delta judged:** `1e0c5c09..1c9a3e8e`, from the head R707-2 reviewed to this head. It is two commits:
  - `10e0b519`: the emission judge;
  - `1c9a3e8e`: docs only.

  It changes `scripts/ci_fast_tool_selftest.py` (+152/-19) and `docs/testing/CI_WORKFLOWS.md` (+45/-13). `git diff 1e0c5c09 1c9a3e8e -- .github scripts/ci_gate_workflows.py hdl syn` is empty (0 lines). So the generator, the templates, all four workflows and the tool key are unchanged.
- **Verdict:** POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. One SUGGESTION (R707-3-S1) and one RESIDUE (R707-3-R1) are recorded below.
- **Prior findings:**
  - R707-2-01 is RESOLVED at its cause: my round-2 probe, rerun unmodified, now refuses N11 by name.
  - R707-2-S1 and R707-2-S2 are closed (taken).
  - R707-1-01 and R707-1-02 stay resolved, re-proven by the same rerun.

## Scope reconstructed from public state

- **Issue #789 Decision:**
  - a dedicated Yosys tool job in `rtl-fast`;
  - its key bound only to the version, the recipe and the image;
  - `yosys-elaboration` `needs:` it and restores the tree, never building;
  - no timeout raised, and every job stays within 30 minutes.
- **Frozen acceptance:**
  1. The job comes through the generator.
  2. The key excludes the workflow files, and a cold build fits 30 minutes on a hosted run.
  3. `yosys-elaboration` restores the tool and finishes under 30 minutes on a head that edits a workflow.
  4. The named gates pass, and the act replay maps the new job.
  5. R705-1-01's wording fix is applied.
- **Round-3 assignment (issuecomment-6420212695):**
  - Fix R707-2-01: a named judge holds the emitted jobs after every stage, the key-binding stage included, and a plant in that stage that drops a self-test must fail it.
  - State a choice on S1 and S2.
  - Keep hosted `rtl-fast` green.
- **Carried from R707-2:** R707-2 judged acceptance 1, 2, 3 and 5 and the key design CLEAN at `1e0c5c09`. This delta changes nothing they depend on: the generator, the workflows and the key are byte-identical.

## Independent pass over the delta

### 1. `fast_tool_emission` (`scripts/ci_fast_tool_selftest.py:320-358`)

- **The replay matches the generator.** The judge replays `ci_runtime_workflows.generate("rtl-fast", ci_install_workflows.generate(gate_graph(...)))`. That is exactly `generate()`'s stage order before `bind_fast_tool_key` (`scripts/ci_gate_workflows.py:383-392`). The only later call, `check_inventory_dependencies`, is read-only.
- **Key normalisation.** The judge normalises only the two keyed steps:
  - the tool cache and the restore must each be the replay's string, with the stand-in replaced by `BOUND_RECIPE` (`:36`);
  - both must bind the same recipe (`:349-350`).
- **Then it compares:**
  - every top-level workflow key;
  - the job order and the job set;
  - every job's non-step keys;
  - every job's step list, through the shared `step_findings` (`:205-218`).
- **The checked-in file.** The judge runs on the in-memory `generate()` output. `ci_gate_workflows.py --check` holds the checked-in `rtl-fast.yml` byte-equal to `rendered()` of that same output. Both run in the hosted "CI scheduling and evidence controls" step, so together they hold the file.
- **What it leaves to the other judges.** The judge does not verify the recipe's value or the `hashFiles` list: its regex accepts any 64-hex digest and any path list. That is by design. `fast_tool_findings` and `fast_tool_key_inputs` hold those, as mutants B09, B10, N01-N04 and N08-N09 below show.

### 2. Generator mutants after the derivation

Script: `scripts/probe_bind_mutants.sh`. Receipts: `receipts/probe/`.

Each mutant edits the key-binding stage in a disposable export of the head. It then regenerates the workflows, as an author would, so `--check` passes by construction. Then it runs the fast-tool controls, `--check` and `ci_events.py --check`.

- **Control:** passes all three.
- **All 12 generator mutants are refused by `fast_tool_controls`, each with a named finding:**

| mutant | edit after the key is bound | first refusal |
|---|---|---|
| B01 | drop the result-cache self-test from the consumer | `emitted yosys-elaboration drops Prove the result cache refuses a planted entry` |
| B02 | tool job `env` set after the digest | `emitted yosys-tool's job keys differ ...` |
| B03 | build body rewritten after the digest | `emitted yosys-tool changes Build Yosys from source on cache miss` |
| B04 | restore loses `fail-on-cache-miss` | `emitted yosys-elaboration changes Restore the pinned Yosys build` |
| B05 | tool timeout raised to 45 | `emitted yosys-tool's job keys differ ...`, `timeout changed or above the hosted budget` |
| B06 | consumer `needs` drops the tool job | `emitted yosys-elaboration's job keys differ ...` |
| B07 | another job (`verilator-lint`) loses a step | `emitted verilator-lint drops Upload actual job execution` |
| B08 | workflow `permissions` changed | `emitted workflow keys differ ...: permissions` |
| B09 | `hashFiles` binding dropped | `tool key does not bind the scripts its build steps run` |
| B10 | digest of `{}` | `tool key unchanged by an edit of its build inputs: ...` |
| B11 | restore bound to another digest | `emitted tool cache and its restore bind different recipes` |
| B12 | restore gains `restore-keys` | `emitted yosys-tool changes Cache ...`, `tool cache restores more than its exact key` |

- **5 judge mutants, J01-J05.** Each makes the self-test fail at its own plant, so every new check can fail for the defect it claims to detect:
  - J01: the job-key comparison removed;
  - J02: the recipe-equality check removed;
  - J03: the top-level comparison removed;
  - J04: the step comparison removed;
  - J05: the replay replaced by the emitted workflow itself.

### 3. Round-2 probe rerun

Script: `scripts/probe_mutants_r2.py`, the round-2 probe unmodified (sha256 `0068f454…`, equal to its round-2 manifest entry). Receipts: `receipts/mutants_r2_rerun.log`, `receipts/mutants_r2_rerun/mutants.json`.

- It ran on a full copy of the head clone, submodules included.
- **Control:** C00 passes every judge.
- **CAUGHT:** G01-G05, G08-G10, G15, N01-N10 and W01-W04.
- **N11, the R707-2-01 survivor, is now CAUGHT** as `emitted yosys-elaboration drops Prove the result cache refuses a planted entry`.
- **Discarded attempt.** A first attempt on a checkout without submodules failed its control for an environmental reason: `capture_coherence` `make -n` needs the submodules. Only the full-tree rerun is published.

### 4. Edge probe

Script: `scripts/probe_unnamed_step.py`. Receipt: `receipts/probe_unnamed_step.txt`. Two inputs make the judge raise `TypeError`:

- **An added step with neither `name` nor `uses`:** `step_findings` concatenates `str + None`.
- **Two differing top-level keys, one of them the YAML `on` key (loaded as `True`):** `sorted(tops)` cannot compare `bool` and `str`.

At this head no emitted step lacks both `name` and `uses` (count 0), and no plant hits either path. Both cases fail closed, by an exception rather than a named finding. See R707-3-S1.

### 5. Docs (`docs/testing/CI_WORKFLOWS.md:343-349, 366-406, 872-882`)

- **Lines 343-349, S1's documentation form.** The new sentence says the generator recognises the after-build pair by the ids `ci_record` and `ci_upload`, and that `fast_tool_emission` holds their content. That is true. `ci_gate_workflows.py:239-243` checks ids, and the plant "the tool evidence record rewritten" and my B-series confirm the content hold.
- **Lines 376-399, the two judges.** The text says which list each judge holds, and the plants it enumerates match `fast_tool_emission_planted` (`:361-434`).
- **Lines 400-406, the stated limitation.** The shared transforms are replayed, not held.
- **The `ci_install_cache_selftest.py` claim** ("keep every derived step, unchanged unless it is an `Install ` or `Build ` step") matches `scripts/ci_install_cache_selftest.py:50-60`.
- **Item 4 (`:872-882`)** now names both judges, and names the generated-graph comparison as the only whole-list hold on what the shared transforms emit. That answers R707-2-01's docs half.
- **Comment rule.** I scanned every added line of `76de691e..1c9a3e8e` (docs, scripts and `.github`). None has a lane label, round, reviewer ID or issue-comment ID. The docs-page hits at `:284, :1206, :1230` predate this PR and are tracked by #746.

### 6. Gates I ran at the exact head

CPython 3.14.8 with PyYAML 6.0.3. Receipts: `receipts/*.log` and `*.rc`. Every gate exited 0:

| gate | result |
|---|---|
| `ci_gate_workflows.py --check` | rc 0 |
| `ci_gate_workflows_selftest.py` | rc 0; 86 "Fast Yosys tool" lines, then `gate workflow and union controls: PASS` |
| `ci_install_cache_selftest.py` | rc 0 |
| `ci_events.py --check` | rc 0; OK, 2199 items |
| `check_py_idiom.py` | rc 0 |
| `check_doc_style.py` | rc 0 |
| `check_doc_paths.py` | rc 0 |
| `check_em_dash.py --base 76de691e` | rc 0; 0 findings over 133 added lines |

- **`check_em_dash.py`** ran under the pinned renderer, installed by hash into a disposable venv under `scratch/`. Before that, a run without the renderer refused to judge (rc 2); the real run's receipt replaced it.
- **Not rerun:** `ci_events.py --selftest`, `act_ci.py --selftest` and the runner contract gate. `act_ci.py` and every workflow are unchanged since `1e0c5c09`, so I relied on the author's published receipts, spot-checked below.

### 7. Hosted evidence at the exact head (read-only)

Receipts: `receipts/hosted_runs_at_head.txt`, `receipts/hosted_docs_gates0_fast_tool.txt`.

- **All four runs at this head succeeded on attempt 2.** `rtl-fast` 40356479027, `docs` 40356478658, `elaborate` 40356478638 and `rtl-full` 40356478782 each show `head_sha` 1c9a3e8e…, status completed, conclusion success.
- **`rtl-fast`: all 16 jobs succeed.**
  - "Prepare pinned Yosys": 17:04:23-17:04:34.
  - `yosys-elaboration`: 17:11:12-17:26:57, so 15 min 45 s, inside its 30-minute limit.
  - The `rtl-fast` aggregate succeeds.
- **The docs-gates-0 log** (job 121720319131, 717302 bytes, sha256 `aca4cea8…`):
  - It prints 86 "Fast Yosys tool" lines, 36 of them emission refusals, then `gate workflow and union controls: PASS`.
  - The 86 lines are textually identical to my local run.
  - The key-binding plant prints `emitted yosys-elaboration drops Prove the result cache refuses a planted entry`.
- **Acceptance 2 and 3** were measured at `1e0c5c09` and judged by R707-2. Run 40321654840 shows the cold tool job at 12m47s, and the cached consumer at 12m45s on a head that edits a workflow. This head changes no workflow.
- **Hosted and act acceptance** are the manager's.

### 8. Author evidence packet (evidence tree commit `1c0c9f4b`)

- **The commit is unsigned:** GitHub verification reports `unsigned`. I verified receipts against the packet's `MANIFEST.json` `published_sha256` instead.
- **28 of 28 sampled `author-r3/` files match** (`receipts/author_r3_manifest_spotcheck.txt`). The sample covers:
  - `HANDOFF.md` and the act offline mapping;
  - gate logs and rc files on both interpreters, at the head and at the intermediate commit (`ci_gate_workflows_selftest`, `ci_events-selftest`);
  - the probe receipts at `1e0c5c09`, `10e0b519` and `1c9a3e8e`.
- **The author's `mutants-1e0c5c09.txt`** shows K01 (= N11), K04 and K05 surviving at the round-2 head. My B-series and the N11 rerun show them refused here.

## Findings

### R707-3-S1: SUGGESTION (Robustness, Tests). Two deviations make the emission judge raise instead of naming them

- **Where:**
  - `scripts/ci_fast_tool_selftest.py:200-202`: `step_label` returns `None` for a step with neither `name` nor `uses`.
  - `:205-218`: `owner + " adds " + label` then fails on that `None`.
  - `:351-353`: `sorted(...)` over the top-level keys mixes `True` (the YAML `on` key) with strings.
- **Evidence:** `receipts/probe_unnamed_step.txt`. Both cases raise `TypeError`.
- **Impact:** none on safety. The self-test exits non-zero, so the hosted controls step fails closed, but the failure text is a traceback rather than a named finding. No such step exists at this head. The retention judge shares `step_findings`, so the same kind of gap predates round 3.
- **Suggestion (optional):** label a step with no name by its `run` text or its index, and sort the top-level keys with `key=str`.
- **Verification:** rerun `scripts/probe_unnamed_step.py <clone>`. Both cases then return a named finding.

### R707-3-R1: RESIDUE (Docs; PR body only). One bullet under-states the re-run

- **Where:** PR #794 body, "Hosted measurement", "Round 3 (this head)": "**Attempt 2: a re-run of all jobs of `rtl-fast` and `docs`.**"
- **Why it is wrong:**
  - Attempt 2 re-ran all four runs: `receipts/hosted_runs_at_head.txt` shows `run_attempt=2` for each.
  - The issue's REVIEW READY comment says "I re-ran all jobs of the four runs".
  - The same PR body says further down that elaborate and rtl-full were re-run.
- **Scope:** wording only. No measurement, verdict or claim changes.
- **Exact fix:** replace the bullet with "**Attempt 2: a re-run of all jobs of all four runs.** The `rtl-fast` jobs are below; `docs`, `elaborate` and `rtl-full` follow."

### Not findings

- `docs/testing/CI_WORKFLOWS.md:370-371` wraps one source line short ("job `env`, a"). It renders identically.

## Prior public review findings on this PR

I wrote my independent pass above before reading the prior rounds' findings. I read R708-1 only after this report's verdict and ledger were written.

| finding | status at `1c9a3e8e` | evidence |
|---|---|---|
| R707-2-01, MINOR (Tests, Docs): the retention judge holds the derivation, not the emitted jobs | **RESOLVED at its cause.** `fast_tool_emission` holds the emitted workflow after every stage, and a drop in the key-binding stage fails by name. Docs item 4, "Fast feedback" and the PR body's "Round 3" say which list each judge holds. | The finding's own verification: the `probe_mutants_r2.py` rerun (N11 CAUGHT with the named refusal; C00 passes; G01-G05 and N01-N10 still CAUGHT; `receipts/mutants_r2_rerun*`). Also B01-B12 and J01-J05 (`receipts/probe/`), and the hosted docs-gates-0 log, which prints the plant's refusal. |
| R707-2-S1, SUGGESTION (Robustness): the after-build pair is identified by `id` only | **Closed: taken in its documentation form.** `CI_WORKFLOWS.md:345-349` states it, and the emission judge holds the content. | The plant "the tool evidence record rewritten"; B03. |
| R707-2-S2, SUGGESTION (Tests): add a workflow `defaults` plant | **Closed: taken.** | `scripts/ci_fast_tool_selftest.py:482-483, 495`; B10's refusal names "the workflow defaults". |
| R707-1-01, MINOR (Conformance, Robustness, Tests) | **Stays RESOLVED.** It was resolved at R707-2, and the key code is unchanged since. | N01-N04, N08-N09, B09 and B10 CAUGHT. |
| R707-1-02, MINOR (Tests, Docs) | **Stays RESOLVED.** | G01-G05 CAUGHT by name. |
| R707-1-S1, SUGGESTION (RTL) | **Closed** at R707-2, declined with a reason. Not reopened. | The PR body. |
| R708-1 (external, POSITIVE at `fddf3671`) | **Nothing to resolve or retain.** It files no BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION. The PR has no review threads and no inline review comments. I read it only after my own verdict and ledger were written. | PR #794 issuecomment-6414349885 |

## Lens ledger (reviewer-owned)

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #789 Decision and Acceptance; round-3 assignment issuecomment-6420212695; `git diff 1e0c5c09 1c9a3e8e -- .github scripts/ci_gate_workflows.py hdl syn` is empty, so the key, generator and workflows are unchanged and R707-2's judgement of acceptance 1-3 and 5 carries; `ci_gate_workflows.py --check` rc 0; hosted runs 40356479027, 40356478658, 40356478638 and 40356478782 succeed at this head; R707-2-01's required outcome met (pass section 3) | R707-3 | 1c9a3e8e54fc746f95ab89e074346904ba49f3e0 |
| RTL | CLEAN | the job graph is unchanged since `1e0c5c09` (0-line workflow and generator diff); no HDL, `syn/` or constraint file in `76de691e..1c9a3e8e`; hosted `yosys-elaboration` job 121720868622 succeeds in 15 min 45 s, under its 30-minute limit; the `needs` order tool -> consumer -> aggregate is unchanged | R707-3 | 1c9a3e8e54fc746f95ab89e074346904ba49f3e0 |
| Robustness | CLEAN (S1 only) | `scripts/ci_fast_tool_selftest.py:200-218, 320-358`; post-binding mutants B01-B12 (`receipts/probe/`); edge probe `receipts/probe_unnamed_step.txt`, which fails closed; the exact restore and `fail-on-cache-miss` held (B04, B12) | R707-3 | 1c9a3e8e54fc746f95ab89e074346904ba49f3e0 |
| Tests | CLEAN (S1 only) | `scripts/ci_fast_tool_selftest.py:320-434, 482-495, 585-610`; judge mutants J01-J05, each failing a plant; the round-2 probe rerun, all 25 rows as expected (`receipts/mutants_r2_rerun*`); `ci_gate_workflows_selftest.py` rc 0 locally, with the same 86 lines hosted (docs-gates-0 job 121720319131) | R707-3 | 1c9a3e8e54fc746f95ab89e074346904ba49f3e0 |
| Docs | CLEAN (R1 residue only) | `docs/testing/CI_WORKFLOWS.md:343-349, 366-406, 872-882` read against the code; `scripts/ci_install_cache_selftest.py:50-60`; the PR #794 body at this head (`receipts/pr794_body_at_review.md`); comment-rule scan of the delta; `check_em_dash` (pinned renderer), `check_doc_style` and `check_doc_paths` rc 0 | R707-3 | 1c9a3e8e54fc746f95ab89e074346904ba49f3e0 |

## Real limits

- **Not rerun by me:** `ci_events.py --selftest`, `act_ci.py --selftest`, the 0555 runner contract gate, and any second interpreter. `act_ci.py` and every workflow are unchanged since the round-2 head, so I relied on the author's receipts, verified by manifest hash.
- **The author evidence commit `1c0c9f4b` is unsigned.** I verified its receipts by the manifest's SHA-256 (28 of 28 sampled files match), not by signature.
- **No hosted run yet shows a key hit across a workflow edit that leaves the build inputs unchanged.** The self-test's key-input plants cover that case offline. Hosted runs show a hit across heads that changed no workflow.
- **Not run:** no live act replay, no Docker, no hardware. Physical calibration is NOT RUN, and field skips are not hardware proof.
- **The shared install and runtime transforms** are held only by the generated-graph comparison. This predates #789, and the docs state it.

## Pending manager duties

- The live act replay at the merge turn. Acceptance 4's "act replay maps the new job" is offline-only so far, which is why the PR body keeps `Relates to #789`. The replay must show act's cache server saving in `yosys-tool` and restoring in `yosys-elaboration`.
- Validate the current-dev merge candidate (builder and native banks) and publish its receipts.
- Hosted acceptance of the exact-head contexts.
- Carry R707-3-R1 to the residue checklist.
- External review at this head, if the review bar requires one.

R707-3 FINISHED
