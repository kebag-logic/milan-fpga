[A568]

Closes #167

At one AVB interface, retain a command's availability-probe cancellation when a simultaneous TIME_LIMITED drain occupies the output. Drain priority and immediate uncontended cancellation remain unchanged; the pending command cancellation follows on the next idle cycle. SC1 checks both row orders and fails when the second cancellation is dropped.

## Round 2

A failure for the commanding owner is now ignored while its cancellation remains pending. This closes the one-cycle window that could remove a live controller and send it a targeted DEREGISTER. SC2 reproduces that report timing in both row orders; removing the guard fails it. The reused P1 probe preserves the live row with both cancellations sent once, and P2 retains its original timing. Count-two behavior and CA1b are unchanged.

Validation at processor main and the new head:

- All 33 processor suites and all static gates pass: 1,028,291 to 1,028,293 checks. Only SC1 and SC2 are added relative to main, and only SC2 relative to the reviewed head.
- All ten affected campaigns pass: 459 existing controls, 461 at head. Every existing behavioral record is identical; every arm still plants.
- All 17 adopted parent consumer gates pass. Behavioral records are unchanged; the script inventory grows by eight lines from the reviewed head with unchanged findings. The existing external calibration-report arm remains recorded as not run.
- Fresh OOC 1x1: LUT 23,160 to 23,171 (+11); FF 19,787 to 19,807 (+20). Both deltas meet the +20 limits. Memory and DSP counts are unchanged.

Ports, parameters and register maps are unchanged.

