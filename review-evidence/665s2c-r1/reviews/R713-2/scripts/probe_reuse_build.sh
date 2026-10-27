#!/usr/bin/env bash
# Disposable source mutants against the S2c harness's build/reuse identity checks.
# Usage: probe_reuse_build.sh <clone at exact head> <scratch dir> <receipt dir>
# Each mutant runs on its own `git archive` copy; the self-test must report >0 failures (killed).
set -u
SRC=$1; SCR=$2; OUT=$3
mkdir -p "$SCR" "$OUT"
H=tb/verilator/ctrl_service_budget
declare -A MUT=(
  [m1_builtas_default_split]="$H/run.py|spec.get('fetch_l1', 'none')|spec.get('fetch_l1', 'split')"
  [m2_selected_drops_xip]="$H/run.py|args.variant, args.fetch_l1, args.xip|args.variant, args.fetch_l1, False"
  [m3_build_drops_xip]="$H/run.py|core=builder.Core(args.cpu_regions, args.fetch_l1, args.xip)|core=builder.Core(args.cpu_regions, args.fetch_l1, False)"
  [m4_soc_gets_split]="$H/build.py|n_if, core.cpu_regions, core.fetch_l1)|n_if, core.cpu_regions, 'split')"
  [m5_refusal_off]="$H/run.py|if built_as(spec) != selected(args, shape, n_if):|if False:"
  [m6_builtas_drops_xip]="$H/run.py|spec.get('fetch_l1', 'none'), spec.get('xip', False))|spec.get('fetch_l1', 'none'), False)"
  [m7_record_xip_false]="$H/build.py|spec['xip'] = core.xip|spec['xip'] = False"
  [m8_selected_drops_fetch]="$H/run.py|args.variant, args.fetch_l1, args.xip|args.variant, 'none', args.xip"
)
run_one() {
  name=$1; IFS='|' read -r file old new <<<"${MUT[$name]}"
  d=$SCR/$name; rm -rf "$d"; mkdir -p "$d"
  git -C "$SRC" archive HEAD | tar -x -C "$d"
  python3 - "$d/$file" "$old" "$new" <<'PY'
import sys; p,o,n=sys.argv[1:]; s=open(p).read(); c=s.count(o)
assert c==1, (p,o,c); open(p,'w').write(s.replace(o,n))
PY
  [ $? -eq 0 ] || { echo "$name APPLY-FAILED" > "$OUT/$name.verdict"; return; }
  (cd "$d" && python3 -B $H/run.py --self-test > "$OUT/$name.log" 2>&1); rc=$?
  fails=$(grep -c '^FAIL' "$OUT/$name.log")
  if [ $rc -ne 0 ] || [ "$fails" -gt 0 ]; then v=KILLED; else v=SURVIVED; fi
  echo "$name rc=$rc fail_lines=$fails $v" > "$OUT/$name.verdict"
}
for n in "${!MUT[@]}"; do run_one "$n" & done; wait
cat "$OUT"/*.verdict | sort
