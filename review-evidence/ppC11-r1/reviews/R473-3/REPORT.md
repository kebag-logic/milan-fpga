[R473] POSITIVE - exact head 5123548eb4de35f24d43eb088c12dab70b06d01d

Round R473-3, external independent review of issue #27 / PR #156. Tree `33b4fe59951370299cad36ec1415ead003524d5f`; source base `c050d97153dd0480ae741102c1647eeda9b7f273`. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains. R472-2 F3, F4 and F5, R473-2 F3, and the hosted-status residue are resolved at this exact head.

The review began from the [public marker](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156#issuecomment-5990583484). I checked the supplied instructions and repository/ancestor instruction locations first; this processor checkout has no AGENTS.md or CONTRIBUTING.md. I then read docs/README and the root README; reconstructed the frozen issue bodies and manager scope; examined their linked registry, compliance and interface authorities; examined the requested base-to-head diff and history; and inspected public executable evidence. The public parent review/merge rules at `fa450d30` were subsequently cross-checked. No private author material, management checkout, lane scratchpad or other reviewer's current-round report was read.

The independent verdict and five-lens ledger were written before opening prior public findings: [independent record](receipts/independent-verdict.md). Reconciliation then used the four earlier public findings comments, retained in [prior-public-findings.json](receipts/prior-public-findings.json). The formal-review and inline-comment lists contain no additional prior findings.

The [frozen scope](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/27#issuecomment-5980174687) covers #27, #70, #75, and #71 acceptance 1 and 3. The [round-3 requirements](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/27#issuecomment-5988273127) govern the four repairs below. #71 acceptance 2 arrived through merged PR #157, as recorded publicly on #71. The round-3 commit changes seven documentation, script and SVG files directly on `80588cdc`; it changes no HDL or testbench file.

**Round-2 findings, graded at this head**

- **R472-2 F3 — MINOR — Conformance, Robustness, Tests, Docs — RESOLVED.** Artifact: `scripts/check-ids.py:117`, suffix evaluation at `:136`, and `docs/architecture/09_verification.md:124`. Authority: #70 acceptance 1 and the round-3 scope. The prior impact was silently accepting an undefined optional member after an ID continuation. Required outcome: evaluate the suffix on the completed ID or reject it. The loop now advances both the token and its end position before suffix processing. Independent `T-ADP-` / `DELAY(-STRT)` and double-break probes fail with `T-ADP-DELAY-STRT`; `START` counterparts pass. The complete `make -j16 ids` target returns 2 for the missing member and 0 for the valid composition. The previous parser with the new tests fails cases 9 and 10. Evidence: [ID probes](receipts/id-probes.json), [make-target probe](receipts/make-ids-composition.log), [previous-parser control](receipts/previous-parser-new-tests.log).

- **R472-2 F4 = R473-2 F3 — MINOR — Tests, Docs — RESOLVED.** Artifacts: `scripts/check-ids.py:218` and `docs/architecture/09_verification.md:124`. Authority: the stated executable self-test coverage and round-3 negative-plant requirement. The prior impact was allowing weakened parsers to pass the mandatory regression guard. Required outcome: missing minus-one base, missing line-broken optional member, and composed continuation all require rc 1 and the exact token. Those cases now exist. The exact “any -1” mutation fails case 7; dropping only a line-broken optional member fails cases 8 and 10. Both mutations pass the old 25-case self-test, establishing that the new negative plants distinguish the regressions. Healthy head: all 30 cases pass. The documentation at line 124 accurately names the new cases and diagnostic/status assertions. Evidence: [minus-one mutant](receipts/any-minus-one.log), [optional mutant](receipts/skip-line-broken-optional.log), their `round2-*` controls, and [healthy ids](receipts/make-ids.log).

- **R472-2 F5 — MINOR — Conformance, Docs — RESOLVED.** Artifacts: `docs/diagrams/wavedrom/fig-02-txwave.svg:4`, `fig-02-memwave.svg:4`, sources in `02_interfaces.md:207` and `:585`, renderer `scripts/render-wavedrom.py:96`. Authority: #27 valid-diagram acceptance and the source/render contract. The prior impact was clipped captions and a clipped port label. Required outcome: all text fits under font substitution and committed renders remain fresh. Both sources add 40 horizontal units per side; the TX captions are shorter. Every text element fits in the browser under six font selections. Minimum left bounds are 42.547 units for TX and 29.797 for management; viewport widths are 680 and 600. Standalone ink bounds also fit for every selection: minimum left edges 43 and 31 pixels. Both original figures reproduce overflow under the monospaced selection in the standalone renderer; the browser's original default controls reproduce the previous 679.063 TX right bound and -10.203 management left bound. Both current figures were visually inspected in both renderers. Six selections resolve to two installed families, not six independent fonts. Evidence: [browser bounds](receipts/browser-bounds.json), [standalone bounds](receipts/raster-bounds.json), and the four `fig-02-*-browser.png` / `*-raster.png` receipts. Freshness passes; removing margins fails for both figures, and negative margins fail with the named diagnostic. Geometry controls preserve children and height at margins 0, 1, 40 and 80; negative, fractional, string, Boolean and null margins are refused. [Render controls](receipts/render-probes.json).

- **R472-2 R1 — RESIDUE — Docs — RESOLVED.** Artifact: PR #156 body, Round 3 paragraph. Authority: the manager's exact wording instruction. The previous impact was an outdated publication-status sentence. Required outcome: “not pushed at REVIEW READY”; manager-owned hosted results recorded separately. The current body uses that wording and assigns hosted reporting to the manager. [Saved public PR](receipts/pr-156.json). No source fix or residual wording change is required.

**Earlier public findings and suggestions**

| Prior item | Disposition and exact-head verification |
|---|---|
| Both round-1 F1, MINOR, Conformance/Robustness/Tests/Docs | RESOLVED. Hyphenated braced members are individually checked; malformed braces fail; prose suffixes use the base ID. `T-NVM-{RS-DEADLINE,RS-TYPO}` fails in the independent probes. Healthy self-tests retain the braced and prose-suffix negatives. |
| Both round-1 F2, MINOR, Tests/Docs | RESOLVED. The 17-case figure self-test plants foreignObject, root, namespace and empty/missing-inventory faults. Four independent mutants disabling the previously missing checks each return self-test rc 1. See `figure-skip-*.log` and [artifact checks](receipts/artifacts.json). |
| R473-1 RESIDUE-1, Docs | RESOLVED. F01.5's P-MAAP-RSP-MS row no longer repeats “under 1,800 ms”; reasoning uses the timing ID. |
| R473-1 RESIDUE-2, Docs | RESOLVED. `tb/side_port/README.md:12` says each request is held until its strobe; `KL_pp_side_port.sv:11` names the bridge mapping. |
| R473-1 RESIDUE-3, Docs/PR body | RESOLVED through the historical correction and current “not pushed at REVIEW READY” wording, graded above. |
| R473-1 RESIDUE-4 = R472-1 R1, Docs | RESOLVED once. `02_interfaces.md:106` says “no dual-clock FIFO”. |
| R473-1 SUGGESTION-1 = R472-1 S2, Tests | Taken. Per-tree strays, later-table use, missing heading, empty and duplicate tables have negative plants in `check-ids.py:223`; their exact expected findings and rc are checked. |
| R473-1 SUGGESTION-2 = R472-1 S1, Robustness/Tests | Pins and full history taken at `.github/workflows/hdl.yml:22`. Full dependency lockfile remains optional S1 below. |
| R473-1 SUGGESTION-3, Robustness | Taken. Minus-two fails, continued IDs are checked whole, feImage is refused and planted. The additional round-2 test gaps are closed above. |
| R473-1 SUGGESTION-4/-5/-6 = R472-1 S3, Docs | Taken. F02.2/F02.9 place host ports in the core behind the integrator's bridge; F00.2 includes hand-authored SVG; the NVM request table includes withdrawal at deadline. |
| #84 remaining item 3 | Taken. `01_overview.md:200` explicitly states that P-EN-PLAIN-IEEE-PROFILE has no RTL consumer. |

**S1 — SUGGESTION — Robustness, Tests.** Artifact: `.github/workflows/hdl.yml:28`. The directly relevant packages are pinned, but the full dependency graph has no committed lockfile. This retains the previously acknowledged optional reproducibility improvement; no failing present-head installation was observed. Optional outcome: lock the complete dependency graph. Verification if adopted: a fresh locked install and `make check` pass with recorded resolved versions.

**S2 — SUGGESTION — Docs.** Artifact: `docs/guides/integrator.md:216`. The pre-existing `wr_done_i` / `wr_ready_i` shorthand remains outside the edited lines, beside a table containing the full names. This retains the earlier acknowledged observation. Optional exact change: use `resp_mem_wr_done_i` / `resp_mem_wr_ready_i` in that paragraph. Verification if adopted: names agree with the table and top declarations. Neither suggestion leaves a lens unclean.

**Acceptance and artifact-specific results**

| Scope | Evidence and result |
|---|---|
| #27 current boundary and RX without backpressure | PASS. 02 §3 names the eight byte-face ports; the RX figure has valid/data/last and no ready. All 109 explicit port names in 02 occur in the top declarations. The top's byte faces at `protocol_processor_top.sv:286`, TX shim at `:4550`, side-port FSM at `KL_pp_side_port.sv:128`, and NVM device face agree with the changed contracts. |
| #27 history and valid diagrams/links | PASS. The history paragraph/table and both old waveform sources are verbatim substrings of base 02. Links from the root README, docs/README and 02 make the history discoverable. Current waveform timing preserves RX byte intake, held TX A2 and held host request/completion behavior. All 1,168 links and 18 generated renders pass. |
| #70 registry rows, values and executable gate | PASS. Both MAAP defaults agree with `KL_acmp_talker.sv:140` and `:180`; they are module parameters, and 02 references their IDs without copied defaults. The dynamic-mapping stray is absent. Healthy scan: 531 files, 91 distinct IDs, 47 P rows and 36 T rows. docs/README §2 and 09 §8 both explicitly leave value scanning unimplemented. |
| #71 acceptance 1 and 3 | PASS. `integrator.md:135` requires complete FCS-good frames, whole-frame discard and no partial presentation because RX has no err/abort. `00_MILAN_COMPLIANCE_REVIEW.md:531` assigns dual-clock FIFOs to the integrator. The reset correction is inherited from the publicly assigned lane. |
| #75 all four acceptance items | PASS. CI executes the actual nine-prerequisite `make check`; hand-authored SVG is listed and gated; all five PNGs are absent; 09 §7 matches execution. Figure totals: 3 source/export pairs, 18 waveforms, 5 hand-authored SVGs. |
| Scope and RTL preservation | PASS. The complete requested diff includes earlier merged lanes. Against incorporated main `ead80360`, C11 changes only comments in three HDL files and one compiled harness: all four executable token streams are identical. The round-3 delta contains no HDL or testbench file. The base/head diff and history are preserved in `source.diff`, `rtl.diff` and `history.txt`. |

**Reviewer execution**

| Receipt | Result |
|---|---|
| [make-check.log](receipts/make-check.log) | rc 0: 41 flow/sequence and 18 waveform blocks; 18 fresh SVGs; 1,168 links; 115 requirements / 17 gaps; module matrix 94 rows / zero untested; parameters 28/28/28; 30 ID and 17 figure self-tests; all nine gates pass. |
| [make-ids.log](receipts/make-ids.log) | Separate exact-head `make -j16 ids`, rc 0. |
| [rx_validator.log](receipts/rx_validator.log), [tx_arbiter.log](receipts/tx_arbiter.log), [side_port.log](receipts/side_port.log) | rc 0 each: 555/555, 66/66 and 368/368 checks. These exercise byte intake, TX stalls/arbitration and host request/strobe behavior with the real trace ring. |
| [id-probes.json](receipts/id-probes.json) and `make-ids-*.log` | Sixteen independent notation probes; two regression mutants rejected; previous parser rejected by revised tests; three missing-ID plants fail the full target and the valid composition passes. |
| [render-probes.json](receipts/render-probes.json), [artifacts.json](receipts/artifacts.json) | Eighteen margin geometry/input checks, two freshness fault controls, four figure-check mutants, port/history/scope checks all meet their expected outcomes. |

Independent checks and three focused builds ran concurrently under a foreground coordinator, with separate logs/status files and a foreground join. Compilation was capped at four workers per build, twelve total; no heavy synthesis build ran. The scoped simulator identity was verified before use and is preserved with its SHA256 in [environment.txt](receipts/environment.txt). Expected negative controls return nonzero by design. Portable scripts and prerequisites are in [REPRODUCE.md](REPRODUCE.md).

**Public and hosted evidence limits**

The assignment reports the manager's full source static/builder and native banks passed at this head. That is recorded as supplied manager evidence, distinct from the focused reviewer executions above. The current PR body separately reports exact-head source and earlier-parent consumer runs.

The [specified immutable public packet](https://github.com/kebag-logic/milan-fpga/tree/4a3ae4a1a4bf5a2fcd85b6d0aeff441f3f853a9f/review-evidence/ppC11-r1) contains the round-1 handoff/body and four adoption patches. Its downloaded handoff hash matches its published manifest; it describes `91cef52`, not this head. The refreshed manager comments on #27 and #156 contain scope and review-start statements, with no exact-head manager bank receipt link. I did not access private files to fill that gap. This is an evidence-attribution limit, not a claim that the stated manager execution failed.

At `2026-10-05T08:23:47Z`, both [push run 37281818928](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37281818928) and [PR run 37281823263](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37281823263) have executed successful docs-gates and portability jobs. Their suite jobs remain in progress and are not counted as passed. The simulator-build step was skipped after cache restoration; it is not a fresh-build result. The saved docs logs prove actual gate execution. The push checkout is the exact head. The PR checkout `be03ccf76f859929f5e26f8d9216ba6b9344421b` is a synthetic merge whose tree exactly equals the reviewed tree. [Hosted summary](receipts/hosted-summary.json), `hosted-docs-*.log`, and [merge identity](receipts/hosted-merge.json).

**Reviewer-owned final ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen #27/#70/#71/#75 acceptance; F01.5/F08.1; 02 interfaces and current figures; REQ-REU-002/003 and REQ-DOC-001; missing-ID outcomes | R473-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| RTL | CLEAN | Top byte/host/NVM ports and TX shim; RX validator, TX arbiter and side-port FSM; C11 executable-token identity; three focused native suites | R473-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Robustness | CLEAN | Continued/optional/braced/sibling/minus-one forms; malformed-input cases; margin type/geometry checks; freshness faults; figure-control mutants | R473-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Tests | CLEAN | 30 ID / 17 figure cases; two old-surviving/new-failing ID mutants; previous-parser control; four figure mutants; full make targets; native checks; hosted execution/skips distinguished | R473-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Docs | CLEAN | docs/README; architecture 01/02/03/07/08/09; guides, history, compliance rows and figure inventory; 09:124 coverage claim; two-renderer measurements and inspected images; PR wording | R473-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |

**Integrity, real limits and remaining manager duties**

The review checkout was never edited. After probes, all 556 tracked blobs, executable modes, HEAD, tree and index match the exact published head. The scratch source copy is restored to the same tracked bytes/modes/index. Both have clean tracked/untracked status; ignored build outputs remain only in scratch. This processor repository has zero submodule gitlinks. A read-only public tree check records all four parent gitlinks at live dev `fa450d301805881ad713b67521477bf042ddadfd`; its existing processor pin is `631eeb34`, so that tree is not the final candidate containing this head. See `integrity-final.json`, `integrity-scratch-final.json` and `parent-live-gitlinks.json`.

No full parent/processor/gPTP/portability/builder bank or synthesis implementation was run by this reviewer. The inherited RTL lanes are not independently recertified in full. No copyrighted specification PDF was consulted; this scope/contract review does not certify every cited standards clause. Physical calibration NOT RUN. Field skips are not hardware proof. No hardware, workflow emulator, privilege/shared install, source fix, commit, push, GitHub write, author contact, delegation or edit to an unrelated checkout occurred.

The manager still owns:

1. Publishing this packet and completing independent review acceptance at this exact head.
2. Associating the manager's source static/builder/native receipts with the exact source head; retaining actual skips and NOT RUN arms, including physical calibration, without upgrading them to passes.
3. Building and validating the final current-dev candidate at the merge turn, with source base `c050d97153dd0480ae741102c1647eeda9b7f273`, live dev `fa450d301805881ad713b67521477bf042ddadfd`, the intended adoption content and required gitlinks. Source validation is distinct from candidate validation.
4. Hosted/local-workflow acceptance, including the unfinished suite jobs, skipped contexts and final public hosted-status record.
5. Carrying the two acknowledged optional follow-ups; closing #27/#70/#75 and the remaining #71 items only after the accepted merge. No new residue is opened by this round.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable; scratch is excluded.

R473-3 FINISHED
