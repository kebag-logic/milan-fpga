#!/usr/bin/env python3
"""Exercise stopped and complete database parses with the selected GNU Make."""
import json, os, pathlib, subprocess, sys, tempfile
root = pathlib.Path.cwd()
sys.path.insert(0, str(root/'scripts'))
import shape_consumer_inventory as inv
print(subprocess.check_output(['make','--version'], text=True).splitlines()[0])
with tempfile.TemporaryDirectory(prefix='make-probes-') as directory:
    work=pathlib.Path(directory)
    for name, body, expected in [
        ('stopped-before', '$(error planted stopped parse)\nall: gen/adp_shape_defaults.svh\n', False),
        ('stopped-after', 'all: gen/adp_shape_defaults.svh\n$(error planted stopped parse)\n', False),
        ('missing-product', 'all: missing-generated-input gen/adp_shape_defaults.svh\n', True),
        ('missing-include', 'include absent.mk\nall: gen/adp_shape_defaults.svh\n', False),
    ]:
        (work/'Makefile').write_text(body)
        raw=subprocess.run(['make','-pqrR','-f','Makefile','--eval','__shape_probe__: ;','__shape_probe__'],cwd=work,capture_output=True,text=True)
        ok, prereqs=inv.shape_prereqs_from_database(work,'Makefile')
        assert ok == expected,(name,ok,raw.stderr)
        if expected: assert 'gen/adp_shape_defaults.svh' in prereqs
        print(json.dumps(dict(case=name,make_rc=raw.returncode,partial_files_section='# Files' in raw.stdout,readable=ok,prerequisites=prereqs,stderr=raw.stderr)))
for name in ('milan_dp_render','pp_shadow'):
    path=root/'tb/verilator'/name
    ok, prereqs=inv.shape_prereqs_from_database(path,'Makefile')
    assert ok and prereqs,(name,ok,prereqs)
    findings=inv.dangling_consumers(str((path/'Makefile').relative_to(root)),(path/'Makefile').read_text(),set(subprocess.check_output(['git','ls-files'],text=True).splitlines()))
    assert not findings,findings
    print(json.dumps(dict(consumer=name,readable=ok,prerequisites=prereqs,findings=findings)))
