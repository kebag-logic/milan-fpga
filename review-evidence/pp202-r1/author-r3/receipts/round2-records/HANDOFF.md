# [A676b] processor #202 round 2 — HANDOFF

**Status: REVIEW READY at head `a8aa626e1cba30625ac764c70e1fb8fb02c69c40`. Every gate is rc 0;
no STOP condition was hit.** TAKEN: issue #202 issuecomment-6408995638. REVIEW READY: see §10.

## 1. Records

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked and HEAD was ed211803 before the first commit) |
| Branch | `202-maap-conflict-new-stream-id` (local; not pushed, no PR) |
| Base (processor main) | `ed2118035e4cec76fb1b59cfbf8a053aeacc8af8` |
| Head | `a8aa626e1cba30625ac764c70e1fb8fb02c69c40`, four commits on base |
| Decision implemented | issuecomment-6408987895 (owner decision, option A) |
| Scratch parent | milan-fpga dev `e76a755afc0536453161e3cd33f6f4d2dcd7641f`, gitlink `a8aa626e`, never pushed (§6) |

Commits (one-line subjects, no body, no trailers):

1. `2a4f2142` Move a declared source to a new distinct Stream ID at the first grant after a MAAP conflict, declare it at once with no two-LeaveAll wait, and publish it on src_stream_id_o (issue #202)
2. `1e0c83df` State the Stream ID move rule and its distinctness proof, name src_stream_id_o, and limit the two-LeaveAllTime gap to the same Stream ID in the architecture, interface and compliance documents (issue #202)
3. `bba84945` Publish src_stream_id_o as a spelled-out expression, since yosys elaborates a function called with a genvar as a constant function (issue #202)
4. `a8aa626e` Label F05.12's backoff exit with the booked move a conflict inside the backoff installs, and widen the integrator guide's move condition to any declared ID (issue #202)

Commit 3: the portability gate (`syn/yosys/run.sh`) refused commit 1's `cur_sid_f(SRC_W_C'(g))`
inside a generate loop ("Non-constant expression in constant function"). Commit 4 is two
document lines found in review. Commit 4 changes nothing under `hdl/`, `tb/`, `scripts/`,
`syn/` or the `Makefile` relative to `bba84945` (`receipts/base-head-records.txt`), so the
suite and campaign records taken at `bba84945` are records of the final head's build inputs;
the gates that read documents (lint, `make check`, the portability elaboration) were rerun at
`a8aa626e`. The AECP, dispatch, counters, Milan-info, name-write, notification, D3, elaboration-
guard and name-state campaigns ran at `a8aa626e` itself. Runs started at `1e0c83df` were
stopped and set aside, never used.

## 2. Behaviour (decision items 1 to 4)

- **Port.** `protocol_processor_top` gains exactly one output, `src_stream_id_o[N_STREAM_OUT_P*64-1:0]`,
  each source's current Stream ID; after reset it equals the `cfg_stream_id_i` slice. No other
  port, parameter or register map changed.
- **Conflict path.** A MAAP conflict on a declaring source withdraws at once, invalidates the DA
  and re-allocates at once (no PRNG draw, no `T-SRP-LEAVEALL2` arm). The next successful
  `ALLOC_DA` installs the new Stream ID and, if the gate is true, declares it in the same walk.
- **Rule (deterministic).** Keep the slot's upper 48 bits; the new unique ID is the first value,
  counted up modulo 2^16 from a move cursor, for which {upper 48, u} is no source's current ID
  and no source's configured ID; the cursor then passes it. The cursor starts at
  `P-N-STREAM-OUT` (the first unique ID past the default {MAC, s}).
- **Distinctness proof (05 §sec-05-sidmove).** At most 2N IDs are excluded, so one of the first
  2N+1 candidates is free (the search, one candidate per clock in walker state `S_EV_SID`, ends
  within that many clocks). The chosen whole 64-bit ID equals no current ID, the withdrawn one
  included, whatever the slots are provisioned with. Only a move changes a current ID and every
  move checks every other current ID. Configured IDs stay excluded after their source moved
  off them, and the cursor revisits no moved ID inside a 2^16 lap. The proof needs nothing but
  `cfg_stream_id_i` and internal flops: no second output (the decision's STOP condition does not
  apply).
- **Booking.** Any conflict books the move once the source's current ID has been declared since
  reset or its last move: also after a withdrawal on a lapsed gate, inside a PCP backoff, or
  while disabled. A never-declared ID is not moved (§7, note 1).
- **Reporting.** `PROBE_TX` answers `TALKER_DEST_MAC_FAILED` until the grant and SUCCESS with the
  new ID and DA from it; GET_TX_STATE, `DECLARE_TALKER` (the Talker Advertise) and
  `src_stream_id_o` carry the current ID.
- **PCP path.** Unchanged: withdraw, `T-SRP-LEAVEALL2`, re-declare with the same Stream ID
  (IEEE 802.1Q-2018 35.2.2.8; the PCP is in PriorityAndRank, 35.2.2.8.5).

## 3. Changes (file:line at head, clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/acmp/KL_acmp_talker.sv:34-47` | DA-gate banner: PCP keeps the gap; a conflict re-allocates at once; the booking rule | 802.1Q-2018 35.2.2.8 |
| `hdl/acmp/KL_acmp_talker.sv:50-78` | the move rule and its distinctness argument | 802.1Q-2018 35.2.2.8, Table 10-7; Milan v1.2 Table 5.3 (5.3.7.5) |
| `hdl/acmp/KL_acmp_talker.sv:298-305` | output `src_stream_id_o` | IEEE 1722-2016 4.4.4.8; IEEE 1722.1-2021 7.4.16.2 |
| `hdl/acmp/KL_acmp_talker.sv:429-450` | move state flops and `cur_sid_f` | — |
| `hdl/acmp/KL_acmp_talker.sv:608` | walker state `S_EV_SID` | — |
| `hdl/acmp/KL_acmp_talker.sv:811-813` | a grant installs a booked move | Milan v1.2 5.5.4.1 step 3 |
| `hdl/acmp/KL_acmp_talker.sv:851-866` | `EVC_CONFLICT`: book the move when the ID has been declared; from DECLARING withdraw, NO_DA, re-allocate at once (was BACKOFF + draw) | 802.1Q-2018 35.2.2.8 |
| `hdl/acmp/KL_acmp_talker.sv:870-871` | `EVC_PCP`: same Stream ID, keeps the gap | 802.1Q-2018 35.2.2.8.5 |
| `hdl/acmp/KL_acmp_talker.sv:1074-1092` | `S_EV_REC` routes a moving grant to `S_EV_SID`; one candidate per clock | — |
| `hdl/acmp/KL_acmp_talker.sv:1302-1323` | the search comparators: configured and moved IDs of every source, whole 64 bits | Milan v1.2 Table 5.3 (streams of one interface distinguished) |
| `hdl/acmp/KL_acmp_talker.sv:1325-1356` | `sid_state`: book, install, cursor, declared mark | — |
| `hdl/acmp/KL_acmp_talker.sv:1357-1364` | the published level, spelled out | — |
| `hdl/acmp/KL_acmp_talker.sv:1447,1470,1500,1507` | PROBE_TX, GET_TX_STATE and both gate strobes read the current ID; the moving grant's strobe carries the new one | Milan v1.2 Table 5.43, 5.5.4.3 |
| `hdl/top/protocol_processor_top.sv:680-686,2356` | the one new port and its connection | decision item 1 |
| `tb/pp_top/pp_top_wrap.sv:268-270,809` | the wrap passes it out | — |
| `docs/architecture/05_acmp_engine.md:415,421` | F05.11: the current stream_id | — |
| `docs/architecture/05_acmp_engine.md:435-448` | F05.12 | 802.1Q-2018 35.2.2.8 |
| `docs/architecture/05_acmp_engine.md:453-510` | §sec-05-sidmove: clauses, the three cases, the rule, the proof, the integrator obligation | as above |
| `docs/architecture/05_acmp_engine.md:526,533` | allocation recovery: a declaring conflict queues allocation at once; the PCP backoff is never shortened | — |
| `docs/architecture/08_timing.md:36` | `T-SRP-LEAVEALL2`: same Stream ID only; 802.1Q-2018 35.2.2.8 and Table 10-7 normative, Table 5.3 informative | decision item 5 |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:406` (and `:141`, `:214`) | REQ-ACMP-010 corrected; the GAP-04 and GAP-07 summaries follow | decision item 5 |
| `docs/architecture/02_interfaces.md:271,298-301,424,562` | `DECLARE_TALKER` carries the current ID; the `maap` event flow; the avtp row; F02.10's `src_stream_id[src]` | decision item 1 |
| `docs/architecture/10_srp_engine.md:337-341,423-429` | the PCP flow keeps the ID and its normative gap; every gate open latches the ID and restarts the Listener registrar | 802.1Q-2018 35.2.2.8 |
| `docs/architecture/06_aecp_engine.md:384-391` | an output's selector 2 answers `src_stream_id_o` | IEEE 1722.1-2021 7.4.16.2 |
| `docs/architecture/09_verification.md:793-811` | §8.13 evidence map | — |
| `docs/guides/integrator.md:332-337,563` | `cfg_stream_id_i` is the reset value; stamp and answer `src_stream_id_o` | — |
| `docs/diagrams/21-integration-faces.svg:119` | class-D line names `src_stream_id_o` (hand-authored; rendered to PNG and inspected) | — |
| `tb/acmp_talker/sim_main.cpp:699-751,768-770,810-811` | section E rewritten for the new path (E1 to E5); E7 and F5 ID checks | — |
| `tb/acmp_talker/sid_cases.hpp` (new) | section S1 to S6 | — |
| `tb/acmp_talker/retry_cases.hpp:199-228,331-332,432-437` | R6, R12, R16 on the new path | — |
| `tb/pp_top/sim_main.cpp:929,1808-1812,9381-9451` | decl rise log; MP8a (called inside MP4) and MP8 | — |
| `tb/pp_top/acmp_mutants.py:416-516` | group `STREAM_ID` (20 arm runs, 17 names) | — |
| `tb/acmp_talker/README.md`, `tb/pp_top/README.md`, `tb/maap/README.md` | records re-measured at head | — |

## 4. New checks, planted mutants, failing words

Talker suite `tb/acmp_talker` 1,376 → 1,463 checks; `tb/pp_top` 10,741 → 10,749 (MP8a, MP8).

| Check (words as printed) | Where | Killed by (planted defect) |
|---|---|---|
| `E1 no backoff: no LEAVEALL2 draw … and no timer arm` | `sim_main.cpp` E | `conflict_keeps_old_wait` (the old BACKOFF + draw restored) |
| `E3 re-declare new DA open sid` | E | `conflict_reuses_old_id` (no move booked), `declare_carries_configured_id` |
| `E3 src_stream_id_o follows the move` | E | `output_ignores_move` (the port publishes the configured slice) |
| `E4 new DA answered`, `E5 probe after the grant` | E | `tx_state_answers_configured_id`, `probe_answers_configured_id` |
| `F5 re-declare src3 same DA open sid`, `F5 the PCP path keeps the Stream ID` | F | `declare_carries_configured_id`, `output_ignores_move` |
| `S1 ALLOC_DA offered in the conflict's millisecond`, `S1 conflict to new declaration under 2 s` | `sid_cases.hpp` S1 | `conflict_keeps_old_wait` |
| `S1 the declaration carries a new Stream ID` | S1 | `conflict_reuses_old_id`, `used_not_marked_by_probe` |
| `S1 src_stream_id_o follows the move` | S1 | `output_ignores_move` |
| `S1 PROBE_TX before the grant` / `after the grant`, `S1 GET_TX_STATE after the grant` | S1 | `probe_answers_configured_id`, `tx_state_answers_configured_id` |
| `S1 the move survives a disable` | S1 | `move_lost_on_disable` |
| `S2 a provisioned collision with the first candidate is skipped` | S2 | `move_takes_colliding_id` (the search refuses nothing) |
| `S3 a move never takes another source's configured ID after that source moved off it` | S3 | `move_ignores_configured_ids` |
| `S4 an equal unique ID under another MAC is not a collision` | S4 | `move_compares_unique_id_only` |
| `S5 no move repeats a unique ID inside one lap` | S5 | `move_cursor_stuck` |
| `S5 after the cursor wraps a move skips every configured ID and another source's current ID` | S5 | `move_ignores_moved_ids` |
| `S6 a conflict after a listener withdrawal moves the ID`, `S6 a conflict after a freshness lapse moves the ID` | S6 | `move_only_when_declaring`, `used_not_marked_by_event`, `used_not_marked_by_probe` |
| `S6 an ID not declared since its move is not moved again` | S6 | `used_kept_after_move` |
| `R6 after backoff src0 status/tuple` | `retry_cases.hpp` R6 | `move_only_when_declaring` |
| `F2 leaveall2 src0`, `R6 full two-LeaveAll backoff armed` | F, R6 | `pcp_skips_the_gap` (the PCP path re-declares without the gap) |
| `MP8: conflict to new declaration under 2 s` | `tb/pp_top` MP8 | `conflict_keeps_old_wait` |
| `MP8: the Talker Advertise carries the new Stream ID and address` | MP8 | `conflict_reuses_old_id` |
| `MP8: src_stream_id_o names the new Stream ID` | MP8 | `output_ignores_move` |
| `MP8a: while the walk probes, PROBE_TX answers TALKER_DEST_MAC_FAILED` | MP8a | `tb/maap`'s `compare-mac-forward` (no conflict at all) |

Every arm, its failing-check count and its named checks: `tb/pp_top/README.md` section MP (17
rows, 20 arm runs). At head all 20 are KILLED with exactly the recorded counts
(`receipts/compare/acmp-arms-head-bba84945.tsv`; the full `results.json` is listed in
`EXTERNAL-RECORDS.csv`).

Measured times: S1 1,700 ms (the bench allocator's walk; the talker adds nothing); MP8
1,737 ms through the in-scope Annex B engine (four probes, then one `T-ACMP-DA-RETRY` round).

## 5. Gates (processor; every `.rc` is the command's own exit status, written by a recording wrapper, never through a pipe)

Local tools: Verilator 5.052 (CI pins 5.050), Yosys 0.66, sv2v 0.0.13, WaveDrom 2.0.3.post3 in a
venv outside the tree, Mermaid CLI 11.16.0. The head suites and every campaign but the base
retry run went through a PATH wrapper that turns Verilator's `-j 0` into a fixed `-j N` (§7,
note 8); the base suites ran without it. Results do not depend on it.

| Gate | Base `ed211803` | Head | Base vs head |
|---|---|---|---|
| `./scripts/lint_hdl.sh` | rc 0 | rc 0 at `bba84945` and at `a8aa626e` (41 modules) | identical |
| `make check` | rc 0 | rc 0 at `bba84945` and at `a8aa626e` | only `ids: 664 files` → `665` (the new `sid_cases.hpp`) |
| `./scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,399 checks, 0 failing | rc 0, 1,030,494 checks, 0 failing (`bba84945`) | only `acmp_talker` 1,376 → 1,463 and `pp_top` 10,741 → 10,749 move (`receipts/compare/suites.diff`) |
| `scripts/check-req-tags.py --suites … --evidence …` | rc 0, 231 tags in 19 files, 231 evidence lines, 14 suites | rc 0, 237 tags in 20 files, 237 evidence lines, 14 suites | the six new tags in `sid_cases.hpp`; the rest line offsets in `tb/acmp_talker/sim_main.cpp` (`receipts/compare/req-tags.diff`) |
| `./syn/yosys/run.sh` | — | rc 0, 42 tops, at `bba84945` and at `a8aa626e` (at `1e0c83df` it failed: commit 3) | — |
| `tb/elab_guards/guards.py --frontend yosys --jobs 4` | — | rc 0, 93 of 93 | — |

| Campaign (builds a changed file) | Base | Head | Notes |
|---|---|---|---|
| `tb/pp_top/acmp_mutants.py --jobs 4` | rc 0, 65 of 65 KILLED, goldens PASS | rc 0, 85 of 85 KILLED, goldens PASS (`bba84945`) | the 72 shared records keep their verdicts; 69 fail identical check sets; `armq_read_tail` also fails the new MP8 checks, and `disconnect_changes_gate`/`disconnect_not_accepted` fail collateral checks of the rewritten section E; every named check still fails |
| `tb/acmp_talker/retry_mutants.py --jobs 4` | rc 0, 62 killed, 7 equivalent, 1 performance control; coverage 59/59 | rc 0, same; 1,463 checks; coverage 59/59 | counts re-measured into the README table (exact match at head) |
| `tb/maap/mutants.py --jobs 4` | — | rc 0, 29 of 29 KILLED, 3 controls PASS | pp_top arms: 4 and 11 FAIL of 42 (README updated) |
| `tb/pp_top/aecp_mutants.py --jobs 4` | — | rc 0, 67 of 67 killed (`a8aa626e`) | — |
| `tb/pp_top/aecp_dispatch_mutants.py --jobs 4` | — | rc 0, 74 of 74 (controls and arms) | — |
| `tb/pp_top/ctr_mutants.py --jobs 4` | — | rc 0, 18 of 18 | — |
| `tb/pp_top/gsi_mutants.py --jobs 4` | — | rc 0, 23 detected, golden and restored PASS | — |
| `tb/pp_top/name_wr_mutant.py` | — | rc 0, killed, golden and restored PASS | — |
| `tb/pp_top/notify_mutants.py --jobs 4` | — | rc 0, 137 of 137 KILLED, goldens PASS | — |
| `tb/pp_top/d3_mutants.py --jobs 4` | — | rc 0, 110 of 110 KILLED, goldens PASS | — |
| `tb/elab_guards/mutants.py --jobs 6` | — | rc 0, 160 of 160 killed | — |
| `tb/name_state/mutants.py --jobs 2` | — | rc 0, 16 KILLED, golden PASS | — |

Not run, because they build no changed file: `tb/srp_top`, `tb/adp_engine` and
`tb/srp_admission` mutants, the `tb/aecp_cmds` standing controls (the engine-only build) and
the `tb/nvm_port` figures. Their suites ran in `run_suites.sh`.

## 6. Consumer gate (scratch parent)

Scratch parent `pp202-parent`: a local clone of the trusted milan-fpga dev lane at
`e76a755afc0536453161e3cd33f6f4d2dcd7641f`, every submodule from local clones, push URL set to an
invalid value, never pushed. Local commits on branch `scratch-pp202-a676b`
(`receipts/consumer/PARENT-STATE.txt`):

- `667ee64d` gitlink at `bba84945`; `7db18be5` the wiring (`parent-src-stream-id-wiring.patch`,
  sha256 `770210604495083d1661f7157111c4f4c2250f80dd610f1a0975d9f5b8585f89`, 7,347 bytes, in this
  directory); `d8b61dcd` the ROM digest rows `ooc.sh --record-rom-digests` wrote for `bba84945`.
- `b3874dcc` gitlink at the final head `a8aa626e` (documents only past `bba84945`); `f46707b3` its
  ROM digest rows. Worktree clean.

Base control `pp202-parent-ctl`: pristine dev `e76a755a` with the processor at `ed211803`, the same
way (no local commit).

**The wiring (decision item 7).** `KL_pp_shadow` passes `src_stream_id_o` out;
`milan_datapath` names it `pp_cd_src_stream_id_w`; GET_STREAM_INFO output selector 2
(`gsi_osid_w`) reads it; the AAF packetizer gains `stream_id_i[N_TALKERS_P*64-1:0]` (default
`'0`, so its other benches are untouched) and stamps it, unless TCTX names a non-zero uid for
t>0 (that software override keeps its precedence, which `tests/` pins); the CRF Media Clock
Output's `sid_i` reads the CRF source's slot when the shape has one. `pp_src_sid_w` stays the
reset value handed to `cfg_stream_id_i`.

| Parent consumer gate | Base (pin `ed211803`) | Head (pin `bba84945` + wiring) | Base vs head |
|---|---|---|---|
| `make -j8 -C tb/verilator/pp_shadow VERILATOR_JOBS=2` | rc 0, 2,187 checks, 0 failures | rc 0, 2,187, 0 (and rc 0 again at pin `a8aa626e`) | equal counts; line-order differences only (four binaries interleave) |
| `make -j8 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2` (every leg) | rc 0, 13,583 checks, 0 failures; 12,014 `[ok]`, 1,199 `[PASS]`, 0 `[FAIL]` | rc 0, the same | sorted check lines identical (13,220 lines, sha256 `3e0cff72…` at both) |
| `make -j8 -C tb/verilator/maap VERILATOR_JOBS=2` | rc 0, 251 checks, 0 failures | rc 0, 251, 0 | identical but for interleaving |
| `make -j8 -C tb/verilator/capture_coherence VERILATOR_JOBS=2` | rc 0, 21,721 checks, 0 failures | rc 0, 21,721, 0 | the planted build-break line moves `milan_datapath.sv:9681` → `:9703` (the wiring's 22 lines) |
| `make -j8 -C tb/verilator/milan_dp_render VERILATOR_JOBS=2` | rc 0, 347 checks, 0 failures | rc 0, 347, 0 | check lines identical |
| `scripts/suite_tally.py --verdict <log>` per suite | rc 0 each | rc 0 each | — |
| `./syn/yosys/ooc.sh --record-rom-digests` (the ROM-digest record check) | — | rc 0: `ltn_rom.hex` `23cc67ee…`, `ucode.hex` `1f78804e…` for `bba84945` and for `a8aa626e` | equal to the ledger's `ed211803` rows |
| `./syn/yosys/ooc.sh KL_pp_shadow` (validates the ROM images against the ledger, then area) | rc 0: LUT 58,185, LUTRAM 4,236, FF 26,948, RAMB36 15, RAMB18 4, DSP 10, CARRY4 2,394 | rc 0: LUT 59,535, FF 27,133, CARRY4 2,407, the rest equal (the same at pin `a8aa626e`) | +1,350 LUT (+2.3 %), +185 FF, +13 CARRY4 |
| `lint_rtl.py --check --self-test --jobs 4`, `check_port_contracts.py`, `check_wire_accountability.py`, `check_sv_idiom.py`, `check_rtl_source_lists.py`, `behave` (`tests/`: 406 scenarios) | rc 0 each | rc 0 each, at both pins | — |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | rc 0 | rc 0, at both pins | — |
| `flock <lock> python3 scripts/xvlog_gate.py --check` (the vendor parser over the patched RTL) | rc 0 | rc 0, at both pins | — |

Tallies: `scripts/suite_tally.py` over the five suite logs, 38,089 checks, 0 in-suite failures at
both (`receipts/compare/tally-*.txt`). FF +185 is the new state: 19 bits per source
(booked, declared, moved-flag, 16-bit unique ID) × 8 + the 16-bit cursor + the 16-bit candidate
make 184. No parent suite drives a MAAP conflict on a declaring source, so the agreement of the wire,
GET_STREAM_INFO and PROBE_TX **after** a conflict rests on the wiring (both stamps and selector 2
read the one published level) and on the processor's MP8; before a conflict the parent's own
checks (`AAF stream_id == {station MAC, uid 0}`, the GSI legs) pass unchanged.

## 7. Notes for the reviewer

1. **The booking rule goes one step past the letter of decision item 2.** Item 2 speaks of a
   conflict "on a declaring source"; item 4 says any path that re-declares the old ID keeps the
   gap. A source that declared, withdrew on a lapsed gate (`DA_OK`) and then took a conflict
   used to re-declare its old ID with the new DA at the next probe, with no gap at all (the
   pre-existing "conflict while DA_OK: re-alloc without backoff" arc). So any conflict books
   the move once the current ID has been declared since reset or its last move: also inside
   a PCP backoff and while disabled. A never-declared ID is still not moved (E7, S1, S6). The
   arms `move_only_when_declaring`, `used_not_marked_by_event`, `used_not_marked_by_probe` and
   `used_kept_after_move` hold it. If the owner wants the narrower reading, it is the one line
   `ev_sid_owe_w = sid_used_r[ev_src_r]` → `(rec_w.gstate == GS_DECLARING_C)`.
2. **Up to one `T-ACMP-DA-RETRY` round between DEFEND and the grant.** Both allocators the
   processor meets (the in-scope engine and the parent's shim) refuse `ALLOC_DA` while they
   probe, so the grant lands on the first 100 ms round after DEFEND. In that window MAAP holds
   the range and `PROBE_TX` still answers `TALKER_DEST_MAC_FAILED`, which is decision item 3's
   reading ("while the source has no valid address"). Conflict to declaration is the walk
   (≤ 3 × 600 ms, Table B.8) plus that round: 1,737 ms measured in MP8.
3. **The gate predicate at the moving grant is unchanged** (a fresh probe or a registered
   Listener). The SRP talker FSM restarts its Listener registrar at every gate open
   (`KL_srp_talker_fsm.sv`, "gate re-open arms a fresh tracker"), so a registration of the
   withdrawn ID can open the gate once but never counts for the new ID afterwards; without a
   fresh probe the new declaration is withdrawn again at the next `LISTENER_REG_CHANGE`, exactly
   as today's backoff exit behaves.
4. **The moved ID lasts until reset.** `cfg_stream_id_i` is quasi-static; a slot reprovisioned
   after a move keeps the moved unique ID under its new upper 48 bits. Clearing the move on a
   disable would re-declare a conflict-withdrawn ID with another DA, so it is kept
   (`move_lost_on_disable`).
5. **Pre-existing, out of scope:** a disable/re-enable that gets a *different* DA without any
   conflict would re-declare the same ID with it. Both block allocators return base + s, and the
   block moves only through a conflict (which books the move), so this needs an allocator the
   processor does not meet today. Not changed.
6. **Parent.** No parent suite drives a MAAP conflict on a declaring source (milan_dp runs
   `KL_maap` at the silicon rate, where a claim does not finish in simulation time; its base leg
   says so), so a parent check of the wire/GSI/PROBE_TX agreement after a conflict would be new
   work for the pin-adoption PR. The patch keeps the packetizer's TCTX uid override precedence,
   so a software-named uid still disagrees with the processor as it does today.
7. **Area.** +1,350 LUT (+2.3 %) and +185 FF on `KL_pp_shadow` out of context: 16 × 16-bit and
   8 × 48-bit comparators, the 8:1 selects of the moving source's slot, and the per-source
   16-bit replacement muxes. Earlier rounds measured the flattened mapping varying by a few
   hundred LUTs on single-constant changes.
8. **Runs and memory.** Verilator's `-j 0` sizes builds to the host's 128 threads rather than
   this unit's 16 CPUs, and a `make -j8` of `capture_coherence` runs its `run`, `dp` and
   `mutants` (one copy per CPU) at once. Two such overlaps took the unit's anonymous memory to
   16.5 GB and 21.8 GB for about two minutes each (the first with head `run_suites` and the
   head `capture_coherence`, the second with the base `pp_shadow` and `capture_coherence`),
   above the 10 GB target. That broke the memory rule, not a result: nothing was killed, the
   parent runs completed rc 0 and stand as records, and the processor `run_suites` was rerun
   whole anyway. From then on every build went through a wrapper capping Verilator's `-j`
   (4, then 2 to 3) and campaigns ran at `--jobs 4` or lower. A pause-based memory guard was tried once: the background runner treats a
   stopped process as finished and killed three chains, which were rerun whole
   (`receipts/VOID.txt`).
9. Ports, parameters and register maps: only `src_stream_id_o` added.

## 8. Commands (plain shell)

```
./scripts/lint_hdl.sh
make check
./scripts/run_suites.sh
python3 scripts/check-req-tags.py --suites SUITES.LOG --evidence REQ_TAGS.TXT
./syn/yosys/run.sh
python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
make -C tb/acmp_talker
make -C tb/pp_top maap-internal
python3 tb/pp_top/acmp_mutants.py --output OUT --jobs 4
python3 tb/pp_top/acmp_mutants.py --output OUT --jobs 4 --only conflict_keeps_old_wait conflict_reuses_old_id output_ignores_move
python3 tb/acmp_talker/retry_mutants.py --logs OUT --jobs 4
python3 tb/maap/mutants.py --output OUT --jobs 4
python3 tb/pp_top/aecp_mutants.py --output OUT --jobs 4
python3 tb/pp_top/aecp_dispatch_mutants.py --output OUT --verilator verilator --jobs 4
python3 tb/pp_top/ctr_mutants.py --output OUT --jobs 4
python3 tb/pp_top/gsi_mutants.py --output OUT --verilator verilator --jobs 4
python3 tb/pp_top/name_wr_mutant.py --output OUT
python3 tb/pp_top/notify_mutants.py --output OUT --verilator verilator --jobs 4
python3 tb/pp_top/d3_mutants.py --output OUT --verilator verilator --jobs 4
python3 -B tb/elab_guards/mutants.py --verilator verilator --output OUT --jobs 6
python3 tb/name_state/mutants.py --verilator verilator --jobs 2 --output OUT
```

In the scratch parent:

```
git apply parent-src-stream-id-wiring.patch
make -j8 -C tb/verilator/pp_shadow VERILATOR_JOBS=2
make -j8 -C tb/verilator/milan_dp SIM_JOBS=2 VERILATOR_JOBS=2
make -j8 -C tb/verilator/maap VERILATOR_JOBS=2
make -j8 -C tb/verilator/capture_coherence VERILATOR_JOBS=2
make -j8 -C tb/verilator/milan_dp_render VERILATOR_JOBS=2
python3 scripts/suite_tally.py --verdict SUITE.LOG
./syn/yosys/ooc.sh --record-rom-digests
./syn/yosys/ooc.sh KL_pp_shadow
```

## 9. Receipts

`receipts/INDEX.md` lists every file present with its size and sha256; it is generated from the
directory. Host paths in copied logs are normalised to `<processor-head>`, `<parent-head>`,
`<work>` and similar. Files over 190 KB are not copied: `EXTERNAL-RECORDS.csv` gives their
sha256 and size (the full suite logs of milan_dp, capture_coherence, pp_shadow, behave, and the
two ACMP `results.json`, summarised in `receipts/compare/acmp-arms-*.tsv`). The parent wiring
patch is `parent-src-stream-id-wiring.patch` in this directory (and a copy under
`receipts/consumer/`).

## 10. Public trail

- TAKEN: issue #202 issuecomment-6408995638.
- REVIEW READY: issue #202 issuecomment-6414252955, head `a8aa626e1cba30625ac764c70e1fb8fb02c69c40`.
- No push, no PR, no merge, no rebase, no edit or deletion of any comment.
