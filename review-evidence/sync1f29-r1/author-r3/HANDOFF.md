# [A10] HANDOFF: sync dev 1f29f189 into dev-soft-core, round 3

Head `b2a1d677`, one commit over `fa019799`, by the manager: one README, 3 lines. No RTL, firmware or generator change, and no harness run, as R759-2 F3 says.

| Finding | Change, `tb/verilator/ctrl_service_budget/README.md` | Verification |
|---|---|---|
| R759-2 F3 | Line 854, the window cell reads 884.91 | Against R759-2's `receipts/window-exact.txt`: 884.91464 ms |
| R759-2 RES-3, R760-2-R1 | Line 843 takes RES-3's exact sentence; the stage adds the fifth record | Against `receipts/windows-*.txt` |
| R759-2 RES-4 | Line 846 has a verb | Read |
| R760-2-R2 | The PR body's Status | Read |

Gates on the head: `check_doc_style.py` rc 0, `docs_check.py` 0 findings, `check_em_dash.py --base 97aab1d0` 0 findings, `check_doc_paths.py` OK, `git diff --check` no finding. The hosted workflows run the rest.
