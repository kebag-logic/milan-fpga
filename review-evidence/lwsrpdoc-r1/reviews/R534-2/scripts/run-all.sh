#!/usr/bin/env bash
# Reproduce this review's executable evidence.
# Usage: run-all.sh CLONE PACKET   (CLONE at cd659eb5e93c4da5e97fcbd6282b1efba16e565d)
# Needs: a C compiler, the build system, the scenario runner, the graph renderer,
# and the unit framework installed under PACKET/scratch/deps (built from its public source).
set -u
clone=$1; packet=$2; s=$packet/scratch; here=$(cd "$(dirname "$0")" && pwd)
"$here/run-doc-checks.sh" "$clone" "$s/doc-checks" &
"$here/run-suites.sh" "$clone" "$s/snap-suites" "$s/suites" "$s/deps" &
"$here/run-probes.sh" "$clone" "$s" "$s/probes" "$s/deps" &
wait
"$here/render-png.sh" "$s/doc-checks/graphs" "$s/png" 830
python3 "$here/edge-node-crossings.py" "$s"/doc-checks/graphs/*.svg
"$here/run-probe-rla.sh" "$s/snap-suites" "$s/probe-rla"
# Headless page check (needs the renderer's bundled browser module on NODE_PATH):
#   NODE_PATH=<renderer node_modules> node "$here/open-iso-page.cjs" "$s/iso-page.png"
