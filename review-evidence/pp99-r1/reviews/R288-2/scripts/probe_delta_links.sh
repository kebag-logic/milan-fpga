#!/usr/bin/env bash
# Fault probes for the round-2 delta: does the repository's own link gate
# (scripts/check-links.py, UNMODIFIED) fail closed when the new explicit
# anchors or the links that use them are broken?
#
# Usage: probe_delta_links.sh <repo-clone-at-exact-head> <scratch-dir>
# Each probe extracts a fresh `git archive` of HEAD into <scratch-dir>/<name>,
# applies one mutation, runs the link gate from the copy and compares rc with
# the expectation. Exits 1 if any expectation is unmet. The clone is never
# written.
set -u
REPO=$(cd "$1" && pwd); SCR=$2; mkdir -p "$SCR"; fail=0
G=docs/guides/integrator.md; M=docs/architecture/07_memory_maps.md
probe() {  # name expected-rc sed-file sed-expr [ sed-file sed-expr ]
  local name=$1 want=$2; shift 2
  local d="$SCR/$name"; rm -rf "$d"; mkdir -p "$d"
  git -C "$REPO" archive HEAD | tar -x -C "$d"
  while [ $# -ge 2 ]; do sed -i -e "$2" "$d/$1"; shift 2; done
  out=$(cd "$d" && python3 scripts/check-links.py 2>&1); rc=$?
  verdict=PASS; [ "$rc" = "$want" ] || { verdict=FAIL; fail=1; }
  printf '%s %-34s want=%s rc=%s | %s\n' "$verdict" "$name" "$want" "$rc" \
    "$(printf '%s' "$out" | grep -E 'sec-(desc|resp)-memory|33[12]-|links:' | tr '\n' ' ' | cut -c1-220)"
}
probe baseline                       0
probe link-resp-typo                 1 $G 's/#sec-resp-memory)/#sec-resp-memoryX)/'
probe link-desc-typo-row80           1 $G '80s/#sec-desc-memory)/#sec-desc-memorX)/'
probe anchor-resp-removed            1 $M '/^<a id="sec-resp-memory"><\/a>$/d'
probe anchor-desc-removed            1 $M '/^<a id="sec-desc-memory"><\/a>$/d'
probe anchor-resp-renamed            1 $M 's/<a id="sec-resp-memory">/<a id="sec-resp-mem">/'
# Observational (pre-existing slug gap, S1 of round 1): the round-1 dead
# heading slug still passes the local gate although GitHub does not render it.
probe OBS-old-332-slug-passes-local  0 $G 's/#sec-resp-memory)/#332-the-other-main-memory-region-the-aecp-response-buffer)/'
echo "probes: $([ $fail = 0 ] && echo all expectations met || echo EXPECTATION UNMET)"
exit $fail
