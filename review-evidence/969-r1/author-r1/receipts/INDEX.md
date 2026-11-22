# Receipts index

Generated from the files present (index.py); size in bytes, sha256 prefix, first line.

## budget

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `grader-flip_grade.py_--check_--point_1x1_1if.txt` | 1784 | `983985379645607f` | Model: under the tiers (slice CTRL_LOOP_SLICE_US, tier 1 aecp-first, tier 2 srp-first, AECP queue) |
| `grader-flip_grade.py_--check_--point_8x8_1if.txt` | 1364 | `e38ea5785c40a017` | \| Point \| Load at the pin \| Flip ceiling \| Compute for the ceiling \| Terms by share (at the pin) \| |
| `grader-load_grade.py_--check.txt` | 1793 | `92b4cc02c193bc5b` | \| Point \| Load at the pin \| Load at the donor's measured costs (the pin carries tsn-c-stack#32) \| Ceiling \| Co |
| `grader-shape_costs.py_--check.txt` | 620 | `802b685df64e78a1` | \| Shape (interfaces, sources, sinks) \| Slice, us \| Build of both, us \| Build of one, us \| SRP record, us \| THE |
| `hot-code-identity-platform-f863258d.txt` | 1173 | `bf0b526f96fbed36` | # text symbols of the platform images (ctrl_plat_image.py, /1if), base dd163e41 (its plat_ledger run) vs the f |
| `hot-code-identity.txt` | 1012 | `c578d9ef56549dcb` | # text symbols of the CPU budget harness's images, base dd163e41 vs head (954e5572; firmware as f6f83166): siz |
| `inputs-and-image-hashes.txt` | 634 | `958326908dd92a4f` | # git diff --stat 954e5572 f6f83166 over the budget images' inputs (firmware, harness, builder, configs, LiteX |
| `per-probe-base-vs-head.txt` | 9727 | `1d9ff3c08f395b2c` | # per-probe sys cycles, base dd163e41 vs head (954e5572, firmware as f6f83166), the five groups; worst pass an |
| `run-summary-base-1x1.txt` | 1613 | `dbb17d5336fe2968` | # head dd163e41438acb86e0c4d4e76df90f3f91ace1c0 status:  |
| `run-summary-base-8x8-1if.txt` | 1615 | `7e5c9c17028f817f` | # head dd163e41438acb86e0c4d4e76df90f3f91ace1c0 status:  |
| `run-summary-g4-1x1.txt` | 1613 | `3c28feed5df97f1c` | # head 954e5572cb9bd7d0c10165df224f9f27ac1a5076 status:  |
| `run-summary-g4-8x8-1if.txt` | 1615 | `1305f9de266e0b75` | # head 954e5572cb9bd7d0c10165df224f9f27ac1a5076 status:  |

## docs

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `01-docs_check.log` | 205 | `02e3f479ff8afcd1` | CMD /usr/bin/python3 scripts/docs_check.py |
| `04-check_em_dash-basedd163e41-c6ef2329.log` | 261 | `a7fec11dd3cd1149` | CMD <tools>/md-venv-40cdefe08ebd/bin/python3 scripts/check_em_dash.py --base dd163e4143 |
| `04-check_em_dash-basedd163e41.log` | 261 | `e0fdef3f2826abfc` | CMD <tools>/md-venv-40cdefe08ebd/bin/python3 scripts/check_em_dash.py --base dd163e4143 |
| `63-check_py_idiom-c6ef2329.log` | 542 | `3b6601e519f9046f` | CMD /usr/bin/python3 scripts/check_py_idiom.py |
| `63-check_py_idiom.log` | 542 | `fffc6d748739be3d` | CMD /usr/bin/python3 scripts/check_py_idiom.py |
| `72-gen_toc-check.log` | 200 | `4396a503305d16bf` | CMD <tools>/md-venv-40cdefe08ebd/bin/python3 scripts/gen_toc.py --check |
| `docs-workflow-aca559e3.txt` | 10054 | `ec7246f2320800e1` | # the docs workflow's 103 commands (the flip lane's table, the em-dash base dd163e41), quick.sh on a clean clo |
| `docs-workflow-c6ef2329.txt` | 10071 | `73a215173fd032b3` | # the docs workflow's 103 commands (the flip lane's table, the em-dash base dd163e41), quick.sh on a clean clo |
| `docs-workflow-commands.tsv` | 8770 | `f75e5f397e6621fa` | 00-check_wire_accountability-selftest	/usr/bin/python3 scripts/check_wire_accountability.py --self-test |
| `docs-workflow-f863258d.txt` | 10071 | `e7d0a4ef802a5a40` | # the docs workflow's 103 commands (the flip lane's table, the em-dash base dd163e41), quick.sh on a clean clo |

## failing-first

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `HOW.md` | 497 | `d57effe4deb67c63` | # Failing first |
| `platsinks-1x1-if1.log` | 11059 | `32a3ed0f11191a31` | [endstation_builder] WARNING: platform.mac_address 02:4b:4c:4b:4c:01 has the U/L bit set: it is locally admini |
| `platsinks-8x8-if1.log` | 11893 | `1ce2c0b0bb050c0c` | [endstation_builder] WARNING: platform.mac_address 02:4b:4c:4b:4c:01 has the U/L bit set: it is locally admini |
| `srp_mbx-endstation_ax7101_1x1_tdm8-if1.log` | 5767 | `c69c84d58a2904fb` | ilure |
| `srp_mbx-endstation_ax7101_1x1_tdm8-if2.log` | 6106 | `f55ffcd8df28559b` | wrote <scratch>/b/ff/srp-b/build/srp-srp_mbx-if2-endstation_ax7101_1x1_tdm8/contract/KL_mbx_pkg.sv (2 interfac |
| `srp_mbx-endstation_ax7101_8x8-if1.log` | 5762 | `84e97c021f814969` | ilure |
| `srp_mbx-endstation_ax7101_8x8-if2.log` | 6086 | `7be9f2509d489b70` | wrote <scratch>/b/ff/srp-d/build/srp-srp_mbx-if2-endstation_ax7101_8x8/contract/KL_mbx_pkg.sv (2 interfaces) |

## failing-first-final

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `HOW.md` | 1110 | `a1645003cafd81bb` | # Failing first, at the final head |
| `platsinks-1x1-if1.log` | 11061 | `be001a6321970bbb` | [endstation_builder] WARNING: platform.mac_address 02:4b:4c:4b:4c:01 has the U/L bit set: it is locally admini |
| `platsinks-8x8-if1.log` | 11893 | `9d8945e814325f3f` | [endstation_builder] WARNING: platform.mac_address 02:4b:4c:4b:4c:01 has the U/L bit set: it is locally admini |
| `srp_mbx-endstation_ax7101_1x1_tdm8-if1.log` | 5767 | `3f5c0106d2239691` |  Which is: '\0' |
| `srp_mbx-endstation_ax7101_1x1_tdm8-if2.log` | 6106 | `2fbc11bbb31e25d1` | wrote <scratch>/b/ff/srp-b/build/srp-srp_mbx-if2-endstation_ax7101_1x1_tdm8/contract/KL_mbx_pkg.sv (2 interfac |
| `srp_mbx-endstation_ax7101_8x8-if1.log` | 5762 | `753e6fc3159eb78f` |  Which is: '\0' |
| `srp_mbx-endstation_ax7101_8x8-if2.log` | 6086 | `e63e2b5dc36d6e56` | wrote <scratch>/b/ff/srp-d/build/srp-srp_mbx-if2-endstation_ax7101_8x8/contract/KL_mbx_pkg.sv (2 interfaces) |

## firmware

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `final-head-image-identity-f863258d.txt` | 1106 | `3a3b15f4a7c27358` | # the firmware gates ran at 4c5018eb; the final head f863258d differs from it by: |
| `final-head-image-identity.txt` | 1002 | `c12dd0610e45ca2b` | # the firmware gates ran at 4c5018eb; the final head e4518a0f differs from it by: |
| `firmware-gate-4c5018eb-shard0.log` | 86540 | `56a8b4efc10a1050` | [endstation_builder] WARNING: platform.mac_address 02:4b:4c:4b:4c:01 has the U/L bit set: it is locally admini |
| `firmware-gate-4c5018eb-shard1.log.gz` | 32639 | `dc62e41ea5169f53` |  |
| `firmware-gate-4c5018eb-shard2.log.gz` | 11894 | `af1ff74ed33e1655` |  |
| `firmware-gate-4c5018eb-shard3.log.gz` | 19776 | `d9118d873347dc50` |  |
| `fw_coverage-check-4c5018eb.log` | 9873 | `a7c532318b41a9a3` | toolchain: {'cc': 'gcc (GCC) 16.2.1 20260810', 'cxx': 'g++ (GCC) 16.2.1 20260810', 'gcov': 'gcov (GCC) 16.2.1  |
| `fw_coverage-check-c6ef2329.log` | 9873 | `a7c532318b41a9a3` | toolchain: {'cc': 'gcc (GCC) 16.2.1 20260810', 'cxx': 'g++ (GCC) 16.2.1 20260810', 'gcov': 'gcov (GCC) 16.2.1  |
| `fw_coverage-check-f863258d.log` | 9873 | `3b1f8751f197d489` | toolchain: {'cc': 'gcc (GCC) 16.2.1 20260810', 'cxx': 'g++ (GCC) 16.2.1 20260810', 'gcov': 'gcov (GCC) 16.2.1  |

## ledger

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `plat_ledger-and-memory-test-4c5018eb.log` | 67951 | `3f27d49a740d3925` | COMMAND $HOME/litex-milan/venv/bin/python3 -B <checkout>/tb/verilator/ctrl_service_budget/runtime_ssp.py --pic |
| `plat_ledger-and-memory-test-f6f83166.log` | 67951 | `6c267ae2763a5cf2` | COMMAND $HOME/litex-milan/venv/bin/python3 -B <checkout>/tb/verilator/ctrl_service_budget/runtime_ssp.py --pic |
| `plat_ledger-base-dd163e41-points.txt` | 459 | `e24799b6d2e7ceef` | POINT 1x1-if1: rom 126,432 B, sram 56,736 B, 45 RAMB36 (the 56-RAMB36 budget), ctrl_plat 18048 B: PASS |

## release

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `release-all-fabric-base-vs-head.txt` | 1088 | `45e025a2209d2bf6` | # the AX7101 release export with BUILD_PLACEMENT=all-fabric (sw/litex/build.sh ax7101 --dry-run, its milan_soc |

## routes/base-reference

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `signoffs.txt` | 3064 | `3aead06ad82155a3` | # the base's route reference: the flip lane's (PR #960) round-1 signoffs of the split images whose inputs equa |

## routes

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `route-1x1-1if-ExtraPostPlacementOpt.txt` | 3137 | `9143ca7d14695718` | # route of the split image at 1x1/1if, clean clone at f6f83166 (firmware as at the final head but for b56664fe |
| `route-8x8-1if-ExtraPostPlacementOpt.txt` | 3143 | `56cf33b1f83407f7` | # route of the split image at 8x8/1if, clean clone at f6f83166 (firmware as at the final head but for b56664fe |

## twin

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `twin-plants-maps-4c5018eb.txt` | 36703 | `74ca1da087a97392` |  1173 \|     $error("milan_datapath: AUDIO_IF_RENDER_SLOTS_P=%0d exceeds the render crossbar's TDM key lane CHM |

