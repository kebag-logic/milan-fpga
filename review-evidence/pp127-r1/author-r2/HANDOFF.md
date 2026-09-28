# Round 2 handoff

Status: REVIEW READY. Author: [A398]. Issue #127 / PR #130.

Final head: `00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c`.

Start: branch `127-srp-leaveall-at-transmit`, head `cf4e5c63ab12442c6c63d2bfe2bb64902674d55e`.
Origin verified: `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.

Scope follows the [round-2 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/127#issuecomment-5861796018),
the [internal review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/130#issuecomment-5861793313),
the [external review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/130#issuecomment-5861714667),
and the [parent consumer results](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/130#issuecomment-5861561819).
The complete issue and round-1 assignment were read. The manager explicitly
accepts the deadline-anchored oracle: the original LV-anchored helper exercises
legitimate post-sLA retention under the IN-registrar stop decision.

## Review responses

| Item | Change and file:line | Evidence |
|---|---|---|
| Both F1: C++ rule 11 | tb/srp_top/sim_main.cpp:334, :726, :829 split multi-declarators into one declaration per name | Final scratch-parent rule 11 rc 0; parent-rule11.log |
| Both F1: Python rule 12 | tb/srp_top/mutants.py:80, :89, :98, :131 annotate/document every public function; all lines within 120 columns | Final scratch-parent rule 12 rc 0; parent-rule12.log |
| Both F1: evidence inventory | tb/srp_top/sim_main.cpp:342 adds a 200,000,000-clock DUT bound; tb/srp_top/mutants.py:80 removes host deadlines; :89 applies explicit mutation patches without reading RTL for an oracle | Final inventory rc 0, unchanged ratchets: 76/77 unarmed, 10/10 unseeded, 0/0 unexplained source readers, 3/3 wall-clock suites |
| Both F2: supersession and intent | tb/srp_top/sim_main.cpp:882 through :1027 add O1–O5 to the default suite and guards group | New group 73/73; every required reviewer edit has an explicit campaign arm |
| Internal F3: canceled empty reservation | docs/architecture/10_srp_engine.md:513 documents the shared slot cost, conditional bounds and down-link limits; tb/srp_top/sim_main.cpp:1041 pins the link-up case | O7: 649 ms measured within 1200 ms; current TX interface has no abort operation |
| Internal F5 / external F3(a): coalescing | tb/srp_top/sim_main.cpp:1029 counts actual walk starts before another cadence opportunity | O6 requires own walk plus exactly one pending ordinary walk |
| External F3(b): arbitration | tb/srp_encoder/srp_tb_wrap.sv:35 exposes the preparation handshake; tb/srp_encoder/sim_main.cpp:1229 drives simultaneous MVRP tick/intake and MSRP preparation | O8: both VIDs accepted and emitted without another MVRP tick; default encoder 562/562 |
| External F3(c): count | tb/srp_stream_fsms/README.md:151 records talker 12/1203 and listener 12/1211 mutated failures, control 1215 | Both applicant-table mutation receipts retained |
| Both F4: replay sources | Portable run_parent.py plus original C++/Python and the accepted deadline patch are in this packet | SHA256 and sizes in parent-source-sha256.txt; deadline-anchored final-head replay rc 0 |

## New cases

The new `guards` group is part of the default `srp_top` entry point: 73 checks.
Encoder O8 contributes six checks to its default entry point. All stimuli use
real RX bytes and allocation/cadence handshakes; no DUT event is forced.

| Case | Committed location | Stimulus and required result |
|---|---|---|
| O1 | tb/srp_top/sim_main.cpp:882 | Peer Domain LeaveAll while preparation waits behind held TX request; cancellation survives busy encoder, with no own action/flags. |
| O2 | tb/srp_top/sim_main.cpp:896 | New timer expiry while canceled preparation stays allocation-blocked; newer intent produces exactly one own action/frame. |
| O3 | tb/srp_top/sim_main.cpp:911 | Peer decoded -1/0/+1 around join opportunity; no own action/flags, both registrar planes IN. |
| O4 | tb/srp_top/sim_main.cpp:951 | Peer decoded -1/0/+1 around retained-slot reuse; exact acceptance separately checked; flags only if uncanceled action occurred. |
| O5 | tb/srp_top/sim_main.cpp:987 | Talker Advertise/Failed Lv, sinks 0/7, decoded -1/0/+1 around acceptance; before/on clears IN, after retains LV. |
| O6 | tb/srp_top/sim_main.cpp:1029 | Multiple blocked cadence ticks coalesce to exactly one immediate ordinary follow-up walk. |
| O7 | tb/srp_top/sim_main.cpp:1041 | Empty canceled Domain-only reservation drains within Periodic plus Join: 649 ms observed, 1200 ms limit. |
| O8 | tb/srp_encoder/sim_main.cpp:1229 | MVRP join tick and VID push coincide with MSRP preparation; both VIDs accepted and deferred MVRP drain completes without another tick. |

The shared TX interface has no abort operation. The documented alternative
holds one standard slot and delays this encoder's MVRP drains. The link-up
bound is to content-driven encoding; serialization and external backpressure
add delay. Link-down waits for link-up content or an unsuperseded own action;
repeated peer cancellation can prevent a finite bound. Reset clears both the
encoder and slot pool. No production RTL changes are required in this round.

## Mutation campaign

The foreground command `python3 tb/srp_top/mutants.py --output /tmp/pp127-a398/mutants`
returned 0: seven positive controls, 56/56 killed arms, 49/49 covered assertion
families, 64/64 campaign checks. The checked-in `mutations/*.patch` files include
all 19 edits from both reviewer scripts, including their aliases. The seven
required previously surviving edits fail O1–O5; suggestions fail O6 and O8.
O7 is pinned by an additional content-drain arm. Every kill requires its own
named assertion, a completed tally and nonzero simulation result. A compile
error, missing tally or DUT budget exit cannot pass the driver.

All mutation and control logs are in `mutants/`; hashes and full sizes are in
`mutant-receipts.json`. Exact patch hashes and required assertions are in
`mutation-patches.json`. Deliberate mutant rc 2 is expected; positive suites
and the campaign itself return 0.

| Arm | Origin | Group | Required assertion | FAIL / total | Result |
|---|---|---|---|---:|---|
| `bad-listener-length` | round 1 | phases | K12: | 1/217 | KILLED, rc 2 |
| `peer-restarts-timer` | round 1 | peer | M4: | 8/67 | KILLED, rc 2 |
| `repeated-action` | round 1 | congestion | N4: | 5/13 | KILLED, rc 2 |
| `expiry-event` | round 1 | phases | K2: | 81/217 | KILLED, rc 2 |
| `before-slot` | round 1 | edge | L1: | 30/86 | KILLED, rc 2 |
| `talker-no-own` | round 1 | phases | K2: | 25/217 | KILLED, rc 2 |
| `listener-no-own` | round 1 | phases | K11: | 13/217 | KILLED, rc 2 |
| `talker-lost-txla` | round 1 | srp_stream_fsms | T QA txla=2: | 12/1203 | KILLED, rc 2 |
| `listener-lost-txla` | round 1 | srp_stream_fsms | L QA txla=2: | 12/1211 | KILLED, rc 2 |
| `talker-strict-lv` | round 1 | phases | K2: | 24/217 | KILLED, rc 2 |
| `listener-strict-lv` | round 1 | phases | K11: | 13/217 | KILLED, rc 2 |
| `listener-sid-ignored` | round 1 | phases | K5: | 33/217 | KILLED, rc 2 |
| `talker-no-renewal` | round 1 | phases | K7: | 1/217 | KILLED, rc 2 |
| `listener-no-renewal` | round 1 | phases | K7: | 1/217 | KILLED, rc 2 |
| `talker-no-expiry` | round 1 | phases | K8: | 1/217 | KILLED, rc 2 |
| `listener-no-expiry` | round 1 | phases | K8: | 1/217 | KILLED, rc 2 |
| `pending-peer-ignored` | round 1 | peer | M1: | 14/67 | KILLED, rc 2 |
| `encoder-peer-ignored` | round 1 | peer | M6: | 20/67 | KILLED, rc 2 |
| `mvrp-supersedes-msrp` | round 1 | peer | M1: | 6/67 | KILLED, rc 2 |
| `reset-retains-intent` | round 1 | phases | K10: | 1/217 | KILLED, rc 2 |
| `full-drain-missing` | round 1 | congestion | N6: | 7/13 | KILLED, rc 2 |
| `already-full-missed` | round 1 | congestion | N10: | 1/13 | KILLED, rc 2 |
| `round-completion-lost` | round 1 | congestion | N13: | 1/13 | KILLED, rc 2 |
| `own-flags-missing` | round 1 | congestion | N5: | 4/13 | KILLED, rc 2 |
| `expiry-congestion` | round 1 | congestion | N1: | 5/13 | KILLED, rc 2 |
| `missing-registrar-edge` | round 1 | edge | L3: | 38/86 | KILLED, rc 2 |
| `empty-canceled-pdu` | round 1 | peer | M11: | 1/67 | KILLED, rc 2 |
| `reserved-slot-not-reused` | round 1 | peer | M12: | 1/67 | KILLED, rc 2 |
| `renewal-congestion` | round 1 | congestion | N7: | 1/13 | KILLED, rc 2 |
| `leaveall-expiry-lost` | round 1 | peer | M9: | 18/55 | KILLED, rc 2 |
| `expiry-outranks-peer` | round 1 | peer | M10: | 1/67 | KILLED, rc 2 |
| `repeated-expiry-queued` | round 1 | congestion | N12: | 1/13 | KILLED, rc 2 |
| `receive-priority-lost` | round 1 | edge | L2: | 2/86 | KILLED, rc 2 |
| `action-omitted` | round 1 | congestion | N3: | 6/13 | KILLED, rc 2 |
| `preparation-before-slot` | round 1 | peer | M5: | 22/67 | KILLED, rc 2 |
| `table-one-short` | round 1 | congestion | N9: | 8/13 | KILLED, rc 2 |
| `my-expiry-pulse` | internal review | phases | K2: | 62/217 | KILLED, rc 2 |
| `my-join-edge-peer` | internal review | guards | O3: | 2/73 | KILLED, rc 2 |
| `my-cancel-eats-new-intent` | internal review | guards | O2: | 1/73 | KILLED, rc 2 |
| `my-edge-cancel-lost` | internal review | peer | M6: | 2/67 | KILLED, rc 2 |
| `my-la-outranks-leave` | internal review | edge | L2: | 2/86 | KILLED, rc 2 |
| `my-drop-join-during-wait` | internal review | guards | O6: | 1/73 | KILLED, rc 2 |
| `my-no-walk-at-sLA` | internal review | congestion | N6: | 5/13 | KILLED, rc 2 |
| `my-reuse-flags-ignore-cancel` | internal review | guards | O4: | 1/73 | KILLED, rc 2 |
| `r-expiry-pulse-restored` | external review | phases | K2: | 62/217 | KILLED, rc 2 |
| `r-cancel-latch-dropped` | external review | guards | O1: | 1/73 | KILLED, rc 2 |
| `r-cancel-consumes-new-intent` | external review | guards | O2: | 1/73 | KILLED, rc 2 |
| `r-join-start-guard-dropped` | external review | guards | O3: | 2/73 | KILLED, rc 2 |
| `r-sink-receive-priority-lost` | external review | guards | O5: | 2/73 | KILLED, rc 2 |
| `r-join-coalesce-dropped` | external review | guards | O6: | 1/73 | KILLED, rc 2 |
| `r-la-only-emission-lost` | external review | peer | M12: | 1/67 | KILLED, rc 2 |
| `r-collect-blocks-pushes` | external review | congestion | N6: | 4/13 | KILLED, rc 2 |
| `r-accept-edge-drain-lost` | external review | congestion | N10: | 1/13 | KILLED, rc 2 |
| `r-reuse-without-action` | external review | peer | M12: | 1/67 | KILLED, rc 2 |
| `r-mvrp-start-during-prepare` | external review | srp_encoder | O8: | 5/562 | KILLED, rc 2 |
| `canceled-content-never-drains` | bound | guards | O7: | 1/73 | KILLED, rc 2 |

## Parent replay and gates

All replay and parent-gate receipts below identify `00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c`.
The trusted parent `931f396ec9f13271e9e67b755e18833d0024f234` was copied to
`/tmp/pp127-a398/parent`; the read-only parent checkout was not edited.
Its initialized gptp submodule stays at `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.
The `protocol-processor` directory contains the candidate's complete tracked
source snapshot with a Git-directory pointer to this lane for tracked-file
inventory. A direct directory symlink is rejected by Git's submodule traversal;
the scratch copy avoids that rejection. The scratch parent gitlink index points
to the candidate head. The three checkers and all ratchets are unchanged;
checker hashes are in `parent-gates.json`.

| Parent command (from scratch parent root) | rc | Result / receipt |
|---|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | 159 translation units; multi-declarator and every other zero ratchet remain 0; parent-rule11.log |
| `python3 scripts/check_py_idiom.py` | 0 | 270 modules; unannotated/undocumented public functions and over-long lines all 0; parent-rule12.log |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 76 <= 77 unarmed, 10 <= 10 unseeded, 0 <= 0 unexplained source readers, 3 <= 3 wall-clock suites; parent-evidence.log |

The assignment reserves the full 11-command consumer set for the manager.
Only the three required repair gates are claimed here. Parent pin adoption,
the CRF frame/STREAM_STOP regression, current-dev integration, hosted checks
at this unpushed head and physical disconnect measurements remain manager work.

The portable command is `python3 run_parent.py PROCESSOR_TREE SCRATCH_DIRECTORY`,
with Verilator 5.050 on PATH. It uses only the sources in this packet and the
supplied processor tree. The actual scratch path was
`/tmp/pp127-a398/parent-replay-final`. `parent-results.json` records every child
command, status, input/build-log/binary hash and size. The aggregate runner
returned 0; `parent-replay-summary.log` records the complete driver result.

| Replay | rc | Meaning |
|---|---:|---|
| Original Python runner and unmodified C++ | 1 (expected control) | Its helper anchors on LV at 14200 ms and retains ACTIVE; its old early-window phase expectation then fails. This is disclosed, not counted as the accepted proof. |
| Original compiled C++ with `deferred` expectation argument | 0 | Selects fixed phase expectations and the unchanged received-LA/type-scope controls; no RTL counterfactual is built. |
| Deadline-patched C++ through original Python runner | 0 | At deadline 14096 ms, Leave at +1 ms sees IN and clears ACTIVE for every clock of the 2000 ms hold; renewal cannot be revoked by stale expiry and no-renewal stays stopped. |

The deadline phase sweep stops at offsets -50, -1, +1, +40 and +80 ms;
+120 and +199 ms see legitimate LV and retain ACTIVE. This matches the
manager's accepted distinction. `deferred` is passed only to the original
compiled executable, never to the Python runner (whose option would create
an RTL counterfactual). The replay measures the SRP ACTIVE licence; it has
no AVTP framer or hardware. No production source is edited for either replay.

Original sources are byte-identical to the permitted analysis packet.

| Published replay and validation source | Bytes | SHA256 |
|---|---:|---|
| reproduce.cpp | 7711 | `a509453e76d47cb004cbdae263c6f0cc859b318dda07cd5b64360d9b7a2b7b1b` |
| run_reproduction.py | 2479 | `d7ecb4cef397a6e53b8a6287ef05ff1b956619ec25556e0c4f94e4a3934a3a1c` |
| parent-expiry-oracle.patch | 3426 | `d99c2df3e6b137a224c30867a163a32c3590606c2865c9b9101f597e67ce422a` |
| reproduce-deadline.cpp | 6736 | `a3ee0057719c7032a5d30e9af82c8709397c5b45b7d2a125d144cb0f1aeffe9f` |
| run_parent.py | 3297 | `241b6e6e4a4bd05f2c301704d85b9e3a859721139988c786bc80a80b7debf84a` |
| run_gates.py | 1612 | `24a45fb9f595556fe9d00d104a0a169096d7a599cb6906b63a291f04f88cecfc` |

The two binaries are over 200 KB and stay in scratch; their sizes and SHA256
are recorded in `parent-results.json`. No toolchain, installed package,
virtual environment or tree export is placed in this packet.

## Suites and gates

The full donor entry point `./scripts/run_suites.sh` returned 0:
33 suites, 1,015,312 checks, no failures or unreadable tallies. A repeated full
`srp_top` run is preserved separately in `srp-top-full.log`: 1987/1987,
no-storm frame counts 4,3,3,3,3,2 and Ready in all six cycles, with the original
limits unchanged. Commands run
in the foreground with stdout/stderr redirected to receipts, never through a
pipeline. Pinned Verilator 5.050 is used with build parallelism capped at eight.

| Suite | Checks | Result |
|---|---:|---|
| acmp_listener | 2544 | PASS, rc 0 |
| acmp_nvm | 349 | PASS, rc 0 |
| acmp_talker | 839 | PASS, rc 0 |
| adp_engine | 533 | PASS, rc 0 |
| aecp_notify | 10 | PASS, rc 0 |
| ca_originator | 16 | PASS, rc 0 |
| desc_mem_guard | 78 | PASS, rc 0 |
| desc_store | 584 | PASS, rc 0 |
| dispatch | 211 | PASS, rc 0 |
| dyn_state | 89 | PASS, rc 0 |
| event_router | 81 | PASS, rc 0 |
| lsn_admit | 18 | PASS, rc 0 |
| maap | 75 | PASS, rc 0 |
| nvm_port | 136 | PASS, rc 0 |
| originator | 104 | PASS, rc 0 |
| pp_top | 7751 | PASS, rc 0 |
| prng | 76 | PASS, rc 0 |
| release_merge | 18 | PASS, rc 0 |
| resp_buf | 64 | PASS, rc 0 |
| rx_slots | 130 | PASS, rc 0 |
| rx_validator | 393 | PASS, rc 0 |
| scoreboard | 3705 | PASS, rc 0 |
| side_port | 368 | PASS, rc 0 |
| srp_admission | 991231 | PASS, rc 0 |
| srp_decoder | 190 | PASS, rc 0 |
| srp_encoder | 562 | PASS, rc 0 |
| srp_stream_fsms | 1215 | PASS, rc 0 |
| srp_top | 1987 | PASS, rc 0 |
| timer_map | 1360 | PASS, rc 0 |
| timer_service | 48 | PASS, rc 0 |
| tx_arbiter | 66 | PASS, rc 0 |
| tx_slots | 95 | PASS, rc 0 |
| ucpu | 386 | PASS, rc 0 |

All donor entry points passed. The NVM figure gate re-measured its historical
forms and every figure; portability elaborated all 35 listed tops and passed
the AECP Xilinx RAM-inference assertions. `gate-results.json` records exact
commands, return codes, complete-log sizes and hashes.

| Entry point | rc | Receipt |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | suites.log |
| `./scripts/lint_hdl.sh` | 0 | lint.log |
| `make check` | 0 | check.log |
| `python3 scripts/gen_matrix.py --check` | 0 | matrix.log |
| `make -C tb/nvm_port figures` | 0 | nvm-figures.log |
| `./syn/yosys/run.sh` | 0 | portability.log |

The measured table is committed in tb/srp_top/README.md:298. The final
`make check` rerun returned 0 after the documentation updates; check-final.log
and gate-results.json retain the result.

## Final state

Commit: `00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c`

Subject: `test(srp): cover LeaveAll cancellation races and restore consumer gates`

The commit has a one-line subject, no body and no trailers. The branch is
`127-srp-leaveall-at-transmit`; origin remains the verified repository URL.
The working tree is clean. All 50 production files match the starting head
byte for byte (`rtl-integrity.json`): LV + rLv and #108 are unchanged.
All validation ran in foreground processes; positive suites and gates return 0.
Deliberate negative simulations and the original historical oracle retain their
expected nonzero results. No push, PR edit, merge, hardware action or edit to
another checkout was performed. `PR-BODY.md` retains its required first line
and closing reference, with a new Round 2 section.

Notice text: `[A398] REVIEW READY 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c`.
The packet inventory is `SHA256SUMS.txt` (hash, size, relative path).
