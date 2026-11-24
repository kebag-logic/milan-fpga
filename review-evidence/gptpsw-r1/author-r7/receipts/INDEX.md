# Receipts index: PR #966 round 2, head 0acf24d9b5060a263f725c02026446dde64c2574

Plain text, bounded. Full shard logs stay in /data-2/milan/tmp/opt-a837-r2/logs (sha256 in each summary). Filtered copies drop only `wrote <contract file>` and the builder's locally-administered-MAC warning lines.

| File | Bytes | sha256 | What |
|---|---:|---|---|
| `delta.diff` | 5382 | `86b82d92e709aa51` | the whole delta 44c56639..0acf24d9 |
| `product-scope.txt` | 54 | `697678ba94aa3ccd` | count of changed paths outside sw/firmware/ctrl/test (0) |
| `plant-old.log` | 244 | `6a341986bdac34a6` | leak planted at 44c56639's tests: ESCAPED, old-rc=0 |
| `plant-old-leak.excerpt.log` | 179 | `48783b4ba7591da0` | the AVB test passing with the leak at 44c56639 |
| `plant-new.log` | 730 | `b7326414debc365b` | three face rows caught on their words; unplanted baseline at 1 and 2 interfaces |
| `plant-new-face-software-gptp-keeps-datapath-capable.excerpt.log` | 887 | `dc3b702b3488086f` | the leak failing the new check only |
| `plant-new-face-software-gptp-clears-link-flags.excerpt.log` | 1725 | `542b7dcfaa91fd11` | the link-flags plant failing its own check only |
| `plant-results.json` | 1453 | `b02a29e9813dca93` | campaign result rows (new, then old) |
| `coverage-check.log` | 4926 | `83c329a71a1c376f` | fw_coverage --check at 0acf24d9: PASS (42 files) |
| `coverage-check.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `fw-shard-0.summary.log` | 314 | `62adefa130b89d4b` | shard 0/4 rc, counts, full-log sha256, clone head |
| `fw-shard-1.summary.log` | 248 | `27c5ee022d4dac5e` | shard 1/4 rc, counts, full-log sha256, clone head |
| `fw-shard-2.summary.log` | 551 | `2a7ba7dff30cd674` | shard 2/4 rc, counts, full-log sha256, clone head |
| `fw-shard-3.summary.log` | 248 | `eca10070b1de9df7` | shard 3/4 rc, counts, full-log sha256, clone head |
| `py-idiom.log` | 466 | `29d88a68a6812dea` | check_py_idiom.py rc 0 |
| `diff-check.log` | 202 | `50eaf304712386d2` | git diff --check rc 0 and diffstat |
| `plant_proof.py` | 2745 | `aaec67232b7b96f4` | reproduction script |
| `launch.sh` | 1098 | `8b207619fb8339c6` | reproduction script |
| `feed.sh` | 556 | `04a6f689ec5d996a` | reproduction script |
| `unit.sh` | 1003 | `e69f6e532f113b1c` | reproduction script |
| `clone.sh` | 1044 | `4fd36598172fe330` | reproduction script |
| `env.sh` | 786 | `e7b44acf8735bf20` | reproduction script |

Total: 24843 bytes.
