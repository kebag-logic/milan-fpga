#!/bin/sh
# Reproduce the R249-3 focused receipts in a disposable copy of the head.
# Usage: run-focused.sh <disposable tree at e122f330> <receipt dir>
# Needs Verilator 5.050 first on PATH, python3 with PyYAML, and for the
# TOC/em-dash gates a python with the pinned Markdown renderer as $MDPY.
set -u
T=$1
R=$2
MDPY=${MDPY:-python3}
cd "$T" || exit 2
t() { name=$1; shift; /usr/bin/time -f 'WALL %e s' "$@" > "$R/$name" 2>&1; echo "exit $?" >> "$R/$name"; }
t 01_pp_shadow_default.log make -C tb/verilator/pp_shadow
t 02_csr_default.log make -C tb/verilator/csr
for d in pp_shadow/obj_vid73 pp_shadow/obj_crf csr/obj_reset pp_shadow/obj_dir csr/obj_dir; do
  echo "== $d"; tr ' ' '\n' < tb/verilator/$d/V*__ver.d | grep svh
done > "$R/03_include_resolution.txt"
t 05_nvm_cosim_quick.log make -C tb/verilator/nvm_cosim quick JOBS=8 POOL=8
t 06_nvm_cosim_full.log make -C tb/verilator/nvm_cosim run JOBS=8 POOL=8
t 09_check_py_idiom.py.log python3 scripts/check_py_idiom.py
t 09_check_cpp_idiom.py.log python3 scripts/check_cpp_idiom.py
t 10_doc_style.log python3 scripts/check_doc_style.py
t 11_doc_paths.log python3 scripts/check_doc_paths.py
t 12_gen_toc.log "$MDPY" scripts/gen_toc.py --check
t 13_em_dash.log "$MDPY" scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7
git diff -U0 7463ab08 e122f330 -- '*.sv' '*.cpp' | grep -E '^[+-][^+-]' | grep -vE '^[+-]\s*//' \
  > "$R/14_comment_only.txt"; echo "exit(grep) $? (1 = every changed line is a comment)" >> "$R/14_comment_only.txt"
