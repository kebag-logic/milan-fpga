# [A525] The issue #639 lockstep benches (processor PR #155)

These are the two benches whose results round 1 recorded in HANDOFF.md §4.1 and §4.2 and
in the PR body. They are published here as they ran, with the result set the record
cites (`results-head9eebc61/`). Since round 2, the arm-port rings' full-queue path is also
graded in the tree by `tb/pp_top` section AQ's drive (AQ3, AQ4). These benches stay the
evidence that both structures match `main` cycle for cycle.

Revisions:
- Reference: processor `main` `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- Candidate: `9eebc61`. Its two files are byte-identical at the round-1 head `9e86991`.
  At the round-2 head, the top differs only by a comment inside the ring's banner (S1).
  The extracted arm-port block includes that banner. A re-cut at the round-2 head
  differs from `dut.sv` in that comment and in the generated first line, which names
  the file it was cut from, and nowhere else (checked).
- Simulator: Verilator 5.050 (the pinned build).

## What is here and what is not

`SHA256SUMS` lists every published file. `GENERATED.sha256` lists, with digest and size,
the inputs the benches generate from processor sources. Those inputs are copies or cuts
of the tree, so they are not published. Each regenerates byte for byte with the steps
below; this was checked for every file.

## `armq/`: the top's timer arm-port block

| File | Role |
|---|---|
| `extract.py` | Cuts the block from a `protocol_processor_top.sv`. The cut runs from the `// ====` line above "timer arm-port priority mux (banner)" to the line before the `// ====` above "PRNG draw-port owner mux (banner)", byte for byte. It wraps the block with the eight faces as inputs and the arm port and drop counter as outputs. `--mutate OLD NEW` plants one exact edit. |
| `controls.sh` | Writes `ctl_*.sv`: six planted controls and one probe, each cut from the candidate top. |
| `tb_top.sv`, `sim.cpp` | `armq_ref` beside `armq_dut` on identical arms. Seeds 1-4 use bursty "shaped" phases; seeds 5-8 use fully random rates with long saturation. Resets are taken mid-run. The port, its valid and the drop counter are compared after both clock phases. The bench exits 1 on any mismatch. |
| `build.sh`, `run_matrix.sh` | Build one binary per extract and slot width; run the candidate at slot widths 6 (1x1), 7 (8x8), 5 and 8, then each control at 6, with 8 seeds x 1,000,000 cycles each. |

To regenerate and re-run, from this directory:

```sh
git -C <processor> show 5c71928a:hdl/top/protocol_processor_top.sv > top_main.sv
git -C <processor> show 9eebc61:hdl/top/protocol_processor_top.sv  > top_head.sv
python3 extract.py top_main.sv armq_ref ref.sv
python3 extract.py top_head.sv armq_dut dut.sv
sh controls.sh top_head.sv
sha256sum -c GENERATED.sha256   # from the parent directory, armq/ lines
# build.sh names pp_pkg.sv by its scratch path: edit its PKG= line to <processor>/hdl/common/pp_pkg.sv
sh run_matrix.sh again          # writes results-again/
```

Result (`results-head9eebc61/summary.txt` and one log per run):

| Run | Runs x cycles | Mismatches | Runs caught |
|---|---|---:|---:|
| candidate, slot widths 5, 6, 7, 8 | 32 x 1,000,000 | 0 | |
| `ctl_wr_at_head` | 8 x 1,000,000 | 6,039,149 | 8 of 8 |
| `ctl_wr_at_mid` | 8 x 1,000,000 | 9,552,242 | 8 of 8 |
| `ctl_head_stuck` | 8 x 1,000,000 | 9,799,762 | 8 of 8 |
| `ctl_read_tail` | 8 x 1,000,000 | 11,760,798 | 8 of 8 |
| `ctl_write_refused` | 8 x 1,000,000 | 922,754 | 8 of 8 |
| `ctl_ring_of_three` | 8 x 1,000,000 | 6,420,932 | 8 of 8 |
| `ctl_probe_head_unreset` (a probe: the head index needs no reset) | 8 x 1,000,000 | 0 | 0 of 8 |

## `lsn/`: the ACMP listener

| File | Role |
|---|---|
| `gen_top.py` | Writes `tb_lsn.sv` and `fields.txt`: `main`'s `KL_pp_acmp_listener` (renamed `KL_pp_acmp_listener_ref`) beside the candidate on identical inputs, every output concatenated per instance. |
| `mkctl.py` | Writes `ctl_*.sv`: five planted copies of the candidate. |
| `sim.cpp` | Emulates the faces: RX slot sync read, TX slot grant, PRNG, timer expiries, TK events, preloads, started and stopped requests, and lock. It answers about half of the listener's own PROBE_TX commands with a matching PROBE_TX_RESPONSE, so streams settle. Every output is compared after both clock phases, with resets mid-run. |
| `build.sh`, `run_matrix.sh`, `run_controls.sh` | Run the candidate at `N_SINKS_P` 2 (1x1), 9 (8x8), 8, 1 and 3, then each control at 2, with 8 seeds x 1,000,000 cycles each. |

To regenerate and re-run, from this directory:

```sh
git -C <processor> show 5c71928a:hdl/acmp/KL_pp_acmp_listener.sv \
  | sed -e 's/^module KL_pp_acmp_listener$/module KL_pp_acmp_listener_ref/' \
        -e 's/^endmodule : KL_pp_acmp_listener$/endmodule : KL_pp_acmp_listener_ref/' > ref_listener.sv
git -C <processor> show 9eebc61:hdl/acmp/KL_pp_acmp_listener.sv > dut_listener.sv
python3 mkctl.py dut_listener.sv
python3 gen_top.py
python3 <processor>/hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex
sha256sum -c GENERATED.sha256   # from the parent directory, lsn/ lines
# build.sh names the package directory by its scratch path: edit its B= line to <processor>/hdl
sh run_matrix.sh again
```

Result (`results-head9eebc61/summary.txt` and one log per run):

| Run | Runs x cycles | Mismatches | Runs caught |
|---|---|---:|---:|
| candidate, `N_SINKS_P` 2, 9, 8, 1, 3 | 40 x 1,000,000 | 0 | |
| `ctl_read_sink_zero` | 8 x 1,000,000 | 15,836,966 | 8 of 8 |
| `ctl_read_sampled_in_idle` (a register sampled in X_IDLE: the stale read) | 8 x 1,000,000 | 15,862,266 | 8 of 8 |
| `ctl_started_bit_unstored` (record bit 12) | 8 x 1,000,000 | 15,605,320 | 8 of 8 |
| `ctl_settled_vlan_bit_unstored` (record bit 305) | 8 x 1,000,000 | 1,613,238 | 8 of 8 |
| `ctl_sweep_misaddressed` (X_INIT writes `sink_r`) | 8 x 1,000,000 | 5,295,758 | 8 of 8 |
