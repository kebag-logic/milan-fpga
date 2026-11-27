# Receipts index

Generated from the files present (index.py); size in bytes, sha256 prefix, first line.

## .

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `deliv12.py.txt` | 3669 | `106b3d3c82a2b741` | #!/usr/bin/env python3 |
| `elf-identity-3256d1d2.txt` | 19955 | `38ae06a7a2b74265` | # every product ELF (plat_ledger.py's platform images and the CPU budget harness's 72 images) built in a clean |

## docs

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `docs-steps-3256d1d2.txt` | 12669 | `e88460e7b1b9d60f` | # docs workflow steps on 3256d1d2 (em-dash base origin/d), 100 steps, 0 with rc != 0 |

## gates

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `cpp_idiom-3256d1d2.txt` | 316 | `119a4859c80431a1` | cpp idiom: 410 first-party translation units, 202 of them C |
| `harness-3256d1d2.txt` | 546 | `f367f6e86f266340` | run.py --self-test rc=0 self-test: 0 failures |
| `harness-flip_grade.py_--check_--point_1x1_1if-3256d1d2.txt` | 1844 | `93536d3c54e21c3d` | Model: under the tiers (slice CTRL_LOOP_SLICE_US, tier 1 aecp-first, tier 2 srp-first, AECP queue) |
| `harness-flip_grade.py_--check_--point_8x8_1if-3256d1d2.txt` | 1465 | `f32737e97a6d319e` | \| Point \| Load at the pin \| Flip ceiling \| Compute for the ceiling \| Terms by share (at the pin) \| |
| `harness-flip_grade.py_--selftest-3256d1d2.txt` | 48 | `6be86b826a432a8a` | flip check: 628 of 628 planted controls refused |
| `harness-kept_grade.py_--selftest-3256d1d2.txt` | 3479 | `1198ee40a73f35fa` | [ok] records at the unit by the rule (27,142 cycles, 285 us), kept <= bound: nothing owed or found |
| `harness-load_grade.py_--check-3256d1d2.txt` | 1871 | `5e65e5755a311d42` | \| Point \| Load at the pin \| Load at the donor's measured costs (the pin carries tsn-c-stack#32) \| Ceiling  |
| `harness-load_grade.py_--selftest-3256d1d2.txt` | 45 | `5dc8f0541b1aacc3` | load gate: 32 of 32 planted controls refused |
| `harness-run.py_--self-test-3256d1d2.txt.gz` | 45642 | `935fcc0595d77ccb` |  |
| `harness-shape_costs.py_--check-3256d1d2.txt` | 680 | `d997a913c759710f` | \| Shape (interfaces, sources, sinks) \| Slice, us \| Build of both, us \| Build of one, us \| SRP record, us  |
| `harness-shape_costs.py_--selftest-3256d1d2.txt` | 55 | `694e4c140b5223ab` | the table of shapes: 25 of 25 planted controls refused |
| `py_idiom-3256d1d2.txt` | 461 | `e8a6790414554794` | py idiom: 721 first-party modules, 340588 lines |

## meas

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `deliv-1x1-e59cf6ea.txt` | 12171 | `de9b3628300c99ce` | # the deferred deliveries at 1x1/1if (deliv12.py, SINKS 2) over every registering group's log of the none and  |
| `deliv-8x8-1if-e59cf6ea.txt` | 12213 | `f961592cf1b1e641` | # the deferred deliveries at 8x8/1if (deliv12.py, SINKS 9) over every registering group's log of the none and  |
| `load-flip-3256d1d2.txt` | 7185 | `95f186b0a924bb4c` | # load_grade.py --check and --selftest, flip_grade.py --check at 1x1/1if and 8x8/1if and --selftest, and the c |

## Publication note

`gates/harness-run.py_--self-test-3256d1d2.txt.gz` is compressed because its log is over 200 KB. If it is published uncompressed, its published path is `gates/harness-run.py_--self-test-3256d1d2.txt`, and the size and hash prefix above are those of the compressed file. The published manifest (`MANIFEST.json`, `published_sha256`) is the hash authority for the published bytes. In these receipts `<clone>` is the clean clone at the head, `<out>` the gate's output directory, `<scratch>` the work directory, and `<home>` the user's home.
