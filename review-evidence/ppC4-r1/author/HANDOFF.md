# [A450] Lane C4 (ACMP) handoff

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
Branch: `c4-acmp-coverage` (local, not pushed), base `main` b2db3a970cedbbff2f8ba813acb96122c442bc58
Head: a9ce0fa2e0b8b120703c6e541668d4281cec286e
Issues: #45 (GAP-15), #47 (GAP-02), #48 (GAP-02)
Assignment: #45 comment 5891906554. TAKEN posted: #45 comment 5891920801.
PR body: PR-BODY.md in this directory (for a new PR; no PR was created).
Scratch (outside the tree and this directory): $VALIDATION_STORAGE/ppC4-a450

## Status

- [x] Item 1: #47 (REQ-ACMP-012) — d87b3d5
- [x] Item 2: #45 (REQ-ACMP-001) — 2a3e608
- [x] Item 3: #48 (REQ-ACMP-016) — af6a5f1 (AS6 tightened in a9ce0fa)
- [x] Item 4: parent-visible list (PR-BODY.md section 4)
- [x] Gates: processor suites, entry points, mutants, all rc 0 at a9ce0fa
- [x] Gates: parent consumer set at 79c36963, gitlink at a9ce0fa; failures
      identical at the lane base, all pass at the parent pin (attribution below)
- No STOP condition met: no RTL defect found, no port, parameter, register or
  RTL behaviour change; hdl/ and docs/ untouched.

## Commits (one-line subjects, no body, no trailers)

| Commit | Item |
|---|---|
| d87b3d5 | 1. #47 inert message types, guard per term, pp_top AI, mutation driver |
| 2a3e608 | 2. #45 96-B ACMPDU: rx_validator F29, pp_top AL, cdl mutant |
| af6a5f1 | 3. #48 settle path: pp_top AS, wrap bound view, st_ls_r / view / matcher mutants |
| 20e24d4 | records: mutation tables remeasured at the lane head |
| a7ccd9e | parent C++ idiom gate (Rule 11): B13 type list split across lines |
| a9ce0fa | item 3: AS6's quiet window counts every ACMP frame, not only the next probe |

Files: tb/acmp_listener/{sim_main.cpp,README.md}, tb/rx_validator/{sim_main.cpp,README.md},
tb/pp_top/{sim_main.cpp,README.md,pp_top_wrap.sv}, tb/pp_top/acmp_mutants.py (new, 755).
`git diff b2db3a97..a9ce0fa -- hdl docs` is empty.

## Item 1: #47 (REQ-ACMP-012, Milan §5.5.3.1) — d87b3d5

No RTL defect found; no RTL change.

- `tb/acmp_listener` B13: message types 3, 5, 7, 9, 11, 13 (IEEE 1722.1-2021
  Table 8-2 responses other than PROBE_TX_RESPONSE) and 14, 15 (reserved),
  own listener EID, valid listener unique_id, shaped as the perfect answer to
  the outstanding probe; in PRB_W_RESP (SUCCESS) and PRB_W_RESP2
  (TALKER_NO_BANDWIDTH). Inert on every face: no frame, no record write, no
  timer op, no strobe, no notify, record unchanged, one RX free of its slot.
- `tb/acmp_listener` B14: guard per term (Milan §5.5.3.5.18 step 1; §5.5.3.5.25
  applies it in PRB_W_RESP2, "same treatment"):
  wrong controller EID, talker EID, talker unique_id each ignored in both
  probing states; the unaltered response then settles (positive control).
- `tb/pp_top` section AC (fresh model, `--acmp-only`, sink 1), AI1-AI3: msg 7
  and msg 14 through the real steer: no ACMP frame, no front-end drop, 4 of 4
  RX slots free, no scoreboard hold; the exact duplicate probe at T-ACMP-CMD
  proves the sink stayed in PRB_W_RESP.
- Failing arms / mutants: `msg_ok_forced` (txn_msg_ok_w forced 1):
  acmp_listener 93 of 2988 (all 16 B13 arms), pp_top AI3 (1 of 42);
  `guard_ctlr_dropped` 50, `guard_talker_eid_dropped` 40,
  `guard_talker_uid_dropped` 30 of 2984 (B14 arms). All KILLED.
- Records: `tb/acmp_listener/README.md`, `tb/pp_top/README.md` section AC.

## Item 2: #45 (REQ-ACMP-001, Milan §5.5.2.2; F09.4 row; 03 V3) — 2a3e608

No RTL defect found; no RTL change.

- `tb/rx_validator` F29: 96-B IEEE 1722.1-2021 ACMPDU (cdl 84, §8.2.1.6,
  Figure 8-1), IP tail pattern-filled, as BIND_RX and PROBE_TX: committed, no
  counter (rx_length) moves, slot holds 96 bytes, header beat field-exact and
  equal to the truncated form's but for cdl.
- `tb/pp_top` AL1-AL4: 96-B UNBIND_RX, BIND_RX (same response as AI1's 56-B
  BIND_RX byte for byte; PROBE_TX #2 regenerated from the long command's
  fields) and PROBE_TX to our talker (same DEST_MAC_FAILED answer as the 56-B
  form); no front-end drop, no slot leak.
- Mutant `cdl_not_44_rejected` (validator accepts ACMP only at cdl 44):
  rx_validator 27 of 495 (F29 both forms, F4 collateral), pp_top 19 of 42
  (AL1-AL4, then AS needs the long BIND_RX's binding). KILLED. Recorded in
  `tb/rx_validator/README.md` (M5) and `tb/pp_top/README.md`.

## Item 3: #48 (REQ-ACMP-016, Milan §5.5.3.5.18/.36/.42/.45/.48, §5.3.8.5/.9) — af6a5f1, a9ce0fa

No RTL defect found; no RTL change. The wrap (`tb/pp_top/pp_top_wrap.sv`, a
test file) now connects the top's existing `acmp_bound_eid/sid/dmac/vlan_o`.

- `tb/pp_top` AS1-AS6 on sink 1 (fresh model, 18.9 s simulated):
  AS1 unanswered probe #2 -> duplicate -> T-ACMP-RETRY re-probes nothing;
  GET_RX_STATE probing form (Table 5.37) byte-exact; talker ENTITY_AVAILABLE
  -> PROBE_TX #3 byte-exact -> PROBE_TX_RESPONSE SUCCESS.
  AS2 bound view [1] = response's {sid, DA, VID} + talker EID, other sinks
  clear; GET_RX_STATE settled (Table 5.38) byte-exact; nothing declared.
  AS3 near misses (DA, VLAN, stream_id): no Listener vector on the wire, no
  class-D registration, no TK_ATTR_REGISTERED{1}.
  AS4 matching Advertise: Listener Ready New byte-exact, class-D READY +
  ADVERTISE, exactly one TK_ATTR_REGISTERED{1}, GET_RX_STATE Table 5.39.
  AS5 SETTLED_RSV_OK held 11.5 s after the settle (no re-probe, no Lv,
  declaration and view held) with the bench re-joining every second.
  AS6 UNBIND_RX: response byte-exact, Listener Lv Ready byte-exact (802.1Q
  §35.2.2.7.2), bound view cleared, no declaration/match, GET_RX_STATE
  unbound byte-exact, no ACMP frame in the next 1.5 s (a9ce0fa: was "no probe
  with the next sequence_id"), no slot/scoreboard leak.
- Mutants (all KILLED, failing checks of 42): st_ls_settle_as_withdraw 7,
  st_ls_teardown_as_declare 1, st_ls_sid_da_swapped 7, st_ls_state_none 7,
  st_ls_vid_dropped 7, st_ls_index_zero 6, st_ls_teardown_lost 2,
  bound_view_not_latched 2, bound_dmac_from_sid 2, bound_view_not_cleared 1,
  matcher_da_ignored 5, matcher_vid_ignored 5.
- Harness fixes during development (tests, before commit): the trace helper
  first keyed TK_ATTR_REGISTERED on router source 2; `pp_evr_map` makes source
  k the event for sink k, so AS3 would have passed vacuously (AS4's "exactly
  one" check caught it).

Noted from the top's source, not graded, not changed (parent-visible if ever
changed): `acmp_bound_sid/dmac/vlan_o` are latched at A15 and cleared only with
the binding (A9), as the port comment says; after an A8 teardown without an
unbind (T-ACMP-NOTK, EVT_TK_UNREGISTERED) they keep the last settled stream
until the next settle. Listed under "what remains".

## Parent-visible list (as in PR-BODY.md section 4)

- No interface or behaviour change: nothing under hdl/ or docs/ changes.
- One parent registry entry: `protocol-processor/tb/pp_top/acmp_mutants.py` in
  `scripts/measure_test_evidence.py` DUT_READER_DISPOSITIONS (text below);
  `d3_mutants.py` (PR #132) needs one too.
- Processor suite totals: acmp_listener 2544 -> 2988, rx_validator 437 -> 495,
  pp_top 7888 -> 7930; sweep 1,016,816. No parent file at 79c36963 quotes them.
- Parent doc that can cite the grading: docs/reference/MILAN_COMPLIANCE_MATRIX.md
  section 1.6 row "5.5.2 / 5.5.3".

## Suite table (processor, at a9ce0fa; Verilator 5.052, taskset 0-7, make -j8)

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,016,816 checks, 0 failing, 7m31s (acmp_listener 2988, rx_validator 495, pp_top 7930) |
| `./scripts/lint_hdl.sh` | 0 | 41 LINT OK |
| `make check` | 0 | lint 41 mermaid + 18 wavedrom, links 976, matrix 115 REQ / 17 GAP, modmatrix 94 rows 0 untested, params 26 |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | 19 of 19 KILLED, 3 goldens PASS (counts identical to the a7ccd9e run) |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected, golden + restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | decode killed, golden + restored PASS |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` | 0 | 83 of 83 KILLED, goldens acmp_nvm / pp_top / rx_validator PASS |
| `git diff --check b2db3a97..a9ce0fa` | 0 | |

The same set also ran at a7ccd9e (all rc 0, same results) and run_suites /
lint / make check / gen_matrix at af6a5f1. Every suite was also run
individually once (cold build + run), all rc 0. Baseline at b2db3a97:
`tb/pp_top` rc 0, 7888 checks.

Not re-run (inputs untouched by this lane: hdl/ and their own tb dirs):
`make -C tb/srp_top mutants`, `make -C tb/nvm_port figures`, `./syn/yosys/run.sh`,
`tb/srp_admission/mutants.py`, `tb/acmp_talker/retry_mutants.py`.

Commands longer than the 10-minute tool cap (the parent builder test, the
parent long batches, the D3 driver; twice the tool backgrounded a command
itself) were run detached in their own session and waited on with foreground
`tail --pid` calls until they exited; nothing is left running. One run was
lost when its scratch parent was deleted and rebuilt; it was superseded by
the runs below.

## Mutant table (acmp_mutants.py at a9ce0fa; failing checks)

| Mutant | Suite | Named checks | Failing |
|---|---|---|---|
| msg_ok_forced | acmp_listener | B13 msg 7/14 PWR, 3/15 PW2 | 93 of 2988 |
| msg_ok_forced | pp_top AC | AI3 | 1 of 42 |
| guard_ctlr_dropped | acmp_listener | B14 wrong controller_entity_id | 50 of 2984 |
| guard_talker_eid_dropped | acmp_listener | B14 wrong talker_entity_id | 40 of 2984 |
| guard_talker_uid_dropped | acmp_listener | B14 wrong talker_unique_id | 30 of 2984 |
| cdl_not_44_rejected | rx_validator | F29 both forms | 27 of 495 |
| cdl_not_44_rejected | pp_top AC | AL1-AL4 | 19 of 42 |
| st_ls_settle_as_withdraw | pp_top AC | AS4 x2, AS5 | 7 of 42 |
| st_ls_teardown_as_declare | pp_top AC | AS6 Lv | 1 of 42 |
| st_ls_sid_da_swapped | pp_top AC | AS4 x2, AS5 | 7 of 42 |
| st_ls_state_none | pp_top AC | AS4 x2, AS5 | 7 of 42 |
| st_ls_vid_dropped | pp_top AC | AS4 x2, AS5 | 7 of 42 |
| st_ls_index_zero | pp_top AC | AS4 class-D, AS4 traced, AS5 | 6 of 42 |
| st_ls_teardown_lost | pp_top AC | AS6 Lv, AS6 decl/match | 2 of 42 |
| bound_view_not_latched | pp_top AC | AS2 view, AS5 view | 2 of 42 |
| bound_dmac_from_sid | pp_top AC | AS2 view | 2 of 42 |
| bound_view_not_cleared | pp_top AC | AS6 view | 1 of 42 |
| matcher_da_ignored | pp_top AC | AS3 x3 | 5 of 42 |
| matcher_vid_ignored | pp_top AC | AS3 x3 | 5 of 42 |

## Parent consumer gate table

Scratch parents built by a script (not in the tree) from `git archive` of the
trusted checkout at 79c36963 (regular files identical to its index; checked
with `git ls-files -s`), verilog-axis 48ff7a7 and gptp-processor 5dce647 cloned
from their public URLs at the pins (the trusted checkout has no submodule
objects), external recorded as a gitlink only, protocol-processor cloned from
the lane and staged as the gitlink. Columns: head a9ce0fa, base b2db3a97, and
the parent's own pin c951a9ff for the commands failing at base. (The full set
also ran with the gitlink at a7ccd9e: same verdicts as a9ce0fa.)

| # | Command | head | base | pin |
|---|---|---:|---:|---:|
| 1 | python3 scripts/check_cpp_idiom.py | 0 | 0 | |
| 2 | python3 scripts/check_py_idiom.py | 0 | 0 | |
| 3 | python3 scripts/xvlog_gate.py --check | 0 | 0 | |
| 4 | python3 scripts/check_rtl_source_lists.py | 0 | 0 | |
| 5 | python3 scripts/pp_srcs.py --check --selftest | 0 | 0 | |
| 6 | python3 sw/builder/test_builder.py | 0 (942 s) | 0 (955 s) | |
| 7 | make -C tb/verilator/pp_shadow -j8 | 2 | 2 | 0 |
| 8 | python3 scripts/check_port_contracts.py | 0 | 0 | |
| 9 | python3 scripts/measure_naming.py --check | 0 | 0 | |
| 10 | python3 scripts/measure_test_evidence.py --check | 1 | 1 | 0 |
| 11 | python3 scripts/docs_check.py | 0 | 0 | |
| 12 | make -C tb/verilator/nvm_cosim lint | 0 | 0 | 0 |
| 13 | make -C tb/verilator/nvm_cosim quick | 2 | 2 | 0 |
| 14 | make -C tb/verilator/milan_dp -j8 | 2 | 2 | 0 (1498 s) |
| 15 | make -C tb/verilator/milan_dp_render -j8 | 2 | 2 | 0 |
| 16 | python3 scripts/lint_rtl.py --check | 1 | 1 | 0 |

- check_cpp_idiom failed once at 20e24d4 (Rule 11: one-line `static constexpr
  uint8_t kTypes[] = {...};` read as a multi-declarator); passes since a7ccd9e.
- Identical failures head vs base: sorted FAIL/%Error/%Warning/RESULT/checks
  lines hash equal for pp_shadow, nvm lint, nvm quick (308/315), milan_dp,
  milan_dp_render; lint_rtl output byte-identical (hdl/milan 3 > ratchet 2:
  PINMISSING restore_closed_o on KL_pp_shadow's processor instance).
- pp_shadow: PINMISSING restore_cause_o, d3_unflushed_o, restore_closed_o,
  restore_rb_o, rs_cause_o (processor PR #132 top outputs) fatal.
- nvm_cosim: its harness leaves #132's rs_agg_i and wr_chg_o unconnected
  (PINMISSING in its lint output); quick fails 7 of 315 at base and head.
- measure_test_evidence: base 1 unexplained (d3_mutants.py, PR #132); head 2
  (+ acmp_mutants.py, this lane). Scratch-verified parent edit, applied and
  reverted at a7ccd9e and at a9ce0fa (1225-byte patch in the scratch area,
  sha256 654d1ca7bb40126d673b12ed8575aaa7803650f67186d3d155709d7fa82edb35):

```
+    "protocol-processor/tb/pp_top/acmp_mutants.py":
+        "mutation campaign; it plants one ACMP listener, validator, top SRP-service or SRP "
+        "matcher defect from its own table into an isolated copy and requires the named "
+        "checks to fail; no expected value is read from RTL",
+    "protocol-processor/tb/pp_top/d3_mutants.py":
+        "mutation campaign; it plants one saved-state control from its own table into an "
+        "isolated copy and requires the named checks to fail; no expected value is read "
+        "from RTL",
```
  (inserted before the gsi_mutants.py entry of DUT_READER_DISPOSITIONS) ->
  `TEST-EVIDENCE RATCHET: PASS (... 0 <= 0 unexplained DUT-source reader(s) ...)`, rc 0.

## What remains (as in PR-BODY.md)

- No hardware used; no RTL change, so bench evidence for #76 is unaffected.
- docs/00 F00.2 still names #45 as GAP-15's open residue (left untouched).
- The bound-view hold across an A8 teardown without an unbind (above).
- The parent consumer set cannot be green at 79c36963 with any processor head
  past c951a9ff until PRs #132 and #133 are adopted.

## Posted

"[A450] REVIEW READY, head a9ce0fa2e0b8b120703c6e541668d4281cec286e" on #45,
comment 5898926588. The branch is local only (no push, no PR by instruction);
PR-BODY.md is ready for whoever opens the PR.
