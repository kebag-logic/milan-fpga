#!/usr/bin/env bash
# Disposable mutation probes on the round-3 claims. Each mutant is planted in
# the clone, the gate that should refuse it is run, and the file is restored
# from the index. A probe PASSES when the gate returns non-zero on the mutant.
# Usage: probe_mutations.sh <repo> <markdown-python> <em-dash-base> <out-dir>
set -u
REPO=$1 MDPY=$2 BASE=$3 OUT=$4
mkdir -p "$OUT"
cd "$REPO" || exit 2
result=0
probe() {   # name file gate...  (mutation already applied by caller)
  name=$1 file=$2; shift 2
  "$@" > "$OUT/$name.log" 2>&1; rc=$?
  git checkout -- "$file"
  if [ "$rc" -ne 0 ]; then v=KILLED; else v=SURVIVED; result=1; fi
  printf '%s rc=%s %s\n' "$name" "$rc" "$v" | tee "$OUT/$name.rc"
}
# M1: drop the new CHANGELOG contents entry -> contents gate must refuse
sed -i '/^- \*\*\[Unreleased - processor pin 2ad2f845\]/d' CHANGELOG.md
probe M1_changelog_contents_entry_removed CHANGELOG.md "$MDPY" scripts/gen_toc.py --check
# M2: stale contents label (heading renamed) -> contents gate must refuse
sed -i 's/^## Unreleased - processor pin 2ad2f845$/## Unreleased - processor pin 2ad2f84/' CHANGELOG.md
probe M2_changelog_heading_renamed CHANGELOG.md "$MDPY" scripts/gen_toc.py --check
# M3: an added em dash in the new section -> em-dash gate must refuse
sed -i 's/^- Later MAC stalls remain a wire-gap limitation\.$/- Later MAC stalls \xe2\x80\x94 a wire-gap limitation./' CHANGELOG.md
probe M3_changelog_em_dash CHANGELOG.md "$MDPY" scripts/check_em_dash.py --base "$BASE"
# M4: the worker cap also changes general.maxThreads -> helper self-test must refuse
sed -i 's|script.write_text("set_param synth.maxThreads 1\\n" + script.read_text())|script.write_text("set_param synth.maxThreads 1\\nset_param general.maxThreads 1\\n" + script.read_text())|' syn/ooc/pp_baseline.py
grep -q 'general.maxThreads 1\\n" + script' syn/ooc/pp_baseline.py || { echo "M4 not planted"; result=1; }
probe M4_cap_touches_general_threads syn/ooc/pp_baseline.py python3 syn/ooc/pp_baseline.py --selftest
# M5: the flag becomes a no-op -> helper self-test must refuse
sed -i 's|script.write_text("set_param synth.maxThreads 1\\n" + script.read_text())|script.write_text(script.read_text())|' syn/ooc/pp_baseline.py
grep -q 'script.write_text(script.read_text())' syn/ooc/pp_baseline.py || { echo "M5 not planted"; result=1; }
probe M5_cap_flag_noop syn/ooc/pp_baseline.py python3 syn/ooc/pp_baseline.py --selftest
# M6: a long multi-sentence bullet in the new section -> style gate must refuse
sed -i 's/^- It also carries #164\.$/- It also carries #164, which grades the Domain notification at the processor top, and this sentence keeps going far beyond what the concise audience style permits for one line. Then another sentence follows on the same line./' CHANGELOG.md
probe M6_changelog_style CHANGELOG.md "$MDPY" scripts/check_doc_style.py
git diff --quiet && git diff --cached --quiet || { echo "tree not restored"; result=1; }
exit $result
