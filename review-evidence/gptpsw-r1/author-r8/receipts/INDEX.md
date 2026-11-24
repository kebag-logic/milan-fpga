# Receipts index: PR #966 round 3b, head e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d

Plain text, bounded. Full logs stay in /data-2/milan/tmp/opt-a837-r3b/logs (each summary records the full log's sha256). Filtered copies drop only the builder's `wrote <contract file>` lines and its locally-administered-MAC warning.

| File | Bytes | sha256 (16) | What |
|---|---:|---|---|
| `commit.txt` | 158 | `2780f5dca2ba58c0` | the commit: full SHA, parent 0acf24d9, one-line subject, empty body |
| `branch-state.txt` | 181 | `e0c7495dbadf58e7` | local head, remote branch tip (still 0acf24d9: not pushed), ahead 1 |
| `delta.diff` | 1767 | `e4bc74b03bee4790` | the whole delta 0acf24d9..e05f800a (2 lines in 2 test files) |
| `diff-check.txt` | 291 | `c955ccdd89da8f9d` | git diff --check rc 0; diffstat; 0 paths outside sw/firmware/ctrl/test; 0 firmware product inputs |
| `wording-grep.txt` | 551 | `3df2652b84e1a605` | no 'software gPTP owner' left under sw/; the tree's existing 'firmware gPTP owner' wording |
| `baremetal-check-lane.log` | 120 | `c89e64f6bccf80ab` | check_baremetal_only.py --check in the lane checkout at the head: OK, 0 findings / 1936 files, rc 0 |
| `docs-gates-0.summary.txt` | 4008 | `69866ae3e2b167c4` | all 42 run-steps of docs.yml docs-gates-0, each STEP rc 0, ALL-STEPS rc=0, clone clean after |
| `docs-gates-0.coverage.txt` | 4287 | `63339193fa03e74d` | every docs-gates-0 workflow step mapped to the local run: all 40 gate_* run-steps ran |
| `docs-gates-0.discarded-attempt.txt` | 1503 | `3950b426f3cde3f7` | the first docs attempt, stopped for a runner setup error, and why it is not counted |
| `aecp-campaign.summary.txt` | 1014 | `7d759c67ac5f2411` | full AECP campaign (aecp_mutants.py, 2 shards): 388/388 caught, 0 escaped, rc 0 + rc 0 |
| `campaign-leak-row.excerpt.log` | 769 | `66142ceb039a48c6` | face-software-gptp-keeps-datapath-capable in the campaign: failed on the new words only |
| `plant-probe.filtered.log` | 728 | `86986cf52b8c06a5` | the three software-gPTP face rows caught on their words; unplanted AVB test green at 1 and 2 interfaces; rc 0 |
| `leak-row.excerpt.log` | 1642 | `ed59dd8ee2d361a1` | the AS_CAPABLE leak's test output in the probe: new words, both interfaces, no link-flag failure |
| `needle-tie.txt` | 421 | `e27d8178d127ac03` | needle is a substring of the assertion; the leak log grades caught on the new words, not on the old or link-flag words |
| `pins.txt` | 772 | `66761c109460a630` | unit start times and CPU ranges |
| `docs_gates0.sh` | 6940 | `ad7b6cfde16b06cb` | reproduction script (docs-gates-0 steps) |
| `plant_proof.py` | 2747 | `38ff504733da5995` | reproduction script (three-row probe + baseline) |
| `unit.sh` | 1008 | `7908a2f7479c892d` | reproduction script (pinned transient unit) |
| `clone.sh` | 1044 | `4fd36598172fe330` | reproduction script (clean shared clone) |
| `env.sh` | 787 | `ffda232d717a45b7` | reproduction script (campaign environment) |

Total: 33685 bytes before this index.
