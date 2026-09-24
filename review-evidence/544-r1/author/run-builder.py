import argparse
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import types
import tempfile
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=("sdk", "absent"))
parser.add_argument("--probe", action="store_true")
parser.add_argument("--base", action="store_true")
parser.add_argument("--disconnect", action="store_true")
parser.add_argument("--tag", required=True)
args = parser.parse_args()
root = Path.cwd()
out = Path(__file__).resolve().parent
sys.path.insert(0, str(root / "sw/builder"))
import test_firmware_compiler as tfc
sdk = Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install") if args.mode == "sdk" else None
if sdk:
    tfc.sdk.verify(sdk)
path = root / "sw/builder/test_builder.py"
argv = [str(path)] + (["--require-rv32"] if sdk else [])
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
inputs = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (path, root / "docs/integration/BAREMETAL_FIRMWARE.md")}
(out / (args.tag + "-inputs.json")).write_text(json.dumps(dict(head=head, inputs=inputs), indent=2) + "\n")
print("Validation head:", head, flush=True)
with (out / (args.tag + "-argv.jsonl")).open("w") as stream:
    audit = tfc.CompilerAudit(stream, sdk)
    def selected_run(command, *positional, **keyword):
        if args.probe or str(command[0]) in audit.cross:
            return audit.invoke(command, **keyword)
        # Full-bank host harnesses remain real host compilations. Only gate
        # 1b's candidate probes go through the absent-firmware audit.
        if str(command[0]) in audit.native and (
                command[1:] == ["--version"] or
                any(Path(str(arg)).name == "probe.c" for arg in command[1:])):
            return audit.invoke(command, **keyword)
        assert not (str(command[0]) in audit.native and "-std=gnu99" in command), "host attempted gate 1b firmware compilation"
        return audit.run(command, *positional, **keyword)
    with patch.object(subprocess, "run", side_effect=selected_run), patch.object(sys, "argv", argv):
        if not args.probe:
            runpy.run_path(str(path), run_name="__main__")
        else:
            if args.base:
                source = audit.run(["git", "show", "ffcbd33de70278ae34b533dcbadde0b36c8cba13:sw/builder/test_builder.py"], capture_output=True, text=True, check=True).stdout
            else:
                source = path.read_text()
            marker = "    subset_note = assert_subset_refuses()"
            assert source.count(marker) == 1
            hook = "    probe_hook(locals())\n    return\n"
            source = source.replace(marker, hook + marker)
            module = types.ModuleType("test_builder_probe")
            module.__file__ = str(path)
            sys.modules[module.__name__] = module
            results = []
            def probe_hook(ns):
                fw = ns["firmware_source"]
                guard = "\tif (id != MILAN_ID_MAGIC) {"
                static = "static int aem_loaded;"
                cases = [
                    ("R272 plain macro", fw.replace(static, "#define MILAN_FORGE(x) x = MILAN_ID_MAGIC\n\n" + static, 1).replace(guard, "\tMILAN_FORGE(id);\n" + guard, 1)),
                    ("R273 parenthesized macro", fw.replace(static, "#define MILAN_FORGE(x) ((x) = MILAN_ID_MAGIC)\n\n" + static, 1).replace(guard, "\tMILAN_FORGE(id);\n" + guard, 1)),
                    ("literal sample macro", fw.replace(static, "#define MILAN_FORGE() id = MILAN_ID_MAGIC\n\n" + static, 1).replace(guard, "\tMILAN_FORGE();\n" + guard, 1)),
                    ("R273-S3 missing else", fw.replace('\treturn 1;\n#else\n\tprintf("Milan baremetal: no QSPI AEM slot; entity disabled.\\n");\n\treturn 0;\n#endif\n}', '\treturn 1;\n#endif\n}', 1)),
                ]
                contract = ns["assert_boot_contract"]
                if args.disconnect:
                    name = "assert_identity_macro_free" if args.mode == "absent" else "assert_preprocessed_identity_sample"
                    closure = dict(zip(contract.__code__.co_freevars, contract.__closure__))
                    assert name in closure, (name, closure.keys())
                    closure[name].cell_contents = lambda *a, **k: None
                if sdk:
                    for label, expression in (
                            ("casted address", "(void)&((id))"),
                            ("sizeof address", "sizeof &(id)"),
                            ("conditional address", "if (1) &(id)")):
                        cases.append((label, fw.replace(static, "#define MILAN_FORGE() " + expression + "\n\n" + static, 1).replace(guard, "\tMILAN_FORGE();\n" + guard, 1)))
                for label, firmware in cases:
                    assert firmware != fw, label
                    try:
                        contract(firmware, ns["docs_source"], ns["csr_source"])
                    except (AssertionError, ValueError) as exc:
                        row = dict(label=label, verdict="REFUSED", reason=str(exc))
                    else:
                        row = dict(label=label, verdict="ACCEPTED")
                    results.append(row)
                    print(json.dumps(row), flush=True)
            module.probe_hook = probe_hook
            exec(compile(source, str(path), "exec"), module.__dict__)
            with tempfile.TemporaryDirectory(prefix="544-probe-") as tmp:
                module.OUT = Path(tmp)
                module.test_baremetal_profile_contract()
            (out / (args.tag + ".json")).write_text(json.dumps(results, indent=2) + "\n")
    print(f"AUDIT: {audit.compiles} gate 1b firmware compiler invocations; mode={args.mode}", flush=True)
    if not sdk:
        assert audit.compiles == 0
        assert audit.hidden == audit.cross
