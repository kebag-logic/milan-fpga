#!/usr/bin/env python3
"""[R316] R316-2 dump harness: writes the census stub headers and W-series sources for issue #544 / PR #558.

Runs the real gate 1b `assert_boot_contract` of sw/builder/test_builder.py
(at the checkout's HEAD, or at a named base commit with --base) over a set
of reviewer-written firmware variants, in one of two compiler modes:

  sdk     the pinned RV32 SDK, verified by scripts/ci_rv32_sdk.py, mapped
          onto the settled absolute selector's argv[0] only
  absent  every cross candidate hidden; host compilers may only answer
          --version and the RV32 probe

--disable NAME replaces one closure cell of assert_boot_contract with a
no-op, as a disconnected-check control.

Run from the root of the checkout under review:
  python3 probe.py sdk|absent --sdk DIR [--base SHA] [--disable NAME] --out FILE
"""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=("sdk", "absent"))
parser.add_argument("--sdk", type=Path)
parser.add_argument("--base")
parser.add_argument("--disable")
parser.add_argument("--only", action="append")
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--scratch", type=Path, required=True)
args = parser.parse_args()

root = Path.cwd()
sys.path.insert(0, str(root / "sw/builder"))
import test_firmware_compiler as tfc  # noqa: E402

destination = args.sdk if args.mode == "sdk" else None
if destination is not None:
    tfc.sdk.verify(destination)

path = root / "sw/builder/test_builder.py"
if args.base:
    source = subprocess.run(["git", "show", f"{args.base}:sw/builder/test_builder.py"],
                            check=True, capture_output=True, text=True).stdout
else:
    source = path.read_text()
marker = "    subset_note = assert_subset_refuses()\n"
assert source.count(marker) == 1, "hook marker not unique"
source = source.replace(marker, "    reviewer_hook(locals())\n    return\n" + marker)

READ = "\tuint32_t id = milan_read(MILAN_ID);\n"
GUARD = "\tif (id != MILAN_ID_MAGIC) {\n"
AFTER_GUARD = "\t/* PHC and fabric gPTP are live from reset, independent of the AEM gate. */\n"
STATIC = "static int aem_loaded;"
FORGE = "#define MILAN_FORGE(x) ((x) = MILAN_ID_MAGIC)"


def edit(fw: str, defines: str = "", before_guard: str = "",
         after_guard: str = "", replace: tuple[str, str] | None = None) -> str:
    out = fw
    if defines:
        assert out.count(STATIC) == 1
        out = out.replace(STATIC, defines + "\n\n" + STATIC)
    if before_guard:
        assert out.count(GUARD) == 1
        out = out.replace(GUARD, before_guard + GUARD)
    if after_guard:
        assert out.count(AFTER_GUARD) == 1
        out = out.replace(AFTER_GUARD, after_guard + AFTER_GUARD)
    if replace:
        assert out.count(replace[0]) == 1, replace[0]
        out = out.replace(*replace)
    return out


CLOBBER_ASM = ('\t__asm__ volatile("li s0, 0x4d494c4e\\n\\tli s1, 0x4d494c4e\\n\\t'
               'li s2, 0x4d494c4e\\n\\tli s3, 0x4d494c4e\\n\\tli s4, 0x4d494c4e\\n\\t'
               'li s5, 0x4d494c4e\\n\\tli s6, 0x4d494c4e\\n\\tli s7, 0x4d494c4e\\n\\t'
               'li s8, 0x4d494c4e\\n\\tli s9, 0x4d494c4e\\n\\tli s10, 0x4d494c4e\\n\\t'
               'li s11, 0x4d494c4e");\n')
CLOBBER_FN = ("static void __attribute__((noinline)) milan_settle(void)\n{\n"
              + CLOBBER_ASM + "}")
DIAG_FN = ("static int __attribute__((noinline)) milan_diag(const char *format, ...)\n{\n"
           "\t(void)format;\n" + CLOBBER_ASM + "\treturn 0;\n}\n#define printf milan_diag")


def cases(fw: str) -> list[tuple[str, str, str]]:
    """(id, description, firmware). Expectations are stated in REPORT.md."""
    return [
        # ---- legitimate shapes the decision authorizes (controls) ----
        ("N01", "extra diagnostic printf with a complete (unsigned long)id argument",
         edit(fw, "", '\tprintf("again %08lx\\n", (unsigned long)id);\n')),
        ("N02", "discarded mask with an ull-suffixed hex literal",
         edit(fw, "", "\t(void)(id & 0x1ull);\n")),
        ("N03", "discarded mask split across lines",
         edit(fw, "", "\t(void)(\n\t\tid & 1u\n\t);\n")),
        # ---- rvalue shapes outside a call the delimiter check may admit ----
        ("N04", "cast argument of __alignof (not a call)",
         edit(fw, "", "\t(void)__alignof((unsigned long)id);\n")),
        ("N05", "cast argument of __builtin_constant_p",
         edit(fw, "", "\t(void)__builtin_constant_p((unsigned long)id);\n")),
        ("N06", "cast argument of __typeof in a block-scope declaration",
         edit(fw, "", "\t{\n\t\t__typeof((unsigned long)id) milan_t = 0;\n\t\t(void)milan_t;\n\t}\n")),
        # ---- hostile near misses on the two shapes ----
        ("N07", "authorized argument followed by an assigning argument",
         edit(fw, "", '\tprintf("%lu", (unsigned long)id, id = MILAN_ID_MAGIC);\n')),
        ("N08", "discarded mask after a label",
         edit(fw, "", "milan_l:\n\t(void)(id & 1u);\n")),
        ("N09", "discarded mask with a character literal",
         edit(fw, "", "\t(void)(id & 'a');\n")),
        ("N10", "cast argument through a parenthesized callee",
         edit(fw, "", '\t(printf)("%lu", (unsigned long)id);\n')),
        ("N11", "cast argument after a comma operator in a nested paren",
         edit(fw, "", '\tprintf("%lu", (0, (unsigned long)id));\n')),
        ("N12", "cast argument of __builtin_choose_expr hidden behind a call",
         edit(fw, "", '\tprintf("%lu", __builtin_choose_expr(1, (unsigned long)id, 0ul));\n')),
        ("N13", "compound assignment to a cast argument",
         edit(fw, "", '\tprintf("%lu", (unsigned long)id += 1);\n')),
        ("N14", "discarded mask whose statement is the body of an if",
         edit(fw, "", "\tif (1) (void)(id & 1u);\n")),
        ("N15", "discarded mask whose statement follows a closing initializer brace",
         edit(fw, "", "\tuint32_t milan_a[1] = {0};\n\t(void)milan_a;\n\t(void)(id & 1u);\n")),
        # ---- escapes elsewhere in the unit (register diagnostic copy) ----
        ("E01", "address in sizeof after the guard",
         edit(fw, "", after_guard="\t(void)sizeof(&id);\n")),
        ("E02", "address in the unselected arm of __builtin_choose_expr after the guard",
         edit(fw, "", after_guard="\t(void)__builtin_choose_expr(0, &id, 0);\n")),
        ("E03", "address in an unselected _Generic association after the guard",
         edit(fw, "", after_guard="\t(void)_Generic(0, char: &id, int: 0);\n")),
        ("E04", "address in __typeof__ after the guard",
         edit(fw, "", after_guard="\t{\n\t\t__typeof__(&id) milan_p = 0;\n\t\t(void)milan_p;\n\t}\n")),
        ("E05", "address via __builtin_memcpy source after the guard",
         edit(fw, "", after_guard="\t{\n\t\tuint32_t milan_c;\n\t\t__builtin_memcpy(&milan_c, &id, 4);\n\t\t(void)milan_c;\n\t}\n")),
        # ---- writes that name nothing in the interval ----
        ("W01", "call to a helper whose asm overwrites every callee-saved register",
         edit(fw, CLOBBER_FN, "\tmilan_settle();\n")),
        ("W02", "function-like macro invoked with the sample expands to the clobbering helper",
         edit(fw, CLOBBER_FN + "\n#define MILAN_FORGE(x) milan_settle()", "\tMILAN_FORGE(id);\n")),
        ("W03", "printf redefined to a clobbering helper; production diagnostic unchanged",
         edit(fw, DIAG_FN)),
        ("W04", "helper call alone, no asm (control for W01)",
         edit(fw, "static void __attribute__((noinline)) milan_settle(void)\n{\n}", "\tmilan_settle();\n")),
        ("W05", "store through the frame address in the interval",
         edit(fw, "", "\t((volatile uint32_t *)__builtin_frame_address(0))[-1] = MILAN_ID_MAGIC;\n")),
        # ---- plain (no macro) forms: compiler-free coverage measurement ----
        ("A01", "plain *(__extension__ &(id)) = MAGIC (R316-1 C09)",
         edit(fw, "", "\t*(__extension__ &(id)) = MILAN_ID_MAGIC;\n")),
        ("A02", "plain asm output operand (R316-1 C11)",
         edit(fw, "", '\t__asm__ volatile("li %0, 0x4d494c4e" : "=r"(id));\n')),
        ("A03", "plain __builtin_choose_expr lvalue",
         edit(fw, "", "\t__builtin_choose_expr(1, id, id) = MILAN_ID_MAGIC;\n")),
        ("A04", "plain _Generic lvalue",
         edit(fw, "", "\t_Generic(0, int: id) = MILAN_ID_MAGIC;\n")),
        ("A05", "plain __real__ lvalue",
         edit(fw, "", "\t(__real__ id) = MILAN_ID_MAGIC;\n")),
        ("A06", "plain __extension__ lvalue",
         edit(fw, "", "\t(__extension__ id) = MILAN_ID_MAGIC;\n")),
        ("A07", "plain asm tied output",
         edit(fw, "", '\t__asm__ volatile ("" : "=r"(id) : "0"(MILAN_ID_MAGIC));\n')),
        ("A08", "plain __builtin_memcpy into &(id)",
         edit(fw, "", "\t__builtin_memcpy(&(id), &(uint32_t){MILAN_ID_MAGIC}, 4);\n")),
        ("A09", "plain (id)++ repeated to the magic is not needed: (id) |= MAGIC",
         edit(fw, "", "\t(id) |= MILAN_ID_MAGIC;\n")),
        ("A10", "plain comma-expression lvalue: (0, id) is not an lvalue; use *(&(id)+0)",
         edit(fw, "", "\t*(&(id) + 0) = MILAN_ID_MAGIC;\n")),
    ]


results = []


def reviewer_hook(ns: dict) -> None:
    """Write the census stub headers and the W-series firmware for a real-flag compile."""
    fw = ns["firmware_source"]
    dump = args.out.with_suffix("")
    dump.mkdir(parents=True, exist_ok=True)
    ns["census_headers"](dump)
    (dump / "production.c").write_text(fw)
    for cid, label, firmware in cases(fw):
        if cid in ("W01", "W02", "W03", "W04"):
            (dump / f"{cid}.c").write_text(firmware)
    results.append(dict(dump=str(dump)))


args.scratch.mkdir(parents=True, exist_ok=True)
audit_path = args.out.with_suffix(".argv.jsonl")
with audit_path.open("w") as stream:
    audit = tfc.CompilerAudit(stream, destination)
    argv = [str(path)] + (["--require-rv32"] if destination else [])
    module = types.ModuleType("r316_2_probe")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    module.reviewer_hook = reviewer_hook
    with patch.object(subprocess, "run", side_effect=audit.invoke), \
            patch.object(sys, "argv", argv):
        exec(compile(source, str(path), "exec"), module.__dict__)
        with tempfile.TemporaryDirectory(prefix="r316-2-", dir=args.scratch) as tmp:
            module.OUT = Path(tmp)
            module.test_baremetal_profile_contract()
    summary = dict(mode=args.mode, base=args.base, disable=args.disable,
                   compiles=audit.compiles, hidden=sorted(audit.hidden),
                   results=results)
    if destination is None:
        assert audit.compiles == 0, "absent mode compiled firmware"
    args.out.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"AUDIT mode={args.mode} base={args.base} disable={args.disable} "
          f"compiles={audit.compiles}", flush=True)
