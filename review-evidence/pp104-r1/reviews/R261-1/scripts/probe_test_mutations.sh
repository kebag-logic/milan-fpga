#!/bin/sh
# Mutation probes for tb/pp_top/test_fixture_guards.py at the PR head.
# Usage: probe_test_mutations.sh <extracted-head-tree> <scratch-dir>
# Each arm copies the two pp_top Python files into its own scratch directory,
# applies ONE literal replacement to fixture_guards.py (refusing unless the
# target occurs exactly once), and runs the unit test there. The control arm
# must pass; every mutant must fail, because each breaks a property the new
# test docstring says the test requires.
set -u
HEAD_TREE=$1
SCRATCH=$2
PASSES=0
FAILS=0

arm() {
    id=$1; expect=$2; old=$3; new=$4; claim=$5
    d="$SCRATCH/$id"
    mkdir -p "$d"
    cp "$HEAD_TREE/tb/pp_top/fixture_guards.py" "$HEAD_TREE/tb/pp_top/test_fixture_guards.py" "$d/"
    if [ -n "$old" ]; then
        python3 - "$d/fixture_guards.py" "$old" "$new" <<'EOF' || { echo "$id: PROBE SETUP ERROR"; FAILS=$((FAILS+1)); return; }
import sys
from pathlib import Path
p, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
text = p.read_text()
if text.count(old) != 1:
    sys.exit(f"target occurs {text.count(old)} times")
p.write_text(text.replace(old, new))
EOF
    fi
    out=$(cd "$d" && python3 -B -m unittest test_fixture_guards.py 2>&1)
    rc=$?
    summary=$(printf '%s\n' "$out" | grep -E '^(OK|FAILED)' | tail -1)
    if { [ "$expect" = pass ] && [ $rc -eq 0 ]; } || { [ "$expect" = fail ] && [ $rc -ne 0 ]; }; then
        verdict=AS-EXPECTED; PASSES=$((PASSES+1))
    else
        verdict=UNEXPECTED; FAILS=$((FAILS+1))
    fi
    echo "$id expect=$expect rc=$rc [$summary] $verdict -- $claim"
}

arm M0-control pass "" "" "unmodified head passes"
arm M1-no-lc-all fail '        compiler_env["LC_ALL"] = "C"
' '' "sets LC_ALL=C for the compiler"
arm M2-lc-all-if-unset fail 'compiler_env["LC_ALL"] = "C"' 'compiler_env.setdefault("LC_ALL", "C")' "LC_ALL=C also when LC_ALL is inherited"
arm M3-env-to-model fail '[args.verilator, *vflags, "--Mdir", tmp], check=True' '[args.verilator, *vflags, "--Mdir", tmp], check=True, env={**os.environ, "LC_ALL": "C"}' "LC_ALL=C for the compiler ONLY (not model generation)"
arm M4-env-to-root-query fail '"VERILATOR_ROOT"], text=True' '"VERILATOR_ROOT"], text=True, env={**os.environ, "LC_ALL": "C"}' "LC_ALL=C for the compiler ONLY (not the root query)"
arm M5-mutate-caller-env fail 'compiler_env = os.environ.copy()' 'compiler_env = os.environ' "caller environment unchanged"
arm M6-drop-caller-env fail 'compiler_env = os.environ.copy()' 'compiler_env = {}' "compiler gets the caller environment plus LC_ALL=C"
arm M7-no-shlex fail '*shlex.split(args.cxx),' 'args.cxx,' "passes every argument through (--cxx split)"
arm M8-keep-dashdash fail '        vflags = vflags[1:]' '        vflags = vflags[0:]' "exact model-generation call"
arm M9-three-cases fail 'for value, expected in cases:' 'for value, expected in cases[:3]:' "four compiler calls"
arm M10-exit-1 fail '    print("fixture guards: 4 cases PASS")
    return 0' '    print("fixture guards: 4 cases PASS")
    return 1' "requires exit 0"
arm M11-drop-define fail '["-DPP_TOP_SRP_DOM_DEF_VID=0x" + value]' '["-DPP_TOP_SRP_DOM_DEF_VID=" + value]' "exact compiler calls"

echo "mutation arms as expected: $PASSES, unexpected: $FAILS"
[ $FAILS -eq 0 ]
