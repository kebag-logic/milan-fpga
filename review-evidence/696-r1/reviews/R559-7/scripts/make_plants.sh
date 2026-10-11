#!/bin/sh
# Re-create the three constant plants used by first_draw_proof_negatives.txt.
# Usage: sh make_plants.sh <path/to/KL_maap.sv> <outdir>
set -eu
mkdir -p "$2"
sed "s/32'h8008_0040/32'h8000_0040/" "$1" > "$2/q9.sv"
sed "s/32'h1040_0000, 32'h0000_0081/32'h1040_0000, 32'h0000_0080/" "$1" > "$2/q3.sv"
sed "s/32'h0000_0409, 32'h2420_0880/32'h0000_0409, 32'h0000_0081/" "$1" > "$2/rowrep.sv"
