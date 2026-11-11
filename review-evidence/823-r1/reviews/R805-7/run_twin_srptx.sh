#!/bin/sh
# S7's two-placement comparison and SRP transmit path at a candidate tree (both compile the saved-state store
# through twin_fw.py); argv: TREE RECEIPTS_DIR VERILATOR_WRAPPER.
T=$1; R=$2; V=$3; cd "$T/tb/verilator/milan_dp" || exit 2
"$V" --version > "$R/verilator-version.txt" 2>&1
make -j8 VERILATOR="$V" twin > "$R/make_twin.log" 2>&1; echo $? > "$R/make_twin.rc"
make -j8 VERILATOR="$V" srptx > "$R/make_srptx.log" 2>&1; echo $? > "$R/make_srptx.rc"
