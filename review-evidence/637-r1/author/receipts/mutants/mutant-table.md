| # | Leg | Planted in | Mutant | Named check that fails | Failures |
|---:|---|---|---|---|---|
| 1 | dynmap | `milan_datapath.sv` | an empty reset: the power-on image holds no mapping | `[DYNMAP] power-on SPI 0: number_of_mappings` | 91 of 331 |
| 2 | dynmap | `milan_datapath.sv` | no clip after the restore: the window ignores a restored input format | `[DYNMAP] restored SPI 0: number_of_mappings` | 6 of 331 |
| 3 | dynmap | `milan_datapath.sv` | no output clip: the window ignores a STREAM_OUTPUT row | `[DYNMAP] window, output row staged at 4 ch: capture RAM keys 0..7 hold the output map` | 2 of 331 |
| 4 | dynmap | `milan_datapath.sv` | the boot writer never fills the crossbar RAMs | `[DYNMAP] power-on: render RAM keys 2..9 hold the input map` | 70 of 331 |
| 5 | dynmap | `milan_datapath.sv` | the CSR writer is not held while the boot writer is busy | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 4 of 331 |
| 6 | dynmap | `milan_datapath.sv` | the input store alone takes a CSR write while the writer is busy | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 2 of 331 |
| 7 | dynmap | `milan_datapath.sv` | the output store alone takes a CSR write while the writer is busy | `[DYNMAP] CSR hold, output: no CSR write splits the store from the RAM` | 2 of 331 |
| 8 | dynmap | `milan_datapath.sv` | the boot window ignores the CLOSED terminal | `[DYNMAP] CSR hold, input: CSR lands in both once the sweep after CLOSED has ended` | 2 of 331 |
| 9 | dynmap | `milan_datapath.sv` | no sweep after the restore's terminal | `[DYNMAP] CLOSED on the roll-back's clock: render RAM keys 2..9 hold the input map` | 6 of 331 |
| 10 | dynmap | `milan_datapath.sv` | no drain clock: busy ends while the last boot write is in flight | `[DYNMAP] CSR hold, input: no CSR write splits the store from the RAM` | 4 of 331 |
| 11 | dynmap | `milan_datapath.sv` | the edit face never waits for the boot writer | `[DYNMAP] edit meets the sweep: the ADD is answered only after the sweep ends` | 2 of 331 |
| 12 | dynmap | `milan_datapath.sv` | the map writer never marks a record dirty | `[MAPREC] empty: the window holds the codec's records and the pend has fallen` | 30 of 331 |
| 13 | dynmap | `milan_datapath.sv` | an empty saved list reads as an erased record (#763) | `[MAPREC] empty, after the power cycle: SPI 0: number_of_mappings` | 17 of 331 |
| 14 | dynmap | `milan_datapath.sv` | no first-dirty window: the change is written at the next tick | `[MAPREC] empty: the write waited out the 500 ms first-dirty window` | 2 of 331 |
| 15 | dynmap | `milan_datapath.sv` | the restore refuses every framed record | `[MAPREC] saved, after the power cycle: SPI 0: number_of_mappings` | 42 of 331 |
| 16 | dynmap | `milan_datapath.sv` | the restore ignores the record's crc16 | `[MAPREC] torn input record: SPI 0: number_of_mappings` | 3 of 331 |
| 17 | dynmap | `milan_datapath.sv` | a failed walk rolls nothing back | `[MAPREC] roll-back: SPI 0: number_of_mappings` | 11 of 331 |
| 18 | dynmap | `milan_datapath.sv` | the roll-back sweeps the RAMs and leaves the stores | `[MAPREC] roll-back: SPI 0: number_of_mappings` | 11 of 331 |
| 19 | dynmap | `milan_datapath.sv` | the roll-back puts the stores back and never sweeps the RAMs | `[MAPREC] roll-back: render RAM keys 2..9 hold the input list` | 3 of 331 |
| 20 | dynmap | `milan_datapath.sv` | the map restore runs over the D3 walk's roll-back | `[MAPREC] D3 roll-back: SPI 0: number_of_mappings` | 6 of 331 |
| 21 | dynmap | `milan_datapath.sv` | GET_AUDIO_MAP does not wait for the map restore | `[MAPREC] held GET: answered with the restored list` | 1 of 331 |
| 22 | dynmap | `milan_datapath.sv` | the format judge does not wait for the map restore | `[MAPREC] held SET_STREAM_FORMAT: SUCCESS against the restored list` | 2 of 331 |
| 23 | dynmap | `milan_datapath.sv` | the entity enable does not wait for the map restore | `[MAPREC] held GET: the entity enable waits for the map restore` | 1 of 331 |
| 24 | dynmap | `milan_datapath.sv` | every phase-5 beat marks its record, changed or not (DR2b) | `[MAPREC] unchanged: no record write follows an unchanged edit` | 3 of 331 |
| 25 | dynmap | `milan_datapath.sv` | a restore write counts as a change | `[MAPREC] saved: the restore itself writes no record` | 2 of 331 |
| 26 | dynmap | `milan_datapath.sv` | a change after the latch does not taint the write | `[MAPREC] taint: the window ends on the final list` | 5 of 331 |
| 27 | dynmap | `milan_datapath.sv` | a fourth attempt follows the third failure | `[MAPREC] failing writes: three attempts, then no more` | 1 of 331 |
| 28 | dynmap | `milan_datapath.sv` | no backoff between attempts | `[MAPREC] failing writes: the attempts are at least 500 ms apart` | 1 of 331 |
| 29 | dynmap | `milan_datapath.sv` | the last failed attempt raises no alarm | `[MAPREC] failing writes: the alarm (PP_STAT[4]) is raised` | 1 of 331 |
| 30 | dynmap | `milan_datapath.sv` | the map restore has no per-wait deadline | `[MAPREC] silent memory: the walk ends at its per-wait deadline` | 1 of 331 |
| 31 | dynmap | `milan_datapath.sv` | the map restore has no aggregate deadline | `[MAPREC] slow memory: SPI 0: number_of_mappings` | 8 of 331 |
| 32 | dynmap | `KL_pp_shadow.sv` | the arbiter does not drain a read the map writer abandoned | `[MAPREC] silent memory, late answer: a later change reaches the window` | 1 of 331 |
| 33 | dynmap | `KL_pp_shadow.sv` | the arbiter's selection moves while the backend serves a command | `[MAPREC] shared face: both writers' records are in the window` | 1 of 331 |
| 34 | dynmap | `KL_pp_shadow.sv` | the map writer's pending is not reported | `[MAPREC] empty: PP_STAT pend rises with the accepted change` | 1 of 331 |
| 35 | dynmap | `KL_pp_shadow.sv` | the map writer's alarm does not reach nvm_alarm | `[MAPREC] failing writes: the alarm (PP_STAT[4]) is raised` | 1 of 331 |
| 36 | listener | `milan_datapath.sv` | an empty reset, under the listener's end-to-end check | `T18 POWER-ON: with no map command since the reset, the lane renders injected events` | 8 of 264 |
| 37 | talker | `milan_datapath.sv` | an empty reset, under the talker's end-to-end check | `[V] every requested column was decoded` | 20 of 134 |
