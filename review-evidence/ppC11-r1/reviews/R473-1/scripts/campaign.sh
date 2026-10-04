#!/usr/bin/env bash
# Reviewer campaign for PR #156 at exact head. Portable: set REPO (the review
# clone), PKT (this packet), WAVEDROM_PYTHONPATH (a site-packages carrying the
# `wavedrom` package) and VERILATOR (pinned 5.050) before running.
# Every probe runs in its own throw-away clone under $PKT/scratch; the review
# clone itself is only read. Each probe writes receipts/<name>.log and .rc.
set -uo pipefail
REPO=${REPO:-$REVIEWS/r473-1-ppC11}
PKT=${PKT:-$REVIEWS/ppC11-r473-1-packet}
HEAD_SHA=91cef52b3c56cc69f66966b004782a69d2940a46
BASE_SHA=c050d97153dd0480ae741102c1647eeda9b7f273
export PYTHONPATH=${WAVEDROM_PYTHONPATH:-$VALIDATION_TOOLS/md-venv-40cdefe08ebd/lib/python3.14/site-packages}
VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
S=$PKT/scratch/campaign; R=$PKT/receipts
rm -rf "$S"; mkdir -p "$S" "$R"

fresh() { # $1 = dir, $2 = sha : a disposable clone at that commit
  git clone -q --no-checkout "$REPO" "$1" && git -C "$1" checkout -q --detach "$2"
}
run() { # $1 = name, rest = function
  local n=$1; shift
  ( "$@" ) >"$R/$n.log" 2>&1; echo $? >"$R/$n.rc"
}

# ---- A: the CI docs-gates step, as written, at the head ----------------------
p_make_check_head() {
  fresh "$S/A" $HEAD_SHA && cd "$S/A" && mmdc --version && make check
}
# ---- B: the new ID gate run over the BASE tree (expect 39 uses / 3 IDs) -------
p_ids_on_base() {
  fresh "$S/B" $BASE_SHA && cd "$S/B" \
    && git -C "$REPO" show $HEAD_SHA:scripts/check-ids.py > /tmp/ids-$$.py \
    && python3 /tmp/ids-$$.py --root "$S/B"; rc=$?
  rm -f /tmp/ids-$$.py
  echo "distinct undefined: $(grep -o 'ID FAIL: [^ ]* [^ ]*' "$R/ids_on_base.log" 2>/dev/null | awk '{print $4}' | sort -u | tr '\n' ' ')"
  return $rc
}
# ---- C: ID-gate fault probes, each planted in its own clone ------------------
ids_probe() { # $1 = tag, $2 = shell that plants, $3 = expected rc
  local d="$S/C-$1"; fresh "$d" $HEAD_SHA >/dev/null 2>&1; cd "$d" || return 99
  bash -c "$2"; python3 scripts/check-ids.py; local rc=$?
  echo "probe $1: rc=$rc want=$3"; [ "$rc" = "$3" ]
}
p_ids_probes() {
  local fails=0
  ids_probe stray-doc-P     'echo "uses P-NOT-DEFINED here" >> docs/architecture/05_acmp_engine.md' 1 || fails=$((fails+1))
  ids_probe stray-history-T 'echo "a T-NOT-DEFINED stray" >> docs/history/02-class-a-word-stream.md' 1 || fails=$((fails+1))
  ids_probe stray-rtl-T     'sed -i "1a // T-NOPE-RTL cited" hdl/packet_engine/KL_pp_tx_slots.sv' 1 || fails=$((fails+1))
  ids_probe stray-untracked 'mkdir -p tb/newsuite && echo "// P-UNTRACKED-STRAY" > tb/newsuite/sim_main.cpp' 1 || fails=$((fails+1))
  ids_probe stray-ignored   'mkdir -p tb/tx_slots/obj_dir && echo "// P-IGNORED-BUILD" > tb/tx_slots/obj_dir/x.cpp && git check-ignore -q tb/tx_slots/obj_dir/x.cpp' 0 || fails=$((fails+1))
  ids_probe del-maap-row    'sed -i "/^| P-MAAP-ACCEPT-CYC |/d" docs/architecture/01_overview.md' 1 || fails=$((fails+1))
  ids_probe del-T-row       'sed -i "/^| T-MAAP-PROBE |/d" docs/architecture/08_timing.md' 1 || fails=$((fails+1))
  ids_probe family-miss     'echo "T-NOFAMILY-* timers" >> tb/tx_slots/README.md' 1 || fails=$((fails+1))
  ids_probe brace-miss      'echo "T-MRP-{JOIN, NOPE}" >> tb/tx_slots/README.md' 1 || fails=$((fails+1))
  ids_probe heading-gone    'sed -i "s/^## 7. Parameter master table (F01.5)/## 7. Parameters/" docs/architecture/01_overview.md' 1 || fails=$((fails+1))
  ids_probe f08-anchor-gone 'sed -i "s/<a id=\"fig-08-constants\"><\/a>//" docs/architecture/08_timing.md' 1 || fails=$((fails+1))
  ids_probe P-TX-revert     'sed -i "s/F01.5 P-TX-STD-SLOTS x 576 +/F01.5 \"P-TX 4x576 + 1600\":/" tb/tx_slots/sim_main.cpp' 1 || fails=$((fails+1))
  # leniency probes: recorded, not judged here (rc 0 means the gate lets it pass)
  ids_probe lenient-minus-n 'echo "P-TX-STD-SLOTS-7 is not a row" >> tb/tx_slots/README.md' 0 || fails=$((fails+1))
  ids_probe lenient-linebrk 'printf "a T-ADP-\nNOPE broken across lines\n" >> tb/tx_slots/README.md' 0 || fails=$((fails+1))
  echo "ids probes: $fails unexpected"; [ $fails = 0 ]
}
# ---- D: figure-gate fault probes --------------------------------------------
fig_probe() { # $1 = tag, $2 = plant, $3 = expected rc
  local d="$S/D-$1"; fresh "$d" $HEAD_SHA >/dev/null 2>&1; cd "$d" || return 99
  bash -c "$2"; python3 scripts/check-figures.py; local rc=$?
  echo "probe $1: rc=$rc want=$3"; [ "$rc" = "$3" ]
}
p_fig_probes() {
  local fails=0
  fig_probe png-restored  "git show $BASE_SHA:docs/diagrams/21-integration-faces.png > docs/diagrams/21-integration-faces.png" 1 || fails=$((fails+1))
  fig_probe png-in-src    'rsvg-convert -w 100 -o docs/diagrams/src/x.png docs/diagrams/20-rtl-dataflow.svg' 1 || fails=$((fails+1))
  fig_probe unlisted-svg  'cp docs/diagrams/20-rtl-dataflow.svg docs/diagrams/25-new.svg && echo "![x](../diagrams/25-new.svg)" >> docs/guides/README.md' 1 || fails=$((fails+1))
  fig_probe truncated     'head -c 500 docs/diagrams/22-aecp-descriptor-fetch.svg > t && mv t docs/diagrams/22-aecp-descriptor-fetch.svg' 1 || fails=$((fails+1))
  fig_probe image-inside  'sed -i "0,/<rect/s//<image href=\"x.png\" width=\"1\" height=\"1\"\/><rect/" docs/diagrams/23-bringup-decision.svg' 1 || fails=$((fails+1))
  fig_probe foreignobj    'sed -i "0,/<rect/s//<foreignObject width=\"1\" height=\"1\"\/><rect/" docs/diagrams/23-bringup-decision.svg' 1 || fails=$((fails+1))
  fig_probe no-viewbox    'sed -i "0,/ viewBox=\"[^\"]*\"/s///" docs/diagrams/24-adp-acmp-states.svg' 1 || fails=$((fails+1))
  fig_probe row-deleted   'sed -i "/^| \`24-adp-acmp-states.svg\`/d" docs/diagrams/README.md' 1 || fails=$((fails+1))
  fig_probe orphan-wd     'cp docs/diagrams/wavedrom/fig-02-rxwave.svg docs/diagrams/wavedrom/fig-99-orphan.svg' 1 || fails=$((fails+1))
  fig_probe unlinked      'grep -rl "24-adp-acmp-states.svg" --include=*.md . | grep -v docs/diagrams/README.md | xargs sed -i "s/24-adp-acmp-states.svg/24-adp-acmp-states.svgX/g"' 1 || fails=$((fails+1))
  fig_probe drawio-noexp  'git rm -q docs/diagrams/01-top-level.svg' 1 || fails=$((fails+1))
  fig_probe subdir-file   'mkdir -p docs/diagrams/wavedrom/old && cp docs/diagrams/wavedrom/fig-02-rxwave.svg docs/diagrams/wavedrom/old/' 1 || fails=$((fails+1))
  # .DS_Store is in the repo .gitignore: an ignored file is out of the gate's set by design
  fig_probe ignored-dotfile 'touch docs/diagrams/.DS_Store && git check-ignore -q docs/diagrams/.DS_Store' 0 || fails=$((fails+1))
  fig_probe tracked-dotfile 'touch docs/diagrams/.DS_Store && git add -f docs/diagrams/.DS_Store' 1 || fails=$((fails+1))
  fig_probe section-gone  'sed -i "s/^## Inventory (hand-authored SVG)/## Hand inventory/" docs/diagrams/README.md' 1 || fails=$((fails+1))
  # leniency probe: an <feImage> raster is not one of the two named elements
  fig_probe lenient-feimage 'sed -i "0,/<rect/s//<filter id=\"q\"><feImage href=\"data:image\/png;base64,AAAA\"\/><\/filter><rect/" docs/diagrams/23-bringup-decision.svg' 0 || fails=$((fails+1))
  echo "figure probes: $fails unexpected"; [ $fails = 0 ]
}
# ---- E: make check (the CI step) fails on planted faults, at the right target --
mc_probe() { # $1 = tag, $2 = plant, $3 = target expected to fail
  local d="$S/E-$1"; fresh "$d" $HEAD_SHA >/dev/null 2>&1; cd "$d" || return 99
  bash -c "$2"; make -k check > mc.out 2>&1; local rc=$?
  cat mc.out; echo "probe $1: make check rc=$rc"
  [ "$rc" != 0 ] && grep -q "$3" mc.out
}
p_mc_probes() {
  local fails=0
  mc_probe mermaid-broken 'sed -i "0,/^flowchart LR/s//flowchart LR\n  a[[[ unclosed/" docs/architecture/02_interfaces.md' 'MERMAID FAIL' || fails=$((fails+1))
  mc_probe stray-id       'echo "P-NOT-A-ROW" >> docs/guides/integrator.md' 'ID FAIL' || fails=$((fails+1))
  mc_probe png            "git show $BASE_SHA:docs/diagrams/20-rtl-dataflow.png > docs/diagrams/20-rtl-dataflow.png" 'FIGURE FAIL' || fails=$((fails+1))
  mc_probe wavedrom-edit  'sed -i "s/\"head\": {\"text\": \"no ready: every byte with rx_valid_i is taken\"}/\"head\": {\"text\": \"edited\"}/" docs/architecture/02_interfaces.md' 'WAVEDROM STALE' || fails=$((fails+1))
  echo "make check probes: $fails unexpected"; [ $fails = 0 ]
}
# ---- F: comment-only proof for the three hdl/tb code files -------------------
p_comment_only() {
  local fails=0
  mkdir -p "$S/F" && cd "$S/F" || return 99
  for f in hdl/packet_engine/KL_pp_trace_ring.sv hdl/packet_engine/KL_pp_tx_slots.sv tb/tx_slots/sim_main.cpp; do
    for v in base head; do
      sha=$BASE_SHA; [ $v = head ] && sha=$HEAD_SHA
      mkdir -p $v/$(dirname $f); git -C "$REPO" show $sha:$f > $v/$f
    done
    case $f in
      *.sv)  "$VERILATOR" -E -P base/$f > b.pp 2>b.err; "$VERILATOR" -E -P head/$f > h.pp 2>h.err ;;
      *.cpp) g++ -fpreprocessed -E -P base/$f > b.pp 2>b.err; g++ -fpreprocessed -E -P head/$f > h.pp 2>h.err ;;
    esac
    # second, independent method: a token stream with comments removed
    python3 - base/$f head/$f <<'EOF' > tok.out
import re, sys
def toks(p):
    t = open(p).read()
    t = re.sub(r'/\*.*?\*/', ' ', t, flags=re.S)
    t = re.sub(r'//[^\n]*', ' ', t)
    return t.split()
a, b = toks(sys.argv[1]), toks(sys.argv[2])
print('tokens', len(a), len(b), 'EQUAL' if a == b else 'DIFFER')
EOF
    s1=$(sha256sum < b.pp | cut -c1-16); s2=$(sha256sum < h.pp | cut -c1-16)
    same=DIFFER; cmp -s b.pp h.pp && [ -s b.pp ] && same=EQUAL
    echo "$f: preprocessed base=$s1 head=$s2 bytes=$(wc -c < h.pp) $same; $(cat tok.out)"
    [ $same = EQUAL ] && grep -q EQUAL tok.out || fails=$((fails+1))
  done
  echo "comment-only: $fails differing"; [ $fails = 0 ]
}
# ---- G: focused suites and lint for the touched modules (pinned Verilator) ----
p_suite() { # $1 = tb dir
  fresh "$S/G-$1" $HEAD_SHA && cd "$S/G-$1/tb/$1" && make VERILATOR="$VERILATOR" -j4
}
p_lint_touched() {
  fresh "$S/G-lint" $HEAD_SHA && cd "$S/G-lint" || return 99
  local fails=0
  for m in KL_pp_trace_ring KL_pp_tx_slots; do
    "$VERILATOR" --lint-only -Wall -Ihdl/common -Ihdl/packet_engine hdl/packet_engine/$m.sv --top-module $m && echo "lint $m OK" || fails=$((fails+1))
  done
  [ $fails = 0 ]
}

"$VERILATOR" --version > "$R/verilator-version.txt"
mmdc --version > "$R/mmdc-version.txt" 2>&1
python3 -c 'import wavedrom, importlib.metadata as m; print("wavedrom", m.version("wavedrom"))' > "$R/wavedrom-version.txt" 2>&1
run make_check_head p_make_check_head &
run ids_on_base     p_ids_on_base &
run ids_probes      p_ids_probes &
run fig_probes      p_fig_probes &
run mc_probes       p_mc_probes &
run comment_only    p_comment_only &
run suite_tx_slots  p_suite tx_slots &
run suite_side_port p_suite side_port &
run lint_touched    p_lint_touched &
wait
for f in "$R"/*.rc; do printf '%-22s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done | tee "$R/campaign-summary.txt"
