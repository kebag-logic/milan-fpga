# Area: round 3 against round 2 (and main)

The processor's yosys flow, as `syn/yosys/run.sh` lowers it: sv2v of every `hdl/` file, then
yosys 0.66 `synth_xilinx -family xc7 -flatten`, per top and shape (`tools/area.sh`).
LUT is LUT1-6, FF the FD cells, INV the inverters, RAM the distributed-RAM cells.

| `KL_srp_top` | main `a9e84b66` | round 2 `a2fce43` | round 3 `834cc88` | round 3 − round 2 | round 3 − main |
|---|---|---|---|---|---|
| 2x2 (shipping) LUT / INV / FF / RAM | 11,475 / 2,811 / 4,812 / 114 | 13,193 / 2,875 / 5,334 / 114 | 13,030 / 2,981 / 5,334 / 114 | −163 / +106 / 0 / 0 | +1,555 / +170 / +522 / 0 |
| 8x8 LUT / INV / FF / RAM | 23,046 / 3,483 / 9,236 / 179 | 28,193 / 4,037 / 11,224 / 179 | 28,480 / 4,194 / 11,224 / 179 | +287 / +157 / 0 / 0 | +5,434 / +711 / +1,988 / 0 |

| `KL_srp_listener_fsm` | round 2 | round 3 | round 3 − round 2 |
|---|---|---|---|
| N = 2 LUT / FF | 5,892 / 1,456 | 6,476 / 1,456 | +584 / 0 |
| N = 8 LUT / FF | 16,029 / 4,952 | 15,985 / 4,952 | −44 / 0 |

- `a2fce43/`: the round-2 head measured again here, in a clean clone. Its four stat files
  are byte-identical to round 2's published ones.
- `834cc88/`: the round-3 head, in a clean clone of the commit. Its four stat files are
  byte-identical to the measurement of the same RTL before the commit.
- Main's figures are round 2's published `a9e84b66` stat files.
- The flip-flops do not change: round 3 adds no state. The listener's link branch is a few
  terms per sink. The LUT figure of this flow moves by up to about 300 at 2x2 for an edit of
  a few LUT (round 2, `AREA.md`), and here by +584 and −44 for the listener alone at N = 2 and
  N = 8. So the LUT deltas above are not measurements of the edit.
- The yosys logs (`*.log`, 0.6 to 2.2 MB each) are not copied; `834cc88/RAW-RECORDS.txt` records their sizes and sha256. Each run's stat file is its
  `tee -o ... stat` output.
