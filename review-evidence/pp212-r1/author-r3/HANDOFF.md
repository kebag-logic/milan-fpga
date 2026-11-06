# [A729c] HANDOFF — processor issue #212, round 3 (PR #213)

**Status: REVIEW READY at `834cc88`.** Every gate below ran on a clean clone of this head,
and every one is rc 0. Every round-3 item of the assignment is resolved (below). One process
breach is recorded under Process notes: the unit's memory peaked at 10.75 GB, against the
10 GB working limit; the 12 GB cap held.

- Repository: the processor repository, branch `212-srp-presettle-talker`. Before the first
  round-3 commit, `git remote get-url origin` was the processor repository and HEAD was the
  round-2 head `a2fce43`.
- Base: processor main `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`.
- Round-2 head: `a2fce4326ebdaf398a1920d79a664d44e6f1e5dd`.
- **Round-3 head: `834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1`** (tree `93bea04f`). Six commits on
  top of `a2fce43`, which is an ancestor of the head (no rebase, no force). One-line
  subjects, no body, no trailer.
- Assignment: the [A10] round 3 assignment on #212 (issuecomment-6670001706), and the delta
  reviews R769-2 (PR #213 issuecomment-6669161852) and R770-2 (PR #213
  issuecomment-6669995272).
- Posts on #212: TAKEN (issuecomment-6670031272); REVIEW READY with the head (issuecomment-6674582254).
- Receipts: `receipts/`, with an `INDEX.md` in every directory, generated from the files
  present. Host paths in the copies are replaced by placeholders. A file over 200 KB is
  recorded by size and sha256 in its directory's `RAW-RECORDS.txt`.
- STOP check: no top-level port, parameter or register-map change. The round-3 diff touches
  `hdl/srp/KL_srp_listener_fsm.sv` only among RTL files; `hdl/top/` and `KL_srp_top.sv` are
  unchanged from round 2. The STOP condition was not met.

## Round-3 design and clauses

**R769-2 F1 = R770-2 F1, option (a) (the ruling).** LINK_DOWN (Flush!) and LINK_UP (Begin!)
take every sink registrar to MT, settled sinks included.

- Clause: IEEE 802.1Q-2022 Table 10-4. Begin! goes to MT from IN, LV and MT. Flush! goes
  to MT from IN and LV with an **Lv** indication, and from MT to MT. leavetimer! goes from
  LV to MT, also with Lv. §10.7.5.1 defines Begin! (the machine is initialized again) and
  §10.7.5.2 Flush! (rapid deregistration).
- Publication (the ruling: "as a leavetimer!'s is"). The withdrawal of a settled sink at a
  link change takes the leavetimer!'s path, because Flush! carries the same Lv:
  - `EVT_TK_UNREGISTERED`;
  - `tk_reg_state` NONE;
  - the declaration-withdrawal request (`ind_unreg_w`), so the applicant takes Lv! and the
    next tx! sends the Lv;
  - an LV registrar's leave slot cancelled.

  An unbound sink's strobe stays masked (F10.5, round 2).
- The two edges are treated alike. LINK_UP after LINK_DOWN finds every registrar MT, so it
  raises nothing. A registrar that is registered at LINK_UP holds a value received while the
  link was down, which a decoder still draining frames can deliver. Begin! ends that
  registration too. It is published the same way, so `tk_reg_state` never changes without
  its strobe.
- Priority: the link change is the first branch of the sink registrar's events, as it
  already was for the port registrars (`pt_next`). A decoder value on the link's own clock
  registers nothing, and requests nothing (`ind_reg_w` carries `!link_ev_w`).
- Milan v1.2 §5.3.8.5: a settled Stream Input declares Listener Ready while a matching
  Talker Advertise "is being received". After an outage nothing is being received until
  the talker declares again, so withdrawing is the required state. Ready returns on the
  talker's next declaration (PS24).
- No new state. The round-2 `link_ev_w && !armed_r[s]` block is replaced by the first
  branch of the chain: the same flip-flops, a few terms per sink.
- Registrar timing is unchanged (Milan v1.2 §4.2.7.2.2, Table 4.3): Δ13, `T-MRP-LEAVE` and
  the LeaveAll cycle are untouched (PS7, PS8, PS9, PS19 unchanged and green).
- Not done: a LeaveAll to force a re-declaration (unchanged, 10 §6.4 "Why no LeaveAll").

**"Before and after the old Lv" under (a).** At round 2 the Lv owed at the re-bind was the
A8's. Under (a) the declaration is withdrawn at the link change, so the owed Lv is that
withdrawal's. "Before" means the A8 and A15 come before that Lv goes out. "After" means a
tx! between the A8 and the A15 sends it. In both runs PS24 requires nothing to be applied,
and the tx!s to send only the owed Lv.

**R770-2 S2 (retire the limit).** The limit "a settled sink across a link change" is removed
from 10 §6.4, the integrator guide and the PR limits.

**R770-2 S1.** PS20's Talker Failed case now runs before tx! and after the old Lv went out.

**R769-2 S1.** The comment at `KL_srp_listener_fsm.sv:501` reads "(13 at the default
T-MRP-LEAVE)". It now states that the width stays 13 bits across F08.1's 4500-7500 ms range
(`$clog2(4501)` = `$clog2(7501)` = 13; `PT_SLACK_C` 3691 to 691, so the wrap-safe compare
holds across the range).

**Residue.**
- R769-2 R1: the PR body's SRP-campaign split, in the reviewer's form (PR-BODY Round 3 and
  Validation).
- R769-2 R2 = R770-2 R1, `10_srp_engine.md:226` and `:782`. The two reviewers' exact texts
  differ in wording. I applied R769-2 R2's, because:
  - the assignment lists it first;
  - its `:782` text cites F08.1, as R770-2's does;
  - it matches the RTL comment wording the assignment gives.

  R770-2 R1's text would read "at the F08.1 `T-MRP-LEAVE`" in both places.

## Changes (file:line at the head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/srp/KL_srp_listener_fsm.sv:38` | banner: every sink registrar, settled or not, takes the link change; the withdrawal published as a leavetimer!'s | 802.1Q-2022 Table 10-4 |
| 2 | `hdl/srp/KL_srp_listener_fsm.sv:165` | `link_up_i` port note: for every Talker registrar | Table 10-4 |
| 3 | `hdl/srp/KL_srp_listener_fsm.sv:500` | the deadline width: 13 at the default T-MRP-LEAVE, 13 across F08.1's 4500-7500 ms | Milan v1.2 Table 4.3; F08.1 (R769-2 S1) |
| 4 | `hdl/srp/KL_srp_listener_fsm.sv:511` | `link_q_r` note | Table 10-4 |
| 5 | `hdl/srp/KL_srp_listener_fsm.sv:579`, `:584`, `:592` (`reg_ind`) | no declaration request on the link's clock; the link change's withdrawal request for a registered sink | Table 10-4 Flush! (Lv); Milan v1.2 §5.3.8.5 |
| 6 | `hdl/srp/KL_srp_listener_fsm.sv:1434` (`reg_plane`) | the link change first among the sink registrar's events, every sink: MT, an LV slot cancelled, EVT_TK_UNREGISTERED when it was registered (masked for an unbound sink, `:1495`); the round-2 unbound-only block removed | Table 10-4 Begin!, Flush! |
| 7 | `tb/srp_stream_fsms/sim_main.cpp:3221` | PS20: the Talker Failed same-stream re-bind before tx! and after the old Lv | R770-2 S1; acceptance 2 |
| 8 | `tb/srp_stream_fsms/sim_main.cpp:3420` (declared `:494`, run `:3584`) | PS24 (11 checks) | R769-2 F1 = R770-2 F1; acceptance 3 |
| 9 | `tb/srp_top/mutants.py:357`, `:464`; `tb/srp_top/mutations/` | five arms under PS24; coverage PS1-PS24; seven patches cut again (below) | acceptance 5 |
| 10 | `docs/architecture/10_srp_engine.md:51` (§2 Consumes), `:227` and `:783` (R769-2 R2, the reviewer's text), `:270` (measured cost of this head), `:620`, `:621` (F10.5 arcs), `:830` (the same-stream re-bind), `:833` (§6.4 "A link change", the limit retired), `:858` (PS1 to PS24) | the settled sink at a link change | Table 10-4; Milan v1.2 §5.3.8.5 |
| 11 | `docs/guides/integrator.md:630` | a link change ends a settled input's registration too, reported as a time-out (the limit retired) | R770-2 S2 |
| 12 | `docs/architecture/02_interfaces.md:300` (§4.1), `:540` (event catalog), `:568` (F02.10) | TK_ATTR_UNREGISTERED at a link change; the listener registrars consume LINK_UP/DOWN | — |
| 13 | `tb/srp_stream_fsms/README.md`, `tb/srp_top/README.md` | PS20, PS24, the new arms, the moved counts, the re-cut patches | — |

## New checks (planted arm, failing words, count)

Every PS24 check is in `tb/srp_stream_fsms` section PS. The counts are from the SRP campaign
at the head (failing checks in the suite run).

| Check (failing words) | What it requires | Planted arm | Failing checks |
|---|---|---|---:|
| `PS24: a sink settled through a link change` (four runs: the port table full or not, before and after the old Lv) | settled, registered, link down and up, A8, A15 on the same triple: no EVT_TK_REGISTERED or latency strobe, NONE, MT, no timer op, nothing declared, the two tx!s send only the owed Lv | `settled-link-flush-dropped`: round 2's exception back (no link input for a settled sink's registrar) | 11 (every PS24 check) |
| `PS24: sink 0 settled and registered` (four runs) | the publication at the link change: one EVT_TK_UNREGISTERED at LINK_DOWN, NONE, MT, the declaration withdrawn, no timer op; nothing more at LINK_UP | `settled-link-unpublished`: no EVT_TK_UNREGISTERED at the link change | 5 |
| the same | the same | `link-withdraw-dropped`: the declaration not withdrawn at the link change | 6 |
| `PS24: sink 0 settled on a Talker Advertise a LeaveAll ages` | LV at LINK_DOWN: Lv, MT, the declaration withdrawn, the leave slot cancelled | `settled-link-keeps-lv-slot`: the slot left armed | 1 |
| `PS24: a Talker Advertise on the clock the link goes down` | a settled sink registers and declares nothing for a value on the link's own clock | `link-clock-indicates`: that value requests the declaration | 1 |
| `PS24: after the link returns` | the talker's next declaration registers the settled sink again: EVT_TK_REGISTERED, ADVERTISE, New Ready | (a recovery check, failed by `settled-link-flush-dropped` and `link-withdraw-dropped`) | — |
| `PS20: every port registrar held by other values, sink 0 registered on a Talker Failed, unbind and bind again after its Lv went out` | FAILED with its FailureInformation and latency at the settle; the next tx! sends New Asking Failed | `keep-declares-seed-type` (both PS20 Failed checks now) | 2 |

PS24 is the reviewers' sequence (R769-2 P1, R770-2 XP2) as a row. Both reviewers' probes
at the head are under `receipts/probes/`:
- R770-2's XP1 to XP6 pass, 1,605 of 1,605. XP2 reads `reg 0 tk 0 state 0`.
- R769-2's block: 1,551 checks, 1 FAIL.
  - P8 now reads `tk 0 state 0 unreg 1`.
  - P1 after the old Lv passes.
  - P1 before it fails only its `nothing_applied()` "no push" clause. `p1-words` prints what
    that clause sees: the settle `reg 0 tk 0 state 0 ops 0`, and on the next tx! the one push
    `5/2@0001`, the owed Lv (Ready) of the link-down withdrawal, then `decl 0`. Under (a) that
    Lv is the publication the ruling asks for. PS24 requires exactly it.

**Patches cut again** (`git apply --check` refused the old context). Each is diff -u of the
same edit, unless noted:
- `link-begin-dropped`, `unarmed-indicates`, `unarmed-latency-strobe`, `unarmed-unregistered`
  (issue #212) and `lv-expiry-masked` (issue #134; its talker section is unchanged).
- Two edits follow the link branch:
  - `r-sink-receive-priority-lost`: the LeaveAll ahead of a reception, now after the link
    change. On every clock without a link change it is the same mutation.
  - `unarmed-link-flush-dropped`: the branch now serves every sink, and the arm keeps it from
    the unbound ones (`link_ev_w && armed_r[s]`). It is still killed by `PS23: sink 0
    unbound`.

**Counts that moved** (SRP campaign at the head against round 2's receipt, label for label;
README cells re-recorded):
- `presettle-removed` 36→37;
- `seed-no-registered-strobe` 25→26;
- `rebind-same-not-kept` 4→5;
- `keep-declares-seed-type` 1→2;
- `pt-link-flush-dropped` 4→6, which now also fails PS24's runs where the port registrar holds
  the value;
- `listener-settle-compare-dropped` 44→45;
- `listener-teardown-keeps-declaring` 83→84;
- `listener-reprobe-abandons-leave` 1→3, PS24. It has no recorded count.

Every other entry is the same, count and tags.

## Area (the processor's yosys flow: sv2v, yosys 0.66 `synth_xilinx -family xc7 -flatten`)

| `KL_srp_top` | main `a9e84b66` | round 2 `a2fce43` | round 3 `834cc88` | round 3 − round 2 | round 3 − main |
|---|---|---|---|---|---|
| 2x2 (shipping) LUT / INV / FF | 11,475 / 2,811 / 4,812 | 13,193 / 2,875 / 5,334 | 13,030 / 2,981 / 5,334 | −163 / +106 / 0 | +1,555 / +170 / +522 |
| 8x8 LUT / INV / FF | 23,046 / 3,483 / 9,236 | 28,193 / 4,037 / 11,224 | 28,480 / 4,194 / 11,224 | +287 / +157 / 0 | +5,434 / +711 / +1,988 |

- RAM is unchanged at both shapes (114 and 179 cells).
- The round-2 head was measured again here with the same flow. Its four stat files are
  byte-identical to round 2's published ones.
- The flip-flops are exactly unchanged, as designed: no new state.
- The LUT figures move within the flow's documented noise: up to about 300 at 2x2 for an
  edit of a few LUT. The listener alone at N = 2 reads +584 LUT and at N = 8 −44 for the same
  edit, so the LUT delta is not resolved by this flow. The true change is a few terms per
  sink.
- For the manager: at the shipping 2x2 shape the yosys LUT figure fell by 163 and FF did not
  change against round 2. Round 2's route duty stands.

## Processor gate table (clean clone of `834cc88`)

Five clones (`c1` to `c5`) of the committed head. At each clone, HEAD, the tree
(`93bea04f`) and an empty `git status --porcelain --ignored` were checked before its first
gate. The receipts are `receipts/processor/head-834cc88/` and
`receipts/campaigns/*-834cc88/`.

| Gate | Result |
|---|---|
| `make check` | rc 0 |
| `bash scripts/lint_hdl.sh`, under Verilator 5.052 and the pinned 5.050 | rc 0 both, 41 modules LINT OK each |
| `./syn/yosys/run.sh` | rc 0, 42 tops |
| `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0, 93 of 93 |
| `bash scripts/run_suites.sh` (pinned 5.050, `MAKEFLAGS=-j16`, `REQ_TAG_LOG`) | rc 0: **1,031,005 checks, 0 failing**, 36 suites. pp_top 11,064, srp_stream_fsms 1,512 (round 2: 1,500), srp_top 8,671. Every other suite's count equals round 2's |
| `python3 scripts/check-req-tags.py --suites ... --evidence ...` | rc 0: 266 evidence lines, 14 suites |
| SRP campaign `tb/srp_top/mutants.py --jobs 4` | rc 0: **280 of 280** (19 controls, 260 arm entries and the coverage check), coverage 167 of 167. Every count equals the README cells: 51 rows of the issue #212 table checked, 0 mismatches |
| ACMP `tb/pp_top/acmp_mutants.py --jobs 3` | rc 0: 103 of 103 KILLED by their named checks, goldens PASS |
| AECP `aecp_mutants.py --jobs 3` | rc 0: 67 checks, 67 PASS |
| GSI `gsi_mutants.py --jobs 3` | rc 0: 30 detected by named checks, golden and restored PASS |
| CTR `ctr_mutants.py --jobs 3` | rc 0: 18 checks, 18 PASS |
| name write `name_wr_mutant.py` | rc 0: decode killed, golden and restored PASS |
| AECP dispatch `aecp_dispatch_mutants.py --jobs 3` | rc 0: 105 checks, 105 PASS |
| notification `notify_mutants.py --jobs 3` | rc 0: 137 of 137 KILLED by their named checks, goldens PASS |
| D3 `d3_mutants.py --jobs 3` | rc 0: 110 of 110 KILLED by their named checks, goldens PASS |
| Area, 2x2 and 8x8 | above (`receipts/area/`) |

The eight campaigns outside SRP ran with the pinned Verilator 5.050, its C++ build capped at
`-j2`, or `-j1` while the governor held it. Each one's result lines equal round 2's receipt,
label for label: ACMP 111, AECP 67, GSI 32, CTR 18, name write 3, AECP dispatch 105,
notification 152 and D3 116 (`vs-round2.txt` in each campaign directory, by
`tools/armcmp.py`). The SRP campaign differs from round 2 only in the five new arms and the
eight moved counts above (`campaigns/srp-834cc88/srp-vs-round2.txt`).

## Scratch-parent consumer gate table (pin `834cc88`)

The scratch parent is the round-1 and round-2 one:
milan-fpga dev `604899c0`, local branch `pp212-consumer-gate`, push URL
`DISABLED-never-push`, never pushed. It has two new local commits:
- `719a461a`: protocol-processor → `834cc88`;
- `92385027`: its ROM digests through `./syn/yosys/ooc.sh --record-rom-digests`, equal to
  main's (ltn `23cc67ee…`, ucode `49a993be…`).

A top-level identity check preceded every git command inside `protocol-processor`. The
tools are the parent's CI pins: Verilator 5.050, yosys 0.66, sv2v v0.0.12, GoogleTest
1.14.0 on the system include path, and a CPython 3.12.3 venv. The venv holds
`ci/constraints-ci.txt` and, as CI's firmware-boundary job installs it,
`sw/litex/litex_pins.txt` (`receipts/records/`).

| Consumer gate (rtl-fast job) | Result |
|---|---|
| ROM digests (`./syn/yosys/ooc.sh --record-rom-digests`) | rc 0; both rows equal main's |
| changes (`ci_scope.py --selftest`; classify from `604899c0`) | rc 0, rc 0 |
| verilator-lint (`lint_rtl.py --check --self-test`; `pp_srcs.py --check --selftest`) | rc 0: 89 ≤ ratchet 89; rc 0 |
| bdd-conformance (`behave`) | rc 0: 14 features, 508 scenarios, 2,330 steps passed |
| yosys-elaboration (elaborate `milan_datapath`, `KL_pp_shadow`, `KL_gptp_shadow`; OOC read sets; `ooc_selftest`; `guard_selftest`; `cache_selftest`) | rc 0 each |
| publication-census | rc 0 |
| firmware-unit (tally and rv32 self-tests; `test_ctrl_firmware.py --shard 0/4`; `test_ctrl_nvm.py`; `fw_coverage.py --selftest`, `--check`) | rc 0 each |
| firmware-control mutants (`--shard 1/4`) | rc 0: 523 of 523 caught |
| firmware-aecp mutants (`--shard 2/4`) | rc 0: 78 `[ok]`, PASS |
| firmware-srp mutants (`--shard 3/4`) | rc 0: 280 `[ok]`, PASS |
| firmware-boundary (`ctrl_boundary.py --selftest --without verilator`) | rc 0: PASS, 0 findings (the second run; see Process notes) |
| firmware-verilator (`ctrl_boundary.py --selftest --only verilator`) | rc 0: PASS, 0 findings |
| milan_dp (`make -C tb/verilator/milan_dp SIM_JOBS=2`) | rc 0: 12,075 `[ok]`, 1,301 `[PASS]`, 0 `[FAIL]` (round 2: the same counts) |

Receipts: `parent/pin-834cc88/`. Two logs are over 200 KB, `behave.log` and `milan_dp.log`.
Each is recorded with its size and sha256 in `RAW-RECORDS.txt`, beside a generated summary.

## Process notes

- The full processor sweep is `scripts/run_suites.sh`, which has no shard option.
  `native-shards.py` shards the parent's `run_all_suites.sh` only, and at the start
  `cpu_ranges.py pick` found no free range ("free16 [] free12 []"). So the sweep runs whole
  in this unit, on its own CPUs 96-111, as in round 2.
- The parent's CI venv of round 1 no longer existed, so I made a new CPython 3.12.3 venv of
  `ci/constraints-ci.txt` in scratch.
  - Its first firmware-boundary run was refused by the gate itself:
    `sw/litex/test_ctrl_memory.py` exited 1 with "No module named 'migen'". That is the
    environment, not the head. CI's firmware-boundary job also installs
    `sw/litex/litex_pins.txt`, which my venv lacked.
  - I installed it as CI does (`pip install pyyaml -r sw/litex/litex_pins.txt` with
    `PIP_CONSTRAINT` set to the CI constraints) and ran the gate again from the start: rc 0,
    PASS.
  - The refused run is kept in `receipts/superseded/fw-boundary-venv-without-litex/`. No other
    rtl-fast job installs those pins, and every other parent gate passed in the first venv.
- A chained command that failed at its first step left a fresh clone of the round-2 head
  inside the lane's working tree, as an untracked directory. I moved it to scratch at
  once, checking its top-level first. The lane was clean before the first commit.
- **Memory: the 10 GB working limit was exceeded once.** The unit's `memory.peak` reads
  10.75 GB, under the 12 GB cap. The governor sampled 10.74 GB at 00:13:54 and 00:14:06, and
  10.14 GB at 00:14:57.
  - Cause: the sweep's `make -j16` compile of `tb/pp_top`, the parent's publication census
    (four `sv2v` runs of `milan_datapath` at about 1 GB each), three campaign chains and the
    parent's milan_dp build overlapped.
  - The governor was running: `tools/memgov.sh`, `memory.reclaim` above 8.5 GB, campaign
    Verilator builds at -j2, or -j1 above 7.5 GB anonymous. Reclaiming page cache cannot
    shed anonymous memory.
  - From 00:20 the governor ran tighter: reclaim above 8.0 GB, -j1 above 6.5 GB anonymous.
    No chain was added until the sweep and the census had ended. No gate failed or was
    stopped by it (`receipts/records/memgov.log`).

## Not done (by the assignment's rules)

No push, no PR creation or edit, no merge or rebase, no comment edits, no hardware or bench
access, no Vivado run, no sub-agents.
