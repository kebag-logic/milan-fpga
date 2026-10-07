[R539] POSITIVE - exact head 4eba61b7b1c49fc9b7260a487240ca86f9d38168

The history and source-anchor findings are resolved. All five lenses are CLEAN for this licence change. Two previously reported wording residues and one evidence suggestion remain non-blocking.

Reviewed tree: `bf90243127da3e4d22eaeef1402542f1095ee263`. Source base: `1401654530ce7d9275de9b901e67df47e5bbc536`. Scope is [issue #8](https://github.com/kebag-logic/lwSRP/issues/8), [PR #9](https://github.com/kebag-logic/lwSRP/pull/9), the [release requirements](https://github.com/kebag-logic/lwSRP/issues/1), and the [R539-2 assignment](https://github.com/kebag-logic/lwSRP/pull/9#issuecomment-6033178004).

Reconstruction followed the requested order: supplied guidance and CONTRIBUTING.md; README and documentation; frozen acceptance and public scope decisions; linked licence/interface authorities; independent diff and history; public executable evidence. No repository AGENTS.md exists. The [independent verdict and five-lens ledger](receipts/independent-ledger.md) were written before either previous review was read; the [record](receipts/independence.txt) includes their digest and timestamp. No private author material, management storage, other checkout, or concurrent review report was inspected. No source fix, commit, push, or GitHub write occurred.

**History and behaviour preservation**

A fresh clone fetched all six publication branches. `git rev-list --all` covers 35 commits and 209 unique blobs. Scanning every commit object, every historical path and every reachable blob found zero excluded-name matches; the removed root file is absent throughout. The [audit](receipts/audit.log) records branch tips, counts and results. Separate [provenance screening](receipts/provenance.json) found only Apache-2.0 identifiers and no competing licence, private-path or credential marker.

The public PR #12 [force-push event](receipts/force-push.json) supplied the original branch head. Its 35 ancestors were fetched into a separate scratch repository. [One-for-one comparison](receipts/history-preservation.log) verifies author and committer identities, timestamps, message bytes, parent topology, file modes and every blob outside the two authorized removals. This independently reconstructs the commit map. Both removals occur in 24 historical trees. Two commit signatures disappear during rewriting; authorship is preserved.

The licence head maps from `1a1d6cbe4f971d2d346b948dd2e9716421f211e9` to the reviewed head with an identical tree. The other open PR head also retains its tree. The main and documentation tips retain theirs. The f4-stack and tests-harness tips differ only by the authorized file/line removals; this does not imply that every historical branch tree is identical.

Against the source base, 33 files change: LICENSE and NOTICE are added, 27 files gain only SPDX comment lines, and four guides receive source-anchor corrections. Removing the new comment restores each executable/configuration/test file byte-for-byte. Documentation prose and graph syntax are unchanged. [Merge replay](receipts/merge-preservation.log) confirms the README uses main's version and the deleted placeholder stays deleted; licence files equal the original licence commit's blobs.

**Previous finding disposition**

The prior findings were read from the [internal round-one review](https://github.com/kebag-logic/lwSRP/pull/9#issuecomment-6031584521) and [external round-one review](https://github.com/kebag-logic/lwSRP/pull/9#issuecomment-6031639662), after the independent verdict. The [public-record receipt](receipts/public-record.json) records all observed discussion entries.

- **R538-1-F1 / R539-1-01 — MAJOR — Conformance, Robustness, Docs — RESOLVED.** Artifact: the former historical root guidance file and architecture reference. Authority: the release privacy rule and the authorized history rewrite. Impact was disclosure through published branch history. Required outcome was removal across all publication branches while preserving attribution and behaviour. Verification: zero matches across all six fresh branch histories; all 35 commit pairs pass preservation checks. Old closed-PR reachability remains a separate manager duty, as explicitly scoped for this round.
- **R539-1-02 — MINOR — Conformance, Docs — RESOLVED.** Artifact: source citations in the developer, integrator, manager and tester guides. Authority: evidence must support the linked numerical and clause statements. Impact was incorrect or incomplete selected source text. Required outcome was correction of every shifted range. Verification: 68 shifted ranges and one already-correct range select byte-identical evidence to the base. `mrp.h:119` contains the Leave interval of 60; `mrp_mad.c:162–163` includes the LA transition; `msrp.c:353–354` includes the address initializer. All 290 local links pass. This semantic range comparison goes beyond the link checker's existence and bounds tests.

**Retained non-blocking findings**

**R539-2-01 — RESIDUE — Docs — retained R538-1-R1.** Artifact: `doc/tools/README.md:31`. The sentence still describes the separate licence change as pending. Both files now exist. Authority/evidence: current tree and [local-link receipt](receipts/links-local.log). Impact is purely prose tense; it changes no test, measurement, conformance claim, generated artifact or privacy rule. Exact required fix:

```markdown
The [licence](../../LICENSE) and [notice](../../NOTICE) links are required and must resolve.
```

Apply that text in its original page context. Verification: inspect the replacement and rerun sentence, reference and local-link checks. The [negative probes](receipts/probes.log) confirm missing licence files already cause link-check failure; no checker change is needed.

**R539-2-02 — RESIDUE — Docs — retained R538-1-R2.** Artifact: `doc/manager.md:85–87`. The release licence paragraph retains prospective wording. Authority/evidence: the current licence files, issue #8 and the same local-link receipt. Impact is only prose chronology, with no change to a result, claim, behaviour or privacy rule. Replace those three lines exactly with:

> The [release issue](https://github.com/kebag-logic/lwSRP/issues/1) required the licence and documentation before publication.
>
> The [licence issue](https://github.com/kebag-logic/lwSRP/issues/8) added both files.

Verification: inspect those two sentences and rerun the documentation checks. The manager carries both residues to the residue checklist; neither leaves a lens unclean.

**R538-1-S1 — SUGGESTION — Tests — RETAINED for the older public packet.** Artifact: public `author/ctest.log`, `author/behave.log` and `author/links.log`. They lack their own exact commit identifiers; PART-A describes an earlier checkpoint. Authority/evidence: the [published packet](https://github.com/kebag-logic/milan-fpga/tree/9d6a0632c73f5a2c6fd61dc827f97f6014b60a85/review-evidence/lwsrplic-r1). Impact is evidence traceability; this review independently reproduces the successful suite figures. Recommended outcome: bind future logs to their tested head. Verification: compare each recorded head and source manifest. This packet supplies common [exact-head metadata](receipts/validation-metadata.json) and an independent per-file [integrity record](receipts/integrity.json). The older logs have not been relabelled as exact-head proof.

**Executed checks and evidence**

LICENSE is byte-exact against the [official Apache text](https://www.apache.org/licenses/LICENSE-2.0.txt): 11,358 bytes; SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`. NOTICE identifies lwSRP and Copyright 2026 kebag-logic without additional conditions. All 43 other tracked files have the correct SPDX comment: 22 C/header, eight Markdown and 13 hash-comment files. The shell shebang remains first. No competing licence or vendored implementation was found. The queue's algorithm attribution was inspected; repository provenance still relies on the owner's public authorship declaration and cannot prove original authorship independently.

| Check | Executed result | Receipt |
| --- | --- | --- |
| Licence, headers, executable preservation, semantic anchors, history | Exit 0 | [audit](receipts/audit.log) |
| Original/revised history comparison | Exit 0; 35 pairs | [history](receipts/history-preservation.log) |
| Isolated dependency and host configure/build | Exit 0; Make uses 16 jobs | [configure](receipts/configure.log), [build](receipts/build.log) |
| CTest and direct unit executable | Exit 0; nine tests, 1,690 assertions | [CTest](receipts/ctest.log), [direct](receipts/unit-direct.log) |
| Scenario execution and dry run | Exit 0; three scenarios, ten steps, none skipped | [execution](receipts/behave.log), [dry run](receipts/behave-dry.log) |
| Python, YAML schema, Kconfig, INI, shell parse/execution, excluded queue compilation | Exit 0 | [syntax](receipts/syntax.log), [shell](receipts/shell-execution.rc), [queue](receipts/queue-syntax.rc) |
| Disposable missing-file and invalid-comment probes | Six expected rejections | [probes](receipts/probes.log) |
| Local links, including all eight licence/notice references | Exit 0; 290 local links | [links](receipts/links-local.log) |
| Sentence and reference checks | Exit 0; 760 fragments, zero over limit; zero unlinked references | [sentences](receipts/sentences.log), [references](receipts/references.log) |
| Reference self-test | Exit 0; 79 cases | [self-test](receipts/references-selftest.log) |
| Authenticated external-link check | Exit 1; 17 pass, ISO page returns HTTP 403 | [external links](receipts/links-authenticated.log) |

The unit dependency was built only under disposable scratch. Header-sensitive parsers, shell execution and excluded queue syntax were rechecked in addition to the required build/CTest/scenario suites. Missing LICENSE and NOTICE fail the local checker. Invalid C, scenario, Kconfig and module headers are rejected by compilation, parsing or exact schema validation. No source mutation was made in the reviewed checkout.

All seven author artifacts match the pinned public manifest's SHA-256 values; see [verification](receipts/public-evidence-verification.json). PART-A's empty suite and scenario setup failure are explicitly historical. Later public logs report the same 1,690 assertions and three passing scenarios reproduced here. The manager's full source static/builder and native passes are stated in the assignment. No manager bank-result comments were present on issue #8 or PR #9 at observation, so those passes are not presented as independently inspected exact-head logs.

Exact-head hosted queries return zero workflow runs, zero check runs and zero status contexts; the aggregate status is pending. [Hosted receipt](receipts/hosted-state.json). No executed or skipped hosted context is counted as a pass.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Frozen issue acceptance; official licence and NOTICE; all 43 headers; ownership/notice scan; 35-commit rewrite comparison; source evidence ranges | R539-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |
| RTL | CLEAN — no applicable RTL change | All 45 files and 33-file diff; zero HDL/gitlinks; unchanged C interfaces, runtime source and build behaviour after comment removal | R539-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |
| Robustness | CLEAN | Six-branch disclosure scan; preserved identities/topology/blobs/modes; Python/YAML/Kconfig/INI/C/shell checks; six negative probes | R539-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |
| Tests | CLEAN | Isolated exact-source build, CTest/direct codec assertions, actual scenarios, parser checks, public manifest comparison and hosted query | R539-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |
| Docs | CLEAN; two RESIDUE items retained | All guides, 68 corrected anchors plus one unchanged range, 290 local links, sentence/reference checks; external access limit explicitly retained | R539-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |

**Limits and pending manager duties**

The external checker is not fully green: ISO returns HTTP 403. Repository links were tested with authenticated access; anonymous availability must be checked after publication. These are retained access limits, not hidden successes. Graph rendering was not repeated because graph bytes are unchanged. No embedded target build, hardware test, interoperability campaign, or full parent bank ran. No HDL simulator was needed or used. Finite name/notice scans are heuristic; they are not forensic proof of all possible provenance strings or authorship.

Physical calibration: **NOT RUN**. Field skips are not hardware proof. Existing protocol gaps and the scenario state-observation weakness remain documented and outside this licence change's acceptance. Passing codec assertions does not establish protocol conformance.

Manager note, **not a finding**: the hosting service retains old commits through closed PR refs. The manager is handling that separately; the clean history result covers all six fresh branch histories, not deletion of every retained hosting object. Commit signatures removed by rewriting also do not constitute preserved signature validation.

The manager retains the final current-dev candidate build and hosted/local-runner acceptance at merge time, using source base `1401654530ce7d9275de9b901e67df47e5bbc536` and live dev `09f1841bd2c6a9dea8eb1994d887f7386ca4f62d`. Source validation here does not approve that future candidate. The manager must also obtain the other independent review, carry the two residues, complete publication hygiene/access duties, and publish this packet.

[Final integrity evidence](receipts/integrity.json) confirms all 45 tracked blobs and modes, the index tree, exact head/tree, and every exported validation-source file. The original checkout is clean, including ignored files. There are no required submodule gitlinks or .gitmodules. All work ran through joined foreground processes; no background job remains. [Reproduction instructions](REPRODUCE.md) and portable scripts accompany the receipts. Publish only REPORT.md and files listed in MANIFEST.sha256; scratch is never publishable. Log path normalization is explicitly documented; unmodified originals remain in scratch.

R539-2 FINISHED
