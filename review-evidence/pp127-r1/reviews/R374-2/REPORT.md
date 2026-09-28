[R374] NEGATIVE - exact head 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c

# R374-2: internal independent review of processor PR #130 (issue #127), round 2

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #130, issue #127.
- **Exact head:** `00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c`, tree `95f398f31a3dc99709b167459576f5e300c3de5d`.
- **Delta reviewed:** `cf4e5c63..00b5c6c9`, one commit, 64 files. There are no `hdl/` changes (0 diff lines). The delta touches tests, mutation patches, READMEs and one paragraph of `docs/architecture/10_srp_engine.md` §6.5.
- **Full base:** `16be6768f710e79450aace277abacd6c2c3336e5`.
- **Round:** R374-2. Cleared context, own detached clone.
- **Reconstructed from:**
  - `README.md` and `docs/README`. The repository has no AGENTS.md or CONTRIBUTING.md.
  - The issue #127 body, the round-1 assignment (5860872275) and the round-2 assignment (5861796018), including the manager decision that the deadline-anchored oracle is the accepted parent-replay proof.
  - `10_srp_engine.md` §6.5 and `08_timing.md`, and the diff and history.
  - The public evidence at kebag-logic/milan-fpga `pp127-review-evidence` @ `86750aca`, `review-evidence/pp127-r1/author-r2/`. This supersedes the round-1 packet at `88ed7be3`.
  - The manager's bank comments on PR #130: 5862222946 (donor bank) and 5862231642 (parent consumer gates).
- **Independence:**
  - I completed my own pass over the delta, with probes and mutants, before I read the prior external round-1 findings (R375-1, 5861714667). Their dispositions are below.
  - I did not read the same-round external report (R375-2, posted during this review), private author material, lane scratchpads or the management tree.

## Verdict

**NEGATIVE.** Every round-1 finding, mine and the external reviewer's, is resolved at this head. The one thing still open is a new MINOR: the donor bank's `git diff --check` fails on the new mutation patch files.

The round-1 findings resolve as follows:

- **Parent gates.** The parent consumer gates pass 11 of 11, per the manager. I independently re-ran the three that failed in round 1, and all three pass.
- **Required reviewer mutants.** All seven required mutants fail named O1–O5 assertions in the committed suite.
- **Coalescing, arbitration and README counts.** Join-tick coalescing is pinned by O6, the MVRP/prepare arbitration by O8, and the stream-FSM README counts are corrected.
- **TX-slot hold.** The canceled-empty-reservation hold is bounded and documented, and the link-up bound is pinned by O7.
- **Replay harness.** The parent replay harness sources are published with the recorded hashes. I re-ran the harness: it passes at head, and the deadline oracle fails on base.

The RTL is byte-identical to round 1, so LV + rLv and #108 are unchanged.

## Findings

### N1 - MINOR - Tests - the new mutation patch files fail the donor bank's `git diff --check`

- **Where:**
  - `tb/srp_top/mutations/*.patch`: 23 of the 56 new files are affected, with 26 "trailing whitespace" entries and 5 "new blank line at EOF" entries.
  - Examples: `tb/srp_top/mutations/action-omitted.patch:10`, `already-full-missed.patch:11` (both kinds), `reserved-slot-not-reused.patch:11` (both kinds), `leaveall-expiry-lost.patch:11`, `listener-sid-ignored.patch:11` and `r-expiry-pulse-restored.patch:36`.
  - The cause is that blank unified-diff context lines are a single space.
- **Authority/evidence:**
  - Manager comment 5862222946 reports donor bank 8/9 at `00b5c6c9`: step 9, `git diff --check 16be6768 HEAD`, fails on these files, and the comment assigns the fix to the next round.
  - I reproduced it in my clone: rc 2 (`receipts/git-diff-check.log`). The same command is rc 0 at `cf4e5c63`, and rc 0 at head when `tb/srp_top/mutations` is excluded, so the failure is confined to this delta.
  - The manager's comment names only one blank-at-EOF file. My run finds five.
  - The hosted docs-gates job does not run this check, so the six green hosted runs do not cover it.
- **Impact:** a required donor-bank gate is red, so the merge bar cannot be met at this head. There is no functional effect: the patches apply, and all 56 arms are killed.
- **Required outcome:** `git diff --check 16be6768 <new head>` returns 0, and every patch still passes `git apply --check`. Either scope a `.gitattributes` whitespace exemption to `tb/srp_top/mutations/*.patch`, or regenerate the patches without whitespace-only lines.
- **Verification:** `git diff --check 16be6768 <head>` rc 0; `python3 tb/srp_top/mutants.py --output <dir>` still reports `64 checks: 64 PASS`; the manager's donor bank is 9/9.

### S1 - SUGGESTION - Tests - the srp_top campaign is not visible to the parent's evidence inventory

- **Where:** `tb/srp_top/Makefile`. No target runs `tb/srp_top/mutants.py`.
- **Evidence:** in my scratch-parent run, `receipts/parent-measure_test_evidence.log` lists `protocol-processor/tb/srp_top` (and `srp_encoder`, `srp_stream_fsms`) among the 76 suites without an executable mutation arm. The gate still passes (76 ≤ 77).
- **Suggested outcome:** add a `mutants` target, the way the armed gPTP suites expose theirs, so the parent inventory counts the campaign and can lower its ratchet. This is optional.

## Resolution of prior findings at this head

| Prior finding | Status at `00b5c6c9` | Evidence |
|---|---|---|
| R374-1 F1 / R375-1 F1 (MAJOR): parent consumer gates 8/11 | **RESOLVED** | See "R374-1 F1 / R375-1 F1: evidence" below. |
| R374-1 F2 (MINOR): `my-join-edge-peer`, `my-cancel-eats-new-intent`, `my-reuse-flags-ignore-cancel` survived | **RESOLVED** | See "R374-1 F2: evidence" below. |
| R375-1 F2 (MINOR): `r-cancel-latch-dropped`, `r-cancel-consumes-new-intent`, `r-join-start-guard-dropped`, `r-sink-receive-priority-lost` survived | **RESOLVED** | See "R375-1 F2: evidence" below. |
| R374-1 F3 (SUGGESTION): canceled empty reservation holds a TX slot | **RESOLVED (documented bound)** | See "R374-1 F3: evidence" below. |
| R374-1 F4 / R375-1 F4 (SUGGESTION): replay sources unpublished; proof wording | **RESOLVED** | See "R374-1 F4 / R375-1 F4: evidence" below. |
| R374-1 F5 / R375-1 F3(a) (SUGGESTION): join-tick coalescing unpinned | **RESOLVED** | O6 (`sim_main.cpp:1029`). `my-drop-join-during-wait` fails O6 in the full default suite, and `r-join-coalesce-dropped` is KILLED (O6). |
| R375-1 F3(b): same-cycle MVRP/prepare arbitration unpinned | **RESOLVED** | Encoder O8 (`tb/srp_encoder/sim_main.cpp:1229`, wrapper exposes preparation). `r-mvrp-start-during-prepare` is KILLED: O8 fails 3 checks and B1-vlan 2, and the encoder control is 562/562. |
| R375-1 F3(c): stream-FSM README counts | **RESOLVED** | `tb/srp_stream_fsms/README.md:151-152` now says 12 of 1203 and 12 of 1211. My campaign logs show `1203 checks: 1191 PASS, 12 FAIL` and `1211 checks: 1199 PASS, 12 FAIL`. |

### R374-1 F1 / R375-1 F1: evidence

- **Manager run:** comment 5862231642 reports 11 of 11 (parent dev `931f396e`, gitlink `00b5c6c9`).
- **My independent run.** I assembled a scratch parent at `931f396e` with the gitlink moved to `00b5c6c9` and gPTP at its pin `5dce647a` (`scripts/parent_gates.sh`). Results:
  - `check_cpp_idiom.py`: rc 0, multi-declarator 0 ≤ 0.
  - `check_py_idiom.py`: rc 0; unannotated, undocumented and over-long are all 0 ≤ 0.
  - `measure_test_evidence.py --check`: rc 0, with 0 ≤ 0 unexplained DUT-source readers and 3 ≤ 3 wall-clock suite files.
  - Receipts: `receipts/parent-*.log`.
- **Constructs removed:**
  - The multi-declarators are split (`tb/srp_top/sim_main.cpp:334-339`, `:726`, `:829`).
  - The Python functions `:80`, `:89`, `:98` and `:131` are annotated and documented.
  - The host `timeout=` is gone. In its place is a DUT-clock budget (`sim_main.cpp:343`, 200,000,000 clocks).
  - The driver applies checked-in patches instead of reading the RTL.

### R374-1 F2: evidence

- **Default suite.** I re-applied my round-1 textual edits verbatim (`scripts/r374_2_mutants.py`) and ran the **full default** srp_top suite, 1987 checks:

  | Mutant | Failures | Assertions |
  |---|---|---|
  | `my-join-edge-peer` | 2 | O3 (delta=0), O4 (delta=-1) |
  | `my-cancel-eats-new-intent` | 1 | O2 |
  | `my-reuse-flags-ignore-cancel` | 1 | O4 (delta=0, actions=0 flags=1) |

- **Probes.** My round-1 probes R3, R4 and R5 still catch the same edits.
- **Committed campaign:** all three arms are KILLED by their required assertion.
- **Receipts:** `receipts/my-mutants/`, `receipts/campaign/`.

### R375-1 F2: evidence

- **Committed campaign:**
  - `r-cancel-latch-dropped`: O1.
  - `r-cancel-consumes-new-intent`: O2.
  - `r-join-start-guard-dropped`: O3 and O4.
  - `r-sink-receive-priority-lost`: O5 at delta=0 for both sink types.
- **Full default suite.** I also ran `r-cancel-latch-dropped` and `r-sink-receive-priority-lost` against the full default suite: 1986/1987 and 1985/1987 respectively.
- **Patch fidelity.** All 19 reviewer edits from both published reviewer scripts are byte-identical to the committed patches (`receipts/reviewer-edit-vs-committed-patch.txt`).

### R374-1 F3: evidence

- **Documentation.** `10_srp_engine.md:514-522` states the bound:
  - the cost is one shared standard slot plus delayed MVRP drains;
  - with the link up, the bound is at most `T-MRP-PERIODIC` plus one `T-MRP-JOIN`;
  - with the link down, it is at most `T-MRP-LEAVEALL` plus `T-MRP-JOIN`, absent further cancellation;
  - it states that repeated cancellation on a down link has no finite bound, and that reset clears the pool.
- **Why not release the handle.** I checked the `KL_pp_tx_slots` port list. It has no abort for an ALLOC slot; `release_valid_i` frees only pinned slots. That makes releasing the handle non-local, so documenting the bound is the fallback the manager accepted.
- **Measurements:**
  - O7 measures 649 ms against a 1200 ms bound, and `canceled-content-never-drains` is KILLED (O7).
  - My probe R2 at head still measures a 654 ms dwell.
- **Down-link case.** `link_up_i` is the physical link level (`KL_srp_top.sv:132`), so the unbounded down-link case needs RX while the link is down. The documented limit is conservative.

### R374-1 F4 / R375-1 F4: evidence

- **Published sources and hashes.** `author-r2/` publishes `reproduce.cpp` (`a509453e…`) and `run_reproduction.py` (`d7ecb4ce…`). These are the hashes recorded in round 1. It also publishes the patch, `reproduce-deadline.cpp` (`a3ee0057…`) and a portable `run_parent.py`.
- **My re-run at head** (`scripts/replay_parent.sh`):
  - original oracle: rc 1, expected (LV-anchored);
  - fixed oracle: rc 0;
  - deadline oracle: rc 0.
  - The deadline sweep stops ACTIVE at -50, -1, +1, +40 and +80 ms, and retains it (legitimate post-`sLA` LV) at +120 and +199 ms.
  - The regenerated `reproduce-deadline.cpp` is byte-identical (`a3ee0057…`).
- **Base control.** The same deadline oracle against base `16be6768` fails: `FAIL: timer expiry prematurely aged registrar`, rc 1. The proof discriminates.
- **Manager decision.** The manager's decision (5861796018) settles the proof wording.

## Lens evidence

### Conformance: CLEAN

- **RTL unchanged.** `git diff cf4e5c63 00b5c6c9 -- hdl` is empty. The round-1 conformance analysis therefore still applies:
  - `sLA` is the preparation/reuse acceptance edge (802.1Q-2014 §10.7.9, Table 10-5);
  - receive priority on that edge is: registering event, then Leave, then LeaveAll;
  - LV + rLv (Table 10-4 as documented) is unchanged;
  - #108 is unchanged: peer supersession neither restarts nor redraws the timer.
- **Probe R1 at head** (`receipts/probe-head-r374r1.log`, 144 offsets): a Listener Leave from -3 to +103 ms after the 14096 ms expiry clears IN and stops. The first retained LV is at +104 ms, on the 14200 ms `sLA` clock. This is identical to round 1.
- **Parent proof.** The parent deadline-anchored proof passes at head and fails at base (see R374-1 F4 above).
- **New O cases vs §6.5 and issue #127:**
  - O3 and O4 check that a peer LeaveAll before or on the acceptance edge supersedes the own action, and after it does not.
  - O5 checks the sink-plane Leave-before-LeaveAll priority at -1/0/+1.
  - O2 checks that a newer own intent survives a canceled acceptance.

### RTL: CLEAN

- **No RTL delta.** All 50 production files are byte-identical to `cf4e5c63`, which my round-1 review found correct.
- **Lint.** `scripts/lint_hdl.sh` with the pinned simulator: rc 0, 40 modules LINT OK (`receipts/head-lint.log`).
- **Testbench wrapper.** The only HDL-adjacent change is `tb/srp_encoder/srp_tb_wrap.sv`. It connects `la_prepare_i`, `la_prepare_done_o` and `la_tx_o` to testbench ports; `la_cancel_i` stays tied to 0, and the other unit cases drive `enc_la_prepare_i = 0` (`bring_out_of_reset`). Encoder 562/562.

### Robustness: CLEAN

- **Canceled empty reservation.** Its bound is documented and pinned (see R374-1 F3 above).
- **O1: busy encoder.** A peer LeaveAll arrives while preparation waits behind a held TX request, and the cancellation latch survives.
- **O2: blocked allocation.** A newer expiry arrives while allocation stays blocked after a cancel, and exactly one own action follows.
- **O6: coalescing.** Coalesced cadence ticks produce exactly one follow-up walk. All three cases pass at head.
- **O8: same-cycle arbitration.** An MVRP tick and VID push on the preparation clock leave MVRP intake open, and both VIDs drain later.
- **DUT-clock budget.** The full default suite uses 103,847,705 clocks of the 200,000,000 budget (52%). By group: phases 28.5M, edge 16.1M, peer 13.6M, congestion 3.1M, guards 35.8M (`receipts/probe-total-cycles.log`). A budget exit counts as UNPROVEN, never as a kill (`mutants.py:116`).
- **Unit suites.** The encoder and stream-FSM loops are bounded by data length. The DUT waits in the new srp_top cases carry explicit guards, and the global budget covers `until_ms`.

### Tests: UNCLEAN (N1)

- **Suites at head,** pinned Verilator 5.050, builds capped at 8 jobs:

  | Suite | Result |
  |---|---|
  | `srp_top` | 1987/1987 (README `:14` says 1987) |
  | `srp_encoder` | 562/562 |
  | `srp_stream_fsms` | 1215/1215 |
  | `srp_decoder` | 190/190 |
  | `pp_top` | 7751/7751 |

  The no-storm counts are 4, 3, 3, 3, 3, 2 against the unchanged limits.
- **Committed campaign.** I re-executed the full committed campaign (`tb/srp_top/mutants.py`) in eight arm chunks plus one required-arm pair (`scripts/run_campaign_chunk.sh`):
  - all 7 positive controls PASS;
  - **56/56 arms are KILLED** by their own required assertion;
  - the union of killed assertion families is **49/49** (K1–K12, L1–L4, M1–M12, N1–N13, O1–O8);
  - receipts: `receipts/campaign-summary.txt` and `receipts/campaign/`.
- **My eight round-1 mutants,** re-applied verbatim, all fail the full default suite:

  | Mutant | Failures | Assertions |
  |---|---|---|
  | `my-expiry-pulse` | 95 | K2, K4, K5, K11, K12, L2, M7, M10, N1, N2, N11, O3, O5 |
  | `my-join-edge-peer` | 2 | O3, O4 |
  | `my-cancel-eats-new-intent` | 1 | O2 |
  | `my-reuse-flags-ignore-cancel` | 1 | O4 |
  | `my-drop-join-during-wait` | 1 | O6 |
  | `my-edge-cancel-lost` | 3 | M6, M7, O4 |
  | `my-la-outranks-leave` | 2 | L2 |
  | `my-no-walk-at-sLA` | 30 | F1–F5, M2, M6, M10–M12, N5, N6, N10, N12, N13, O2, O4, O6, O7 |

- **Test design.** The new cases calibrate each timing point, then assert the measured placement: `placed`, `seen == 7`, and O4 `prep_cycles[0] == acceptance`. A sweep that drifts off -1/0/+1 therefore fails instead of passing vacuously. No DUT event is forced.
- **Hosted CI at this exact head.** Six check runs executed and succeeded (suites, portability and docs-gates, twice each). None were skipped (`receipts/head-check-runs.json`). The manager owns hosted/act acceptance.
- **Open item:** N1, the donor-bank `git diff --check` failure, which is attributable to the new test artifacts.

### Docs: CLEAN

- **§6.5 paragraph.** The new paragraph in `10_srp_engine.md` matches the RTL and `08_timing.md`: `T-MRP-PERIODIC` is 1000 ms, `T-MRP-JOIN` is 200 ms, and `T-MRP-LEAVEALL` is 10–15 s.
- **srp_top README.** The Round 2 table (O1–O8) and the campaign table match my runs: the failing counts and tags for all 20 listed arms are identical, and the "64 checks: 64 PASS" arithmetic (7 controls + 56 arms + 1 coverage check) holds.
- **srp_encoder README.** The 562 count and the O8 note are correct.
- **srp_stream_fsms README.** The 1203 and 1211 counts are correct.
- **Docs gates.** `make links matrix modmatrix params stale` all return rc 0 at head (`receipts/head-make-*.log`).
- **Wording.** No wording for LV + rLv or #108 changed.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Unchanged `hdl/` (empty delta) against 802.1Q-2014 §10.7.9, Table 10-4/10-5, Δ13, #108 and the #608 decision; §6.5; probe R1 at head (`receipts/probe-head-r374r1.log`); parent replay at head and base (`receipts/replay-*`) | R374-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |
| RTL | CLEAN | 0-line `hdl/` delta; `tb/srp_encoder/srp_tb_wrap.sv` diff; `KL_pp_tx_slots.sv` port list; lint (`receipts/head-lint.log`); `pp_top` 7751/7751 | R374-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |
| Robustness | CLEAN | O1, O2, O6, O7, O8 at head; probes R2–R5 (`receipts/probe-head-r374r2..5.log`); DUT-clock budget measurement (`receipts/probe-total-cycles.log`); slot-hold bound in §6.5 | R374-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |
| Tests | UNCLEAN (N1 MINOR) | `tb/srp_top/sim_main.cpp`, `mutants.py`, 56 `mutations/*.patch`, `tb/srp_encoder/sim_main.cpp`; 5 suites; full committed campaign 56/56 and 49/49 (`receipts/campaign*`); 8 own and 2 external full-suite mutants (`receipts/my-mutants/`); patch fidelity (`receipts/reviewer-edit-vs-committed-patch.txt`); parent checkers (`receipts/parent-*.log`); `git diff --check` (`receipts/git-diff-check.log`); manager comments 5862222946 and 5862231642; hosted check runs | R374-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |
| Docs | CLEAN | `10_srp_engine.md` §6.5 delta against `08_timing.md` and the RTL; the `tb/srp_top`, `tb/srp_encoder` and `tb/srp_stream_fsms` READMEs; `make links matrix modmatrix params stale` (`receipts/head-make-*.log`) | R374-2 | 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c |

## Real limits

- **Simulator path.** The assigned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, sha256 `905795b9…`. That is byte-identical to the manager's `pp127-manager-00b5c6c9` wrapper, and it reports Verilator 5.050 rev v5.050. Hashes are in `receipts/tool-identity.txt`.
- **Parent consumer set.** I ran only the three repaired parent checkers, in a scratch parent. The full 11-command consumer set and the donor bank are the manager's receipts (11/11, and 8/9 with N1). I did not run the full parent, processor, gPTP, Yosys or builder banks, `srp_admission`, act, or hardware.
- **Bank-status wording.** The assignment text says the manager's source banks passed at this head. The manager's later public comment 5862222946 records donor bank 8/9, and this review follows that comment.
- **Replay scope.** The replay measures the SRP ACTIVE licence in simulation. It has no AVTP framer, no CRF STREAM_STOP count and no hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Compressed time.** Probes and O cases use the testbench's compressed time (1 ms = 40 clocks).
- **Same-round report.** The same-round external report (R375-2) was posted during this review. I did not consult it.

## Pending manager duties

1. After N1 is fixed, re-run the donor bank to 9/9 and confirm the parent consumer set stays 11/11 at the new head.
2. At pin adoption, add the CRF frame/STREAM_STOP integration regression required by issue #127, and schedule the bench re-measurement for #608.
3. At the merge turn, build and gate the final current-dev candidate (source base `16be6768`, live dev `931f396e`), which is separate from this source validation. Own hosted/act acceptance.
4. Archive this packet. Only `REPORT.md` and the files listed in `MANIFEST.sha256` are publishable.

## Reproduction

Run the scripts in `scripts/` from this packet directory. Set `VERILATOR` or `JOBS` to override the pinned wrapper or the default of 8 compile jobs.

- **Suites:** `scripts/run_suite.sh <tree> <suite> [group]`.
- **Committed campaign chunk:** `scripts/run_campaign_chunk.sh <tree> <out> <4|8> <arm,...>`.
- **Own mutants on the full suite:** `python3 scripts/r374_2_mutants.py <tree> <out> [names]`. This uses `install_probe.py` and `r374_probe.cpp.inc`.
- **Committed patch on the full suite:** `scripts/run_patch_full.sh <tree> <scratch> <arm>`.
- **Patch fidelity:** `python3 scripts/compare_reviewer_edits.py <tree> <r374_mutants.py> <r375_run.py> <scratch>`.
- **Parent replay and base control:** `scripts/replay_parent.sh <author-r2 dir> <head clone> <base clone> <scratch> <out>`.
- **Parent checkers:** `scripts/parent_gates.sh <processor clone> <scratch> <out>`.

After all probes, I verified the review clone against the exact head (`receipts/clone-integrity.txt`):

- HEAD is `00b5c6c9…`, and both the HEAD tree and the index tree are `95f398f3…`;
- all 306 tracked blobs and modes match, with 0 mismatches;
- there are no untracked or ignored files;
- the repository has no submodule gitlinks and no `.gitmodules`.

R374-2 FINISHED
