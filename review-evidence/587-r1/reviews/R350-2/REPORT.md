[R350] POSITIVE - exact head ce65430125a3c800138d5206dd481ba060cb2328

# R350-2 internal independent review: issue #587 / PR #589

- Round: R350-2. This is a delta review of `55079500..ce654301`. R350-1 covered `55079500`.
- Exact head: `ce65430125a3c800138d5206dd481ba060cb2328`, tree `91accb6f4620fd36593b7e186f89b972ff5451a8`.
- Parent: `55079500483970ee244f12fa4c94401783f3df6f`. PR base: `63fe4fb0164d798d44a6476001dc8b887cdd4609`.
- Role: internal independent reviewer. Cleared context, own detached clone.
- Lenses applied: Conformance, RTL, Robustness, Tests and Docs (all five).

## Verdict summary

The round-2 commit closes R350-1 F1 and takes R350-1 F2.

**F1.** The manifest's normalization rule now replaces the checkout root with
the literal token `$REPO`. The unchanged round-1 script
`scripts/normalized_verilog.py` gave the committed digest `38f6c8dd...` from
two fresh 8x8 exports. The exports were made in two different checkout roots,
with different lengths and depths, and different build roots. Neither root is
the author's lane or the reviewer's round-1 scratch. An independent literal
implementation of the committed rule gives the same digest for both exports.
The same implementation shows that the Tcl and XDC files are equal after both
root replacements.

**F2.** Every historical 8x8 figure on the page now carries its clock and
processor pin, either inline or through a scoping sentence immediately before
it. The pins are correct. Every #231 lane commit carries `990f9652`, and
`0922e434` is the head's gitlink.

**Figures.** No figure changed value. In the page and the manifest, the only
changed value is the digest and its rule.

**Gates.** All 17 gate commands return rc 0 at the exact head.

No MINOR, MAJOR or BLOCKER finding is open, so all five lenses are covered
clean at this head. One optional SUGGESTION (S1) about wording is recorded.

## Reconstruction (public state only)

- AGENTS.md, CONTRIBUTING.md and docs/README.md at the head.
- Issue #587 body, frozen acceptance items 1-3.
- [A10] assignment 5855348441, which carries the scope, the "derive, never
  restate" rule, the requirement that every figure is tagged with its clock,
  and the gates.
- [A10] Round 2 assignment 5856241447:
  - no re-measurement;
  - F1: name the checkout root as a token, recompute the digest, and check it
    with this reviewer's unchanged script on a fresh export in a different
    directory;
  - F2: tag every historical 8x8 figure with its clock and processor pin;
  - take R351-1's suggestions if they are text only.
- [A365] REVIEW READY 5856350942.
- R350-1 (this reviewer's round-1 report, PR comment 5856181980) and its
  published scripts at `7b4e6317`.
- Manager start comment 5856357812.
- `git diff 55079500..ce654301`: three documentation paths, all mode 100644.
- `git diff 63fe4fb0..ce654301`: four documentation paths.
- The #231 lane history, used to check the pins.
- Evidence packet `f847f343:review-evidence/587-r1` (author round-1 receipts;
  no bank receipts). The round-2 author packet `d33c3493` exists on the
  evidence branch. It was not needed and not relied on: every claim here comes
  from reviewer execution.

## Independent verification (reviewer-run)

Environment (`receipts/tool-identity.log`):

- Python 3.14.7.
- LiteX, liteeth, litedram, litex-boards and vexiiriscv at exactly the
  manifest's `dependency_revisions`, with patches 0002, 0004 and 0005 applied
  (reverse-apply checks).
- The pinned SDK archive `d42680e9...`, freshly installed into scratch and
  verified; GCC 14.3.0.
- The hash-locked Markdown renderer, for the renderer gates.
- No Vivado, Verilator or Yosys run. No re-measurement was required or made.

### 1. F1: normalized-Verilog digest reproduces from any checkout

Two fresh clones of the exact head were made, each with its three submodules
at their gitlinks:

- `<scratch>/rootA-7q/milan-checkout`;
- `<scratch>/zz-second-root/b/deeper/mf`.

Each ran the recipe's "Before measuring" redirects and the `ax8x8 --dry-run`
preview (`--milan-clk-freq 50e6` in both). Each then ran the recipe's export
step, `ax8x8` only, into its own build root: `workA-exports/w1` and
`other-work/B_long_named_build_dir`. Both returned rc 0
(`receipts/fresh-export-A.log`, `receipts/fresh-export-B.log`).

- **Unchanged script.** `scripts/normalized_verilog.py` has sha256
  `0f418e05...`, identical to the published R350-1 copy
  (`receipts/script-identity.log`). It was run with the token `$REPO` as its
  replacement argument:
  - export A: 3 root occurrences, normalized sha256 `38f6c8dd93ba018d009875412b82dd9f34e2149244eda20ab1e2f81d3f85f575`;
  - export B: 3 root occurrences, the same digest;
  - committed `export_comparison.normalized_verilog_sha256`: `38f6c8dd...`,
    with `equal: true`;
  - the raw files differ (`dee4a7db...` against `047481a5...`) because they
    embed different roots.

  Receipt: `receipts/normalized-verilog-round2.log`.
- **Negative controls, same file:**
  - substituting the author's round-1 lane path gives the superseded
    `3d371f2d...`;
  - leaving the reviewer's root in place gives `c7e1c6c0...`;
  - spelling the token `${REPO}` gives `7d3f40a5...`.

  So the digest depends on the token exactly and no longer depends on any
  host path.
- **Rule as written.** `scripts/rule_as_written.py` reads the committed rule
  text and implements it literally:
  - replace the build root with `$BUILD`, then the checkout root with `$REPO`;
  - strip `/\*.*?\*/` in DOTALL mode, then `//[^\n]*`;
  - hash UTF-8 bytes.

  Results:
  - Both exports give the committed digest.
  - The generated Verilog embeds the checkout root three times, in
    `GPTP_UCODE_HEX_P`, `PP_TROM_HEX_P` and `PP_UCODE_HEX_P`, as the rule
    states.
  - It embeds the build root zero times, so the `$BUILD` step is vacuous for
    Verilog and the order does not matter here.
  - `alinx_ax7101.tcl` differs raw, and is equal after both replacements.
    `alinx_ax7101.xdc` is equal raw.
  - rc 0 (`receipts/rule-as-written.log`).
- **Input manifest still binds the fresh exports.** `baseline_integrated.tcl`
  was prepared with `pp_baseline.py` (default in A, attribution in B, rc 0),
  and the unchanged round-1 `verify_inputs.py` was run:
  - 130/130 default and 131/131 attribution repository, processor, gPTP,
    AXIS, CPU-package and image records match;
  - the only differing records are the three generated files that embed roots.

  Receipts: `receipts/verify-inputs-default-A.log` and
  `receipts/verify-inputs-attribution-B.log`. Their `NORMALIZED` lines come
  from the round-1 tool, which replaces build roots only, and are superseded
  by the two receipts above.

### 2. F2: historical 8x8 clock and processor-pin tags

**Whole page read at the head.** Every historical #231 8x8 figure falls into
one of four groups:

- **Inline row label or column header:** lines 52, 77, 80, 94, 157, 198,
  309, 321, 368, 380-384, 484, 493, 510, 536 and 566.
- **Prose line naming both clock and pin:** lines 97-98, 103-105, 113-115,
  128-129 and 359-362. Also lines 347-349, which cover 350-352, and lines
  396-399.
- **Scoping sentence immediately before a table or paragraph:**
  - line 178 for the attribution table at 183;
  - lines 129-130 for the default table at 140;
  - line 386 for the load-stem prose;
  - lines 278-279 for the original ranking file;
  - lines 443-444 for the original manifest and the 8x8 firmware word count
    at 454;
  - lines 474-476 for every Mapping-differences figure, including the prose
    at 486-490, 502 and 581.
- **Rerun rows:** these carry "Declared 50 MHz" or "at 50 MHz", and the rerun
  pin `0922e434` at lines 32, 130 and 151.

**Pins verified** (`receipts/pin-provenance.log`):

- The #231 measured revision `7eb3b0d4` and every #231 lane commit
  (`af6d19c5`, `0a506fa8` for the attribution run, and `ae729bbf`) carry
  `990f9652`.
- `0922e434` entered dev at `1912c047`, which is on the first-parent side of
  the #231 merge, not in the lane.
- The head's gitlink is `0922e434`.
- So "historical ... pin `990f9652`" is true of every tagged historical row,
  including the attribution and Yosys mapping rows.

**Clocks** are consistent with the original configuration table (lines
49-52):

- the 1x1 timer runs at 50 MHz and the 8x8 timer at 100 MHz;
- the out-of-context clock is 100 MHz;
- line 349 ("50 MHz and 100 MHz, respectively") and line 566
  ("50/100 MHz timers") agree with it.

### 3. No figure changed value except the digest

`scripts/check_delta_figures.py` checks `55079500` against `ce654301`
(`receipts/delta-figures.log`, rc 0):

- **Tables:** 138 rows in both versions, in order. Every data cell is
  byte-identical. Only 14 row labels and 5 headers changed, and only by adding
  clock or pin tags.
- **Prose:** no numeric token was lost. The only added numeric tokens are the
  tags 100, 50, 231, 587 and the shape digits 8 and 1. Pin hashes and
  "SHA-256" are masked before counting.
- **Manifest JSON:** a recursive diff finds exactly
  `export_comparison.normalized_verilog_sha256` and
  `export_comparison.normalization`. `equal` is true in both versions.
- **`PP_SHADOW_BASELINE_50MHZ_RANKING.tsv`:** byte-identical.
- **`AREA_BUDGET.md`:** one added pointer sentence and nothing removed.

**Checker mutation probes** (`receipts/delta-figures-mutants.log`): a clean
fresh checkout passes as the control. Three single-value mutants are each
detected with rc 1:

- a table cell `68,136` changed to `68,137`;
- a prose figure `4,736` changed to `4,737`;
- a manifest metric `68047` changed to `68048`.

The checkout was restored afterwards.

**Round-1 page checker rerun unchanged at the head**
(`receipts/page-figures-round2.log`): 124/124 rerun-section checks pass. They
cover the cells, deltas, the 4,647 excess, prose totals and the probe table
against the manifest.

**Stale figures:** a tree-wide search at the head finds no historical 8x8
integrated figure outside the baseline page and its manifests
(`receipts/stale-figure-search.log`). R350-1 had already shown the
base-to-`55079500` history rows unchanged, so together these show base-to-head
history values are unchanged.

### 4. Gates at the exact head

These ran in the fresh clean checkout B. Receipts are in `receipts/gates/`,
summarised in `SUMMARY.tsv`. Every row returned rc 0:

- `python3 syn/ooc/pp_baseline.py --selftest`: valid pathname and 9
  refusals; export, attribution and CLI containment.
- `python3 syn/ooc/pp_baseline_mutants.py`: the control passes and 28
  removals are killed (29 PASS lines).
- `docs_check.py` in Git mode and in `GIT_DIR=/dev/null` mode: 0 findings;
  169 md and 901 text files.
- `check_em_dash.py --base 63fe4fb0`: 0 findings over 230 added lines;
  339/339 arms.
- `check_doc_style.py`: OK.
- `gen_toc.py --check`: OK. `gen_toc.py --verify-anchors`: 179 anchors.
- `check_doc_paths.py`: 848 paths.
- `git diff --check` for base-to-head, for the delta and for the worktree.
- `check_baremetal_only.py --check`: 899 files, 0 findings. Its
  `--selftest` also passes.
- `check_entity_shape.py --self-test`, and the default run: 113 checks, 0
  failures.
- `pp_srcs.py --check --selftest`.

The renderer-dependent gates ran under the hash-locked
`tools/markdown/requirements.txt` renderer (cmarkgfm 2025.10.22, html5lib
1.1).

### 5. Hosted evidence (inspected only)

Snapshot: `receipts/hosted-check-runs.tsv` and
`receipts/hosted-workflow-runs.tsv`, 20 check runs at `ce654301`.

- At the final snapshot (13:52Z), 14 had completed with success. These
  include the whole `rtl-fast` workflow, the whole `elaborate` workflow,
  `yosys-elaboration`, Yosys shards 0-3 of 4 and Verilator shard 3/5.
- 5 were still in progress: `docs-check`, and Verilator shards 0, 1, 2 and 4
  of 5 (the `docs` and `rtl-full` workflows).
- `Physical gPTP (nightly and manual)` was skipped. That is a skipped context,
  not hardware proof.

The manager owns hosted and local-replica acceptance.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

### S1 - SUGGESTION - Docs

- **Artifact:** `docs/findings/PP_SHADOW_BASELINE.md:386-399` and `:347-349`.
- **Title:** The probe-paragraph scoping sentence is slightly narrower than
  its paragraph, and one growth tag is repeated.
- **Evidence:**
  - Line 386 opens "The following historical 8x8 probes use 100 MHz, pin
    `990f9652`". Line 391 in the same paragraph says the histogram files are
    empty "at both synthesis shapes", which includes the 1x1 50 MHz probe.
  - Lines 396-398 restate the standalone-growth clock and pin that lines
    347-349 already give. They sit in the probe paragraph, just ahead of the
    758-LUT timer figure they tag.
  - No figure is mis-tagged, and every figure's clock and pin is correct.
- **Suggested outcome (optional):** Scope line 386 to the 8x8 sentences only.
  Move the 758-LUT timer sentence beside lines 347-352, so one tag covers
  both.

## Round-1 finding status (this reviewer)

- **R350-1 F1 (MINOR, Docs): CLOSED at `ce654301`.**
  - `PP_SHADOW_BASELINE_50MHZ_INPUTS.json:30-31` now names the checkout root
    as `$REPO`, lists the three parameters that carry it, and gives the exact
    regexes and the byte encoding.
  - The unchanged round-1 script and an independent literal implementation
    give the committed digest from two fresh exports in two new roots.
  - The superseded digest reproduces only with the author's host path.
  - Page lines 174-176 describe the same rule and point to the manifest.
- **R350-1 F2 (SUGGESTION, Docs): TAKEN at `ce654301`.**
  - Every item listed in R350-1 is now tagged: the Provenance pin and table,
    the standalone BRAM, critical-path and growth prose, the original ranking
    link, and the load-stem prose.
  - Evidence: section 2 above.

## Reviewer-owned completion ledger

A later commit that touches any artifact within a lens's scope un-covers that
lens.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #587 acceptance 1-3; [A10] assignments 5855348441 and 5856241447 (no re-measurement; F1; F2). `PP_SHADOW_BASELINE.md:119-273` rerun figures, 124/124 against the manifest (`receipts/page-figures-round2.log`). History values unchanged (`receipts/delta-figures.log`). Every historical 8x8 figure tagged with clock and pin, with pins proven (`receipts/pin-provenance.log`). The digest reproduces as the round-2 assignment requires (`receipts/normalized-verilog-round2.log`). The #229 comment is manager-owned after merge. | R350-2 | `ce65430125a3c800138d5206dd481ba060cb2328` |
| RTL | CLEAN | `git diff --raw 55079500..ce654301` and `63fe4fb0..ce654301`: documentation paths only, mode 100644, no `hdl/`, configuration, tooling or gitlink change (`receipts/restore-and-scope-verification.log`). The fresh exports bind `--milan-clk-freq 50e6` from the configuration (`receipts/fresh-export-*.log`, the dry-run in both). The generated top's three ROM path parameters are the only root-bearing RTL text (`receipts/rule-as-written.log`). Gitlinks `0922e434`, `5dce647a` and `48ff7a7e` at the head. | R350-2 | `ce65430125a3c800138d5206dd481ba060cb2328` |
| Robustness | CLEAN | Digest independence across two checkout roots of different depth and length and two build roots. Three negative controls: the author path, an unreplaced root and a wrong token spelling (`receipts/normalized-verilog-round2.log`). Rule order and vacuous `$BUILD` step (`receipts/rule-as-written.log`). Tcl and XDC equal after replacement. Manifest rehash of 130/130 and 131/131 records against the fresh exports (`receipts/verify-inputs-*.log`). Review clone restored and verified. | R350-2 | `ce65430125a3c800138d5206dd481ba060cb2328` |
| Tests | CLEAN | `pp_baseline.py --selftest`, and `pp_baseline_mutants.py` with control plus 28 killed. `pp_srcs --check --selftest`, `check_baremetal_only --check/--selftest`, `check_entity_shape --self-test` and default: all rc 0 (`receipts/gates/`). Reviewer checkers: `check_delta_figures.py`, with three killed mutants and a passing control (`receipts/delta-figures-mutants.log`), and the unchanged `check_page_figures.py` and `normalized_verilog.py`. | R350-2 | `ce65430125a3c800138d5206dd481ba060cb2328` |
| Docs | CLEAN (S1 optional) | `PP_SHADOW_BASELINE.md` whole page at the head. `PP_SHADOW_BASELINE_50MHZ_INPUTS.json:29-33`. `AREA_BUDGET.md:9-12`. All docs gates rc 0 (`receipts/gates/SUMMARY.tsv`). No stale historical figure elsewhere (`receipts/stale-figure-search.log`). R350-1 F1 closed and F2 taken. | R350-2 | `ce65430125a3c800138d5206dd481ba060cb2328` |

## Prior public review findings

These were read only after the verdict and ledger above were fixed
(`receipts/verdict-before-prior-findings.txt`). Public review findings on
PR #589 at `55079500` come from two rounds.

**R350-1 (5856181980).** F1 is closed and F2 is taken. See "Round-1 finding
status" above.

**R351-1 (5856239199):**

- **R351-F1 (MINOR, Docs; retains R350-1 F1): CLOSED at `ce654301`.** Its
  verification asks for the committed rule to be applied to a fresh export in
  an arbitrary checkout, with the committed digest as the result. That was
  done literally, for two fresh exports in two new roots
  (`receipts/rule-as-written.log`), and with the unchanged round-1 script
  (`receipts/normalized-verilog-round2.log`). All docs gates return rc 0
  (`receipts/gates/SUMMARY.tsv`).
- **R351-S1 (SUGGESTION, Docs; overlaps R350-1 F2): TAKEN at `ce654301`.**
  - The Provenance table is headed "Original #231 input" (`PP_SHADOW_BASELINE.md:34`).
  - Lines 30-32 state that the 8x8 #231 measurements use 100 MHz and pin
    `990f9652`, and that the #587 rerun uses pin `0922e434`.
  - The configuration table is headed "Original #231 product configuration",
    with its 8x8 row pinned (lines 49-52).
  - The remaining prose is tagged (section 2).
  - The suggestion's verification (Provenance against the manifest's
    `submodules`) holds: the 50 MHz manifest records `0922e434`, and the #231
    measured revision carries `990f9652` (`receipts/pin-provenance.log`).
- **R351-S2 (SUGGESTION, Docs): TAKEN at `ce654301`.** `AREA_BUDGET.md:10`
  now reads "It also records issue #587's 50 MHz 8x8 rerun." The statement is
  true and nothing was removed (`receipts/delta-figures.log`).

There are no other review bodies or findings on the PR or the issue. No prior
finding is retained at this head.

## Real limits

- There was no re-measurement. The Vivado synthesis endpoints were not rerun
  in this round. R350-1 reproduced them at `55079500`, and this round proves
  that no figure or input changed since then.
- Only the `ax8x8` export and script preparation were run: no 1x1, OOC,
  Yosys, placement, routing, bitstream or hardware work. Physical calibration
  was not run. Skipped hosted contexts are not hardware proof.
- The LiteX environment is the host's installed one. Its revisions and patch
  state were verified, but it is not a fresh `ci_litex_env.py` build.
- The full builder, parent, PP, gPTP and Yosys banks were not run (not
  allowed). The manager's source static, builder and native bank receipts for
  this head were not found in the published evidence inspected (`f847f343`),
  so they were not independently inspected.
- Hosted `docs` and `rtl-full` were still in progress at the final
  inspection. `rtl-fast` and `elaborate` had completed with success.
- Tag completeness (section 2) is a reviewer reading of the whole page, not a
  mechanical proof. Mechanical proof covers value stability only.

## Pending manager duties

- Hosted exact-head completion (`rtl-fast`, `docs`, `elaborate`,
  `rtl-full`/`verilator-suites`, Yosys portability), the local replica, and
  the candidate-merge validation against live dev `682ecf0c`.
- The second positive review from the external reviewer, and the rest of the
  CONTRIBUTING review bar.
- The #229 reference comment update after merge (acceptance item 2's last
  clause).
- Issue closure and moving the card to Done after merge.

R350-2 FINISHED
