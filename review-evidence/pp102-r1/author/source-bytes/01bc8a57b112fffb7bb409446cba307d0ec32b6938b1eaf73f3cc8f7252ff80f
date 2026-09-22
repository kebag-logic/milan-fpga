<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# aecp_notify registry monitor lifecycle

Builds `KL_aecp_notify` with two controller rows and drives its registry,
timer, PRNG, and CONTROLLER_AVAILABLE faces directly.

The suite registers a TIME_LIMITED controller, starts its availability probe,
expires the registry row while that probe is active, and requires a targeted
cancellation before the row is cleared. It then reuses the same row for a
different controller and verifies that the next probe carries only the new
Entity ID and MAC tuple.

Run `make`. Exit status zero and the printed check tally are required.
