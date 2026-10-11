[R585] NEGATIVE - exact head be607527eaac84cfc8d7456167b070a22228345b

Independent verdict recorded before reading prior public review findings or any other reviewer's report. All five lenses have been applied to the round-10 delta, the source-range inventory and relevant integration artifacts. Prior-finding reconciliation and the requested prior executable probes remain for the final report.

R585-9-F1: MINOR; Conformance, Robustness, Tests, Docs. The module-wide dynamic-code prohibition is not enforced. `ctrl_pin.py:224` checks DYNAMIC for imports and bare names, but not attributes; `inspect.builtins.exec` is accepted outside the helper and a disposable specimen launches a child. `ctrl_pin.py:229` also skips every helper node, accepting all five forbidden dynamic facilities inside the helper. Authority: issue #697 comment 6112358746 and this review's explicit assignment. Evidence: `census-matrix.log`, `dynamic-launch.log`. Required outcome: reject the forbidden dynamic facilities throughout both modules, including attributes and the helper, while retaining the launch-facility exception for the helper. Verification: both probes refuse, clean census and the eight standing census controls still pass. The README and docstring must describe the enforced contract accurately.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #697 body and scope rulings; ctrl_pin.py:224, ctrl_build.py:197; census-matrix.log | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |
| RTL | CLEAN | delta.diff; integration.diff; hdl and firmware-image input invariants; source-evidence.txt | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Robustness | UNCLEAN | ctrl_pin.py:224; dynamic-launch.log; 35 pin controls in focused-checks.log | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Tests | UNCLEAN | ctrl_pin.py:153,631,653; census-matrix.log; focused-checks.log | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Docs | UNCLEAN | sw/firmware/ctrl/README.md:169; ctrl_pin.py:11; ctrl_boundary.py:78; PR #705 Round 10; focused-checks.log | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |

No RTL, firmware source, image builder, configuration, pin or image artifact changed in round 10. Published author receipts, rather than a manager source-head bank, supply source validation. Physical calibration NOT RUN. Current-dev merge-candidate validation and hosted/local-replica acceptance remain manager duties.
