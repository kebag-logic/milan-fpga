#!/bin/sh
# Replay the round-7 internal probes byte-unchanged at the exact head (run under isolated.sh).
# usage: replay_r556_7.sh PACKET   (scripts in PACKET/prior-probes/R556-7/scripts, trees in PACKET/scratch/trees)
P=$1; S=$P/prior-probes/R556-7/scripts; T=$P/scratch/trees; W=$P/scratch/r556-7-replay; O=$P/receipts/r556-7-replay
mkdir -p "$W" "$O"
sha256sum "$S"/probe_assertions.py "$S"/probe_comment_gate.py "$S"/probe_spi_tree.sh "$S"/probe_dependency.sh | sed "s#$P/##" > "$O/provenance.sha256"
python3 -B "$S/probe_assertions.py" "$T/head" "$T/old" "$W/assertions" > "$O/probe_assertions.log" 2>&1; echo "probe_assertions rc=$?"
python3 -B "$S/probe_comment_gate.py" "$T/head" "$T/old" "$W/comment-gate" > "$O/probe_comment_gate.log" 2>&1; echo "probe_comment_gate rc=$?"
sh "$S/probe_spi_tree.sh" "$P/scratch/replay-clone" abe2476c4771bedc84531cf8d05fd12ef947c0cf "$W/spi-tree" > "$O/probe_spi_tree.log" 2>&1; echo "probe_spi_tree rc=$?"
PC_PLAIN=$P/scratch/sdk/gtest/lib/pkgconfig PC_ISYSTEM=$P/scratch/pc-isystem sh "$S/probe_dependency.sh" "$T/head" "$W/dependency" > "$O/probe_dependency.log" 2>&1; echo "probe_dependency rc=$?"
