#!/usr/bin/env bash
# collect3final.sh <part...>: round 3's final-head receipts (a91fb27d): ci (the replay), docsyml, sweep, tools.
# Host paths replaced (receipt.py); logs over 200 KB reduced to their verdict lines with size and sha256.
set -uo pipefail
S=<scratch>; O=<home>/milan-fpga-management/2026-09-23/665s9-a760/receipts/r3/final
R="python3 $S/tools/receipt.py"; H=a91fb27dd39483e4694e193504da1dbe06208807; C=$S/ci/a91fb27dd394
san() { sed -e "s#$S#<scratch>#g; s#<lane>#<lane>#g; s#<tools>#<tools>#g; s#<home>#<home>#g; s#<data>#<data>#g" "$1"; }
for part in "$@"; do
  case $part in
    ci)
      $R "$S/ci-table.md" "$O/ci/ci-table.md" $H "ci_replay.py table: every run: step of every job a pull_request to dev-soft-core triggers" > /dev/null
      $R "$S/ci-table.out" "$O/ci/ci-table.out" $H "ci_replay.py table" > /dev/null
      san "$S/ci-not_run.json" > "$O/ci/not_run.json"
      $R "$S/ci-plan.txt" "$O/ci/plan.txt" $H "ci_replay.py plan" > /dev/null
      $R "$S/ci-tick.log" "$O/ci/tick.log" $H "tools/replay-drive.sh (ci_replay.py tick, at most 3 units)" > /dev/null
      for n in 1 2 3 4; do $R "$S/ci-local-$n.log" "$O/ci/local-$n.log" $H "ci_replay.py local (runner $n)" > /dev/null; done
      for j in $C/jobs/*/; do
        n=$(basename "$j")
        [ -f "$j/result.json" ] && $R "$j/result.json" "$O/ci/jobs/$n/result.json" $H "ci_replay.py job" > /dev/null
        for l in "$j"/logs/*.log; do
          [ -f "$l" ] && $R "$l" "$O/ci/jobs/$n/$(basename "$l")" $H "ci_replay.py job (the step's own log)" > /dev/null
        done
      done
      ;;
    docsyml)
      $R "$S/docsyml-verify.log" "$O/docsyml/verify_docs_yml.log" $H "tools/docsyml/from_replay.py <replay> <root>; tools/docsyml/verify_docs_yml.py $H <root>" > /dev/null
      san "$S/tools/docsyml/not_run.json" > "$O/docsyml/not_run.json"
      ;;
    sweep)
      $R "$S/native-spec.json" "$O/sweep/native-spec.json" $H "the full sweep's spec (Make's --no-print-directory in MAKEFLAGS)" > /dev/null
      $R "$S/sweep-watch.log" "$O/sweep/sweep-watch.log" $H "tools/sweep-watch.py (shards launched as cpu_ranges.py ranges freed)" > /dev/null
      for k in 0 1 2 3; do
        d=$S/sweep/shard-$k
        $R "$d/spec.json" "$O/sweep/shard-$k/spec.json" $H "tools/sweep-shard.py $k" > /dev/null
        [ -f "$d/spec/results.json" ] && $R "$d/spec/results.json" "$O/sweep/shard-$k/results.json" $H "run-recorded-gates.py" > /dev/null
        for l in "$d"/spec/*.log; do [ -f "$l" ] && $R "$l" "$O/sweep/shard-$k/$(basename "$l")" $H "scripts/run_all_suites.sh --shard $k/4" > /dev/null; done
        [ -d "$d/logs" ] && for l in "$d"/logs/*; do [ -f "$l" ] && $R "$l" "$O/sweep/shard-$k/logs/$(basename "$l")" $H "the suite's own log" > /dev/null; done
      done
      ;;
    tools)
      mkdir -p "$O/../tools/docsyml" "$O/../tools/replay"
      for f in $S/tools/docsyml/*.py; do san "$f" > "$O/../tools/docsyml/$(basename "$f")"; done
      for f in $S/tools/*.sh $S/tools/*.py; do san "$f" > "$O/../tools/$(basename "$f")"; done
      for f in $S/tools/replay/ci_replay.py $S/tools/replay/overrides.json $S/tools/replay/pidfd_shim.py; do san "$f" > "$O/../tools/replay/$(basename "$f")"; done
      ;;
  esac
done
echo "collected: $*"
