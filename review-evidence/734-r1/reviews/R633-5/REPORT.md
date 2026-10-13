[R633] POSITIVE - exact head 7c862ad980dfe829ef4d85ff8f4fb4fab451984f

Round R633-5, external independent delta review of issue #734 / PR #735. Tree: `622e79ae2a21917a49426c675d417307104112a1`. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains open. One wording RESIDUE and one previously recorded optional SUGGESTION remain. This verdict covers the assigned merge review; hosted/replay acceptance and merge-candidate validation remain pending manager duties.

The merge has exactly two parents: previous reviewed head `59354ffe75697e17a16fd117d9ba853e104394bc` and dev `0136de16291a127e0a34627c77ac09cd41efc08b`. The original source base is `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`.

Scope was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the [issue contract](https://github.com/kebag-logic/milan-fpga/issues/734), and the public [initial assignment](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6151273761), [round 2](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6151933918), [round 3](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6152693618), [round 4](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6153494016), and [merge decision](https://github.com/kebag-logic/milan-fpga/issues/734#issuecomment-6154792285). Authorities include REQUIREMENTS.md:307-317, especially REQ-VER-04; docs/testing/CI_WORKFLOWS.md; and docs/reference/SUBMODULES.md:20. The original-base diff, parent deltas, merge reconstruction and lane history are retained as receipts. Product changes imported from #705 are checked for exact preservation, without reopening that lane's implementation review.

The independent verdict and ledger in `independent-pass.md` were written before reading prior public reviewer findings or reports. Those findings were then reconciled below. No private author material or management checkout was read. No source edit, commit, push, GitHub write, merge, host runner execution, replay execution, privileged action or delegation was performed.

The merge preserves both sides:

| File or artifact | Merge disposition | Evidence |
|---|---|---|
| `scripts/ci_events.py:598-600` | The only conflicted file. Keeps the lane's `PR_BASE_REF` and `PR_HEAD_SHA`, and dev's `FIRMWARE_BOUNDARY_RESULT` and `FIRMWARE_VERILATOR_RESULT`, with existing inputs. | `merge-resolution.diff`; four deletion probes each produce a named contract rejection, rc 1; pristine control rc 0. |
| `scripts/act_ci.py:255`, :13243, :13388 | Automatic merge retains the stack entry, six approved entries, five public pins, corrected lwSRP omission control, and four stack refusal controls. Live-base replay and complete flat-install self-test remain intact. | `merge-delta.diff`; `receipt-audit.json`: only two manifest test functions changed and the stack test function was added; every other existing function/class is structurally identical to the previous head. |
| `docs/testing/CI_WORKFLOWS.md:59`, :227, :1608, :1666 | Automatic merge retains the imported stack-boundary policy, live-base rule, candidate-bank requirement, inline fixtures and isolated single-file installation. | Both parent diffs; source hashes match the exact checkout. |
| All remaining paths | No other manual conflict resolution. Outside the ten CI/doc paths differing from dev, every tree entry equals dev in object ID and mode. Product inputs and gitlinks equal dev. | `final-tree.json`; `scope-lane.diff`; complete `merge-resolution.diff`. |

[R633] PASS Conformance - `.github/workflows/rtl.yml:98`, `rtl-fast.yml:36`, `elaborate.yml:84`; `scripts/ci_events.py:598`; `scope.log`; `b16-scope-delta.json` - The authorized live-base rule survives. Hosted scope compares the synthetic merge to its first parent. Replay composes the verified live ref with the PR head and compares that tree with live. All three complete selector steps are identical to the previous head. REV and REV+E remain relevant; B16 remains documentation-only. Source acceptance items 1-4, as amended publicly, and the round-five preservation requirements are satisfied. Acceptance item 5's complete remote evidence is not claimed.

[R633] PASS RTL - `final-tree.json`; `submodule-integrity.json`; `.github/workflows/rtl-fast.yml:614-630`; `scripts/act_ci.py:255`; `public-source/r5-images.log` - The merge preserves the imported product tree and stack pin exactly. The aggregate consumes both new firmware-boundary results. The approved dependency list includes the stack without weakening the existing trust/fetch interface. No additional datapath, clock, reset, CDC, width, FSM or product interface change was introduced by resolving the merge. Published linked-image measurements agree across all five configurations.

[R633] PASS Robustness - `scripts/ci_scope_history.py:18`, :239, :268; `scripts/act_ci.py:13243`, :13388; `scope.log`; `public-source/r5-workflow.log` - Actual workflow bodies retain conservative empty/gitlink behavior and reject missing revisions, ambiguous ancestry and replay conflicts. Hostile signing and Git-directory controls pass. Base-side renames and independently identical edits retain hosted/replay equality. Both published runner forms reject stack omission, URL redirection, missing stack gitlink and extra stack gitlink before fetching.

[R633] PASS Tests - `.github/workflows/docs.yml:389`; `scripts/act_ci.py:6482`; `scripts/ci_events.py:1112`; `events-selftest.log`; `resolution-probes.json`; `receipt-audit.json` - The docs step executes the ordinary complete runner self-test and the mode-0555 isolated single-file invocation with explicit worktree. The ordinary form also runs the complete isolated child, skipping only its launcher inside the child. Published execution passes 570 ordinary and 568 flat assertions. The independent contract run passes 2174 items and 3096 mutation arms, including flat-install guards. Four conflict-input deletion probes fail for their intended missing input. Scope tests pass 198 assertions and the existing 48 history mutation checks.

[R633] PASS Docs - `docs/testing/CI_WORKFLOWS.md:227`, :740, :754, :955, :1608, :1666; `docs/testing/TESTING.md:1414`; `scripts/act_ci.py:2381`; `public-source/r5-docs-final.log` - Both policy texts survive and match merged bindings, execution forms and failure behavior. Current-dev candidate builder/native banks remain mandatory. Earlier stale failure descriptions remain corrected. Source-head receipt hashes match the reviewed files. The remaining publication-status sentence is wording residue, described below.

Focused execution evidence:

| Execution or audit | Result | Receipt |
|---|---|---|
| `python3 -B scripts/ci_scope.py --selftest` | rc 0; 198 assertions, including REV, REV+E, B16 shape, rename, identical-edit, hostile-environment and refusal controls | `scope.log`, `.json`, `.rc` |
| `python3 -B scripts/ci_events.py --check` | rc 0; 2174 items | `events-check.log`, `.json`, `.rc` |
| `python3 -B scripts/ci_events.py --selftest` | rc 0; 3096 arms | `events-selftest.log`, `.json`, `.rc` |
| Four conflict-input deletion probes | Clean copy rc 0; each deletion rc 1 with its input named | `resolution-probes.json`, `resolution-*.log`, `.rc` |
| Three selector steps before/after merge | Entire step mappings identical; six real-object B16 executions pass | `b16-scope-delta.json` |
| Public receipt authentication | 27 selected entries match the publication manifest; all ten source hashes match the checkout | `publication-manifest-selected.json`, `receipt-audit.json` |
| Published runner contract step | rc 0; both complete forms and all four stack controls pass | `public-source/r5-workflow.json`, `.log` |
| Published before/after scope comparison | All 30 path/verdict rows agree, including historical B16 | `public-source/r5-scope-classifications.json` |
| Published five-image comparison | All five pre/post hashes and lengths agree with the previous round | `receipt-audit.json`, `public-source/r5-image-hashes.json`, `r4-image-hashes.json` |

The first conflict-probe driver attempt failed to alter two newline-delimited tokens. It was not credited as a mutation test. The corrected driver asserts each plant changes source before execution; all four removals are rejected. Mutations were confined to scratch copies. The three independent gate processes ran concurrently under a foreground driver; no detached job remains.

B16 was independently executed from historical head `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, merge `6c810c45ac4ac7d5b45797430753020c9ea31d86`, and its live first parent `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`. All three current selectors in hosted and replay modes return exactly `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`, with `rtl=false`. The unchanged history module and current gate execution preserve REV/REV+E's restored RTL path and `rtl=true`.

The [published execution packet](https://github.com/kebag-logic/milan-fpga/tree/ff22678d017ecc58e271c917a76cb3423f4a0498/review-evidence/734-r1/author-r5) binds its runner step and image build to this head and tree. Its boundary launcher was inspected, not executed. The runner log digest matches its receipt directly. Where publication redacted paths, the outer manifest authenticates the published bytes; original unredacted digests are not treated as hashes of redacted logs. These are author execution receipts, not manager source-bank runs or reviewer image rebuilds.

Five image SHA-256 values, equal before and after the merge:

| Shape | Bytes | SHA-256 |
|---|---:|---|
| `endstation_arty_4x4` | 50752 | `f70be6b729d203ade7fb75e832d1ca0b1d1d9ba99f03e746cc2907174ec9cce4` |
| `endstation_arty_8ch` | 50752 | `eb5dfe04250400df1a0546c4f52096cfbd4e8f0e7abc777388e6d55cf64802e6` |
| `endstation_arty_current` | 50744 | `9600824e12c1890edebeee455afe2244dc4fa9166c463fbb01591e284fe1f441` |
| `endstation_ax7101_1x1_tdm8` | 50768 | `ee7991b0b767b331d1b9fc84972b5a610ec0e9ae521ddf20689d9b4df4a9f33c` |
| `endstation_ax7101_8x8` | 50776 | `1b17baeb51ab66d3eeaeb97e5136fc8f516361ca6d99900d490a7953689e7018` |

Prior findings are explicitly reconciled at this head, retaining their original lenses:

| Prior ID and classification | Disposition | Current evidence |
|---|---|---|
| R632-1-F1; BLOCKER; all five lenses | RESOLVED | Selector steps unchanged from corrected head; current REV/REV+E pass; frozen-base mutants rejected. |
| R632-1-F2; MINOR; Docs, and R633-1-D1; RESIDUE; Docs | RESOLVED | Policy lists/counts current base-ref/head bindings at :740, :754 and :955; contract passes. |
| R633-2-F1; MAJOR; all five lenses | RESOLVED | Inline fixtures, explicit worktree and complete flat launcher unchanged; both published exact-source forms pass. |
| R632-2-F1; MINOR; Robustness, Tests | RESOLVED | Environment isolation unchanged; signing/Git-directory controls pass without altering their victim. |
| R632-2-F2; MINOR; Conformance, Docs | RESOLVED | Composed replay unchanged; current identical-edit and base-side-rename controls agree with hosted. |
| R632-3-F1; MINOR; Tests, Conformance | RESOLVED | Complete flat self-test and unrelated-sibling-import control retained; published execution and current CI-events guards pass. |
| R632-1-F3 / R632-2-S1; SUGGESTION; Tests | RESOLVED | History-call guard unchanged; published removed/discarded/zeroed-result controls pass. |
| R632-2-R1; RESIDUE; Docs | RESOLVED | Policy :289 distinguishes empty relevance, PR ancestry failure and push fallback. |
| R632-3-R1; RESIDUE; Docs | RESOLVED | TESTING.md:1414 and elaborate.yml:80 retain corrected failure wording. |
| R632-3-R2 / R633-3-R1; RESIDUE; Docs | RESOLVED | Current PR body contains exactly one `Closes #734`. |
| R633-2-D1 / R632-4-R1; RESIDUE; Docs | RETAINED in current wording | R633-5-R1 below. |
| R632-2-S2 / R632-3-S1 / R632-4-S1; SUGGESTION; Robustness | RETAINED, optional | R633-5-S1 below. |
| R632-1 criss-cross note | RESOLVED | Unique-base refusal and its mutation control remain and pass. |

**Finding R633-5-R1. Severity: RESIDUE. All attributable lenses: Docs.**

Artifact: PR #735 body, Status, sentence `The merge commit remains local; publication is pending.`; captured in `public-state/pull.json`. Authority/evidence: the same public object reports head `7c862ad980dfe829ef4d85ff8f4fb4fab451984f`, and hosted jobs execute that published head. Impact: stale publication wording only; it changes no measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule. Required outcome / exact fix: replace the sentence with `Round 5 head 7c862ad980dfe829ef4d85ff8f4fb4fab451984f is published.` Verification: read the published body against its head after the manager's edit. Carry to the residue checklist; no lens is unclean.

**Finding R633-5-S1. Severity: SUGGESTION, retained. All attributable lenses: Robustness.**

Artifact: hosted branches at `.github/workflows/rtl.yml:123`, `rtl-fast.yml:55`, `elaborate.yml:112`. Authority/evidence: the repository contract supplies a synthetic merge to hosted jobs; unchanged bodies rely on that shape without asserting the second parent equals `PR_HEAD_SHA`. Impact: an unsupported source-head checkout without the replay marker could classify only the final commit. No supported reachable instance was found; this merge does not change the assumption. Optional outcome: assert the expected second parent before the hosted diff. Verification if adopted: a source-head checkout must refuse; a valid synthetic merge and marked replay must retain their results. This remains optional and does not unclean a lens.

Reviewer-owned ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue decisions; three selector steps; ci_events.py:598; merge-resolution.diff; scope.log; b16-scope-delta.json | R633-5 | 7c862ad980dfe829ef4d85ff8f4fb4fab451984f |
| RTL | CLEAN | final-tree.json; submodule-integrity.json; rtl-fast.yml:614-630; act_ci.py:255; published image receipts | R633-5 | 7c862ad980dfe829ef4d85ff8f4fb4fab451984f |
| Robustness | CLEAN | ci_scope_history.py:18,239,268; act_ci.py:13243,13388; scope.log; published r5-workflow.log | R633-5 | 7c862ad980dfe829ef4d85ff8f4fb4fab451984f |
| Tests | CLEAN | docs.yml:389; act_ci.py:6482; events-check.log; events-selftest.log; resolution-probes.json; receipt-audit.json | R633-5 | 7c862ad980dfe829ef4d85ff8f4fb4fab451984f |
| Docs | CLEAN | CI_WORKFLOWS.md:227,740,754,955,1608,1666; TESTING.md:1414; public source receipts; public-state/pull.json | R633-5 | 7c862ad980dfe829ef4d85ff8f4fb4fab451984f |

Real limits and pending manager duties:

- Source execution consists of the focused reviewer gates/probes and authenticated author receipts. No manager source bank at this head is claimed. No full parent, processor, gPTP, synthesis or builder bank was run here; no linked images were rebuilt. The pinned simulation compiler was not invoked.
- The successful hosted snapshot at 2026-10-13 21:01 UTC is retained in `public-state/hosted.json`, including exact run/job identities. `changes`, `full-ci-gate`, lint, BDD, AECP mutations, Yosys shards 0/1/2, wire accountability and docs-without-Git succeeded. Other expensive jobs and required contexts remained incomplete. Physical gPTP was skipped. Two later refresh attempts encountered HTTP 502; neither replaces that successful snapshot or proves later completion.
- No completed exact-head replay receipt was publicly linked in the inspected issue/PR manager comments. The manager must publish and accept trusted replay receipts and all required hosted evidence, distinguishing execution from skipped contexts.
- At the merge turn, the manager builds against then-current dev and validates the candidate builder/native banks, linking receipts on the PR. Supplied live dev is `0136de16291a127e0a34627c77ac09cd41efc08b`; original source base remains `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`. This source verdict does not pre-approve a later candidate.
- Obtain the independent internal verdict, finish every review round, confirm remaining sequencing, obtain merge authorization, perform post-merge containment, and complete Issue/board workflow. Publish this report and carry R633-5-R1 to the residue checklist.
- Physical calibration NOT RUN. Field skips, desk gates and image equality are not hardware proof.

Final restoration proof: HEAD, tree, every tracked blob's raw bytes and executable/symlink mode, and all 1316 index/tree entries match exactly. The four required populated submodules match their pins, raw bytes, modes and indexes: processor `2ad2f845dd583f8310075fa2380cb60a04fd091a` (562 blobs), gPTP `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` (104), AXIS `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214), and stack `405dc68310a18f669049ffc10cc23eef7300dcff` (78). Inactive external and uninitialized lwSRP gitlinks remain exactly recorded. No source restoration was needed; the original checkout is clean.

Portable scripts, raw receipts and provenance are listed in MANIFEST.sha256. Publish only those listed files and REPORT.md. Everything under scratch/ is disposable and excluded from publication.

R633-5 FINISHED
