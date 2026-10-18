#!/usr/bin/env bash
# Independent re-run of the R650-2 controls drop_keeps_flags and
# held_no_rearm at an exact head, outside the repository's own arm.
# Both are generator-only defects, so one engine build serves every image.
# Usage: probe_r650_2_mutants.sh <clone> <work-dir> <verilator> <head>
# Writes <work-dir>/<variant>-{default,p1}.{log,rc} for variant in
# clean, drop_keeps_flags, held_no_rearm.
set -euo pipefail
clone=$1; work=$2; vl=$3; head=$4
test "$(git -C "$clone" rev-parse HEAD)" = "$head"
rm -rf "$work"; mkdir -p "$work/src"
git -C "$clone" archive "$head" | tar -x -C "$work/src"
eng=$work/src/tb/verilator/engine
gen=hdl/ucode/gen_gptp_ucode.py
genargs=(--clk-hz 2000000 --cease-ms 3000)
# build exactly as the Makefile's run recipe does (its first --cc line)
(cd "$eng" && make -n run VERILATOR="$vl" | grep -m1 -e '--cc' | sh) \
  >"$work/build.log" 2>&1
test -x "$eng/obj_dir/Vengine_sim"
exe=$eng/obj_dir/Vengine_sim
mutate() {  # variant -> mutated copy of the generator on stdout path
  local v=$1 d=$work/gen-$1
  mkdir -p "$d"; cp -r "$work/src/hdl" "$d/"
  python3 - "$d/$gen" "$v" <<'EOF'
import sys
path, v = sys.argv[1], sys.argv[2]
s = open(path, encoding="utf-8").read()
if v == "drop_keeps_flags":
    # delete only the BECGATE drop's flags write before BR SELF
    old = ('    p.emit("WRST", ra=0, imm=RG_PUB | 2, fmt=FMT_Q)\n'
           '    p.emit("BR", label=LB["SELF"])\n')
    new = '    p.emit("BR", label=LB["SELF"])\n'
elif v == "held_no_rearm":
    # delete the BECGATE incapable-branch re-arm of the receipt watch
    old = ('    p.emit("MOVE", rd=RU, ra=0, imm=3000)\n'
           '    p.emit("WRST", ra=RU, imm=RG_TMR | 2, fmt=FMT_Q)'
           '  # keep watching\n')
    new = ''
else:
    sys.exit(0)
assert s.count(old) == 1, (v, s.count(old))
open(path, "w", encoding="utf-8").write(s.replace(old, new))
EOF
  echo "$d/$gen"
}
pids=()
for v in clean drop_keeps_flags held_no_rearm; do
  g=$(mutate "$v")
  for pass in default p1; do
    r=$work/run-$v-$pass; mkdir -p "$r"
    if [ "$pass" = p1 ]; then
      python3 "$g" "${genargs[@]}" --p1 255 -o "$r/gptp_ucode.hex" >/dev/null
      arg=+not-gm-capable
    else
      python3 "$g" "${genargs[@]}" -o "$r/gptp_ucode.hex" >/dev/null
      arg=
    fi
    ( cd "$r" && set +e; "$exe" $arg >"$work/$v-$pass.log" 2>&1
      echo $? >"$work/$v-$pass.rc" ) &
    pids+=($!)
  done
done
for p in "${pids[@]}"; do wait "$p"; done
for v in clean drop_keeps_flags held_no_rearm; do
  for pass in default p1; do
    printf '%-17s %-7s rc=%s  %s\n' "$v" "$pass" "$(cat "$work/$v-$pass.rc")" \
      "$(grep -E '^[0-9]+ checks:' "$work/$v-$pass.log" | tail -1)"
    grep -E '^FAIL ' "$work/$v-$pass.log" | sed 's/^/    /' || true
  done
done
