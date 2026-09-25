#!/usr/bin/env bash
# [R319] round-2 disposable probes for PR #118 (issue #77): does tb/pp_top M4L fail
# for the defects it claims to pin? Each probe regenerates ucode.hex from a PATCHED
# COPY of gen_ucode.py taken from a `git archive` extract, then runs the unmodified
# default-build binary produced by `probes.sh base` against it. The clone is never edited.
# Usage: REPO=<clone> BASE=<probes.sh SCRATCH>/base SCRATCH=<dir> OUT=<receipt dir> probes-r2.sh <probe>...
# Probes:
#   ucode-lockcheck   E_NOTIMPL gains CHECK_LOCK: a foreign lock turns the refusal into
#                     ENTITY_LOCKED (status 3). Expect only the two M4L refusal checks red.
#   ucode-dupresp     under a foreign lock only, E_NOTIMPL sends its correct response twice.
#                     Expect only the two M4L "extra AECP frame" checks red.
#   rtl-bench-short-sets-m4
#                     round-1 bench fault `rtl-bench-short-sets`, scoped to the M4 function
#                     body (the unchanged round-1 text replace also edits the new M4L body
#                     and no longer compiles). Needs VERILATOR (default build, own extract).
set -uo pipefail
: "${REPO:?}" "${BASE:?}" "${SCRATCH:?}" "${OUT:?}"
HEAD_SHA=${HEAD_SHA:-490e4309749c83f92d794a8ff10d3043e0f5f080}
mkdir -p "$SCRATCH" "$OUT"

run_bin() {  # $1 = run dir, $2 = log
  ( cd "$1" && rm -f obj_dir/build_tally.txt && ./obj_dir/Vpp_top_sim ) >"$2" 2>&1
  local rc=$?
  echo "exit=$rc" >>"$2"
  printf '%s exit=%s %s\n' "$(basename "$2" .log)" "$rc" \
    "$(grep -Eo '\[build default[^]]*\] [0-9]+ checks, [0-9]+ failures' "$2" | tail -1)"
}

ucode_probe() {  # $1 = name; python edit of gen_ucode.py on stdin
  local x="$SCRATCH/src-$1" d="$SCRATCH/run-$1" log="$OUT/ucode-$1.log"
  rm -rf "$x" "$d"; mkdir -p "$x" "$d/obj_dir"
  git -C "$REPO" archive "$HEAD_SHA" hdl/aecp/ucode | tar -x -C "$x"
  python3 - "$x/hdl/aecp/ucode/gen_ucode.py" >"$log" 2>&1
  ( cd "$x/hdl/aecp/ucode" && python3 gen_ucode.py -o "$d/ucode.hex" ) >>"$log" 2>&1 \
    || { echo "ucode-$1 GENERATION FAILED" | tee -a "$log"; return; }
  cp "$BASE/tb/pp_top/obj_dir/Vpp_top_sim" "$d/obj_dir/"; cp "$BASE/tb/pp_top/ltn_rom.hex" "$d/"
  { echo "reference ROM vs mutant ROM (changed zero-based words):"
    diff <(nl -v0 -ba "$BASE/tb/pp_top/ucode.hex") <(nl -v0 -ba "$d/ucode.hex") | grep '^[<>]'
    sha256sum "$BASE/tb/pp_top/ucode.hex" "$d/ucode.hex" | sed "s#$SCRATCH/##; s#$BASE/##"
  } >>"$log"
  run_bin "$d" "$OUT/ucode-$1.run.log"
  cat "$OUT/ucode-$1.run.log" >>"$log"; rm -f "$OUT/ucode-$1.run.log"
}

build_default() {  # $1 = tree; the same VFLAGS/SRCS as tb/pp_top/Makefile's first build
  ( cd "$1/tb/pp_top" && make -s ltn_rom.hex ucode.hex >/dev/null &&
    printf 'r319-default: ltn_rom.hex ucode.hex\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim\n' |
      make -f Makefile -f - r319-default VERILATOR="${VERILATOR:?}" )
}

rtl_probe() {  # $1 = name; python edit script on stdin, receives the extract root
  local d="$SCRATCH/rtl-$1" log="$OUT/rtl-$1.log"
  rm -rf "$d"; mkdir -p "$d"; git -C "$REPO" archive "$HEAD_SHA" | tar -x -C "$d"
  python3 - "$d" >"$log" 2>&1 || { echo "rtl-$1 PATCH FAILED" | tee -a "$log"; return; }
  if ! build_default "$d" >"$OUT/rtl-$1.build.log" 2>&1; then
    echo "rtl-$1 BUILD FAILED" | tee -a "$log"; return
  fi
  rm -f "$OUT/rtl-$1.build.log"
  run_bin "$d/tb/pp_top" "$OUT/rtl-$1.run.log"
  cat "$OUT/rtl-$1.run.log" >>"$log"; rm -f "$OUT/rtl-$1.run.log"
}

for p in "$@"; do
  case "$p" in
    ucode-lockcheck) ucode_probe lockcheck <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
old = """place(E_NOTIMPL, [
    u('SET_STATUS', imm=ST_NIMPL),"""
new = """place(E_NOTIMPL, [
    u('CHECK_LOCK', ra=15, imm=E_NOTIMPL + 2),   # R319 mutant: foreign lock -> ENTITY_LOCKED
    u('SET_STATUS', imm=ST_NIMPL),"""
assert s.count(old) == 1; p.write_text(s.replace(old, new)); print("patched E_NOTIMPL: CHECK_LOCK prepended")
EOF
      ;;
    ucode-dupresp) ucode_probe dupresp <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
old = """place(E_NOTIMPL, [
    u('SET_STATUS', imm=ST_NIMPL),
    u('BUILD_HDR', ra=15, rb=13),
    u('SEND_RESP'),
    u('END'),
])"""
new = """place(E_NOTIMPL, [
    u('CHECK_LOCK', ra=15, imm=E_NOTIMPL + 6),   # R319 mutant: foreign lock -> duplicate
    u('SET_STATUS', imm=ST_NIMPL),
    u('BUILD_HDR', ra=15, rb=13),
    u('SEND_RESP'),
    u('END'),
    u('END'),
    u('SET_STATUS', imm=ST_NIMPL),               # +6: correct refusal, then a second copy
    u('BUILD_HDR', ra=15, rb=13),
    u('SEND_RESP'),
    u('BUILD_HDR', ra=15, rb=13),
    u('SEND_RESP'),
    u('END'),
])"""
assert s.count(old) == 1; p.write_text(s.replace(old, new)); print("patched E_NOTIMPL: duplicate response under a foreign lock")
EOF
      ;;
    rtl-bench-short-sets-m4) rtl_probe bench-short-sets-m4 <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1], "tb/pp_top/sim_main.cpp"); s = p.read_text()
a = s.index("  void m4_the_waived_pairs_and_a_reserved_command_type() {")
b = s.index("  // ---- M4L:", a)
m4 = s[a:b]
for old, new in [("{0x0001, 16, 28, 60},", "{0x0001,  8, 28, 60},"),
                 ("{0x0003, 80, 92, 118},", "{0x0003,  8, 92, 118},"),
                 ("putbe(&payload[8], 0x0123456789ABCDEFull, 8);",
                  "if (payload.size() >= 16) putbe(&payload[8], 0x0123456789ABCDEFull, 8);"),
                 ("payload[8] = 3;", "if (payload.size() >= 80) { payload[8] = 3;"),
                 ("std::copy(name.begin(), name.end(), payload.begin() + 16); // @40",
                  "std::copy(name.begin(), name.end(), payload.begin() + 16); } // @40")]:
    assert m4.count(old) == 1, old; m4 = m4.replace(old, new); print("patched (M4 only)", old, "->", new)
p.write_text(s[:a] + m4 + s[b:])
EOF
      ;;
    *) echo "unknown probe $p"; exit 2 ;;
  esac
done
