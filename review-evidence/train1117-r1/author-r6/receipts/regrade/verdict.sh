#!/bin/bash
# verdict.sh REV UNIT: RULING-1118b item 2b's test of r4meas/REV at 8x8/1if over every arm, against the candidate's
# tables (clones/r5-candv-8x8-1if, the candidate tip's clone): the survey (every statement), record_classes, the SRP
# record against UNIT, every BUDGET finding, every JOINS line against its range, and the load and THE TRANSMIT's row
# with REV's own over-statement costs restated on a scratch copy of the candidate's tables.
set -u
T=<scratch>; . $T/bin/env.sh
REV=$1 UNIT=$2; O=$T/r4meas/out/$REV; M=$T/r4meas/$REV/8x8-1if
echo "# verdict of $REV at 8x8/1if, unit $UNIT us, $(date +%T)"
for k in none aep ap vd; do n=$(python3 -c "import json;print(len(json.load(open('$M/$k/parts.json'))['parts']))" 2>/dev/null); echo "leg $k: $(ls $M/$k/part*/results.json 2>/dev/null | wc -l) of $n parts done"; done
POINTS=8x8-1if CLONES=$T/clones/r5-candv bash $T/r4meas/analyse.sh $REV > /dev/null 2>&1
echo "== survey (the candidate's statements)"; tail -3 $O/survey-8x8-1if.out | cut -c1-220
grep -h 'OVER' $O/survey-8x8-1if/compare-ordinary.txt | sort -u | cut -c1-200
echo "== record classes"; grep -h 'held\|REFUSED' $O/record-classes-8x8-1if.txt | cut -c1-200
echo "== the SRP record against its unit"
python3 - "$M" "$UNIT" <<'PY'
import glob, math, sys
m, unit = sys.argv[1], int(sys.argv[2]); most, at = 0, '-'
for f in glob.glob(f'{m}/*/part*/*.log'):
    for line in open(f, errors='replace'):
        if line.startswith('SPAN ') and line.rstrip().endswith(' srp_mbx:receive'):
            c = int(line.split()[3])
            if c > most: most, at = c, f.split('/8x8-1if/')[-1]
rule = int(math.ceil(most * 1.05 / 100 / 5 - 1e-9) * 5)
print(f'record.srp {most:,} cycles ({at}), {rule} us by the rule, unit {unit}: {"WITHIN" if rule <= unit else "OVER"}; '
      f'margin {math.floor(unit * 100 / 1.05) - most:+,} cycles')
PY
echo "== budget misses (BUDGET findings); the backlog-owed group's seven egress-hold rows (backlog.owed*, backlog-owed.*) are the scenario's 60 ms hold, ledgered (README: they miss at every point; egress_ledger.py)"
echo "egress-hold rows: $(grep -h '^BUDGET' $M/*.part*.log | grep -cE '^BUDGET backlog(\.owed|-owed\.)')"
echo "any other: $(grep -h '^BUDGET' $M/*.part*.log | grep -cvE '^BUDGET backlog(\.owed|-owed\.)')"
grep -h '^BUDGET' $M/*.part*.log | grep -vE '^BUDGET backlog(\.owed|-owed\.)' | head -5 | cut -c1-200
echo "== join intervals"
python3 - "$M" <<'PY'
import glob, re, sys
lo_all, hi_all, bad, n = 1e9, 0, [], 0
for f in glob.glob(f'{sys.argv[1]}/*.part*.log'):
    for line in open(f, errors='replace'):
        m = re.match(r'JOINS (\S+): (\d+) join interval\(s\), the shortest ([\d.]+) ms and the longest ([\d.]+) ms, against ([\d.]+) to ([\d.]+)', line)
        if not m: continue
        n += 1; lo, hi, a, b = float(m[3]), float(m[4]), float(m[5]), float(m[6])
        lo_all, hi_all = min(lo_all, lo), max(hi_all, hi)
        if lo < a or hi > b: bad.append(line.strip()[:160])
print(f'{n} JOINS line(s); shortest {lo_all} ms, longest {hi_all} ms; out of range: {len(bad)}')
for b in bad[:5]: print('  ', b)
PY
echo "== the load and THE TRANSMIT with $REV's own restated costs (scratch copy of the candidate's tables)"
python3 -I $T/r5re/spec_from_survey.py $O $O/spec-8x8-1if.json | grep '8x8/1if' || echo "no 8x8/1if statement to restate"
W=$T/clones/r5-whatif-cand; [ -d $W ] || $T/bin/clone.sh $(git -C $T/clones/r5-cand2 rev-parse HEAD) $W > /dev/null
git -C $W checkout -q -- . && git -C $W checkout -q --detach $(git -C $T/clones/r5-cand2 rev-parse HEAD)
python3 - $O/spec-8x8-1if.json <<'PY'
import json, sys
spec = [e for e in json.load(open(sys.argv[1])) if e['point'] == '8x8/1if']
json.dump(spec, open(sys.argv[1] + '.81', 'w'))
PY
python3 -I $T/r5re/commit_restate.py $W $O/spec-8x8-1if.json.81 2>&1 | tail -1
(cd $W && python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check 2>&1 | tail -1; \
 python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if 2>&1 | grep -E '^\| 8x8/1if \| 0\.|^HELD|^OVER|^RESULT' | cut -c1-200)
git -C $W checkout -q -- .
