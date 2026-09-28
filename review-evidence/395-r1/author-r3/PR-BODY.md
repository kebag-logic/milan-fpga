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

## Round 2

Record the rejected crossing exceptions, their source and log locations,
and the missing clock-name prefix. The retained census contains 14 emitted
critical warnings; a fifteenth text match is echoed source. The unsafe
Ethernet/milan pairs and unbounded Ethernet-to-system false paths are explained,
with measured slack against the intended 8 ns bound. [Issue #607](https://github.com/kebag-logic/milan-fpga/issues/607)
owns the constraint fix.

Apply the [recorded margin](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611):
WNS >= +0.03 ns and WHS >= 0 at every corner. The shipping placement meets
both thresholds for its applied constraints. The intended crossing bound's
smallest measured slack is +2.560 ns; this measurement does not restore
missing constraints or establish CDC correctness.

The builder now exercises refusal through the actual report hook and checks
setup, hold, unconstrained-path and verbose report content. The AX7101 PLL
speed grade derives from the declared platform part, with a changed-part
control. BUILDING's retention list includes the critical-warning census.

Round-2 validation at `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`: the full builder bank
in both compiler modes with required elaboration, CI scope self-test,
the listed documentation gates and whitespace checks returned 0. The bare-metal
scope gate was omitted and later failed in both independent reviews. Fresh checkpoint
reports reproduce the corner metrics. All five required faults fail through
the full builder entry point; the broader 21-fault campaign has no unexpected
outcomes, and the unmodified control passes. The PLL literal control also
fails as intended. Both builder modes retain the historical calibration skip;
the absent mode records its expected compiler-dependent stand-downs.

Clearing all false paths exposes fourteen milan-to-Ethernet endpoints,
including reset paths. Their worst Slow/Fast slack is +4.056/+5.878 ns.
The review's six-endpoint measurement retained generic false paths and gave
+7.066/+7.538 ns. The record distinguishes both path populations.

Items 3 and 4 remain open. Relates to #395.

## Round 3

Reword the crossing description so the unchanged bare-metal scope gate passes.
Identify both generic false-path classes and their endpoints: MultiReg D pins
and AsyncResetSynchronizer PRE pins. Reset-assertion policy remains for #607.
Link the retained crossing script and results at their published evidence commit,
and add the commercial timing record to the findings index.

The standalone timing-grade entry now also runs the changed-part PLL control
when given the platform interpreter. Align the older margin wording with
WNS >= +0.03 ns and WHS >= 0 at every corner. The
[owner's correction](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860783553)
states that these thresholds are not automatically enforced; sweep seed
selection is manual.

Round-3 validation at `3b5603e3d16a164c35329efeb633800fe4fe9f95`: the full builder bank in
both compiler modes with required elaboration, the bare-metal check and
self-test, CI scope self-test, documentation and idiom gates, and whitespace
checks all returned 0. The standalone PLL control passes and the restored
literal fails at the expected assertion. Fresh read-only checkpoint reports
reproduce every corner value and crossing endpoint class; all seven shipping
input hashes remain unchanged. Both banks retain the historical calibration
skip, and the absent mode records expected compiler-dependent skips.

Items 3 and 4 remain open. Relates to #395.
