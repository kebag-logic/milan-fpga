# Receipts index (#946 round 3)

Generated from the files present by make_index.py after sanitizing (host paths replaced by `<lane>`, `<scratch>`, `<tmp>`, `<systmp>`, `<tools>`, `<home>`, `<mgmt>`). Each row: path, size, sha256 prefix, first line.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `budget/image-hashes-arm-a.txt` | 440 | `c34bb3cb2974657e` | # CPU budget harness images, arm A (legs.py build, as run.py builds by default) |
| `docs/composition-f8694fdd-docs-workflow-steps.txt` | 10030 | `4722796bf53ff951` | # the docs workflow steps on the composition f8694fdd: 97 of 97 rc=0 |
| `docs/lane-fe297847-docs-workflow-steps.txt` | 10455 | `e3c96b5abc7e171f` | # the docs workflow steps on the lane fe297847; steps 73, 74, 79, 80 and 81 run scripts only the flip train ha |
| `firmware/new-plants.txt` | 794 | `74b47ca92c5aa186` | # the two plants R867-2-F-1 asks for, through ctrl_mutants.campaign (the tree as fe297847's sink_mutants.py):  |
| `firmware/sinks-both-shapes.txt` | 4274 | `b4849d8c7af970f9` | # the platsinks arms (8x8/1if, then 1x1/1if) with round 3's tests, the tree as cbbd1ac0 and fe297847 (the next |
| `gates/composition-f8694fdd-firmware-gate.txt` | 9656 | `e8113067394aaf63` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 on the composition f8694fdd |
| `gates/composition-f8694fdd-fw-coverage.txt` | 9561 | `c2947db3e7ad0df2` | HEAD f8694fdd start 00:06:58 |
| `gates/lane-fe297847-firmware-gate.txt` | 10278 | `0e133c829496875a` | # test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 on the lane fe297847 |
| `gates/lane-fe297847-fw-coverage.txt` | 5382 | `437973bc93aee2dd` | HEAD fe297847 start 00:06:35 |
| `ledger/composition-f8694fdd-ledger.txt` | 3971 | `64d38c202c9cf1c9` | HEAD f8694fdd start 00:07:00 |
| `ledger/lane-fe297847-ledger.txt` | 3778 | `908577e9d73352da` | HEAD fe297847 start 00:06:37 |
| `ledger/product-images-unchanged.txt` | 824 | `09213d509044cd9d` | # the platform (product) image at each ledger point: round 2 (lane 548324b5, composition d98dd322) against rou |
| `memory/lane-fe297847-test_ctrl_memory.txt` | 50238 | `7dc45e023328bab8` | # python3 sw/litex/test_ctrl_memory.py on the lane fe297847 |
| `merge/composition.txt` | 1210 | `c9b9508b8c68ced8` | # step 12 composition at the lane's round-3 head fe297847, scratch clone only, by round 2's recipe (receipts/m |
