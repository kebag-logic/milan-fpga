#!/usr/bin/env bash
# Disposable composition probes. Usage: probes.sh <probe-clone-at-candidate> <python-with-pinned-markdown-env>
# Each arm plants one defect into the composed findings index or a cross-page anchor,
# runs the gates that read it, records their rc, then restores the exact bytes.
set -u
D=$1; PY=$2; cd "$D" || exit 2
R=docs/findings/README.md; P8=docs/findings/608_75_WITHDRAWAL_AND_RESTART.md
arm() { # name file python-edit
  local name=$1 f=$2 edit=$3
  cp "$f" "$f.orig"
  "$PY" -c "import sys;p=sys.argv[1];s=open(p).read();n=$edit;assert n!=s,'edit did not apply';open(p,'w').write(n)" "$f" || { echo "ARM $name: edit failed"; mv "$f.orig" "$f"; return; }
  echo "ARM $name"
  "$PY" scripts/docs_check.py >/tmp/r405_p.$$ 2>&1; echo "  docs_check rc=$? $(tail -1 /tmp/r405_p.$$ | cut -c1-120)"
  "$PY" scripts/check_doc_paths.py >/tmp/r405_p.$$ 2>&1; echo "  check_doc_paths rc=$? $(tail -1 /tmp/r405_p.$$ | cut -c1-120)"
  "$PY" scripts/gen_toc.py --verify-anchors >/tmp/r405_p.$$ 2>&1; echo "  gen_toc --verify-anchors rc=$? $(tail -1 /tmp/r405_p.$$ | cut -c1-120)"
  git -c core.whitespace=blank-at-eol diff --check >/tmp/r405_p.$$ 2>&1; echo "  git diff --check rc=$? $(head -1 /tmp/r405_p.$$ | cut -c1-120)"
  mv "$f.orig" "$f"
}
arm broken-index-link "$R" "s.replace('](606_FIRST_BIND_MEASUREMENT.md)','](606_FIRST_BIND_MEASUREMEN.md)',1)"
arm broken-cross-anchor "$P8" "s.replace('606_FIRST_BIND_MEASUREMENT.md#saved-state-layer','606_FIRST_BIND_MEASUREMENT.md#saved-state-layers',1)"
arm conflict-residue "$R" "s.replace('| [451_TDM8', '<<<<<<< HEAD\n| [451_TDM8',1).replace('\n| [COMMERCIAL', '\n=======\n>>>>>>> dev\n| [COMMERCIAL',1)"
rm -f /tmp/r405_p.$$
echo "restored: $(git status --porcelain | wc -l) dirty path(s); tree $(git write-tree 2>/dev/null)"
