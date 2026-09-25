#!/usr/bin/env bash
# [R319] disposable mutation / fault probes for PR #118 (issue #77) at exact head.
# Each probe runs in its own `git archive` extract under $SCRATCH; the clone is never edited.
# Usage: REPO=<clone> VERILATOR=<verilator 5.050> SCRATCH=<dir> OUT=<receipt dir> probes.sh <probe>...
# Probes:
#   base        build + run the default pp_top build at exact head (reference binary)
#   rom-<name>  ROM swap on the reference binary (needs `base` first)
#   rtl-<name>  patched RTL / bench, default build only, run
set -uo pipefail
: "${REPO:?}" "${VERILATOR:?}" "${SCRATCH:?}" "${OUT:?}"
HEAD_SHA=b51bc3893b06f4d39be49726c1b8f4ed6c65573d
mkdir -p "$SCRATCH" "$OUT"

extract() {  # $1 = dir
  rm -rf "$1"; mkdir -p "$1"
  git -C "$REPO" archive "$HEAD_SHA" | tar -x -C "$1"
}

# default build only: the same VFLAGS/SRCS as tb/pp_top/Makefile's first build
build_default() {  # $1 = tree
  ( cd "$1/tb/pp_top" && make -s ltn_rom.hex ucode.hex >/dev/null &&
    printf 'r319-default: ltn_rom.hex ucode.hex\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim\n' |
      make -f Makefile -f - r319-default VERILATOR="$VERILATOR" )
}

run_bin() {  # $1 = tb/pp_top dir, $2 = log
  ( cd "$1" && rm -f obj_dir/build_tally.txt && ./obj_dir/Vpp_top_sim ) >"$2" 2>&1
  local rc=$?
  echo "exit=$rc" >>"$2"
  printf '%s exit=%s %s\n' "$(basename "$2" .log)" "$rc" \
    "$(grep -Eo '\[build default[^]]*\] [0-9]+ checks, [0-9]+ failures' "$2" | tail -1)"
}

rom_word() {  # $1 = hex file, $2 = zero-based word, $3 = new value
  python3 - "$1" "$2" "$3" <<'EOF'
import sys
f, w, v = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lines = open(f).read().split('\n')
print(f"word {w}: {lines[w]} -> {v}")
lines[w] = v
open(f, 'w').write('\n'.join(lines))
EOF
}

rom_probe() {  # $1 = name, $2 = word, $3 = value
  local ref="$SCRATCH/base/tb/pp_top" d="$SCRATCH/rom-$1"
  rm -rf "$d"; mkdir -p "$d/obj_dir"
  cp "$ref/obj_dir/Vpp_top_sim" "$d/obj_dir/"; cp "$ref/ltn_rom.hex" "$ref/ucode.hex" "$d/"
  rom_word "$d/ucode.hex" "$2" "$3" >"$OUT/rom-$1.log"
  sha256sum "$ref/ucode.hex" "$d/ucode.hex" | sed "s#$SCRATCH/##" >>"$OUT/rom-$1.log"
  run_bin "$d" "$OUT/rom-$1.run.log"
  cat "$OUT/rom-$1.run.log" >>"$OUT/rom-$1.log"; rm -f "$OUT/rom-$1.run.log"
}

rtl_probe() {  # $1 = name, $2 = python edit script (file, old, new triples on stdin)
  local d="$SCRATCH/rtl-$1"
  extract "$d"
  python3 - "$d" >"$OUT/rtl-$1.log" 2>&1
  if ! build_default "$d" >>"$OUT/rtl-$1.build.log" 2>&1; then
    echo "rtl-$1 BUILD FAILED" | tee -a "$OUT/rtl-$1.log"; return
  fi
  run_bin "$d/tb/pp_top" "$OUT/rtl-$1.run.log"
  cat "$OUT/rtl-$1.run.log" >>"$OUT/rtl-$1.log"; rm -f "$OUT/rtl-$1.run.log" "$OUT/rtl-$1.build.log"
}

for p in "$@"; do
  case "$p" in
    base)
      extract "$SCRATCH/base"
      build_default "$SCRATCH/base" >"$OUT/base.build.log" 2>&1 || { echo "base BUILD FAILED"; exit 1; }
      rm -f "$OUT/base.build.log"
      run_bin "$SCRATCH/base/tb/pp_top" "$OUT/base.log" ;;
    # generated ROM (zero-based words; checked against the extract's ucode.hex in the log)
    rom-notimpl-success) rom_probe notimpl-success 560 c00000000000 ;;  # E_NOTIMPL SET_STATUS -> SUCCESS
    rom-features-3)      rom_probe features-3      741 230000000003 ;;  # both Table 5.20 flags
    rom-features-1)      rom_probe features-1      741 230000000001 ;;  # REDUNDANCY only
    rom-features-2)      rom_probe features-2      741 230000000002 ;;  # TALKER_DYNAMIC_MAPPINGS only
    # RTL: the MVU sub-decode serves GET_MILAN_INFO for every command_type 0x0000..0x0007
    rtl-mvu-range) rtl_probe mvu-range <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1], "hdl/aecp/KL_aecp_engine.sv"); s = p.read_text()
old = "&& (desc_ty_r  == MVU_GET_MILAN_INFO_C);"
new = "&& (desc_ty_r[15:3] == 13'd0);"
assert s.count(old) == 1; p.write_text(s.replace(old, new)); print("patched", old, "->", new)
EOF
      ;;
    # RTL: only SET_MEDIA_CLOCK_REFERENCE_INFO (the 104-byte form) is answered SUCCESS
    rtl-mvu-0003) rtl_probe mvu-0003 <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1], "hdl/aecp/KL_aecp_engine.sv"); s = p.read_text()
old = "&& (desc_ty_r  == MVU_GET_MILAN_INFO_C);"
new = "&& ((desc_ty_r == MVU_GET_MILAN_INFO_C) || (desc_ty_r == 16'h0003));"
assert s.count(old) == 1; p.write_text(s.replace(old, new)); print("patched", old, "->", new)
EOF
      ;;
    # bench-only fault probe: M4's command_type loop skips nothing, but a bench that sent
    # the SHORT form for the SETs must still be noticed by the length/cdl columns
    rtl-bench-short-sets) rtl_probe bench-short-sets <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1], "tb/pp_top/sim_main.cpp"); s = p.read_text()
for old, new in [("{0x0001, 16, 28, 60},", "{0x0001,  8, 28, 60},"),
                 ("{0x0003, 80, 92, 118},", "{0x0003,  8, 92, 118},")]:
    assert s.count(old) == 1; s = s.replace(old, new); print("patched", old, "->", new)
s = s.replace("putbe(&payload[8], 0x0123456789ABCDEFull, 8);", "if (payload.size() >= 16) putbe(&payload[8], 0x0123456789ABCDEFull, 8);")
s = s.replace("payload[8] = 3;", "if (payload.size() >= 80) { payload[8] = 3;")
s = s.replace("std::copy(name.begin(), name.end(), payload.begin() + 16); // @40", "std::copy(name.begin(), name.end(), payload.begin() + 16); } // @40")
p.write_text(s)
EOF
      ;;
    # robustness probe (additive bench code only): under a LOCK held by controller 1, the
    # waived SETs from controller 2 still take the NOT_IMPLEMENTED echo (06 section 6.8 claim)
    rtl-lock-probe) rtl_probe lock-probe <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1], "tb/pp_top/sim_main.cpp"); s = p.read_text()
anchor = "    m5_the_r_field_is_compared_the_reserved_field_is_not(info_pl);\n"
probe = r'''    {  // R319 lock probe
      const uint64_t C2_MAC = 0x0202C2C2C2C2ull;
      std::vector<uint8_t> lock(16, 0);
      h.q_aecp.clear();
      h.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, 0xC0E0, 0x0001, lock));
      auto lk = h.wait_any(h.q_aecp, 200);
      CHECK(lk.size() > 17 && (lk[16] >> 3) == AECP_SUCCESS, "R319-LOCK: lock not taken");
      for (uint16_t ct : {uint16_t(0x0001), uint16_t(0x0003)}) {
        auto pl = mvu_cmd_pl(MVU_PID_LO, ct, ct == 1 ? 16 : 80);
        pl[8] = 1;
        const uint16_t seq = uint16_t(0xC0E0 + ct);
        h.q_aecp.clear();
        h.feed(aecp_frame(OWN_MAC, C2_MAC, VU_COMMAND, 0, EID, CTLR2_EID, seq, MVU_PID_HI, pl));
        auto got = h.wait_any(h.q_aecp, 200);
        auto want = aecp_frame(C2_MAC, OWN_MAC, VU_RESPONSE, AECP_NOT_IMPLEMENTED, EID, CTLR2_EID, seq, MVU_PID_HI, pl);
        CHECK(got == want, "R319-LOCK: foreign MVU 0x%04x under lock is not the NOT_IMPLEMENTED echo (status %u)",
              ct, got.size() > 16 ? unsigned(got[16] >> 3) : 99u);
      }
      lock[3] = 1;
      h.q_aecp.clear();
      h.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID, CTLR_EID, 0xC0EF, 0x0001, lock));
      lk = h.wait_any(h.q_aecp, 200);
      CHECK(lk.size() > 17 && (lk[16] >> 3) == AECP_SUCCESS, "R319-LOCK: unlock failed");
      std::printf("R319-LOCK probe ran\n");
    }
'''
assert s.count(anchor) == 1; s = s.replace(anchor, probe + anchor); p.write_text(s); print("inserted lock probe before M5")
EOF
      ;;
    *) echo "unknown probe $p"; exit 2 ;;
  esac
done
