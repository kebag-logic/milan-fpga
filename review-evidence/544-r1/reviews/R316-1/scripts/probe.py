#!/usr/bin/env python3
"""[R316] R316-1 probe harness for issue #544 / PR #558.

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


def cases(fw: str) -> list[tuple[str, str, str]]:
    """(id, description, firmware). Expectations are stated in REPORT.md."""
    s3_old = ('\treturn 1;\n#else\n\tprintf("Milan baremetal: no QSPI AEM slot; '
              'entity disabled.\\n");\n\treturn 0;\n#endif\n}')
    mismatch = ("\t\tprintf(\"Milan baremetal: CSR identity mismatch; "
                "fabric remains disabled.\\n\");\n")
    c18 = edit(fw, "", "\tif (milan_alias)\n\t\t*milan_alias = MILAN_ID_MAGIC;\n",
               replace=(READ, "\tuint32_t *milan_alias = 0;\nmilan_again:;\n" + READ))
    assert c18.count(mismatch) == 1
    c18 = c18.replace(mismatch, mismatch + "\t\tif (!milan_alias) {\n\t\t\tmilan_alias = &id;"
                      "\n\t\t\tgoto milan_again;\n\t\t}\n")
    return [
        ("C01", "published R272 macro x = MILAN_ID_MAGIC before guard",
         edit(fw, "#define MILAN_FORGE(x) x = MILAN_ID_MAGIC", "\tMILAN_FORGE(id);\n")),
        ("C02", "published R273 macro ((x) = MILAN_ID_MAGIC) before guard",
         edit(fw, FORGE, "\tMILAN_FORGE(id);\n")),
        ("C03", "header token paste __CONCAT(i, d) = MILAN_ID_MAGIC before guard",
         edit(fw, "", "\t__CONCAT(i, d) = MILAN_ID_MAGIC;\n")),
        ("C04", "local ## paste macro MILAN_CAT(i, d) = MILAN_ID_MAGIC",
         edit(fw, "#define MILAN_CAT(a, b) a##b", "\tMILAN_CAT(i, d) = MILAN_ID_MAGIC;\n")),
        ("C05", "local macro builds the sample through header __CONCAT(a, d)",
         edit(fw, "#define MILAN_FORGE2(a) __CONCAT(a, d) = MILAN_ID_MAGIC",
              "\tMILAN_FORGE2(i);\n")),
        ("C06", "macro takes the address and writes: *&(x) = MAGIC",
         edit(fw, "#define MILAN_FORGE(x) (*&(x) = MILAN_ID_MAGIC)", "\tMILAN_FORGE(id);\n")),
        ("C07", "macro sets a pointer alias, then a write through the alias",
         edit(fw, "#define MILAN_ALIAS(x) uint32_t *milan_alias = &(x)",
              "\tMILAN_ALIAS(id);\n\t*milan_alias = MILAN_ID_MAGIC;\n")),
        ("C08", "macro takes the address behind __extension__ and writes",
         edit(fw, "#define MILAN_FORGE(x) (*(__extension__ &(x)) = MILAN_ID_MAGIC)",
              "\tMILAN_FORGE(id);\n")),
        ("C09", "no macro: *(__extension__ &(id)) = MAGIC",
         edit(fw, "", "\t*(__extension__ &(id)) = MILAN_ID_MAGIC;\n")),
        ("C10", "macro writes the sample through an asm output operand",
         edit(fw, '#define MILAN_FORGE(x) __asm__ volatile("li %0, 0x4d494c4e" : "=r"(x))',
              "\tMILAN_FORGE(id);\n")),
        ("C11", "no macro: asm output operand writes the sample",
         edit(fw, "", '\t__asm__ volatile("li %0, 0x4d494c4e" : "=r"(id));\n')),
        ("C12", "published R273 macro inside a nested block",
         edit(fw, FORGE, "\t{\n\t\tMILAN_FORGE(id);\n\t}\n")),
        ("C13", "object-like alias of the forging function-like macro",
         edit(fw, FORGE + "\n#define MILAN_ALIAS MILAN_FORGE", "\tMILAN_ALIAS(id);\n")),
        ("C14", "published R273 macro invoked AFTER the guard (must be accepted)",
         edit(fw, FORGE, after_guard="\tMILAN_FORGE(id);\n")),
        ("C15", "plain write id = 0u AFTER the guard (must be accepted)",
         edit(fw, "", after_guard="\tid = 0u;\n\t(void)id;\n")),
        ("C16", "no macro: (id) = MAGIC before guard",
         edit(fw, "", "\t(id) = MILAN_ID_MAGIC;\n")),
        ("C17", "no macro: *&(id) = MAGIC before guard",
         edit(fw, "", "\t*&(id) = MILAN_ID_MAGIC;\n")),
        ("C18", "alias taken in the mismatch block, goto back before the sample",
         c18),
        ("C19", "R273-S3: verifier group's #else deleted",
         edit(fw, replace=(s3_old, "\treturn 1;\n#endif\n}"))),
        ("C20", "read-only macro use (void)(x) of the sample before guard",
         edit(fw, "#define MILAN_SHOW(x) ((void)(x))", "\tMILAN_SHOW(id);\n")),
        ("C21", "variadic forwarding macro to the forging macro",
         edit(fw, FORGE + "\n#define MILAN_V(...) MILAN_FORGE(__VA_ARGS__)",
              "\tMILAN_V(id);\n")),
        ("C22", "sample passed doubly parenthesized MILAN_FORGE((id))",
         edit(fw, FORGE, "\tMILAN_FORGE((id));\n")),
        ("C23", "object-like macro naming the sample used as an lvalue",
         edit(fw, "#define MILAN_SAMPLE id", "\tMILAN_SAMPLE = MILAN_ID_MAGIC;\n")),
        ("C24", "__builtin_memcpy into &id via macro",
         edit(fw, "#define MILAN_FORGE(x) __builtin_memcpy(&(x), &(uint32_t){MILAN_ID_MAGIC}, 4)",
              "\tMILAN_FORGE(id);\n")),
        ("C25", "compound assignment through a macro, no parentheses: x |= 0x4d494c4eu",
         edit(fw, "#define MILAN_FORGE(x) x |= MILAN_ID_MAGIC", "\tMILAN_FORGE(id);\n")),
    ]


results = []


def reviewer_hook(ns: dict) -> None:
    fw = ns["firmware_source"]
    contract = ns["assert_boot_contract"]
    if args.disable:
        cells = dict(zip(contract.__code__.co_freevars, contract.__closure__))
        assert args.disable in cells, sorted(cells)
        cells[args.disable].cell_contents = lambda *a, **k: None
    for cid, label, firmware in cases(fw):
        if args.only and cid not in args.only:
            continue
        assert firmware != fw, cid
        try:
            contract(firmware, ns["docs_source"], ns["csr_source"])
        except (AssertionError, ValueError) as exc:
            row = dict(id=cid, label=label, verdict="REFUSED", reason=str(exc)[:600])
        else:
            row = dict(id=cid, label=label, verdict="ACCEPTED")
        results.append(row)
        print(json.dumps(row), flush=True)


args.scratch.mkdir(parents=True, exist_ok=True)
audit_path = args.out.with_suffix(".argv.jsonl")
with audit_path.open("w") as stream:
    audit = tfc.CompilerAudit(stream, destination)
    argv = [str(path)] + (["--require-rv32"] if destination else [])
    module = types.ModuleType("r316_probe")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    module.reviewer_hook = reviewer_hook
    with patch.object(subprocess, "run", side_effect=audit.invoke), \
            patch.object(sys, "argv", argv):
        exec(compile(source, str(path), "exec"), module.__dict__)
        with tempfile.TemporaryDirectory(prefix="r316-", dir=args.scratch) as tmp:
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
