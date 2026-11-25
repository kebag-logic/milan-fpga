# Receipts, round 7

Head 09201d35d7ea720b3ba205da185ba35c159ec24a. Paths are normalized: `$CHECKOUT` is the lane worktree, `$SCRATCH` the round's scratch directory, `$TOOLS` the shared tool directory, `<home-path>` the user's home.
Each file is a copy of a scratch log or record with only those paths rewritten; the hash is of the copy.

## Hosted evidence at 1516b2ff

Excerpts of hosted run 45469088206 (rtl-fast): `firmware-boundary` job 138726979088 refusing on `tb/verilator/input_loopback_dp/run.py`, and `firmware-verilator` job 138726979378 passing. Excerpts of run 45469087943 (rtl-full) shards 12/19 and 13/19, both cancelled before either loopback suite ran.

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| [`hosted--hosted--firmware-boundary-138726979088.excerpt.log.txt`](hosted--hosted--firmware-boundary-138726979088.excerpt.log.txt) | 1124 | `173c56dc684b0ddf` |
| [`hosted--hosted--firmware-verilator-138726979378.excerpt.log.txt`](hosted--hosted--firmware-verilator-138726979378.excerpt.log.txt) | 22354 | `55518985f00cffa7` |
| [`hosted--hosted--shard12.excerpt.log.txt`](hosted--hosted--shard12.excerpt.log.txt) | 607 | `733ea50df7e6912b` |
| [`hosted--hosted--shard13.excerpt.log.txt`](hosted--hosted--shard13.excerpt.log.txt) | 497 | `eb185431c600d3b5` |

## Firmware boundary gate (item 1)

`--only verilator`: the standalone command stopped at 590 s (`fwv-only-verilator`), then the same four builders captured one per call into one capture (`fwv-cap-*`) and judged with `--require-rv32 --selftest --only verilator --capture` (`fwv-judge`: PASS, 202 controls ok, 0 escaped). `--without verilator`: capture legs 0/2 and 1/2 as the workflow runs them, each stopped at 590 s (`fwb-leg0`, `fwb-leg1`). The judge's text cross-check on a partial capture, with the fix (`fwb-judge-partial-fixed`) and with the entry removed (`fwb-judge-partial-planted`); `reasons-*` are the sorted refusal reasons, the planted run's one extra reason equal to the hosted one. `loopback-found-by-text`: the gate's own discovery over both suites' files.

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| [`boundary--logs--fwv-only-verilator.log.txt`](boundary--logs--fwv-only-verilator.log.txt) | 410 | `3eb1b84f0a9a3b52` |
| [`boundary--logs--fwv-cap-mbx.log.txt`](boundary--logs--fwv-cap-mbx.log.txt) | 15512 | `e15e20f1bb766741` |
| [`boundary--logs--fwv-cap-maap.log.txt`](boundary--logs--fwv-cap-maap.log.txt) | 12987820 | `82fa5336096dfabb` |
| [`boundary--logs--fwv-cap-aecpwire.log.txt`](boundary--logs--fwv-cap-aecpwire.log.txt) | 527 | `d61476ca896e53e2` |
| [`boundary--logs--fwv-cap-loopback-1.log.txt`](boundary--logs--fwv-cap-loopback-1.log.txt) | 76556 | `ed021825e8ed16ae` |
| [`boundary--logs--fwv-cap-loopback-8.log.txt`](boundary--logs--fwv-cap-loopback-8.log.txt) | 77300 | `c0ac3be20427b415` |
| [`boundary--logs--fwv-judge.log.txt`](boundary--logs--fwv-judge.log.txt) | 62174 | `1b55f433aa027b78` |
| [`boundary--logs--fwb-leg0.log.txt`](boundary--logs--fwb-leg0.log.txt) | 397 | `bde26f14981ced08` |
| [`boundary--logs--fwb-leg1.log.txt`](boundary--logs--fwb-leg1.log.txt) | 693 | `5787ce6b13408f66` |
| [`boundary--logs--fwb-partial-capture.log.txt`](boundary--logs--fwb-partial-capture.log.txt) | 1837 | `f664a85e0ea4aa01` |
| [`boundary--logs--fwb-judge-partial-fixed.log.txt`](boundary--logs--fwb-judge-partial-fixed.log.txt) | 2528 | `8a0daf2d92228aa6` |
| [`boundary--logs--fwb-judge-partial-planted.log.txt`](boundary--logs--fwb-judge-partial-planted.log.txt) | 2798 | `00adda72a46535a7` |
| [`boundary--logs--reasons-fixed.txt.txt`](boundary--logs--reasons-fixed.txt.txt) | 2260 | `a09f8dc8b66cd26b` |
| [`boundary--logs--reasons-planted.txt.txt`](boundary--logs--reasons-planted.txt.txt) | 2529 | `428d27ff2b7a4b9b` |
| [`boundary--logs--reasons-hosted.txt.txt`](boundary--logs--reasons-hosted.txt.txt) | 269 | `9fe1897fda3d07ac` |
| [`boundary--logs--loopback-found-by-text.log.txt`](boundary--logs--loopback-found-by-text.log.txt) | 1082 | `4af05aff2b5dee9b` |

## Verilator planner

`planner-selftest` at the head (27 workers). `fit-at-merge-26-workers`: the merge commit's planner at 26 workers with trial figures (scratch probe `tools--fit.py`). `rtl-ownership`: rtl.yml's ownership step for shards 0-26/27 at the replay merge.

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| [`planner--logs--planner-selftest.log.txt`](planner--logs--planner-selftest.log.txt) | 5011 | `9a186ce318cac4b9` |
| [`planner--logs--fit-at-merge-26-workers.txt.txt`](planner--logs--fit-at-merge-26-workers.txt.txt) | 197 | `c88d42393902d729` |
| [`planner--logs--rtl-ownership.log.txt`](planner--logs--rtl-ownership.log.txt) | 1795 | `fe29bed9cc0e9673` |

## Egress ledger

`egress_ledger.py --selftest` PASS (18 mutants). The 8x8-1if harness build at the head and at dev, and the `backlog-owed` group on the reused head build, each stopped at 590 s. `harness-head-vs-dev`: the two builds' images, gateware, CSR map and stimulus configuration compared (PASS).

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| [`egress--logs--egress-ledger-selftest.log.txt`](egress--logs--egress-ledger-selftest.log.txt) | 13520 | `8ef6773238abcc84` |
| [`egress--logs--budget-8x8-1if-build.log.txt`](egress--logs--budget-8x8-1if-build.log.txt) | 20333 | `6486fdb8dae7f5b9` |
| [`egress--logs--budget-8x8-1if-backlog-owed.log.txt`](egress--logs--budget-8x8-1if-backlog-owed.log.txt) | 177 | `7783b4c0fe80f362` |
| [`egress--logs--budget-dev-8x8-1if-build.log.txt`](egress--logs--budget-dev-8x8-1if-build.log.txt) | 20619 | `a2b6504b301aa204` |
| [`egress--logs--harness-head-vs-dev.txt.txt`](egress--logs--harness-head-vs-dev.txt.txt) | 909 | `9c616a7704b885d9` |

## Image identity against 1516b2ff and dev 5de21ff3

`fwimages-compare`: the twelve SRP-composition firmware images (both shapes, one and two interfaces, three compositions) by loaded segments; `fwimages-headers`: their generated headers. `ident-*`: builder artifacts and AEM descriptor images of both shipped configs (the review session's `identity.py` and `compare_identity.py`, run at one output path per tree), with the enabled control.

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| [`identity--logs--fwimages-compare.md.txt`](identity--logs--fwimages-compare.md.txt) | 2079 | `b6662e9b06df205d` |
| [`identity--logs--fwimages-headers.txt.txt`](identity--logs--fwimages-headers.txt.txt) | 232 | `dbe9342e5142c945` |
| [`identity--img--old--fwimages.json.txt`](identity--img--old--fwimages.json.txt) | 28309 | `74e1f6ac29dfc249` |
| [`identity--img--dev--fwimages.json.txt`](identity--img--dev--fwimages.json.txt) | 28309 | `97af340b085c8761` |
| [`identity--img--head--fwimages.json.txt`](identity--img--head--fwimages.json.txt) | 28309 | `97af340b085c8761` |
| [`identity--logs--ident-head-vs-dev.txt.txt`](identity--logs--ident-head-vs-dev.txt.txt) | 402 | `7bbc9cee3728233b` |
| [`identity--logs--ident-head-vs-base.txt.txt`](identity--logs--ident-head-vs-base.txt.txt) | 456 | `918b11026d47738d` |
| [`identity--logs--ident-dev-vs-base.txt.txt`](identity--logs--ident-dev-vs-base.txt.txt) | 212 | `65393e2a867f7afe` |
| [`identity--identity--old.json.txt`](identity--identity--old.json.txt) | 4472 | `b9732c97c8e38078` |
| [`identity--identity--dev.json.txt`](identity--identity--dev.json.txt) | 4472 | `6857f61765a8dc6c` |
| [`identity--identity--head.json.txt`](identity--identity--head.json.txt) | 8976 | `bc14d7e95ed059c6` |

## Loopback suites and campaigns

`suite-input_loopback-premerge-fix`: the leaf suite at e9f95da4, failing on the removed depacketizer ports. The four suite logs at the head, each run as `run_all_suites.sh` runs a suite (`tools--suite1.sh`). Leaf campaign and bounds, parent campaign with its results.json, and the builder driver's loopback gate.

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| [`suites--logs--suite-input_loopback-premerge-fix.log.txt`](suites--logs--suite-input_loopback-premerge-fix.log.txt) | 10629 | `110092643f4df958` |
| [`suites--suites--input_loopback.log.txt`](suites--suites--input_loopback.log.txt) | 28143 | `70fad027a869167a` |
| [`suites--suites--input_loopback_dp.log.txt`](suites--suites--input_loopback_dp.log.txt) | 157543 | `f9545eb5342243e2` |
| [`suites--suites--render_queue.log.txt`](suites--suites--render_queue.log.txt) | 17482 | `d19fee243f5a289c` |
| [`suites--suites--chmap_capture.log.txt`](suites--suites--chmap_capture.log.txt) | 114268 | `79b4817ffa373366` |
| [`suites--logs--suite-input_loopback.log.txt`](suites--logs--suite-input_loopback.log.txt) | 402 | `16e2f5e2a2badbb0` |
| [`suites--logs--suite-input_loopback_dp.log.txt`](suites--logs--suite-input_loopback_dp.log.txt) | 416 | `60e8afeaca99a9cf` |
| [`suites--logs--suite-render_queue.log.txt`](suites--logs--suite-render_queue.log.txt) | 201 | `e7f342a7a5841286` |
| [`suites--logs--suite-chmap_capture.log.txt`](suites--logs--suite-chmap_capture.log.txt) | 203 | `22a9b4a7851cc34c` |
| [`suites--logs--leaf-mutants.log.txt`](suites--logs--leaf-mutants.log.txt) | 508 | `29646beeb842f769` |
| [`suites--logs--parent-mutants.log.txt`](suites--logs--parent-mutants.log.txt) | 640 | `77ac852ebc1bfa0e` |
| [`suites--parent-mutants--results.json.txt`](suites--parent-mutants--results.json.txt) | 10650 | `24975eb38d4270ee` |
| [`suites--logs--builder-input-loopback.log.txt`](suites--logs--builder-input-loopback.log.txt) | 611 | `45a02eec723cf359` |

## Docs workflow replay at the replay merge

`results.json` and every step log: docs.yml's gate steps at a merge of the head into dev-soft-core 5de21ff3, tree a3b3dca8 (equal to the head's tree). `030-selftest`: the compiler-absent step's `--selftest` command.

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| [`docswf--docswf--results.json.txt`](docswf--docswf--results.json.txt) | 11174 | `06a6cab4cf0e46f8` |
| [`docswf--docswf--030-selftest.log.txt`](docswf--docswf--030-selftest.log.txt) | 138 | `f6da142138888df7` |
| [`docswf--docswf--002-wire-accountability-4.log.txt`](docswf--docswf--002-wire-accountability-4.log.txt) | 5267 | `382e33a7f51ccf5c` |
| [`docswf--docswf--006-docs-check-no-git-3.log.txt`](docswf--docswf--006-docs-check-no-git-3.log.txt) | 353 | `495260032b8da0d6` |
| [`docswf--docswf--009-docs-gates-0-3.log.txt`](docswf--docswf--009-docs-gates-0-3.log.txt) | 1078 | `ff57110d5830c4d2` |
| [`docswf--docswf--014-docs-gates-0-11.log.txt`](docswf--docswf--014-docs-gates-0-11.log.txt) | 263 | `f3a79cf536a0eb27` |
| [`docswf--docswf--015-docs-gates-0-12.log.txt`](docswf--docswf--015-docs-gates-0-12.log.txt) | 243 | `e26c38a101291019` |
| [`docswf--docswf--016-docs-gates-0-13.log.txt`](docswf--docswf--016-docs-gates-0-13.log.txt) | 281 | `71d75e95b87caf35` |
| [`docswf--docswf--017-docs-gates-0-14.log.txt`](docswf--docswf--017-docs-gates-0-14.log.txt) | 352 | `8247f10d5a6ef71d` |
| [`docswf--docswf--018-docs-gates-0-15.log.txt`](docswf--docswf--018-docs-gates-0-15.log.txt) | 259 | `e88b7bb2c0ea09d7` |
| [`docswf--docswf--019-docs-gates-0-16.log.txt`](docswf--docswf--019-docs-gates-0-16.log.txt) | 344 | `14c171d9614e64cd` |
| [`docswf--docswf--020-docs-gates-0-17.log.txt`](docswf--docswf--020-docs-gates-0-17.log.txt) | 353 | `b521cd3d1702fb66` |
| [`docswf--docswf--021-docs-gates-0-18.log.txt`](docswf--docswf--021-docs-gates-0-18.log.txt) | 231 | `972f73b1d2b49239` |
| [`docswf--docswf--022-docs-gates-0-19.log.txt`](docswf--docswf--022-docs-gates-0-19.log.txt) | 1685 | `c10ebbfca6108558` |
| [`docswf--docswf--023-docs-gates-0-20.log.txt`](docswf--docswf--023-docs-gates-0-20.log.txt) | 231 | `3ab9ea41f8343b28` |
| [`docswf--docswf--025-docs-gates-0-22.log.txt`](docswf--docswf--025-docs-gates-0-22.log.txt) | 2721 | `2e143a59c695444e` |
| [`docswf--docswf--026-docs-gates-0-23.log.txt`](docswf--docswf--026-docs-gates-0-23.log.txt) | 3408 | `b0733261bd84dc20` |
| [`docswf--docswf--028-docs-gates-0-26.log.txt`](docswf--docswf--028-docs-gates-0-26.log.txt) | 216 | `cf9cf63e264287ac` |
| [`docswf--docswf--030-selftest.log.txt`](docswf--docswf--030-selftest.log.txt) | 138 | `f6da142138888df7` |
| [`docswf--docswf--031-docs-gates-0-30.log.txt`](docswf--docswf--031-docs-gates-0-30.log.txt) | 20347 | `1bf865505cb3d1df` |
| [`docswf--docswf--032-docs-gates-0-31.log.txt`](docswf--docswf--032-docs-gates-0-31.log.txt) | 1313 | `7704a15559a95f4a` |
| [`docswf--docswf--033-docs-gates-0-32.log.txt`](docswf--docswf--033-docs-gates-0-32.log.txt) | 52076 | `cdae4bfb853c6f29` |
| [`docswf--docswf--034-docs-gates-0-33.log.txt`](docswf--docswf--034-docs-gates-0-33.log.txt) | 4937 | `a7df508930f5f63d` |
| [`docswf--docswf--035-docs-gates-0-34.log.txt`](docswf--docswf--035-docs-gates-0-34.log.txt) | 3559 | `0cd61baccdd7e44e` |
| [`docswf--docswf--036-docs-gates-0-35.log.txt`](docswf--docswf--036-docs-gates-0-35.log.txt) | 40707 | `035a69fc7c1a8c3e` |
| [`docswf--docswf--037-docs-gates-0-36.log.txt`](docswf--docswf--037-docs-gates-0-36.log.txt) | 5138 | `cb971a1c7de246b2` |
| [`docswf--docswf--038-docs-gates-0-37.log.txt`](docswf--docswf--038-docs-gates-0-37.log.txt) | 12629 | `e3b18b0447a1c0a0` |
| [`docswf--docswf--039-docs-gates-0-38.log.txt`](docswf--docswf--039-docs-gates-0-38.log.txt) | 2844 | `7cc1c59e8341a411` |
| [`docswf--docswf--040-docs-gates-0-39.log.txt`](docswf--docswf--040-docs-gates-0-39.log.txt) | 33286 | `31ea223ddf3c82b1` |
| [`docswf--docswf--041-docs-gates-0-40.log.txt`](docswf--docswf--041-docs-gates-0-40.log.txt) | 4078 | `097121d86f573d10` |
| [`docswf--docswf--042-docs-gates-0-41.log.txt`](docswf--docswf--042-docs-gates-0-41.log.txt) | 3277 | `4556cc504bc98529` |
| [`docswf--docswf--043-docs-gates-0-42.log.txt`](docswf--docswf--043-docs-gates-0-42.log.txt) | 4835 | `f2d8ce10ad90162b` |
| [`docswf--docswf--044-docs-gates-0-43.log.txt`](docswf--docswf--044-docs-gates-0-43.log.txt) | 3089 | `0cfa858c8f46d5a1` |
| [`docswf--docswf--045-docs-gates-0-44.log.txt`](docswf--docswf--045-docs-gates-0-44.log.txt) | 2792 | `4df399bcd51cb90a` |
| [`docswf--docswf--046-docs-gates-0-45.log.txt`](docswf--docswf--046-docs-gates-0-45.log.txt) | 200 | `9b5a15a14e5cdaf2` |
| [`docswf--docswf--047-docs-gates-0-46.log.txt`](docswf--docswf--047-docs-gates-0-46.log.txt) | 230 | `8dd7669c1ea19338` |
| [`docswf--docswf--048-docs-gates-0-47.log.txt`](docswf--docswf--048-docs-gates-0-47.log.txt) | 298 | `5d0714b0a4d877d6` |
| [`docswf--docswf--049-docs-gates-0-48.log.txt`](docswf--docswf--049-docs-gates-0-48.log.txt) | 247 | `d0d217cf3226cc26` |
| [`docswf--docswf--050-docs-gates-0-49.log.txt`](docswf--docswf--050-docs-gates-0-49.log.txt) | 3705 | `c6c91a1584429870` |
| [`docswf--docswf--051-docs-gates-0-50.log.txt`](docswf--docswf--051-docs-gates-0-50.log.txt) | 26923 | `0b51f866da495ce6` |
| [`docswf--docswf--052-docs-gates-0-51.log.txt`](docswf--docswf--052-docs-gates-0-51.log.txt) | 10417 | `0361c9121b2b1e21` |
| [`docswf--docswf--053-docs-gates-0-52.log.txt`](docswf--docswf--053-docs-gates-0-52.log.txt) | 29104 | `587b81947258748e` |
| [`docswf--docswf--054-docs-gates-0-53.log.txt`](docswf--docswf--054-docs-gates-0-53.log.txt) | 3862 | `46b4db2b03dc2a52` |
| [`docswf--docswf--056-docs-gates-0-55.log.txt`](docswf--docswf--056-docs-gates-0-55.log.txt) | 176391 | `8923aa8be007dd41` |
| [`docswf--docswf--079-docs-gates-2-15.log.txt`](docswf--docswf--079-docs-gates-2-15.log.txt) | 384472 | `3172113b8fb11eac` |
| [`docswf--docswf--080-docs-gates-2-16.log.txt`](docswf--docswf--080-docs-gates-2-16.log.txt) | 131391 | `af7d5b10ef7314d7` |

## Scratch tools

Every script this round wrote or reused, as run.

| File | Bytes | SHA-256 (first 16) |
|---|---:|---|
| [`tools--tools--ciexec.sh.txt`](tools--tools--ciexec.sh.txt) | 768 | `288503de801cb133` |
| [`tools--tools--cmpharness.py.txt`](tools--tools--cmpharness.py.txt) | 1753 | `00513df6d69505c6` |
| [`tools--tools--cmpimg.py.txt`](tools--tools--cmpimg.py.txt) | 1114 | `72457238e679af84` |
| [`tools--tools--compare_identity.py.txt`](tools--tools--compare_identity.py.txt) | 1486 | `7328e01b8391ed1f` |
| [`tools--tools--fit.py.txt`](tools--tools--fit.py.txt) | 693 | `73ba692a56c95417` |
| [`tools--tools--found.py.txt`](tools--tools--found.py.txt) | 1111 | `448b3f6c6295d45a` |
| [`tools--tools--fwimages.py.txt`](tools--tools--fwimages.py.txt) | 2493 | `6496a078b7d05256` |
| [`tools--tools--henv.sh.txt`](tools--tools--henv.sh.txt) | 686 | `94e6ad34135d1e08` |
| [`tools--tools--identity.py.txt`](tools--tools--identity.py.txt) | 3113 | `a1c8e87d79d424fa` |
| [`tools--tools--pack.py.txt`](tools--tools--pack.py.txt) | 3099 | `ae9f3aa2ac7168d3` |
| [`tools--tools--rows.py.txt`](tools--tools--rows.py.txt) | 612 | `4a878a491cb02ed4` |
| [`tools--tools--suite1.sh.txt`](tools--tools--suite1.sh.txt) | 794 | `01598c74f8c04e22` |
| [`tools--tools--wfreplay.py.txt`](tools--tools--wfreplay.py.txt) | 4225 | `76a2ab9437078521` |
