#!/bin/sh
# R575-3 reproduction of every check in REPORT.md.
# usage: run_all.sh <clone at 42399611> <work dir> <verilator 5.050> <python with tools/markdown/requirements.txt>
# The clone is never modified except for ignored __pycache__ directories, which this removes at the end.
set -u
C=$1; W=$2; V=$3; MDPY=$4
S=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W/out"
cd "$C" || exit 2
test "$(git rev-parse HEAD)" = 42399611fc2217014024f03f4ba0365fb072688c || { echo "wrong head"; exit 2; }

# 1. Evidence archive: author/ subtree at archive commit 273764df (reviews/ is not extracted).
git init -q --bare "$W/evid.git"
git -C "$W/evid.git" fetch -q --depth=50 https://github.com/kebag-logic/milan-fpga.git 608-b14-review-evidence
mkdir -p "$W/archive"
git -C "$W/evid.git" archive 273764dfe9147f6749908358032ef397f785e05c review-evidence/608-b14-r1/author | tar -x -C "$W/archive"
AU=$W/archive/review-evidence/608-b14-r1/author
sha256sum "$AU/round2-recompute/MANIFEST.sha256"                       # expect 65636059...89dc
(cd "$AU/round2-recompute" && sha256sum -c MANIFEST.sha256)
sh "$AU/round2-recompute/scripts/run_all.sh" "$AU" "$W/out/rerun"; echo "round2 rerun rc=$?"
python3 -I "$S/recheck_round2_records.py" "$AU"; echo "recheck rc=$?"
python3 -I "$S/cited_paths.py" docs/findings/B14_BENCH_5603C353.md "$AU"; echo "cited paths rc=$?"
git show d981b1cc574f757a1d04d1b21d34a078ad85be3d:docs/findings/B14_BENCH_5603C353.md > "$W/page_d981b1cc.md"
python3 -I "$S/cited_paths.py" "$W/page_d981b1cc.md" "$AU"; echo "planted (previous page) rc=$? expect 1"

# 2. Counters feature, and the INFO-grading mutant.
(cd tests && behave -f progress features/counters_contract_milan.feature); echo "feature rc=$?"
mkdir -p "$W/mut1" && git archive HEAD tests tb/tools | tar -x -C "$W/mut1"
sh "$S/mut_info_probe.sh" "$W/mut1"; echo "mutant rc=$? expect 1 (only :408 fails; the 8 errors also occur unmutated in a partial tree)"

# 3. AAF listener NxN suite at the head and with FRAMES_RX reverted to +1 per interval.
VAX=$W/vaxis.git
git init -q --bare "$VAX" && git -C "$VAX" fetch -q --depth=1 https://github.com/alexforencich/verilog-axis 48ff7a7e2ef782cf778d47910cf85835c64b1bce
for t in rxbase rxmut; do
  mkdir -p "$W/$t/third_party/verilog-axis/rtl"
  git archive HEAD hdl tb/verilator/avtp_rxmon tb/common | tar -x -C "$W/$t"
  git -C "$VAX" show FETCH_HEAD:rtl/axis_fifo.v > "$W/$t/third_party/verilog-axis/rtl/axis_fifo.v"
done
sed -i "s/? 32'(frx_add_r) : 32'd1);/? 32'd1 : 32'd1);/" "$W/rxmut/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
sh "$S/rxmon_nx_run.sh" "$W/rxbase" "$V" & sh "$S/rxmon_nx_run.sh" "$W/rxmut" "$V" & wait

# 4. Documentation gates.
"$MDPY" scripts/docs_check.py; "$MDPY" scripts/check_doc_style.py
"$MDPY" scripts/gen_toc.py --check; "$MDPY" scripts/gen_toc.py --verify-anchors
"$MDPY" scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee; "$MDPY" scripts/check_doc_paths.py
python3 scripts/check_baremetal_only.py --check; python3 scripts/check_baremetal_only.py --selftest
git diff --check 5603c353137e90c1fa95429f6d00ef7a2298d9ee HEAD; git diff --check d981b1cc574f757a1d04d1b21d34a078ad85be3d HEAD
rm -rf scripts/__pycache__ tb/tools/__pycache__ tests/steps/__pycache__
git status --porcelain --ignored
