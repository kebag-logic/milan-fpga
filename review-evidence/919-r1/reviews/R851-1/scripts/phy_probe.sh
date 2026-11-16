#!/usr/bin/env bash
# phy_probe.sh OUT [SRC]: build test_plat_phy.cpp against ctrl_plat_phy.c (SRC, default the clone's) and run it.
# The store's three calls the poll's THE STEP client makes are stubbed (stubs.c): the suite never calls that client.
# Exit: the suite's. Disposable: OUT is under the packet's scratch.
set -u
R=${CLONE:?export CLONE, the review clone at the exact head}
G=${PACKET}/scratch/fw-unit/checkout/acmpnvm/gen
OUT=$1; SRC=${2:-$R/sw/firmware/ctrl/plat/ctrl_plat_phy.c}
mkdir -p "$OUT"
cat > "$OUT/stubs.c" <<'EOF'
#include "nvm_store.h"
static struct nvm_status st;
const struct nvm_status *nvm_store_status(void) { return &st; }
bool nvm_store_step(void *ctx, uint32_t deadline) { (void)ctx; (void)deadline; return false; }
uint32_t nvm_store_clock(void *ctx) { (void)ctx; return 0u; }
EOF
T=$R/sw/firmware/ctrl/test
INC="-I$R/sw/firmware/ctrl/plat -I$T -I$R/sw/firmware/gtest -I$R/sw/firmware/ctrl_nvm -I$G -I$R/sw/firmware/ctrl/mbx -I$R/sw/firmware/ctrl/loop -I$R/sw/firmware/ctrl/port -I$R/sw/firmware/ctrl/host -I$R/third_party/tsn-c-stack/include -I$R/sw/firmware/ctrl/maap -I$R/sw/firmware/ctrl/srp -I$R/sw/firmware/ctrl/app -I$R/sw/firmware/ctrl/aecp -I$R/sw/firmware/ctrl/acmp -I$R/sw/firmware/ctrl/adp"
gcc -std=c11 -O1 -Wall -Wextra -Werror $INC -c "$SRC" -o "$OUT/phy.o" || exit 3
gcc -std=c11 -O1 -Wall $INC -c "$OUT/stubs.c" -o "$OUT/stubs.o" || exit 3
g++ -std=c++20 -O1 -Wall $INC -c "$T/test_plat_phy.cpp" -o "$OUT/t.o" || exit 3
g++ -std=c++20 -O1 -Wall $INC -c "$T/plat_bus.cpp" -o "$OUT/bus.o" || exit 3
printf '#include "fw_gtest.hpp"\nFW_TALLY_LABEL("probe")\n' > "$OUT/label.cpp"
g++ -std=c++20 -O1 $INC -c "$OUT/label.cpp" -o "$OUT/label.o" || exit 3
g++ "$OUT"/*.o -lgtest_main -lgtest -pthread -o "$OUT/t" 2> "$OUT/link.err" || { cat "$OUT/link.err" | head -20; exit 3; }
"$OUT/t" --gtest_brief=1 > "$OUT/run.log" 2>&1
rc=$?
grep -E '^\[  (FAILED|PASSED) |Failure|^.*: Failure|<<|P[0-9]+ ' "$OUT/run.log" | head -12
exit $rc
