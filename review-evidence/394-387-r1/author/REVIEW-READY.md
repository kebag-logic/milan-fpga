[A375] REVIEW READY

Commit: `fddc58e43733afd90d6222e58999e0f416a30df9` (local, unpushed).
Changed: `docs/findings/394_387_E1_SWITCH_CYCLES.md` only.

#394 acceptance 2 (e1): **FAIL**, because LINK_UP and LINK_DOWN remained flat in all ten cycles. Recovery itself succeeded. #387 acceptance 4: **PASS for the assigned CRF recovery measurement**; every observed PHC step recovered locked media within one further stream restart. AAF render timing was not measured. These are operator findings, not independent review verdicts.

| Cycle | OFF duration (s) | LINK_UP / DOWN delta | DUT MEDIA_LOCKED / UNLOCKED delta | gPTP recovery (s) | Both streams / bindings | PHC step to locked media (s) |
|---|---|---|---|---|---|---|
| 1 | 21.09 | +0 / +0 | +1 / +1 | 1.564 | automatic / automatic | 8.00-8.28 |
| 2 | 20.89 | +0 / +0 | +1 / +1 | 0.680 | automatic / automatic | 10.25-10.54 |
| 3 | 20.96 | +0 / +0 | +1 / +1 | 1.622 | automatic / automatic | 7.50-7.78 |
| 4 | 20.92 | +0 / +0 | +1 / +1 | 1.815 | automatic / automatic | 7.50-7.79 |
| 5 | 20.90 | +0 / +0 | +1 / +1 | 0.632 | automatic / automatic | 11.25-11.54 |
| 6 | 20.94 | +0 / +0 | +1 / +1 | 0.638 | automatic / automatic | 10.75-11.04 |
| 7 | 21.05 | +0 / +0 | +1 / +1 | 0.441 | automatic / automatic | 8.25-8.53 |
| 8 | 21.05 | +0 / +0 | +1 / +1 | 0.474 | automatic / automatic | 12.25-12.54 |
| 9 | 21.02 | +0 / +0 | +1 / +1 | 1.817 | automatic / automatic | 8.50-8.78 |
| 10 | 20.92 | +0 / +0 | +1 / +1 | 0.680 | automatic / automatic | 8.75-9.04 |

All gPTP returns were within the documented five-second bound. DUT link status stayed `0x0d`, so exact DUT link down/up timestamps could not be measured. The page separately records controller carrier edges, GM/PHC events, first PDUs, observed mr changes and MEDIA_RESET sequences. First valid PDUs followed the tapped wire-return landmark by 5.07-14.00 s; this is distinct from #75's CONNECT_RX trigger. No #593 verdict is applied. Timing resolution and cross-host uncertainty are documented.

Identity gate and OUT4 proof passed. No STOP condition occurred. Full restore passed: outlets as found (all ON), all eighteen stream states unbound, original clock source and settings restored, final UART 10/10, final capture without CRF traffic, temporary capture driver/build and controller files removed. Bench lock released and verified available. No DUT reboot, reflash or power cycle.

Validation at the stated head: all nine assigned gates returned 0: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 2a2a7bb6`, `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, and `git diff --check`. The committed diff also passes whitespace validation.

Packet: `2026-09-23/394-a375`, with `HANDOFF.md`, `PR-BODY.md`, `MANIFEST.sha256`, scripts, analyses and exact gate output. Large raw captures remain under `/tmp/a375`; `RAW-ARTIFACTS.json` and per-cycle manifests list paths, sizes and hashes. No push or PR operation was performed. Independent reviews remain pending.
