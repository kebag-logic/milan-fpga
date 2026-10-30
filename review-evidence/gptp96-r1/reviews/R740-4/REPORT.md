[R740] NEGATIVE - exact head db9ab2215ba18aec4c1828090b3611b001dbf2b8

Two MINOR findings remain: a new fence-parsing regression lets visible copied values pass the documentation gate, and an independently reproduced public finding shows another escape through underscore emphasis. Normal source gates pass. The named round-3 defects are resolved. Wording residue and remaining suggestions are included below.

Tree: `df0a399476813ccfda8d3bb03fa9d7a272b5fd0c`. Delta base: `411b35fcc56d11c2361d861e7205307587a04a1d`. Full PR base: `135afd04`. Review start: [public assignment](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6523023825).

**Scope and independence.** Repository/ancestor instruction and contribution-file discovery found no additional checked-in files of those names. The supplied instruction file was read, followed by the documentation map, start-here guide, frozen [issue #96](https://github.com/Mister-M-alt/FPGA-gPTP/issues/96), parent [#797](https://github.com/kebag-logic/milan-fpga/issues/797), manager's [round-4 ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/96#issuecomment-6521925963), linked interface authorities, source and history. The delta contains three Markdown pages and `scripts/check_docs.py`. The full-PR diff and history were inspected for context; unchanged implementation retains prior coverage.

Before the independent verdict, PR access used only the two permitted metadata commands. No other review report or PR comment was read. [INDEPENDENT-VERDICT.md](INDEPENDENT-VERDICT.md), with all five lens verdicts, was written at 12:44:00 UTC; PR comments were fetched at 12:44:15 UTC. [The independence record](receipts/independence-record.json) preserves the digest and timestamps. F1 and R1 were already recorded; F2 and R2 were added after reconciliation. No private author material, other checkout, management source bank or private review scratchpad was accessed.

**The manager's four checks.**

| Check | Result and evidence |
|---|---|
| Remove matching-rule prose from pages and PR body | The changed pages have the requested linked pointer; no accepted/rejected-form descriptions remain there. The PR still enumerates five rejected forms: residue R1. R2 records a wording clarification of the pointer's scope. |
| Cover decimal minutes, comma-less units and the rejected-set examples | Resolved. Checker:756-786 adds 11 arms: two decimal-minute forms, larger number word, minimum-prefix control, tilde fence, unspaced minutes, number-word/min form, mixed-marker fence and three unit-cell variants. All 53 self-tests pass. Own full-gate probes agree. These cases need no expected-failure designation. |
| Preserve rejection of real stale/copy plants | Ordinary stale table value, stale duplicate row and unit-bearing prose copy all fail. F1 nevertheless lets actual copies and an incorrect numeric statement through after valid fenced examples. F2 retains another publicly named copy escape. |
| Keep docs and CI-hygiene gates passing | Source docs, diagrams, source evidence, contract, pinned lint and both diff checks pass. Author parent hygiene receipts pass; parent documentation pins still require integration updates. No manager source bank is claimed. |

**R740-4-F1 — MINOR — Conformance, Robustness, Tests, Docs.**

Artifact: `scripts/check_docs.py:479-486`, introduced by `c6bca77`. Independently found; also retains public R739-4 F1.

Authority: issue #96's single-source value rule and manager check (3). The ruling excludes real-copy escapes from wording residue. Under [CommonMark §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks), a closing fence must have sufficient marker length and cannot carry arbitrary trailing text.

The checker stores only three marker characters. A shorter same-character line inside a longer fenced block closes its state early; the real closing fence reopens it. Visible prose after the actual fence is skipped. Append this to Current page `docs/HDL_DEVELOPER.md` in a disposable source archive:

``````text
~~~~text
~~~
~~~~

The Sync receipt timeout is 125 ms.
``````

The final sentence renders as a normal paragraph, recorded in [fence-case.html](receipts/fence-case.html). It is false: generator:526-527 and integration guide:869-870 specify Sync timeout 375 ms and Follow_Up timeout 125 ms. This is a planted incorrect statement, not a claim that the submitted documentation contains it.

| Full `make -j16 docs` probe | Previous head | Reviewed head |
|---|---:|---:|
| Unmodified tree | 0 | 0 |
| Incorrect sentence as plain prose | 2 | 2 |
| Ordinary four-tilde block followed by sentence | 2 | 2 |
| Four-tilde block containing three tildes, then sentence | 2 | **0** |
| Three-tilde block containing `~~~example`, then sentence | 2 | **0** |

The longer-fence construction also hides `The Sync watch is 375 ms.`, a matching-value restatement. The failure therefore affects the copy guard independently of the sentence's semantics. Shorter-marker and trailing-text cases share one cause. The pre-existing backtick version identified publicly belongs to the same parser defect; only the tilde regression is claimed as introduced by this delta.

Impact: valid Markdown examples can disable copy checking for subsequent visible prose. The complete docs target, including self-tests, returns success. This is executable protection failing on a real copy, not wording residue. No tracked page presently uses the triggering construction.

Required outcome: preserve opening marker kind and length, and close only on a valid matching closing fence. Add shorter-inner-marker and trailing-text cases, with after-fence copy controls. If the manager accepts deferral under the ruling, record explicit expected-failure cases in the executable specification; the escape remains retained pending that disposition.

Verification: [fence_regression.py](fence_regression.py), [fence-regression.json](receipts/fence-regression.json), `fence-*` logs/return codes, [reconcile_probes.py](reconcile_probes.py) and [reconciliation-probes.json](receipts/reconciliation-probes.json). A fix must reject after-fence copies while retaining legitimate fenced-code controls and existing arms. No source repair was applied.

**R740-4-F2 — MINOR — Conformance, Robustness, Tests, Docs.**

Artifact: `scripts/check_docs.py:446-457`, especially unit-ending boundaries and the word-form lookbehind. Retained from [public R739-4 F2](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6523035037), after the independent verdict and separate reproduction.

Authority: the same single-source rule and real-copy exception. [CommonMark emphasis](https://spec.commonmark.org/0.31.2/#emphasis-and-strong-emphasis) permits underscores. The regex treats underscore as a word character, so boundaries fail around emphasized values.

Evidence: each following addition to the Current HDL guide produces full docs-target rc 0 at both heads:

- `The Sync receipt timeout is _125 ms_.`
- `A _5 minutes_ countdown.`
- `A _five minutes_ countdown.`

The asterisk control, `The Sync receipt timeout is *125 ms*.`, fails with rc 2 at both heads. The first plant contradicts the actual Sync constant; the other two copy the cease constant. [Raw results](receipts/reconciliation-probes.json) and `reconcile-*` logs preserve all controls.

Impact: commonplace emphasis lets a visible numeric copy pass. This predates the delta, but is a named public finding within this PR and remains unresolved. It is retained rather than presented as a new round-4 regression. No such emphasis copy was found in the submitted pages.

Required outcome: recognize emphasis delimiters without matching fractional suffixes or larger words. Add isolated underscore controls for unit, digit-minute and word-minute forms. Any manager-approved expected-failure disposition must be executable and explicit.

Verification: run [reconcile_probes.py](reconcile_probes.py) after [fence_regression.py](fence_regression.py). After a fix, all three plants must reject while unrelated-number and ordinary markup controls remain valid. No repair was implemented here.

**Wording residue.** Neither item independently makes a lens unclean.

| ID / severity / all lenses | Artifact, authority and evidence | Impact and exact outcome | Verification |
|---|---|---|---|
| R740-4-R1 / RESIDUE / Conformance, Docs | [Saved PR body](receipts/pr-body.txt):55-62 lists five production findings, including missing rows and non-decimal ROM counts, and says the gate reports all five. The ruling covers PR matching-rule prose. | Rejected forms are still described outside the executable specification. Delete that five-item enumeration and explanatory paragraph. Retain the single checker/self-test pointer and make its `selftest()` reference a working source link. | Inspect the refreshed body for absence of the enumeration and presence of the linked pointer. |
| R740-4-R2 / RESIDUE / Docs | Integration:856, Manager:59, documentation map:48 and PR pointer; public R739-4 RES-1. Makefile:28-36 also runs diagram and source-evidence checks. | Table context makes this wording-only. Exact wording: “The `make docs` rules for this table are `scripts/check_docs.py`; its [`selftest()`](https://github.com/Mister-M-alt/FPGA-gPTP/blob/db9ab2215ba18aec4c1828090b3611b001dbf2b8/scripts/check_docs.py#L588) cases are the specification.” Use “these tables” in the PR with a working link. | Inspect four pointers; run docs; retain one pointer sentence per location. |

**Prior public findings.** Reports were read by section after the independent verdict. Items are grouped only when they share a cause.

| Named prior item | Disposition at this head | Cause-level evidence |
|---|---|---|
| R740-3 F1; R739-3 F2 decimal-minute portion | RESOLVED | Negative lookbehind at checker:456; explicit `2.5 min` and `0.5 minutes` arms. Own full-target probes pass; author receipts also cover `1.5 min` and `7.5 minutes`. Integer controls reject. |
| R740-3 F2; R739-3 F1 unit-source portion | RESOLVED | Matcher:123 accepts comma, whitespace and parentheses. Three self-test arms and own no-comma current-page copy produce named rejections. |
| R739-3 F1 minute rejected-set portion | RESOLVED | `5min` and `five min` have explicit rejection arms and fail own full-target probes. |
| R739-3 F2 simple tilde fence | RESOLVED as stated; new regression retained as F1 | Simple fenced copy passes as code. Mixed-marker after-fence copy rejects. Insufficient-length/trailing-text escapes are the distinct new regression. |
| R739-3 S-1 larger words / minimum prefix | RESOLVED | New `twenty-five minutes` and `5 minimum` arms pass. Own larger-word control and published cases agree. |
| R739-2 F1 duplicate-row self-test gap | RESOLVED; closure retained | Checker:713-718 appends a duplicate true row and requires its named finding. Self-tests and published finding-site controls preserve coverage. |
| R739-2 F2 overly broad copy claims | RESOLVED as a claim defect | Matching prose removed; round-3 cases have arms. Actual escapes are separately F1/F2; PR residue is R1. |
| R740-2 F1; R739-1 F2 historical pointer | RESOLVED; closure retained | History:32-37 links four `.rpt` blobs at `4999d8d6`. Own previous review verified figures and targets. Neither changed in this delta. |
| R740-1 F1 = R739-1 F3 publication timing | RESOLVED; closure retained | Guides state sampling and staging behavior. Engine:1134-1146 exposes staged state. Commit/reset ordering is unchanged from the reviewed prior head. |
| R740-1 F2 = R739-1 F4 stale/formatted rows | RESOLVED; closure retained | Rows identified by name and checked against generator. Formatting/missing/duplicate cases remain self-tested. Own stale and stale duplicate table plants fail. |
| R740-1 F3 = R739-1 F5 duplicated values | RESOLVED for submitted pages | Earlier literal copies remain canonical links; no numeric copy was added to a submitted page. Gate escapes do not assert otherwise. |
| R740-1 F4 = R739-1 F1 Follow_Up clause | RESOLVED; closure retained | Glossary:19 retains IEEE 802.1AS-2011 11.4.4 and 11.4.7. No clause changed. |
| R739-1 RES-1/2/3; R739-2 RES-1/2/3 | RESOLVED; closure retained | PHC pulse/level, port-enable scope, dated synthesis, complete tuple, staging wording and checker issue references remain repaired. No new workflow label in changed source comments. |
| R739-1 S-3 bytecode-cache side effect | RESOLVED | Generator import disables bytecode output; final status including ignored files is empty. |
| R739-4 F1 / F2 / RES-1 | RETAINED as F1 / F2 / R2 | Independently reproduced fence and underscore cases; R1 is additional independently recorded PR residue. |

Prior public anchors: [round 1 external](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6520003465), [round 1 internal](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6520239117), [round 2 internal](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6521153811), [round 2 external](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6521377152), [round 3 internal](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6521923722), [round 3 external](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6521925305). Manager round-2/3 issue decisions were reconciled with these dispositions after the independent pass.

**Remaining suggestions.** Nonblocking; they do not authorize extra work beyond the ruling.

| ID / severity / all lenses | Artifact and authority/evidence | Impact, optional outcome and verification |
|---|---|---|
| S1 / SUGGESTION / Robustness, Docs | Checker:459-494; R739-2 S-1, R740-3 S1, R739-3 S-2, R739-4 S-4. Value matching lacks semantic context. | Unrelated coincident measurements can be reported as copies. Optionally acknowledge coincidence in the diagnostic; retain real-copy rejections. |
| S2 / SUGGESTION / Robustness, Tests, Docs | Checker:441-473 and self-tests; R739-2 S-3, R740-3 S3, R739-4 S-1. Unitless values, decimal seconds and spelled-unit forms remain outside represented copy cases. | Optionally retain inherited limits as explicit known-escape/pass cases in the executable specification; verify these together with rejection controls. No submitted-page copy is asserted. |
| S3 / SUGGESTION / Robustness, Tests, Docs | Manager:57, checker:559-560, engine Makefile; R739-1 S-2, R739-2 S-4, R740-2 S1, R740-3 S4. | Naming the selected seeded image resolves the claim concern. Checking the additional Sync-seeded image remains optional; verify both correct counts and an isolated mismatch if added. |
| S4 / SUGGESTION / Tests | Makefile:20; R739-2 S-5, R740-3 S5, R739-3 S-3, R739-4 S-5. | Lint selection depends on PATH. An explicit override could help reproducibility; verify identity before use, as done here. |
| S5 / SUGGESTION / Docs | History:30 and candidate timing link; R739-3 S-4, R739-4 S-6. | Optional wording: “WNS moves from +2.249 ns to +1.773 ns; timing remains met.” Verify against the linked dated report; do not imply a current-head measurement. |
| S6 / SUGGESTION / Tests | Checker:787; R739-4 S-2 and delta show `usage ={`. | Restore the space to `usage = {` when touching the code. No behavior changes; existing self-test suffices. |
| S7 / SUGGESTION / Robustness, Tests | Checker:164-174 and :477-486; R739-4 S-3. | A shared valid-fence parser could prevent caller divergence. If adopted, exercise both callers with code/prose, marker-length and trailing-text controls. Optional factoring is separate from F1's required behavior. |

Prior unit-label suggestion R739-2 S-2 / R740-3 S2 is resolved for every named variant by the new matcher and arms. A separate unit schema is optional. The PR's pre-existing source-header/history observations and dated synthesis qualification retain earlier scope dispositions; no RTL/source-comment cleanup is added here.

**Reviewer-owned ledger.** Conformance includes issue acceptance and required gate protection; no new IEEE/Milan clause error is asserted. Docs is unclean for copy protection, not because unmodified pages contain the planted timeout statements.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Frozen #96/#797, manager decisions, four requested checks, constants/source agreement, unchanged clauses | R740-4 delta/named findings; earlier clause coverage retained | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| RTL | CLEAN | No hdl/ or simulation/build-input delta; staging/publication assigns; unchanged commit sequencing; source-anchor, contract, lint gates | R740-4 dependency checks; R740-3 publication and earlier unchanged coverage | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Robustness | UNCLEAN (F1, F2) | Unit/numeric boundaries, fence state, stale/duplicate/copy controls, fence and emphasis probes | R740-4 | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Tests | UNCLEAN (F1, F2) | 53 checker arms, source/diagram arms, published 9 mutants/25 probes, own two-head full-target reproductions | R740-4; unchanged simulation coverage retained | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Docs | UNCLEAN (F1, F2); R1/R2 nonblocking | Three changed pages, current-page gate references, PR body, table/status map and actual-page fault plants | R740-4 delta/named findings; earlier unchanged-page coverage retained | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |

**Execution and evidence.** Awaited foreground controllers used at most four local-check workers and eight read-only fetch workers. Make used `-j16`. No heavy build or full bank ran. All disposable archives, products and temporary files stayed under packet `scratch/`.

| Independent exact-head check | Result | Receipt |
|---|---|---|
| Complete docs | rc 0; 14 current / 18 historical pages; 53 checker arms | `receipts/docs.log`, `.rc` |
| Diagrams within docs | 9 pinned assets, 3 bound PNGs, 10 arms pass | `receipts/docs.log` |
| Source evidence within docs | 20 exact anchors, no findings, 7 arms pass | `receipts/docs.log` |
| Contract; pinned lint | rc 0 each; required 5.050 identity checked first | `receipts/contract.*`, `lint.*`, `lint-identity.*` |
| Whitespace from source base and prior head | rc 0 each | `receipts/diff-check-base.*`, `diff-check-previous.*` |
| Stale row; stale duplicate; ordinary copy | rc 2 each with named diagnostics | `receipts/probe-stale-*`, `probe-restated-unit-value.*` |
| Round-3 controls and restored archive | Expected outcomes; restoration rc 0 | `receipts/checks.json`, `probe-*` |
| Two-head fence/emphasis cases | F1/F2 escapes and rejecting controls as above | `receipts/fence-regression.json`, `reconciliation-probes.json` |

All 60 author-r4 receipts match SHA-256 entries at [the pinned evidence publication](https://github.com/kebag-logic/milan-fpga/tree/b71327c650cd5a941ebbb73e64695650a21861cb/review-evidence/gptp96-r1). [public-digests.json](receipts/public-digests.json) records every comparison; selected raw logs are in `public-receipts/`. Exact-head author identity/gate logs agree with independent results. Published nine reverted changes kill their self-tests; published 25 tree probes have no unexpected outcome. Those campaigns omit F1/F2's forms.

Both source and publication commit APIs report `verified: false`, `reason: unsigned`, with null signature/payload. Content integrity is verified; signer authentication is not. This is an evidence limit, not an invented acceptance failure. See [public-commit.json](receipts/public-commit.json) and [hosted-and-signature.json](receipts/hosted-and-signature.json).

Author parent-consumer receipts show unchanged quality/hygiene passes and identical parent docs failures from stale donor pins. Re-pinning makes the documented parent gPTP check pass. These are author receipts, not manager validation. Exact-head hosted endpoints contain zero check runs and zero commit statuses; no executed or skipped hosted contexts can be credited from them.

**Limits and pending manager duties.** No manager source bank exists at this head and none is inferred. The manager owns final current-dev candidate validation, builder/native banks, parent gitlink/documentation pins, hosted/act acceptance and publication of receipts. Source base `135afd04` and supplied live-dev boundary `1e80128f0a467b58bf884b7d9bf62e013a2fb141` are distinct.

Physical calibration: NOT RUN. Field skips and software checks are not hardware proof. No full simulation, engine mutation, synthesis or hardware bank was repeated; inputs are unchanged. Dated reports establish their pinned historical measurements only. Full corrected-standard access retains the earlier review's limitation; no protocol clause or value changes in this delta.

The final audit verifies all 113 tracked blobs/modes, exact index-to-HEAD equality and empty status including ignored files. No nested submodules or required gitlinks exist. [final-integrity.json](receipts/final-integrity.json) records this. No source fix, commit, push, GitHub write, shared install or other-checkout edit occurred.

Reproduce with `review_checks.py <source-clone>`, `fence_regression.py <source-clone>`, then `reconcile_probes.py`. `fetch_evidence.py` verifies only pinned public author receipts. All use packet scratch; source files remain untouched. `MANIFEST.sha256` lists every publishable receipt and script with relative paths. Scratch and unlisted staging metadata are excluded.

R740-4 FINISHED
