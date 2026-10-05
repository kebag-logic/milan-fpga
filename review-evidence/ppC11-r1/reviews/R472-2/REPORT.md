[R472] NEGATIVE - exact head 80588cdc43ca5605a1d3748d13dd8ed7f22f7000

Round R472-2, issue #27 / PR #156. Tree `e20b82dacbc2a3299f47c8e8444537f979d17029`; source base `c050d97153dd0480ae741102c1647eeda9b7f273`. All five lenses were applied. The original F1 and F2 are resolved as reported. Three MINOR findings remain: a composed ID notation bypasses the gate, two ID self-test omissions survive deliberate weakening, and text clips in two committed waveform renders. No RTL behavior defect was found in this lane.

**Round-1 findings graded first.** The independent verdict and ledger were frozen in `receipts/independent-pass.md` before opening either prior public review. The subsequent reconciliation uses only the [internal public findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156#issuecomment-5982079701) and [external public findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156#issuecomment-5982154411).

| Prior item | Disposition at this head | Verification |
|---|---|---|
| Both reviews F1: hyphenated braced members; prose suffix treated as a family | RESOLVED for the reported cases | `T-NVM-{RS-DEADLINE, RS-TYPO}` and `P-TX-shaped` fail. Removing either real NVM row fails at `docs/README.md:89`. Removing braced expansion fails the self-test. See `use-braced-hyphenated`, `use-prose-suffix`, `row-braced-*`, and `mutant-skip-brace-check` receipts. Expanded parsing has the new F3 below. |
| Both reviews F2: figure self-test missing claimed faults | RESOLVED | Real-tree foreignObject, missing namespace, malformed root and missing/empty inventory plants fail. The self-test rejects each of four mutants disabling foreignObject, namespace, root, or empty-inventory checks. `figure-mutant-*.log`; 17-case healthy self-test passes. |
| External RESIDUE-1 | RESOLVED exactly | F01.5 `P-MAAP-RSP-MS`, `01_overview.md:184`, no longer says “under 1,800 ms”. |
| External RESIDUE-2 | RESOLVED exactly | `tb/side_port/README.md:12` describes the held request and strobe; `KL_pp_side_port.sv:11` names the bridge mapping. Preprocessed code is unchanged. |
| External RESIDUE-3 | Historical sentence corrected; new publication-state residue R1 below | The PR now states both round-1 runs passed; fetched job records corroborate that. Its separate round-2 “no hosted run” sentence is now stale. |
| External RESIDUE-4 / internal R1 | RESOLVED exactly, counted once | `02_interfaces.md:105` says “no dual-clock FIFO”. |
| Internal S2 / external SUGGESTION-1 | RESOLVED for the named weaknesses | Eight mutants narrowing the scan, reading the whole master page, accepting duplicate/empty tables, accepting arbitrary tails, or returning success on unreadable tables all fail their own self-test: `prior-controls.log`. |
| Internal S1 / external SUGGESTION-2 | Pins and full history implemented; lockfile remains optional | Exact pinned installations succeed; resolved dependency tree and hosted logs confirm the versions. Full-history fetch is executed. No lockfile was added; the public PR lists it as open. |
| External SUGGESTION-3 | RESOLVED for named cases | Non-minus-one numeric suffix and missing line-broken member fail; feImage is rejected and planted. New missing negative controls are F4. |
| Internal S3 / external SUGGESTION-4, -5, -6 | RESOLVED | F02.9/F02.2 place host ports in the core clock with the integrator's bridge; F00.2 lists hand-authored SVG; `02_interfaces.md:630` includes withdrawal at the deadline. |
| #84 “What remains” item 3 | RESOLVED | `01_overview.md:200` records no RTL consumer for `P-EN-PLAIN-IEEE-PROFILE`. |
| Prior observation: guide `wr_done_i` / `wr_ready_i` short names | Retained as the acknowledged pre-existing, out-of-scope observation | No new claim of correcting those lines; the public PR explicitly lists them as open. |

**F3 — MINOR — Conformance, Robustness, Tests, Docs — an optional member after a line-broken ID is silently lost.**

Location: `scripts/check-ids.py:126` through its suffix checks at lines 128–135; claims at `docs/README.md:86` and `docs/architecture/09_verification.md:124`. Authority: [#70 acceptance 1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/70) and the [round-2 scope](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/27#issuecomment-5982157556): every used ID must have a master row. The gate promises both line continuation and optional segments.

In a disposable exact-head clone, replace the existing `T-ADP-` / `DELAY-START` use in `tb/adp_engine/tb_adp_top.sv:10` with:

```text
T-ADP-
//                DELAY(-STRT)
```

`T-ADP-DELAY-STRT` has no row. Nevertheless, both the checker and `make -j16 ids` return 0, with **531 files, 91 IDs, OK**. Writing the same expression as `T-ADP-DELAY(-STRT)` on one line returns checker rc 1 / make rc 2 and names the missing row. `receipts/minimal-reproductions.log` contains both executions; `scripts/reproduce_findings.py` reproduces them. The parser yields the continued base but keeps `token` and `end` at the original match when looking for its optional suffix.

Impact: wrapping a legitimate combination of the documented forms hides an undefined member, defeating the registry drift gate. Required outcome: evaluate optional suffixes on the fully continued ID, or reject an unhandled composition instead of accepting its valid prefix. Plant the combination. Verification: the broken member above fails with its full ID named; its valid `START` counterpart succeeds; existing forms and healthy `make check` remain green.

**F4 — MINOR — Tests, Docs — the ID self-test does not plant a missing ID in two forms it claims to cover.**

Location: `scripts/check-ids.py:205` (`SELFTEST_CASES`, especially the positive-only uses at 208 and 210), against `docs/architecture/09_verification.md:124`: “a stray in each of those forms”. Authority: that test claim and the Tests lens requirement that each claimed defect can make the test fail.

Two independent mutants both pass **25 cases, OK**:

| Deliberate weakening | Defect accepted in the real tree | Healthy checker |
|---|---|---|
| `resolves()` accepts every token ending in `-1`, without checking its base row | `P-R472-MISSING-1`, rc 0 | rc 1, missing F01.5 row |
| `uses()` omits the optional member only when its optional segment contains a newline | `T-ADP-DELAY(-` followed by `// MISSING)`, rc 0 | rc 1, missing `T-ADP-DELAY-MISSING` row |

Evidence: `mutant-any-minus-one*.log`, `mutant-skip-optional-linebreak*.log`, and the healthy/mutated pairs in `minimal-reproductions.log`. These are disposable mutations, not source fixes. The production scanner correctly catches both isolated forms today. Impact: regressions removing those checks pass the mandatory self-test despite its stronger published claim. Required outcome: add negative controls for a missing minus-one operand and a missing member in the broken optional form, asserting the diagnostic token and failure status. Verification: both mutants must fail their own self-test; all healthy controls pass. This is a verification claim, not wording residue.

**F5 — MINOR — Conformance, Docs — two published waveform SVGs clip text with the available browser's font rendering.**

Artifacts: `docs/diagrams/wavedrom/fig-02-txwave.svg:4` and `fig-02-memwave.svg:4`; editable sources at `02_interfaces.md:207` and `:576`. Authority: #27's valid-diagram acceptance and the documentation's editable-source/rendered-figure contract.

After opening the committed SVGs directly and waiting for fonts, the TX figure's footer extends to x=679.06 in a 600-unit viewport with `overflow="hidden"`; its heading reaches x=604.32. The final footer word is outside the visible figure. In the management figure, `host_req_valid_i` starts at x=-10.20 and its first letter is clipped. The RX figure has no text overflow. Screenshots were inspected; `receipts/waveform-measurements.log` records the text, bounds and computed font. `scripts/measure_waveforms.mjs` reproduces the measurements and optionally captures images under scratch. The extent depends on font substitution; these are measured rendering failures, not claims that every browser clips identically.

Impact: the published contract loses caption text and part of a port label even though freshness and syntax gates pass. Required outcome: regenerate from sources with sufficient label/caption room, using shorter captions, appropriate layout spacing, or a reliable font arrangement. Verification: inspect the regenerated TX and management figures in both available renderers and confirm that all text fits the viewport; keep the freshness gate green. This changes figures, so it is not RESIDUE.

**R1 — RESIDUE — Docs — round-2 hosted-status wording in the public PR body.**

Artifact: PR #156, Validation paragraph “The round-2 head was not pushed, so it has no hosted run.” This was true before publication and is now stale. Exact fix as of the observed job snapshot: “At `80588cdc`, push run 37262072707 and pull-request run 37262073270 have successful docs-gates and portability jobs; suites is still in progress.” The manager should update that last clause when it concludes. Evidence: `hosted-jobs-*.json` and the executed docs logs. This is publication-status wording only; no code, test, figure, measurement or conformance verdict changes. Verification: compare the revised sentence to the exact-head job records. It does not affect lens cleanliness.

**Scope and acceptance.** The processor has no tracked `AGENTS.md` or `CONTRIBUTING.md`; the supplied review instructions and repository documentation governed this checkout. Reconstruction read the absent local rule locations, docs/README, frozen issue bodies and manager scope, interface/master-table authorities, the base-to-head diff and history, then public evidence. The parent's public AGENTS §6/§7 and CONTRIBUTING review/merge rules at `e6172750` were subsequently cross-checked; they agree with the five-lens and exact-head completion rules used here. No private author files, management checkout, scratchpad, current-round external report, or other checkout was read. Prior public findings were opened only after the independent freeze.

| Acceptance / constraint | Result and artifact evidence |
|---|---|
| #27 current byte-wide ports; RX has no backpressure | Met. `02_interfaces.md:136`, F02.3/F02.4, top ports at `protocol_processor_top.sv:286`; 151 explicit architecture port names are declared in HDL. RX complete/FCS-good ownership is explicit. F3/F4 do not change RTL behavior. |
| #27 historical material discoverable | Met. History prose/table and both old waveform sources are verbatim from `c050d971`; links from root README, docs/README and 02 remain. `authority-checks.log`. |
| #27 links/diagrams | Links, syntax and generated freshness pass; waveform timing matches RTL. Rendering issue F5 remains. |
| #70 ID gate | Original defects repaired; F3 remains. Real missing-row probes catch both braced NVM members, the real line-broken ADP ID, inline/broken optional ADP suffix, optional base, and both `-1` uses in `hdl/common/pp_pkg.sv:72`. |
| #70 rows, removed copied values, documentation, CI | Met except the stronger self-test claim in F4. MAAP defaults match `KL_acmp_talker.sv:140/:180`; values are absent from 02's consumers. The dynamic-mapping stray already had no base use. docs/README §2 and 09 §8 explicitly leave value scanning unimplemented. |
| #71 acceptance 1 and 3 | Met: integrator §3 at `integrator.md:135`, REQ-REU-003 at `00_MILAN_COMPLIANCE_REVIEW.md:531`. C11 itself leaves rule 5 unchanged; the merged #157 rule now states synchronous active-low reset. |
| #75 all four acceptance items | Met. CI executes `make check`; hand-authored SVG is listed and gated; five PNGs are absent; 09 §7 lists the actual nine prerequisites. Figure self-test F2 is resolved. |
| Docs/scripts/CI-only lane behavior | Met. C11 changes four HDL/test source files only in comments; their base/head preprocessing matches byte-for-byte. All other merged HDL/test blobs equal main `ead80360`. `comment-scope.log`. |

**Merge and scan provenance.** All three main merges (`07b1469d`, `b0a74196`, `ead80360`) and their three C11 integration commits (`5b2199b`, `e219709`, `80588cdc`) have two parents. Recomputing each tree with a clean, non-checkout merge-tree operation returns rc 0, no conflicts, and its exact published tree. No branch merge or commit was performed. `tree-and-merges.log` gives all parent and tree IDs. The scan remains **91 IDs**, with **47 P rows / 36 T rows**. Its files increase **488 → 531**, exactly **39 #154 additions + four #157 additions + zero #155 additions**; premerge C11 has the same 488-file set as round 1. The receipt lists every added path and verifies equality with the merged main additions.

**Executed evidence at this head.**

| Receipt | Result |
|---|---|
| `make-check.log` | rc 0: 41 Mermaid / 18 WaveDrom; 18 fresh renders; 1,168 links; 115 REQ / 17 GAP; 94 module rows / zero untested; parameters 28/28/28; ID self-test 25 and 531 files/91 IDs; figure self-test 17 and 3/18/5 classes; staleness passed. |
| `gate-probes.json`, individual logs/rc files | 42 initial probes: 37 expected results, five unexpected results comprising F3 and the two F4 mutant/self-test pairs. The overall orchestrator rc 0 means observations completed; it does not mean every expectation passed. |
| `minimal-reproductions.log` | F3 reproduced in an existing file and through `make ids`; both F4 mutants reproduced against healthy controls. |
| `prior-controls.log` | Eight additional prior-review hardening mutants all rejected by their self-tests. |
| `side_port.log`, `tx_arbiter.log`, `rx_validator.log` | rc 0 each; 368/368, 66/66, 555/555. Ran concurrently in scratch with the scoped 5.050 simulator identity verified first; nested builds bounded to four workers each. |
| `comment-scope.log`, `authority-checks.log` | Four comment-only preprocessing equalities; merged executable provenance; port names, historical text, reset-lane ownership, no-consumer note and PNG removal checked. |
| `npm-pinned-install.log`, `npm-resolved.txt`, `wavedrom-install.log` | Real versions installed locally: CLI 11.16.0, mermaid 11.17.2, puppeteer 25.12.0, wavedrom 2.0.3.post3. The CLI resolves the pinned mermaid/puppeteer directly. No shared installation. |
| `hosted-docs-push.log`, `hosted-docs-pr.log`, `hosted-jobs-*.json` | Both docs jobs executed successfully, including full-history fetch, installs, rendering and both self-tests. Both portability jobs succeeded. Suites remains in progress in the captured metadata; no pending or skipped context is counted as a pass. |
| `hosted-pr-merge-commit.json` | PR run checkout `544554ef9e2e75b558ff669df0fe9f611698fbfc` combines this head with `ead80360` and has exactly the reviewed tree. Push run uses the exact head. |
| `final-integrity.log`, `probe-tree-restored.log` | All **556 tracked blob bytes and modes**, HEAD and index tree match the exact head; clean status in both source and probe clones. This processor repository has **zero gitlinks** and no submodule checkout to restore. |

Two reviewer-environment diagnostics are retained separately: the first docs attempt omitted the existing runtime directory from PATH, and the first port-name inventory counted wildcard suffix fragments as complete names. Neither was a repository defect. Corrected reviewer invocations pass, and their final scripts state the adjustment. Disposable images, dependencies and builds remain under scratch and are excluded from publication.

**Reviewer-owned ledger.**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F3, F5 | #27/#70/#71/#75 frozen acceptance; F01.5/F08.1; 02 byte/host/device tables and rendered figures; real-tree missing-ID controls | R472-2 | 80588cdc43ca5605a1d3748d13dd8ed7f22f7000 |
| RTL | CLEAN | top ports 286–295, 566–589 and TX shim 4550–4635; side-port FSM 128–219 against F02.7; NVM device-face 157–177 against 02 §8; four preprocessing equalities; main-lane blob/merge equality; three interface suites | R472-2 | 80588cdc43ca5605a1d3748d13dd8ed7f22f7000 |
| Robustness | UNCLEAN — F3 | ID continued/suffixed forms, missing rows and malformed lists; figure XML/inventory/embedded-image faults; reconstructed merge trees and exact scan inventory | R472-2 | 80588cdc43ca5605a1d3748d13dd8ed7f22f7000 |
| Tests | UNCLEAN — F3, F4 | both gate self-tests, 42 probes and eight prior-control mutants; minimal healthy/mutated pairs; focused suites; local and hosted docs executions | R472-2 | 80588cdc43ca5605a1d3748d13dd8ed7f22f7000 |
| Docs | UNCLEAN — F3, F4, F5 | changed architecture/guide/history/registry/figure text, 09 §7 claims, generated SVG inspection, PR wording, public evidence manifest | R472-2 | 80588cdc43ca5605a1d3748d13dd8ed7f22f7000 |

**Evidence limits and pending manager duties.** No full parent, processor, gPTP, portability or builder bank, synthesis implementation, local hosted-job replication, hardware operation, source fix, commit, push, GitHub write, author contact, or delegation was performed. Focused executable checks and provenance do not independently re-prove the merged lanes' full banks or their resource measurements.

The review instructions report successful manager source static/builder and native banks at this head. I keep that attribution separate from reviewer execution. The supplied [public packet snapshot](https://github.com/kebag-logic/milan-fpga/tree/4a3ae4a1a4bf5a2fcd85b6d0aeff441f3f853a9f/review-evidence/ppC11-r1) contains a manifest, author handoff/body and four adoption patches; it contains no manager raw bank receipts. The refreshed public issue/PR manager comments contain scope and review-start statements, not those bank receipts. The four published patches were downloaded and verified against their manifest hashes (`adoption-patches-verified.json`). No claim here substitutes the author's parent run at `fea346e7` for the manager's live-dev validation.

The manager must provide/link the source-bank receipts, return F3–F5 for correction and obtain reviews of the corrected exact head; carry R1 and the acknowledged optional lockfile/guide observations; finish hosted/act acceptance, distinguishing executed jobs from skipped contexts; and construct and validate the final current-dev candidate at the merge turn using source base `c050d97153dd0480ae741102c1647eeda9b7f273`, live dev `e617275074e370cec342af99b929e2588fc8d43f`, the four adoption patches and the approved processor pin. Source validation does not validate that final candidate. Public live-dev gitlinks were recorded in `live-parent-gitlinks.json` without modifying or building that checkout. Two independent positive reviews and clean exact-head lens coverage remain required before merge and issue closure; #71 closure must account for both lanes.

Physical calibration **NOT RUN**. Field skips and software simulation are not hardware proof. Only this report and files listed in `MANIFEST.sha256` are publishable; scratch is excluded.

R472-2 FINISHED
