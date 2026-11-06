#!/bin/bash
# shape_boots.sh CLONE WORK RECEIPTS: boot, on the split boot simulation's own driver, the images the page's two new
# sentences describe, where the earlier receipts left a gap: a true no-map image at 1x1, and control, stand-in mem.h
# and stand-in csr.h at 8x8. Each runs in a disposable copy; the clone is only read. Needs env.sh sourced.
C=$1; W=$2; R=$3; mkdir -p "$W" "$R"
RV=sw/firmware/ctrl_nvm/test/rv32/generated
standin() { # copy header
  python3 -I - "$1/tb/verilator/ctrl_split_boot/run.py" "$1/$RV/$2" "$2" <<'PY'
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text()
a="    flash_map = budget_build.flash_map(out / 'split-soc/flash-map', shape)\n"
assert s.count(a)==1
p.write_text(s.replace(a,a+f"    shutil.copy({sys.argv[2]!r}, flash_map / 'generated/{sys.argv[3]}')\n"))
PY
}
nomap() { # copy: remove the refusal, and pass no map to either link
  python3 -I - "$1/tb/verilator/ctrl_split_boot/run.py" "$1/sw/firmware/ctrl/test/ctrl_plat_image.py" <<'PY'
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text()
a="         '--flash-map', str(maps.flash_map), '--output', str(out / name), '--libc', str(archives[0]),\n"
assert s.count(a)==1
p.write_text(s.replace(a,"         '--output', str(out / name), '--libc', str(archives[0]),\n"))
q=pathlib.Path(sys.argv[2]); t=q.read_text()
b="        refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n"
assert t.count(b)==1
q.write_text(t.replace(b,""))
PY
}
variant() { # name shape edit [header]
  local d=$W/$1; cp -a --reflink=auto "$C" "$d"
  case $3 in standin) standin "$d" "$4";; nomap) nomap "$d";; none) ;; esac
  ( cd "$d" && date -u +'# start %FT%TZ' && timeout 570 python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$W/$1-build" --shape "$2"; echo "rc=$?"; date -u +'# end %FT%TZ' ) > "$R/$1.log" 2>&1
}
S1=endstation_ax7101_1x1_tdm8; S8=endstation_ax7101_8x8
variant nomap-1x1 $S1 nomap &
variant control-8x8 $S8 none &
variant stand-in-mem-8x8 $S8 standin mem.h &
variant stand-in-csr-8x8 $S8 standin csr.h &
wait
