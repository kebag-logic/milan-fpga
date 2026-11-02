#!/bin/sh
# The sweep as committed at fd12faf9, run on the e90284bd page, to reproduce the
# PR's "64 on shipping, 256 on 2x2" baseline. The tree copy is under PACKET/scratch.
# Usage: run_fd12_sweep.sh CLONE PACKET PYTHON
set -u
C=$1; P=$2; PY=$3
S=$P/scratch; R=$P/receipts/probes; mkdir -p "$R"
export PATH="$P/bin:$PATH"
rm -rf "$S/sweep_fd12"; rsync -a --exclude=.git "$C/" "$S/sweep_fd12/"
cd "$C" || exit 2
git show fd12faf9:scripts/register_read_sweep.py > "$S/sweep_fd12/scripts/register_read_sweep.py"
git show e90284bd:docs/reference/REGISTER_MAP.md > "$S/page_e90284bd.md"
git diff --quiet fd12faf9 HEAD -- hdl/common/csr/milan_csr.sv configs/generated && echo "rtl unchanged since fd12faf9"
"$PY" "$S/sweep_fd12/scripts/register_read_sweep.py" --page "$S/page_e90284bd.md" --work "$S/w_fd12" \
    > "$R/sweep_fd12_on_e90284bd.log" 2>&1
echo $? > "$R/sweep_fd12_on_e90284bd.rc"
grep '^DISAGREE' "$R/sweep_fd12_on_e90284bd.log" | cut -d' ' -f2,3 | sort | uniq -c
grep '17 tables' "$R/sweep_fd12_on_e90284bd.log"
