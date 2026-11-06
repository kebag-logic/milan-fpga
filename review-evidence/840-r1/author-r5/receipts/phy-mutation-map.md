# Round 5 PHY mutants

Head `27df6e08cf157b9c5e4b0fdb7da2fa28d8ab83fa`. Each row fails on the named words in [phy_firmware.log](gates/phy_firmware.log).

| New check | Planted mutant | Failing words |
|---|---|---|
| `power_down_kept` | `force-bit-0.11` | `Assertion `power_down_kept' failed` |
| `power_down_kept` | `drop-bit-0.11` | `Assertion `power_down_kept' failed` |
| `loopback_kept` | `force-bit-0.14` | `Assertion `loopback_kept' failed` |
| `loopback_kept` | `drop-bit-0.14` | `Assertion `loopback_kept' failed` |

What each part of the driver buys, from [arm_probe.log](gates/arm_probe.log). The committed firmware passes every variant.

| Temporary change to `phy_host.c` | Mutants of the four that then escape |
|---|---|
| None | None |
| First arm back at `0x9400` | `drop-bit-0.11` |
| Second arm back at `0x2100` | `drop-bit-0.14` |
| Both arms back | `drop-bit-0.11`, `drop-bit-0.14` |
| Second arm with power-down also set, `0x6900` | `force-bit-0.11` |
| First arm with loopback also set, `0xdc00` | `force-bit-0.14` |
| `power_down_kept` not asserted | `force-bit-0.11`, `drop-bit-0.11` |
| `loopback_kept` not asserted | `force-bit-0.14`, `drop-bit-0.14` |
