#!/usr/bin/env python3
"""Reproduce the merged README selector error with absent and competing defaults."""
import argparse,os,sys
from pathlib import Path
from unittest.mock import patch
p=argparse.ArgumentParser();p.add_argument("--repo",required=True,type=Path);p.add_argument("--out",required=True,type=Path);a=p.parse_args()
sys.path.insert(0,str(a.repo.resolve()/"sw/firmware/gtest"));import fw_rv32
out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
for name in ("riscv64-elf-gcc","fallback-gcc"):
 f=out/name;f.write_text("#!/bin/sh\nexit 0\n");f.chmod(0o755)
requested=str(out/"riscv64-elf-gcc");fallback=str(out/"fallback-gcc")
recipe=(a.repo/"sw/firmware/ctrl/maap/README.md").read_text().splitlines()[154]
assert recipe.startswith("CTRL_RV32_CC=riscv64-elf-gcc "),recipe
print("Exact-head README:155:",recipe)
for candidates in ((),(fallback,)):
 with patch.dict(os.environ,{"PATH":str(out),"CTRL_RV32_CC":"riscv64-elf-gcc"},clear=True),patch.object(fw_rv32,"CANDIDATES",candidates):
  got=fw_rv32.compiler()
  assert got==(fallback if candidates else None)
  print("Documented selector with",("competing default" if candidates else "no default"),"=>",("fallback-gcc" if got else "NO COMPILER"))
  os.environ["MILAN_RV32_CC"]="riscv64-elf-gcc"
  got=fw_rv32.compiler();assert got==requested
  print("Supported selector => requested riscv64-elf-gcc")
print("REPRODUCED: the executable README override does not choose the specified compiler")
