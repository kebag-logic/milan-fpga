[R305] NEGATIVE - exact head 49d23b20fcad15a3c03554476d8b8c9116b3b375

# R305-1 independent external review: FPGA-gPTP issue #75 / PR #76

- Head `49d23b20fcad15a3c03554476d8b8c9116b3b375`, tree `804cd0dae42b46a2a85656f6e49781687ba671e6`, base `e5dcea6e351abff18a27a00f8e345f3251bdbd8f` (one commit).
- Scope: `phc_slew_active_o`, the registered `clk_i`-synchronous level for the step policy's transient offset correction through the rate path. Its lifecycle, tests, mutants, ROM regeneration, `docs/INTEGRATION.md`, and area.
- Reconstruction order: `docs/README.md`, the role guides and `docs/SOURCE_EVIDENCE.md` (the repository has no AGENTS.md or CONTRIBUTING.md). Then the issue #75 body and the assignment comment, the parent manager decision (milan-fpga #387 comment 5816509317), the PR body, and the base..head diff and history. Last, the public evidence at milan-fpga `941a6c73…/review-evidence/gptp75-r1`.
- This verdict and ledger were written before any other reviewer's report was read. The reconciliation with prior public findings is appended at the end.

## Verdict summary

The RTL and microcode meet the timing contract. The level rises on the policy decision, before the affected addend. It stays high between pairs and clears on the same cycle as the completing or replacement addend pulse. Reset clears it. asCapable loss, missing Sync, missing Follow_Up and a GM identity change hold it and restart qualification. A replacement step holds it through the step and clears it on the step's integral-only rate. Becoming grandmaster retires it together with an integral-only addend. I found no RTL defect.

The verdict is NEGATIVE for two MINOR findings:

- **F1 (Tests, Conformance):** the guards that keep ordinary tracking inactive after a lapse, and after a return from mastership, are not load-bearing in the suite. Two non-equivalent reviewer mutants survive the full PR harness, and a directed probe catches both.
- **F2 (Docs):** the PR moves the engine's lines, so 9 of the 10 `KL_gptp_engine` line anchors in `docs/SOURCE_EVIDENCE.md` are now stale. That ledger says its line numbers describe the current layout. It also has no row for the new claim.

## Findings

### F1 - MINOR - Tests, Conformance - untested inactive branches let false-assertion regressions pass

- **Where:**
  - `hdl/top/KL_gptp_engine.sv:876-878`: the lapse hook is guarded by `phc_slew_active_o &&`.
  - `hdl/top/KL_gptp_engine.sv:940`: mastership (PHC word 3) clears `phc_slew_left_r`.
  - `tb/verilator/engine/sim_main.cpp:4760-4817`: every lapse, identity-change and mastership case starts from an active level. The return-to-slave pair is +50 µs (line 4804), which is outside the tracking band.
- **Authority:**
  - Issue #75 Required item 3 asks for "ordinary tracking that does not assert it, and each defined edge case".
  - `docs/INTEGRATION.md` (Slew-active level) defines "Tracking inside the band without an active correction: Stay inactive" and "Returning to slave duty: Next consumed pair makes the policy decision".
- **Evidence** (Verilator 5.050; `receipts/reviewer_mutants_00_10.txt`, `receipts/probe_harness_*.txt`, `receipts/r305_probe_harness.diff`):
  - Mutant R01 drops the `phc_slew_active_o &&` guard. It **survives** the unmodified PR harness (1,532 checks).
  - Mutant R06 lets mastership leave `phc_slew_left_r` armed. It also **survives**.
  - I added two directed scenarios to a disposable copy of the harness:
    - (A) After completion, a 400 ms Sync lapse while inactive, then two in-band pairs. They must stay inactive.
    - (B) Correction, mastership, return to slave, then two in-band pairs. They must stay inactive.
  - The unmodified head passes the extended harness, 1,573/1,573.
  - R01 fails (A) and (B): the level asserts on "r305: tracking after an inactive Sync lapse stays inactive" and on "r305: in-band return pair stays inactive".
  - R06 fails (B).
  - Both mutants are therefore reachable behaviour changes, not equivalents.
- **Impact:** a regression that raises the level during ordinary in-band tracking would pass every gate. The triggers are a Sync receipt timeout, a GM identity change, a Pdelay-driven asCapable loss or cease while inactive, or a return from mastership. The consumer (#545) would then discard and count CRF windows during ordinary tracking. That contradicts the issue's "ordinary tracking that does not assert it".
- **Required outcome:**
  - Add directed checks for the inactive-lapse case and the in-band return-to-slave case, through the public wire interface as the existing probes do.
  - Add named mutants for both guards to `tb/verilator/engine/mutants.py`, so each must fail its named check.
- **Verification:** both mutants fail their named checks, the positive control passes, and the three engine images pass.

### F2 - MINOR - Docs - the source-evidence ledger no longer binds to the head layout

- **Where:** `docs/SOURCE_EVIDENCE.md:9-37`. The PR adds lines at `hdl/top/KL_gptp_engine.sv:30`, `:107-109` and `:694-700`, which shifts the lines after them.
- **Authority:**
  - `docs/SOURCE_EVIDENCE.md:7` says "Line numbers describe the current branch layout."
  - `docs/README.md` names the ledger as the binding of claims to implementation.
  - At base `e5dcea6` every anchor pointed at its claimed construct. Earlier PRs (#68, cbccf22) added a row for each new claim.
- **Evidence (base line → head line):**
  - #L57 `module KL_gptp_engine` → 58
  - #L99 `tx_credit_i` → 100
  - #L120 `pub_commit_o` → 124
  - #L156 `u_parser` → 160
  - #L236 `t1v_valid_r` → 240
  - #L339 `txts_pend_r` → 343
  - #L345 `txts_ready_o` → 349
  - #L381 `KL_gptp_timer` → 385
  - #L401 `evq_r` → 405
  - #L428 `push_arb` → 432
  - Only #L20 still matches. At head, the anchored lines are unrelated comments or declarations.
  - `make docs` passes, so the check does not detect this.
  - No row binds the new `phc_slew_active_o` contract.
- **Impact:** the second-ranked evidence map points readers and reviewers at the wrong code for ten claims, including the result face and the transmit credit. The new interface claim has no binding.
- **Required outcome:**
  - Re-anchor every `KL_gptp_engine` link to the head layout.
  - Add a row that binds the slew-active level to `KL_gptp_engine` (`phc_slew_active_o`, PHC words 2 and 3) and the generator policy leg, with the engine suite as executable evidence.
- **Verification:** at the new head, each anchor line shows its claimed construct.

### S1 - SUGGESTION - Docs - manager snapshot

`docs/MANAGER.md:42` says the image uses 931 words. The generator reports 994 real words at base and 1,008 of 1,024 at head, so 16 words remain (`receipts/rom_regen.txt`). This staleness predates the PR. The "PHC control" status row also does not mention the new level. Consider recording the new ROM headroom, since the next policy change may not fit.

### S2 - SUGGESTION - Tests - record the equivalent-in-reach arm

Mutant R02 restricts the lapse hook to sync-ok (bit 3). It survives even the extended harness, and I found no reachable arm for it:

- asCapable can only recover after at least two 1 s Pdelay exchanges (`ASCAP_UP_C = 2`).
- The 375 ms Sync watch is re-armed only by a consumed pair, and only mastership disarms it.
- So the Sync watch always clears sync-ok, and restarts qualification, before a pair can be consumed again.

Consider recording this defence-in-depth arm in the `mutants.py` docstring, as that file already does for the pending-pair read gate.

## Lens assessment (artifact-specific evidence)

- **Conformance:**
  - Items 1, 2, 4 and 5 are met:
    - one-bit registered level;
    - rise on the decision before the addend;
    - held between pairs;
    - clear with the completing rate while PI tracking continues;
    - every listed edge defined in `docs/INTEGRATION.md` and implemented as documented;
    - parent connection deferred to #545 as scoped.
  - Item 3 is only partly demonstrated (F1).
  - The ±100 ns, two-pair completion rule is the author's own choice. The issue did not specify one. It is documented, and it leaves the step thresholds, PI arithmetic and 200 ppm clamp unchanged, as the diff confirms.
- **RTL:**
  - `KL_gptp_engine.sv:694-758` and `:792-945`: both the output and the qualifier are flops in the reset `always_ff`. The clear shares the cycle with `phc_addend_we_o`.
  - This invariant holds on every write path: a nonzero `phc_slew_left_r` implies the level is high.
  - Word 3 writes an addend only while active, so mastership without a correction keeps the pre-PR behaviour. R07 confirms this is checked.
  - Engine and bench lint are clean with the pinned simulator.
  - The generator's band comparison is exact. The step gate bounds |RA| ≤ 100 µs, and the 32-bit unsigned compare of RA+100 against 201 selects exactly [-100, +100] ns.
  - The micro-CPU starts only at dispatch entries 16…512 (`KL_gptp_ucpu.sv:510-515`, `KL_gptp_engine.sv:521-541`). Placing legs in µPC 0..15 is therefore safe.
- **Robustness:**
  - Reset is cold, and a warm reset does not revive the level from retained scratch.
  - A late Follow_Up after a lapse cannot retire the rate or count as a settled pair.
  - A held level can last indefinitely while asCapable is lost or during cease. This is documented.
  - The measured closed-loop duration is 3.069 s / 1.917 s for ±90 µs at 140 ppm. That is longer than the 0.5 s the parent decision assumed. The PR discloses this and does not hide it (see manager duties).
- **Tests:**
  - I reran all three engine images at 1,532/1,532 each.
  - I reran all 30 PR mutants: 30 caught. The three #75 controls fail their named checks.
  - 20 reviewer mutants: 17 caught. R01 and R06 survived and are real gaps (F1). R02 is equivalent in reach (S2).
  - MicroCPU 768/768, tsngen 288/288, bench tag PASS, contract PASS.
- **Docs:**
  - The new INTEGRATION.md section matches the RTL and microcode for every event row, as I checked against `gen_gptp_ucode.py:837-886, 1603, 1639-1647, 1880-1895`.
  - The HDL and TEST guides are updated.
  - The source-evidence ledger is stale (F2).
  - The manager snapshot is stale, pre-existing (S1).
  - `make docs` and the diagram checks pass.

## Other evidence

- **ROM:** all four tracked images regenerate byte-identically from the head generator with the Makefile arguments. They match the published `rom-sha256.txt` (`receipts/rom_regen.txt`).
- **Published sources:** the published `candidate-sources.sha256` matches all 13 changed files in this clone.
- **Area and timing:** the published Vivado 2026.1 OOC reports (`xc7a100tfgg484-2`) show 4,773 → 4,853 LUTs (+80) and 3,646 → 3,652 registers (+6). Memory LUTs, BRAM and DSPs are unchanged. Candidate WNS is +1.773 ns, and all constraints are met. I did not rerun synthesis.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Issue #75 body and assignment; parent decision 387/5816509317; PR body; base..head diff; INTEGRATION contract rows | R305-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |
| RTL | CLEAN | `KL_gptp_engine.sv` diff and PHC/pub write paths; `KL_gptp_ucpu.sv` dispatch/compare; `gen_gptp_ucode.py` servo/slew/svrate/become/srto/btca legs; four ROM images; bench instantiation; lint | R305-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |
| Robustness | CLEAN | Reset, warm reset, asCapable loss/recovery, missing Sync/Follow_Up, GM change, replacement step, mastership both ways; timer re-arm paths; closed-loop durations | R305-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |
| Tests | UNCLEAN (F1) | `sim_main.cpp` slew contract and long-slew checks; `mutants.py`; 3 engine images; 30 PR mutants; 20 reviewer mutants; 2 directed probes; ucpu/tsngen/bench/contract | R305-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |
| Docs | UNCLEAN (F2) | INTEGRATION.md, HDL_DEVELOPER.md, TEST_DEVELOPER.md, SOURCE_EVIDENCE.md, MANAGER.md, README.md; `make docs` | R305-1 | 49d23b20fcad15a3c03554476d8b8c9116b3b375 |

## Real limits

- **Simulation only:**
  - The pinned Verilator 5.050 ran the focused suites: engine ×3 images, ucpu, tsngen, bench tag, lint, contract and docs.
  - It also ran the 30 PR mutants and the 20 reviewer mutants, the mutants on the shipping engine image only.
  - Not run by me: the parser and gasket suites (unchanged by the diff), OOC synthesis, the full parent/PP/gPTP/Yosys/builder banks, and hosted/act jobs.
- **Area:** accepted from the published reports, not re-synthesized.
- **Field behaviour:**
  - The harness uses ideal timestamps. Whether real steady-state jitter stays inside ±100 ns (and so leaves the level inactive during ordinary tracking) is not demonstrated.
  - Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Parent consumer:** the `KL_gptp_shadow` connection and the CRF-servo consumption belong to kebag-logic/milan-fpga #545. I examined neither.
- **Candidates:** source validation at this head is distinct from the final current-dev candidate (source base e5dcea6e, live dev 57456af9), which the manager builds at the merge turn.

## Pending manager duties

- **Tolerance:** explicitly accept or override the author-chosen ±100 ns / two-pair completion tolerance. The issue did not set one.
- **Duration:** reconcile the parent decision's "a slew lasts at most 0.5 s" with the measured 1.9–3.1 s intervals and the documented indefinite hold under asCapable loss or cease. This belongs in #545, where the CRF servo holds its integrator for the whole interval.
- **New addend source:** in #545's consumer gates, confirm the new addend source (mastership retire, word 3) against the parent PHC.
- **Parent validation:** run the parent consumer gates on the #545 branch that connects the port, and field-check that the level stays inactive in steady state.
- **Merge candidate:** build and gate the merge-turn current-dev candidate. Own hosted/act acceptance.

## Reconciliation with prior public review findings (read after the verdict and ledger above)

PR #76 has no review objects and no inline comments. One public review report exists at this head: the internal independent review R304-1 (PR #76 comment 5818298785, NEGATIVE). I read it only after writing everything above.

| Prior finding | Status at this head | Basis |
|---|---|---|
| R304 F1 (MINOR; Tests, Conformance): inactive-direction lifecycle not pinned; guard mutants survive | **Retained.** Same defect as R305 F1, reached independently. | My R01 matches its R14 (the `phc_slew_active_o &&` guard). My R06 matches its R07 (word 3 leaves `phc_slew_left_r` armed). Both survive the PR suite and fail my directed probes A and B. The head passes the extended harness. |
| R304 F2 (MINOR; Docs): ten `KL_gptp_engine` anchors in SOURCE_EVIDENCE.md are stale | **Retained.** Same defect as R305 F2. | I measured the same ten line shifts (58/100/124/160/240/343/349/385/405/432). |
| R304 S1 (SUGGESTION): ROM headroom 1,008/1,024; the µPC 0..15 prefix policy change is not recorded | Agreed; merged with R305 S1. I also verified the prefix is safe (entries ≥ 16; reset does not fetch). | `receipts/rom_regen.txt` |
| R304 S2 (SUGGESTION): the RTL-owned lapse hook (publish-flags write restarts qualification) is not described in HDL_DEVELOPER.md | Agreed, as a SUGGESTION. The hook couples state region 3 to the PHC qualifier, and a contributor changing flag bits 2/3 needs to know. | `KL_gptp_engine.sv:872-878` |
| R304 S3 (SUGGESTION): field noise and duration are uncharacterised | Agreed. It is already covered by my limits and manager duties. | — |
| R304 R02 equivalence | Agreed (R305 S2). Both reviews rest on code reading of the 375 ms Sync watch against the 1 s Pdelay cadence. | `gen_gptp_ucode.py:396-399, 880, 1668` |

Nothing in the prior report contradicts this verdict, and it adds no finding I would reject. The verdict stays **NEGATIVE** on F1 and F2.

## Receipts and reproduction

The tree is a `git archive` export of the exact head under `scratch/`. The reviewed clone was never built in. Tools:

- Simulator: the pinned wrapper reporting Verilator 5.050 (`receipts/tool_identity.txt`).
- Python 3.14.7.

| Receipt | Content |
|---|---|
| `receipts/rom_regen.txt` | Four ROM images regenerated and byte-compared, plus base ROM usage |
| `receipts/engine_run.log` | Engine suite on three images: 1,532/1,532 each, with the SLEW TRACE durations |
| `receipts/focused_gates.txt` | Contract, lint (engine and bench), docs and diagrams, ucpu 768/768, tsngen 288/288, bench tag |
| `receipts/pr_mutants_00_15.txt`, `receipts/pr_mutants_15_30.txt` | The 30 PR mutants, all caught (named-check gate applied to `slew:` arms) |
| `receipts/reviewer_mutants_00_10.txt`, `receipts/reviewer_mutants_10_20.txt` | 20 reviewer mutants: 17 caught; R01, R02, R06 not caught |
| `receipts/r305_probe_harness.diff` | The two directed scenarios added to a disposable harness copy |
| `receipts/probe_harness_control.txt` | Unmodified head passes the extended harness, 1,573/1,573 |
| `receipts/probe_harness_survivors.txt` | R01 and R06 caught by the probes; R02 not caught |
| `receipts/clone_integrity.txt` | The clone's HEAD, tree, index and blobs are exact; no gitlinks |
| `scripts/probe_mutants.py` | Mutant and probe runner, at most 4 jobs × 2 build threads |
| `scripts/make_probe_tree.py` | Reproduces the probe tree from the exact head |

**Process deviation, recorded:**

- The engine suite built with `-j 8`, and mutant pools ran 4 workers × 2 build threads.
- The ucpu, tsngen and bench-tag suites were built with their Makefiles' default `--build -j 0`. That allows the simulator's build to use all host cores. Each ran as a single, sequential build of a few seconds, but it may have exceeded the 8-job cap during those builds. Verdict evidence does not depend on these three suites.

Everything ran in the foreground. No source file, commit, push or GitHub write was made.

R305-1 FINISHED
