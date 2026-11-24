[R916] NEGATIVE - exact head bbfdb6746d585e490508783dc8a88c79fbab02c0

Independent pass recorded before reading this PR's prior review findings or another review report.
All five lenses applied to the four-commit delta from 300da99beed5bb1c77e4b04af0bb4f9369856e0d.

F1 | MAJOR | Conformance, Robustness, Tests | tb/verilator/gptp_plane/sim_main.cpp:506; tb/verilator/gptp_shadow/sim_main.cpp:1311; tb/verilator/milan_dp/sim_gptp.cpp:2057; PR #995 Known limitations.
The adoption adds no platform assertions for the first-Announce race or the mastership rate reset. CONTRIBUTING.md section 3 requires self-checking coverage of functional RTL changes, including imported behavior; the changed parent contract is docs/design/GPTP_PLANE.md:94 and docs/design/GM_LOSS_RECOVERY.md:46, under REQ-PTP-05.
Independent probes: baseline, restored 2 ms first-Announce arm, and rate word 3 applying only during a slew all pass the existing gptp_plane run (31/31) and gptp_shadow run (326/326). An observation-only print after mastership sees rate 0 in the control and 13414 Q8.24 units in the retained-rate fault, with all 31 checks still passing.
Impact: the root consumer regression can remain green with either adopted defect restored.
Required outcome: add platform regressions through the parent transport and real PHC, proving an Announce before queued re-election and a return from nonzero slave trim to the local oscillator without a phase step; prove the regressions reject these faults.
Verification: focused positive and negative runs, then the required consumer legs and gates at the corrected head. No production defect is asserted at this head.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #994; REQUIREMENTS.md:172; adoption pins; route receipts; F1 | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |
| RTL | CLEAN | imported KL_gptp_engine.sv:958,1283; gen_gptp_ucode.py:1994,2036,2487; KL_gptp_shadow.sv:717,784; milan_datapath.sv:3259,9265 | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |
| Robustness | UNCLEAN | Announce deadline/re-election and settled/slewing mastership cases; gptp_shadow reset/backpressure checks; F1 | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |
| Tests | UNCLEAN | three independent paired probes, gptp_plane and gptp_shadow; published consumer receipts; F1 | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |
| Docs | CLEAN | 20-file adoption diff, both pin diagrams, pin/guide checkers, PR body versus public author receipts | R916-1 | bbfdb6746d585e490508783dc8a88c79fbab02c0 |

This is the independent-pass snapshot. Public-findings reconciliation, full receipt audit and final integrity proof follow in REPORT.md.
