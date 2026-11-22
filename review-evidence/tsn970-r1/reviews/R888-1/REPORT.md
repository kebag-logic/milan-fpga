[R888] NEGATIVE - exact head 5d14a6d816a43a49299172a34e3eeaea44c267c6

Round R888-1 independently applied all five lenses to stack PR #35 and its parent consumer. One MAJOR finding remains open. The implementation passes the focused functional checks, but the claimed conformance of the shortened randomization windows is not accepted.

Scope and authorities

The stack tree is `2112d0526c8f5ab49440e89202af526b1b9b65fc`, compared with `715589c1db7cf67e2f3259fd7083ebc7f0923376`. The parent is `27495a06d5569336a098da20381ced3e331ba665`, tree `5b8c0565c3347989b1af6f38d2479007d2c5c1f5`, compared with the reviewed flip head `dd163e41`. Its `third_party/tsn-c-stack` gitlink is exactly the reviewed stack head. The public issue identifies the parent branch as `pf-970-1`; `970-first-advertise` is the stack branch. Commit identities govern this review.

Reconstruction used the supplied operating instructions, stack CONTRIBUTING, README, coding/verification/porting/requirements documents, parent AGENTS/CONTRIBUTING and docs/README, then the [frozen issue acceptance and public scope discussion](https://github.com/kebag-logic/milan-fpga/issues/970). The interface authorities included parent REQUIREMENTS, FR_NFR, MAILBOX_CONTRACT and MAILBOX_SPLIT. The relevant Milan and IEEE clauses were read directly before the independent diff pass. Both commit ranges and histories were examined, followed by the [published author packet](https://github.com/kebag-logic/milan-fpga/tree/134345784d83af67316c82ac8495d89a489e604e/review-evidence/tsn970-r1/author-r1), particularly HANDOFF sections 2-5 and receipts. All 154 published packet entries match their published SHA-256 values.

The standards read were [Milan v1.2](https://avnu.org/resource/milan-specification/), printed pages 101-105, Tables 5.49-5.51 and 5.6.3.5.2/.3/.4/.5/.7/.9, and [IEEE 1722.1-2021](https://standards.ieee.org/ieee/1722.1/6670/), 6.2.2.15/.16, 6.2.4.2.2 and 6.2.5, printed pages 53, 55-57. The PDF identities are recorded in `receipts/authority-identities.txt`. No standards PDF or extracted standards text is republished.

Finding R888-1-F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs

Artifact: stack `include/adp.h:87`, `src/adp.c:53`, `src/adp.c:265`, `tests/test_adp.cpp:476`, `tests/mutations.json` entries `startup-range-two-seconds` and `link-up-range-four-seconds`, `docs/PORTING.md:194`, and generated MFDISC-01. Parent artifacts: `sw/firmware/ctrl/test/test_adp.cpp:562`, `sw/firmware/ctrl/test/adp_walk.cpp:268`, `docs/design/MAILBOX_SPLIT.md:537`, and `docs/reference/FR_NFR.md:415`. The PR body's range-conformance claim is also affected.

Authority and ruling: Milan requires the per-interface state machine described in 5.6.3. Its startup transition specifies a random draw over 0-2 s, and its DOWN/LINK_UP transition specifies 0-4 s. Table 5.49 explains that DELAY spreads advertisements when devices start together, avoiding storms. I read these as prescribed randomization intervals, not merely ceilings permitting an implementation to concentrate every draw into an arbitrarily small subinterval. Thus a uniform draw restricted to 0-0.5 s is not accepted as conforming to those prescribed intervals merely because every result is numerically inside them. The implementation removes all probability above 500 ms: three quarters of the startup interval and seven eighths of the LINK_UP interval are unreachable.

IEEE 6.2.4.2.2 explicitly specifies a uniform distribution across its own interval. Milan supplies the PAAD-AE replacement state machine and timer values; importing the IEEE machine's exact timer formula into Milan would be wrong. That distinction does not establish permission to replace Milan's explicitly stated intervals. IEEE 6.2.5 governs interface transmission and provides no such permission either. This ruling rests on Milan's own transition requirements and its stated storm-avoidance purpose. Also, the 2 s startup rule is in 5.6.3.5.2, not Table 5.50 as the PR body's combined citation implies.

Evidence: `receipts/draw-distribution.txt` comes from `draw_probe.c`, compiled separately against the actual base and head cores and driven through their exported APIs with 65,536 distinct seed inputs. The base visits all 4,001 LINK_UP millisecond values and all 2,001 startup values. The head visits only 501 values in either case. Same-millisecond unordered pairs rise from 541,988 to 4,315,733 for LINK_UP, and from 1,082,405 to 4,315,733 for startup, approximately 8x and 4x. This measures concentration under the stated input population. It neither models a complete network nor proves an actual network collapse. The unchanged xorshift generator still provides randomness; retaining randomness alone does not preserve the original spreading interval.

Impact: the sub-second criterion is obtained by changing the protocol's randomization contract and increasing concurrent advertisement concentration. The new literal oracles and mutation plants enforce that choice, including treating restoration of the stated Milan maxima as defects. Their successful execution cannot validate the normative premise. The parent service-budget receipts establish individual endpoint execution costs; they do not establish storm handling for many entities sharing a link. Documentation presents the disputed interpretation as established conformance.

Required outcome: resolve the conflict between the frozen one-second acceptance and the cited randomization requirements publicly before merge. Preserve the specified startup/LINK_UP randomization intervals, or supply an applicable authoritative interpretation permitting the narrower intervals and evidence addressing their storm-avoidance consequences. A local acceptance change alone cannot amend an external standard. Update the implementation, independent oracle, plants and conformance claims consistently with the resolved contract. Do not address this by silently changing acceptance, weakening a test, or asserting that a value inside the interval proves an equivalent distribution.

Verification: re-read the governing interpretation; exercise startup and LINK_UP across the permitted range using independent seed populations and literal bounds; test concurrent entity starts with a declared population/load and observable queue/drop/discovery criteria; retain DISCOVER/TMR_ADVERTISE/GM_CHANGE behavior, GM field freshness, both GM orders, indices and backpressure regressions; regenerate documentation and rerun affected stack and parent gates at the corrected exact head.

The attribution covers each lens: Conformance owns the prescribed interval; RTL owns timer/FSM architecture and interface timing; Robustness owns concurrent-start concentration; Tests owns the oracle that encodes the disputed interval; Docs owns the conformance claims and requirement derivations. All five therefore remain unclean while F1 is open. No separate wording-only RESIDUE was identified in the reviewed source-comment delta.

Independent executable checks

| Check | Result and receipt |
|---|---|
| Stack hosted tests | 10/10 binaries pass; registration has 459 instances and 185 declarations. `receipts/stack-host.log`, `stack-generated.log` |
| Stack coverage | Ratchet passes: 100% lines/branches after the existing exclusions. ADP raw coverage is 209/211 lines and 99/106 branches. No exclusion or ratchet changed. `stack-host.log` |
| Stack Debug and Release RV32 | Both link and execute smoke checks successfully; no unresolved final symbols. `stack-rv32.log` |
| Static analysis | Project checks pass, including the two independent range tests introduced by the second stack commit. `stack-static.log` |
| Comments, licence, port contract | Pass. `stack-contracts.log` |
| Seven changed stack plants | Five new and two restated plants caught by their registered assertions; no escapes or errors. `selected-plants.log`, `stack-plants-raw/` contains individual logs, XML, markers and results |
| Stack generators | Ran `traceability.py --write` and `test_inventory.py --write` in a disposable exact-head copy. REQUIREMENTS, TRACEABILITY and TESTS are byte-identical to the reviewed head. `regeneration.log` |
| Parent ADP and walk | 58 ADP tests and 41 state-table tests pass. `parent-adp.log`, `parent-walk.log` |
| Parent changed/restated plants and GM control | Nine plants, all 13 registered kill obligations caught, including G3 restart and G4 ignored-GM defects. `parent-plants.json` and `plant-*.log` |
| Draw population | Base/head public-API comparison, as described in F1. `draw-distribution.txt` |
| Exact source restoration | Stack, parent and five initialized dependency trees have exact tracked bytes, modes and index records. All six parent gitlinks match. The unused external checkout is uninitialized. `exact-bytes.json` |

The first stack mutation invocation used an unsupported comma-separated selection and exited without a selected campaign. It is retained in `stack-plants.log` and identified as an invocation error in `stack-results.json`. The corrected seven-entry disposable registry ran the unchanged campaign driver successfully. This initial invocation is neither a product failure nor a mutation catch. Expected nonzero exits in base-reproduction and plant receipts are the intended failing assertions.

Cause and grandmaster checks

The parent G tests compiled against base stack `715589c1` reproduce the cause independently: G1 latest 3,990 ms after LINK_UP, G2 startup 1,981 ms, G3 early GM change 3,649 ms, G4 later GM change 3,364 ms. Exactly those four tests fail their one-second assertions; the GM semantics are not the cause of the delay. At the reviewed head their latest first advertisements are respectively 499, 496, 457 and 421 ms; G4's follow-up advertisement arrives within 3,994 ms of the GM change. See `parent-base-reproduction.log` and `parent-adp.log`.

The stock parent fixture advertises eight sources and eight sinks and uses the default one-interface mailbox. A supplemental disposable fixture changes only the two advertised counts to one and reruns exactly the four G tests against base and head; `shape-one-base.log` and `shape-one-head.log` record the one-source/one-sink case. These host tests model prompt service, not physical port timing.

Inspection of `src/adp.c:282`, `adp_build`, and parent `adp_mbx.c` confirms that GM_CHANGE in DELAY leaves the current delay running, and the eventual frame samples current GM/domain data. GM_CHANGE in WAITING starts the retained 0-4 s delay, then sends the new GM and next index. G3 and G4 exercise both orders, with named plant kills. The draw is the sole intentional first-advertisement wait in the core; the adapter does not add an asCapable, GM-settle or debounce prerequisite. DISCOVER and TMR_ADVERTISE retain the general delay kind. A18/A20 retain departure ordering and link-loss cancellation. The appended draw enum preserves the existing numeric values; the largest multiplication in the draw remains within uint32_t. No new RTL, CDC, reset or mailbox layout change appears in either diff.

Public parent and stack evidence

The authoritative source execution evidence is the author's published receipts. `receipts/evidence-audit.txt` independently reconciles their identities and summaries. The stack packet records 28 successful validation gates, 482/482 plants and both RV32 configurations. The final parent packet records all four firmware shards at `27495a06`, 75 passing suite verdicts, 832/832 control plants, and successful AECP/SRP campaigns. This review reran the focused ADP checks above, not those complete parent banks.

The twin, map/plant checks, firmware coverage, split boot, images and CPU legs were published at `b000faa5`. Inspection of the subsequent parent commits confirms only test and documentation changes; no image input changes. Published coverage covers 40 files. The split-boot receipts explicitly distinguish real simulation assertions from stand-in register values; their apparent physical gPTP checks do not prove hardware behavior.

The platform ledger passes at all four published points, with 45/46/58/63 RAMB36, unchanged from base and subject to each point's own ledger. Eight platform/size-fixture image pairs have successful relinks and canonical comparisons; the differing production input is `adp.o`, with `enter_delay` growing from 176 to 180 bytes. Twelve budget-image pairs have base/head hashes. Their attempted canonical comparison/relink receipts fail for missing map paths: no successful canonical comparison of those twelve is claimed here. This does not invalidate the separately published CPU executions or extend the eight successful image comparisons.

Both 1x1/1if and 8x8/1if CPU legs pair 63/63 probes, with zero changed verdicts and zero misses. Their largest differences are -0.074 ms and +0.097 ms against 20 ms. The four grader outputs are byte-identical between base and head. FR_NFR's ADP 30 ms composed row bound is unchanged; the new 50 ms derivation does not move it. Published first-frame observations of 91.142 and 89.366 ms are CPU/mailbox simulation measurements using one deterministic draw, not physical link-up measurements. The submodule row, links, diagram source/SVG/PNG and manifest carry the reviewed stack pin; the rendered diagram was inspected.

The parent docs steps report 104/104 successful steps. Builder legs report success with explicit NOT RUN arms: the ineffective MAKEFLAGS mutation and the absent physical-calibration build report. They remain limits. Physical calibration NOT RUN and field skips are not hardware proof.

The exact-head [hosted stack run 45031015936](https://github.com/kebag-logic/tsn-c-stack/actions/runs/45031015936) has executed successful `quality` and `bare-metal` validation steps, with no skipped steps in the returned job records. The workflow explicitly checks out the pull request head SHA. `receipts/public-state.json` records the read-only inspection. Hosted/act acceptance remains the manager's responsibility.

Prior findings and independence

The independent verdict and five-lens ledger were written before checking prior reviewer findings. The subsequent public PR timeline contained only two review-start notices; the review and inline-thread queries returned empty lists. Therefore no prior public FINDINGS existed to resolve or retain at the time checked. No other reviewer's report was read. No private author material, management checkout material, source fixes, commits, pushes, GitHub writes or hardware actions were used.

Reviewer-owned ledger

Every row covers the stack head below together with parent `27495a06d5569336a098da20381ced3e331ba665`. UNCLEAN denotes the open F1 finding, not an omitted lens.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Milan Tables 5.49-5.51 and startup/LINK_UP clauses; IEEE 6.2.2.16, 6.2.4/.5; issue #970; include/adp.h:87; draw population and base reproduction | R888-1 | 5d14a6d816a43a49299172a34e3eeaea44c267c6 |
| RTL | UNCLEAN | src/adp.c:53/265/282 and send/timer paths; parent adp_mbx.c; unchanged mailbox contract; exact gitlink; CPU and image receipts | R888-1 | 5d14a6d816a43a49299172a34e3eeaea44c267c6 |
| Robustness | UNCLEAN | draw_probe.c; A18/A20 owed output and link loss; GM event ordering; parent backlog tests and 63-probe comparisons | R888-1 | 5d14a6d816a43a49299172a34e3eeaea44c267c6 |
| Tests | UNCLEAN | A0/A3/A9/A18/A20; seven stack plants; parent G1-G5, LINK_UP x DOWN and nine plants; generated inventory; CONTRIBUTING gate receipts | R888-1 | 5d14a6d816a43a49299172a34e3eeaea44c267c6 |
| Docs | UNCLEAN | PORTING:187-196; MFDISC-01; generated REQUIREMENTS/TRACEABILITY/TESTS; parent MAILBOX_SPLIT:533-544, FR_NFR:415-416, pin diagram, public evidence and PR claim | R888-1 | 5d14a6d816a43a49299172a34e3eeaea44c267c6 |

Limits and pending manager duties

This is a source review, not merge approval or completion of issue #970. No manager source bank exists at this head and none is inferred. The manager must resolve F1, obtain the required independent positive reviews, update the parent gitlink and all pin records after stack merge, then validate the actual current-dev merge candidate with builder and native banks and publish its receipts. The declared live development reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`; this review does not validate a composition with it. Complete hosted/act acceptance remains separate.

The affected bench scenarios at 1x1/1if and 8x8/1if, both GM orders and actual wire timing remain pending under the frozen acceptance. No bench or hardware access occurred. The separate boot/autonegotiation contribution of approximately 1.8-2.8 s is outside this finding. No full parent, processor, gPTP, synthesis or builder bank was run. The pinned simulator's 5.050 identity was verified, but no fresh RTL simulation is claimed. Functional probes do not certify a loaded network or physical timing. Scripts and receipts are listed in MANIFEST.sha256; scratch trees are excluded. Receipt text preserves execution results and assertions, with only local filesystem prefixes normalized for publication.

R888-1 FINISHED
