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
    import ast
    values = next(ast.literal_eval(node.value) for node in ast.walk(ast.parse(source)) if isinstance(node, ast.Assign) and any(isinstance(t,ast.Name) and t.id == 'identity_near_misses' for t in node.targets))
    contract=ns['assert_boot_contract'];fw=ns['firmware_source']
    cells=dict(zip(contract.__code__.co_freevars,contract.__closure__))
    cell=cells['assert_preprocessed_identity_sample'];check=cell.cell_contents
    fixtures={label:fw.replace('static int aem_loaded;', '#define MILAN_FORGE(x) '+expression+'\n\nstatic int aem_loaded;').replace('if (id != MILAN_ID_MAGIC) {', 'MILAN_FORGE(id);\nif (id != MILAN_ID_MAGIC) {') for label,expression in values.items()}
    fixtures['printf macro assigns argument']=fw.replace('static int aem_loaded;', '#define printf(...) MILAN_DIAG(__VA_ARGS__, 0u, 0u)\n#define MILAN_DIAG(format, value, ...) (((value) = MILAN_ID_MAGIC), (printf)(format, value, __VA_ARGS__))\n\nstatic int aem_loaded;')
    for label,fixture in fixtures.items():
        for disconnected in (False,True):
            if disconnected and label in ('cast used as lvalue','discarded mask used as lvalue','printf macro assigns argument'):continue
            cell.cell_contents=(lambda *_:None) if disconnected else check
            try:contract(fixture,ns['docs_source'],ns['csr_source'])
            except (AssertionError,ValueError) as exc:row=dict(label=label,disconnected=disconnected,verdict='REFUSED',reason=str(exc))
            else:row=dict(label=label,disconnected=disconnected,verdict='ACCEPTED')
            print(json.dumps(row),flush=True);rows.append(row)
            assert row['verdict']==('ACCEPTED' if disconnected else 'REFUSED'),row
            if not disconnected:assert 'identity-sample absence rule' in row['reason'],row
    cell.cell_contents=check
with (out / "near-miss-controls-argv.jsonl").open("w") as stream:
    audit = tfc.CompilerAudit(stream, Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install"))
    module = types.ModuleType("isolation_probe")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    module.isolation_hook = isolation_hook
    with patch.object(subprocess, "run", side_effect=audit.invoke):
        exec(compile(source, str(path), "exec"), module.__dict__)
        module.test_baremetal_profile_contract()
(out / "near-miss-controls.json").write_text(json.dumps(rows, indent=2) + "\n")
