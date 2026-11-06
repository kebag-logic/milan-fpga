#!/bin/bash
# partial_boot.sh CLONE WORK RECEIPTS: boot, on the split boot simulation's own driver, the image a map lacking one
# header gave before round 8. Each copy puts the stand-in where the generated header was, which is what the compiler
# found behind a missing one, so this measures what the page says such an image does. The unedited copy is the control.
C=$1; W=$2; R=$3
RV=sw/firmware/ctrl_nvm/test/rv32/generated
variant() { # name header-or-none
  local d=$W/$1; cp -a --reflink=auto "$C" "$d"
  if [ "$2" != none ]; then
    python3 -I - "$d/tb/verilator/ctrl_split_boot/run.py" "$d/$RV/$2" "$2" <<'EOF'
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text()
a="    flash_map = budget_build.flash_map(out / 'split-soc/flash-map', shape)\n"
assert s.count(a)==1
p.write_text(s.replace(a,a+f"    shutil.copy({sys.argv[2]!r}, flash_map / 'generated/{sys.argv[3]}')\n"))
EOF
  fi
  ( cd "$d" && date -u +'# start %FT%TZ' && timeout 540 python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$W/$1-build"; echo "rc=$?"; date -u +'# end %FT%TZ' ) > "$R/$1.log" 2>&1
}
variant control none & variant stand-in-mem mem.h & variant stand-in-csr csr.h &
wait
