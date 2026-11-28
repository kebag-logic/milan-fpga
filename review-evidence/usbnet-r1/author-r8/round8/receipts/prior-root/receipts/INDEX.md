# Receipts, usbnet A855 (#1011, #1018)

Branch head `cc49123d2db1e01e80859efa10f8da43a01344ef` (dev-soft-core c34e7d8b06 + 8 commits).
Arty integration head `660ed296780e3ff1e5cdc88b9b1ce32d08e94b49` (this branch merged onto the Arty split merge
49b534fc9). The bench, defect, gate and identity receipts are at the branch head. The firmware receipts are at
7e4cdddc76; the last commit changes no firmware file. The full outputs remain in $VALIDATION_STORAGE/usbnet-a855 (route/, ident/, fw-*/, mut/).

| Receipt | What it shows |
|---|---|
| `bench-tap-leds.txt` | the tap bench, 9 cases, and the LED bench, at the head |
| `rtl-planted-defects.txt` | 43 of 43 RTL planted defects caught, each by its named check (`mutants.py`) |
| `shaper-suites.txt` | the stand-alone CBS, shaping-core and queue suites pass, unchanged |
| `firmware-leds-tests.txt` | `Leds.*` on the shipping, dev-soft-core Arty and Arty split models; the full application arm (186 tests) |
| `firmware-led-defects.txt` | 8 of 8 firmware LED defect rows caught; the plant table claims every test |
| `firmware-aecp-arms.txt` | every AECP arm, 26 of 26, the new Arty LED arms among them |
| `gates.txt` | 17 repository gates at the head, all rc 0 |
| `alinx-identity.txt`, `alinx-identity.json` | ax7101, ax8x8, ax7a200t SoC exports at c34e7d8b06 and at the head: no differing file, no differing RTL source, same launch line; same-tree control clean |
| `alinx-firmware-identity.txt` | the 1x1 and 8x8 product firmware and map headers byte-identical at base and head |
| `arty-routes.json` | the four Arty routes: per-corner WNS/TNS/WHS/THS and failing endpoints, routing errors, utilisation, per-instance cost, bitstream and manifest |
| `arty-route-*-{Slow_0C,Fast_0C}-summary.txt`, `*-route_status.rpt`, `*-utilization_place.rpt`, `*-hierarchy-extract.txt`, `*.command.json` | the reports behind arty-routes.json, per route |
| `arty-route-baseline.json`, `arty-cost-delta.txt` | the pristine Arty split route (the same recipe argv, the base firmware, ExtraTimingOpt), and the cost delta to the selected image |
| `arty-csr-map-added-rows.diff` | the Arty CSR map against the base product's: rows added only, none moved |
| `arty-firmware-plan.txt` | the Arty firmware with the LEDs: same flash map, same block-RAM banks (44.5 of 56 tiles); the image identity gate on the final image |

Routes, all with `--usb-net` and the Arty split recipe's argv, through the Vivado slot wrapper at nice 19 with 4
threads:

| Route | Integration | Firmware | Directive | Worst WNS / WHS |
|---|---|---|---|---|
| `ExtraTimingOpt` | 38ec75b7d8 | b9935f68 (base) | ExtraTimingOpt | 0.417 / 0.013 ns |
| `ExtraTimingOpt-final` | b1a1b4cb58 | 18c9b404 (with the LEDs) | ExtraTimingOpt | 0.212 / 0.050 ns; the receive copy's descriptor write was the setup-critical path |
| `ExtraTimingOpt-final2` | 660ed29678 | 18c9b404 | ExtraTimingOpt | 0.072 / 0.050 ns; mailbox DMA reset paths, none of this change |
| **`AltSpreadLogic_high-final2`, selected** | 660ed29678 | 18c9b404 | AltSpreadLogic_high | **0.601 / 0.050 ns** |
| `arty-route-baseline*` | 49b534fc9 (pristine) | b9935f68 | ExtraTimingOpt, without `--usb-net` | 0.433 / 0.050 ns |

`cc49123d2d` registers the receive copy's input beat. It was made after `ExtraTimingOpt-final` showed that path
setting the image's setup slack.
