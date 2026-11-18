# Receipts index (#946 round 1)

Generated from the files present by make_index.py after sanitizing (host paths replaced by `<lane>`, `<scratch>`, `<tmp>`, `<tools>`, `<home>`, `<mgmt>`). Each row: path, size, sha256 prefix, first line.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `boot/composition-b180fda5-8x8-csr-writes-before-ready.txt` | 1461 | `4b2d188e2cbcfb9a` | 1: CSRW 442197 600 5a060000 |
| `boot/composition-b180fda5-8x8-report.txt` | 2319 | `dd82e8f571acf8df` | 1:HEAD b180fda5 start 19:22:08 |
| `boot/composition-d6d71354-1x1-report.txt` | 794 | `5d635552771ac283` | 1:HEAD d6d71354 start 20:25:46 |
| `boot/delta.txt` | 982 | `08e0f6c421a64571` | # the 8x8 split boot simulation, the train head b1f1161b against the composition (b180fda5; its image inputs a |
| `boot/train-b1f1161b-1x1-report.txt` | 794 | `bfe20d0ecabb73ef` | 1:HEAD b1f1161b start 20:29:07 |
| `boot/train-b1f1161b-8x8-csr-writes-before-ready.txt` | 603 | `dc281795e0613ff3` | 1: CSRW 441748 600 5a060000 |
| `boot/train-b1f1161b-8x8-report.txt` | 794 | `af5250b104cde8fd` | 1:HEAD b1f1161b start 20:21:51 |
| `budget/image-hashes-arm-a.txt` | 521 | `2549c00370de73ba` | # CPU budget harness images, arm A (legs.py build, as run.py builds by default), on the composition b180fda5 |
| `docs/composition-8dbd0a48-docs-workflow-steps.txt` | 9960 | `985dd7836667562d` | 00-check_wire_accountability-selftest rc=0  RESULT: PASS |
| `docs/lane-0749e0d8-docs-workflow-steps.txt` | 10286 | `5a9b12fbbc85660f` | 00-check_wire_accountability-selftest rc=0  RESULT: PASS |
| `firmware/object-size-delta.txt` | 369 | `aba4c5fabe3226f6` | # RV32 sections of the changed objects, dev-soft-core cb96336d against the lane head (platrv32 arm's flags, -O |
| `firmware/shipped-behaviour-fails.txt` | 2608 | `f186e0b892099ac5` | # the platform's open write removed (the shipped firmware writes no context), 8x8/1if and 1x1/1if |
| `gates/composition-8dbd0a48-firmware-gate.txt` | 5525 | `8230d59ffaafb9b0` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 on the composition 8dbd0a48 (code and tests as d6d |
| `gates/composition-8dbd0a48-fw-coverage.txt` | 4487 | `a46ee5873f00506f` | HEAD 8dbd0a48 start 20:14:55 |
| `gates/lane-0749e0d8-firmware-gate.txt` | 5312 | `e34f3fdabe70d785` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 on the lane 0749e0d8 (code and tests as 66c6edf3) |
| `gates/lane-0749e0d8-fw-coverage.txt` | 4380 | `34dd5b25496257d5` | HEAD 0749e0d8 start 20:05:09 |
| `ledger/composition-b180fda5-ledger.txt` | 1058 | `42b2b3bead9f94e3` | 1:HEAD b180fda5 start 19:22:08 |
| `ledger/lane-0749e0d8-ledger.txt` | 936 | `239a2532e75ff766` | 1:HEAD 0749e0d8 start 19:29:11 |
| `merge/composition.txt` | 2056 | `6da1936571715ebe` | # step 12 composition, scratch clone only: git merge-tree --write-tree b1f1161b 0749e0d8 |
| `rtl/avtp_rxmon-suite-lane.rc` | 5 | `93ff7811a209e2a8` | rc=0 |
| `rtl/avtp_rxmon-suite-lane.txt` | 5051 | `f46165131f89da2a` | KL_avtp_rx_monitor: 97 checks, 0 failures |
| `rtl/ctxfmt-N8.log` | 7266 | `d2c67ffeb9a96a6c` | ... Use "/* verilator lint_off PINMISSING */" and lint_on around source to disable this message. |
| `rtl/ctxfmt-mutants.log` | 1121 | `c915b2b0a8122785` | [PASS] the unmutated context engine still passes the N=8 format contract |
| `rtl/verilator-version.txt` | 38 | `46aedd5b30efdd94` | Verilator 5.050 2026-07-01 rev v5.050 |
| `sweep/SUMMARY.txt` | 1407 | `c1c118a477e6e99d` | # the composition 8dbd0a48's sweep, scripts/run_all_suites.sh --shard k/4, four units (native-shards.py); pinn |
| `sweep/composition-8dbd0a48-shard0.txt` | 480 | `a7e41b7764b0dd85` | shard: 0/4   selected suites: 15 |
| `sweep/composition-8dbd0a48-shard1.txt` | 583 | `c9357a4d2201308c` | shard: 1/4   selected suites: 17 |
| `sweep/composition-8dbd0a48-shard2.txt` | 581 | `0810fe665d0b8cba` | shard: 2/4   selected suites: 17 |
| `sweep/composition-8dbd0a48-shard3.txt` | 1096 | `95fb90fa819116f9` | shard: 3/4   selected suites: 16 |
| `twin/base-cb96336d-twin.txt` | 4228 | `4085b9bb8c1e15d0` | 1463:[LEDGER] root-configuration-index: the fabric sends one response, BAD_ARGUMENTS, the received configurati |
| `twin/composition-8dbd0a48-twin-plants.txt` | 9687 | `45bd084e7cc47dd3` | 81:plant missing-notification: REFUSED by "the fabric sent and the split did not: AECP notice STOP_STREAMING 0 |
| `twin/composition-8dbd0a48-twin.txt` | 222 | `571f96f2bed0e913` | 1473:twin: 0 finding(s); counts {'all-fabric': {'ACMP': 7, 'ADP': 12, 'AECP': 53, 'MAAP': 8, 'MSRP': 88, 'MVRP |
| `twin/lane-0749e0d8-twin.txt` | 4228 | `4f9b8491127f02d2` | 1463:[LEDGER] root-configuration-index: the fabric sends one response, BAD_ARGUMENTS, the received configurati |
| `twin/lane-vs-base-captures.txt` | 641 | `6fc81a8823174113` | # the 1x1 twin's captures, the lane 0749e0d8 against dev-soft-core cb96336d (both with the same single finding |
