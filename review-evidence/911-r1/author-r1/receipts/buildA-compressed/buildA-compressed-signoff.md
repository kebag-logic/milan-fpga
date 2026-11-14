# buildA-compressed: signoff facts of buildA
| corner | WNS ns | TNS ns | failing setup | WHS ns | THS ns | failing hold | WPWS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Slow_0C | 0.174 | 0.000 | 0 | 0.102 | 0.000 | 0 | 0.264 |
| Slow_85C | 0.174 | 0.000 | 0 | 0.102 | 0.000 | 0 | 0.264 |
| Fast_0C | 1.633 | 0.000 | 0 | 0.036 | 0.000 | 0 | 0.264 |
| Fast_85C | 1.633 | 0.000 | 0 | 0.036 | 0.000 | 0 | 0.264 |
| all (both models) | 0.174 | 0.000 | 0 | 0.036 | 0.000 | 0 | 0.264 |
timing constraints met: True
check_timing no_clock: 0
check_timing constant_clock: 0
check_timing pulse_width_clock: 0
check_timing unconstrained_internal_endpoints: 0
check_timing no_input_delay: 46
check_timing no_output_delay: 87
check_timing multiple_clock: 0
check_timing generated_clocks: 0
check_timing loops: 0
check_timing partial_input_delay: 0
check_timing partial_output_delay: 0
check_timing latch_loops: 0
util Slice LUTs: 53590 of 133800 (40.05 %)
util LUT as Logic: 49764 of 133800 (37.19 %)
util LUT as Memory: 3826 of 46200 (8.28 %)
util Slice Registers: 54971 of 267600 (20.54 %)
util Slice: 19672 of 33450 (58.81 %)
util F7 Muxes: 941 of 66900 (1.41 %)
util Block RAM Tile: 87.5 of 365 (23.97 %)
util DSPs: 15 of 740 (2.03 %)
util Bonded IOB: 109 of 285 (38.25 %)
util BUFGCTRL: 11 of 32 (34.38 %)
util MMCME2_ADV: 1 of 10 (10.00 %)
util PLLE2_ADV: 2 of 10 (20.00 %)
bitstream header part: 7a200tfbg484; payload 5566832 B; .bit 5567050 B sha256 db315d7a33b71d8d288ce9b26791464bb36b1a0b897ca9b9bc6cbee89055dcc1
aem_desc.bin 7512 B sha256 bdfde7cf448ed032ffb1663b0898aeef9ded3bb11b4ead5dc36dfa3df873f180
flashboot_layout.json 853 B sha256 3f8c4e9f7c5530d24e7978da64f441fa241142b3c7853414e271ef0ba23c1b11
nets with routing errors: 0
iob pack: 21 PASS, 0 FAIL
