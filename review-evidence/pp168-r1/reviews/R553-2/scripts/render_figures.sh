#!/usr/bin/env bash
set -euo pipefail
src=${1:?source clone}
packet=${2:?packet directory}
mkdir -p "$packet/receipts" "$packet/scratch/figures"
rsvg-convert -b white "$src/docs/diagrams/24-adp-acmp-states.svg" -o "$packet/receipts/states-render.png"
rsvg-convert -b white "$src/docs/diagrams/wavedrom/fig-07-sinkrec.svg" -o "$packet/receipts/sinkrec-render.png"
printf 'text, tspan { font-family: monospace; }\n' > "$packet/scratch/figures/alternate.css"
rsvg-convert -b white -s "$packet/scratch/figures/alternate.css" "$src/docs/diagrams/wavedrom/fig-07-sinkrec.svg" -o "$packet/receipts/sinkrec-alternate-render.png"
fc-match sans-serif
fc-match monospace
