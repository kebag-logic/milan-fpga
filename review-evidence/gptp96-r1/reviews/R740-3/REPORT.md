[R740] NEGATIVE - exact head 411b35fcc56d11c2361d861e7205307587a04a1d

Independent delta review of issue #96 / PR #97, round R740-3. Tree `131a1ffff543977e1881e3ba5b70a2871f7a6d89`; source base `135afd043309369a87ddbc8d6550aff8ec52a157`; previous head `806957b35c3c23a36505744d205f9692720d19e2`.

Two MINOR claim errors remain: decimal minutes do not always pass, and unit inference requires a comma that the new PR description omits. The direct report links and duplicate-constant self-test are repaired. The revised publication timing is consistent with the implementation. No RTL change is requested.

Scope and independence

The supplied repository instruction was read; no applicable on-disk AGENTS.md or CONTRIBUTING.md was present. Reconstruction covered README and docs/README, the [frozen issue acceptance](https://github.com/Mister-M-alt/FPGA-gPTP/issues/96), public issue scope decisions including the [round-three ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/96#issuecomment-6521384667), [parent #797](https://github.com/kebag-logic/milan-fpga/issues/797), source-evidence and integration contracts including issues #31/#35, then the base-to-head diff, delta and history, then public author evidence. The own previous report supplied inherited coverage. No other reviewer's report or PR comments were read before this independent verdict and ledger were written.

The round-three delta is four commits, five files, +35/-8: four Markdown pages and the documentation checker. Production checker behavior is unchanged; its only executable delta adds a duplicate-constant self-test arm. The full PR changes twelve Markdown files and two documentation scripts. RTL, generator, simulation implementations, generated images, synthesis inputs and build rules are unchanged. Earlier clean coverage of those unchanged inputs is retained. `scope.txt`, `delta.diff`, `history.txt` and `integrity.json` record the boundary.

Findings

F1 — MINOR — Conformance, Robustness, Tests, Docs — decimal-minute behavior contradicts the newly documented gate limit.

Artifact: `docs/INTEGRATION.md:862-874`, especially line 872; PR body, “Freshness checks / Copies,” the sentence beginning “Decimal forms,” and its later statement that decimals pass. Cause: `scripts/check_docs.py:451-454`; contrasting symbol-number boundary at lines 446-449.

Authority: issue #96 requires that no current document contradict the code. The manager's round-three ruling requires every gate sentence to describe exactly what the checker enforces. This is the same claim-accuracy class as prior R739-2 F2, not a request for a new gate feature.

Evidence: append `Wait 0.5 minutes.` to `docs/HDL_DEVELOPER.md` in a disposable exact-head archive, then run `make -j16 docs`. It returns 2 with exactly one finding:

```text
docs/HDL_DEVELOPER.md:420: '5 min' restates CEASE_MS_C; link its constants row
```

The integer-minute pattern uses a word boundary, which also matches after a decimal point. It interprets the fractional suffix as the five-minute constant. Direct probing also rejects `1.5 min` with the same diagnostic. Neither value equals the constant. By contrast, `Wait 0.375 s.` passes the complete target. Untouched and restored archives pass. See `decimal-minute-full-gate.log/.rc`, `decimal-symbol-full-gate.log/.rc`, `claim-probes.json`, and portable `probe_claims.py`.

Impact: a documented passing form fails with a false copy finding; the claimed rejected set (“that row value”) also includes an unrelated decimal value. Published examples test decimal seconds and milliseconds, not decimal minutes, so they do not substantiate the blanket claim. This affects an executable gate contract and claimed test coverage: MINOR, not wording-only RESIDUE. It does not demonstrate an RTL or protocol defect.

Required outcome: accurately describe decimal-minute handling in the guide and PR body. The smallest permitted repair is to narrow the claim, for example: “Decimal symbol forms pass, except minute forms matching integer suffixes.” Follow with “For example, `0.5 minutes` matches the `5 min` pattern.” Keep the integer-copy description consistent with that limitation. Alternatively, correct the existing minute-number boundary and add a focused passing decimal-minute control. Do not retain the universal “decimals pass” assertion.

Verification: retain `5 min`, `five minutes`, and `five-minute` rejection controls; run `0.5 minutes`, `1.5 min`, and `0.375 s` probes and state their actual outcomes. Under a claim-only repair, the first two still fail and must be documented as such; under a boundary repair, they pass while genuine integer copies still fail. The unchanged full docs target must pass.

No BLOCKER or MAJOR is found. No additional wording-only residue or new suggestion is asserted in this independent pass. Changed source comments add only the issue reference; no workflow label is introduced.

F2 — MINOR — Conformance, Robustness, Tests, Docs — the new unit-inference claim omits a required delimiter.

Artifact: PR body, “Freshness checks / Copies”: “A row has a unit when its Meaning cell ends in ms, ns or ppm.” The adjacent guide description is `docs/INTEGRATION.md:860`; the actual matcher is `UNIT_CELL_RE` at `scripts/check_docs.py:123`, used at 465.

Authority: the same issue acceptance and manager rule cited for F1. This was investigated after the independent seal while reconciling the prior unit-inference suggestion. The original implementation suggestion remains optional; the new unconditional PR claim must be accurate.

Evidence: in the restored exact-head archive, append `A 375 ms watch.` to the HDL guide. The full docs target correctly returns 2 with `restates SYNC_RTO_MS_C`. Change only that constant's Meaning cell from `syncReceiptTimeout, ms` to `syncReceiptTimeout ms`, leaving its name, value and terminal unit unchanged. The full target now returns 0. The regex requires a comma followed by optional whitespace and the terminal unit; a terminal unit alone is insufficient. Restoring both files returns 0. `probe_unit_marker.py`, `unit-marker-probes.json`, and `unit-comma-control.*` / `unit-no-comma.*` / `unit-marker-restored.*` preserve the control, counterexample and restoration.

Impact: an editor following the stated suffix rule can unknowingly disable a constant's copy check. The PR's claimed recognition condition is broader than the implemented condition. This is a testable gate guarantee, not a purely stylistic comma preference.

Required outcome: narrow the PR body to say that the Meaning cell must end in a comma, optional whitespace, and `ms`, `ns`, or `ppm`. Make the guide equally explicit; for example: “Units require a comma before the Meaning cell's final symbol.” State the three supported symbols beside it. No new unit-inference feature is needed.

Verification: retain the comma-bearing rejecting control and the otherwise identical non-comma passing control; verify the revised text states those outcomes accurately. Keep the unchanged docs target green.

Named prior findings

| Prior item | Disposition | Cause-level verification |
|---|---|---|
| R739-2 F1, duplicate constants / self-test claim | RESOLVED on independent evidence | Checker:713-718 appends a duplicate true row and requires its named diagnostic. Muting checker:415 alone makes self-test return 1, “duplicate constant row escaped”; normal self-test passes 42 arms. PR body lists five findings without isolating arms. |
| R739-2 F2, copy-gate claims | PARTIALLY REPAIRED; claim-accuracy obligation retained as F1/F2 | Previously named decimal-seconds and spelled-unit exclusions are now stated. Decimal-minute behavior and the comma-dependent unit rule still contradict the new broader statements. |
| R740-2 F1, report-file links | RESOLVED | History:32-37 links four `.rpt` blobs at `4999d8d6344e373e0204995cb36c93cf616e8f9e`. Retrieved figures: LUTs 4,773/4,853; registers 3,646/3,652; memory LUTs 466/466; BRAM 1.5/1.5; DSPs 4/4; WNS +2.249/+1.773 ns. `report-link-check.json` records blobs and excerpts. |
| R740-2 S1, seeded ROM freshness scope | RESOLVED by narrowing | Manager:59 and PR body name `--seq-seed 0x200000`, exactly as checker:556 invokes it. No new image check is required. |
| R740-1 F1 = R739-1 F3, publication timing | RESOLVED; closure retained | Sampling statements and the new complete-tuple wording agree with staging and commit sequencing, examined below. |
| R740-1 F2 = R739-1 F4, stale constants | RESOLVED; closure retained | All 17 constants reject independent +1 drift. Formatted, negative, unit-bearing, deleted and unnamed rows produce named findings. |
| R740-1 F3 = R739-1 F5, duplicated values | RESOLVED; closure retained | Earlier literal copies remain replaced by canonical links; this delta adds no value copy. Remaining gate-contract defects are F1/F2, not a reintroduced duplicate. |
| R740-1 F4 = R739-1 F1, Follow_Up clause | RESOLVED; closure retained | Glossary:19 remains at 2011 11.4.4 / 11.4.7; no clause changed this round. |
| R739-1 F2, historical pointer | RESOLVED | The current direct report links satisfy both the earlier directory-level requirement and the later explicit `.rpt` requirement. |

Publication evidence

Integration:567 and HDL:12 agree with the shipped implementation. Engine:994-997,1013-1015 write staging fields; 1031-1053 resolve and write the path. Engine:1134-1146 continuously exposes that state, with the shown flag/path derivations, and combines the microcode/bootstrap commits. There is no second output latch.

Completeness follows sequencing: microCPU:438-442 decodes the advancing COMMIT; generator commit sites at 1072,1712,1856,1953,2022 follow the relevant transaction writes. Announce resolves path and updates parent/GM before 1856; self-publication writes GM/parent/path before 1953. Peer-delay and servo tails finish updates before committing. Engine:885-900 initializes the reset tuple; 924-925 emits its bootstrap commit before event dispatch; 933-940 asserts the path-stage invariant at commit. Outputs can remain complete between commits too, so removing “Only” is correct. This verifies shipped sequencing, not arbitrary substituted microcode.

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Frozen #96 and manager ruling; gate-limit claims F1/F2; direct report-link requirement; unchanged clauses | R740-3 delta/named findings; earlier unchanged coverage retained | 411b35fcc56d11c2361d861e7205307587a04a1d |
| RTL | CLEAN | Engine staging/assigns/reset/bootstrap/path assertion; microCPU commit decode; generator commit ordering; implementation identity | R740-3 publication; R740-2/R740-1 unchanged coverage retained | 411b35fcc56d11c2361d861e7205307587a04a1d |
| Robustness | UNCLEAN | Status/constants/copy/ROM boundaries; decimal-minute and comma-marker behavior contradict new contract (F1/F2) | R740-3 gate claims; earlier unchanged implementation coverage retained | 411b35fcc56d11c2361d861e7205307587a04a1d |
| Tests | UNCLEAN | 42-arm self-test; duplicate-rule weakening; 64 probes plus unit-marker controls; published gate coverage claims disproved (F1/F2) | R740-3 changed claims/self-test; earlier unchanged simulation evidence retained | 411b35fcc56d11c2361d861e7205307587a04a1d |
| Docs | UNCLEAN | Four changed pages, PR body, checker comments, report targets, current gate wording (F1/F2), inherited reader/status paths | R740-3 delta/named findings; R740-2/R740-1 unchanged pages retained | 411b35fcc56d11c2361d861e7205307587a04a1d |

Independent execution and public evidence

Foreground controllers ran all commands without detached jobs. Contract, lint and whitespace ran concurrently with at most three workers. Make invocations used `-j16`. Disposable archives and generator products stayed under packet `scratch/`; source was never mutated.

| Check | Result | Receipt |
|---|---|---|
| Complete docs target | rc 0: 14 current / 18 historical pages; 42 docs arms; 20 exact anchors / 7 anchor arms; 9 diagram assets / 3 bound previews / 10 diagram arms | `docs-control.log/.rc` |
| Status, 17 constant drifts, row formatting/deletion/duplicates, copy forms/exemptions, shipping/seeded ROM drift | 64 direct probes: 62 match documentation; two decimal-minute cases contradict it | `claim-probes.json` |
| Unchecked cadence changed to stale value | Full target rc 0, as documented | `cadence-outside-gate.*` |
| Decimal minute / decimal second | Full target rc 2 / rc 0 | `decimal-minute-full-gate.*`, `decimal-symbol-full-gate.*` |
| Duplicate-constant diagnostic silenced | Self-test rc 1 with named failure | `duplicate-rule-muted.*` |
| Restored archive | Full target rc 0 | `docs-restored.*` |
| Comma unit marker / terminal unit without comma / restoration | Full target rc 2 / rc 0 / rc 0 | `unit-marker-probes.json`, corresponding logs/rc files |
| Contract, lint, full-PR whitespace | rc 0 each; required lint revision checked before use | `checks.json`, logs/rc files, `lint-identity.txt` |

All 60 author-r3 files in the [public packet](https://github.com/kebag-logic/milan-fpga/tree/2f8fce3af1d658c6b558bf6b26598c5698144a6c/review-evidence/gptp96-r1) match publication-manifest SHA-256 and Git blob ID (`evidence-integrity.json`, `fetch_evidence.py`). The publication commit reports `verified: false`, `reason: unsigned`, null signature/payload; source has no signature header either. Hash integrity is verified; signer authentication is not. This is an evidence limit, not an invented acceptance failure.

Exact-head author receipts show docs, diagrams, contract, lint and whitespace rc 0, agreeing with own focused runs. Published copy probes, checker weakenings and finding-site mutants were inspected by section; selected raw receipts are in `public-author-receipts/`. The site campaign reports 18 killed / 14 surviving sites. Five survivors belong to status/constants/ROM rules and are explicitly disclaimed in the PR body. Own direct probes confirm those production diagnostics still fire. The new duplicate-row arm kills its newly covered site.

Simulation inputs did not change. Earlier public source-suite evidence and prior lens coverage remain applicable; no simulation bank, engine mutation bank or synthesis bank was rerun. Published parent-consumer comparisons report identical pin-related documentation failures at both heads and passing quality/hygiene checks; re-pinning parent gPTP references makes that check pass. These are attributed author receipts, not manager source-bank results.

Limits and pending manager duties

No manager source bank exists at this exact head and none is inferred. The manager owns final current-dev candidate validation, builder/native banks, parent reference updates, hosted/act acceptance, and publication of those receipts. Given source base: `135afd04`; given live-dev boundary: `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.

Physical calibration is NOT RUN. Field skips and software checks are not hardware proof. Historical reports establish their pinned measurements, not present-head synthesis. Full corrected-standard access retains the earlier review's limit; no standards clause changes this round. Existing publicly recorded source-header/history inconsistencies retain their prior disposition, including “latched by OP_COMMIT.”

All 113 tracked blob bytes/modes match HEAD, the index tree matches HEAD, no nested gitlinks exist, and source status is clean. No source fix, commit, push, GitHub write, hardware work, or other-checkout edit occurred. Only manifest-listed receipts and REPORT.md are publishable; scratch is excluded.

Public reconciliation after independent seal

`INDEPENDENT.md` and `independent-seal.json` preserve the original negative verdict and five-lens ledger, written before PR comment retrieval or the other reviewer's reports. Post-seal inspection covered the [previous internal delta review](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6521153811), its [first-round findings](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6520239117), and the manager's public notices. Those findings agree with the cause-level dispositions above. F2 was added after an independent reproduction prompted by that reconciliation; F1 was already sealed.

All prior wording residues are resolved: first-round PHC pulse/level, port-enable scope and dated-measurement wording remain repaired; second-round RES-1/RES-2 are the two publication sentences checked above; second-round RES-3 is addressed by the three `(#96)` comment references. First-round bytecode-cache suggestion S-3 remains resolved by `sys.dont_write_bytecode = True` in checker:394.

The remaining prior suggestions are recorded here so nothing is deferred to a separate report. They are non-blocking and do not authorize new gate features in this round.

| ID / severity / lenses | Artifact and evidence | Impact, optional outcome and verification |
|---|---|---|
| S1 — SUGGESTION — Robustness, Docs (prior R739-2 S-1) | Checker:459-489 matches numeric value without semantic context. A genuine integer figure coincident with a constant is treated as a copy. | Conservative false positives remain possible. Optionally describe value coincidence in the diagnostic; confirm existing copy failures remain failures. This unchanged behavior is distinct from F1's decimal-suffix error. |
| S2 — SUGGESTION — Robustness, Tests (prior R739-2 S-2) | Checker:123,465 takes units from the Meaning-cell comma suffix. Own full-target marker probe confirms the dependency. | Deriving or requiring units independently remains an optional feature, outside this round. If later authorized, a changed unit label must not silently disable its copy check. The current misleading claim is separately F2 and needs only a description repair. |
| S3 — SUGGESTION — Robustness, Docs (prior R739-2 S-3) | Rows without recognized units are excluded; direct controls for `248` and `1,024 words` pass. The PR now states this limit. | Review continues to enforce unitless-value single sourcing. No gate extension is required; retain current-page audits when those values change. |
| S4 — SUGGESTION — Robustness, Tests, Docs (prior R739-2 S-4 / R740-2 S1) | Manager:59 and checker:556 explicitly name the checked seeded image; the engine makefile also has a Sync-seeded image. | The claim-side suggestion is resolved. Checking both images remains optional future work; if adopted, verify both matching controls and an isolated mismatch. No present false count is found. |
| S5 — SUGGESTION — Tests (prior R739-2 S-5) | Makefile:20 selects the lint executable through PATH. The required version was placed first and its identity verified in this run. | A future override variable could make selection explicit. No build change is required here; verify identity before execution as done in `lint-identity.txt`. |

There are ten public PR comments: six review-start notices and four earlier reports. Formal reviews and inline-comment endpoints are empty. The [current review start](https://github.com/Mister-M-alt/FPGA-gPTP/pull/97#issuecomment-6521663669) binds this exact head/tree and the two-positive-review completion requirement. Manager comments on the issue and PR provide scope, assignment, readiness and review notices; none publishes a source-bank execution. `public-reconciliation.json` records the inspection.

Exact-head hosted check-runs total zero, and commit statuses total zero. There are no executed hosted jobs or skipped hosted contexts to credit from those endpoints. Hosted/act acceptance remains with the manager; it is not inferred from source gate passes.

Reproduction: run `python3 probe_claims.py <source-clone>` from the published packet, then `python3 probe_unit_marker.py`. Both use only packet scratch copies. `run_checks.py <source-clone>` runs focused checks and verifies exact source integrity. `fetch_evidence.py` re-fetches only the public author packet and pinned measurement reports. No source mutation is needed to reproduce either finding.

Final verdict: NEGATIVE for F1 and F2. RTL is CLEAN; Conformance, Robustness, Tests and Docs remain UNCLEAN for the precise gate-contract defects above. All named prior findings are resolved or explicitly retained here. The final packet manifest lists every publishable receipt; scratch is never published.

R740-3 FINISHED
