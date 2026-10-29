# The harness's controls at head 01879189 (harness code as the final head's)

Commands: `run.py --point 1x1 --build-dir <scratch>/builds/CTL-<name> <args>` from a clean clone, product clocks (CPU 50 MHz, bus 100 MHz), no variant.

| Name | Arguments | Result |
|---|---|---|
| rx-none | `--fetch-l1 none --mutation slow-adp-rx` | rc 0, `CONTROL slow-adp-rx caught`: RCV_ADP_DISCOVER 48.697 ms over its 20 ms budget |
| sd-none | `--fetch-l1 none --variant shutdown-entry --mutation slow-adp-shutdown` | rc 0, `CONTROL slow-adp-shutdown caught`: SHUTDOWN 48.932 ms |
| ab-none | `--fetch-l1 none --cpu-regions as-built` | rc 0, `CONTROL as-built caught: an instruction access fault (cause 1)` |
| un-none | `--fetch-l1 none --groups control` | rc 0, the unplanted RCV_ADP_DISCOVER 0.057 ms, fits |
| unsd-none | `--fetch-l1 none --variant shutdown-entry --groups control-shutdown` | rc 0, the unplanted SHUTDOWN 0.291 ms, fits |
| rx-split | `--mutation slow-adp-rx` (the split's own fetch L1 and data cache) | rc 1, `CONTROL slow-adp-rx ESCAPED`: 17.324 ms fits the 20 ms budget |
| sd-split | `--variant shutdown-entry --mutation slow-adp-shutdown` (the split's caches) | rc 1, `CONTROL slow-adp-shutdown ESCAPED`: 17.406 ms fits |

The controls are the cacheless core's (README, Controls and self-test); the two split-cache runs are the evidence for that statement, not gates.
