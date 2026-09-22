[R236] POSITIVE - exact head a769d9dbc937fb324c4726e60dee5b2f7ad349e3

Independent external review R236-1 of issue #464 / PR #513. Reviewed tree: `31ddc6b5615ff91ceed7a6b52afca61c5fb9653d`. All five lenses were applied. No BLOCKER, MAJOR, MINOR, or SUGGESTION findings remain open in this scoped change. This is a source-review verdict; it does not authorize merge or assert that the outstanding manager duties have completed.

The contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md (particularly REQ-VER-03/04), the [issue body and public decisions](https://github.com/kebag-logic/milan-fpga/issues/464), architecture/interface documentation, the complete six-file PR delta and commit history, and executable evidence. Governing decisions are comments 5770832953, 5774939905 and 5775302273. No private author reasoning, other reviewer report, or local author-lane material was used. The [public review start](https://github.com/kebag-logic/milan-fpga/pull/513#issuecomment-5777127589) identifies this independent round.

The reviewed commit has parents `88e9276b2a220c716f64a843f7e1eb8f9265e896` and original author head `1576f0893ae9781074fffb105f5384fe774ff11e`. Its complete binary-capable diff against the former is byte-for-byte equal to the original issue diff from `ec34fcdee0ca9ffa63564a9af8ad70a3a618de29` to the latter. Original author evidence remains attributed to `1576f089`; manager candidate evidence and this review belong to `a769d9d`. See `issue-delta.patch` and `static-equivalence.json`.

[R236] PASS Conformance - `avdecc/gen_aem_store.py:157`, `avdecc/aem_maps.py:107`, issue #464 acceptance 1-3 - the retained self-test repairs the identified fixture failures without changing production validation policy.

Evidence: independent historical runs pass at `b7d0bbcd` and fail at `da71309c7b5067c0cb43ceb211a364c5ab037202`. On Python 3.14, the first failure is the `global_index` assignment to absent `audio_maps[1]`, before the generator can reject anything. That historical change made the input dynamic and renumbered the remaining output map to index 0. The original input-duplicate and CRF vectors therefore reached the wrong direction/bound; two later output-map vectors also indexed a nonexistent map. On Python 3.12, the missing `Callable` import causes an earlier `NameError`. The added import is necessary there; removing it remains invisible on 3.14 because annotations are deferred. These are test/entry-point defects, not evidence of a production validator defect.

Primary clauses were read from IEEE 1722.1-2021 7.2.13/Table 7-23, 7.2.16/Table 7-27, 7.2.19/Tables 7-32/7-33; Milan v1.2 5.3.3.7-5.3.3.9, 6.4 and 6.5/Table 6.2; and IEEE 1722-2016 Annex I.2.4. PDF identities and examined pages are in `standards-identities.json`. The static input fixture is a supported IEEE generator shape, expressly not the Milan shipping input model. Static `number_of_maps == 1` is this generator's retained serving limitation, not a claim that IEEE/Milan generally permits only one map. The 62-row limit concerns an AUDIO_MAP descriptor, not a dynamic GET_AUDIO_MAP response.

The fixture declares two input streams (AAF and CRF), one two-channel AAF output, eight clusters per direction, input map 0 at cluster base 0, and output map 1 at cluster base 8. It builds before mutation and each call returns independent nested objects. Its output still records six format-width deviations; fixture acceptance does not falsely certify their absence. The deployed model remains a separate positive control. The repaired self-test passes 20 arms on both Python 3.14.7 and 3.12.13. Acceptance 1 is publicly documented; acceptance 2's runnable repair is demonstrated at the exact PR head, with landing on dev still a manager duty; acceptance 3 is implemented and has real hosted execution.

[R236] PASS RTL - `docs/overview/ARCHITECTURE.md:58`, `docs/reference/SUBMODULES.md:23`, `avdecc/aem_assemble.py:585`, and `issue-delta.patch` - the descriptor-image boundary and imported processor interfaces are preserved.

Evidence: the complete issue diff contains no RTL, configuration, builder, encoder, assembly, or processor-pin change. AST comparison of production portions of the two changed Python modules is equal after excluding self-test functions, the explicit Callable import, the module docstring, and the reviewed deviation-label assignment. The production validator bodies are unchanged. `KNOWN_MAP_DEVIATIONS` is consumed by the self-test path, not shipping image generation. PP remains `424c688fa2205b934a7689a58f2aa766420f2326`; gPTP remains `c1b617435824929a790739ea8585c3fe1a328cc0`. There is no changed clock, reset, CDC, FSM, backpressure, latency, or resource contract to validate in this delta. No #509 descriptor-ownership requirement is introduced.

Shipping-byte attribution is bounded: the published author manifests contain 83 identical generated files, comprising 50 builder CLI files, 20 image/overlay files, 12 store out-directory files, and the default JSON. I inspected their generation script and verified manifest equality and published hashes. I independently regenerated the default JSON and both builtin `--out-dir` outputs against current base/head in scratch; all were byte-identical. These are generated-artifact comparisons, not bitstream, installed firmware, physical-wire, or hardware measurements. The unused tracked snapshot drift remains #495 and is not a finding or scope expansion here.

[R236] PASS Robustness - `avdecc/gen_aem_store.py:199`, `avdecc/gen_aem_store.py:289`, `avdecc/aem_maps.py:153`, and `geometry-results.json` - the repaired refusals have valid starting geometry and fail for the intended causes.

Evidence: all nine map refusal guards were removed independently in scratch, on both interpreters. Each removal makes the self-test fail at the corresponding artifact. Removing base-map or stream-index guards causes an uncaught IndexError at the relevant lookup, so those runs fail closed; I do not describe them as successful explicit diagnostic assertions. Removing the CRF guard produces an unrelated `max()` ValueError, which the new cause check correctly rejects. Applying either directional duplicate rule to both directions fails. Complementary direct controls accept input fan-out and repeated output cluster offsets, and reject an output stream/channel duplicated across two output ports.

The new 63-row vector uses distinct output stream channels and cluster offsets modulo eight. It breaches the row count without also breaching a refusing row/duplicate bound. Independent boundary controls accept 0, 1 and 62 rows, reject 63, and accept those same 63 rows when only the row limit is raised; the 61 format-width deviations are recorded, not refusals. A fixture-only refusal trips the fixture positive control, and sharing the fixture between vectors produces wrong-cause failures.

The deployed deviation set is exactly six strings for output stream 0, channels/cluster offsets 2 through 7, cluster channel 0, format `0x0205022000806000`, now at AUDIO_MAP[0]. There is no size increase or production refusal relaxation. Missing, extra, and stale-index records fail. Disabling the new-deviation assertion fails the empty-allowlist arm. Disabling the reverse comparison permits an extra recorded entry, confirming that the reverse check is necessary.

[R236] PASS Tests - `avdecc/gen_aem_store.py:157`, `.github/workflows/docs.yml:390`, `scripts/ci_events.py:1065`, and the focused receipts - the preserved arms and new CI carrier are executable and sensitive to the claimed guard losses.

Independent evidence consists of 52 expected focused execution outcomes, 14 geometry/boundary controls, eight supplementary causal controls, and 13 carrier controls. The 52 include historical baselines, pristine scratch controls, both interpreter runs, mutations, and the CI contract checks; they are not 52 distinct product behaviors. The earlier mutation harness attempt lacking its CSR version input is explicitly invalid and excluded from every pass count. Its receipts are retained under `invalid-harness-*`.

| Check | Result and limitation |
|---|---|
| Nine map refusals | Each original arm retained, with fresh valid geometry and cause-specific matching; independent guard-loss controls fail. |
| Two positive map controls plus allowed output duplicate-cluster case | All pass; fixture refusal and shared-state plants fail. |
| Two deviation cases | Exact deployed set and empty-allowlist control pass; stale, widened, reduced, and neutered variants fail. |
| Four directory/name cases | Contiguity, index ordering, off-by-one lookup base, and unnamed-type mask remain exercised. Disabling their checks produces the corresponding failures. |
| Two Base-format cases | Complete 48-kHz input family passes; missing ut coverage and a neutered family checker fail. |
| Cause-oracle controls | CRF guard removal passes only when the cause oracle is also disabled. Old count geometry with the oracle disabled misses count-guard removal; new geometry alone and the oracle alone each detect it. |
| CI check/self-test | 1513 contract items and 1150 arms pass. The six new step-derived arms include no-op, swallowed failure, appended command, missing flag, continue-on-error, and missing canonical record. |
| Independent carrier controls | Reject the preceding rewrites plus wrong source path, step removal, `if`, shell, working-directory and checkout-ref overrides. |

The canonical record pins the workflow command `python3 avdecc/gen_aem_store.py --self-test`, its position, name and key set. This is command/source-path binding to the event checkout, not a cryptographic pin of the Python file's contents. The checker does not derive the canonical record from the workflow under test. YAML step 41 runs before the three shape gates; GitHub's job API numbers it 42 after its setup step.

Real execution is proven by [docs-check job 106752129822](https://github.com/kebag-logic/milan-fpga/actions/runs/35729759797/job/106752129822), which ran the new command and printed all 20 successful arms and the final PASS. The run names head `a769d9d`; the checkout log names GitHub test merge `e8e3f66527b3bbc93f3a72b7bcedbb968e4886fc`. Its API commit record gives parents `88e9276b` and `a769d9d` and tree `31ddc6b5615ff91ceed7a6b52afca61c5fb9653d`, exactly the reviewed tree. Receipts preserve both identities.

Coverage is bounded to this repair. The inherited nine vectors are not exhaustive testing of every possible malformed spec or every boundary. In particular, the embedded output-duplicate vector uses one output port; configuration-wide behavior was additionally checked directly in this review. No claim is made that its embedded vector alone detects every possible cross-port scoping mutation.

[R236] PASS Docs - `docs/testing/CI_WORKFLOWS.md:1059`, `docs/testing/RUNNING_TESTS.md:24`, `avdecc/gen_aem_store.py:6`, issue public decisions and the immutable evidence packet - documentation matches the repaired behavior and preserves evidence identities and limits.

The pages document the command, explicit fixture, deployed positive control and carrier pin. The generator overview now correctly says two CLOCK_SOURCE descriptors and one AUDIO_MAP. No authoritative requirement is changed. Published [candidate evidence](https://github.com/kebag-logic/milan-fpga/tree/6ae76b6a31b496a6b636c7a9ea71959b34a479a0/review-evidence/464-r1/candidate1) has 41 completed static/builder commands and five completed native groups, all exit 0 at `a769d9d`, with completion markers and final blob/index/pin integrity. I verified 204 downloaded Git blobs and 203 corresponding published-manifest digests, and inspected the relevant raw results. The native parent sweep reports 55 passing suites and 2,118,264 checks; four optional campaign skips add zero checks. Builder gate 11 is NOT RUN and supplies no hardware evidence. The superseded original-source native attempt is explicitly NOT PASS. Native Verilator 5.052 evidence is not relabeled as the replicas'/hosted pin 5.050.

Reviewer-owned coverage ledger:

| Lens | Covering round | Exact head |
|---|---|---|
| Conformance | R236-1 CLEAN | a769d9dbc937fb324c4726e60dee5b2f7ad349e3 |
| RTL | R236-1 CLEAN | a769d9dbc937fb324c4726e60dee5b2f7ad349e3 |
| Robustness | R236-1 CLEAN | a769d9dbc937fb324c4726e60dee5b2f7ad349e3 |
| Tests | R236-1 CLEAN | a769d9dbc937fb324c4726e60dee5b2f7ad349e3 |
| Docs | R236-1 CLEAN | a769d9dbc937fb324c4726e60dee5b2f7ad349e3 |

Open findings: none in this review's scope. Existing recorded product deviations are preserved, not asserted resolved or newly approved as product compliance.

Limits and manager duties: the last captured public state is 2026-09-22 13:23:56 UTC. PR head remains `a769d9d`; live dev remains `88e9276b`. Hosted docs, elaborate and rtl-fast are complete/success. Hosted rtl-full is still in progress, with neither final `verilator-suites` nor `yosys-portability` aggregate present in that captured job list. The trusted act public comment records a real start, not a completed pass. Manager must obtain its completed result and both required hosted aggregates, finish the independent review bar without a round in flight, recheck then-current dev/candidate identity, obtain explicit maintainer merge authorization, verify the actual merge result, perform containment and review-integrity checks after the branch stops moving, verify post-merge hosted results, and finish Issue/Project state. This report neither reads nor substitutes for the other review.

No source fixes, commits, pushes, public comments, metadata changes, hardware operations, installs, privilege changes, Docker/act execution, or full native/builder/processor reruns were performed. Candidate `act_ci.py` and its self-test were never executed on the host. Focused computation was sequential; evidence downloads used at most four workers, within the eight-job cap.

Final checkout integrity equals initial integrity: 851 parent blobs, 103 gPTP blobs, 222 PP blobs, and 214 AXIS blobs matched their committed bytes, file kinds and executable modes; index records and raw index hashes are unchanged; all four populated repositories are clean. The optional unused historical `external` import remains uninitialized. See `integrity-before.json`, `integrity-after.json`, and `integrity-comparison.json`. Reproduction and receipt scope are documented in `README.md`. Manager publishes this report faithfully with workstation-path neutralization; R236 has not self-published.

R236-1 FINISHED
