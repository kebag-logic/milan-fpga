#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Shared settings for the R259-3 review scripts, sourced by each of them.
# DATA must name the directory that holds reviews/ and tmp/ on the review
# host; every other path defaults beneath it or beside this script.
: "${DATA:?set DATA to the directory holding reviews/ and tmp/}"
: "${CLONE:=$DATA/reviews/r259-3-gptp68}"
: "${PACKET:=$(cd "$(dirname "$0")/.." && pwd)}"
: "${SCRATCH:=$PACKET/scratch}"
: "${PINNED_VERILATOR:=$DATA/tmp/372-manager-candidate1/pinned-tool-bin/verilator}"
HEAD_SHA=ba9268100ebe92dfc61aed30e2910245fc8c97cf
HEAD_TREE=5a02fa35db15d9a773895f82bb17020b55cfa775
BASE_SHA=c1b617435824929a790739ea8585c3fe1a328cc0
PREV_SHA=cbccf226068c107fb30764891c98b8d70c54d775
export DATA CLONE PACKET SCRATCH PINNED_VERILATOR HEAD_SHA HEAD_TREE BASE_SHA PREV_SHA
