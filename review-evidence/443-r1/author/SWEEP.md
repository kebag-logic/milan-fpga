# Default datapath sweep chunks

The default Makefile ran unchanged, with each build/run recipe logged.
Every recorded chunk returned zero; the enclosing make also returned zero.
Exact commands are retained in `sweep-chunks.jsonl` and each log.

| Chunk | Step | Exit | Seconds |
|---|---|---:|---:|
| `sweep-chunk-1790306703038876192.log` | `build obj_gptp` | 0 | 17.32 |
| `sweep-chunk-1790306720389175615.log` | `./obj_gptp/Vmilan_dp_gptp` | 0 | 103.78 |
| `sweep-chunk-1790306824209293264.log` | `build obj_gptplat` | 0 | 18.78 |
| `sweep-chunk-1790306843037665962.log` | `./obj_gptplat/Vmilan_dp_gptplat` | 0 | 88.52 |
| `sweep-chunk-1790306931903188509.log` | `build obj_gmstep` | 0 | 18.01 |
| `sweep-chunk-1790306949964116606.log` | `./obj_gmstep/Vmilan_dp_gmstep obj_gmstep/aemi.bin 0` | 0 | 24.42 |
| `sweep-chunk-1790306974454248830.log` | `build obj_dir` | 0 | 16.18 |
| `sweep-chunk-1790306990667724821.log` | `build obj_nxn` | 0 | 18.89 |
| `sweep-chunk-1790307009596300059.log` | `build obj_nxndv` | 0 | 17.52 |
| `sweep-chunk-1790307027149971488.log` | `build obj_nxn8` | 0 | 17.72 |
| `sweep-chunk-1790307044898154339.log` | `build obj_nxn4c` | 0 | 17.26 |
| `sweep-chunk-1790307062184923257.log` | `build obj_nolpf` | 0 | 14.76 |
| `sweep-chunk-1790307076974126147.log` | `build obj_prune` | 0 | 14.45 |
| `sweep-chunk-1790307091453461877.log` | `build obj_ax1x1` | 0 | 13.85 |
| `sweep-chunk-1790307105333177253.log` | `build obj_aclk` | 0 | 0.11 |
| `sweep-chunk-1790307105505643531.log` | `build obj_notify` | 0 | 15.65 |
| `sweep-chunk-1790307121192500023.log` | `build obj_crflic` | 0 | 14.36 |
| `sweep-chunk-1790307135580014820.log` | `./obj_dir/Vmilan_dp_sim` | 0 | 5.62 |
| `sweep-chunk-1790307141272424361.log` | `./obj_notify/Vmilan_dp_notify` | 0 | 13.44 |
| `sweep-chunk-1790307154778688491.log` | `./obj_crflic/Vmilan_dp_crflic` | 0 | 26.42 |
| `sweep-chunk-1790307181231543323.log` | `./obj_nxn/Vmilan_dp_nxn` | 0 | 6.33 |
| `sweep-chunk-1790307187619088649.log` | `./obj_nxndv/Vmilan_dp_nxndv` | 0 | 6.33 |
| `sweep-chunk-1790307193980195314.log` | `./obj_nxn8/Vmilan_dp_nxn8` | 0 | 11.69 |
| `sweep-chunk-1790307205728655833.log` | `./obj_nxn4c/Vmilan_dp_nxn4c` | 0 | 6.38 |
| `sweep-chunk-1790307212167067165.log` | `./obj_nolpf/Vmilan_dp_nolpf` | 0 | 5.62 |
| `sweep-chunk-1790307217852583901.log` | `./obj_prune/Vmilan_dp_prune` | 0 | 0.62 |
| `sweep-chunk-1790307218529156103.log` | `./obj_ax1x1/Vmilan_dp_ax1x1` | 0 | 6.23 |
| `sweep-chunk-1790307224815958860.log` | `./obj_aclk/Vmilan_dp_aclk` | 0 | 460.39 |
| `sweep-chunk-1790307789462124668.log` | `build obj_prefill_target_three_events_high` | 0 | 13.95 |
| `sweep-chunk-1790307849792649612.log` | `build obj_recentre_pulse_ignored` | 0 | 13.1 |
| `sweep-chunk-1790307910006113661.log` | `build obj_recentre_counted_and_cleared_but_not_snapped` | 0 | 13.05 |
| `sweep-chunk-1790307970778796938.log` | `build obj_clock_source_trigger_dropped_from_the_recentre_set` | 0 | 13.34 |
| `sweep-chunk-1790307685271665155.log` | `python3 render_mutants.py` | 0 | 355.51 |
| `sweep-chunk-1790308065934562740.log` | `build obj_c0` | 0 | 15.45 |
| `sweep-chunk-1790308106392835951.log` | `build obj_c1` | 0 | 17.11 |
| `sweep-chunk-1790308148614422394.log` | `build obj_c2` | 0 | 17.0 |
| `sweep-chunk-1790308040847109860.log` | `python3 gmstep_mutants.py` | 0 | 149.57 |

## Simulation verdicts

| Leg | Exit | Report |
|---|---:|---|
| `./obj_gptp/Vmilan_dp_gptp` | 0 | 181 checks: 181 PASS, 0 FAIL |
| `./obj_gptplat/Vmilan_dp_gptplat` | 0 | 181 checks: 181 PASS, 0 FAIL |
| `./obj_gmstep/Vmilan_dp_gmstep obj_gmstep/aemi.bin 0` | 0 | == gmstep: checks: 48   failures: 0 == |
| `./obj_dir/Vmilan_dp_sim` | 0 | milan_datapath: 233 checks, 0 failures |
| `./obj_notify/Vmilan_dp_notify` | 0 | checks: 147   failures: 0 |
| `./obj_crflic/Vmilan_dp_crflic` | 0 | checks: 85   failures: 0 |
| `./obj_nxn/Vmilan_dp_nxn` | 0 | checks: 1708   failures: 0 |
| `./obj_nxndv/Vmilan_dp_nxndv` | 0 | checks: 1710   failures: 0 |
| `./obj_nxn8/Vmilan_dp_nxn8` | 0 | checks: 3136   failures: 0 |
| `./obj_nxn4c/Vmilan_dp_nxn4c` | 0 | checks: 1708   failures: 0 |
| `./obj_nolpf/Vmilan_dp_nolpf` | 0 | milan_datapath: 233 checks, 0 failures |
| `./obj_prune/Vmilan_dp_prune` | 0 | checks: 33   failures: 0 |
| `./obj_ax1x1/Vmilan_dp_ax1x1` | 0 | milan_datapath: 230 checks, 0 failures |
| `./obj_aclk/Vmilan_dp_aclk` | 0 | media_aclk: 188 checks, 0 failures |
| `python3 render_mutants.py` | 0 | 6 checks: 6 PASS, 0 FAIL |
| `python3 gmstep_mutants.py` | 0 | 4 checks: 4 PASS, 0 FAIL |
