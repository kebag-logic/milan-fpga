#!/bin/sh
# Reviewer probe (R420-4): run main's C5a sections with the lane's identify
# sequencer BUILT (EN_IDENTIFY_NOTIF_P = 1, button idle), in a private copy of
# the head export: (a) DL and HZ beside ID in the identify build; (b) TB in a
# build that sets both PP_TOP_EN_IDENT and PP_TOP_TIM_REAL.
# Usage: en1_c5a_probe.sh HEAD_EXPORT WORK_DIR
set -eu
src=$1; work=$2
rm -rf "$work"; mkdir -p "$work"
cp -a "$src/hdl" "$src/tb" "$src/scripts" "$work/"
rm -rf "$work/tb/pp_top"/obj_*
python3 - "$work/tb/pp_top/sim_main.cpp" "$work/tb/pp_top/Makefile" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
old = "  run_identify(h);\n  const char* const build = \"identify\";\n"
assert s.count(old) == 1
new = ("#ifdef PP_TOP_TIM_REAL\n  run_budgets(h);\n#else\n  run_identify(h);\n"
       "  run_deadlines(h);\n  run_hazards(h);\n#endif\n  const char* const build = \"identify\";\n")
p.write_text(s.replace(old, new))
m = pathlib.Path(sys.argv[2]); t = m.read_text()
old = "identify-build: ltn_rom.hex ucode.hex\n"
assert t.count(old) == 1
t = t.replace(old, "identify-tim-build: ltn_rom.hex ucode.hex\n"
    "\t@mkdir -p obj_dir\n"
    "\t$(VERILATOR) $(VFLAGS) \"+define+PP_TOP_EN_IDENT\" \"+define+PP_TOP_TIM_REAL\" \\\n"
    "\t    -CFLAGS \"-DPP_TOP_EN_IDENT -DPP_TOP_TIM_REAL -Wall -Wextra\" \\\n"
    "\t    --Mdir obj_idt $(SRCS) $(CPP) -o Vpp_top_idt\n\n" + old)
m.write_text(t)
PY
cd "$work/tb/pp_top"
echo "== (a) identify build: ID, DL, HZ at EN_IDENTIFY_NOTIF_P = 1"
make identify-build > build-a.log 2>&1
./obj_idn/Vpp_top_idn | grep -E '^FAIL|^(ID|DL|HZ): |^\[build' || true
echo "== (b) identify + nominal timebase: TB at EN_IDENTIFY_NOTIF_P = 1"
make identify-tim-build > build-b.log 2>&1
./obj_idt/Vpp_top_idt | grep -E '^FAIL|^TB: |^\[build' || true
