[R686] POSITIVE - exact head 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6

External independent review R686-3 of issue #775 / PR #777. The assigned prior findings are resolved. All five lenses are CLEAN at this head. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION was found. The optional watchdog-coverage suggestion remains disclosed and out of scope. This is a source review verdict, not merge authorization or hardware acceptance.

Reviewed tree: `a4bc2ed645a1cc426a2e83d1773c3c5e2ccb5405`. Source base: `a032c6d6e3775f145349d5a495c1e1ad12294936`. Previously reviewed head: `c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83`. Four commits touch five files: tests, documentation, a comment rewrap and mutation-result accounting. No executable RTL changes.

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #775 and its ruling](https://github.com/kebag-logic/milan-fpga/issues/775#issuecomment-6379902989), the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/pull/777#issuecomment-6383212982), REQUIREMENTS.md, FR-STR-03, architecture and listener interfaces. Both `a032c6d6..220b51f2` and `c2a080ae..220b51f2` diffs and history were examined. Prior findings were reconciled after the independent source pass. Public PR retrieval also supplied historical comments; no other current-round report, private author material or management checkout was read. `independent-pass.md` records the source assessment before deliberate prior-finding reconciliation.

The governing public ruling applies Milan v1.2 Table 5.6 and 4.4.2.2: a rejected off-format received PDU advances sequence state, counts only UNSUPPORTED_FORMAT and presents nothing. This review applies that ruling and carried-forward coverage; it does not claim a fresh reading of an external standards archive. Unchanged CRF, reference, integration, requirement and compliance artifacts retain rounds 1 and 2 coverage because the delta changes none of their dependencies.

Prior findings and assigned checks:

| Finding/check | Disposition at this head | Evidence |
|---|---|---|
| R686-2-F1, MINOR, Conformance/Tests/Docs | RESOLVED | `format_mutants.py:189-222` writes both planted sources. NX builds the planted engine; lockstep builds that engine and the planted reference at N=1 and N=8. `receipts/format-details/build-inputs.json` records the actual inputs to real builds. All pairs execute and fail their required NX checks. Driver descriptions, TESTING.md:617 and the PR's round-3 text accurately distinguish those roles. |
| R685-2-S1, SUGGESTION, Tests | RESOLVED | The committed campaign executes the paired lockstep case. Every pair measures N=1 116/0 and N=8 119/0. Its result is reported without grading the mutation arm. |
| R685-2-F1, MINOR, Tests/Docs | RESOLVED | `sim_main_nx.cpp:1124-1181` adds SQ6/SQ7. The seed-set/clear replacement lines at `format_mutants.py:116-121` exactly match the archived probe after bundle-name substitution. Both fail named counter checks. The unchanged `probe_sq_claims.py` now catches 6/6. TESTING.md:617 distinguishes both seed states. |
| R685-2-R1, RESIDUE, Docs | RESOLVED | `KL_avtp_rx_monitor_ctx.sv:18-22` has the requested rewrap. Independent comment stripping and preprocessing prove identical executable source. |
| R685-1-F1, MINOR, Tests/Docs | RESOLVED, including the formerly open method portion | SQ4/SQ5 still catch lock-set/settle-step through SQ4f/SQ5c; the committed paired construction now meets the assignment. The archived probe also catches settle restart and lock clear. |
| R685-1-F2, RESIDUE, Docs | Remains RESOLVED | Context banner lines 18-22 distinguish the context rule from the flat instrument; lines 96-99 name the flat instrument's absent sequence advance. |
| R685-1-F3, SUGGESTION, Tests | RETAINED, out of scope | Watchdog preservation across a reject remains ungraded and explicitly excluded by TESTING.md:617. Details below. |
| R686-1 | No findings to resolve | Unchanged functional and structural coverage carries forward. |
| Commit 220b51f2 tally correction | VERIFIED | Mutant-pair diagnostics contribute zero checks/failures to the sweep parser. Synthetic passing and failing pair results remain measurements. The actual published suite log parses as 577 checks, zero failures, no unparsed tallies. |

Independent executable evidence:

| Execution | Result | Receipt |
|---|---|---|
| Clean N=4 stack, rebuilt by the committed campaign | 218 checks, zero failures | `receipts/format-details/obj_clean.log` |
| Committed format campaign, every arm | 13/13, rc 0 | `receipts/format.log` |
| Paired lock-set | SQ4c/SQ4f fail; lockstep 116/0, 119/0 | `receipts/format-details/obj_lock_set.log`, `pair-0.log` |
| Paired settle-step | SQ5c/SQ5d/SQ5g fail; lockstep 116/0, 119/0 | `receipts/format-details/obj_settle_step.log`, `pair-1.log` |
| Paired seed-set | SQ6c/SQ6e/SQ6i fail; SQ6e gets 1 instead of 0; lockstep 116/0, 119/0 | `receipts/format-details/obj_mr_seed_set.log`, `pair-2.log` |
| Paired seed-clear | SQ7c/SQ7d/SQ7e fail; SQ7d gets 0 instead of 1; lockstep 116/0, 119/0 | `receipts/format-details/obj_mr_seed_clear.log`, `pair-3.log` |
| Archived six-mutant probe, unchanged script bytes | Six caught by named NX assertions; all paired lockstep runs pass | `receipts/sq-probe/SUMMARY.txt` and individual logs |
| Executable-source equality, mutation-byte comparison and accounting controls | PASS | `delta-inspection.json` |

The archived probe returns rc 0 even when a mutant survives, so its return code was not treated as a catch verdict. All six NX failure summaries, named failures and twelve lockstep results were inspected. The committed campaign's clean control passes; its verdict routine rejects compilation failure and failures lacking the named check.

`scripts/run_checks.py CHECKOUT PACKET PINNED_SIMULATOR` reproduces both independent campaigns under one foreground supervisor. The probe uses two workers and each build at most four compiler jobs: at most twelve concurrently, with make's job setting 16. All execution completed; no process was left running. Simulator identity was checked as 5.050, revision v5.050. Mutation sources/builds reside under unpublished `scratch/`. The observer records real build inputs and raw run output without replacing compilation or changing verdicts.

[R686] PASS Conformance - `docs/reference/FR_NFR.md:271`; `KL_avtp_rx_monitor_ctx.sv:1012-1021`; `KL_crf_rx.sv:598-607`; `sim_main_nx.cpp:1124-1181`; round-3 assignment - sequence-only rejection and the assigned paired-mutation method are satisfied. SQ6's first accepted mr=1 PDU seeds without counting MEDIA_RESET. SQ7 preserves an existing seed and counts the subsequent toggle once. No normative requirement or acceptance criterion changed.

[R686] PASS RTL - `KL_avtp_rx_monitor_ctx.sv:18-22,494-498,550-562,1012-1021`; `delta-inspection.json` - only banner comments change. Both revisions produce 804 nonblank executable lines and SHA-256 `7c7446423ec3bfbb1b04f5b01f1017a5e484d00770158def9386a92ced60f046` after removing comments and trailing whitespace. Independent preprocessing agrees under the same normalization. The mr reference/seed remain MON_STATE bits 22/23; rejection preserves bits 31:8. Ports, encoding, reset, clocks, RAM layout and timing are unchanged. CRF and the reference file are byte-unchanged from round 2.

[R686] PASS Robustness - `sim_main_nx.cpp:1124-1217`; `receipts/sq-probe/SUMMARY.txt`; clean NX receipt - fresh binding and seeded-stream preconditions are observed explicitly. Rejection produces no accept/payload; following observation intervals verify counter effects. Holding mr does not count again. Existing lock/settle boundary cases remain effective, including independent restart/clear mutations. Untouched reset, wrap and stream-isolation coverage carries forward. Watchdog preservation remains a stated limit.

[R686] PASS Tests - `format_mutants.py:99-222`; `Makefile:45-83`; `sim_main_nx.cpp:1124-1181`; actual build/run receipts - both sources of every pair are constructed, compiled and executed. NX supplies the independent count oracle; mutated lockstep agreement is measured only. Seed replacements match the archived probe byte for byte. Pair measurements neither inflate nor decide the clean-tree suite tally. Every archived falsifier triggers named failures.

[R686] PASS Docs - `docs/testing/TESTING.md:617`; `format_mutants.py:22-37,189-222`; context banner; PR #777 round-3 text; verified receipts - descriptions match execution and distinguish graded NX from measured lockstep. Historical round-2 claims are explicitly corrected by the PR's round-3 explanation. New source comments contain no bench-lane labels, reviewer identities, review rounds or issue-comment IDs. Four commits have one-line messages without trailers. No additional wording residue was identified.

Reviewer-owned coverage ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue ruling/assignments; FR-STR-03; ctx/CRF paths; SQ6/SQ7; paired campaign | R686-3, carrying unchanged R686-1/R686-2 coverage | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |
| RTL | CLEAN | ctx banner/executable equality; reference/CRF; MON_STATE contracts | R686-3, carrying unchanged R686-1/R686-2 coverage | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |
| Robustness | CLEAN | SQ4-SQ7; clean run; six-mutant probe; paired results | R686-3 | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |
| Tests | CLEAN | format driver; Makefile inputs; campaign/probe; tally controls; published gates | R686-3 | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |
| Docs | CLEAN | TESTING.md:617; driver text; ctx banner; PR body; public receipts | R686-3 | 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 |

R685-1-F3 - SUGGESTION - Tests - retained watchdog-coverage limitation.

- Artifact: TESTING.md:617's explicit exclusion and the AAF SQ campaign.
- Authority/evidence: the round-2 assignment leaves this earlier suggestion out of scope. The delta makes no watchdog-coverage claim.
- Impact: these cases do not detect every future defect that refreshes the 100 ms watchdog on rejection. No new shipping defect is asserted.
- Optional outcome: manager-owned follow-up coverage; no change is required in this delta.
- Verification: a watchdog-refresh mutation should fail an independent timeout assertion while the unmutated implementation passes. This suggestion leaves coverage clean.

The [public evidence tree at 36b5ada0](https://github.com/kebag-logic/milan-fpga/tree/36b5ada0cf094f322f16ea15fe4b87835bae5edd/review-evidence/775-r1) was verified against MANIFEST.json. `public-hash-audit.json` records 324 selected round-3 receipt/probe files, zero hash mismatches. The commit reports signature status `N`, unsigned; no cryptographic signature was available to verify. This establishes content integrity against the pinned archive, not signer authentication. Redacted files were compared with published hashes, not pre-redaction hashes.

`public-gate-summary.json` and `published-receipts/` retain checked source evidence:

- Four exact-head shards: 15 + 16 + 17 + 16 distinct suites, 64/64 passing, 2,189,668 checks, zero failures, each completion rc 0.
- avtp_rxmon: flat 97/0, NX 218/0, clean lockstep 116/0 and 119/0, lockstep campaign 14/14, format campaign 13/13. The sweep counts 577; pair measurements add none.
- Behavior: 14 features, 406 scenarios, 1,977 steps; zero failures/skips.
- Thirty static gates, rc 0; lint 89 findings within ratchet 89.
- Docs: 42 executed entries, rc 0 under Make 4.3; two explicit skips, the host-runner contract and metadata-stripped docs step. In-place checks do not prove metadata-stripped execution.

These are author source-head executions. There is no manager source bank at this head. This review independently reran the focused campaign and six-mutant probe, not the full parent/processor/synthesis/builder banks, route, hosted workflows or local workflow replica. Prior synthesis/route results retain round-1 attribution; executable RTL equality permits carry-forward under the assignment. Physical calibration was NOT RUN. Field campaigns and freshness arms skipped for an absent generator contribute no executed proof. Routed timing and field skips are not hardware proof. No hosted skipped context is represented as an executed job.

The manager owns reconciliation with the other independent review, watchdog/flat-instrument follow-ups, hosted/local-replica acceptance and the final candidate against then-current dev, including builder/native banks and linked receipts. The assignment names live dev `a032c6d6e3775f145349d5a495c1e1ad12294936`; this report does not certify a future merge candidate. Explicit maintainer authorization, completion of review rounds, post-merge containment and issue/project closure remain required.

Final `integrity.json` proves parent tracked blob bytes, modes and index entries, plus required processor, axis and stack submodules and lwSRP against exact gitlinks and tracked bytes. All match the assigned head/tree. The unused external submodule remains uninitialized. Status is clean and diff checking passes. No tracked source edit, commit, push, GitHub write, author contact or merge occurred. `receipt-redactions.json` records normalized installation paths; originals and disposable artifacts remain under unpublished `scratch/`. Only MANIFEST.sha256-listed files and this report are publishable.

R686-3 FINISHED
