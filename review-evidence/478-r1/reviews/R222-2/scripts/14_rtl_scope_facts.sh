#!/usr/bin/env bash
# RTL-lens scope facts at the exact head. Read-only git queries against the
# review clone (and its initialized protocol-processor submodule).
set -euo pipefail
R=$VALIDATION_STORAGE/reviews/r222-478-r2
HEAD_C=1496558d82cf35fc98dda0e781b2a1be643c301a
BASE_NOW=88e9276b2a220c716f64a843f7e1eb8f9265e896
OLD_C=d81a302760b84f32d2aa019643f57682bb6e052c
PIN=424c688fa2205b934a7689a58f2aa766420f2326
cd "$R"
echo "## PR delta ($BASE_NOW..$HEAD_C) paths under RTL/bench/synthesis/pin scope"
git diff --name-only $BASE_NOW $HEAD_C -- hdl tb syn sw/litex constraints third_party protocol-processor gptp-processor external .gitmodules | sed 's/^/  /'
echo "  (end; empty means none)"
echo "## changes since round-1 head ($OLD_C..$HEAD_C) under the same scope"
git diff --name-only $OLD_C $HEAD_C -- hdl tb syn sw/litex constraints third_party protocol-processor gptp-processor external .gitmodules | sed 's/^/  /'
echo "  (end; empty means none)"
echo "## consumers of the emitted AEM_RATES_* tables (parent hdl/ and pinned processor hdl/)"
git grep -n -E 'AEM_RATES_(N_)?C' $HEAD_C -- hdl | sed 's/^/  /' || echo "  parent hdl/: none"
git -C protocol-processor grep -n -E 'AEM_RATES_(N_)?C' $PIN -- hdl | sed 's/^/  /' || echo "  protocol-processor@$PIN hdl/: none"
echo "## where the emitted table goes (avdecc/aem_emit.py) and the descriptor count width (avdecc/aem_descriptors.py)"
git grep -n -E 'AEM_RATES_N_C =|AEM_RATES_C \[' $HEAD_C -- avdecc/aem_emit.py | sed 's/^/  /'
git grep -n -E 'be16\(144\)|be16\(len\(rates\)\)' $HEAD_C -- avdecc/aem_descriptors.py | sed 's/^/  /'
echo "## hand-built pp_shadow spellings of the AUDIO_UNIT (unchanged; S1 residue)"
git grep -n -E 'AU_RATES_C\[3\]|AU_CUR_RATE_C =|AU_LEN_C +=|put16be_v\(d, 142, 3\)|k < 3; k\+\+' $HEAD_C -- tb/verilator/pp_shadow/sim_main.cpp | sed 's/^/  /'
echo "## pp_shadow harness elaborates the arty_current shape"
git grep -n -E 'endstation_arty_current' $HEAD_C -- tb/verilator/pp_shadow/Makefile | sed 's/^/  /'
