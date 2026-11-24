# Round 6 receipts

Candidate head: c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99.
Prior reviewed head: 9acb9b828b29aba71bd51303a4836f86c2278267.
Final merge the replays read: 79d350657a5966306c87a607ffc3e52ecf6abc05 (tree ecaf54ccedc2f1fcdd4806dd3c0d510a202e273b), the candidate merged into dev-soft-core 2509db684b58b920e215b0d5d327b4a845bac3f4.

Plain text only; each file is smaller than 200,000 bytes; nothing is compressed.
Original SHA256 values precede path/host normalization. `$SCRATCH` was `round6/scratch` while the receipts were taken and is now `/data-2/milan/tmp/loopbram-a826-r6/scratch`. [manifest-1.jsonl](manifest-1.jsonl) binds every receipt by size and SHA256.

## Key receipts

- [Source binding](source-binding.json.txt)
- [Hosted failure reproduced and its cause isolated](repro--repro.log.txt)
- [Hosted docs-check excerpt](hosted--job-138601303963.excerpt.txt), [hosted elaborate excerpt](hosted--job-138602447405.excerpt.txt)
- [Docs workflow replay results](docswf2--results.json.txt), [firmware gate split attempt](docswf2--030-split.log.txt)
- [rtl ownership and physical selection steps, all 19 shards](rtl-ownership.log.txt)
- [Builder driver, the changed gate](driver-input-loopback.log.txt), [its receipt](driver-input-loopback.json.txt)
- [Planner self-test](lane--planner-selftest.log.txt), [19 shard listings](lane--shard-lists.log.txt), [timeout arms](lane--timeout-arms.log.txt)
- Cold suite runs: [input_loopback](cold-input_loopback.log.txt), [input_loopback_dp](cold-input_loopback_dp.log.txt)

## Docs workflow replay at the final merge

| Row | Job | Step | Exit | Seconds |
|---:|---|---|---:|---:|
| 2 | wire-accountability | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | 1.3 |
| 6 | docs-check-no-git | Strip git metadata, then run the docs gate | 0 | 18.5 |
| 9 | docs-gates-0 | Build the validated HDL reference | 0 | 4.6 |
| 14 | docs-gates-0 | Link health, wording, dead-reference and local-info gate | 0 | 17.1 |
| 15 | docs-gates-0 | Added-line em-dash gate | 0 | 9.4 |
| 16 | docs-gates-0 | Concise audience documentation gate | 0 | 1.6 |
| 17 | docs-gates-0 | Audience diagram no-drift gate | 0 | 3.2 |
| 18 | docs-gates-0 | Product solution source-fact gate | 0 | 9.0 |
| 19 | docs-gates-0 | Verified submodule documentation gate | 0 | 2.8 |
| 20 | docs-gates-0 | HDL timing diagram no-drift gate | 0 | 2.0 |
| 21 | docs-gates-0 | Published diagram PNG gate | 0 | 9.8 |
| 22 | docs-gates-0 | Milan feature-status consistency gate | 0 | 2.6 |
| 23 | docs-gates-0 | Traceability matrix no-drift gate | 0 | 2.7 |
| 25 | docs-gates-0 | Imported gPTP documentation gate | 0 | 2.7 |
| 26 | docs-gates-0 | Code-quality measurement self-tests | 0 | 0.4 |
| 28 | docs-gates-0 | Bare-metal scope gate | 0 | 81.2 |
| 31 | docs-gates-0 | NVM record-space gate | 0 | 149.0 |
| 32 | docs-gates-0 | Capture measurement census and clock gate | 0 | 1.7 |
| 33 | docs-gates-0 | Saved-state writer gate | 0 | 319.9 |
| 34 | docs-gates-0 | SoC source-list gate (Vivado would fail 40 min in without this) | 0 | 7.2 |
| 35 | docs-gates-0 | RTL source-list drift gate | 0 | 10.3 |
| 36 | docs-gates-0 | Boundary-unit naming ratchet | 0 | 2.1 |
| 37 | docs-gates-0 | Port contract gate | 0 | 12.1 |
| 38 | docs-gates-0 | Fail-fast ratchet | 0 | 7.2 |
| 39 | docs-gates-0 | TODO ownership gate | 0 | 9.4 |
| 40 | docs-gates-0 | Test-evidence ratchet | 0 | 34.1 |
| 41 | docs-gates-0 | Mechanical hygiene ratchet | 0 | 1.9 |
| 42 | docs-gates-0 | SystemVerilog idiom gate | 0 | 2.0 |
| 43 | docs-gates-0 | C and C++ idiom gate | 0 | 8.1 |
| 44 | docs-gates-0 | Python idiom gate | 0 | 24.8 |
| 45 | docs-gates-0 | Shell idiom gate | 0 | 1.0 |
| 46 | docs-gates-0 | Doc cited-path gate | 0 | 0.3 |
| 47 | docs-gates-0 | Archive integrity gate | 0 | 1.5 |
| 48 | docs-gates-0 | Per-page contents gate | 0 | 25.4 |
| 49 | docs-gates-0 | Documentation inventory freshness gate | 0 | 7.4 |
| 50 | docs-gates-0 | AEM store generator self-test | 0 | 0.2 |
| 51 | docs-gates-0 | Sweep/build shape gate | 0 | 43.2 |
| 52 | docs-gates-0 | Deploy shape gate | 0 | 1.0 |
| 53 | docs-gates-0 | Entity shape gate | 0 | 150.9 |
| 54 | docs-gates-0 | Register reference freshness gate | 0 | 145.9 |
| 56 | docs-gates-0 | CI scheduling and evidence controls | 0 | 67.9 |
| 79 | docs-gates-2 | CI event and SHA contract gate | 0 | 373.1 |
| 80 | docs-gates-2 | Local act runner contract gate | 0 | 133.6 |

## All receipts

| Receipt | Bytes | Source |
|---|---:|---|
| [source-binding.json.txt](source-binding.json.txt) | 1862 | `source-binding.json` |
| [tools--audit.py.txt](tools--audit.py.txt) | 3164 | `tools/audit.py` |
| [tools--pack.py.txt](tools--pack.py.txt) | 7170 | `tools/pack.py` |
| [tools--repro.sh.txt](tools--repro.sh.txt) | 3227 | `tools/repro.sh` |
| [tools--stepcmd.sh.txt](tools--stepcmd.sh.txt) | 1337 | `tools/stepcmd.sh` |
| [tools--verify.sh.txt](tools--verify.sh.txt) | 1264 | `tools/verify.sh` |
| [tools--wfreplay.py.txt](tools--wfreplay.py.txt) | 4595 | `tools/wfreplay.py` |
| [repro--list-7bfae19-nosub.json.txt](repro--list-7bfae19-nosub.json.txt) | 402 | `repro/list-7bfae19-nosub.json` |
| [repro--list-7bfae19-nosub.stderr.txt](repro--list-7bfae19-nosub.stderr.txt) | 560 | `repro/list-7bfae19-nosub.stderr` |
| [repro--list-7bfae19-sub.json.txt](repro--list-7bfae19-sub.json.txt) | 4500 | `repro/list-7bfae19-sub.json` |
| [repro--list-7bfae19-sub.stderr.txt](repro--list-7bfae19-sub.stderr.txt) | 402 | `repro/list-7bfae19-sub.stderr` |
| [repro--list-final-nosub.json.txt](repro--list-final-nosub.json.txt) | 4500 | `repro/list-final-nosub.json` |
| [repro--list-final-nosub.stderr.txt](repro--list-final-nosub.stderr.txt) | 402 | `repro/list-final-nosub.stderr` |
| [repro--repro.log.txt](repro--repro.log.txt) | 2717 | `repro/repro.log` |
| [repro--union-docs-7bfae19-sub.json.txt](repro--union-docs-7bfae19-sub.json.txt) | 1627 | `repro/union-docs-7bfae19-sub.json` |
| [repro--union-elaborate-7bfae19-sub.json.txt](repro--union-elaborate-7bfae19-sub.json.txt) | 911 | `repro/union-elaborate-7bfae19-sub.json` |
| [hosted--job-138601303963.excerpt.txt](hosted--job-138601303963.excerpt.txt) | 6393 | `hosted/job-138601303963.excerpt` |
| [hosted--job-138602447405.excerpt.txt](hosted--job-138602447405.excerpt.txt) | 6904 | `hosted/job-138602447405.excerpt` |
| [hosted-receipts--run-45434456591--gate-docs-0-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt](hosted-receipts--run-45434456591--gate-docs-0-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt) | 5301 | `hosted-receipts/run-45434456591/gate-docs-0-7bfae19dee8a1eb105e8481691a407e66b92c142/receipt.json` |
| [hosted-receipts--run-45434456591--gate-docs-1-7bfae19dee8a1eb105e8481691a407e66b92c142--builder-leg-0.json.txt](hosted-receipts--run-45434456591--gate-docs-1-7bfae19dee8a1eb105e8481691a407e66b92c142--builder-leg-0.json.txt) | 5355 | `hosted-receipts/run-45434456591/gate-docs-1-7bfae19dee8a1eb105e8481691a407e66b92c142/builder-leg-0.json` |
| [hosted-receipts--run-45434456591--gate-docs-1-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt](hosted-receipts--run-45434456591--gate-docs-1-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt) | 1306 | `hosted-receipts/run-45434456591/gate-docs-1-7bfae19dee8a1eb105e8481691a407e66b92c142/receipt.json` |
| [hosted-receipts--run-45434456591--gate-docs-2-7bfae19dee8a1eb105e8481691a407e66b92c142--builder-leg-1.json.txt](hosted-receipts--run-45434456591--gate-docs-2-7bfae19dee8a1eb105e8481691a407e66b92c142--builder-leg-1.json.txt) | 22514 | `hosted-receipts/run-45434456591/gate-docs-2-7bfae19dee8a1eb105e8481691a407e66b92c142/builder-leg-1.json` |
| [hosted-receipts--run-45434456591--gate-docs-2-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt](hosted-receipts--run-45434456591--gate-docs-2-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt) | 1510 | `hosted-receipts/run-45434456591/gate-docs-2-7bfae19dee8a1eb105e8481691a407e66b92c142/receipt.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-0-7bfae19dee8a1eb105e8481691a407e66b92c142--builder-leg-0.json.txt](hosted-receipts--run-45434456617--gate-elaborate-0-7bfae19dee8a1eb105e8481691a407e66b92c142--builder-leg-0.json.txt) | 5381 | `hosted-receipts/run-45434456617/gate-elaborate-0-7bfae19dee8a1eb105e8481691a407e66b92c142/builder-leg-0.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-0-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt](hosted-receipts--run-45434456617--gate-elaborate-0-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt) | 923 | `hosted-receipts/run-45434456617/gate-elaborate-0-7bfae19dee8a1eb105e8481691a407e66b92c142/receipt.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-1-7bfae19dee8a1eb105e8481691a407e66b92c142--builder-leg-1.json.txt](hosted-receipts--run-45434456617--gate-elaborate-1-7bfae19dee8a1eb105e8481691a407e66b92c142--builder-leg-1.json.txt) | 17415 | `hosted-receipts/run-45434456617/gate-elaborate-1-7bfae19dee8a1eb105e8481691a407e66b92c142/builder-leg-1.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-1-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt](hosted-receipts--run-45434456617--gate-elaborate-1-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt) | 923 | `hosted-receipts/run-45434456617/gate-elaborate-1-7bfae19dee8a1eb105e8481691a407e66b92c142/receipt.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-2-7bfae19dee8a1eb105e8481691a407e66b92c142--litex-leg-0.json.txt](hosted-receipts--run-45434456617--gate-elaborate-2-7bfae19dee8a1eb105e8481691a407e66b92c142--litex-leg-0.json.txt) | 960 | `hosted-receipts/run-45434456617/gate-elaborate-2-7bfae19dee8a1eb105e8481691a407e66b92c142/litex-leg-0.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-2-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt](hosted-receipts--run-45434456617--gate-elaborate-2-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt) | 943 | `hosted-receipts/run-45434456617/gate-elaborate-2-7bfae19dee8a1eb105e8481691a407e66b92c142/receipt.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-3-7bfae19dee8a1eb105e8481691a407e66b92c142--litex-leg-1.json.txt](hosted-receipts--run-45434456617--gate-elaborate-3-7bfae19dee8a1eb105e8481691a407e66b92c142--litex-leg-1.json.txt) | 1339 | `hosted-receipts/run-45434456617/gate-elaborate-3-7bfae19dee8a1eb105e8481691a407e66b92c142/litex-leg-1.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-3-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt](hosted-receipts--run-45434456617--gate-elaborate-3-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt) | 943 | `hosted-receipts/run-45434456617/gate-elaborate-3-7bfae19dee8a1eb105e8481691a407e66b92c142/receipt.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-4-7bfae19dee8a1eb105e8481691a407e66b92c142--litex-leg-2.json.txt](hosted-receipts--run-45434456617--gate-elaborate-4-7bfae19dee8a1eb105e8481691a407e66b92c142--litex-leg-2.json.txt) | 1040 | `hosted-receipts/run-45434456617/gate-elaborate-4-7bfae19dee8a1eb105e8481691a407e66b92c142/litex-leg-2.json` |
| [hosted-receipts--run-45434456617--gate-elaborate-4-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt](hosted-receipts--run-45434456617--gate-elaborate-4-7bfae19dee8a1eb105e8481691a407e66b92c142--receipt.json.txt) | 943 | `hosted-receipts/run-45434456617/gate-elaborate-4-7bfae19dee8a1eb105e8481691a407e66b92c142/receipt.json` |
| [docswf2--results.json.txt](docswf2--results.json.txt) | 11568 | `docswf2/results.json` |
| [docswf2--002-wire-accountability-4.log.txt](docswf2--002-wire-accountability-4.log.txt) | 5657 | `docswf2/002-wire-accountability-4.log` |
| [docswf2--006-docs-check-no-git-3.log.txt](docswf2--006-docs-check-no-git-3.log.txt) | 761 | `docswf2/006-docs-check-no-git-3.log` |
| [docswf2--009-docs-gates-0-3.log.txt](docswf2--009-docs-gates-0-3.log.txt) | 1463 | `docswf2/009-docs-gates-0-3.log` |
| [docswf2--014-docs-gates-0-11.log.txt](docswf2--014-docs-gates-0-11.log.txt) | 667 | `docswf2/014-docs-gates-0-11.log` |
| [docswf2--015-docs-gates-0-12.log.txt](docswf2--015-docs-gates-0-12.log.txt) | 647 | `docswf2/015-docs-gates-0-12.log` |
| [docswf2--016-docs-gates-0-13.log.txt](docswf2--016-docs-gates-0-13.log.txt) | 685 | `docswf2/016-docs-gates-0-13.log` |
| [docswf2--017-docs-gates-0-14.log.txt](docswf2--017-docs-gates-0-14.log.txt) | 756 | `docswf2/017-docs-gates-0-14.log` |
| [docswf2--018-docs-gates-0-15.log.txt](docswf2--018-docs-gates-0-15.log.txt) | 663 | `docswf2/018-docs-gates-0-15.log` |
| [docswf2--019-docs-gates-0-16.log.txt](docswf2--019-docs-gates-0-16.log.txt) | 748 | `docswf2/019-docs-gates-0-16.log` |
| [docswf2--020-docs-gates-0-17.log.txt](docswf2--020-docs-gates-0-17.log.txt) | 757 | `docswf2/020-docs-gates-0-17.log` |
| [docswf2--021-docs-gates-0-18.log.txt](docswf2--021-docs-gates-0-18.log.txt) | 635 | `docswf2/021-docs-gates-0-18.log` |
| [docswf2--022-docs-gates-0-19.log.txt](docswf2--022-docs-gates-0-19.log.txt) | 2089 | `docswf2/022-docs-gates-0-19.log` |
| [docswf2--023-docs-gates-0-20.log.txt](docswf2--023-docs-gates-0-20.log.txt) | 635 | `docswf2/023-docs-gates-0-20.log` |
| [docswf2--025-docs-gates-0-22.log.txt](docswf2--025-docs-gates-0-22.log.txt) | 3125 | `docswf2/025-docs-gates-0-22.log` |
| [docswf2--026-docs-gates-0-23.log.txt](docswf2--026-docs-gates-0-23.log.txt) | 3812 | `docswf2/026-docs-gates-0-23.log` |
| [docswf2--028-docs-gates-0-26.log.txt](docswf2--028-docs-gates-0-26.log.txt) | 620 | `docswf2/028-docs-gates-0-26.log` |
| [docswf2--030-docs-gates-0-29.log.txt](docswf2--030-docs-gates-0-29.log.txt) | 655 | `docswf2/030-docs-gates-0-29.log` |
| [docswf2--030-split.log.txt](docswf2--030-split.log.txt) | 653 | `docswf2/030-split.log` |
| [docswf2--031-docs-gates-0-30.log.txt](docswf2--031-docs-gates-0-30.log.txt) | 20751 | `docswf2/031-docs-gates-0-30.log` |
| [docswf2--032-docs-gates-0-31.log.txt](docswf2--032-docs-gates-0-31.log.txt) | 1717 | `docswf2/032-docs-gates-0-31.log` |
| [docswf2--033-docs-gates-0-32.log.txt](docswf2--033-docs-gates-0-32.log.txt) | 52557 | `docswf2/033-docs-gates-0-32.log` |
| [docswf2--034-docs-gates-0-33.log.txt](docswf2--034-docs-gates-0-33.log.txt) | 5341 | `docswf2/034-docs-gates-0-33.log` |
| [docswf2--035-docs-gates-0-34.log.txt](docswf2--035-docs-gates-0-34.log.txt) | 3963 | `docswf2/035-docs-gates-0-34.log` |
| [docswf2--036-docs-gates-0-35.log.txt](docswf2--036-docs-gates-0-35.log.txt) | 41111 | `docswf2/036-docs-gates-0-35.log` |
| [docswf2--037-docs-gates-0-36.log.txt](docswf2--037-docs-gates-0-36.log.txt) | 5542 | `docswf2/037-docs-gates-0-36.log` |
| [docswf2--038-docs-gates-0-37.log.txt](docswf2--038-docs-gates-0-37.log.txt) | 13033 | `docswf2/038-docs-gates-0-37.log` |
| [docswf2--039-docs-gates-0-38.log.txt](docswf2--039-docs-gates-0-38.log.txt) | 3248 | `docswf2/039-docs-gates-0-38.log` |
| [docswf2--040-docs-gates-0-39.log.txt](docswf2--040-docs-gates-0-39.log.txt) | 33690 | `docswf2/040-docs-gates-0-39.log` |
| [docswf2--041-docs-gates-0-40.log.txt](docswf2--041-docs-gates-0-40.log.txt) | 4482 | `docswf2/041-docs-gates-0-40.log` |
| [docswf2--042-docs-gates-0-41.log.txt](docswf2--042-docs-gates-0-41.log.txt) | 3681 | `docswf2/042-docs-gates-0-41.log` |
| [docswf2--043-docs-gates-0-42.log.txt](docswf2--043-docs-gates-0-42.log.txt) | 5239 | `docswf2/043-docs-gates-0-42.log` |
| [docswf2--044-docs-gates-0-43.log.txt](docswf2--044-docs-gates-0-43.log.txt) | 3493 | `docswf2/044-docs-gates-0-43.log` |
| [docswf2--045-docs-gates-0-44.log.txt](docswf2--045-docs-gates-0-44.log.txt) | 3196 | `docswf2/045-docs-gates-0-44.log` |
| [docswf2--046-docs-gates-0-45.log.txt](docswf2--046-docs-gates-0-45.log.txt) | 604 | `docswf2/046-docs-gates-0-45.log` |
| [docswf2--047-docs-gates-0-46.log.txt](docswf2--047-docs-gates-0-46.log.txt) | 634 | `docswf2/047-docs-gates-0-46.log` |
| [docswf2--048-docs-gates-0-47.log.txt](docswf2--048-docs-gates-0-47.log.txt) | 702 | `docswf2/048-docs-gates-0-47.log` |
| [docswf2--049-docs-gates-0-48.log.txt](docswf2--049-docs-gates-0-48.log.txt) | 651 | `docswf2/049-docs-gates-0-48.log` |
| [docswf2--050-docs-gates-0-49.log.txt](docswf2--050-docs-gates-0-49.log.txt) | 4109 | `docswf2/050-docs-gates-0-49.log` |
| [docswf2--051-docs-gates-0-50.log.txt](docswf2--051-docs-gates-0-50.log.txt) | 27312 | `docswf2/051-docs-gates-0-50.log` |
| [docswf2--052-docs-gates-0-51.log.txt](docswf2--052-docs-gates-0-51.log.txt) | 10815 | `docswf2/052-docs-gates-0-51.log` |
| [docswf2--053-docs-gates-0-52.log.txt](docswf2--053-docs-gates-0-52.log.txt) | 29532 | `docswf2/053-docs-gates-0-52.log` |
| [docswf2--054-docs-gates-0-53.log.txt](docswf2--054-docs-gates-0-53.log.txt) | 4266 | `docswf2/054-docs-gates-0-53.log` |
| [docswf2--056-docs-gates-0-55.log.txt](docswf2--056-docs-gates-0-55.log.txt) | 140076 | `docswf2/056-docs-gates-0-55.log` |
| [docswf2--079-docs-gates-2-15.log.part001.txt](docswf2--079-docs-gates-2-15.log.part001.txt) | 190404 | `docswf2/079-docs-gates-2-15.log` |
| [docswf2--079-docs-gates-2-15.log.part002.txt](docswf2--079-docs-gates-2-15.log.part002.txt) | 177881 | `docswf2/079-docs-gates-2-15.log` |
| [docswf2--080-docs-gates-2-16.log.txt](docswf2--080-docs-gates-2-16.log.txt) | 131795 | `docswf2/080-docs-gates-2-16.log` |
| [rtl-ownership.log.txt](rtl-ownership.log.txt) | 89542 | `rtl-ownership.log` |
| [driver-input-loopback.log.txt](driver-input-loopback.log.txt) | 696 | `driver-input-loopback.log` |
| [driver-input-loopback.json.txt](driver-input-loopback.json.txt) | 4712 | `driver-input-loopback.json` |
| [cold-input_loopback.log.txt](cold-input_loopback.log.txt) | 62305 | `cold-input_loopback.log` |
| [cold-input_loopback_dp.log.txt](cold-input_loopback_dp.log.txt) | 156221 | `cold-input_loopback_dp.log` |
| [lane--cancellation.log.txt](lane--cancellation.log.txt) | 7653 | `lane/cancellation.log` |
| [lane--evidence-check.log.txt](lane--evidence-check.log.txt) | 25932 | `lane/evidence-check.log` |
| [lane--evidence-selftest.log.txt](lane--evidence-selftest.log.txt) | 6401 | `lane/evidence-selftest.log` |
| [lane--gate-workflows-check.log.txt](lane--gate-workflows-check.log.txt) | 502 | `lane/gate-workflows-check.log` |
| [lane--loopback-standalone.log.txt](lane--loopback-standalone.log.txt) | 610 | `lane/loopback-standalone.log` |
| [lane--planner-selftest.log.txt](lane--planner-selftest.log.txt) | 4859 | `lane/planner-selftest.log` |
| [lane--shard-lists.log.txt](lane--shard-lists.log.txt) | 1857 | `lane/shard-lists.log` |
| [lane--suite-workflows-check.log.txt](lane--suite-workflows-check.log.txt) | 504 | `lane/suite-workflows-check.log` |
| [lane--tally-selftest.log.txt](lane--tally-selftest.log.txt) | 491 | `lane/tally-selftest.log` |
| [lane--timeout-arms.log.txt](lane--timeout-arms.log.txt) | 698 | `lane/timeout-arms.log` |
