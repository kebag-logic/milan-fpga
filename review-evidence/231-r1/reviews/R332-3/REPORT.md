[R332] NEGATIVE - exact head 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4

Round R332-3 is an internal, cleared-context review of PR #572 for issue #231 (parent epic #229). It is a delta round.

- Head: `0a506fa8f0032d21e9614a617b75b0a57dc5f2e4`, tree `925498fa6e15c7fc53705810a42cff4278b0b336`.
- The delta judged is `af6d19c5..0a506fa8`: one commit, 11 files, no `hdl/` and no gitlink change.
- The full base is `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.

All five lenses were applied.

**Verdict: NEGATIVE, on two MINOR findings.**
- F1 leaves Tests and Conformance unclean.
- F2 leaves Conformance and Docs unclean.
- RTL and Robustness are clean.

**The core of this round holds up.** The KEEP_HIERARCHY attribution run really does preserve the protocol-wrapper boundary. I re-ran it myself at both shapes, and every attribution figure and boundary-probe count I reproduced matches the page to the digit. The complete rankings, the standalone 1x1 figures, the flattened Yosys figures and the hierarchical Yosys reconciliation at 1x1 also reproduce exactly.

All six prior MINOR/MAJOR findings are closed in the tree:
- R333-1: F1, F2, F3 and F4;
- R332-1: F1, F2 and F3.

Two gaps remain:
- **F1:** one enforcement line the page claims, the ambiguous-image refusal, still survives removal under the self-test.
- **F2:** the epic's baseline reference on #229 still publishes the unqualified default-flow wrapper and AECP figures that R333-1 F1 required to be qualified.

## Reconstruction

**Authorities read:**
- AGENTS.md, CONTRIBUTING.md and docs/README.md;
- the issue #231 body and its frozen acceptance criteria;
- the scope decision 5844867171;
- the round-two assignment and decision 5846064333;
- the historical provenance comments 5393881955, 5394395001, 5410760834 and 5411378865;
- the round-one [A328] REVIEW READY and the round-two [A337] REVIEW READY (5846494955);
- the PR #572 body at this head;
- the epic #229 baseline reference 5845524962.

**Public evidence:** the tree at `bc7fdb29.../review-evidence/231-r1`, which holds the `author-r2` summaries, rankings and mapping (byte-identical to the committed TSVs), and the round-one reports. The recipe-cited probe scripts come from `e21bc530.../review-evidence/231-r1/reviews/R333-1/probe_boundary`. They are byte-identical to the copies used here, sha256 `45debf29...` and `a1a9097c...`.

**Order of reading:** the prior review findings (R332-1, 5846062021; R333-1, 5846062510) were read only after my independent pass over the diff and after my own reproductions. The concurrent same-head R333-2 report was not read.

## What was reproduced (clean copy of the exact head, recipe as committed)

**Setup:**
- a disposable copy of the head with its three pinned submodules;
- the SDK installed fresh from the pinned archive and verified (`scripts/ci_rv32_sdk.py`, sha256 `d42680e9...`);
- the host's LiteX environment, used read-only;
- Vivado 2026.1 and Yosys 0.66 (`86f2ddebc-dirty`).

**Recipe:**
- The export followed the recipe's Prerequisites and Export steps verbatim (`scripts/export.sh`).
- Attribution scripts came from `pp_baseline.py <gateware> --synthesis-only --attribution-only`, unmodified, with 32 threads.
- The 1x1 attribution route was not rerun.

**Result:** every run returned rc 0. The only `Synth 8-4445` text in any Vivado log is the echoed promotion command (`receipts/reproduced/*/synth-8-4445-grep.txt`).

| Measurement | Reproduced | Page / committed |
|---|---|---|
| Export images, 6 per shape | all 12 sha256 values found in `PP_SHADOW_BASELINE_INPUTS.json` (`receipts/images-vs-inputs-json.txt`) | identical |
| Source reads | 118 `read_verilog` per shape | "118-source exports" |
| Attribution constraint | generated `baseline_boundary.xdc` = `set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath/pp_shadow]`, read before `synth_design` and parsed at both XDC passes | as documented (recipe :186) |
| Wrapper cell property in the synthesized checkpoint, 1x1 and 8x8 | `KEEP_HIERARCHY TRUE`, `ORIG_REF_NAME KL_pp_shadow` (`receipts/reproduced/probes/keep_*_attr_synth.txt`) | as claimed |
| Attribution 1x1 synthesis, whole / wrapper | 52,210 LUT; wrapper 22,314 LUT / 24,535 FF / 21 / 3 / 5 DSP; wrapper internal WNS -1.201 | 52,210; 22,314 / 24,535 / 21 / 3 / 5 / -1.201 (page :85, :191) |
| Attribution 8x8 synthesis, whole / wrapper | 70,206 LUT; wrapper 29,489 / 32,991 / 26 / 5 / 8 DSP; WNS -10.846 | identical (page :87, :193) |
| Attribution 8x8 child rows | `u_pp` 28,277; `u_aecp` 5,025; `u_srp` 8,382; `u_notify` 2,895; `u_listener` 1,655; `u_talker` 1,350; `u_nvm` 1,131 LUT / 4 DSP; `u_dyn` 574; scoped WNS all equal | identical (page :150-160) |
| Rankings, `attribution-synth-1x1` and `-8x8` | `pp_baseline_rank.py` on my reports: 40 rows each, byte-identical to the committed TSV rows (`receipts/rank-attribution-synth-*.tsv`) | identical |
| Rankings, default and OOC endpoints | each of 31 rows present in the round-one public (filtered) reports equals the committed row, for all 5 endpoints. The 8 rows per endpoint absent from the filtered reports are small instances (at most 44 LUT) (`receipts/rank-crosscheck-r1-reports.txt`) | consistent |
| Boundary probe, 1x1 attribution synthesis | `u_dyn` 144/0/0; `u_aecp` 5,269/18/0; `u_srp` 4,947/96/96; `u_notify` 3,361/0/0; wrapper 24,983/173/131 | identical (page :200-204) |
| Boundary probe, 8x8 attribution synthesis | `u_dyn` 607/0/0; `u_aecp` 5,607/18/0; `u_srp` 9,480/442/432; `u_notify` 3,027/0/0; wrapper 32,833/519/467 | identical (page :205-209) |
| `u_dyn` load histograms, 1x1 and 8x8 attribution | empty (0 rows) | "empty at both synthesis shapes" |
| Vivado OOC 1x1 | 22,350 / 24,533; scoped WNS equal; census sha256 `edfd86ab...`; raw LUT1-6 24,941; CARRY4 1,415 | identical |
| Yosys flattened 1x1 | 41,258 / 5,972 / 47,230 / 23,041 / 15 / 4 / 5 / 1,813 | identical |
| Yosys hierarchical 1x1 (the recipe's block, 1x1 only) and `pp_baseline_mapping.py` | all 38 rows plus residual and total byte-identical to the committed 1x1 rows. The Yosys design-hierarchy LUT1-6 sum is 48,915; the residual is -7,657; the gap is 16,317 (`receipts/mapping-1x1-reproduced.tsv`, `receipts/reproduced/yosys-1x1/`) | identical |
| Mapping arithmetic, both shapes | the three named scopes plus the remainder, the residual and the flat total balance exactly: 16,317 and 33,374 (`receipts/mapping-arith.txt`) | identical |

**Where the remaining external-load LUTs go.** I ran the unchanged `loads.tcl` on the wrapper and `u_srp` scopes (`receipts/reproduced/probes/loads_*`). They feed:
- the datapath's `gsi_data_r` answer mux (442 at 8x8);
- `csr/live_mux_q`;
- `csr/snap_shadow_r`;
- a few CDC gray counters and LiteX `storage_*` registers.

These are the wrapper's exported read and status faces. `hdl/milan/KL_pp_shadow.sv:385-406` describes the gather face as answered by `milan_datapath` from processor-side selectors. The wrapper cell carries KEEP_HIERARCHY TRUE, so none of these LUTs can be relocated datapath logic. The residual is wrapper-sourced output-cone logic.

## Prior findings: resolution at this head

| Prior finding | Status | Evidence |
|---|---|---|
| R333-1 F1 MAJOR: integrated hierarchical rows counted datapath logic as wrapper, AECP and `u_dyn` | **Closed in the tree and in the PR body.** The #229 epic residue is filed as new F2 | Attribution run reproduced with KEEP_HIERARCHY TRUE confirmed on the cell. The probe shows zero `u_dyn`/`u_aecp` "outside input and only outside loads" and empty `u_dyn` load histograms at both shapes. Default totals are unchanged at page :69-73. The difference is stated at page :180-193, and the default rows are relabelled "rebuilt wrapper-name" (:232-239). The PR body carries the qualification. |
| R333-1 F2 MINOR: Yosys and Vivado logic-mapping difference not explained | **Closed** | Assignment item 3 accepts "an equivalent-geometry run that is not flattened". My hierarchical run reproduces the committed reconciliation byte-for-byte. The page names the dominant scopes, keeps the flattening residual global and unassigned, and records the INV/IBUF/OBUF/MUXF counts as excluded (:314-360). |
| R333-1 F3 MINOR: a-priori subset of consumers | **Closed** | `PP_SHADOW_BASELINE_RANKING.tsv`: 8 endpoints x 33 `u_pp` children plus 3 wrapper children, own-logic rows and reconciliation. The threshold is zero (page :108-118). The timing tables are labelled subsets (:120). The timer growth of +758 is now stated (:220). Verified above. |
| R333-1 F4 MINOR: self-test does not guard enforcement points | **Closed** | `pp_baseline_mutants.py` kills all four named mutants: ROM promotion, readmemh equality, parameter-ROM depth and image depth, and the outside-repository guard (`receipts/gate-pp_baseline_mutants.log`). CI wiring is at `.github/workflows/rtl-fast.yml:209-211` and `scripts/ci_events.py:2325-2327`. `ci_events --check` passes, and hosted `rtl-fast` succeeded at this head. |
| R332-1 F1 MINOR: `check_doc_paths` failed on a clean checkout | **Closed** | `git archive` export of the head plus `git init`, with `sw/builder/out` absent: rc 0, "848 cited paths all resolve" (`receipts/doc-paths-git-archive.txt`). The recipe now cites `sw/builder/out/` (:44). |
| R332-1 F2 MINOR: hierarchy tables were a fixed subset | **Closed** | Same evidence as R333-1 F3. `u_timer`, `u_dispatch`, `u_originator`, `u_nvm_shadow` and the own-logic rows are all ranked. |
| R332-1 F3 MINOR: self-test could not detect removal of the #246 guard | **Closed** | `export_selftest` drives `inventory()`, `prepare()` and `main()` on a synthetic export. My own mutants also kill ROM_ERROR severity text, ROM_ERROR placed after `synth_design`, KEEP_HIERARCHY on the wrong cell, and a weakened hex check (`receipts/extra-mutants.tsv`). |
| R332-1 S1 (mixed-shape log), S2 (automated rehash) | Unchanged; remain suggestions | |
| R332-1 S3 (unexplained integrated `u_dyn` growth) | **Answered** by the attribution run: 6,915 falls to 574 at 8x8 | |
| R333-1 S1 (rehash command), S2 (executed-script provenance) | S1 unchanged. S2 is addressed in author-r2 evidence by `input-validation-final.json`, which is referenced but not public | |

## Findings

### F1 - MINOR - Tests, Conformance - `syn/ooc/pp_baseline.py:174-175` (and `:143-144`); claim at `docs/findings/PP_SHADOW_BASELINE.md:280`; mutant list at `syn/ooc/pp_baseline_mutants.py:12-38` - A claimed ambiguous-input refusal still survives removal under the self-test

**Authority:**
- Assignment 5846064333, item 4: "`syn/ooc/pp_baseline.py`'s self-test must fail when the #246 ROM guard, or any other enforcement line it claims, is removed. Add a mutant for each."
- AGENTS.md section 6, Tests lens: each test "can fail for the defect it claims to detect".
- The page claims the helper "rejects missing, short, malformed and ambiguous inputs before synthesis" (:280).

**Evidence:**
- The only image-ambiguity enforcement is `if len(matches) != 1 or len(packages) != 1: raise ValueError("ambiguous image or geometry source")` (:174-175). Its geometry counterpart is the uniqueness check in `package_number` (:143-144).
- With either line replaced by `if False:`, `pp_baseline.py --selftest` still exits 0. The unchanged control also passes (`scripts/extra_mutants.py`, `receipts/extra-mutants.tsv`).
- Neither removal is in the maintained ten-mutant list.
- I ran a functional probe (`scripts/ambiguity_probe.py`, `receipts/ambiguity-probe.tsv`) on a synthetic export that binds `PP_UCODE_HEX_P` twice, the second time to a one-word image:
  - the pristine helper refuses it;
  - with the guard removed, the helper accepts it, and the partial image is never inventoried, hashed or geometry-checked.

**Impact:**
- A later edit can delete this guard with the self-test and fast CI green.
- An export with a second, partial microcode binding would then be measured with no refusal. That is the #246 failure class: a file that exists but is incomplete raises no `Synth 8-4445`.
- The round-two answer to "a mutant for each" claimed enforcement line is therefore incomplete.

**Required outcome:** the self-test refuses a synthetic export whose image parameter or geometry package is ambiguous. The ambiguous cases are a duplicated `.<PARAM>("...")` binding, a missing binding, or a duplicated or missing package, and a duplicated geometry declaration. The maintained mutant driver includes the removal of each of these guards and requires it to fail.

**Verification:** run `scripts/extra_mutants.py <head>/syn/ooc/pp_baseline.py`, expecting "killed" for the first two rows and control-pass. Also run `python3 syn/ooc/pp_baseline_mutants.py` at the fixed head.

### F2 - MINOR - Conformance, Docs - issue #229 comment 5845524962 (the epic's "BASELINE REFERENCE -- #231") - The epic reference still publishes the default-flow wrapper and AECP figures as the wrapper's consumption

**Authority:**
- The #231 acceptance criterion: "The baseline is linked from #229 and becomes the reference for the remaining optimization tickets".
- R333-1 F1's required outcome: "The PR and issue summaries must carry the same qualification".
- Decision 5846064333: the default-flow names are relabelled and the attribution rows answer ownership.

**Evidence:**
- The only #231 reference on #229 (read at review time) still lists "Vivado shipping 1x1 route, wrapper 22,441" and "Vivado integrated 8x8 synthesis, wrapper 37,809". It still states "integrated 8x8 AECP is 15,199 LUTs" and "The baseline records complete hierarchy resources".
- It carries no attribution qualification.
- Its links pin the superseded page at `af6d19c5`.
- At this head, the page says those rows "describe reconstructed names, not source ownership" (:117-118, :238-239). The reproduced attribution values are 20,655, 29,489 and 5,025.
- The PR body was corrected; the epic reference was not.

**Impact:** the epic's reference, which the remaining #229 tickets read, still points optimization at roughly 10,000 AECP LUTs at 8x8 that the attribution run shows are not AECP logic. This is the exact failure R333-1 F1 was raised for.

**Required outcome:** the #229 reference identifies the default-flow wrapper and AECP rows as rebuilt-hierarchy names, not ownership. It gives the attribution-only figures, or points to them, and links the page at the merged head rather than `af6d19c5`. Editing, superseding or following up the comment are all acceptable.

**Verification:** read the #229 reference comments at the merge turn. No unqualified default-flow wrapper or AECP figure may remain presented as ownership, and the links must resolve to the merged page.

### Suggestions (do not affect coverage)

**S1 - SUGGESTION - Robustness.** Locations: `syn/ooc/pp_baseline.py:193-198`, and line 5 of the generated integrated script. Nothing asserts that the attribution constraint took effect:
- The exported LiteX script demotes `Common 17-55` (set_property with no objects) to a Warning.
- So if `milan_datapath/pp_shadow` were ever renamed, the attribution run would silently produce default-flow attribution under an "attribution-only" label.

Today the property is TRUE at both shapes (`receipts/reproduced/probes/keep_*`). Consider appending a post-synthesis check to the attribution script that errors unless `get_property KEEP_HIERARCHY [get_cells milan_datapath/pp_shadow]` is TRUE.

**S2 - SUGGESTION - Docs.** Location: `docs/findings/PP_SHADOW_BASELINE.md:207, :217`, against recipe :216 ("Report the measured residual, including its named load stems"). The page does not name two things that the stems I measured explain:
- the attribution residual's load stems;
- the SRP external-only increase from 74 to 442 at 8x8.

The stems I measured are the `gsi_data_r` answer mux, `csr/live_mux_q`, `snap_shadow_r` and CDC counters, and the increase is consistent with the unmeasured reverse relocation under the default flow. One sentence would stop a reader treating the SRP increase as a defect of the attribution run.

**S3 - SUGGESTION - Tests.** Removing several further guards also leaves the self-test green. The page does not explicitly claim these as refusals, which is why they are not in F1 (`receipts/extra-mutants.tsv`):
- wrapper-declaration equality (:133);
- the empty parameter block (:100);
- the integrated-output-directory guard (:191);
- attribution-requires-integrated (:194);
- CLI endpoint exclusivity (:406);
- single `synth_design` (:224);
- the image pathname character guard (:219).

Consider arms for the ones intended as enforcement.

## Clean lenses

- `[R332] PASS RTL - git diff --stat 7eb3b0d4..0a506fa8 (no hdl/, no gitlink); generated baseline_integrated.tcl and baseline_boundary.xdc at both shapes; reopened attribution checkpoints (KEEP_HIERARCHY TRUE on milan_datapath/pp_shadow); hdl/milan/KL_pp_shadow.sv:385-406 - I checked the following:`
  - The attribution variant changes only the added XDC. Source reads are 118/118 in the same order, and the part, directive and clocks are unchanged.
  - The boundary is preserved on the synthesized cell at both shapes.
  - The attribution DSP change is located in `u_nvm` (1 to 4, wrapper 5 to 8), as stated.
  - Scoped-timing semantics are unchanged. The remaining boundary-crossing LUTs are wrapper output-cone logic by construction of the preserved boundary.
  - No module or interface contract is touched.
- `[R332] PASS Robustness - syn/ooc/pp_baseline.py:185-236,384-409; receipts/extra-mutants.tsv; receipts/ambiguity-probe.tsv; receipts/clone-state-before.txt vs clone-state-after.txt - I checked the following:`
  - Attribution is refused with `--integrated-log`, both in the CLI and in `prepare`.
  - The integrated output must equal the gateware directory.
  - Output inside the repository is refused.
  - The pristine helper refuses duplicated image bindings.
  - A stale `baseline_boundary.xdc` is never read by a default script.
  - The review clone is byte-identical before and after all probes: HEAD, index hash, status and the three gitlinks.
  - Only S1 remains, and it is a suggestion.

## Lens coverage for the unclean lenses

- **Conformance.** Applied to each #231 acceptance criterion and to decisions 5844867171 and 5846064333, items 1-5:
  - Both OOC configurations are reproducible from a clean checkout: 1x1 was re-run exactly this round, and 8x8 in R332-1.
  - Dominant consumers are identified by hierarchy: complete rankings, reproduced.
  - Standalone, integrated, Vivado and Yosys figures are distinguished, and attribution is labelled separately.
  - Default totals are unchanged and the difference is stated.
  - The mapping explanation is evidence-backed and was reproduced at 1x1.
  - The measurement is measurement-only (no RTL).
  - Open: F1 (assignment item 4, incomplete) and F2 (the #229 reference).
- **Tests.** Applied by mutation:
  - The ten maintained mutants are killed and the control passes.
  - 15 extra reviewer mutants give F1 and S3.
  - `pp_baseline_reports_selftest.py` passes.
  - The focused gates at the head all pass (`receipts/gates-rc.txt`): `pp_baseline --selftest`, mutants, report self-test, doc paths (also on a `git archive` export), doc style, TOC check and anchors, em-dash against the base, py-idiom, `docs_check`, and `ci_events --check`.
  - The TOC, anchor, em-dash and `docs_check` gates were rerun in a scratch virtual environment with the pinned renderer from `tools/markdown/requirements.txt`. The system interpreter lacks html5lib (rc 2, environment only).
  - Hosted exact-head contexts: 21 succeeded, and `Physical gPTP` was skipped. That skip is not hardware evidence (`receipts/hosted-checks.tsv`).
- **Docs.** Applied to the page, recipe, ranking TSV, mapping TSV, PR body and #229 reference:
  - Every attribution, probe, ranking and 1x1 mapping number on the page was checked against my reproductions.
  - The recipe's evidence link `e21bc530` resolves, and its probes are byte-identical.
  - Open: F2. Suggestion: S2.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #231 AC; decisions 5844867171 and 5846064333; PP_SHADOW_BASELINE.md; RANKING/MAPPING TSVs; reproduced attribution 1x1/8x8, OOC 1x1, Yosys flat and hierarchical 1x1; #229 comment 5845524962 | R332-3 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |
| RTL | CLEAN | diff stat; generated attribution Tcl/XDC; KEEP_HIERARCHY property on both checkpoints; `KL_pp_shadow.sv:385-406`; DSP and scoped-timing rows | R332-3 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |
| Robustness | CLEAN | `pp_baseline.py:185-236,384-409`; extra-mutant and ambiguity probes; clone before/after state | R332-3 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |
| Tests | UNCLEAN (F1) | `pp_baseline.py` self-test under 10 maintained plus 15 reviewer mutants; `pp_baseline_reports_selftest.py`; focused gates; hosted check runs | R332-3 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |
| Docs | UNCLEAN (F2) | PP_SHADOW_BASELINE.md, PP_SHADOW_BASELINE_RECIPE.md, the TSVs, PR body, #229 reference; doc gates, including the `git archive` path gate | R332-3 | 0a506fa8f0032d21e9614a617b75b0a57dc5f2e4 |

## Real limits

- **Not rerun this round:**
  - the 1x1 attribution place-and-route (20,655 LUT, +0.041/+0.015 ns) and its boundary probe;
  - the default-flow runs;
  - the placement sweep;
  - the 8x8 standalone and 8x8 Yosys runs, flattened and hierarchical.

  The default and OOC rankings were checked against the round-one public reports only for rows present there. The 8x8 mapping rows were checked for arithmetic, not re-derived.
- The author-r2 raw reports and checkpoints are not public; only summaries are. My conclusions rest on my own reproductions.
- The LiteX environment is the host's existing one, used read-only. Its patch series was not re-derived. Yosys is the unpinned host package, as the page states.
- The boundary probe classifies by cell location. It does not measure reverse relocation (wrapper logic moved into the datapath).
- **No banks, candidate build, act or hardware:**
  - No full parent, processor, gPTP, Yosys or builder bank was run.
  - No act or hardware run was made.
  - This is not the current-dev candidate build.
  - Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Answer F1 and F2, then re-review the corrected head. This round does not approve later fixes. A pp_baseline change re-opens Tests and Robustness, and an edit to the #229 reference re-opens Conformance and Docs.
- Build and validate the candidate merge result against live `dev` (`462b714f...`; the source base is `7eb3b0d4`) at the merge turn.
- Complete act and hosted acceptance on the final head.
- Assemble the completion ledger with the external review.
- Merge only with maintainer authorization, then run post-merge containment.

Receipts and portable scripts are listed in `MANIFEST.sha256`. Host paths in receipts are written as `$PACKET`, `$REVIEW_CLONE` and `$HOME`.

R332-3 FINISHED
