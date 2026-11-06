OPEN
## Scope

Move the `gptp-processor` gitlink from `135afd04` to FPGA-gPTP main `1616fc8f`. That carries:

- **FPGA-gPTP #98 / PR #99:** a Follow_Up whose first TLV is unknown is accepted when the information TLV follows (IEEE 802.1AS-2011 11.4.1).
- **FPGA-gPTP #100 / PR #101:**
  - The Follow_Up information TLV values after becoming grandmaster (10.2.8.2.1 i)-l), 10.2.9, 11.4.4.3).
  - The announce receipt timeout from the received interval (10.3.9.1).
  - The maintainer's stricter readings: an Announce at the timeout instant ages the port; a Pdelay response later than the Milan v1.2 4.2.6.2.6 bound counts as lost; clockAccuracy is a build parameter.

## Required in the parent

1. **clockAccuracy per board (maintainer ruling 2026-11-05).** The builder passes each config's `gptp.clock_accuracy` to the generator's `--clock-accuracy` and relaxes its pin for that field.
   - The AX7101 shipping config is `0x22`, the maintainer's decision.
   - The Arty configs are `0xFE`, since their oscillators are not characterised (802.1AS-2011 8.6.2.3).
   - Correct the builder comments at `endstation_builder.py:3561`, `:4153` and `:4165-4168`. They must no longer say the generator "consumes only" priority1, MAC and clock, or "announces this field from a constant".
2. The ROM digests are re-recorded through their recorder. The `test_builder.py` model-shape hashes are re-pinned where clock_accuracy, as descriptor content, moves them.
3. The `gptp_shadow` and `gptp_plane` harness constants named `OUR_CQ` hold the new value, or take it from the build.
4. The page listing where the board follows a stricter reading than its clause points at the merged gPTP behaviour.

## Acceptance

- The full sweep, with milan_dp's gptp and gptp-lat legs, gptp_shadow and gptp_plane, the firmware self-test, the builder, behave and the docs gates are green, and the docs inventory is regenerated.
- A builder test with a `0xFE` config and one with a `0x22` config each produce that value on the wire in the gPTP leg.
- Area and timing of the shipping route are recorded against dev.

