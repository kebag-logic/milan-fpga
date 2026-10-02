#!/bin/sh
# Run the tb/desc_store suite (generator-check gate + RTL suite) of a processor
# tree with the pinned Verilator. usage: run_desc_store_suite.sh <tree> <log> <rcfile>
cd "$1/tb/desc_store" || exit 2
make VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator > "$2" 2>&1
echo $? > "$3"
