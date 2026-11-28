Status: DONE (20:35). Desk what-ifs by the unchanged rule, from round 1's 4x4 census and round 9's 1x1 census. No new firmware, no route, no commit (branch `arty-4x4-1127` stays at `11f903bd4`; tree clean). Nothing pushed or posted.

[A863], round 2. Full results: [REPORT-whatif.md](REPORT-whatif.md); receipts in `receipts/` (`SHA256SUMS`).

## Answers for the owner's choice

**2x2 on the Arty now, at 80 MHz.** No row at the interpolated costs: least ACMP 34.03 ms (bound 30) and least txL 49.55 ms (49), never in the same candidate.
- With every cost at the 1x1's measurement, a row exists, but narrowly: ACMP 29.77 ms, txL 48.46 ms.
- With every cost at the 4x4's, there is none.
- Undecided on the desk, likely a miss. Only a 2x2 census decides it.
3x3 has no row at 80 MHz under any cost assumption.

**A clock raise to 100 MHz (cycles unchanged).** Every shape has a row by the rule. 4x4: queued 125 ms, pace 5 ms, slice 1250 us; ACMP 27.07, txL 47.00, last notice 113.60 ms; load 0.463; THE SHARE 1.517 ms. 2x2 and 3x3 qualify under both cost bounds.
- "Cycles unchanged" is optimistic for datapath and flash waits; a 100 MHz census must confirm it.
- **Timing: plausible, not shown.** In round 1's three 80 MHz routes only about five sys endpoints lack the 2.5 ns that 100 MHz takes, a different family in each placement (a CPU DMA path; reset fan-out). The rest have +2.5 to +4.5 ns.
  - Against: the -1 part and 94-97 % slice occupancy.
  - #878's 100 MHz pass at 1x1 predates the CPU's move onto sys.
  - A 100 MHz route would decide it.
- 100 MHz divides the VCO exactly. The latency pair must be measured again (#878 read 1,465 ns at 100 MHz against 1,509).

**Firmware work toward 4x4 at 80 MHz.** Uniform: a 13.9 % cut of every measured cost.
Smallest set found (greedy; no single cost and no pair at 50 % each suffices):
- the ordinary AECP record 275 -> 150 us (-45 %);
- the SRP record 375 -> 280 us (-25 %);
- the polls' base 290 -> 215 us (-25 %).
The rule's row is then 140 / 10 / 1200: ACMP 28.57, txL 48.78, last 135.56 ms, load 0.496.

## Recorded

- Milan v1.2 5.4.2.7: formats that do not fit are left out of the advertised set, not refused at SET_STREAM_FORMAT (no bandwidth refusal is available).
- Latency pair: the 4x4 configuration's 1409/100 ns is the board's sum measured on the 1x1 image at 80 MHz, registered as such; not measured on the 4x4 image.

## Method and validation

- `tools/whatif.py`: round 1's derivation with the shape's exact counts and every cost table it reads replaced by the what-if's. Costs are interpolated linearly in N between the measured 1x1 (round 9's merged census) and 4x4.
- It reproduces round 9's installed 1x1 row (125/10/1250, load 0.5014) and round 1's 4x4 result (least ACMP 37.39, txL 58.71) exactly.
- `tools/cuts.py`: the uniform bisection and the greedy set; `receipts/pairs-4x4-80.txt` holds the single and pair checks.
- Scratch `$VALIDATION_STORAGE/arty4x4-a863/whatif/`. No job left running.
