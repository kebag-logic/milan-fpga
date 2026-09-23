#!/usr/bin/env bash
# CLI edge probes for syn/yosys/result_cache.py rom-digest / --rom-sha256.
# usage: cli_edge_probe.sh TREE WORK     (TREE: disposable exact-head copy)
set -uo pipefail
tree="$1"; work="$2"
rc_py="$tree/syn/yosys/result_cache.py"
mkdir -p "$work"
d="$work/roms"; rm -rf "$d"; mkdir -p "$d"
printf '01\n' > "$d/gptp_ucode.hex"; printf '02\n' > "$d/ltn_rom.hex"; printf '03\n' > "$d/ucode.hex"
probe() { # label, expected exit, command...
  local label="$1" want="$2"; shift 2
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  printf '%-44s exit=%s want=%s %s | %s\n' "$label" "$rc" "$want" \
    "$([ "$rc" = "$want" ] && echo OK || echo MISMATCH)" "$(printf '%s' "$out" | head -1 | cut -c1-110)"
}
base="$(python3 "$rc_py" rom-digest --rom-dir "$d")"
probe "baseline digest" 0 python3 "$rc_py" rom-digest --rom-dir "$d"
probe "repeat digest identical" 0 test "$(python3 "$rc_py" rom-digest --rom-dir "$d")" = "$base"
touch -d '2001-01-01' "$d/ucode.hex"
probe "mtime change keeps digest" 0 test "$(python3 "$rc_py" rom-digest --rom-dir "$d")" = "$base"
cp -a "$d" "$work/roms-moved"
probe "different directory path keeps digest" 0 test "$(python3 "$rc_py" rom-digest --rom-dir "$work/roms-moved")" = "$base"
mv "$d/ucode.hex" "$work/ucode.real"; ln -s "$work/ucode.real" "$d/ucode.hex"
probe "symlinked image digests its target bytes" 0 test "$(python3 "$rc_py" rom-digest --rom-dir "$d")" = "$base"
rm "$d/ucode.hex"; mkdir "$d/ucode.hex"
probe "directory in place of image refused" 2 python3 "$rc_py" rom-digest --rom-dir "$d"
rmdir "$d/ucode.hex"; printf '03' > "$d/ucode.hex"
probe "trailing-newline-only change moves digest" 0 test "$(python3 "$rc_py" rom-digest --rom-dir "$d")" != "$base"
printf '03\n' > "$d/ucode.hex"
probe "absent rom dir refused" 2 python3 "$rc_py" rom-digest --rom-dir "$work/nope"
printf 'module T; endmodule\n' > "$work/T.v"
common=(--top T --mode full --sv2v-file "$work/T.v" --program p --yosys-version Y --yosys-bin-sha256 B --sv2v-version S)
probe "key with valid digest" 0 python3 "$rc_py" key "${common[@]}" --rom-sha256 "$base"
probe "key with empty digest refused" 2 python3 "$rc_py" key "${common[@]}" --rom-sha256 ""
probe "key with uppercase digest refused" 2 python3 "$rc_py" key "${common[@]}" --rom-sha256 "$(printf '%s' "$base" | tr a-f A-F)"
probe "key without --rom-sha256 refused" 2 python3 "$rc_py" key "${common[@]}"
probe "lookup without --rom-sha256 refused" 2 python3 "$rc_py" lookup --dir "$work/c" "${common[@]}"
k1="$(python3 "$rc_py" key "${common[@]}" --rom-sha256 "$base")"
k2="$(python3 "$rc_py" key "${common[@]}" --rom-sha256 "$(printf '%064d' 0)")"
probe "key moves with digest" 0 test "$k1" != "$k2"
