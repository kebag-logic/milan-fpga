# [A676c] processor #202 round 3 — HANDOFF

**Status: REVIEW READY. All required gates passed; no STOP condition met.** TAKEN: issue #202 issuecomment-6414945910.

Round-3 assignment: issue #202 issuecomment-6414935566, answering R710-1 (PR #204
issuecomment-6414931259, 2 MAJOR + 1 RESIDUE) and R709-1 (PR #204 issuecomment-6414853154,
3 MINOR + 1 RESIDUE + 5 SUGGESTIONs). Owner decision in force: issuecomment-6408987895 (option A).

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked; initial base `ed211803` is recorded in the earlier handoff. Round 3 began at the required round-2 head `a8aa626e`; this resume found clean `ebb1f00`. No reset or rebase was performed.) |
| Branch | `202-maap-conflict-new-stream-id` (local; not pushed) |
| Base (processor main) | `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8` |
| Round-2 head (start) | `a8aa626e1cba30625ac764c70e1fb8fb02c69c40` |
| Head | `ebb1f00` (full hash in `receipts/base-head-records.txt`) |
| Scratch parent | milan-fpga dev `e76a755afc0536453161e3cd33f6f4d2dcd7641f`, branch `scratch-pp202-a676c`, never pushed (§7) |

Round-3 commits on `a8aa626e` (one-line subjects, no body, no trailers):

1. `39358354` Move a declared source to a new Stream ID when it returns from a disable, and keep a PCP change after a withdrawal two LeaveAllTime away from the same-ID declaration (issue #202)
2. `9a6d1d08` State the disable move and the PCP gap after a withdrawal in F05.12, REQ-ACMP-010, the timing row and the interface documents, and say the re-open after a move is a Join!, not a New (issue #202)
3. `1cfd3b1` Re-measure the talker, processor-top and MAAP records for the disable move and the PCP gap, and note the applicant's LA window a fast return reaches (issue #202)
4. `ebb1f00` Name the talker timeline's disable-move IDs by what each source did, not by check name (issue #202)

Commit 1 was amended once before anything else used it (a REQ_TAG name split across two string
literals failed `make check`'s tag gate); nothing was pushed or published from the first version.
Commits 3 and 4 change no file under `hdl/`, `scripts/`, `syn/` or the `Makefile`; commit 4 changes
one comment in `tb/acmp_talker/sim_main.cpp` (`receipts/processor/after-sweep-commits.txt`). The
sweep and the campaigns built `9a6d1d08`; lint, `make check` and the talker suite were rerun at
`ebb1f00`, the yosys portability run and the elaboration guards at `1cfd3b1` (identical `hdl/`).

## 2. What each finding asked, and what was done

| Finding | Done | Where |
|---|---|---|
| R710-F01 (MAJOR): a PCP change after a withdrawal re-declares the same ID with the changed FirstValue 2 ms later | **wait the gap** (the decision's PCP policy kept): `EVC_PCP` on a `DA_OK` source whose ID has been declared enters `BACKOFF` and arms `T-SRP-LEAVEALL2` from the change, which comes after the withdrawal, so the gap since the withdrawal is at least two LeaveAllTime; no same-ID open while a PCP change is pending (`pcp_hold_w`), which closes the command-ahead-of-event race | §3 rows 1-4; tests S7, S8, S9; mutants `pcp_after_withdrawal_skips_the_gap`, `pcp_pending_not_held` |
| R709 F-1 (MINOR): a disable/re-enable returns the same ID with another DA | **move**: `EVC_OFF` books the move when the current ID has been declared, so the return grant installs a new ID whatever DA comes back (a fresh allocator's or a block allocator's same one); a PCP or TSpec change while disabled is covered by the same move | §3 row 5; tests S10, J7, K8, S1; mutant `disable_keeps_declared_id` |
| R710-F02 (MAJOR): the parent patch let a non-zero TCTX uid outrank `src_stream_id_o` | `KL_aaf_packetizer` gains `SID_PP_P`; `milan_datapath` sets it, so every talker stamps the processor's current ID and no TCTX uid can name another; the standalone default keeps the old derivation. Proven by two new parent legs through a real MAAP conflict on the wire (§7) | `parent-src-stream-id-wiring.patch`; legs `sidmove`, `sidmove8`; controls in `receipts/parent/` |
| R709 F-2 (MINOR): no check binds a slot's published upper 48 bits to its slot | S4 now provisions slot 7 `0xCD00000000000008` and slot 5 `0x0123456789ABCDEF`, checks every slot's whole published ID after reset, after another slot's move, and after its own move | test S4; mutant `publish_upper_from_slot0` |
| R709 F-3 (MINOR): 10 says "first New", the RTL issues Join! | **documents follow the RTL**: the re-open is Join! (802.1Q-2018 10.7.5.5); New! (10.7.5.4) only at a source's first open since reset; Table 10-3 Join! → VP (from VO) or AA (from LA), sJ = JoinMt (10.7.6.3); 35.2.3.1.1 maps REGISTER_STREAM.request onto MAD_Join.request; a new StreamID is a new attribute value, registered on rJoinMt! like rNew! (Table 10-4). Graded: MP8 now reads the event (JoinMt); the parent legs show New before the move and JoinMt after it | 10 §6.1/F10.4; MP8; mutant `reopen_sends_new` |
| R710-R01 (RESIDUE): bench labels in new source comments | removed as listed (sid_cases.hpp headings, talker sim_main.cpp :13 and :213, acmp_mutants.py group comment, pp_top_wrap.sv, pp_top sim_main.cpp MP8/MP8a comments); one label of this round in a new comment fixed in commit 4 | commits 1 and 4 |
| R709 RESIDUE-1: "Measured 2026-10-26 on the lane tree" | the record was re-measured, so the line names the commit it was measured at: "Measured 2026-10-26 at 9a6d1d08a5d1 (RTL as at 39358354c47a)" | `tb/pp_top/README.md` |
| R709 S-1 (suggestion): the LA window | stated in 05 (the disable path can reach it; nothing is declared under the withdrawn ID with another FirstValue; the withdrawn registration ages out at LeaveAll) | 05 sec-05-sidmove |
| R709 S-2 / S-4 | S-2: the proof's quasi-static `cfg_stream_id_i` assumption named in 05. S-4: GAP-04 marks the new Stream ID as this design's choice, Table 5.3 informative | 05; 00 GAP-04 |
| R709 S-3 / S-5 | the parent patch lets the processor win (R710-F02) and adds the parent conflict scenario | §7 |

The inherited base-to-round-2 change map is preserved in `receipts/round2-records/HANDOFF.md` §3. It is historical evidence; the round-3 findings and corrections below supersede its PCP, disable and parent-precedence claims.

## 3. Changes (file:line at head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/acmp/KL_acmp_talker.sv:37-57` | banner: the PCP path after a withdrawal, the pending-change hold, the disable move; "never declared again with another FirstValue before two LeaveAllTime" | 802.1Q-2018 35.2.2.8 |
| 2 | `hdl/acmp/KL_acmp_talker.sv:520-528` | `pcp_hold_w`: a PCP change pending (or strobing) on a source whose ID has been declared | 802.1Q-2018 35.2.2.8 |
| 3 | `hdl/acmp/KL_acmp_talker.sv:778, 842-844, 921, 950-951` | no same-ID open while held: PROBE_TX commit, non-moving grant, backoff exit, Listener event | 802.1Q-2018 35.2.2.8 |
| 4 | `hdl/acmp/KL_acmp_talker.sv:903-910` | `EVC_PCP` from `DA_OK` with the ID declared: `BACKOFF` + draw, nothing to withdraw | 802.1Q-2018 35.2.2.8, 35.2.2.8.5; Table 10-7 |
| 5 | `hdl/acmp/KL_acmp_talker.sv:870-874, 109, 1374-1376` | `EVC_OFF` books the move (`ev_sid_owe_w = sid_used_r`) | 802.1Q-2018 35.2.2.8; Milan v1.2 Table 5.3 (5.3.7.5) |
| 6 | `tb/acmp_talker/sid_cases.hpp:318-497` | new cases S7, S8, S9, S10 and `last_open` | as above |
| 7 | `tb/acmp_talker/sid_cases.hpp:96-171, 204-236` | S1: the disabled source keeps its moved ID while out, then moves again (UP\|9); S4: the per-slot publish checks | decision item 1 |
| 8 | `tb/acmp_talker/sim_main.cpp:704-709, 989, 998, 1125` | J7, J7b, K8 expect the disable move (`SID4B`, `SID6B`) | as row 5 |
| 9 | `tb/pp_top/sim_main.cpp:9424-9444` | MP8 reads the new ID's first Talker Advertise event: JoinMt | 802.1Q-2018 10.7.5.5, 10.7.6.3 |
| 10 | `tb/pp_top/acmp_mutants.py:416-560` | five new STREAM_ID arms (25 arm runs, 22 names) | — |
| 11 | `docs/architecture/05_acmp_engine.md:446, 448, 477-511, 533-540` | F05.12 arcs (DA_OK → BACKOFF; removal books a move); the two same-ID bullets; "Together"; the LA-window note; the proof's assumption | 802.1Q-2018 35.2.2.8, Table 10-3 |
| 12 | `docs/architecture/08_timing.md:36` | `T-SRP-LEAVEALL2`: also after a withdrawal; a disable takes a new ID | 802.1Q-2018 35.2.2.8, Table 10-7 |
| 13 | `docs/architecture/10_srp_engine.md:336-342, 417, 427-439` | PCP gap also after a withdrawal; F10.4 New!/Join!; the Join! paragraph | 802.1Q-2018 10.7.5.4/.5, 10.7.6.3, Tables 10-3/10-4, 35.2.3.1.1 |
| 14 | `docs/00_MILAN_COMPLIANCE_REVIEW.md:141-142, 407` | GAP-04 (S-4); REQ-ACMP-010 adds both paths | 802.1Q-2018 35.2.2.8; Milan v1.2 Table 5.3 |
| 15 | `docs/architecture/02_interfaces.md:300-303, 564`; `06_aecp_engine.md:390`; `docs/guides/integrator.md:332-335, 564` | the allocator may grant another DA after a release; the disable move named wherever the output is described | 02 §4.2 |
| 16 | `docs/architecture/09_verification.md:797-811` | §8.13 rows for the new properties | — |
| 17 | `tb/acmp_talker/README.md:8, 33, 232, 251-286, 355-392`, `tb/pp_top/README.md:2042, 2059-2101`, `tb/maap/README.md:246, 248` | case tables, the STREAM_ID record (25 arms), the retry table (12 rows' counts), MP 43 checks, maap pp_top arms 4 and 12 of 43 | — |

## 4. New checks, planted mutants, failing words

Talker suite 1,463 → 1,520 checks; `tb/pp_top` 10,749 → 10,750. On the round-2 RTL (`a8aa626e`)
the new talker bench fails 18 checks (`receipts/tests/talker-new-bench-on-a8aa626e.txt`), among
them `S7 two LeaveAllTime periods separate the withdrawal and the same-ID declaration (2 ms)` (R710's
2 ms reopen) and `S10 a declared source returns from a disable under a new Stream ID (got
ab00000000000003)` (R709's RP1 shape).

| Check (words as printed) | Killed by (planted defect), failing checks |
|---|---|
| `S7 a PCP change after a listener withdrawal arms T-SRP-LEAVEALL2`, `S7 two LeaveAllTime periods separate the withdrawal and the same-ID declaration`, `S8 two LeaveAllTime periods separate the withdrawal and the moved ID's declaration` (also `S7/S8 ... does not declare ... inside the gap`) | `pcp_after_withdrawal_skips_the_gap` (the DA_OK branch of `EVC_PCP` removed): 9 |
| `S9 a probe served with a PCP change pending does not declare the same ID` | `pcp_pending_not_held` (`pcp_hold_w = '0`): 1 |
| `S10 a declared source returns from a disable under a new Stream ID`, `J7 grant re-declares open sid` (also `S10 the move does not depend on the returned DA`) | `disable_keeps_declared_id` (the `EVC_OFF` booking removed): 9 |
| `S4 after reset every slot publishes its own whole configured ID`, `S4 a slot under other upper 48 bits keeps them when it moves` | `publish_upper_from_slot0` (every slot publishes `cfg_stream_id_i[16 +: 48]`): 6 |
| `MP8: the new Stream ID's first Talker Advertise is a JoinMt, not a New` | `reopen_sends_new` (`KL_srp_talker_fsm`'s gate open always New!): 1 (MP section alone) |
| `S1 the move survives a disable` (now read while the source is out) | `move_lost_on_disable`: 1 |

Group `STREAM_ID`: 25 of 25 KILLED, both goldens PASS; whole ACMP campaign 90 of 90 KILLED, 8
goldens PASS (`receipts/compare/acmp-arms-head-9a6d1d0.tsv`). Counts that moved against round 2
(new checks failing too): `conflict_keeps_old_wait` 108 → 124 (MP8 5 → 6), `conflict_reuses_old_id`
28 → 35 (MP8 4 → 5), `output_ignores_move` 11 → 17, `move_compares_unique_id_only` 1 → 3,
`move_cursor_stuck` 2 → 3, `used_not_marked_by_event` 8 → 19, `used_not_marked_by_probe` 22 → 34,
`probe_answers_configured_id` 4 → 8, `declare_carries_configured_id` 12 → 18,
`disconnect_changes_gate` 72 → 73, `armq_read_tail` 77 → 78 (one more collateral MP8 check; its
README row is a dated #639 record, 72, left as round 2 left it).

## 5. Same-Stream-ID paths, enumerated

After an ID has been declared (`sid_used_r`) and withdrawn:
- withdrawn by a lapsed gate (`DA_OK`): the DA is kept; a PCP change → `BACKOFF` (gap); otherwise
  the next declaration has the FirstValue it was withdrawn with (no gap needed);
- withdrawn by a PCP change (`BACKOFF`): the existing gap;
- withdrawn by a conflict (`NO_DA`): a move is booked;
- withdrawn by a disable (`NO_DA`): a move is booked (new);
- `NO_DA` with a declared ID therefore always has a move booked, so a PCP change there needs nothing;
- TSpec, rank, accumulated latency: quasi-static (02 §2 rule 4), stable while the entity is
  enabled; changed while the source is disabled, they are covered by the move.

## 6. Processor gates (every `.rc` is the command's own exit status, never through a pipe)

Local tools: Verilator 5.052 (CI pins 5.050) through a PATH wrapper that turns `-j 0` into `-j 4`
(sweep) or `-j 2` (campaigns); Yosys and sv2v as installed. Results do not depend on the wrapper.

| Gate | Base `ed211803` (round-2 record) | Round-2 head `a8aa626e` (round-2 record) | Head |
|---|---|---|---|
| `./scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,399 | rc 0, 1,030,494 | rc 0, 1,030,552 checks, 0 failing (at `9a6d1d08`); only `acmp_talker` 1,463 → 1,520 and `pp_top` 10,749 → 10,750 move (`receipts/compare/suites-a8aa626e-vs-9a6d1d0.diff`) |
| `check-req-tags.py --suites … --evidence …` | rc 0 | rc 0, 237 tags | rc 0, 241 tags in 20 files, 241 evidence lines, 14 suites |
| `./scripts/lint_hdl.sh` | rc 0 | rc 0 | rc 0 at `ebb1f00` |
| `make check` | rc 0 | rc 0 | rc 0 at `ebb1f00` |
| `./syn/yosys/run.sh` | — | rc 0 | rc 0 at `1cfd3b1` |
| `tb/elab_guards/guards.py --frontend yosys --jobs 4` | — | 93 of 93 | rc 0, 93 of 93 at `1cfd3b1` |

| Campaign (at `9a6d1d08`, six workers; name_state two) | Result |
|---|---|
| `tb/pp_top/acmp_mutants.py` | rc 0, 90 of 90 KILLED, goldens PASS |
| `tb/acmp_talker/retry_mutants.py` | rc 0, 62 killed, 7 equivalent, 1 performance control, baseline and restored 1,520 checks, coverage 59/59; 12 rows' counts moved (README re-measured) |
| `tb/maap/mutants.py` | rc 0, 29 of 29 KILLED, 3 controls PASS; pp_top arms 4 and 12 FAIL of 43 |
| AECP | rc 0, 67 of 67 |
| dispatch | rc 0, 74 of 74 controls and arms |
| counters | rc 0, 18 of 18 |
| GET_STREAM_INFO | rc 0, 23 detected, golden and restored PASS |
| name write | rc 0, mutant killed, golden and restored PASS |
| notifications | rc 0, 137 of 137 KILLED, goldens PASS |
| D3 | rc 0, 110 of 110 KILLED, six goldens PASS |
| elaboration-guard mutants | rc 0, 160 of 160 killed, control PASS |
| name_state | rc 0, 16 of 16 killed, golden PASS |

## 7. Parent: the corrected wiring and the conflict-and-move proof

Scratch parent `pp202-parent`, branch `scratch-pp202-a676c` from dev `e76a755a`, push URL invalid,
never pushed (`receipts/parent/PARENT-STATE.txt`): `309af35f59` gitlink at `9a6d1d08`;
`18561a20f0` the wiring and the legs; `cb22699767` the capture anchors; `dcd3273d09` the silence-fill classifier; `f0e3054da` pins final processor `ebb1f00`; `157e34c84` records the ROM digests. The round-2 branch and its records are kept as they were.

`parent-src-stream-id-wiring.patch` (this directory; sha256 in `receipts/parent/patch-record.txt`) = `git diff
309af35f59 dcd3273d09`:
- `KL_aaf_packetizer`: `stream_id_i` per talker and parameter `SID_PP_P` (default 0). With 1 every
  talker, t0 included, stamps `stream_id_i`; a TCTX uid feeds only the standalone derivation.
- `milan_datapath`: `.SID_PP_P(1'b1)`, `.stream_id_i(pp_cd_src_stream_id_w)`; GET_STREAM_INFO
  output selector 2 and the CRF Media Clock Output's stamp read `pp_cd_src_stream_id_w`;
  `KL_pp_shadow` passes `src_stream_id_o` out (as round 2).
- behave: a new step pins the precedence (`the integrated framer stamps the processor's current
  stream_id over any TCTX uid`).
- `tb/verilator/milan_dp`: `sim_sid_move.cpp`, `sidmove_probes.vlt`, legs `sidmove` (the shipping
  AX 1x1 shape: AAF talker 0 and the CRF output, uid 1) and `sidmove8` (8x8 shape: AAF talkers 0 and
  1, talker 1's TCTX uid named 1), both in `ORDINARY_CASES` so `milan_dp`'s sweep runs them.

Parent patch file map (at `18561a20f0`; paths relative to the scratch parent):

| File:line | Change | Clause / requirement |
|---|---|---|
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:131, 167, 504` | Explicit processor-owned ID selection, input, and stamp precedence | IEEE 1722-2016 4.4.4.8; decision item 7 |
| `hdl/milan/KL_pp_shadow.sv:716, 1451` | Forward the published per-source output | decision items 1 and 7 |
| `hdl/milan/milan_datapath.sv:1526, 1549, 2551, 6169, 7480, 9629` | AAF selection and wiring, CRF stamp, output GSI selector 2, processor connection | IEEE 1722-2016 4.4.4.8; IEEE 1722.1-2021 7.4.16.2 |
| `tb/verilator/milan_dp/Makefile:345, 600, 687, 855`; `sim_sid_move.cpp:1`; `sidmove_probes.vlt:1` (both in that directory) | Build and run both conflict-and-move legs in the ordinary gate | decision item 7; round-3 item 2 |
| `tests/features/milan_streaming_licence.feature:88`; `tests/steps/milan_streaming_licence_steps.py:360` | Pin integrated stamp precedence with two failing plants | decision item 7; round-3 item 2 |

The legs, on the crflic grid (1 ms = 100 cycles): the listener probes, MAAP claims, the switch
declares Listener Ready for the ID the PROBE_TX answer names, the sources stream; then a peer
ANNOUNCEs the claimed block from a lower MAC (IEEE 1722-2016 B.3.6.4), every declaring source
withdraws and moves, the listener re-probes and rebinds. Graded per source, before and after: the
PROBE_TX answer's stream_id and DA, GET_STREAM_INFO(STREAM_OUTPUT) stream_id, the Talker Advertise,
`src_stream_id_o`, and every AVTP PDU to the source's address; after: a new ID with the old upper
48 bits, declared under 2 s after the conflict (1,735 ms on AX 1x1, 1,778 ms on 8x8), the
withdrawn ID's Leave seen, no PDU with the withdrawn ID 50 ms after it. To answer AECP the legs
serve the shape's AEM image (regenerated with the builder and `gen_aemi_image.py`, as `sim_nxn`
does) and the response memory, and start the restore walk (PP_CTRL[1]).

| Leg / control | Result | Failing words |
|---|---|---|
| `sidmove` (AX 1x1) | rc 0, 50 checks, 0 failures | — |
| `sidmove8` (8x8, TCTX uid 1) | rc 0, 52 checks, 0 failures | — |
| control: round-2 precedence (`\|sid_in_w && !sid_named_w`), `sidmove8` | rc 2, 2 failures, both uid 1 | `[AFTER] no PDU carries the withdrawn ID 50 ms after its Leave (55)`; `[AFTER]: every one carries src_stream_id_o (else 0200000000010001)` |
| control: no wiring (the base laws), `sidmove` | rc 2, 6 failures, AAF and CRF | `[AFTER]: GET_STREAM_INFO selector 2 is src_stream_id_o`; `[AFTER]: every one carries src_stream_id_o (else 0200000000010000)`; `... (else 0200000000010001)`; the two `no PDU carries the withdrawn ID` checks |

Receipts: `receipts/parent/` (leg outputs, control outputs, `control-plants.txt`).

**A parent defect found on the way (outside #202, not fixed here).** `milan_datapath`'s maap face
source index is `PP_SRC_IDX_W_C = $clog2(N_STREAMS)` bits, while the processor's is
`$clog2(N_STREAM_OUT_P)` with `N_STREAM_OUT_P = ACMP_SRC_C = N_STREAMS + 1` when the shape has the
CRF output. On the 8x8 shape (9 sources, 3 bits against 4) source 8, the CRF output, requests as
source 0: the shim grants it source 0's address (both declare `...f838` in the first `sidmove8`
run), and its conflict event is delivered to source 0, so it never moves. The 4x4 shape (5
sources, 2 against 3) has the same truncation. AX 1x1 (2 sources, 1 bit each) is unaffected, which
is why the CRF output is graded on `sidmove`. Recommended: a parent issue for the pin-adoption
manager.

## 8. Consumer gate and final pin

| Consumer gate | Result at pin `9a6d1d08` + wiring |
|---|---|
| `pp_shadow` | rc 0; 2,187 checks, 0 failures; verdict rc 0; repeated at final pin `ebb1f00`, both rc 0 |
| `maap` | rc 0; 251 checks, 0 failures; verdict rc 0 |
| `milan_dp_render` | rc 0; 347 checks, 0 failures; verdict rc 0 |
| `capture_coherence` | corrected parent `cb22699767`: four whole-suite shards rc 0; 43 cases exactly once, checked observations verified by the case-union checker (rc 0); both repaired plants detected |
| `milan_dp` (all legs) | rc 0 at `dcd3273d09`, 13,685 checks, 0 failures; aggregate verdict rc 0; includes both new conflict legs and all render-law mutants |
| ROM-digest record and out-of-context validation | rc 0 at pin `9a6d1d08`; LUT 59,862, LUTRAM 4,236, FF 27,133, RAMB36 15, RAMB18 4, DSP 10, CARRY4 2,407; final-pin record rc 0, committed in `157e34c84` |
| static, specification, elaboration and parser gates | all rc 0; `receipts/consumer/` |

The suite counts above were read with the parent's `scripts/suite_tally.py`.
The inherited base consumer record (pin `ed211803`) has 2,187 `pp_shadow`, 251 `maap`, 347 `milan_dp_render`, and 13,583 `milan_dp` checks, all rc 0. Its capture receipt totals 21,721 embedded checks; the round-3 acceptance instead enumerates the 43 case identities and verifies their observations. The new datapath legs contribute 102 checks. Base OOC used 58,185 LUT and 26,948 FF; round 2 used 59,535 LUT and 27,133 FF; round 3 uses 59,862 LUT and 27,133 FF. These are historical comparisons, not new executions at the old pins; see `receipts/round2-records/HANDOFF.md` §8.
The scratch parent now pins `ebb1f00`; final-pin `pp_shadow` and its aggregate verdict passed (rc 0, 2,187 checks). `receipts/consumer-final/processor-consumed-inputs.diff` is empty (rc 0): processor `hdl`, `scripts`, `syn` and `Makefile` are identical at the full-gate pin and the final pin. Parent HDL is unchanged since `18561a20f0`.

## 9. Completion

All assigned findings are addressed, with their tests and planted faults above. Every required gate returned 0; failed setup and legacy-expectation attempts are retained and excluded in `receipts/VOID.md`. The scratch parent is committed at `157e34c84` with processor `ebb1f0010bde76c38cc5270a6366ee9e3157ec54` as its gitlink. Both tracked trees are clean; the processor also has no ignored build products. No push, PR creation/edit, merge, rebase, hardware operation, or additional top-level interface change was performed.

`INDEX.md` and `receipts/INDEX.md` are generated from the files present. Each retained file has a size and SHA-256; larger raw logs are represented by their hashes, sizes and bounded excerpts. `receipts/gate-status.json` indexes the accepted return-code records. The parent wiring patch remains separate for pin adoption.

## Resume audit

The resumed processor tree was clean at `ebb1f00`; the existing TAKEN comment was verified and not repeated. The earlier campaign and consumer processes were still alive and were retained until completion. The consumer receipt script produced numeric verdict filenames instead of the suite names; the actual `pp_shadow` and `maap` suite commands returned 0. Their verdict checks were rerun against the actual logs and returned 0. No failed verdict invocation is credited as a passing check.

Resource note on resume: the inherited parent capture-coherence default launched 16 workers (its CPU-affinity default). At about 9.4 GB MemoryCurrent, the service MemoryHigh was set to 8 GiB to trigger reclaim/throttling below the 10 GB target; MemoryMax remains the existing 12 GB limit. No gate result is inferred from resource controls.

Capture gate repair: `tb/verilator/capture_coherence/mutants.py:135, 277, 293` matches the AAF input-delay parameter binding alone, rather than assuming it ends the parameter list. Adding `SID_PP_P` made both old anchors miss. The fixed-delay-minus-one-period and excessive-fixed-delay plants are retained with their original wire/grid and refusal checks. Parent commit `cb22699767` is included in the wiring patch; the first failed run is retained and not credited as passing.

Capture rerun custody: all four accepted shards ran in the isolated clone at `cb22699767`, with identical gitlinks. The official union check verified 43 cases exactly once and their recorded observations. An earlier shard in the main parent was cancelled (rc 143) because ROM-ledger generation changed its source during execution; it is excluded.

The dependency pin proof rejects an added push-URL setting. Removing that setting from `tsn-c-stack` restored the exact-pin proof; its canonical origin and source revision are unchanged. No push occurred.

The complete datapath run exposed an existing silence-fill classifier that still expected the explicit TCTX UID 5 to stamp talker 1. Parent commit `dcd3273d09` updates `tb/verilator/milan_dp/sim_nxn.cpp:7475, 7497` to expect the processor-owned UID 1 (IEEE 1722-2016 4.4.4.8; processor #202). It retains all silence, format, liveness and foreign-ID checks. The prior patch-precedence control is the corresponding planted defect; the dedicated conflict case already detects it after the move. The initial four failures are preserved in `receipts/consumer-rerun/milan_dp.excerpt.txt`; the complete replacement gate passed (rc 0, 13,685 checks, 0 failures), as did its aggregate verdict.
