[R472] NEGATIVE - exact head 5123548eb4de35f24d43eb088c12dab70b06d01d

Round R472-3, issue #27 / PR #156. Tree `33b4fe59951370299cad36ec1415ead003524d5f`; source base `c050d97153dd0480ae741102c1647eeda9b7f273`. Head has one parent, `80588cdc43ca5605a1d3748d13dd8ed7f22f7000`, and changes seven documentation, script and SVG files in this round.

The round-3 source repairs pass the technical review: F3, F4, F5 and R1 are resolved, as are the original F1/F2. No new product defect was found. **The overall verdict is nevertheless NEGATIVE because this session did not preserve the required independent-review reading sequence (F6). This packet must not count as the required independent positive sign-off.** No source change is requested for F6; a replacement review is required. All five lenses were applied.

**F6 - MINOR - Tests, Docs - required report-reading sequence was not preserved.**

- **Artifact:** this review's evidence collection and `receipts/independent-assessment.md`.
- **Authority/evidence:** the assignment forbids reading another reviewer's report before this review's own verdict and ledger are written. While locating manager evidence comments, a filter excluded uppercase `FINDINGS` but failed to exclude reviewer-prefixed comments containing complete reports. Prior public reports were exposed after the independent diff pass, focused suites and ID controls, but before the written verdict and ledger. The native measurement campaign was still being corrected at that point. The subsequent assessment records this deviation. No private author material, management checkout, private scratchpad or separately linked reviewer packet was opened.
- **Impact:** the stricter independence sequence cannot be certified. Passing source checks do not repair this review-process defect. Tests and Docs coverage cannot be banked as clean independent approval from this session.
- **Required outcome:** a fresh cleared-context review of this exact head, preserving the requested order and writing its own verdict and ledger before opening other review reports. Do not interpret this process finding as a request for another source patch.
- **Verification:** the replacement packet records its ordered authority/diff/evidence reconstruction, independent verdict and ledger, then prior-finding reconciliation. No replacement session or sub-agent was started here, as prohibited by the assignment.

**Prior-finding dispositions at this head.**

| Prior item and attributable lenses | Disposition | Exact-head verification |
|---|---|---|
| R472-2 F3: MINOR; Conformance, Robustness, Tests, Docs | RESOLVED | `scripts/check-ids.py:115` completes successive continued segments before evaluating suffixes. `T-ADP-` followed by `DELAY(-STRT)` fails naming `T-ADP-DELAY-STRT`; `START` passes. Both-newline, CRLF and seven comment-leader forms also behave correctly. The real-tree composition makes `make -j16 ids` return 2 with the full token. `ids-probes.json`, `artifact-probes.json`. |
| R472-2 F4 / R473-2 F3: MINOR; Tests, Docs | RESOLVED | Cases 7-10 of the 30-case self-test plant the missing minus-one base, missing line-broken optional member, continued-ID composition and both breaks together. Exact diagnostic tokens and rc 1 are asserted. The independent “any -1” mutant fails case 7; skipping a line-broken optional fails cases 8 and 10. The previous parser with the new plants fails cases 9 and 10. Healthy controls, valid minus one and invalid minus two behave correctly. `09_verification.md:124` matches the executable coverage. |
| R472-2 F5: MINOR; Conformance, Docs | RESOLVED | F02.4/F02.7 source margins and regenerated SVGs pass browser/native measurements and visual inspection under both installed font families. Old-head controls reproduce clipping. Freshness passes; removing both margins fails freshness naming both figures. See measurements below. |
| R472-2 R1: RESIDUE; Docs | RESOLVED | The public PR body's Round 3 paragraph now says “not pushed at REVIEW READY; the manager records the hosted runs after the push.” This is a historical snapshot, not a current no-hosted-run claim. No further wording fix is required. `receipts/pr.json`. |
| R472-1 / R473-1 F1: MINOR; Conformance, Robustness, Tests, Docs | Remains RESOLVED | Hyphenated braced-member control fails with its expanded missing ID. `P-RX-shaped` is a negative self-test case; family notation is explicit `-*`. Healthy self-test and full IDs target pass. |
| R472-1 / R473-1 F2: MINOR; Tests, Docs | Remains RESOLVED | All 17 figure cases pass. Independently disabling foreignObject, root/namespace or empty-inventory checks makes self-test return 1 on the corresponding case. `artifact-probes.json`. |
| R473-1 RESIDUE-1/-2/-4; R472-1 R1 | Remains RESOLVED | F01.5 omits “under 1,800 ms”; the side-port README describes each request held until its strobe; the module banner names the bridge mapping; 02 rule 2 says “no dual-clock FIFO”. |
| R473-1 RESIDUE-3 | Superseded and RESOLVED by the historical status wording above | Current PR body makes no claim that the published head lacks hosted runs. Actual observed jobs are recorded separately below. |
| R472-1 S2 / R473-1 SUGGESTION-1 | Implemented | Per-tree strays, later-table use, missing heading, empty timing table and duplicate parameter row are executable cases in `check-ids.py:223` onward. |
| R472-1 S1 / R473-1 SUGGESTION-2 | Pins/full history implemented; lockfile SUGGESTION retained | `.github/workflows/hdl.yml:18` fetches full history and pins diagram packages. A complete transitive dependency lockfile remains an acknowledged non-blocking follow-up. |
| R473-1 SUGGESTION-3 | Implemented | Minus-one exception requires a defined base; continued IDs resolve; `feImage` has a check and negative plant. |
| R472-1 S3 / R473-1 SUGGESTION-4/-5/-6; #84 remaining item 3 | Implemented | F02.2/F02.9 put host ports in the core domain behind the integrator's bridge; F00.2 lists hand-authored SVG; NVM table includes withdrawal at deadline; F01.5 records no RTL consumer for the plain-IEEE profile. |
| Pre-existing integrator `wr_done_i` / `wr_ready_i` short-name observation | Retained outside this lane's changes | The public PR acknowledges this existing follow-up. It requests no new source fix in this round. |

No earlier MINOR, MAJOR or BLOCKER remains an open product defect. No new wording-only residue is opened.

**Technical evidence by lens.**

| Lens | Examined artifacts and result |
|---|---|
| Conformance | Frozen #27/#70/#71/#75 acceptance; 00 REQ-REU-002/003 and REQ-DOC-001; F01.5/F08.1; 02 sections 2/3/7/8; integrator section 3. Byte-wide MAC, host and device-side NVM ports agree with the landed top. All 109 explicit 02 port names are declared there. RX has no ready/error/abort; complete FCS-good frame delivery and CDC ownership belong to the integrator. History prose/table and both old waveform sources match base bytes. Links, figures, ID rows and scope changes pass. |
| RTL | `hdl/top/protocol_processor_top.sv:285`, `:565`, `:583`, TX output shim and host binding at `:4667`; `KL_pp_tx_arbiter.sv`, `KL_pp_tx_slots.sv`, `KL_pp_side_port.sv`, NVM device declarations. Traced byte acceptance, held TX data under stalls, frame arbitration, host request/completion and NVM directions. Four focused suites pass. Against merged main `ead80360`, the three changed HDL files and `tb/tx_slots/sim_main.cpp` have identical executable tokens after comments/whitespace are removed. Round 3 changes no HDL or testbench file. |
| Robustness | `check-ids.py:109`, `:146`, `:210`; `check-figures.py:93`; `render-wavedrom.py:96`. Twenty-one independent ID controls cover undefined bases, optional/continued compositions, repeated continuation, malformed optional syntax, braced/sibling/family suffixes and CRLF/comment leaders. Three parser mutants are rejected. Margins 0/1/40/80 preserve waveform children and height and expand width/viewBox correctly. Negative, fractional, string, Boolean and null margins are rejected. Source-removal and malformed-margin controls fail actual freshness checks. |
| Tests | Makefile's nine check prerequisites and CI invocation match 09 section 7. Complete `make -j16 check` and separate `make -j16 ids` return 0. Both gate self-tests pass; requested parser mutants and original figure-check mutants make self-test red. Four real interface suites run from an exact-head disposable clone. No test weakness remains in the reported source fixes. F6 prevents clean independent Tests approval from this session. |
| Docs | Root/docs READMEs; architecture 01/02/03/07/08/09; guide/history/inventory; F02.3/F02.4/F02.7; public PR body. Current/history separation is explicit. No obsolete RX backpressure contract is presented as current. Value scanning remains outside the implemented gate's claim. The 09:124 case description and status snapshot are accurate. Both repaired renders were inspected and measured. F6 prevents clean independent Docs approval from this session. |

**Executed checks and measurements.** Independent commands ran concurrently under a foreground coordinator with individual log/rc files, following the assignment's final foreground instruction. Four small compilations were capped at two build workers each. No full processor, parent, gPTP, synthesis or builder bank was run here.

| Receipt | Result |
|---|---|
| `receipts/make-check.log` / `.rc` | rc 0: 41 flow/sequence and 18 waveform blocks; 18 fresh SVGs; 1,168 links; 115 requirements / 17 gaps; 94 module rows, zero untested; parameters 28/28/28; IDs 30 cases, 531 files, 91 uses, 47 P rows, 36 T rows; figures 17 cases and 3/18/5 classes; staleness passes. |
| `receipts/make-ids.log` / `.rc` | rc 0, healthy 30-case self-test and real-tree scan. |
| `receipts/side_port.log`, `tx_arbiter.log`, `tx_slots.log`, `rx_validator.log` and `.rc` | All rc 0: respectively 368/368, 66/66, 95/95 and 555/555 checks. |
| `receipts/ids-probes.json`, `.log`, `.rc` | 21 controls and three rejected mutants. Campaign rc 0 means every expected outcome occurred, including intentional checker/self-test rc 1. |
| `receipts/artifact-probes.json`, `.log`, `.rc` | History/executable-token identity; 109 port names; margin/type controls; actual freshness failures; two real-tree `make ids` failures; three rejected figure mutants; disposable copy restored. Campaign rc 0. |
| `receipts/browser-bounds.json`, `native-bounds.json`, measurement `.rc` files and PNGs | Both campaigns rc 0; head text inside viewport; old controls fail as expected. |
| `receipts/identities.json` | Scoped compiler reports 5.050, revision v5.050; entry SHA256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`. Diagram CLI 11.16.0; source renderer 2.0.3.post3. Compiler identity was checked before suite execution. |

TX viewport is now 680 by 272 units; host viewport is 600 by 286. Browser minimum left text margins are 42.55 and 29.80 units. Native measurements at 96 dpi with the installed monospaced font give 43.09 and 31.00 units. Both installed families, proportional and monospaced, pass. Six browser selections include fallback aliases and are not six distinct installed fonts. Native default and both-family checks pass. Original browser controls reproduce TX right edges 604.32 and 679.06 in a 600-unit viewport, and host left edge -10.20. Native monospaced controls reproduce the same fault classes. Freshness is checked separately from fit.

Portable scripts in `scripts/` take repository and packet paths; all mutation/build copies and the Python environment live in packet `scratch/`. `run_checks.py --jobs 6` bounds concurrent checks; `probe_ids.py --jobs 4` bounds the control campaign. `measure_browser.mjs` also accepts the browser-driver package directory. `measure_native.py` uses the installed SVG library at 96 dpi. These are reviewer probes, not proposed repository changes.

**Public authorities and evidence limits.** Local/ancestor rule-file locations were checked first: this checkout has no tracked AGENTS.md or CONTRIBUTING.md. Supplied instructions, docs/README, issue bodies and public manager scope comments, linked interface/registry authorities, then the requested base-to-head diff and history governed the pass. The parent's public AGENTS section 6 and CONTRIBUTING were subsequently cross-checked at `4a3ae4a1`. They confirm the five-lens and two-review rules. The task's stricter severity, foreground and prohibited-command instructions governed here. The full requested diff includes already-merged main lanes #154/#157/#155. Their storage/hazard changes were inspected for provenance and interface implications; their complete banks were not rerun or recertified here.

The six files in the [specified public packet](https://github.com/kebag-logic/milan-fpga/tree/4a3ae4a1a4bf5a2fcd85b6d0aeff441f3f853a9f/review-evidence/ppC11-r1) match every published manifest hash. That packet contains round-1 executor handoff/body and four adoption patches at `91cef52` and an earlier parent base. It contains no current-head manager bank receipts. Fetched #27/#156 comments contain scope, readiness, review starts and prior reports; no current-head manager bank receipt was available there. Current PR body separately describes round-3 executor results.

The assignment's statement that manager source static/builder and native banks passed at `5123548e` is recorded as supplied manager evidence, not independently inspected raw receipts or reviewer execution. It does not establish the final current-dev candidate result.

At the saved 2026-10-05 08:19 UTC snapshot, [push run 37281818928](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37281818928) and [PR run 37281823263](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37281823263) identify the exact reviewed head. Both have executed successful docs-gates and portability jobs; both suites jobs remain in progress. Cached-compiler build steps are skipped, not fresh build evidence. Pending exhaustive campaign steps are not passes. Both raw docs-job logs were retrieved and show full-history checkout, actual diagram checks and the 30-case ID self-test. Push checks out the exact head; PR checks out synthetic merge `be03ccf`, whose tree is independently confirmed equal to the reviewed tree (`hosted-pr-merge-tree.json`). Hosted/local-workflow acceptance remains the manager's duty.

**Reviewer-owned final ledger.** CLEAN rows report bounded source examination; this overall NEGATIVE packet cannot supply independent sign-off.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen #27/#70/#71/#75; F01.5/F08.1; REQ-REU-002/003; 02 interfaces; history identity and gates | R472-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| RTL | CLEAN | Top byte/host/NVM faces and wiring; TX arbiter/serializer and side-port; executable-token identity; four suites | R472-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Robustness | CLEAN | 21 ID controls; three parser mutants; margin/type/freshness controls; figure-check mutants | R472-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Tests | UNCLEAN (F6, review process) | Complete gates and focused suites; negative controls; independence-sequence receipt | R472-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Docs | UNCLEAN (F6, review process) | 09:124 coverage; current/history docs; measured F02.4/F02.7; PR snapshot; collection record | R472-3 | 5123548eb4de35f24d43eb088c12dab70b06d01d |

Final integrity verifies all 556 raw tracked blobs, 539 regular and 17 executable modes, every index entry, HEAD/tree and index tree. No mismatch; clean status. Review clone and both disposable exact-head source copies match. Processor contains no submodule gitlinks. Read-only parent-tree inspection at supplied live dev `fa450d301805881ad713b67521477bf042ddadfd` records `external=efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`, `gptp-processor=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, `third_party/verilog-axis=48ff7a7e2ef782cf778d47910cf85835c64b1bce`, and existing processor pin `631eeb342ca1e3fa80e734077a56a943aee76ff1`. That parent tree alone is not a candidate with this reviewed head. No parent checkout or gitlink was changed.

Physical calibration **NOT RUN**. Field skips are not hardware proof. No hardware, prohibited full bank, workflow emulator, privileged/shared install, source fix, source commit, push, merge, GitHub write, author contact or sub-agent was used. Scratch is never publishable. Only REPORT.md and files listed in MANIFEST.sha256 are publishable.

Pending manager duties:

1. Obtain a replacement independent review preserving the required sequence; do not count this as a positive review. Technical closures above require no further source patch on the evidence examined.
2. Publish/link current-head manager source/static/builder/native receipts with exact identities and exclusions.
3. Construct and validate the final current-dev candidate at merge turn, using the reviewed source head, source base `c050d97153dd0480ae741102c1647eeda9b7f273`, current parent dev and intended adoption/gitlink changes. Keep source validation separate from candidate validation.
4. Complete hosted/local-workflow acceptance, distinguishing executed, pending and skipped work; retain calibration/hardware limitations.
5. Preserve acknowledged lockfile and guide-short-name follow-ups. Close scoped issues only after accepted merge and required containment checks.

R472-3 FINISHED
