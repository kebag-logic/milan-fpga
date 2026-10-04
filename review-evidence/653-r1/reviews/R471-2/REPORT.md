[R471] POSITIVE - exact head 03895b63a3e8197353c2483593927b92efb73092

# R471-2: external review of PR #655 (Relates #653), round 2

- **Head:** `03895b63a3e8197353c2483593927b92efb73092`, tree `c43cabe5a60ee90e737e268e27532221f176c288`.
- **Commits under review:** the lane's commits on dev `fea346e7`, plus round 1b. Round 1b is `b2098fd9`, docs only, and a merge of dev `6c22d3ca`.
- **The merge is the automatic merge:** `git merge-tree --write-tree b2098fd9 6c22d3ca` gives `c43cabe5`, the head tree. The dev side adds only #649 files under `syn/resmap/` and `docs/findings/`, and none of them overlaps the lane's twelve files (`receipts/merge_check.txt`).
- **Processor pin:** `631eeb34`, unchanged.
- **Date:** 2026-10-04 UTC.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open. All five lenses are covered clean at this exact head.

- Two RESIDUE items are recorded with their exact fixes: a stale line pointer, and a stale head in the PR body.
- There is one new SUGGESTION, and two prior SUGGESTIONs are retained.
- Every prior BLOCKER/MAJOR/MINOR/RESIDUE finding on this PR is resolved at this head (section "Prior findings").

## Scope, from the public record

- **Issue #653** reports the counters push leaving before the UNBIND_RX response on hardware.
- **The executor's STOP** (issuecomment-5980272602) found that simulation does not reproduce that order. It did find that a locked CRF input's unbind leaves MEDIA_LOCKED 1 / MEDIA_UNLOCKED 0 for up to 100 ms.
- **The manager's ruling** (issuecomment-5980290102) re-scoped the lane to four items:
  1. Count the CRF unbind's unlock at the bind fall: parent only, no port, register or parameter change, the 100 ms path kept without double counting, and no STREAM_INTERRUPTED.
  2. Commit standing `[UNB]` tests for AAF and CRF, covering (a) the order and (b) the invariant. They need planted controls for the order reversed, the CRF unlock uncounted and a double count, and they are recorded in the README.
  3. Report the OOC area, with a STOP above 30 LUT / 60 FF.
  4. Correct the stale pointer in the PR body.
- **The PR says "Relates to #653".** Acceptance 4 and the bench capture are manager bench items, now in bench lane B10 (#629 issuecomment-5983013590).

## Findings

### R471-2-F1: RESIDUE, Docs

- **Where:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:536`, "oscillator margin, `:280-292`): 601 ns".
- **Evidence:**
  - The bare pointer continues the `hdl/ieee1722/crf/KL_crf_rx.sv:284-299` citation on `:531`.
  - At the base, `KL_crf_rx.sv:280-292` was the oscillator-margin and 601 ns derivation.
  - This PR adds five header lines above it, so that text is now `:285-297`. At this head, `:280-282` are the `NOM_PDU_NS_C`/`NOM_WIN_NS_C` constants.
  - Round 1b moved two other pointers of the same kind (R471-F3, R470-1-F1) and missed this third one.
- **Impact:** a reader is sent five lines too high. The cited text still largely overlaps, and no claim, figure, test or code changes.
- **Exact fix:** `:536`: change `` `:280-292` `` to `` `:285-297` ``.
- **Classification:** a citation-only correction, consistent with how both prior rounds classified the same pointer class.

### R471-2-F2: RESIDUE, Docs

- **Where:** PR #655 body, in two places:
  - the Status line, "head `77ea6cb4`, four commits on dev `fea346e7`";
  - "How to get into the same state", `git checkout 653-unbind-order          # head 77ea6cb4`.
- **Evidence:** the published head is `03895b63`. It is the round-1b docs commit plus a merge of dev `6c22d3ca`. The body's trailing "Manager round 1b" note records this, but the two head statements were not updated.
- **Impact:** wording only. No measurement, verdict or claim changes; the gate table is correctly labelled "at `77ea6cb4`".
- **Exact fix:**
  - Status: "head `03895b63` (the lane's commits on dev `fea346e7`, round-1b docs commit `b2098fd9`, merge of dev `6c22d3ca`)".
  - Setup comment: `# head 03895b63`.

### R471-2-S1: SUGGESTION, Docs

- **Where:** `tb/verilator/milan_dp/README.md:693`, and the PR body's trace table, "CRF input 1, dev `fea346e7`" column: "+9,818,177".
- **Evidence:** that figure is a true record of the round-1 reproduction bench, the uncommitted patch `bc4bf432...` run at dev (published `author/base-unb-trace-run.log`). The committed `[UNB]` bench with the base `KL_crf_rx` gives +9,818,097, with pushes at +9,819,057 / +9,819,820, and so does unb-mutant 2 (`receipts/leg_basecrf.log`, `receipts/leg_m2.log`). The 80-cycle offset comes from the talker cadence of the two benches. It is not a defect.
- **Optional:** say that the dev column was measured with the reproduction patch, so a re-run of mutant 2 is not read as a discrepancy.

### Retained SUGGESTIONs (unchanged at this head)

- **R471-S1 = R470-1-S1, Tests:** no root-level test grades a followed-CRF input's unbind with CRF selected. That test would check one restart request, HOLDOVER, and no second request at the timeout.
- **R471-S2, Tests:** `unb_mutants.py` runs its mutants serially and has no `--jobs`. This round ran it one mutant per process instead.

## Prior findings, resolved or retained at this head

| Finding | Severity | State at `03895b63` | Evidence |
|---|---|---|---|
| R471-F1 (lock-loss rule omitted the CRF unbind's earlier fall) | MINOR | **Resolved** | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1061-1063` now says a followed CRF input's lock falls at the unbind, counting one MEDIA_UNLOCKED, and that an AAF meter lock falls at its 100 ms timeout. Rules 2 to 4 (`:1064-1079`) still read true for both sources. |
| R471-F2 (changelog stated the order as a device fact) | MINOR | **Resolved** | `CHANGELOG.md:50`: "Simulation shows the UNBIND_RX response leaving before the counters push. The hardware order in #653 awaits a bench capture." |
| R471-F3 (two stale pointers) | RESIDUE | **Resolved** | `MEDIA_CLOCK_FOLLOWING.md:964` reads `:397-410` and `:1502` reads `:405-407`. Both match head `KL_crf_rx.sv`. A third pointer of the same kind is new R471-2-F1. |
| R470-1-F1 (`:1499` pointer) | RESIDUE | **Resolved** | Same line, now `:1502`, `:405-407`. |
| R471-S1 / R470-1-S1, R471-S2 | SUGGESTION | Retained | See above. |

## What was checked, per lens

### Conformance

- **Ruling item 1**, `hdl/ieee1722/crf/KL_crf_rx.sv:395`, `:627-631`:
  - `w_bind_fall_w = !en_i && en_q` reuses the existing `en_q`.
  - When the input is locked at the fall, `locked_o` drops, `cnt_unlocked_o` +1 and `dirty_p_o` pulses.
  - Milan v1.2 5.3.8.10 (Table 5.6) makes a Controller Unbind a MEDIA_UNLOCKED event and never a STREAM_INTERRUPTED. The pair then reads LOCKED = UNLOCKED, "not synchronized".
  - The bound-to-unbound edge resets nothing, as the clause's asymmetry requires; the rise wipe (`:641-696`) is unchanged.
- **Silence path** (`:540-545`): unchanged. After an unbind it finds `locked_o` low and counts nothing. On a shared edge both arms write the same `+1` (unit `[UNB-d2]`).
- **STREAM_INTERRUPTED** cannot move: `w_ev_si_w` requires `w_acc`, which requires `en_i` (`:314`, `:356`, `:391`).
- **Ruling item 1 constraints:** no port, register field or parameter change (`git diff 6c22d3ca..HEAD -- hdl/`).
- **Ruling item 2:** U1 to U4 (`tb/verilator/milan_dp/sim_nxn.cpp:2293-2630`) grade both inputs of the shipping 1x1 shape. The three demanded controls are planted, plus two more (`unb_mutants.py:95-131`).
- **Ruling item 3:** area is within the bound and fell (Tests and RTL).
- **Ruling item 4:** the body states `:533-536` and `:619-670` at dev, and `:540-545`, `:641-696` and `:627-631` at head. I checked each against the base and head bytes.
- **Order mechanism**, read in the pinned processor, which supports the simulated order by construction:
  - The bind level is the debounced `bound_hold_r`, which falls only when the listener is idle (`protocol-processor/hdl/top/protocol_processor_top.sv:948-952`). The response is therefore queued before any unlock source sees the fall (trace: queued +193, fall +199).
  - The counters push payload is store-and-forward: it is sealed before it requests TX (`protocol-processor/hdl/aecp/KL_aecp_resp_buf.sv:12-17`). A push that carries the new count therefore requests TX after the response is already queued.
  - ACMP holds the top TX class (`PRIO_MAP_P`, lane 2 = 0, `protocol_processor_top.sv:4453`).
  - This is simulation and RTL reading only. The hardware order stays with the bench item.
- **Acceptance 3** holds in simulation for both inputs: 1/1 at the response's last byte, 1/1/0 in GET_COUNTERS right after it, every later push equal, and 1/1/0 past both timeouts (`receipts/notify_head.log`).

### RTL

- **Single clock, synchronous reset.** `en_q` resets to 0 and `en_i` is 0 at reset, so no false fall occurs.
- **The fall arm cannot meet the accept arm**, because `w_hit` is gated by `en_i`, so the lock-set and the fall are mutually exclusive.
- **Rise and fall are exclusive by construction.** The rise block stays the last writer of `locked_o`. A fall followed by a rise on the next cycle counts the unlock and then wipes it, which is the clause's era edge.
- **No new flop.** Widths are unchanged: a 32-bit wrapping add, as on the silence path.
- **Consumers** (`hdl/milan/milan_datapath.sv:2661`, `:3189-3232`, `:5625`, `:5652`, `:5745-5746`):
  - `CRF_CTRL[31]`, the 4.4.4.3 restart request when CRF is selected, and the servo reference lock now see the fall at the unbind instead of up to 100 ms later.
  - The number of falls per unbind is unchanged, because the rise wipe already dropped the lock on a fast re-bind.
  - The `milan_datapath.sv:3174-3176` comment states this.
- **Bench lever:** `en_i = cfg_crf_en | acmpl1_bound` (`:5625`). With the bench lever held, an ACMP unbind drops nothing. This is pre-existing and documented (`docs/reference/REGISTER_MAP.md:851`).
- **Area:** Yosys `ooc.sh KL_crf_rx`, AX 1x1 TDM8 shape, reproduced. Base engine 433 LUT / 544 FF / 1 RAMB18; head 368 LUT / 544 FF / 1 RAMB18 (`receipts/ooc_base.log`, `receipts/ooc_head.log`). That is within the 30 LUT / 60 FF STOP bound.
- **Lint:** `scripts/lint_rtl.py --check` gives 90 <= 90 with the pinned Verilator 5.050 (`receipts/lint_rtl_check.log`). The SV idiom gate passes (`receipts/sv_idiom.log`).

### Robustness

Every case below is pinned by the unit suite. My planted probes confirm the checks can fail.

| Case | Checks | Result |
|---|---|---|
| Unbind of an unlocked input | `[UNB-c1/c2]` | No count, no pulse. Probe P6, which counts on any fall, fails `[UNB-c1]`, `[UNB-c2]` and `[dirty-e1]` (`receipts/crfrx_unit_p6.log`). |
| Unbind and timeout on one edge | `[UNB-d2..d4]` | One unlock and one pulse. |
| Stopped input still holding lock | `[UNB-e1]` | One unlock. |
| Talker still streaming with gaps after the unbind | `[UNB-b1..b3]` | No second count, no STREAM_INTERRUPTED. |
| Bound silence still unlocks | `[UNB-d0]` | Pass. |
| Unbind keeps the totals, re-bind zeroes them | `[5t-g3]`, `[5t-g3b]` | Pass. |

- **Fall drops the lock and pushes but scores no unlock:** probe P7 fails `[5t-g3]`, `[5t-g3b]`, `[UNB-a2]`, `[UNB-a4]`, `[UNB-b1]` and `[UNB-e1]` (`receipts/crfrx_unit_p7.log`).
- **At root level,** the `[UNB]` talker keeps streaming through the unbind and past both 100 ms timeouts. The wait, 10.5 M cycles, outlasts the CRF timeout (+9.82 M, mutant 2 and the base engine) and the AAF timeout (+9.98 M, probe P1).

### Tests

All runs used the pinned Verilator 5.050 (identity: wrapper sha256 `905795b9...`, `--version` "Verilator 5.050 2026-07-01 rev v5.050").

**Suites at head:**
- `make -C tb/verilator/milan_dp notify`: 421 checks, 0 failures. The `[UNB]` section has 38 checks, so 383 + 38 = 421 as `docs/testing/TESTING.md` and the README state. The trace matches the README, PR body and CHANGELOG to the cycle: AAF +204/+277/+2294/+3057, CRF +200/+277/+2294/+3057 (`receipts/notify_head.log`).
- `make -C tb/verilator/crf_rx all`: unit 14287/0, discontinuity 2201/0, talker_step 69/0, receiver mutants 10/0, total 16567 as stated (`receipts/crfrx_head.log`).
- The four other `sim_nxn.cpp` elaborations of the milan_dp suite, built from its own recipe lines (`scripts/nxn_extra.mk`): 4x4 1961/0, divergent 1961/0, 8x8 3746/0, 4-channel 1961/0 (`receipts/nxn-*.log`). The changed harness compiles and passes in every shape. `[UNB]` returns early outside the 1x1 shape, as designed (`sim_nxn.cpp:2617`).

**The committed campaign, `unb_mutants.py`:** run as one process per mutant (`python3 unb_mutants.py N`, N = 1..5). Each run passed its clean control and caught its mutant, 2/2 each (`receipts/unbmut_*.log`).

**The same five defects planted by hand, with full logs** (`scripts/wave2.sh`). Each fails exactly the checks the README table names, and nothing else:

| Mutant | Failures (of 421) | Checks that fail |
|---|---|---|
| M1 | 4 | The four U2 order checks. The response leaves at +6277 and the pushes at +2294/+3057. |
| M2 | 2 | CRF U3 at the response and right after it. |
| M3 | 2 | CRF U3 every later push, and CRF U4 (0x10200). |
| M4 | 2 | CRF U3 STREAM_INTERRUPTED, and CRF U4 (0x10101). |
| M5 | 2 | CRF U2 a push reached A and B. |

**This review's own probes:**
- **P1 (AAF):** the AAF bind-fall unlock is removed in `KL_avtp_rx_monitor_ctx.sv`. It fails AAF U3 at the response and right after it, 2 of 421, with the unlock moved to +9,982,974 (`receipts/leg_p1.log`). The AAF invariant checks therefore have power too, which closes the PR's stated "no AAF-only RTL mutant" limitation for this round.
- **Base `KL_crf_rx` in the committed bench:** the same two failures as M2 (`receipts/leg_basecrf.log`).
- **Base engine in the unit suite:** fails 8 checks, `[5t-g3]`, `[5t-g3b]` and six `[UNB-*]` (`receipts/crfrx_unit_base.log`). The new unit checks fail on the defect they claim.

**Harness timing:** U3 samples the source pair on the posedge that takes the response's last beat (`sim_nxn.cpp:1784-1799`), and responses and pushes share one timestamp convention.

**Ratchets:** `scripts/measure_test_evidence.py --check` passes. The new disposition is at `:669` (`receipts/measure_test_evidence_check.log`). The C++ and Python idiom gates pass (`receipts/cpp_idiom.log`, `receipts/py_idiom.log`).

### Docs

- **Gates:** `scripts/docs_check.py` reports 0 findings over 188 md files and 985 scrubbed files. `scripts/check_doc_style.py` is OK. The pinned-renderer `scripts/gen_toc.py --check` is OK. `scripts/check_em_dash.py --base 6c22d3ca` reports 0 findings over 113 added lines (`receipts/docs_check.log`, `check_doc_style.log`, `gen_toc_check.log`, `em_dash.log`).
- **Pointers in `MEDIA_CLOCK_FOLLOWING.md`:** I read every `KL_crf_rx` pointer against the head bytes (`:295-299`, `:494`, `:516`, `:531`, `:632`, `:759`, `:964`, `:975`, `:983-984`, `:996`, `:1499`, `:1502`). All are correct except `:536` (R471-2-F1).
- **Other documents updated for the change:**
  - `REGISTER_MAP.md:188`, `:851`: the `CRF_CTRL[31]` unbind fall.
  - `TESTING.md:273`, `:311-313`.
  - The milan_dp README: `:93`, `:656-716`, and `:1073` (421/0).
  - `CHANGELOG.md:11`, `:41-56`.
  - The `KL_crf_rx.sv` header (`:34-38`, `:138-142`).
- **The PR body's tables match the reproduced runs.** Its two stale head statements are R471-2-F2.

## Clean-lens results (findings format)

```text
[R471] PASS Conformance - hdl/ieee1722/crf/KL_crf_rx.sv:314,:356,:391,:395,:540-545,:627-631,:641-696; tb/verilator/milan_dp/sim_nxn.cpp:2293-2630; protocol-processor/hdl/top/protocol_processor_top.sv:948-952,:4453; protocol-processor/hdl/aecp/KL_aecp_resp_buf.sv:12-17; receipts/notify_head.log - ruling items 1-4 and #653 acceptance 3 against Milan v1.2 5.3.8.10 Table 5.6 and 5.4.5 Table 5.22, at the exact head; order shown in simulation only
[R471] PASS RTL - hdl/ieee1722/crf/KL_crf_rx.sv:354,:393-395,:445-698; hdl/milan/milan_datapath.sv:2661,:3172-3232,:5596-5653,:5745-5746; receipts/ooc_head.log, receipts/ooc_base.log, receipts/lint_rtl_check.log, receipts/sv_idiom.log - edge detect, last-writer order, exclusivity with accept and rise, consumer effects, area 433->368 LUT, 544 FF unchanged
[R471] PASS Robustness - tb/verilator/crf_rx/sim_main.cpp:1475-1601 ([UNB-a..e]), :1016-1070 ([5t-g2b..g3b]); receipts/crfrx_head.log, crfrx_unit_p6.log, crfrx_unit_p7.log, leg_p1.log - unlocked unbind, shared timeout edge, stopped input, streaming talker with gaps after unbind, bound silence, both receivers' timeouts inside the U4 window
[R471] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:1729-1843,:2293-2630; tb/verilator/milan_dp/unb_mutants.py; tb/verilator/crf_rx/sim_main.cpp; receipts/notify_head.log, unbmut_1..5.log, leg_m1..m5.log, leg_basecrf.log, leg_p1.log, crfrx_unit_base.log, nxn-*.log, measure_test_evidence_check.log - every new check shown to fail on its defect, the committed campaign 5/5 with clean control, all four other sim_nxn shapes green
[R471] PASS Docs - CHANGELOG.md:11,:41-56; docs/design/MEDIA_CLOCK_FOLLOWING.md:295-299,:531-536,:964-996,:1058-1079,:1499-1502; docs/reference/REGISTER_MAP.md:188,:851; docs/testing/TESTING.md:273,:311-313; tb/verilator/milan_dp/README.md:93,:656-716,:1073; PR #655 body; receipts/docs_check.log, check_doc_style.log, gen_toc_check.log, em_dash.log - prior MINORs F1/F2 resolved; open items are RESIDUE F1/F2 only (wording/citation, do not un-cover the lens under the 2026-10-02 owner rule)
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_crf_rx.sv` (fall arm, silence, accept gate, rise wipe); `sim_nxn.cpp` `[UNB]`; processor debounce, TX priority, response buffer; notify-leg trace | R471-2 | `03895b63a3e8197353c2483593927b92efb73092` |
| RTL | CLEAN | `KL_crf_rx.sv`; `milan_datapath.sv` CRF consumers and comment; Yosys OOC head and base; lint and SV idiom gates | R471-2 | `03895b63a3e8197353c2483593927b92efb73092` |
| Robustness | CLEAN | crf_rx `[UNB-a..e]`, `[5t-g2b..g3b]`; probes P6, P7, P1; U4 window against both timeouts | R471-2 | `03895b63a3e8197353c2483593927b92efb73092` |
| Tests | CLEAN | notify leg 421/0; crf_rx 16567/0; committed `unb_mutants.py` 5/5 plus clean; M1 to M5 full logs; P1; base-engine bench and unit; four other sim_nxn shapes; test-evidence, C++ and Python ratchets | R471-2 | `03895b63a3e8197353c2483593927b92efb73092` |
| Docs | CLEAN (RESIDUE F1, F2 carried) | CHANGELOG; MEDIA_CLOCK_FOLLOWING; REGISTER_MAP; TESTING; milan_dp README; `KL_crf_rx` header; datapath comment; PR body; docs, style, TOC and em-dash gates | R471-2 | `03895b63a3e8197353c2483593927b92efb73092` |

## Real limits

- **Simulation and RTL reading only.** No hardware was used. Physical calibration was NOT RUN. The hardware order reported in #653 and acceptance 4 (20 controller connects) are not shown by this round. Field skips are not hardware proof.
- **Not run:**
  - the full milan_dp `run` target (its gptp, gmstep and render/gmstep mutant legs);
  - `milan_dp_render` `tdm8render-mutants`, `milan_dp_gptp`, `pp_shadow`, `milan_dp_mclk`, `capture_coherence` and `aaf_clock_meter`;
  - the Yosys `run.sh` bank, the xvlog gate, behave and the builder bank;
  - hosted CI and act.

  For these, this round relies on the manager's exact-head banks. The two pre-existing failures the executor reported are filed as #656 and #657. The published logs show identical clean outputs with the base `KL_crf_rx` (`author/tdm8r-epoch-only-{head,devcrf}.log` are byte-identical).
- **No Vivado run.** The Vivado OOC figures (373 to 352 LUT) are the executor's and were not reproduced. The Yosys figures were reproduced exactly.
- **The probe copies are not git checkouts.** They are byte copies of the clone's working tree, with a throwaway local index in each submodule so that `scripts/pp_srcs.py` can list sources. The listed processor `.sv` set equals the pinned checkout's (59 files).
- **The clone was restored** after one temporary swap for the base OOC. Its working tree, index, every tracked blob and mode, and the three required submodule gitlinks match the exact head (`receipts/clone_restore_check.txt`).

## Pending manager duties

- Carry RESIDUE R471-2-F1 (`MEDIA_CLOCK_FOLLOWING.md:536`, `:280-292` -> `:285-297`) and R471-2-F2 (the PR body's head statements) to the residue checklist.
- Hosted and act acceptance at the exact head, and the candidate merge on live dev `6c22d3ca`. The source base is `fea346e7`; the head already contains dev `6c22d3ca`.
- The bench item in lane B10: the port capture of one disconnect and 20 controller connect/disconnect cycles (#653 acceptance 2's bench half and acceptance 4). #653 stays open.
- Track #656 and #657, the pre-existing gate failures.
- The second positive (internal round R470-2) and the merge authorization stay with the maintainer.
- **Receipts:** some logs carry local absolute paths, from build command lines and the pinned tool wrapper. Apply the usual path redaction before publication.

## Receipts

Scripts are in `scripts/`; raw logs and `rc` files are in `receipts/`. All are listed in `MANIFEST.sha256`.

R471-2 FINISHED
