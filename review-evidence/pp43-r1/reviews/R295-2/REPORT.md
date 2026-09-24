[R295] POSITIVE - exact head a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72

# R295-2 independent external review: PR #111 (issues #43, #49), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72`, tree `71081cc12048a81b920dc48b9a508e3b120b96e3`.
  - Verified in the clone: HEAD, HEAD^{tree} and the index write-tree all match.
  - Every tracked blob and mode matches the worktree. No status lines.
  - This repository has no gitlinks and no `.gitmodules` (`receipts/clone_integrity.txt`).
- Source base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`.
  - Reviewed diff: `939c143..a14ef8b`, 26 files, +1264/-130.
  - Round-2 delta: `5771578..a14ef8b`, three commits (`f28e90b`, `68ad935`, `a14ef8b`), 23 files.
- Reviewer role: external, with a cleared context and its own detached clone. I made no source edits, commits, pushes or GitHub writes. Every probe and mutant ran in extracted copies under the packet's `scratch/`.

## Verdict

**POSITIVE.** All three round-1 findings from this reviewer are resolved at this head:

- **R295-1 F1:** the re-bind started/stopped notification.
- **R295-1 F2:** the FailureInformation change re-declaring the Listener with New.
- **R295-1 F3:** the untested sample-and-hold, now removed by manager decision.

The four round-1 suggestions have also been taken. The other round-1 reviewer's public findings, which I read only after writing this verdict and ledger, are also resolved (Section 4b): R294-1-F1 MAJOR, S1 and S2. R294-1-S3 is taken except for one item outside this diff, which remains a suggestion.

Round-1 probes and mutants, rerun unchanged:

- Probes R1, R2 and R3 now pass, 8 of 8 checks.
- Mutants on unchanged sites are killed. That includes `sink-index-guard-removed`, which survived in round 1.

A new round-2 probe set passed 16 of 16 at head:

- **R4:** a changed FailureInformation adds no Listener declaration of any event type. Only the periodic JoinMt follows, as after an unchanged refresh.
- **R6:** the latency-only residual is the same on base and head.
- **R7:** a re-bind that moves pbsta and started/stopped in one write gives exactly one frame.

Mutants and suites:

- 16 reviewer mutant runs at this head: the 3 unchanged round-1 sites, 1 re-expressed round-1 site and 12 runs on the new code. 13 are killed. 3 runs survive; they cover two edits, neither with any effect at the response level (S1 and S2 below).
- All 13 of the author's retained mutants are killed by their named checks. Golden and restored runs are clean.
- Four focused suites pass with the pinned simulator.

I have no open MINOR, MAJOR or BLOCKER finding.

## 1. Reconstruction (in the prescribed order)

1. **Guidance.** There is no `AGENTS.md` or `CONTRIBUTING.md` at this head (checked with `git ls-files`).
   - `README.md` names the gates: `run_suites.sh`, `lint_hdl.sh` and `make check`.
   - `docs/README.md` sets the single-source rules: F02.10 holds the status names and F06.13 the lineage. `make check` gates any doc edit.
2. **Frozen acceptance.**
   - The bodies of issues #43 and #49.
   - The manager's seam decision [A253] (issue #43 comment 5813138046, the same text on #49): served internally with no new ports, the response-level state list, two distinct sinks, solicited equal to unsolicited, and mutants for zero/wrong-sink/old path.
   - The round-2 decision [A255] (issue #43 comment 5814505442):
     - F1 must notify every committed change, including a re-bind that flips started/stopped. It needs a REBIND test and a retained mutant.
     - F2 needs a separate notify-only strobe: no New and no TK_REGISTERED. It needs a wire test, and FAILED-REFRESH must still notify.
     - F3: remove the hold, read live, state the bound in F06.13, and report the FF saved.
     - Area: gate the bridge once after the mux, compare on the hit sink only, and report the 8x8 and 1x1 deltas against the base.
     - Also: an index-guard test, portable affinity, and `dbg_recwr` named or documented.
3. **Authorities used.**
   - Milan v1.2 as the repository cites it: §5.3.8.6, §5.3.8.7, §5.3.8.8, Table 5.22, and §5.5.3.5.x through the F05.3 matrix (`hdl/acmp/rom/gen_ltn_rom.py`).
   - IEEE 802.1Q MRP applicant and registrar semantics as cited in `KL_srp_listener_fsm.sv`.
   - The repository contracts: F02.10, F06.12/F06.13, 06 §7 and 10 §6.4.
   - The specification PDFs are not in the repository.
4. **Diff and history.** I read every RTL, test and doc hunk of `939c143..a14ef8b`, and the round-2 delta separately.
5. **Public evidence.**
   - `kebag-logic/milan-fpga@87b38a25/review-evidence/pp43-r1`: the tree is listed in `receipts/public_evidence_tree.txt`. I used the `author-r2/area` reports and summary, and the author's reproduced mutant and probe logs as cross-checks only.
   - The [A255] REVIEW READY comment on issue #43 (5816221930).
   - Hosted checks at the exact head: six jobs executed (suites, docs-gates and portability, two runs each), all `success`, none skipped (`receipts/hosted_checks.txt`).
   - The only manager validation comment on the PR (5814055772) is at the round-1 head. Per the brief, the manager's bank pass at this head is a manager receipt that I did not re-run.

## 2. Round-2 RTL, checked against its claims

| Claim | Where | Checked |
|---|---|---|
| One event gives one frame: the started/stopped pulse and the pbsta/acmpsta compare register off the same record write | `KL_pp_acmp_listener.sv:738-765` (`dbg_recwr_o` = combinational `recwr_en_w` in X_WB); `:1418-1422` (`act_strt_chg_o <=` in X_WB); `protocol_processor_top.sv:3053-3073` (`lstn_gsi_changed_r <=` on the same write) | Both assert in cycle X_WB+1 for `sink_r`, and `stri_events` ORs them (`:3133-3142`). Probe R7 shows exactly one frame when both move. |
| Re-bind exclusion removed | `bind_act_r` is deleted, and `act_strt_chg_o` keeps only `bnd_was_r && f_bound` | R1: 1 notification (base 2). The author mutant re-applies the exclusion as `!apend_r[ACT_A2_C]`, which matches the deleted `bind_act_r`: the bitmap is loaded once per walk (`:1141`), not consumed per action, and both clear at walk start (`:922`). |
| Dropped arm/disarm/settle/teardown terms lose no visible change | F05.3 table in `gen_ltn_rom.py:40-98`, pbsta writers `:1230-1308` | Every cell that runs A8, A10, A15, A4/A5, A12/A14/A17 moves pbsta/acmpsta or runs an SRP event. The cells that no longer push are a re-bind in PWR/PW2 with the same STREAMING_WAIT, and BIND_SAME without a STREAMING_WAIT change. Neither changes a GET_STREAM_INFO-visible input field (stream_id/DA/VLAN are only valid once settled). |
| FailureInformation strobe is notify-only | `KL_srp_listener_fsm.sv:453-480, :735`; `KL_srp_top.sv:197, :622`; `protocol_processor_top.sv:2210, :2287, :3141` | `srp_evt_tk_fail_chg_w` has exactly one reader, `stri_events`. `ind_reg_w` is byte-identical to base, so there is no New and no TK_REGISTERED. |
| One comparator on the lowest candidate sink | `:463-479` | Candidates are armed, hit on the exact {stream_id, DA, VLAN} triple, registered (IN/LV) and of Failed type. They entered on a latching event and take every later registering event on that triple (`:723-733`), so their latches are equal. A15/A8 clear to MT and so leave the set. `ind_reg_w` and `ind_fchg_w` are mutually exclusive. |
| Bridge gated once after the index mux | `protocol_processor_top.sv:3096-3106` | Gated on `srp_tk_reg_state_w[gsi_sink_w] == FAILED` inside the full-index guard. The code stays gated at the source (`KL_srp_listener_fsm.sv:849`). |
| Sample-and-hold removed, owners read live | `protocol_processor_top.sv:3075-3118` | There are no `gsi_*_r` registers. F06.13's coherence bound (`06_aecp_engine.md:307-317`) holds: `KL_aecp_notify.sv:758` sets pending and `:987` clears it at the pick, before the gather, so a change landing mid-gather re-pends and gets its own later frame. For a change on the pick cycle itself, the clear wins, but the gather starts after the pick and reads post-change values. |
| Word layout | `gen_ucode.py:1010-1017` | Selector 4 `{dmac, code, 8'0}`, selector 5 bridge, selector 7 `{32'0, pbsta:acmpsta, 24'0}` land at @58, @60 and @76. Validity flags stay the integrator's (selector 0). |

## 3. Executed evidence (all with the pinned simulator)

The simulator identity: `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` is a wrapper script (sha256 `905795b9…e92f`) that reports `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/focused_lint.log`).

| Item | Result | Receipt |
|---|---|---|
| `tb/pp_top` `make run` (default and VID fixture builds) | 1948 PASS, 0 FAIL | `receipts/suites/pp_top.log` |
| `tb/acmp_listener` | 2544 PASS, 0 FAIL | `receipts/suites/acmp_listener.log` |
| `tb/srp_stream_fsms` | 1087 PASS, 0 FAIL | `receipts/suites/srp_stream_fsms.log` |
| `tb/srp_top` | 259 PASS, 0 FAIL | `receipts/suites/srp_top.log` |
| Focused lint: 5 changed tops, plus `protocol_processor_top` at 1x1, 8x8 and 3x5 | all LINT OK | `receipts/focused_lint.log` |
| `scripts/check-links.py` | 846 links OK | `receipts/check_links.log` |
| Round-1 probes, unchanged (`scripts/run_probe.sh`, `r295_probe.hpp`, sha256 equal to the round-1 packet) | head 8/8 PASS: R1 rebind notifications = 1 (started 1→0); R1b 0; R2 changed-refresh New = 0, code 9 served; R3 no leak. Base: R1 = 2, R1b = 2 (duplicates) | `receipts/probe_head.log`, `receipts/probe_base.log` |
| Round-2 probes (`scripts/run_probe2.sh`, `r295_probe2.hpp`) | head 16/16 PASS (details below). Base fails R4, R6 and R7 as expected (no internal path; R7 = 2 frames) | `receipts/probe2_head.log`, `receipts/probe2_base.log` |
| Round-1 mutant script, unchanged (`scripts/r295_mutants.py`) | golden-gi 488/0; `sink-index-guard-removed` KILLED (INDEX-GUARD); `status-compare-removed` KILLED; `desc-type-ignored` KILLED (G2); golden-full 1928/0. The three removed-by-design sites refuse on the site count | `receipts/r295_mutants_r1script*` |
| Round-2 reviewer mutants (`scripts/r295_mutants2.py`) | 16 runs: 13 killed; 3 runs survive (two edits, both without response-level effect: S1, S2) | `receipts/r295_mutants2_a/`, `receipts/r295_mutants2_b/`, `receipts/r295_mutants2_c/` |
| Author's retained mutants, reproduced in parallel with the wrapper's own named-check rule (`scripts/author_mutants_par.py`, which imports `tb/pp_top/gsi_mutants.py` unchanged) | 15/15 verdicts as required: golden and restored 488/0, all 13 killed by their named check | `receipts/author_mutants/`, `receipts/author_mutants.stdout` |
| Area (public reports, parsed here) | 8x8: 28,092→28,326 LUT (+234), 30,354→31,064 FF (+710). 1x1: 20,978→21,245 (+267), 23,446→23,674 (+228). The 1x1 logs show `-generic N_STREAM_IN_P=1 -generic N_STREAM_OUT_P=1` | `receipts/public_area/`, `receipts/public_area_summary.txt` |

**Round-2 probe detail (head):**

- **R4 (a registered Failed on a settled sink).**
  - The first Failed declares New ×2, which is the control.
  - The unchanged refresh gives 2 Listener vectors (JoinMt ×2 periodic).
  - The changed refresh gives 1 Listener vector (JoinMt ×1), with none in its first 250 ms and 0 New.
  - Exactly 1 unsolicited response, carrying code 9, bridge `117d23456789abcd` and pbsta/acmpsta `0x60`.
  - 0 ACMP frames.
- **R6.**
  - Failed→Advertise pushes once, with code and bridge 0 (the bridge is gated after the mux).
  - A latency-only Advertise refresh pushes 0 at head, and 0 on base as well.
- **R7.** A settled, started sink re-bound to another talker with STREAMING_WAIT gives started 1→0 and exactly 1 frame with pbsta/acmpsta `0x40` (ACTIVE/0). Base gives 2 frames.

**Round-2 reviewer mutants:**

| Mutant | Bench | Verdict (first named failure) |
|---|---|---|
| `srp-failure-change-strobe-removed-r2` (round-1 site re-expressed: `ind_fchg_w = 0`) | GI | KILLED: `GI FAILED-REFRESH unsolicited: complete Milan response` |
| `fail-chg-not-routed-to-notify` | GI | KILLED: same check |
| `strt-term-not-routed-to-notify` | GI | KILLED: `GI REBIND-SW: exactly one unsolicited response` |
| `status-compare-wrong-sink` (compare against sink 0's view) | GI | KILLED: `GI BIND-TIMEOUT unsolicited: acmpsta sink 1` |
| `status-view-reads-sink0` | GI | KILLED: `GI BIND-ACTIVE unsolicited: pbsta sink 1` |
| `bridge-gate-reads-sink0-state` | GI | KILLED: `GI DISTINCT-1 solicited: full failure bridge` |
| `fchg-lv-excluded` (LV registrations are not candidates) | srp_stream_fsms | KILLED: L6 |
| `fchg-compare-sink0` | srp_stream_fsms | KILLED: L8, L9 |
| `fchg-recoupled-into-reg` (round-1 coupling folded back into `ind_reg_w`) | srp_stream_fsms | KILLED: 8 of 1087 FAIL (L2, L3, L4, L6, L9) |
| `fchg-recoupled-into-reg` | srp_top | KILLED: 3 of 259 FAIL (D: strobe count, no Listener New on the wire, unchanged refresh) |
| `fchg-compare-sink0-gi` | GI | survives (S2) |
| `strt-bound-before-removed` | acmp_listener and GI | survives (S1) |

**Removed-by-design sites and their re-expression:**

- **`sample-transparent` (GI and full): moot.** The hold it tested is gone by manager decision. Its replacement is the documented live read and coherence bound, which I checked against the notify engine (Section 2). The top's FF delta is −81 against round 1 (public summary).
- **`srp-failure-change-strobe-removed`: re-expressed as `-r2` and KILLED.** Its round-1 site (a term in `ind_reg_w`) was replaced by the separate strobe.
- **The wrapper's re-application of removed code is faithful:**
  - `rebind-started-trigger-removed` re-applies the deleted `bind_act_r` exclusion as `!apend_r[ACT_A2_C]`, which has the same semantics (Section 2).
  - `failure-change-redeclares` re-applies the round-1 coupling of `ind_fchg_w` into `ind_reg_w`, and is killed by the wire check.
  - `index-guard-removed` is my round-1 mutant, verbatim.
  - `bridge-gate-removed` removes the new single gate.
  - All are killed by named checks.
- **Portability.** `gsi_mutants.py` now guards `sched_setaffinity` and `sched_getaffinity` with `hasattr`.

**Stated residual.** A Talker refresh that changes only the latency raises no notification. Probe R6 shows 0 on both base and head, so the behaviour predates this PR. It is tracked in open issue #113, which asks for the Table 5.22 decision and either a trigger or an F06.13 note. F06.13's row "msrp_accumulated_latency … talker-attr change … yes" is therefore not yet exact for a latency-only refresh. That word is the integrator's (selector 3), not one of the processor-owned fields this PR serves. I accept the residual as out of scope and tracked; it is not a finding against this head.

## 4. Round-1 findings of this reviewer, resolved at this head

| ID | Round-1 | Status at a14ef8b | Evidence |
|---|---|---|---|
| R295-1 F1 MAJOR | Re-bind from ACTIVE/0 that flips started/stopped did not notify | **RESOLVED** | R1 = 1 (≥1 required, and exactly one); GI REBIND-SW (`gsi_internal.hpp:224-253`); retained mutant killed; R7 one frame when pbsta also moves. The listener comment (`:221-228`, `:324-341`, `:1405-1417`), the top comment (`:3124-3131`, `:3523-3531`) and 06 §7 (`:732-743`) are corrected. |
| R295-1 F2 MINOR | A changed FailureInformation re-declared the Listener with New and raised TK_REGISTERED | **RESOLVED** | R2 New = 0. R4: no extra declaration of any event type, and 0 ACMP frames. The strobe has one reader (the notify OR). `ind_reg_w` is the base form. GI FAILED-REFRESH still notifies. The wire check (`gsi_internal.hpp:329-331`) has a New control (`:325-326`). Module checks in srp_stream_fsms L1–L9 and srp_top D. My `-r2` mutant and the author's `failure-change-strobe-removed`/`failure-change-redeclares` are killed. |
| R295-1 F3 MINOR | Untested sample-and-hold | **RESOLVED (removed by manager decision)** | No hold registers remain. F06.13 states the bound, and I verified the bound against `KL_aecp_notify.sv`. The integrator guide (`:307-309`) is updated. The top's own FF are −81 at 8x8 and −78 at 1x1 against round 1. |
| R295-1 S1 | Index guard not pinned | taken | INDEX-GUARD (ten-input image, index 9 aliasing sink 1). My round-1 mutant is now KILLED. |
| R295-1 S2 | SRP listener area | taken | The bridge is gated once after the mux, and the change is compared on the hit sink only. SRP `u_listener` is +455 LUT at 8x8 (round 1: +808). |
| R295-1 S3 | Linux-only affinity | taken | `hasattr` guard |
| R295-1 S4 | `dbg_recwr_*` functional use | taken (documented, name kept) | `KL_pp_acmp_listener.sv:230-235` |

## 4b. Prior public findings of the other round-1 reviewer (R294-1), read after this verdict and ledger were written

Source: PR #111 comment 5814496442 (R294-1, NEGATIVE at `5771578`). I did not read that reviewer's packet or scripts.

| ID | Round-1 | Status at a14ef8b | Evidence |
|---|---|---|---|
| R294-1-F1 MAJOR | A changed FailureInformation re-declares the Listener with New and raises TK_REGISTERED into the event router and ACMP listener; no module-suite update | **RESOLVED** | Same root cause as R295-1 F2 (Section 4). `ind_reg_w` is back to its base form. The separate `evt_tk_fail_chg_o` has one reader, `stri_events`, so it reaches neither the event router nor the ACMP listener. 10 §6.4, the SRP banner, the 02 event catalog and F06.13 are updated. The module suites gain srp_stream_fsms L (1087) and srp_top D (259). Folding the change back into `ind_reg_w` turns both red (8 and 3 FAIL, run here), and the GI wire check red (author mutant `failure-change-redeclares`, reproduced). I did not run that reviewer's P1/P2 scripts themselves. My R2 and R4 top-level probes and the module checks L2 ("no Listener New, no message at all, on the next tick") cover their verification intent. |
| R294-1-S1 | Selector-0 sample (81 FF) untested; prove it or drop it | **RESOLVED (removed by manager decision)** | Same as R295-1 F3. Its mutant `live-unsampled-fields` is moot. |
| R294-1-S2 | Index guard untested | **RESOLVED** | GI INDEX-GUARD. It is solicited-only, with a stated reason: notifications are raised per hardware sink, so no unsolicited response can name an index past the shape. The equivalent mutant is killed (Section 3). |
| R294-1-S3 | Area at the shipping shape; decoder `evt_failure_system_id_o` copy | **TAKEN IN PART** | The OOC tcl takes `N_STREAM_IN_P`/`N_STREAM_OUT_P` arguments, and 1x1 is recorded (`syn/ooc/README.md`). The decoder copy (+128 FF at either shape, `KL_srp_decoder.sv`, outside this diff) remains, and is documented in the area note. It stays a SUGGESTION and does not affect the verdict. |

## 5. Findings at this head

No MINOR, MAJOR or BLOCKER.

### S1: SUGGESTION. The "load-bearing" `bnd_was_r` guard is not pinned by any test

- **Lenses:** Tests, Docs.
- **Location:** `hdl/acmp/KL_pp_acmp_listener.sv:337-341`, which says: "The bound-before half is load-bearing: a fresh bind from UNBOUND without STREAMING_WAIT moves `f_started` 0 -> 1 … and only `bnd_was_r` keeps that undefined -> started step from raising this trigger." The guard itself is at `:1418`.
- **Evidence:** Mutant `strt-bound-before-removed` (drop `bnd_was_r &&`) SURVIVES `tb/acmp_listener` (2544/0) and the GI bank (488/0), per `receipts/r295_mutants2_b/`.
- **Impact:** None at any response or port. The pulse's only consumer, `stri_events`, ORs it with the pbsta compare, and that compare fires in the same cycle on every fresh bind (DISABLED→ACTIVE). As a result, the unsolicited frame count is unchanged. The comment's module-level claim is true, but no test holds it.
- **Suggested outcome:** In `tb/acmp_listener`, count `act_strt_chg_o` (`col.strt_chgs`) across a fresh BIND_RX without STREAMING_WAIT and require 0. Alternatively, soften the comment to "module-level only; masked at the top by the same-cycle pbsta compare".
- **Verification:** The `strt-bound-before-removed` mutant turns the new check red.

### S2: SUGGESTION. The hit-sink comparator is proven only at module level

- **Lenses:** Tests.
- **Location:** `hdl/srp/KL_srp_listener_fsm.sv:463-479`.
- **Evidence:** Mutant `fchg-compare-sink0` is KILLED in `tb/srp_stream_fsms` (L8, L9) but SURVIVES the GI bank. The GI refreshes exercise sink 0 only, or sinks whose comparison against sink 0's latch gives the same verdict.
- **Impact:** None. The module suite covers it, with two sinks on different streams and three on one stream.
- **Suggested outcome (optional):** A GI step with an unchanged Failed refresh on sink 1 while sink 0 holds a different FailureInformation would pin it at the response level.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table 5.22 STREAM_INPUT trigger set against `stri_events`; the F05.3 cells (all 14 rows × 8 states) against the pbsta writers and the dropped terms; Milan §5.3.8.6/.7/.8 field placement @58/@60/@76 (`gen_ucode.py`); MRP applicant path unchanged from base (no New on a FailureInformation change); probes R1, R2, R4, R6, R7 on base and head | R295-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |
| RTL | CLEAN | `protocol_processor_top.sv` (status view, owner read, bridge gate, index guard, notify OR, integrator isolation); `KL_pp_acmp_listener.sv` (X_WB timing, `bind_act_r` removal); `KL_srp_listener_fsm.sv` (candidate set, shared comparator, strobe); `KL_srp_top.sv`; `KL_aecp_engine.sv` missing-descriptor guard; `KL_aecp_notify.sv` pending set/clear order; focused lint at 3 shapes; public area reports | R295-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |
| Robustness | CLEAN | Mid-gather change bound versus the notify pick; index ≥ `N_STREAM_IN_P` (INDEX-GUARD, mutant killed); gather-watchdog void (R3, no leak); reset and preload writes of the status view; wrong-sink mutants on compare, view and gate; LV-state change detection; out-of-shape shapes lint | R295-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |
| Tests | CLEAN (S1, S2 suggestions only) | `gsi_internal.hpp` (488 checks), full pp_top 1948, acmp_listener 2544, srp_stream_fsms 1087, srp_top 259; 13 author mutants reproduced; round-1 mutants rerun unchanged; 16 reviewer mutant runs across 4 benches; probes R1–R4, R6, R7; R294-1 findings resolved (Section 4b) | R295-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |
| Docs | CLEAN | 02 F02.10 rows and event catalog; 06 F06.13 (live read and coherence bound) and §7 trigger list; 10 §6.4 and the FSM arc; integrator guide §8; `syn/ooc/README.md` area table (matches public reports) and the shape arguments in the tcl; four tb READMEs (check counts match executed tallies); RTL port and comment text; link check | R295-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |

## 7. Real limits

- **P1/P2 not rerun as such.** The brief lists "P1/P2" among the round-1 probes to rerun. They are not in this reviewer's round-1 packet, which holds R1, R2 and R3 only; they belong to the other round-1 reviewer, whose material I did not read before this verdict. I re-expressed their evident intent (Listener declarations and pushes after a changed FailureInformation) as my own probe R4. R4 counts every Listener event type, both early and over 1.5 s, against an unchanged-refresh control.
- **Area not re-synthesized.** I verified the area figures by parsing the public post-synthesis reports. I did not run synthesis myself, and those reports are not routed timing or hardware proof. I also cannot independently bind the synthesized source bytes to this head beyond the logs' own statements.
- **Banks not re-run.** I did not run the full processor bank (`run_suites.sh`, full `lint_hdl.sh`, `make check`) or any parent, gPTP, Yosys or builder bank, by instruction. I ran only the four focused suites, the focused lint and the link check.
- **Spec text as quoted.** Milan and IEEE clauses are taken as the repository quotes them; the PDFs are not available here.
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Receipt edits.**
  - In published logs, the local install prefix of the pinned simulator is replaced by `<pinned-simulator-root>`. No other bytes were changed.
  - Build logs (`*-build.log`, `*.build`) are not published. Every run log records its own tally line.

## 8. Pending manager duties

- Push status and the PR body update for round 2.
- Hosted and act acceptance. The six exact-head hosted jobs I inspected all executed and succeeded, but acceptance is the manager's.
- The parent consumer gates at the new parent dev (manager receipts).
- The merge-turn candidate on live dev `59b816708852472da6ed4576386c30ebd5f8f839`. Source validation at base `939c1433` is distinct from that candidate.
- Decision on issue #113 (the latency-only residual).

R295-2 FINISHED
