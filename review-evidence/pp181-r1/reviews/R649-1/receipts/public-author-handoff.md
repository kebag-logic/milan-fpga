# [A635] #181 handoff — cut the notify-queue to event-router path

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
