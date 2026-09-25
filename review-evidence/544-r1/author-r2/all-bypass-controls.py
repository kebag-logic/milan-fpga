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
    tree=ast.parse(source)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='test_baremetal_profile_contract')
    # Reproduce fixture construction against the current production strings.
    fw=ns['firmware_source'];sample='id';guard='if (id != MILAN_ID_MAGIC) {'
    make=lambda body:fw.replace('static int aem_loaded;', '#define MILAN_FORGE(x) '+body+'\n\nstatic int aem_loaded;').replace(guard,'MILAN_FORGE(id);\n'+guard)
    get=lambda name:next(ast.literal_eval(n.value) for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
    fixtures={}
    for label,body in get('identity_bypass_bodies').items():
        fixtures['macro '+label]=make(body)
        import re
        fixtures['plain '+label]=fw.replace(guard,re.sub(r'\bx\b',sample,body)+';\n'+guard)
    fixtures['macro generic default lvalue']=make('_Generic(0, default: x) = MILAN_ID_MAGIC')
    for word in ('asm','__asm','__asm__'):fixtures[word+' no operand']=fw.replace(guard,word+' volatile("" ::: "memory");\n'+guard)
    for label,expr in [('plain','&(id)'),('extension','__extension__ &(id)'),('choose','&__builtin_choose_expr(1,id,id)'),('generic','&_Generic(0,int:id)'),('real','&(__real__ id)'),('wrapped extension','&(__extension__ id)')]:
        after='/* PHC and fabric gPTP are live from reset, independent of the AEM gate. */'
        fixtures[label+' after guard']=fw.replace(after,'(void)('+expr+');\n'+after)
    contract=ns['assert_boot_contract'];cells=dict(zip(contract.__code__.co_freevars,contract.__closure__));cell=cells['assert_preprocessed_identity_sample'];check=cell.cell_contents
    for label,fixture in fixtures.items():
        for disconnected in (False,True):
            cell.cell_contents=(lambda *_:None) if disconnected else check
            try:contract(fixture,ns['docs_source'],ns['csr_source'])
            except (AssertionError,ValueError) as exc:row=dict(label=label,disconnected=disconnected,verdict='REFUSED',reason=str(exc))
            else:row=dict(label=label,disconnected=disconnected,verdict='ACCEPTED')
            print(json.dumps(row),flush=True);rows.append(row)
            assert row['verdict']==('ACCEPTED' if disconnected else 'REFUSED'),row
            if not disconnected:assert 'identity-sample absence rule' in row['reason'],row
    cell.cell_contents=check
with (out / "all-bypass-controls-argv.jsonl").open("w") as stream:
    audit = tfc.CompilerAudit(stream, Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install"))
    module = types.ModuleType("isolation_probe")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    module.isolation_hook = isolation_hook
    with patch.object(subprocess, "run", side_effect=audit.invoke):
        exec(compile(source, str(path), "exec"), module.__dict__)
        module.test_baremetal_profile_contract()
(out / "all-bypass-controls.json").write_text(json.dumps(rows, indent=2) + "\n")
