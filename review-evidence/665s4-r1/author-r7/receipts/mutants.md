| Mutant | File | Caught by | rc | Failing words |
|---|---|---|---:|---|
| head: ctrl_image_selftest (no mutant) | none | | 0 | `ctrl_image self-test: 37 checks PASS` |
| head: placement controls (no mutant) | none | | 0 | `ctrl_split_boot placement controls: 8 of 8 as required` |
| head: stopped_at_link (no mutant) | none | | 0 | `ctrl_plat_image.py endstation_ax7101_1x1_tdm8, 1 interface(s): exit 2; ELF present False; stopped_at_link True` |
| refusal-removed | `sw/firmware/ctrl/test/ctrl_plat_image.py` | ctrl_image_selftest plat | 1 | `AssertionError: ('both archives', 'collect2: error: ld returned 1 exit status')` |
| any-archive-to-all | `sw/firmware/ctrl/test/ctrl_plat_image.py` | ctrl_image_selftest plat | 1 | `AssertionError: ('the C library alone', 'collect2: error: ld returned 1 exit status')` |
| refused-with-a-map | `sw/firmware/ctrl/test/ctrl_plat_image.py` | ctrl_image_selftest plat | 1 | `AssertionError: REFUSED: no --flash-map: a split platform image is never linked on the flash port's RV32 stand` |
| compile-only-refused | `sw/firmware/ctrl/test/ctrl_plat_image.py` | ctrl_runs.stopped_at_link | 1 | `ctrl_plat_image.py endstation_ax7101_1x1_tdm8, 1 interface(s): exit 2; ELF present False; stopped_at_link Fals` |
| guard-call-removed | `tb/verilator/ctrl_split_boot/boot_soc.py` | run.py --placement-controls | 1 | `PLACEMENT export-refuses: WRONG (export TAKEN)` |
| guard-raise-removed | `tb/verilator/ctrl_split_boot/boot_soc.py` | run.py --placement-controls | 1 | `PLACEMENT export-refuses: WRONG (export TAKEN)` |
| deviations-return-empty | `tb/verilator/ctrl_service_budget/split_soc.py` | run.py --placement-controls | 1 | `PLACEMENT register-moved: WRONG (deviations [])` |
| window-unchecked | `tb/verilator/ctrl_service_budget/split_soc.py` | run.py --placement-controls | 1 | `PLACEMENT window-moved: WRONG (deviations [])` |
| guard-refuses-a-true-map | `tb/verilator/ctrl_split_boot/boot_soc.py` | the boot itself | 2 | `REFUSED: python3 exited 1; see <scratch>/mutants/true-map-boot/soc-provisional.log` |
