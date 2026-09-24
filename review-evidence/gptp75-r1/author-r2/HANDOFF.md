[A272]

PR #76 / issue #75, Round 2.

Head: `4a897e44243d39945df763d00b96049363a58e78`

Branch: `75-slew-active`

Round 2 base: `49d23b20fcad15a3c03554476d8b8c9116b3b375`

Source base: `e5dcea6e351abff18a27a00f8e345f3251bdbd8f`

Commit subject: `Pin inactive slew lifecycle checks and refresh source evidence`

## Review response

The [assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/75#issuecomment-5818374671) and both reports were read in full: [R304-1](https://github.com/Mister-M-alt/FPGA-gPTP/pull/76#issuecomment-5818298785) and [R305-1](https://github.com/Mister-M-alt/FPGA-gPTP/pull/76#issuecomment-5818368508). Their public scripts, harness diffs, and receipts were fetched read-only from the specified archives into temporary scratch.

F1: Added public-wire checks for an inactive 400 ms Sync receipt lapse, an inactive GM identity change followed by in-band pairs, and an in-band first pair after returning from mastership. Each pair verifies offset consumption, one rate write, expected steps, PI arithmetic, and the level's complete edge history. The first two scenarios retain capability; the GM-change scenario checks the newly selected identity and slave role. The return scenario follows an active correction retired by mastership.

| Defect | Committed control | Required named failure |
|---|---|---|
| R304 R14 / R305 R01 | `slew idle lapse arms qualification` | `slew: in-band pair after idle timeout stays inactive` |
| R304 R07 / R305 R06 | `slew mastership keeps qualification` | `slew: in-band return from GM stays inactive` |

F2: Refreshed all engine anchors, fixed the pre-existing blank-line parser anchor, and added the slew port/PHC word 2/word 3/policy row. The committed `scripts/check_source_evidence.py` binds each local claim to exact source text. The documentation gate runs it and its seven positive/negative controls. All 20 local line anchors report EXACT. The pinned remote parent link remains outside this local check.

Suggestions: Recorded 1,008/1,024-word ROM usage, 16 free words, prefix packing at addresses 0..15, dispatch/reset invariants, and gap-fit requirements. Updated the PHC status row and documented the region-3 flags hook in the HDL guide. The mutation guide now records the asCapable-only arm's reachability argument and its dependency on the 375 ms Sync watch versus capability recovery cadence. This argument remains code reasoning, not an executed proof.

RTL, the generator, and all ROM images are unchanged in this round. No parent files were edited and no hardware action occurred.

## Validation

The full required local gate and the explicit engine mutation target both returned 0. No suite skipped. The results cover this exact committed content.

| Check | Result |
|---|---|
| Engine, shipping and both seeded images | 1,586/1,586 each |
| Engine mutations, both invocations | 32/32 caught; clean control passed |
| Arithmetic | 768/768 |
| Parser | 268/268 |
| Adapters | 81/81; 4/4 mutations caught |
| Independent packet generation | 288/288; 3/3 mutations caught |
| Timestamp tags | Both tags passed |
| PHC contract and both lint gates | Passed |
| Documentation and diagrams | Passed, including their controls |
| Local source anchors | 20 EXACT; 7/7 checker controls |


Both unchanged reviewer drivers ran the required two-defect subsets against an export of this exact head. R304 indices 6/13 and R305 prefixes R01/R06 all report caught, with the corresponding named failure; both clean controls pass 1,586 checks. The R304 idle-lapse mutation also fails the GM-change and return checks. These were executed on the committed harness without adding the reviewers' temporary harness patches.

Receipts:

- [Full required local gate](all-result.json), [complete log](all.log).
- [Explicit engine mutation target](engine-mutants-result.json), [complete log](engine-mutants.log).
- [Reviewer commands and results](reviewer-results.json), [script identities](reviewer-script-identity.json).
- [R304 log](reviewer-r304.log), [R07 failure](reviewer-r304/reviewer_06.json), [R14 failure](reviewer-r304/reviewer_13.json).
- [R305 positive control](reviewer-r305-control.log), [R305 mutations](reviewer-r305.log).
- [Exact anchors](source-evidence.log), [ROM byte comparisons](rom-regeneration.txt).
- [Head and scope](head.json), [source hashes](candidate-sources.sha256), [validation environment](validation-environment.json).

The repository has no hosted workflow files. Every required local gate ran in the foreground with its direct exit code recorded; no gate output was piped. All four tracked ROM images regenerate byte-identically. Optional synthesis and board targets were not rerun for this tests-and-documentation change.

The public evidence archives were `d62575884fce9f595595a2a22726d2f850e29a29` and `281c6ee3bba29354af04952170d6ee1d630dab9e` on `kebag-logic/milan-fpga`, branch `gptp75-review-evidence`. Both mutation drivers match the archived bytes and their manifest hashes. Ten archived text receipts differ from their embedded manifests, and one bytecode cache is absent; [the archive check](review-archive-check.txt) records this. Validation above uses new executions. Fetched evidence, exported trees, and scratch builds were deleted after use.

## Remaining integration work

The [updated PR body](PR-BODY.md) is ready for the manager; the PR was not edited and the branch was not pushed. Parent #545 owns the new port connection, consumer gates, and mastership retirement addend validation. The manager must accept or revise the ±100 ns/two-pair tolerance and reconcile the parent's 0.5 s premise with measured intervals of 3.069413 s and 1.916689 s. Lost capability or missing measurements can hold the correction indefinitely. Field behavior and the final merge candidate remain separate validation duties.
