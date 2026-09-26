[R337] POSITIVE - exact head 11dd3e903685183250e7cd8ecc391b04fe7fd494

# R337-2 external independent review: processor issue #123 / PR #124, round 2

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| Pull request / issue | #124 / #123 |
| Exact head | `11dd3e903685183250e7cd8ecc391b04fe7fd494`, tree `2e66f6caff52773103df53bc4992d92f72328d0b` |
| Round-1 head | `eb734969154d5a75ff84b2779ff6088a2f4311a5` (the parent of this head; my R337-1 reviewed it in full) |
| Base | `870ff88ad35bbd532244e4c7e6d7661b9f6e1366` |
| Round | R337-2. This is a delta review of `eb734969..11dd3e90`, judged as the exact-head review for merge |
| Verdict | POSITIVE. No open MINOR, MAJOR or BLOCKER finding. Every round-1 finding and suggestion is closed. |

## 1. Reconstruction

- **Conventions.** There is still no `AGENTS.md` or `CONTRIBUTING.md`. As in round 1, conventions come from `README.md`, `docs/README.md`, the `Makefile`, `scripts/run_suites.sh` and `.github/workflows/hdl.yml`.
- **Scope.** These sources are unchanged since round 1:
  - the issue #123 body;
  - the assignment `issuecomment-5847636202` (acceptance items 1-5);
  - the kebag-logic/milan-fpga#509 ownership decision.

  The round-2 assignment `issuecomment-5847977272` asks for exactly four items and "no behaviour change":
  1. **R336-1 F1:** PEP 484 signatures and docstrings on every public function in the test file.
  2. **R336-1 F2:** drop `timeout=60`.
  3. **S1:** add `descriptor_index` to the input sketch.
  4. **S2:** add one F07.4 sentence.

  Manager comment `issuecomment-5847888234` gives the parent-bank origin of F1/F2. It leaves item 3, the DUT-reader disposition, to the parent pin-bump patch.
- **Diff.** `git diff eb734969..11dd3e90` touches three files, +26/-12 (`receipts/diff-r1head-head.patch`, `receipts/scope.txt`):
  - `tb/desc_store/test_gen_desc_image.py`: annotations, docstrings, `from typing import Any`, and removal of `timeout=60`;
  - `hdl/aecp/desc/gen_desc_image.py`: one docstring line;
  - `docs/architecture/07_memory_maps.md`: two added lines.

  The cumulative base..head diff is in `receipts/diff-base-head.patch`. The head is one commit whose parent is `eb734969`. PR #124's `head.sha` equals the exact head.
- **Public evidence.** I read kebag-logic/milan-fpga branch `pp123-review-evidence` at `d01c1722`. The brief's `8a640700` is an ancestor of it, but it does not yet contain `reviews/R336-1/`; the R336-1 scan scripts first appear at `b4a249b`. I read `author-r2/` (suites, figure, Yosys, image and scan logs) and the manager's comments 5847782435 and 5847888234 on the PR and issue.
- **Prior public findings.** I read these only after my own pass: R336-1 (`reviews/R336-1/REPORT.md`, F1, F2, S1, S2) and my own R337-1 (S1). Each is resolved in §3. PR #124 has 0 reviews and 0 review comments.

## 2. Verification of the round-2 delta

### 2.1 R336's scans, rerun unchanged (`receipts/scan-*.log`)

I copied `parent_idiom_scan.py` and `parent_wallclock_scan.py` byte-for-byte from the evidence branch. Their sha256 values equal those in the R336-1 `MANIFEST.sha256`. I ran them with the parent scripts from kebag-logic/milan-fpga `831f94f4` (digests in `receipts/environment.txt`) over `git archive` exports.

| Scan | base 870ff88a vs round-1 eb734969 | base 870ff88a vs head 11dd3e90 |
|---|---|---|
| Rule 12 idiom (budget 0/0) | rc 1: head adds 10 unannotated and 9 undocumented public functions in `tb/desc_store/test_gen_desc_image.py`. This reproduces F1. | rc 0: **0 unannotated, 0 undocumented**. The only non-zero row is the pre-existing `long module` in `hdl/aecp/ucode/gen_ucode.py`, unchanged from base. |
| Wall-clock / deadline | rc 1: 1 file added (`test_gen_desc_image.py`). This reproduces F2. | rc 0: base 0, head 0, **no file added** |

The same scans in the author's `author-r2/parent-*-scan.log` agree.

### 2.2 Sketch and F07.4 sentence (`scripts/sketch_and_f074.py`, `receipts/sketch-f074.log`)

**Sketch.** The script lifts the JSON sketch literally out of each tree's `INPUT FORMAT` docstring. It drops only the `//` comments, the bare `...` list token and the ellipsis after a hex prefix; the `"string": "..."` placeholder stays literal. It then runs the generator's own `_grouped_descriptors()`, which is where the body/key rule lives.

| Tree | ENTITY body bytes 0-3 | Body/key rule | Full `build()` |
|---|---|---|---|
| round-1 `eb734969` | `0000 2e2e` | **refused**: `cfg 0 directory key type 0x0000 index 0 disagrees with body type 0x0000 index 11822` | refused (same) |
| head `11dd3e90` | `0000 0000` | **accepted** | refused: `cfg 0 ENTITY entity_name differs from name-table entry 0` |
| base `870ff88a` | `0000 2e2e` | (no rule) | refused: same ENTITY name-offset message as head |

At head the sketch satisfies the new rule. The ENTITY name-offset refusal that remains is pre-existing: it is identical at base. It comes from the sketch being schematic (it puts `entity_name` at offset 4, where the ENTITY layout has it at offset 48). The assignment required only the body/key rule. The AUDIO_MAP `bytes` alternative starts `0017 0000`, which also satisfies the rule.

**F07.4 sentence.** The new sentence at `docs/architecture/07_memory_maps.md:246-247` reads: "Bytes 0–3 of every packed descriptor equal its index-map key (type, index), and the generator refuses a disagreement." I checked it three ways:
- **Source.** Every body that `_render_image` writes comes from `_grouped_descriptors`, after the check (`gen_desc_image.py:203-236, 352-377`). No descriptor is synthesized elsewhere.
- **Bytes.** The script walks each built image's header and index map. It uses the store's run-relative addressing, so the key for member i of a row is (row type, earlier-row count + i). Every descriptor's bytes 0-3 equal that key:
  - `example_milan_8`: 8 rows / 8 descriptors, 0 mismatches, for base, round 1 and head;
  - the tests' 8 legal images (two configurations, index 1): 0 mismatches (`receipts/legal-probe-images.txt`).
- **Attribution.** The sentence assigns the refusal to the generator only. `KL_aecp_desc_store.sv` locates bodies through the index map and does not inspect body bytes, so the sentence neither overclaims nor underclaims.

### 2.3 No behaviour change

- **Executable content** (`scripts/ast_delta.py`, `receipts/ast-delta.txt`). I stripped docstrings, parameter and return annotations, `from typing import ...` and `timeout=` keywords. After that, the round-1 and head ASTs of both Python files are **equal**. The test file's `timeout=` goes from present to absent. The docs file only gains 2 lines, and no other path differs.
- **Tests at head** (`receipts/new-tests-head.log`). 6 tests pass, rc 0: `KEYS` has 4 spellings × 6 tests = 24 subtest cases.
- **Tests against the base generator** (`receipts/new-tests-vs-base-generator.log`). rc 1, `FAILED (failures=16)`. `scripts/compare_rounds.py` (`receipts/round1-vs-round2.txt`) shows that the set of 22 (test, key, outcome) lines and the 16 assertion messages equal round 1's. The raw text differs only because unittest now prints the new docstrings, and because of paths and line numbers.
- **Round-1 probe matrix** (`scripts/probe_bodykey.py`, unchanged). `receipts/probes-head.jsonl` and `receipts/probes-base.jsonl` are **byte-identical** to the round-1 receipts: 33/33 as expected at each revision.
- **Round-1 mutants** (`scripts/mutants.py`, unchanged, over the head tree; `receipts/mutants.jsonl`). The control passes (tests rc 0, `make generator-check` rc 0). All 13 mutants are killed (tests rc 1, make rc 2). Once timings are normalised, the receipt is **identical** to round 1. The author's mutant still fails 16 refusal cases, and the legal tests still pass.
- **Entry points** (`scripts/entry_point.sh`, `receipts/entry-point.log` and the `entry-*` logs). This used a reduced head tree with the pinned Verilator 5.050 and `-j 8`.
  - Control: `make` rc 0 (`Ran 6 tests ... OK`, then `584 checks: 584 PASS, 0 FAIL`); `run_suites.sh` rc 0 (`PASS desc_store`).
  - Check removed: `make` rc 2 (stops at `generator-check`, `FAILED (failures=16)`); `run_suites.sh` rc 1 (`FAIL desc_store`).
  - Both results match round 1.
- **Images** (`scripts/image_digests.sh`; `receipts/images-{base,r1,head}.sha256`, `receipts/images-compare.txt`). base = round 1 = head, byte for byte:
  - `desc_store_image.bin` `20356f59…b62c`
  - `.map` `23a43044…091c`
  - `ltn_rom.hex` `23cc67ee…e956`
  - `ucode.hex` `23605682…7144`

  The head digests also equal my round-1 receipt. The eight legal probe images from the PR's own test models are identical across base, round 1 and head: `005bbc19…f071` ×6 and `a0483ef4…0c04` ×2. That matches the author's `author-r2/probe-image-digests.json`.

### 2.4 Gates (`receipts/gates.log`, scratch clone at the exact head; all rc 0)

- `make check`: lint 41 mermaid + 18 wavedrom, links 915, REQ matrix 115 rows, module matrix 92 rows / 0 untested, params 24/24/24.
- `scripts/check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `gen_matrix.py --check`, `render-wavedrom.py --check`, `make stale`.
- `git diff --check`, for both `870ff88a..11dd3e90` and `eb734969..11dd3e90`.
- `scripts/lint_hdl.sh` with pinned Verilator 5.050: every module `LINT OK`.

The scratch clone was clean after the gates.

**Hosted jobs at the exact head** (`receipts/hosted-check-runs.tsv`, `hdl` workflow, push and pull_request events):
- `docs-gates` and `portability` (Yosys) **executed and succeeded** on both events.
- `suites` was **in progress** at my final query (see the receipt's timestamp).

The author's public `author-r2/suites.log` records `suites: 1014722 checks total, 0 failing`, and its figure and Yosys logs are rc 0. None of this is my execution.

## 3. Round-1 findings: closed or retained

| Finding | Origin | Status at 11dd3e90 | Evidence |
|---|---|---|---|
| R336-1 F1 (MINOR): 10 unannotated / 9 undocumented public functions | R336-1 | **CLOSED** | `scan-idiom-base-vs-head.log`: 0/0 at head, rc 0 (was 10/9 at round 1, rc 1). Every method has a complete signature, including `-> None` on all tests and a typed `model`/`cli`/`legal`/`refused`, plus a docstring stating what it builds or proves (`test_gen_desc_image.py:26-131`). This matches the idiom of `tb/pp_top/test_fixture_guards.py:15-22`. I checked that each docstring agrees with its body. The `str | int` syntax already has precedent in `tb/srp_admission/mutants.py:68`, and CI runs on `ubuntu-latest`. |
| R336-1 F2 (MINOR): `timeout=60` host deadline | R336-1 | **CLOSED** | `scan-wallclock-base-vs-head.log`: no file added, rc 0. In `ast-delta.txt`, `timeout=` goes from present to absent and the logic is otherwise equal. No other clock or deadline use was introduced. The processor's other `tb/` subprocess callers carry no deadline either. The hang bound is the parent sweep's per-suite `timeout "$TMO" make`, together with the hosted job limit. The child is a deterministic pure-Python packer with no blocking I/O. |
| R337-1 S1 = R336-1 S1 (SUGGESTION): sketch lacked `descriptor_index` | R337-1, R336-1 | **CLOSED** | `gen_desc_image.py:31`. `sketch-f074.log` shows the round-1 sketch refused by the body/key rule, and the head sketch accepted by it. |
| R336-1 S2 (SUGGESTION): F07.4 note | R336-1 | **CLOSED** | `07_memory_maps.md:246-247`. The sentence is accurate against the source, the built image bytes and the store's behaviour (§2.2). |
| R336-1, not a processor finding: DUT-source reader | R336-1 / manager 5847888234 item 3 | Parent-side, unchanged | This is left to the parent pin-bump patch. No processor change is due. |

## 4. Findings at this head

There are no findings: no BLOCKER, MAJOR, MINOR or SUGGESTION is open.

## 5. Lens assessments (delta `eb734969..11dd3e90`, carrying the round-1 full review)

- **Conformance.** Acceptance items 1-4 are unaffected by the delta: the executable AST is equal, the probes are byte-identical and the images are byte-identical. The sketch now matches IEEE 1722.1 §7.2 (u16 type, then u16 index) and the rule it documents. The F07.4 sentence states the §7.2 layout relation correctly. Item 5 (the parent consumer bank) remains the manager's duty.
- **RTL.** No RTL, `syn/`, workflow, port or parameter path changed (`scope.txt`). `lint_hdl.sh` passes, params are 24/24/24, the desc_store RTL suite is 584/584 over a byte-identical image, and the hosted `portability` job succeeded at the exact head.
- **Robustness.** The 33-probe adversarial matrix is byte-identical at head and still shows CLI atomicity. The deadline removal cannot turn a slow host into a false FAIL. Every legal image, including multi-configuration images, keeps bytes 0-3 equal to the key.
- **Tests.** The tests still discriminate: 16 failures against the base generator, 13 of 13 mutants killed, and red/green entry points under `make` and `run_suites.sh`. The parent Rule 12 and wall-clock scans are clean, and the tests are no longer host-clock dependent.
- **Docs.** The test docstrings are accurate. The sketch now satisfies the rule stated two lines below it. The F07.4 sentence is accurate and correctly attributed to the generator. `tb/desc_store/README.md` (unchanged) still matches the observed 6 tests / 24 cases and the 8-pass / 16-fail mutant table. The PR body's round-2 section matches my receipts. `make check`, links, wavedrom, stale and `git diff --check` all pass.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #123 body; assignments `5847636202`, `5847977272`; manager `5847888234`; `gen_desc_image.py:17-42,203-236`; `07_memory_maps.md:239-247`; `sketch-f074.log`; `ast-delta.txt`; `probes-head.jsonl` | R337-2 (delta) on R337-1 (full) | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |
| RTL | CLEAN | `scope.txt`, where the delta has no HDL, syn, workflow or parameter path; `gates.log` (`lint_hdl.sh`, params); `entry-control-make.log` (584/584); `hosted-check-runs.tsv` (portability success) | R337-2 on R337-1 | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |
| Robustness | CLEAN | `probes-{head,base}.jsonl` (byte-identical to round 1); `scan-wallclock-*.log`; `ast-delta.txt`; `legal-probe-images.txt`; `images-*.sha256`; `KL_aecp_desc_store.sv` locate path | R337-2 on R337-1 | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |
| Tests | CLEAN | `test_gen_desc_image.py` (head); `new-tests-head.log`; `new-tests-vs-base-generator.log`; `mutants.jsonl`; `round1-vs-round2.txt`; `entry-point.log` with the four `entry-*` logs; `scan-idiom-*.log` | R337-2 on R337-1 | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |
| Docs | CLEAN | test docstrings; `gen_desc_image.py:20-42`; `07_memory_maps.md:246-247`; `tb/desc_store/README.md:59-90`; PR #124 body, round-2 section; `gates.log` (`make check`, links, wavedrom, stale, matrix, `git diff --check`) | R337-2 on R337-1 | 11dd3e903685183250e7cd8ecc391b04fe7fd494 |

## 7. Real limits

- **Full banks not run.** I did not run the full 33-suite `run_suites.sh`, `syn/yosys/run.sh`, the 46-build `nvm_port` figure gate, or any parent, donor or consumer bank. I ran `run_suites.sh` and `make` over a reduced desc_store-only tree, for control and mutant, and all docs, matrix and lint gates locally.
  - For the rest I rely on the author's public `author-r2` logs, the manager's source banks, and the hosted jobs.
  - Hosted `suites` was still in progress when I last queried. Its outcome is not asserted here.
- **Parent gates.** The R336 scans call only the parent gates' pure per-file `scan()` / `uses_wall_clock()`, at parent `831f94f4`. They are not the parent consumer bank. That bank, run with the pin-bump patch (the `aecp_name_wr_o` port plus the DUT-reader dispositions), was not observed by me.
- **Evidence ref.** The R336-1 scripts were taken from evidence branch head `d01c1722`, because the brief's `8a640700` predates them. Their digests match R336-1's own manifest.
- **Verilator substitution.** The brief's Verilator path (`$VALIDATION_STORAGE/372-manager-candidate1/...`) does not exist on this host. I used the head-specific wrapper `$VALIDATION_STORAGE/pp123-manager-11dd3e90/pinned-tool-bin/verilator`. It reports `Verilator 5.050 2026-07-01 rev v5.050`, and its wrapper and binary digests equal those used in round 1 (`receipts/environment.txt`). The local image-root path is redacted to `<verilator-image-root>` in `environment.txt` and `entry-control-make.log`. That redaction is the only edit to any receipt.
- **Local tool versions.** I used local Python 3.14.7, GNU Make 4.4.1 and g++ 16.2.1. They differ from the hosted runner images.
- **Hardware.** Physical calibration was NOT RUN. No hardware proof is claimed, and field skips are not hardware proof.
- **Clone integrity** (`receipts/clone-integrity.txt`). The review clone was never modified; all probes ran on `git archive` exports or a scratch clone. The final check showed:
  - HEAD `11dd3e90`, tree `2e66f6ca`, `write-tree` = tree;
  - an empty `status --porcelain --ignored`, and empty `diff-index`/`diff-files` (content and mode);
  - `ls-files -s` digest `5d0544bc…2ad9` (249 entries).

  The repository has no `.gitmodules` and no mode-160000 gitlinks, so no submodule gitlink applies.

## 8. Pending manager duties

- Run the parent consumer bank at `11dd3e90` with the parent pin-bump patch (#120 `aecp_name_wr_o` port and the DUT-reader dispositions for `name_wr_mutant.py` and `test_gen_desc_image.py`). This confirms issue #123 acceptance item 5 and the verification clauses of F1/F2 on the parent side: the Rule 12 gate passes and the wall-clock ratchet is ≤ 3.
- Confirm that the hosted `suites` job succeeds at this exact head on both events, and own hosted and act acceptance.
- Build and validate the final current-dev candidate at the merge turn: source base `870ff88a`, live dev `831f94f4`. That candidate is distinct from this source validation.
- Obtain the other independent exact-head review (R336-2) and the full completion bar before merging.

R337-2 FINISHED
