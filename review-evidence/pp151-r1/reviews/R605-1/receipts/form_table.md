| form | P | Verilator 5.050 lint | sv2v 0.0.12 + Yosys 0.66 | sv2v 0.0.13 + Yosys 0.66 |
|---|---|---|---|---|
| fatal_mod | 0 | refused: %Warning-USERFATAL: r605_fatal_mod.sv:6:5: probe: P=0 must be at least 1 | refused: lowered_tc012_fatal_mod.v:10: ERROR: FATAL: . | refused: lowered_tc013_fatal_mod.v:12: ERROR: System task `$finish' executed. |
| fatal_mod | 1 | elaborates | elaborates | elaborates |
| error_mod | 0 | refused: %Warning-USERERROR: r605_error_mod.sv:6:5: probe: P=0 must be at least 1 | refused: lowered_tc012_error_mod.v:10: ERROR: probe: P=%0d must be at least 1. | elaborates |
| error_mod | 1 | elaborates | elaborates | elaborates |
| warning_mod | 0 | refused: %Warning-USERWARN: r605_warning_mod.sv:6:5: probe: P=0 must be at least 1 | elaborates | elaborates |
| warning_mod | 1 | elaborates | elaborates | elaborates |
| info_mod | 0 | elaborates | elaborates | elaborates |
| info_mod | 1 | elaborates | elaborates | elaborates |
| fatal_init | 0 | elaborates | refused: lowered_tc012_fatal_init.v:10: ERROR: Can't resolve task name `$fatal'. | refused: lowered_tc013_fatal_init.v:11: ERROR: System task `$finish' executed. |
| fatal_init | 1 | elaborates | elaborates | elaborates |
