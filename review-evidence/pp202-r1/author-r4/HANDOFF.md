# [A676d] processor #202 round 4 — HANDOFF

**Status: REVIEW READY. Every required gate returned 0; no STOP condition met.**
TAKEN: issue #202 issuecomment-6421137774. REVIEW READY: issue #202 issuecomment-6429376528.

Round-4 assignment: issue #202 issuecomment-6421118089, answering R709-2 (PR #204
issuecomment-6420727339) and R710-2 (PR #204 issuecomment-6421117210). Owner decision in force:
issuecomment-6408987895 (option A); round-3 assignment issuecomment-6414935566.

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked before the first commit; the branch's merge base and `origin/main` were `ed211803`, and the checked-out start was the round-3 head `ebb1f001`, as the assignment says) |
| Branch | `202-maap-conflict-new-stream-id` (local; not pushed) |
| Base (processor main) | `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8` |
| Round-3 head (start) | `ebb1f0010bde76c38cc5270a6366ee9e3157ec54` |
| Head | `429c909cb8a60398a2028436932e04b95dd0a0bd`, tree `338b112f854a16ef831c39dc1b3a3f66108190a2` (RTL as at `ffc76f1741e355bea3d2aa78f232a56a3db3d241`) |
| Scratch parent | the committed local clone `pp202-parent`, branch `scratch-pp202-a676d` from round 3's `dcd3273d09` (dev `e76a755a` with the wiring), push URL invalid, never pushed (§7) |

Round-4 commits on `ebb1f001` (one-line subjects, no body, no trailers):

1. `83107719` Quarantine moved Stream IDs for two LeaveAll periods, keep a fast return's owed Leave in the SRP talker, and name the disable move in the two port comments (issue #202)
2. `59f34d3d` State the Stream ID quarantine and its proof in F05.12, the timing row and the interface documents, and the talker's owed Leave on a fast re-open in 10 (issue #202)
3. `3cf53348` Grade a configured Stream ID's exclusion past its source's quarantine record, a minute after the source moved off it (issue #202)
4. `7e0ff0ba` Record the quarantine and owed-Leave cases, their planted arms and the re-measured talker, stream-FSM, SRP, processor-top and MAAP campaign counts (issue #202)
5. `ffc76f17` Lay the talker's SRP leave copy out at 128 bits a source with the stream_id at bit 0, so its two variable-index reads are multiplexers, not barrel shifters (issue #202)
6. `429c909c` Name the commit the SRP, processor-top and talker retry campaign records were measured at (issue #202)

Why commits 3 and 5 exist:

- Commit 3: the first full ACMP campaign at `59f34d3d` left `move_ignores_configured_ids` with
  its named check passing. S3's `...09` was refused by src7's young quarantine record as well as
  by the configured-ID term, so the record hid the term. S3 now moves src0 a minute after src7
  left its configured ID, past the record.
- Commit 5: the parent's out-of-context synthesis at the `7e0ff0ba` pin measured `KL_pp_shadow`
  at 66,724 LUT against round 3's 59,862. Synthesizing the two changed modules alone at
  8 sources attributed it: `KL_acmp_talker` 3,434 → 4,228 LUT (the quarantine), and
  `KL_srp_talker_fsm` 7,373 → 12,964 LUT. In the SRP talker, the leave copy's 124-bit stride
  with the stream_id at an offset made the gate-source read of the held stream_id a
  `$shiftx_1020` and the walk read a `$shiftx_992`, both barrel shifters (about 4,300 LUT). At a
  128-bit stride with the stream_id at bit 0, both are `$shiftx_1024`, which maps to a
  multiplexer: `KL_srp_talker_fsm` 8,948 LUT (+1,575 over round 3), with the same 2,641
  flip-flops. Behaviour is unchanged; every gate that builds the SRP talker was run again at
  `ffc76f17`, and the earlier runs are kept as superseded records (`receipts/records/VOID.md`).

## 2. What each finding asked, and what was done

| Finding | Done | Where |
|---|---|---|
| R709-2 F1 (MINOR): a disable and return inside one `T-MRP-JOIN` replaces the withdrawn ID's owed Leave with the moved ID's Join! | **RTL (option a), at the SRP applicant**: a gate re-open under another stream_id while the applicant is LA or LO leaves the applicant on the old value in a leave copy until its next tx! sends the owed Lv (or the Empty of LO), with the FirstValue it was declared with; the re-open's Join! waits for that tx!, so the new value's first Talker Advertise goes out one `T-MRP-JOIN` later. The listener's #188 rule, for the talker. 10 no longer cites Table 10-3 across two attribute values | §3 rows 6-9; tests TP1-TP9, WK13, MP9; 15 SRP patches and `moved_open_skips_leave` |
| R710-2 F01 (MINOR): disable-triggered moves can lap the cursor and reuse a historical ID 403 ms after its withdrawal | **a time-qualified quarantine** in the move search: per-source records of left IDs (refused for more than 30 s, kept while younger), and a cursor guard (a half of the unique IDs is re-entered only four 30 s epochs after the cursor left it). A search the guard blocks takes no ID: the source keeps its ID and waits `T-SRP-LEAVEALL2` from the grant. 05 proves that no move takes an ID declared within 30 s, whatever the rate of disables | §3 rows 1-5; tests S5 (history oracle), S11 (R710-2's fast lap); six `STREAM_ID` arms |
| R709-2 F2 / R710-2 F02 (MINOR): the 8x8 recovery figure | re-measured at this round's RTL: 1,735 ms on AX 1x1 and 1,816 ms on 8x8, the published receipts' values; the PR body states those and cites this round's receipt | `receipts/parent/consumer/milan_dp.sidmove-legs.txt` (the two legs from the full log: 50 and 52 checks, 0 failures) |
| R709-2 RESIDUE-1: two port comments omit the disable move | reworded as asked | §3 row 10 |
| R709-2 RESIDUE-2 / R710-2 R01: the PR body says it supersedes itself | the body says "This revision addresses the reviews of PR #204 at `a8aa626e` (R710-1, R709-1) and at `ebb1f001` (R709-2, R710-2)" | `PR-BODY.md` |
| R710-2 R02: bench identifiers in the parent patch's source comments | `[BOOT]`, `[A]`, `[MOVE]`, `[AFTER]` headings become boot, bind, move, after; `obj_sidmove:` becomes "Protocol processor #202 recovery:"; the elaborations are named by their 1x1 and 8x8 shapes; "crflic grid" becomes "shared compressed millisecond grid", "TSPEC8 shape" "8x8 shape", "the three sources" "the graded sources"; the `make sidmove / sidmove8` usage moved to the bench README; three more comment-only bench names reworded. Every changed line outside the README is a comment; executable target names, assertion strings and receipt labels are unchanged | `receipts/records/round4-parent-comment.diff` |
| R709-2 SUG-1 | superseded: 05's lap argument is replaced by the quarantine proof, which needs no rate assumption | 05 `sec-05-sidq` |
| R709-2 SUG-2, SUG-3 | not done (outside the assignment) | — |

## 3. Changes (file:line at head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/acmp/KL_acmp_talker.sv:42-104` | banner: the move rule with the quarantine, the distinctness and no-reuse arguments | 802.1Q-2018 35.2.2.8, Table 10-7; Milan v1.2 Table 5.3 |
| 2 | `hdl/acmp/KL_acmp_talker.sv:472-491` | `SIDQ_MS_C` (30 s), epoch timer, per-source records `sid_rec_*`, cursor guard `sid_half_r`/`sid_oth_*`, `sid_none_r` | 802.1Q-2018 35.2.2.8; `T-MRP-LEAVEALL` 10-15 s (F08.1) |
| 3 | `hdl/acmp/KL_acmp_talker.sv:870-900` | `EVC_GRANT`: a search with no ID keeps the ID and enters `BACKOFF` with a `T-SRP-LEAVEALL2` draw | 802.1Q-2018 35.2.2.8 |
| 4 | `hdl/acmp/KL_acmp_talker.sv:1169-1176` | `S_EV_SID`: records refuse, the guard ends the search; bound 3 x P-N-STREAM-OUT + 1 | — |
| 5 | `hdl/acmp/KL_acmp_talker.sv:1409-1496` | `sid_quarantine` (record hit, guard block) and `sid_state` (epoch ageing, record write unless young, half crossing, keep path) | 802.1Q-2018 35.2.2.8 |
| 6 | `hdl/srp/KL_srp_talker_fsm.sv:55-69` | banner: a re-open never abandons the withdrawal's Leave | 802.1Q-2018 10.7.7, Table 10-3 |
| 7 | `hdl/srp/KL_srp_talker_fsm.sv:394-402, 440, 481-492, 508-518` | `lvp_r`, `lvj_r`, `lwid_r` (128-bit stride, stream_id at bit 0); no received value reaches a parked applicant; `hsid_w`/`gpark_w`/`gnew_w`; a parking open gives the applicant no event; the waiting Join! once the park ends | 802.1Q-2018 10.7.7, Table 10-3 |
| 8 | `hdl/srp/KL_srp_talker_fsm.sv:583-608` | the walk reads the parked FirstValue; the leave copy (flip-flops, one enable per source; TSpec in distributed RAM) | 802.1Q-2018 10.7.6, Table 10-3 |
| 9 | `hdl/srp/KL_srp_talker_fsm.sv:667-673, 693-695` | the gate open parks or un-parks, a close drops the waiting Join!; a tx! ends the park, a txLA! keeps it | 802.1Q-2018 Table 10-3 |
| 10 | `hdl/top/protocol_processor_top.sv:680-686`, `hdl/acmp/KL_acmp_talker.sv:325-332` | the two port comments name the disable move | R709-2 RESIDUE-1 |
| 11 | `docs/architecture/05_acmp_engine.md:442, 497-506, 509-512, 516-575` | F05.12 arc for the keep path; the owed Leave; "Together"; the move rule, `sec-05-sidq` and both proofs | 802.1Q-2018 35.2.2.8, 10.7.7 |
| 12 | `docs/architecture/10_srp_engine.md:214, 432-438, 464-491` | storage row; the Join! statement for a new value; `sec-10-talker-owed-leave` | 802.1Q-2018 10.7.5.5, 10.7.7, Table 10-3 |
| 13 | `docs/architecture/08_timing.md:36`, `docs/00_MILAN_COMPLIANCE_REVIEW.md:407`, `docs/architecture/02_interfaces.md:303-305, 566`, `docs/guides/integrator.md:338-341`, `docs/architecture/09_verification.md:795-799, 809-811` | the timing row (keep path, 30 s), REQ-ACMP-010, the maap face and status dictionary, the integrator note, the evidence map | as above |
| 14 | `tb/acmp_talker/sid_cases.hpp:19-48, 230-246, 318-435, 437-497, 662-675` | `SidHistory` (every declaration against the last withdrawal of its ID); S3 past the record; S5 re-timed with records and the oracle; S11 | 802.1Q-2018 35.2.2.8 |
| 15 | `tb/srp_stream_fsms/sim_main.cpp:2240-2444`, `walk_main.cpp:41-46, 552-589` | TP1-TP9; WK13 at the four walk shapes | 802.1Q-2018 10.7.7, Table 10-3 |
| 16 | `tb/pp_top/sim_main.cpp:9464-9516`, `tb/pp_top/pp_top_wrap.sv:27-28, 259, 566` | MP9; the bench's test-only `cfg_src_off_i` (0 everywhere else) | 802.1Q-2018 10.7.7 |
| 17 | `tb/pp_top/acmp_mutants.py:560-601`, `tb/srp_top/mutants.py:258-282, 357`, `tb/srp_top/mutations/{talker-*,walk-ignores-talker-leave-copy,lwid-*,lwtsp-read-at-gate-source}.patch` | seven `STREAM_ID` arms; fifteen SRP patches, coverage TP1-TP9 and WK13 | — |
| 18 | `tb/acmp_talker/README.md`, `tb/srp_stream_fsms/README.md`, `tb/srp_top/README.md`, `tb/pp_top/README.md`, `tb/maap/README.md` | case tables and re-measured records | — |

## 4. New checks, planted mutants, failing words

Talker suite 1,520 → 1,540 checks; `srp_stream_fsms` 1,422 → 1,435 (walk arms 43/57/87/155 →
48/64/96/176 at 1/1, 2/2, 3/5, 9/9); `pp_top` 10,750 → 10,753 (MP 43 → 46).

On the round-3 RTL (`ebb1f001`), with this round's benches (`receipts/tests/old-rtl/`):

- talker 8 FAIL, among them `S5 no ID is declared again with another DA inside two LeaveAllTime periods (1, first ab00000000000008 after 65 ms)` and `S11 no ID is declared again with another DA inside two LeaveAllTime periods (4472, first ab00000000000008 after 0 ms)` (R710-2's shape);
- stream FSMs: suite 9 FAIL (`TP1: the next tx! sends the withdrawn stream's Lv with the FirstValue it was declared with, and nothing for the new one (1 pushes, code 3)`, TP4, TP6, TP7 x2, TP8, TP9) and walk 2/3/4/10 FAIL of WK13 at the four shapes;
- `pp_top` MP: `MP9: a disable and return granted at once still sends the withdrawn ID's Lv, before the new ID's first Talker Advertise (frames -1, 0)` (R709-2's PROBE arm, on the wire).

| Check (words as printed) | Killed by (planted defect): failing checks |
|---|---|
| `S5 no ID is declared again with another DA inside two LeaveAllTime periods`, `S5 after the cursor wraps a move skips every configured ID, the IDs ...` | `move_ignores_left_ids` (records refuse nothing): 2 |
| `S5 after the cursor wraps ...` | `record_lapses_in_one_epoch` (refused at age 0 only): 1; `record_overwritten_while_young` (always written): 1 |
| `S11 a return the cursor guard blocks keeps its ID and waits T-SRP-LEAVEALL2`, `S11 no ID is declared again with another DA ...` | `cursor_reenters_early` (guard removed): 6; `blocked_move_declares_at_once` (keep path removed): 6 |
| `S11 three quarantine epochs after the cursor left the lower half a return still keeps its ID` | `cursor_guard_three_epochs`: 2 |
| `S3 a move never takes another source's configured ID after that source moved off it` | `move_ignores_configured_ids` (existing arm, now graded past the record): 3 |
| `MP9: a disable and return granted at once still sends the withdrawn ID's Lv` | `moved_open_skips_leave` (`gpark_w` forced 0): 1 in the MP section |
| TP1 ... TP9, WK13 | the 15 SRP patches, each its named check (`tb/srp_top/README.md`, issue #202 section) |

The counts above are those of the runs at `ffc76f17` (identical to the runs at `3cf53348`).

## 5. Same-Stream-ID paths, enumerated

After an ID has been declared and withdrawn:

- withdrawn by a lapsed gate (`DA_OK`): the DA is kept; a PCP change → `BACKOFF` (gap); otherwise the next declaration has the FirstValue it was withdrawn with;
- withdrawn by a PCP change (`BACKOFF`): the existing gap;
- withdrawn by a conflict or a disable (`NO_DA`): a move is booked; the grant takes a new ID outside the quarantine, or, when the guard blocks the search, keeps the ID and waits `T-SRP-LEAVEALL2` from the grant;
- an ID another source left: refused by that source's record for more than 30 s, or out of the cursor's reach for more than 90 s (05 proof);
- TSpec, rank, accumulated latency: quasi-static (02 §2 rule 4); changed while the source is disabled, covered by the move.

## 6. Processor gates (every `.rc` is the command's own exit status, never through a pipe)

Local tools: Verilator 5.052 (CI pins 5.050) through a PATH wrapper that turns a build's
`-j 0` into `-j 2` to `-j 6`, so concurrent runs share the unit's 16 CPUs; Yosys and sv2v as
installed. Results do not depend on the wrapper. Every gate ran in a disposable clone, never in
the lane tree.

| Gate | Base `ed211803` (round-2 record) | Round-3 head `ebb1f001` (round-3 record) | This round |
|---|---|---|---|
| `./scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,399 | rc 0, 1,030,552 (at `9a6d1d08`) | rc 0, 1,030,588 checks, 0 failing, at `ffc76f17`; only `acmp_talker` 1,520 → 1,540, `pp_top` 10,750 → 10,753 and `srp_stream_fsms` 1,422 → 1,435 move |
| `check-req-tags.py --suites … --evidence …` | rc 0 | rc 0, 241 tags | rc 0, 245 tags in 20 files, 245 evidence lines, 14 suites |
| `./scripts/lint_hdl.sh` | rc 0 | rc 0 | rc 0 at `ffc76f17` and at `429c909c` |
| `make check` | rc 0 | rc 0 | rc 0 at `ffc76f17` and at `429c909c` |
| `./syn/yosys/run.sh` | — | rc 0 | rc 0 at `ffc76f17` (42 tops) |
| `tb/elab_guards/guards.py --frontend yosys --jobs 4` | — | 93 of 93 | rc 0, 93 of 93 at `ffc76f17` |
| `tb/acmp_talker` | — | 1,520 | rc 0, 1,540 at `ffc76f17` and at `429c909c` |

`ffc76f17..429c909c` changes three test READMEs only. The suite inputs of `3cf53348` and
`ffc76f17` differ only in `KL_srp_talker_fsm`'s leave-copy layout and the 15 SRP patches; the
sweep at `ffc76f17` has every tally of the sweep at `3cf53348`.

| Campaign | Result |
|---|---|
| `tb/pp_top/acmp_mutants.py` (at `ffc76f17`, `--jobs 3`) | rc 0, 97 of 97 KILLED, eight goldens PASS; `STREAM_ID` 32 of 32 (29 names); every count identical to the run at `3cf53348` |
| `tb/srp_top/mutants.py` (at `ffc76f17`) | rc 0, 207 arm runs KILLED, 18 controls PASS, assertion coverage 142 of 142, `226 checks: 226 PASS, 0 FAIL` |
| `tb/acmp_talker/retry_mutants.py` (at `3cf53348`, the talker RTL and suite of the head) | rc 0, 62 killed, 7 equivalent, 1 performance control, baseline and restored 1,540; eight with more failing assertions (README re-measured) |
| `tb/maap/mutants.py` | rc 0, 29 of 29 KILLED, 3 controls PASS; pp_top arms 4 and 15 FAIL of 46 |
| AECP deadline and hazard class | rc 0, 67 of 67 |
| dispatch | rc 0, 74 of 74 |
| counters | rc 0, 18 of 18 |
| GET_STREAM_INFO | rc 0, 23 detected, golden and restored PASS |
| name write | rc 0, mutant killed, golden and restored PASS |
| notifications | rc 0, 137 of 137 KILLED, goldens PASS |
| D3 (`--jobs 7`) | rc 0, 110 of 110 KILLED, six goldens PASS |
| elaboration-guard mutants | rc 0, 160 of 160 killed |
| name_state | rc 0, 16 of 16 killed, golden PASS |

Area, out of context (yosys `synth_xilinx -family xc7 -flatten`, `receipts/area/`): at 8
sources `KL_acmp_talker` 3,434 → 4,228 LUT and 838 → 1,028 FF; `KL_srp_talker_fsm` 7,373 →
8,948 LUT and 1,630 → 2,641 FF (12,964 LUT before the stride fix). The parent's
`KL_pp_shadow`: 59,862 LUT, 27,133 FF in round 3; 61,219 LUT, 4,332 LUTRAM, 28,334 FF here.

## 7. Parent: the wiring patch and the conflict-and-move legs

Scratch parent `pp202-parent`, branch `scratch-pp202-a676d` from round 3's `dcd3273d09`,
push URL invalid, never pushed (`receipts/records/PARENT-STATE.txt`). Local commits this round:
`fe68644177` and `d3ab5b37f5` (comment fixes, README rows), `e9f3263f0b` (pin `59f34d3d`),
`33772611bb` (pin `7e0ff0ba`), `a5a1034639` (pin `ffc76f17`: the consumer gate), `e28bb468c9`
(pin `429c909c`, the final head), `2eb0139126` (ROM digests for that pin). HEAD `2eb0139126`,
tree `8608474fea`.

`parent-src-stream-id-wiring.patch` (this directory; `receipts/records/patch-record.txt`) =
`git diff 309af35f59 d3ab5b37f5 -- . ':(exclude)protocol-processor'`: round 3's wiring with
this round's comment fixes. Against round 3's patch (sha256 `c8a74c2a…`) only comment lines,
hunk offsets and the two bench README rows differ (`receipts/records/round4-parent-comment.diff`;
every changed line outside the README is a comment). The legs, the wiring and the patch file map
are as in round 3's hand-over §7: `sidmove` (AX 1x1, AAF talker 0 and the CRF output) and
`sidmove8` (8x8, AAF talkers 0 and 1, talker 1's TCTX uid named), both in `ORDINARY_CASES`.

Recovery figures at this round's RTL (`receipts/parent/consumer/milan_dp.sidmove-legs.txt`): conflict to the
new ID's declaration 1,735 ms on AX 1x1 and 1,816 ms on 8x8, both graded sources each; the
published round-3 receipts recorded the same values.

The parent maap-face source-index width defect on 4x4/8x8 shapes, found in round 3, is unchanged
and outside #202; it stays for the pin adoption.

## 8. Consumer gate and final pin

| Consumer gate (processor pinned at `ffc76f17`, parent `a5a1034639`) | Result |
|---|---|
| static: `lint_rtl`, port contracts, wire accountability, SV idiom, RTL source lists, behave, yosys elaboration of `milan_datapath`/`KL_pp_shadow`/`KL_gptp_shadow`, the parser gate | all rc 0 |
| `pp_shadow` | rc 0; 2,187 checks, 0 failures; verdict rc 0 |
| `maap` | rc 0; 251 checks, 0 failures; verdict rc 0 |
| `milan_dp_render` | rc 0; 347 checks, 0 failures; verdict rc 0 |
| `milan_dp` (all legs) | rc 0; 13,685 checks, 0 failures; verdict rc 0; both recovery legs pass |
| `capture_coherence` | four whole-suite shards rc 0; case union rc 0: 43 cases exactly once, observations verified |
| tally (`scripts/suite_tally.py`) | 16,470 checks, 0 in-suite failures, identical to round 3 |

| Final pin (processor `429c909c`, parent `e28bb468c9` then `2eb0139126`) | Result |
|---|---|
| processor consumed inputs `hdl`, `scripts`, `syn`, `Makefile` between `ffc76f17` and `429c909c` | empty diff |
| ROM-digest record (`./syn/yosys/ooc.sh --record-rom-digests`) | rc 0; digests for `429c909c` recorded (the same ROM contents as before), committed in `2eb0139126` |
| `pp_shadow` and its verdict | rc 0; 2,187 checks, 0 failures |
| out-of-context `./syn/yosys/ooc.sh KL_pp_shadow` | rc 0; 61,219 LUT, 4,332 LUTRAM, 28,334 FF, 15 RAMB36, 4 RAMB18, 10 DSP, 2,428 CARRY4 |

## 9. Completion

Every assigned finding is addressed at its cause, each with a test that fails on `ebb1f001` and
planted faults killed by named checks. Every required gate returned 0. Superseded and stopped
runs are kept and excluded (`receipts/records/VOID.md`): the first ACMP campaign at `59f34d3d` (the S3
masking), the runs before the stride fix, and runs stopped at the session's two-hour background
limit or on purpose when superseded. The scratch parent is committed at `2eb0139126` with
processor `429c909c` as its gitlink. The processor tree is clean, ignored files included. No
push, PR creation or edit, merge, rebase, hardware operation, or top-level interface change
other than `src_stream_id_o` was performed.

Resources: one service unit of 16 CPUs; no CPU range was free for shard units
(`cpu_ranges.py` reported every 16- and 12-CPU range busy), so the sweep and the campaigns ran
inside the unit. Its `memory.current`, which counts page cache, peaked at 11.5 GiB at
18:16 UTC on 2026-10-26 with about 4.2 GB anonymous; MemoryHigh was then set to 9 GiB on the unit, and the sampled
maximum afterwards was 9.00 GiB (`receipts/records/resources.txt`).

`INDEX.md` and `receipts/INDEX.md` are generated from the files present. `receipts/gate-status.json`
indexes the accepted return-code records and the expected failures on the round-3 RTL. Files
over 190 KB are kept as their size, sha256 and last 80 lines; `receipts/RAW-RECORDS-*.csv`
list every raw record with its size and sha256, and the per-arm logs of superseded runs are kept
as per-directory digests (`receipts/void/PER-ARM-DIGESTS.txt`). Every directory has its own
generated `INDEX.md`. Local paths in receipts are normalized.
