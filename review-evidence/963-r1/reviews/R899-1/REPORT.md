[R899] NEGATIVE - exact head 4cca956932073b3f704f12f81c53f2934cfa215c

External independent review R899-1 of issue #963 / PR #984. Tree: `2f4e963dcaf2e5739003fbd3059610fe2f2ee9b0`; comparison base: `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`. All five lenses were applied. Two MINOR findings remain under Tests and Docs. No functional defect was found in the reviewed production change. This is not merge approval.

**Findings**

**R899-1-F1 - MINOR - Tests, Docs - PR #984 Status / issue #963 REVIEW READY: ordinary suite runs counted as caught plants.**

Authority/evidence: the [PR Status](https://github.com/kebag-logic/milan-fpga/pull/984) and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/963#issuecomment-7096625846) claim “1,846 plants caught”. `sw/firmware/ctrl/test/test_ctrl_firmware.py:168-170,241-260` partitions suites, control mutations, AECP mutations and SRP mutations. The published `author/receipts/gates-current/firmware-0/gate.log` executes 88 ordinary suites; those are not planted defects. The remaining receipts establish 826 control mutations, 389 AECP mutations, 541 SRP mutation executions (359 + 167 + 15), and two dependency-pin controls. Thus the supported result is 88 normal suite invocations, 1,756 mutation executions and two pin controls, not 1,846 caught plants. `shard-census.json`, `shard-selftest.log` and `receipt-audit.json` independently verify the live dispatch partition; invocation counts and caught-case counts are intentionally distinct.

Impact: the public quantitative evidence overstates mutation coverage by calling successful normal executions caught faults. The passing suite results and actual caught mutations remain useful evidence.

Required outcome: correct the count and categories in the PR and public readiness evidence, and any retained packet summary that repeats the claim. Preserve the actual logs. This is not RESIDUE because it changes an evidence figure.

Verification: reconcile each reported category with its shard dispatch and log, distinguishing normal invocations, mutation executions and the pin controls; inspect the corrected public claims.

**R899-1-F2 - MINOR - Tests, Docs - PR #984 Definition of Done: required verification marked complete despite the missing full native sweep.**

Authority/evidence: the PR checks “Required local verification bar passes” while its limitations explicitly state that the full native sweep, four shards, was not run. `CONTRIBUTING.md:96-97` requires the Section 3 bar on the branch; `CONTRIBUTING.md:349-363` independently requires local long-gate evidence and hosted results before validation. The focused runs in this review do not discharge that full sweep.

Impact: the completion checklist asserts a verification state unsupported by the disclosed execution evidence. The full verification/completion bar is pending, even though the focused change has passing evidence.

Required outcome: uncheck the completed-bar claim and accurately record the source-head gap. Complete and link the applicable required validation before asserting that the bar passes. Keep the source-head record separate from the manager's future current-dev candidate result; do not relabel candidate execution as source-head execution.

Verification: inspect the corrected checklist and the eventual exact-object receipts. The manager owns execution and acceptance of the full candidate banks and hosted/local workflow evidence. This review did not execute prohibited full banks.

**Scope and reconstruction**

I read the repository operating contract and contribution rules, documentation map, frozen issue acceptance and public scope comments, linked requirements and interface authorities, then the five-file diff and ten-commit history. The public source-evidence packet is [review-evidence/963-r1 at e31126d8](https://github.com/kebag-logic/milan-fpga/tree/e31126d8e3c975f09a9c539f1496d3bccf44e8f2/review-evidence/963-r1). Its 703 published hashes verified. Only the public author packet was examined.

The independent verdict and ledger were written in `independent-verdict.md` before looking for prior public findings. The subsequently inspected PR discussion, review submissions and inline threads contained no prior review finding to resolve or retain. The two discussion comments were review-start notices. No other reviewer's report was read. `review-context.json` records the snapshot and links. The PR remained at the requested head in the final public snapshot.

**Conformance - CLEAN**

Artifacts: `sw/firmware/ctrl/aecp/aecp_maps.c:255-288,478-570`; `aecp_commands.c:116-122`; IEEE 1722.1-2021 7.4.44-7.4.46 and 9.2.2.6; Milan v1.2 5.4.2.26-5.4.2.28; issue #963 acceptance; `probe-results.json`.

The standards were read from the primary specification texts. In IEEE 1722.1-2021, GET_AUDIO_MAP is 7.4.44, ADD_AUDIO_MAPPINGS is 7.4.45 and REMOVE_AUDIO_MAPPINGS is 7.4.46. The PR cites the ADD/REMOVE clauses correctly. Milan's invalidity condition concerns the currently streaming Stream Output; it does not require one hardware observation per mapping referring to that stream. The edit still checks mappings in order, refuses a running or initially unanswered stream, and changes no mapping on refusal. Existing geometry, duplicate/conflict, capacity, persistence and notification handling remain in place.

There is a real, disclosed possible controller-visible difference. A disposable port callback answered the first observation and refused the second. The base made two reads and returned BAD_ARGUMENTS (7), leaving zero rows; the head made one read and returned SUCCESS (0), adding two rows. Both outcomes were reproduced, and the probe also required the observation to arrive zeroed. Consequently, byte-identical campaign output is not a universal equivalence claim for every possible port failure schedule. The PR discloses this exception. Reusing the successful observation within the command is conformant; an extra later read is not required by the cited clauses.

**RTL and architecture - CLEAN**

Artifacts: `aecp_maps.c:173-180,255-288,478-559`; `sw/firmware/ctrl/aecp/aecp_face.c:164-184`; `sw/firmware/ctrl/mbx/mbx.c:304` and `hdl/milan/mailbox/KL_mbx.sv:914-946` as identified in the interface reconstruction; `native-base-*-image-proof.json`; published placement and product-image receipts.

The only production-source delta is in `aecp_maps.c`; no RTL, CDC, clock, reset or mailbox interface changed. The stream state is read through the existing brief `aecp_stream_read` path. That function preserves `brief` while initializing the observation, eliminating the redundant caller zeroing. The per-edit bitmap is initialized before the checks. Input maps bypass it. Legal/domain checks precede indexing; word selection and shifts stay within the allocated bitmap and 32-bit word. Setting the bit before the read is safe because a failed read or running result immediately exits the whole edit. No subsequent mapping can reuse that failed observation.

The product's published running/license state is controlled by the single firmware event loop and mailbox writes; another firmware command does not run beside this record. Reset and window failure remain distinct from an independently executing map command. No new concurrent observation writer was found in the examined contract.

The three independently rebuilt base/head firmware pairs have identical function addresses and sizes and identical module spans, with loaded-byte differences confined to `aecp_map_command`. Its size is 2,204 B in both 8x8 arms and 2,208 B at the tested 1x1 arm. The public placement proofs cover all 16 arm images. This avoids the earlier 36 B growth and placement-induced load regression.

The published complete load comparison remains exactly 0.4891093771929825 at 1x1/1if and 0.6008172807017544 at 8x8/1if. Product image receipts give 8x8/1if ROM 139,208 B, SRAM 98,160 B and 58.0 RAMB36 against the 58.0 ledger; 1x1 gives ROM 126,432 B, SRAM 56,736 B and 45.0 tiles against budget 56. These are the published image measurements, not new synthesis or hardware measurements. The smaller ROM sizes in this review's image proofs belong to harness images, not product images.

**Robustness - CLEAN**

Artifacts: `sw/firmware/ctrl/test/test_aecp.cpp:2857-3014`; `aecp_maps.c:488-570`; `core.log`; `probe-results.json` and individual probe logs.

The complete focused AECP core execution passed 99 tests across four suites. The two mapping tests pass at the head and fail against the exact base production blob. Eight focused mutations were caught using their prescribed diagnostics: unread port rows, unread ownership, checks before the read, observing every mapping, an uncleared observation table, one shared stream bit, accepting a running stream, and a non-brief observation. This checks repeated edits, independent streams, initial refusal, initialization and the intended reduction in work, rather than merely accepting an updated oracle.

The existing definition test exercises legal/illegal row combinations, duplicates, conflicting rows and unchanged maps on errors; the new work test checks observation count and per-stream behavior. Bounds, zero-count/input behavior and failure exit paths were also examined in the implementation. No source fix was made. All mutation and extra-test edits were confined to disposable copies.

**Tests - UNCLEAN: F1 and F2**

Artifacts: `native-summary.json`, six complete compressed native logs and stimuli; `receipt-audit.json`; `group-census.txt`; `shard-census.json`; `harness-parallel.json`; published gate receipts.

The native executable identity was verified as the pinned 5.050 version before use. Three focused head runs and matching base reproductions completed:

| Point / arm | Base passes over share | Base longest cycles | Head passes over share | Head longest cycles |
|---|---:|---:|---:|---:|
| 8x8/1if answering-ports | 2 / 108 | 222,104 | 0 / 106 | 149,307 |
| 8x8/1if declaring-outputs | 2 / 108 | 227,112 | 0 / 106 | 153,071 |
| 1x1/1if answering-ports | 0 / 107 | 145,380 | 0 / 107 | 136,285 |

THE SHARE is 200,000 cycles at 100 MHz. Both 8x8 base runs therefore have strict share verdict 1; all head runs have verdict 0. The reproduction driver itself returns zero when execution and probe grading complete, so the separate strict verdict in `native-summary.json` must not be confused with its process status. There were no refusals or graded row misses.

Every focused pair produced 59 identical wire frames, in global order, without masking any frame byte. Publication values in each word's order, completion counts, and probe statuses/verdicts also matched. Timestamps are timing observations and are not compared as payload bytes. Complete raw native logs are retained compressed with deterministic gzip; their uncompressed hashes are recorded.

The cause is supported by the source walk and the public committed-PC trace: each base REMOVE/ADD walks 63 copies of a mapping and calls the stream reader 63 times, costing 55,052 inclusive cycles in answering-ports and 56,005 in declaring-outputs. At 8x8 the input map has zero capacity, so this is the output edit. Its 550-byte unsolicited REMOVE/ADD response (`0x802d`/`0x802c`) goes to 15 controllers. The head observes each mapped stream once through the hot reader. The independently measured pass reductions match the published results exactly.

The complete public differential has 481 unique base/head pairs across both points and eight arms, including save windows. The live group census equals those 481 identities. The final strict rows report zero differences with no masked frame fields, all stated rows passing, and all run statuses zero under the campaign's reporting mode. All 16 calibration records identify matching reference/checkpoint hashes. This was an audit of published execution evidence; I did not rerun all 962 simulations. The 1x1 declaring-outputs target is covered by that evidence (146,088 -> 137,072 cycles), not by a separate reviewer execution.

All held AECP classes remain at or below the base and within their statements: 1x1 long 91,641 -> 82,546, paced 29,993 -> 29,822, other 23,726 unchanged; 8x8 long 163,316 -> 90,258, paced 56,492 -> 56,327, other 20,202 unchanged. The distinction between held and reported classes matters. The reported-only 1x1 declaring-outputs paced row remains 325 us by the rule versus 315 us stated (30,839 -> 30,688 cycles). That baseline condition was not newly introduced, is excluded by the harness's held-class contract, and is not claimed here as a passing held row. The manager owns the #958/composition statement reconciliation.

Shard 0 carry-forward is valid: it ran at `25d3dd7a`; the only later changes are `50d3f10e`'s mutation re-anchor and the final design documentation. Neither changes normal-suite inputs or their dispatcher. The changed mutation belongs to shard 2, which was rerun. Final shard 1/2/3 receipts pass, as do the firmware-unit coverage ratchet (40 files), twin and twin plants, and documented portable/docs gates. Carry-forward does not repair F1's inaccurate tally or supply F2's missing full sweep.

The independently executed shard self-test passed. The harness self-test ran unchanged baseline checks in eight fresh processes and partitioned all 295 existing mutations into disjoint subsets; all 295 were caught, with zero failures in every process. An earlier serial attempt was stopped for scheduling and is not counted as a pass. Two base-driver setup attempts failed before simulation; corrected reruns supply the reported results. `REPRODUCE.md` and the portable scripts state the exact methods.

**Docs - UNCLEAN: F1 and F2**

Artifacts: `docs/design/SPLIT_CONTROL_MEMORY.md:2628`; source comments in `aecp_maps.c:255-272,478-483,530-531`; issue acceptance/readiness and PR Status, limitations and checklist.

The design entry accurately explains the repeated stream check, single initialization, discarded cold-reader/layout forms, final pass measurements and ledger. New source comments describe behavior and reason with issue and requirement references. No new bench label, review round, reviewer identity or issue-comment identity was found in the source-comment delta. No new source-comment RESIDUE is recorded. The disclosed port-read exception limits the surrounding unchanged-response language; the report above explicitly demonstrates that limit. The evidence-count and completion-state defects are F1 and F2.

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IEEE 1722.1-2021 7.4.44-.46; Milan 5.4.2.26-.28; aecp_maps.c:255-288,478-570; refusal probe | R899-1 | 4cca956932073b3f704f12f81c53f2934cfa215c |
| RTL | CLEAN | aecp_maps.c bitmap/initialization; stream/mailbox interface; native image proofs; published 16-image placement proof | R899-1 | 4cca956932073b3f704f12f81c53f2934cfa215c |
| Robustness | CLEAN | test_aecp.cpp:2857-3014; core.log; eight mutation probes and later-unanswered probe | R899-1 | 4cca956932073b3f704f12f81c53f2934cfa215c |
| Tests | UNCLEAN (F1, F2) | native-summary.json; 481-pair audit; firmware partition and gate receipts; PR tally/checklist | R899-1 | 4cca956932073b3f704f12f81c53f2934cfa215c |
| Docs | UNCLEAN (F1, F2) | SPLIT_CONTROL_MEMORY.md:2628; changed source comments; PR and issue readiness claims | R899-1 | 4cca956932073b3f704f12f81c53f2934cfa215c |

**Limits and pending manager duties**

No manager source bank was run at this exact head, and none is inferred. Source execution evidence is the public author's receipts plus the focused reviewer executions distinguished above. Full native, parent/processor, synthesis and builder banks were not executed by this review. Hosted contexts and local workflow acceptance belong to the manager; this report asserts no hosted success and treats no skipped context as an executed job.

The manager must build and validate the actual current-dev merge candidate, reconcile #958 with the train, publish the candidate identities and builder/native receipts, discharge applicable hosted/local acceptance, obtain the remaining required reviews, and perform authorized merge and post-merge containment. The supplied live-dev snapshot is `e275d7950ef3385753e6a15d2e191ba855b171ed`; it is distinct from source base `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`. No future candidate result is claimed here. Physical calibration was NOT RUN; field skips and desk evidence are not hardware proof.

The final integrity check independently hashes tracked blob bytes and verifies executable modes, the stage-zero index and all five required submodule heads, bytes, modes and indexes against their gitlinks. The exact reviewed head/tree is retained. The unused optional `external` submodule remains uninitialized with its recorded gitlink intact. No source commits, remote writes or changes to another checkout were made. Disposable builds and probes are beneath `scratch/`, excluded from publication.

`MANIFEST.sha256` names every publishable receipt relative to this packet. Host diagnostic path-prefix redaction is documented separately; raw native simulation logs are unchanged. Review findings require correction and re-review before Tests and Docs can be recorded clean.

R899-1 FINISHED
