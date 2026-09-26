[R250] POSITIVE - exact head a07a75de78b19369e228d4ab8403a52f7435fd64

# R250-6: external delta review of issue #400 / PR #566, round 5

- Exact head `a07a75de78b19369e228d4ab8403a52f7435fd64`, tree `0c8c1de484f5b305f40bfbcb171f61a16e38dd26`. Git reports this tree for both the index and the worktree after cleanup.
- Delta judged: `c6c65e80..a07a75de`. This is the clean merge `6d181922` of dev `220cb5a3` (it brings in #562, #561, #564/#559 and #553), plus one commit, `a07a75de`. That commit re-measures the saved-state capture on the composed product firmware.
- Assignment: [issue 400 comment 5838671391](https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5838671391). It answers the composition review R249-4 F1 BLOCKER.
- The source reviews at `c6c65e80` (R250-4 and R249-3) stand. They are not repeated here.
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- **No BLOCKER, MAJOR or MINOR finding is open.** There is one new SUGGESTION (S1), and two earlier SUGGESTIONs are carried.
- R249-4 F1 is **CLOSED** at this head.

## Reconstruction

Sources were read in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.
3. Issue #400: the body, decision 5770922734, and the round-4 and round-5 assignments (5836794096, 5838671391). Also the [A323] TAKEN and REVIEW READY posts.
4. The authorities: the tb/verilator/nvm_capture_cpu README, `scripts/check_nvm_capture.py`, and `.github/workflows/docs.yml`.
5. The history and diff of `6d181922` and `a07a75de`.

I made my own pass over the diff and receipted the reproduction before I read any prior findings on this PR. The prior findings are R249-4 at `09419d88` and the R250-4/R249-3 finding lines. The author's round directories in the evidence tree were not read. I did not read any other reviewer's report for this round.

## Assigned verifications

### (1) Merge integrity

- `git show --remerge-diff 6d181922` is **empty** (receipt `receipts/remerge-diff-6d181922.txt`, one line with the commit id).
- `git merge-tree --write-tree c6c65e80 220cb5a3` independently gives `87ed44d7...`, which equals `6d181922^{tree}`. The merge base is `864b36f5`. See `receipts/merge-verification.txt`.
- Seven files changed on both sides:
  - `docs/reference/REGISTER_MAP.md`
  - `hdl/common/csr/milan_csr.sv`, `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/milan_datapath.sv`
  - `tb/verilator/csr/sim_main.cpp` and `sim_win.cpp`
  - `tb/verilator/milan_dp/README.md`

  None of their hunks overlap. For example, `KL_pp_shadow.sv` has PR hunks at 187/1053 and dev hunks at 635/637. Composition is exercised by the suites in section (4).
- The gitlinks are identical across `864b36f5`, `c6c65e80`, `220cb5a3` and `a07a75de`: gptp `e5dcea6e` and pp `990f9652`.
- `a07a75de` changes exactly two files: `measurements.json` and `SAVED_STATE_SNAPSHOT_OWNERSHIP.md`. `scripts/check_nvm_capture.py`, every harness `.py`/`.cpp` file, the workflows and `ci_events.py` are unchanged against dev, so the gate was not weakened. The firmware is not reverted: `milan_baremetal.c` is `0bf43cd4...` and keeps the #400 `configure_fabric()` change.

### (2) Re-measurement follows the README, reproduced independently

- Receipt audit (`scripts/receipt_audit.py`, `receipts/receipt-audit.txt`), all checked against the receipt:
  - The receipt has six arms: both contract shapes at 50 MHz, ON and OFF, plus the labelled 100 MHz 8x8 ON/OFF.
  - Every arm has 16 captures, indices 0-15, with ok=1, mismatches=0 and open=0.
  - ON arms have positive request, response and read counters. OFF arms have all three at zero.
  - Every arm's phase is `aligned rising edges`.
  - I recomputed each minimum, maximum and margin, and the `maxima` block, from the rows. They agree with the receipt.
  - `product_firmware_sha256` (`measurements.json:17`) equals the head's `milan_baremetal.c`, `0bf43cd4...`.
  - Tool identity: simulator Verilator 5.052; LiteX, migen, litedram, litespi and VexiiRiscv revisions as in the receipt; cached CPU netlist sha256 `c208df0b...`.
- Reproduction (`scripts/reproduce_capture.sh`):
  - Inputs: the pinned LiteX tree at the receipt revisions, the pinned RV32 SDK (gcc 14.3.0) and Verilator 5.052, which is the receipt's simulator.
  - Environment: networking disabled (`unshare -Urn`), `PYTHONHASHSEED=0`, offline coursier/sbt, and external build directories.
  - Arms run, each with 16 captures: **8x8 at 50 MHz, traffic ON and OFF**, plus the 100 MHz 8x8 ON arm.
- Comparison with the receipt (`scripts/compare_reproduction.py`, `receipts/reproduction-compare.txt`, `receipts/rows-*.log`, `receipts/measurement-*.json`):
  - **All 48 reproduced rows are identical to the receipt, field by field.**
  - The instrumented firmware and BIOS sha256 values also match: `d82f1d40...`/`f8aad0a0...` for ON and `71aef8c3...`/`4c74bd59...` for OFF.
  - 8x8 at 50 MHz: ON is 24.29290 to **24.30246 ms**; OFF is 24.25794 to 24.26154 ms.
  - The worst case over both arms is 24.30246 ms. It is at or below 24.5 ms with 0.19754 ms spare, and the floor margin is 2.0163x. The STOP condition was not triggered.
- The 100 MHz rows are byte-identical to dev's pre-refresh receipt. This looked like a possible copy-forward, so I re-ran that arm. It reproduces exactly, so the harness is deterministic at 100/100 and those rows are genuinely unchanged.
- The 1x1 arms and the 100 MHz OFF arm were not re-run. They are covered by the receipt audit and by the determinism shown above.

### (3) Section 18 and UNRESOLVED 6 figures

- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` was checked against the recomputed values:
  - Lines 1573-1575: 24.30246 ms, 2.0163x, 0.19754 ms.
  - Lines 1583-1592: the table rows, each arm margin, and the 1x1 maximum of 6.60642 ms / 7.4170x.
  - Lines 1613-1618: ON minus OFF is 0.04092 ms (0.169%) at 8x8 and 0.01785 ms (0.271%) at 1x1. At 100 MHz, ON is 0.78591 ms faster.
  - Lines 1740-1748: UNRESOLVED 6 (24.30246 / 2.0163x / 6.60642 / 19.79024).

  All of these agree with the recomputation.
- The old sentence "Product firmware, RTL and builder census lists remain unchanged" that R249-4 cited is gone.
- A repository-wide search for `24.30454`, `24.305`, `2.0161`, `0.19546`, `0.04300`, `0.177%`, `24.29322`, `24.25516`, `6.59822` and the old digests `7cdc5e68`, `368eb10b` and `040b8450` finds **no match**. There is no stale 24.305 claim.

### (4) Gates at the exact head

- **Capture gate** (`receipts/suites/capture_*.log`):
  - `check_nvm_capture.py` passes (PASS), and its named controls run first.
  - The four `--mutation` runs (bytes, records, clock and ignore-off-timing) each exit nonzero with the expected FAIL line.
- **Disposable probes** (`scripts/capture_gate_probes.sh`, `receipts/capture-gate-probes.txt`):
  - Dev's pre-refresh receipt against this head's firmware fails with `product firmware changed`. This reproduces R249-4 F1.
  - The refreshed receipt passes.
  - A one-line firmware edit fails.
  - A harness edit fails.
  - An OFF row set one tick over 24.5 ms fails.
  - After restoring, the tree passes again with zero changed entries.
- **Full docs-check step set** (`scripts/docs_check_steps.sh`, `receipts/docs-check/summary.txt`): **75 of 75 commands exit 0**.
  - This covers every gate command of the `docs-check` job, including `test_builder.py --require-rv32` against the pinned SDK and all commands of the steps after the capture gate, plus the `wire-accountability` job's command.
  - The only exception is the local act-runner self-test, which is reserved to the manager.
  - Not run locally:
    - The HDL-reference build, because the locked parser wheel is not installed here.
    - The no-git job.
  - Hosted evidence covers those. At the exact head, `docs-check` job 108249399678 executed all 51 steps with success, including steps 30-51 after the capture gate and step 44, the act contract gate. `docs-check-no-git` and `wire-accountability` also succeeded (`receipts/hosted-docs-check-steps.txt`, `receipts/hosted-check-runs.txt`).
- **Suites** (`scripts/run_suites.sh`, `receipts/suites/`):
  - `test_declarations.py`: 0.
  - `test_nvm_firmware.py --self-test`: 0, with 5 shapes, and every planted defect reddened.
  - `make -C tb/verilator/csr`: 0. The legs ran 400/400/121/44/400 checks plus the reset-bits leg (400 checks). The composed checks for AAF/MAAP neutral reset and RENDER_STAT executed.
  - `make -C tb/verilator/pp_shadow`: 0, with three legs of 402 checks each.
  - `make -C tb/verilator/nvm_cosim`: 0, with 465/465 checks and 39/39 mutants killed.

## Findings

### S1 - SUGGESTION - Tests, Robustness, Docs - `scripts/check_nvm_capture.py:62-63` with `sw/litex/boot_policy.py:55-63` and `sw/firmware/milan_baremetal/milan_baremetal.c:1376-1385`

**Evidence.**
- The capture gate pins only the bytes of `milan_baremetal.c`.
- The words that `configure_fabric()` writes come from `boot_policy.fabric_constants()` as compile-time constants. This PR adds or moves `MILAN_MAC_CTRL_SET`, `MILAN_TCAM_CTRL_BOOT`, `MILAN_AAF_CTRL_BOOT` and `MILAN_MAAP_CTRL_BOOT`. The capture driver calls `milan_init()` (and so `configure_fabric()`, `:1449`) before timing, so these words shape the measured firmware, including its receive posture during the traffic-ON arm.
- Probe (`receipts/capture-gate-boot-policy-probe.txt`): I set `MILAN_TCAM_CTRL_BOOT` and `MILAN_MAC_CTRL_SET` to 0 in a scratch copy, and the gate still PASSES.
- The docs claim more than this. "Firmware edits also require new measurements" (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1634`, `:1752`) and "The product firmware hash also prevents carrying timing across edits" (`nvm_capture_cpu/README.md:151`) read more broadly than the gate's coverage.

**Why SUGGESTION, not MINOR.**
- The same gap already exists on dev for `MILAN_SR_VID`, `MILAN_LWSRP_CTRL_RESET` and `MILAN_CRF_TX_CTRL_BOOT`, so it is a limit of the #559 gate's design. This delta did not introduce it.
- The measurement at this head is reproduced bit-exactly.
- The assignment froze scope ("Change nothing else").

**Impact.** A future boot-policy edit could carry the timing receipt across a firmware behaviour change without being detected.

**Suggested outcome.** A follow-up issue against the capture gate. It could hash `boot_policy.py`, or better the generated `MILAN_*` constants per shape, into the receipt, or narrow the prose to "firmware source". This is for the manager to route. No action is required for this merge.

**Verification.** Re-run the probe above; the gate should fail.

### Carried
- **R250-4 S1 / R250-3 S1 (Tests, Conformance):** the timer profile is read from `KL_srp_top` defaults. Routed to #495. **Retained as SUGGESTION.**
- **R249-3 S1 / R249-2 S1 (Conformance):** `boot_policy.py` literals. Routed to #495. **Retained as SUGGESTION.**

### Prior finding disposition
- **R249-4 F1 (BLOCKER; Tests, Conformance, Docs): CLOSED.**
  - Every required outcome in R249-4 is met at this head:
    - Re-measured per the README, with the arms reproduced exactly here.
    - `measurements.json` refreshed: digest, rows and maxima.
    - The section 18 figures updated.
    - A public lane decision exists: assignment 5838671391 names [A323].
    - The gate is not weakened, and the firmware change is not reverted.
  - Its verification also holds:
    - `check_nvm_capture.py` exits 0 locally.
    - Hosted `docs-check` is green at the exact head, with steps 30-51 executed.
    - This reviewer regraded the rows, recomputed the maxima and stated the 0.19754 ms spare against 24.5 ms.
- R250-4 and R249-3 at `c6c65e80` had no open BLOCKER, MAJOR or MINOR finding. Their closures stand, because the delta does not touch those artifacts beyond the clean merge exercised above.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 and carried SUGGESTIONs only) | Assignment 5838671391 items 1-3 against `measurements.json:3,17,290` and the six arms. STOP bar: 24.30246 is at or below 24.5 ms, reproduced (`receipts/reproduction-compare.txt`). README run matrix (clocks, phase, 16 captures, ON/OFF, labelled 100 MHz). R249-4 F1 required outcomes. | R250-6 | a07a75de78b19369e228d4ab8403a52f7435fd64 |
| RTL | CLEAN | Merge `6d181922`: remerge-diff empty and merge-tree equal. Non-overlapping hunks in `milan_csr.sv`, `KL_pp_shadow.sv` and `milan_datapath.sv`. Composed csr (AAF/MAAP neutral reset + RENDER_STAT) and pp_shadow legs. `test_builder.py --require-rv32` elaboration. rtl-src, port-contract and sv-idiom gates. The refresh commit touches no RTL. | R250-6 | a07a75de78b19369e228d4ab8403a52f7435fd64 |
| Robustness | CLEAN (S1 SUGGESTION only) | Gate negative probes (old receipt, firmware edit, harness edit, OFF row +1 tick over the bar) and the four `--mutation` arms. Determinism of the 100 MHz rows checked by re-run. Boot-policy sensitivity probe (S1). | R250-6 | a07a75de78b19369e228d4ab8403a52f7435fd64 |
| Tests | CLEAN (S1 SUGGESTION only) | 48 reproduced capture rows. `check_nvm_capture.py` plus controls. 75/75 docs-check commands. declarations, nvm_hosttest `--self-test`, nvm_cosim (465, 39/39), csr and pp_shadow defaults. Hosted exact-head docs-check steps 1-51. | R250-6 | a07a75de78b19369e228d4ab8403a52f7435fd64 |
| Docs | CLEAN (S1 SUGGESTION only) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557-1618,1735-1760` recomputed against the receipt. Stale-figure search: zero hits. docs_check, em-dash (base 220cb5a3), doc-style, TOC/anchors and doc-paths all pass. | R250-6 | a07a75de78b19369e228d4ab8403a52f7435fd64 |

## Limits

- The scoped Verilator 5.050 path named in the assignment does not exist on this host. I used the system Verilator 5.052 instead. That is the simulator the receipt names; its identity is in each capture log.
- `sv2v` on this host is v0.0.13, while the workflow pins v0.0.12. The builder gate passed with it.
- Locally not run:
  - The HDL-reference build.
  - The docs no-git job.
  - The act self-test, which is forbidden to me.
  - The 1x1 arms, the 100 MHz OFF arm, and the two simulation controls (skip-copy and no-traffic). The harness is unchanged since #559.

  Hosted exact-head jobs cover the first three. The unrun capture arms are covered by the receipt audit and by the determinism shown above.
- The harness writes gitignored `configs/generated/{ltn_rom,ucode}.hex` into the working tree during a run. Both are shape-independent generator outputs. I removed them afterwards along with the `__pycache__` directories.
- Tree integrity after all probes (`receipts/final-integrity.txt`):
  - The index tree and the worktree equal HEAD.
  - Every tracked blob re-hashes to its index id.
  - All gitlinks match: external `efeb541a` (uninitialised), gptp `e5dcea6e`, pp `990f9652` and verilog-axis `48ff7a7e`.
  - The shared LiteX tree and the SDK are unchanged.
- Physical calibration was NOT RUN. Field skips are not hardware proof. The capture figures are simulation measurements, not silicon timing or memory ordering (UNRESOLVED 6 stays open).

## Pending manager duties

- Build and validate the final current-dev candidate. Source base `220cb5a3`; live dev `1658ded2` is not present in this clone. That includes any gitlink reconciliation, such as the gptp pin R249-4 noted on the train.
- Hosted and act acceptance, exact-head gate bookkeeping, and the second positive review.
- Routing S1 to a follow-up issue if accepted.
- Merge only under explicit maintainer authorization.

R250-6 FINISHED
