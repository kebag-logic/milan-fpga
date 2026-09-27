[R350] NEGATIVE - exact head 55079500483970ee244f12fa4c94401783f3df6f

# R350-1 internal independent review: issue #587 / PR #589

- Round: R350-1 (first review of PR #589)
- Exact head: `55079500483970ee244f12fa4c94401783f3df6f`, tree `791dba22b442a3c5bc43223a1cd74f4200ffdf82`
- Base: `63fe4fb0164d798d44a6476001dc8b887cdd4609` (dev after #565); one commit, docs-only
- Role: internal independent reviewer, cleared context, own detached clone
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs (all five)

## Verdict summary

The measurement itself is correct and reproducible. Both integrated 8x8
syntheses were rerun by the reviewer from a clean clone at the exact head,
using the recipe, the configuration-derived 50 MHz clock and the same tool
revisions. The default flow gives 68,047 LUTs and -1.708 ns WNS. That is 89
fewer than the 100 MHz run's 68,136 LUTs, and 4,647 above the device's
63,400. Every committed figure matches. The committed ranking TSV is
byte-identical after reassembly. The per-cell primitive census, scope-timing
tables and all six probe outputs are byte-identical to the committed hashes.
Every source and image hash in the manifest matches.

One committed evidence value does not reproduce as documented. The manifest
gives a normalized-Verilog digest. The rule stated beside it does not produce
that digest from any other checkout, because the digest still contains the
author's absolute checkout path (F1, MINOR, Docs). An open MINOR leaves Docs
unclean, so the verdict is NEGATIVE. The four other lenses are covered clean
at this head. F2 is optional (SUGGESTION): tag the remaining untagged
historical 8x8 figures with their clock.

## Reconstruction (public state only)

- AGENTS.md, CONTRIBUTING.md, docs/README.md at the head.
- Issue #587 body (frozen acceptance 1-3). Assignment [A10] 5855348441 sets
  scope, the no-RTL/config/tooling rule, the "derive, never restate" clock
  rule, the gates and "every figure is tagged with the clock it was measured
  at". Also read: [A360] TAKEN, [A360] REVIEW READY and the PR body.
- #231 decisions 5844867171 (integrated baseline definition) and 5846064333
  (separate boundary-preserving attribution run; complete rankings; mutants).
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `syn/ooc/pp_baseline.py`,
  `syn/ooc/pp_baseline_mutants.py`, `syn/ooc/pp_baseline_rank.py`.
- `git diff 63fe4fb0..55079500`: three paths, all under `docs/findings/`, and
  history (`ac18b509` #231 merge, `63fe4fb0` #565 merge).
- Published evidence packet `f847f343:review-evidence/587-r1` (author gate
  receipts, artifact hashes) and the manager's review-start comment
  5855783988. The packet holds no manager bank receipts. The source
  static/builder/native bank results the brief cites were therefore not
  inspectable by this reviewer and are not relied on.
- Not treated as part of the PR: the edit to the #229 reference comment.
  Per the brief, the manager restored it and updates it after merge.
- Prior public review findings: see the section after the ledger. It was
  written after this verdict and ledger were fixed.

## Independent reproduction (reviewer-run)

The environment was:

- Vivado 2026.1 build 6511674.
- Python 3.14.7.
- The pinned SDK, installed from the pinned archive (sha256 `d42680e9...`)
  into a scratch destination and verified; GCC 14.3.0.
- LiteX/liteeth/litedram/litex-boards/vexiiriscv at exactly the manifest's
  `dependency_revisions`, with the repository patch series 0002/0004/0005
  applied (reverse-apply checks).
- All seven manifest `recipe_inputs` hashes equal at the head.
- Recipe files (`syn/`, the recipe page, `build.sh`, patches, the SDK
  installer) unchanged since the #231 merge `ac18b509`.

Receipts: `receipts/tool-identity.log`, `receipts/scope-and-recipe-identity.log`.

1. **Clock provenance (derived, not restated).**
   - #565 changed only `configs/endstation_ax7101_8x8.yaml` `milan_clk_hz`
     from 100000000 to 50000000.
   - The launcher preview regenerated `soc_params.json`
     (`_source_config: configs/endstation_ax7101_8x8.yaml`) and emitted
     `--milan-clk-freq 50e6` (`sw/builder/endstation_builder.py:4649`).
   - The synthesis log binds `MILAN_CLK_FREQ_HZ`, `MILAN_CLK_FREQ_HZ_P`,
     `PHC_CLK_HZ_P` and 7x `CLK_HZ_P` to 50000000. `TIM_DIV_US_P` is 50
     and `TIM_DIV_MS_P` is 1000.
   - `milan_clk` is `BUFG(milansoc_crg_clkout1)`. The timing report's clock
     summary gives `milansoc_crg_clkout1` a 20.000 ns period (50.000 MHz).
   - Receipts: `receipts/default-run-facts.log`, `receipts/attribution-run-facts.log`.
2. **Default flow** (`pp_baseline.py <gw> --synthesis-only`, rc 0):
   - Whole design: LUT 68,047; FF 70,744; RAMB36 80; RAMB18 29; DSP 11;
     CARRY4 3,913; WNS -1.708 ns. All 91 compared quantities agree with the
     committed manifest: whole-design utilization, every hierarchical metric
     row and every scoped WNS. The ranking rows also agree
     (`receipts/compare-default.log`).
   - The worst path runs from `u_pp/u_notify/ctr_pend_r_reg[3]/C` to
     `u_pp/u_event_router/sel_r_reg[3]/D`: 43 logic levels, requirement
     20.000 ns.
   - Zero `Synth 8-4445` diagnostics. The `12-4739`/`12-5201`/`20-1307`
     warnings are present. Check-timing reports 0 unclocked pins, 0 pins
     without a maximum-delay constraint, 46 inputs without input delay and
     86 outputs without output delay.
   - `baseline_cells.tsv` (10,521,434 bytes) and `baseline_scope_timing.tsv`
     are byte-identical to the committed hashes. Every other vendor report
     has the same byte length (timestamped header).
3. **Attribution flow** (`--synthesis-only --attribution-only`, separate
   clean clone and work directory, rc 0):
   - All 91 compared quantities agree. Wrapper: LUT 28,955, WNS -1.700.
     Whole design: 69,923 LUTs.
   - The census and scope-timing TSV are byte-identical.
   - The executed scripts of the two exports differ only by
     `read_xdc baseline_boundary.xdc` (`KEEP_HIERARCHY TRUE` on
     `milan_datapath/pp_shadow`), once roots are replaced. Both exports
     issue 118 `read_verilog` commands
     (`receipts/export-script-diff.log`).
4. **Public boundary probes.**
   - Probes were fetched from the #231 packet `e21bc530`. The hashes of
     `boundary.tcl` and `loads.tcl` equal the manifest `probe_sources`.
   - All three probe runs per checkpoint returned rc 0. All six outputs are
     byte-identical to the committed report hashes, including the empty
     attribution `loads.tsv` and the 518-cell wrapper residual
     (`receipts/probe-hash-comparison.log`).
5. **Ranking TSV.**
   - `pp_baseline_rank.py` was run on both reviewer hierarchy reports and
     the rows were prefixed with the two measurement labels. The result is
     byte-identical to `docs/findings/PP_SHADOW_BASELINE_50MHZ_RANKING.tsv`
     (sha256 `f5168fc5...`, `receipts/ranking-reproduction.log`).
6. **Input manifest.**
   - The manifest was rehashed before and after both syntheses against the
     reviewer's trees: 130/130 (default) and 131/131 (attribution)
     repository, processor, gPTP, AXIS, CPU-package and image records
     match.
   - The only differing records are the three generated files that embed
     the absolute checkout and work roots (`alinx_ax7101.v`,
     `alinx_ax7101.tcl`, `baseline_integrated.tcl`). Their difference is
     inherent (`receipts/verify-inputs-*.log`).
   - The processor pin moved from `990f9652` to `0922e434`. The two pins
     differ in 16 files, none under `hdl/`. The zero-byte `hdl/` diff is
     in `receipts/processor-pin-hdl-diff.log`.
   - Against the #231 record, only `CLK_HZ_P` and `TIM_DIV_US_P` differ.
     The firmware, listener ROM and microcode hashes are equal, and the
     gPTP image hash changes (`receipts/historical-vs-50mhz-params.log`).
7. **Page figures.**
   - 124 checks cover every numeric cell of the rerun section's tables, all
     stated deltas, the 4,647 capacity excess, the prose totals and the
     boundary-probe table against the manifest (`receipts/page-figures.log`).
   - A single-cell mutant (-89 to -88) is detected
     (`receipts/page-figures-mutant.log`).
   - All 109 table rows of the pre-PR page keep identical values. Only row
     labels gained clock tags (`receipts/history-rows-unchanged.log`). The
     1x1 values are unchanged.

## Gates at the exact head

Receipts are in `receipts/gates/`, from a separate scratch clone at the head
with submodules at their gitlinks. Every row passed with rc 0:

- `python3 syn/ooc/pp_baseline.py --selftest`: 9 refusals, plus
  export/attribution/CLI containment.
- `python3 syn/ooc/pp_baseline_mutants.py`: the control passes and all 28
  mutants are killed (`receipts/baseline-mutants.log`).
- `docs_check.py` in Git mode and in `GIT_DIR=/dev/null` mode: 0 findings;
  901 text files.
- `check_em_dash.py --base 63fe4fb0`: 0/188 added lines, 339/339 arms.
- `check_doc_style.py`.
- `gen_toc.py --check` and `--verify-anchors`: 179 anchors.
- `check_doc_paths.py`: 848 paths.
- `git diff --check`, both committed and worktree.
- `check_baremetal_only.py --check` and `--selftest`: 899 files, 0 findings.
- `check_entity_shape.py --self-test` and default: 113 checks, 0 failures.
- `pp_srcs.py --check --selftest`.

The three renderer-dependent gates first refused with rc 2 because the
system interpreter lacks the pinned renderer. They were rerun with the
hash-locked `tools/markdown/requirements.txt` renderer and passed
(`receipts/gates/RENDERER.txt`).

The brief says a sibling lane's committed JSON receipts once tripped
`pp_srcs`, `check_baremetal_only` and `check_entity_shape`. To show that the
new files are inside those gates' scope, two disposable plants were made:

- A literal `protocol-processor/hdl/...` path planted in the new JSON makes
  `pp_srcs --check` fail (rc 1) and name that file.
- A retired-stack term planted in the new TSV makes
  `check_baremetal_only --check` fail (rc 1) and name that file.

Both files were restored and the clone was verified clean
(`receipts/gates/gate-bite-probes.log`). The full builder bank was not run
(not allowed). No builder test reads `docs/findings/`: the only builder
reads of `docs/` target other pages.

Hosted evidence at the exact head, inspected only
(`receipts/hosted-runs.tsv`, `receipts/hosted-checks-snapshot.txt`):

- `rtl-fast`, `docs` and `elaborate` completed with success on `55079500`.
- `rtl-full` was still in progress, with Verilator shard 4/5 pending.
- Physical gPTP was skipped: a skipped context, not hardware proof.

## Findings

### F1 - MINOR - Docs

- **Artifact:** `docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json:29-32`
  (`export_comparison`).
- **Title:** The committed normalized-Verilog digest is not reproducible
  from its stated normalization.
- **Authority/evidence:**
  - The field states: "Replace each absolute build root with `$BUILD`;
    strip block and line comments from generated Verilog."
  - The generated top embeds the absolute checkout root three times, in the
    `GPTP_UCODE_HEX_P`, `PP_TROM_HEX_P` and `PP_UCODE_HEX_P` parameters.
  - Applying the stated rule to the reviewer's two exports makes them equal
    to each other, which confirms `equal: true`. The digest is `1f7c01e2...`,
    not the committed `3d371f2d...`.
  - The committed digest is reproduced exactly only by writing the author's
    private lane path (`$LANES/587-8x8-baseline-50mhz`) into the
    reviewer's text before stripping comments. That path is known only from
    the REVIEW READY comment. See `scripts/normalized_verilog.py` and
    `receipts/normalized-verilog.log`.
  - So the committed value binds a host path, and the manifest's own rule
    does not produce it. AGENTS.md section 2 requires a future cold reviewer
    to reconstruct from the repository and GitHub. The brief asks that the
    committed JSON be reproducible.
- **Impact:** A cold reviewer who follows the stated rule gets a different
  digest. They could wrongly conclude that the measured generated RTL
  differs, or be unable to confirm the value. The underlying claim, that
  both exports are equal and match the measured sources, is true. The page
  text is also true.
- **Required outcome:** The manifest's normalization reproduces its digest
  from any checkout. For example, name the checkout root as a replaced root
  and recompute. Alternatively, record the digest's root dependence
  explicitly, or drop the digest and keep the equality with its rule. No
  remeasurement is needed.
- **Verification:** Run `scripts/normalized_verilog.py`, or the stated rule,
  on a fresh export in an arbitrary checkout and obtain the committed digest.
  All docs gates stay rc 0.

### F2 - SUGGESTION - Docs

- **Artifact:** `docs/findings/PP_SHADOW_BASELINE.md`:32, 48, 92-98, 261,
  329-331 and 364-373.
- **Title:** Some historical 8x8 figures still lack an inline clock tag.
- **Evidence:** The assignment asks that "every figure is tagged with the
  clock it was measured at". The labelled tables do this. Some figures
  near them do not:
  - the Provenance processor pin (`990f9652`, the #231 pin; the rerun used
    `0922e434`, stated only at :141);
  - the standalone 8x8 BRAM, critical-path and growth prose (100 MHz OOC,
    100 MHz timer geometry);
  - the "original resource ranking" link, whose 8x8 integrated rows are the
    100 MHz runs and carry no clock in their measurement labels;
  - the 8x8 load-stem prose.

  Each is recoverable from the adjacent labelled table or from the
  "original" wording, so this is optional.
- **Suggested outcome:** Tag these as "historical (#231) 100 MHz". Also
  label the Provenance table as the original record.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts (at head `55079500`) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #587 acceptance 1-3 and assignment 5855348441. Reviewer rerun of both 8x8 variants at the configuration-derived 50 MHz. `PP_SHADOW_BASELINE.md:111-257` against `receipts/compare-*.log` and `receipts/page-figures.log` (LUT delta -89, WNS -1.708 ns, 100 MHz retained as labelled history, 1x1 values unchanged). The #229 comment is excluded per the brief. | R350-1 | `55079500483970ee244f12fa4c94401783f3df6f` |
| RTL | CLEAN | `git diff --raw 63fe4fb0..55079500`: 3 docs paths, no `hdl/`, config, tooling or gitlink change (`receipts/scope-and-recipe-identity.log`). Bound clock-derived parameters and the `milan_clk` derivation from `clkout1` at 20.000 ns (`receipts/default-run-facts.log`). Worst path and check-timing. Processor HDL identity `990f9652` to `0922e434` (`receipts/processor-pin-hdl-diff.log`). | R350-1 | `55079500483970ee244f12fa4c94401783f3df6f` |
| Robustness | CLEAN | Zero `Synth 8-4445` in both runs. Pre- and post-synthesis rehash of all 133/134 manifest records (`receipts/verify-inputs-*post-synthesis.log`). Launcher refusal/preview path. Gate-bite plants on both new files (`receipts/gates/gate-bite-probes.log`). Repeated identical results across two clean clones. Exact-head restoration (`receipts/restore-verification.log`). | R350-1 | `55079500483970ee244f12fa4c94401783f3df6f` |
| Tests | CLEAN | `pp_baseline.py --selftest` and `pp_baseline_mutants.py`: control plus 28 killed. `pp_srcs --check --selftest`, `check_baremetal_only --check/--selftest`, `check_entity_shape --self-test` and default all rc 0 (`receipts/gates/`). Ranking reproduced byte-for-byte with the maintained parser (`receipts/ranking-reproduction.log`). Reviewer figure checker with a killed mutant (`receipts/page-figures-mutant.log`). | R350-1 | `55079500483970ee244f12fa4c94401783f3df6f` |
| Docs | UNCLEAN (F1 MINOR open) | `PP_SHADOW_BASELINE.md` whole page. `PP_SHADOW_BASELINE_50MHZ_INPUTS.json:29-32` (`receipts/normalized-verilog.log`). `PP_SHADOW_BASELINE_50MHZ_RANKING.tsv`. All docs gates rc 0 (`receipts/gates/SUMMARY.tsv`). No stale 100 MHz 8x8 figure elsewhere in the tree (search for 68,136/4,736/-11.331). | R350-1 | `55079500483970ee244f12fa4c94401783f3df6f` |

## Prior public review findings

This was checked after the verdict and ledger above were fixed. PR #589 has
two public comments, both start notices from the manager:

- R350-1 (5855783988);
- R351-1 (5855796851, start notice for the external review).

The PR has no review bodies. Issue #587 has no review findings. So there are
no prior public review findings to resolve or retain at this head.

## Real limits

- Only the integrated 8x8 synthesis endpoints were reproduced, which is the
  scope of this PR. No 1x1 runs, OOC runs, Yosys runs, placement, routing,
  bitstream or hardware work was done. Physical calibration was not run.
  Skipped hosted contexts are not hardware proof.
- The runs used the host's installed LiteX environment, whose revisions and
  patch state were verified. It is not a fresh `ci_litex_env.py` build.
  Vendor reports other than the census, scope-timing and probe outputs
  differ from the committed hashes only in timestamped headers, at equal
  byte length. They are not byte-compared.
- The full builder, parent, PP, gPTP and Yosys banks were not run (not
  allowed). The manager's bank receipts were not present in the published
  packet at `f847f343`, so they were not independently inspected.
- `rtl-full` was still running at inspection time. The manager owns hosted
  and local-replica acceptance.
- The reviewer's scratch clone for the attribution run and the gates is
  unpublished. The review clone was restored and verified: 925 tracked
  blobs, modes, index and three gitlinks, with 0 mismatches.

## Pending manager duties

- Resolve F1 and re-review the corrected head. Docs must be re-covered at
  the new head. The other four lenses stay covered only if the new commit
  touches nothing in their scope.
- Update the #229 reference comment after merge (acceptance item 2's last
  clause), as stated in the brief.
- Hosted `rtl-full` completion, local replica, and candidate-merge
  validation against live dev.
- External review ([R351]) and the second positive review required by
  CONTRIBUTING.

R350-1 FINISHED
