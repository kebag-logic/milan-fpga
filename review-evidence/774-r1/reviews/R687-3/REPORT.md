[R687] POSITIVE - exact head f8775f7b92b1ceff106ebb02b0e2f4ca48972ad7

# R687-3: internal cleared-context review of PR #778 (issue #774), round 3 delta

Head `f8775f7b92b1ceff106ebb02b0e2f4ca48972ad7`, tree `8d057d8471c2138dc8c375dbc0027cd55b1a309f`.
The delta is one manager merge commit, `01fc5475..f8775f7b`. It merges dev `ae255ead` (PR #779 for #773, PR #782 for #781, PR #777 for #775) into `774-crf-tspec-max-frame`. The merge base is `a032c6d6`.

Verdict: POSITIVE. The delta has no BLOCKER, MAJOR or MINOR finding. All five lenses are CLEAN at this exact head. There is one RESIDUE (PR body wording) and two new optional SUGGESTIONs. The R687-1 and R687-2 suggestions are retained.

## 1. What the merge is

- **The recorded tree is the plain three-way auto-merge plus one hand resolution.** `git merge-tree --write-tree 01fc5475 ae255ead` reports one conflict, `CHANGELOG.md`. It auto-merges `KL_crf_tx.sv`, `milan_datapath.sv`, `TESTING.md` and `MILAN_COMPLIANCE_MATRIX.md`. The recorded tree differs from that auto-merge in `CHANGELOG.md` only, where the conflict markers are removed and one blank separator line is added. Receipt: `receipts/compose_check.txt`, script `scripts/compose_check.sh`.
- **Each side's hunks are carried verbatim.** For each of the four auto-merged files, the added and removed lines of `a032c6d6..01fc5475` equal those of `ae255ead..f8775f7b`, and those of `a032c6d6..ae255ead` equal those of `01fc5475..f8775f7b` (`compose_check.txt`).
- **CHANGELOG: nothing is lost.**
  - `## Unreleased - per-source TSpec` (this PR) is byte-identical to its text at `01fc5475`.
  - `## Unreleased - talker capture-to-wire latency` (#773) is byte-identical to its text at `ae255ead`.
  - Line counts add up: base 889, +14 from the branch, +18 from dev, head 921.
  - Every Contents line of each side is present at the head. This PR's entry sits above #773's, both in Contents (`CHANGELOG.md:11-12`) and in the body (`:48`, `:61`).
  - Both anchors (`#unreleased---per-source-tspec`, `#unreleased---talker-capture-to-wire-latency`) are reproduced by `gen_toc.py --check --verify-anchors` (rc 0).
- **The merge adds no source line of its own.** `ae255ead..f8775f7b` touches exactly this PR's 20 files (`receipts/delta_scope.txt`). The trees of `hdl/ieee1722/avtp`, `tb/verilator/avtp_rxmon`, `tb/verilator/capture_coherence`, `tb/verilator/crf_rx`, `tb/verilator/media_phase`, `scripts` and `.github` are identical to `ae255ead`.

## 2. Findings

### R687-3-R1 RESIDUE - Docs - PR #778 body, "Status" and "Contents" - the body still describes head `01fc5475`

- **Evidence:** the body's Status reads "GREEN at `01fc5475` (round 2)". Its Contents end at "Round 2". It names neither `f8775f7b` nor the dev merge, although the PR head is `f8775f7b` (`gh pr view 778`, `headRefOid`).
- **Why RESIDUE:** this is purely PR-body wording. Every figure in it is stated for the head it names, and no measurement, verdict, test or code changes.
- **Exact fix:** add one line under Status and a matching Contents entry: "Head `f8775f7b` merges dev `ae255ead` (PR #779 for #773, PR #782 for #781, PR #777 for #775) into this branch. The one conflict, `CHANGELOG.md`, keeps both Unreleased entries; every other file is the automatic merge. The figures above are at the heads they name; the merge candidate is validated at the merge turn."

### R687-3-S1 SUGGESTION - Tests - `scripts/suite_shards.py:162` (`PIECE_SECONDS["milan_dp"]`) - the registered leg figures no longer match the partition

- **Evidence:** this PR's `tspec8` case is tenth in `make ci-list`'s 22 names (`receipts/milan_dp_ci_list.txt`). `partition()` takes `names[i::4]`, so every case after it changes leg (`receipts/milan_dp_partition.txt`).
- The hosted windows at `01fc5475` were about 1099, 832, 823 and 493 s for legs 0 to 3, measured from listing to PASS on worker jobs 120902541812, 120902541762, 120902541795 and 120902541972. The registered figures are (378, 1483, 1156, 231).
- Dev's own windows were already off before this PR: about 2004 s for leg 0 at a `a032c6d6` run, job 120672717060. The reshuffle balances the legs better than before. Every window is far inside the 45-minute job limit, and `suite_shards.py --selftest` passes.
- **Impact:** only the projection's accuracy.
- **Optional:** re-apportion the four milan_dp figures from a measured hosted run of the current inventory.

### R687-3-S2 SUGGESTION - Docs - none in tree - nxn8's "CRF adds 2 media clock periods" next to #773's "one at 8x8"

- **Evidence:** at this head, `obj_nxn8` prints `#773 output 8 CRF adds 2 media clock periods beside its offset` (`receipts/milan_dp_nxn8.log`). #773's CHANGELOG entry and `milan_datapath.sv`'s talker-terms block say TC is one period at 8x8.
- These do not contradict each other. `build-nxn8` leaves `AUDIO_IF_SLOTS_P` at its default 0 (`milan_datapath.sv:129`; `tb/verilator/milan_dp/Makefile:717`), so it is not the shipping TDM32 8x8 shape that the "one period" figure describes.
- This is #773's text and bench, outside this PR's scope.
- **Optional, for #773's owner:** say beside that harness line which shape it reports.

### Prior public findings at this head

| Finding | State at `f8775f7b` | Evidence |
|---|---|---|
| R687-1-F1 BLOCKER, Tests/RTL (BDD frame-size resolver) | RESOLVED, holds | `KL_crf_tx.sv:248` `CRF_PDU_C = CRF_HDR_C + 32'(CRF_DLEN_C)` is unchanged by the merge. Dev's added `TC_*`/`PIPE_CYC_C` localparams come after `FRAME_BYTES`/`NUM_BEATS` (`:254-255`, `:320-326`), so the resolver's first match is unchanged. `cd tests && behave` on the head: 14 features, 406 scenarios, 1977 steps passed, 0 skipped (`receipts/behave_all.log`). Hosted `bdd-conformance` at this head: success. |
| R687-1-F2 MINOR, Docs (version token as clause) | RESOLVED, holds | `gen_module_matrix.py --check` rc 0 (79 modules, generator controls 7/7). No `1.2` clause token in `MODULE_MATRIX.md` (`receipts/module_matrix_check.log`, `prior_findings_check.txt`). |
| R687-1-F3 MINOR, Tests (command table) | RESOLVED, holds | `crflic_mutants.py` sha256 `baec486a…15d2` equals `command-table.json`'s entry (`prior_findings_check.txt`). |
| R687-1-R1 RESIDUE (Q-10 wording) | RESOLVED, holds | `docs/traceability/ieee8021q.md` is unchanged since `01fc5475`. |
| R687-1-S1 SUGGESTION (unequal AAF widths) | RETAINED, optional | `milan_datapath.sv` `g_pp_maxf` and `sim_crf_licence.cpp` are unchanged by the delta. |
| R687-2-S2 SUGGESTION (`make clean` leaves `obj_tspec8`) | RETAINED, optional | `tb/verilator/milan_dp/Makefile:904` is unchanged and still omits `obj_tspec8`. |
| R687-2-S3 SUGGESTION (generator accepts a dotted version) | RETAINED, optional | `gen_module_matrix.py` is unchanged by the delta. |
| R688-2-F1 MINOR (six vs five planted BDD faults) | RESOLVED, holds | The public correction on #774 (issuecomment-6385747770) stands. It is not a tree artifact, and nothing in the delta restates the count. |
| R688-2-R1 RESIDUE (role placeholders) | RESOLVED, holds | The PR body names `[R687]` and `[R688]`. |

## 3. Lens results at this head

```text
[R687] PASS Conformance - hdl/milan/milan_datapath.sv:9116-9124,9472; hdl/ieee1722/crf/KL_crf_tx.sv:234,261; receipts/milan_dp_crflic_mutants.log - every source's Talker Advertise TSpec on the MERGED tree against Milan v1.2 4.3.3.2 Table 4.4 and IEEE 802.1Q-2018 35.2.2.8.4 a): obj_tspec8 (8x8, nine sources) uid 0..7 got=217, uid 8 CRF got=29, MaxIntervalFrames 1, 61/0; obj_crflic (1x1) 217/29 and both equal the emitted AVTPDU + 1, 427/0. #773's Equation (14) TC and AAF lead compose beside it: the capture_coherence datapath [WIRE]/[GRID]/[HOLD] pass (CRF hand-over spare 20503 ns, as the RTL comment states), and nxn8 3998/0 and ax1x1 233/0 pass, including every "#773 output n ... at or before its timestamp less the offset" check. #775's [SQ] inputs (hdl/ieee1722/avtp, tb/verilator/avtp_rxmon) are byte-identical to ae255ead.
[R687] PASS RTL - hdl/ieee1722/crf/KL_crf_tx.sv:133-234,248-261,315-330,556; hdl/milan/milan_datapath.sv:2044,2488,7446-7449,7492,9116-9124 - composition: this PR adds an output port (tspec_max_frame_o) and re-expresses CRF_PDU_C (still 28); #773 adds parameters TC_P/CLK_HZ_P/EV_LATE_NS_P and localparams that read NUM_BEATS (unchanged, 8). No name, parameter or port overlaps. The one instance carries #773's three overrides and this PR's port. g_pp_maxf/pp_src_maxf_w and the TLK_*/DOM_* terms are disjoint. No shaper reads the TSpec-derived slope (milan_datapath.sv:8492-8498), so the CRF value 29 cannot move #773's hand-over timing. lint_rtl.py --check with pinned Verilator 5.050: PASS, 89 <= 89 (receipts/lint_rtl_check.log). The other KL_crf_tx instances (media_phase wraps) are unchanged from both parents' accepted state.
[R687] PASS Robustness - receipts/milan_dp_crflic_mutants.log, receipts/capture_coherence_whole.log - the planted pre-#774 control (talker 0's TSpec on every source) fails "CRF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 28 + 1" on both shapes of the merged tree, and the six #530 grant/ACTIVE mutants are still caught (10/10). #773's controls on the merged datapath (no lead, lead one period short, no TC, TC one period short, 125 us late, fixed delay past 125 us refused at build) are caught, 44/44.
[R687] PASS Tests - receipts/shards_17.txt, receipts/milan_dp_partition.txt, receipts/suite_shards_selftest.txt, receipts/test_sim_pool.log, receipts/ci_suite_pieces_selftest.log - suite_shards --selftest PASS; 17 workers place 81 units once each (union equals --ci-pieces, no duplicate); milan_dp's 22 driver cases fall into 4 legs once each, tspec8 in leg 1; test_sim_pool.py 17/17 (fifteen legs); ci_suite_pieces_selftest 64 parents, 81 units, PASS. The merged-tree suites listed under Conformance and Robustness all exit 0. Dev added no stack-pin target (26 targets at a032c6d6 and at ae255ead), so sw/firmware/ctrl/README.md's "167 pin controls" still composes (27 at the head).
[R687] PASS Docs - CHANGELOG.md:11-12,48-75; docs/testing/TESTING.md; docs/reference/MILAN_COMPLIANCE_MATRIX.md; receipts/docs_*.log - both Unreleased entries byte-identical to their sides, anchors resolve. Auto-merged hunks of TESTING.md (fifteen milan_dp commands; seventeen workers) and the compliance matrix (4.3.3 row; 5.3.7.6 and 4.4.2.2 rows) are each side's own lines. No dev-side text restates the old CRF TSpec (search for CRF_SRP_MAXF_C, tctx_maxf_w[0], MaxFrameSize 42/217). docs_check, gen_toc --check --verify-anchors, check_em_dash --base ae255ead (0 findings over 38 added lines), check_doc_style and check_doc_paths: rc 0; gen_module_matrix --check rc 0. RESIDUE R687-3-R1 does not leave the lens unclean.
```

Comment rule: the delta adds no source line of its own. In the dev lines it carries, a scan finds no bench lane label, reviewer ID, round or issue-comment ID; "the control lane's IFG gasket" names a hardware path. So there is no RESIDUE under that rule.

## 4. Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv` g_pp_maxf/TLK terms; `KL_crf_tx.sv` port and TC; tspec8 / crflic `[TSPEC]`, capture_coherence `[WIRE]/[GRID]/[HOLD]`, nxn8, ax1x1 on the merged tree | R687-3 | `f8775f7b92b1ceff106ebb02b0e2f4ca48972ad7` |
| RTL | CLEAN | `KL_crf_tx.sv`, `milan_datapath.sv` composition, both sides' hunks, lint ratchet | R687-3 | `f8775f7b92b1ceff106ebb02b0e2f4ca48972ad7` |
| Robustness | CLEAN | crflic-mutants 10/10; capture_coherence mutants 44/44 | R687-3 | `f8775f7b92b1ceff106ebb02b0e2f4ca48972ad7` |
| Tests | CLEAN | 17-worker shard map; milan_dp 4-leg partition; sim-pool and suite-pieces self-tests; behave 406/406 | R687-3 | `f8775f7b92b1ceff106ebb02b0e2f4ca48972ad7` |
| Docs | CLEAN (RESIDUE R1 carried) | `CHANGELOG.md`, `TESTING.md`, compliance matrix, module matrix; five docs gates | R687-3 | `f8775f7b92b1ceff106ebb02b0e2f4ca48972ad7` |

R687-2's ledger at `01fc5475` covers everything outside this delta. The delta changes nothing those verdicts depend on beyond what was re-run above.

## 5. Probes run (merged tree, pinned Verilator 5.050, wrapper sha256 of its binary `fb2cc573…cdef`)

| Probe | Result | Receipt |
|---|---|---|
| `make -j2 crflic-mutants` (builds and runs obj_crflic and obj_tspec8 first) | rc 0; crflic 427/0; tspec8 61/0; mutants 10/10 | `milan_dp_crflic_mutants.log`, `.rc` |
| `capture_coherence/mutants.py --whole-suite --jobs 2` | rc 0; capture_coherence 20832/0; capture_coherence_dp 847/0; mutants 44/44 | `capture_coherence_whole.log`, `.rc` |
| milan_dp `build-nxn8`/`exec-nxn8` | rc 0; 3998/0 | `milan_dp_nxn8.log`, `.rc` |
| milan_dp `build-ax1x1`/`exec-ax1x1` | rc 0; 233/0 (5 guarded, not run in this shape) | `milan_dp_ax1x1.log`, `.rc` |
| `behave` (tests/) | 406/406 scenarios, 1977/1977 steps | `behave_all.log` |
| `lint_rtl.py --check` | PASS 89 <= 89 | `lint_rtl_check.log` |
| docs gates (5) and `gen_module_matrix.py --check` | all rc 0 (pinned renderer, CPython 3.14.8, html5lib 1.1, cmarkgfm 2025.10.22 in a disposable venv) | `docs_*.log`, `docs_gates.rc`, `module_matrix_check.log` |
| shard map, partition, self-tests | as in Tests | `shards_17.txt`, `milan_dp_partition.txt`, `suite_shards_selftest.txt`, `test_sim_pool.log`, `ci_suite_pieces_selftest.log` |
| restore check | 1442 tracked files rehash to the head blobs and modes; index writes tree `8d057d84`; five gitlinks at their recorded commits and clean; `external` uninitialized, as at start | `restore_verify.txt` |

## 6. Real limits

- **No manager source bank runs at this head, and none is claimed.** The suites above are focused reviewer probes, not the full sweep, Yosys, the builder or native banks.
- **No Vivado run.** The PR's route-1x1/ooc figures are at `e70a99ba` on base `a032c6d6`. The merged tree adds #773's packetizer and TC logic to this PR's change, and the route record has 19 free slices.
- **Hosted evidence at this head is partial.** In my snapshot (`receipts/hosted_checks_f8775f7b_snapshot.tsv`) these completed with success: `bdd-conformance`, `changes`, `docs-check-no-git`, `docs-gates-0`, `full-ci-gate` and `wire-accountability`. `Physical gPTP` was skipped by schedule. The 17 Verilator shards, Yosys, lint, firmware and the remaining docs and elaborate legs were queued or in progress. At `01fc5475`, shard 10/16 failed only through `media_phase`'s 900 s TIMEOUT, which this delta's #781 raises to 1400 s; `milan_dp__3` passed on that worker.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. The wire evidence is the simulated DUT's own MSRP and AVTP frames.
- **The capture_coherence local run used two workers.** Its hosted four-piece split is not reproduced here; the union of cases ran.

## 7. Pending manager duties

- Build and validate the current-dev merge candidate (live dev `ae255ead86d59277762444c44bb3086ab1879448`, the same as the source base) with the builder and native banks. Link the receipts on the PR.
- Run the resource gate on the candidate (route-1x1, ooc-1x1, ooc-8x8 against the eleventh record), because the candidate combines #773's RTL with this PR's.
- Own acceptance of the exact-head hosted `verilator-suites`, `yosys-portability` and act replicas once they finish.
- Carry R687-3-R1 to the residue checklist.
- Track the three optional suggestions (R687-1-S1, R687-2-S2/S3) and the two new ones (R687-3-S1, R687-3-S2) at the author's or owner's discretion.

R687-3 FINISHED
