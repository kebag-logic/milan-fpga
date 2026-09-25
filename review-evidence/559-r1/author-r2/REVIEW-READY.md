[A309] REVIEW READY

Commit: `31808e6525a83955bc4322ac8ac6871f9e6b10e6` (local, unpublished; branch `559-capture-copy`).

Changed: explicit contract-clock override and aligned rising edges; normal timing grading for traffic ON and OFF; a hosted generated-table census/clock gate with named controls; complete measurement receipt; section 18, UNRESOLVED 6 and both test indexes corrected.

Each row below contains 16 captures. Both shapes use the contract's 50 MHz CPU; the 100 MHz rows are non-contract comparisons. All use a 100 MHz system timer and aligned rising edges.

| Shape | CPU MHz | Traffic | Maximum ms |
|---|---|---|---|
| 8x8 | 50 | ON | 24.30454 |
| 8x8 | 50 | OFF | 24.26154 |
| 1x1 | 50 | ON | 6.60642 |
| 1x1 | 50 | OFF | 6.58857 |
| 8x8 | 100, non-contract | ON | 19.00433 |
| 8x8 | 100, non-contract | OFF | 19.79024 |

STOP did not trigger: the maximum over both 8x8 contract arms is **24.30454 ms**, below 24.5 ms by **0.19546 ms**. The unchanged nominal 50 ms hold has a guaranteed 49 ms floor, giving **2.0161x** measured margin. The remedy remains conditional on the measured inputs. Product firmware, RTL, YAML configurations, donor pins and builder census lists are unchanged; #565 retains the configuration reconciliation.

Both reviewers' 50 MHz figures reproduce cycle-for-cycle, including all traffic counts: original-phase ON 24.15248 ms, OFF 24.15108 ms, and the aligned ON probe 24.29902 ms. The fetched evidence scratch was deleted after comparison. The new receipt contains all 96 captures and input hashes.

Traffic characterization: aligned 50 MHz ON maxima exceed OFF by 0.04300 ms (0.177%) at 8x8 and 0.01785 ms (0.271%) at 1x1. These are small measurable increases, so the docs report the numbers rather than claiming literal zero effect. At 100 MHz OFF is slower. Every arm contributes to the maximum.

Validation: **all requested gate commands returned 0**. Both full builder modes ran, with the prescribed pinned-compiler argv mapping and with cross-compiler candidates hidden. The SDK mode executed the compiled census. The absent mode intentionally reports that census and its dependent controls NOT RUN; both modes report the absent historical placement-calibration report NOT RUN. These are explicit skips, not executed passes.

`nvm_cosim`: 465 PASS, 0 FAIL, 39/39 named mutants killed. Backend: both shapes and all four controls pass. Firmware host suite: all five shapes and controls pass. Both capture simulation controls are detected. OOC is inapplicable without an RTL change.

The new `python3 scripts/check_nvm_capture.py` gate passes without a compiler, simulation or LiteX import. It regenerates bytes/records, checks the explicit CPU clock plus configured CPU/system clocks, checks source hashes, regrades every row and recomputes maxima. Named bytes, records and clock mutations each fail for input drift. A planted grader that ignores OFF timing fails its control; the OFF limit accepts 24.5 ms and refuses one extra system tick.

Other completed gates: bare-metal-only; documentation in both Git inventory modes; em-dash against `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`; documentation style; Contents and anchors; paths; module matrix; parser; all three language idioms; port contracts; naming; test evidence; unstaged and staged whitespace. The parser ran and matched its existing pinned-source ratchet.

Acceptance: measured remedy, census/clock protection and documentation are implemented. Independent re-review and exact-head hosted acceptance remain. Physical timing, DDR calibration, debounce and memory ordering remain unmeasured. HANDOFF.md and the full updated PR-BODY.md are in the assigned output directory. No push, PR edit, merge, hardware access or delegated work was performed.
