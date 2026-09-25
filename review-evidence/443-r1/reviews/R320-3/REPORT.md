[R320] POSITIVE - exact head b3458db0db5a7c8b15582d80b492620f05f62e70

# R320-3: merge-dev delta review of PR #561 (issue #443)

- Round: R320-3, internal independent review, cleared context.
- Exact head: `b3458db0db5a7c8b15582d80b492620f05f62e70`, tree `59769fb73ef17bdc3ffd8a2f1e9149915003837e`.
- Parents: `5beebb7c7edd908d08be34e52286c9eee441f5b3` (lane, R320-2 and R321-2 POSITIVE) and `864b36f5e9450ef64f75ca3f0d68c44330e447d7` (dev, with #508/PR #560 and PR #533 merged).
- Assignment: issue #443 comment 5831902580 (merge dev `864b36f5`, resolve `CHANGELOG.md` keeping both Unreleased entries verbatim, change nothing else, rerun the lane gates).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. All five are CLEAN at this head.
- Open BLOCKER, MAJOR or MINOR findings: none. Two prior SUGGESTIONs are retained unchanged. They are optional and do not affect coverage.

## Reconstruction order

1. `AGENTS.md` and `CONTRIBUTING.md` (sections 2, 3 and 6), then `docs/README.md`.
2. Issue #443: its body, the readiness correction, decision 5789749713 (item 4: counters and CSR state only, no STREAM_INTERRUPTED), scope 5826079535, round-2 assignment 5826779078, merge assignment 5831902580, and the three executor REVIEW READY comments.
3. Authorities: `docs/reference/REGISTER_MAP.md` (legend, claim rule, `0x800` selector, `0x8DC` section), `docs/reference/REGISTER_MAP_CLASSES.md`, and the `KL_render_setpoint` tap contract.
4. `git show --remerge-diff b3458db0`, `git diff 864b36f5..b3458db0`, and dev's own delta `0755923d..864b36f5` on every file this PR also touches.
5. Executable evidence, all reviewer-run at this head. Then the public merge-round evidence tree `review-evidence/443-r1/author-r3` at `667ec7db` and the exact-head hosted contexts.
6. Prior public review findings on PR #561 (R320-1, R321-1, R320-2, R321-2). I read these only after my own pass over the diff and my own runs.

## Merge resolution (the assignment's primary question)

- `git show --remerge-diff b3458db0` touches exactly one path, `CHANGELOG.md` (`receipts/remerge-diff.txt`). The resolution removes the conflict markers in both hunks, keeps both Contents lines and both sections, and adds one blank separator line between the two sections.
- `check_changelog_resolution.py` checks the merged file against both parents (`receipts/changelog-resolution.txt`, 10/10 PASS):
  - Both Unreleased sections and both Contents lines are byte-identical to their parents and occur once.
  - The merged file minus the render additions equals dev's file exactly.
  - The merged file minus the pin additions equals the lane's file exactly.
  - Neither section exists at the merge base `0755923d`.
- Every file changed by the merge, `git diff --name-only 864b36f5 b3458db0`, is exactly the 17-path set of `git diff 0755923d 5beebb7c`. For every one of the 17 paths, the added and removed line content is identical in both diffs. So the PR's net change against current dev is the reviewed round-2 change, re-based with no textual drift.
- Gitlinks at the head: `protocol-processor` is at `990f96526bb89356c963a260ebbdcf2a77e6623a` (dev's pin). `external`, `gptp-processor` and `third_party/verilog-axis` are unchanged. These match dev.
- `hdl/common/csr`, `tb/verilator/csr`, `hdl/ieee1722/aaf`, `render_csr_controls.py` and `render_mutants.py` are byte-identical between `5beebb7c` and `b3458db0`.

## Semantic interaction with dev (#508 / PR #560, PR #533, and the rest of `0755923d..864b36f5`)

Ten files are touched by both dev and this PR. For each one I checked whether dev's change reaches the PR's sites:

- **`hdl/milan/milan_datapath.sv`.** Dev's edits cover three sites, all disjoint from this PR's three sites (`:1202` declaration, `:2589` port connection, `:6163-6167` packing):
  - the GET_STREAM_INFO answer block (selectors 4, 5 and 7 handed to the processor);
  - the CRF `rate_valid` net into the servo;
  - admission-round comments.

  No dev edit touches `rsp_*`, `KL_render_setpoint` or the `milan_csr` instance. The front-end gate reports zero first-party findings, so the declaration-before-use ordering holds at the merge.
- **`tb/verilator/milan_dp/sim_aclk.cpp`.** Dev adds `start_the_boot_restore_walk()` (`:1224`) and calls it from the ACMP bind helper (`:1252`). Since processor pin `a8f8ce81`, the listener serves nothing until that walk ends.
  - The PR's positive leg and its absent-stage control both bind through that helper. The merge therefore gains one check in each: aclk 189 to 190, clean control 63 to 64, absent control 32 to 33.
  - At this head the absent control shows `[RENDER-BIND] PP_STAT[2] the restore walk sequenced = 1` and `RENDER-CSR-ABSENT: ingress accepted media = 1` before its structural-zero reads. Its "despite accepted ingress" premise therefore still holds on the new pin (`receipts/render_csr_controls.log`).
- **`tb/verilator/milan_dp_render/sim_tdm8_render.cpp`.** Dev reworks the multi-stream boot helper and adds the restore walk. The PR's `RENDER-CSR-MULTI` checks (`:3304-3320`) print nothing when they pass, so I proved they still execute: the index-alias mutant `multi_alias_idx0` fails `RENDER-CSR-MULTI: flushed listener 1 has empty prefill` (got 12, expected 256) and `first absent index reads zero`. The clean two-listener leg passes 65/0 (`receipts/probes.log`).
- **`tb/verilator/milan_dp/Makefile`.** Dev adds `NOTIFY_BUILD`, `notify` and `gsi-mutants`, and rewrites the `.PHONY` list. The PR's `CSR_SRC ?=` (`:112`), its use in `SRCS` (`:200`) and `render-csr-controls` (`:434-436`) survive intact. The `CSR_SRC` override still reaches both the aclk recipe and the `milan_dp_render` recipe through `print-srcs`: the bit-9 mutant and my index-alias mutant are both elaborated from it and both caught.
- **Dev's #508 seam at the merged datapath.** `obj_notify` (timed notify and `[GSI]`) passes 381/0 at this head (`receipts/milan_dp_notify_run.log`). The first attempt, `receipts/milan_dp_notify.build-and-invocation-error.log`, is my own invocation error: the recipe prefixes `./` to `NOTIFY_MDIR`, and I passed an absolute path. The build had succeeded. The rerun executed that built binary unchanged.
- **Docs.** `docs/reference/REGISTER_MAP.md`: dev edits `CRF_RATE`, the published-round wording and the `PP_CTRL[1]` restore_go row, and claims no address. `0x8DC` is claimed once (`:203`, `:242`, `:1825-1826`, `:1946-1997`), and `0x8E0` to `0x8F4` stay unmapped. The other docs:
  - `docs/testing/TESTING.md`: dev's `gsi-mutants` row sits next to the PR's `render-csr-controls` row (`:265`), with no conflict.
  - `tb/verilator/milan_dp/README.md`: dev's dated count table states that "No count is inferred for their merged tree". It makes no current-count claim that the merge falsifies.
  - `docs/design/TIME_SYNC.md`: the edits are in different sections.
  - `scripts/measure_test_evidence.py`: the PR's disposition (`:631`) coexists with dev's entries, and `--check` passes.
- **VERSION.** `milan_csr.sv:196` stays `32'h0002_0060`. Both Unreleased entries defer the bump to the release step, consistently.

## Independent evidence (reviewer-run at this head, pinned simulator 5.050 verified by `--version`, at most 8 jobs)

| Check | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/csr` | 380/0, 380/0, 115/0, 38/0, 380/0; all 8 `RENDER_STAT` checks and the `0x8E0` neighbour OK; rc 0 | `receipts/csr.log` |
| `make -C tb/verilator/milan_dp aclk` | 190/0, including all `RENDER-CSR` phases (prefill 0x100, filling 0x106 with prefill held, converged 0x208, rail, selection, reset) and dev's restore-walk check; rc 0 | `receipts/milan_dp_aclk.log` |
| `make -C tb/verilator/milan_dp render-csr-controls` | clean 64/0; wrong-fill caught at `RENDER-CSR: filling mirrors taps` (got 256, expected 262); bit-9 caught at `RENDER-CSR: bit 9 preserves talker rejection` (got 65549, expected 0); absent-stage 33/0; `4 checks, 0 failures`; rc 0 | `receipts/render_csr_controls.log` |
| `make -C tb/verilator/milan_dp_render` | shipping 152/0, two-listener 65/0, existing controls 5/5; rc 0 | `receipts/milan_dp_render.log` |
| Reviewer mutation probes (`probes.py`) | 4/4 as expected. `multi_clean` 65/0. `multi_alias_idx0` caught by the named multi-listener checks. `aclk_rails_zero` caught at `rail event reached the word` and `rail mirrors taps`. `aclk_flag_swap` (prefill and converged swapped) caught at `prefill mirrors taps` and `prefill still held` | `receipts/probes.log`, `receipts/probe-*.log` |
| `obj_notify` (#508 `[GSI]` and notifications, timed) | 381/0; rc 0 | `receipts/milan_dp_notify_run.log` |
| `docs_check.py`, git mode and filesystem-walk mode | 0 findings in each mode; rc 0 with and without the locked renderer | `receipts/docs_check_*.log` |
| `gen_toc.py --verify-anchors` and `--check` | rc 2 without the locked renderer (a missing-dependency refusal, recorded). With `tools/markdown/requirements.txt` installed hash-locked into a disposable environment under scratch: 176 cross-page anchors reproduced, and the TOC gate OK; rc 0 | `receipts/gen_toc_*.log`, `receipts/md_venv_install.log` |
| `measure_test_evidence.py --check` | runner evidence contract OK; ratchet PASS; rc 0 | `receipts/measure_test_evidence_check.log` |
| `check_em_dash.py --base 864b36f5`, doc style, doc paths, `git diff --check 864b36f5 b3458db0` | rc 0 each (0 em-dash findings over 109 added lines in 7 pages) | `receipts/check_*.log`, `receipts/git_diff_check.log` |
| SV, C++ and Python idiom gates; `xvlog_gate.py --check` | rc 0; front end 0 first-party findings, 4 pinned-processor findings equal to the ratchet | `receipts/check_*_idiom.log`, `receipts/xvlog_gate_check.log` |
| Exact-head hosted contexts (inspected, not owned) | `rtl-fast`, `full-ci-gate`, docs, lint, elaborate, bdd, wire-accountability and Yosys shards 0-3 succeeded; Verilator shards 0, 2 and 3 succeeded; **shards 1/5 and 4/5 were `in_progress` at 13:04:46Z**; Physical gPTP was **skipped** (not executed, not hardware proof) | `receipts/hosted_check_runs.tsv` |
| Clone restoration | HEAD and tree exact; index equals HEAD; 892 tracked blobs match in bytes and mode; gitlinks match (`external` uninitialized, as at start); 0 untracked or ignored entries | `receipts/restore-verification.txt` |

The public merge-round evidence (`review-evidence/443-r1/author-r3` at `667ec7db`) agrees with these counts: `final-gate-results.json` all rc 0, and `merge-verification.log` shows both sections retained. The manager's source static, builder and native banks are cited as passed. I did not re-run them. That is outside this round's allowance.

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

Retained SUGGESTIONs, both optional. They do not affect coverage.

- **S-A (R320-2 S2-residual), SUGGESTION, Tests.** `hdl/milan/milan_datapath.sv:6163-6167`. No integration leg reaches 256 rails, so a datapath packing that dropped `rsp_rails_w[15:8]` would stay green. The CSR half is graded by the CSR bench's full-width `0xffff0100` read. The packing lines are byte-identical to `5beebb7c`. My `aclk_rails_zero` probe ties all 16 bits, so it does not close this.
  - Optional outcome: a check at the datapath port with bit 8 or higher set.
  - Verification: an upper-byte-only mutant fails by name.
- **S-B (R321-2 S1), SUGGESTION, Tests.** `tb/verilator/csr/sim_main.cpp`, the neighbour reads in `reserved_inert_csr_gap()`. These run while `i_render_status` is tied to zero, so a decode aliasing `0x8E0` to `RENDER_STAT` would survive. The file is byte-identical to `5beebb7c`.
  - Optional outcome: repeat the neighbour reads while the input is driven non-zero.
  - Verification: an `0x8E0` alias mutant fails by name.

Out-of-scope observation, not a finding against this PR: in dev's `tb/verilator/milan_dp/Makefile`, the `notify` recipe runs `./$(NOTIFY_MDIR)/Vmilan_dp_notify`, so an absolute `NOTIFY_MDIR` override fails to run. The in-tree callers use relative paths. If the manager wants this tracked, it belongs in a separate Issue.

## Prior public findings, resolved or retained at this head

| Prior finding | Status at `b3458db0` | Evidence at this head |
|---|---|---|
| R320-1 F1 = R321-1 F1 (CSR bench asserted `0x8DC` unmapped) | RESOLVED | `receipts/csr.log`: `-- RENDER_STAT (0x8DC) --` has 8 driven checks in each N=1 variant, and the `0x8E0` neighbour is still unmapped. Bench file unchanged since `5beebb7c` |
| R321-1 F2 (`STRM_SEL[9]` not graded) | RESOLVED | The bit-9 mutant is caught by name in `receipts/render_csr_controls.log`, and `RENDER-CSR: bit 9 preserves talker rejection` passes in the positive leg |
| R321-1 F3 (campaign missing from `TESTING.md`) | RESOLVED | `docs/testing/TESTING.md:265` |
| R320-1 F2 = R321-1 F4 (no VERSION step or recorded deferral) | RESOLVED | `CHANGELOG.md:32-40`, `REGISTER_MAP.md:1946-1997`, `milan_csr.sv:196` at `0x0002_0060`; decision comment 5826779078 |
| R320-1 F3 = R321-1 F5 (group index lacks `0x8DC`) | RESOLVED | `docs/reference/REGISTER_MAP.md:242` |
| R320-2 S2-residual | RETAINED as S-A (SUGGESTION) | Lines unchanged |
| R321-2 S1 | RETAINED as S-B (SUGGESTION) | File unchanged |

None of these was moved to another Issue.

## Per-lens results

- `[R320] PASS Conformance` at the head. Evidence:
  - Acceptance items 1, 2, 3 and 5 hold on unchanged RTL and docs.
  - Item 4 follows decision 5789749713: the diff adds no STREAM_INTERRUPTED wiring. Its 4 mentions are documentation "does not raise" statements.
  - `grep` finds 0 stale `#390` render pointers.
  - The merge assignment 5831902580 is met exactly: a CHANGELOG-only resolution, both entries verbatim (`receipts/changelog-resolution.txt`).
  - VERSION stays `0x0002_0060` under the recorded deferral.
- `[R320] PASS RTL` at `milan_csr.sv:437,922,2389-2395,2561`, `milan_datapath.sv:1202,2589,6163-6167`, and `KL_render_setpoint.sv` (identical to `5beebb7c`). Checked:
  - Dev's datapath edits (GSI selectors, CRF `rate_valid`, comments) are disjoint from the PR sites.
  - Widths still hold: `N_LISTENERS_P = N_STREAMS` at `milan_datapath.sv:2353`, and rails are 16 bits.
  - The same `aclk` domain is used, with no new crossing.
  - The front end reports 0 first-party findings, and the SV idiom gate is clean.
- `[R320] PASS Robustness` at `sim_aclk.cpp:367-440` and `render_csr_controls.py`, at this head. Checked:
  - Absent stage reads structural zero under accepted ingress on the new pin.
  - Talker, bit-9 and out-of-range selections read zero; writes are ignored.
  - RVALID and RDATA hold under backpressure.
  - Rail and convergence clear on reset; the CSR bench's full-width saturated rails hold.
  - The absent-index read in the two-listener leg is zero.
- `[R320] PASS Tests` at `sim_aclk.cpp`, `sim_tdm8_render.cpp:3304-3320`, `render_csr_controls.py`, `Makefile:112,200,434-436` and `measure_test_evidence.py:631`. Checked:
  - Re-run at this head with the counts above.
  - Both campaign mutants and 3 reviewer mutants fail by name, which proves the merged-in boot changes did not bypass the PR checks.
  - `measure_test_evidence --check` passes.
  - S-A and S-B are optional.
- `[R320] PASS Docs` at `CHANGELOG.md:11-12,32-70`, `REGISTER_MAP.md:203,242,1825-1826,1946-1997`, `REGISTER_MAP_CLASSES.md:107`, `TESTING.md:265`, `AAF_LATENCY_TAPS.md:96`, `TIME_SYNC.md:342`, `tb/verilator/milan_dp/README.md:889-911`, and the PR #561 body. Checked:
  - Consistent with dev's concurrent edits.
  - Both `docs_check` modes pass.
  - Anchors are verified with the locked renderer, and the TOC, em-dash, style and path gates pass.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #443 body and decisions 5789749713, 5826079535, 5826779078, 5831902580; remerge diff; `changelog-resolution.txt`; `milan_csr.sv:196`; the 17-path identity with the round-2 change | R320-3 | `b3458db0db5a7c8b15582d80b492620f05f62e70` |
| RTL | CLEAN | `milan_csr.sv:437,922,2389-2395,2561`; `milan_datapath.sv:1202,2353,2589,6163-6167` plus dev's datapath delta; `xvlog_gate_check.log`; `check_sv_idiom.log` | R320-3 | `b3458db0db5a7c8b15582d80b492620f05f62e70` |
| Robustness | CLEAN | `sim_aclk.cpp:367-440,1224-1252`; absent-stage control log; CSR bench `RENDER_STAT` section; two-listener absent-index check | R320-3 | `b3458db0db5a7c8b15582d80b492620f05f62e70` |
| Tests | CLEAN (S-A, S-B optional) | csr, aclk, controls, render and notify logs; `probes.log`; `render_csr_controls.py`; `Makefile:112,200,434-436`; `measure_test_evidence_check.log` | R320-3 | `b3458db0db5a7c8b15582d80b492620f05f62e70` |
| Docs | CLEAN | `CHANGELOG.md`, `REGISTER_MAP.md`, `REGISTER_MAP_CLASSES.md`, `TESTING.md`, `AAF_LATENCY_TAPS.md`, `TIME_SYNC.md`, `milan_dp/README.md` at the cited lines; PR body; doc gate logs | R320-3 | `b3458db0db5a7c8b15582d80b492620f05f62e70` |

## Real limits

- I did not run these; they were outside this round's allowance:
  - the full `milan_dp` default sweep, the parent, PP and gPTP banks, the builder, and Yosys cell counts;
  - act, Docker, host act_ci and its selftest;
  - hardware.

  The item-5 cell counts were recorded at `c9bbb03`. The merged datapath now also carries dev's RTL, so a merged-tree count is the manager's candidate-build concern and not a claim of this round.
- Physical calibration was NOT RUN, and builder gate 11 was previously NOT RUN. The skipped Physical gPTP context is not hardware proof.
- Hosted Verilator shards 1/5 and 4/5 were still in progress when I queried them. I make no claim about their outcome.
- The Markdown renderer dependency was installed only into a disposable environment under scratch, from the hash-locked `tools/markdown/requirements.txt`. The runs without it are recorded as rc 2.
- Receipts and scripts had local paths replaced by the placeholders `$CLONE`, `$PACKET`, `$PIN_BIN`, `$HOME` and `$WORK`, and the commit-author line in the remerge receipt replaced by a placeholder. `run_gate.sh` now requires `PIN_BIN` instead of embedding a local default. Its behaviour is otherwise unchanged from the runs recorded here. `verify_restore.sh` was corrected twice before its recorded run: once for `ls-tree` field parsing, once for detecting an uninitialized submodule. Only the passing run is recorded.
- This is a delta review. The PR's RTL, CSR bench and controls are byte-identical to `5beebb7c`, where R320-2 and R321-2 were POSITIVE. My lens coverage above was nonetheless applied at this exact head.

## Pending manager duties

- Hosted and act acceptance at this exact head, including the two in-progress Verilator shards.
- The final current-dev candidate build at the merge turn. The source base is `864b36f5`. Live dev was `864b36f5` when this round was assigned; recheck it at the merge turn.
- Publication of this report and its manifest.
- Confirming the two-positive bar: this round, plus R321-2 on the ancestor per assignment 5831902580.
- Post-merge containment, and closing issue #443 and moving it to Done.
- A merge requires explicit maintainer authorization.

R320-3 FINISHED
