[A568]

Closes #167

At one AVB interface, retain a command's availability-probe cancellation when a simultaneous TIME_LIMITED drain occupies the output. Drain priority and immediate uncontended cancellation remain unchanged; the pending command cancellation follows on the next idle cycle.

SC1 exercises both row orders and requires both cancellations exactly once. It fails on the original RTL and on the new control that drops the second cancellation. The count-two implementation, CA1b, and its control retain their existing records. Ports, parameters, and register maps are unchanged.

Validation at base and head:

- All 33 processor suites, HDL lint, documentation checks, matrix checks, and synthesis pass. The suite adds only SC1: 1,028,291 to 1,028,292 checks.
- All ten affected campaigns pass: 459 existing controls at base, 460 at head. Every common result is identical; only the SC1 golden and its control are added.
- All 17 parent consumer commands pass with both adoption patches. Behavioral records are unchanged. The Python inventory grows by 21 lines with unchanged findings; the existing unavailable external calibration-report arm remains marked not run.
- OOC 1x1: LUT 23,160 to 23,101 (−59); FF 19,787 to 19,802 (+15). Both deltas meet the +20 limits. Memory and DSP counts are unchanged.
