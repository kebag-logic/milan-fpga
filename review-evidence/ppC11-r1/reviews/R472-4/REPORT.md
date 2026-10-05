[R472] POSITIVE - exact head 5123548eb4de35f24d43eb088c12dab70b06d01d

Round R472-4 is a replacement internal review of issue #27 / PR #156. It covers tree `33b4fe59951370299cad36ec1415ead003524d5f`, source base `c050d97153dd0480ae741102c1647eeda9b7f273`, and one head parent, `80588cdc43ca5605a1d3748d13dd8ed7f22f7000`. The round-3 commit changes seven documentation, script and SVG files. In the lane's net change against merged main `ead80360`, the only HDL and testbench edits are comments.

I applied all five lenses. The round-3 scope is resolved at this head: R472-2 F3, F4 and F5, R473-2 F3, and R472-2 R1. No MINOR, MAJOR or BLOCKER is open. Three new SUGGESTIONs are recorded (S1 to S3). They do not leave any lens unclean.

## Review order (independence record)

1. **Authority.** I checked for tracked `AGENTS.md` / `CONTRIBUTING.md`; this repository has neither. I then read the root README and docs/README, and the frozen issue #27 body. From the issue and PR, I read only the non-reviewer comments: the lane scope (5980174687), the round-2 and round-3 assignments (5982157556, 5988273127), the REVIEW READY posts and the review-start notices. Reviewer-tagged comments were filtered out by their first line. Interface authorities were 02 §2/§3/§7, F01.5/F08.1, docs/README §2/§3, 09 §7, and the top's port declarations.
2. **Diff and history.** I read `c050d971..5123548e`, the lane's net change `ead80360..5123548e` (31 files) and the round-3 commit `80588cdc..5123548e`.
3. **Public evidence.** The manifest at `kebag-logic/milan-fpga@4a3ae4a1` `review-evidence/ppC11-r1`, its six files, and the exact-head hosted job records.
4. **Verdict frozen.** I wrote my own verdict and lens ledger to `VERDICT-PRE-RECONCILE.md` (sha256 `c81bd8074885060aed4abf2c3872f627df922aa69d3d3185c409955c34382ed1`). Only after that did I open any prior review report on PR #156: R472-1/R473-1, R472-2/R473-2 and R472-3/R473-3. Reconciliation added two confirmatory reproductions, `realtree_prior_controls.txt` and mutant M12. No verdict changed.

I did not read any private author material, management checkout, scratchpad or other reviewer packet.

## Prior findings, resolved or retained at this head

| Prior item (severity; lenses) | Disposition | Exact-head verification |
|---|---|---|
| R472-2 F3 (MINOR; Conformance, Robustness, Tests, Docs): an optional member after a line-broken ID was lost | **RESOLVED** | `scripts/check-ids.py:115-120` completes every continuation line before the suffix checks at `:121-140`. Probes on planted trees: `T-ADP-`⏎`DELAY(-STRT)` gives rc 1 naming `T-ADP-DELAY-STRT` in markdown, `//`, `#`, ` * `, `>` and CRLF forms. Break-in-both and double-continuation forms also give rc 1. The `START` counterparts give rc 0 (`probe_ids_forms.txt`). In a disposable real-tree copy, editing `tb/adp_engine/tb_adp_top.sv:10` to `DELAY(-STRT)` makes `make ids` return 2 with `T-ADP-DELAY-STRT has no F08.1 row`. The `START` form returns 0, and the restored copy returns 0 (`realtree_prior_controls.txt`). |
| R472-2 F4 = R473-2 F3 (MINOR; Tests, Docs): no missing-ID plant for minus-one or a line-broken optional | **RESOLVED** | Self-test cases 7-10 (`check-ids.py:218-221`) plant a missing minus-one base, a line-broken optional, the F3 composition and both breaks. Each asserts rc 1 and the exact token (`:274`). The mutants all turn the self-test red: any-minus-one (M1, case 7), R472-2's skip-optional-only-when-line-broken (M12, cases 8 and 10), and the round-2 continuation order (M2, cases 9 and 10). The real round-2 parser with the head's cases fails 9 and 10 (`mutate_ids_selftest.txt`, `round2_parser_with_head_cases.txt`). R473-2's real-tree plant `P-R472-MISSING-1` in an untracked `tb/` file makes `make ids` return 2 (`realtree_prior_controls.txt`). `09_verification.md:124` matches the executable cases. |
| R472-2 F5 (MINOR; Conformance, Docs): F02.4/F02.7 renders clipped text | **RESOLVED** | Sources `02_interfaces.md:207` and `:585` carry `svg_margin: 40`, and the TX captions are shorter. Headless-browser text bounds were measured under eight font selections, which resolve to the two installed families. Every text element of both head SVGs is inside the viewBox: TX minimum left margin 40.50 to 61.47 units, host 26.50 to 61.33. The round-2 SVGs reproduce both faults as controls: TX footer to x = 687.0 and host `host_req_valid_i` at x = -13.5 / -10.2 (`text_fit.txt`). Standalone-rasterizer renders were inspected visually, with no clipping or overlap. Committed renders are fresh under the CI-pinned renderer. |
| R472-2 R1 (RESIDUE; Docs): stale hosted-status sentence | **RESOLVED** | The PR body's Round 3 entry reads "not pushed at REVIEW READY; the manager records the hosted runs after the push. No hosted result is claimed for this round." That is the manager's exact wording. |
| R472-3 F6 (MINOR; Tests, Docs): review-process order not preserved | **RESOLVED by this replacement round** | This round kept the required order (see above). F6 requested no source change. |
| R472-1/R473-1 F1 and F2, their residues, and the #84 item | Remain **RESOLVED** (spot-checked) | The full `make check` passes with the figures self-test at 17 cases and the ids self-test at 30. Mutants M9 (family) and M10 (bad braced list) are killed. The R473-1 RESIDUE-4 wording "no dual-clock FIFO" is at `02_interfaces.md:106`. |
| Optional dependency lockfile for the diagram CLI (R472-1 S1 / R473-3 S1) | **Retained as SUGGESTION** | `.github/workflows/hdl.yml:27-28` pins the direct packages only. Non-blocking, and acknowledged in the PR body. |
| Integrator guide short names `wr_done_i` / `wr_ready_i` (R473-3 S2) | **Retained as SUGGESTION** | `docs/guides/integrator.md:216-217`. Blame shows these lines predate source base `c050d971`, and the lane does not edit them. |

## New findings (reviewer-owned)

**S1 - SUGGESTION - Robustness, Tests - a sibling or optional form wrapped at whitespace is read as prose.**
- **Artifact:** `scripts/check-ids.py:49` (`SIBLING`) and `:55` (`OPTIONAL`). They allow no line break before `/`, between `/` and `-`, after the sibling's hyphen, or between an ID and `(`.
- **Evidence:** planted trees using the self-test master tables (`probe_ids_forms.txt`). Each of these returns rc 0 with no finding: `T-BUDGET-AECP-TYP /`⏎`-XX`, the same with a `//` leader, `T-BUDGET-AECP-TYP`⏎`/ -XX`, `T-BUDGET-AECP-TYP / -`⏎`XX`, and `T-ADP-DELAY`⏎`(-STRT)`.
- **Why not MINOR:** the documented sibling and optional forms are single-line. "An ID broken at a line end" is handled, including that composition with a sibling (`T-BUDGET-AECP-`⏎`TYP / -XX` gives rc 1). The tree's only sibling use is the F08.1 row at `08_timing.md:50`, and it is not wrapped. The gate's stated model treats any other text as prose.
- **Impact:** latent. A future prose wrap at the space inside `TYP / -WC` would hide a mistyped sibling.
- **Optional outcome:** accept `NEXT_LINE` around `/` and after `-` in `SIBLING`, or fail closed when a line ends on `ID /` or `ID / -`, and plant one wrapped stray.
- **Verification if adopted:** each wrapped stray above gives rc 1 with its token.

Related observation, no finding: `T-NVM-`⏎`{RS-DEADLINE}` fails closed with a `T-NVM` diagnostic. That is a false positive, not a bypass.

**S2 - SUGGESTION - Tests - no negative plant for successive continuation lines.**
- **Artifact:** the `check-ids.py:118` loop and self-test case 6 (`:216-217`, which is positive only).
- **Evidence:** mutant M3 replaces `while` with `if`. It passes all 30 cases, yet returns rc 0 on `T-ADP-`⏎`DELAY-`⏎`STRT` (`mutate_ids_selftest.txt`, `m3_failopen_probe.txt`). The production loop is correct: the same text gives rc 1 (`probe_ids_forms.txt`).
- **Why not MINOR:** the round-3 required plants and both named mutants are covered. 09 §7's per-form claim (a stray in the line-broken form) is met by case 18. Only the round-3 PR-body remark "Successive continuation lines work as well" lacks a regression guard.
- **Optional outcome:** add `({CASE: "T-ADP-\n// DELAY-\n// STRT"}, ["T-ADP-DELAY-STRT"])`.
- **Verification if adopted:** M3 turns the self-test red.

**S3 - SUGGESTION - Docs - F02.3 (rxwave) has little left text margin.**
- **Artifact:** `docs/diagrams/wavedrom/fig-02-rxwave.svg` and its source at `02_interfaces.md:171-186`.
- **Evidence:** it fits under every measured selection, with minimum left margin 0.50 to 2.55 units (`text_fit.txt`). It is not clipped, and no lane claim is affected.
- **Optional outcome:** add the same `"config": {"svg_margin": 40}` and re-render.
- **Verification if adopted:** freshness passes and the bounds stay positive with headroom.

## Acceptance and lens evidence at this head

| Acceptance / constraint | Result |
|---|---|
| #27: current pages show only landed ports; RX has no backpressure | Met. 02 §3 (`02_interfaces.md:135-161`, table rows `:145-152`) lists `rx_valid_i`, `rx_data_i`, `rx_last_i` and the five TX ports, exactly as declared at `protocol_processor_top.sv:286-295`. 02 §7 (`:554-560`) lists the seven `host_*` ports declared at `:583-589`. F02.3 has no ready signal. F02.4's source and render (A2 held while `tx_ready_i` is low, B after A's eof) match 02 §3's prose at `:159-161`, so the shortened captions drop no contract text. F02.7 shows the request held through its strobe and one wait state on the read. |
| #27: history discoverable; links and diagrams valid | Met. `make check`: 1,168 links, 41 Mermaid and 18 WaveDrom blocks, all 18 renders fresh, and the figures gate at 3/18/5 classes. |
| Round-3 F5 renderer contract | Met. `render-wavedrom.py:96-108` widens the viewBox and width by 2 × margin and leaves the content unchanged. `probe_margin.txt`: removing the TX margin, or changing both margins to 39, fails freshness naming the figures. Margins -1, 1.5, "40", true and null fail with `config.svg_margin must be a non-negative integer`. Margin 0 reproduces the round-2 geometry header exactly. The docs/README §3 text at `:119-123` describes this behaviour accurately. |
| Docs, scripts and CI only | Met. Comment-stripped preprocessed token streams of `KL_pp_side_port.sv`, `KL_pp_trace_ring.sv`, `KL_pp_tx_slots.sv` and `tb/tx_slots/sim_main.cpp` are identical between `ead80360` and the head. A planted one-identifier code change is detected (`comment_only.txt`, `comment_only_control.txt`). Round 3 touches no HDL or testbench file. |

## Executed evidence (reviewer execution)

| Receipt | Result |
|---|---|
| `make_check.log` / `.rc` | rc 0, run with the CI-pinned renderer 2.0.3.post3 from a scratch environment. Lint: 41 Mermaid + 18 WaveDrom blocks. WaveDrom: 18 fresh. Links: 1,168. Matrix: 115 REQ / 17 GAP. Modmatrix: 94 rows, 0 untested. Parameters: 28/28/28. Figures: self-test 17, and 3/18/5 classes. IDs: self-test 30, then 531 files, 91 IDs, 47 P rows, 36 T rows. Staleness passes. |
| `lint_hdl.log`, `suite_tx_slots.log`, `suite_side_port.log` with `.rc` files | All rc 0: lint 41 targets OK, tx_slots 95/95, side_port 368/368. These used the scoped simulator 5.050 (rev v5.050, entry sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`), whose identity was checked before use. The local include path in the suite logs is redacted to `<VERILATOR_ROOT>`. |
| `probe_ids_forms.txt` | 24 planted-tree probes of the parser (F3 forms, minus-one, continuation compositions, and the S1 wrap forms). |
| `mutate_ids_selftest.txt`, `m3_failopen_probe.txt`, `round2_parser_with_head_cases.txt` | 13 self-test runs: the identity plus 12 mutants. 11 mutants are killed. M3 survives (S2). The round-2 parser with the head's cases fails 9 and 10. |
| `realtree_prior_controls.txt` | Real-tree `make ids` controls for R472-2 F3 and R473-2 F3, run in a disposable clone and restored to rc 0. |
| `text_fit.txt` | Text bounds for 3 head and 2 round-2 SVGs × 8 font selections. Overall rc 1 is expected and comes only from the round-2 controls. |
| `probe_margin.txt`, `comment_only*.txt` | Described above. |
| `public_evidence_and_hosted.txt` | All 6 evidence files match the published manifest hashes. Hosted docs-gates jobs for the push run 37281818928 and the pull-request run 37281823263 at the exact head executed step 4, `make check`, with success. Portability succeeded in both runs. Suites was **in progress** at the 08:42 UTC snapshot; no pass is counted for it. |
| `integrity_final.txt` | See Integrity below. |

Measurement note: the round-3 PR body gives minimum left margins of 42.55 (TX) and 29.80 (host). I reproduce those exactly when the monospaced family is named directly. The SVG's authored `Helvetica` alias resolves to the same family here but with whole-pixel advances, which gives 40.50 and 26.50. All measured values are positive. This is an environment difference, not a defect.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #27 frozen acceptance and the lane and round-3 scope; 02 §2 rule 2, §3 and §7 tables against top ports `:286-295` and `:583-589`; F02.3/F02.4/F02.7 sources and renders against 02 prose; F01.5/F08.1 masters through the ids gate | R472-4 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| RTL | CLEAN | Comment-only token identity of the three HDL files and one testbench file, with a detected control; HDL lint (41 targets); tx_slots and side_port suites; no round-3 HDL change | R472-4 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Robustness | CLEAN (S1 suggestion) | `check-ids.py` continuation, optional, sibling, brace, family and minus-one parsing across 24 probes and the real-tree controls; `render-wavedrom.py` margin type and range validation and geometry | R472-4 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Tests | CLEAN (S2 suggestion) | 30-case ids self-test against 12 mutants plus the round-2 parser; full `make check`; freshness negative controls; hosted docs-gates step execution (suites pending) | R472-4 | 5123548eb4de35f24d43eb088c12dab70b06d01d |
| Docs | CLEAN (S3 suggestion) | docs/README §3 margin text; 09 §7 `:124` against the executable cases; 02 F02.4/F02.7 captions; the PR body's round-3 claims (parent, 7 files, 25→30 cases, 556 files, counts) and its R1 wording; visual and bounds inspection of the renders | R472-4 | 5123548eb4de35f24d43eb088c12dab70b06d01d |

## Real limits

- I did not run the full processor suite set, Yosys, gen_matrix outside `make check`, the parent consumer set, gPTP, builder, synthesis, hardware, or local workflow emulation.
- The manager's statement that the source static/builder and native banks passed at this head is recorded as supplied. It is not reviewer execution. The linked public evidence tree at `4a3ae4a1` holds only round-1 author material at `91cef52` (handoff, body, four adoption patches). It contains no exact-head manager bank receipts, and no non-reviewer comment on #27 or #156 links any.
- The font check covers only the two installed font families, in one headless browser plus one standalone rasterizer.
- Physical calibration was **NOT RUN**. Field skips and simulation are not hardware proof.

## Integrity

The review clone is at HEAD `5123548eb4de35f24d43eb088c12dab70b06d01d` with tree and index tree `33b4fe59951370299cad36ec1415ead003524d5f`. All 556 tracked blobs (539 regular, 17 executable) match by bytes and mode, the index entries equal the HEAD tree, and status (including ignored files) is empty after I removed my build outputs. The repository has zero gitlinks and no `.gitmodules`, so there are no submodules to restore. All probes and mutations ran on copies under the packet's `scratch/`, which is not published. I made no source edit, commit, push, GitHub write, merge or author contact, and used no sub-agent.

## Pending manager duties

1. Publish or link the exact-head manager source static/builder/native receipts, with identities and exclusions.
2. Record the final hosted result. The suites jobs of runs 37281818928 and 37281823263 were still in progress at this review. Own hosted/act acceptance and distinguish executed jobs from skipped contexts.
3. At the merge turn, build and validate the final current-dev candidate: source base `c050d97153dd0480ae741102c1647eeda9b7f273`, live dev `fa450d301805881ad713b67521477bf042ddadfd`, the four adoption patches and the approved processor pin. Source validation does not replace it.
4. Carry the optional suggestions: S1 to S3 from this round, the dependency lockfile, and the integrator short names. Merge still needs two independent positive reviews. #71 closes only when both of its lanes are merged.

R472-4 FINISHED
