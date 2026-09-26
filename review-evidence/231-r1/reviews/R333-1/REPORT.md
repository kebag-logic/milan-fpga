[R333] NEGATIVE - exact head af6d19c553ad8c445a80528344baf2273b41ad46

# R333-1 external review: issue #231 / PR #572

Reviewer: [R333], external independent reviewer, round R333-1.
Head `af6d19c553ad8c445a80528344baf2273b41ad46`, tree `abdc83b490114b217f40951173d637cbe2ba7dcf`.
Base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`. Diff: 5 files, +1,086, no RTL, no gitlink change.

Context reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #231 body and its
comments (assignment decision 5844867171, takeover 5844892720, review-ready 5845532313, the
historical measurement comments 5393881955 / 5394395001 / 5410760834 / 5411378865), PR #572 body,
the diff, and the public evidence packet `review-evidence/231-r1` at `63cd047a`. The verdict and
ledger below were written before any other review of this PR was read.

## Verdict

NEGATIVE. The standalone and integrated synthesis figures reproduce exactly from a clean
checkout, the ROM trap is enforced, and the parameters, part and constraint match the integrated
build. But the integrated hierarchical attribution, which is the page's answer on the 8x8 fit
question, counts datapath logic as protocol-wrapper logic (F1, MAJOR). Three MINOR findings
remain open: the Yosys explanation, the dominant-consumer selection and self-test coverage.

## What was reproduced (clean checkout, exact head)

Disposable clean clone at the exact head with the three public submodules at their gitlinks,
the LiteX patch series verified applied, the SDK installed from the pinned archive and verified,
and the recipe followed. The only deviations were 8 threads instead of 32, and the integrated
1x1 run stopping at synthesis (no placement or route). Receipts are under `receipts/`.

| Measurement | Page | Reproduced | Match |
|---|---|---|---|
| Firmware and ROM images, 10 files, both shapes | `PP_SHADOW_BASELINE_INPUTS.json` sha256 | `receipts/image_sha256.txt` | all 10 identical |
| Vivado OOC 1x1: LUT / FF / RAMB36 / RAMB18 / DSP / CARRY4 / WNS | 22,350 / 24,533 / 21 / 3 / 5 / 1,415 / -6.180 | same | exact |
| OOC 1x1 raw LUT1-6 census / LUT as logic | 24,941 / 21,148 | 24,941 / 21,148 | exact; `baseline_cells.tsv` sha256 `edfd86ab...` equals the author's omitted file |
| OOC 1x1 hierarchy and scoped timing | packet `ax7101-ooc` | `receipts/ax7101-ooc` | identical apart from date/host |
| Vivado OOC 8x8: LUT / FF / RAMB36 / RAMB18 / DSP / CARRY4 / WNS | 28,992 / 32,984 / 26 / 5 / 5 / 1,775 / -10.987 | same | exact; hierarchy and scoped timing identical to packet `ax8x8-ooc`; `baseline_cells.tsv` sha256 `17f32ee5...` equals the author's omitted file |
| OOC 1x1 worst path | `u_notify/pend_r_reg[4]/C` to `u_tx_arbiter/slot_r_reg[0]/D` | same | exact |
| Integrated 1x1 synthesis, whole / wrapper | 51,125 / 23,272 LUT, WNS -1.201 | same, CARRY4 3,214 / 1,364 | exact; hierarchy identical to packet `ax7101-synth-reports` |
| Integrated 8x8 synthesis, whole / wrapper | 68,136 / 37,809 LUT, WNS -11.331 / -10.594 | same, CARRY4 3,916 / 1,803 | exact; hierarchy identical to packet `ax8x8-synth-reports` |
| Yosys 1x1 `ooc.sh KL_pp_shadow` | 41,258 / 5,972 / 47,230 / 23,041 / 15 / 4 / 5 / 1,813 | same | exact |
| Wrapper parameters, both shapes | manifest | `baseline_parameters.json` from the integrated logs | all 20 equal (paths differ by root only) |
| `Synth 8-4445` diagnostics | zero | zero in all four Vivado logs (the only hit is the echoed `set_msg_config`) | yes |
| `12-4739`, `12-5201`, `20-1307` warnings | retained | 10 / 2 / 2 in the integrated 1x1 log | yes |

Both Vivado OOC configurations the acceptance criterion names therefore reproduce from a clean
checkout.

Configuration checks, independently established:

- The standalone script keeps the exported `create_project -part xc7a100t-fgg484-2`, the full
  118-file source list and include directories, and the `AreaOptimized_high` synthesis command.
  It changes only `-top`, adds `-mode out_of_context` and the 20 generics, and reads a 10 ns
  `clk_i` constraint before `synth_design`. `KL_pp_shadow` has exactly one clock input
  (`hdl/milan/KL_pp_shadow.sv:245`). Neither the wrapper nor any protocol-processor source has a
  `` `ifdef `` or `` `include ``, so defines cannot make the standalone build diverge.
- The 8x8 integrated elaboration used the 8x8 shape header even though the tracked header is the
  1x1 one. The integrated 8x8 log binds `N_STREAM_IN_P = 9`, which comes from
  `ADP_LISTENER_SINK_C = 9` through `milan_datapath.sv:1583`. The tracked 1x1 header would give 2.
- Every `$readmem` site in the integrated source set is inventoried by the helper: the three
  parameter-bound ROMs (`KL_pp_acmp_listener.sv:417`, `KL_aecp_ucpu.sv:121`,
  `KL_gptp_ucpu.sv:107`) and the three LiteX init files.
- The `Synth 8-4445` rule is enforced, not only reported (probe `probe_8_4445/`). On a design
  with a missing `$readmemh` file, Vivado 2026.1 finishes at rc 0 behind a CRITICAL WARNING
  without the helper's promotion (control arm). With the promotion, `synth_design` fails at rc 1
  (promoted arm).

## Findings

### F1 - MAJOR - Conformance, RTL, Docs

Location: `docs/findings/PP_SHADOW_BASELINE.md:69-74`, `:124-134`, `:136-146`, `:154-160`, and the
PR body's "22,441 in the protocol wrapper".

Title: the integrated hierarchical rows count datapath logic as wrapper and AECP logic.

Evidence: a netlist probe (`probe_boundary/boundary.tcl`) classifies every LUT cell under a
scope by where its drivers and loads sit relative to `milan_datapath/pp_shadow`. It ran on the
integrated synthesis checkpoints this review reproduced; their hierarchy reports are identical to
the published ones.

| Scope, integrated synthesis | LUT cells | Loads only outside the wrapper | Datapath inputs and loads only outside |
|---|---:|---:|---:|
| 1x1 `u_pp/u_aecp/u_dyn` | 1,624 | 763 | 476 |
| 1x1 whole wrapper | 26,213 | 1,175 | 792 |
| 8x8 `u_pp/u_aecp/u_dyn` | 8,817 | 5,922 | 3,108 |
| 8x8 `u_pp/u_aecp` | 17,872 | 6,187 | 3,357 |
| 8x8 whole wrapper | 42,962 | 6,397 | 3,499 |

The standalone `u_dyn` has 111 LUTs at 1x1 and 574 at 8x8. At 8x8, the `u_dyn` LUTs with no load
inside the wrapper feed datapath state: `amap_out_owner_r`, `amap_out_cluster_r` and
`amap_edit_oclaim_{word,expect,cluster}_r` (`probe_boundary/loads_8x8_udyn.tsv`). These registers
are declared at `hdl/milan/milan_datapath.sv:1205-1206` and `:4005-4007`, sized
`N_STREAMS*8*{13,16}`. Under the default rebuilt hierarchy, Vivado moved the datapath's
audio-map next-state logic into `u_dyn`.

The page states "The 8x8 integrated AECP engine occupies 15,199 LUTs" and "Within that engine,
`u_dyn` changes from 574 to 6,915 LUTs". It attributes the difference only to "different
synthesis contexts", and its tables present these rows as the wrapper's consumers. The
assignment decision (issue 231 comment 5844867171) defines the integrated baseline as "the
placed-and-routed hierarchy of `KL_pp_shadow`". The acceptance criterion requires the report to
"identify the dominant resource consumers by hierarchy".

Impact: at the shape that does not fit (8x8 over capacity by 4,736 LUTs), the largest integrated
consumer points the epic's optimization tickets at the AECP dynamic-state block. Several thousand
of those LUTs belong to the datapath's audio-map logic, which grows with the stream count. The
integrated wrapper totals (22,441 routed 1x1; 37,809 8x8) are overstated by up to the
datapath-only-load population. The reverse leakage (wrapper logic moved into the datapath) is
not measured either.

Required outcome: the integrated hierarchical figures published as wrapper, AECP and `u_dyn`
consumption must be one of the following:

- measured with the wrapper boundary preserved, for example an attribution-only integrated
  synthesis variant that keeps the `pp_shadow` hierarchy; or
- published with the relocated datapath share quantified, with the 8x8 dominant-consumer
  statement corrected to say which logic actually grows.

The PR and issue summaries must carry the same qualification.

Verification: rerun `probe_boundary/boundary.tcl` and `loads.tcl` on the checkpoint behind each
published integrated row. Either the datapath-only-load population inside the wrapper is near
zero, or the page reports it and no longer attributes it to the AECP engine.

### F2 - MINOR - Conformance, Docs

Location: `docs/findings/PP_SHADOW_BASELINE.md:237-247`.

Title: the dominant Yosys-versus-Vivado mapping difference is reconciled but not explained.

Evidence: the scope of issue #231, restated in assignment decision item 3, is "Yosys with
equivalent geometry. Explain the significant mapping differences." The page's own reconciliation
leaves the largest term unexplained. It lists "Difference between raw logic-cell mappings" as
16,317 of 24,880 LUTs at 1x1 (65.6 %) and 33,374 of 42,868 at 8x8 (77.9 %). It then states that
"This measurement does not isolate each optimizer transformation behind it." The concrete
explanations given cover only memory, BRAM and DSP mapping. The reproduced Yosys netlist also
carries unmentioned artifacts (`receipts/ax7101-yosys/final_stat_block.txt`): 14,204 `INV` cells,
13,108 of them inverting the active-low reset into `FDRE` R pins; 1,283 `IBUF` and 2,174 `OBUF`;
and 473 `MUXF7`/`MUXF8`. None of these is in the LUT columns, but they show the Yosys mapping is
not structurally comparable without explanation.

Impact: `syn/yosys/ooc.sh` describes its number as "the only number an area lever may be judged
on". A roughly 2x logic-LUT disagreement at 1x1, and roughly 2.3x at 8x8, left unexplained means
the remaining #229 tickets cannot tell which instrument to trust for a lever.

Required outcome: explain the significant logic-mapping difference with evidence, for example by
hierarchy using a non-flattened or per-module equivalent-geometry Yosys run, or by naming the
transformations responsible. Alternatively, record a public scope decision that narrows this
item.

Verification: the page names where the raw logic difference arises, with numbers that sum to the
reconciled term, or it links the recorded decision.

### F3 - MINOR - Conformance, Docs

Location: `docs/findings/PP_SHADOW_BASELINE.md:100-146`. The row set comes from the fixed list at
`syn/ooc/pp_baseline.py:51`.

Title: the "Hierarchical consumers" tables are an a-priori subset, not the dominant consumers.

Evidence: the published hierarchy reports show that the tables omit children larger than rows
they include.

- 8x8 standalone: `u_timer` 1,452 LUT and `u_rx_validator` 861 are unlisted. Listed rows include
  `u_talker` 1,354 and `u_nvm` 745.
- 8x8 integrated: `u_timer` 1,460 and `u_rx_validator` 858 are unlisted. Listed rows include
  `u_talker` 848 and `u_nvm` 635.
- 1x1 standalone: `u_dispatch` 879 is unlisted while `u_talker` 860 is listed; `u_rx_validator`
  510 is unlisted while `u_nvm` 507 is listed.
- In FFs, the processor's own logic `(u_pp)` holds 3,242 at 1x1 and 4,700 at 8x8 standalone
  (4,643 integrated), more than every listed row except `u_srp`. It appears nowhere.

The acceptance criterion is "Reports identify the dominant resource consumers by hierarchy".

Impact: readers take the six rows as the ranking and miss consumers larger than some listed
ones. At 8x8, `u_timer` (about 1.45k LUT, roughly 2x its 1x1 size) is invisible.

Required outcome: rank the direct children of `u_pp` (and the wrapper) by measured LUT and FF
above a stated threshold, including own-logic rows. Or label the tables as a timing-scope subset
and publish the complete ranking beside them.

Verification: every child whose LUT or FF count exceeds the smallest listed row appears in the
tables, or the page states the threshold and the omission.

### F4 - MINOR - Tests

Location: `syn/ooc/pp_baseline.py:231-277`, guarding `:18`/`:188`, `:161-163`, `:178-179` and
`:297-299`.

Title: the helper's self-test does not guard the enforcement points it exists for.

Evidence: the mutation probe `probe_selftest/mutate.py` (results in `mutation_results.txt`)
applies single mutations to a copy of the helper. Four mutants still pass `--selftest`:

- removing the `Synth 8-4445` promotion from the generated scripts;
- disabling the `$readmemh` inventory equality;
- skipping the depth check on parameter-bound ROMs;
- disabling the outside-repository guard.

The control mutant, which removes the width check, is killed, so the probe discriminates. The
self-test never calls `prepare()` or `inventory()`. No workflow or gate runs
`pp_baseline.py --selftest`: its only references in the repository are in the recipe.

Impact: the #246 guard is effective today (confirmed by the Vivado probe), but a later edit can
remove it with the self-test green. The recipe's "zero `Synth 8-4445`" claim then rests on a
manual log check.

Required outcome: add self-test arms on a synthetic gateware tree that fail if either generated
script lacks the promotion before `synth_design`. They must also require a refusal on a
`$readmemh` set mismatch, a short parameter-bound ROM, and an in-repository output directory.
Consider running the self-test in the same CI step as the repository's other self-tests.

Verification: each of the four mutants above makes `--selftest` fail.

### Suggestions (do not affect coverage)

- S1 (Robustness, Docs). `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:262` says "Rehash
  `baseline_images.json` inputs after each run" but gives no command. Images are validated at
  preparation time and could change before Vivado opens them. A `--verify <json>` mode, or a
  printed command, would make the post-run check reproducible.
- S2 (Docs). The published integrated run directories hold `baseline_pp_cells.tsv`, which the
  committed helper does not emit. The integrated runs therefore used an earlier helper revision.
  The reopened reports use the committed commands, and this review's reproductions match them, so
  the figures stand. Recording the executed script hashes in the packet would close the
  provenance gap.

## Lens results

- **Conformance: UNCLEAN** (F1, F2, F3). Criteria met: clean-checkout reproduction of both
  standalone configurations (exact); standalone, integrated, Vivado and Yosys figures separately
  labelled (`PP_SHADOW_BASELINE.md:58-92`, `:221-230`); integrated 8x8 synthesis only, per the
  decision; baseline linked from AREA_BUDGET and, per the public review-ready comment, from #229;
  historical figures quoted with provenance and marked non-current (`:290-305`, checked against
  `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:329,459-484` and issue comment 5411378865).
- **RTL: UNCLEAN** (F1: the resource effects of the integrated boundary are misattributed). No RTL
  is changed, and the part, clock constraint, directive, source order and parameters were
  verified against the integrated elaboration.
- **Robustness: CLEAN.** Artifacts: `syn/ooc/pp_baseline.py:71-133,146-180,297-301` at the head;
  `probe_8_4445/` (a missing image fails synthesis at rc 1 under the promotion); nine self-test
  refusals re-run (rc 0); the log parser refuses zero or duplicate wrapper blocks and non-literal
  unreported defaults; the helper refuses an in-repository output. After every run, the clean
  clone's `git status` shows only the recipe's own `sw/builder/out` symlink, and no tracked file
  was written.
- **Tests: UNCLEAN** (F4). The existing arms were checked individually and each fails for its
  stated defect (the control mutant is killed).
- **Docs: UNCLEAN** (F1, F2, F3). `check_py_idiom.py` and `docs_check.py` pass at the head
  (`receipts_py_idiom.txt`, `receipts_docs_check.txt`), with no home paths or bench identifiers in
  the four deliverables.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR, F3 MINOR) | `docs/findings/PP_SHADOW_BASELINE.md`, `PP_SHADOW_BASELINE_INPUTS.json`, recipe; reproduced `receipts/ax7101-ooc`, `ax8x8-ooc`, `ax7101-integrated-synth`, `ax8x8-integrated-synth`, `ax7101-yosys`; issue #231 decision 5844867171 | R333-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |
| RTL | UNCLEAN (F1 MAJOR) | `probe_boundary/*.tsv` on the reproduced integrated checkpoints; `hdl/milan/KL_pp_shadow.sv:180-245`; `hdl/milan/milan_datapath.sv:1205-1206,1583,4005-4007`; generated `baseline_ooc.tcl` and `clock.xdc` | R333-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |
| Robustness | CLEAN | `syn/ooc/pp_baseline.py:71-180,297-301`; `probe_8_4445/probe_results.txt`; self-test output; clean-clone `git status` | R333-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |
| Tests | UNCLEAN (F4 MINOR) | `syn/ooc/pp_baseline.py:231-277`; `probe_selftest/mutation_results.txt`; repository-wide search for self-test wiring | R333-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |
| Docs | UNCLEAN (F1 MAJOR, F2 MINOR, F3 MINOR) | the four deliverables and the `docs/design/AREA_BUDGET.md` link; `receipts_py_idiom.txt`; `receipts_docs_check.txt` | R333-1 | af6d19c553ad8c445a80528344baf2273b41ad46 |

## Prior public review findings on this PR

Read after the verdict and ledger above were written, at 2026-09-26T11:46Z. PR #572 carries no
prior review finding: its two comments are the review-start notices for R332-1 and R333-1, and it
has no review bodies and no inline comments. There is nothing to resolve or retain.

## Limits

- The 1x1 placement, route and the three-directive sweep were not reproduced. The routed rows
  (48,618 / 22,441 LUT, WNS +0.013, WHS +0.014, placement sweep) are checked only against the
  published reopen reports and scoped-timing TSVs, which agree with the page. The routed timing
  reports themselves are omitted from the public packet.
- Runs used 8 threads, not 32. Synthesis results matched the published reports bit for bit,
  including the primitive census hash.
- The 8x8 Yosys row was not reproduced; the 1x1 row was, exactly.
- The boundary probe classifies by cell location. It does not measure the reverse direction
  (wrapper logic moved into the datapath).
- No hardware, bitstream, act or hosted-gate evidence was produced or judged. Physical
  calibration was NOT RUN.

## Pending manager duties

- Hosted and act acceptance at the final head, and the current-dev candidate build at the merge
  turn.
- Publication of this packet (REPORT.md plus the files in MANIFEST.sha256).
- Re-review of any corrected head, which must re-cover every lens this round left UNCLEAN.

R333-1 FINISHED
