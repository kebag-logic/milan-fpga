Status: REVIEW READY for independent review. ETA: author work complete.

[A826], issue #979, round 2. Local head `2e278379c1ae9ea09063b3e3cb183d0e8a3f0929` on `pf-loopbram-1`; intended base `dev-soft-core`. Worktree clean. No push or board operation.

The nine-cluster port probe passed. Implemented widths are `[9,8,8,8,8,8,8,7]`: port 0 retains physical plus eight loopback destinations; port 7 has seven. The 63 independent loopback destinations and independent physical destination fit 64 keys. The 1x1 shape has 16 keys. The option defaults off.

The separate sample RAM, scheduled mapped copy, synchronous reads, one-frame delay and invalidation/silence behavior are implemented. Both wire shapes pass, all seven fault plants are detected, affected render/capture suites pass, the 114-gate builder union passes, and all 63 portability tops pass. One existing historical calibration row remains unrun because its external Arty report is absent. Disabled builder artifacts, descriptor images and firmware ROM bytes match the baseline.

| Shape | Placement | LUT | FF | RAMB36 / RAMB18 | Slices | Min WNS ns | Min WHS ns | Floor |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1x1/1if | AltSpreadLogic_high | 32971 | 42686 | 63 / 37 | 14290 | 0.290 | 0.036 | PASS |
| 8x8/1if | ExtraPostPlacementOpt | 49097 | 54663 | 94 / 34 | 15803 | 0.233 | 0.025 | PASS |

The fresh leaf increment is 650 LUTs, 259 FFs and 1 RAMB18, versus 2088 LUTs, 2360 FFs and 1 RAMB36 for the legacy capture-lane increment. Integrated figures include map and control-image growth.

The enabled 8x8 control-memory allocation is 70.5 RAMB36-equivalent tiles: +11.5 above the unchanged 59.0 ledger entry, or +14.5 above the 56-tile default budget. This is S14 debt. The normal allocator still refuses that enabled image. The separate measurement export records the refusal and overrides the allocation check only in its temporary process; no owner ledger or product guard changed. The 1x1 allocation is 46.5 tiles (45.0 disabled), within 56.

[REVIEW-READY.md](REVIEW-READY.md) records commands, the complete placement sweep, proof limits and acceptance evidence. [PR-BODY.md](PR-BODY.md) is prepared for `pf-loopbram-1` into `dev-soft-core`. [receipts/INDEX.md](receipts/INDEX.md) indexes compressed, privacy-checked receipts. [DESIGN.md](DESIGN.md) records the chosen design. No independent review or merge approval is claimed.

REVIEW READY 2e278379c1ae9ea09063b3e3cb183d0e8a3f0929

Manager note: the five lane-labelled commit subjects were reworded before the push (tree unchanged, a765d48 -> 2e278379).
