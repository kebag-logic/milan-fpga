#!/usr/bin/env bash
# Run the docs workflow's static gate commands, and the static rtl-fast/elaborate commands, concurrently in a disposable copy.
# One log and rc per command. Usage: run_gates3.sh COPY OUTDIR BASE
set -u
copy=$1; out=$2; base=$3; mkdir -p "$out"
cmds=$(python3 - "$copy" "$base" <<'PY'
import sys, yaml, re
copy, base = sys.argv[1:3]
skip = ("pip install", "ci_install_cache", "ci_rv32_sdk", "ci_runtime_evidence", "ci_gate_receipts", "test_firmware_compiler",
        "test_builder", "ci_builder_legs", "act_ci", "ci_fail_fast.py ", "gen_hdl_reference.py \\", "gen_wavedrom", "make -C", "ci_case",
        "check_diagram_pngs", "check_gptp_docs.py --with-submodule", "iob_pack", "ci_suite_", "ci_maap_", "ci_capture_", "ci_make_")
seen = []
for wf, jobs in (("docs", None), ("rtl-fast", None), ("elaborate", None)):
    d = yaml.safe_load(open(f"{copy}/.github/workflows/{wf}.yml"))
    for j, v in d["jobs"].items():
        for s in v.get("steps", []):
            for line in str(s.get("run", "")).split("\n"):
                c = line.strip()
                if c.startswith("python3 ") and "\\" not in c and "$" not in c and not any(k in c for k in skip) and c not in seen:
                    seen.append(c)
seen.append(f"python3 scripts/check_em_dash.py --base {base}")
print("\n".join(seen))
PY
)
i=0
while IFS= read -r c; do
  i=$((i+1)); n=$(printf '%03d' $i)
  ( cd "$copy" && echo "\$ $c" > "$out/$n.log" && timeout 500 bash -c "$c" >> "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" ) &
  while [ "$(jobs -rp | wc -l)" -ge 16 ]; do wait -n; done
done <<< "$cmds"
wait
for f in "$out"/*.rc; do n=$(basename "$f" .rc); printf '%s\trc=%s\t%s\n' "$n" "$(cat "$f")" "$(head -1 "$out/$n.log" | cut -c3-)"; done
