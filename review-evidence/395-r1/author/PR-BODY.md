[A387] Relates to #395.

Declare the AX7101 dev-board release's commercial grade (0 to 85 C junction)
once in the platform timing definition. New builds and the saved-checkpoint
reporter derive their part and conditions from it. Builder tests pin the
decision and reject changed conditions or disabled setup/hold analysis.

The shipping 1x1 TDM8 checkpoint has Slow WNS/WHS +0.123/+0.101 ns and Fast
WNS/WHS +1.429/+0.036 ns, with zero TNS/THS and no negative-slack paths.
These fixed speed-model results repeat at both recorded temperature endpoints.
The findings document retains ten Critical CDC diagnostics, two unsafe clock
pairs and 46 input/87 output ports without delay constraints. Positive timing
slack does not discharge those findings.

Validation at `66001a307ce5de57577e66d6e3a18b9f4020764b`: full builder bank in both compiler modes with required elaboration, CI scope self-test, documentation gates, whitespace checks, routed-checkpoint reports and live wrong-condition controls all returned 0. Both builder modes record an unavailable legacy calibration report; the absent mode also records its expected compiler-dependent skips.

Items 3 and 4 remain: die-temperature logging and external oscillator measurements.
See [the candidate record](docs/findings/COMMERCIAL_TIMING_395.md) for hashes,
implementation recipe, the per-corner table and report limitations.
