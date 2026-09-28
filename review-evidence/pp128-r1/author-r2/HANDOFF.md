# [A399] Round 2 handoff

Ready for review. Head `cc7c911e933aed4bfc9324eb5da473ae73bef618` on `128-acmp-da-retry`.
Starting head `9476898b28ffc8f77b2aa5f873f3899a17287d3a`; main/base
`16be6768f710e79450aace277abacd6c2c3336e5`.
Origin verified: `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.
One new commit, subject only, no body or trailers:
`Close ACMP retry review gaps and document paced allocation semantics`.

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/128#issuecomment-5861952375
TAKEN: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/128#issuecomment-5861962008
Delivery text: `[A399] REVIEW READY cc7c911e933aed4bfc9324eb5da473ae73bef618`.

## Changes and reviewer reconciliation

| Item | Change with file:line | Disposition |
|---|---|---|
| R376 F1 / R377 F1 | `hdl/acmp/KL_acmp_talker.sv:878` declares the pending-event group before `retry_round` at :885 and its use at :898 | New use-before-declaration finding removed; parent xvlog gate passes. The four remaining findings are in byte-identical base files, proven in `interface-and-preexisting.txt`. |
| R376 F2 / R377 F4 | `docs/architecture/05_acmp_engine.md:412` and :452; `docs/architecture/02_interfaces.md:268` | Keeps the assigned paced-round policy. Documents deferred within-round demand and automatic acquisition for every enabled in-block source. Exact parent [H]/[I] reconciliation below. |
| R376 F3 / R377 F2 | `tb/acmp_talker/retry_mutants.py:237` | Removed host deadline; completed cycle-bounded simulation and named assertion failures remain mandatory. Parent evidence check is run unchanged and with only the proposed disposition row. No ratchet changed. |
| R376 F4 / R377 F3 | `tb/acmp_talker/retry_cases.hpp:270`–R9, :279–R10, :298–R11, :320–R12 | Consecutive commands, same-round lifetime restart, release/disable fairness, and all three demand arcs now have committed regressions. Every non-equivalent surviving reviewer mutant fails a named assertion. |
| R377 S1 | `retry_cases.hpp:343`–R13, :363–R14, :381–R15; `retry_mutants.py:219` and :229; `KL_acmp_talker.sv:898` | Exact-edge cancellation/INIT guards and release pacing are pinned. Four mutually redundant single-term variants are explicit clean controls; the redundant `!en_q_r[i]` pacing-clear term is removed. Construction arguments below. |
| R376 S1 / R377 S2 | Packet `original-run_first_probe.py`, `original-reproduce_first_probe.cpp`, `run_parent_probe.py`, `reproduce_first_probe.cpp`, `harness-oracle.diff`, `first-probe-wrapper.sv` and hashes | Original wiring and defect oracle are preserved, fixed oracle is explicit, and the original driver runs in scratch against this head. |
| R376 S2 / R377 S3 | `KL_acmp_talker.sv:174`, `tb/acmp_talker/sim_main.cpp:957`, `docs/guides/operator.md:282` | Removes stale probe-first allocation/arbitration descriptions and explains failure before the acquisition bound. |
| R376 S3/S4 | `05_acmp_engine.md:389`, :412; `docs/guides/integrator.md:44` | Adds the NO_DA retry arc, references the timing ID instead of repeating its value, and documents the running-timebase dependency. |

Only declaration order, the redundant term and explanatory comments change in
production RTL in round 2. Ports/parameters are identical to base. Allocation,
conflict and PCP backoff policy are retained. Full issue, both assignments, both
reviews, consumer comments/receipts, donor contribution/quality rules and design,
parent shim, and the permitted analysis/harness inputs were read. The parent and
review input directories stayed read-only.

## Case table

The talker now has 1,172 checks, 65 more than round 1. Section R contains 333
checks and 50 assertion sites, all with killed witnesses. Expectations use ports
and independent timing/tuple contracts, without forced internal state.

| Case | Observation | Review coverage |
|---|---|---|
| R1 | Every refused source acquires after the round; no attempt at bound minus one; correct first-probe tuple; freshness expiry | Original acceptance retained |
| R2 | Permanent refusal, repeated probes/listeners, disabled sources and re-enable stay paced and honest | [H] policy retained |
| R3 | Never-ready allocator, rotating all-source fairness and bounded continuous command service | Original fairness retained |
| R4 | Obsolete success after disable/re-enable or conflict is discarded and released before fresh allocation | Whole-cause cancellation mutants |
| R5 | Response timeout, stale FIFO debt, saturation/drain, modulo-time behavior | Late response acceptance retained |
| R6 | Conflict/PCP leave full backoff and timer arms intact; only conflict needs a new DA | Original backoff retained |
| R7 | Block count growth/shrink and base move, all-source mapping, out-of-range failure | [I] source-index policy retained |
| R8 | Retry boundary on both sides of millisecond wrap | Original timing retained |
| R9 | Six consecutive probes during an accepted, unanswered allocation each meet the command bound and return honest failure | R377 P1 / R376 P5; starvation mutant |
| R10 | DA_OK conflict and disable/re-enable of a refused source immediately restart within the same round | R377 P2 / R376 P1/P2 |
| R11 | Continuous commands continue through teardown while disable/withdrawal and immediate/owed release also progress | R376 P3b / R377 S1; additional busy-tracker mutant |
| R12 | Probe, listener and full two-LeaveAll expiry each allocate strictly between retry ticks | R377 P4–P6 / R376 demand mutants m20–m22 |
| R13 | Disable/conflict swept over response edge and next three edges, including the grant write, never publish poison and release it | R377 S1; m04/m10/m11 |
| R14 | Cancellation in the allocation read/action window suppresses the obsolete request | R377 S1; m05/m13 |
| R15 | Re-enable at the release offer does not consume the new lifetime's allocation opportunity | wait_on_release / m08 |

## Mutant table

`python3 tb/acmp_talker/retry_mutants.py --logs /tmp/pp128-a399/mutants-complete`
returns 0: **56 killed defects, four equivalent controls**, baseline/restored
**1172/1172, rc 0**. A missing simulation tally or compiler failure is never a
kill. `mutants/coverage.txt` gives a named killed witness for **50/50** sites.
Counts below are all named suite assertion failures; the separate coverage file
tracks retry assertion sites specifically. All 22 internal and 26 external
review identifiers are mapped, including the removed redundant term.

| Campaign mutant | Review identifier(s) | Result | Named assertion witness |
|---|---|---|---|
| `no_round` | R376 m18_no_round | killed; rc 2; 22 failures | R1 automatic bounded acquisition |
| `early_round` | author campaign | killed; rc 2; 2 failures | R1 no retry before 100 ms |
| `late_round` | author campaign | killed; rc 2; 21 failures | R1 automatic bounded acquisition |
| `retry_wrap` | author campaign | killed; rc 2; 2 failures | R8 wrap retry bound minus one |
| `no_pacing` | author campaign | killed; rc 2; 36 failures | R2 demand cannot bypass retry pacing |
| `fixed_priority` | author campaign | killed; rc 2; 1 failures | R3 every source gets an attempt under continuous commands |
| `command_monopoly` | author campaign | killed; rc 2; 5 failures | R3 every source gets an attempt under continuous commands |
| `retry_monopoly` | author campaign | killed; rc 2; 60 failures | R3 absent allocator src0 consumed |
| `disabled_alloc` | author campaign | killed; rc 2; 2 failures | R2 disabled listener event cannot allocate |
| `no_accept_bound` | author campaign | killed; rc 2; 50 failures | R3 every source gets an attempt under continuous commands |
| `short_accept_bound` | author campaign | killed; rc 2; 2 failures | R3 absent request respects accept bound |
| `refusal_is_grant` | author campaign | killed; rc 2; 62 failures | R1 automatic bounded acquisition |
| `obsolete_grant` | author campaign | killed; rc 2; 19 failures | R4 obsolete grant rejected src0 status/tuple |
| `obsolete_release_lost` | author campaign | killed; rc 2; 11 failures | R4 obsolete successful allocation released before retry |
| `no_response_bound` | author campaign | killed; rc 2; 16 failures | R5 timeout retries automatically across wrap |
| `response_wrap` | author campaign | killed; rc 2; 1 failures | R5 no premature response timeout across wrap |
| `no_stale_swallow` | author campaign | killed; rc 2; 9 failures | R5 stale timeout response src0 status/tuple |
| `no_stale_capacity` | author campaign | killed; rc 2; 2 failures | R5 silent accepts stop at stale-credit capacity |
| `no_stale_drain` | author campaign | killed; rc 2; 16 failures | R5 retry response src0 status/tuple |
| `backoff_bypass` | author campaign | killed; rc 2; 2 failures | R6 retries leave backoff and timer untouched |
| `reallocate_owned` | author campaign | killed; rc 2; 119 failures | R1 owned addresses are never reallocated |
| `half_backoff` | author campaign | killed; rc 2; 6 failures | R6 full two-LeaveAll backoff armed |
| `fresh_forever` | author campaign | killed; rc 2; 93 failures | R1 freshness expiry still withdraws every source |
| `declare_without_demand` | author campaign | killed; rc 2; 150 failures | R1 acquired addresses neither declare nor borrow timer slots |
| `source_alias` | author campaign | killed; rc 2; 166 failures | R1 first probe after bound src0 status/tuple |
| `gate_without_ownership` | author campaign | killed; rc 2; 47 failures | R1 acquired addresses neither declare nor borrow timer slots |
| `no_requests` | author campaign | killed; rc 2; 206 failures | R1 one refused startup attempt per source |
| `no_command_ready` | author campaign | killed; rc 2; 541 failures | R1 first probe after bound src0 consumed |
| `busy_tracker_blocks_commands` | author campaign | killed; rc 2; 62 failures | R4 obsolete grant rejected src0 consumed |
| `no_conflict_wait_clear` | R376 m01_conflict_keeps_wait; R377 no_conflict_wait_clear | killed; rc 2; 3 failures | R10 conflict immediately restarts acquisition |
| `wait_on_release` | R376 m08_release_sets_wait; R377 wait_on_release | killed; rc 2; 48 failures | R15 release does not consume re-enabled lifetime allocation attempt |
| `tick_no_rearm` | R377 tick_no_rearm | killed; rc 2; 40 failures | R2 one attempt per enabled source per round |
| `no_rotate_advance` | R376 m14_round_skips_rotation; R377 no_rotate_advance | killed; rc 2; 1 failures | R3 every source gets an attempt under continuous commands |
| `no_sticky_gp_window` | R377 no_sticky_gp_window | equivalent; rc 0 | construction argument below |
| `grant_kill_reg_only` | R376 m04_grant_kill_reg_only; R377 grant_kill_reg_only | killed; rc 2; 3 failures | R13 cancellation kind0 edge3 never publishes obsolete grant |
| `accept_kill_zero` | R377 accept_kill_zero | equivalent; rc 0 | construction argument below |
| `kill_no_pending_conflict` | R377 kill_no_pending_conflict | equivalent; rc 0 | construction argument below |
| `kill_no_live_conflict` | R376 m10_kill_ignores_conflict_strobe; R377 kill_no_live_conflict | killed; rc 2; 2 failures | R13 cancellation kind0 edge3 never publishes obsolete grant |
| `kill_no_disable` | R376 m11_kill_ignores_disable; R377 kill_no_disable | killed; rc 2; 1 failures | R13 cancellation kind1 edge3 never publishes obsolete grant |
| `init_elig_no_avail` | R376 m19_init_elig_no_avail; R377 init_elig_no_avail | killed; rc 2; 15 failures | R9 consecutive command during silent allocation src1 consumed |
| `no_turn_restore` | R376 m06_turn_never_returns; R377 no_turn_restore | killed; rc 2; 57 failures | R3 commands never starve behind retries (gap=0) |
| `elig_drop_rel` | R376 m07_eligible_ignores_rel; R377 elig_drop_rel | killed; rc 2; 1 failures | R11 owed release serviced under continuous commands |
| `elig_drop_off` | R377 elig_drop_off | killed; rc 2; 4 failures | R11 disable withdraws under continuous commands |
| `ready_ignores_turn` | R376 m09_ready_ignores_turn; R377 ready_ignores_turn | killed; rc 2; 89 failures | B4 re-ping: timer arm missing |
| `init_ignores_off_conflict` | R376 m05_init_ignores_pending_off_conflict; R377 init_ignores_off_conflict | killed; rc 2; 2 failures | R14 cancellation kind0 prevents obsolete allocation offer |
| `retry_period_200` | R377 retry_period_200 | killed; rc 2; 21 failures | R1 automatic bounded acquisition |
| `tick_ge_to_gt` | R377 tick_ge_to_gt | killed; rc 2; 21 failures | R1 automatic bounded acquisition |
| `kill_no_conflict_at_all` | R377 kill_no_conflict_at_all | killed; rc 2; 10 failures | R4 obsolete grant rejected src0 status/tuple |
| `kill_no_disable_at_all` | R377 kill_no_disable_at_all | killed; rc 2; 9 failures | R4 obsolete grant rejected src0 status/tuple |
| `kill_sticky_off` | R376 m12_sticky_kill_off; R377 kill_sticky_off | killed; rc 2; 10 failures | R4 obsolete grant rejected src0 status/tuple |
| `no_probe_initset` | R376 m20_no_probe_initset; R377 no_probe_initset | killed; rc 2; 1 failures | R12 demand arc 0 allocates inside round |
| `no_lsn_initset` | R376 m21_no_lsn_initset; R377 no_lsn_initset | killed; rc 2; 1 failures | R12 demand arc 1 allocates inside round |
| `no_conflict_daok_initset` | R377 no_conflict_daok_initset | killed; rc 2; 39 failures | R10 conflict immediately restarts acquisition |
| `no_backoff_exit_initset` | R376 m22_no_backoff_exit_initset; R377 no_backoff_exit_initset | killed; rc 2; 1 failures | R12 demand arc 2 allocates inside round |
| `no_enable_wait_clear` | R376 m02_enable_keeps_wait | killed; rc 2; 2 failures | R10 re-enable immediately restarts acquisition |
| `eligible_only_init` | R376 m17_eligible_only_init | killed; rc 2; 4 failures | R11 disable withdraws under continuous commands |
| `accept_kill_no_disable` | R376 m03_no_accept_kill | equivalent; rc 0 | construction argument below |
| `init_no_enable_check` | R376 m13_init_no_enable_check | killed; rc 2; 1 failures | R14 cancellation kind2 prevents obsolete allocation offer |
| `eligible_ignores_init` | R376 m15_eligible_ignores_init | killed; rc 2; 1 failures | R3 every source gets an attempt under continuous commands |
| `tick_keeps_wait` | R376 m16_tick_keeps_wait | killed; rc 2; 31 failures | R1 automatic bounded acquisition |
| `no_reenable_wait_clear` | R377 no_reenable_wait_clear | redundant term removed | disable/reset already clear wait; see below |

Equivalence arguments (passing a finite suite alone is not the argument):

- `no_sticky_gp_window`: Until GRANT consumes gp_valid, OFF/CONFLICT cannot dispatch; their pending bits retain every cancellation through the grant action.
- `accept_kill_zero`: Cancellation on accept is pending on the next busy edge; a response cannot be consumed as a grant before that edge latches the kill.
- `accept_kill_no_disable`: An accept-edge disable sets OFF, which persists and latches the kill on the next busy edge before grant consumption.
- `kill_no_pending_conflict`: A conflict after accept latches the live kill; an older pending conflict is captured by the accept-side kill expression.
- `no_reenable_wait_clear`: Removed !en_q_r: reset clears wait and each disabled edge already clears it through !cfg_src_en_i; no enable-edge clear is needed.

Whole-cause conflict, disable and sticky-kill removals are also executed and
killed. The four controls do not contribute assertion-coverage witnesses.
The final Python formatting folds fourteen tuple literals; parsed program
identity was checked (`validation-inputs.txt`).

## Parent gates and first-probe result

Parent gate source: `931f396ec9f13271e9e67b755e18833d0024f234`.
Scratch: `/tmp/pp128-a399/parent-gates-final`, with processor contents pointing
at this tree and private Git metadata recording the final pin. The pinned gPTP
dependency `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` was exported from fetched
objects under `/tmp`; no additional branch/worktree checkout was performed.
The gate's population/hash checks and ratchets were not bypassed or changed.
`run_parent_gates.py` reproduces the staging and both evidence variants.

- `xvlog_gate.py --check`: **rc 0**, 72 parent plus 51 processor source files,
  exactly four grandfathered findings. This PR's talker finding is gone.
- `measure_test_evidence.py --check`, original table: **rc 1**, solely the
  missing `retry_mutants.py` disposition. The wall-clock count is back to 3.
- Same check, proposed disposition only in scratch: **rc 0**; 76 <= 77 suites
  without an executable arm, 10 <= 10 unseeded sites, 0 unexplained readers,
  3 <= 3 wall-clock-dependent files. The budget remains unchanged.
- Parent C++ and Python source-quality checks: **rc 0**. Mutation-table literal
  wrapping fixes the Python column-limit finding without changing the program.
- Real parent-shim first-probe harness against `cc7c911e933aed4bfc9324eb5da473ae73bef618`: **rc 0**;
  first response status **0**, DA **91e0f0006818**, expected source SID/VID,
  no probe-triggered allocation. Repeated-probe and warm-start controls pass.
  The replay advances 100 to 200 ms and allows the 8,704-clock source sweep.

The original parent oracle deliberately asserts the defect. The packet preserves
it verbatim and records every fixed-oracle change in `harness-oracle.diff`.
The packet-only replay also passes: `run_parent_probe.py` accepts this packet as its
ANALYSIS argument and uses its preserved original driver and oracle.
The unchanged shim SHA256 is
`965fbee050c985f767423bf63f2c0f0a507faf5ede7cc81e3a939bee963ba98e`.
Original driver, `first-probe-wrapper.sv`, both oracles, commands and artifact
hashes make the replay independent of unpublished glue. The generated wrapper
is a test harness; no processor/parent interface source is changed.

The round-1 consumer result remains the supplied **8/11** record:
`xvlog`, `pp_shadow` and evidence were red. `07.log` also confirms `[I]` in
CRF, in addition to `[H]` in base/vid73/CRF. This lane does not claim a new
`pp_shadow` pass: parent test changes and reruns belong to pin adoption.

## Exact parent-check reconciliation text

[H]: `pp_shadow [H]` must allow one `T-ACMP-DA-RETRY` round plus the source sweep before requiring a new accepted/refused ALLOC_DA. A PROBE_TX inside an already attempted round does not force another allocation. Observe an accepted request, its refusal, the closed DA gate, an honest status-3 probe response and continuing command service; do not require a probe-caused request within 4000 fixed-time cycles.

[I]: `pp_shadow [I]` must associate each allocation response with the source index of its accepted request and compare that source's DA with KL_maap base + source index. Every enabled in-block source auto-acquires, including CRF source 1; a single global last_da is not necessarily source 0's grant.

DUT-reader disposition line (one logical dictionary entry; wrap literals to the
parent's column limit when inserting it):

```python
"protocol-processor/tb/acmp_talker/retry_mutants.py": "mutation campaign; plants named defects in a scratch copy and requires named assertion failures from completed cycle-bounded simulations; reads no expected behavior from RTL",
```

These three parent edits belong to the pin-adoption lane. Keep the paced rounds;
no immediate-probe exception or interface change is proposed. Re-run all parent
`pp_shadow` builds after changing [H]/[I], retain the real-shim first-probe case,
and adopt the pin after the consumer checks pass.

## Suite and gate table

Every command completed in the foreground, with its return code preserved and
without a pipe. Final full sweep: **33 suites, 1,015,055 checks, zero failures**.
All three ACMP and all five SRP suites are included.

| Suite | Checks | rc |
|---|---:|---:|
| `acmp_listener` | 2544 | 0 |
| `acmp_nvm` | 349 | 0 |
| `acmp_talker` | 1172 | 0 |
| `adp_engine` | 533 | 0 |
| `aecp_notify` | 10 | 0 |
| `ca_originator` | 16 | 0 |
| `desc_mem_guard` | 78 | 0 |
| `desc_store` | 584 | 0 |
| `dispatch` | 211 | 0 |
| `dyn_state` | 89 | 0 |
| `event_router` | 81 | 0 |
| `lsn_admit` | 18 | 0 |
| `maap` | 75 | 0 |
| `nvm_port` | 136 | 0 |
| `originator` | 104 | 0 |
| `pp_top` | 7751 | 0 |
| `prng` | 76 | 0 |
| `release_merge` | 18 | 0 |
| `resp_buf` | 64 | 0 |
| `rx_slots` | 130 | 0 |
| `rx_validator` | 393 | 0 |
| `scoreboard` | 3705 | 0 |
| `side_port` | 368 | 0 |
| `srp_admission` | 991231 | 0 |
| `srp_decoder` | 190 | 0 |
| `srp_encoder` | 556 | 0 |
| `srp_stream_fsms` | 1087 | 0 |
| `srp_top` | 1531 | 0 |
| `timer_map` | 1360 | 0 |
| `timer_service` | 48 | 0 |
| `tx_arbiter` | 66 | 0 |
| `tx_slots` | 95 | 0 |
| `ucpu` | 386 | 0 |

| Entry point / gate | rc | Receipt |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | `suites.txt` |
| `./scripts/lint_hdl.sh` | 0 | `lint.txt` |
| `make check` | 0 | `docs.txt`; 41 Mermaid, 18 WaveDrom, 921 links, matrices/parameters/freshness |
| `python3 scripts/gen_matrix.py --check` | 0 | 92 rows, zero untested; also in `docs.txt` |
| `./syn/yosys/run.sh` | 0 | `portability.txt`; all tops plus memory-mapping gate |
| `make -C tb/nvm_port figures` | 0 | `nvm-figures.txt` |
| Full retry mutation campaign | 0 | `mutants.txt`, `mutants/` |
| Parent `xvlog_gate.py --check` | 0 | `xvlog.txt` |
| Parent evidence, unchanged disposition table | 1, expected adoption dependency | `evidence-original.txt` |
| Parent evidence, proposed disposition only | 0 | `evidence-disposition.txt` |
| Parent C++ / Python quality checks | 0 / 0 | `parent-cpp.txt`, `parent-python.txt` |
| Parent first-probe harness | 0 | `parent-harness.txt`, `run_parent_probe.py` |
| `git diff --check`, final worktree status | 0, clean | final verification |

## Scope, limits and final state

Source and test failures found during development were resolved: added exact-edge
and release checks killed the formerly surviving variants; a busy-tracker mutant
supplies the previously missing R11 command-progress witness; Python literals
were folded for the parent source-quality gate. None was counted as a successful
campaign before the complete runner passed.

The acquisition bound assumes a running millisecond input, a stable block and
bounded allocator service without stale response debt or sustained higher-priority
configuration/conflict/PCP churn. Refusal, absence and out-of-block behavior stay
honest and bounded. The replay does not reconstruct the peer's 6.877-second retry
interval or the full bench startup history. No hardware result is claimed.

No parent or review input was edited; no existing comment was edited/deleted;
no push, PR creation/edit, merge, hardware action or delegation was performed.
The working tree is clean. The packet contains only source-sized harnesses,
receipts and documentation; no toolchain, environment, installed package, tree
export or file over 200 KB. Large artifacts remain under `/tmp`; their sizes and
SHA256 values are in `SCRATCH-ARTIFACTS.md`. `MANIFEST.sha256` inventories the packet.
