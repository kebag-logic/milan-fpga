[A375] Record ten e1 switch power cycles on the assigned image.

Refs #394. Refs #387.

- #394 acceptance 2: FAIL. All ten recoveries succeeded, but LINK_UP/LINK_DOWN stayed at 1/0, so exact DUT link-edge timestamps are unavailable.
- #387 acceptance 4: PASS for the assigned CRF recovery measurement. Each observed PHC step was followed by locked media within one further stream restart. AAF render timing was not measured; #593 is not graded.
- gPTP recovery took 0.44-1.82 s against the five-second bound. Both bindings and streams recovered without controller re-bind or DUT reboot.
- First valid PDUs followed the wire-return landmark by 5.07-14.00 s. This records the requested one-second comparison while distinguishing the missing DUT link edge and #75's CONNECT_RX trigger.

Only `docs/findings/394_387_E1_SWITCH_CYCLES.md` changes. It contains the per-cycle table, method limits, restore proof and raw artifact hashes. The operator packet is published on the lane's review-evidence branch. The raw captures are retained in private cold storage and indexed there by size and SHA-256.

Validation at `fddc58e43733afd90d6222e58999e0f416a30df9`: all nine assigned gates returned 0: docs_check.py, check_doc_style.py, gen_toc.py --check, check_em_dash.py --base 2a2a7bb6, check_doc_paths.py, ci_scope.py --selftest, check_baremetal_only.py --check, check_feature_status.py --self-test, and git diff --check. The committed diff also passes whitespace validation.

Full restore passed: all seven outlets ON as found, all eighteen stream states unbound, original clock source and settings restored, final UART 10/10, no CRF in the final capture, temporary capture driver and controller files removed. The bench lock is free.

The flat LINK_UP/LINK_DOWN counters are the bare-metal link-status defect, filed as #599: nothing publishes the PHY state, so MAC_STATUS stays at its reset value. #394 acceptance 2 is re-run after #599 lands. Operator evidence is under independent review.
