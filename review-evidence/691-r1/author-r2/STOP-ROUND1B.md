[A564] STOP — round 1b
Head: `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd` (unchanged).

The six-row shipping sweep completed. All full IOB checks pass (21 PASS, 1 expected INERT, 0 FAIL each, including all nine required RX captures). Timing passes 5/6 rows. The #645 round-2d overlay with `ExtraTimingOpt` has Slow WNS +0.013 ns at both endpoints, below the required +0.030 ns by 0.017 ns. Qualification returned rc 1. This triggers ruling 6042557053's STOP condition; no directive retry or candidate change followed.

Inputs: dev base `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` plus this fix; #645 base `2525eae9567865a8bc741901914bdf5a1caf2c26` plus the same fix, overlay tree `01f65c3b2693d2b1c494e0738b9562a1778740b5`.

Recipe: AX7101 `xc7a100t-fgg484-2`, shipping 1x1 TDM8 / eight channels, all-fabric control, 50 MHz Milan clock, inverted transmit clock and shipping floorplan. `AreaOptimized_high` synthesis, `ExploreArea` optimization, `AggressiveExplore` routing/physical optimization, default seed; implementation 12 threads under the exclusive lock.

Corner cells are WNS / WHS in ns. The 0 C and 85 C endpoints repeat the fixed Slow/Fast models.

| Tree | Placement directive | Full IOB check | Slow 0 C | Slow 85 C | Fast 0 C | Fast 85 C | Result |
|---|---|---|---|---|---|---|---|
| dev + fix | ExtraPostPlacementOpt | 21 PASS, 1 INERT, 0 FAIL | +0.492 / +0.040 | +0.492 / +0.040 | +1.660 / +0.007 | +1.660 / +0.007 | PASS |
| dev + fix | AltSpreadLogic_high | 21 PASS, 1 INERT, 0 FAIL | +0.064 / +0.052 | +0.064 / +0.052 | +1.638 / +0.029 | +1.638 / +0.029 | PASS |
| dev + fix | ExtraTimingOpt | 21 PASS, 1 INERT, 0 FAIL | +0.098 / +0.074 | +0.098 / +0.074 | +1.362 / +0.036 | +1.362 / +0.036 | PASS |
| #645 round 2d + fix | ExtraPostPlacementOpt | 21 PASS, 1 INERT, 0 FAIL | +0.238 / +0.102 | +0.238 / +0.102 | +1.518 / +0.036 | +1.518 / +0.036 | PASS |
| #645 round 2d + fix | AltSpreadLogic_high | 21 PASS, 1 INERT, 0 FAIL | +0.227 / +0.071 | +0.227 / +0.071 | +1.521 / +0.035 | +1.521 / +0.035 | PASS |
| #645 round 2d + fix | ExtraTimingOpt | 21 PASS, 1 INERT, 0 FAIL | +0.013 / +0.069 | +0.013 / +0.069 | +1.561 / +0.036 | +1.561 / +0.036 | FAIL |

Every corner has TNS/THS 0. All six clock-interaction reports retain four 8 ns Ethernet datapath-only checks, with positive slack and no Unsafe rows. Combined logs have no critical warnings or rejected-constraint diagnostics. The reported failing setup path is `pp_shadow/u_pp/u_notify/wr_ix_r_reg[1]` to `pp_shadow/u_pp/u_tx_arbiter/slot_r_reg[1]`, in the 20 ns clock group. No cause or repair is asserted.

Validation completed this round:

- Dev and #645 overlay full-image synthesis: rc 0.
- Complete builder rerun: rc 0; all executed gates pass, one absent retired-board calibration report explicitly NOT RUN.
- Final datapath physical-clock leg: 193 checks, zero failures, rc 0. Round 1 completed constituents and its interrupted aggregate remain recorded separately.
- Round 1 behavioral, planted-defect, Ethernet, patch, checker, lint/parser and documentation evidence is retained.

Acceptance 1 and 2 are met; acceptance 3 is supported by the recorded constituent runs and negative controls; acceptance 4 is NOT MET; acceptance 5 remains unchanged in scope. The broader complete local gates remain unrun at this STOP. No review verdict is claimed.

Both input identities, all six per-corner rows, gate receipts, warning census, artifact hashes/sizes and the failing path excerpt are in the updated HANDOFF.md and prepared PR-BODY.md packet. All long jobs ended. Peak sampled memory was 10.72 GB; minimum free space was 180.80 GB. No push, PR creation, source/configuration change, deployment or hardware access occurred in round 1b. Awaiting a new ruling.
