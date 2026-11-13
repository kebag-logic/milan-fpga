#!/bin/bash
# Round 2's final gate queue for HEAD (lane 895): round 1's gate_queue.sh lines (every workflow job a pull request to
# dev-soft-core triggers, each on its own fresh clone, and the lane's own gates), each unit named X-<name> with the
# gate root passed to it, and the CPU budget harness at both points in every arm against this round's legs
# (harness_final.sh: a fresh build at HEAD, a sample group, its image against the leg's, every measured group regraded).
# usage: queue3.sh HEAD GATES_ROOT > QUEUE
set -u
H=$1 GR=$2
G=$MANAGEMENT/2026-09-23/895-a775/scripts/gates
HF="GATES_ROOT=${GR}h BUILD_PREFIX=F4 /bin/bash $G/harness_final.sh $H"
echo "X-harness-A8 10G $HF A8:8x8:none:R3-A8:results-all:srp"
bash $G/gate_queue.sh "$H" "$GR/wf" | sed -e 's/^\(lane-[abc]\) \(10G\) /X-\1 \2 GATES_ROOT='"${GR//\//\\/}"' /' -e 's/^W-/X-W-/' | head -4
echo "X-harness-NWB8 10G $HF N8:8x8:answering-every-port:R3-N8:results:notice-every-1 W8:8x8:valid-destinations:R3-W8:results:srp-talker-loss B8:8x8:answering-ports:R3-B8:results:aecp:aecp"
echo "X-harness-A1 10G $HF A1:1x1:none:R3-A1:results-all:srp"
echo "X-harness-NWB1 10G $HF N1:1x1:answering-every-port:R3-N1:results:notice-every-1 W1:1x1:valid-destinations:R3-W1:results:srp-talker-loss B1:1x1:answering-ports:R3-B1:results:aecp:aecp"
bash $G/gate_queue.sh "$H" "$GR/wf" | sed -e 's/^\(lane-[abc]\) \(10G\) /X-\1 \2 GATES_ROOT='"${GR//\//\\/}"' /' -e 's/^W-/X-W-/' | tail -n +5
