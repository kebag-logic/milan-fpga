#!/usr/bin/env bash
# Disposable boundary-gate probes on a scratch copy of a tree (git checkout + clean restore after each).
# Usage: run_probes.sh <tree-copy> <out-dir> [probe ...]
set -u
T=$(cd "$1" && pwd); OUT=$2; shift 2
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
C=$T/sw/firmware/ctrl
restore() { git -C "$T" checkout -q -- . && git -C "$T" clean -qfd -- sw tb scripts >/dev/null; }
firmware_guard() {  # a firmware unit that reaches a stack example header only when macro $1 is defined
  printf '#ifdef %s\n#include "adp_port.h"\n#endif\n' "$1" >> "$C/adp/adp_mbx.c"
}
plant() {
  case "$1" in
    r584-maap-differential)  # a C++-only header reached only through test_maap_differential.cpp
      printf '#ifndef MAAP_R584_H\n#define MAAP_R584_H\n#ifdef __cplusplus\n#include "acmp_fake.hpp"\n#endif\n#endif\n' > "$C/maap/maap_r584.h"
      sed -i '0,/^#include/s//#include "maap_r584.h"\n#include/' "$C/test/test_maap_differential.cpp" ;;
    cxx-name-no-file) printf '\nR585_SOURCE = "test/test_r585_missing.cpp"\n' >> "$C/test/ctrl_arms.py" ;;
    cxx-name-computed) printf '\nR585_N = 4\nR585_SOURCE = f"test/test_r585_{R585_N}.cpp"\n' >> "$C/test/ctrl_arms.py" ;;
    py-join) printf '\nR585_FLAGS = ["-D" + "CTRL_R585_MODE"]\n' >> "$C/test/ctrl_arms.py" ;;
    py-format) printf '\nR585_FLAGS = ["-DCTRL_R585_MODE={}".format(1)]\n' >> "$C/test/ctrl_arms.py" ;;
    py-strjoin) printf '\nR585_NAME = "CTRL_R585_MODE"\nR585_FLAGS = "".join(["-D", R585_NAME])\n' >> "$C/test/ctrl_arms.py" ;;
    py-list-literal-control)  # the detectable form: the mode is explored and the reach is found
      printf '\nR585_FLAGS = ["-DCTRL_R585_MODE"]\n' >> "$C/test/ctrl_arms.py"; firmware_guard CTRL_R585_MODE ;;
    py-midstring)  # a -D inside a multi-word literal (a command line split later)
      printf '\nR585_FLAGS = "-O2 -DCTRL_R585_MODE".split()\n' >> "$C/test/ctrl_arms.py"; firmware_guard CTRL_R585_MODE ;;
    py-fstring-mid)
      printf '\nR585_CC = "gcc"\nR585_CMD = f"{R585_CC} -DCTRL_R585_MODE -c x.c"\n' >> "$C/test/ctrl_arms.py"; firmware_guard CTRL_R585_MODE ;;
    mk-spaced-control)
      printf '\nCFLAGS += -DCTRL_R585_MAKE\n' >> "$T/tb/verilator/mbx/Makefile"; firmware_guard CTRL_R585_MAKE ;;
    mk-append-nospace)
      printf '\nCFLAGS+=-DCTRL_R585_MAKE\n' >> "$T/tb/verilator/mbx/Makefile"; firmware_guard CTRL_R585_MAKE ;;
    mk-patsubst)
      printf '\nR585_MODES = CTRL_R585_MAKE\nCFLAGS += $(patsubst %%,-D%%,$(R585_MODES))\n' >> "$T/tb/verilator/mbx/Makefile"; firmware_guard CTRL_R585_MAKE ;;
    unplanted) : ;;
    *) echo "unknown probe $1"; return 1 ;;
  esac
}
for p in "$@"; do
  restore; plant "$p" || continue
  git -C "$T" status --short > "$OUT/$p.diffstat"; git -C "$T" diff > "$OUT/$p.patch"
  for f in $(git -C "$T" ls-files --others --exclude-standard sw tb); do printf '\n+++ new file %s\n' "$f"; cat "$T/$f"; done >> "$OUT/$p.patch"
  python3 -I "$HERE/probe_gate.py" "$T" 12 > "$OUT/$p.log" 2>&1; rc=$?
  echo "$rc" > "$OUT/$p.rc"
  printf '%-26s rc=%s %s\n' "$p" "$rc" "$(grep -m1 -E 'REFUSED|\[FAIL\]|^findings' "$OUT/$p.log" | cut -c1-230)"
done
restore
