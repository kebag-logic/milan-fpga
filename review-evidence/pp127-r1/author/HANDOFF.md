# [A394] Issue #127 handoff

Status: REVIEW READY. Committed with a clean working tree; all donor gates, all 36 mutation runs and the final-head expiry-window parent replay pass.

Final head: cf4e5c63ab12442c6c63d2bfe2bb64902674d55e

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
Branch: 127-srp-leaveall-at-transmit
Verified origin: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git
Verified starting head: 16be6768f710e79450aace277abacd6c2c3336e5

## Change and file locations

| Location | Change |
|---|---|
| hdl/srp/KL_srp_top.sv:1080 | Retain expiry intent; start a prepared round only after the previous applicant round completes. Coalesce repeated expiries until acceptance. |
| hdl/srp/KL_srp_top.sv:1102 | Preserve each walk completion across pending cadence ticks; drain full tables, including a table full before acceptance. |
| hdl/srp/KL_srp_top.sv:1167 | Timer expiry sets intent, not a registrar pulse. |
| hdl/srp/KL_srp_top.sv:1177 | A peer MSRP LeaveAll supersedes only an unaccepted own action; timer cadence is unchanged. |
| hdl/srp/KL_srp_encoder.sv:343 | A newly reserved or retained empty slot accepts sLA. Cancellation wins on the same edge. |
| hdl/srp/KL_srp_encoder.sv:592 | Collect both induced walks before serializing. A canceled empty reservation waits for content or a later own action; it never emits an empty MRPDU. |
| hdl/srp/KL_srp_talker_fsm.sv:570; hdl/srp/KL_srp_listener_fsm.sv:625 | Include same-edge sLA when selecting txLA for the new walk. Both registrars receive the accepted action. |
| tb/srp_top/sim_main.cpp:371 | Respect the serializer return-to-idle edge before issuing its next request. |
| tb/srp_top/sim_main.cpp:608, :665, :697, :794 | K/L/M/N phase, acceptance, supersession and congestion regressions. |
| tb/srp_stream_fsms/sim_main.cpp:476, :514 | Every applicant state also tested with coincident sLA/join. |
| tb/srp_top/mutants.py | Scratch-only controls and exact deliberate breakages with named failing assertions. |
| docs/architecture/10_srp_engine.md:488 | Define acceptance, cancellation, backpressure and event priority; retain the #108 deviation. |

No external processor interface changes. The internal encoder gains preparation,
cancellation and acceptance connections. LV + rLv semantics remain unchanged.

Reviewed: issues #127 and #108 including all comments, the assignment,
contribution/quality rules in hdl/README.md, docs/README.md and
docs/guides/hdl-engineer.md, SRP design including section 6.5, top/encoder/both
stream FSMs, SRP benches, and the permitted parent analysis and harness.
TAKEN: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/127#issuecomment-5860877319

## Phase-sweep case table

| Cases | Expected | Current result |
|---|---|---|
| Ready / Ready Failed, sources 0/3/7; offsets -50/-1/+1/+40/+80 ms from expiry | IN + Leave clears; inactive for the two-second hold | Pass |
| Same sources at +120/+199 ms | After accepted sLA: LV + Leave retains registration | Pass |
| Advertise / Failed sink Leaves at the same seven offsets | Same IN/LV distinction | Pass |
| Decoded Listener Leave -1/0/+1 clocks around acceptance | Clear before/on the edge; retain afterward | Pass |
| Peer LeaveAll -1/0/+1 clocks around acceptance | Supersede before/on the edge only | Pass |
| Peer LeaveAll -1/0/+1 clocks around real timer expiry | Same-edge/earlier intent canceled; later expiry remains new intent | Pass |
| Each MSRP peer type before preparation and while allocation blocked | No own action/flags/re-aging; deadline unchanged | Pass |
| MVRP control | Pending MSRP action survives | Pass |
| Reset, SID mismatch, malformed Leave, renewal/expiry | Pending reset cleared; matching and timers preserved | Pass |
| Encoder/TX blocked, full and already-full table, asymmetric walks | Deferred action, single flagged round, all declarations complete | Pass |
| Canceled preparation with no stream declarations | No empty MRPDU; later Domain content or own action consumes the reserved slot | Pass |

Final integration groups: K=217, L=86, M=67, N=13 (383 new checks); full integrated suite 1914/1914. Stream-FSM tally: 1215/1215 (128 additional same-edge checks).
Six-cycle no-storm counts: 4, 3, 3, 3, 3, 2; unchanged limits 18 total / 4 per cycle.

## Mutant table

Measured on the final implementation: all five positive controls pass; all 36
mutation runs finish with the required named assertion failing. Restoring the
timer-expiry registrar pulse causes 81 failures. The union of killed assertions
covers all 41 new integration check families (K1–K12, L1–L4, M1–M12, N1–N13).
Both same-edge applicant tables are also mutation-proven. The complete campaign
returns 0 (42/42 checks), and the mutated RTL source hashes remain unchanged.
Build errors and timeouts are never counted as kills.

| Deliberate breakage | Group | Failing checks | Named failing assertions |
|---|---|---:|---|
| `bad-listener-length` | phases | 1 | K12 |
| `peer-restarts-timer` | peer | 8 | M4 |
| `repeated-action` | congestion | 5 | N10, N12, N13, N4, N8 |
| `expiry-event` | phases | 81 | K1, K11, K12, K2, K4, K5, K9 |
| `before-slot` | edge | 30 | L1, L4 |
| `talker-no-own` | phases | 25 | K2, K4, K8 |
| `listener-no-own` | phases | 13 | K11, K6 |
| `talker-lost-txla` | stream FSMs | 12 | same-edge Table 10-3 states/messages |
| `listener-lost-txla` | stream FSMs | 12 | same-edge Table 10-3 states/messages |
| `talker-strict-lv` | phases | 24 | K2, K4 |
| `listener-strict-lv` | phases | 13 | K11, K6 |
| `listener-sid-ignored` | phases | 33 | K12, K3, K5, K8 |
| `talker-no-renewal` | phases | 1 | K7 |
| `listener-no-renewal` | phases | 1 | K7 |
| `talker-no-expiry` | phases | 1 | K8 |
| `listener-no-expiry` | phases | 1 | K8 |
| `pending-peer-ignored` | peer | 14 | M1, M10, M2, M3 |
| `encoder-peer-ignored` | peer | 20 | M1, M11, M12, M2, M3, M6, M7 |
| `mvrp-supersedes-msrp` | peer | 6 | M1, M2, M3 |
| `reset-retains-intent` | phases | 1 | K10 |
| `full-drain-missing` | congestion | 7 | N10, N13, N3, N4, N5, N6, N8 |
| `already-full-missed` | congestion | 1 | N10 |
| `round-completion-lost` | congestion | 1 | N13 |
| `own-flags-missing` | congestion | 4 | N10, N12, N5, N6 |
| `expiry-congestion` | congestion | 5 | N1, N11, N12, N2, N9 |
| `missing-registrar-edge` | edge | 38 | L2, L3 |
| `empty-canceled-pdu` | peer | 1 | M11 |
| `reserved-slot-not-reused` | peer | 1 | M12 |
| `renewal-congestion` | congestion | 1 | N7 |
| `leaveall-expiry-lost` | peer | 18 | M1, M10, M12, M2, M3, M5, M8, M9 |
| `expiry-outranks-peer` | peer | 1 | M10 |
| `repeated-expiry-queued` | congestion | 1 | N12 |
| `receive-priority-lost` | edge | 2 | L2 |
| `action-omitted` | congestion | 6 | N10, N12, N13, N3, N4, N8 |
| `preparation-before-slot` | peer | 22 | M1, M10, M11, M12, M5, M6, M8 |
| `table-one-short` | congestion | 8 | N10, N13, N3, N4, N5, N6, N8, N9 |


## Suite and gate table

Every production command is run synchronously, with output redirected to a file
and its actual return code checked. No command is piped. Generated builds remain
in the working tree or scratch; bounded logs and hashes are kept here.

| Suite / entry point | Result | rc |
|---|---|---:|
| make -C tb/srp_admission (all 1/2/3/5/8-source shapes) | Eight-source tally 991231/991231 | 0 |
| make -C tb/srp_decoder | 190/190 | 0 |
| make -C tb/srp_encoder | 556/556 | 0 |
| make -C tb/srp_stream_fsms | 1215/1215 | 0 |
| make -C tb/srp_top | 1914/1914 | 0 |
| ./scripts/run_suites.sh | All 33 suites; 1015233 checks; zero failing; UPC map passes | 0 |
| ./scripts/lint_hdl.sh | Every module, zero warnings | 0 |
| make check | 41 Mermaid, 18 WaveDrom, 920 links, matrices, parameters, staleness | 0 |
| python3 scripts/gen_matrix.py --check | 92 rows; zero untested | 0 |
| make -C tb/nvm_port figures | Pass on final RTL | 0 |
| ./syn/yosys/run.sh | Pass on final RTL | 0 |
| python3 tb/srp_top/mutants.py --output SCRATCH | 36/36 mutation runs killed; 41/41 integration families; 42/42 campaign checks | 0 |
| git diff --check | Clean | 0 |

The five SRP commands above are also invoked by the full suite entry point.
Environment: Verilator 5.052 (repository floor 5.050), Yosys and sv2v available.
Detailed invocation, size and SHA-256 records are in gate-results.json.

The first NVM figures attempt found missing historical objects, although all
measured figures agreed. Fetched origin refs/pull/13/head, exactly as CI requires;
no checkout, branch switch or tracked-file change. The initial result is retained
in nvm-figures-initial.log and gate-results-initial.json. Final results supersede
that incomplete-history attempt.

The exploratory mutation run exposed weak negative arms and led to stronger
malformed-frame, round-completion and repeated-expiry checks. Its restore check
correctly refused certification after the implementation advanced. Only the
settled final campaign is used as review evidence.

## Parent-harness result

Final replay was rebuilt against head `cf4e5c63ab12442c6c63d2bfe2bb64902674d55e` in
`/tmp/pp127-head-cf4e5c63ab12`. Both original source files were copied
from the permitted parent analysis directory; the originals remain unchanged.
The original C++ SHA-256 is
`a509453e76d47cb004cbdae263c6f0cc859b318dda07cd5b64360d9b7a2b7b1b`.

| Replay | Result | rc |
|---|---|---:|
| Original Python runner and original C++, baseline expectations | Expected rejection of the obsolete early-window expectation | 1 (expected) |
| Original C++ binary with `deferred` expectation argument | All phase and normal/peer controls pass | 0 |
| Scratch C++ adaptation anchored to actual timer expiry +1 ms | ACTIVE=0 throughout both two-second disconnect holds; renewal and no-renewal controls pass | 0 |
| `run_parent.py` aggregate, checking the three expected return codes | Pass | 0 |

The original Python runner is never given `deferred`: that option would rewrite
RTL. The argument is passed only to the already-built, unchanged C++ binary to
select the fixed phase expectations and skip the helper that waits for LV. The
inherited printed label `variant=defer registrar to join` names those expectations;
no RTL counterfactual is compiled. See parent-results.json for exact commands,
head, source/binary sizes and SHA-256 hashes.

At real deadline 14096 ms, Leaves at -50/-1/+1/+40/+80 ms see IN and clear ACTIVE.
At +120/+199 ms they see legitimate LV and retain ACTIVE. The original
`own_leaveall_race` helper waits for LV rather than for the timer: its stimulus
therefore moves from 14096 to 14200 ms with this fix and still demonstrates the
explicitly required LV retention. Its old `timer/LV` label now describes accepted
sLA, not timer expiry. This is not a blanket promise that every Leave stops.

The scratch adaptation tests the reported defect at deadline +1 ms: ACTIVE stays
0 for the full 2000 ms, with both renewal and no-renewal follow-ups. The exact
oracle change is parent-expiry-oracle.patch; parent-expiry-oracle.log contains
the passing replay. No parent source or artifact was edited.

Consumer work: adopt this pin and run the parent CRF integration regression that
counts frames and STREAM_STOP. Processor top-level ports are unchanged; there is
no parent interface migration. Parent consumer gates and hardware were not run.

## Review artifacts

- PR-BODY.md: ready-to-use description, starting with [A394] and closing #127.
- gate-results.json and bounded gate logs: every donor entry point returns 0.
- mutant-summary.log, mutant-results.json, mutant-assertions.log and
  mutant-source-sha256.txt: measured kills, raw-log sizes/hashes and source check.
- phase-results.log: measured phase and acceptance offsets from positive controls.
- parent-results.json, parent-*-oracle.log and parent-expiry-oracle.patch:
  original, expectation-only and deadline-anchored parent evidence.
- source-manifest.json: committed change sizes and SHA-256 hashes.
- artifact-manifest.json: bounded output artifact sizes and SHA-256 hashes.

Build products, tree copies and raw large logs remain outside this directory.
No push, pull request creation, merge, parent edit or hardware action was performed.
