[R686] NEGATIVE - exact head c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83

External independent review R686-2 of issue #775 / PR #777. One MINOR remains: the committed mutation driver does not plant the reference-copy defects required by the round-2 assignment, although its generated results claim that it does. The new count assertions work, the independent two-copy probe catches both defects, and no shipping RTL defect was found. This is a source review verdict, not merge authorization or hardware acceptance.

Reviewed tree: `cdba1b2c7fce0d098e8a8858275505932892b072`. Source base: `a032c6d6e3775f145349d5a495c1e1ad12294936`. Previously reviewed head: `c7e87c8c87494f3444000b46954648ba1a94dcb8`. The three new commits are `50275e295b9feb25762159202ed949e7cd4a5a01`, `3f5cebd0dab688db937357ffefab07b7a89fe0e3`, and the reviewed head. They change four files: the NX harness, its format mutation driver, the testing guide, and context-engine comments.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [issue #775 and its frozen ruling](https://github.com/kebag-logic/milan-fpga/issues/775#issuecomment-6379902989), the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/777#issuecomment-6381709748), REQUIREMENTS.md, FR-STR-03, architecture and listener interface authorities, then the base-to-head diff and history. Public evidence followed the independent source pass. The named prior findings were read after that pass. No private author material, other current-round report, or management checkout was read.

The governing public ruling interprets Milan v1.2 Table 5.6 and 4.4.2.2: a rejected off-format received PDU advances sequence state, counts only UNSUPPORTED_FORMAT, and presents nothing. This report applies that ruling; it does not claim a fresh independent reading of an external standards archive. Round-1 coverage carries forward for unchanged artifacts and dependencies. The changed tests, documentation, and RTL comments were examined at this head.

R686-2-F1 - MINOR - Conformance, Tests, Docs - the committed driver reports a two-copy mutation but constructs only the engine copy.

- Artifact: `tb/verilator/avtp_rxmon/format_mutants.py:22-31`, `:130-164`, `:200-204`; `docs/testing/TESTING.md:617`; PR #777's round-2 mutation table. `delta_inspection.json` records generated source files at the driver's build boundary. `receipts/format-mutants.log` records its actual generated verdict text.
- Authority/evidence: assignment item 1 explicitly requires each defect to be planted in the engine and lockstep reference together. `run_mutant()` merely checks the reference anchor at lines 146-147. It writes only `KL_avtp_rx_monitor_ctx_<tag>.sv` at lines 149-150 and invokes `nx-build` with that engine at line 151. No mutated reference is written or passed to a build. The N=4 recipe does not compile a reference. Nevertheless, lines 162-163 print “the defect in the engine and the reference.” Both inspected arms generate exactly one source file, and the reference remains unchanged. The guide and PR repeat the two-copy claim. The docstring acknowledges that NX does not compile the reference, but an anchor-existence check still does not perform the assigned planting.
- Impact: the durable gate's executed mutation population differs from its stated population and assigned method. Its 11/11 result proves engine mutations are caught; it does not itself execute the claimed two-copy campaign. This is a test implementation and generated-evidence defect, not purely wording RESIDUE. The separate archived reviewer probe exercises both copies successfully, so this finding does not allege that the new assertions or shipping RTL are incorrect.
- Required outcome: the committed regression must actually construct the paired mutations and validate the assigned two-copy case, retaining the independent named `[SQ]` failure requirement. Its guide, result messages and PR evidence must describe what that regression executes. Disposable probe success does not substitute for the assigned committed mutation arms.
- Verification: rerun the committed driver and inspect its engine/reference artifacts and build inputs. Both cases must be planted as claimed; `[SQ4f]` and `[SQ5c]` must fail for their intended causes. Re-run the archived `probe_lock_settle.py` and focused suite at the corrected head. This is the remaining assignment-method portion of R685-1-F1, tracked here at its precise cause.

The Conformance attribution concerns the explicit round-2 task contract, not a new wire-protocol defect. The original issue's functional acceptance remains satisfied.

| Prior finding | Disposition at this head |
|---|---|
| R685-1-F1, MINOR, Tests/Docs | Partially resolved. `[SQ4]` grades the unlocked first-reject case and first accepted PDU's MEDIA_LOCKED increment. `[SQ5]` grades both settle boundaries. Independent paired probes fail the named checks. The broad “writes only prev_seq” guide claim is replaced with specific measurements and a watchdog exclusion. The committed paired-mutation implementation remains open as R686-2-F1. |
| R685-1-F2, RESIDUE, Docs | Resolved. Context-engine lines 19-23 separate its rule from the flat instrument's contract. Lines 96-100 contain the exact requested delta text: “it does not compare the channel count with the current format (#765), and its format reject does not advance prev_seq (#775).” Comment-stripped equality is independently verified. |
| R685-1-F3, SUGGESTION, Tests | Retained as out of scope under the assignment. AAF watchdog preservation remains ungraded across a reject; the guide explicitly says so. The manager owns any follow-up issue. No new shipping defect is asserted. |
| R686-1 | Its positive report raised no findings. Unchanged artifact coverage carries forward; this round's specific finding supersedes clean coverage for its affected lenses. |

No additional BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION was found in the round-2 delta.

[R686] PASS RTL - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:19-23,96-100,1013-1022`; `delta_inspection.json` - both revisions preprocess to the same 804 nonblank lines, SHA-256 `026a45f41d0e12df857d1a12ea1e4333945cf6d291777731d1d06321815dc700`. No executable RTL, port, clock, reset, state encoding, RAM layout or service timing changes in round 2. Existing sequence-only AAF writes and the CRF branch retain R686-1 coverage. No route rerun is required by the assignment's condition.

[R686] PASS Robustness - `tb/verilator/avtp_rxmon/sim_main_nx.cpp:1066-1173`; `receipts/lock-settle/SUMMARY.txt`; `receipts/nx-run.log` - the fresh binding is observed unlocked before rejection, remains unlocked without counting a lock at rejection, then counts exactly one lock at the first accepted PDU. The settle case observes one PDU remaining and places gaps on both sides of its boundary: the first does not count and the second does. Acceptance, payload absence, format count, anomaly/event holds and accepted-frame totals remain checked. The 25 added assertions pass. Both planted causes fail the intended assertions. Reset, isolation and sequence-wrap coverage carries forward from R686-1.

[R686] MINOR Conformance - `format_mutants.py:146-151`; round-2 assignment item 1 - F1 leaves the paired-planting requirement unmet. Separately, FR-STR-03 at `docs/reference/FR_NFR.md:271`, the unchanged AAF/CRF sequence paths, and `[SQ4]`/`[SQ5]` behavior satisfy the functional rule.

[R686] MINOR Tests - `format_mutants.py:146-164`; `receipts/format-mutants.log` - F1 remains open. The count checks themselves are effective: clean NX is 194/0; lock-set fails `[SQ4c]`/`[SQ4f]`; settle-decrement fails `[SQ5c]`/`[SQ5d]`/`[SQ5g]`. With both copies mutated, lockstep remains 116/0 and 119/0, demonstrating that count assertions supply detection. The archived probe was rerun without source changes. Existing `[SQ0]`-`[SQ3]` expectations and counter/sequence/timestamp baselines remain equivalent through helper extraction. Published restart-mutant evidence also shows `[SQ5d]` failing with got 0, expected 1.

[R686] MINOR Docs - `docs/testing/TESTING.md:617`; `format_mutants.py:22-31,162-163`; PR #777 - F1 leaves the campaign description inaccurate. The rest of the changed guide accurately distinguishes settled, fresh-era and settling cases, mr grading, and the ungraded watchdog. F2 is corrected. Added source comments explain behavior/reason with issue references; no new bench lane label, reviewer identity, review round or issue-comment identity was found.

Reviewer-owned coverage ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | Issue ruling; round-2 assignment; FR_NFR:271; ctx:1013; CRF:598; format_mutants:146-151 | R686-2, carrying unchanged R686-1 functional coverage | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |
| RTL | CLEAN | ctx comment delta/preprocessor equality; unchanged ctx/CRF/reference logic; lockstep executions | R686-2, carrying unchanged R686-1 logic coverage | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |
| Robustness | CLEAN | sim_main_nx:1066-1173; NX and paired-probe receipts; inherited reset/wrap/isolation coverage | R686-2 | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |
| Tests | UNCLEAN, F1 | NX refactor/new arms; both mutation drivers; paired probe; behavior suite; sweep receipts | R686-2 | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |
| Docs | UNCLEAN, F1 | TESTING:617; ctx:19-23/96-100; driver documentation/output; PR #777; docs receipts | R686-2 | c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 |

Independent executions:

| Execution | Result | Receipt |
|---|---|---|
| Clean NX | 194 checks, 0 failures | `receipts/nx-run.log` |
| Clean lockstep N=1 / N=8 | 116/0 and 119/0 | `receipts/lockstep1.log`, `receipts/lockstep8.log` |
| Committed format campaign | 11/11; two-copy claim qualified by F1 | `receipts/format-mutants.log` |
| Existing lockstep campaign | 14/14 | `receipts/lockstep-mutants.log` |
| Archived lock/settle probe, engine-only and paired variants | Both causes fail named NX checks; paired lockstep passes at both shapes | `receipts/lock-settle/` |
| rtl-fast behavior step: `cd tests && behave --no-capture -f plain` | 14 features, 406 scenarios, 1,977 steps; zero failures/skips | `receipts/behave.log` |
| Lint including self-test, four jobs | rc 0; 89 findings within ratchet 89 | `receipts/lint.log` |
| Docs check | rc 0; zero findings, scrub 23/23, routing 4/4 | `receipts/docs-check.log` |
| Comment equivalence / driver construction observation | Equal RTL; only engine mutation constructed | `delta_inspection.json` |

`run_checks.py CHECKOUT PACKET PINNED_SIMULATOR` runs independent campaigns concurrently under one foreground process, with bounded compilation parallelism and `make -j16`. Simulator identity was verified as version 5.050, revision v5.050. Builds and mutation inputs reside under `scratch/`; temporary build-path links were removed. `inspect_delta.py` intercepts the driver's build entry only to inspect constructed inputs; this is not simulation evidence. The actual builds/runs have separate receipts. These focused rtl-fast steps do not constitute a complete local workflow replica: container execution and full banks were expressly excluded.

Public source evidence was checked at [archive commit 15b983df](https://github.com/kebag-logic/milan-fpga/tree/15b983dfebd59ad8b658d69bfb0bac237c1c27f2/review-evidence/775-r1). `public_hash_audit.json` verifies all 643 selected author receipt and archived probe files against the manifest's published SHA-256 values, with zero mismatches. Redacted bytes are compared with published hashes, not original-byte hashes. The archive commit reports signature status `N` (unsigned); no cryptographic signature was available to verify. This establishes content hashes against the pinned archive, not signer authentication.

`public_gate_summary.json` and `published_receipts/` preserve the checked totals: four exact-head source shards, 15 + 16 + 17 + 16 distinct suites, 64/64 passing, 2,189,642 checks, zero failures. The increase of 27 matches 25 NX assertions and two mutation arms. The suite log supports flat 97/0, NX 194/0, lockstep 116/0 and 119/0, and campaigns 14/14 and 11/11. Thirty static gates report rc 0; lint reports 89 <= 89. The exact-head docs receipt contains 44 entries: 42 executed with rc 0 under Make 4.3, plus two explicit skips, the host-runner contract and metadata-stripped docs step. In-place checks do not prove metadata-stripped execution. Field campaigns and freshness arms skipped for an absent generator contribute no executed validation.

These are author source-head executions. There is no manager source bank at this head. Round-1 synthesis and route evidence retains its earlier source attribution; executable RTL equality supports carrying it forward under the assignment. No new route, full parent/processor/synthesis/builder bank, hardware test, or hosted execution audit was performed here. Physical calibration is NOT RUN. Routed timing and field skips are not hardware proof. Hosted skipped contexts must not be described as executed jobs.

The manager owns F1 resolution and re-review, reconciling the other independent review, watchdog/flat-instrument follow-ups, hosted/local-replica acceptance, current-dev candidate construction and builder/native banks with linked receipts, explicit maintainer merge authorization, post-merge containment, and issue/project closure. The assignment names live dev `a032c6d6e3775f145349d5a495c1e1ad12294936`; the merge turn must use the then-current dev. This report does not certify that future candidate.

Final `integrity.json` verifies all 1,441 parent tracked blobs, modes and index entries, plus the required processor, axis and stack submodules and lwSRP against exact gitlinks and tracked bytes. All match; status is clean and diff checking passes. The unused external submodule remains uninitialized. No tracked source edits, commits, pushes, GitHub writes, author contact or merge occurred. Measurement/verdict receipts are retained with installation paths normalized for publication, and original/published hashes in `receipt_redactions.json`; originals and disposable artifacts remain under unpublished `scratch/`. Only manifest-listed files and this report are publishable.

R686-2 FINISHED
