[A172] Correction handoff

Commit `b5e6c23e1b9802b5cacbc62db212064d7e429862`; tree `2fd42873a06123f87f539c116e4969c87f5e33d8`. Branch `437-container-paragraph-scopes`. Clean, local only.

Starting head was `65df1df50a80cd5f540a93d8f0cfabc97da3da75`. The disjoint dev integration is commit `3003bee2a33a6ae2f650ec7bd54fb7730d82086f`, tree `8327dfa5387e01988c567b952b3a2f9f123b7a8c`, based on dev `52711029f374650dc93830d5ea28e81cb5c8f410`. `integration-proof.json` records empty path intersection and byte-identical complete issue patch before/after integration. The correction commit has a one-line message and no trailers.

The code preserves the item paragraph when the tag remains at its content column, keeps outside tags able to open HTML, and releases item context at dedented quotes/footnotes. Public R237/R238 counterexample bytes are regression inputs. P01/P04 first-paragraph counterparts also agree through this same mechanism. Changes since the integration are limited to CONTRIBUTING.md, gen_toc.py and gen_toc_container_cases.py.

Status: corrected-but-unreviewed for the named code/test counterexamples. No reviewer-confirmed resolution, approval or clean-lens ledger is asserted. R237 and R238 must independently reassess this head.

Acceptance remains open:

- AC1 is UNPROVEN. Nine historical descriptions are reproducible, but the eleven historical IDs have no justified complete per-ID correspondence. R237 F2 remains open MAJOR Conformance/Tests/Docs. Equal counts and R238's narrower assessment do not clear it.
- AC2 retains all five explicit omissions. No setext/container headings or anchors are added.
- AC3's named corrections have observable failure controls in both consumers, including the three block-marker controls. See MUTATIONS.md and mutations.json.
- AC4: zero classification differences on each of the baseline, starting and corrected 163-page populations, using all three parsers on each identical input population. The comparison includes blocks, line kinds, headings/anchors, plans, generated navigation provenance, ownership and refusals.
- AC5's focused commands pass without any budget change. The manager-owned full native/act/hosted/current-candidate/review/merge/post-merge bars remain outstanding; none is claimed from these checks.

Additional open evidence: the unclosed-comment reproduction in additional-observation.md remains wrong at the starting and corrected heads. Six resumed variants differ from the original baseline; six first-paragraph variants are already wrong there. This is published as a manager-decision item, not silently moved into optional R238 F3 or declared resolved. The source documentation states its precise boundary. The twelve raw requests/responses and the three-revision measurements are retained in exploratory-unclosed-comments.json. Closed-comment outside-tag controls are separate fixtures, not evidence that the unclosed forms pass.

Optional R238 F3 is NOT adopted. P02/P03/F09 and two empty-item counterparts remain measured residues of item HTML termination; #495 owns the optional follow-up. New renderer requests contain synthetic pages only.

Validation at this commit:

- TOC selftest 909/909, check 105 pages, anchors 144.
- Em-dash selftest 254 arms; integrated-dev diff gate: zero findings, 16 added Markdown lines, zero exemptions.
- 155 correction rows and the original 42 probe rows agree with fresh GitHub renders. The core receipt set has 308 labeled rows / 241 unique requests, including independent public probes, boundaries and explicit limitations. It is NOT claimed wholly equivalent: the five known item-HTML residues remain, and the separate twelve unclosed-comment requests remain mismatches. The five selected omission rows are compared as omissions, not as successful heading-list equality.
- 197 real-Git and generated-navigation controls pass; 189 unique synthetic base-page renders independently confirm those label-presence expectations. Receipt files contain exact base/head bytes, commit IDs, Git diffs, generated blocks, refusal reasons and exemptions.
- 23 exact mutants (six targeted, seventeen prior public mutants) fail both selftests at named property arms. The narrow block-marker mutant fails exactly the three R237 marker arms, with TOC exit 1 and em-dash exit 2. Its real-Git rerun changes precisely those three labels from 0 findings/1 exemption to 1 mirrors-no-heading finding/0 exemptions. Thematic-break and ordinal controls do not fail under that narrow mutant.
- All 707 prior arms classify identically, including all 428 #507 closer arms. Old case/guard/closer files and check_em_dash.py are unchanged from the starting head. All 42 old I437 real-Git base fixtures remain byte-identical. Policy/provenance/refusal functions are unchanged.
- 25 focused docs/idiom/hygiene/source commands pass; logs contain exact argv, cwd, exits and source hashes. No budget file changes. The final integrity check verifies all 852 tracked parent blobs and a clean status; required submodules are at their recorded pins. This is not a fresh full submodule-byte audit or native run.

Packet entry points: RESPONSE.md (original finding identities/lenses), HISTORICAL.md (evidence gap), REVIEW-READY.md (public handoff text), PR-BODY.md (proposed body only), COMMANDS.md, MUTATIONS.md, final-integrity.json, preservation.json, public-input-preservation.json, renderer-results.json, renderer-consumers.json, consumers-corrected.json, and mutations.json.

Reproduction: `rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-correction/reproduce.py`. It requires this exact clean head and uses cached synthetic renderer responses. A missing cache requests only the corresponding synthetic fixture. At most four jobs run inside either bounded batch; this author used at most eight concurrently. The wrapper was assembled from individually executed steps; no additional full-wrapper run is claimed.

Manager A10 owns publication/push, independent R237/R238 re-review, full required validation, acceptance decisions, any follow-up Issue for the additional observation, current-candidate validation and eventual authorized merge/containment. No push, PR metadata change, external message outside the permitted GitHub comments, delegation, other-lane edits, installs, privilege, hardware, Docker/act or native exhaustive bank occurred. Work stops at the commit above.

Public factual handoff: https://github.com/kebag-logic/milan-fpga/pull/515#issuecomment-5778679836
Nine-description exact public receipt: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5778671234
