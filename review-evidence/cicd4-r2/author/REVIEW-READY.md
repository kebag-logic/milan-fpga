# Review ready, delta: PR #1019 round 2, `5b5b0765..6841c5e3be` (not pushed)

Six commits on the reviewed head. One of them is a merge commit, of dev-soft-core `4df125b8`.

| Finding | Where | Evidence |
|---|---|---|
| R947-1 F1: the command's COUNT is not held to the matrix | `scripts/ci_events.py` (`FAST_LEG_CAMPAIGNS`, `CAMPAIGN_SHARD_RE`, `check_fast_legs`, `_m_campaign_command`, 13 new arms); `scripts/ci_fast_legs_selftest.py` | `receipts/probes/P1.txt`: probe P1 refused by the contract for all 3 campaign jobs and by the self-test; the unplanted head passes |
| R947-1 F2 / R948-1 D1: the policy's docs total | `docs/testing/CI_WORKFLOWS.md`, the docs-workflow paragraph | `docs-gates-1` 1302 s, workflow 1572 s, 26.2 min, 228 s margin; 1302 s stated over the budget |
| R947-1 F3: the generator comment | `scripts/ci_gate_workflows.py`, the `DOCS_WORKERS` comment | cites the table: worker 3 at 1237 s, `docs-gates-1` at 1302 s |
| R947-1 F4 (suggestion): the proof bypasses `main()`'s mapping | `test_ctrl_firmware.py` `campaign_leg`, used by `main()` and by `test_ctrl_firmware_shards.inventory` | P6 (the mapping removed) is now refused |
| R948-1 T1: the census receipts | `receipts/census-receipts/` (5 JSON files, `SHA256SUMS`, `replay.sh`, `plant_census.py`) | `replay.txt`: union rc 0, its output identical to the original; 7 of 7 plants refused at `530149b5` |
| Hosted failure of the PR's own run | `sw/firmware/ctrl/test/ctrl_configs.py` (`OUTSIDE`) | `receipts/hosted/firmware-boundary-*.log:529`; `receipts/probes/boundary-scan.txt` (refused at `5b5b0765`, clean at the head) |
| Base moved | merge of `4df125b8`; `gptp_shadow` set to 679 | the 27-worker deal at most 1275 s; `receipts/hosted/gptp/45755846909-22of27.log` |

Measured leg windows from the PR's own run: `receipts/hosted/windows.tsv`. Gates: `receipts/gates/summary`.
