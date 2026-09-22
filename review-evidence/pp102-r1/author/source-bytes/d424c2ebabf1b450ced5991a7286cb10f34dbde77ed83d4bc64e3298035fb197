#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Elaborate the REAL protocol_processor_top across shapes. Two claims:
#
#   LEGAL shapes must elaborate with ZERO warnings under -Wall. This is the
#   only thing that can prove the F08.4 map and every index width actually
#   TRACK P-N-STREAM-IN / P-N-STREAM-OUT: a simulation of the 8x8 shape sees
#   nothing, because 8x8 is the one shape a literal map is right at.
#
#   OVER-LARGE shapes must FAIL, loudly, at elaboration. The 8-bit expiry
#   bus's owner-tag allocation (pp_pkg PP_OWN_*) is fixed, so a shape past
#   it has no correct map; the guard in the top turns that into a build stop
#   instead of two engines sharing an owner tag in silence.
#
# Exit 0 = both claims hold.
#
# Strict mode, with the three statuses this script EXPECTS to be non-zero
# marked where they are read: the OVER loop's elaboration (which MUST fail),
# and the two `grep`s that take the verdict. Those greps read $out from a
# HERE-STRING rather than a pipe, because under `pipefail` a `grep -q` that
# matches early closes the pipe, the `echo` feeding it dies of SIGPIPE, and the
# pipeline reports non-zero - which here would print SHAPE OK for a shape that
# WARNED, and turn this script's whole claim into a false green.
set -euo pipefail
cd "$(dirname "$0")" || exit 1      # $HDL below is relative to this directory
VERILATOR=${VERILATOR:-verilator}
HDL=../../hdl
SRCS=$( (find "$HDL" -name '*_pkg.sv' | sort; find "$HDL" -name '*.sv' ! -name '*_pkg.sv' | sort) )
VFLAGS="--lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM"

# One elaboration of the real top at one shape: combined output on stdout,
# verilator's own status as the return status. $VFLAGS is a flag list and
# $SRCS a file list, and the word split of both is what builds the command.
elaborate() { # $1=N_STREAM_IN_P $2=N_STREAM_OUT_P
  $VERILATOR $VFLAGS --top-module protocol_processor_top -GN_STREAM_IN_P="$1" -GN_STREAM_OUT_P="$2" $SRCS 2>&1  # shellcheck disable=SC2086 # deliberate word split of the flag and source lists
}

# SI SO — the F01.5 default, the board's 1-stream shipping shape, the 9x9
# shape the reference platform's generated header asks for, and asymmetric
# shapes (a map derived from the WRONG count still looks right when SI == SO)
LEGAL="1:1 1:8 8:1 2:2 4:4 8:8 9:9 9:2 3:12 16:16"
# past the owner-tag space: SO 17 overruns the talker tag base, SI 33 the
# listener tag base (ADP publishes its slot AS its owner tag)
OVER="17:17 16:17 33:8"

rc=0
for pair in $LEGAL; do  # shellcheck disable=SC2086 # deliberate word split of the space-separated shape list
  si=${pair%%:*}; so=${pair##*:}
  if ! out=$(elaborate "$si" "$so") || grep -qE '%(Warning|Error)' <<<"$out"; then
    echo "SHAPE FAIL SI=$si SO=$so (legal shape must elaborate clean)"
    # The verdict is already taken; `head` closing this pipe early is expected.
    grep -E '%(Warning|Error)' <<<"$out" | head -5 || true
    rc=1
  else
    echo "SHAPE OK   SI=$si SO=$so"
  fi
done

for pair in $OVER; do  # shellcheck disable=SC2086 # deliberate word split of the space-separated shape list
  si=${pair%%:*}; so=${pair##*:}
  # This elaboration MUST fail - that is the claim - so its status is consumed
  # here. Unguarded, `errexit` would end the script at the first over-large
  # shape and never print the verdict the failure was run to produce.
  out=$(elaborate "$si" "$so") || true
  if grep -q 'F08.4: owner tags OVERLAP' <<<"$out"; then
    echo "GUARD OK   SI=$si SO=$so (elaboration refused, as it must)"
  else
    echo "GUARD FAIL SI=$si SO=$so — the guard did NOT fire. An over-large"
    echo "           shape would alias owner tags in silence."
    rc=1
  fi
done
exit "$rc"
