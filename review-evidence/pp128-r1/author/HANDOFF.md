# [A395] Issue #128 handoff

Completed 2026-09-28. Local head `9476898b28ffc8f77b2aa5f873f3899a17287d3a` on `128-acmp-da-retry`.
Starting HEAD verified as `16be6768f710e79450aace277abacd6c2c3336e5`;
origin verified as `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.
Commit subject: `Retry refused ACMP destination allocations in fair paced rounds`.
The commit has no body or trailers. Working tree clean at delivery.

Assignment and full issue: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/128#issuecomment-5861093499
TAKEN: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/128#issuecomment-5861100560
Delivery notice: `[A395] REVIEW READY 9476898b28ffc8f77b2aa5f873f3899a17287d3a` on issue #128.

## Change and file:line references

- `hdl/acmp/KL_acmp_talker.sv:448`: 100 ms retry round on the existing millisecond input; one allocation attempt per enabled source per round, including repeated probe/listener demand.
- `hdl/acmp/KL_acmp_talker.sv:457`: rotating source selection for pending allocation work; busy allocation cannot monopolise the event walker.
- `hdl/acmp/KL_acmp_talker.sv:594` and `:1403`: alternate commands and pending events, with ready independent of valid for scoreboard integration. Retry-induced command service is bounded by the accept window plus 64 clocks.
- `hdl/acmp/KL_acmp_talker.sv:733` and `:1083`: successful grants invalidated by disable/re-enable or conflict are released before reacquisition and never installed.
- `hdl/acmp/KL_acmp_talker.sv:878` and `:1122`: coalesced retry scheduling, enabled-source filtering and per-round pacing. Existing freshness/backoff timer slots and watchdog/stale-credit rules are retained.
- `tb/acmp_talker/retry_cases.hpp:40`: eight scenario groups, 268 added checks; complete talker tally 1107. `retry_mutants.py:13` names the 28 mutants; `:56` rejects build errors as mutation evidence and records assertion witnesses.
- `tb/pp_top/sim_main.cpp:8403`: first probe succeeds after the internal allocator acquisition bound. `:9435`: absent allocator still fails honestly, then all eight sources acquire after availability without a new probe. Expected DAs come from the independent allocator BFM's per-source grants.
- `docs/architecture/05_acmp_engine.md:411`, `08_timing.md:34`, and `02_interfaces.md` document policy, bounds, assumptions and unchanged interface.

Choice: automatic acquisition was selected over a command-time wait. It repairs
startup independently of listener timing and keeps allocation response waits off
the command walker. A refusal never fabricates ownership or an SRP declaration.
The source record remains in the existing synchronous RAM; the scheduler adds
one round timestamp, a per-source pacing bitmap, a rotating index and arbitration
state. No processor/parent port or parameter contract changed.

Read the donor engineer, HDL and verification rules, ACMP talker design and
MAAP interface, ACMP benches, parent contribution/quality rules, the specified
parent adapter and the specified analysis/harness inputs. Parent and analysis
inputs stayed read-only. No hardware work, push, PR creation/edit, merge, or
existing comment edit/delete was performed.

## Acquisition bound and limits

For a stable parent block adapter with no stale response debt or higher-priority
configuration/conflict/PCP/event churn, the bound is one **100 ms** retry period
plus `N_STREAM_OUT * (MAAP_ACCEPT_CYC + 64)` core clocks. With 8 sources and
100 MHz this is **100 ms + 87.04 us**. Continuous solicited commands are included.
A slower conforming allocator adds its bounded response latency per source.
The existing response watchdog and stale-credit capacity preserve bounded
failure for permanently unanswered requests; acquisition cannot be promised
until an untagged stale-response debt drains. Adjacent round boundaries can
produce two close attempts, but sustained attempts stay at one/source/round.
Disable and conflict start a new acquisition lifetime. Conflict/PCP backoff is
unchanged, including the shared timer's exact freshness restoration.

## Late-availability and failure case table

| Case | Expected behavior and measured result | Evidence |
|---|---|---|
| Refused startup, then available | All 8 sources acquire without a probe at the round boundary; none retries at boundary minus 1 ms; first probe returns success and correct tuple | R1; real parent replay |
| Permanent refusal, repeated probes/listener changes | Status 3 and zero tuple; one attempt/enabled source/round, no declaration | R2 |
| Disabled source, listener event, re-enable | Disabled source allocates nothing and probe returns unknown; all sources recover on re-enable | R2 |
| Ready permanently low with continuous probes | All sources get a turn; offer lasts exactly 1024 clocks; command gap <=1088 clocks | R3 |
| Disable/re-enable or conflict before grant | Obsolete DA never reaches a record/gate; successful obsolete allocation is released before fresh grant | R4 |
| Timed-out request and late response | Late poison response swallowed before retry's own response; safe success afterward | R5 |
| Permanently silent accepted requests | Three stale credits saturate safely; commands still fail honestly; draining a credit permits another attempt | R5 |
| Conflict and PCP change | Full two-LeaveAll deadline retained; retry rounds neither allocate during backoff nor replace timer arms; only conflict changes the DA | R6 |
| Block count grows, shrinks, address moves | Every source checked; high out-of-range sources remain paced failures, in-range sources use the new mapping | R7 |
| Millisecond wrap | Retry and response deadlines checked on both sides of wrap | R5, R8 |
| Freshness expires | All previously probed sources withdraw; cached owned addresses are retained without new allocation | R1 |
| Real internal allocator and SRP wire | First internal probe succeeds after the bound; external source grants reach both ACMP and SRP | Updated MP3/S10; full pp_top |

## Mutant table

All 28 variants completed simulation, failed new assertions, and returned the
expected nonzero suite status. Build errors never count as kills. Baseline and
restored RTL each return 0 with 1107/1107 checks. All **38/38 new assertion sites**
have a named killed witness in `mutants/coverage.txt`; individual failure receipts
are in `mutants/`. `mutants.txt` is the full driver verdict (driver rc 0).

| Mutation | Expected failing suite rc | New assertion failures |
|---|---:|---:|
| `no_round` | 2 | 22 |
| `early_round` | 2 | 2 |
| `late_round` | 2 | 20 |
| `retry_wrap` | 2 | 2 |
| `no_pacing` | 2 | 6 |
| `fixed_priority` | 2 | 1 |
| `command_monopoly` | 2 | 1 |
| `retry_monopoly` | 2 | 4 |
| `disabled_alloc` | 2 | 1 |
| `no_accept_bound` | 2 | 3 |
| `short_accept_bound` | 2 | 1 |
| `refusal_is_grant` | 2 | 47 |
| `obsolete_grant` | 2 | 10 |
| `obsolete_release_lost` | 2 | 3 |
| `no_response_bound` | 2 | 5 |
| `response_wrap` | 2 | 1 |
| `no_stale_swallow` | 2 | 3 |
| `no_stale_capacity` | 2 | 2 |
| `no_stale_drain` | 2 | 2 |
| `backoff_bypass` | 2 | 2 |
| `reallocate_owned` | 2 | 9 |
| `half_backoff` | 2 | 2 |
| `fresh_forever` | 2 | 1 |
| `declare_without_demand` | 2 | 7 |
| `source_alias` | 2 | 31 |
| `gate_without_ownership` | 2 | 15 |
| `no_requests` | 2 | 61 |
| `no_command_ready` | 2 | 221 |

The updated integration assertions were separately exercised using their actual
S10 and MP methods in a scratch selection main. Baseline and restored: **45/45,
rc 0**. Removing the periodic retry raises exactly the S10 all-source acquisition
and MP3 first-probe-success failures: **43/45, rc 1**. The driver returns 0;
see `top-retry-mutants.txt` and `check_top_retry.py`.

## Suite and gate table

All final entry points completed in the foreground, without piping their exit
status. The final full simulation sweep reports **1,014,990 checks, zero failing
suites**. The three ACMP suites and all five SRP suites are included below.

| Suite | Checks | rc |
|---|---:|---:|
| `acmp_listener` | 2544 | 0 |
| `acmp_nvm` | 349 | 0 |
| `acmp_talker` | 1107 | 0 |
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
| `./scripts/run_suites.sh` | 0 | `suites.txt`; 33 suites, 1,014,990 checks |
| `./scripts/lint_hdl.sh` | 0 | `lint.txt`; includes processor top |
| `make check` | 0 | `docs.txt`; diagrams, WaveDrom, links, matrices, parameters and freshness |
| `python3 scripts/gen_matrix.py --check` | 0 | 92 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | `portability.txt`; all listed tops and memory-mapping gate |
| `make -C tb/nvm_port figures` | 0 | `nvm-figures.txt`; all measured figures agree |
| `python3 tb/acmp_talker/retry_mutants.py --logs <scratch-logs>` | 0 | `mutants.txt`, `mutants/coverage.txt` |
| Focused S10/MP mutation driver | 0 | `top-retry-mutants.txt` |
| Parent first-probe driver against committed head | 0 | `parent-harness.txt` |
| `git diff --check` and clean worktree | 0 | verified at delivery |

Development failures were resolved: top lint detected a valid/ready combinational
loop in the initial arbitration expression; command eligibility is now independent
of valid. Integration S10/MP3 used the old probe-triggered allocation expectation
and checked before the new bound; they now grade paced automatic acquisition,
while the absent-allocator failure remains byte-exact. No failure was waived.

## Parent harness result and consumer work

Ran from `/tmp/pp128-a395/parent-probe-head`, using the actual donor head
`9476898b28ffc8f77b2aa5f873f3899a17287d3a` and the unchanged parent shim copied from the supplied read-only lane.
The parent shim SHA256 is
`965fbee050c985f767423bf63f2c0f0a507faf5ede7cc81e3a939bee963ba98e`.
The donor talker SHA256 is
`7a242dc78558f17c6fb89a7373d2d9a28a9f3382fc1bdf16fddadb84d3b38d0b`.

The original reproduction deliberately asserts the defect. The scratch oracle
changes those assertions to require automatic allocation and first-probe success,
and expands the post-availability walk to the stated sweep bound. No RTL behavior
is changed in that harness. `harness-oracle.diff` shows every oracle edit;
`run_parent_probe.py` preserves the supplied wiring runner and builds from copied
inputs. `reproduce_first_probe.cpp` retains the small adapted oracle only.

Result: **first probe status 0**, DA **91e0f0006818**, expected source SID and
VID; no probe-triggered ALLOC. The repeated-probe and warm-start controls also
return success. No premature declaration occurs before demand. See
`parent-harness.txt` for the committed head, sizes, hashes and full result.

The consumer lane should retain the real-shim regression with the 100 ms plus
sweep acquisition allowance, extend its real block count/conflict coverage, and
adopt this commit only after its own integration gates. Parent MAAP-shim/datapath
regression changes and pin adoption remain consumer work. This simulation does
not explain the reference peer's historical 6.877-second retry interval or
reconstruct the exact bench startup allocator history.

Large binaries and build trees remain under `/tmp`; `SCRATCH-ARTIFACTS.md` records
sizes and SHA256 values. The output directory contains no toolchain, environment,
installed package, tree export or file over 200 KB.
