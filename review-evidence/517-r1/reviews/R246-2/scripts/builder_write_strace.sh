#!/bin/sh
# R246-2: trace the exact generator commands sim_nxn.cpp:run_the_image_generators
# issues (same relative argv, run from tb/verilator/milan_dp, private mkdtemp dir)
# for the three sim_nxn configs, and list every path opened for writing, created,
# renamed or removed OUTSIDE the private directory. Used at a checkout that has
# no built models (the merged tree), where a full leg cannot run.
# Usage: builder_write_strace.sh <tree> <out-dir>
set -eu
tree=$1; out=$2; mkdir -p "$out"
cd "$tree/tb/verilator/milan_dp"
for cfg in endstation_ax7101_8x8 endstation_arty_4x4 endstation_ax7101_1x1_tdm8; do
  d=$(mktemp -d "${TMPDIR:-/tmp}/milan_nxn_XXXXXX")
  strace -f --seccomp-bpf -qq -y -s 4096 -e signal=none \
    -e trace=open,openat,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,unlinkat,rmdir,link,linkat,symlink,symlinkat,truncate,chmod,fchmodat,utimensat,chdir \
    -o "$out/$cfg.strace" sh -c "
      python3 ../../../sw/builder/endstation_builder.py '../../../configs/$cfg.yaml' -o '$d/builder' > '$d/generator.log' 2>&1 &&
      python3 ../../../avdecc/gen_aemi_image.py --overlay '$d/builder/$cfg/aem_overlay.json' -o '$d/image.bin' --json '$d/image.json' --line-bytes 576 > '$d/generator.log' 2>&1"
  echo "$cfg rc=$? private_files=$(find "$d" -type f | wc -l)"
  python3 - "$out/$cfg.strace" "$d" <<'EOF'
import re, sys
trace, private = sys.argv[1], sys.argv[2]
bad = set()
for raw in open(trace, errors="replace"):
    m = re.match(r"^\d+\s+(\w+)\((.*)\)\s+=\s+(-?\d+)(<[^>]*>)?", raw)
    if not m or int(m.group(3)) < 0:
        continue
    call, args, _ret, fdp = m.groups()
    if call == "chdir":
        bad.add("CHDIR " + args)
        continue
    if call in ("open", "openat") and not re.search(r"O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND", args):
        continue
    target = fdp[1:-1] if fdp else (re.findall(r'"([^"]*)"', args) or ["?"])[0]
    if target.startswith(("/dev/", "pipe:")) or target.startswith(private) or "milan_nxn_" in target or "milan_nxn_" in args:
        continue
    bad.add(f"{call} {target}")
print("  writes outside private dir:", sorted(bad) if bad else "NONE")
EOF
  rm -rf "$d"
done
