[R351] POSITIVE - exact head ce65430125a3c800138d5206dd481ba060cb2328

# R351-2 external independent review: issue #587 / PR #589, round 2

- Head under review: `ce65430125a3c800138d5206dd481ba060cb2328`, tree `91accb6f4620fd36593b7e186f89b972ff5451a8`. It is one commit on `55079500`, which is itself one commit on dev `63fe4fb0164d798d44a6476001dc8b887cdd4609`.
- Role: [R351], external independent reviewer, cleared context, isolated detached clone.
- Round: R351-2, a delta review of `55079500..ce654301`. My round-1 review (R351-1) covered `55079500`.
- Lenses applied at this head: Conformance, RTL, Robustness, Tests, Docs (all five).
- Verdict: POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. My round-1 MINOR (R351-F1, which retained [R350] F1) is closed with reviewer-executed evidence. One new SUGGESTION is recorded; it does not affect coverage.

## 1. Reconstruction

I reconstructed the task from public state only, in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. Issue #587: the frozen acceptance 1-3, the [A10] assignment `5855348441`, the [A10] "Round 2 for PR #589" assignment `5856241447`, and the [A365] REVIEW READY `5856350942`.
4. The recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
5. The diff `55079500..ce654301` (and `63fe4fb0..ce654301` for the cumulative view) and the commit metadata.
6. The manager-published packet `review-evidence/587-r1` at `f847f343` (file inventory).
7. The hosted check runs at the exact head.

The round-2 assignment requires three things, with no re-measurement:
1. The `export_comparison` normalization must also replace the checkout root with a named token, and the digest must be recomputed so it reproduces from any checkout.
2. Every remaining historical 8x8 figure must carry its clock and processor pin, including the provenance pin: `990f9652` for #231 and `0922e434` for the rerun.
3. R351-1's suggestions are to be taken if they are text only.

What changed in `55079500..ce654301` (`git diff --raw`):
- Three files, all mode 100644:
  - `docs/design/AREA_BUDGET.md`
  - `docs/findings/PP_SHADOW_BASELINE.md`
  - `docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json`
- `PP_SHADOW_BASELINE_50MHZ_RANKING.tsv` is unchanged.
- There is no RTL, configuration, tooling, recipe or gitlink change.
- The commit message is one line with no body and no trailers.
- The GitHub PR head equals `ce654301`, and the base is dev at `63fe4fb0`.

The assignment text names another reviewer's `scripts/normalized_verilog.py`. To keep this review independent, I did not read or run that script. My round-1 packet had no script of that name; the round-1 normalization ran inline. For this round I wrote `scripts/normalized_verilog.py` from the committed rule text alone. I froze its hash (`receipts/normalized_verilog_script_frozen.sha256`, `b24e5d0b...`) before any export existed at this head, and ran it unchanged afterwards.

## 2. Reviewer-executed verification (at this head)

### 2.1 Digest reproduces from relocated checkouts (R351-F1)

I rebuilt a private environment under the reviewer scratch directory, which is never published:
- the pinned SDK, freshly installed from the archive with sha256 `d42680e9...` and verified (GCC 14.3.0);
- private copies of the LiteX packages at the manifest's dependency revisions, carrying patches 0002 and 0004;
- the VexiiRiscv package copy, restricted to the cached netlist `f5f08b17...`. Its generator sources were excluded, so a cache miss would fail rather than regenerate (`receipts/export_environment.out`).

I made two full copies of this clone at different absolute paths of different lengths:
- `<scratch>/ck/alpha/milan-fpga` with build root `<scratch>/work-alpha`;
- `<scratch>/ck/relocated-beta/deeper/checkout-b` with build root `<scratch>/wk/beta-build-root`.

In each copy I ran the recipe's Prerequisites symlinks, the launcher `ax8x8 --dry-run` preview, and the export (firmware compiled, `--build` removed). The preview emitted `--milan-clk-freq 50e6` and both exports returned rc 0 (`scripts/export_ax8x8.sh`, `receipts/export_environment.out`). Neither path is the executor's path or my round-1 path.

| Check | Result | Receipt |
|---|---|---|
| Frozen rule script on export alpha | `38f6c8dd93ba018d009875412b82dd9f34e2149244eda20ab1e2f81d3f85f575`, 1,657,308 bytes, 3 checkout-root replacements (the three ROM-path parameters), 0 residual absolute string literals | `receipts/normalized_verilog_two_exports.out` |
| Frozen rule script on export beta | the same digest, byte count and replacements | same |
| Committed `normalized_verilog_sha256` at `ce654301` | `38f6c8dd...`: EQUAL | same |
| Same Verilog, checkout root replaced with `$BUILD` (the round-1 rule as written) | `1f7c01e2...`, equal to my round-1 receipt | `receipts/digest_crosscheck.out` |
| Same Verilog, checkout root replaced with the executor's published lane path | `3d371f2d...`, equal to the digest committed at `55079500` | same |
| Sensitivity control: one-identifier mutation under the new rule | `58e0e94f...` (differs) | same |
| Export inputs vs the manifest | 130 of the 133 default records (127 sources, 6 images) match raw on both exports, including all 6 images and the CPU netlist. The other three are the root-bearing generated files: `alinx_ax7101.v` and `alinx_ax7101.tcl` differ raw, and `baseline_integrated.tcl` is absent because an export alone does not produce it | `receipts/compare_inputs_two_exports.out` |
| Generated Tcl rebased to the executor's published roots | `ce14fb89...`, 29,686 bytes, equal to the manifest on both exports. Under the rule's two root replacements, alpha and beta Tcl are equal to each other; the XDC is raw-equal | `receipts/tcl_identity.out` |
| Symlinked-checkout probe (a third copy, reached through a symlink) | The launcher preview refuses, so no export is produced. A logical-versus-physical checkout-root ambiguity cannot enter a recipe export | `receipts/probe_symlinked_checkout.out` |

Conclusions:
- The new digest identifies the same generated Verilog that R351-1 and the executor measured. The three digests (`38f6c8dd`, `1f7c01e2`, `3d371f2d`) are the same text under three root tokens.
- The committed rule now reproduces the committed value from any checkout path and build root.

### 2.2 No figure changed value

`scripts/delta_values.py` over `55079500..ce654301` returned PASS (`receipts/delta_values.out`):
- All 76 numeric table rows of the page are identical in their numeric cells, count and order.
- No number token was removed from the page. The added tokens are only label material: `100`, `50`, `231`, `587`, `8x8`/`1x1` fragments, and `SHA-256`.
- The input manifest is identical after removing exactly the two changed keys, `normalized_verilog_sha256` and `normalization`.

The round-1 history check against dev `63fe4fb0` also still passes: all 60 base numeric rows survive, and no prose number is lost (`receipts/check_history_numbers_vs_dev.out`).

### 2.3 Clock and processor pin on historical 8x8 figures

I checked the pins against the repository:
- `git ls-tree 7eb3b0d4 protocol-processor` gives `990f96526bb8...`. That is the #231 `measured_rtl_commit` in `PP_SHADOW_BASELINE_INPUTS.json`.
- `63fe4fb0` and `ce654301` give `0922e43408f8...`, the 50 MHz manifest's submodule pin.

I then read the whole page at head. Every historical 8x8 figure now carries its clock and pin, in one of three places:
- its row label: `:52`, `:77`, `:80`, `:94`, `:198`, `:368`, `:380-384`, `:484`;
- its table or column heading: `:34`, `:157`, `:309`, `:321`, `:493`, `:510`, `:536`, `:566`;
- an adjacent framing sentence: `:30-32` (provenance), `:97-98`, `:103-105`, `:113-116`, `:129-130`, `:178-179`, `:277-279`, `:347-349`, `:359-362`, `:386`, `:396-398`, `:443-444`, `:474-476`.

The clocks agree with the Provenance configuration table (`:48-52`): timers of 50 MHz at 1x1 and 100 MHz at 8x8, an OOC clock of 100 MHz, and integrated clocks of 50 MHz at 1x1 and 100 MHz historically at 8x8.

The `AREA_BUDGET.md:10` pointer now names the #587 rerun (R351-S2 taken).

### 2.4 Gates (reviewer-run at this head, foreground)

All rc 0 (`receipts/gates.rc`, `receipts/gate_*.out`):
- `docs_check.py`, in Git mode and in `GIT_DIR=/dev/null` mode (0 findings over 901 text files);
- `check_doc_style.py`;
- `check_doc_paths.py` (848 paths);
- `gen_toc.py --check`, and `--verify-anchors` (179 anchors);
- `check_em_dash.py`, with base `63fe4fb0` and with base `55079500` (339/339 arms);
- `git diff --check` from both bases;
- `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`;
- `pp_srcs.py --check`, `check_baremetal_only.py --check` and `--selftest`, `check_entity_shape.py`.

The em-dash and contents gates used the locked Markdown renderer, installed with hashes from `tools/markdown/requirements.txt` into a private scratch environment. Verilator was not needed, because nothing in the delta is RTL.

### 2.5 Hosted snapshot (not an acceptance)

The snapshot was taken at 2026-09-27T13:47:25Z and is recorded in `receipts/hosted_check_runs.tsv`:
- Completed with success: `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, and Yosys shards 0-3.
- Still in progress: `docs-check`, `elaborate`, `yosys-elaboration` and Verilator shards 0-4.
- Skipped: `Physical gPTP (nightly and manual)`. A skipped context is not hardware proof.

The manager owns hosted and act acceptance.

## 3. Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

```text
[R351] SUGGESTION Docs - docs/findings/PP_SHADOW_BASELINE.md:140 - R351-S3: one historical row takes its pin from prose above the table
Requirement/evidence: The "Historical 100 MHz, 2026-09-26" row of the default 8x8 table carries its clock in the label.
  Its pin 990f9652 is stated at :129-130, before the table, and nowhere in the row or heading. The matching attribution
  table uses an explicit "The following historical 100 MHz row uses processor pin" sentence (:178-179), and other
  historical rows carry the pin in the label.
Impact: Uniformity only; the pin is unambiguous from the same section, so the round-2 requirement is met.
Suggested change: Optionally add ", pin `990f9652`" to the row label, or a "following row" sentence like :178-179.
Verification: Read :127-142.
```

## 4. Clean-lens results (same format, with evidence)

```text
[R351] PASS Conformance - issue #587 acceptance 1-3 and round-2 assignment 5856241447; PP_SHADOW_BASELINE_50MHZ_INPUTS.json:29-32; PP_SHADOW_BASELINE.md:30-36,:119-199; receipts/normalized_verilog_two_exports.out, receipts/delta_values.out
  Assignment item 1: the rule now names $REPO for the three ROM-path parameters. The committed digest is reproduced by
  a rule-derived script on two fresh exports in relocated checkouts. Item 2: every historical 8x8 figure carries its
  clock and pin (section 2.3); both pins are correct against the gitlinks at 7eb3b0d4 and 63fe4fb0. Item 3: R351-S1
  and R351-S2 were taken as text. Frozen acceptance 1-3 still holds: 68,047 LUT, -89 versus 100 MHz, WNS -1.708 ns at
  50 MHz, and 100 MHz kept as labelled history. No figure changed value, and no re-measurement was made.
[R351] PASS RTL - git diff --raw 55079500..ce654301 (three docs paths, no hdl/, configs/, syn/, sw/ or gitlink change); <scratch> exports' generated alinx_ax7101.v; receipts/digest_crosscheck.out, receipts/compare_inputs_two_exports.out
  There is no RTL change. The generated top at this head, exported twice at 50e6, is the same normalized text that R351-1
  synthesized (1f7c01e2 under the old rule). All repository, processor, gPTP, AXIS, CPU-package and image inputs match
  the manifest raw. The three ROM-path parameters resolve to the checkout's configs/generated and
  sw/builder/out paths, and the wrapper parameters in the manifest are unchanged.
[R351] PASS Robustness - receipts/normalized_verilog_two_exports.out, receipts/digest_crosscheck.out, receipts/probe_symlinked_checkout.out, receipts/tcl_identity.out
  The digest is invariant across two checkout paths of different lengths and two build roots. It is sensitive to a
  one-identifier change. The old rule and the old private-path substitution map to the old values, so the rule is not
  tuned to a value. No absolute path survives normalization. A symlinked checkout is refused by the launcher before
  any export. The build root never appears in the generated Verilog, so the rule's replacement order cannot bite.
[R351] PASS Tests - scripts/normalized_verilog.py (frozen sha256 b24e5d0b before any export), scripts/delta_values.py, receipts/gates.rc, receipts/gate_pp_baseline_selftest.out, receipts/gate_pp_baseline_mutants.out
  The reviewer's checks can fail for the defects they target: the digest check fails under the old rule and on
  mutation, and the value check fails on any removed number, changed row or extra manifest key. Existing baseline
  self-tests, mutants and repository gates are green at this head. This docs-only scope needs no repository test
  change, and no repository test asserts the digest.
[R351] PASS Docs - docs/findings/PP_SHADOW_BASELINE.md (whole page at head), PP_SHADOW_BASELINE_50MHZ_INPUTS.json:29-32, docs/design/AREA_BUDGET.md:9-10; receipts/gates.rc, receipts/delta_values.out, receipts/check_history_numbers_vs_dev.out
  The page's normalization summary (:174-176) matches the manifest rule. The Provenance and configuration tables are
  labelled as the original #231 record, and both pins are stated. Every historical 8x8 figure carries its clock and pin.
  The AREA_BUDGET pointer names the rerun. The docs, style, path, contents, anchor, em-dash and whitespace gates pass.
  The committed files contain no private path. Only SUGGESTION R351-S3 remains, which does not affect coverage.
```

## 5. Reviewer-owned completion ledger

This round changed three docs/evidence files. My round-1 coverage of Conformance, RTL, Robustness and Tests was at `55079500`, and those files are within the scope of Conformance and Docs, so I re-applied all five lenses at this head rather than carrying any forward.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #587 acceptance 1-3; round-2 assignment 5856241447; INPUTS.json:29-32; PP_SHADOW_BASELINE.md:30-36, :119-199; digest reproduction; value-preservation check | R351-2 | ce65430125a3c800138d5206dd481ba060cb2328 |
| RTL | CLEAN | `git diff --raw 55079500..ce654301`; two fresh generated `alinx_ax7101.v` at 50e6; input comparison vs manifest; digest cross-check to R351-1's synthesized text | R351-2 | ce65430125a3c800138d5206dd481ba060cb2328 |
| Robustness | CLEAN | two relocated checkouts and build roots; mutation sensitivity; old-rule and old-path controls; symlinked-checkout probe; residual-path scan | R351-2 | ce65430125a3c800138d5206dd481ba060cb2328 |
| Tests | CLEAN | frozen rule script; delta_values.py; baseline self-test and mutants; repository and docs gates | R351-2 | ce65430125a3c800138d5206dd481ba060cb2328 |
| Docs | CLEAN (SUGGESTION R351-S3 only) | full page at head; INPUTS.json normalization text; AREA_BUDGET.md:9-10; docs gates; history-number checks | R351-2 | ce65430125a3c800138d5206dd481ba060cb2328 |

## 6. Prior public review findings (read after my independent pass)

I recorded my verdict and ledger before reading any other review body for this round (`receipts/independent_verdict_before_prior_findings.txt`, 13:47:45Z). Before that I had read only my own round-1 report. I then read the [R350] round-1 review (PR comment `5856181980`). There was no round-2 review comment or PR review on #589 when I checked.

- **R351-F1 (MINOR Docs, my round 1) = [R350] F1 (MINOR Docs): CLOSED at `ce654301`.** The committed rule reproduces the committed digest `38f6c8dd...` on two fresh exports in two relocated checkouts, using a script written from the rule text and frozen before the exports. The old and new values are shown to hash the same generated text (section 2.1).
- **[R350] F2 (SUGGESTION Docs) = R351-S1: RESOLVED.** Each location it named now carries clock and pin:
  - the Provenance pin (`:30-32`, `:34-36`);
  - the standalone 8x8 BRAM (`:97-98`);
  - the critical path (`:103-105`);
  - the growth prose (`:347-349`, `:396-398`);
  - the original ranking link (`:277-279`);
  - the load-stem prose (`:386`);
  - and the remaining historical tables.
- **R351-S2 (SUGGESTION Docs, AREA_BUDGET pointer): RESOLVED** (`AREA_BUDGET.md:10`).

No other review findings exist on PR #589 or issue #587.

## 7. Real limits

- **No re-measurement.** As assigned, I did not re-synthesize. The measured figures rest on R351-1's reproduction at `55079500`. The delta changes none of them (section 2.2), and the exports at this head normalize to the same text R351-1 synthesized.
- **Environment.** The exports used the host's cached VexiiRiscv netlist and private copies of the host's patched LiteX packages at the recorded revisions. They are not a fresh generator build.
- **Executor roots.** The rebased-Tcl identity relies on the executor's checkout and build roots, which are published in the round-1 REVIEW READY comment and HANDOFF.
- **Other reviewer's script.** I did not run the other reviewer's `normalized_verilog.py` that the assignment names. I ran an independent script derived from the committed rule text.
- **Manager source-bank receipts.** The manager's source-bank receipts for this head were not present in the named public packet at `f847f343`, which holds round-1 author material, so I did not inspect them.
- **Hosted evidence.** The hosted evidence is a partial snapshot: several contexts were in progress, and the physical context was skipped.
- **Hardware.** Physical calibration was NOT RUN. All figures are synthesis estimates, with no placement, routing, bitstream or hardware result.
- **Scope of banks.** I did not run the full parent, PP, gPTP, Yosys, builder or native banks, Docker/act, or host act_ci, as assigned.

## 8. Pending manager duties

- Hosted and act acceptance at the exact head, including exact-head `verilator-suites` and `yosys-portability` evidence after the PR is marked ready (AGENTS.md section 7). Several hosted contexts were still in progress at my snapshot.
- The second positive review required by CONTRIBUTING, and confirmation that no review round remains in flight.
- Final current-dev candidate merge validation: source base `63fe4fb0`, live dev `682ecf0c`.
- Post-merge containment.
- The #229 reference-comment update after merge (acceptance 2, manager-owned).
- Closing the issue and moving the card.
- Publishing this packet.

## 9. Clone restoration

I made no edit in the reviewer clone. All exports and probes ran in disposable copies under the scratch directory, and the gates ran with bytecode writes disabled. At the end of the round:
- HEAD is `ce654301`;
- the index tree equals the head tree `91accb6f`;
- the worktree and index are clean;
- all 925 tracked non-gitlink blobs re-hash equal, and their modes match;
- the gitlinks are protocol-processor `0922e434`, gptp-processor `5dce647a` and verilog-axis `48ff7a7e`, and all three submodules are clean;
- there are 0 untracked or ignored entries.

The shared LiteX checkouts were only copied from; their revisions and dirty counts are unchanged. Receipt: `receipts/restore_verification.out`.

R351-2 FINISHED
