[R740] NEGATIVE - exact head 806957b35c3c23a36505744d205f9692720d19e2

Independent delta review of issue #96 / PR #97, round R740-2. Tree: `a3920c96afb9a4917515d337514de26ced4857b3`. Source base: `135afd043309369a87ddbc8d6550aff8ec52a157`. Previously reviewed head: `8607347675743fe8d1ccaa370c63905c5ca1ccd5`.

The four shared prior findings are resolved. The original historical-link defect is also repaired in the form its reviewer allowed. This round adds an explicit direct-file criterion for that named finding, which remains unmet: the link reaches the containing directory, rather than the `.rpt` files themselves. All required local gate and fault probes pass their expected outcomes. No RTL change is requested.

The independent verdict and five-lens ledger below were written before fetching PR comments, reviews or inline threads, or reading the other reviewer's report. The own round-one report was read after the independent diff pass. The public author packet was read only after that pass. Post-seal public reconciliation is included below; `INDEPENDENT.md` preserves the original assessment.

Scope and authorities

Repository `AGENTS.md` and `CONTRIBUTING.md` are absent. The supplied repository instruction was read. Reconstruction covered `README.md`, `docs/README.md`, the frozen [issue #96 acceptance](https://github.com/Mister-M-alt/FPGA-gPTP/issues/96), its [round-two manager scope](https://github.com/Mister-M-alt/FPGA-gPTP/issues/96#issuecomment-6520243918), [parent #797](https://github.com/kebag-logic/milan-fpga/issues/797) and its [sweep decision](https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6518880512), `docs/SOURCE_EVIDENCE.md`, linked interface issues #31/#35, the publication/PHC/port-enable source contracts, the full base-to-head diff and history, then the public executable evidence. The delta was read independently before the own prior report and public author resolution narrative.

There are eight commits after the prior head, ten changed files (+263/-72): eight Markdown pages and two documentation checker scripts. Across the whole PR there are twelve Markdown files and those two scripts. RTL, generator, generated images, simulation implementations, synthesis inputs and build rules are unchanged. The inherited source findings and evidence remain applicable unless affected by these documentation/checker edits. `full.diff`, `delta.diff`, `history.txt` and `integrity.json` record that scope.

Findings

F1 — MINOR — Conformance, Docs — outstanding round-two direct-file criterion attached to R739-1 F2.

Artifact: `docs/history/v1/RESOURCE_DELTAS_2026_10.md:32`.

Authority: the manager requires links to the measurement reports themselves; this review's explicit acceptance clarifies that the link must land on the `.rpt` files. The new target is `https://github.com/kebag-logic/milan-fpga/tree/4999d8d6344e373e0204995cb36c93cf616e8f9e/review-evidence/gptp75-r1/author`, a directory listing. This improves the former commit-diff link, but still does not identify the required report files as the hyperlink destinations. `archive-link-target.json` confirms the listing contains separate baseline/candidate utilization and timing reports alongside unrelated logs and narrative files.

Impact: the round-two direct-file acceptance item remains incomplete; the historical numerical evidence is discoverable but not directly linked as required. The measurements themselves are corroborated: baseline/candidate LUTs 4,773/4,853, registers 3,646/3,652, memory LUTs 466/466, and WNS +2.249/+1.773 ns. This is evidence traceability, not a purely prose preference or a wrong measurement claim.

Required outcome: use label-free direct links at the same pinned parent commit to the applicable files, for example [baseline utilization](https://github.com/kebag-logic/milan-fpga/blob/4999d8d6344e373e0204995cb36c93cf616e8f9e/review-evidence/gptp75-r1/author/baseline-engine_util.rpt), [candidate utilization](https://github.com/kebag-logic/milan-fpga/blob/4999d8d6344e373e0204995cb36c93cf616e8f9e/review-evidence/gptp75-r1/author/candidate-engine_util.rpt), [baseline timing](https://github.com/kebag-logic/milan-fpga/blob/4999d8d6344e373e0204995cb36c93cf616e8f9e/review-evidence/gptp75-r1/author/baseline-engine_timing.rpt), and [candidate timing](https://github.com/kebag-logic/milan-fpga/blob/4999d8d6344e373e0204995cb36c93cf616e8f9e/review-evidence/gptp75-r1/author/candidate-engine_timing.rpt). Preserve the historical values and commit pin.

Verification: follow each final hyperlink, confirm it opens the intended `.rpt` blob at `4999d8d6344e373e0204995cb36c93cf616e8f9e`, inspect its resource/timing summary, and rerun `make -j16 docs`. No synthesis rerun is needed for this link repair.

There are no new BLOCKER or MAJOR findings. No new wording-only residue or suggestion is asserted. One prior non-blocking suggestion is retained below after public reconciliation. No workflow/reviewer label was introduced in source comments by this delta.

Prior-finding disposition

| Prior finding | Disposition at this head | Cause-level verification |
|---|---|---|
| R740-1 F1 = R739-1 F3, publication timing | RESOLVED | `docs/INTEGRATION.md:11-16,555-567`, `docs/HDL_DEVELOPER.md:12,317-323`, README:60, glossary:36, manager:20,34 now distinguish staging from commit sampling. Engine:994-997 and 1037-1053 write fields separately; 1134-1146 expose staging and the separate pulse. PHC writes at 1060-1084 and pulse defaults at 921-922 agree with the revised summary; serializer:127-158 agrees with disabled/unstarted versus started-frame behavior. |
| R740-1 F2 = R739-1 F4, stale constants escape | RESOLVED | `scripts/check_docs.py:112-122,403-438` recognizes names independently of value syntax, validates decimal syntax and the source value, and requires all 17 names. Each row independently failed a +1 stale-value probe. Bold stale and negative values fail the complete gate with their named diagnostics. |
| R740-1 F3 = R739-1 F5, duplicated values | RESOLVED | Integration policy/timeout/capability sections and HDL/test/manager guides now use linked constants. The former 20/100 us threshold copies, receipt times, 200 ppm, tracking band, fifth-loss wording, default priority and ROM-word copies were removed. The formula at Integration:442 has correct units: ns divided by ppm gives ms. Remaining 250 ms/60 ms and 3,000 ms values are explicitly test stimuli; dated resource measurements and structural widths are distinct facts. Own 375 ms and 20 us reintroduction probes fail. |
| R740-1 F4 = R739-1 F1, Follow_Up clause | RESOLVED | Glossary:19 names both companions and cites 2011 11.4.4 and 11.4.7. Indexed primary 2011 text identifies Follow_Up/preciseOriginTimestamp at 11.4.4/11.4.4.2.1 and responseOriginTimestamp for Pdelay_Resp_Follow_Up at 11.4.7.2.1. The former 11.4.3 Sync citation is gone. |
| R739-1 F2, historical report link | Original cause RESOLVED; round-two direct-file criterion OPEN (F1) | The earlier reviewer explicitly allowed a report-directory tree URL. The head supplies exactly that. The newer round instruction requires landing on `.rpt` files; that stricter criterion remains unmet. Reports exist and their summary values match. |

The clause evidence is the indexed [IEEE Std 802.1AS-2011 primary document](https://www.ida.liu.se/~sohsa65/courses/tsn-course-2021/stds/8021AS-2011.pdf), not a later edition. Direct retrieval returns 404; the indexed text supplies the two corrected message definitions. Full corrected-standard access remains a limit, as in round one.

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Frozen #96 and manager scope; named findings; glossary clauses; canonical-value references; direct report-link requirement (F1) | R740-2 delta and prior-finding closure; R740-1 unchanged coverage retained | 806957b35c3c23a36505744d205f9692720d19e2 |
| RTL | CLEAN | Engine publication writers and assigns, commit/reset path, PHC writes/pulse defaults, port enable and serializer cancellation; implementation identity | R740-2 F1 cause recheck; R740-1 remaining implementation coverage retained | 806957b35c3c23a36505744d205f9692720d19e2 |
| Robustness | CLEAN | Constant/name/decimal/required-row logic, copy scanning, strict ROM rows and duplicates, restored controls, 17 independent stale-row probes | R740-2 | 806957b35c3c23a36505744d205f9692720d19e2 |
| Tests | CLEAN | Makefile docs/diagram/source-anchor self-tests; own full-gate negative controls; contract/lint; public author mutation script and results; inherited unchanged suites | R740-2 changed gates; R740-1 unchanged source evidence retained | 806957b35c3c23a36505744d205f9692720d19e2 |
| Docs | UNCLEAN | All eight changed pages, README/map/glossary/status routes, source evidence rename, constant references, historical evidence target (F1) | R740-2 delta and prior-finding closure; R740-1 unchanged pages retained | 806957b35c3c23a36505744d205f9692720d19e2 |

Independent execution

`run_checks.py` runs a bounded foreground controller, with at most three independent commands active, no detached shell jobs, and `make -j16`. Disposable archives and temporary generator products are only under this packet's `scratch/`. The lint executable's identity was checked as the required 5.050 revision before execution. No build bank or hardware campaign was run.

| Check | Result | Receipt |
|---|---|---|
| Exact-head `make -j16 docs` | rc 0: 14 current and 18 historical pages; 41 docs self-test arms; 20 exact source anchors and 7 anchor self-test arms; 9 diagram assets, 3 source-bound previews, 10 diagram self-test arms | `docs.log`, `docs.rc` |
| Interface contract and lint | rc 0 each | `contract.*`, `lint.*` |
| Full-PR whitespace check | rc 0 | `diff-check.*` |
| Every one of 17 constants changed by +1 independently | checker rc 1 each, diagnostic names the changed constant | `constant-*.log`, `constant-*.rc` |
| Plain stale, bold stale and negative constant | full docs target rc 2 each, named constant error | `probe-stale.*`, `probe-bold-stale.*`, `probe-negative.*` |
| Current HDL page restates 375 ms | full docs target rc 2, copy diagnostic | `probe-unit-copy.*` |
| Current integration threshold restates 20 us | full docs target rc 2, converted-copy diagnostic | `probe-converted-copy.*` |
| Broken formatted ROM row | full docs target rc 2, strict ROM-row diagnostic | `probe-broken-rom.*` |
| Duplicate otherwise valid ROM row | full docs target rc 2, duplicate-row diagnostic | `probe-duplicate-rom.*` |
| Restored exact-head archive | full docs target rc 0 | `restored-control.*` |

`checks.json` records commands, expected outcomes, diagnostic checks and all return codes. A failing negative control is not credited merely because another rule failed: the expected rule-specific diagnostic is required. The source checkout itself was never mutated.

Public source evidence

The [published packet at parent 84d4dd7](https://github.com/kebag-logic/milan-fpga/tree/84d4dd7fdfdabfe5c8ac94c697dd913eee3fb315/review-evidence/gptp96-r1) contains the current author handoff, PR body, planted-defect script and receipts. All seven author-r2 files match the publication manifest SHA-256 values; retrieved bytes also matched their Git blob identifiers. See `evidence-hash-check.json`.

Signature verification did not establish a signed packet: the publication commit API reports `verified: false`, `reason: unsigned`, and null signature/payload. The source head also has no commit signature. This is an integrity/authentication limit, not an invented acceptance failure. Hash agreement is established; signer authentication is not. See `evidence-commit.json`.

The author planted-defect receipt names this exact head and the prior checker head: 15 negative document/source controls plus a passing control, and seven checker weakenings rejected by self-tests. The script and relevant raw log were inspected, including the named-diagnostic fixes in the latest commit. The own probes above independently cover the required current-head failures.

The author handoff reports matching base/head passes for the arithmetic suite (768), parser plus mutations (378/16), engine run (2,048 in three runs plus 60), gasket plus mutations (81/5), independent decode plus mutations (288/4, explicitly no skip), and bench timestamp-tag suite. Those are attributed source execution claims in the published handoff, not own reruns or manager bank results. Underlying raw simulation logs are not among this author-r2 packet's published files. Engine mutation bank and synthesis are explicitly NOT RUN. The delta does not change their inputs; no full bank was repeated here.

Parent consumer comparison evidence reports quality/hygiene passes; gPTP/submodule documentation gates fail at both source heads while parent pins remain at the older gitlink. The author reports the gPTP docs gate passes after pin adjustment. This is an adoption requirement for the manager, not evidence that the final live-dev merge candidate has passed.

Limits and pending manager duties

- This is a delta review retaining the own round-one checks for unchanged code and documents. It does not re-certify every inherited protocol clause from complete primary standards. Direct 2011 PDF retrieval still fails; full Cor1/Cor2 and Milan-document access limits from round one remain. No later edition was substituted for the corrected clause check.
- The copy checker covers explicit recognized spellings and units; it is not a semantic parser for arbitrary prose, and the cadence literals are explicitly outside generator freshness checking. The reviewed pages and required regression controls are clean in those areas.
- No manager source bank exists or is inferred at this exact head. Source validation is distinct from the current-dev merge candidate. The manager owns the builder/native banks, parent documentation/gitlink reconciliation, hosted/act acceptance and publication of receipts at the merge turn against live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- Physical calibration is NOT RUN. Historical silicon campaigns and field skips are not new hardware proof. Parent physical acceptance, timestamp calibration and donor #58 remain outside this docs change.
- Existing engine-header publication-latch wording, generator historical loss/timeout/cease notes, literal priority default, and dated resource measurements remain the published pre-existing follow-ups. They are unchanged by this delta; no new source-comment provenance label was found. Existing provenance cleanup remains tracked by parent #746.

Reproduction and integrity

Run `python3 run_checks.py /path/to/checkout /path/to/pinned-lint-directory` and `python3 audit_integrity.py /path/to/checkout`. Use a fresh packet scratch directory for a probe rerun. `audit_integrity.py` verifies every tracked blob directly, executable modes, exact head/tree and index, and enumerates gitlinks. At review completion all 113 blobs/modes match, the index matches HEAD, status is clean, and this repository has no nested submodule gitlinks. Parent gitlink adoption is a separate manager duty.

No source fix, commit, push, GitHub write, author contact, other checkout edit, parent build, or hardware operation was performed. Publish only `REPORT.md` and the files listed by relative path in `MANIFEST.sha256`; `scratch/` is excluded.

Post-seal public reconciliation

The [other round-one report](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6520239117) was fetched only after the independent verdict and ledger had been sealed. Its F2 expressly permitted the tree URL of the author report directory. The head implements that requested repair exactly. Therefore the original wrong-artifact cause is resolved, and it would be inaccurate to say the author ignored that prior review. F1 in this report is limited to the newer task instruction, “the link must land on the .rpt files.” The negative verdict depends on that narrower, stricter current criterion, not on a claim that the directory is broken or the figures are false. If the manager preserves the earlier directory-link interpretation, this single remaining negative condition disappears; all other findings and required gate probes are clean. No permission or scope decision was requested during execution.

All other prior public findings are resolved as shown in the disposition table. Prior RES-1 and RES-2 are fixed by the exact PHC-level and port-enable summary changes at Integration:11-16. RES-3 is fixed at Manager:45-49 by describing the latest dated measurements and acknowledging later RTL. Prior S-3 is resolved by `sys.dont_write_bytecode = True` at checker:394; the complete gate leaves source status clean.

S1 — SUGGESTION — Robustness, Tests, Docs — retained prior R739-1 S-2.

Artifact: `scripts/check_docs.py:554-556`; `tb/verilator/engine/Makefile:40`; `docs/MANAGER.md:62`.

Authority/evidence: the single “Seeded regression” ROM row is checked only using `--seq-seed 0x200000`; the engine suite also builds `--sync-seq-seed 0x10000`. Independent generator spot checks confirm both currently use 1,023 real words of 1,024 (`spot-seq.log`, `spot-sync.log`, both rc 0). There is no present false count or failing acceptance.

Impact: a future change affecting only the Sync-seeded image could evade this particular budget freshness comparison. Suggested outcome: compute both seeded-image usages and ensure the shared row remains true for both, or label the row specifically for its checked image. Verification: both current seeded controls pass, and an isolated mismatch in either checked image fails with a named diagnostic. This remains non-blocking and leaves the lenses clean except for F1.

The [public review start](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6520991799) confirms the exact head/tree and two-positive-review completion requirement. PR comment inspection found six comments: four review starts and the two round-one reports. Reviews and inline-comment endpoints are empty. Issue comments contain assignment/readiness and the manager's round-two scope; none publishes a manager source bank. `public-reconciliation.json` records the public scope notices and endpoint counts. No additional prior finding or manager execution receipt was present.

The exact-head hosted check-runs endpoint reports zero runs (`check-runs.json`). Thus there are neither executed hosted jobs nor skipped hosted contexts to credit from that endpoint. Hosted/act acceptance remains pending with the manager. Author-reported independent-decode execution explicitly says no skip; it is still not treated as a local execution or hardware proof.

Final result: one open MINOR under the current direct-file instruction, so Conformance and Docs are UNCLEAN and the verdict is NEGATIVE. RTL, Robustness and Tests are CLEAN for this delta, with the stated inherited coverage and limits. The final checkout integrity check confirms 113 exact tracked blobs and modes, an unchanged index, no nested gitlinks, and clean status. All publishable receipts are listed in `MANIFEST.sha256`.

R740-2 FINISHED
