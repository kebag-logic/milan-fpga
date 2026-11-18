# Receipts index (#946 round 2)

Generated from the files present by make_index.py after sanitizing (host paths replaced by `<lane>`, `<scratch>`, `<tmp>`, `<systmp>`, `<tools>`, `<home>`, `<mgmt>`). Each row: path, size, sha256 prefix, first line.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `boot/composition-d98dd322-1x1-report.txt` | 11646 | `8c7ec2f16f07fbd7` | HEAD d98dd322 start 22:30:12 |
| `boot/composition-d98dd322-8x8-csr-writes-before-ready.txt` | 1668 | `ba49acb703e2c0e6` | # the 8x8 split boot simulation on the composition d98dd322: every CSR window write before ready (bus cycle 6, |
| `boot/composition-d98dd322-8x8-report.txt` | 11493 | `de09f2b8aaa55e3e` | HEAD d98dd322 start 22:26:41 |
| `boot/delta.txt` | 1212 | `a50415ecd2a250e2` | # the split boot simulation, the train head b1f1161b (round 1's receipts boot/train-b1f1161b-*, the same head) |
| `boot/lane-9f4f3de0-8x8-report.txt` | 10694 | `4fd509aee618ed0b` | HEAD 9f4f3de0 start 23:27:37 |
| `budget/image-hashes-arm-a.txt` | 808 | `f8c544796291537a` | # CPU budget harness images, arm A (legs.py build, as run.py builds by default), on the composition d98dd322 |
| `docs/composition-d98dd322-docs-workflow-steps.txt` | 9961 | `a3d803785ac6910c` | 00-check_wire_accountability-selftest rc=0  RESULT: PASS |
| `docs/lane-9f4f3de0-docs-workflow-steps.txt` | 10616 | `16b22946ca4ff1e1` | # the docs workflow steps (the repository's docs workflow, quick.sh) on the lane 9f4f3de0; steps 73, 74, 79, 8 |
| `firmware/platsinks-oldcode-fails.txt` | 5584 | `665489d217ef69c6` | # Sinks at 8x8/1if: round 1's platform (66c6edf3's ctrl_plat.c) with round 2's test_plat_sinks.cpp (as 548324b |
| `firmware/sink-campaign-0f6c12ba.txt` | 5768 | `6dc81629fc5d32be` | # the sink table's 26 planted defects through ctrl_mutants.campaign (the code as 0f6c12ba and 548324b5: ctrl_p |
| `gates/composition-d98dd322-firmware-gate.txt` | 9510 | `39d752e783d9e08e` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 on the composition d98dd322 |
| `gates/composition-d98dd322-fw-coverage.txt` | 9561 | `22e9baadc5b92e97` | HEAD d98dd322 start 23:27:31 |
| `gates/lane-548324b5-firmware-gate.txt` | 10132 | `e6e399e5bef345e7` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 on the lane 548324b5 |
| `gates/lane-548324b5-fw-coverage.txt` | 5382 | `7c4e6af693be0692` | HEAD 548324b5 start 22:03:40 |
| `ledger/composition-d98dd322-ledger.txt` | 3971 | `27dd96952aa96333` | HEAD d98dd322 start 22:07:59 |
| `ledger/lane-548324b5-ledger.txt` | 3778 | `68cd2d4e322be15a` | HEAD 548324b5 start 22:02:44 |
| `memory/composition-d98dd322-test_ctrl_memory.txt` | 55447 | `46a4bda955066238` | # python3 sw/litex/test_ctrl_memory.py, the composition's tree as d98dd322 |
| `memory/lane-9f4f3de0-test_ctrl_memory.txt` | 50239 | `8fd9fabad63accbe` | # python3 sw/litex/test_ctrl_memory.py, the lane at 9f4f3de0 |
| `merge/composition-ledger-raise.patch` | 31363 | `f9b43d50aeaaaa6b` | diff --git a/docs/design/SPLIT_CONTROL_MEMORY.md b/docs/design/SPLIT_CONTROL_MEMORY.md |
| `merge/composition.txt` | 4838 | `9406d96df617f9fd` | # step 12 composition, scratch clone only: git merge-tree --write-tree --name-only b1f1161b 548324b5 |
| `rtl/avtp_rxmon-suite-0f6c12ba.txt` | 6579 | `cc72831c6e193034` | # make -C tb/verilator/avtp_rxmon (pinned Verilator) at 0f6c12ba; no input of this suite changes after it (548 |
| `sweep/SUMMARY.txt` | 1607 | `c17e5b01ea12814c` | # the composition d98dd322's sweep, scripts/run_all_suites.sh --shard k/4, four units (native-shards.py); pinn |
| `sweep/composition-d98dd322-avtp_rxmon.txt` | 6836 | `e1be4e474f80b73f` | # the composition sweep's avtp_rxmon suite (shard 2), result lines |
| `sweep/composition-d98dd322-shard0.txt` | 378 | `0096422f98f5f0a2` | shard: 0/4   selected suites: 15 |
| `sweep/composition-d98dd322-shard1.txt` | 481 | `b6d7dd6263add502` | shard: 1/4   selected suites: 17 |
| `sweep/composition-d98dd322-shard2.txt` | 479 | `fdde591d9dbe9d12` | shard: 2/4   selected suites: 17 |
| `sweep/composition-d98dd322-shard3.txt` | 916 | `d06d2468c1db0656` | shard: 3/4   selected suites: 16 |
| `twin/base-cb96336d-twin-plants.txt` | 225 | `d99d6f1600aea8b0` | plant byte-flip: REFUSED by "ADP frame 1 differs at byte 34" |
| `twin/base-cb96336d-twin.txt` | 4628 | `25afc0bd54852272` | HEAD cb96336d start 23:24:14 |
| `twin/composition-d98dd322-twin-plants.txt` | 5363 | `93fc84bb0c6652cf` | plant byte-flip: REFUSED by "ADP frame 1 differs at byte 34" |
| `twin/composition-d98dd322-twin.txt` | 2558 | `284eacbc59fdd109` | HEAD d98dd322 start 22:09:45 |
| `twin/lane-548324b5-twin-plants.txt` | 225 | `db4cd4e7a37b7fab` | plant byte-flip: REFUSED by "ADP frame 1 differs at byte 34" |
| `twin/lane-548324b5-twin.txt` | 4628 | `8f54253d5b3dad5a` | HEAD 548324b5 start 23:13:05 |
| `twin/lane-vs-base-captures.txt` | 846 | `236d6efbf1216dfc` | # the 1x1 twin's captures, the lane (548324b5; 9f4f3de0 changes one docstring) against dev-soft-core cb96336d, |
