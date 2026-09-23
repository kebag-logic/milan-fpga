#!/bin/sh
# Start-phase probe for the #387 gmstep leg (disposable; never committed).
# Copies the tree under review (without build outputs), adds to a COPY of
# sim_gmstep.cpp (1) an idle delay of GMSTEP_PHASE_DELAY cycles before the
# peer's media feed starts and (2) a print of the render fill's per-cycle
# minimum and maximum over the baseline, then builds the leg on the head
# datapath and, optionally, on a patched datapath, and runs each delay.
# No RTL is changed by this probe.
# Usage: phase_probe.sh <tree> <work dir> <verilator> <edited datapath|-> <delay>...
set -u
tree=$1 work=$2 vl=$3 edited=$4; shift 4
rm -rf "$work/tree" && mkdir -p "$work" || exit 2
if command -v rsync > /dev/null; then
  rsync -a --exclude 'obj_*' "$tree/" "$work/tree/" || exit 2
else
  cp -a "$tree" "$work/tree" || exit 2
fi
cd "$work/tree/tb/verilator/milan_dp" || exit 2
python3 -I - << 'EOF' || exit 2
p = 'sim_gmstep.cpp'
s = open(p).read()
def once(anchor, new):
    global s
    assert s.count(anchor) == 1, anchor
    s = s.replace(anchor, new)
once('#include <cstdint>\n', '#include <cstdint>\n#include <cstdlib>\n')
once('''    write(0x654, 0x00020003);
    media_on_ = true;''', '''    write(0x654, 0x00020003);
    if (const char* d = std::getenv("GMSTEP_PHASE_DELAY")) run_cycles(std::strtoull(d, nullptr, 0));
    media_on_ = true;''')
a = '''    if (root->milan_datapath__DOT__avtprx_accept_p)
        fills_.emplace_back(cyc_, root->milan_datapath__DOT__rsp_fill_w & 0xFF);'''
once(a, a + '''
    if (probe_on_) {
        const unsigned f = root->milan_datapath__DOT__rsp_fill_w & 0xFF;
        probe_min_ = std::min(probe_min_, f);
        probe_max_ = std::max(probe_max_, f);
    }''')
once('    Trace trace_;', '''    Trace trace_;
    bool probe_on_ = false;
    unsigned probe_min_ = 255;
    unsigned probe_max_ = 0;''')
once('''    run_cycles(kClkHz / 5);
    check_.that("baseline: the listener accepted PDUs", fills_.size() - fills0 > 100);''',
     '''    run_cycles(kClkHz / 20);
    probe_on_ = true;
    run_cycles(kClkHz / 5 - kClkHz / 20);
    probe_on_ = false;
    printf("PROBE: baseline sawtooth min %u max %u\\n", probe_min_, probe_max_);
    check_.that("baseline: the listener accepted PDUs", fills_.size() - fills0 > 100);''')
open(p, 'w').write(s)
EOF
export PYTHONDONTWRITEBYTECODE=1
make gmstep-build GMSTEP_MDIR=obj_head VERILATOR="$vl" VERILATOR_JOBS=8 > "$work/build_head.log" 2>&1 || { echo "build head failed"; exit 2; }
variants=head
if [ "$edited" != "-" ]; then
  make gmstep-build GMSTEP_MDIR=obj_edited DP_SRC="$edited" VERILATOR="$vl" VERILATOR_JOBS=8 > "$work/build_edited.log" 2>&1 || { echo "build edited failed"; exit 2; }
  variants="head edited"
fi
# at most 8 legs run at once
for v in $variants; do
  printf '%s\n' "$@" | xargs -P 8 -I{} sh -c \
    'GMSTEP_PHASE_DELAY={} ./obj_'"$v"'/Vmilan_dp_gmstep obj_'"$v"'/aemi.bin > "$0/'"$v"'_{}.log" 2>&1; echo "exit $?" >> "$0/'"$v"'_{}.log"' "$work"
done
for v in $variants; do
  for d in "$@"; do
    f="$work/${v}_$d.log"
    printf '%s delay=%s | %s | %s | %s | %s | FAIL: %s\n' "$v" "$d" \
      "$(grep -h 'RENDER: fill at accept' "$f")" "$(grep -h '^PROBE:' "$f")" \
      "$(grep -h '^== gmstep' "$f")" "$(tail -n 1 "$f")" \
      "$(grep -h '\[FAIL\]' "$f" | sed 's/ got=.*//; s/^ *\[FAIL\] //' | tr '\n' ';')"
  done
done
