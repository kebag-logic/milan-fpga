#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Shared settings for the R259-2 review packet; sourced by every script.
# PACKET is this packet (the parent of scripts/). CLONE is the exact-head
# review clone and PIN_BIN the directory holding the pinned Verilator 5.050
# wrapper; both default to this host's layout relative to the packet and
# may be overridden from the environment.
PACKET=$(cd "$(dirname "$0")/.." && pwd)
: "${CLONE:=$(cd "$PACKET/.." && pwd)/r259-2-gptp68}"
: "${PIN_BIN:=$(cd "$PACKET/../.." && pwd)/tmp/372-manager-candidate1/pinned-tool-bin}"
HEAD_SHA=cbccf226068c107fb30764891c98b8d70c54d775
HEAD_TREE=e8b9fa23fe5e1d5e3bd3ab1dd3c09196760a5063
BASE_SHA=c1b617435824929a790739ea8585c3fe1a328cc0
REVIEWED_SHA=77c34e904eba2446755d13e1bf4763d1652c3ca7
WRAPPER_SHA256=905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f
SCRATCH="$PACKET/scratch"
RECEIPTS="$PACKET/receipts"
# scripts/bin/verilator caps --build -j 0 at 8 jobs and runs the pinned wrapper
PATH="$PACKET/scripts/bin:$PATH"
export PACKET CLONE PIN_BIN HEAD_SHA HEAD_TREE BASE_SHA REVIEWED_SHA SCRATCH RECEIPTS PATH
