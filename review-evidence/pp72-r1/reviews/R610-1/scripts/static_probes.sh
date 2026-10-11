#!/usr/bin/env bash
# Plant one fault at a time in a disposable clone at the reviewed head, run the
# static half of scripts/check-req-tags.py (and check-matrix.py where it bears),
# record the output and rc, and restore the clone with `git checkout -- .`.
# usage: static_probes.sh CLONE OUTDIR
set -u
clone=$1; out=$2
mkdir -p "$out"
cd "$clone" || exit 2
R=docs/00_MILAN_COMPLIANCE_REVIEW.md
V=docs/architecture/09_verification.md

probe() {  # name, then a command that plants the fault
  local name=$1; shift
  git checkout -q -- . && git clean -qfd tb docs
  "$@"
  { echo "## probe $name"; git diff --stat | tail -1
    python3 scripts/check-req-tags.py; echo "reqtags rc=$?"
    python3 scripts/check-matrix.py; echo "matrix rc=$?"; } >"$out/$name.txt" 2>&1
  git checkout -q -- . && git clean -qfd tb docs
}

# the assignment's five (the executed one, a dead tag, is in executed_probe.sh)
probe p1-tag-removed sed -i '/REQ_TAG("REQ-AEM-005", "RND"/d' tb/originator/sim_main.cpp
probe p2-unknown-req sed -i 's/REQ_TAG("REQ-ADP-006", "DIR"/REQ_TAG("REQ-ADP-099", "DIR"/' tb/adp_engine/sim_main.cpp
probe p4-waiver-no-gap sed -i 's/^| REQ-AEM-025 | RND | GAP-06 |/| REQ-AEM-025 | RND | |/' "$V"
probe p5-row-added sed -i 's/^\(| REQ-AEM-026 .*\)$/\1\n| REQ-AEM-027 | x | y | shall | A | [GAP-06](#gap-06) | a | d | DIR |/' "$R"
# beyond the five
probe x1-wrong-category sed -i 's/REQ_TAG("REQ-AEM-005", "RND"/REQ_TAG("REQ-AEM-005", "DIR"/' tb/originator/sim_main.cpp
probe x2-name-not-at-check sed -i 's/REQ_TAG("REQ-ADP-006", "DIR", "P12 no committed/REQ_TAG("REQ-ADP-006", "DIR", "P99 no committed/' tb/adp_engine/sim_main.cpp
probe x3-other-rows-gap sed -i 's/^| REQ-AEM-025 | RND | GAP-06 |/| REQ-AEM-025 | RND | GAP-04 |/' "$V"
probe x4-cov-state-wrong sed -i 's/^\(| REQ-AEM-005 | [^|]*| [^|]*| shall | \)A; traced |/\1A; waived GAP-17 |/' "$R"
probe x5-stale-waiver sed -i 's/^\(| REQ-AEM-025 | RND .*\)$/\1\n| REQ-AEM-005 | RND | GAP-17 | stale |/' "$V"
probe x6-row-short sed -i 's/^\(| REQ-AEM-026 .*\)$/\1\n| REQ-AEM-027 | x | y | shall | A | [GAP-06](#gap-06) | a | DIR |/' "$R"
probe x7-row-empty-ver sed -i 's/^\(| REQ-AEM-026 .*\)$/\1\n| REQ-AEM-027 | x | y | shall | A | [GAP-06](#gap-06) | a | d | |/' "$R"
probe x8-commented-tag sed -i 's|^  REQ_TAG("REQ-AEM-005", "RND"|  // REQ_TAG("REQ-AEM-005", "RND"|' tb/originator/sim_main.cpp
probe x9-name-substring sed -i 's/REQ_TAG("REQ-MAAP-002", "DIR", "U1: PROBE byte-exact")/REQ_TAG("REQ-MAAP-002", "DIR", "U1")/' tb/maap/sim_main.cpp
probe x10-tag-in-untracked-file bash -c 'printf "  REQ_TAG(\"REQ-ZZZ-001\", \"DIR\", \"Z\");\n  CHECK(1, \"Z\");\n" > tb/originator/extra.cpp'
probe x11-coverage-table-drop sed -i 's/^| traced | RND | REQ-AEM-005, /| traced | RND | /' "$V"
probe x12-waiver-dup-gap sed -i 's/^| REQ-AEM-025 | RND | GAP-06 |/| REQ-AEM-025 | RND | GAP-06, GAP-06 |/' "$V"
git checkout -q -- . && git clean -qfd tb docs
git status --short >"$out/restore-status.txt"
git rev-parse HEAD >>"$out/restore-status.txt"
