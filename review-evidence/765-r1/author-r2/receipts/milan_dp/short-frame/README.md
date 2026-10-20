# Short-frame drop on the pruned 1x1 leg (outside #765)

`tb/verilator/milan_dp/sim_prune.cpp`, built by the suite's `build-prune`
recipe in a scratch copy of the harness directory, with one debug `printf`
before the check "listener 0 accepted the fed AAF PDUs". Each `.patch` is the
harness change for that run.

| Run | RTL | Frame octets | FRAMES_RX | PCMRX_CNT pdus | Format errors |
|---|---|---:|---:|---:|---:|
| `short-frame-base-86` | base `4191b098` | 86 (bare 2-channel PDU) | 16 | 0 | 0 |
| `short-frame-cand-86` | this lane (RTL of `31903ec1`) | 86 | 16 | 0 | 0 |
| `short-frame-cand-120` | this lane | 120 | 16 | 15 | 0 |
| `short-frame-cand-230` | this lane | 230 (the leg's former length) | 16 | 16 | 0 |

The monitor accepts all 16 PDUs in every run; the depacketizer emits fewer
when the frame is short. The base run shows the same with the old family
compare, so the drop is not caused by #765.
