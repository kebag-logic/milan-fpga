#!/usr/bin/env bash
# Reproduces the R726-2 checks. Usage: r726_2_probe.sh <clone at 4f3ebffb> <out dir> <pinned sv2v v0.0.12>
set -u
C=$1; O=$2; SV2V_BIN=$3; mkdir -p "$O"; cd "$C" || exit 2
test "$(git rev-parse HEAD)" = 4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020 || { echo "wrong head"; exit 2; }
git diff --raw ca39dc1b0bd917e3e033df9d9db762514318377a HEAD > "$O/delta_raw.txt"
SV2V=$SV2V_BIN YOSYS=$(command -v yosys) python3 sw/mailbox/publication_census.py --check --jobs 6 > "$O/census_check.log" 2>&1; echo $? > "$O/census_check.rc"
python3 sw/mailbox/gen_mailbox.py --check > "$O/gen_mailbox_check.log" 2>&1; echo $? > "$O/gen_mailbox_check.rc"
python3 -I -c "import sys,collections; sys.path.insert(0,'sw/mailbox'); import publication_census as p; print(collections.Counter(r.kind for r in p.CENSUS.values())); print(len({n for n,_ in p.CENSUS}),'read nets'); print(len(p.CLASS_D_PORTS),'class-D ports')" > "$O/census_kinds.txt"
for c in docs_check check_hygiene check_doc_paths; do a=; [ $c = check_hygiene ] && a=--check; python3 scripts/$c.py $a > "$O/$c.log" 2>&1; echo "rc=$?" > "$O/$c.rc"; done
awk 'length>80 && /^#/{print NR": "length}' sw/mailbox/mailbox.yaml > "$O/yaml_long_comment_lines.txt"
