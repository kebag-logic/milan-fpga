Reviewer receipts for R703-1 (PR #792, head d58c8e22e9bd96237b9a28ea1ddd55b0426380c4).
Host path substitution in published copies: the product LiteX tree is written $LITEX and the
user's home $HOME (build.json files, environment.txt, scripts/env.sh). Simulation logs, results.json,
table.md and every other receipt are byte-for-byte as produced.
runs/<name>/      results.json, table.md, build.json and the printed summary + rc of each harness run
                  (a1x1, a8x8 = arm A; b1x1, b8x8 = arm B; c-asbuilt, c-slow = the harness's controls;
                  plant-over, plant-under = reviewer firmware plants, see runs/plant-over/plant.diff)
gates/            docs, idiom, hygiene, source-list gates and behave at the head; summary.txt has every rc
compare_*.txt     reviewer runs against the published receipts (results.json, logs, scripts)
recompute_*.json  figures recomputed from raw logs by scripts/recompute.py (no harness grader import)
access_*.json     per-access, idle, fetch-share, code-size figures by scripts/access_stats.py
review_mutants.log, mutant_regrade_A1.txt   reviewer source mutants vs the self-test, and their effect on real logs
drain_*.txt, composed_population.txt        per-pass ring releases and committed populations (F1)
notify_fanout_A8.txt                        the 8x8 set_name fan-out (F3)
stale_probe.log, regrade_empty.log          the reuse and regrade probes (F5, F6)
idle_profile_A1.txt                         function-level profile of idle passes from a committed-PC trace
fixture_regen.txt, build_identity.txt, environment.txt, clone_identity_final.txt, selftest.log
