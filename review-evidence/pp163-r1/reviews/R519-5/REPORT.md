[R519] POSITIVE - exact head 8947bafdd62b4bf991debf7bfd8cdb73994a3a81

All five lenses are CLEAN for this source delta. R518-2-F1 is resolved. The timing-input finding remains resolved, and the `c4539ff1` timing record stands for this comment-only HDL change. No open BLOCKER, MAJOR or MINOR remains. The retained suggestions below do not prevent this verdict. This is not acceptance of the future parent adoption candidate or routed timing.

Reviewed tree: `9436b17406d7f6a1f9241331781bcc09a5d72633`. Source base: `86a7b0c57831c15e9cd8b42d64cc4a9843f4e726`. Delta base: `c4539ff107a6a4c7d2e4a4844182b00a2bf33c82`; commits `740b15b346baad13fc17954cc4c8aa6335872c58` and `8947bafdd62b4bf991debf7bfd8cdb73994a3a81`. [Public review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/166#issuecomment-6037066303).

Reconstruction covered the supplied instructions, absence of tracked AGENTS.md/CONTRIBUTING.md, docs/README and repository README, [issue acceptance and frozen scope](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163), the [round-4 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6033185530), the requirements/interface authorities, full base-to-head diff and history, and then public evidence. The independent diff pass preceded consultation of prior public finding comments. No linked review report file or current peer report was opened. The six earlier public finding comments, and empty submitted/inline review surfaces, are preserved for explicit disposition.

Authorities examined include `docs/00_MILAN_COMPLIANCE_REVIEW.md` REQ-NOT-004 and REQ-SCP-003; `02_interfaces.md` class-A streaming; `03_packet_engine.md:195` and `:488` originator, release and arbitration contracts; `06_aecp_engine.md:877` availability cancellation; `08_timing.md`; `09_verification.md:297`; and the public #638 measurement recipe and recorded bound parameters. The historical full diff contains 47 files, including merged #42/#69 work. This delta contains seven files; its sole HDL edit is the top comment. [Source lineage](receipts/source-lineage.json), [history](receipts/history.txt), [full diff](receipts/full.diff), [round-4 diff](receipts/round4.diff).

**R518-2-F1 — MINOR — Conformance, Robustness, Tests, Docs — RESOLVED.** This also resolves the underlying R519-2-S2 suggestion, which R519-4 had subsumed into F1. Artifacts: `tb/pp_top/notify_phases.hpp:2005`, `notify_mutants.py:424`, `sim_main.cpp:14064`, `docs/architecture/03_packet_engine.md:488`, `hdl/top/protocol_processor_top.sv:4444`, and the WD README at `tb/pp_top/README.md:2553`. Authority: acceptance item 2 and round-4 assignment items 1–4. Previous impact: withdrawal by the release term allowed mask removal or an extra mask clock to escape WD and the default build. Required outcome: prove the parked coincidence, next-clock withdrawal before start, and absence of the probe on the wire, with the requested negative controls.

WD4 now registers two controllers through the receive face, sends row 1's first probe, and queues row 0's probe and row 1's retry behind a held answer. Row 0's TIME_LIMITED drain coincides with row 1's matched response and the arbiter's selection of row 0. The three observed clocks distinguish the mask from release:

| Clock | Observed behavior in the clean control |
|---|---|
| c | Cancellation asserted; both exchanges live; arbiter idle with two queued attempts and no serializer start |
| c+1 | Matched-response report for owner 1; its slot 2 released; arbiter holds row 0's slot 3 in start state, with start suppressed |
| c+2 | Row 0's slot 3 released; arbiter idle; no start; exchanges and queue empty |

The check also requires two distinct slot identities, both solicited answers, one targeted DEREGISTER, exactly one row-1 wire attempt, no row-0 probe, and complete pool recovery after a 1.5-second observation. The compressed fixture postpones only an already-armed timer deadline located by owner tag; it does not deposit cancellation, mask, queue or arbiter state. The existing sixth build independently passes the same check with the top's TIME_LIMITED default and no deadline deposit. The check never reads the mask register itself, so removal of its readers is graded behaviorally rather than as a compilation failure.

Reviewer executions at this head:

| Execution | Result | Raw receipt |
|---|---|---|
| `ctl-withdraw` | PASS; 4 checks, zero failures | [control](receipts/runs/probes/ctl-withdraw.log) |
| `r-wd-mask-dropped` | KILLED by WD4 only; completed 4-check run | [probe](receipts/runs/probes/r-wd-mask-dropped.log) |
| `r-wd-two-clocks` | KILLED by WD4 only; completed 4-check run | [probe](receipts/runs/probes/r-wd-two-clocks.log) |
| `r-full-mask-dropped` | KILLED by WD4 only; completed 9,975-check run | [probe](receipts/runs/probes/r-full-mask-dropped.log) |
| `r-full-two-clocks` | KILLED by WD4 only; completed 9,975-check run | [probe](receipts/runs/probes/r-full-two-clocks.log) |
| New shipped mask-removed and two-clock arms | 2/2 KILLED at WD4; golden PASS | [structured results](receipts/runs/shipped/results.json) |
| Clean default top build | 9,975 checks, zero failures | [run](receipts/runs/default-run.log) |
| Default-timeout WD replay | 4 checks, zero failures; no deadline deposit | [run](receipts/runs/shipping-withdraw.log) |
| Arbiter / originator / notification suites | 66/66, 107/107, 65/65 PASS | [arbiter](receipts/runs/tx_arbiter.log), [originator](receipts/runs/originator.log), [notification](receipts/runs/aecp_notify.log) |
| Plant audit | 298/298 patches; 91 notification arms, 101 edits; no removed arms or refusals | [audit](receipts/plant-audit.json) |
| Documentation gates | PASS | [tracked-tree log](receipts/docs-check-tracked.log), [return code](receipts/docs-check-tracked.rc) |

All six faulty mask executions build successfully, complete their run and fail WD4 with setup, coincidence and release-order premises intact; both withdrawal and wire checks fail. Refused edits, failed builds and missing tallies receive no kill credit. [Requested-probe results](receipts/runs/probes/results.json). The complete 91-arm campaign and seven-build aggregate of 10,469 are published source evidence in the [round-4 packet](https://github.com/kebag-logic/milan-fpga/tree/350e06ae86bd5372f9f79b5fa5c95e0f3863b5d2/review-evidence/pp163-r1/author-r4), not fresh full-campaign executions by this reviewer. This round independently executes the two new arms, five requested probes and focused suites above. The manager's stated full source static/builder and native-bank passes remain distinct from final-candidate validation.

**R519-2-F1, its R519-3 carry, and R518-2-S2 — MINOR / SUGGESTION — Conformance, Tests, Docs — RESOLVED, closure retained.** Artifacts: the public `author-r3/measurement-m3final/inputs-digest/` addendum, record output, and `author-r4/measurement-digest/inputs-components-8947baf.json`. Authority: frozen measurement-input binding requirements. Previous impact: unavailable components prevented independent reconstruction of the measurement identity. Required outcome: publish component bytes and order sufficient to reproduce the digest. R519-4 closed this at `c4539ff1`; this review independently verifies the new delta rather than silently treating the old byte digest as current.

All 46 measured processor components were rehashed against both revisions. The four supplied generated inputs and clock constraint also match their records. The 124-component inventories differ only at component 46; all 21 generic strings and six image identities are unchanged. Comment removal preserves quoted strings and directives; the only changed HDL lines are comments, with **zero non-comment changed lines**. The aggregates reproduce exactly:

| Identity | SHA-256 |
|---|---|
| `c4539ff1` inputs | `24ba6a244a83a0b764e6de5131a9c94752135f01ecab5afad83258c7b4767be1` |
| This head's inputs | `09369bc8e21e2dc00a94de148b927a4f41602ac282b18dc8bdbb12a6b5d7eaa9` |
| Component 46 before | `64a6c7f812fb220e6ef0eb0c6f6c9c5dfe00a93c576b55a10a0f5d00243bc4ff` |
| Component 46 now | `7abc4b2b9af751211a543f47849bd9d4e7682a52d62899a68d1fdbf5172408e4` |

[Independent digest audit](receipts/delta-digest-audit.json), [replay output](receipts/delta-digest-audit.log), [timing judgment](receipts/timing-record-judgment.json). Unchanged parent/dependency component provenance retains R519-4's accepted audit; it was not rebuilt here. All 43 downloaded non-manifest artifacts match their publication hashes. The old `replayed` field in the new inventory is historical; the current aggregate is explicitly identified by `inputs_sha256_8947baf` and independently reproduced.

The `c4539ff1` OOC record therefore stands for this head: **WNS +3.337 ns, WHS +0.159 ns, maximum arbiter depth 16, zero pairs above 20**. The histogram sums to 17,990 pairs; all six published preparation/measurement/query return codes are zero. Own logic remains -110 LUT/+6 FF against merged main, within the assigned limits. This is source-equivalence and published-measurement verification, not a new synthesis, implementation sweep or hardware measurement.

**R518-1-S1 / R519-1-S1 / R518-2-S1 — SUGGESTION — Robustness, Tests, Docs — RETAINED, NARROWED.** Artifact: public cone/path transcripts and grouped summaries. Authority: acceptance items 1–2 require all arbiter input cones. Impact: traversal commands are now inspectable, but complete before/after pair tables, explicit pin inventory and summary transformation remain unavailable. Optional required outcome: publish the remaining extraction artifacts or complete replay bundle. Verification: reproduce 187 cells/561 pins, 263,154/17,990 pairs, 146,535/0 above-20 counts and no-slack accounting. No incorrect path or measurement is established; no lens is unclean.

**R518-2-S3 — SUGGESTION — Docs — PARTLY RESOLVED.** Artifacts: `docs/architecture/09_verification.md:300`, `:313`, `:320`; `tb/aecp_notify/README.md:15`. Authority: prior public documentation-discoverability suggestion. WD/CX, `--withdraw-only`, and the six-section count are now indexed correctly. Remaining impact is only source-prose readability of the long README sentence. Optional exact outcome: wrap that sentence after “CA:” and after “registry”, preserving every word. Verification: unchanged rendered sentence and passing documentation gates. This remains a formatting suggestion, not an open acceptance defect. [Complete prior-finding disposition](receipts/prior-findings-disposition.json).

The ledger below is reviewer-owned. Each lens was applied separately to the listed artifacts; earlier coverage is carried only where source identity and the examined delta support it.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance/round-4 scope; documented availability cancellation and streaming contracts; WD4 premises and wire outcome; timing/source binding | R519-5 delta; unchanged source scope from R519-1/-2 and timing provenance from R519-4 | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |
| RTL | CLEAN | Top mask stage/reset and all three readers; originator response-before-cancel action priority; arbiter age/class/index selection and pre-start abort; no non-comment HDL delta; arbiter 66/66 | R519-5 inspection and execution; unchanged implementation from R519-1/-2 | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |
| Robustness | CLEAN | Parked drain versus matched response; distinct releases, held EOF, slot recovery, absent retry/probe; default-timeout replay; originator 107/107 and notification 65/65 | R519-5, closing R518-2-F1 carried in R519-4 | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |
| Tests | CLEAN | Four requested fault probes and clean control; two shipped arms; default 9,975; no-deposit WD; 298 patch/91 arm plant audit; complete tallies and build status | R519-5 executions; published complete campaign and unchanged prior suite coverage explicitly distinguished | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |
| Docs | CLEAN | 03 withdrawal row, top comment, WD README, 09 catalogue, current PR-body round; reproduced measurement identity; documentation gates; prior finding dispositions | R519-5; R519-4 timing closure retained | 8947bafdd62b4bf991debf7bfd8cdb73994a3a81 |

Real limits and pending manager duties:

- Build and validate the final current-dev candidate at the merge turn. The source review base above and parent dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` are different objects. No parent candidate was constructed or approved here. Both independent reviews and the remaining completion bar are required before merge.
- Run the adopted-pin parent three-directive sweep and require at least +0.03 ns on every directive. OOC provenance and unchanged logic do not establish routed closure. The PR correctly retains “Relates to #163”.
- Hosted/local workflow acceptance remains manager-owned. At the recorded observation, both exact-head hosted runs had successful documentation and portability jobs; suite jobs were in progress, and the cached compiler-build step was skipped. Neither an in-progress job nor a skipped step is credited as an executed pass. See [hosted run inventory](receipts/hosted-runs.json) and the two `hosted-jobs-*.json` receipts.
- Physical calibration is **NOT RUN**. Field skips and software tests are not hardware proof. No full parent, processor-bank, clock-bank, synthesis or builder-bank rerun, fresh normative-PDF audit, route, hardware operation or hosted-workflow execution was performed by this reviewer.
- The first documentation attempt used a metadata-free export and failed Git-dependent inventory checks. The corrected tracked-tree run passed. Two reviewer audit-script preparation corrections are also disclosed in [preparation notes](receipts/preparation-notes.json); none is counted as a design failure or a passed test.

All processes were foreground and joined. Disposable builds and probes are confined to `scratch/`. Compiler identity was checked before execution; concurrency stayed within 16 build workers and the 12 GiB unit cap, with no out-of-memory events. [Execution records](receipts/runs/execution.json), [unit runs](receipts/runs/units.json), [resource receipt](receipts/resources.json). No source fix, commit, push, merge, GitHub write, author contact, shared install, privilege or other-checkout edit was performed.

Final [checkout verification](receipts/checkout-integrity.json) matches all 581 tracked blobs, modes and index entries to the assigned tree; status is clean. This processor tree has no gitlinks. Public metadata for the recorded parent and supplied live dev confirms clock-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` and stream-library `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Their processor pin is still `ead8036035affd53ef4b29979190f2f4f67084c0`; the measurement's explicit `c4539ff1` substitution and this review's comment-only equivalence are separate from future pin adoption. Required candidate gitlinks and post-merge containment remain manager duties.

[Portable scripts](scripts/README.md) and raw receipts are selected by `MANIFEST.sha256`, with packet-relative paths. `scratch/` is never published.

R519-5 FINISHED
