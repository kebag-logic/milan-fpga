[R383] POSITIVE - exact head f5f42bde2a2bf6651693644aa6e6d2d524c5bc95

# R383-4 composition review: issue #607 / PR #615 on merge-train candidate C_602

Round: R383-4 (composition acceptance only). Reviewer: [R383], independent of the lane.
Candidate: `f5f42bde2a2bf6651693644aa6e6d2d524c5bc95`, tree `087d79a481c34a48d784a98142fac4dbd0c54b50`.
Parents: C_602 `a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c` (dev `7390b436` + #595 PR #614 + #602 PR #603) and PR #615 source head `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5`.

**Verdict: POSITIVE.** The composed tree introduces no defect beyond the reviewed sources.
No BLOCKER, MAJOR or MINOR finding. I raise no new SUGGESTION.
All five lenses were applied at this exact head and are CLEAN.

Paths in receipts are rewritten to `$CLONE`, `$PACKET`, `$HOME` and `$DATA`.
Every receipt named below is listed in `MANIFEST.sha256`.

## 1. Reconstruction

I read these in order:

- AGENTS.md, CONTRIBUTING.md (section 7 candidate validation, section 6 documentation rules), and docs/README.md.
- Issue #607 body, acceptance 1-4 and the manager's decisions. These are the assignment and round 2/3/merge-dev comments, and the gitlink disposition.
- REQ-VER-02/03/04 in REQUIREMENTS.md.
- `.github/workflows/elaborate.yml` and `docs.yml`, which define the hosted dependency set and the Markdown gates.
- The diff and history, then public evidence. That covers the round-1 packet at `bae7b082` and the manager's round-state comment 5878033579.

I read the prior review findings only after the checks in sections 2-5 were done (see section 6).

## 2. Composition structure (receipts 00, 01, 02, 03_*)

- **Base identity.** Dev `7390b436` and the #395 train candidate `0ba810fe` have the same tree, `702a78ea…`. So C_602 is live dev plus #595 and #602 by content, even though `7390b436` is not an ancestor of C_602.
- **The candidate is the clean merge.** I recomputed `git merge-tree --write-tree a3f95a4c c7ee5cbd` and got `087d79a4…`, which equals the candidate tree. No hand edit rides in the merge commit.
- **Overlap: exactly one file.** #607 (dev..c7ee5cbd) and the predecessors (dev..C_602) both touch only `sw/builder/test_builder.py`.
  - Every other #607 file is blob-identical to the source head: 11 files.
  - Every other predecessor file is blob-identical to C_602: 25 files.
- **The #607 hunk in the shared file is unchanged.** candidate-vs-C_602 on `test_builder.py` has the same +/- lines as source-vs-dev (receipt 03_hunk_equality).
  - The #607 hunk sits at `test_builder.py:27797-27803` and in the run list at `:27827`.
  - The predecessor hunks are at `:10714-16651` and `:25544-25810`, which is #595's quoted-hex declarations and #602's restart census.
  - The two sets of hunks share no lines.
- **Gitlinks** are identical at source and candidate: `protocol-processor` `c951a9ff`, `gptp-processor` `5dce647a`, `verilog-axis` `48ff7a7e`, `external` `efeb541a`.

## 3. Semantic interaction checks

**Run list and gate namespace (receipt 04, `runlist_audit.py`).**
- At the candidate: 309 top-level functions with no duplicate definition. The run list has 96 entries, with no duplicate and no unresolved name.
- Dev..candidate adds only `test_clock_crossing_constraints`. The relative order of all 95 dev entries is preserved.
- Positions: `test_commercial_timing_grade` (#395) 0, `test_declaration_contracts` (#595) 5, `test_clock_crossing_constraints` (#607) 6, `test_all_configs_build` 7.
- #607's only skip label is `"607 clock constraints"`. It appears once among the file's 13 `_litex_or_skip` calls.

**Every arm runs exactly once, in order (receipts 10/12/13 `_arms.txt`, `arm_count.py`).**
- In all three banks, each of the 96 entries prints exactly once, in run-list order.

**No hidden prerequisite.**
- #607's arm performs its own `eb.build` for each shipping configuration.
- On fresh scratch clones (`src-c7ee`, `src-f5f4`, with no prior outputs), its first execution passed (receipt 30).
- It therefore does not depend on `test_all_configs_build` or on #595's arm running first.

**Shipping emission is unchanged by the predecessors (receipts 30, 30_emission/, 31, `compare_shipping_emission.sh`).**
- I ran #607's own real-Builder probe for `ax7101_1x1_tdm8` and `ax7101_8x8`, on e1 and e2, in scratch clones of the source head and the candidate.
- After path normalisation, all 8 emitted `alinx_ax7101.tcl`/`.xdc` pairs are **byte-identical** between `c7ee5cbd` and `f5f42bde`.
- Candidate emitted Tcl order, identical for all 4 builds:

| Line | Command | Placement |
| --- | --- | --- |
| 258 | `synth_design` | |
| 269-271 | `source clock_constraints.tcl`, `kl_quasi_static_constraints`, `milan_eth_constraints eth_clocks<n>_rx [list milansoc_crg_clkout0 milansoc_crg_clkout1] …` | after synthesis |
| 275 | `opt_design` | after the hooks |
| 280 | `kl_timing_grade_configure … {commercial} {0} {85} {Slow Fast}` | before placement |
| 284 | `place_design` | |
| 303 | `route_design` | |
| 314 | `kl_timing_grade_reports alinx_ax7101_signoff` | after routing |
| 325 | `write_bitstream` | after the reports |

- The shipping XDCs contain no `mr_ff` line.

**#595 × #607 (probe P1, receipt 50).**
- Unquoting the shipping `platform.mac_address` makes #607's shipping arm fail with rc 1. The refusal is #595's "quote the hexadecimal value as a YAML string" (`endstation_builder.py:3193`), not a skip.
- #607's arm therefore sits on #595's stricter config path. At the candidate the shipping configs satisfy that path; control P0 is rc 0.

**#602 × #607 (probe P2, receipts 07, 50).**
- #602's RTL delta:
  - removes `media_rebase_p_w` from `mcr_restart_p_w` (`milan_datapath.sv:3133`);
  - rewrites comments in `KL_media_clock_restart.sv`.
- It is a single-domain combinational change. It touches no `quasi_static`, `mr_ff`, `ASYNC_REG` or clock object.
- With both #602 RTL files reverted to dev bytes, the emitted shipping Tcl/XDC are identical to the candidate's.
- So nothing in #602 alters what #607's hook, scoping or refusal read.
- Relative to `c7ee5cbd`, the candidate adds no constraint, clock or build-flow change. The only non-test, non-doc changes are those two RTL files and #595's `endstation_builder.py` validation (receipt 01).

**Probe checks.**
- P3 shows the run-list audit flags both a duplicated #607 arm and a missing #595 arm in a scratch copy.
- P1-P3 ran in a disposable scratch clone. Afterwards it reported 0 modified paths.

## 4. Gate results at the candidate (all rc 0)

| Gate | Result | Receipt |
| --- | --- | --- |
| Full builder bank `test_builder.py --require-rv32 --require-elaboration` (bench LiteX interpreter; pinned sv2v v0.0.12 and Verilator 5.050 first on PATH) | rc 0, 763 s. `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, the historical Arty calibration report, absent here). 96/96 arms. 4 `[constraints] shipping … PASS` lines | 10_* |
| Pins-only bank, same command, with no `MILAN_LITEX_PYTHON`. Fresh Python 3.12.13 venv with an isolated HOME, set up as elaborate.yml does: `pyyaml` plus exactly `sw/litex/litex_pins.txt`, `ci_litex_env.py`, `apply.sh`, and the pinned RV32 SDK (digest verified). `pythondata_software_picolibc` and `_compiler_rt` are absent | rc 0, 632 s. Same verdict and not-run arm. 96/96 arms. 4 shipping PASS lines. No ImportError or traceback | 11_*, 12_* |
| Compiler-absent bank: the three RV32 candidates refused in-process, `--require-elaboration` kept (`run_builder_absent.py`) | rc 0, 543 s. `EXCEPT 2 NOT RUN`: gate 1b, the compiled CSR census, is recorded unavailable, plus gate 11. 3 compiler launches refused. 96/96 arms. 4 shipping PASS lines | 13_* |
| `test_declarations.py`, `test_timing_grade.py <py>`, `test_shipping_clock_constraints.py`, `test_clock_constraints.py`, on the candidate clone | rc 0 each, in the bench interpreter and again in the pins-only environment. Each shipping or constraints run prints 4 shipping PASS lines | 40_* |
| Markdown gates in a hash-locked `tools/markdown/requirements.txt` venv (plus `pyyaml` and `wavedrom==2.0.3.post3`, as docs.yml installs them) | 34 commands rc 0 (table below) | 06_*, 20_static_gates.tsv, static_logs/ |

Markdown and static gates, all rc 0:

- **Wording and em dash.**
  - `docs_check.py`: 0 findings over 174 md files and 930 scrubbed files.
  - `check_em_dash.py --base a3f95a4c`: 0 findings over 68 added lines in the 4 pages #607 changes.
  - `check_em_dash.py --base 7390b436`: 0 findings over 257 lines in 19 pages.
- **Contents and anchors.**
  - `gen_toc.py --selftest`, `--verify-anchors` (238 cross-page fragments) and `--check` (116 pages).
- **Documentation structure.**
  - `check_doc_style` and its selftest, `check_gptp_docs`, `DOC_MAP.gen.py --check`.
  - `check_solution_docs`, `check_submodule_docs`, `check_diagram_pngs`, `check_archive`, `check_feature_status`.
- **Source and RTL lists.**
  - `check_baremetal_only --check`, `check_soc_sources` and its selftest, `check_rtl_source_lists`, `check_port_contracts`.
- **Ratchets and idiom checks.**
  - `measure_naming --check`, `measure_fail_fast --check`, `measure_test_evidence --check`, `check_hygiene --check`.
  - `check_todo_ownership`, and the idiom checks for SV, C++, Python and shell.
- **CI inventory.**
  - `ci_events.py --check` (1655 contract items) and `--selftest`.
- **Other.**
  - `check_nvm_record_space`, `check_wire_accountability --self-test`, `iob_pack_selftest`.

**Cross-lane links.**
- #607's new doc lines link only to BUILDING section 5, `clock_constraints.tcl` and issue #395. No predecessor changes any of those, and no predecessor changes a heading.
- The anchors verify, per `gen_toc.py --verify-anchors`.

**Clone restoration (receipt 90).**
- HEAD is `f5f42bde…`. The index tree equals `087d79a4…`, and the index and HEAD have the same mode+blob digest.
- There are no tracked modifications.
- The submodule checkouts equal their gitlinks and are clean.
- Only gitignored build outputs and `__pycache__` remain.

## 5. Findings

None at BLOCKER, MAJOR, MINOR or SUGGESTION severity from this round.

## 6. Prior public findings on PR #615, status at this head

I read these after sections 2-5 were done.

| Finding | Severity; lenses | Status at `f5f42bde` |
| --- | --- | --- |
| R382-1 F1 / R383-1 F1 (no check that the shipping build installs the Ethernet hook) | MINOR; Tests (+Robustness) | **Resolved and still resolved.** The shipping arm runs and passes in all three candidate banks (receipts 10/12/13). The candidate emission is byte-identical to the source's (receipt 30) |
| R382-2 F2 / R383-2 F2 (shipping arm needs a firmware data package absent from the pins) | BLOCKER; Conformance, Tests, Robustness | **Resolved and still resolved.** The candidate pins-only bank passes, with picolibc and compiler-rt absent (receipts 11/12) |
| R382-1 S1-S4, R383-1 S1-S2 | SUGGESTION | Taken at `a9f5e34f` as dispositioned. The composition does not touch those files |
| R382-3 S1 (XDC clock-group line order differs across interpreter paths) | SUGGESTION; Docs | **Retained** as an optional evidence note. The composition does not change it; candidate and source emissions are identical under one interpreter |
| R382-4 S1 (shipping probe does not also assert #395's configure/report positions) | SUGGESTION; Tests | **Retained**, and the manager has routed it to the #495 checklist. At this head the positions are correct in the emitted Tcl (receipt 31) |
| R382-4 S2 (merge-dev packet at a doubly nested path) and S3 (forward pointer from the #395 finding) | SUGGESTION; Docs | **Retained**, dispositioned by the manager (comment 5878033579). The composition does not affect them |

No open BLOCKER, MAJOR or MINOR remains from any prior round.

## 7. Clean-lens results

```text
[R383] PASS Conformance - f5f42bde test_builder.py:27797-27803,27827; emitted alinx_ax7101.tcl:258-325 (receipts 30, 31); banks 10/12/13 - #607 acceptance 3 wiring and REQ-VER-03 shipping elaboration hold in the composed tree: arm present once, 4 shipping PASS in bench, pins-only and compiler-absent banks; Ethernet hook between synth_design and opt_design; #395 configure before place_design and reports after route_design; XDC has no mr_ff line
[R383] PASS RTL - receipt 07 (dev..C_602 hdl diff), milan_datapath.sv:3133, sw/litex/clock_constraints.tcl, receipts 30 and 50 P2 - #602's RTL is a same-domain combinational removal with no quasi_static/mr_ff/clock change; emitted Tcl/XDC identical with #602 RTL reverted and identical to source head; no constraint, clock or build-flow change relative to c7ee5cbd
[R383] PASS Robustness - receipts 12 (pins-only, firmware data packages absent), 13 (RV32 compilers absent), 50 P1 (unquoted shipping mac_address) - composed tree passes the hosted dependency set and the compiler-absent configuration; a predecessor-validation refusal on the shipping path turns #607's arm red (rc 1) rather than skipping
[R383] PASS Tests - test_builder.py run list at f5f42bde (receipt 04), bank arm counts (10/12/13 _arms.txt), standalone tests (40_*), probe P3 (audit sensitivity) - 96 entries, no duplicate definition or entry, dev order preserved, each lane's arm executes exactly once in order in all three banks; #595, #395 and #607 standalone tests rc 0 in both environments
[R383] PASS Docs - receipt 20_static_gates.tsv and static_logs/ at f5f42bde - no doc file shared between lanes; docs_check, em-dash against both C_602 and dev bases, gen_toc selftest/verify-anchors/check, doc_style, DOC_MAP, ci_events check/selftest and the remaining docs.yml static gates all rc 0 in the hash-locked Markdown environment
```

## 8. Reviewer-owned completion ledger

This round checks the composition only. The source-level coverage it relies on is:

- [R382] R382-4, POSITIVE at `c7ee5cbd` (comment 5878000673);
- [R383] R383-3, POSITIVE at ancestor `a9f5e34f` (comment 5871377940).

The merge-dev delta `a9f5e34f..c7ee5cbd` is covered by R382-4. The composition touches every lens's scope in the way described above, so each lens was re-applied here.

| Lens | Status | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | test_builder.py:27797-27827; emitted shipping Tcl/XDC (4 builds); banks 10/12/13 | R383-4 (composition); source: R382-4, R383-3 | f5f42bde2a2bf6651693644aa6e6d2d524c5bc95 |
| RTL | CLEAN | dev..C_602 hdl diff; milan_datapath.sv:3133; clock_constraints.tcl; emission identity and P2 | R383-4 (composition); source: R382-4, R383-3 | f5f42bde2a2bf6651693644aa6e6d2d524c5bc95 |
| Robustness | CLEAN | pins-only bank; compiler-absent bank; P1 | R383-4 (composition); source: R382-4, R383-3 | f5f42bde2a2bf6651693644aa6e6d2d524c5bc95 |
| Tests | CLEAN | run-list audit; per-bank arm counts; 4 standalone tests in 2 environments; P3 | R383-4 (composition); source: R382-4, R383-3 | f5f42bde2a2bf6651693644aa6e6d2d524c5bc95 |
| Docs | CLEAN | 34 docs/static gates; cross-lane link/anchor check | R383-4 (composition); source: R382-4, R383-3 | f5f42bde2a2bf6651693644aa6e6d2d524c5bc95 |

## 9. Real limits

- **No vendor run.** There was no Vivado run, sweep or live wrong-name control at the candidate. The timing tables (A427 re-sweep) describe the `c7ee5cbd` netlist.
  - The candidate adds #602's small combinational RTL change, so its placement is not measured.
  - The Tcl/XDC inputs are proven identical.
  - The next shipping image build carries #395's corner signoff, with #607's `12-4739`/`20-1307`/`12-5201` refusal active (`milan_soc.py:3966`).
- **Gate 11 not run.** It is the historical Arty calibration report, absent in every bank. Gate 1b is not run in compiler-absent mode by design.
- **Local tools and interpreters.**
  - The bench bank used the bench LiteX interpreter (Python 3.14.7). The pins-only bank used Python 3.12.13, with sv2v v0.0.12 (sha-checked) and Verilator 5.050.
  - The Verilator path named in the assignment does not exist. I used an identical wrapper, which reports `Verilator 5.050 2026-07-01 rev v5.050` and matches the other manager candidates' wrapper byte for byte (receipt 05).
  - The pins-only environment was built locally with network access. It is not the hosted runner.
- **Hosted evidence is for the source head only.**
  - Hosted checks exist for PR head `c7ee5cbd` only: all success, and the physical gPTP job skipped (receipt 60).
  - The candidate `f5f42bde` has no hosted or act run from this round.
- **Not hardware proof.** Physical calibration was not run, and field skips are not hardware proof.

## 10. Pending manager duties

- Act and hosted acceptance for the merge candidate, including the exact-head `elaborate` job.
- Rebuild the candidate if live dev or the train moves beyond C_602 `a3f95a4c` before merge. This verdict covers tree `087d79a4` only.
- Merge only with maintainer authorization, then run post-merge containment (`check_merge_containment.py`, `check_merge_review_integrity.py`).
- Carry R382-4 S1 and S3 to the #495 checklist as announced. Link the merge-dev packet (R382-4 S2).
- The next shipping image build carries the timing signoff and the refusal gate.

R383-4 FINISHED
