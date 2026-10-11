#!/usr/bin/env bash
# Scratch: each form a builder writes a mode in, planted into a REAL builder that runs, then judged end to end.
# The Makefile forms go into the mailbox bench's firmware library recipe (obj_fw/libctrlfw.a, which needs no
# Verilator), run under its own capture beside the given one; the Python forms go into ctrl_image.py's
# IMAGE_FLAGS, which the boundary runs itself under its capture. A compiler a recipe names by its path is a
# bypass the boundary reads from make's dry run. Each plant also gives the firmware's ADP adapter an include of
# a stack example's header under CTRL_R5_PROBE.
# usage: real_probes.sh <clean clone of the head> <capture of the hosted job's firmware steps> <out> [probe...]
set -u
T=$(cd "$1" && pwd); CAP=$(cd "$2" && pwd); mkdir -p "$3"; OUT=$(cd "$3" && pwd); shift 3
C=$T/sw/firmware/ctrl
MK=$T/tb/verilator/mbx/Makefile
IMG=$C/test/ctrl_image.py
RECIPE='cd obj_fw && $(CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic $(FW_INC) -c $(FW_SRC)'
restore() { git -C "$T" checkout -q -- . && git -C "$T" clean -qfdx -- tb/verilator/mbx >/dev/null; }
guard() {
  python3 - "$C/adp/adp_mbx.c" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
old = '#include "adp_mbx.h"\n'
assert t.count(old) == 1
open(p, "w").write(t.replace(old, old + '#ifdef CTRL_R5_PROBE\n#include "../../../../third_party/tsn-c-stack/examples/adp_port.h"\n#endif\n'))
EOF
}
recipe() {  # replace the firmware library's compile with $2, after defining $1
  python3 - "$MK" "$RECIPE" "$2" "$1" <<'EOF'
import sys
p, old, new, head = sys.argv[1:]
t = open(p).read()
assert t.count(old) == 1
t = t.replace(old, new)
if head:
    t = t.replace("CC     ?= cc\n", "CC     ?= cc\n" + head.replace("\\n", "\n") + "\n")
open(p, "w").write(t)
EOF
}
image() {  # append $1 to ctrl_image.py's IMAGE_FLAGS
  python3 - "$IMG" "$1" <<'EOF'
import sys
p, extra = sys.argv[1:]
t = open(p).read()
old = 'IMAGE_FLAGS = ("-DNDEBUG", "-ffunction-sections", "-fdata-sections", "-fno-pic", "-fno-pie")\n'
assert t.count(old) == 1
open(p, "w").write(t.replace(old, old.rstrip("\n") + " + " + extra + "\n"))
EOF
}
plant() {
  case "$1" in
    unplanted) : ;;
    mk-patsubst) guard; recipe 'R5_MODES := CTRL_R5_PROBE' "${RECIPE/\$(CC)/\$(CC) \$(patsubst %,-D%,\$(R5_MODES))}" ;;
    mk-foreach) guard; recipe '' "${RECIPE/\$(CC)/\$(CC) \$(foreach m,CTRL_R5_PROBE,-D\$(m))}" ;;
    mk-append-nospace) guard; recipe 'R5_CFLAGS+=-DCTRL_R5_PROBE' "${RECIPE/\$(CC)/\$(CC) \$(R5_CFLAGS)}" ;;
    mk-addprefix) guard; recipe '' "${RECIPE/\$(CC)/\$(CC) \$(addprefix -D,CTRL_R5_PROBE)}" ;;
    mk-compiler-path) recipe '' "${RECIPE/\$(CC)/$(command -v gcc)}" ;;
    py-split) guard; image 'tuple("-Os -DCTRL_R5_PROBE".split())' ;;
    py-fstring-mid) guard; image "tuple(f\"{'-Os'} -DCTRL_R5_PROBE\".split())" ;;
    py-format) guard; image '("-D{}".format("CTRL_R5_PROBE"),)' ;;
    py-join) guard; image '("-D" + "CTRL_R5_PROBE",)' ;;
    *) echo "unknown probe $1"; return 1 ;;
  esac
}
for p in "$@"; do
  restore; plant "$p" || continue
  git -C "$T" diff > "$OUT/$p.patch"
  extra=()
  case "$p" in
    mk-*) rm -rf "$OUT/$p.capture"
          (cd "$T" && python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$OUT/$p.capture" -- make -C tb/verilator/mbx obj_fw/libctrlfw.a > "$OUT/$p.make.log" 2>&1)
          echo "make rc=$?" >> "$OUT/$p.make.log"
          # a recipe that names its compiler by a path compiles nothing the wrappers record: its own capture is
          # empty, and the boundary must refuse the path it reads from make's dry run of the checkout's bench
          [ "$p" = mk-compiler-path ] || extra=(--capture "$OUT/$p.capture") ;;
  esac
  (cd "$T" && python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --capture "$CAP" "${extra[@]}" --without verilator) > "$OUT/$p.log" 2>&1
  rc=$?; echo "$rc" > "$OUT/$p.rc"
  printf '%-20s rc=%s %s\n' "$p" "$rc" "$(grep -m1 -E 'REFUSED|\[FAIL\]|ctrl_boundary: PASS' "$OUT/$p.log" | cut -c1-260)"
done
restore
