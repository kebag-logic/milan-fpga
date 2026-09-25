[A301]

# Round 2 handoff for PR #561

Branch: `443-render-csr`.
Starting head: `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e`.
Base: `0755923d983218ca6ca9db6891a558cbe6425b8d`.
Final head: `5beebb7c7edd908d08be34e52286c9eee441f5b3`.
Commit subject: `test: close render CSR round 2 review findings`.

Assignment: [Round 2 on issue #443](https://github.com/kebag-logic/milan-fpga/issues/443#issuecomment-5826779078).
Reviews: [R320-1](https://github.com/kebag-logic/milan-fpga/pull/561#issuecomment-5826774268) and [R321-1](https://github.com/kebag-logic/milan-fpga/pull/561#issuecomment-5826662478).
Author role: [A301]. Independent delta reviews remain with [R320] and [R321].
This handoff is implementation evidence, not a review verdict.

## Assignment outcomes

| Item | Review references | Change and evidence |
|---|---|---|
| 1 | R320-1 F1; R321-1 F1 | `tb/verilator/csr/sim_main.cpp` drives `i_render_status` explicitly. It grades a zero tie, driven prefill reset value, nonzero selected word, write-ignore behavior, talker and out-of-range rejection, and saturated full-width rails. Unmapped neighbour checks remain at `0x8E0` and `0x8F4`, alongside the existing compatibility-gap checks. `sim_win.cpp` grades four distinct listener words. The missing-decode probe exits 1 at `RENDER_STAT selected listener preserves all fields`, got `0`, expected `0xA5C30216`. |
| 2 | R321-1 F2; R320-1 X2/S1 | `sim_aclk.cpp` grades `STRM_SEL=0x300` at `RENDER-CSR: bit 9 preserves talker rejection`. The four-listener CSR leg also grades nonzero indices with bit 9 set. `render_csr_controls.py` includes the exact formerly surviving window-semantics mutant. A `CSR_SRC` override constructs it in temporary scratch through the normal build recipe. |
| 3 | R321-1 F3; R320-1 X3 | `docs/testing/TESTING.md` lists `render-csr-controls`, names `render_csr_controls.py`, and assigns authors and reviewers of the relevant wiring, decode, taps, bench and campaign changes. The suite README records the new mutant and three additional elaborations. |
| 4 | R320-1 F2; R321-1 F4 | `CHANGELOG.md` has an Unreleased `RENDER_STAT` (`0x8DC`) entry. VERSION remains `0x0002_0060`; the release step owns the minor bump. The register section links the recorded decision and says that the source revision must identify this addition before the bump. |
| 5 | R320-1 F3; R321-1 F5 | The register-groups index has a `0x8DC` row describing `RENDER_STAT`, selected state, global rails, structural zero and the deferred minor bump. |

The evidence inventory now classifies the campaign's CSR source read as mutation construction. No expectation comes from the source text, and no gate budget changed. Its initial refusal is retained in `test-evidence-initial.log`; the corrected gate and self-test pass.

## Suggestions and limits

The CSR bench now covers the upper rail byte. The integration campaign still does not accumulate 256 rail events; full datapath rail width remains supported by static packing review, as stated in the reviews.

The register page now states that the reset value assumes a present stage and the reset listener-0 selection. It also records shared-selector snapshot invalidation, concurrent-reader coordination and restoration of the prior selection.

The PR body names the existing latency-page correction: the shipping TDM8 shape clocks its frame pin. Round 2 does not further change that page.

Round 1 generic synthesis counts, reproduced by both reviewers:

| Module | Base | Implementation head | Delta |
|---|---:|---:|---:|
| `milan_csr` | 70,355 | 70,466 | +111 |
| `milan_datapath` | 1,633,435 | 1,631,783 | -1,652 |

The base and implementation head are the full object IDs above. The decrease is unattributed. These are generic cell counts, with no physical area or timing claim. Round 2 changes no RTL and does not re-run synthesis.

Round 1's complete default sweep is prior public evidence. Round 2 runs the touched `aclk` leg and the requested focused banks. Physical calibration and hardware are not run. Round 1 builder gate 11 remains NOT RUN because its placement report is absent.

## Validation

All required gates returned 0. The CSR variants pass 380, 380, 115, 38 and 380 checks. The full `aclk` leg passes 189 checks. The render suite passes 150 shipping checks, 64 two-listener checks and five existing controls. The render CSR campaign passes 63 clean checks and 32 absent-stage checks; both wrong-fill and bit-9 mutants exit 1 at their required named checks. The standalone missing-decode mutant also exits 1 at its named check. All mutants build successfully; their enclosing campaigns return 0.

The front-end gate actually ran: zero first-party findings and four existing pinned-processor findings, exactly matching the unchanged ratchet. Both documentation modes pass; normal mode covers the inventory-parity check that cannot run without git discovery.

| Command | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/csr` | rc 0 | `csr.log` |
| `make -C tb/verilator/milan_dp aclk` | rc 0 | `aclk.log` |
| `make -C tb/verilator/milan_dp render-csr-controls` | rc 0 | `render-csr-controls.log` |
| `make -C tb/verilator/milan_dp_render` | rc 0 | `milan-dp-render.log` |
| `python3 scripts/docs_check.py` | rc 0 | `docs-check-final.log` |
| `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | rc 0 | `docs-check-no-git.log` |
| `python3 scripts/check_em_dash.py --base 0755923d983218ca6ca9db6891a558cbe6425b8d` | rc 0 | `em-dash.log` |
| `python3 scripts/check_doc_style.py` | rc 0 | `doc-style.log` |
| `python3 scripts/gen_toc.py --check` | rc 0 | `toc.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0 | `toc-anchors.log` |
| `python3 scripts/check_doc_paths.py` | rc 0 | `doc-paths.log` |
| `python3 scripts/xvlog_gate.py --check` | rc 0 | `xvlog.log` |
| `python3 scripts/check_sv_idiom.py` | rc 0 | `sv-idiom.log` |
| `python3 scripts/check_cpp_idiom.py` | rc 0 | `cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | rc 0 | `py-idiom.log` |
| `python3 scripts/measure_test_evidence.py --check` | rc 0 | `test-evidence.log` |
| `git diff --check` | rc 0 | `diff-check.log` |
| `python3 probe_csr_decode.py` | rc 0 | `csr-nodecode.log` |
| `python3 scripts/measure_test_evidence.py --selftest` | rc 0 | `test-evidence-selftest.log` |
| `python3 scripts/check_rtl_source_lists.py` | rc 0 | `rtl-source-lists.log` |
| `git diff c9bbb03cc3d4da9c6ee28996b91addbb081efa7e HEAD --check` | rc 0 | `committed-diff-check.log` |

Run repository-relative commands from the candidate worktree. The standalone `probe_csr_decode.py` command runs from this output directory. The receipt helper prefixes commands with `rtk proxy` and uses `VERILATOR_JOBS=8` for the integration builds.

`validation-head.json` identifies the final tree and proves the committed delta equals the final tested working-tree diff: SHA256 `ce765acb79b734dde2b2899ff7f2fff7ad77001e677ed4a4ba9da9b1515599b4`. Earlier receipts precede only the documented comment positioning and source-reader classification updates. The CSR suite and affected gates were rerun after those edits as applicable. The committed diff and worktree are clean. VERSION and all RTL are unchanged from the round-1 head.

`gates.jsonl` records commands, exits, elapsed seconds, starting head and the working-tree diff hash. Commands run in the foreground without pipelines. `run_gate.py` reproduces each command with raw logs. `probe_csr_decode.py` builds its source and model only in temporary scratch and deletes them after the named failure.

The no-git documentation mode uses `GIT_DIR=/dev/null` for that process. Its receipt explicitly reports `filesystem walk (no git)`; the inventory-parity self-test is inapplicable there. The normal git-mode run covers that parity check.

## Public review evidence inspected

The supplied archives were fetched read-only into a temporary bare repository:

- `2ff0fa7a5970f16127045461af957c1e9ed97614`, R320-1.
- `6d3328d37325d5c889c32c4c436e4ec934a73373`, R321-1.

Only public review files were extracted. Both reports and relevant receipts were read. Manifest mismatches were limited to the four build/control logs named by the archived redaction notes; other manifest entries matched. `review-evidence-read.txt` records the inspected receipts and hashes. The temporary repository and extracted evidence were deleted. No private transcript or other management directory was read.

## Delivery boundary

No push, PR edit, merge, other checkout, delegated session or hardware action was performed. `PR-BODY.md` contains the full fetched current PR body with Round 2 updates and `Closes #443` retained. The local head, body publication, exact-head hosted and local-replica evidence, independent delta reviews, candidate-merge validation and containment remain for the manager's next steps.

The authorized `[A301] REVIEW READY` comment on issue #443 names `5beebb7c7edd908d08be34e52286c9eee441f5b3`. Its exact body is `REVIEW-READY.md`; posting it is the final operation.
