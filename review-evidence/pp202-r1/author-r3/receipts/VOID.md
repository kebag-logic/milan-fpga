# Runs not credited as passing acceptance gates

| Record | Why excluded / replacement |
|---|---|
| `consumer/capture_coherence.excerpt.txt`, rc 2 | Two stale AAF delay mutation anchors planted nothing after the new parameter was added. Anchors repaired in parent cb22699767; replaced by the complete four-shard capture run. |
| `consumer/milan_dp.log` or its bounded excerpt, rc 2 | Dependency proof refused the resume-added push-URL configuration before the ordinary legs ran. Configuration corrected; replaced by the complete datapath rerun. |
| `consumer/399_verdict.*`, `1144_verdict.*`, `2108_verdict.*` | Receipt script supplied numeric log names. Replaced by correctly named verdict invocations over the actual suite logs. |
| `consumer-capture/shard0.*`, rc 143 | Cancelled because the main parent generated ROM-ledger rows during the run; replaced by shard0-isolated in the immutable capture clone. |

Expected failing planted controls in `parent/` and mutation logs are positive detection evidence, not passing golden runs. Only completed replacement runs with rc 0 and the verified full case union are accepted.

- `consumer-rerun/milan_dp`: rc 2, four silence-fill checks failed because the legacy classifier expected TCTX UID 5. Parent commit dcd3273d09 expects the published UID 1; the complete replacement run is `milan_dp-final`. The failed run is excluded from passing totals.
