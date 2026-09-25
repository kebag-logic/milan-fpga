#!/usr/bin/env python3
"""[R316] R316-2 sub-rule necessity harness (--disable mut:NAME mutates one sub-rule in memory) for issue #544 / PR #558.

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


MUTATIONS = {
    "nested": ('assert "ISO C forbids nested functions" not in checked.stderr, \\',
               'assert True or "ISO C forbids nested functions" not in checked.stderr, \\'),
    "asm": ('assert not {"asm", "__asm", "__asm__"}.intersection(identifiers), \\',
            'assert True or not {"asm", "__asm", "__asm__"}.intersection(identifiers), \\'),
    "extblank": ('if token.group() == "__extension__"]', 'if False]'),
    "register": ('"register " + diagnostic[stop:])', '"" + diagnostic[stop:])'),
    "storage": ('        assert storage in ("", "auto", "register"), \\\n            f"{IDENTITY_SAMPLE_PIN}',
                '        assert True or storage in ("", "auto", "register"), \\\n            f"{IDENTITY_SAMPLE_PIN}'),
}
if args.disable and args.disable.startswith("mut:"):
    old, new = MUTATIONS[args.disable[4:]]
    assert source.count(old) == 1, args.disable
    source = source.replace(old, new)
    args.disable = None
NESTED_DECL = "auto void forge_sample(void);\n"
NESTED_DEF = ("\n__attribute__((always_inline)) inline void forge_sample(void) "
              "{ id = MILAN_ID_MAGIC; }\n")


def cases(fw: str) -> list[tuple[str, str, str]]:
    """(id, description, firmware). Sub-rule necessity probes."""
    nested = edit(fw, "", "\tforge_sample();\n", NESTED_DEF,
                  replace=(READ, NESTED_DECL + READ))
    old_style = nested.replace("auto void forge_sample(void);", "auto void forge_sample(int);") \
        .replace("__attribute__((always_inline)) inline void forge_sample(void) ",
                 "__extension__ __attribute__((always_inline)) inline void forge_sample(value) int value; ") \
        .replace("\tforge_sample();\n", "\tforge_sample(0);\n")
    return [
        ("S01", "nested function defined after the guard writes the sample, called before it", nested),
        ("S02", "__extension__ old-style nested function capture", old_style),
        ("S03", "asm without a sample operand in the interval",
         edit(fw, "", '\t__asm__ volatile("" ::: "memory");\n')),
        ("S04", "plain &(id) after the guard", edit(fw, "", after_guard="\t(void)(&(id));\n")),
        ("S05", "__extension__ &(id) after the guard",
         edit(fw, "", after_guard="\t(void)(__extension__ &(id));\n")),
        ("S06", "asm writing s0 directly in the interval (no operands)",
         edit(fw, "", '\t__asm__ volatile("li s0, 0x4d494c4e");\n')),
    ]


def storage_rows(ns: dict) -> None:
    model = ns["CsrModel"](ns["firmware_source"], ns["blanked_sv"](ns["csr_source"]))
    check = ns["assert_preprocessed_identity_sample"]
    for storage in ("static", "extern", "_Thread_local static"):
        unit = ("typedef unsigned int uint32_t; uint32_t milan_read(uint32_t); "
                f"static void milan_init(void) {{ {storage} uint32_t id "
                f"= milan_read({model.identity}); "
                f"if (id != {model.identity_default}) {{ return; }} }}")
        try:
            check({"ran": True, "text": unit, "compiler": ns["census_compiler"]()}, "id", model)
        except AssertionError as exc:
            row = dict(id="ST-" + storage, label="storage unit", verdict="REFUSED", reason=str(exc)[:300])
        else:
            row = dict(id="ST-" + storage, label="storage unit", verdict="ACCEPTED")
        results.append(row)
        print(json.dumps(row), flush=True)


results = []


def reviewer_hook(ns: dict) -> None:
    fw = ns["firmware_source"]
    contract = ns["assert_boot_contract"]
    if args.disable:
        cells = dict(zip(contract.__code__.co_freevars, contract.__closure__))
        assert args.disable in cells, sorted(cells)
        cells[args.disable].cell_contents = lambda *a, **k: None
    if args.mode == "sdk":
        storage_rows(ns)
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
