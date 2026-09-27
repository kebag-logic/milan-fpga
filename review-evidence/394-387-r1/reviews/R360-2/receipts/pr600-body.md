[A375] Record ten e1 switch power cycles on the assigned image.

Refs #394. Refs #387. Neither issue closes.

- #394 acceptance 2: FAIL. All ten recoveries succeeded, but LINK_UP/LINK_DOWN stayed at 1/0. MAC_STATUS remained at its software-published reset value, `0x0d`; nothing in this build writes it (#599). DUT PHY link loss was not observed, and the inline capture point may hold the link up.
- #387 acceptance 4: NOT MET (not exercised). Every PHC step occurred in HOLDOVER with both CRF streams absent. A grandmaster change while a locked CRF stream keeps running is still needed. Item 2 requires one counted media event per step and provides no step-to-relocked-media time bound.
- gPTP outage recovery took 0.44-1.82 s against #117's five-second bound. Both bindings and streams recovered without controller re-bind or DUT reboot. The media interval measures outage recovery after the step, including stream return and acquisition; #117's one-further-restart media row is context only.
- First valid PDUs followed the wire-return landmark by 5.07-14.00 s. The missing DUT link edge and #75's CONNECT_RX trigger remain distinct. AAF render timing was not measured; #593 is not graded.

Only `docs/findings/394_387_E1_SWITCH_CYCLES.md` changes. It records the per-cycle measurements, limits, restore proof and raw artifact hashes.

The [public packet archive](https://github.com/kebag-logic/milan-fpga/tree/8f983d245a12e18a47ced37904d405b624c7e024/review-evidence/394-387-r1) is on `394-387-review-evidence`, at `review-evidence/394-387-r1`, commit `8f983d245a12e18a47ced37904d405b624c7e024`. Its publisher index is `MANIFEST.json`. Raw captures remain in private cold storage, indexed by size and SHA-256 in `author/RAW-ARTIFACTS.json` and the per-cycle indexes. Their temporary-directory paths are historical names.

## Round 2

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5859045504) addresses both round-1 reviews:

- R360-1 F1 / R361-1 F2: repair the nine-column table delimiter; preserve every measurement.
- R360-1 F2 / R361-1 F3: explain the missing status publisher, unknown PHY state, unsampled link-guard input and flat peer counters. The #394 FAIL remains.
- R360-1 F3 / R361-1 F1: replace #387 PASS with NOT MET (not exercised), distinguish its counted-event contract from #117 outage recovery, and rename the media interval.
- R360-1 F4 / R361-1 F4: replace the private locator with the public archive and publisher index; describe cold storage and historical index paths.

Validation at `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1`: all nine assigned gates returned 0: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 2a2a7bb6`, `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, and `git diff --check`. The pinned renderer produces six tables; the per-cycle header, delimiter and all ten rows have nine cells. Independent recomputation reports zero differing rows; all 50 raw-artifact rows match both public indexes; the publisher index verifies 165/165 hashes. The committed diff also passes whitespace validation.

The recorded restore remains unchanged: all seven outlets ON as found, all eighteen stream states unbound, original clock source and settings restored, final UART 10/10, no CRF in the final capture, and temporary acquisition components removed.

#394 acceptance 2 awaits the #599 re-run. #387 acceptance 4 awaits the running-stream measurement. Independent re-review of the corrected head remains required.

