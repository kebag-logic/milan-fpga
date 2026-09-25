from pathlib import Path
import json, subprocess, sys, types
from unittest.mock import patch
root = Path.cwd()
out = Path(__file__).resolve().parent
sys.path.insert(0, str(root / "sw/builder"))
import test_firmware_compiler as tfc
path = root / "sw/builder/test_builder.py"
source = path.read_text()
marker = "    subset_note = assert_subset_refuses()"
assert source.count(marker) == 1
source = source.replace(marker, "    isolation_hook(locals())\n    return\n" + marker)
rows = []
def isolation_hook(ns):
    check = ns["assert_preprocessed_identity_sample"]
    compiler = ns["census_compiler"]()
    model = types.SimpleNamespace(identity=0, identity_default=0x4d494c4e)
    prefix = "typedef unsigned int uint32_t; uint32_t milan_read(uint32_t); int printf(const char *, ...); "
    declarations = {"automatic": "", "static": "static ", "extern": "extern ",
                    "auto": "auto ", "register": "register "}
    cases = [(label, storage, "", "") for label, storage in declarations.items()]
    for expression in ["&(id)", "__extension__ &(id)",
                       "&__builtin_choose_expr(1, id, id)",
                       "&_Generic(0, default: id)", "&(__real__ id)",
                       "&(__extension__ id)", "sizeof &id",
                       "__builtin_choose_expr(1, 0, &id)"]:
        cases.append((expression, "", "", "(void)(" + expression + ");"))
    cases += [("postguard write", "", "", "id = 0;"),
              ("unrelated asm interval", "", '__asm__("" ::: "memory");', ""),
              ("sample rvalue interval", "", "(void)id;", "")]
    cases += [
        ("allowed diagnostic", "", 'printf("id=%lu", (unsigned long)id);', ""),
        ("allowed discarded mask", "", '(void)(id & 0x1UL);', ""),
        ("nested capture", "", "", 'void f(void) { id=1; }'),
        ("old-style capture", "", "", 'void f(x) int x; { id=x; }'),
        ("suppressed old-style capture", "", "", '__extension__ void f(x) int x; { id=x; }'),
        ("wrapped argument", "", 'printf("", __extension__ (unsigned long)id);', ""),
        ("choose argument", "", 'printf("", __builtin_choose_expr(1, (unsigned long)id, 0ul));', ""),
        ("cast lvalue", "", '(unsigned long)id = 0;', ""),
        ("discarded compound", "", '(void)(id &= 1u);', ""),
        ("discarded comma", "", '(void)(id & 1u), id = 0;', ""),
        ("discarded lvalue", "", '(void)(id & 1u) = 0;', ""),
    ]
    for label, storage, between, after in cases:
        unit = prefix + "static void milan_init(void) { " + storage + \
               "uint32_t id = milan_read(0); " + between + \
               " if (id != 0x4d494c4e) { return; } " + after + " }"
        try:
            check(dict(ran=True, text=unit, compiler=compiler), "id", model)
        except AssertionError as exc:
            row = dict(label=label, verdict="REFUSED", reason=str(exc))
        else:
            row = dict(label=label, verdict="ACCEPTED")
        expected = "ACCEPTED" if label in ("automatic", "auto", "register", "postguard write", "allowed diagnostic", "allowed discarded mask") else "REFUSED"
        assert row["verdict"] == expected, row
        rows.append(row)
        print(json.dumps(row), flush=True)
with (out / "continued-isolation-argv.jsonl").open("w") as stream:
    audit = tfc.CompilerAudit(stream, Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install"))
    module = types.ModuleType("isolation_probe")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    module.isolation_hook = isolation_hook
    with patch.object(subprocess, "run", side_effect=audit.invoke):
        exec(compile(source, str(path), "exec"), module.__dict__)
        module.test_baremetal_profile_contract()
(out / "continued-isolation.json").write_text(json.dumps(rows, indent=2) + "\n")
