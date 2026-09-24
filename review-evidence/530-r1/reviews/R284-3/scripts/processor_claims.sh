#!/bin/sh
# Print the processor lines the round-2 corner text cites, at the pinned gitlink,
# plus the parent status-word packing, so each claim can be checked by eye.
# Usage: processor_claims.sh <repo>
set -eu
R=$1
PP=$(git -C "$R" ls-tree HEAD protocol-processor | awk '{print $3}')
echo "parent HEAD $(git -C "$R" rev-parse HEAD), protocol-processor gitlink $PP"
show() { git -C "$R/protocol-processor" show "$PP:$1" | awk -v a="$2" -v b="$3" -v f="$1" 'NR>=a&&NR<=b{printf "%s:%d: %s\n", f, NR, $0}'; }
show hdl/srp/KL_srp_top.sv 444 445
show hdl/srp/KL_srp_top.sv 772 781
show hdl/srp/KL_srp_top.sv 850 862
show hdl/srp/KL_srp_admission.sv 152 155
show hdl/srp/KL_srp_admission.sv 206 214
show hdl/srp/KL_srp_talker_fsm.sv 438 441
show hdl/srp/KL_srp_talker_fsm.sv 539 542
show hdl/srp/KL_srp_talker_fsm.sv 636 639
show hdl/srp/KL_srp_talker_fsm.sv 684 711
show hdl/srp/KL_srp_talker_fsm.sv 800 803
pshow() { git -C "$R" show "HEAD:$1" | awk -v a="$2" -v b="$3" -v f="$1" 'NR>=a&&NR<=b{printf "%s:%d: %s\n", f, NR, $0}'; }
pshow hdl/milan/milan_datapath.sv 1652 1658
pshow hdl/milan/milan_datapath.sv 2505 2511
pshow hdl/milan/milan_datapath.sv 3055 3059
pshow hdl/milan/milan_datapath.sv 5280 5281
pshow hdl/milan/milan_datapath.sv 5305 5319
pshow hdl/milan/milan_datapath.sv 6632 6647
pshow hdl/ieee1722/avtp/KL_talker_diag_ctx.sv 255 278
pshow hdl/ieee1722/crf/KL_crf_tx.sv 497 510
pshow hdl/ieee1722/aaf/KL_aaf_packetizer.sv 314 316
pshow hdl/ieee1722/aaf/KL_aaf_packetizer.sv 732 738
