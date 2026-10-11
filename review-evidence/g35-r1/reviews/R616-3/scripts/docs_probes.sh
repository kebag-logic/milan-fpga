#!/bin/sh
# Usage: docs_probes.sh <clone> <scratch-dir>
# Plants merge-resolution faults in disposable exports of the exact head and
# records whether `make docs` (check_docs + source evidence + diagrams) rejects
# each one. Never touches the clone's worktree.
set -u
C=${1:?clone}; S=${2:?scratch}
HEAD_C=49b9d0fdab9956d5294e60a07bbb8dfb9a23a78c
probe() {
  name=$1; shift
  d=$S/probe-$name; rm -rf "$d"; mkdir -p "$d"
  git -C "$C" archive "$HEAD_C" | tar -x -C "$d"
  ( cd "$d" && sh -c "$*" )
  ( cd "$d" && make docs > "$S/probe-$name.log" 2>&1 ); rc=$?
  [ "$rc" -ne 0 ] && v=REJECTED || v=ACCEPTED
  echo "$name rc=$rc $v"
}
probe control 'true'
probe conflict-marker-readme \
  "sed -i 's/^## Known risks\$/## Known risks\n\n<<<<<<< a70e388\n=======\n>>>>>>> 155de13/' README.md"
probe open-risks-heading-renamed \
  "sed -i 's/^## Open risks\$/## Open gaps/' docs/MANAGER.md"
probe stale-35-row-restored \
  "sed -i 's/^| Donor asymmetry input/| Mid-frame receive errors | Fix in review; not merged here | [Issue #35](https:\/\/github.com\/Mister-M-alt\/FPGA-gPTP\/issues\/35) |\n| Donor asymmetry input/' docs/MANAGER.md"
probe parser-anchor-shifted \
  "sed -i 's/KL_gptp_rx_parser.sv#L393/KL_gptp_rx_parser.sv#L392/' docs/SOURCE_EVIDENCE.md"
