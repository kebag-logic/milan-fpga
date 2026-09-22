<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# ca_originator frame builder lifecycle

Builds `KL_aecp_ca_originator` and verifies CONTROLLER_AVAILABLE construction,
owner-indexed sequence capture, registered allocation handshakes, and every
pre-issue cancellation phase.

The suite checks that allocation requests are separated while waiting for the
registered pool result, frame bytes 34 and 35 use the newly selected owner's
sequence, and cancellation releases an allocated slot without committing or
issuing a partial frame.

Run `make`. Exit status zero and the printed check tally are required.
