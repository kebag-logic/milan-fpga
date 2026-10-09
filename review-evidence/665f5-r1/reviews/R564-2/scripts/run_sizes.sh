#!/usr/bin/env bash
# Link the opt-in AECP size fixture at two heads with one identical reviewer stub runtime.
# Usage: run_sizes.sh <packet> ; trees: scratch/tree (round-2 head), scratch/tree-r1 (round-1 head)
P=$1; S=$P/scratch/size
export MILAN_RV32_CC=$P/scratch/sdk/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc PYTHONDONTWRITEBYTECODE=1
pids=()
for head in tree tree-r1; do for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do for n in 1 2; do
  out=$S/$head-$shape-if$n; rm -rf "$out"; mkdir -p "$out"
  ( cd $P/scratch/$head && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --with-aecp --config configs/$shape.yaml \
      --output "$out" --interfaces $n --libc $S/libstubc.a --compiler-runtime $S/libstubrt.a > "$out.log" 2>&1; echo $? > "$out.rc" ) &
  pids+=($!)
done; done; done
wait "${pids[@]}"
python3 -I - "$S" <<'PY'
import json,sys,pathlib
S=pathlib.Path(sys.argv[1]); rows={}
for head in ("tree-r1","tree"):
    for shape in ("endstation_ax7101_1x1_tdm8","endstation_ax7101_8x8"):
        for n in (1,2):
            p=S/f"{head}-{shape}-if{n}"/"size.json"; rc=(S/f"{head}-{shape}-if{n}.rc").read_text().strip()
            r=json.loads(p.read_text()) if p.exists() else None
            rows[head,shape,n]=r
            sec=r["sections"] if r else {}
            print(head,shape,n,"rc",rc,"span",r and r["ram_span"],{k:sec.get(k) for k in (".text",".rodata",".data",".bss",".stack")})
print("delta round2-round1 (same stub runtime):")
for shape in ("endstation_ax7101_1x1_tdm8","endstation_ax7101_8x8"):
    for n in (1,2):
        a,b=rows["tree-r1",shape,n],rows["tree",shape,n]
        if a and b: print(shape,n,"span delta",b["ram_span"]-a["ram_span"],
              {k:b["sections"].get(k,0)-a["sections"].get(k,0) for k in (".text",".rodata",".data",".bss")})
PY
