[R524] POSITIVE - exact head 708e5634f28e6e5a19236a9b0a9a543c3622e52d

R524-4 is the internal independent delta review of issue #677 / PR #684 (with the #678 scope), round 4. Head `708e5634f28e6e5a19236a9b0a9a543c3622e52d`, tree `5aab27ec48b9ac84d26e92440b6a55b59cf69298`. The delta since the round-3 head `34475e77` is one docs commit. It changes the five `text` cells of the "Static sizes" table in `sw/firmware/ctrl_nvm/README.md` and nothing else.

At this head the pinned-SDK store gate measures exactly the new figures for every shipped shape, matched by bss. Every other column of each row also matches. R524-3-F1 is RESOLVED. No BLOCKER, MAJOR, MINOR or RESIDUE is open, so all five lenses are CLEAN. This is a source-review verdict, not merge authorization.

## Reconstruction

Sources read, in this order:

1. AGENTS.md, then CONTRIBUTING.md for the review and commit rules.
2. Issue #677:
   - body, with frozen acceptance 1-3;
   - comments: assignment, TAKEN, REVIEW READY, correction, round-3 assignment and round-3 REVIEW READY.
3. Interface authority for the changed text:
   - `sw/firmware/ctrl_nvm/test/nvm_rv32.py:25-26,71-72`: the RV32 flags and the `size -t` totals;
   - `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py:150-155`: the gate line that prints the sizes;
   - `scripts/ci_rv32_sdk.py:24-30`: the SDK pin.
4. The history and diff `34475e77..708e5634`, plus the PR footprint against live dev `910f338d`.
5. Public evidence:
   - the manager evidence tree `review-evidence/677-r1` at `412c0f10`, from its manifest listing only;
   - the exact-head hosted check runs, read-only.

My draft verdict and ledger came before I read any prior review report on this PR (`receipts/draft_verdict_before_prior_findings.txt`, 04:37:29Z). After that I read R524-3 (6030939675) and R525-3 (6030841235) to resolve prior findings. I did not read any round-4 report from another reviewer.

## The delta

- `708e5634` has a single parent, `34475e77`. Its one-line subject is "Record the measured RV32 text sizes of the store after the erased-payload check" and it carries no trailers.
- `git diff 34475e77 708e5634` touches exactly one file, `sw/firmware/ctrl_nvm/README.md`, with 5 lines added and 5 removed (`receipts/delta_34475e77_708e5634.diff`).
  - The only changes are the five `text` cells at `:351-355`: 12,112→12,116, 12,128→12,132, 12,120→12,124, 12,120→12,124 and 12,132→12,136.
  - Every other cell, the table preamble (`:337-347`) and the surrounding prose are byte-identical.
- No other file in the repository quotes these figures. I searched the tree for the old and new values. Every hit outside this table is unrelated: LUT and resource counts, SVG colour codes, and capture file sizes.
- Against live dev `910f338d`, the PR still changes 30 paths, all under `sw/firmware/`.

## Executed evidence at 708e5634

| Command | Result | Receipt |
|---|---|---|
| Pinned SDK: archive `riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz` extracted to scratch | sha256 `d42680e9…b78f`, equal to `ARCHIVE_SHA256` in `scripts/ci_rv32_sdk.py:25`; `riscv32-linux-gcc` reports GCC 14.3.0 | this table |
| `MILAN_RV32_CC=<pinned riscv32-linux-gcc> python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | rc 0; 5 shapes, 435 tests ("saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests"); all five RV32 builds pass; largest static frame 128 bytes per shape | `receipts/test_ctrl_nvm_rv32.log`, `.rc` |
| `scripts/match_sizes.py` (log against `README.md`, matched by bss; compares clock, stage, payload, chunk, store, clock counters, bss and text) | ALL MATCH, rc 0. The measured text values are 12116 (bss 3160), 12132 (4048), 12124 (5452), 12124 (8012) and 12136 (14408), which are the new cells in table order | `receipts/match_sizes.txt` |
| Negative control: the same script against the `34475e77` README | MISMATCH on all five text cells (table 4 bytes low), rc 1, so the script can fail | `receipts/match_sizes_parent_negative_control.txt` |
| `scripts/probe_drop_erased_check.sh`: removes only the 3-line `loaded` bound at `nvm_klj2.c:298-300`, reruns the gate, then restores | text drops back to 12112 / 12128 / 12120 / 12120 / 12132, the old cells exactly. `NvmCodec.codec_erased_loaded_prefix` fails with an ASan heap-buffer-overflow; suite rc 1; restored clean | `receipts/probe_drop_erased_check.log` |
| `docs_check.py`; `gen_toc.py --check` and `--verify-anchors`; `check_em_dash.py --base 34475e77` and `--base 910f338d`, all with the pinned Markdown venv (requirements sha256 `40cdefe0…2817`); `git diff --check` against `34475e77` and `910f338d` | all rc 0, each the gate's own exit status | `receipts/docs_gates.log` |
| Clone integrity after the probes | HEAD `708e5634`; `git write-tree` = `5aab27ec…`; the index (mode, blob, path) digest equals the HEAD tree digest; no untracked or ignored files; all four gitlinks unchanged | `receipts/clone_integrity_final.txt`, `receipts/pycache_removed.txt` |

The probe shows that the 4 bytes per shape are exactly the cost of this PR's erased-payload check. The new column is therefore the measurement of the code this PR ships, and not a figure carried over from a drifted base.

**Hosted contexts at the exact head, read-only** (snapshot taken at 04:39Z, `receipts/hosted_checks_708e5634.tsv`):

- Executed and successful (11): `firmware-unit`, `docs-check-no-git`, `verilator-lint`, Yosys shards 0-3, `bdd-conformance`, `wire-accountability`, `changes` and `full-ci-gate`.
- Still in progress (8): `docs-check`, `elaborate`, `yosys-elaboration` and Verilator shards 0-4.
- Skipped: `Physical gPTP`. A skipped context is not executed evidence or hardware proof.

The manager owns hosted and act acceptance.

## Findings

No new finding at any severity.

### Prior public findings at this head

- **R524-3-F1 (MINOR, Docs): RESOLVED.** The text column at `sw/firmware/ctrl_nvm/README.md:351-355` now reads 12,116 / 12,132 / 12,124 / 12,124 / 12,136, and the gate measures exactly that at this head (`receipts/match_sizes.txt`). The verification route F1 named was followed as written.
- **R524-3-S1 (SUGGESTION, Tests): RETAINED, routed to #495.** #495 is open: "[Residue] Review leftovers: one checklist instead of one issue per pull request". The gate still prints the sizes without comparing them with the table (`test_ctrl_nvm.py:150-155`). The suggestion is optional and does not affect coverage.
- **R525-3-S1 (SUGGESTION, Conformance, RTL): RETAINED, unaffected.** `rv32_include/assert.h` and `ctrl_build.py` are not in the delta.
- **R524-1-F1 / R525-1-F1 (MINOR, Conformance, Docs) and R524-1-F2 / R525-1-F2 (MINOR, Tests, Docs): RESOLVED, retained.** The delta touches neither the PR body authority bullet nor `sw/firmware/gtest/README.md`.

## Lens results

[R524] PASS Conformance - `receipts/delta_34475e77_708e5634.diff`, `sw/firmware/ctrl_nvm/nvm_klj2.c:298-300`, `receipts/probe_drop_erased_check.log` - checked:
- The delta changes no firmware behaviour and no clause claim, so #677 acceptance 1-3 and the #678 scope stand as R524-3 covered them at `34475e77`.
- The code R524-3 judged is byte-identical here.
- The probe re-confirms that the erased branch's `loaded` bound is present and caught by the ASan prefix test.

[R524] PASS RTL - `receipts/delta_34475e77_708e5634.diff`, `git diff --name-only 910f338d 708e5634` (30 paths, all `sw/firmware/`) - checked:
- No HDL, testbench, synthesis, build-flag or interface artifact is in the delta.
- R524-3's RTL coverage at `34475e77` stands for unchanged scope.

[R524] PASS Robustness - `receipts/delta_34475e77_708e5634.diff`, `receipts/probe_drop_erased_check.log` - checked:
- No code path changed.
- The truncated-prefix failure path is still guarded and still caught at this head.
- R524-3's Robustness coverage at `34475e77` stands.

[R524] PASS Tests - `receipts/test_ctrl_nvm_rv32.log` (rc 0, 435 tests, 5 RV32 builds), `scripts/match_sizes.py` with `receipts/match_sizes.txt` and the parent negative control, `receipts/probe_drop_erased_check.log` - checked:
- The verification F1 required, run at this head.
- That the comparison can fail: it fails on the parent README.
- That the ASan prefix test still fails for the restored defect.
- No test file changed. R524-3's campaign coverage at `34475e77` stands for unchanged scope.

[R524] PASS Docs - `sw/firmware/ctrl_nvm/README.md:337-355`, `receipts/match_sizes.txt`, `sw/firmware/ctrl_nvm/test/nvm_rv32.py:25-26`, `receipts/docs_gates.log` - checked:
- All eight shared columns of all five rows against the head's measurement.
- The preamble claims (RV32I with ILP32 at `-Os`, stack protector disabled, 128-byte largest frame) against `nvm_rv32.py` flags and the gate log.
- That no other document quotes the figures.
- That the docs gates pass.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta diff (docs only). Earlier coverage: `rv32_include/assert.h` (C11 7.2), `nvm_klj2.c:296-300`, `adp.c`/`adp.h`, merge fidelity. Re-checked here: the `loaded`-bound probe | R524-3, with nothing in scope changed since; confirmed by R524-4 | 34475e774dfe1c92c81fa51293668e64dc95fa85 (ancestor, scope untouched) and 708e5634f28e6e5a19236a9b0a9a543c3622e52d |
| RTL | CLEAN | PR vs live dev (`sw/firmware/` only), `ctrl_build.py:42-46`, `fw_rv32.py:24-42`; the delta has no RTL or build artifact | R524-3, with nothing in scope changed since | 34475e774dfe1c92c81fa51293668e64dc95fa85 (ancestor, scope untouched) |
| Robustness | CLEAN | Witnesses W1-W10, ASan prefix test, erased-payload and re-entry defects. Re-checked here: the truncated-prefix probe | R524-3, with nothing in scope changed since; confirmed by R524-4 | 34475e774dfe1c92c81fa51293668e64dc95fa85 (ancestor, scope untouched) and 708e5634f28e6e5a19236a9b0a9a543c3622e52d |
| Tests | CLEAN | At R524-3: ctrl 79/79, NVM 109/109, RV32 self-test 17, coverage 14 files plus self-test 28/28, tally 18/18. At R524-4: store gate rc 0 (435 tests, 5 RV32 builds), size match plus negative control, probe | R524-3 for the campaigns (no test file changed since); R524-4 for the store gate | 34475e774dfe1c92c81fa51293668e64dc95fa85 (ancestor, scope untouched) and 708e5634f28e6e5a19236a9b0a9a543c3622e52d |
| Docs | CLEAN | `sw/firmware/ctrl_nvm/README.md:337-355` against the measurement, docs gates. The other docs R524-3 found correct (`gtest/README.md`, `ctrl/README.md`, PR body authority bullet) are untouched by the delta | R524-4 | 708e5634f28e6e5a19236a9b0a9a543c3622e52d |

Open: none at BLOCKER, MAJOR, MINOR or RESIDUE. The SUGGESTIONs R524-3-S1 (routed to #495) and R525-3-S1 do not affect coverage.

## Real limits

- **Not re-run in this round:** the ctrl and NVM mutant campaigns, the coverage ratchet, the RV32 self-test and the tally self-test. The delta changes no code or test file, and R524-3 ran them at the ancestor `34475e77`. The store gate and the size comparison were re-run here.
- **Not run:** the lwSRP arm (the private checkout is absent), the builder bank, `scripts/run_all_suites.sh`, `syn/yosys/run.sh`, act, Docker, physical calibration and hardware. Physical calibration was NOT RUN. Field skips and skipped hosted contexts are not hardware proof.
- **The sizes are object sizes, not a linked image.** They come from `size -t` over the freestanding RV32I objects, as the README itself states.
- **The probe ran in this clone.** It edited `nvm_klj2.c` temporarily and restored it with `git checkout`. My runs created 24 ignored `__pycache__` files, all timestamped at the first gate run, and I listed and then removed them. The final integrity receipt shows no untracked or ignored file and index = HEAD.
- **Hosted results are from a snapshot.** Eight hosted contexts were still in progress when I read them.

## Pending manager duties

- Accept the exact-head hosted contexts once the 8 in-progress runs finish, and run the trusted-dev act replica for PR #684.
- Build and validate the final current-dev candidate at the merge turn (source base `6714181d0c8a16e2983f85b724f4d688f5111835`, live dev `910f338dbd050f4efd2d96991ddcf928a583d55f`).
- Record the long local gates still owed under CONTRIBUTING (`run_all_suites.sh`, `syn/yosys/run.sh`).
- Note that physical calibration was NOT RUN.
- Carry R524-3-S1 to #495.
- Merge requires the second independent positive and explicit maintainer authorization.

R524-4 FINISHED
