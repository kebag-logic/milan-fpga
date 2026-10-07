#!/usr/bin/env bash
# Start the independent review campaigns concurrently, each with its own log and rc file.
# Usage: campaigns.sh <checkout> <packet>
set -u
SRC=$1; PKT=$2
S=$PKT/scratch; R=$PKT/receipts; P=$S/cgreen-prefix; SC=$PKT/scripts
mkdir -p "$R"
export PYTHONDONTWRITEBYTECODE=1
launch() {
  local name=$1; shift
  ( "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) &
}
launch profile-off bash "$SC/run_profile.sh" "$SRC" OFF "$S/build-off" "$R/profile-off" "$P"
launch profile-on bash "$SC/run_profile.sh" "$SRC" ON "$S/build-on" "$R/profile-on" "$P"
launch reversals-off env LD_LIBRARY_PATH="$P/lib" python3 "$SRC/tests/check_reversals.py" --work-dir "$S/rev-off" --prefix "$P"
launch reversals-on env LD_LIBRARY_PATH="$P/lib" python3 "$SRC/tests/check_reversals.py" --work-dir "$S/rev-on" --prefix "$P" --milan ON
launch probes python3 "$SC/probes.py" "$SRC" "$S/probes" "$P" "$R/probes.json" --jobs 2
launch embedded bash -c "cd '$SRC' && python3 tests/check_embedded.py --work-dir '$S/embedded'"
launch freestanding-off bash -c "cd '$SRC' && python3 tests/check_freestanding.py"
launch freestanding-on bash -c "cd '$SRC' && CC='cc -DLWSRP_MILAN=1' python3 tests/check_freestanding.py"
launch doc-sentences bash -c "cd '$SRC' && python3 doc/tools/check_sentences.py"
launch doc-references bash -c "cd '$SRC' && python3 doc/tools/check_references.py"
launch doc-references-selftest bash -c "cd '$SRC' && python3 doc/tools/check_references.py --self-test"
launch doc-links bash -c "cd '$SRC' && python3 doc/tools/check_links.py --github-auth"
launch doc-mermaid bash -c "cd '$SRC' && python3 doc/tools/render_mermaid.py --output '$S/graphs'"
wait
echo campaigns-done
