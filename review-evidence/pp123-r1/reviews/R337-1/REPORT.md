[R337] POSITIVE - exact head eb734969154d5a75ff84b2779ff6088a2f4311a5

# R337-1 external independent review: processor issue #123 / PR #124

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| Pull request / issue | #124 / #123 |
| Exact head | `eb734969154d5a75ff84b2779ff6088a2f4311a5`, tree `66f2b9733acc16a2e4588178e4582d62ce7f84fb` |
| Base | `870ff88ad35bbd532244e4c7e6d7661b9f6e1366` (one commit, parent = base) |
| Round | R337-1, first review of this PR |
| Verdict | POSITIVE. No open MINOR, MAJOR or BLOCKER finding. One SUGGESTION. |

## 1. Reconstruction

- **Repository conventions.** There is no `AGENTS.md` or `CONTRIBUTING.md` at this head. Conventions were taken from `README.md` ("Building and checking"), `docs/README.md` (author conventions and the `make check` scope), the `Makefile`, `scripts/run_suites.sh` and `.github/workflows/hdl.yml`.
- **Scope authority.** The scope comes from the issue #123 body (F7 of the parent ownership matrix), the assignment comment `issuecomment-5847636202` (acceptance items 1-5 and the gates), and the decision in kebag-logic/milan-fpga#509. That decision is recorded in `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`, which I read at PR #568 head `04c9802d`. Its row L2 says: "Packer accepts disagreement between row metadata and wire type/index. Body/key consistency needs F7". F7 is a processor follow-up, separate from PP60.
- **Issue #60.** The body was last updated 2026-09-18, before this work. Its acceptance targets the L1-L8 model lint and REQ-MDL rows. This PR touches no file named there except the packer, and it does not claim or close #60.
- **Diff.** `git diff 870ff88a..eb734969` changes four files:
  - `hdl/aecp/desc/gen_desc_image.py`: +10 lines, a docstring rule and the check.
  - `tb/desc_store/Makefile`: `run` now depends on the new `generator-check` target.
  - `tb/desc_store/README.md`: a new section.
  - `tb/desc_store/test_gen_desc_image.py`: new file.

  The raw patch is in `receipts/diff-base-head.patch` and the scope listing in `receipts/scope.txt`.
- **Public evidence.** I read kebag-logic/milan-fpga `8a640700`, `review-evidence/pp123-r1`, which contains the author mutant, image digests, suite and gate logs. I also read the manager's parent five-config image comment `issuecomment-5847782435`.
- **Prior public findings.** After my own pass, I checked the PR for prior review findings: 0 reviews, 0 review comments, and no finding in the issue or PR comments. None needs resolving or retaining.

## 2. What the change does, and how I verified it

`_grouped_descriptors` (`hdl/aecp/desc/gen_desc_image.py:215-221`) now decodes body bytes 0-1 and 2-3 big-endian. It runs after `descriptor_bytes` has assembled either input form and applied `pad_to` and the 4-byte minimum. It compares them with the normalized key (`_type_code(type)`, `_u(index)`) and raises `ImageError("cfg C directory key type 0xTTTT index I disagrees with body type 0xBBBB index J")`. It runs for every descriptor before name handling, duplicate detection, density, name binding and run splitting. `main()` catches `ImageError` before opening any output, so the CLI returns 1 and writes nothing.

### 2.1 Reviewer probe matrix (`scripts/probe_bodykey.py`)

The matrix has 33 probes, each run through `build()` and the CLI. For a refusal, the CLI must return 1, write no image and no map, and print exactly the `build()` message on stderr. For an accept, the CLI image and map must equal `build()`'s.

| Group | Probes | Head | Base |
|---|---|---|---|
| Legal pair, both forms | `legal_bytes`, `legal_fields` | accept | accept |
| Type-only / index-only mismatch, both forms | 4 | refused, exact message (cfg, key, body) | all 4 accepted |
| Endianness; high byte only / low byte only | 4 | refused | accepted |
| Other field shapes: one u32 field; split 1+0+1-byte fields; a `string` field; an all-default field | 5 (1 legal) | legal accepted, 4 refused | all accepted |
| `pad_to`: short body completed by zeros (legal); empty body / no fields with a non-zero key; type correct but index padded to 0 | 4 (1 legal) | legal accepted, 3 refused | all accepted |
| Grouped descriptors: bad middle member; mixed-length second run; second configuration; swapped pair; two types exchanging bodies | 5 | refused, naming the right cfg/type/index | all accepted |
| Name handling: named group legal; named group with bad index; `name_index: -1`; ENTITY legal; ENTITY bad type | 5 (2 legal) | legal accepted, 3 refused | all accepted |
| Key spellings: hex string / decimal string; type key above u16; negative index | 4 (1 legal) | legal accepted; the rest named refusals | the u16-overflow key crashed with `OverflowError`; negative index got the density refusal |

Result: `SUMMARY head: 33 probes, 33 as expected`; `SUMMARY base: 33 probes, 33 as expected`, and the base expectation for every mismatch is "packs unchanged". The receipts are `receipts/probes-head.jsonl` and `receipts/probes-base.jsonl`.

No input path bypasses the check: `pad_to`, `name_index`, grouped and multi-run descriptors, multiple configurations and the CLI are all covered. The only way to "pass" with zero padding is a body whose padded bytes really equal the key, which is a correct accept. As a side effect, a type key above u16 is now a named refusal where the base crashed with a traceback.

### 2.2 Tests, mutants and entry point

- **New tests at head.** `test_gen_desc_image.py` passes: 6 tests covering 24 subtests (`receipts/new-tests-head.log`). Against the **base** generator, the same file fails 16 subtests: every type and index refusal in both forms, while the legal tests pass (`receipts/new-tests-vs-base-generator.log`). The tests therefore discriminate.
- **Mutants** (`scripts/mutants.py`, `receipts/mutants.jsonl`). Each mutant is applied to a copy of `hdl/aecp/desc` and `tb/desc_store`. The author's mutant removes the check; it fails 16 cases in 4 tests, and the legal tests still pass. I wrote 12 more mutants:
  - compare type only, or index only;
  - compare low bytes only;
  - decode little-endian;
  - shift the offsets by one;
  - check the `bytes` form only, or the `fields` form only;
  - check the first descriptor only;
  - drop cfg from the message;
  - report body values as the key;
  - raise `ValueError` instead of `ImageError`;
  - check named-type keys only.

  **All 13 mutants are killed** by the test file and by `make generator-check` (rc 2). The unmutated control passes (tests rc 0, make rc 0).
- **Entry point** (`scripts/entry_point.sh`, `receipts/entry-point.log`). I built a reduced copy of the head tree: every other suite directory was removed, and the shared `tb/common` harness was kept. The pinned Verilator 5.050 was used.

  | Copy | `make` in `tb/desc_store` | `scripts/run_suites.sh` |
  |---|---|---|
  | Unmodified control | rc 0: tests OK, then the RTL suite `584 checks: 584 PASS, 0 FAIL` | rc 0: `PASS desc_store` |
  | Check removed | rc 2: stops at `generator-check` with `FAILED (failures=16)` before Verilator runs | rc 1: `FAIL desc_store` |

  `scripts/run_suites.sh` is what the hosted `suites` job runs. The hosted `suites` job at this head shows `PASS desc_store (584 checks...)` and `suites: 1014722 checks total, 0 failing` on both the push and pull_request runs (`receipts/hosted-suites-excerpt.txt`).

### 2.3 No legal image changes (`scripts/image_digests.sh`)

I rebuilt every generated image from exports of the base and head trees:
- the `tb/desc_store` image and map from `example_milan_8.json`;
- `ltn_rom.hex`;
- `ucode.hex`, which is what the ucpu, pp_top and Yosys paths generate.

The base and head digests are identical (`receipts/images-{base,head}.sha256`, `receipts/images-compare.txt`). The image is `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c`, which matches the author's published digest. `ltn_rom.hex` is `23cc67ee…` and `ucode.hex` is `23605682…`.

I did not re-derive parent-side identity for the five parent configs. The manager's comment `issuecomment-5847782435` reports base = PR for all five AEM images and all 50 builder outputs.

### 2.4 Nothing else changes

No `.sv`/`.svh`/`.v`, `syn/`, `.github/`, `scripts/`, `docs/` or `hdl/README.md` path changed (`receipts/scope.txt`). There is no port or parameter change: `check-integrator-params.py` reports 24/24/24 OK. The store RTL takes lengths from the index map and does not read descriptor interiors, so the packer is the right, and only, place for this generic check. That is consistent with the #509 decision.

### 2.5 Gates (`receipts/gates.log`)

These ran in a scratch clone at the exact head, all rc 0:
- `make check`: diagram lint, wavedrom, links (915), REQ matrix, module matrix (92 rows, 0 untested), params, stale;
- `scripts/check-links.py`, `scripts/check-matrix.py`, `scripts/check-integrator-params.py`, `scripts/gen_matrix.py --check`, `scripts/render-wavedrom.py --check`, `make stale`;
- `git diff --check 870ff88a eb734969`;
- `scripts/lint_hdl.sh` with pinned Verilator 5.050, every module `LINT OK`.

I did not run the full 33-suite `run_suites.sh`, `syn/yosys/run.sh` or the 46-build `nvm_port` figure check (see Limits). The hosted `suites`, `portability` (Yosys) and `docs-gates` jobs **executed and succeeded** at this exact head for both the push and pull_request events (`receipts/hosted-check-runs.tsv`). None of them was skipped.

## 3. Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R337-1-S1 | SUGGESTION | Docs | `hdl/aecp/desc/gen_desc_image.py:29-31` and new text at `:40-41` | The PR adds "The assembled body must start with its directory key: a big-endian u16 type and u16 index" directly under an input sketch whose ENTITY `fields` go from `descriptor_type` (2 B) straight to `entity_name`. Taken literally, bytes 2-3 are the first name bytes, so the new check refuses the sketch. The sketch was already not packable at base, because of the ENTITY name-offset rule, so this is not a regression. | A reader copying the sketch meets the new refusal first. This is cosmetic. | Optional: add `{"name": "descriptor_index", "size": 2, "value": 0}` after `descriptor_type` in the sketch. | Reading the docstring. Non-blocking, and it does not affect the verdict. |

There are no MINOR, MAJOR or BLOCKER findings.

## 4. Lens assessments

- **Conformance.** IEEE 1722.1-2021 §7.2 makes every descriptor start with `descriptor_type` and `descriptor_index` (u16, big-endian). The store serves the located body verbatim to READ_DESCRIPTOR, so a body that disagrees with its directory key would put a response on the wire whose type or index differs from the request's. The check enforces exactly the F7 row and the assignment's item 1: both forms are covered, and the `ImageError` names cfg, key and body. Ownership follows #509: a generic packed-image check, in the processor. Issue #60's acceptance is untouched.
- **RTL.** No RTL, port, parameter, `syn/` or workflow change. `lint_hdl.sh` passes. The hosted Yosys `portability` job and the full suite sweep passed at the head. The desc_store RTL suite reports an unchanged 584/584 over byte-identical `image.bin`.
- **Robustness.** Of 33 adversarial probes, none bypasses the check, and all refusals are atomic at the CLI (rc 1, no image or map). The check runs after `pad_to` and the length floor, so it never indexes a short body. Key values outside u16, or negative, can never match and are now named refusals, where the base crashed with an `OverflowError` traceback. The diagnostic order changes only for inputs that were already invalid. No legal image changes.
- **Tests.** The tests use both input forms, both entry points (`build()` and the CLI) and four key spellings. The type and index mismatches are independent. The legal controls also assert exact bytes. The tests fail against the base generator. All 13 mutants are killed, including partial, endianness, offset, single-form, message and exception mutants. The entry point is proven red, by `make` in `tb/desc_store` and by `scripts/run_suites.sh`, with the check removed, and green unmodified. CI runs that path.
- **Docs.** The `tb/desc_store/README.md:59-90` section matches the observed behaviour: 6 tests / 24 cases, a legal pass of 8, 16 refusal failures and make exit 2 under the mutant. It also accurately describes the high-byte-only mutation and the run_suites gating. The generator docstring states the rule, and the PR body's claims match my receipts. `make check` and the CI docs gates pass. The only docs item is SUGGESTION S1.

## 5. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #123 body and assignment `5847636202`; `PP_DESCRIPTOR_OWNERSHIP.md` L2 and F7 (at `04c9802d`); issue #60 acceptance; `gen_desc_image.py:40-41,202-235`; `probes-head.jsonl` | R337-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |
| RTL | CLEAN | `scope.txt` (no HDL, syn, workflow or parameter paths); `gates.log` (`lint_hdl.sh`, params); `entry-control-make.log` (584/584); `hosted-check-runs.tsv` (portability, suites) | R337-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |
| Robustness | CLEAN | `probe_bodykey.py` with `probes-{head,base}.jsonl` (33 probes: pad_to, names, groups, runs, configs, key spellings, CLI atomicity); `images-{base,head}.sha256` | R337-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |
| Tests | CLEAN | `test_gen_desc_image.py`; `new-tests-head.log`; `new-tests-vs-base-generator.log`; `mutants.jsonl` (13 mutants and a control); `entry-point.log` with the make and run_suites logs for control and mutant; `hosted-suites-excerpt.txt` | R337-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |
| Docs | CLEAN (S1 open, non-blocking) | `tb/desc_store/README.md:59-90`; `gen_desc_image.py` docstring; PR #124 body; `gates.log` (`make check`, links, wavedrom, stale, matrix, params, `git diff --check`) | R337-1 | eb734969154d5a75ff84b2779ff6088a2f4311a5 |

## 6. Real limits

- **Full banks not run.** Under this assignment's constraints I did not run the full 33-suite `scripts/run_suites.sh`, `syn/yosys/run.sh` or the `nvm_port` 46-build figure check. I ran `run_suites.sh` over a reduced tree (desc_store only, control and mutant), and all docs, matrix and lint gates locally. For the rest I rely on the hosted executed jobs at this head and on the manager's and author's public logs.
- **Parent five-config identity not re-derived.** I rely on the manager's comment `5847782435`. The donor bank and parent consumer bank were not observed by me.
- **Verilator substitution.** The Verilator path named in the brief (`$VALIDATION_STORAGE/372-manager-candidate1/...`) does not exist on this host. I used the head-specific pinned wrapper `$VALIDATION_STORAGE/pp123-manager-eb734969/pinned-tool-bin/verilator` after checking its identity: `Verilator 5.050 2026-07-01 rev v5.050`, with wrapper and binary sha256 in `receipts/environment.txt`.
- **One over-limit build.** One early entry-point attempt, discarded because the reduced tree lacked `tb/common`, ran the Makefile's `-j 0` Verilator build, which used 16 compile jobs. That exceeded the 8-job limit. The retained run caps the build at `-j 8`. That cap is the only other edit in the reduced copies, and it is disclosed in the script.
- **Local tool versions.** I used local Python 3.14.7, GNU Make 4.4.1 and g++ 16.2.1, which differ from the hosted runner images.
- **Hardware.** Physical calibration was NOT RUN. No hardware proof is claimed, and field skips are not hardware proof.
- **Clone integrity.** Nothing was modified in the review clone. After the probes I verified the HEAD, the tree, `git write-tree` = HEAD tree, an empty `status --porcelain --ignored`, worktree = index = HEAD for content and modes, and the `ls-files -s` digest (`receipts/clone-integrity.txt`). This repository has no submodules or gitlinks (no `.gitmodules`, no mode-160000 entries).

## 7. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn: source base `870ff88a`, live dev `831f94f4`. That candidate is distinct from this source validation.
- Record the donor bank and parent consumer bank results at `eb734969`. This covers issue #123 acceptance item 5 at the new pin.
- Own hosted and act acceptance.
- Obtain the second independent review (R336-1) and the full completion bar before merging.
- Dispose of SUGGESTION R337-1-S1 at your discretion.

R337-1 FINISHED
