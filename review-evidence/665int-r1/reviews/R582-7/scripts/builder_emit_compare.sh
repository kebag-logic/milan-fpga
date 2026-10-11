#!/usr/bin/env bash
# builder_emit_compare.sh CLONE SCRATCH REV_A REV_B : export REV_A and REV_B
# with git archive (submodules linked to CLONE's checkouts, whose gitlinks are
# equal at both revisions), run the end-station builder for every
# configs/*.yaml in each, and compare every file it writes and the SoC argv
# it emits. Exit 1 on any difference.
set -euo pipefail
clone=$1 scratch=$(cd "$2" && pwd) a=$3 b=$4
for rev in "$a" "$b"; do
  t="$scratch/tree-$rev"
  rm -rf "$t"; mkdir -p "$t"
  git -C "$clone" archive "$rev" | tar -x -C "$t"
  for s in protocol-processor gptp-processor third_party/verilog-axis; do
    rmdir "$t/$s" 2>/dev/null || true
    ln -s "$clone/$s" "$t/$s"
  done
  ( cd "$t" && python3 - "$t" <<'EOF'
import json, pathlib, sys
t = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(t / "sw/builder"))
import endstation_builder as eb
out = t / "sw/builder/out"
argv = {}
for cfg_path in sorted((t / "configs").glob("*.yaml")):
    cfg = eb.load_config(cfg_path)
    eb.build(cfg_path, out)
    argv[cfg["name"]] = eb.emit_soc_argv(cfg)
(t / "emitted_argv.json").write_text(json.dumps(argv, indent=1, sort_keys=True))
print(len(argv), "config(s) built")
EOF
  ) >"$scratch/build-$rev.log" 2>&1
done
ta="$scratch/tree-$a" tb="$scratch/tree-$b"
rc=0
diff -r "$ta/sw/builder/out" "$tb/sw/builder/out" >"$scratch/diff-out.txt" || rc=1
diff -r "$ta/configs/generated" "$tb/configs/generated" >"$scratch/diff-gen.txt" || rc=1
diff "$ta/emitted_argv.json" "$tb/emitted_argv.json" >"$scratch/diff-argv.txt" || rc=1
nf=$(find "$tb/sw/builder/out" "$tb/configs/generated" -type f | wc -l)
echo "configs: $(tail -1 "$scratch/build-$b.log"); files compared: $nf; differences: out=$(wc -l <"$scratch/diff-out.txt") generated=$(wc -l <"$scratch/diff-gen.txt") argv=$(wc -l <"$scratch/diff-argv.txt")"
exit $rc
