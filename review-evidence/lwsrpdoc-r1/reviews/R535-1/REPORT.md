[R535] NEGATIVE - exact head 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65

One open MINOR fails the owner's graph-readability requirement.
An ownership edge is hidden behind an unrelated timer node.
Two prose residues also remain, including the carried layout correction.
The code comparisons and executed checks otherwise support the documentation's stated implementation limits and test results.

Reviewed tree: `e8bc64162172057dc185b67d0b4a19839819a78d`.
This is the standalone library review for [issue #1](https://github.com/kebag-logic/lwSRP/issues/1) and [PR #5](https://github.com/kebag-logic/lwSRP/pull/5).
The [public review start](https://github.com/kebag-logic/lwSRP/pull/5#issuecomment-6030839413) identifies this exact head.

The reconstruction followed the required order:

1. Read the supplied instructions, repository guidance, [contribution rules](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/CONTRIBUTING.md), overview and all documentation pages. No repository instruction file exists at this head.
2. Read the issue body, [assignment](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6030336537), and [scope update](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6030706379). The separate licence dependencies and authenticated repository checks are authorized exceptions.
3. Read the public interfaces and local normative standard. Compare the selected state transitions with [IEEE 802.1Q-2018](https://standards.ieee.org/ieee/802.1Q/6844/), Tables 10-3 through 10-6, including their conditions.
4. Independently inspect the change set from `19f5796` to the reviewed head and its four-commit history. Protocol source is unchanged. The executable files match the merged test fix.
5. Read the [public author archive](https://github.com/kebag-logic/milan-fpga/tree/3f31bba3bfade7da27bc45f42080aae9a9887a22/review-evidence/lwsrpdoc-r1). All eleven published file hashes match its manifest. See [hash receipts](receipts/public-evidence-hashes.json).
6. Write the [independent verdict and ledger](receipts/independent-verdict.md), then examine public review findings. No prior findings, formal reviews, or inline comments existed on this PR. Reconcile the explicitly carried [layout residue](https://github.com/kebag-logic/lwSRP/pull/3#issuecomment-6030780352) below.

**R535-1-01 — MINOR; Conformance, Docs.**

Location: [doc/developer.md:28](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/doc/developer.md#L28-L39).
The “Attribute list” to “Value and identity” edge crosses behind the “LeaveAll and periodic timers” node.
The [reviewer-rendered image](diagrams/doc-developer.md-28.png) shows the interruption at native size.
The [SVG](graphs/doc-developer.md-28.svg) confirms the curve crosses the unrelated node's rectangle.
Exact geometry is recorded in the [graph review](receipts/graph-review.md).

Authority: owner rule 4 and acceptance item 1 in the [release issue](https://github.com/kebag-logic/lwSRP/issues/1).
Successful parsing and a ten-node count do not satisfy the separate clean-layout requirement.
Impact: the figure obscures ownership and can suggest that attribute values belong to the port timers.
The [actual structures](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/src/core/mrp_mad.c#L59-L95) separate these relationships.

Required outcome: rearrange or split this graph so each ownership edge remains visible outside unrelated nodes.
Verification: render the corrected graph and inspect the complete edge at native and page widths.
Recheck the nearby data-structure explanation and the [PR body's readability claim](https://github.com/kebag-logic/lwSRP/pull/5).
This changes a figure, so it is not prose residue.

**R535-1-02 — RESIDUE; Conformance, Docs.**

Locations: [README.md:29](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/README.md#L29), [doc/integrator.md:16](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/doc/integrator.md#L16), and [doc/tester.md:10](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/doc/tester.md#L10).
The three C11 references are plain text.
Owner rule 2 requires standard references to be links.
The heuristic checker returns zero because its standard pattern does not include this identifier.
Its [documented heuristic limitation](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/doc/tools/README.md#L49) correctly requires manual review.

Exact fix: replace each prose `C11` with `[C11](https://www.iso.org/standard/57853.html)`.
The [standard's publication page](https://www.iso.org/standard/57853.html) was verified.
Impact is navigation only; the language requirement and conformance claim remain unchanged.
Verification: inspect all three links and rerun the documentation checks.
The manager carries this prose-only correction to the residue checklist.

**R536-1-01 — RETAINED RESIDUE; Docs.**

Location: [doc/architecture.md](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/doc/architecture.md), formerly the directory listing.
Authority: the [original finding](https://github.com/kebag-logic/lwSRP/pull/3#issuecomment-6030780352) and this review's explicit carry-forward instruction.
The obsolete placeholder listing is gone because the entire listing was removed.
The architecture page still contains neither the new runner nor the binding file.
Their links elsewhere do not complete the specifically requested architecture-page correction.

Exact remaining fix: add a short test-layout table to the architecture page with these two linked entries:

| Entry | Required relative link | Description |
| --- | --- | --- |
| Unit runner | `../tests/unit/main.c` | Codec suite runner. |
| Scenario bindings | `../tests/features/switch_bindings.c` | Switch wrapper bindings. |

Impact is the prose file map only; no test, measurement, figure, code, or conformance claim changes.
Verification: the architecture page names and links both current files and contains no deleted placeholder entry.
Keep this item on the manager's residue checklist until that outcome is present.

The acceptance assessment is independently supported by the following artifacts:

| Acceptance item | Result and evidence |
| --- | --- |
| 1. Rendered, small, readable graphs | All 22 render commands return 0; 2–11 named nodes or participants. One visual failure remains. [Inventory](receipts/graph-inventory.json), [individual assessments](receipts/graph-review.md). |
| 2. Resolving links | 269 local occurrences and 12 external URLs checked. Only eight authorized licence dependencies fail. Three repository URLs pass authenticated checks; nine external URLs answer anonymously. [Receipt](receipts/docs-links.log). |
| 3. Sentences at most 25 words | 708 sentences/fragments checked; zero over-limit results and zero prose exemptions. Literal fenced syntax is explicitly listed. [Receipt](receipts/docs-sentences.log). |
| 4. Reference checker | Returns 0 with no detected unlinked references. Manual review retains the three prose-only reference corrections above. [Receipt](receipts/docs-references.log). |
| 5. Every published command | All 16 occurrences executed, including duplicate quick-start commands and the complete isolated-test here-document. Every rc is recorded in the [command ledger](receipts/page-commands.md). |
| 6. Code-backed claims | The manager matrix, all six selected state graphs, implementation differences, build choices and test claims were checked. [Claim-by-claim evidence](receipts/code-claims.md). |
| 7. Publication privacy | Current documentation and added files contain no private host locations, private identities, or prohibited assistance identifiers. Removed instruction content remains absent. [Publication receipt](receipts/publication-audit.json). |

All four audiences receive practical usage guidance.
The developer guide covers extensions and state limitations; the integrator guide supplies six call-sequence graphs.
The manager guide bounds implementation and release evidence; the tester guide supplies commands, scenario-writing steps and coverage limits.
Short-sentence compliance passes. The reference rule has only the recorded prose residue; the graph rule has the open MINOR.
All original coding-style requirements survive in the [contribution rules](https://github.com/kebag-logic/lwSRP/blob/5f9b9d99e1d94485fc00a1b1539baf2ae861cb65/CONTRIBUTING.md#L8-L16).

The execution results reproduce the published measurements:

| Reviewer execution | rc and result |
| --- | --- |
| Both configure/build sequences | 0 for every command. |
| Both configured suite invocations | 0; one registered target passes. |
| Direct unit runner and isolated codec executable | 0 each; nine tests and 1,690 assertions each. |
| Both scenario executions | 0 each; one feature, three scenarios and ten steps pass. None skip. |
| Scenario dry run | 0; ten steps match. It executes no behavior. |
| Sentence, reference and graph commands | 0 each. |
| Link command | 1; precisely the eight allowed licence dependencies. |
| Negative sentence/reference/link/oversized-graph probes | 1 as expected; valid-link control returns 0. |
| Empty-suite mutation | Direct executable returns 0 without assertions; configured test command returns 8 and rejects it. |
| Authentication-routing probes | Correct repository/comment routing; foreign and unsupported URLs remain distinct. |

See the [command receipts](receipts/commands.json), [quick-start receipts](receipts/quick-start-commands.json), and [focused probe results](receipts/probes.json).
Dependencies and build trees were confined to disposable scratch.
Independent check, render and build campaigns ran concurrently inside joined foreground processes.
The unit dependency used a 16-job build; no hardware or parent build bank ran.
An optional preview dependency was initially absent; its scratch-only installation resolved that setup failure.
Versions, archive hash and both setup outcomes appear in the [environment receipt](receipts/environment.json).

The reviewer-owned ledger covers this exact head:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN | Frozen issue and scope decisions; seven acceptance items; local normative tables; manager matrix; graph finding | R535-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |
| RTL | CLEAN | Not applicable. Standalone C11 source/build inventory contains no RTL or programmable-logic implementation | R535-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |
| Robustness | CLEAN | Checker implementations and negative fixtures; allocation, timer, parser, callback, propagation and queue documentation against code | R535-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |
| Tests | CLEAN | All published commands; configured and isolated codec suites; scenarios; dry run; empty-suite rejection | R535-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |
| Docs | UNCLEAN | Eight pages; all 22 diagrams; audience paths; style migration; links; sentence/reference audits; graph finding | R535-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |

These clean lenses apply to this documentation change's acceptance, not general protocol or deployment correctness.
The documented timer lifetime defect, incomplete transmission, parser limitations and state-table differences remain real implementation limitations.
The current suites do not establish parser, state-machine, timer, target, or network-interoperability coverage.
The local standard comparison checked displayed transitions and the listed differences; it does not establish full standards conformance.

The [public snapshot](receipts/public-snapshot.json) contains zero exact-head workflow runs, check runs and commit-status contexts.
The empty combined status is labelled pending. It is neither executed success nor a skipped job.
No manager execution-evidence comment was present on the issue or PR at collection.
The supplied manager source-bank passes remain separate evidence; the public archive inspected here contains author documentation receipts.
No private author material, other checkout contents, or unpublished reviewer report was used.

The manager still owns publication, both independent-review requirements, hosted/local workflow acceptance, and the final current-development integration candidate.
Source base `19f5796` and live parent development `910f338dbd050f4efd2d96991ddcf928a583d55f` remain distinct from this standalone head.
The current PR base has moved; its identifier is recorded without changing the requested review comparison.
Verify the separate licence files in the combined release and repeat anonymous repository-link checks after publication.
Physical calibration is NOT RUN. Field skips provide no hardware proof.

The [final integrity receipt](receipts/integrity.json) verifies all 43 tracked file blobs, executable modes, index entries, HEAD and tree.
There are no staged, tracked or untracked changes in the reviewed checkout.
The standalone tree has zero gitlinks, so no submodule gitlink restoration is required.
All mutations were confined to scratch and the temporary executable replacement was restored.
No source fixes, commits, pushes, merges, shared installations or external writes were performed.

Portable scripts, rendered evidence and receipts are listed in [MANIFEST.sha256](MANIFEST.sha256).
Published process streams preserve output except absolute-path normalization; original streams and disposable trees remain in unpublished scratch.

R535-1 FINISHED
