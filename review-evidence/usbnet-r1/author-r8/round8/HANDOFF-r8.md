Status: REVIEW READY for round-8 desk scope. ETA: complete.

Local head: `701f294405d47a81eed1079d32b54e1eea4a4f31` on `1011-usbnet`. Two local commits; nothing pushed or posted. Bench, flash and physical implementation were untouched.

Applied the [held-egress ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667) exactly. The separate `arty-usbnet-1x1` point derives each figure from the larger original Arty or injected measurement under #894's unchanged rule. The table lives in `docs/design/USB_NET_PATH.md`. The original `arty-1x1` and `8x8-1if` figures are unchanged. Six figures match the original Arty ledger; the last AECP figure derives as `60 + 1.05 * 2.03635 = 62.1381675` ms, rounded upward to 62.14 ms. Its measurement has 103.65 us margin. All seven remain recorded service-budget misses, within their ruled ledger; this is not a waiver of service budgets.

Regraded all 159 retained traces across the same eight images. Every raw trace and stimulus was verified against the retained packet; every regenerated grade is byte-identical to round 7. All eight complete per-image regrades pass with the existing #969 disposition. The final ledger leg passes with no new miss, no larger miss and no missing measurement. No native measurement was rerun.

| Check | Result | Bound or figure |
|---|---:|---:|
| Load | 0.501397114035 | 0.70 |
| ACMP | 29.84000 ms | 30 ms |
| txL | 48.90000 ms | 49 ms |
| Last notice | 117.58000 ms | 140 ms |
| THE SHARE | 1.7923875 ms | 2 ms |
| Complete wire egress | 644.980750 us | 1000 us |
| USB held AECP last delivery | 62.03635 ms | 62.14 ms |

The installed scheduling row remains slice 1250 us, pace 10 ms, queued bound 125 ms and stated transmit bound 35 ms. Its costs, derivation and fixed-point evidence are unchanged. The current owner model equals the retained model exactly. Adding the local mailbox bound of 38.075 us gives ACMP 29.878075 ms, still below 30 ms. The wire evidence was carried only after verifying every retained replay's trace, source and parameter binding and rerunning its aggregate verdict; no fresh wire replay is claimed.

Controls at the final head:

- The complete retained data still fails at `arty-1x1`, solely for 62.03635 ms versus 61.99 ms. That expected failure is retained, not cleared at the old point.
- A retained-data fixture at 62.14 ms passes the USB point. At one 80 MHz cycle higher, 62.1400125 ms (62.14001 at the existing grade resolution), it fails solely for that row.
- The ledger self-test passes 218 control executions and catches all 25 mutations. It reads both documents and tests all three points, including every row's one-cycle excess.
- All fourteen focused final-head gates pass. Contents controls pass 1501/1501; inventory controls pass 60/60. The generated inventory was written by its own generator in its own commit. Whitespace checks and the final worktree are clean.

No firmware, RTL, queue model, configuration, scheduling constant or submodule pin changed. The other thirteen files from #1004's `640699e6866602b2a5de5d404c43f3bd4df8037c` remain byte-identical, including `SPLIT_CONTROL_MEMORY.md`. The inventory is the sole authorized exception among those fourteen dependency files.

The six retained same-pin builds were rehashed, and their implementation inputs are unchanged since the measured merge. Both sides of each Arty and ALINX comparison still match. This is an identity carry with fresh hash verification, not a new build.

| Image | ELF SHA-256 |
|---|---|
| Arty | `f17d1a9da8ba6e50a1e8cf0af9b77ed434288a1d0a689a357a0c6a57ecda92cf` |
| ALINX 1x1 | `6e0a54124483adfadd04e8e6f62d296bdf884794b197d0ed9dc24c71de49fd56` |
| ALINX 8x8 | `0f1450acefdd7fa0173d1de3221f8c5a6456e59d96fc99611b5121b1c26a2c3f` |

All control map headers: `5f0c602687dacba302959ebb99763e5922aff8ad19f76e7c7c05919b45a936fa`.

Pins on both sides:

```text
 efeb541ae5fe1e078332d8462dca2fc2d9cb8db5 external (heads/main)
 3ce71b768a2f6f6a5274c127080146e755d02275 gptp-processor (remotes/origin/640-m7-124-g3ce71b7)
 801ef2283ec793e35a2590fc6593c90313a64041 protocol-processor (v2.0-912-g801ef22)
 d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b third_party/lwSRP (heads/main)
 c3bff8f3dea03870ea7ae62965db360b509ee3b3 third_party/tsn-c-stack (heads/main)
 48ff7a7e2ef782cf778d47910cf85835c64b1bce third_party/verilog-axis (heads/master)
```

Commits:

- `9da0ba5fc17201e6b030babb8f73714d96f14306` Derive a separate held-egress ledger for USB networking
- `701f294405d47a81eed1079d32b54e1eea4a4f31` Regenerate the documentation inventory for USB networking

Round-7 simulation, filter/LED plants, injection controls and shaping evidence remain applicable because their sources and implementation inputs are unchanged; they were not rerun in this ledger-only round. Earlier physical-route, attachment, external-I/O and whole-image crossing limitations remain open. No new routed image, board observation, independent approval, hosted gate success or issue completion is claimed. The separate source points and existing #969 debt remain explicit. Use `Relates to #1011` and `Relates to #1018`.

Receipts and reproduction: [INDEX.md](receipts/INDEX.md), [derivation](receipts/DERIVATION.md), [qualification](receipts/qualification.json). The foreground jobs retained the unit's CPU weight 200; scratch used 12.90 GiB and /data retained 21.25 GiB free. Gate cleanup removals were logged before execution. No additional build or implementation run was needed.
