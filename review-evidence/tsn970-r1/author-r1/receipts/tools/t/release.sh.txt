#!/usr/bin/env bash
# release.sh CLONE OUT REV...: the AX7101 1x1 shipping (all-fabric) export with its software compiled, no Vivado (the
# launcher's dry run, its printed milan_soc.py command without --build), at each REV in turn in the one CLONE path, so
# no build path differs; then the sha256 of the release firmware (bios.bin, bios.elf, libmilan_baremetal.a), the
# disassembly of bios.elf and every gateware .v/.init file, per REV, in OUT/<rev>/IMAGES.sha256.
set -u
C=$1 O=$2; shift 2
PY=<litex>/venv/bin/python3
export PATH=<litex>/venv/bin:/usr/local/bin:/usr/bin:/bin:<sdk>/host/bin
for REV in "$@"; do
  W=$O/$REV; mkdir -p "$W"; cd "$C" || exit 3
  git -c advice.detachedHead=false checkout -q --detach "$REV" && git submodule update -q --init --force protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
  rm -rf "$C/export"
  echo "rev $(git rev-parse --short=8 HEAD) porcelain $(git status --porcelain --untracked-files=no | wc -l) start $(date +%T)" > "$W/RUN.txt"
  (cd sw/litex && REPO=$C bash ./build.sh ax7101 --dry-run) > "$W/dry-run.log" 2>&1
  REPO=$C WORK=$C/export LOG=$W "$PY" - <<'PYEOF'
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); log = Path(os.environ["LOG"])
lines = [l for l in (log / "dry-run.log").read_text().splitlines() if "exec python3 milan_soc.py " in l]
argv = shlex.split(lines[0].split("exec python3 ", 1)[1]); argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax7101")
(log / "argv.json").write_text(json.dumps(argv, indent=2))
with (log / "elaboration.log").open("w") as f:
    r = subprocess.run(["<litex>/venv/bin/python3", *argv], cwd=root / "sw/litex", stdout=f, stderr=subprocess.STDOUT)
(log / "elaboration.rc").write_text(f"{r.returncode}\n")
PYEOF
  (cd "$C/export" && find . \( -path '*/software/bios/bios.bin' -o -path '*/software/bios/bios.elf' -o -name 'libmilan_baremetal.a' -o -path '*/gateware/*.v' -o -path '*/gateware/*.init' \) | LC_ALL=C sort | xargs -r sha256sum) > "$W/IMAGES.sha256"
  OD=<sdk>/host/bin/riscv32-buildroot-linux-gnu-objdump
  for e in $(cd "$C/export" && find . -path '*/software/bios/bios.elf' | LC_ALL=C sort); do
    "$OD" -d --no-show-raw-insn "$C/export/$e" | tail -n +3 | sha256sum | sed "s#-#$e (disassembly)#"
  done >> "$W/IMAGES.sha256"
  for v in $(cd "$C/export" && find . -path '*/gateware/*.v' | LC_ALL=C sort); do
    grep -v -E '^\s*//' "$C/export/$v" | sha256sum | sed "s#-#$v (outside its // comment lines)#"
    grep -E '^\s*//' "$C/export/$v" | head -40 > "$W/$(basename $v).comments.txt"
  done >> "$W/IMAGES.sha256"
  for a in $(cd "$C/export" && find . -name 'libmilan_baremetal.a' | LC_ALL=C sort); do
    d=$(mktemp -d); (cd "$d" && <sdk>/host/bin/riscv32-buildroot-linux-gnu-ar x "$C/export/$a" && sha256sum * | sed "s#  #  $a member #")
    rm -rf "$d"
  done >> "$W/IMAGES.sha256"
  echo "end $(date +%T) files $(wc -l < "$W/IMAGES.sha256") elaboration rc $(cat $W/elaboration.rc)" >> "$W/RUN.txt"
done
git -C "$C" checkout -q -- configs sw/builder 2>/dev/null; git -C "$C" clean -q -fd configs/generated sw/builder/out 2>/dev/null
