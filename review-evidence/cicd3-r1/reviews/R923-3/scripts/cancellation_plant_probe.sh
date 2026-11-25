#!/bin/sh
# usage: cancellation_plant_probe.sh REPO COMMIT OUTDIR
# Extracts COMMIT into OUTDIR/<case> and plants each capture-matrix cancellation configuration
# in the template and/or the generated rtl-fast workflow, then runs the render check
# (ci_gate_workflows.py --check) and the contract check (ci_events.py --check) on each copy.
set -u
repo=$1; commit=$2; out=$3; mkdir -p "$out"; out=$(cd "$out" && pwd)
T=.github/ci-templates/rtl-fast.yml; W=.github/workflows/rtl-fast.yml
for case in control both-false both-absent template-only-false workflow-only-false; do
  d="$out/$case"; rm -rf "$d"; mkdir -p "$d"
  git -C "$repo" archive "$commit" | tar -x -C "$d"
  ( cd "$d"
    case $case in
      both-false) for f in $T $W; do python3 -I -c "import sys;p=sys.argv[1];s=open(p).read();i=s.index('  firmware-boundary-capture:\n');j=s.index('fail-fast: true',i);open(p,'w').write(s[:j]+'fail-fast: false'+s[j+15:])" $f; done;;
      both-absent) for f in $T $W; do python3 -I -c "import sys;p=sys.argv[1];s=open(p).read();i=s.index('  firmware-boundary-capture:\n');j=s.index('      fail-fast: true\n',i);open(p,'w').write(s[:j]+s[j+22:])" $f; done;;
      template-only-false) python3 -I -c "import sys;p=sys.argv[1];s=open(p).read();i=s.index('  firmware-boundary-capture:\n');j=s.index('fail-fast: true',i);open(p,'w').write(s[:j]+'fail-fast: false'+s[j+15:])" $T;;
      workflow-only-false) python3 -I -c "import sys;p=sys.argv[1];s=open(p).read();i=s.index('  firmware-boundary-capture:\n');j=s.index('fail-fast: true',i);open(p,'w').write(s[:j]+'fail-fast: false'+s[j+15:])" $W;;
    esac
    echo "== $case: capture-job fail-fast lines (template | workflow):"
    for f in $T $W; do awk '/^  firmware-boundary-capture:$/{on=1} on&&/fail-fast/{print FILENAME": "$0; exit} on&&/^  firmware-boundary:$/{print FILENAME": (none)"; exit}' $f; done
    python3 scripts/ci_gate_workflows.py --check > "$out/$case.render.log" 2>&1; echo "render check rc=$?"; grep -i -m3 'fail\|drift\|differ\|stale' "$out/$case.render.log" | cut -c1-220
    python3 scripts/ci_events.py --check > "$out/$case.events.log" 2>&1; echo "contract check rc=$?"; grep -m3 'strategy\|fail-fast\|OK' "$out/$case.events.log" | cut -c1-260 )
done
