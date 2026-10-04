| control | declared | suite | rc | failing | named failing checks (shapes) | verdict |
|---|---|---|---:|---:|---|---|
| `tf-ls-head-reads-tk-ram` | catch | srp_top | 2 | 24 | F2 (suite, no shape tag); F4 (suite, no shape tag); F5a (suite, no shape tag); K8 (suite, no shape tag); TF1 (1/1, 2/2, 3/5, 9/9); TF2 (1/1, 2/2, 3/5, 9/9); TF3 (9/9); TF4 (1/1, 2/2, 3/5, 9/9); +1 more | |
| `tf-ls-head-reads-tk-ram` | catch | **all** | | | | killed by a named committed check |
| `tf-tk-head-reads-next` | catch | srp_top | 2 | 14 | F5c (suite, no shape tag); TF1 (1/1, 2/2, 3/5, 9/9); TF4 (1/1, 2/2, 3/5, 9/9) | |
| `tf-tk-head-reads-next` | catch | **all** | | | | killed by a named committed check |
| `tf-ls-write-ignores-full` | catch-at-full | srp_top | 2 | 4 | TF5 (1/1, 2/2, 3/5, 9/9) | |
| `tf-ls-write-ignores-full` | catch-at-full | **all** | | | | killed by a named committed check |
| `tf-tk-write-at-rptr` | catch | srp_top | 2 | 9 | K8 (suite, no shape tag); TF1 (1/1, 2/2, 3/5, 9/9); TF4 (1/1, 2/2, 3/5, 9/9) | |
| `tf-tk-write-at-rptr` | catch | **all** | | | | killed by a named committed check |
| `tf-tk-same-entry-bypass` | equiv | pp_top | 0 | 0 |  | |
| `tf-tk-same-entry-bypass` | equiv | srp_top | 0 | 0 |  | |
| `tf-tk-same-entry-bypass` | equiv | **all** | | | | silent in every suite, as declared |
| `wtsp-written-on-close` | catch | srp_stream_fsms | 2 | 4 | WK3 (1/1, 2/2, 3/5, 9/9) | |
| `wtsp-written-on-close` | catch | srp_top | 2 | 2 | C2 (suite, no shape tag) | |
| `wtsp-written-on-close` | catch | **all** | | | | killed by a named committed check |
| `wtsp-prio-rank-swapped` | catch | srp_stream_fsms | 2 | 82 | T AA prio/rank byte (suite, no shape tag); T AN prio/rank byte (suite, no shape tag); T AP prio/rank byte (suite, no shape tag); T LA prio/rank byte (suite, no shape tag); T LO prio/rank byte (suite, no shape tag); T QA prio/rank byte (suite, no shape tag); T QP prio/rank byte (suite, no shape tag); T VN prio/rank byte (suite, no shape tag); +6 more | |
| `wtsp-prio-rank-swapped` | catch | srp_top | 2 | 2 | B: Talker Advertise New byte-exact (suite, no shape tag); C: Talker Failed code 1 byte-exact (suite, no shape tag) | |
| `wtsp-prio-rank-swapped` | catch | **all** | | | | killed by a named committed check |
| `wtsp-read-at-source-0` | catch | srp_stream_fsms | 2 | 50 | WK1 (2/2, 3/5, 9/9); WK2 (2/2, 3/5, 9/9); WK3 (2/2, 3/5, 9/9); WK4 (2/2, 3/5, 9/9); WK5 (2/2, 3/5, 9/9) | |
| `wtsp-read-at-source-0` | catch | srp_top | 2 | 1 | C: Talker Failed code 1 byte-exact (suite, no shape tag) | |
| `wtsp-read-at-source-0` | catch | **all** | | | | killed by a named committed check |
| `wid-ram-read-neighbour` | catch | srp_stream_fsms | 2 | 94 | T AA FirstValue VLAN (suite, no shape tag); T AA FirstValue stream_id/DA (suite, no shape tag); T AN FirstValue VLAN (suite, no shape tag); T AN FirstValue stream_id/DA (suite, no shape tag); T AP FirstValue VLAN (suite, no shape tag); T AP FirstValue stream_id/DA (suite, no shape tag); T LA FirstValue VLAN (suite, no shape tag); T LA FirstValue stream_id/DA (suite, no shape tag); +15 more | |
| `wid-ram-read-neighbour` | catch | srp_top | 2 | 26 | B: Talker Advertise New byte-exact (suite, no shape tag); B: second tick repeats New (AN row (suite, no shape tag); B: third tick JoinMt (AA row) (suite, no shape tag); C2 (suite, no shape tag); C: Talker Failed code 1 byte-exact (suite, no shape tag); I: wire Talker Advertise for sourc (suite, no shape tag); N6 (suite, no shape tag); Q1 (suite, no shape tag); +2 more | |
| `wid-ram-read-neighbour` | catch | **all** | | | | killed by a named committed check |
| `wid-flops-vid-of-source-0` | catch | srp_stream_fsms | 2 | 6 | WK1 (2/2); WK2 (2/2); WK3 (2/2); WK4 (2/2); WK5 (2/2) | |
| `wid-flops-vid-of-source-0` | catch | srp_top | 0 | 0 |  | |
| `wid-flops-vid-of-source-0` | catch | **all** | | | | killed by a named committed check |
| `wid-threshold-ram-from-1` | equiv | pp_top | 0 | 0 |  | |
| `wid-threshold-ram-from-1` | equiv | srp_stream_fsms | 0 | 0 |  | |
| `wid-threshold-ram-from-1` | equiv | srp_top | 0 | 0 |  | |
| `wid-threshold-ram-from-1` | equiv | **all** | | | | silent in every suite, as declared |
| `wid-threshold-flops-always` | equiv | pp_top | 0 | 0 |  | |
| `wid-threshold-flops-always` | equiv | srp_stream_fsms | 0 | 0 |  | |
| `wid-threshold-flops-always` | equiv | srp_top | 0 | 0 |  | |
| `wid-threshold-flops-always` | equiv | **all** | | | | silent in every suite, as declared |
| `wsid-ram-written-on-teardown` | catch | srp_stream_fsms | 2 | 2 | WK7 (3/5, 9/9) | |
| `wsid-ram-written-on-teardown` | catch | srp_top | 0 | 0 |  | |
| `wsid-ram-written-on-teardown` | catch | **all** | | | | killed by a named committed check |
| `wsid-flops-read-sink-0` | catch | srp_stream_fsms | 2 | 4 | WK6 (2/2); WK7 (2/2); WK8 (2/2) | |
| `wsid-flops-read-sink-0` | catch | srp_top | 0 | 0 |  | |
| `wsid-flops-read-sink-0` | catch | **all** | | | | killed by a named committed check |
| `slope-store-at-stage-1-index` | catch | srp_admission | 2 | 1333 | grant belongs to the current decla (suite, no shape tag); refused current TSpec never pulses (suite, no shape tag); round publishes the greedy walk ov (suite, no shape tag); settled ceiling refusal N=2 (suite, no shape tag); settled greedy grants N=2 (suite, no shape tag); settled sum of grants N=2 (suite, no shape tag) | |
| `slope-store-at-stage-1-index` | catch | srp_top | 2 | 673 | B: granted slope 0 vs model 682240 (suite, no shape tag); B: sum slope vs model (suite, no shape tag); C2 (suite, no shape tag); C: Talker Failed code 1 byte-exact (suite, no shape tag); C: granted slope 0 while refused (suite, no shape tag); C: msrp_fail_code 1 (suite, no shape tag); C: over_limit view (suite, no shape tag); C: src 1 refused (suite, no shape tag); +44 more | |
| `slope-store-at-stage-1-index` | catch | **all** | | | | killed by a named committed check |
| `slope-read-source-0` | catch | srp_admission | 2 | 578 | grant belongs to the current decla (suite, no shape tag); live granted sum stays within the (suite, no shape tag); refused current TSpec never pulses (suite, no shape tag); round publishes coherent bounded s (suite, no shape tag); round publishes the greedy walk ov (suite, no shape tag); settled ceiling refusal N=2 (suite, no shape tag); settled greedy grants N=2 (suite, no shape tag); settled sum of grants N=2 (suite, no shape tag) | |
| `slope-read-source-0` | catch | srp_top | 2 | 217 | G0 (suite, no shape tag); G1 (suite, no shape tag); G10 (suite, no shape tag); G11 (suite, no shape tag); G12 (suite, no shape tag); G13 (suite, no shape tag); G14 (suite, no shape tag); G15 (suite, no shape tag); +28 more | |
| `slope-read-source-0` | catch | **all** | | | | killed by a named committed check |
| `tf-tk-write-ignores-full` | catch | srp_top | 2 | 4 | TF4 (1/1, 2/2, 3/5, 9/9) | |
| `tf-tk-write-ignores-full` | catch | **all** | | | | killed by a named committed check |

0 controls not as declared
