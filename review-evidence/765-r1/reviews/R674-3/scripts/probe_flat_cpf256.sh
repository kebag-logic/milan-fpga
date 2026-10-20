#!/bin/sh
# Probe: does the flat instrument KL_avtp_rx_monitor accept "any nonzero
# channel count"? Feeds 10-bit channels_per_frame 256 (low byte 0) and 257
# into the [28] scenario of a disposable copy of the flat harness.
# usage: probe_flat_cpf256.sh <repo-at-head> <scratch-dir> <verilator>
set -eu
REPO=$1; S=$2; V=$3
rm -rf "$S"; mkdir -p "$S"
git -C "$REPO" archive HEAD hdl tb/verilator/avtp_rxmon tb/common | tar -x -C "$S"
mkdir -p "$S/third_party/verilog-axis/rtl"; cp "$REPO/third_party/verilog-axis/rtl/axis_fifo.v" "$S/third_party/verilog-axis/rtl/"
cd "$S/tb/verilator/avtp_rxmon"
python3 -I - sim_main.cpp <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
a='    uint8_t  chans    = 8;\n'
assert s.count(a)==1; s=s.replace(a,a+'    uint8_t  cpf_hi   = 0;\n')
b='        f[o+17]=static_cast<uint8_t>(c.nsr<<4);\n'
assert s.count(b)==1; s=s.replace(b,'        f[o+17]=static_cast<uint8_t>((c.nsr<<4)|(c.cpf_hi&3));\n')
c='        ck("[28f] ...and no UNSUPPORTED for it", dut->cnt_unsupported_fmt_o, 1);\n'
assert s.count(c)==1
s=s.replace(c,c+'''        { AafCfg c; c.seq=3; c.chans=0; c.cpf_hi=1; feed(build_aaf(stim, c)); }
        printf("PROBE cpf=256: frames_rx=%ld unsupported=%ld\\n", (long)dut->cnt_frames_rx_o, (long)dut->cnt_unsupported_fmt_o);
        { AafCfg c; c.seq=3; c.chans=1; c.cpf_hi=1; feed(build_aaf(stim, c)); }
        printf("PROBE cpf=257: frames_rx=%ld unsupported=%ld\\n", (long)dut->cnt_frames_rx_o, (long)dut->cnt_unsupported_fmt_o);
''')
open(p,'w').write(s)
PY
make -s -n VERILATOR="$V" run > recipe.txt || true
sh -c "$(head -1 recipe.txt)" > build.log 2>&1
./obj_dir/Vavtp_rxmon_wrap_sim 2>&1 | grep -E "PROBE|\[28|PASS|FAIL|passed|failed" | head -40
