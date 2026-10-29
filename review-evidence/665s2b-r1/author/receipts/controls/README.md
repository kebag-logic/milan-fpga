# The harness's controls at head 51fa5f18 (the merge c5676878 and its three fixes)

Commands: `run.py --point 1x1 --build-dir <scratch>/builds/CTL-<name> --record-budget-findings <args>` from a clean clone at `51fa5f18`, product clocks (CPU 50 MHz, bus 100 MHz), no variant.

| Name | Arguments | Result |
|---|---|---|
| rx-none | `--fetch-l1 none --mutation slow-adp-rx` | rc 0, `CONTROL slow-adp-rx caught`: RCV_ADP_DISCOVER 48.697 ms over its 20 ms budget |
| sd-none | `--fetch-l1 none --variant shutdown-entry --mutation slow-adp-shutdown` | rc 0, `CONTROL slow-adp-shutdown caught`: SHUTDOWN 48.933 ms |
| ab-none | `--fetch-l1 none --cpu-regions as-built` | rc 0, `CONTROL as-built caught: an instruction or load access fault (cause 1 or 5)`; `TRAP 166 0 5 00000020` |
| un-none | `--fetch-l1 none --groups control` | rc 0, the unplanted RCV_ADP_DISCOVER 0.056 ms, fits |
| unsd-none | `--fetch-l1 none --variant shutdown-entry --groups control-shutdown` | rc 0, the unplanted SHUTDOWN 0.292 ms, fits |
| ab-split | `--cpu-regions as-built` (the split's own fetch L1 and data cache) | rc 0, `CONTROL as-built caught`; `TRAP 390 0 5 00000020` |
| rx-split | `--mutation slow-adp-rx` (the split's caches) | rc 1, `CONTROL slow-adp-rx ESCAPED`: 17.322 ms fits the 20 ms budget |
| sd-split | `--variant shutdown-entry --mutation slow-adp-shutdown` (the split's caches) | rc 1, `CONTROL slow-adp-shutdown ESCAPED`: 17.411 ms fits |

The spin controls are the cacheless core's (README, Controls and self-test); the two split-cache spin runs are the evidence for that statement, not gates. The merged 1x1 image's `.data` load image is at 0x19428 (bit 15 set), so the start code's first copy load meets #791's decode first, cause 5, on either core.
