# Yosys area of the datapath in both placements

RTL at `61d680dd`. Every later commit to `hdl/` is comment-only (`ce5ee9d9`, `KL_ctrl_split.sv` comments), so the figures hold at the head.
Yosys 0.66 `synth_xilinx` of `milan_datapath`, `CTRL_SPLIT_P` 0 (all-fabric) and 1 (split); the per-run JSON beside this file is the measurement.
A Yosys estimate, not a Vivado placement.

| Shape | Placement | LUT | FF | RAMB36 | RAMB18 | DSP |
|---|---|---|---|---|---|---|
| endstation_ax7101_1x1_tdm8 | all-fabric | 99,794 | 44,073 | 18 | 15 | 21 |
| endstation_ax7101_1x1_tdm8 | split | 60,298 | 23,468 | 3 | 14 | 11 |
| endstation_ax7101_1x1_tdm8 | split minus all-fabric | -39,496 | -20,605 | -15 | -1 | -10 |
| endstation_ax7101_8x8 | all-fabric | 170,479 | 59,357 | 21 | 15 | 21 |
| endstation_ax7101_8x8 | split | 84,327 | 28,722 | 5 | 14 | 11 |
| endstation_ax7101_8x8 | split minus all-fabric | -86,152 | -30,635 | -16 | -1 | -10 |

The split's mailbox side, each elaborated as its own top (`mbx-split1.json`):

- `KL_mbx`: 9,559 LUT, 9,888 FF, 1 RAMB36, 9 RAMB18, 0 DSP
- `KL_mbx_cdc`: 464 LUT, 9,633 FF, 0 RAMB36, 0 RAMB18, 0 DSP

`KL_mbx_cdc` is measured standalone, with every output kept as a port. It is not a measurement of what the image keeps.
