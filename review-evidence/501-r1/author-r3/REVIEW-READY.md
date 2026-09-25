[A291] REVIEW READY

Commit: `afdd28b701e7f5849317e27ce845c31d1c87f2a6` (local branch `501-outmap-record`; not pushed).

Changed: only `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and UNRESOLVED 6, per the [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5824209814). They state today's CLOSED-record copy independent of materialization, RELOAD closure, 12,634 bytes across 156 records at 8x8 including 4,672 output-map bytes, and the present 0.78x doubled-cost exposure. #559 owns measurement and resolution. Safety through void/retry and unchanged 1x1 margins remain explicit; the donor-adoption trigger is removed.

Validation: both reviewers' unchanged `capture_copy_probe.py` and `hold_margin.py` ran, all four rc 0 with archived output matched. Current record figures also match the archived head. The page agrees with these results.

All assigned gates returned rc 0:
- `python3 scripts/check_nvm_record_space.py` and `--self-test`;
- `python3 scripts/docs_check.py` in both CI modes;
- `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55`;
- `python3 scripts/check_doc_style.py`, `python3 scripts/gen_toc.py --check`, `python3 scripts/check_doc_paths.py`;
- `git diff --check`, also checked across the committed round-3 delta.

Acceptance: assignment items 1-3 met. `HANDOFF.md`, the full updated `PR-BODY.md`, and receipts are prepared in the assigned output directory. Scratch removed; worktree clean. No push or PR edit performed.

Open risks/questions: no new decision; product copy timing and resolution remain #559. Times above are modelled. The no-metadata documentation mode skips inventory parity as designed. Delta reviews by [R312] and [R313] remain pending.
