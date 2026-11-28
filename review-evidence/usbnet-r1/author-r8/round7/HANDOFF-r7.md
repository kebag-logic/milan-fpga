Status: STOP. ETA: measurement and evidence complete; a corrective design decision is required before implementation can resume. No completion ETA is claimed for that undecided change.

Local head: `a4f00496fdaede7a6e6baee46e360f7cbc7f0c95`. Branch: `1011-usbnet`. No push or posting. Bench and flash untouched.

The requested dependency `640699e6866602b2a5de5d404c43f3bd4df8037c` is a parent of merge `91252ecf7457287079d5d2f794b8544f0d9d34c4`; its commits were not rewritten. All fourteen files changed by its round-10 commit are byte-identical at the final head. The conflict in the firmware mutation fixture took the dependency version. Round-7 implementation changes only tests and documentation; the fabric LED design and control firmware remain unchanged.

The full injected link-rate census finished: 159 cases, all eight images, no omitted stimulus. The replay of the original census changed 44 cases' tails and refused 15 cases' successful-commit free-space outcomes, so its cost evidence was not carried alone. The fresh census includes one 1539-wire-octet injection (123.2 us) plus the measured 260 ns handshake at every busy period, through the live queue's backpressure. Every trace was independently replayed across eight stream phases with exact phase-zero departure agreement. All native stimuli are byte-identical to the dependency campaign.

The unchanged rule and #969 disposition reproduce the installed row as a fixed point. No scheduling constant or bound was adjusted. The complete candidate and cost tables are in [DERIVATION.md](receipts/DERIVATION.md). The rule-selected row remains slice 1250 us, AECP pace 10 ms, queued bound 125 ms and stated TX bound 35 ms. Retry cold/attempt/notice terms remain [130, 30, 230] us; poll base is 235 us, centisecond 160 us, LINK 205 us, MAAP 165 us and withdrawal 95 us.

| Check | Measured or derived | Unchanged bound | Result |
|---|---:|---:|---|
| Load | 0.501397114035 | 0.70 | PASS |
| ACMP | 29.84000 ms | 30 ms | PASS |
| txL | 48.90000 ms | 49 ms | PASS |
| Last notice | 117.58000 ms | 140 ms | PASS |
| THE SHARE | 1.7923875 ms | 2 ms | PASS |
| Wire egress, including all terms | 644.980750 us | 1000 us | PASS |
| Held AECP last delivery | 62.03635 ms | 61.99 ms | FAIL |

The blocking case is `none/backlog-owed`: last AECP delivery exceeds the frozen held-egress ledger by 46.35 us. Six other held-egress rows pass. The ordinary owner model and the 1 ms wire gate do not waive that failure. The service gate explicitly rejects any increase beyond a frozen ledger entry. No smaller host segment, empty-ring injection rule or firmware pacing change was selected.

The shipping MII attachment measured 257.5 ns maximum across 512 length/phase cases; it rounds to 260 ns. The fixed path independently measured 312.5 ns and remains stated at 320 ns. The queue already charges the handshake; the final expression conservatively adds it once more: `(558.835 + 54.88) * 1.05 + 0.32 + 0.26 = 644.980750 us`. The largest-wait witness is `none/aecp-largest-notice`, stream phase 5. The 54.88 us term is the inherited gPTP burst. The maximum recorded queue occupancy is 27 records, below the inherited 254-record capacity. Host-local RX remains bounded at 38.075 us by the production mailbox test (81 checks); together with the derived ACMP row this is 29.878075 ms, below 30 ms.

Six fresh builds establish same-pin ELF and map-header identity against the dependency. Fresh Arty SoC generation also confirms the map used by those builds; the raw CSV changes only its generation timestamp. These comparisons use the requested dependency and its current pins. The earlier packet used a different tsn-c-stack pin, so its older ELF hashes are not the comparison baseline. Whole-ALINX-bitstream identity is not claimed.

| Image | ELF SHA-256 | Comparison |
|---|---|---|
| ax7101 | `6e0a54124483adfadd04e8e6f62d296bdf884794b197d0ed9dc24c71de49fd56` | identical |
| ax8x8 | `0f1450acefdd7fa0173d1de3221f8c5a6456e59d96fc99611b5121b1c26a2c3f` | identical |
| arty | `f17d1a9da8ba6e50a1e8cf0af9b77ed434288a1d0a689a357a0c6a57ecda92cf` | identical |

Every control map header has SHA-256 `5f0c602687dacba302959ebb99763e5922aff8ad19f76e7c7c05919b45a936fa`. Pins on both sides:

```text
 efeb541ae5fe1e078332d8462dca2fc2d9cb8db5 external (heads/main)
 3ce71b768a2f6f6a5274c127080146e755d02275 gptp-processor (remotes/origin/640-m7-124-g3ce71b7)
 801ef2283ec793e35a2590fc6593c90313a64041 protocol-processor (v2.0-912-g801ef22)
 d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b third_party/lwSRP (heads/main)
 c3bff8f3dea03870ea7ae62965db360b509ee3b3 third_party/tsn-c-stack (heads/main)
 48ff7a7e2ef782cf778d47910cf85835c64b1bce third_party/verilog-axis (heads/master)
```

Validation: 92,755 USB/LED checks and four real SET_CLOCK_SOURCE cases pass; all 72 existing named RTL plants are caught. The new shipping-chain test catches both physical handshake plants. The injection grader passes nine clean controls and catches nine planted defects. The inherited egress grader passes 17 controls. Existing CBS, shaper-core and queue regressions pass (130,256 / 1,521,627 / 13 checks). Full traces, manifests, commands and source hashes are retained in [receipts/INDEX.md](receipts/INDEX.md).

A second gate remains failed: keeping `docs/DOCUMENTATION_AUDIT.md` byte-identical to the dependency leaves out the two existing USB documentation pages. The freshness gate reports that exact difference. No exception to the byte-identity instruction was assumed. The prior inventory, failing output and decision record are preserved. Other focused code, documentation and evidence gates pass as listed in the index.

No current-head physical route or release is claimed. This round generated maps through the required lowest-priority slot but did not synthesize or route. Earlier route, attachment, external-I/O and whole-image crossing limitations remain open; the earlier physical result is not promoted to proof for the new firmware ROM. No independent approval, hosted gate success or merge into `dev` is claimed. Issues #1011 and #1018 remain related, not closed.
