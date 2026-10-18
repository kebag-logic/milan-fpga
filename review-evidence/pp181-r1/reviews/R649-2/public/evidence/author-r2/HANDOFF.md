# [A635] #181 handoff — cut the notify-queue to event-router path

**Round 2 (latest): REVIEW READY at head `c5afc0a42f200af01dd83e67b579dc3badc42601`; see "Round 2" at the end. The round-1 sections below describe head `16c89c53` as they did then.**

Status: DONE, REVIEW READY at head `16c89c53a0d7de322d40310e45b972a6057b9593`, with one acceptance
item NOT met. **Item 1 (the depth roughly halves) is not met.** The occupancy register removes every
path from `cmdq_count_r` to `sel_r`, and the router's scan comes off the acknowledge. The longest half,
though, keeps 22 levels in OOC (the cone was 22 at 1x1 and 32 at 8x8) and 24 routed (the cone was 30).
Most of that depth sits in `u_aecp`, `u_dispatch`, `u_scoreboard` and `u_listener`, between the two
blocks, and this lane may not touch them. The PR body therefore does not say "Closes #181". Items 2 to 5
are met. With #760, route-1x1 WNS moves from +0.016 ns (base, below the gate's +0.03 floor, rc 1) to
+0.144 ns (head, rc 0), and the worst path leaves the cone.

- Processor branch: `181-notify-router-cut`, base `22c139a4323bc96c779d13e3f6774480c5fb9b75`
- Head: `16c89c53a0d7de322d40310e45b972a6057b9593`, 4 commits: RTL `dcb71893`, docs `7979866f`,
  OOC record `07447acb`, the record of the two halves `16c89c53`
- `git diff dcb71893 16c89c53 -- hdl tb syn/ooc/protocol_processor_ooc.tcl syn/yosys` is empty. Every
  RTL measurement taken at `dcb71893`, `7979866f` or `07447acb` (campaigns, routes, OOC, proofs) is
  therefore of the head's RTL. The processor gates and the parent consumer gates ran again at `16c89c53`.
- Merges cleanly into current processor main `77cf6fb4` (`git merge-tree --write-tree`, rc 0). Main
  does not touch either changed RTL file. Not rebased, not pushed, no PR opened.
- Assignment: processor issue #181, comment 6241709741 (A10)
- TAKEN posted: comment 6241718692, 2026-10-17T21:47:17Z; REVIEW READY posted: comment 6249043044 (head `16c89c53`)

## The cone (measured before any edit)

Base + #760 route-1x1 (this lane's scratch parent, gitlink at base `22c139a4`, #760 applied):
`u_notify/cmdq_count_r_reg[0]` -> `u_event_router/sel_r_reg[0]/D`, 30 levels, slack +0.016 ns, the
design's worst setup path. #760's own lane's routed checkpoint, read only, shows the same path at the
same slack. It runs through:

- `u_notify`: the count compare, merged with the emission pick into `amap_busy_o`;
- `u_aecp`: the admission ready;
- `u_dispatch` / `u_scoreboard`: the ACMP-versus-AECP pick;
- `u_listener`: its ready;
- `u_event_router`: ack -> deliver -> scan base `rr_next(sel_r)` and pending-minus-delivered ->
  priority scan -> `sel_r`.

## Changes (file:line, at head)

- `hdl/aecp/KL_aecp_notify.sv:429` new flop `cmdq_nempty_r`, the registered occupancy.
- `hdl/aecp/KL_aecp_notify.sv:832` the emission pick reads `cmdq_nempty_r` instead of `cmdq_count_r != 0`.
- `hdl/aecp/KL_aecp_notify.sv:1165` `amap_busy_o` reads `cmdq_nempty_r` instead of `cmdq_count_r != 0`.
- `hdl/aecp/KL_aecp_notify.sv:1196` reset clears it; `:1299` a push sets it; `:1511` a pop with no
  push writes `cmdq_count_r != 1` (a pop beside a push keeps it set, count unchanged).
- `hdl/packet_engine/KL_pp_event_router.sv:109-117` comment; `:121` pending-minus-presented keyed on
  `valid_r`; `:125` scan base keyed on `valid_r`; `:146-147` `sel_next_w`; `:186` `sel_r <= sel_next_w`
  inside the unchanged load enable `deliver_w || !valid_r` (`:184`).
- `docs/architecture/03_packet_engine.md:227-231` the router's registered scan.
- `docs/architecture/06_aecp_engine.md:968` the queue row records `cmdq_nempty_r`.
- `syn/ooc/README.md:241-285` the OOC measurement of the cone, base and head, 1x1 and 8x8, with the two
  halves and the statement that the depth does not halve.

No register-map, top-level port or parameter change. Nothing outside `u_notify` and `u_event_router`
and their docs changes. The queue's push condition (`cmd_class_ok_w`, `cmd_push_w`) and every emission
rule are untouched, so the #176, #177 and #178 code paths are not touched.

## Accepted lengths and refusal cases (unchanged)

This lane changes no command decode. SET_STREAM_INFO (06 §6.3 row, IEEE 1722.1-2021 7.4.15, Milan v1.2
5.4.2.9) is accepted at head exactly as at base:

- Accepted: the 2021 84-byte body only (control_data_length 96).
- The 2013 form is refused BAD_ARGUMENTS at the 2021 response length (that is #176's lane).
- NOT_SUPPORTED for a Stream Input, and for any flag set other than MSRP_ACC_LAT_VALID alone.
- BAD_ARGUMENTS for an offset with bit 31 set.
- STREAM_IS_RUNNING while streaming.
- ENTITY_LOCKED under another controller's lock.
- NO_SUCH_DESCRIPTOR.

Its success notification (7.4.15: "On success this command also sends an unsolicited notification")
is pushed on the same queue condition and emitted in the same cycle as at base (proofs below).

## Behaviour: equivalence, no added cycle

No cycle of latency is added. Every port of both modules is cycle-for-cycle equal to base, so the
documented service bounds are unchanged and there is nothing to re-derive.

- Router: Yosys sequential equivalence of base against head `KL_pp_event_router`
  (`equiv_make`, `equiv_simple -seq 2`, `equiv_induct -seq 2`, `equiv_status -assert`), with every port
  and register matched, at `N_SRC_P` 1, 5, 8, 16 and 29. All equivalence cells are proven
  (91 / 205 / 286 / 505 / 859), 0 unproven.
- Notify: temporal induction (`sat -tempinduct -prove inv_ok 1 -set-at 1 rst_n 0 -seq 1 -maxsteps 1
  -verify`, 1-inductive) proves `cmdq_nempty_r == (cmdq_count_r != 0)` in every cycle after reset at
  1 in / 1 out. It is also proven at the default shape and at `N_IF_P=2, EN_IDENTIFY_NOTIF_P=1`
  (deeper bound). Given the invariant, the head's two reads of `cmdq_nempty_r` are the base's two reads
  of `cmdq_count_r != 0`. The head differs from base only by those reads and the flop (diff recorded),
  so every output is unchanged.

### New checks and their planted mutants (scratch only, not in the tree)

| Check | Mutant | Result | Failing words |
|---|---|---|---|
| notify invariant (1x1) | N1 pop keeps occupied: `:1511` `<= 1'b1` | rc 1 | `Induction step failed` ... `ERROR: Called with -verify and proof did fail!` |
| notify invariant (1x1) | N2 push not seen: `:1299` deleted | rc 1 | same |
| notify invariant (1x1) | N3 pop off by one: `:1511` `!= 5'd0` | rc 1 | same |
| notify invariant (1x1) | none (control) | rc 0 | `Induction step proven: SUCCESS!` |
| router equivalence (N=8) | R1 base always `ptr_r`: `:125` | rc 1 | `ERROR: Found 6 unproven $equiv cells in 'equiv_status -assert'.` |
| router equivalence (N=8) | R2 presented not removed: `:121` `if (1'b0)` | rc 1 | `ERROR: Found 2 unproven $equiv cells ...` |
| router equivalence (N=8) | R3 load ignores ack: `:184` `if (1'b1)` | rc 1 | `ERROR: Found 8 unproven $equiv cells ...` |
| router equivalence (N=8) | none (control) | rc 0 | `Of those cells 286 are proven and 0 are unproven.` |

## Depth: OOC synthesis (processor recipe `syn/ooc/protocol_processor_ooc.tcl`, unchanged, 10 ns)

| | 1x1 base | 1x1 head | 8x8 base | 8x8 head |
|---|---:|---:|---:|---:|
| `cmdq_count_r` -> `sel_r` | 22 levels, -2.204 ns | no path | 32 levels, -8.234 ns | no path |
| `cmdq_count_r` -> `cmdq_nempty_r` | - | 3 levels, +7.716 | - | 2 levels, +7.936 |
| `cmdq_nempty_r` -> `sel_r` | - | **22 levels**, -1.719 | - | **22 levels**, -2.032 |
| deepest into `sel_r` | 24, `u_talker/gp_valid_r` | 24, same start | 39, `u_notify/ctr_pend_r`, D | 28, same start, CE |
| WNS | -5.416 | -5.416 | -11.482 | -6.045 |

Along the head's 22-level occupancy-to-select path, by block (nets):

- `u_notify`: 3;
- `u_aecp` / `u_dispatch` / `u_scoreboard` / `u_listener`: 16 at 1x1, 18 at 8x8;
- `u_event_router`: 6 at 1x1, 4 at 8x8.

At base 8x8 the router alone held 14. The cut therefore saves about 10 levels at 8x8 and none at 1x1,
where the count compare was already folded into the emission pick.

## Depth and WNS: parent route-1x1 (recipe unchanged, exclusive lock, `pp_resource_gate.py check --endpoint route-1x1`)

| Route | WNS | gate rc | worst path | `cmdq_count_r` -> `sel_r` | `cmdq_nempty_r` -> `sel_r` |
|---|---:|---:|---|---|---|
| base `22c139a4` + #760 | +0.016 ns | 1 (`REGRESSION: below the floor 0.03`) | the cone, 30 levels | 30 levels, +0.016 | - |
| head, without #760 | +0.181 ns | 0 | `u_aecp/u_d3/rec_r` -> `deb_cnt_r`, 28 levels | no path | 24 levels, +2.778 |
| head + #760 | +0.144 ns | 0 | Ethernet rx group, `tx_crc_pipe_valid` -> `KL_gptp_gmii_launch/src_in_r`, 8 levels | no path | 24 levels, +3.196 |

Both routes that item 3 requires (head without and with #760) are recorded. Routed, the count's half
is 2 levels (+17.7 / +16.8 ns). The occupancy-to-select half is 24 of the cone's 30:

- 3 levels in `u_notify`;
- about 15 in `u_aecp` / `u_dispatch` / `u_scoreboard` / `u_listener`;
- 5 in the router after the acknowledge.

Every other figure passes the gate. #760 is `760-pdelay-hysteresis` at `22840662`, read only. It was
applied to the scratch parent's working tree only and reverted after each route.

## Base and head records

Processor gates, unpiped, one log and rc per gate. Base ran in the scratch parent's submodule at
`22c139a4`, head in the lane at `16c89c53`. Toolchain: pinned Verilator 5.050, sv2v v0.0.12, Yosys 0.33.

| Gate | base rc | head rc | verdict line (identical at both) |
|---|---:|---:|---|
| `scripts/run_suites.sh` | 0 | 0 | `suites: 1029951 checks total, 0 failing` |
| `scripts/check-req-tags.py --suites --evidence` | 0 | 0 | `req-tags executed: 226 evidence lines, 14 suites, OK` |
| `scripts/lint_hdl.sh` | 0 | 0 | whole log identical (41 `LINT OK` lines) |
| `make check` | 0 | 0 | whole log identical |
| `scripts/gen_matrix.py --check` | 0 | 0 | `matrix: OK (94 rows, 0 untested)` |
| `syn/yosys/run.sh` | 0 | 0 | identical except flattened-netlist line numbers (`all.v:N`) in Yosys warnings |
| `tb/elab_guards/guards.py --frontend yosys` | 0 | 0 | `elab guards: 93 checks: 93 PASS, 0 FAIL`; identical except source line numbers |

Campaigns that build a changed file (`KL_aecp_notify.sv` or `KL_pp_event_router.sv`). Base ran in a
clean export of `22c139a4`, head in the lane at the head's RTL. Records are compared on their graded
lines, with tree, output and temporary paths and timings normalised:

| Campaign | base rc | head rc | records |
|---|---:|---:|---|
| `tb/pp_top/d3_mutants.py` | 0 | 0 | console identical, 117 / 117 records identical |
| `tb/pp_top/notify_mutants.py` | 0 | 0 | identical, 107 / 107 |
| `make -C tb/pp_top aecp-dispatch-mutants` | 0 | 0 | identical, 45 / 45 |
| `make -C tb/pp_top aecp-mutants` | 0 | 0 | identical, 67 / 67 |
| `make -C tb/pp_top ctr-mutants` | 0 | 0 | identical, 18 / 18 |
| `tb/pp_top/gsi_mutants.py` | 0 | 0 | identical, 45 / 45 |
| `tb/pp_top/name_wr_mutant.py` | 0 | 0 | identical, 7 / 7 |
| `tb/pp_top/acmp_mutants.py` | 0 | 0 | identical, 58 / 58 (`ACMP mutations: 51 of 51 KILLED by their named checks; goldens PASS`) |
| `make -C tb/name_state mutants` | 0 | 0 | identical, 39 / 39 |
| `make -C tb/elab_guards mutants` | 0 | 0 | 161 / 161 identical once source line numbers (`KL_aecp_notify.sv:N`, `all.v:N`) are normalised; `elab guard mutants: 160 of 160 killed` |

The head campaign run was resumed after the 10:57 crash. `acmp` (cut mid-run), `name_state` and
`elab_guards` re-ran from scratch; the others completed before the crash, at the same RTL.

## Scratch-parent consumer gate table

Scratch parent: milan-fpga dev `7d79ffb26308ac51eaeeab6ec43d798d057ae0cd`, its `protocol-processor`
gitlink staged at base `22c139a4` and then at head `16c89c53`, never committed or pushed. Before and
after each run, the parent's status is that one staged gitlink only.

| Gate | base rc | head rc |
|---|---:|---:|
| `bdd` (406 scenarios passed, 0 failed) | 0 | 0 |
| `feature_status` / selftest | 0 / 0 | 0 / 0 |
| `pp_srcs --check --selftest` | 0 | 0 |
| `check_py_idiom` / selftest | 0 / 0 | 0 / 0 |
| `check_cpp_idiom` / selftest | 0 / 0 | 0 / 0 |
| `check_sv_idiom` / selftest | 0 / 0 | 0 / 0 |
| `check_sh_idiom` / selftest | 0 / 0 | 0 / 0 |
| `check_todo_ownership` / selftest | 0 / 0 | 0 / 0 |
| `check_port_contracts` / selftest | 0 / 0 | 0 / 0 |
| `check_rtl_source_lists` / selftest | 0 / 0 | 0 / 0 |
| `check_soc_sources` / selftest | 0 / 0 | 0 / 0 |
| `check_submodule_docs` / selftest | 1 / 0 | 1 / 0 |
| `check_hygiene` / selftest | 0 / 0 | 0 / 0 |
| `measure_test_evidence` / selftest | 1 / 1 | 1 / 1 |
| `measure_naming` / selftest | 0 / 0 | 0 / 0 |
| `measure_fail_fast` / selftest | 0 / 0 | 0 / 0 |
| `measure_control_flow` / `measure_cohesion` selftests | 0 / 0 | 0 / 0 |
| `check_nvm_record_space` / selftest | 0 / 0 | 0 / 0 |
| `check_entity_shape` selftest | 0 | 0 |
| `check_wire_accountability` | 0 | 0 |
| `lint_rtl --check --self-test` | 0 | 0 |
| `ooc.sh --record-rom-digests tcam` | 0 | 0 |
| `ooc_selftest` | 0 | 0 |
| `ooc.sh KL_pp_shadow` | 0 | 0 |

The rc table is identical at base and head. Every log is identical except three:

- `bdd`: step timings.
- The ROM digest record: the pin sha. The digests themselves are identical (`ltn_rom.hex` `23cc67ee…`,
  `ucode.hex` `518b900c…`).
- `ooc.sh KL_pp_shadow`: LUT 56117 -> 56021, FF 26281 -> 26282; RAMB, DSP and CARRY4 unchanged.

The two rc 1 rows match at base and head and are not this lane's:

- `check_submodule_docs` reports `protocol-processor: documented pin differs from Git` (the moved
  gitlink) and the stale submodule diagram.
- `measure_test_evidence` reports `FAIL: 3 unexplained DUT-source reader(s) > ratchet 0`, with the same
  readers at both.

## Tool identities

- Verilator 5.050 (`2026-07-01 rev v5.050`), the pinned build, exported first on PATH
- sv2v v0.0.12, sha256 `b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b`
- Yosys 0.33 (git sha1 `2584903a060`), the CI image's, sha256
  `88c0a12bb814a1a8716b1ae10b482e35d3005ed558e1f5f626b3dc983ea3abd0`. The scratch parent's own gates
  use the host Yosys 0.66, as its scripts pick it, the same at base and head.
- Python 3.14.8; Vivado 2026.1, every run under the exclusive lock

## Scratch (not in the tree, not in this directory)

Logs, campaign outputs, proofs, mutants, and OOC and routed reports are under the lane's scratch root:
`logs/{base,head2}`, `camp/{base,head}`, `equiv/`, `ooc/`, `cone/`, `route-*`, `prec/{base,head2}` and
`route-chain.txt`.

## Round 2

Status: REVIEW READY at head `c5afc0a42f200af01dd83e67b579dc3badc42601`. Steps 0 to 4 are done.
REVIEW READY was posted on processor issue #181 as comment 6252495012 (2026-10-18).

- Every processor gate, and every campaign that builds a changed file, returns rc 0 at base `08ae0013` and
  at the head. Every record is identical except the new checks themselves.
- Route-1x1 with #760 at the head closes at WNS **+0.220 ns**, and the route-1x1 resource gate returns
  rc 0. `cmdq_count_r` has no path to `sel_r`, and the worst path is in `u_aecp`, outside this cone.
- One item is not met as worded: "the parent consumer gates ... all rc 0". The scratch parent's rc table is
  identical at base and head, but three rows return rc 1 at both. They are the moved gitlink's
  documented pin, and dev's own test-evidence ratchet with its self-test. Both predate this change, and
  this lane cannot change them (see the consumer gate table below). The round-2 STOP condition (a
  register-map, port or parameter change) did not occur.

Assignment: PR #187 comment 6249816230 (A10). Ruling: issue #181 comment 6249065327. Reviews, both
NEGATIVE at `42eb9aef`: R649-1 (6249229516) and R648-1 (6249813126), whose mutant diffs were read from
their published receipts (milan-fpga `65f0ab37`, `review-evidence/pp181-r1/reviews/R648-1/receipts/`).

- Branch `181-notify-router-cut`, from `42eb9aef`. New head: `c5afc0a42f200af01dd83e67b579dc3badc42601`.
  Three commits, not pushed:
  - `2cacc920` merges processor main `08ae0013` (#183, #176's SET_STREAM_INFO 2013 body). Its tree
    `0e779022` is the one `git merge-tree --write-tree 42eb9aef origin/main` gave, with no conflict;
  - `a0a57895` is R649-1-F2's comment wording (comment only);
  - `c5afc0a4` is R648-1-F-2's in-tree checks.
- Base for every round-2 base/head comparison: processor main `08ae00130f096f241463172c4781885934400ee4`.
- `git diff 42eb9aef c5afc0a4 -- hdl` holds main's #176 RTL (`KL_aecp_engine.sv`) and, in this lane's two
  files, comment lines only. No register-map, top-level port or parameter change; nothing outside the
  `u_notify` / `u_event_router` cone, its tests and the docs that record it.

### Step 0: the merge

`2cacc920` merges `origin/main` at `08ae0013` (at least `08ae0013`, as assigned). No rebase.

### Step 3: R649-1-F2, the exact wording (`a0a57895`)

- `hdl/aecp/KL_aecp_notify.sv:426`: `(issue #181)` is now `(issue #181; REQ-NOT-001, REQ-NOT-002)`.
- `hdl/packet_engine/KL_pp_event_router.sv:110`: `(issue #181)` is now `(issue #181; REQ-REU-001, F02.6)`.

Both comments were re-wrapped to the file's width without changing a word, so every later line of
`KL_aecp_notify.sv` moved down by one. The occupancy flop's lines are now `:430` (declaration), `:833`
(emission pick), `:1166` (`amap_busy_o`), `:1197` (reset), `:1300` (push) and `:1512` (pop without push).

### Step 2: R648-1-F-2, the occupancy invariant in tree (`c5afc0a4`)

Every change, file:line at the head:

- `tb/aecp_notify/occupancy.vlt:1-8` (new): a Verilator configuration file. `public_flat_rd` on
  `KL_aecp_notify`'s `cmdq_count_r` and `cmdq_nempty_r` makes the two readable by the bench. No RTL changes.
- `tb/aecp_notify/Makefile:22-24`: every build reads `occupancy.vlt` (in `SRCS`).
- `tb/aecp_notify/sim_main.cpp`:
  - `:17` includes the root class header;
  - `:43` adds `NOTIF_QUEUE_DEPTH`, which cites `P-NOTIF-QUEUE-DEPTH` (F01.5, 16);
  - `:47-75` section OC: `struct Occupancy` samples both registers after every clock edge, and
    `occupancy_held` is check **OC1**;
  - `:142`, `:1196` and `port_tuple.hpp:74,91` sample in every harness's `tick()`;
  - `:289`, `:294`, `:341`, `:1272`, `:1299` and `port_tuple.hpp:634` end every run with OC1. That covers
    the default run, SC1, SC2, FT (including its premise's early return) and the third build;
  - `:968-1113` section CQ: `queue_drain` (`:985`) presents the pushes and plays the engine; `delivered`
    (`:1022`) is the independent expectation; `command_queue` (`:1057`) holds checks **CQ1**, **CQ1b**,
    **CQ2** and **CQ2b** (`:1090-1110`, with `REQ_TAG("REQ-NOT-001", "DIR", "CQ2")` at `:1098`);
  - `:340` runs CQ after CX.
- `tb/pp_top/notify_mutants.py:622-674`: the eleven planted mutants, as arms of the existing notify campaign.
  The docstring is at `:31-33`.
- `tb/aecp_notify/README.md:14-17,27-29,37-40,359-420`: sections CQ and OC, the counts (67 to 80) and the
  mutation record.
- `docs/architecture/09_verification.md:309,330-331`: the CQ and OC rows of section 8.4 ("nine of the
  notification block's").
- `docs/architecture/06_aecp_engine.md:998`: the `cmdq_*` row names OC and CQ.

The checks:

- **OC1** (every run of every build): `cmdq_nempty_r == (cmdq_count_r != 0)` at every clock edge.
- **CQ1**: two commands back to back into an idle block, the second pushed in the clock the emitter claims
  the first (the count reads 1 after it, not 2). C receives entry 0, and D entries 0 and 1, in order, each
  at its next sequence_id.
- **CQ1b**: `amap_busy_o` is low before the first push, high in every clock from the one after it to the
  last job, and low after. In the clock after the first push, only the queue holds it.
- **CQ2**: `P-NOTIF-QUEUE-DEPTH` + 1 = 17 commands back to back behind a held round. That gives one entry
  in the round and a full queue (16), the second command again beside the first's claim. Every entry
  reaches each registered controller but its requester, in order, at that controller's next
  sequence_id: 26 jobs.
- **CQ2b**: as CQ1b through 17 rounds. Between two rounds, only the queue holds `amap_busy_o` for a clock.

The suite grows from 67 to 80 checks: 51 in the first run, 5 in FT, 20 in the third build, and 2 in each
of SC1 and SC2. The CQ checks pass on the RTL before the flop (main `08ae0013`) with the same jobs and the
same `amap_busy_o` trace (`receipts-r2/in-tree-checks/basecq/`), so they describe unchanged behaviour.
R648-1's base equivalents fail them: B5 fails CQ1b and CQ2b, and B7 fails CQ2.

### New checks and their planted mutants (in tree: `tb/pp_top/notify_mutants.py`)

The N labels are R648-1's (`receipts/mutant_N*.diff`); the edits are the reviewer's own. Every arm is
KILLED by its named checks in the head campaign (`receipts-r2/camp/head/notify/results.json`, `109 of
109 KILLED`):

| R648-1 | Arm | Planted | Named checks | Failing words (the head campaign) |
|---|---|---|---|---|
| N1 | `occupancy_pop_keeps_set` | a pop without a push leaves the occupancy set | OC1, CQ1, CQ2 | `FAIL: OC1: ... (134 of 12411 edges differ ...)`, `FAIL: CQ1: ...`, `FAIL: CQ2: ...`; also DR2, DR2b, CQ1b, CQ2b |
| N2 | `occupancy_push_unseen` | a push does not set it | OC1, CQ1, CQ1b, CQ2, CQ2b | `FAIL: CQ1: ... (count 2 after it, want 1) ...`; also DR2, DR2b |
| N3 | `occupancy_pop_one_late` | a pop clears it one entry late | OC1, CQ1, CQ2 | `FAIL: OC1: ...`, `FAIL: CQ1: ...`, `FAIL: CQ2: ...`; also DR2, DR2b |
| **N4** | `occupancy_cleared_beside_push` | a pop beside a push clears it, so CQ1's last entry is stranded | OC1, CQ1 | `FAIL: CQ1: two commands back to back, the second pushed in the clock the first is claimed (count 1 after it, want 1): ... (2 jobs, want 3)`, `FAIL: OC1: ... (40 of 8609 edges differ ...)` |
| **N5** | `occupancy_not_busy` | `amap_busy_o` drops the occupancy term | CQ1b, CQ2b | `FAIL: CQ1b: ... (2 low) ...`, `FAIL: CQ2b: ... between rounds included (17 low) ...` |
| N6 | `occupancy_reset_set` (and `_identify`, `_interfaces`, `_collision`, `_failure`) | the reset sets it | OC1 | `FAIL: OC1: ... the first at edge 1)` in each of the five runs (the default run fails 13 other checks too, the third build 12, SC1 and SC2 one each, FT none) |
| **N7** | `occupancy_pop_clears` | a pop without a push clears it, so CQ2's queue is stranded | OC1, CQ2 | `FAIL: CQ2: ... (16 entries at most, want 16; 1 after the push beside the first claim, want 1) ... (3 jobs, want 26)`, `FAIL: OC1: ... (36 of 8515 edges differ ...)` |

N4, N5 and N7 each fail at least one in-tree check by name, as step 2 requires. The four `occupancy_reset_set_*`
arms put OC1's failure on record in the four runs that `make run` does not reach once the first binary
fails. Every new check is failed by a planted mutant: OC1 by N1-N4, N6 and N7; CQ1 by N1-N4 and N6; CQ1b by
N1, N2, N5 and N6; CQ2 by N1-N3, N6 and N7; CQ2b by N1, N2, N5 and N6.

### The out-of-tree proofs, re-run at the head (`receipts-r2/proofs/`)

These are the round-1 proofs, the same scripts with only their scratch paths changed. The sources are
taken from `c5afc0a4` and, for the router's gold, from `08ae0013`. Yosys 0.33.

- Router equivalence (base `08ae0013` against head; every port and register matched; `equiv_simple -seq
  2`, `equiv_induct -seq 2`, `equiv_status -assert`). At `N_SRC_P` 1, 5, 8, 16 and 29, every cell is proven
  (91 / 205 / 286 / 505 / 859, 0 unproven). Mutants at N = 8 each fail with `ERROR: Found N unproven $equiv
  cells in 'equiv_status -assert'.`:
  - R1, the base always `ptr_r`: 6 unproven;
  - R2, the presented event not removed: 2;
  - R3, the load ignores the acknowledge: 8;
  - R4, the select reloads outside the enable (R648-1's edit): 6;
  - R5, no grant clears the select (R648-1's edit): 6.
- Occupancy induction (`sat -tempinduct -prove inv_ok 1 -set-at 1 rst_n 0 -seq 1 -maxsteps 1 -verify`):
  - proven (`Induction step proven: SUCCESS!`) at 1 in / 1 out, at the default shape and at `N_IF_P=2,
    EN_IDENTIFY_NOTIF_P=1`;
  - N1, N2, N3, N4, N6 and N7 each fail (`ERROR: Called with -verify and proof did fail!`);
  - N5 is proven, as it must be: it only reads the flop, and the in-tree CQ1b and CQ2b kill it.

  The full induction logs (9 to 19 MB) are kept in scratch. `LARGE.tsv` lists their sha256 and size, and
  each has an excerpt beside it.

### Step 1: receipts (`receipts-r2/` in this directory)

`receipts-r2/RECEIPTS.md` is the index: what ran, at which head, and with which command. It covers gate
logs, OOC and route reports with the exact commands, proof, control and mutant logs, the campaign records
and the parent consumer gates. Text files are at most 200 KB, with host paths redacted (`<home>`,
`<data>`, `<host>`). Larger files are listed in `LARGE.tsv` by sha256 and size, with an excerpt where they
are text. `sums/RAW-<dir>.sha256` hold every copied file's digest before redaction, and
`sums/MANIFEST-<dir>.sha256` the published bytes. `sha256sum -c sums/MANIFEST-*.sha256` passes.

Which head each receipt ran at:

- `c5afc0a4` (the head): processor gates (`logs/head`), campaigns (`camp/head`), the scratch parent's
  consumer gates (`pgates/head`), route-1x1 with #760 (`route-head760`), OOC (`ooc/head-*`) and the proofs
  (`proofs`, sources `git show c5afc0a4:...`).
- `08ae0013` (main, the base): processor gates (`logs/base`, in the scratch parent's submodule),
  campaigns (`camp/base`, in a clean `git archive` export), consumer gates (`pgates/base`) and OOC
  (`ooc/base-*`, the same export).
- The working tree just before `a0a57895`'s comment edit (the same bench and RTL logic as the head):
  `in-tree-checks/occ2`, the eleven arms' development run (all KILLED), `in-tree-checks/basecq` and
  `in-tree-checks/pre`. The head campaign repeats the eleven arms at `c5afc0a4`.
- The round-1 receipts at `16c89c53` stay where the manager published them (milan-fpga `d678eaa0`,
  `review-evidence/pp181-r1/author-receipts/`).

### Route-1x1 with #760 at the head (recipe unchanged)

Scratch parent: milan-fpga dev `7d79ffb2`, gitlink staged at `c5afc0a4`, and #760 applied to the working
tree only (`22840662`; patch sha256 `003e4985...`, the round-1 patch, re-verified against the #760 lane's
`git diff 7d79ffb2 22840662`). It was reverted after the route, and the parent's status went back to the
one staged gitlink (`receipts-r2/route-head760/chain.txt`). The driver is round 1's `route.sh`
(`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`):

1. the dry run and the elaboration;
2. `pp_baseline.py --single-thread-synthesis`;
3. Vivado `baseline_integrated.tcl` under `flock -x $VIVADO_LOCK`;
4. `pp_resource_gate.py check --endpoint route-1x1`.

The only difference from round 1 is the SDK's location. The round-1 SDK, in another lane's scratch, had
been removed, so the parent's own installer put the same pinned release into this lane's scratch and
verified it. The routed cone reports are `route_cone.tcl` on the routed checkpoint.

| Route | WNS | WHS | gate | worst setup path | `cmdq_count_r` -> `sel_r` | count -> occupancy | occupancy -> `sel_r` | worst into `sel_r` |
|---|---:|---:|---|---|---|---|---|---|
| round 1: base `22c139a4` + #760 | +0.016 | - | rc 1 (`REGRESSION: below the floor 0.03`) | the cone, 30 levels | 30 levels, +0.016 | - | - | - |
| round 1: head `16c89c53` + #760 | +0.144 | +0.036 | rc 0 | Ethernet rx, 8 levels | no path | 2 levels | 24 levels, +3.196 | - |
| **round 2: head `c5afc0a4` + #760** | **+0.220** | +0.029 | **rc 0** (`RESULT: PASS`) | `u_aecp/u_ucpu/uop_e_r` -> `u_aecp/u_d3/deb_cnt_r`, 34 levels | **no path** | 2 levels, +16.795 | 22 levels, +3.510 | `u_notify/ctr_pend_r[2]`, 24 levels, +1.758 |

The round-2 gate figures are LUT 49806, FF 52406, SLICE 15668, RAMB36 74, RAMB18 25 and DSP 14. Route
status: complete, no unrouted net. Under the ruling, the cone no longer limits the shipping timing gate. The
route closes above the +0.030 ns floor, and the worst path is internal to `u_aecp`, not through the cone.
Routed, the half after the register is 22 levels at this head (24 at round 1's).

### OOC at the head and the base (`syn/ooc/protocol_processor_ooc.tcl`, unchanged, 10 ns)

| | 1x1 base `08ae0013` | 1x1 head | 8x8 base | 8x8 head |
|---|---:|---:|---:|---:|
| `cmdq_count_r` -> `sel_r` | 22 levels, -2.653 | no path | 33 levels, -8.930 (CE) | no path |
| `cmdq_count_r` -> `cmdq_nempty_r` | - | 3 levels, +7.716 | - | 2 levels, +7.909 |
| `cmdq_nempty_r` -> `sel_r` | - | **19 levels**, -0.367 | - | **21 levels**, -1.741 (CE) |
| deepest into `sel_r` | 24, `u_talker/gp_valid_r`, -3.282 | 20, the same start, -0.956 | 36, `u_notify/ctr_pend_r`, -10.720 (CE) | 25, the same start, -4.303 (CE) |
| WNS | -4.819 (`u_aecp/u_d3`) | -4.819 | -10.720 | -5.844 |

The half after the register is 19 levels at 1x1 and 21 at 8x8. Round 1 measured 22 at both, at
`16c89c53`; the head now also carries main's #176 engine change on the cone's AECP side. The depth still
does not halve. Under the ruling, that is no longer the acceptance item. `syn/ooc/README.md` keeps round
1's dated record (see "Not done").

### Processor gates, base and head (unpiped, one log and rc per gate)

Base ran in the scratch parent's submodule at `08ae0013`, head in the lane at `c5afc0a4`. Toolchain:
pinned Verilator 5.050, sv2v v0.0.12, Yosys 0.33.

| Gate | base rc | head rc | verdict line (base / head) |
|---|---:|---:|---|
| `scripts/run_suites.sh` | 0 | 0 | `suites: 1030000 checks total, 0 failing` / `suites: 1030013 checks total, 0 failing` |
| `scripts/check-req-tags.py --suites --evidence` | 0 | 0 | `req-tags executed: 226 evidence lines, 14 suites, OK` / `227 ...` |
| `scripts/lint_hdl.sh` | 0 | 0 | whole log identical (41 `LINT OK` lines) |
| `make check` | 0 | 0 | identical but the tag count (226 / 227 tags) and the ID scan's file count (592 / 593) |
| `scripts/gen_matrix.py --check` | 0 | 0 | identical: `matrix: OK (94 rows, 0 untested)` |
| `syn/yosys/run.sh` | 0 | 0 | identical once netlist line numbers (`all.v:N`) are normalised |
| `tb/elab_guards/guards.py --frontend yosys` | 0 | 0 | identical once line numbers are normalised: `elab guards: 93 checks: 93 PASS, 0 FAIL` |

`run_suites.sh` differs in exactly two lines: `aecp_notify (67 checks ...)` becomes `(80 checks ...)`,
and the total grows by those 13. `git status` is empty after every run.

### Campaigns that build a changed file, base and head

Base ran in a clean export of `08ae0013`, head in the lane. Records were compared with
`scripts/camp_compare_lines.py` (round 1's comparator with line-number normalisation;
`receipts-r2/camp/camp_compare_lines.out`):

| Campaign | base rc | head rc | verdict (base / head) | records |
|---|---:|---:|---|---|
| `tb/pp_top/d3_mutants.py` | 0 | 0 | `D3 mutations: 110 of 110 KILLED` | 117 / 117 identical |
| `tb/pp_top/notify_mutants.py` | 0 | 0 | `98 of 98` / `109 of 109 KILLED by their named checks; goldens PASS` | 112 base / 123 head: every base record is identical at head but the run golden's log, whose tally gains the new checks (65 / 76), and `results.json`, which gains the eleven arms (its shared entries keep their verdicts and failing checks) |
| `make -C tb/pp_top aecp-dispatch-mutants` | 0 | 0 | | 59 / 59 identical |
| `make -C tb/pp_top aecp-mutants` | 0 | 0 | `67 checks: 67 PASS` | 67 / 67 identical |
| `make -C tb/pp_top ctr-mutants` | 0 | 0 | `18 checks: 18 PASS` | 18 / 18 identical |
| `tb/pp_top/gsi_mutants.py` | 0 | 0 | `GSI mutations: 20 detected by named checks` | 45 / 45 identical |
| `tb/pp_top/name_wr_mutant.py` | 0 | 0 | `decode killed; golden and restored PASS` | 7 / 7 identical |
| `tb/pp_top/acmp_mutants.py` | 0 | 0 | `ACMP mutations: 51 of 51 KILLED` | 58 / 58 identical |
| `make -C tb/name_state mutants` | 0 | 0 | | 39 / 39 identical |
| `make -C tb/elab_guards mutants` | 0 | 0 | `elab guard mutants: 160 of 160 killed` | 161 / 161 identical once line numbers are normalised |

In the notify campaign, the eleven head-only records are the new arms. Every shared mutant has the same
verdict and the same failing checks at base and head, so no existing mutation record changed.

### Scratch-parent consumer gate table

Scratch parent: milan-fpga dev `7d79ffb26308ac51eaeeab6ec43d798d057ae0cd`, its `protocol-processor`
gitlink staged at base `08ae0013` and then at head `c5afc0a4`, never committed or pushed. Before and after
each run the parent's status is that one staged gitlink only (`pgates/*/parent-status-*.txt`).

| Gate | base rc | head rc |
|---|---:|---:|
| `bdd` (406 scenarios passed, 0 failed) | 0 | 0 |
| `feature_status` / selftest | 0 / 0 | 0 / 0 |
| `pp_srcs --check --selftest` | 0 | 0 |
| `check_py_idiom` / selftest | 0 / 0 | 0 / 0 |
| `check_cpp_idiom` / selftest | 0 / 0 | 0 / 0 |
| `check_sv_idiom` / selftest | 0 / 0 | 0 / 0 |
| `check_sh_idiom` / selftest | 0 / 0 | 0 / 0 |
| `check_todo_ownership` / selftest | 0 / 0 | 0 / 0 |
| `check_port_contracts` / selftest | 0 / 0 | 0 / 0 |
| `check_rtl_source_lists` / selftest | 0 / 0 | 0 / 0 |
| `check_soc_sources` / selftest | 0 / 0 | 0 / 0 |
| `check_submodule_docs` / selftest | **1** / 0 | **1** / 0 |
| `check_hygiene` / selftest | 0 / 0 | 0 / 0 |
| `measure_test_evidence` / selftest | **1 / 1** | **1 / 1** |
| `measure_naming` / selftest | 0 / 0 | 0 / 0 |
| `measure_fail_fast` / selftest | 0 / 0 | 0 / 0 |
| `measure_control_flow` / `measure_cohesion` selftests | 0 / 0 | 0 / 0 |
| `check_nvm_record_space` / selftest | 0 / 0 | 0 / 0 |
| `check_entity_shape` selftest | 0 | 0 |
| `check_wire_accountability` | 0 | 0 |
| `lint_rtl --check --self-test` | 0 | 0 |
| `ooc.sh --record-rom-digests tcam` | 0 | 0 |
| `ooc_selftest` | 0 | 0 |
| `ooc.sh KL_pp_shadow` | 0 | 0 |

The rc table is identical at base and head. Every log is identical except these:

- `bdd`: step timings.
- `check_py_idiom`: 248304 / 248355 first-party lines (the campaign's eleven arms).
- `check_todo_ownership`: 1297 / 1298 files read (`occupancy.vlt`).
- The ROM digest record: the pin sha. The digests are identical (`ltn_rom.hex` `23cc67ee...`, `ucode.hex`
  `a3b62cab...`).
- `ooc.sh KL_pp_shadow`: LUT 56150 -> 55888 and FF 26293 -> 26282. RAMB, DSP and CARRY4 are unchanged.

**Not all rc 0, as step 4 asks.** The three rc 1 rows match at base and head, and they are the same
families as in round 1 at `22c139a4` and `16c89c53`:

- `check_submodule_docs`: `protocol-processor: documented pin differs from Git` and the stale submodule
  diagram. Any moved gitlink fails it until the adoption updates the parent's pin documentation.
- `measure_test_evidence` and its self-test: `FAIL: 3 unexplained DUT-source reader(s) > ratchet 0`. The
  readers are `protocol-processor/tb/aecp_cmds/mutants.py`, `tb/elab_guards/guards.py` and
  `tb/elab_guards/mutants.py`, all present in main `08ae0013`. The parent's
  `scripts/measure_test_evidence_readers.py` dispositions none of the three, at dev `7d79ffb2` or at live
  dev `e9cbb676` (read through the API), which both still pin processor `2cbed0a9`. This head adds no
  reader: `tb/pp_top/notify_mutants.py` already has its disposition. Clearing either row is a parent-side
  edit, outside this lane.

### Accepted lengths and refusal cases (at the head, after main's #176)

This lane changes no command decode. SET_STREAM_INFO (06 §6.3 row, IEEE 1722.1-2021 7.4.15, Milan v1.2
5.4.2.9) is accepted at the head exactly as at main `08ae0013`, which now takes the 2013 body (#176):

- Accepted: exactly two bodies. The 2021 84-byte body (control_data_length 96, Figure 7-40), and the 2013
  48-byte body (control_data_length 60), which is the 2021 body's first 48 bytes. Every answer is the 2021
  form (108 bytes, cdl 96).
- BAD_ARGUMENTS for any other length, shorter or longer, at the full 2021 response length. It writes
  nothing.
- NOT_SUPPORTED for a Stream Input, and for any flag set other than MSRP_ACC_LAT_VALID alone.
- BAD_ARGUMENTS for an offset with bit 31 set.
- STREAM_IS_RUNNING while streaming.
- ENTITY_LOCKED under another controller's lock.
- NO_SUCH_DESCRIPTOR.

Its success notification (7.4.15: "On success this command also sends an unsolicited notification") is
pushed on the same queue condition and emitted in the same cycle as at base (the router equivalence and the
occupancy induction above). Section CQ now grades that queue in tree.

### Not done, and why

- R648-1's S-1 (the router comment's first sentence) and S-2 (pinning `evt_src_o` while idle; "worst
  (least slack)" in `syn/ooc/README.md`) are suggestions outside the round-2 assignment. They were not
  applied. R5 is killed by the out-of-tree equivalence only, as in R648-1.
- `syn/ooc/README.md` still records round 1's measurement (base `22c139a4`, head `16c89c53`), which stays
  true as a dated record. The new head's OOC figures are in `receipts-r2/ooc/` and below. They were not
  written into the tree, because that would have moved the head after its banks.
- R648-1's RES-1 (the PR body's first paragraph) is applied in PR-BODY.md's Round 2 section, word for word.
