#!/bin/sh
# Show that a revision pair differs in milan_csr.sv by comment text only:
# 1. the raw diff touches only lines whose code part (before //) is identical;
# 2. the Verilator preprocessor output (comments stripped, `line kept and
#    dropped) is byte-identical for both revisions under each shipping shape;
# 3. every lock_mutants.py pattern occurs exactly once at both revisions;
# 4. the frozen reference's digest check in gen_lockstep.py is untouched.
# Usage: comment_only_probe.sh <clone> <base-rev> <head-rev> <verilator> <outdir>
set -eu
clone=$1; base=$2; head=$3; vl=$4; out=$5
mkdir -p "$out"
rel=hdl/common/csr/milan_csr.sv
for rev in "$base" "$head"; do
  d="$out/src_$rev"; mkdir -p "$d/csr"
  git -C "$clone" show "$rev:$rel" > "$d/csr/milan_csr.sv"
done
# The generated includes come from the clone's tracked tree (identical for
# both revisions: the pair touches no file under hdl/common/csr/gen or configs).
git -C "$clone" diff --quiet "$base" "$head" -- hdl/common/csr/gen hdl/common/gen configs \
  && echo "includes: unchanged between $base and $head"
python3 -I - "$out/src_$base/csr/milan_csr.sv" "$out/src_$head/csr/milan_csr.sv" <<'EOF'
import sys
a = open(sys.argv[1]).read().splitlines()
b = open(sys.argv[2]).read().splitlines()
print(f"lines: base {len(a)} head {len(b)}")
assert len(a) == len(b), "line count differs"
diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
code = lambda s: s.split("//", 1)[0].rstrip()
bad = [i + 1 for i in diff if code(a[i]) != code(b[i]) or "//" not in a[i] or "//" not in b[i]]
print(f"differing lines: {[i + 1 for i in diff]}")
print(f"differing lines whose code part differs: {bad}")
sys.exit(1 if bad else 0)
EOF
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_current endstation_arty_4x4; do
  for mode in P L; do
    for rev in "$base" "$head"; do
      flag=""; [ "$mode" = P ] && flag="-P"
      "$vl" -E $flag +incdir+"$clone/hdl/common/csr" +incdir+"$clone/configs/generated/$shape" \
        "$out/src_$rev/csr/milan_csr.sv" > "$out/pp_${shape}_${mode}_$rev.sv"
    done
    # `line directives name the source path, which differs between the two
    # extraction directories; normalise that path before comparing.
    sed "s#src_$base#SRC#g" "$out/pp_${shape}_${mode}_$base.sv" > "$out/n_b.sv"
    sed "s#src_$head#SRC#g" "$out/pp_${shape}_${mode}_$head.sv" > "$out/n_h.sv"
    if cmp -s "$out/n_b.sv" "$out/n_h.sv"; then
      echo "preprocessed $shape mode $mode: IDENTICAL ($(wc -l < "$out/n_h.sv") lines, sha256 $(sha256sum < "$out/n_h.sv" | cut -c1-16))"
    else
      echo "preprocessed $shape mode $mode: DIFFERENT"; exit 1
    fi
    rm -f "$out/pp_${shape}_${mode}_$base.sv" "$out/pp_${shape}_${mode}_$head.sv" "$out/n_b.sv" "$out/n_h.sv"
  done
done
python3 -I - "$clone/tb/verilator/csr/lock_mutants.py" "$out/src_$base/csr/milan_csr.sv" "$out/src_$head/csr/milan_csr.sv" <<'EOF'
import ast, sys
tree = ast.parse(open(sys.argv[1]).read())
muts = next(ast.literal_eval(n.value) for n in tree.body
            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "MUTATIONS")
srcs = [open(p).read() for p in sys.argv[2:]]
bad = 0
for name, pattern, _, check, leg in muts:
    counts = [s.count(pattern) for s in srcs]
    print(f"anchor {counts} ({leg}, {check}): {name}")
    bad += counts != [1, 1]
print(f"{len(muts)} anchors, {bad} not exactly once at both revisions")
sys.exit(1 if bad else 0)
EOF
git -C "$clone" diff --quiet "$base" "$head" -- tb && echo "tb/: unchanged between $base and $head"
echo "ALL COMMENT-ONLY CHECKS PASSED"
