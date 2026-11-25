# Receipts, head ec727b64663b4eef2fc8da1ea5e0eae6541597d1

Paths in logs are relative to the repository or to the build directory; host prefixes were removed, and nothing else was changed.

| File | What it shows |
|---|---|
| commits-and-merge.txt | the two commits and their files; trial merges with dev-linux and main |
| tools.txt | tool versions of the two gates |
| validate.log, validate.rc, gates.json | the Linux gate on a clean clone, 28 of 28 steps rc 0 |
| baremetal.rc, rv32-results.json | the RV32 gate on the same clone |
| coverage.txt, adp_rx.gcov.txt | the coverage gate; line and branch counts of `adp_rx` |
| plants.txt | the eleven length plants and the campaign total, 489 of 489 |
| own-mutants-e0b1449.txt | the published `own_mutants.py TREE WORK '<'` at round 1: 7 mutants survive, beside the control |
| own-mutants-head.txt | the same at this head: the 15 mutants caught, `control-unmutated` passes |
| overread.txt | the published overread control and the unchanged core, plain and under address and undefined-behaviour sanitizers, three test filters |
| overread-asan.txt | the sanitizer's report: a read past the 82-octet allocation from `accepted_discovery` |
| old-core-run.txt | these tests on main's core: the five accept instances fail, 44 pass |
| rv32-smoke-exits.txt | the smoke image's exit: head 0; exact comparison 64; mask 0x00FF 64; check removed 63 |
| parent-consumer.patch | the milan-fpga test and plant changes for the pin bump |
| consumer-arms.log | nine consumer arms with the patch at 5de21ff3, all pass |
| consumer-plants.log | 10 of 10 selected plants caught, rc 0; test naming judged over the full table of 847 |
| consumer-rv32-hot-entity-bounds.log | the rv32, hot, entity and service_bounds arms |
