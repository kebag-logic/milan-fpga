[R336] POSITIVE - exact head 11dd3e903685183250e7cd8ecc391b04fe7fd494

# R336-2 independent internal review: processor PR #124 / issue #123, round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan.
- Exact head `11dd3e903685183250e7cd8ecc391b04fe7fd494`, tree `2e66f6caff52773103df53bc4992d92f72328d0b`. It is one commit on the round-1 head `eb734969154d5a75ff84b2779ff6088a2f4311a5`, which is one commit on base `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`. The PR head was rechecked at the end of the review and had not moved (`receipts/hosted-check-runs.txt`).
- This is a delta review. Round 1 (R336-1) covered eb734969 in full. This round judges eb734969..11dd3e90 and re-proves the behaviour of the whole change at the new head.
- Delta: 3 files, +26/-12 (`receipts/delta-r1-head.diff`):
  - `tb/desc_store/test_gen_desc_image.py` +23/-12;
  - `hdl/aecp/desc/gen_desc_image.py` +1, one line in the module docstring;
  - `docs/architecture/07_memory_maps.md` +2.
- Whole PR against base: 5 files, +186/-2 (`receipts/diffstat-base-head.txt`). No `.sv`, `.svh`, `.v`, C++ harness, Makefile or README change in round 2. There are no submodules or gitlinks.
- Assignment: issue #123 comment 5847977272. Review start: PR comment 5848109400. Reviewer role: internal independent reviewer, cleared context, isolated detached clone.

## Verdict in one paragraph

Round 2 closes both round-1 MINOR findings and both suggestions, and it changes no behaviour:
- **F1 closed.** The round-1 Rule 12 scan, run unchanged with the parent gate at `831f94f4`, reports 0 unannotated and 0 undocumented public functions at head. Round 1 had 10 and 9.
- **F2 closed.** The round-1 wall-clock scan, run unchanged, flags no processor `tb/` file at head. Round 1 flagged one.
- **S1 and S2 closed.** The sketch now satisfies the body/key rule; the round-1 sketch did not. The F07.4 sentence is accurate.
- **No behaviour change.** A syntax-tree comparison proves the round-2 edits are only annotations, docstrings, one `typing` import, the removed `timeout=` keyword and one docstring line. The tests still run 6 tests / 24 cases. The round-1 probes, mutants and legal-model digests reproduce byte-for-byte against the published round-1 receipts. All 11 image artifacts are identical at base, round 1 and head.
- **Gates.** The docs gates and `git diff --check` pass at head.

No MINOR, MAJOR or BLOCKER finding is open, so the verdict is **POSITIVE**.

## Reconstruction (in the required order)

1. **Repository conventions.** There is still no `AGENTS.md` or `CONTRIBUTING.md` in the tree. I read:
   - `README.md` ("Building and checking" and the submodule pin rule);
   - `docs/README.md`;
   - the root `Makefile`;
   - `.github/workflows/hdl.yml`, which has three jobs: docs-gates, suites and portability;
   - `scripts/run_suites.sh`;
   - `tb/desc_store/Makefile`.
2. **Issue #123.** I read the body, the frozen acceptance and gates (comment 5847636202), both executor READY comments (5847761667, 5848100735) and the round-2 assignment (5847977272, items 1-4).
3. **Manager evidence.**
   - PR comment 5847782435: five parent configs, base and PR AEM images identical.
   - PR comment 5847888234: consumer bank 8/11 at eb734969. Items 1-2 were assigned to the processor; item 3, the DUT-reader disposition, was assigned to the parent pin-bump patch.
4. **Authorities.**
   - Parent `docs/development/CODE_QUALITY.md` Rule 12, through `scripts/check_py_idiom.py` and `scripts/py_idiom.budget` at parent dev `831f94f4`. The budget has `unannotated public function = 0`, `undocumented public function = 0` and `over-long line = 0` at 120 columns.
   - Parent Rule 8 ratchet 4, through `scripts/measure_test_evidence.py` and `scripts/test_evidence.budget` at `831f94f4` (value 3). The note on ratchet 4 says a hang bound is "a guard, never an oracle".
   - Processor 07 §3.3 / F07.4.
   - The processor test idiom `tb/pp_top/test_fixture_guards.py`.
5. **Diff and history.** I read `git diff eb734969..11dd3e90` in full, plus the full head test file and generator lines 1-80 and 175-240.
6. **Public evidence.**
   - kebag-logic/milan-fpga `review-evidence/pp123-r1` at `8a640700`, the round-1 author packet.
   - The same tree on branch `pp123-review-evidence` at `d01c1722`. It adds the R336-1 packet, whose scripts I reused byte-unchanged, and the round-2 author packet `author-r2`.
     - `head.txt` = 11dd3e90.
     - `suites.log`: 33 PASS, 1,014,722 checks, rc 0.
     - `lint-hdl`, `yosys`, `nvm-figures`, `make-check`, `links`, `matrix` and `params`: rc 0.
     - Parent scans: 0/0 and nothing added.
7. **Prior public review findings.** I read my own R336-1 report (F1, F2, S1, S2) only after my independent pass over the delta. The other reviewer's round-1 report was read only after this verdict and ledger were written; see "Prior public findings at this head". The other reviewer's round-2 review had started (PR comment 5848112346) but was not read.

## Assignment verification

| # | Required | Result | Evidence |
|---|---|---|---|
| 1 | R336's scans rerun unchanged with the parent scripts at 831f94f4: 0 unannotated, 0 undocumented, no wall-clock file added | **met** | `receipts/r1-scripts-identity.txt`: all 7 round-1 scripts are blob-identical to the published R336-1 scripts. `receipts/parent-gate-provenance.txt` and `receipts/parent-gate-scripts.sha256`: the gate sources equal the 831f94f4 blobs. `receipts/parent-idiom-scan.log`: base->head rc 0 and round1->head rc 0. Head non-zero totals are only the pre-existing `long module: 1` in `hdl/aecp/ucode/gen_ucode.py`, the same as base. Round 1 shows the old 10/9 sites. `receipts/parent-wallclock-scan.log`: head flags 0 processor `tb/` files, round 1 flagged 1, and none were added (rc 0 both ways). |
| 2 | The sketch satisfies the body/key rule; the F07.4 sentence is accurate | **met** | `receipts/sketch-probe.log`, `scripts/sketch_probe.py`. The sketch is lifted from each tree's own docstring. At head, both sketch descriptors agree: ENTITY bytes 0-3 are `00000000` and AUDIO_MAP bytes 0-3 are `00170000`, and `_grouped_descriptors()` accepts the sketch (rc 0). At round 1 the ENTITY sketch read body index 0x2E2E (11822) from `entity_name` and was refused, so the probe discriminates. F07.4: see the Docs lens. |
| 3 | No behaviour change: 6 tests / 24 cases, round-1 probes and mutants as in round 1, images byte-identical | **met** | See the three rows below. |
| 3a | Syntax-tree equivalence | **met** | `receipts/ast-equiv.log`, `scripts/ast_equiv.py`. The generator's code AST without its module docstring is equal. The normalised test AST is equal once annotations, docstrings, the `typing` import and `timeout=` are removed. |
| 3b | Test counts and runs | **met** | `receipts/head-count-cases.log`: 6 tests, 24 subtests passed, 0 failed. Also `head-tests-direct.log` and `head-generator-check.log` (rc 0). `receipts/interpreters.log`: 6/24 under Python 3.11, 3.12 and 3.14. `receipts/head-tests-vs-base-generator.log`: 16 refusal subtests fail against the base generator, the same as round 1. |
| 3c | Probes, mutants, legal models and images vs published round 1 | **met** | `receipts/round1-vs-round2.txt`: `mutants-summary.txt`, `mutants.json`, `probes.json` and `legal-models.log` are identical to the published R336-1 receipts. That means 11/11 mutants killed with the same failing sets and 21/21 probes. `receipts/images-compare.txt`: base == round 1 == head for 11 artifacts, and head equals the published R336-1 head digests. The worked example is `20356f59…3b62c`. |
| 4 | Repository gates pass | **met** (my runs + public evidence) | `receipts/docs-gates.log` at head, all rc 0: `make check`; the CI docs-gates commands individually; `gen_matrix.py --check`; `check_upc_map.py`; `git diff --check` for base..head and for round1..head. `receipts/run_suites-reduced-head.log`: desc_store 584/584 through `scripts/run_suites.sh`. `receipts/run_suites-reduced-M0.log`: the M0 mutant turns the runner red (rc 1, `FAILED (failures=16)`). The full suites, `lint_hdl.sh`, Yosys and the `nvm_port` figures come from the author-r2 evidence and the manager's banks (see Limits). |

## Lens results

### Conformance

- **Enforcement.** The body/key check at `hdl/aecp/desc/gen_desc_image.py:214-222` is byte-for-byte the round-1 code. The only generator change is docstring line `:31`, and `receipts/ast-equiv.log` shows the code AST is equal.
- **Round-1 conclusions still hold.** Acceptance items 1-4 of 5847636202 remain met exactly as round 1 established:
  - named `ImageError` with cfg, key and body values, for both input forms;
  - discriminating tests and the mutant proof;
  - no image change;
  - no RTL, port or parameter change, and issue #60 untouched.
- **Evidence at this head.** Identical probe and mutant receipts, and images identical at base, round 1 and head.
- **Round-2 scope.** Round 2 does exactly the four assigned items and nothing else. The DUT-reader disposition correctly stays out of the processor, as manager item 3 requires.

Verdict: **CLEAN**.

### RTL

- There is no RTL, harness, port, parameter or Makefile change in the delta or in the PR.
- desc_store passes 584/584 through `scripts/run_suites.sh` on a reduced tree at head (`receipts/run_suites-reduced-head.log`).
- The author-r2 evidence at 11dd3e90 has 33 suites / 1,014,722 checks, `lint_hdl.sh` and `syn/yosys/run.sh`, all rc 0.
- Hosted `hdl` at the exact head: `docs-gates` and `portability` completed with success in both runs. Both `suites` jobs were still `in_progress` when last checked (`receipts/hosted-check-runs.txt`); I did not treat them as passed.

Verdict: **CLEAN**. The focused run used a non-pinned Verilator; see Limits.

### Robustness

- **Deadline removed.** The host deadline is gone. `cli()` at `tb/desc_store/test_gen_desc_image.py:61-65` now calls `subprocess.run(..., capture_output=True, text=True)` with no `timeout`. The parent detector flags no processor `tb/` file.
- **Hang bound.** The CLI reads a named file and writes two named files; it does not read stdin. A hang is bounded by the consumer runner's per-suite `timeout` (parent `scripts/run_all_suites.sh:389-390` at 831f94f4) and, in the standalone repository, by the hosted job limit. Neither affects pass or fail.
- **Probes.** All 21 round-1 robustness probes reproduce identically at head (`receipts/probes.json` equals the published R336-1 file). They cover `pad_to`, `name_index`, mixed-length runs, several configurations, ENTITY, duplicates, out-of-range keys, CLI `--line-bytes` and position.
- **Interpreters.** The new PEP 604 / PEP 585 annotations are evaluated at definition time. They run under Python 3.11, 3.12 and 3.14 (`receipts/interpreters.log`). Gating code already requires 3.10 or later: `tb/pp_top/test_fixture_guards.py` uses a parenthesised multi-item `with`.

Verdict: **CLEAN**. F2 is closed.

### Tests

- **Signatures and docstrings.** Every public method of `BodyKeyTest` now has a complete PEP 484 signature and a docstring: `model`, `cli`, `legal`, `refused` and the six `test_*` (`:26-131`).
  - The idiom scan shows 0/0, and no over-long line against the parent's 120-column limit. The longest line is `:57` at 94 columns.
  - Each docstring matches what its body does. For example, `refused` checks the exact message, CLI rc 1, empty stdout and the absence of both output files. `legal` checks exact bytes and that the CLI output equals `build()`.
- **Discrimination unchanged.**
  - 24 cases, with the cfg 1 / index 1 target and high-byte-only mismatches.
  - 16 refusal failures against the base generator.
  - All 11 mutants are killed with identical failing sets: M0 removes the check (16 fail, 8 pass, make rc 2), and M1-M10 as in round 1.
  - Wiring through `scripts/run_suites.sh` is still proven red on M0.

Verdict: **CLEAN**. F1 and F2 are closed.

### Docs

- **Test docstrings.** They are present and accurate (F1 closed), in the idiom of `tb/pp_top/test_fixture_guards.py`.
- **Generator sketch.**
  - `gen_desc_image.py:31` adds `{"name": "descriptor_index", "size": 2, "value": 0}` directly after `descriptor_type`. The ENTITY example now starts with type 0x0000 and index 0, matching its key (`"type": "ENTITY"`, `"index": 0`).
  - The AUDIO_MAP example `00170000…` also matches its key (0x0017, index 0).
  - Proven executable in `receipts/sketch-probe.log` (S1 closed).
- **F07.4 sentence** (`docs/architecture/07_memory_maps.md:246-247`): "Bytes 0–3 of every packed descriptor equal its index-map key (type, index), and the generator refuses a disagreement."
  - **Accurate.** Every descriptor that reaches the image passes through `_grouped_descriptors()`, which compares big-endian bytes 0-1 and 2-3 with the normalised `(type, index)` it is located by. `build()` has no other path. The refusal is proven by the tests, the probes and the mutants.
  - **Scoped to the generator.** The sentence does not claim that the store re-checks the bytes. That matters because the store does not read offsets 0-3 (round-1 finding, unchanged).
  - **Wording.** It follows the manager's item 4 text (S2 closed).
- **PR body and tb README.**
  - The PR body's "Round 2" section matches my receipts: signatures and docstrings, no host deadline, the sketch and F07.4, images identical at base, round 1 and round 2, 6 tests / 24 cases, the M0 8/16 split, and 0/0/0 scans.
  - `tb/desc_store/README.md` has no deadline claim and needed no change.
- **Gates.** The docs gates are rc 0: links 915, matrix, modmatrix 92 rows / 0 untested, params, wavedrom 18, and stale.

Verdict: **CLEAN**.

## Round-1 findings at this head

| Round-1 item | Status at 11dd3e90 | Evidence |
|---|---|---|
| R336-1 **F1** MINOR (Tests, Docs): 10 unannotated and 9 undocumented public functions | **CLOSED** | `receipts/parent-idiom-scan.log`: head 0/0 against round-1 10/9, with the round-1 scanner and the 831f94f4 gate unchanged. Signatures and docstrings are at `test_gen_desc_image.py:26-131`. Tests and mutants are unchanged (`receipts/round1-vs-round2.txt`). |
| R336-1 **F2** MINOR (Tests, Robustness): `timeout=60` host deadline | **CLOSED** | `receipts/parent-wallclock-scan.log`: head flags 0 files, round 1 flagged 1, none added. `test_gen_desc_image.py:61-65` has no deadline, and the AST shows `timeout=` was the only call change. |
| R336-1 **S1** SUGGESTION (= R337-1 S1): sketch lacked `descriptor_index` | **CLOSED** | `gen_desc_image.py:31`; `receipts/sketch-probe.log` (head agrees and is accepted; round 1 disagreed with index 0x2E2E). |
| R336-1 **S2** SUGGESTION: F07.4 did not state the body/key rule | **CLOSED** | `07_memory_maps.md:246-247`; accuracy argued in the Docs lens. |

## Prior public findings at this head

I read these only after the verdict and ledger above were written.

| Prior review | Finding | Status at 11dd3e90 | Evidence |
|---|---|---|---|
| R337-1 (POSITIVE at eb734969) | **R337-1-S1** SUGGESTION (Docs): the sketch at `gen_desc_image.py:29-31` lacks `descriptor_index` under the new rule | **CLOSED** | Same item as R336-1 S1: `gen_desc_image.py:31`, `receipts/sketch-probe.log`. R337-1 notes that the sketch's ENTITY was already not fully packable because of the name-offset rule, which is why the probe exercises `_grouped_descriptors()`, the rule's enforcement point. |
| R337-1 | no MINOR, MAJOR or BLOCKER | none to resolve | R337-1 report, section 3 |
| R336-1 (NEGATIVE at eb734969) | F1, F2, S1, S2 | all **CLOSED** | see "Round-1 findings at this head" |

There were no GitHub review threads or formal reviews on the PR, only the issue and PR comments listed above.

## Findings (this round)

None. No BLOCKER, MAJOR, MINOR or SUGGESTION is raised at this head.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta eb734969..11dd3e90; `gen_desc_image.py:1-80,175-240`; generator AST equality; issue #123 acceptance and round-2 assignment; manager items 1-3 of 5847888234; probes and images at base, round 1 and head | R336-2 (delta) on R336-1 (full) | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |
| RTL | CLEAN | diff name list (no HDL or harness); desc_store 584/584 through reduced `run_suites.sh` (non-pinned 5.052); author-r2 suites 1,014,722, lint and yosys rc 0; hosted docs-gates and portability success, suites in progress | R336-2 | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |
| Robustness | CLEAN | `test_gen_desc_image.py:57-65`; parent wall-clock detector at 831f94f4; parent runner per-suite `timeout`; 21 probes identical to round 1; Python 3.11, 3.12 and 3.14 runs | R336-2 | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |
| Tests | CLEAN | `test_gen_desc_image.py:1-136`; parent Rule 12 scan 0/0; AST normalised equality; 6 tests / 24 cases; 16 failures against the base generator; 11/11 mutants identical to round 1; reduced runner red on M0 | R336-2 | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |
| Docs | CLEAN | test docstrings; `gen_desc_image.py:20-42` sketch and rule, executed; `07_memory_maps.md:240-247`; PR body "Round 2"; `tb/desc_store/README.md`; `make check` and the CI docs-gates commands; `git diff --check` (both ranges) | R336-2 | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |

## Real limits

- **Pinned Verilator unavailable.** The designated pinned Verilator 5.050 path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host, so I could not verify its identity and did not use it. I also did not use any other unassigned binary. The focused desc_store run used the host Verilator 5.052; it is supplementary, not a pinned-tool result. Round 2 changes no HDL or harness.
- **Banks not run.** Per scope, I did not run the full processor `run_suites.sh` bank, `lint_hdl.sh`, `syn/yosys/run.sh`, the `nvm_port` figures, or any parent, gPTP or builder bank. For these I rely on the author-r2 evidence at 11dd3e90 and the manager's banks.
- **Parent gates.** I did not run the parent gates themselves. I called only their pure per-file detectors, fetched read-only from 831f94f4, through the unchanged round-1 scanners. The parent-wide totals come from the consumer bank, which the manager runs separately with the parent pin-bump patch.
- **Hosted jobs.** Both hosted `suites` jobs at the exact head were still `in_progress` at 2026-09-26T17:09Z. `docs-gates` and `portability` had succeeded. I did not fetch job logs.
- **Parent images.** I did not re-derive the parent's five-config image identity. Round 2 changes no generator code (AST equal), so manager comment 5847782435 still applies.
- **Wavedrom gate.** It bootstrapped a local virtual environment inside the disposable scratch clone only.
- **Hardware.** Physical calibration NOT RUN. No hardware was used. Field skips are not hardware proof.

## Clone state after probes

All probes ran on exported copies under the packet's scratch directory. The review clone is untouched (`receipts/clone-integrity.txt`):
- HEAD, index tree and worktree all match 11dd3e90 / 2e66f6ca;
- index blob IDs and modes equal the HEAD tree;
- worktree blob bytes and executable modes equal the HEAD tree;
- 0 untracked or ignored entries;
- 0 gitlinks, and no `.gitmodules` (none are required in this repository).

## Pending manager duties

- Parent consumer bank at this head with the parent pin-bump patch: the #120 `aecp_name_wr_o` port, and the DUT-reader dispositions for `name_wr_mutant.py` and `test_gen_desc_image.py` (manager comment 5847888234, item 3).
- Completion of the hosted `suites` jobs at 11dd3e90, and hosted/act acceptance.
- The final current-dev merge candidate: source base 870ff88a onto live dev 831f94f4.
- Merge only with two independent positive reviews and the full completion bar.
- Publication of this packet.

## Reproduction

`scripts/run_r2.sh <processor-clone> <packet-dir> <parent-gate-scripts-dir> [<R336-1-receipts-dir>]` regenerates every receipt except the following:
- `hosted-check-runs.txt`, a read-only API listing;
- `r1-scripts-identity.txt` and `parent-gate-provenance.txt`, blob comparisons against kebag-logic/milan-fpga;
- `interpreters.log`, from `scripts/count_cases.py <head-tree>` under each interpreter, run from `tb/desc_store`;
- `clone-integrity.txt`.

What the driver uses:
- `scripts/r1/` holds the R336-1 scripts, byte-identical to the published ones (`receipts/r1-scripts-identity.txt`). Only `parent_idiom_scan.py`, `parent_wallclock_scan.py`, `images.sh`, `mutants.py`, `probes.py` and `legal_models.py` are invoked; `run_all.sh` is kept for reference.
- The new round-2 helpers are `sketch_probe.py`, `ast_equiv.py` and `count_cases.py`.
- The parent gate directory directly holds the six files named in `receipts/parent-gate-provenance.txt` from 831f94f4.

All receipts are listed in `MANIFEST.sha256`.

R336-2 FINISHED
