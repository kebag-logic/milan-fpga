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
    contract = ns['assert_boot_contract']
    fw = ns['firmware_source']
    read = 'uint32_t id = milan_read(MILAN_ID);'
    guard = 'if (id != MILAN_ID_MAGIC) {'
    end = '/* PHC and fabric gPTP are live from reset, independent of the AEM gate. */'
    cells = dict(zip(contract.__code__.co_freevars, contract.__closure__))
    cell = cells['assert_preprocessed_identity_sample']
    check = cell.cell_contents
    for prefix, params in [('', 'void'), ('', 'value'), ('__extension__ ', 'value')]:
        old = params == 'value'
        fixture = fw.replace(read, 'auto void forge_sample(' + ('int' if old else 'void') + ');\n' + read)
        fixture = fixture.replace(guard, ('forge_sample(0);' if old else 'forge_sample();') + '\n' + guard)
        fixture = fixture.replace(end, prefix + '__attribute__((always_inline)) inline void forge_sample(' + params + ') ' + ('int value; ' if old else '') + '{ id = MILAN_ID_MAGIC; }\n' + end)
        for disconnected in (False, True):
            cell.cell_contents = (lambda *_: None) if disconnected else check
            try:
                contract(fixture, ns['docs_source'], ns['csr_source'])
            except (AssertionError, ValueError) as exc:
                row = dict(case=prefix+params, disconnected=disconnected, verdict='REFUSED', reason=str(exc))
            else:
                row = dict(case=prefix+params, disconnected=disconnected, verdict='ACCEPTED')
            rows.append(row)
            print(json.dumps(row), flush=True)
            assert row['verdict'] == ('ACCEPTED' if disconnected else 'REFUSED'), row
            if not disconnected: assert 'identity-sample absence rule' in row['reason'], row
    cell.cell_contents = check
with (out / "inline-capture-controls-argv.jsonl").open("w") as stream:
    audit = tfc.CompilerAudit(stream, Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install"))
    module = types.ModuleType("isolation_probe")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    module.isolation_hook = isolation_hook
    with patch.object(subprocess, "run", side_effect=audit.invoke):
        exec(compile(source, str(path), "exec"), module.__dict__)
        module.test_baremetal_profile_contract()
(out / "inline-capture-controls.json").write_text(json.dumps(rows, indent=2) + "\n")
