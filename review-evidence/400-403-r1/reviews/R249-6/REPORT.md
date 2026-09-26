[R249] POSITIVE - exact head a07a75de78b19369e228d4ab8403a52f7435fd64

# R249-6: internal independent review of issue #400 / PR #566, round 5 delta

- Head `a07a75de78b19369e228d4ab8403a52f7435fd64`, tree `0c8c1de484f5b305f40bfbcb171f61a16e38dd26`.
- Delta judged: `c6c65e80..a07a75de`. It is the merge `6d181922` of dev `220cb5a3` into `c6c65e80`, plus `a07a75de`, which re-measures the saved-state capture on the composed product firmware.
- Assignment: [issue #400 comment 5838671391](https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5838671391). It answers the composition review R249-4 F1 BLOCKER.
- The source reviews at `c6c65e80` (R250-4, R249-3) stand, per that assignment.
- Result: all five lenses were applied and all five are CLEAN.
  - No BLOCKER, MAJOR or MINOR is open.
  - R249-4 F1 is CLOSED, with an exact reproduction of the measurement.
  - One new SUGGESTION (S1) and one observation routed as a SUGGESTION (S2). Two carried SUGGESTIONs stay routed to #495.

## Reconstruction

I read these in order:

1. `AGENTS.md`, `CONTRIBUTING.md` sections 2-3 and 6, and `docs/README.md`.
2. Issue #400: the body, the 2026-09-22 pre-implementation decision, the 2026-09-23 owner decision, the round 2-5 assignments (5838671391 for this round), and the author's REVIEW READY 5839527815.
3. The #559 capture decision [5831090112](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112). It sets the 24.5 ms STOP condition and the measurement shape.
4. `tb/verilator/nvm_capture_cpu/README.md`, `scripts/check_nvm_capture.py` and `.github/workflows/docs.yml` (the docs-check step list).
5. `git diff 220cb5a3..a07a75de`, `git diff c6c65e80..a07a75de`, the merge commit and `a07a75de`.
6. The public author evidence `review-evidence/400-403-r1/author-r6` at `b031932d`: the recipes, the environment, per-arm rows and the abandoned serial run.

My draft verdict and ledger were written before I read any prior review report (`receipts/draft-verdict-before-prior-findings.txt`). Only then did I read R249-4, R250-4 and R249-3.

No private author material or lane scratchpad was read, and the author's build directories were not opened. I did not read the concurrent R250-6 review.

## Assigned verification items

### (1) The merge is clean: CONFIRMED

`receipts/remerge-diff-6d181922.txt`, `receipts/merge-check.txt`:

- `git show --remerge-diff 6d181922` prints only the commit header line. There is no resolution hunk.
- An independent `git merge-tree --write-tree c6c65e80 220cb5a3` yields `87ed44d7d61c6ccad6d31e1a9a51bafbad43adee`. That equals the recorded tree of `6d181922`.
  - Seven files auto-merged: `REGISTER_MAP.md`, `milan_csr.sv`, `KL_pp_shadow.sv`, `milan_datapath.sv`, csr `sim_main.cpp` and `sim_win.cpp`, and the `milan_dp/README.md`.
- `a07a75de` changes exactly two files relative to the merge:
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`
  - `tb/verilator/nvm_capture_cpu/measurements.json`
  - This meets "change nothing else".
- The submodule gitlinks are identical at `c6c65e80`, `220cb5a3`, `6d181922` and `a07a75de`: protocol-processor `990f9652`, gptp-processor `e5dcea6e`, verilog-axis `48ff7a7e`, external `efeb541a`.

### (2) The re-measurement follows the README and reproduces exactly: CONFIRMED

Receipt shape (`measurements.json`, checked by `scripts/check_nvm_capture.py` and by me):

- Both contract shapes are measured at 50 MHz with aligned edges, 16 captures per arm, traffic ON and OFF.
- The labelled 100 MHz 8x8 non-contract point has both arms.
- That is 96 rows. `measured_for` is unchanged: 12,634 B / 156 records at 8x8 and 3,218 B / 53 records at 1x1.
- `product_firmware_sha256` (line 17) is `0bf43cd4...`. That equals `sha256(sw/firmware/milan_baremetal/milan_baremetal.c)` at this head.
  - It is the PR-side firmware (`c6c65e80`).
  - The pre-merge dev digest was `7cdc5e68...`.
- The harness hashes equal the head's harness files.

I reproduced the measurement independently at this head. The environment was:

- the README recipe, run with `unshare -Urn`, `PYTHONHASHSEED=0` and offline flags;
- the pinned RV32 SDK (`riscv32-linux-gcc 14.3.0`);
- LiteX components at the receipt's revisions;
- Verilator 5.052, the simulator the receipt names;
- external build directories.

`scripts/reproduce_capture.sh` and `scripts/compare_capture_rows.py` are the reproduction scripts; `receipts/environment.txt` records the tool identities.

| Arm | Harness grade | Rows equal to receipt | Min to max, ms | Receipt maximum, ms |
|---|---|---|---|---|
| 8x8, 50 MHz, ON | rc 0 | 16/16 identical | 24.29290 to 24.30246 | 24.30246 |
| 8x8, 50 MHz, OFF | rc 0 | 16/16 identical | 24.25794 to 24.26154 | 24.26154 |
| 1x1, 50 MHz, ON | rc 0 | 16/16 identical | 6.59814 to 6.60642 | 6.60642 |
| 1x1, 50 MHz, OFF | rc 0 | 16/16 identical | 6.58554 to 6.58857 | 6.58857 |
| 8x8, 100 MHz, ON (non-contract) | rc 0 | 16/16 identical | 18.99012 to 19.00433 | 19.00433 |

The row-by-row comparison is in `receipts/capture-compare.log`, `receipts/capture-compare-1x1.log` and `receipts/capture-compare-100.log`. The rows and graded summaries are in `receipts/rows-*.log` and `receipts/measurement-*.json`.

- **Every row is identical, not just the maxima.** That covers `sys_cycles`, request/response/read counters, mismatches and open for all 80 reproduced captures (64 contract-point captures plus the 100 MHz ON arm).
- **The 8x8 contract maximum is 24.30246 ms over both arms.** That is 0.19754 ms under 24.5 ms, with 2.0163x margin against the 49 ms floor, so the STOP condition is not triggered. This matches the author's figure.
- **The firmware digest ties to this head's build.** My build's instrumented firmware and BIOS hash to exactly the receipt's `instrumented_firmware_sha256` and `bios_sha256` for both 8x8 50 MHz arms and the 8x8 100 MHz ON arm, and the CPU netlist hash matches (`receipts/firmware-hash-compare.txt`). The receipt therefore describes the firmware and BIOS this head builds, not a carried-over build.
  - The pre-merge receipt's BIOS hashes differ (`841e894f...`/`cda2be86...`), so the change is real.
- The published abandoned serial ON run (author-r6) shows the same first four rows as the published parallel run. My reproduction also matches, so the simulation is deterministic and no row selection occurred.

### (3) Section 18 and UNRESOLVED 6 are consistent, with no stale claim: CONFIRMED

`scripts/check_section18.py` recomputes every published figure from the receipt rows and finds each literal in the document. The result is 20/20 OK (`receipts/section18-crosscheck.log`). It covers:

- all six table rows (ticks, ms and per-arm margin);
- the worst 8x8 figure, its margin and its slack;
- the ON/OFF deltas (0.04092 ms / 0.169%, 0.01785 ms / 0.271%, 0.78591 ms);
- the 1x1 and 100 MHz maxima in both places, and the 96-capture count.

`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1573-1578` and `:1740-1743` carry 24.30246 / 2.0163x / 0.19754. The earlier sentence "Product firmware, RTL and builder census lists remain unchanged", which R249-4 F1 flagged, is replaced by `:1577-1578`: the composed firmware is pinned, and firmware and hold are unchanged.

A tree-wide search for `24.30454`, `24.305`, `2.0161`, `0.19546`, `0.04300` and `0.177%`, and for the old digests `7cdc5e68`/`368eb10b`/`841e894f` outside the receipt, finds nothing.

### (4) Gates pass at this head: CONFIRMED

- `python3 scripts/check_nvm_capture.py` exits 0. `--mutation bytes|records|clock|ignore-off-timing` each exit 1 with their controls printed (`receipts/check_nvm_capture-*.log`).
- **docs-check** (`scripts/run_docs_check.py` runs each step's `run:` text verbatim from `docs.yml` at this head; `receipts/docs-check/`):
  - Every executed step exits 0: steps 7-16, 18, 19, 21 and 24-49 except 42.
  - That includes the capture gate (27) and 21 of the 22 steps after it (28-41, 43-49).
  - The builder step 25 (`test_builder.py --require-rv32`) printed "ALL GATES PASS EXCEPT 1 NOT RUN". The arm not run is gate 11, the historical calibration report, which is known and pre-existing.
  - Not run by me:
    - 42 (`act_ci.py --selftest`): outside my authority.
    - 1 (HDL reference): needs a pip install.
    - The install/cache steps 3, 5, 6, 17, 20, 22 and 23: prerequisites were already present and verified.
  - Em-dash (8) was judged against base `220cb5a3`.
- **Hosted, read-only:** the exact-head `pull_request` run 36189029286 (`docs-check` job 108249399678) executed all 51 steps with success. That includes the capture gate, all 22 later steps (hosted 30-51, including the act self-test) and the HDL reference (`receipts/hosted-docs-check-steps.txt`).
- **Suites** use the pinned Verilator 5.050 with its version output verified. The scoped wrapper path named in the assignment does not exist on this host; the same release's install was used instead. The wrapper caps `-j 0` at 6 (`scripts/verilator-wrapper.sh`, `receipts/suite-rcs.txt`).

  | Target | Result |
  |---|---|
  | `sw/builder/test_declarations.py` | rc 0: five configs, 26 refusals, 9 binding/reset mutants |
  | `make -C tb/verilator/csr` | rc 0: legs of 400/400/400/400/121/44 checks with 0 failures; RENDER_STAT and "AAF/MAAP neutral reset" checks both execute |
  | `make -C tb/verilator/pp_shadow` | rc 0 |
  | `make -C tb/verilator/nvm_cosim` | rc 0: 465/465 checks, 39/39 mutants |
  | `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` (docs-check 28) | rc 0: 5 shapes, every planted defect reddened |
  | builder (docs-check 25) | rc 0, as above |

## Composition beyond the assigned items (RTL, Robustness)

The textual merge is clean. I still checked the semantic seams in the seven auto-merged files.

- **`milan_datapath.sv`: no shared nets between the two sides.**
  - PR: the `SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C)` binding, the `ADP_STROUT_PRES_NS_C` fold and passive public taps.
  - dev: #551 `lwsrp_stream_gate = ACTIVE & grant` and #443 `render_status_w` to `i_render_status`.
- **`milan_csr.sv`: the PR's neutral `AAF_CTRL_RST_C`/`MAAP_CTRL_RST_C` and dev's `A_RENDER_STAT` live arm are independent.** VERSION is not bumped by either side, and dev states that the release step owns the bump.
- **#551's licence test programs AAF and MAAP absolutely, so the PR's neutral resets cannot leak into it.** It writes AAF `0x00020001` and MAAP `0x201` at `sim_crf_licence.cpp:828-830`.
- **Focused composition probe: `make -C tb/verilator/milan_dp crflic` at this head exits 0 with 415 checks and 0 failures** (`receipts/milan_dp-crflic.log`). Its checks include:
  - the CRF C-tag `{PCP 3, VID 2}`, with the processor's startup VID now bound from the PR's generated `SRP_DOM_DEF_VID_P`;
  - #551's refused re-declaration arms: the gate never opens, and there is no STREAM_START or STREAM_STOP.
- `python3 scripts/lint_rtl.py --check`: PASS (90 <= ratchet 90) (`receipts/lint_rtl.log`).
- **Receipt robustness probes** (`scripts/probe_capture_gate.sh`, `scripts/probe_capture_maxima.sh`, `receipts/capture-gate-probes.log`). Each probe perturbs one tracked file in the clone, runs the gate, then restores the HEAD blob. The gate refused each perturbation for its named reason:

  | Probe | Gate message |
  |---|---|
  | One-byte firmware edit (the F1 shape) | `product firmware changed` |
  | Receipt reverted to the dev digest | `product firmware changed` |
  | A row +1 tick with the summary stale | `receipt summary differs from rows` |
  | An OFF row made the slowest, arm summary regraded by the harness, published maxima stale | `published maximum must include every traffic arm` |
  | An OFF row with traffic | `traffic arm failed` |
  | An 8x8 row at 24.50001 ms | `exceeds half the 49 ms hold floor` |

  The unperturbed run passes, and the tracked bytes equal HEAD afterwards.

## Prior public findings at this head

| Finding | Status at `a07a75de` | Evidence |
|---|---|---|
| R249-4 F1 BLOCKER (Tests, Conformance, Docs): the composed tree fails `check_nvm_capture.py` on the firmware pin; section 18 claimed unchanged firmware | **CLOSED** | Gate rc 0 locally and hosted. The receipt was refreshed with digest `0bf43cd4...` = the head firmware, and all 96 rows were re-measured. My reproduction of 80 rows (the four contract arms and the 100 MHz ON arm) is identical, with BIOS and instrumented-firmware hashes equal. Section 18 and UNRESOLVED 6 were updated (item 3). The gate, its pin and its controls are unweakened: `check_nvm_capture.py` is byte-identical to dev `220cb5a3`. The firmware was not reverted. The lane was named by assignment 5838671391. |
| R250-3 S1 / R250-4 S1 carried SUGGESTION (Tests, Conformance): the timer profile is read from `KL_srp_top` defaults (`sw/builder/test_declarations.py:162-166`) | Retained as SUGGESTION, routed to #495 (open) | The file is unchanged in `c6c65e80..a07a75de`. No coverage effect. |
| R249-2/3 S1 carried SUGGESTION (Conformance): `sw/litex/boot_policy.py` literals | Retained as SUGGESTION, routed to #495 | Unchanged in the delta. No coverage effect. |
| All other R249-2/3 and R250-2/3/4 findings | Closed at earlier heads (R249-3, R250-4) | Their files are unchanged by the delta, except the auto-merged files examined above. |

## New findings

### S1 - SUGGESTION - Docs - `tb/verilator/nvm_capture_cpu/measurements.json:79,116,153,190,227,264`: the receipt's `command` fields record a host work path

- **Authority/evidence.**
  - The README run recipe (`tb/verilator/nvm_capture_cpu/README.md` "Run") and the pre-merge receipt use `/tmp/nvm-capture-*` build directories.
  - The refreshed receipt records `--build-dir` under a host-specific work-storage directory, with a lane-named subdirectory.
  - The published author evidence rewrote the same path to a `$VALIDATION_STORAGE` placeholder, but the tracked file keeps the raw path.
- **Why not MINOR.**
  - None of `CONTRIBUTING.md` section 6's enumerated categories applies: it is not a hostname, a home path, a subnet, a serial or an interface name.
  - The docs-check local-info sweep passes.
  - The path reveals nothing beyond the public project and lane identifiers.
  - The build directory is arbitrary and does not affect the result.
- **Impact.** The receipt's command is not copy-paste portable, and it is inconsistent with the evidence-publication convention.
- **Suggested outcome.** At the next receipt refresh, record the README's `/tmp` form or a placeholder.
- **Verification.** The `--build-dir` values in `measurements.json` show no host-specific path.

### S2 - SUGGESTION - Tests, Robustness - `scripts/check_nvm_capture.py:61-63` (pre-existing #559 design, not introduced here): the firmware pin covers `milan_baremetal.c` bytes only

- **Evidence.**
  - The BIOS also compiles generated constants (`tb/verilator/nvm_capture_cpu/soc.py` `_firmware_constants`: `fabric_constants`, `firmware_constants`). A builder-only change to those constants changes the shipped binary without changing the pinned source or the census.
  - This round's own data shows that edits outside the timed interval move individual 8x8 ON captures by up to 11.56 µs (row 10: 2,430,454 to 2,429,298 ticks), against 0.19754 ms of slack.
  - This PR was caught because it edited the `.c` file.
- **Impact.** It is small today, but it is a path by which timing could be carried across a binary change.
- **Suggested outcome.** The manager decides whether to route this to #495 or to a #559 follow-up. It is out of this PR's frozen scope, and it has no coverage effect.

## Clean-lens evidence (same fields as a finding)

- **[R249] PASS Conformance.** Artifacts: `a07a75de` diff; `measurements.json:2-17,270-290`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557-1596,1613-1620,1737-1747`; `scripts/check_nvm_capture.py`; `receipts/capture-compare*.log`. Checked against assignment 5838671391 items 1-3 and #559 decision 5831090112:
  - the clean merge, the full 96-row matrix, and the digest equal to the head firmware;
  - the 8x8 maximum over both arms is 24.30246 ms, at most 24.5 ms, so the STOP condition is not triggered;
  - the hold and firmware are unchanged, and nothing else changed.
- **[R249] PASS RTL.** Artifacts: the auto-merged regions of `hdl/milan/milan_datapath.sv` (the `lwsrp_stream_gate` licence block, `render_status_w`/`g_render_status`, `.i_render_status`, `.SRP_DOM_DEF_VID_P`), `hdl/common/csr/milan_csr.sv` (`AAF_CTRL_RST_C`/`MAAP_CTRL_RST_C`, `A_RENDER_STAT` decode, live mux and read-valid) and `hdl/milan/KL_pp_shadow.sv` (`SRP_DOM_DEF_VID_P` parameter and pass-through, `srp_active_o`/`srp_sr_admitted_o` comments); `receipts/merge-check.txt`, `lint_rtl.log`, `milan_dp-crflic.log`, `csr.log`, `pp_shadow.log`. Checked for net and parameter collisions between #551/#443 and the PR's VID and reset changes:
  - none found; the lint ratchet holds;
  - the composed crflic, csr and pp_shadow legs pass.
- **[R249] PASS Robustness.** Artifacts: `receipts/capture-gate-probes.log` (7 perturbations, 7 refusals with named reasons, restored); the deterministic reproduction; the `sim_crf_licence.cpp:828-830` absolute CSR programming. Checked:
  - receipt tampering, stale maxima, an OFF arm carrying traffic, an over-limit row and a stale digest are all refused;
  - the neutral resets cannot leak into dev's legs.
- **[R249] PASS Tests.** Artifacts: `check_nvm_capture.py` plus 4 mutation controls; docs-check steps 7-49 as listed; hosted run 36189029286; `test_declarations`, csr, pp_shadow, nvm_cosim (465/465, 39/39) and `test_nvm_firmware --self-test`; the independent capture reproduction (80 rows identical). Checked that the required gates pass and can fail: the mutations and probes each go red.
- **[R249] PASS Docs.** Artifacts: `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and UNRESOLVED 6 (20/20 figures recomputed); a tree-wide stale-figure search; the merged `REGISTER_MAP.md` rows `0x654`, `0x6CC` and `0x8DC` and the #551 licence text; the `milan_dp/README.md` merged sections; the docs-check wording, em-dash, TOC, cited-path and doc-style steps. Checked:
  - there are no stale figures and no contradiction between the merged sides;
  - S1 is a suggestion only.

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5838671391 items 1-3; #559 decision 5831090112; `measurements.json`; section 18 / UNRESOLVED 6; remerge-diff; reproduction | R249-6 | `a07a75de78b19369e228d4ab8403a52f7435fd64` |
| RTL | CLEAN | The 7 auto-merged files' overlapping regions; lint ratchet; composed crflic, csr and pp_shadow legs | R249-6 | `a07a75de78b19369e228d4ab8403a52f7435fd64` |
| Robustness | CLEAN | 7 capture-gate perturbation probes; deterministic re-run; neutral-reset leakage check | R249-6 | `a07a75de78b19369e228d4ab8403a52f7435fd64` |
| Tests | CLEAN (S2 SUGGESTION only) | The capture gate and controls; docs-check 7-49 (not 42); hosted docs-check; assigned suites; 80-row reproduction | R249-6 | `a07a75de78b19369e228d4ab8403a52f7435fd64` |
| Docs | CLEAN (S1 SUGGESTION only) | Section 18 / UNRESOLVED 6 figure recomputation; stale search; merged REGISTER_MAP and README; doc gates | R249-6 | `a07a75de78b19369e228d4ab8403a52f7435fd64` |

The ledger covers the round-5 delta `c6c65e80..a07a75de`. The source content at `c6c65e80` is covered by R249-3 and R250-4, per the assignment. Every artifact that `c6c65e80..a07a75de` changes is either dev's already-merged content or the two files of `a07a75de`, and both kinds were examined here.

## Packet

Every file listed in `MANIFEST.sha256` is published.

**Scripts** (`scripts/`):

| Script | Purpose |
|---|---|
| `reproduce_capture.sh` | One harness arm. Needs `SDK_BIN` and `LITEX_VENV_BIN`. |
| `compare_capture_rows.py` | Row-by-row comparison against the receipt. |
| `check_section18.py` | Document figures recomputed from the rows. |
| `run_docs_check.py` | docs-check steps verbatim from `docs.yml`. Needs `PYTHON_BIN_DIR` and `SDK_BIN`. |
| `probe_capture_gate.sh`, `probe_capture_maxima.sh` | Gate fault probes, with restore. |
| `verilator-wrapper.sh` | Needs `PINNED_VERILATOR`. Caps `-j 0`. |
| `verify_clone_integrity.sh` | Tracked-state integrity check. |

**Receipts** are under `receipts/`. Host path prefixes in them are replaced by the placeholders `$CANDIDATE`, `$PACKET`, `$VALIDATION_TOOLS`, `$VALIDATION_STORAGE` and `$HOME`.

## Real limits

- **Physical calibration is NOT RUN.** The capture figures are simulation measurements with substituted clocks, DDR PHY, MAC transport and flash (README "Substitutions"). They are not hardware proof, and field skips are not hardware proof. The builder's gate 11 historical calibration arm is NOT RUN.
- **Not run locally:**
  - docs-check step 42 (`act_ci.py --selftest`): outside my authority;
  - step 1 (HDL reference): requires a pip install;
  - the install/cache steps.
  - The hosted exact-head run shows all of these executed with success, but that is hosted evidence, not mine.
- **Tool deviations.**
  - The local sv2v is v0.0.13; the pinned CI install is v0.0.12. It was used by the builder, bare-metal-scope, fail-fast and entity-shape steps, all green.
  - The scoped Verilator wrapper path named in the assignment does not exist. I used the host's Verilator 5.050 install with verified version output (5.050 2026-07-01), and the build logs report 5.050.
- **Not reproduced by me:** the 8x8 100 MHz OFF arm, which is non-contract. The other five arms (80 of 96 rows) were reproduced identically.
- **The final current-dev candidate is not validated here.** Source base `220cb5a3`; live dev `1658ded2` is not in this clone.
- **Parallelism.** During two staggered 8-job capture compiles, one single-threaded simulation ran alongside, and docs-check steps also ran beside two single-threaded simulations. Busy processes briefly exceeded 8.
- **Clone state.** The in-clone probes were restored. The integrity check (`scripts/verify_clone_integrity.sh`, `receipts/clone-integrity.log`) confirms:
  - HEAD and tree;
  - the index equals the HEAD tree, all 911 entries at stage 0;
  - every tracked file hashes to its blob with its mode;
  - no assume-unchanged or skip-worktree flags;
  - the three required gitlinks are at their pins and clean.

  The checker's own negative controls are in `receipts/integrity-checker-controls.txt`. Ignored build products (`obj_*`, `__pycache__`, `sw/builder/out`) remain in the clone.

## Pending manager duties

- Build and validate the final current-dev candidate (live dev `1658ded2`) at the merge turn. That includes `check_nvm_capture.py`, because any dev-side firmware or census change since `220cb5a3` would require another re-measurement.
- Own hosted and act acceptance for the exact head and the candidate.
- Obtain the second independent positive (the external review) and publish the combined completion ledger.
- Route S2 (and, optionally, S1) to #495 or to a #559 follow-up issue.
- Physical calibration and hardware timing remain UNRESOLVED 6 and are not claimed.
- Merge requires explicit maintainer authorization.

## Note: the 8x8 100 MHz ON arm

- **Why it was reproduced.** The refreshed receipt's 100 MHz rows are byte-identical to the pre-merge receipt, but their BIOS and firmware hashes changed. That pattern could have meant the rows were carried over, so I reproduced the ON arm at this head.
- **Result.** The harness exits 0 and all 16 rows are identical to the receipt: 18.99012 to 19.00433 ms. My build's instrumented-firmware and BIOS hashes equal the receipt's (`receipts/capture-compare-100.log`, `receipts/firmware-hash-compare.txt`).
- **Conclusion.** The unchanged 100/100 MHz timing is genuine for the new firmware. The firmware edit lies outside the timed interval, and that clock pair has no phase offset.

R249-6 FINISHED
