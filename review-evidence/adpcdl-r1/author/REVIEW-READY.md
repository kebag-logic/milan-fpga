REVIEW READY e0b144904e57c96928f1dd3fca36a00df42f6ed3

[A849] tsn-c-stack, branch `adp-long-discover` in `/data-2/milan/tmp/adpcdl-a849/tsn-c-stack`, one commit on main `69bac7c`. Not pushed, nothing posted.

| Check | Result |
|---|---|
| Linux `validate.py --graphs` on a clean clone | rc 0, 28 of 28 steps (gates.json) |
| RV32 `baremetal.py` on the same clone | rc 0, Debug and Release |
| Plants | 484 of 484 caught; the 6 new ones by their named tests (plants.txt) |
| Coverage | 100 % lines and branches after the existing exclusions; `adp_rx` fully covered (adp_rx.gcov.txt) |
| New tests on the old core | exactly the 5 `AcceptsLongControlDataLength` instances fail (red-run-old-core.log) |
| dev-linux | trial merge tree = head tree |
| milan-fpga 5de21ff3 with this core | 1 expected test fails unmodified; with `parent-consumer.patch` every arm run passes, 11 of 11 selected plants caught |

Not run: the complete parent firmware gate (AECP, SRP, lwSRP, platform and MAAP arms), the parent stack boundary gate, hosted CI, any bench.
