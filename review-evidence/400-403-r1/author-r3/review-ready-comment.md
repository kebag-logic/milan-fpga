[A316] REVIEW READY
Commit: 7463ab0889da9a95fce7c921e386d6035d69778e (local head, not pushed)
Changed: the saved-state host-test header derives every boot constant from each generated overlay/SRP table through boot_policy.fabric_constants(); the builder compiler fixture uses the same derivation, and the complete builder gate now runs the firmware self-test.
Validation: all 48 manager builder-bank commands returned 0. Both complete builder modes returned 0; `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` passed all five shapes and detected all four planted defects. Declaration checks, CSR and protocol-wrapper suites, every default milan_dp recipe chunk including both mutation campaigns, all 344 behavior scenarios, and the requested documentation/source gates returned 0. Default-shape OOC area deltas are zero for milan_csr, KL_pp_shadow and milan_datapath.
Acceptance criteria: both Round 2 items met. The initial missing-constant failure was reproduced before the fix.
Limits: the compiler-absent mode deliberately leaves compiler-dependent instruments unmeasured; the historical placed-utilization calibration report remains unavailable. No product behavior or RTL changed in Round 2.
Handoff: HANDOFF.md and the full updated PR-BODY.md are complete in the assigned output directory. No push, PR edit or merge performed.
