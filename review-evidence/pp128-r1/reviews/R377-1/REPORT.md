[R377] NEGATIVE - exact head 9476898b28ffc8f77b2aa5f873f3899a17287d3a

# R377-1: external independent review of processor PR #129 / issue #128

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `9476898b28ffc8f77b2aa5f873f3899a17287d3a`, tree `0a41c0be33df4fa4113f2c4ac752e7a976487369`
- Base: `16be6768f710e79450aace277abacd6c2c3336e5` (the parent's current pin). One commit.
- Review start: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/129#issuecomment-5861363402

## Verdict summary

The retry design is sound and does fix the parent's #606 first-probe failure.

- **What the head does.** Enabled `GS_NO_DA` sources are revisited every 100 ms, in rotating order. Commands and pending events alternate. Obsolete grants are released without being installed. Backoff and freshness are untouched. The port and parameter interface is identical to the base.
- **Checks the head passes.**
  - All 13 ACMP, SRP, MAAP, top and related suites I ran.
  - The author's 28 mutants, reproduced.
  - 47 new reviewer probe checks.
  - A reconstructed real-shim parent harness.
- **Why NEGATIVE.** Four MINOR findings stay open:
  - one language-conformance defect, which the parent's consumer gates flag;
  - one test-evidence rule violation, also flagged by the parent's consumer gates;
  - a set of non-equivalent mutants the suite no longer kills;
  - an undeclared consumer-visible behaviour change that fails parent integration checks.

  None of them is a functional defect of the retry mechanism at this head.

## Reconstruction (in order)

1. **Contribution rules.** There is no `AGENTS.md` or `CONTRIBUTING.md` in the processor repository. I read `README.md` and `docs/README.md`. The latter covers conventions, the single-source rules for timing values (F08.1) and parameters (F01.5), and the editing workflow.
2. **Issue #128.** I read the body plus the manager's assignment comment 5861093499. The frozen scope:
   - bounded, fair reattempts in `GS_NO_DA`;
   - honest failure is kept;
   - no retry storm and no command starvation;
   - no change to conflict or PCP backoff;
   - no interface change;
   - every new check pinned by a killed mutant;
   - the parent harness returns first-probe success.
3. **Linked authorities.**
   - Parent issue kebag-logic/milan-fpga#606 and its analysis comment 5860869610.
   - Parent `hdl/milan/KL_pp_maap_shim.sv` @ `931f396e`, sha256 `965fbee0…`.
   - Processor docs: 02 §4.2 maap face, 05 §6bis, 08 F08.1, `hdl/maap/KL_pp_maap.sv` allocator seam.
4. **Diff and history.** `git diff 16be6768..9476898b`: 10 files, +680/−63; the only RTL file is `hdl/acmp/KL_acmp_talker.sv`.
5. **Public evidence.**
   - Packet `kebag-logic/milan-fpga@b367df5d:review-evidence/pp128-r1`: all 48 MANIFEST entries hash-verified.
   - Hosted check runs at the exact head.
   - Manager comments 5861504990 and 5861562548 on the PR.
   - The manager's consumer-gate receipts for candidate `13fd3b68` on parent base `931f396e`, read as they landed.
6. **Prior review findings.** There were none on this PR at review time. The only other entries are review-start notices.

## Findings

### F1: MINOR. A signal is used before its declaration (new in this PR)

- **Lenses:** RTL, Conformance
- **Where:** `hdl/acmp/KL_acmp_talker.sv:891` (use of `set_conflict_w` inside `always_ff retry_round`); `hdl/acmp/KL_acmp_talker.sv:1110` (its declaration).
- **Authority / evidence:**
  - IEEE 1800 requires declare-before-use for module-scope variables.
  - The reference platform's Vivado front end reports it as VRFC 10-3380. The manager's parent consumer gate `scripts/xvlog_gate.py --check` goes over its ratchet at this head (comment 5861504990/5861562548).
  - Independent static scan `receipts/forward-ref.txt`: 1 forward reference at the head, 0 at the base.
  - Verilator tolerates it, so the processor's own lint (`receipts/gates.txt`: clean for `KL_acmp_talker` and `protocol_processor_top`) cannot catch it.
- **Impact:** The pin-adopting candidate fails a parent consumer gate. Tools that enforce the LRM may reject or mis-elaborate the module.
- **Required outcome:** Declare `set_conflict_w` (or the `pe_sets` declarations) before `retry_round`, or move `retry_round` below `pe_sets`, with no behaviour change.
- **Verification:**
  - `scripts/forward_ref_check.sh` reports 0 forward references at the new head.
  - `acmp_talker` and `pp_top` stay green.
  - The parent `xvlog_gate.py --check` is back within its ratchet on the pin-adopting candidate.

### F2: MINOR. The new mutation driver breaks the parent's test-evidence rules

- **Lenses:** Tests, Conformance
- **Where:** `tb/acmp_talker/retry_mutants.py:59` (`subprocess.run(..., timeout=900, ...)`); `tb/acmp_talker/retry_mutants.py:85-86` (reads the production RTL).
- **Authority / evidence:**
  - The parent's `scripts/measure_test_evidence.py` (@931f396e, sha256 `bfa1e442…`), rule 4: "New behavioral tests use DUT cycles, not host time."
  - The manager receipt (10.log, `receipts/manager-consumer-extract.txt`) reports `FAIL: 4 wall-clock-dependent suite file(s) > ratchet 3`, naming this file, and `FAIL: 1 unexplained DUT-source reader(s) > ratchet 0`, again naming this file.
  - I ran the parent's own classifier over every processor `tb/*/*.py` (`receipts/wall-clock-classifier.txt`). Only `retry_mutants.py` is True. The same file with the `timeout` keyword removed is False.
- **Impact:** The pin-adopting candidate fails the parent's test-evidence gate. A host-time deadline makes a mutant verdict depend on machine speed.
- **Required outcome:**
  - Processor side: remove the host deadline from `retry_mutants.py`. The simulation is already cycle-bounded; the other processor mutation drivers use no host deadline.
  - Consumer lane: add a `DUT_READER_DISPOSITIONS` entry for this reader (a manager duty, since the table is parent-side).
- **Verification:** The parent `measure_test_evidence.py --check` passes on the pin-adopting candidate, and the driver still kills all its mutants.

### F3: MINOR. Five non-equivalent mutants of acceptance-relevant logic survive the suite

- **Lenses:** Tests
- **Where:**
  - `hdl/acmp/KL_acmp_talker.sv:597`, the `maap_avail_w &&` term of `txn_eligible_w`;
  - `:891`, the `set_conflict_w[i]` restart of the pacing bit;
  - `:1145`, the probe-driven `set_init_w`;
  - `:843`, the listener-driven `ev_initset_w`;
  - `:815`, the backoff-exit `ev_initset_w`.
- **Evidence** (reviewer mutants, pinned 5.050; `receipts/mutants/summary-acmp_talker.txt`, `receipts/mutants-demand/summary-acmp_talker.txt`, `receipts/probes/summary-probes.txt`, `receipts/base-demand/summary-base-demand.txt`). Each row survives the head suite (1107/1107 pass) and is killed by a reviewer probe; the head RTL passes every probe (1154/1154).

  | Mutant | What it breaks | Killed by |
  |---|---|---|
  | `init_elig_no_avail` | Commands **starve** while an accepted allocation sits unanswered with another source's retry pending: after one command, the walker idles for up to `P-MAAP-RSP-MS` (10 s). This violates "no starving of solicited commands" and the response budget. The existing K3 check sends only one command in that state. | probe P1: command 1 not consumed in 4096 cycles |
  | `no_conflict_wait_clear` | The documented rule "conflict starts a new acquisition lifetime" (05 §6bis) is lost. A `DA_OK` source conflicted in the round it acquired waits for the next round. That is a change to pre-#128 conflict handling. | P2, P4, P5, P6 |
  | `no_probe_initset` | The probe-driven attempt path. | P5 |
  | `no_lsn_initset` | The listener-driven attempt path. | P6 |
  | `no_backoff_exit_initset` | The F05.12 arc "backoff expiry without DA re-enters `NO_DA` + `ALLOC_DA`". | P4 |

  The last three were killed by the **base** suite (I4, I3, E3 at `16be6768`) and are no longer killed at the head. The new time steps line up with retry-round boundaries and mask them:
  - `tb/acmp_talker/sim_main.cpp:836` adds `+= 100`;
  - `tb/acmp_talker/retry_cases.hpp:207` fires the backoff expiry at 20100, exactly on a round boundary.
- **Impact:**
  - The response-budget property that the issue requires is not protected against regression.
  - Protection that the suite had before this PR is lost for three demand paths.
  - The author's claim covers assertion sites (38/38, reproduced: `receipts/author-mutants/coverage.txt` is byte-identical to the author's), not these RTL terms.
- **Required outcome:** Add regressions equivalent to reviewer probes P1, P2 and P4–P6 (`scripts/probe_cases.hpp`), and add these five mutants to the `retry_mutants.py` table.
- **Verification:** All five are killed by the suite's own checks; the head stays green.

### F4: MINOR. A consumer-visible behaviour change on the maap face is undeclared, and parent integration checks fail

- **Lenses:** Conformance, Docs
- **Where:**
  - PR body and the author handoff ("the parent interface … unchanged"; the consumer-needs paragraph);
  - `docs/architecture/05_acmp_engine.md:411-449`;
  - `docs/architecture/02_interfaces.md:264-267`.
- **Evidence:**
  - The manager's `make -C tb/verilator/pp_shadow` on the pin-adopting candidate (07.log, `receipts/manager-consumer-extract.txt`).
  - Section `[H]`, "the processor ASKED and the shim ACCEPTED — no request seen", fails in the base, vid73 and crf builds.
  - The **crf build also fails `[I]` "granted DA == KL_maap base + source index"**. That is 2 failures in crf; the manager's comment 5861504990 names only `[H]`.
  - I read the parent test at 931f396e (`tb/verilator/pp_shadow/sim_main.cpp`, sha256 `c9062587…`, `grade_maap_refuses_without_wedging` and `grade_maap_grants_and_opens_the_da_gate`). Both failures are expectations of the old stimulus-driven behaviour:
    - `[H]` expects a PROBE_TX in `NO_DA` to produce an `ALLOC_DA` within 4000 cycles. At this head a probe inside a round that has already attempted is deferred to the next round (05: "one attempt per source per round, including probe/listener-triggered requests").
    - `[I]` reads `mo.last_da` as source 0's grant. At this head the round also acquires source 1 (the CRF output) in the same window, so the last grant is source 1's.
- **Reviewer judgment:** The processor behaviour is the intended, sound consequence of automatic paced retries. The parent expectations are stale. No processor RTL change is required for F4.
- **Impact:** The pin cannot be adopted until the parent reconciles the difference. The assignment asked the author to "record what the parent test needs". The handoff asks for a new real-shim regression but does not name the two existing parent checks this change invalidates, or why.
- **Required outcome:**
  - Record the reconciliation reason in the PR and handoff. Optionally add a one-line consumer note to 02 §4.2: a probe no longer forces an immediate `ALLOC_DA` within a round, and all enabled in-block sources auto-acquire.
  - Consumer lane (a manager duty): update `[H]` to allow one retry round (or count the startup attempt), and key the `[I]` DA check by source index.
- **Verification:** pp_shadow is green in all four builds on the pin-adopting candidate, with the reason cited.

### Suggestions (do not affect the verdict)

- **S1 (Tests, RTL).** Several single terms are unpinned because they are mutually redundant or only matter in exact-cycle races:
  - `no_sticky_gp_window`, `grant_kill_reg_only`, `accept_kill_zero`, `kill_no_pending_conflict`, `kill_no_live_conflict` and `kill_no_disable` (`:476-483`, `:733`, `:1076-1084`);
  - `init_ignores_off_conflict` (`:866-867`);
  - `elig_drop_rel` and `elig_drop_off` (`:595-596`);
  - `no_reenable_wait_clear`. The `!en_q_r[i]` term at `:891` is logically redundant, because `!cfg_src_en_i[i]` already clears the bit throughout a disable.

  Removing each whole cause is killed (`receipts/mutants-kill/summary-acmp_talker.txt`: conflict, disable and the sticky set all fail R4). Either simplify the logic or add exact-cycle race tests. The 05 claim that commands alternate with *all* pending events is pinned only for retry events.
- **S2 (Tests, Docs).** Publish the #606 wiring runner (`run_first_probe.py`, its wrapper, and the original defect-asserting oracle) with hashes. The packet contains only the adapted oracle, so reproducing the harness required my own wrapper (`scripts/first_probe_wrap.sv`). Its block base `91:E0:F0:00:68:17` is inferred from the oracle constant.
- **S3 (Docs).** The talker banner at `hdl/acmp/KL_acmp_talker.sv:174-176` still says an allocation is "requested by a stimulus — normally the PROBE_TX". The operator guide's `TALKER_DEST_MAC_FAILED` row (`docs/guides/operator.md:282`) could add "or the allocator became available less than one `T-ACMP-DA-RETRY` ago".

## Assignment verification items

1. **Retry behaviour.** Met at the head.
   - R1 and the reconstructed parent harness show acquisition without a probe after a round.
   - R2, R7 and probe P3 show honest status 3 with no DA.
   - Disabled sources stay quiet (R2).
   - Out-of-block sources are paced (R7, P3: exactly one attempt per source per round).
   - Rotating fairness is shown by R3 and the reviewer mutant `no_rotate_advance` (killed).
   - Backoff and timers are untouched (R6).
   - The walker is bounded by `P-MAAP-ACCEPT-CYC` (R3, P1, P3: maximum wait ≤ 1088 cycles).
   - Protection of the command-starvation property is incomplete (F3).
2. **No interface change.** Met at port and parameter level.
   - `receipts/interface.txt`: the talker's declarations are identical with comments stripped.
   - `protocol_processor_top.sv` and `KL_pp_maap.sv` blobs are unchanged.
   - Only the talker changed under `hdl/`.
   - The behavioural contract on the maap face did change, as the issue intends; that is covered by F4.
3. **Test coverage and mutants.** All required scenario classes are covered (R1–R8, updated S10 and MP3).
   - The pre-fix RTL fails 38 new talker checks, and fails the head `pp_top` S10 and MP3 checks (`receipts/mutants-pp_top`).
   - The author's 28/28 kills reproduce with the pinned tool (`receipts/author-mutants`).
   - Of my 26 planted mutants, 11 are killed. 5 non-equivalent survivors are open under F3. The other 10 survivors are redundant or race-only terms (S1).
4. **Parent harness.** Reproduced with the real talker at the head, the real parent shim (sha256 `965fbee0…`) and the published oracle (sha256 `9a195388…`): first probe status 0, DA `91e0f0006818`, harness rc 0 (`receipts/parent-first-probe-9476898b.txt`). The base RTL fails the same oracle: "automatic retry sweep missing", rc 1 (`receipts/parent-first-probe-16be6768.txt`). The packet lacks the wiring runner (S2).
5. **Existing suites.** All pass with pinned Verilator 5.050 (`receipts/suites/summary.txt`):
   - `acmp_talker` 1107, `acmp_listener` 2544, `acmp_nvm` 349, `pp_top` 7751, `maap` 75;
   - `srp_decoder` 190, `srp_encoder` 556, `srp_stream_fsms` 1087, `srp_top` 1531, `srp_admission` 991231;
   - `timer_service` 48, `dispatch` 211, `scoreboard` 3705.

   The counts match the author's receipts. Other gates:
   - `make check` passes (docs, figures, links, matrix, parameters).
   - `gen_matrix --check` passes (92 rows, 0 untested).
   - Talker `make lint` is clean (`receipts/gates.txt`).

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F4) | issue #128 frozen scope and assignment; parent #606 and its analysis; parent shim @931f396e; processor 02 §4.2, 05 §6bis, 08 F08.1, 01 single-source rules; port/parameter diff; manager consumer receipts (xvlog, pp_shadow, test-evidence); parent pp_shadow bench and evidence gate @931f396e | R377-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |
| RTL | UNCLEAN (F1) | full read of `hdl/acmp/KL_acmp_talker.sv` at the head (retry round, picker, eligibility, kill tracker, EVC_INIT guards, `txn_ready_o`); top instance wiring; internal MAAP allocator seam; declare-before-use scan; lint of talker and top | R377-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |
| Robustness | CLEAN | bounded walker and response wait (R3, P1, P3); absent, silent and refusing allocators; stale-credit saturation (R5); obsolete-grant release (R4 plus whole-cause mutants); wrap (R5, R8); disable/re-enable, conflict and PCP (R2, R4, R6); real-shim harness; no wire-traffic amplification (both allocators answer ALLOC locally in one cycle) | R377-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |
| Tests | UNCLEAN (F2, F3) | `retry_cases.hpp`, `retry_mutants.py`, `sim_main.cpp` edits, `pp_top` S10/MP3; author driver rerun (28/28, coverage identical); 26 reviewer mutants; pre-fix RTL on talker and `pp_top`; base-suite demand mutants; 47 probe checks; the parent's wall-clock classifier | R377-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |
| Docs | UNCLEAN (F4) | 02, 05 and 08 diffs; `tb/acmp_talker` and `tb/pp_top` READMEs; talker banner; integrator and operator guides; PR body and handoff consumer notes; `make check` | R377-1 | 9476898b28ffc8f77b2aa5f873f3899a17287d3a |

## Receipts and scripts (listed in MANIFEST.sha256)

The scripts are portable: each takes the clone, the revisions, the scratch directory and the simulator path as arguments, and none writes to the clone.

| Script | What it does |
|---|---|
| `scripts/run_suites_subset.sh` | runs the named suites from a `git archive` export |
| `scripts/reviewer_mutants.py` | 26 reviewer mutants; a missing tally is never counted as a kill |
| `scripts/probe_cases.hpp`, `scripts/run_probe_cases.sh` | reviewer probes P1–P6, at the head and under the mutants |
| `scripts/base_demand_mutants.sh` | demand-path mutants planted in the base with its own tests |
| `scripts/first_probe_wrap.sv`, `scripts/parent_first_probe.sh` | reconstructed parent harness |
| `scripts/forward_ref_check.sh` | declare-before-use scan |
| `scripts/check_wall_clock.py` | applies the parent's classifier to processor scripts |

Receipts are under `receipts/`, with host paths redacted to `<HOME>`, `<TOOLROOT>` and `<LANE>`:
- `inputs.txt` (hashes of every fetched input);
- `manager-consumer-extract.txt`;
- `hosted-checks.txt`;
- `clone-integrity.txt`;
- `incident-wrapper-overwrite.txt`.

## Incident disclosure

One of my own commands passed its arguments in swapped order, and a log redirect overwrote the manager's pinned simulator wrapper `$VALIDATION_STORAGE/pp128-manager-9476898b/pinned-tool-bin/verilator`. The overwrite lasted from about 03:00:48 to 03:01:14 CEST.

- **Restore.** I restored it byte-exact from a sibling wrapper with the same sha256 (`905795b9…`, verified), kept the mode, and set the mtime from its directory.
- **Overlap.** The manager's parent-consumer run finished inside that window, at 03:01:04 with exit 1. Its pp_shadow binaries had been built beforehand, and its failures are simulation assertions with tallies. In my judgment they were not caused by the overwrite. Even so, re-run any step that may have invoked the wrapper during the window.
- **Guard.** The script now refuses an existing or non-`.txt` log path.
- **Other writes outside the packet.** A single transient list file was written to `/tmp` and deleted in the same command.

The full record is in `receipts/incident-wrapper-overwrite.txt`.

## Real limits

- I did not run the parent's bank or pp_shadow myself. The pin-adopting candidate `13fd3b68` is not public, so those results come from the manager's receipts; my part is reading the public parent test source.
- The first-probe harness wrapper is my reconstruction, not the unpublished #606 runner.
- The pinned simulator path named in the brief did not exist. I used the manager's per-PR pinned wrapper (`pp128-manager-9476898b`), whose identity is verified as Verilator 5.050.
- I ran only a subset of processor suites (13 of 33), plus talker and top lint, `make check` and the matrix check. I did not run the full processor, Yosys or portability banks.
- No physical calibration, hardware or field evidence was involved. Simulation is not hardware proof.
- The reference peer's 6.877 s retry interval and the bench's allocator history are not modelled.
- Hosted CI: all six runs at the exact head executed and succeeded, and none was skipped. Hosted and act acceptance belong to the manager.
- No interface-level formal proof. The alternation bound is argued from the RTL plus bounded-scenario tests.

## Pending manager duties

- Re-run the parent-consumer steps that could have overlapped the incident window.
- Consumer lane, for the pin-adopting candidate:
  - reconcile pp_shadow `[H]` (all three 591-check builds) and `[I]` "granted DA" (crf build) with the reason (F4);
  - add a `DUT_READER_DISPOSITIONS` entry for `retry_mutants.py` (F2);
  - re-run xvlog after F1 is fixed;
  - add the real-shim first-probe regression with the 100 ms plus sweep allowance;
  - adopt the pin only after the gates pass.
- Build and validate the final current-dev candidate at the merge turn (source base `16be6768`, live dev `931f396e`), which is distinct from this source validation.
- Hosted and act acceptance.

R377-1 FINISHED
