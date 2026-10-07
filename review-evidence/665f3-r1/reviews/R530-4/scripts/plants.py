#!/usr/bin/env python3
"""Reviewer plants for #665 F3 round 5: each mutant is a single textual replacement in a disposable copy of the
tree (git archive of the head); the self-test must fail (exit != 0) for every helper or audit plant."""
import concurrent.futures, os, shutil, subprocess, sys
from pathlib import Path

PKT = Path(sys.argv[1]); REPO = Path(sys.argv[2]); CC = sys.argv[3]
BASE = PKT / "scratch/plant-base"
ARITH = "sw/firmware/ctrl/test/rv32_image/image_arith.c"
IMG = "sw/firmware/ctrl/test/ctrl_image.py"
PLANTS = [
    ("C00-control-unplanted", ARITH, "i < 64u", "i < 64u"),
    ("H01-udiv32-strict-compare", ARITH, "\t\tif (r >= d) {\n\t\t\tr -= d;\n\t\t\tq |= 1u;\n\t\t}\n\t}\n\t*rem = r;\n\treturn q;\n}\n\nstatic uint64_t",
     "\t\tif (r > d) {\n\t\t\tr -= d;\n\t\t\tq |= 1u;\n\t\t}\n\t}\n\t*rem = r;\n\treturn q;\n}\n\nstatic uint64_t"),
    ("H02-udiv64-63-steps", ARITH, "i < 64u", "i < 63u"),
    ("H03-mulsi3-or", ARITH, "p += a & (0u - (b & 1u));", "p |= a & (0u - (b & 1u));"),
    ("H04-muldi3-no-carry", ARITH, "hi += (xhi & m) + (lo < add ? 1u : 0u);", "hi += (xhi & m);"),
    ("H05-divsi3-sign", ARITH, "return (int32_t)((a < 0) != (b < 0) ? 0u - q : q);", "return (int32_t)((a < 0) ? 0u - q : q);"),
    ("H06-modsi3-sign", ARITH, "return (int32_t)(a < 0 ? 0u - r : r);", "return (int32_t)(b < 0 ? 0u - r : r);"),
    ("H07-divdi3-sign", ARITH, "return (int64_t)((a < 0) != (b < 0) ? 0u - q : q);", "return (int64_t)((b < 0) ? 0u - q : q);"),
    ("H08-moddi3-sign", ARITH, "return (int64_t)(a < 0 ? 0u - r : r);", "return (int64_t)(r);"),
    ("H09-lshrdi3-boundary", ARITH, "\tif (b >= 32) {\n\t\tlo = hi >> (b - 32);", "\tif (b > 32) {\n\t\tlo = hi >> (b - 32);"),
    ("H10-ashldi3-carry-bits", ARITH, "hi = (hi << b) | (lo >> (32 - b));", "hi = (hi << b) | (lo >> (31 - b));"),
    ("H11-ashrdi3-no-sign-fill", ARITH, "hi >>= 31;", "hi = 0;"),
    ("H12-umoddi3-returns-quotient", ARITH, "\tuint64_t r;\n\t(void)image_udivmod64(a, b, &r);\n\treturn r;", "\tuint64_t r;\n\treturn image_udivmod64(a, b, &r);"),
    ("H13-udivsi3-rem-off", ARITH, "\t\tr = (r << 1) | (n >> 31);", "\t\tr = (r << 1) | ((n >> 31) & (r & 1u));"),
    ("H14-abs64-unsigned", ARITH, "return v < 0 ? 0u - (uint64_t)v : (uint64_t)v;", "return (uint64_t)v;"),
    ("A01-audit-accepts-M", IMG, "return funct7 == 0 or (funct7 == 0x20 and funct3 in (0, 5))", "return funct7 in (0, 1) or (funct7 == 0x20 and funct3 in (0, 5))"),
    ("A02-audit-ignores-eflags", IMG, "    if flags:\n        named", "    if False:\n        named"),
    ("A03-audit-no-open-symbols", IMG, "    if undefined:\n        found.append(f\"symbols left undefined", "    if False:\n        found.append(f\"symbols left undefined"),
    ("A04-measure-skips-audit", IMG, "    if findings:\n        raise Refusal(f\"the image at", "    if False:\n        raise Refusal(f\"the image at"),
    ("A05-leaf-ignores-calls", IMG, "    if calls:\n        found.append", "    if False:\n        found.append"),
    ("A06-arch-prefix", IMG, 're.fullmatch(r"rv32i\\d+p\\d+", arches[0])', 're.match(r"rv32i\\d+p\\d+", arches[0])'),
]

def one(plant):
    name, rel, old, new = plant
    tree = PKT / "scratch/plants" / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(BASE, tree, symlinks=True)
    f = tree / rel
    text = f.read_text()
    if text.count(old) != 1:
        return name, "PLANT-TEXT-NOT-FOUND-ONCE", ""
    f.write_text(text.replace(old, new))
    env = dict(os.environ, MILAN_RV32_CC=CC)
    res = subprocess.run([sys.executable, str(tree / "sw/firmware/ctrl/test/ctrl_image_selftest.py"), "--require-rv32"],
                         capture_output=True, text=True, env=env, cwd=tree)
    out = res.stdout + res.stderr
    (PKT / "receipts/plants").mkdir(parents=True, exist_ok=True)
    (PKT / f"receipts/plants/{name}.log").write_text(out + f"\nrc={res.returncode}\n")
    last = [l for l in out.splitlines() if l.strip()][-1] if out.strip() else ""
    return name, ("PASSED" if res.returncode == 0 else "FAILED") if name.startswith("C00") else ("CAUGHT" if res.returncode != 0 else "ESCAPED"), f"rc={res.returncode} {last[:200]}"

if __name__ == "__main__":
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)
    arc = subprocess.run(["git", "-C", str(REPO), "archive", "HEAD"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(BASE)], input=arc, check=True)
    for sub in ("gptp-processor", "protocol-processor", "third_party/verilog-axis"):
        shutil.rmtree(BASE / sub, ignore_errors=True)
        shutil.copytree(REPO / sub, BASE / sub, symlinks=True, ignore=shutil.ignore_patterns(".git"))
    only = sys.argv[4:]
    if only:
        PLANTS[:] = [p for p in PLANTS if p[0] in only]
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:
        results = list(ex.map(one, PLANTS))
    for name, verdict, detail in results:
        print(f"{verdict:<10} {name}: {detail}")
    sys.exit(0 if all(v in ("CAUGHT", "PASSED") for _, v, _ in results) else 1)
