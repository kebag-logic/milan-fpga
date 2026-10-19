#!/bin/sh
# Prints the cited line ranges at the lane head, with relative paths.
set -e
cd "$1"
echo "head: $(git rev-parse HEAD)"
echo "processor submodule: $(git -C protocol-processor rev-parse HEAD)"
show() { echo; echo "== $1:$2-$3"; sed -n "$2,$3p" "$1" | nl -ba -v "$2"; }
show protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv 98 121
show protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv 397 406
show hdl/milan/KL_pp_shadow.sv 929 932
show hdl/milan/KL_pp_shadow.sv 949 951
show hdl/milan/milan_datapath.sv 4452 4455
show docs/design/SAVED_STATE_MATERIALIZATION.md 17 20
show docs/design/SAVED_STATE_MATERIALIZATION.md 1138 1151
show docs/design/SAVED_STATE_MATERIALIZATION.md 1164 1164
show docs/design/SAVED_STATE_MATERIALIZATION.md 1217 1219
show docs/design/SAVED_STATE_MATERIALIZATION.md 2754 2758
show docs/design/SAVED_STATE_FASTCONNECT.md 332 332
show docs/design/SAVED_STATE_FASTCONNECT.md 661 676
show docs/design/SAVED_STATE_FASTCONNECT.md 1472 1476
show sw/firmware/milan_baremetal/milan_baremetal.c 894 921
show sw/firmware/ctrl_nvm/nvm_store.c 288 309
show sw/firmware/ctrl_nvm/nvm_store.c 494 517
show sw/firmware/ctrl/aecp/aecp_nvm.c 56 73
show sw/firmware/ctrl/aecp/aecp_nvm.c 94 105
show sw/firmware/ctrl/test/test_aecp.cpp 208 225
