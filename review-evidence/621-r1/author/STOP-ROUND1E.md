[A576] STOP

Parent head: `034e2e30f225f3fcd755cac8ad01c60dda5b366a`.
Donor head: `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`.
Both are unchanged. No round 1e commit was made.

[Ruling 6088189432](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6088189432) authorizes the refresh only if every verdict field stays byte-identical. Any change is a STOP. The full refresh campaign ran at the candidate head on Verilator 5.052. All six arms and all three controls exit 0. Each arm ran its receipt `command` byte for byte. Both 8x8 contract arms (CPU 50 MHz) change verdict fields in their first captures:

| Arm, capture | Field | Receipt (`measurements.json` line) | Candidate |
|---|---|---:|---:|
| 8x8 ON, 0 | `sys_cycles` / `responses` / `reads` | 1385074 / 91 / 3549 (`:496`) | 1385678 / 92 / 3558 |
| 8x8 ON, 1 | `sys_cycles` / `responses` / `reads` | 1386484 / 92 / 3587 (`:508`) | 1384682 / 91 / 3575 |
| 8x8 ON, 2 | `sys_cycles` | 1386318 (`:520`) | 1386046 |
| 8x8 OFF, 0 | `sys_cycles` | 1367682 (`:711`) | 1369030 |
| 8x8 ON summary | minimum / maximum / margin | 13.84836 / 13.86484 / 3.53412 (`:487`) | 13.84682 / 13.86318 / 3.53454 |
| 8x8 OFF summary | minimum | 13.67682 (`:702`) | 13.68947 |
| Published 8x8 / 50 MHz | maximum / margin | 13.86484 / 3.53412 (`:1350`) | 13.86318 / 3.53454 |

Captures 3 to 15 keep every verdict field. The 1x1 arms and both 8x8 / 100 MHz arms keep every verdict field. Every capture stays below 24.5 ms. `requests` differs in 24 traffic-ON rows and stays positive. All traffic-OFF counters stay zero.

**Attribution: dev, not this lane.** Both 8x8 / 50 MHz arms ran at two more clean trees with the same recipe and simulator:

| Tree | Rows against the receipt |
|---|---|
| Receipt's measured tree `a2f17342` (donor `5dce647a`, protocol `b2db3a97`) | all 16 rows and every summary field equal, both arms |
| Original base `5603c353` (donor `5dce647a`, protocol `2ad2f845`) | capture logs byte-identical to the candidate's, both arms |

The firmware side is identical across the three trees: the AEM image (19520 bytes, CRC `0x2104c2d3`), the BIOS and every memory initialization file match. The cause is the capture-SoC RTL that changed on dev after `a2f17342` (the 30 files listed in round 1d). It shifts the first three captures; later rows realign. No single commit was isolated. The 1x1 traffic-ON log is byte-identical to the round 1d runs, so the harness is deterministic.

The would-be refresh diff has 56 field changes: 18 provenance fields, 24 `requests` values and 14 verdict fields. Two provenance fields are outside the ruling's list:
- the four 8x8 arms' `config_sha256` changes (dev `6178aa1bd`, a model-lint waiver; the flash image is unchanged);
- `remeasurement_assignment` would name this ruling.

A refresh would also leave `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1625-1628`, `:1641-1643` and `:1660-1661` stale (measured commit and pin, 13.86484 ms, 3.5341x, the 8x8 / 50 MHz table rows). That page is outside this lane.

**Decisions needed:**
1. Whether to accept the 14 dev-caused verdict-field changes.
2. Whether to accept the two unlisted provenance fields.
3. Whether this lane updates the stale design-page figures.

The nine completed runs are at these heads and this recipe, and can be composed into the refresh without rerunning.

Reproduce from each clean checkout. Use the recipe's offline environment with networking disabled and Verilator 5.052 first on `PATH`:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir "$RESULTS/8x8-50-off"
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir "$RESULTS/8x8-50-on"
```

The receipt diff is empty; its SHA-256 remains `ed871bdd09bde7ebde1ae021cd647e3cad354d3f8682c5b7308cda91e4cbd72a`, and the input gate is unchanged. The 61-suite sweep and vendor stages were not started; no vendor lock was taken. HANDOFF.md and PR-BODY.md hold the row-by-row tables, the full field-level diff and size/SHA-256 receipts. The worktrees are clean, no validation job remains, and nothing was pushed or opened as a PR. The later physical repeat still closes #621.
