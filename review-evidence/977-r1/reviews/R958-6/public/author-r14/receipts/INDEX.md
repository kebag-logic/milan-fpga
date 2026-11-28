# Receipts index

Generated from the files present (index.py); size in bytes, sha256 prefix, first line.

## .

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `elf-identity-a5b19f70.txt` | 19955 | `d8c2cd65e2dd895b` | # every product ELF (plat_ledger.py's platform images and the CPU budget harness's 72 images) built in a clean |

## docs

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `docs-steps-a5b19f70.txt` | 12669 | `486fab765dced0d2` | # docs workflow steps on a5b19f70 (em-dash base origin/d), 100 steps, 0 with rc != 0 |

## gates

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `cpp_idiom-a5b19f70.txt` | 316 | `119a4859c80431a1` | cpp idiom: 410 first-party translation units, 202 of them C |
| `harness-a5b19f70.txt` | 546 | `f367f6e86f266340` | run.py --self-test rc=0 self-test: 0 failures |
| `harness-flip_grade.py_--check_--point_1x1_1if-a5b19f70.txt` | 1844 | `93536d3c54e21c3d` | Model: under the tiers (slice CTRL_LOOP_SLICE_US, tier 1 aecp-first, tier 2 srp-first, AECP queue) |
| `harness-flip_grade.py_--check_--point_8x8_1if-a5b19f70.txt` | 1465 | `f32737e97a6d319e` | \| Point \| Load at the pin \| Flip ceiling \| Compute for the ceiling \| Terms by share (at the pin) \| |
| `harness-flip_grade.py_--selftest-a5b19f70.txt` | 48 | `6be86b826a432a8a` | flip check: 628 of 628 planted controls refused |
| `harness-kept_grade.py_--selftest-a5b19f70.txt` | 3479 | `1198ee40a73f35fa` | [ok] records at the unit by the rule (27,142 cycles, 285 us), kept <= bound: nothing owed or found |
| `harness-load_grade.py_--check-a5b19f70.txt` | 1871 | `5e65e5755a311d42` | \| Point \| Load at the pin \| Load at the donor's measured costs (the pin carries tsn-c-stack#32) \| Ceiling  |
| `harness-load_grade.py_--selftest-a5b19f70.txt` | 45 | `5dc8f0541b1aacc3` | load gate: 32 of 32 planted controls refused |
| `harness-run.py_--self-test-a5b19f70.txt.gz` | 45643 | `73cdd43374039fa9` |  |
| `harness-shape_costs.py_--check-a5b19f70.txt` | 680 | `d997a913c759710f` | \| Shape (interfaces, sources, sinks) \| Slice, us \| Build of both, us \| Build of one, us \| SRP record, us  |
| `harness-shape_costs.py_--selftest-a5b19f70.txt` | 55 | `694e4c140b5223ab` | the table of shapes: 25 of 25 planted controls refused |
| `py_idiom-a5b19f70.txt` | 461 | `df2c8ea6b7a2b039` | py idiom: 721 first-party modules, 340591 lines |

## meas

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `load-flip-a5b19f70.txt` | 6746 | `80e833f9e6832db9` | # load_grade.py --check and --selftest, load_deliveries.py, flip_grade.py --check at 1x1/1if and 8x8/1if and - |

## Publication note

`gates/harness-run.py_--self-test-a5b19f70.txt.gz` is compressed because its log is over 200 KB. If it is published uncompressed, its published path is `gates/harness-run.py_--self-test-a5b19f70.txt`, and the size and hash prefix above are those of the compressed file. The published manifest (`MANIFEST.json`, `published_sha256`) is the hash authority for the published bytes. In these receipts `<clone>` is the clean clone at the head, `<out>` the gate's output directory, `<scratch>` the work directory, and `<home>` the user's home.
