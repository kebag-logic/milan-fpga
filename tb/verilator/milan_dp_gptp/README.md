# AX7101 physical gPTP integration suite

Run `make` here for the trimmed physical integration.
The shared recipe remains in `../milan_dp/Makefile`.
It builds one eight-channel TDM8 datapath with gPTP enabled.
It then checks uncounted audio omissions after zero-cycle setup failure.
The original long spans require `make extended` explicitly.

The [model and phase rationale](../milan_dp/README.md#ax7101-1x1-eight-channel-gptp-physical-rate-run)
document clocks, independent peer events, assertions, and exclusions.
The [testing guide](../../../docs/testing/TESTING.md) declares the 2400-second budget.
The driver gives the historical `milan_dp` suite 1800 seconds.
Sharding places this suite on worker 3/4.
The sweep executes each leg once.
