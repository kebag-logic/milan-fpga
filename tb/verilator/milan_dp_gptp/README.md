# AX7101 physical gPTP integration suite

Run `make` here for the physical integration.
The shared recipe remains in `../milan_dp/Makefile`.
It builds one eight-channel TDM8 datapath with gPTP enabled.
It then grades setup, audio-window and missing-response accounting.
The normal total is 177 checks: 137 physical, 40 accounting.
The original long spans require `make extended` explicitly.
Extended mode runs the physical harness alone, with 137 checks.

The [model and phase rationale](../milan_dp/README.md#ax7101-1x1-eight-channel-gptp-physical-rate-run)
document clocks, independent peer events, assertions, exclusions, and measured timings.

The default sweep excludes this directory.
The [workflow policy](../../../docs/testing/CI_WORKFLOWS.md) assigns nightly and manual execution.
Physical regressions report nightly, outside the required PR aggregate.
The suite retains every transition, physical rate, timer, and threshold.

```sh
VERILATOR_JOBS=4 scripts/run_all_suites.sh /tmp/physical-logs --physical-gptp
make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4
make -C tb/verilator/milan_dp_gptp extended VERILATOR_JOBS=4
```

The first command includes preflight, timeout, verdict, and tally handling.
The [testing guide](../../../docs/testing/TESTING.md) declares 5400 seconds, including compilation.
The separate four-core `ubuntu-latest` workflow job permits 120 minutes.
The reference machine uses an EPYC 9554P with 128 logical CPUs.
Measurements restrict each job to four cores under background load.
Completed hosted physical evidence remains required to validate that deadline.
The historical `milan_dp` suite retains its 1800-second default.

The accounting verifier retains each failing DUT control transcript.
They reside under `../milan_dp/obj_ax1x1gptp/`, outside passing suite logs.
Initial silence produces RX traffic with zero TX or comparisons.
The stopped-traffic control preserves previous comparisons before withholding admission.
Each silent window prints three explicit, uncounted comparison omissions.
Activity and payload checks retain their nonzero DUT verdicts.
The missing-response control transmits real Pdelay requests and withholds every response.
It runs through the unchanged 1.8-second acquisition deadline and acquired-publication check.
First-exchange, peer-arrival and delay comparisons remain explicitly uncounted without responses.
The missing-response and publication-health assertions retain a failing DUT result.
The verifier grades fourteen checks on that failure path.
