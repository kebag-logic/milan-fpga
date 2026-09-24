#!/bin/sh
# Disposable probe: do MVU command_types 0x0001, 0x0003 and 0x0004 (Milan v1.2
# Table 5.18) receive the byte-exact MVU NOT_IMPLEMENTED echo at the pinned
# protocol processor, as FR-MVU-02 and compliance-matrix row 1.4 state?
#
# Usage: probe_pp_mvu_fallback.sh <parent-clone> <scratch-dir> <verilator> <stage>
#   stage = extract | gen | build | run   (build is incremental and re-runnable)
#
# extract: exports the pinned protocol-processor tree with `git archive` (exact
#          pinned bytes, no working-tree edits), then applies the probe patch
#          to the SCRATCH copy of tb/pp_top/sim_main.cpp only, and caps the
#          Verilator build at 8 jobs in the scratch Makefile.
# Nothing in <parent-clone> is written.
set -eu
clone=$1; scratch=$2; vl=$3; stage=$4
pp="$scratch/pp_probe"
tb="$pp/tb/pp_top"
here=$(cd "$(dirname "$0")" && pwd)

case "$stage" in
extract)
  rm -rf "$pp"; mkdir -p "$pp"
  pin=$(git -C "$clone" ls-files -s protocol-processor | awk '{print $2}')
  echo "pinned gitlink: $pin"
  echo "checkout HEAD:  $(git -C "$clone/protocol-processor" rev-parse HEAD)"
  git -C "$clone/protocol-processor" archive "$pin" | tar -x -C "$pp"
  echo "sim_main.cpp sha256 before patch: $(sha256sum "$tb/sim_main.cpp" | cut -d' ' -f1)"
  echo "pinned blob sha1 of sim_main.cpp: $(git -C "$clone/protocol-processor" rev-parse "$pin:tb/pp_top/sim_main.cpp")"
  echo "scratch copy git hash-object:     $(git hash-object "$tb/sim_main.cpp")"
  python3 -B "$here/patch_pp_mvu_probe.py" "$tb/sim_main.cpp"
  sed -i 's/--build -j 0/--build -j 8/' "$tb/Makefile"
  grep -n -- '--build -j' "$tb/Makefile"
  ;;
gen)
  # hex images, then the Verilator C++ (no C++ compile yet)
  make -C "$tb" ltn_rom.hex ucode.hex
  cd "$tb"
  srcs=$(make -s -f Makefile -f - print-srcs <<'EOF'
print-srcs:
	@echo $(SRCS) $(CPP)
EOF
)
  "$vl" --cc --exe -j 8 --top-module pp_top_wrap \
    -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
    -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
    -CFLAGS "-std=c++17 -O2 -I$(pwd) -Wall -Wextra" \
    $srcs -o Vpp_top_sim > "$scratch/pp_probe_verilate.log" 2>&1
  echo "verilate exit 0; warnings: $(grep -c '%Warning' "$scratch/pp_probe_verilate.log" || true)"
  ;;
build)
  make -C "$tb/obj_dir" -f Vpp_top_wrap.mk -j 8 Vpp_top_sim > "$scratch/pp_probe_build.log" 2>&1
  echo "build exit 0"
  ;;
run)
  cd "$tb"
  ./obj_dir/Vpp_top_sim
  ;;
*) echo "unknown stage $stage" >&2; exit 2 ;;
esac
