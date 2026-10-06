#!/usr/bin/env bash
# Disposable probes on the moved table, run in a clone at the head. Each probe
# edits one tracked file, runs the gate that must see it, records the rc, and
# restores the file with `git checkout --`. Usage: move_probes.sh <repo> <outdir>
set -u
repo=$1; out=$2; mkdir -p "$out"; cd "$repo" || exit 2
R=scripts/measure_test_evidence_readers.py
log(){ echo "$1 rc=$2 :: $3" >> "$out/probes.txt"; }
# Q0: dict order and content equal to the pre-move table, by parse.
python3 - > "$out/Q0_order.out" 2>&1 <<'PY'
import ast, subprocess
def tbl(rev, path):
    src = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "DUT_READER_DISPOSITIONS":
            return ast.literal_eval(n.value)
old = tbl("c79c178e7edc427df347787aff6a2cf03adb13ae", "scripts/measure_test_evidence.py")
new = tbl("0f3d37dbffc4ca3f0e0f69499de80fc256a7db57", "scripts/measure_test_evidence_readers.py")
print("entries old/new:", len(old), len(new))
print("same items in same order:", list(old.items()) == list(new.items()))
print("old module still defines a table at head:",
      tbl("0f3d37dbffc4ca3f0e0f69499de80fc256a7db57", "scripts/measure_test_evidence.py") is not None)
PY
log Q0 $? "parse old/new table, compare items and order"
# Q1: drop the first entry from the new module -> an UNEXPLAINED reader.
python3 - <<'PY'
import re, pathlib
p = pathlib.Path("scripts/measure_test_evidence_readers.py"); s = p.read_text()
s2 = re.sub(r'    "protocol-processor/tb/pp_top/acmp_mutants.py":\n(        ".*\n){3}', "", s, count=1)
assert s2 != s; p.write_text(s2)
PY
python3 scripts/measure_test_evidence.py --check > "$out/Q1.out" 2>&1; log Q1 $? "drop acmp_mutants.py entry; expect --check nonzero"
git checkout -- $R
# Q2: add an entry whose reader does not exist -> stale.
python3 - <<'PY'
import pathlib
p = pathlib.Path("scripts/measure_test_evidence_readers.py"); s = p.read_text()
s2 = s.replace("DUT_READER_DISPOSITIONS = {\n", 'DUT_READER_DISPOSITIONS = {\n    "tb/no_such/reader.py": "probe",\n', 1)
assert s2 != s; p.write_text(s2)
PY
python3 scripts/measure_test_evidence.py --check > "$out/Q2.out" 2>&1; log Q2 $? "add stale entry; expect --check nonzero"
git checkout -- $R
# Q3: pad the new module past LONG_MODULE_LINES -> the idiom gate counts it.
python3 -c "import pathlib;p=pathlib.Path('$R');p.write_text(p.read_text()+'\n'.join(['X_%d = %d' % (i, i) for i in range(900)])+'\n')"
python3 scripts/check_py_idiom.py > "$out/Q3.out" 2>&1; log Q3 $? "pad new module to >1000 lines; expect long module 11 > 10"
git checkout -- $R
# Q4: an over-long line in the new module -> the idiom gate counts it.
python3 -c "import pathlib;p=pathlib.Path('$R');p.write_text(p.read_text()+'Y = \"'+'y'*200+'\"\n')"
python3 scripts/check_py_idiom.py > "$out/Q4.out" 2>&1; log Q4 $? "200-char line in new module; expect over-long line > 0"
git checkout -- $R
# Q5: ci_scope classification of the new path, and its selftest.
printf 'scripts/measure_test_evidence_readers.py\n' | python3 scripts/ci_scope.py > "$out/Q5.out" 2>&1; log Q5 $? "ci_scope on the new path; expect true"
python3 scripts/ci_scope.py --selftest > "$out/Q6.out" 2>&1; log Q6 $? "ci_scope --selftest"
