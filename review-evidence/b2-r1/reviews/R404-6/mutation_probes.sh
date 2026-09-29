#!/usr/bin/env bash
# Mutation probes for delta_check.sh. Builds mutant merge commits in a
# disposable clone and requires delta_check.sh to FAIL on each mutant and
# PASS on the unmutated control. Usage: mutation_probes.sh <source-repo> <scratch-dir>
set -euo pipefail
SRC=$1; S=$2; HERE=$(cd "$(dirname "$0")" && pwd)
HEAD=d62b1e1a3a37283ebad039880163873698a011db
PR=5c57927413e0dae279f06a75d2a58e3fec8a2bb0
DEV=79c36963660c10e4c1c11a744fb5bff41a552b8b
OLDDEV=13eda870d1a6cf3f946fc228a98862366b08d102
rm -rf "$S/probe"; git clone -q --no-checkout "$SRC" "$S/probe"; cd "$S/probe"
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@invalid GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@invalid
mk() { # name, then a function editing the index/worktree
  local name=$1; shift
  git read-tree "$HEAD"
  "$@"
  local t; t=$(git write-tree)
  local c; c=$(git commit-tree "$t" -p "$PR" -p "$DEV" -m "probe $name")
  local out rc=0
  out=$(HEAD_OVERRIDE=$c "$HERE/delta_check.sh" "$S/probe" 2>&1) || rc=$?
  local v; v=$(printf '%s\n' "$out" | grep -E '^DELTA-CHECK' || echo "DELTA-CHECK ERROR rc=$rc")
  printf '%-22s tree=%s %s\n' "$name" "$t" "$v"
  printf '%s\n' "$out" | grep -E '^FAIL ' | sed 's/^/    /' | head -5 || true
}
blob() { git hash-object -w --stdin; }
upd() { git update-index --add --cacheinfo "$1,$2,$3"; }
control() { :; }
m_page() { local b; b=$( (git show "$HEAD:docs/findings/606_FIRST_BIND_MEASUREMENT.md" | sed '17s/5 of 5/4 of 5/') | blob); upd 100644 "$b" docs/findings/606_FIRST_BIND_MEASUREMENT.md; }
m_drop451() { local b; b=$(git show "$PR:docs/findings/README.md" | blob); upd 100644 "$b" docs/findings/README.md; }
m_old75() { local b; b=$(git show "$DEV:docs/findings/README.md" | blob); upd 100644 "$b" docs/findings/README.md; }
m_order() { local b; b=$(git show "$HEAD:docs/findings/README.md" | python3 -c "
import sys
l=sys.stdin.read().splitlines(True)
i=[n for n,x in enumerate(l) if x.startswith('| [451_')][0]; r=l.pop(i)
j=[n for n,x in enumerate(l) if x.startswith('| [608_75_')][0]; l.insert(j+1,r); sys.stdout.write(''.join(l))" | blob); upd 100644 "$b" docs/findings/README.md; }
m_rtl() { local b; b=$(git show "$OLDDEV:hdl/milan/milan_datapath.sv" | blob); upd 100644 "$b" hdl/milan/milan_datapath.sv; }
m_gitlink() { upd 160000 "$(git rev-parse "$DEV:gptp-processor" | sed 's/^./0/')" protocol-processor; }
m_mode() { upd 100644 "$(git rev-parse "$DEV:sw/litex/sweep_extra.sh")" sw/litex/sweep_extra.sh; }
m_extra() { local b; b=$(printf 'x\n' | blob); upd 100644 "$b" docs/findings/STRAY.md; }
mk control control
mk page_byte m_page
mk readme_drop_451 m_drop451
mk readme_dev_side m_old75
mk readme_451_order m_order
mk dev_rtl_lost m_rtl
mk gitlink_moved m_gitlink
mk mode_lost m_mode
mk extra_file m_extra
