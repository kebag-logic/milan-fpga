#!/bin/sh
# [R325] R325-3 disposable workflow-contract mutations of the new docs-check step.
# Usage: r325_workflow_mutations.sh <clean clone at b02af048> <scratch dir>
# Each arm edits a fresh copy's .github/workflows/docs.yml (or ci_events.py),
# runs `ci_events.py --check`, and must exit nonzero naming the defect.
set -u
CLONE=$1; SCRATCH=$2; M=$SCRATCH/wfmut
rm -rf "$M"; cp -a "$CLONE" "$M"
test "$(git -C "$M" rev-parse HEAD)" = b02af0480d3a3061df24683d522799d1759f7c33
W=.github/workflows/docs.yml
arm() {  # name, python edit expression over text t
  git -C "$M" checkout -q -- . 
  (cd "$M" && python3 - "$2" <<'PY'
import sys, pathlib
p = pathlib.Path('.github/workflows/docs.yml'); t = p.read_text()
old = "        run: python3 scripts/check_nvm_capture.py\n"
assert t.count(old) == 1
exec(sys.argv[1]); p.write_text(t)
PY
  )
  out=$(cd "$M" && python3 scripts/ci_events.py --check 2>&1); rc=$?
  echo "ARM $1 rc=$rc"; echo "$out" | grep -i 'capture\|must carry\|step 2[6-9]\|FAIL\|finding' | head -4
}
arm or-true            't = t.replace(old, old.rstrip("\n") + " || true\n")'
arm mutation-flag      't = t.replace(old, old.rstrip("\n") + " --mutation bytes\n")'
arm continue-on-error  't = t.replace(old, old + "        continue-on-error: true\n")'
arm if-always          't = t.replace(old, "        if: ${{ always() }}\n" + old)'
arm other-script       't = t.replace(old, "        run: python3 scripts/check_nvm_record_space.py\n")'
arm appended-cmd       't = t.replace(old, "        run: |\n          python3 scripts/check_nvm_capture.py\n          true\n")'
arm set-plus-e         't = t.replace(old, "        run: |\n          set +e\n          python3 scripts/check_nvm_capture.py\n")'
arm shell-override     't = t.replace(old, old + "        shell: bash {0}\n")'
arm env-bash-env       't = t.replace(old, old + "        env:\n          BASH_ENV: scripts/x.sh\n")'
git -C "$M" checkout -q -- .
echo "ARM unmodified: rc=$(cd "$M" && python3 scripts/ci_events.py --check >/dev/null 2>&1; echo $?)"
