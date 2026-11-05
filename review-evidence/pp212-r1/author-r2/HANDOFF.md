# [A729b] HANDOFF — processor issue #212, round 2 (PR #213)

**Status: REVIEW READY at `a2fce43`.** Every gate below is rc 0. A host reset at 13:10 stopped
four gates mid-run. They were run again from the beginning, from 17:42, on the same clean clones
(see Process notes).

- Repository: the processor repository, branch `212-srp-presettle-talker`. Before the first
  round-2 commit, `git remote get-url origin` was the processor repository and HEAD was the
  round-1 head.
- Base: processor main `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`.
- Round-1 head: `04856e48619866e08ccaf5ffc34cf1636d8c5b74`.
- **Round-2 head: `a2fce4326ebdaf398a1920d79a664d44e6f1e5dd`** (tree `40d4bfd5`). Six commits on
  top of the round-1 head; it is an ancestor of the head (no rebase, no force). One-line
  subjects, no body, no trailer (`receipts/records/processor-records.txt`).
- Every gate below ran on a clean clone of this exact head (HEAD, tree and an empty
  `git status --ignored` checked at the clone).
- Posts on #212: TAKEN (issuecomment-6654229877); REVIEW READY with the head (issuecomment-6667806908).
- Receipts: `receipts/`, with an `INDEX.md` in every directory. Each index is generated from
  the files present by `receipts/tools/receipt.py index`. Host paths in the copies are
  replaced by placeholders. A file over 200 KB is recorded by size and sha256 in its
  directory's `RAW-RECORDS.txt`.
- STOP check: no top-level file changed (`hdl/top/` empty in the records' diff), no register
  map, and `KL_srp_top`'s port list is byte-identical to main's. `KL_srp_listener_fsm` gains
  one internal input, `link_up_i`, fed from `KL_srp_top`'s existing `link_up_i` (the
  ruling's construction). The STOP condition was not met.

## Round-2 design and clauses

1. **R769-1 F1, option (a): a re-bind to the same stream keeps its registration.**
   - An A8 now only disarms the matcher. The sink registrar keeps running Table 10-4 on its
     record's {stream_id, DA, VLAN} until the sink's next A15, with Δ13, the LeaveAll lanes
     and its own leave slot. An A15 on the same triple keeps that state, whatever the port
     table holds.
   - Clauses: 802.1Q-2022 §10.7 and §10.7.8 (a registrar's state does not depend on when the
     application became interested); Milan v1.2 §5.3.8.9 (the exact triple); Milan v1.2
     §5.3.8.5 and §5.5.3.5.18 step 4 (declare at once).
   - While unbound, the sink raises and publishes nothing. There is no declaration request
     and no class-C strobe (F10.5's teardown edges carry none). `tk_reg_state` reads NONE,
     `acc_latency` 0 (a raw top-level output, kept at 0 as before) and the debug registrar MT.
     The FailureInformation bridge is ungated by contract, and its only consumer
     (GET_STREAM_INFO) gates it on FAILED.
   - A withdrawal while unbound follows Table 10-4 (rLv Δ13, LeaveAll then leavetimer!), so
     it is not applied at the re-bind (acceptance 3). The registration is not kept when its
     leavetimer! or a link change ends it on the settle's clock.
   - The construction is the ruling's cheapest: no new state, and one {DA, VLAN} comparator
     per sink beside the existing stream_id compare (`cset_w`).
2. **R770-1 F4: Flush!/Begin!.**
   - `KL_srp_top`'s `link_up_i` feeds the listener. Its fall is LINK_DOWN (Flush!) and its
     rise LINK_UP (Begin!), the same edges the Domain FSM takes (`KL_srp_domain`
     `link_q_r`, which yosys merges with the listener's).
   - Both take every port registrar, and the registrar of every sink not settled, to MT
     (802.1Q-2022 Table 10-4: Begin! goes to MT from every state, Flush! from IN and LV).
   - A settled sink's registrar keeps the behaviour that predates issue #212 (no link input),
     which R770-1 named as such.
3. **R769-1 S2 / R770-1 S1: the 13-bit deadline, taken because it measured smaller.**
   - The port registrars keep their leave deadline in `$clog2(LEAVE_MS_P + 1)` bits: 13 at
     5000 ms (F08.1 T-MRP-LEAVE, Milan v1.2 Table 4.3 LeaveTime).
   - An LV entry is compared on every clock and `now_ms_i` steps by one, so its modular age
     runs from −T-MRP-LEAVE to 0, the expiry.
   - A seeded LV arm's absolute deadline is now plus the remaining time. Registrar timing is
     unchanged: PS7, PS8, PS9 and PS19 grade it.
   - Figures are under Area below.
4. **R769-1 S3: guard kept, §6.4 corrected.**
   - The arm path's latency is not visible to the listener: `KL_srp_top` itself notes that
     the processor top queues the arm behind other faces.
   - An exact guard would need one of two things. Per sink, the intended deadline, as
     `KL_srp_top` keeps `cad_dl_r` for its LeaveAll slots: 13 to 32 flip-flops and a
     comparator per sink. Or an applied indication from the timer service through the
     processor top.
   - Either is more than a few LUT, so the guard stays, and §6.4 now says what it covers and
     what it does not.
5. **Acceptance 5's "mutant that removes the pre-settle path".** With item 1, a re-bind to
   the same stream (PS3) is served by both the kept registration and the seed.
   - `pt-seed-dropped` now names PS5, a re-bind to another stream that only the seed serves.
   - The new `presettle-removed` arm names PS3. It removes the seed, the kept registration
     and the one-walk declaration: the behaviour before the issue.

## Changes (file:line at the head, clause)

| # | File:line | Change | Clause |
|---|---|---|---|
| 1 | `hdl/srp/KL_srp_listener_fsm.sv:34` | banner: the kept registration, the link change | 802.1Q-2022 §10.7, §10.7.8, Table 10-4 |
| 2 | `hdl/srp/KL_srp_listener_fsm.sv:166`, `:513`, `:1534` | `link_up_i`, `link_q_r`, `link_ev_w` (fall LINK_DOWN Flush!, rise LINK_UP Begin!) | Table 10-4 Begin!, Flush! |
| 3 | `hdl/srp/KL_srp_listener_fsm.sv:537` | the sink registrar matches on its record (`rec_valid_r`), through an A8 | §10.7, §10.7.8 |
| 4 | `hdl/srp/KL_srp_listener_fsm.sv:572`, `:615` | no declaration request and no failure-change strobe while unbound | F10.5 (teardown edges carry no event) |
| 5 | `hdl/srp/KL_srp_listener_fsm.sv:500`, `:684`, `:708`, `:742`, `:1518` | the 13-bit leave deadline, its wrap-safe expiry, the seeded arm's rebuilt absolute deadline | Milan v1.2 Table 4.3; F08.1 |
| 6 | `hdl/srp/KL_srp_listener_fsm.sv:698` | the port registrars to MT on a link change | Table 10-4 |
| 7 | `hdl/srp/KL_srp_listener_fsm.sv:868` (`settle_keep`) | `kset_w` (the record's exact triple), `kexp_w`, `keep_v_w` | §10.7.8; Milan v1.2 §5.3.8.9 |
| 8 | `hdl/srp/KL_srp_listener_fsm.sv:1197` | a keeping settle requests the declaration at once, of the kept type | Milan v1.2 §5.3.8.5, §5.5.3.5.18 step 4 |
| 9 | `hdl/srp/KL_srp_listener_fsm.sv:1464`, `:1476`, `:1484`, `:1498` | the A15's fresh start only off the kept triple; no unregistration or latency strobe while unbound; the unbound registrar to MT on a link change; the keep's EVT_TK_REGISTERED and latency strobe | F10.5; Table 10-4 |
| 10 | `hdl/srp/KL_srp_listener_fsm.sv:1642`, `:1646` | `acc_latency` 0 and the debug registrar MT while unbound | — (the published contract before issue #212) |
| 11 | `hdl/srp/KL_srp_top.sv:622` | `.link_up_i (link_up_i)` on the listener | R770-1 F4 ruling |
| 12 | `tb/srp_stream_fsms/srp_stream_fsms_wrap.sv`, `srp_walk_wrap.sv`; `sim_main.cpp:241`, `:254` | the link input (walk wrap ties it 1), the latency strobe counted, the harness drives the link up | — |
| 13 | `tb/srp_stream_fsms/sim_main.cpp:3042` to `:3401` | PS16 to PS23 | acceptance 1 to 3 |
| 14 | `tb/srp_top/sim_main.cpp:3179`, group `link` | LK1 | the wiring of item 11 |
| 15 | `tb/srp_top/mutants.py`, `tb/srp_top/mutations/` (27 new patches; 11 of issue #212's own cut again with their edits unchanged) | the new arms; coverage PS1-PS23 and LK1; `pt-seed-dropped` on PS5, `presettle-removed` on PS3 | acceptance 5 |
| 16 | `docs/architecture/10_srp_engine.md:42`, `:51`, `:195`, `:225`, `:226` (R769-1 R1, the reviewer's text), `:228`, `:265`, `:610`, `:621`, `:767` and `:845` (R770-1 F5, the reviewer's text), `:781`, `:793`, `:807`, `:820`, `:831`, `:852` | contract, state, storage rows, measured cost, F10.5 arcs, §6.4: the deadline, the reach at N = 2, the S3 correction, the same-stream re-bind, the link change | as above |
| 17 | `docs/guides/integrator.md:618` | the path's reach at the shipping N = 2 (R769-1 S1) | — |
| 18 | `docs/architecture/02_interfaces.md:298`, `05_acmp_engine.md:301`, `docs/00_MILAN_COMPLIANCE_REVIEW.md` REQ-ACMP-018 | a kept registration strobes and applies at the settle | Milan v1.2 §5.3.8.5 |
| 19 | `tb/srp_stream_fsms/README.md`, `tb/srp_top/README.md` | the rows, the arms, the counts the new rows move | — |

## New checks (planted arm, failing words, count)

Unit (`tb/srp_stream_fsms` section PS) and `tb/srp_top` (LK1), SRP campaign at the head:
**275 of 275** (5 controls, 269 arm entries, coverage **166 of 166**), every count equal to
the README cells (`receipts/campaigns/srp-a2fce43/`).

| Check | Acceptance / finding | Planted arm | Named failing words | Failing checks |
|---|---|---|---|---:|
| PS16 | 3; R770-1 F1 | `pt-alloc-any-event` | `PS16:` | 9 |
| PS17 | 2; R770-1 F2 | `pt-fcode-first-only` | `PS17: a held Talker Failed` | 1 |
| PS17 | 2; R770-1 F2 | `pt-lat-on-alloc-only` | `PS17: a held Talker Advertise whose latency` | 3 |
| PS17 | 2 | `pt-type-on-alloc-only` | `PS17: a held Talker Advertise that turns Failed` | 1 |
| PS18 | F10.5; R770-1 F3 | `seed-on-teardown` | `PS18:` | 2 |
| PS19 | 3; R770-1 F3 | `pt-rlv-on-lv-ends` | `PS19:` | 2 |
| PS20 | 2; R769-1 F1 | `rebind-same-not-kept` | `PS20: every port registrar held by other values, sink 0 registered on its stream` | 4 |
| PS20 | exact triple | `keep-ignores-da`; `keep-ignores-vlan` | `PS20: a re-bind to the same stream_id on another DA`; `... VLAN` | 1; 1 |
| PS20 | 2 | `keep-declares-seed-type` | `PS20: every port registrar held by other values, sink 0 registered on a Talker Failed` | 1 |
| PS20 | latency strobe | `keep-latency-strobe-dropped` | `PS20: every port registrar held by other values, sink 0 registered on its stream` | 2 |
| PS21 | 3 | `unarmed-registrar-deaf` | `PS21: sink 0 unbound from a stream only its registrar holds, the talker withdraws` | 2 |
| PS21 | same-clock expiry | `keep-ignores-expiry` | `PS21: a re-bind on the clock of the kept registration` | 1 |
| PS22 | F10.5 | `unarmed-indicates`, `unarmed-fail-chg`, `unarmed-unregistered`, `unarmed-latency-strobe`, `unarmed-publishes-latency`, `unarmed-dbg-registrar` | `PS22:` | 1, 1, 1, 1, 2, 2 |
| PS23 | 3; R770-1 F4 | `pt-link-flush-dropped` | `PS23: a Talker Advertise registered before the link` | 4 |
| PS23 | Begin! | `link-begin-dropped` | `PS23: LINK_UP (Begin!)` | 1 |
| PS23 | 3; R770-1 F4 | `unarmed-link-flush-dropped` | `PS23: sink 0 unbound` | 1 |
| PS23 | same-clock link | `keep-on-link-clock` | `PS23: a re-bind to that stream on the clock the link goes down` | 1 |
| LK1 | R770-1 F4 wiring | `top-listener-link-unwired` | `LK1:` | 1 |
| PS8 | 13-bit deadline | `pt-expiry-sign-bit`; `seed-deadline-rebuild-drops-now` | `PS8:` | 6; 4 |
| PS3 | acceptance 5 | `presettle-removed` | `PS3:` | 36 |
| PS5 | acceptance 5 | `pt-seed-dropped` (entry re-named from PS3) | `PS5:` | 26 |

**Counts that moved** (the new rows fail under these arms too; README cells re-recorded):
`pt-seed-dropped` 22→26, `pt-never-holds` 22→26, `seed-no-registered-strobe` 17→25,
`pt-leaveall-ignored` 9→11, `seed-lv-fresh-deadline` 2→3, `pt-allocation-overwrites-entry-0`
4→6, `listener-settle-compare-dropped` 40→44 (PS20, PS21), `listener-teardown-keeps-declaring`
74→83 (PS20 to PS23). `lv-expiry-dropped` 87→89 keeps its 80 SC1 failures, and the stream-FSM
README now names its PS8, PS19 and PS21 failures. `listener-reprobe-parks-own-stream` 3→5
has no recorded count. Every walk-shape arm count is unchanged.

**The reviewers' probes at the head** (`receipts/probes/`):
- R769-1's re-bind probe passes, 1,502 of 1,502.
- R770-1's six previously-passing probes each fail their row: PS16, PS17 (three probes),
  PS18, PS19.

## Area (the processor's yosys flow: sv2v, yosys 0.66 `synth_xilinx -family xc7 -flatten`)

| `KL_srp_top` | base `a9e84b66` | round 1 `04856e48` | round 2 `a2fce43` | round 2 − round 1 |
|---|---|---|---|---|
| 2x2 (shipping) LUT / FF | 11,475 / 4,812 | 12,690 / 5,372 | 13,193 / 5,334 | +503 / −38 |
| 8x8 LUT / FF | 23,046 / 9,236 | 27,399 / 11,376 | 28,193 / 11,224 | +794 / −152 |

- RAM is unchanged everywhere. The head's stat files are byte-identical to the measured
  variant's. Base and round-1 figures reproduce round 1's exactly.
- FF from base: N×244 + (1 + log2 N + 32) + 1 at the listener (+523 at N = 2); +522 in
  `KL_srp_top`, where the link flip-flop merges with the Domain FSM's.
- The 13-bit deadline decision, measured with everything else equal:
  - `KL_srp_top` 2x2: 13,260 → 13,193 LUT, 5,372 → 5,334 FF;
  - 8x8: 28,276 → 28,193 LUT, 11,376 → 11,224 FF.
  - Smaller at both, so it was taken. The listener alone at 8 sinks: +131 LUT, −152 FF.
- **The LUT figure is noisy at the ±300 level** (`receipts/area/AREA.md`):
  - `keep-ignores-vlan` (about −8 true LUT) measured −150;
  - `keep-latency-strobe-dropped` (about −11 LUT) measured +56.
  - So round 2's +503 LUT at 2x2 is not resolved by this flow. The FF figure (−38) is exact.
- **For the manager:** the PR #213 route comment says round 2 must not grow the shipping
  image beyond round 1 without a new route. FF fell by 38. The yosys LUT figure rose within
  its noise, so I cannot show that the image did not grow. Please route the head (no Vivado
  was run here).

## Processor gate table (clean clone of `a2fce43`)

| Gate | Result | Receipt |
|---|---|---|
| `make check` | rc 0 | `processor/head-a2fce43/make_check.*` |
| `bash scripts/lint_hdl.sh` (Verilator 5.052; pinned 5.050) | rc 0 both, 41 modules LINT OK each | `lint_hdl_5052.*`, `lint_hdl_5050.*` |
| `./syn/yosys/run.sh` | rc 0 | `yosys_run.*` |
| `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0, 93 of 93 | `elab_guards.*` |
| `bash scripts/run_suites.sh` (pinned 5.050, `MAKEFLAGS=-j16`, `REQ_TAG_LOG`) | rc 0: **1,030,993 checks, 0 failing**, 36 suites; pp_top 11,064, srp_stream_fsms 1,500 (round 1 1,468), srp_top 8,671 (8,669) | `run_suites.*`, `sweep-summary.txt` |
| `python3 scripts/check-req-tags.py --suites ... --evidence ...` | rc 0: 266 evidence lines, 14 suites | `check_req_tags_exec.*` |
| SRP campaign `tb/srp_top/mutants.py --jobs 4` | rc 0: 275 of 275, coverage 166 of 166 | `campaigns/srp-a2fce43/` |
| ACMP `tb/pp_top/acmp_mutants.py --jobs 3` | rc 0: 103 of 103 KILLED by their named checks, goldens PASS | `campaigns/acmp-a2fce43/` |
| AECP `aecp_mutants.py --jobs 3` | rc 0: 67 checks, 67 PASS | `campaigns/aecp-a2fce43/` |
| GSI `gsi_mutants.py --jobs 3` | rc 0: 30 detected by named checks, golden and restored PASS | `campaigns/gsi-a2fce43/` |
| CTR `ctr_mutants.py --jobs 3` | rc 0: 18 checks, 18 PASS | `campaigns/ctr-a2fce43/` |
| name write `name_wr_mutant.py` | rc 0: decode killed, golden and restored PASS | `campaigns/name-wr-a2fce43/` |
| AECP dispatch `aecp_dispatch_mutants.py --jobs 3` | rc 0: 105 checks, 105 PASS | `campaigns/aecp-dispatch-a2fce43/` |
| notification `notify_mutants.py --jobs 3` | rc 0: 137 of 137 KILLED by their named checks, goldens PASS | `campaigns/notify-a2fce43/` |
| D3 `d3_mutants.py --jobs 3` | rc 0: 110 of 110 KILLED by their named checks, goldens PASS | `campaigns/d3-a2fce43/` |
| Area | above | `area/` |

The eight campaigns outside SRP ran with the pinned Verilator 5.050, its C++ build capped at
`-j2`, or `-j1` while the governor held it. Compared with round 1's runs (at `913214a`,
the round-1 handoff), every per-arm result is the same, label for label:
- the ACMP, notification and D3 verdicts;
- the AECP, CTR and AECP-dispatch arm lines (label, rc, failures, named): 61, 17 and 100;
- the GSI and name-write variant lines (build and run rc): 32 and 3.

## Scratch-parent consumer gate table (pin `a2fce43`)

The scratch parent is the round-1 one (milan-fpga dev `604899c0`, local branch, push URL
`DISABLED-never-push`, never pushed). Two new local commits:
- `5396b1a2`: protocol-processor → `a2fce43`;
- `5761bf45`: its ROM digests through `./syn/yosys/ooc.sh --record-rom-digests`, equal to
  main's (ltn `23cc67ee…`, ucode `49a993be…`).

A top-level identity check preceded every git command inside `protocol-processor`. The tools
are the parent's CI pins: Verilator 5.050, yosys 0.66, sv2v v0.0.12, a CPython 3.12.3 venv of
`ci/constraints-ci.txt`, and GoogleTest 1.14.0 on the system include path
(`receipts/records/parent-records.txt`).

| Consumer gate (rtl-fast job) | Result |
|---|---|
| changes (`ci_scope.py --selftest`; classify from `604899c0`) | rc 0, rc 0 |
| verilator-lint (`lint_rtl.py --check --self-test`; `pp_srcs.py --check --selftest`) | rc 0: 89 ≤ ratchet 89; rc 0 |
| bdd-conformance (`behave`) | rc 0: 14 features, 508 scenarios, 2,330 steps passed |
| yosys-elaboration (elaborate `milan_datapath`, `KL_pp_shadow`, `KL_gptp_shadow`; OOC read sets; `ooc_selftest`; `guard_selftest`; `cache_selftest`) | rc 0 each |
| publication-census | rc 0: 0 of 31 rules no arm proves |
| firmware-unit (tally and rv32 self-tests; `test_ctrl_firmware.py --shard 0/4`; `test_ctrl_nvm.py`; `fw_coverage.py --selftest`, `--check`) | rc 0 each: shard 0 PASS, ctrl_nvm OK across 5 shapes, coverage PASS (30 files) |
| firmware-control mutants (`--shard 1/4`) | rc 0: 523 of 523 caught |
| firmware-aecp mutants (`--shard 2/4`) | rc 0: 78 `[ok]`, PASS |
| firmware-srp mutants (`--shard 3/4`) | rc 0: 280 `[ok]`, PASS |
| firmware-boundary (`ctrl_boundary.py --selftest --without verilator`) | rc 0: PASS |
| firmware-verilator (`ctrl_boundary.py --selftest --only verilator`) | rc 0: PASS |
| milan_dp (`make -C tb/verilator/milan_dp SIM_JOBS=2`) | rc 0: 12,075 `[ok]`, 1,301 `[PASS]`, 0 `[FAIL]` (round 1: the same counts) |

Receipts: `parent/pin-a2fce43/`. Two logs are over 200 KB, `behave.log` and `milan_dp.log`.
Each is recorded with its size and sha256 in that directory's `RAW-RECORDS.txt`, beside a
generated summary.

## Process notes

- **Memory: the 10 GB working limit was exceeded once.** The unit's `memory.peak` reads
  10.75 GB (under the 12 GB cap). It was reached at about 10:45, during development runs
  before any gate: a `pp_top` build and an 8-job arm campaign overlapping, before I started
  the reclaim governor (`tools/memgov.sh`: `memory.reclaim` above 8.5 GB, no process
  stopped). From then on it held, with `memory.current` back under 10 GB within 2 s of
  each sample above 8.5 GB (`receipts/records/memgov.log`). Anonymous memory stayed below
  7.5 GB in every sample taken.
- The full processor sweep is `scripts/run_suites.sh`, which has no shard option
  (`native-shards.py` drives the parent's `run_all_suites.sh`), so it ran whole in this unit.
- Superseded: the first AECP-dispatch start was stopped after 4 minutes to split the long
  D3 campaign into its own chain (`receipts/superseded/`).
- **Host reset (2026-11-05, 13:10 to 17:35).** It stopped the ACMP, AECP-dispatch and D3
  campaigns and the parent's firmware-control shard (1 of 4) mid-run. It was not a gate
  failure: no arm had escaped in the partial logs. Those partial logs are kept in
  `receipts/superseded/host-reset-1310/`.
  - Before the restart I checked that each clone was still at the head with an empty
    `git status --ignored`, and that the scratch parent was clean at `5761bf45`.
  - The four gates, and the ones queued behind them, then ran again from the start.
  - The gates that had finished before the reset are kept as they were: the SRP campaign,
    the processor fast gates and sweep, and the parent's rtl-fast jobs through
    firmware-unit.
  - The governor was restarted on the new unit's cgroup. It now also caps the campaign
    Verilator builds at `-j1` while anonymous memory is above 7.5 GB.
  - In the restarted unit, `memory.peak` reads 8.81 GB, so the 10 GB limit held throughout.
    The governor reclaimed page cache 10 times, and the `-j1` cap held once, for 9 s, at
    7.78 GB anonymous (the post-reset part of `records/memgov.log`).
- **For the manager: CPU overlap after the reset.** This unit's CPUs (96-111) are also the
  affinity of two other lanes' units, started at 17:58, 20 minutes after this one. The CPU
  booking helper's `show` lists no free range. I left those units alone, so the restarted
  gates ran on a shared block and took longer: D3 at `--jobs 3` took 3 h 11 min, against
  2 h 10 min at `--jobs 4` in round 1.

## Not done (by the assignment's rules)

No push, no PR creation or edit, no merge or rebase, no comment edits, no hardware or bench
access, no Vivado run, no sub-agents.
