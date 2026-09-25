[R323] POSITIVE - exact head fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c

# R323-2: external independent re-review of issue #541 / PR #562

- Round: R323-2 (external, cleared context). Delta review of `2734b771bcf0b383ea62ef05744452827bafe9e4..fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` (one commit, [A306]). Every lens is also re-checked against the whole PR diff from source base `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
- Head `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c`, tree `f77cc840ece81a2bcda303696d96136a2b0ca415`. Parent is `2734b771`, and the PR base is `5b73d3f4`.
- Scope authority:
  - Issue #541 body (acceptance 1-3).
  - Decision comment 5827373589.
  - Round-2 assignment 5828726541: F1 needs a check on a LOCKED sink with validation errors spaced so the timeout expires only if they refresh it, plus a named refresh mutant, and the reviewers' refresh mutants re-run unchanged. F2 names both mutants in the `TESTING.md` `crf_rx` row and keeps `measure_test_evidence --check` in agreement.
- Evidence read:
  - Author round-2 packet: `review-evidence/541-r1/author-r2` at archive `3a211d8d`.
  - Hosted check runs at the exact head.

## Verdict

POSITIVE. No finding of any severity is open at this head, and all five lenses are covered clean at `fa1b5c36`.

- My round-1 finding R323-1 F1 (MINOR, Tests and Robustness) is **closed**. The same defect was filed as R322-1-F1, and it is closed too.
- R323-1 F2 (SUGGESTION, Docs) is addressed.
- The delta introduces no new finding.

## Resolution of prior public findings (read after my independent pass; see receipt 09)

| Prior finding | Severity / lenses | Status at `fa1b5c36` | Evidence |
| --- | --- | --- | --- |
| R323-1 F1: "a validation error does not refresh the timeout" had no failing arm | MINOR / Tests, Robustness | **CLOSED** | `rejected_stream_timeout` (`tb/verilator/crf_rx/sim_discontinuity.cpp:227-264`) is enabled at `:29`. My round-1 `uf_refreshes_timeout` was run unchanged (script sha256 `013eb10a...`). It is now DETECTED by discontinuity with 4 named failures, including `reject stream cannot refresh the 100 ms timeout` (receipt 02). The campaign mutant `validation_error_refreshes_timeout` fails that same named check (receipt 01). |
| R322-1-F1: same defect; also asked to correct the comment "only silence expires lock" | MINOR / Tests, Robustness | **CLOSED** | That reviewer's probe `P2_error_refreshes_timeout` was run unchanged (`probe_mutants.py` sha256 `8f2137b5...`, equal to the author's provenance record). It mutates `w_acc_run_w = w_hit && !stop_i`, a different form from mine. It is DETECTED by the same 4 named checks, and the clean control passes (receipt 10). The comment at `sim_discontinuity.cpp:183-184` now reads "does not refresh the 100 ms timeout measured from the last consumed accepted PDU". |
| R323-1 F2: testing index does not name the new mutant | SUGGESTION / Docs | Addressed | `docs/testing/TESTING.md:463` names `validation_error_unlocks` and `validation_error_refreshes_timeout` and states the timeout property. |
| R322-1-S1: `CRF_CTRL` row qualifiers | SUGGESTION / Docs | Not taken; still optional | `docs/reference/REGISTER_MAP.md:837` is byte-identical to `2734b771` (blob `d8156cdf`). A SUGGESTION does not affect coverage. I concur that the row is not wrong. |

## Findings

None at this head.

## Per-lens results (each clean lens carries its artifact evidence)

- **[R323] PASS Conformance** - issue #541 acceptance 1-3; decision 5827373589; round-2 assignment 5828726541; `hdl/ieee1722/crf/KL_crf_rx.sv:34-42,354,374,531-537`; `docs/reference/REGISTER_MAP.md:837`; receipts 01, 03, 05.
  - Acceptance 1 (clause decision): unchanged from round 1 and still recorded publicly (takeover comment 5827406716). The stop condition does not apply.
  - Acceptance 2 (RTL, header and row agree; a test with a failing arm):
    - The RTL is unchanged. The header and row say "does not refresh the timeout", and the RTL resets `tout_r` only on `w_acc_run_w` (`KL_crf_rx.sv:531-532`).
    - The new check grades exactly that with a failing arm. Rejects every 2 ms keep the sink locked through 99.96 ms. The sink unlocks by 100.06 ms with exactly one MEDIA_UNLOCKED, and it never relocks or recounts through 200.06 ms (receipt 01, the `reject stream ...` lines).
    - Round-2 item 1 is met in every clause: LOCKED sink, validation errors spaced so the timeout expires only if they refresh it, unlock required on schedule, named mutant failing the named check, reviewer mutants run unchanged with verdicts recorded.
  - Acceptance 3 (gates green): the receiver gate is green at the head (receipt 01). The hosted exact-head contexts executed and succeeded (receipt 05; see limits).
- **[R323] PASS RTL** - `hdl/ieee1722/crf/KL_crf_rx.sv` at `fa1b5c36`; receipt 03.
  - The round-2 delta touches no HDL. `KL_crf_rx.sv` has blob `6ddd3af2` at both `2734b771` and `fa1b5c36`.
  - Comment-stripped, it is IDENTICAL to base `5b73d3f4` (sha256 `f0081e18...`, 278 lines).
  - No other `.sv`, `.v` or `.svh` file changes between base and head.
  - The four submodule gitlinks are equal at base and head.
- **[R323] PASS Robustness** - `KL_crf_rx.sv:354,374,531-560`; `sim_discontinuity.cpp:227-264`; receipts 01, 02, 04a, 04b, 10.
  - The malformed-only timeout path is now graded under a continuous reject stream, both before and after expiry. Seven refresh, schedule and idempotence variants are all DETECTED:
    - my round-1 `uf_refreshes_timeout`;
    - R322's `P2`;
    - refresh only while locked (`r2_refresh_when_locked`);
    - refresh only in the second half of the window (`r2_refresh_late_window`);
    - timeout 1 ms late;
    - timeout 0.2 ms early;
    - unlock recounted while silent (`r2_unlock_recounts`).
  - An eighth variant, where a reject relocks an unlocked sink (`r2_reject_relocks`), is also DETECTED. In every one of these eight, a round-2 `reject stream ...` check fires.
  - The existing lock-retention case (`validation error preserves established lock`, `sim_discontinuity.cpp:198`) and the 100 ms silence unlock (`sim_main.cpp:575-584`, `sim_discontinuity.cpp:222`) are still graded and pass.
- **[R323] PASS Tests** - `tb/verilator/crf_rx/sim_discontinuity.cpp:29,181-264`; `tb/verilator/crf_rx/mutants.py:19-34`; `tb/verilator/crf_rx/Makefile` (`all: run mutants`); receipts 01, 02, 04a, 04b, 10.
  - The new check can fail for the defect it claims. Both refresh forms fail it by name, and the clean control passes.
  - It grades public outputs only (`locked_o`, `cnt_locked_o`, `cnt_unlocked_o`, `fmt_err_o`).
  - The bracket follows from the Makefile's documented 200 kHz clock: 100 ms is 20,000 clocks. It is measured from the final accepted PDU of `fill()`. That PDU is followed by exactly two idle `tick()` calls in `send()` (`:58-62`), so the loop starts at clock 3.
  - Stimulus: matched SID and subtype, `type_i = 0`, single-cycle `frame_p_i` pulses every 400 clocks. A reject lands at clock 20,000 as well, so a refresh defect is still locked at the 20,012 grade point.
  - Head gate (receipt 01, exit 0): unit 13,836 checks, discontinuity 2,201, talker_step 69, all with 0 failures. The campaign has 10 controls and 0 failures, and `validation_error_unlocks` and `validation_error_refreshes_timeout` each print their named rejection.
  - My unchanged round-1 set (receipt 02) matches round 1 except that `uf_refreshes_timeout` is now DETECTED. `uf_counts_frames_rx` still survives. As in round 1, it is the near-equivalent tick-cycle-only form, and its corrected form `uf_flags_frames_rx` is DETECTED.
- **[R323] PASS Docs** - `docs/testing/TESTING.md:463`; `scripts/measure_test_evidence.py:596-601`; `KL_crf_rx.sv:34-42`; `REGISTER_MAP.md:837`; receipts 06, 07.
  - The `crf_rx` row names both validation-error mutants and the "cannot extend the 100 ms timeout" property. That matches the campaign inventory in `mutants.py` and the check in `sim_discontinuity.cpp`.
  - The `DUT_READER_DISPOSITIONS` text names the same two mutants and the existing tu, jump, refill, accept-edge, ignored-validity and PI-resume arms. That matches `mutants.py:19-34` plus the two servo mutants.
  - `measure_test_evidence.py --check` passes: RATCHET PASS, 0 unexplained DUT-source readers.
  - Documentation gates return 0: `check_doc_style`, `check_doc_paths`, `check_em_dash --base 5b73d3f4` (0 findings), `gen_toc --check`, `gen_toc --verify-anchors`, the C++ and Python idiom checks, and `git diff --check`.
  - Both commits have one-line messages with no trailers.

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | issue #541 body, 5827373589, 5828726541; `KL_crf_rx.sv:34-42,354,374,531-537`; `REGISTER_MAP.md:837`; receipts 01, 03, 05 | R323-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |
| RTL | CLEAN | `KL_crf_rx.sv` (blob `6ddd3af2`, comment-stripped identical to base); HDL-free delta; gitlinks; receipt 03 | R323-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |
| Robustness | CLEAN | `KL_crf_rx.sv:354,374,531-560`; `sim_discontinuity.cpp:227-264`; receipts 01, 02, 04a, 04b, 10 | R323-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |
| Tests | CLEAN | `sim_discontinuity.cpp:29,181-264`; `mutants.py:19-34`; `Makefile`; receipts 01, 02, 04a, 04b, 10 | R323-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |
| Docs | CLEAN | `TESTING.md:463`; `measure_test_evidence.py:596-601`; `KL_crf_rx.sv:34-42`; `REGISTER_MAP.md:837`; receipts 06, 07 | R323-2 | `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c` |

All five lenses are re-covered at the merge-candidate source head. The round-1 coverage at `2734b771` is superseded because the delta touched artifacts in the Tests, Robustness and Docs scopes.

## Receipts (all in MANIFEST.sha256)

- `receipts/00_tool_identity.txt`: pinned simulator wrapper (sha256 `905795b9...`, same as round 1), Verilator 5.050.
- `receipts/01_crf_rx_make_all.log` and `.rc`: `make all` in `tb/verilator/crf_rx` on a `git archive` export of the head.
- `receipts/02_round1_reviewer_mutants_unchanged.log`: my round-1 `scripts/reviewer_mutants.py`, unchanged.
- `receipts/03_rtl_strip_and_scope.txt`: comment-stripped RTL comparison, blob ids, delta file list and gitlinks.
- `receipts/04a_round2_delta_mutants.log` and `receipts/04b_round2_delta_mutants.log`: `scripts/reviewer_mutants_r2.py` (seven round-2 mutants plus the clean control).
- `receipts/05_hosted_checks.tsv`: exact-head check-run snapshot.
- `receipts/06_doc_and_ratchet_checks.log`: the ratchet and documentation checks. The three Markdown-renderer gates return rc 2 here only because the renderer is not installed; they are re-run in receipt 07.
- `receipts/07_doc_markdown_gates.log`: the three Markdown-renderer gates, run in a private virtual environment from `tools/markdown/requirements.txt` with `--require-hashes`.
- `receipts/08_clone_integrity.txt`: the review clone after all probes.
- `receipts/09_independent_verdict_before_prior_findings.txt`: my verdict and ledger, written before I read the other reviewer's report.
- `receipts/10_prior_r322_P2_unchanged.log`: R322-1's P2 probe, run unchanged from archive `3a211d8d`.
- `scripts/`: `reviewer_mutants.py`, `strip_compare.py`, `verify_clone.sh` and `verilator_j8.sh` are the round-1 scripts, byte-identical. `reviewer_mutants_r2.py` is new this round.

Reproduce (paths are relative to this packet; `HEAD_EXPORT` = `git archive fa1b5c36 | tar -x`):

```sh
export PINNED_VERILATOR=<pinned verilator 5.050>; export VERILATOR=$PWD/scripts/verilator_j8.sh
make -C "$HEAD_EXPORT/tb/verilator/crf_rx" all VERILATOR="$VERILATOR"
python3 scripts/reviewer_mutants.py "$HEAD_EXPORT" work-r1
python3 scripts/reviewer_mutants_r2.py "$HEAD_EXPORT" work-r2
python3 scripts/strip_compare.py <repo> 5b73d3f47dfed519eb988c13d6beb1db664ef1e0 fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c hdl/ieee1722/crf/KL_crf_rx.sv
sh scripts/verify_clone.sh <repo> fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c f77cc840ece81a2bcda303696d96136a2b0ca415
```

## Real limits

- **Harness scope.** Only the receiver harnesses were run. The talker_step leg ran for the head gate and my round-1 set, but not for the round-2 delta mutants, because it does not drive the lock timeout under rejects.
- **Other suites.** I did not run the servo suite (`mmcm_servo`), `docs_check.py`, `xvlog_gate`, the SystemVerilog idiom check, or any parent, PP, gPTP, Yosys or builder bank. For those I rely on the manager's source static/builder and native banks at this head, the author's packet, and the hosted runs. The delta touches none of their inputs except documentation.
- **Hosted runs.** Receipt 05 shows every exact-head hosted context executed and succeeded, except `Physical gPTP (nightly and manual)`, which was **skipped**, not run. The aggregate `verilator-suites` and `yosys-portability` contexts reflect shards that executed. Acceptance of hosted and act results belongs to the manager.
- **Timeout duration.** The new check runs at the harness's scaled 200 kHz clock, and the 100 ms bracket is 20 clocks (0.1 ms) wide. The silicon-rate duration is inferred from `TOUT_CYC_C = CLK_FREQ_HZ_P / 10`, not simulated.
- **No hardware.** Physical calibration was NOT RUN. No hardware or field result is claimed, and field skips are not hardware proof.
- **Candidate merge not validated.** This is source-head evidence. The final current-dev candidate (source base `5b73d3f4` onto live dev `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`) was not built or validated here.

## Pending manager duties

- Build and validate the current-dev candidate merge result at the merge turn, including the receiver and servo suites and the hosted or act acceptance.
- Confirm the second required positive review (the internal R322-2) at this same head before any merge.
- Obtain explicit maintainer merge authorization.
- Perform post-merge containment, close #541 through `Closes #541`, and move the issue to Done.
- R322-1-S1 (SUGGESTION) stays optional. Whether to file it separately is the manager's call.

R323-2 FINISHED
