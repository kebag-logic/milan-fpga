#!/usr/bin/env bash
# Composition checks for processor PR #133 at its merge head (read-only on the repo).
# usage: composition_check.sh <repo> [head=99bfd4bc...] [c1=412efeb7] [d3=d352bbaa] [base=c951a9ff]
set -uo pipefail
repo=$1; head=${2:-99bfd4bc3180bab97d47f63056513fb39eea6a37}
c1=${3:-412efeb750e358a65b04bae1cbb3086134d15b7e}; d3=${4:-d352bbaa7cae0be2c6248f7869afe2a272ab014b}
base=${5:-c951a9ff0cb5851fb159d33e966e5a2a9a188fe3}
cd "$repo"
echo "head $(git rev-parse $head) tree $(git rev-parse $head^{tree}) parents $(git rev-parse $head^1) $(git rev-parse $head^2)"
echo "merge-base(c1,d3) $(git merge-base $c1 $d3)"
echo "fresh merge-tree(c1,d3) $(git merge-tree --write-tree $c1 $d3 | head -1)  (must equal the head tree)"
c1f=$(git diff --name-only $base $c1 | sort); d3f=$(git diff --name-only $base $d3 | sort)
echo "files changed by both lanes: $(comm -12 <(echo "$c1f") <(echo "$d3f") | tr '\n' ' ')"
echo "C1-only files differing from $c1 at head: $(git diff --name-only $c1 $head -- $(comm -23 <(echo "$c1f") <(echo "$d3f")) | wc -l)"
echo "#132-only files differing from $d3 at head: $(git diff --name-only $d3 $head -- $(comm -13 <(echo "$c1f") <(echo "$d3f")) | wc -l)"
echo "hdl files changed by C1: $(git diff --name-only $base $c1 -- hdl | tr '\n' ' ')"
echo "hdl files changed by #132: $(git diff --name-only $base $d3 -- hdl | tr '\n' ' ')"
echo "--- protocol_processor_top.sv: head vs #132 (only C1's comment may differ)"
git diff $d3 $head -- hdl/top/protocol_processor_top.sv | grep -E '^[+-][^+-]'
echo "--- #132's top diff lines naming SRP/MRP/arm/draw/TX nets (expect none)"
git diff $base $d3 -- hdl/top/protocol_processor_top.sv | grep -E '^[+-][^+-]' \
  | grep -E 'mrp_|srp_|now_ms|draw|\barm_|txs_|txreq|v_mrp' || echo "(none)"
echo "--- shared-service instances, byte-compared across base, C1, #132 and head"
python3 - "$base" "$c1" "$d3" "$head" <<'PY'
import re, subprocess, sys
revs = sys.argv[1:]
src = {r: subprocess.run(["git", "show", f"{r}:hdl/top/protocol_processor_top.sv"],
                         capture_output=True, text=True, check=True).stdout for r in revs}
end = re.compile(r'^\s*\);\s*$', re.M)
def inst(s, pat):
    i = s.find(pat); k = s.find(" u_", i); m = end.search(s, k)
    return s[i:m.end()]
for pat in ["KL_pp_timer_service #(", "KL_pp_prng u_prng", "KL_pp_tx_arbiter #(", "KL_srp_top #("]:
    b = [inst(src[r], pat) for r in revs]
    print(f"{pat:24s} {len(b[-1]):5d} chars, identical in all four: {all(x == b[0] for x in b)}")
arm = [[l for l in src[r].splitlines() if re.search(r'\barm', l)] for r in revs]
print(f"lines naming arm*: {len(arm[-1])}, identical in all four: {all(a == arm[0] for a in arm)}")
PY
echo "--- the D3 writer's ports naming a shared service (expect none)"
grep -n -E '^\s*(input|output)' hdl/aecp/KL_aecp_nvm_writer.sv 2>/dev/null | grep -i -E '\barm|draw|prng|\btx' || git show $head:hdl/aecp/KL_aecp_nvm_writer.sv | grep -n -E '^\s*(input|output)' | grep -i -E '\barm|draw|prng|\btx' || echo "(none)"
