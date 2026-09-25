[A312] REVIEW READY

Commit: `9eee43831d487a52637d34d87a727f6e174e7cab` (local `551-licence-real-grant`; not pushed).
Parents: `babb8925030612e47c687b1fda1a1ce614988721` and dev `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.

Changed: merged the assigned dev tip and resolved all five conflict hunks in the three named files. The ACTIVE AND real-grant licence, published-round/pending-declaration rules, CSR bit distinctions and GET_STREAM_INFO coverage all survive. The processor is at `990f96526bb89356c963a260ebbdcf2a77e6623a`, including the #112 fix from `a8f8ce81`.

Acceptance: the unwarmed refusal arm now runs by default, with no EXPECTED-FAIL skip. Both sources and both admission phases pass the no-grant/no-licence/no-counter-pair/no-reset/no-PDU checks. The reverse TSpec change also streams and re-measures admitted-start latency. Both histories add 5/5 cycles for AAF and 3/5 for CRF across the two phases (30--50 ns at the fixture's 100 MHz clock); ordinary Listener Ready adds zero. The obsolete residual-window claims are removed. Q-9/Q-10 retain their mapping, status, rationale and 75% boundary caveat; generated mappings remain current.

Failing control: the existing submodule was temporarily repinned to `7a47f5788ff504f099a47ad4407c340771bb6bdb`, before the fix, and the unchanged fixture ran once. Build rc 0, fixture rc 1: 28 targeted unwarmed-refusal failures across all four source/phase cases (34 total, including six admitted-case ACTIVE timing checks). The merged gitlink and clean processor checkout were restored. No control pin or processor edit is shipped.

Validation, all foreground and without gate pipelines:

- `behave --no-capture -f plain` from `tests`: rc 0; 14 features, 344 scenarios, 1739 steps, none failed or skipped.
- `make -C tb/verilator/milan_dp crflic VERILATOR_JOBS=8`: rc 0; 415 checks, zero failures.
- `make -C tb/verilator/milan_dp crflic-mutants VERILATOR_JOBS=8`: rc 0; 7/7. All six mutants caught, including all three real-grant removals.
- `make -C tb/verilator/milan_dp VERILATOR_JOBS=8`: rc 0; all 14 simulation legs, render controls 6/6 and grandmaster-step controls 4/4.

Each command below returned 0:

```sh
python3 scripts/docs_check.py
env GIT_DIR=/tmp/551-a312-no-git-absent python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_py_idiom.py
python3 scripts/check_cpp_idiom.py
git diff --check
git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 HEAD
```

Syntax analysis ran with zero first-party findings and four unchanged processor findings at the ratchet. Both documentation inventory modes ran. Regeneration with `python3 docs/traceability/gen_module_matrix.py` returned 0 and left all 14 generated artifacts unchanged.

HANDOFF.md records every conflict with file:line, regeneration, gate commands/results and receipts. PR-BODY.md contains the full updated replacement, including the merge-dev section and `Closes #551`. The final worktree/index and all submodules are clean; the merge commit has one subject line, no body or trailers.

Open risks/questions: no remaining assignment blocker. Full independent review by [R296] and [R297], publication and subsequent merge gates remain pending. No push, PR creation/edit, merge into dev, sub-agent, additional checkout, hardware action or processor source edit was performed.
