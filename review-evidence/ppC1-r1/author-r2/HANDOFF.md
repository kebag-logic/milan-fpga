# [A443] Lane C1 round 2 handoff: SRP/MVRP timers and LeaveAll (PR #133)

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
Branch: `c1-srp-mrp-timers`, round-2 start `81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b`
Assignment: issue #108 comment 5886235840 (round 2); round 1: comment 5883702094
Reviews addressed: R398-1 (PR #133 comment 5885913612, NEGATIVE on F1), R399-1 (comment 5886227048, POSITIVE)
Parent reference: milan-fpga dev `57b8c867` (read-only)

Status: REVIEW READY at `412efeb750e358a65b04bae1cbb3086134d15b7e` (not pushed; no PR edit;
three commits on `81b8d6d`: `e2c631d` item 2, `c9584bc` item 3, `412efeb` item 4; item 1 is
the PR body). No STOP condition met: no top-level port, no parent or processor interface
change. TAKEN posted: #108 comment 5886249432. REVIEW READY posted: #108 comment
5887775920. PR body: `PR-BODY.md` in this directory
(section 4 amended, "Round 2" section added).

## Reconstruction

- Confirmed `origin` = `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`
  and HEAD `81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b`, clean.
- Read: the round-2 assignment (#108 comment 5886235840), the round-1 assignment (5883702094),
  R398-1 (PR #133 comment 5885913612) and R399-1 (5886227048); the review packets
  (`ppC1-r398-1-packet`: REPORT, `patches/rvw-*.patch`, `scripts/run_arms.sh`, receipts;
  `ppC1-r399-1-packet`: REPORT, `scripts/probe_arm_race.py`, `scripts/probe_licence.py`,
  receipts); the previous author packet (`ppC1-a437` HANDOFF and PR-BODY) and its scratch
  (`parent-declared-edit.diff`, the submodule sources used read-only); the manager's consumer
  receipts (`ppC1-manager-81b8d6d7/parent-consumer`, whose `results.json` names the sixteen
  commands: the fifteen public ones plus `python3 scripts/lint_rtl.py --check`).
- Processor: README, docs/README, docs/architecture/09_verification.md, 10_srp_engine.md;
  `hdl/srp` (KL_srp_top cadence plane, VLAN, talker FSM licence term, encoder strobe),
  `hdl/common/KL_pp_prng.sv` (rejection-sampled kind-3 draw: variable latency),
  `hdl/common/KL_pp_timer_service.sv` (arm shadow, wrap-safe compare),
  `hdl/top/protocol_processor_top.sv` (arm-port queues: 4-deep per face, fixed priority
  listener > talker > ADP > SRP; `now_ms` and expiries wired straight from the timer);
  tb/srp_top (harness, wrapper, README, mutants.py, mutations), tb/srp_stream_fsms,
  tb/srp_encoder, tb/pp_top.
- Standards, clause text from 802.1Q-2014: Table 10-5 (rLA!, leavealltimer!), 10.7.4.3,
  10.7.5.22 (leavealltimer!), 10.7.6.10 (Start leavealltimer), 10.7.5.20 b)2) and NOTE,
  10.8.2.6. Milan v1.2 4.3.2 as cited in the tree.
- Parent (read-only, trusted checkout at `57b8c867`): `tb/verilator/milan_dp/README.md` (blob
  `3f05559f`) lines 443 and 528-530, `sim_crf_licence.cpp:953,956`, `scripts/check_cpp_idiom.py`
  and `scripts/code_quality_scope.py` (the submodule-pin rule).
- Toolchain: Verilator 5.050 (the CI pin) through a byte-identical copy of the manager's
  pinned wrapper (sha256 `905795b9...e92f`; `verilator_bin` sha256 `44898b22...bfdd`), first on
  PATH for every processor, probe and parent command.

## Item 1: R398-1 F1, the parent-visible list

PR body only (no processor source change). `PR-BODY.md` section 4, "Parent documents to update
at adoption", now names `tb/verilator/milan_dp/README.md` (blob `3f05559f` at parent dev
`57b8c867`, checked read-only in the trusted checkout):
- line 443, the `[C]` row "76 s bound across five DUT and five switch LeaveAll MRPDUs": becomes
  the re-based bound (at least three DUT and three switch LeaveAll MRPDUs, the declared
  `sim_crf_licence.cpp:953,956` edit);
- lines 528-530, "This station's leavealltimer does not restart on a received LeaveAll
  (processor issue 108), and nothing here measures that.": now implemented (processor docs 10
  section 6.5), measurable with the restart check the list already suggests.
Nothing else in that bullet changed.

## Item 2: R399-1 S1, latency-independent LeaveAll re-arm guard (+ R398-1 S2)

### Design (written before implementation)

**Clause.** 802.1Q-2014 Table 10-5 rLA!: "Start leavealltimer, Passive" in both states;
10.7.6.10 Start leavealltimer: started per 10.7.4.3 (a fresh draw); 10.7.5.22: leavealltimer!
occurs "when the leavealltimer associated with that state machine expires". After rLA! the
associated timer is the restarted one, so a timer-service expiry of the superseded deadline is
not leavealltimer! and must not produce sLA (Passive holds).

**Defect (R399-1 S1).** At `81b8d6d` the stale-expiry guard `la_rearm_w` is
`need_draw_r || draw in flight || cad_pend_r[slot]`. `cad_pend_r` clears when the cadence arm
is *issued*, not when it reaches `KL_pp_timer_service`. The product top queues SRP arms behind
listener, talker and ADP faces (4-deep per face, fixed priority), so with more than two clocks
of arm-path latency the old deadline can still fire after issue and passes the guard: one own
LeaveAll right after the peer's (R399 probe: 4-15 offsets at arm delays 3-16).

**Change.** Replace the `cad_pend_r[slot]` term with "now_ms_i is before the intended deadline
`cad_dl_r[slot]`" (wrap-safe, bit 31 of `now_ms_i - cad_dl_r[slot]`, as the timer service
compares). `cad_dl_r[slot]` is written only when the fresh draw lands, with a deadline 10-15 s
ahead, and it is exactly the value the arm carries; a genuine expiry fires at or after it (the
timer service fires when `now - deadline >= 0`, on the same `now_ms`). The draw-path terms stay:
they are exact state (`need_draw_r`, the in-flight draw), not a latency assumption. So the guard
holds from rLA! until the restarted deadline, whatever the arm-path and PRNG-mux latency.
`cad_pend_r` is subsumed (it is only set together with a deadline 10 s ahead). No port or
parameter change.

**Tests.**
- M10 (group `peer`) and P6 (group `restart`) sweep the peer lane from -k to +1 clocks of the
  real expiry (was -1/0/+1), across the draw request, the PRNG's rejection retries and the arm
  issue. Placement is graded against the calibrated expiry clock (the superseded deadline need
  not fire at all once the arm has landed).
- New P7 (group `restart`): the MVRP equal edge. With the own MVRP flag pending and VID content
  queued, a peer MVRP LeaveAll at -1/0/+1 clocks of the MVRP join tick that would carry the flag:
  -1 and 0 leave no own flag (Passive; the rider's `!dec_la_mvrp_w`), +1 is after tx! so the
  own flag goes out (an accepted own LeaveAll is never retracted).
- New P8 (new group `armdelay`, also in the default run): the committed form of R399-1's
  delayed-arm probe. The wrapper gets a tb-only arm-path delay line (runtime tap, 0 = the
  direct wire, default 0, so every other check is unchanged). At delays 3, 4, 8 and 16 the peer
  MSRP LeaveAll is swept from -(N+12) to +2 clocks of the own MSRP expiry, and in the same
  scenario a peer MVRP LeaveAll around the own MVRP expiry: 0 offsets may produce an own
  LeaveAll, every peer lands at its offset and restarts its timer.
- Mutants: `rearm-at-issue` (the issue-time `cad_pend_r` guard restored) must turn P8 red and
  leave M10/P6 green; the three R398-1 S2 mutants re-based on the new guard:
  `r-rearm-no-inflight` (same edit), `r-rearm-no-deadline` (the successor of
  `rvw-rearm-no-cadpend`: the term that replaced `cad_pend_r` removed) and
  `r-flag-ignores-edge-peer` (same edit), each killed by a named check.

### Implementation

Commit `e2c631d` (line numbers at that commit).

- **RTL.** `hdl/srp/KL_srp_top.sv:1015-1033`: `la_msrp_age_w`/`la_mvrp_age_w` =
  `now_ms_i - cad_dl_r[slot]`; `la_rearm_w[a] = need_draw_r[a] || draw in flight for a ||
  age[31]` (the `cad_pend_r` term replaced); comment states the clause (Table 10-5 rLA!,
  10.7.5.22). Used unchanged at `:1216` and `:1222`. No port, parameter or other logic change.
  Lint (`lint_hdl.sh` flags) clean.
- **Docs.** `docs/architecture/10_srp_engine.md:600-609` (section 6.5, "Start leavealltimer"):
  stale until the restarted deadline, judged from engine state (draw outstanding, or `now_ms`
  before the drawn deadline), not from arm-path latency; cites 10.7.5.22.
- **Wrapper** (`tb/srp_top/srp_top_wrap.sv`, tb only): `:64` input `arm_delay_i`; `:192-229` a
  16-stage arm delay line with a runtime tap (0 = the direct wire, the default for every other
  check); `:375-379` the timer takes the tapped arm; `:127,164` read-only probe
  `dbg_mvrp_join_o` (MVRP join-tick expiry). The DUT's `.arm_*_o (arm_*_w)` connections, the
  `KL_pp_timer_service #(` anchor and the other probe anchors are unchanged, so both reviewers'
  probe scripts still apply as written.
- **Tests** (`tb/srp_top/sim_main.cpp`):
  - `:613` `REARM_CLOCKS = 12`.
  - M9/M10 (`check_peer_at_own_expiry`, `:878`): delta -12..+1 (was -1..+1); M9 grades the
    placement against the calibrated expiry clock and requires the expiry for delta >= 0.
  - P6 (`:1350`): the MVRP lane -12..+1, same grading; coverage check over all 14 offsets.
  - P7 (`check_mvrp_peer_at_flag_tick`, `:1390`): calibrates the MVRP join tick that carries
    the own flag (the clock before `enc_la_r[1]`, confirmed against `dbg_mvrp_join_o`), then a
    peer MVRP LeaveAll at -1/0/+1: no own flag at -1 and 0, the accepted flag goes out at +1,
    timer restarted in all three.
  - P8 (`check_restart_across_arm_latency` `:1442`, `calibrate_expiry_clocks` `:1465`,
    `sweep_arm_offset` `:1496`; group `armdelay`, `:594`, admitted at `:2720`): delays 3, 4,
    8, 16; per offset one reset scenario with the MVRP peer around the own MVRP expiry, then the
    MSRP (Domain) peer around the own MSRP expiry, -(N+12)..+2 clocks; 91 scenarios.
  - `:357` the DUT-clock guard 200 M -> 300 M: the complete default run is now 185,012,669
    clocks (P8 alone 53,331,188; before this change 118,534,445).
- **Results at `e2c631d`** (scratch snapshot, Verilator 5.050): armdelay 13/13, peer 89/89,
  restart 49/49; full default run 2200/2200. P8 prints `own_msrp=0 own_mvrp=0` at every delay.
- **Failing arms** (each built from the checked-in patch in a scratch copy):

  | Arm | Group | Failing checks | Where |
  |---|---|---:|---|
  | `rearm-at-issue` | armdelay | 8 | P8: MSRP 4/4/7/15 offsets at delays 3/4/8/16 (peer -11..-8, -11..-8, -14..-8, -22..-8: exactly the R399-1 receipts), MVRP 2/2/6/14 |
  | `rearm-at-issue` | peer / restart | 0 / 0 | the issue-time guard holds on the direct path (as R399-1 found at delays 0 and 2) |
  | `r-rearm-no-inflight` | peer / restart / armdelay | 3 / 6 / 8 | M10 -4..-2; P6 -7..-2; P8 |
  | `r-rearm-no-deadline` | peer / restart / armdelay | 3 / 0 / 8 | M10 -7..-5; P8 |
  | `r-flag-ignores-edge-peer` | restart | 1 | P7 delta 0 |
  | `stale-expiry-honoured` | peer / armdelay | 7 / 4 | M10 -7..-1 |
  | `mvrp-stale-expiry-honoured` | restart / armdelay | 7 / 4 | P6 -7..-1 |

- **Campaign** (chunked exploration at `e2c631d`'s content, 8 parallel `--only` chunks): 11
  controls pass (new: `srp_top armdelay`), 78/78 arms KILLED, 0 UNPROVEN, coverage union 65/65
  (P1-P8). The gate run of the unchunked entry point is in the gate table.
- `draw-kind-0.patch` regenerated (same edit; its context held the replaced guard line).
- Re-measured counts (README): `mvrp-expiry-only-redraw` 6 -> 17, `stale-expiry-honoured` 1 -> 7,
  `mvrp-stale-expiry-honoured` 1 -> 7, `mvrp-passive-lost` 4 -> 6, `mvrp-flag-at-expiry` 6 -> 11,
  `pending-peer-ignored` 15 -> 26, `leaveall-expiry-lost` 18 -> 16, `preparation-before-slot`
  22 -> 21 (the last two no longer fail M10, whose scenario now sees no own action under them;
  both stay killed by their named assertions, M9 and M5).

## Item 3: docs, licence bound, VLAN-table overflow, ordering assumption

Commit `c9584bc`, docs only (R399-1 S2 = R398-1 S1, plus R398-1 S3). No port, no RTL;
`dbg_vlan_err_o` stays unconnected at the processor top (out of scope).

- `docs/architecture/10_srp_engine.md:251-258`, "The licence's added wait": the wait exists
  only for a Ready registered before the VID's first MVRP MRPDU; it is at most one
  `T-MRP-JOIN` plus any time that MRPDU waits for a TX slot, the TX arbiter, or (the one
  engine-internal case) a canceled own LeaveAll reservation holding MVRP drains back (section
  6.5); closed while the arbiter refuses, open one clock after acceptance (R1; R399-1 S5).
- `:260-270`, "A full VLAN table holds the licence closed": the refused join is dropped
  (`KL_srp_vlan` `user_err_o`, visible only as `dbg_vlan_err_o`, which the processor top does
  not export); closed with Ready and admission, still closed after an entry frees; once an entry
  is free a withdraw + declare opens it as a fresh declaration does (R399-1 S7 probe,
  reproduced at `412efeb`: -1 / -1 / 149 ms); before #65 such a source streamed without a join
  (Milan 4.3.2).
- `:272-278`, "The ordering this engine assumes of the integrator": the licence rises one
  clock after the arbiter grant while the MRPDU is still serializing onto the parent's egress;
  the declaration precedes the first stream frame only if the parent's egress does not let a
  licensed stream frame overtake a control frame already granted.
- Parent-visible list (`PR-BODY.md` section 4, the `srp_active_o` bullet): the same three
  statements. `docs/guides/integrator.md`'s `srp_active_o` row links section 6.2 and states no
  bound, so it is unchanged (the assignment places these statements in section 6.2 and the
  list).
- `make check` rc 0.

## Item 4: docs, per-application restart versus per-type aging

Commit `412efeb`, docs only (R399-1 S3), no RTL change, as assigned.

`docs/architecture/10_srp_engine.md:649-664` (section 6.5), "A peer that flags only some
types": the restart is per application, the aging per Attribute Type. A peer MSRP LeaveAll
flagging only some types restarts the whole MSRP timer (rLA! for the machine, 10.7.5.20 b)2)
and NOTE) but ages only the flagged types' registrars (10.8.2.6, the lane table). The
unflagged types' registrations are then aged only by the own LeaveAlls this participant still
sends: about every other cycle against a peer drawing from the same range, never against a
peer faster than the shortest draw. Such a peer departs from 10.7.5.20 as #106 applies it (the
NOTE: a LeaveAll "must generate a LeaveAll Attribute for each Attribute Type supported by the
application"); the engine does not compensate; an unflagged registration still ends at the
peer's Lv (Delta 13); the bench switch flags all four types. `make check` rc 0.

## Parent-visible list (for the pin-adoption lane; also `PR-BODY.md` section 4)

Changed in round 2 (items 1 and 3); the rest stands as round 1 wrote it.
1. No interface change: no port, parameter or register of `protocol_processor_top` or
   `KL_srp_top` changes in round 2 either (RTL change is internal to `KL_srp_top`'s cadence
   plane; the new wrapper port `arm_delay_i` is tb-only).
2. `srp_active_o` carries the Milan 4.3.2 term. Added wait only for a Ready registered before
   the VID's first MVRP MRPDU: at most one T-MRP-JOIN plus any wait for a TX slot or the TX
   arbiter; rises one clock after acceptance. A VLAN-table overflow (beyond four entries) holds
   the licence closed until the source is re-declared once an entry is free; visible only on
   `dbg_vlan_err_o`, not exported by the processor top. Ordering the parent must keep: the
   licence rises one clock after the arbiter grant while that MRPDU still serializes onto the
   parent's egress, so the egress must not let a licensed stream frame overtake a granted
   control frame.
3. Fewer own LeaveAlls: unchanged from round 1. Round 2's guard only removes the rare extra own
   LeaveAll that the queued arm port could let through (R399-1 S1).
4. Consumer gate to re-base: `tb/verilator/milan_dp` `obj_crflic` [C],
   `sim_crf_licence.cpp:953,956` `>= 4` -> `>= 3` (the declared edit; measured below at
   `412efeb`: with it 415/415 and 3 + 3 LeaveAlls, without it exactly those two checks fail).
5. Parent documents at adoption: `docs/traceability/ieee8021q.md` MRP-4/5/6/7,
   `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.2.7.1 and 4.2.7.3/4.4.1, and (round 2, R398-1
   F1) `tb/verilator/milan_dp/README.md` line 443 (the `[C]` count becomes the re-based bound)
   and lines 528-530 (the #108 limitation is now implemented).

## Gates

All at `412efeb750e358a65b04bae1cbb3086134d15b7e`, Verilator 5.050 (the manager's pinned
wrapper, byte-identical copy). Processor gates ran in a scratch export of the head made a
repository with read-only object alternates onto this lane's objects (so `nvm_port figures`
can read its pinned revisions; no clone, no checkout of the lane). Logs stay in scratch
(`$VALIDATION_STORAGE/c1-a443/{proc-logs,parent-logs,r398,r399}`), each row with size and SHA-256
(first 16 hex). Commands over ten minutes were started detached through the same one-command
runner and waited on in the foreground until they exited; nothing was left running.

### Processor entry points and suites

| Command | rc | s | Log bytes | Log SHA-256 | Result |
|---|---:|---:|---:|---|---|
| `./scripts/run_suites.sh` | 0 | 655.1 | 1,645 | `92d1023253110bb2` | 33 suites, 1,016,051 checks, 0 failing (srp_top 2200, srp_stream_fsms 1219, srp_encoder 581, pp_top 7751) |
| `./scripts/lint_hdl.sh` | 0 | 17.1 | 1,028 | `49e02975050b914d` | 40 modules, LINT OK each |
| `make check` | 0 | 40.4 | 225 | `85373785a2c97554` | |
| `python3 scripts/gen_matrix.py --check` | 0 | 0.0 | 33 | `98e5ebd5eedcc618` | |
| `./syn/yosys/run.sh` | 0 | 85.4 | 25,185 | `00aa33ca78c7aafc` | 35 tops + the Xilinx memory-map check |
| `make -C tb/nvm_port figures` | 0 | 297.3 | 3,609 | `ec80b86ffee73347` | |
| `make -C tb/srp_top mutants` | 0 | 1873.5 | 5,751 | `0d61ad6109d9553a` | 11 controls pass, 78/78 arms KILLED by their named assertions, coverage 65/65 (K12 L4 M12 N13 O8 P8 Q4 R4), `90 checks: 90 PASS`; per-arm lines identical to the chunked exploration run |
| `python3 tb/srp_admission/mutants.py --output <scratch>` | 0 | 776.6 | 479 | `6977d367d954c85c` | 12/12 |
| `python3 tb/pp_top/gsi_mutants.py --output <scratch> --verilator <pinned>` | 0 | 816.9 | 4,150 | `5f6d67707db7bfed` | 20 detected; golden and restored PASS |
| `python3 tb/pp_top/name_wr_mutant.py --output <scratch>` | 0 | 46.3 | 2,550 | `055560a7d55d359d` | decode killed; golden and restored PASS |
| `python3 tb/acmp_talker/retry_mutants.py --logs <scratch>` | 0 | 438.0 | 3,865 | `7bda8adf83703e45` | 62 killed, 7 equivalence, 1 performance |
| `git diff --check c951a9ff..412efeb` / `81b8d6d..412efeb` | 0 / 0 | | 0 / 0 | | |

### Mutants of this round (srp_top campaign, named assertion first)

| Arm | Group | Failing checks | Tags |
|---|---|---:|---|
| `rearm-at-issue` | armdelay | 8 | P8 |
| `r-rearm-no-inflight` | peer / restart | 3 / 6 | M10 / P6 |
| `r-rearm-no-deadline` | peer / armdelay | 3 / 8 | M10 / P8 |
| `r-flag-ignores-edge-peer` | restart | 1 | P7 |
| `draw-kind-0` (regenerated) | timers | 6 | Q1-Q4 |

### The reviewers' round-1 probes at `412efeb` (their scripts and patches, unmodified)

| Probe | Result | Log SHA-256 |
|---|---|---|
| R399-1 `probe_arm_race.py`, arm delay 0 / 2 / 3 / 4 / 8 / 16 | 0 of 83 offsets send an own MSRP LeaveAll at every delay; `1 checks: 1 PASS` each (at `81b8d6d`, per R399-1's receipts: 0 / 0 / 4 / 4 / 7 / 15; its REPORT table prints 5 and 5 for delays 8 and 16, but its receipt files list 7 and 15 offsets, and `rearm-at-issue` reproduces the receipts offset for offset) | `167fec4976de3ec9` / `fe7127065f798ed8` / `48f87d93db88a260` / `2907bab6d335adde` / `c90f39831a9c3ec6` / `7ad59fab4a87fd46` |
| R399-1 `probe_licence.py` | 8/8; S0 200, S3 0, S4 142/150, S5 closed then 0, S6 held, S7 -1 / -1 / 149 ms after re-declaration: identical to the R399-1 receipt | `ddbe63007697fe4d` |
| R398-1 `rvw-probes.patch` (V1, V2) | PASS 4/4; `RVW` lines identical to the R398-1 receipt (V1 rise 24047 after New accept 24046; V2 `vids=0xf vlan_err=1 ... active=0`, after free `vids=0xe active=0`) | `c3a02c9772c1716c` |
| R398-1 `rvw-sent-survives-removal` + probes | KILLED by V1 | (summary `4b47c98f80d733c5`) |
| R398-1 mutants, full srp_top | `rvw-licence-any-vid` R3, `rvw-mvrp-restarts-msrp` M4/P2/P3/P8, `rvw-msrp-restart-domain-only` P3, `rvw-flag-rides-empty-drain` P5, `rvw-flag-ignores-edge-peer` P7 (was a survivor): KILLED. `rvw-sent-on-any-mvrp-tx` and `rvw-sent-survives-removal` survive srp_top as at `81b8d6d` and are KILLED at unit level (srp_encoder W3, W4; summary `747037dca5ce4c41`), as R398-1 recorded. `rvw-rearm-no-cadpend` and `rvw-rearm-no-inflight` no longer apply (their context is the replaced guard); their re-based in-tree arms are `r-rearm-no-deadline` and `r-rearm-no-inflight` above | (summary `4b47c98f80d733c5`) |

### Parent consumer gates

Scratch parent: export of the trusted checkout at `57b8c867` (965 tracked files), made a
repository with object alternates onto the trusted checkout; submodules exported at their pins
(`external` efeb541a, `gptp-processor` 5dce647a, `third_party/verilog-axis` 48ff7a7e, from
the previous author's read-only source repos) and `protocol-processor` at `412efeb`, each made a
repository the same way; `git submodule init` (config only); the gitlink set to `412efeb` and
the declared edit (`parent-declared-edit.diff`, sha256 `fce36b70...eb14ed5`,
`sim_crf_licence.cpp:953,956` `>= 4` -> `>= 3`) applied and committed locally in the scratch
repository only. `git submodule status` showed all four at their pins before and after. The
sixteen commands are the manager's (`results.json`), in its order and environment shape.

| # | Command | rc | s | Log bytes | Log SHA-256 | Note |
|---:|---|---:|---:|---:|---|---|
| 01 | `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | 315 | `3673d5b75f37a526` | every ratchet 0 <= 0 with the new srp_top test code |
| 02 | `python3 scripts/check_py_idiom.py` | 0 | 3.4 | 461 | `6019866e401625dd` | |
| 03 | `python3 scripts/xvlog_gate.py --check` | 0 | 181.8 | 1,320 | `d54be51307b08b8d` | 4 findings == ratchet, none in `KL_srp_top.sv` |
| 04 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.4 | 390 | `1dd83081ba29241f` | |
| 05 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | 955 | `fb4b6d8cc0ca4895` | |
| 06 | `python3 sw/builder/test_builder.py` | 0 | 945.4 | 98,932 | `9a9e58439feedf82` | |
| 07 | `make -C tb/verilator/pp_shadow -j8` | 0 | 43.4 | 320,826 | `2efb86cf2b193834` | 635 checks, 0 failures |
| 08 | `python3 scripts/check_port_contracts.py` | 0 | 2.3 | 421 | `a8731f105748ccdd` | |
| 09 | `python3 scripts/measure_naming.py --check` | 0 | 0.4 | 36,572 | `bee3051c403aa565` | |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | 5.6 | 11,253 | `02b91ce2d5607aa9` | |
| 11 | `python3 scripts/docs_check.py` | 0 | 4.5 | 127 | `10b05553129a85c2` | |
| 12 | `python3 scripts/lint_rtl.py --check` | 0 | 5.7 | 14,186 | `100ecae619de3a93` | 90 <= ratchet 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | 0.3 | 29,629 | `07c9c2d3586875f7` | no PINMISSING |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 27.5 | 388 | `6f5db23b3286c9be` | 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | 0 | 1414.7 | 2,078,648 | `fc88a0c98d2f17e8` | every leg passes; `obj_crflic` 415/415, `[C]` 3 DUT and 3 switch LeaveAll MRPDUs |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 306.1 | 169,090 | `af0f185ff5669b17` | 65/65, 152/152, leg defects 5/5 |

16/16 rc 0 with the declared edit. Attribution, same scratch parent with only the declared edit
reversed (restored afterwards): `make -C tb/verilator/milan_dp crflic
CRFLIC_MDIR=obj_crflic_noedit` rc 2 in 60.5 s (log `3de51a39538ded16`): 2 of 415 fail, exactly
"the DUT sent >= 4 LeaveAll MRPDUs" and "the switch sent >= 4 of its own", with 3 and 3
counted. So at this head, as at `81b8d6d` (the manager's 15/16), the one parent expectation to
re-base is the declared one.

## What remains

- Hosted checks at the new head, the review deltas ([R398], [R399]) and the pin adoption
  (the declared crflic edit and the parent documents above) belong to the manager.
- The arm-port queue in the processor top drops the newest arm on overrun (counted, never
  silent). A dropped cadence arm would stop that cadence slot; this is pre-existing, common to
  every cadence slot, and not changed here. With the new guard a dropped LeaveAll re-arm leaves
  that timer idle until the next received LeaveAll or reset, where the old guard would have
  let the superseded deadline act (one own LeaveAll, then a fresh draw). Not in this
  assignment's scope; a possible follow-up is to re-issue the intended deadline when a stale
  expiry arrives with no draw outstanding (harmless when the arm is only late, restoring it
  when it was dropped).
- Carried from round 1: no hardware; the re-DECLARE_TALKER VLAN refcount leak needs its own
  issue; an MVRP drain has no LeaveAll-only form.
- The new guard costs two 32-bit subtractions in `KL_srp_top` (the sign of `now_ms - deadline`
  per LeaveAll slot); `KL_srp_top` is not among the Yosys tops, so no figure is measured.

## Scratch (outside this directory, not in the tree)

`$VALIDATION_STORAGE/c1-a443`: the gate runner `gate.py`, `launch.sh`, `snap.sh`, `mkrepo.sh`,
`run_mut.sh`, `gen/gen_patches.py` (the textual edits behind the new and regenerated patches),
the processor gate tree `proc`, the scratch parent `parent`, logs, the chunked campaign
`camp1`, and the probe reproductions `r398`, `r399`.
