[R336] NEGATIVE - exact head eb734969154d5a75ff84b2779ff6088a2f4311a5

# R336-1 independent internal review: processor PR #124 / issue #123

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `eb734969154d5a75ff84b2779ff6088a2f4311a5`, tree `66f2b9733acc16a2e4588178e4582d62ce7f84fb`. This is one commit on base `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`. The PR head was rechecked at the end of the review and had not moved.
- Diff: 4 files, +172/-2:
  - `hdl/aecp/desc/gen_desc_image.py` +10
  - `tb/desc_store/Makefile` +5/-2
  - `tb/desc_store/README.md` +33
  - `tb/desc_store/test_gen_desc_image.py`, new, mode 100644, +124
- No `.sv`, `.svh`, `.v` or C++ harness file changed. There are no submodules or gitlinks.
- Review start: PR comment 5847847067. Reviewer role: internal independent reviewer, cleared context, isolated detached clone.

## Verdict in one paragraph

The functional change is correct and complete:
- it refuses a body type or index mismatch for both input forms;
- nothing bypasses it;
- it changes no legal image;
- the tests discriminate, are wired into `scripts/run_suites.sh`, and kill all 11 mutants.

The verdict is **NEGATIVE** because the new test file carries two defects that make the parent consumer gates fail once this head is pinned. Both are processor-side fixes (F1, F2, both MINOR):
- **F1:** 10 unannotated and 9 undocumented public functions, against a zero budget.
- **F2:** a host `subprocess` deadline.

The manager's consumer-bank comment 5847888234 surfaced both. I reproduced both independently with the parent gates' own per-file detectors. The processor's pre-existing Python and `tb/` files are clean under both detectors at base.

## Reconstruction (in the required order)

1. **Repository conventions.** There is no `AGENTS.md` or `CONTRIBUTING.md` in the tree. I read `README.md`, `docs/README.md`, the `Makefile`, `hdl/README.md` (rules and consumption contract) and `.github/workflows/hdl.yml`. The gates are:
   - `scripts/run_suites.sh`, which runs `make` in every `tb/*/` directory that has a Makefile;
   - `scripts/lint_hdl.sh`;
   - `make check`;
   - `gen_matrix.py --check`;
   - the CI docs-gates job;
   - the `nvm_port` figures check;
   - `syn/yosys/run.sh`.
2. **Issue #123.** I read the body and the assignment comment 5847636202, which holds acceptance items 1-5 and the gates. The executor's REVIEW READY comment 5847761667 is also on the issue.
3. **Ownership authority.** Issue #123 cites follow-up F7 of the parent ownership matrix (kebag-logic/milan-fpga#509; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` at PR #568 head `04c9802d`, lines 59 and 242). F7 reads: "Refuse descriptor body type/index disagreement with its directory key... Legal body/key pair accepted; independently refuse mismatched body type and mismatched body index. Both invalid probes currently pack unchanged." The decision says the processor keeps generic packed-image checks.
4. **Interface authority.** 07 §3.3 / F07.4 (`docs/architecture/07_memory_maps.md:226-245`) defines the flat image. The store never reads a descriptor's interior, apart from the name overlay at offsets 4, 48 and 180, so it does not touch offsets 0-3. In IEEE 1722.1-2021 §7.2, every descriptor starts with `descriptor_type` (u16) at offset 0 and `descriptor_index` (u16) at offset 2, big-endian.
5. **Issue #60.** The body is unchanged since it was created (updated_at = created_at = 2026-09-18T13:33:02Z, 0 comments). Its only new event is a cross-reference from this PR.
6. **Diff and history.** I read the full diff 870ff88a..eb734969 and the full post-change generator.
7. **Public evidence.**
   - kebag-logic/milan-fpga `review-evidence/pp123-r1` at `8a640700`: `head.txt` = eb734969. It also holds `mutant.patch` and `mutant-results.json`, plus the suites (1,014,722 checks), lint, yosys, `make check` and `nvm_port` figures logs, all rc 0.
   - Manager parent image comment 5847782435: five parent configs, base and PR AEM images byte-identical, 50 builder outputs identical.
   - Manager bank-results comment 5847888234, read after my independent pass:
     - donor bank 9/9;
     - parent consumer bank 8/11 with the unpatched parent. Two failures are attributed to #120's port, which is parent pin-bump work. Three gates are tripped by this PR's new test file; two of those are classified as processor fixes.
8. **Prior public review findings on PR #124.** There were none at the start of this review: 0 review threads, 0 reviews, and only manager comments. There is nothing to resolve or retain. The other reviewer's verdict comment (5847930248) was posted during this review; I did not read its content.

## Lens results

### Conformance
- **Placement.** The check sits at `gen_desc_image.py:214-221`, in `_grouped_descriptors`, immediately after `descriptor_bytes()`. That function is the single place where both body forms, `fields` and literal `bytes`, are assembled and `pad_to` is applied (`:177-193`). It reads the big-endian u16 at body offsets 0 and 2 and compares the pair with the normalised directory key `(typ, idx)`. A mismatch raises `ImageError("cfg C directory key type 0xTTTT index I disagrees with body type 0xBBBB index J")`, which names the cfg, both key values and both body values (acceptance item 1).
- **Scope.** The change matches F7 and the #509 ownership decision: a generic check with no configuration-dependent semantics.
- **Base behaviour.** At base, the invalid probes pack. My probes show this for both forms (`receipts/probes.json`, `base_build`), and the new test fails 16 refusal cases against the base generator (`receipts/head-tests-vs-base-generator.log`, rc 1).
- **Parent coverage.** The parent packer `avdecc/gen_aemi_image.py:422` at parent dev `831f94f4` calls `image.build(doc, line_bytes)`, so the parent path cannot bypass the check.

### RTL
- No RTL, port, parameter or harness change.
- The desc_store RTL suite passes at head: 584 checks, 584 PASS, the same tally as the author's evidence. I ran it through `scripts/run_suites.sh` on a reduced tree containing `tb/common` and `tb/desc_store` only (`receipts/run_suites-reduced-head.log`). That run used a system Verilator 5.052, **not** the CI-pinned 5.050 (see Limits).
- Hosted `hdl` workflow at the exact head: two runs, 36254506231 and 36254508303. Their six jobs (suites, docs-gates and portability in each) all completed with success, and none was skipped (`receipts/hosted-check-runs.txt`). I could not fetch the job logs.

### Robustness
I wrote my own probes (`scripts/probes.py`, 21 cases). Each case is packed through `build()` and the CLI, at both base and head. **21/21 behaved as expected** (`receipts/probes.log`, `receipts/probes.json`).

Refused at head, each with the body/key diagnostic, CLI rc 1, and no image and no map written:
- **`pad_to`:** an empty `bytes` body padded to 8, and an empty `fields` list padded to 16.
- **`name_index`:**
  - a named multi-descriptor group with a body index mismatch;
  - `name_index -1`;
  - an invalid `name_index` 70000, where the body/key refusal fires first.
- **Grouped / mixed-length:** a STREAM_INPUT with runs of 140 and 148 bytes and a mismatch in the second run.
- **Several configurations:** the mismatch is in cfg 2, and the diagnostic names cfg 2.
- **ENTITY:** a body index of 1.
- **Duplicate key:** the body/key refusal fires first.
- **Out-of-range keys:**
  - a key type over 16 bits; at base this crashed with `OverflowError`, now it is a clean `ImageError`;
  - a key index of 65536;
  - a key index of -1.
- **CLI `--line-bytes 8`:** the body/key refusal fires first.
- **Position:** a mismatch in the first of four descriptors.

Accepted at head, byte-identical to base:
- a legal `bytes` body;
- a 4-byte `value` field;
- a `bytes` field with whitespace;
- a `string` field at offset 0;
- a short body padded with `pad_to`;
- a legal ENTITY;
- a key written as `" 0x0014"`.

`build()` is the only route into `_grouped_descriptors`, and `main()` calls it before opening any output.

This lens is still UNCLEAN because of F2: the new test's CLI calls carry a host wall-clock deadline.

### Tests
- **New tests.** `tb/desc_store/test_gen_desc_image.py` has six tests × four key spellings = 24 subtests. They cover the legal pair, type-only mismatch and index-only mismatch for both forms. Each case goes through both `build()` and the CLI:
  - refusals: exact message, rc 1, empty stdout, no image and no map;
  - legal cases: exact bytes, and the CLI image and map equal the `build()` output.
- **Discrimination.** The target is cfg 1, index 1, and each mismatch flips only the high byte. The tests pass at head (`receipts/head-tests-direct.log`, `receipts/head-generator-check.log`).
- **Wiring.** `tb/desc_store/Makefile:21` makes `run` depend on `generator-check`, and `:31-32` runs the tests. `run` is the default target that `scripts/run_suites.sh` invokes.
  - I proved the wiring by breaking the check: with the author's mutant, `scripts/run_suites.sh` prints `FAIL desc_store` and exits 1, with `FAILED (failures=16)` at `Makefile:32` (`receipts/run_suites-reduced-M0.log`).
  - `make generator-check` and the default `make` both exit 2.
- **Mutants.** I ran the author's mutant (M0, identical to `mutant.patch`) and ten of my own (`scripts/mutants.py`, `receipts/mutants.json`). **All 11 were killed**, with exactly the expected tests failing and both entry points non-zero.
  - M0 removes the check. The 16 refusal cases fail and the 8 legal cases pass, which reproduces the README table.
  - M1 compares type only; M2 compares index only.
  - M3 compares only the low bytes.
  - M4 checks the `fields` form only; M5 checks the `bytes` form only.
  - M6 drops cfg from the message.
  - M7 raises the wrong exception type.
  - M8 reads the type from the wrong slice.
  - M9 makes the CLI write output before `build()`.
  - M10 makes the check over-strict.

This lens is still UNCLEAN because of F1 and F2, which are about the test file's code quality and determinism, not its discrimination.

### Docs
- **Generator docstring.** `gen_desc_image.py:40-41` states the new rule.
- **tb README.** Every factual claim in `tb/desc_store/README.md:59-90` holds against the tree and my runs:
  - 24 cases;
  - cfg 1 / index 1;
  - high-byte-only mismatches;
  - the list of legal controls;
  - `run_suites.sh` gating;
  - M0: 16 fail / 8 pass, make exit 2.
- **Docs gates.** All rc 0 (`receipts/docs-gates.log`):
  - `make check` (lint, wavedrom-check, links 915, matrix, modmatrix, params, stale);
  - the CI docs-gates commands individually;
  - `gen_matrix.py --check`;
  - `check_upc_map.py`;
  - `git diff --check 870ff88a eb734969`.

This lens is still UNCLEAN because of F1: nine of the new test's public functions have no docstring. The processor's existing unittest file documents each test (`tb/pp_top/test_fixture_guards.py:15-22`). S1 and S2 are optional suggestions.

## Acceptance items (issue #123, comment 5847636202)

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Named `ImageError`, stating cfg, key and body; both forms | met | `gen_desc_image.py:214-221`; probes; exact-message assertions |
| 2 | Legal accepted; type-only and index-only refused independently, both forms; mutant proof | met | tests pass at head; M0-M10 killed |
| 3 | No legal image changes | met | 11 image artifacts rebuilt at base and head are identical (`receipts/images-*.sha256`). They are the desc_store `image.bin`/`image.map`, three `ltn_rom.hex`, two `ucode.hex`, the Yosys generator outputs, and `build()` of `example_milan_8.json`. The worked example is `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c`. The eight legal test models are identical base = head, as are 7 accept probes. |
| 4 | Nothing else changes; issue #60 untouched | met | 4-file diff; no RTL; issue #60 unchanged |
| 5 | Parent images byte-identical at the new pin, checked by the consumer bar | images met by manager evidence (5847782435); **consumer bar not met** | Consumer bank 8/11 (5847888234). Two of its failures come from this head's new file and need a processor change: F1 and F2. |
| Gates | Processor suites, lints, docs gates, `git diff --check` | met by my runs (docs gates, diff hygiene, desc_store suite) and by public evidence (full suites, lint, Yosys, `nvm_port` figures) | receipts; author evidence; hosted jobs success |

## Findings

**F1: MINOR**
- **Lenses:** Tests, Docs.
- **Location:** `tb/desc_store/test_gen_desc_image.py:25, 55, 64, 82, 104, 107, 110, 113, 116, 119`.
- **Authority / evidence:**
  - Parent consumer gate `scripts/check_py_idiom.py` (Rule 12, parent `docs/development/CODE_QUALITY.md:2567`) scans the `protocol-processor` submodule. Its `scripts/py_idiom.budget` at parent dev `831f94f4` holds `unannotated public function = 0` and `undocumented public function = 0`.
  - Applying the gate's own `scan()` to every processor `*.py` (`scripts/parent_idiom_scan.py`, `receipts/parent-idiom-scan.log`):
    - base: 0 / 0;
    - head: 10 unannotated (`model`, `cli`, `legal`, `refused` and the six `test_*` methods) and 9 undocumented (the same, except `model`).
  - Processor idiom: the existing unittest `tb/pp_top/test_fixture_guards.py:15-22` is annotated `-> None` and documented, and the generator's public functions are annotated.
  - First reported in manager comment 5847888234, item 1; independently reproduced.
- **Impact:** At this pin, the parent consumer bank fails the Rule 12 gate, so the consumer bar (acceptance item 5 and the `hdl/README.md` consumption contract) cannot pass without a processor change. The new file also departs from the processor's own test idiom.
- **Required outcome:** give every public method of `BodyKeyTest` a complete PEP 484 signature and a docstring. For example, `-> None` on the tests, typed `model`, `cli`, `legal` and `refused`, and a docstring saying what each test proves.
- **Verification:**
  - `scripts/parent_idiom_scan.py` reports head totals of 0 for both rows;
  - `make -C tb/desc_store generator-check` still passes;
  - `scripts/mutants.py` still kills all mutants;
  - the parent consumer bank's Rule 12 gate passes at the new pin.

**F2: MINOR**
- **Lenses:** Tests, Robustness.
- **Location:** `tb/desc_store/test_gen_desc_image.py:62` (`subprocess.run(..., timeout=60)` in `cli()`).
- **Authority / evidence:**
  - Parent consumer gate `scripts/measure_test_evidence.py`, rule 4 (wall-clock dependence), counts suite files that use a host clock or a process/socket deadline. Its ratchet in `scripts/test_evidence.budget` at parent dev `831f94f4` is 3. The budget's own note says the hang bound is the runner's guard, "never an oracle".
  - The gate's `uses_wall_clock()` applied to every processor `tb/` file (`scripts/parent_wallclock_scan.py`, `receipts/parent-wallclock-scan.log`): base 0 files; head 1 file, `tb/desc_store/test_gen_desc_image.py`.
  - First reported in manager comment 5847888234, item 2 (4 > 3); independently reproduced.
- **Impact:**
  - The parent ratchet fails at this pin.
  - The suite's pass/fail becomes dependent on host speed: a loaded host that exceeds 60 s turns a legal case into a `TimeoutExpired` error, reported as FAIL rather than UNKNOWN.
- **Required outcome:** remove the host deadline from the test's CLI invocation and leave hang bounding to the runner's guard, as the manager directed.
- **Verification:**
  - `scripts/parent_wallclock_scan.py` reports no file added by the PR;
  - the tests and mutants still behave as above;
  - the parent consumer bank's wall-clock ratchet passes.

Not a processor finding: the parent gate's DUT-source reader check (manager comment 5847888234, item 3). The test legitimately imports the generator under test by its `hdl/` path, and the manager assigns the disposition to the parent pin-bump patch. I agree.

**S1: SUGGESTION**
- **Lenses:** Docs.
- **Location:** `hdl/aecp/desc/gen_desc_image.py:29-34`, against `:40-41`.
- **Evidence:** The docstring's `fields` example for an ENTITY goes from `descriptor_type` straight to `entity_name` at offset 2, with no `descriptor_index`. The rule added two lines below says the body must start with type and index. The example was already schematic, so this is not a regression.
- **Suggested outcome:** add a `descriptor_index` field (size 2, value 0) to the example.

**S2: SUGGESTION**
- **Lenses:** Docs, Conformance.
- **Location:** `docs/architecture/07_memory_maps.md:239-245`.
- **Evidence:** F07.4's notes list the generator-enforced constraints but not the new body/key agreement. The duplicate and name-binding refusals are not listed there either.
- **Suggested outcome:** optionally add one sentence saying that offsets 0-3 of every packed descriptor equal its index-map key.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `gen_desc_image.py:177-235`, `:433-481`; issue #123 body and assignment; parent F7 and #509 decision; 07 §3.3 / F07.4; IEEE 1722.1 §7.2 descriptor header; parent `avdecc/gen_aemi_image.py:422`; base-vs-head probes | R336-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |
| RTL | CLEAN | diff name list (no HDL); desc_store suite 584/584 at head (reduced `run_suites.sh`, non-pinned Verilator 5.052); hosted jobs success at head; author lint/yosys/suites logs rc 0 | R336-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |
| Robustness | UNCLEAN (F2) | `scripts/probes.py`: 21 cases × {`build()`, CLI} × {base, head}; the test's subprocess deadline under the parent wall-clock detector | R336-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |
| Tests | UNCLEAN (F1, F2) | `tb/desc_store/test_gen_desc_image.py`; Makefile wiring; `run_suites.sh` red on mutant; 11 mutants killed; head tests red against the base generator; parent Rule 12 and wall-clock per-file scans | R336-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |
| Docs | UNCLEAN (F1) | `gen_desc_image.py` docstring; `tb/desc_store/README.md:59-90`; PR body claims; `make check` and CI docs-gates commands; `gen_matrix --check`; `check-links.py`; `git diff --check`; test docstrings vs `tb/pp_top/test_fixture_guards.py` | R336-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |

## Real limits

- **Pinned Verilator unavailable.** The designated pinned Verilator 5.050 path does not exist on this host (`$VALIDATION_STORAGE/372-manager-candidate1/...` is absent), so I could not verify its identity and did not use it. The one focused desc_store suite run used the host's Verilator 5.052. That run is supplementary, not a pinned-tool result.
- **Banks not run.** Per scope, I did not run the full processor `run_suites.sh` bank, `lint_hdl.sh`, `syn/yosys/run.sh`, `nvm_port` figures, or any parent bank. For these I rely on:
  - the unchanged HDL and harness sources;
  - the public author evidence;
  - the hosted jobs (success at the exact head);
  - the manager's banks.
- **Hosted logs.** I could not retrieve the hosted job logs. I checked the check-run conclusions only.
- **Parent gates.** I did not run the parent gates themselves. I called only their pure per-file detectors (`check_py_idiom.scan`, `measure_test_evidence.uses_wall_clock`), fetched read-only from parent dev `831f94f4`, on the processor trees. The parent-wide ratchet totals (4 > 3) come from the manager's comment; my receipts prove the +1 and the 10/9 delta from this head.
- **Parent images.** I did not re-derive the five-config parent image identity; I rely on manager comment 5847782435.
- **Wavedrom gate.** It bootstrapped a local virtual environment inside the disposable scratch clone only.
- **Hardware.** Physical calibration NOT RUN. No hardware was used. Field skips are not hardware proof.

## Clone state after probes

All probes ran on exported copies under the packet's scratch directory. The review clone is untouched (`receipts/clone-integrity.txt`):
- HEAD, index tree and worktree all match eb734969 / 66f2b973;
- index blob IDs and modes equal the HEAD tree;
- worktree blob bytes equal the HEAD tree;
- 0 untracked or ignored entries;
- 0 gitlinks, and no `.gitmodules`.

## Pending manager duties

- Round 2 for F1 and F2 (processor fixes, batched as the manager announced), then re-review at the new head.
- The parent pin-bump patch: the #120 port wiring and the DUT-source reader disposition.
- The consumer bank rerun at the new pin.
- The final current-dev merge candidate: source base 870ff88a onto live dev 831f94f4.
- Hosted/act acceptance.
- Publication of this packet.

## Reproduction

`scripts/run_all.sh <processor-clone> <packet-dir> [<parent-gate-scripts-dir>]` regenerates every receipt except `hosted-check-runs.txt`, which is a read-only API listing. It calls:
- `images.sh`;
- `mutants.py`;
- `probes.py`;
- `legal_models.py`;
- `parent_idiom_scan.py`;
- `parent_wallclock_scan.py`.

The optional third directory holds the parent's `check_py_idiom.py`, `code_quality_scope.py`, `py_idiom.budget`, `measure_test_evidence.py`, `suite_tally.py` and `test_evidence.budget` from kebag-logic/milan-fpga `831f94f4`, under `scripts/`. All receipts are listed in `MANIFEST.sha256`.

R336-1 FINISHED
