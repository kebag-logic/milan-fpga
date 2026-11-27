# Receipts index

Generated from the files present (index.py); size in bytes, sha256 prefix, first line.

## pins

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `elf-identity.txt` | 29366 | `3107165a3015c79d` | # every product ELF (plat_ledger.py's platform images and the CPU budget harness's 72 images: 8 arms x 1x1, 8x |

## r10d

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `agg10d.py.txt` | 2774 | `d7d56e3ee99751ff` | #!/usr/bin/env python3 |
| `alone10.py.txt` | 1353 | `b04279ca6d79326d` | #!/usr/bin/env python3 |
| `elf-identity-final.txt` | 20267 | `e09238b36614c0a7` | # every product ELF (plat_ledger.py's platform images and the CPU budget harness's 72 images: 8 arms x 1x1, 8x |
| `hot_apply.py.txt` | 3651 | `96d233b73060f456` | #!/usr/bin/env python3 |
| `hot_cut4.py.txt` | 2381 | `17f09a67bad67731` | #!/usr/bin/env python3 |
| `hot_learn.py.txt` | 3998 | `0dd4d514e0198cbe` | #!/usr/bin/env python3 |
| `poolx.py.txt` | 3293 | `ec406722e295ae6c` | #!/usr/bin/env python3 |
| `postswap10.py.txt` | 2702 | `0177e1e843a13d59` | #!/usr/bin/env python3 |
| `regcost3.py.txt` | 2360 | `7c157b7197dd0272` | #!/usr/bin/env python3 |
| `settle10.py.txt` | 500 | `47b3b93dd1cd6630` | #!/usr/bin/env python3 |
| `srpplant10.py.txt` | 1117 | `30f0b8e45a7a12f3` | #!/usr/bin/env python3 |
| `tx80-elf-identity-e59cf6ea.txt` | 20653 | `8c630ac50259ad93` | # every product ELF (plat_ledger.py's platform images, the 8x8/1if one linked under its 61.0 entry, and the CP |
| `tx80-elf-identity.txt` | 21128 | `26e4f49380e1014c` | # every product ELF (plat_ledger.py's platform images and the CPU budget harness's 72 images: 8 arms x 1x1, 8x |

## r10d/docs

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `docs-steps-235a48c8.txt` | 12751 | `b332058849b85f7c` | # docs workflow steps on 235a48c8 (em-dash base origin/d), 100 steps, 1 with rc != 0 |
| `docs-steps-25ff0632.txt` | 12659 | `7668fd155269004f` | # docs workflow steps on 25ff0632 (em-dash base origin/d), 100 steps, 0 with rc != 0 |

## r10d/gates

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `coverage-8765bfd5.txt` | 9929 | `8cb576427f8628ff` | # gates10.sh step coverage on a clean clone at 8765bfd5 |
| `cpp_idiom-8765bfd5.txt` | 373 | `12c83598bef356a4` | # gates10.sh step cpp_idiom on a clean clone at 8765bfd5 |
| `ctrl_hot_check-8765bfd5.txt` | 107 | `02e8cd7ed61d01c5` | # gates10.sh step ctrl_hot_check on a clean clone at 8765bfd5 |
| `ctrl_hot_selftest-8765bfd5.txt` | 1297 | `2de8b6d283b8685f` | # gates10.sh step ctrl_hot_selftest on a clean clone at 8765bfd5 |
| `fwgate-shard0-8765bfd5.txt` | 89611 | `63f0f6cec392d342` | # sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4 on a clean clone |
| `fwgate-shard1-8765bfd5.txt.gz` | 35450 | `21f2c733cc80d59d` |  |
| `fwgate-shard2-8765bfd5.txt.gz` | 12336 | `23d9dff9e6b2782a` |  |
| `fwgate-shard3-8765bfd5.txt.gz` | 25701 | `8f645c727e9809e1` |  |
| `harness-flip_grade.py_--check_--point_1x1_1if-8765bfd5.txt` | 1844 | `e8c95d786f905411` | Model: under the tiers (slice CTRL_LOOP_SLICE_US, tier 1 aecp-first, tier 2 srp-first, AECP queue) |
| `harness-flip_grade.py_--check_--point_8x8_1if-8765bfd5.txt` | 1447 | `57b8fdd84f36aff3` | \| Point \| Load at the pin \| Flip ceiling \| Compute for the ceiling \| Terms by share (at the pin) \| |
| `harness-flip_grade.py_--selftest-8765bfd5.txt` | 48 | `6be86b826a432a8a` | flip check: 628 of 628 planted controls refused |
| `harness-kept_grade.py_--selftest-8765bfd5.txt` | 3479 | `1198ee40a73f35fa` | [ok] records at the unit by the rule (27,142 cycles, 285 us), kept <= bound: nothing owed or found |
| `harness-load_grade.py_--check-8765bfd5.txt` | 1835 | `1cae6c2075107e42` | \| Point \| Load at the pin \| Load at the donor's measured costs (the pin carries tsn-c-stack#32) \| Ceiling  |
| `harness-load_grade.py_--selftest-8765bfd5.txt` | 45 | `43d9de9746dd4580` | load gate: 28 of 28 planted controls refused |
| `harness-run.py_--self-test-8765bfd5.txt.gz` | 45497 | `cdcda5655b778112` |  |
| `harness-shape_costs.py_--check-8765bfd5.txt` | 680 | `714514acafb9edab` | \| Shape (interfaces, sources, sinks) \| Slice, us \| Build of both, us \| Build of one, us \| SRP record, us  |
| `harness-shape_costs.py_--selftest-8765bfd5.txt` | 55 | `694e4c140b5223ab` | the table of shapes: 25 of 25 planted controls refused |
| `plat_ledger_selftest-8765bfd5.txt` | 12933 | `028e8899ceb0c0a3` | # gates10.sh step plat_ledger_selftest on a clean clone at 8765bfd5 |
| `py_idiom-8765bfd5.txt` | 174 | `16ebab1866a40f5c` | # gates10.sh step py_idiom on a clean clone at 8765bfd5 |
| `py_idiom-dfda4df4.txt` | 501 | `058461aaa7b2d0bb` | # scripts/check_py_idiom.py at dfda4df4 |
| `test_ctrl_memory-4e595c85.txt` | 59956 | `e6262a3a913b5bbf` | # sw/litex/test_ctrl_memory.py at the tree with the 61.0 entry's cases (committed as 4e595c85) |
| `test_ctrl_memory-8765bfd5.txt` | 59925 | `ee070ed87cddbc20` | # gates10.sh step test_ctrl_memory on a clean clone at 8765bfd5 |
| `twin-8765bfd5.txt` | 746 | `103a9f353375fdd9` | # gates10.sh step twin on a clean clone at 8765bfd5 |

## r10d/gates/final

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `coverage-25ff0632.txt` | 9929 | `a7051e8b1c1b0cbe` | # gates10.sh step coverage on a clean clone at 25ff0632 |
| `cpp_idiom-25ff0632.txt` | 373 | `b6c452e60e89feab` | # gates10.sh step cpp_idiom on a clean clone at 25ff0632 |
| `ctrl_hot_check-25ff0632.txt` | 107 | `e85fa1a8f6695cf0` | # gates10.sh step ctrl_hot_check on a clean clone at 25ff0632 |
| `ctrl_hot_selftest-25ff0632.txt` | 1297 | `96d147853cd1bcef` | # gates10.sh step ctrl_hot_selftest on a clean clone at 25ff0632 |
| `fwgate-shard0-25ff0632.txt` | 89610 | `f77a77666caecfcd` | # sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4 on a clean clone |
| `fwgate-shard1-25ff0632.txt.gz` | 35450 | `cc37bd36f3e7b678` |  |
| `fwgate-shard2-25ff0632.txt.gz` | 12338 | `c79e74d8c3c6e441` |  |
| `fwgate-shard3-25ff0632.txt.gz` | 25699 | `dad74f49661a68d3` |  |
| `harness-25ff0632.txt` | 601 | `6a870d12548a5efa` | # gates10.sh step harness on a clean clone at 25ff0632 |
| `harness-flip_grade.py_--check_--point_1x1_1if-25ff0632.txt` | 1844 | `93536d3c54e21c3d` | Model: under the tiers (slice CTRL_LOOP_SLICE_US, tier 1 aecp-first, tier 2 srp-first, AECP queue) |
| `harness-flip_grade.py_--check_--point_8x8_1if-25ff0632.txt` | 1447 | `e76e9d9aacd60854` | \| Point \| Load at the pin \| Flip ceiling \| Compute for the ceiling \| Terms by share (at the pin) \| |
| `harness-flip_grade.py_--selftest-25ff0632.txt` | 48 | `6be86b826a432a8a` | flip check: 628 of 628 planted controls refused |
| `harness-kept_grade.py_--selftest-25ff0632.txt` | 3479 | `1198ee40a73f35fa` | [ok] records at the unit by the rule (27,142 cycles, 285 us), kept <= bound: nothing owed or found |
| `harness-load_grade.py_--check-25ff0632.txt` | 1835 | `1cae6c2075107e42` | \| Point \| Load at the pin \| Load at the donor's measured costs (the pin carries tsn-c-stack#32) \| Ceiling  |
| `harness-load_grade.py_--selftest-25ff0632.txt` | 45 | `43d9de9746dd4580` | load gate: 28 of 28 planted controls refused |
| `harness-run.py_--self-test-25ff0632.txt.gz` | 45498 | `2539c8a342bc8c50` |  |
| `harness-shape_costs.py_--check-25ff0632.txt` | 680 | `d997a913c759710f` | \| Shape (interfaces, sources, sinks) \| Slice, us \| Build of both, us \| Build of one, us \| SRP record, us  |
| `harness-shape_costs.py_--selftest-25ff0632.txt` | 55 | `694e4c140b5223ab` | the table of shapes: 25 of 25 planted controls refused |
| `plat_ledger_selftest-25ff0632.txt` | 12933 | `411ead7f050527db` | # gates10.sh step plat_ledger_selftest on a clean clone at 25ff0632 |
| `py_idiom-25ff0632.txt` | 517 | `2e2ad2e4238779b1` | # gates10.sh step py_idiom on a clean clone at 25ff0632 |
| `test_ctrl_memory-25ff0632.txt` | 59925 | `c887c35938c46da1` | # gates10.sh step test_ctrl_memory on a clean clone at 25ff0632 |
| `twin-25ff0632.txt` | 746 | `235e7ab1bbddae5d` | # gates10.sh step twin on a clean clone at 25ff0632 |

## r10d/hot

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `filter-c63e9d58.txt` | 1800 | `1c5e81846f4e2ebf` | # tools/hot_apply.py: the ruled filter over the 72 link maps the list serves (8 arms x 1x1, 8x8/1if, 8x8/2if x |
| `hashes.txt` | 346 | `fe4e8bbccebf235b` | backlog 63f421364d7bbf85dc716a7fa9515ada7e2cbe9d66f73aba45327ed568e53455 206393 |
| `learn-70468e2a.txt` | 1317 | `48940408b671a5c3` | # tools/hot_learn.py on the 1x1/1if split image, the default (none) arm, at 70468e2a (items 1-5 in, the hot li |
| `learned-295.txt` | 5716 | `f0eab95e85ab14e2` | ctrl_loop ctrl_loop_service |

## r10d/meas

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `agg-e59cf6ea.txt` | 2758 | `13ca2375893935e6` | # tools/agg10d.py over every group run of the pools (tools/poolx.py, one group a run) on e59cf6ea's images (oH |
| `alone-1x1.txt` | 2036 | `ddac6fbe31d1caf1` | 1x1/answering-ports/s-srp-register-both-owed/srp-register-both-owed.log: one record 64,112, more 0 |
| `alone-8x8-1if.txt` | 2140 | `089a331ff1fce385` | 8x8-1if/answering-ports/s-srp-register-both-owed/srp-register-both-owed.log: one record 159,456, more 0 |
| `alone-every-log.txt` | 58352 | `7194c4117f52ca81` | # tools/alone10.py's first line over every log (one-record and more-record SRP passes), both points |
| `groups-e59cf6ea.csv` | 44152 | `8e008df469009060` | point,arm,group,rc,longest_pass_cycles,polls_base,polls_walk,srp_slice,build_slice,round_slice,over_statements |
| `postswap-8x8-1if.txt` | 7050 | `3c457d7db551bd96` | answering-ports srp-register-swap: record at bus 190237205, over the dearest base before it (24,717): 3 passes |
| `regcost-1x1.txt` | 5478 | `39d9a5b3f3832205` | answering-ports srp-register-both-owed at cpu 107887641: apply 54,551, 26,051 past the unit, settle 412, 2 val |
| `regcost-8x8-1if.txt` | 6446 | `b77d998bfdd8690a` | answering-ports srp-register-both-owed at cpu 186659570: apply 149,963, 112,463 past the unit, settle 30,706,  |
| `settle-every-log.txt` | 49521 | `ccecf175b13ed8d4` | # tools/settle10.py over every log: the longest THE SETTLE run that did work |

## r10d/routes

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `plat_ledger.txt` | 1669 | `76fe4fee6a808ef9` | # tb/verilator/ctrl_split_boot/plat_ledger.py in the route clone at e59cf6ea (the 8x8/1if route's images) |
| `route-1x1-1if-c63e9d58.txt` | 1502 | `78d1f70e4a8dac23` | # route of the split image at 1x1/1if, clean clone at c63e9d58, the platform image plat_ledger.py linked there |
| `route-8x8-1if-e59cf6ea.txt` | 1503 | `ad7389037696d610` | # route of the split image at 8x8/1if, clean clone at e59cf6ea, the platform image plat_ledger.py linked there |

## step0

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `load-flip-restated-a35b092f.txt` | 1399 | `71ef79b0cea5417b` | # load_grade.py --check and flip_grade.py --check at a35b092f with load_grade.REGISTRATION_US restated, nothin |
| `regcost-1x1-nowindow.txt` | 4397 | `a14fe32c695fc44d` | answering-ports srp-register at cpu 107821221: apply 30,587, 2,087 past the unit, settle 7,697, 2 values: 1,04 |
| `regcost-8x8-1if-nowindow.txt` | 4769 | `57085902e260d5c8` | answering-ports srp-register at cpu 186528059: apply 77,291, 39,791 past the unit, settle 35,613, 9 values: 4, |
| `regcost-8x8-1if-window.txt` | 4767 | `4c3a4a14137ec9e0` | answering-ports srp-register-burst at cpu 198383492: apply 79,844, 42,344 past the unit, settle 36,708, 9 valu |
| `regcost-table.md` | 1885 | `2f57ae4dba078e47` | # The dearest record of each registering group, a Talker all in (its apply past the unit plus THE SETTLE after |
| `regcost3.py.txt` | 2360 | `7c157b7197dd0272` | #!/usr/bin/env python3 |
| `window-learn.txt` | 2064 | `d6439b6de5fe535c` | # the fourth hot-list window (#977, its ruling on round 9's STOP, item 3): srp-register-swap on the 1x1/1if sp |

## stop10c

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `load-flip-e62e1936.txt` | 913 | `49cae8e76832bffb` | # load_grade.py --check and flip_grade.py --check at e62e1936 (ceiling 0.77 at 8x8/1if) with load_grade.REGIST |
| `regcost-1x1-e62e1936.txt` | 5183 | `f4df08e38415b6b5` | answering-ports srp-register-both at cpu 107845669: apply 54,148, 25,648 past the unit, settle 7,598, 2 values |
| `regcost-8x8-1if-e62e1936.txt` | 6164 | `b95f890d4dbb1fcc` | answering-ports srp-register-both at cpu 187177367: apply 162,757, 125,257 past the unit, settle 37,848, 9 val |
| `regcost3.py.txt` | 2360 | `7c157b7197dd0272` | #!/usr/bin/env python3 |
| `registering-1x1-e62e1936.txt` | 12825 | `3e89665320fb7969` | # the registering groups at 1x1/1if, none and answering-ports, at e62e1936, each run alone (tools/poolx.py): e |
| `registering-8x8-1if-e62e1936.txt` | 14481 | `07f67a5ecbee7b61` | # the registering groups at 8x8/1if, none and answering-ports, at e62e1936 (the delivery bound with one of a b |
