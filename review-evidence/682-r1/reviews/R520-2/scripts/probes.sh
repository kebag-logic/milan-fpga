#!/usr/bin/env bash
# Usage: probes.sh <repo> <python-with-locked-markdown-renderer> <receipt-dir> <em-dash-base>
# Disposable fault probes against the round-3 delta. Each probe edits one
# tracked file, runs the gate that should refuse it, and restores HEAD bytes.
# A probe is KILLED when the gate returns nonzero.
set -u
repo=$1; py=$2; out=$3; base=$4
mkdir -p "$out"; : > "$out/probe_rc.tsv"
cd "$repo"
probe() { name=$1; file=$2; edit=$3; shift 3
  "$py" -I -c "$edit" "$file"
  git diff --stat -- "$file" > "$out/$name.diffstat"
  "$@" > "$out/$name.log" 2>&1; rc=$?
  git checkout -- "$file"
  verdict=SURVIVED; [ "$rc" -ne 0 ] && verdict=KILLED
  printf '%s\t%s\t%s\t%s\n' "$name" "$rc" "$verdict" "$*" >> "$out/probe_rc.tsv"; }
sub='import sys;p=sys.argv[1];s=open(p,encoding="utf-8").read();'
probe P1_drop_contents_entry CHANGELOG.md \
  "$sub"'o="- **[Unreleased - processor pin 2ad2f845](#unreleased---processor-pin-2ad2f845)** -- Notifications follow grants and round boundaries.\n";assert s.count(o)==1;open(p,"w",encoding="utf-8").write(s.replace(o,""))' \
  "$py" scripts/gen_toc.py --check
probe P2_rename_heading CHANGELOG.md \
  "$sub"'o="## Unreleased - processor pin 2ad2f845\n";assert s.count(o)==1;open(p,"w",encoding="utf-8").write(s.replace(o,"## Unreleased - processor pin 2ad2f84\n"))' \
  "$py" scripts/gen_toc.py --check
probe P3_em_dash_added_line CHANGELOG.md \
  "$sub"'o="- It also carries #164.\n";assert s.count(o)==1;open(p,"w",encoding="utf-8").write(s.replace(o,"- It also carries #164 — the last.\n"))' \
  "$py" scripts/check_em_dash.py --base "$base"
probe P4_long_sentence CHANGELOG.md \
  "$sub"'o="- It also carries #164.\n";assert s.count(o)==1;open(p,"w",encoding="utf-8").write(s.replace(o,"- It also carries #164 and one two three four five six seven.\n"))' \
  "$py" scripts/check_doc_style.py
probe P5_em_dash_recipe docs/testing/PP_SHADOW_BASELINE_RECIPE.md \
  "$sub"'o="Current baseline F was recorded with";assert s.count(o)==1;open(p,"w",encoding="utf-8").write(s.replace(o,"Current baseline F — was recorded with"))' \
  "$py" scripts/check_em_dash.py --base "$base"
probe P6_flag_cap_wrong syn/ooc/pp_baseline.py \
  "$sub"'o="script.write_text(\"set_param synth.maxThreads 1\\n\" + script.read_text())";assert s.count(o)==1,s.count(o);open(p,"w",encoding="utf-8").write(s.replace(o,"script.write_text(\"set_param synth.maxThreads 2\\n\" + script.read_text())"))' \
  "$py" syn/ooc/pp_baseline.py --selftest
probe P7_flag_ignored syn/ooc/pp_baseline.py \
  "$sub"'o="    if args.single_thread_synthesis:\n";assert s.count(o)==1;open(p,"w",encoding="utf-8").write(s.replace(o,"    if False and args.single_thread_synthesis:\n"))' \
  "$py" syn/ooc/pp_baseline.py --selftest
probe P8_drop_recipe_flag docs/testing/PP_SHADOW_BASELINE_RECIPE.md \
  "$sub"'o="python3 syn/ooc/pp_baseline.py \"$WORK/ax7101/gateware\" --single-thread-synthesis\n";assert s.count(o)==1;open(p,"w",encoding="utf-8").write(s.replace(o,"python3 syn/ooc/pp_baseline.py \"$WORK/ax7101/gateware\"\n"))' \
  "$py" scripts/docs_check.py
git status --porcelain=v1 --untracked-files=all > "$out/status_after.txt"
cat "$out/probe_rc.tsv"; echo "status-lines: $(wc -l < "$out/status_after.txt")"
