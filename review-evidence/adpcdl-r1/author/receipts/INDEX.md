# Receipts, head e0b144904e57c96928f1dd3fca36a00df42f6ed3

| File | What it shows |
|---|---|
| commit-stat.txt | the commit and its files |
| tools.txt | tool versions of the two gates |
| validate.log, validate.rc, gates.json | the Linux gate on a clean clone, every step rc 0 |
| baremetal.rc, rv32-results.json | the RV32 gate on the same clone |
| coverage.txt, adp_rx.gcov.txt | the coverage gate; line and branch counts of `adp_rx` |
| plants.txt | the six new plants and the campaign total |
| red-run-old-core.log | the new tests on main's core: 5 fail, 20 pass (`*AdpInputControl*`) |
| green-run.log | the whole ADP binary on the changed core: 44 pass |
| sizes-and-merge.txt | RV32I sizes of adp.c, main against head; the dev-linux trial merge |
| consumer-unmodified-tests.log | milan-fpga's `adp` arm, its tests unmodified: 1 expected failure |
| parent-consumer.patch | the milan-fpga test and plant changes for the pin bump (applies to 5de21ff3) |
| consumer-arms.log | nine consumer arms with the patch, all PASS |
| consumer-plants.log | 11 of 11 selected plants caught (the rc 1 is the subset, see HANDOFF) |
| consumer-rv32-hot-entity-bounds.log | the rv32, hot, entity and service_bounds arms, rc 0 |
