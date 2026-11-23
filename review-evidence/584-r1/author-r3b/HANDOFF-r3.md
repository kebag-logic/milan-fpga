Status: REVIEW READY for correction re-review; owner backing disposition remains pending.
ETA: complete; manager may publish the committed head and packet.

[A818] #584 / PR #975, round 3

Candidate: `599c79af9cfe242bc3d60dd1c80f3e8d57cca12e`, branch `pf-584-1`.
Round-2 review head: `64d539f12532b2591f734b8e756f8a9358bb742c`.
PR base remains `dev-soft-core`; original source base `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`.

The resumed session found a clean tree with both correction commits already present. It preserved them, checked their changes and execution evidence, and completed the packet. No push, PR edit, merge, hardware operation or additional TAKEN comment was made. The resumed session confirmed no round-3 REVIEW READY comment existed before publication.

## Pending owner disposition

The owner's decision remains pending. Port 0's cluster is backed by TDM32 slot 0, standing for the first TDM8 channel; ports 1-7 own `Unrouted S<p>`. No input cluster is loopback-backed, and the 8x8 loopback lane is disabled. D8, D10, the ownership page, the changelog and PR body state this. This packet does not approve that deviation or authorize merge.

## Changes and reasons

| Finding / residue | File:line | Change and reason |
|---|---|---|
| R894 F2-R2 / R893 F6 | `tb/verilator/milan_dp_render/sim_ship8_render.cpp:185`, `:1156`, `:1215` | The recovery record grades the entire transition: permitted pre-loss audio until the epoch closes, closed-epoch silence, leading silence after rebind, and the first and every subsequent nonzero word. It checks source identity, event freshness/order, gaps, zero tail, pad and framing. |
| Same freshness finding | `tb/verilator/milan_dp_render/sim_ship8_render.cpp:1262`, `:1293` | Collection begins before unbind and at reset release, respectively, and continues through bind and the lead interval. The later steady windows remain. Decoder resynchronization excludes the interrupted partial frame; a bind fall must close within one PDU. |
| Freshness sensitivity | `tb/verilator/milan_dp_render/sim_ship8_render.cpp:341`, `:566`, `:1269`, `:1305`; `ship8_mutants.py:93`, `:176` | Two explicit leg modes replay pre-loss/pre-reset samples with fresh timestamps inside the recovery interval. Each must fail its own named FRESHNESS check. |
| Additional reviewer probes banked | `tb/verilator/milan_dp_render/ship8_mutants.py:80` | Zero-tail, stream-epoch-mask and REMOVE-as-ADD faults join the projection/adapter/bus campaign. |
| R4 | `sw/builder/endstation_builder.py:6046` | Add the `Unrouted S<p>` name example only when an input pool is unrouted. All unaffected configurations' generated documents remain byte-identical. |
| R5 / RS2 | `CHANGELOG.md:72`, `:79` | Name port 0's binding and explicitly include the TDM32 interpretation among the three pending points. Slots 1-31 stay zero; unrouted mappings reach no slot. |
| RS1 | `docs/testing/TESTING.md:431` | Restore the timing paragraph's referent before the ship8 paragraph. |
| RS3 and coverage statement | `sim_ship8_render.cpp:41`; `docs/testing/TESTING.md:748` | State the stream-table taps actually graded, the continuous recovery interval and the fresh-gate isolation limit. |
| R894 F5-R2 / R893 F7 / R6 | `receipts/f5/index-audit.md`, `round2-INDEX-corrected.md`; `receipts/tools/pubcheck.py`, `verify_packet.py` | Correct the historical nested index using immutable published bytes, explain redaction without raw host-path examples, normalize before indexing, and independently check all current hashes and publication invariance. |

Local commits (one-line subjects, no bodies or trailers):

- `31d40c0eb47b40fb1489780e247a731a8acdf743`: continuous recovery grading, replay controls and three additional plants.
- `599c79af9cfe242bc3d60dd1c80f3e8d57cca12e`: conditional build-plan wording and documentation residues.

No RTL, firmware, configuration or gitlink delta from round 2. No reroute was required. See `receipts/source-identity.txt`.

## New checks and planted faults

| Check / boundary | Planted fault | Required failing words / result |
|---|---|---|
| Every post-rebind sample and actual first nonzero sample | `--defect-stale-rebind`, pre-loss samples during recovery | `B3 FRESHNESS: from the rebind, every rendered slot-0 word`; the first-frame check also fails |
| Every post-reset/rebind sample | `--defect-stale-reset`, pre-reset samples during recovery | `Z3 FRESHNESS: from the rebind, every rendered slot-0 word` |
| Physical projection | input key 0 projects beyond the lane | `P1 POWER-ON: render keys 0-9`; `P3 POWER-ON RENDER: slot 0 carries stream 0 channel 0` |
| Unrouted isolation | input port 1 projects onto key 2 | `U3: render keys 0-9`; `U4 RENDER: slot 0 carries stream 3 channel 2` |
| Adapter | first write reads the next key | `P3 POWER-ON RENDER: slot 0 carries stream 0 channel 0`; `R1 RENDER: slot 0 carries stream 0 channel 5` |
| Bus framing | serialize eight slots in the 32-slot frame | `P3 POWER-ON RENDER: slots 1-31 carry zero`; `R1 RENDER: slots 1-31 carry zero` |
| Bus guard | bind bus width to render width | elaboration refuses `does not match $clog2(BUS_SLOTS_P*SLOT_BITS_P)` |
| Zero tail | copy slot 0 into remaining slots | `P3 POWER-ON RENDER: slots 1-31 carry zero` |
| Stream-qualified epoch | any stream's bind fall closes the lane | `B1: a bind fall on stream 5, which the lane does not render, opens no epoch` |
| REMOVE | execute REMOVE as ADD | `X2 SILENCE: all 32 slots are digital silence` |
| Publication invariance | synthetic raw host prefix | `publication rewrite changes bytes`, `raw host prefix remains` |
| Receipt authentication | same-length content mutation, size mutation, omitted file | `HASH_MISMATCH`, `SIZE_MISMATCH`, `UNINDEXED_FILE` in the packet-checker selftest |

`receipts/rtl/ship8-mutants.txt` records the clean control and all ten negative controls: 11/11 PASS. Preliminary full replay logs are `rebind1.log` and `reset1.log`; the exact-head campaign independently catches both modes. The clean recovery record contains 357 bind-loss frames and 492 reset frames. After one pre-loss frame the bind-loss record is silent until rebind; reset is silent from release. No stale/foreign word, reordered event, framing error or gap occurs in the clean recovery records.

The render stage's flush masks a separately forced-open `tdmr_fresh_w`; those isolation probes pass, and are explicitly not claimed as mutation catches. `receipts/rtl/fresh-gate-probes.md` gives the precise planted diffs, source sizes/hashes and logs. The replay controls prove detection when a stale word reaches the pins.

## Gate table

All new execution receipts below use head `599c79af` unless explicitly described as preliminary or carried.

| Gate / command | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/milan_dp_render ship8` | PASS, 130 checks, 0 failures | `receipts/rtl/ship8.log` |
| `make -C tb/verilator/milan_dp_render ship8-mutants` | PASS, 11/11 | `receipts/rtl/ship8-mutants.txt` |
| `make -C tb/verilator/milan_dp_render` | PASS: 263, 79 and 130 checks; zero failures; 5/5 leg-side controls | `receipts/rtl/milan_dp_render-suite.txt` |
| `ci_builder_legs.py run 0/1 -- ... test_builder.py --require-elaboration --require-rv32` | PASS: union covers 113 gates exactly once; two existing arms NOT RUN (make-profile arm and physical calibration report) | `receipts/gates/builder-union.txt`, `builder-leg0.log`, `builder-leg1.log` |
| Five configurations, both placements: generated actual-byte comparison | PASS: 153/155 artifacts identical to round 1. Only 8x8 `build_plan.md` at both placements adds the 17-byte name example. All 1x1/1if TDM8 and Arty artifacts, every model ID and every binary unchanged | `receipts/builder/artifact-comparison.txt`, `final-artifacts.json`, `r3-artifacts.json` |
| Docs workflow commands, including docs/style/inventory/census/source-list/selftests | 99/103 rc 0. Four hosted-environment commands fail locally: missing installed-runner location and missing event path (three commands), as in round 2. Not claimed green | `receipts/docs/workflow-summary.txt`, `receipts/docs/commands/` |
| Historical nested index audit against `e3127c91` | PASS: corrected round 1 80/80; corrected round 2 16/16 | `receipts/f5/audit-results.txt` |
| Packet hash coverage and publication rewrite | PASS: all current receipt rows authenticate; every packet file survives the publication rewrite unchanged | `receipts/INDEX.md`, `receipts/f5/publication-check.txt`, `index-selftest.txt`, `publication-selftest.txt` |
| Source/pins/commit format | clean; required initialized submodules pinned and clean; external unused/uninitialized | `receipts/source-identity.txt` |

The docs command log exceeding 200 KB is represented by its size, SHA256 and final verdict excerpt. Build trees, toolchains and binaries stay outside the output packet.

## Carried evidence and limits

`receipts/carried/README.md` identifies the immutable publication and exact source files copied here. These are prior runs, not new measurements:

- Round 1's full 65-suite sweep, firmware bank and loopback-on nxn8 control.
- Round 1's three 8x8/1if routes: all close against #818; best setup/hold +0.363/+0.036 ns; device fit retained.
- The recorded per-image control-memory growth/debt, saved-state service/capture measurements and unchanged owner budget checks.
- Round 2's twin/ledger run. No affected implementation or generated model changes in round 3; the artifact-byte comparison substantiates that carry.

Hosted checks, local workflow replica, the hosted ship8 runtime window, independent re-reviews and the final merge-candidate bank remain manager duties. The owner disposition is still open. No physical evidence was obtained in this lane; the manager reruns the bench scenarios after merge. The existing all-fabric console-listing budget overrun remains recorded, outside this correction.

## Manager handoff

Push only after accepting this packet; update the PR from `PR-BODY.md`, archive these already-normalized receipt bytes, and obtain both delta reviews. The author does not approve its own work or assemble the reviewer-owned completion ledger. Await the owner's backing disposition before merge. If it requires loopback-backed input clusters, reopen the affected implementation and gates.

REVIEW READY comment: posted once on #584, [issuecomment-7086448470](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-7086448470). Its exact text is `REVIEW-READY.md`.

REVIEW READY 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e
