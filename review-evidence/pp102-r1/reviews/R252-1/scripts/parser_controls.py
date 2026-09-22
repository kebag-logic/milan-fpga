#!/usr/bin/env python3
"""Invoke the real immutable parent parser on source and disposable controls."""
import importlib.util
import json
import sys
from collect import BASE, CHECKOUT, HEAD, OUT, blob_hash, capture

sys.dont_write_bytecode = True
path = OUT/'parent/scripts/check_cpp_idiom.py'
assert blob_hash(path.read_bytes()) == '1d9ccd7fa1fded549f8988149397ff10bc12b0d5'
assert blob_hash(path.with_name('code_quality_scope.py').read_bytes()) == '4603080a48d97e1e45f8b787273a2b459b1aebe6'
spec = importlib.util.spec_from_file_location('immutable_parent_cpp',path)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
head = (CHECKOUT/'tb/pp_top/Makefile').read_text()
before = capture('controls/Makefile.before',['git','show',BASE+':tb/pp_top/Makefile']).decode()
old = '-CFLAGS "-DPP_TOP_SRP_DOM_DEF_VID=0x$(SRP_VID_FIXTURE)"'
new = '-CFLAGS "-DPP_TOP_SRP_DOM_DEF_VID=0x$(SRP_VID_FIXTURE) -Wall -Wextra"'
assert before.count(old) == head.count(new) == 1
assert head == before.replace(old,new)
cases = [('baseline',before,['-Wall','-Wextra']),('head',head,[])]
for flag in ('-Wall','-Wextra'):
    mutant = head.replace(new,new.replace(' '+flag,''))
    cases.append(('remove-'+flag[1:],mutant,[flag]))
results=[]
for label,content,want in cases:
    dest = OUT/'controls'/('Makefile.'+label)
    dest.write_text(content)
    got = checker.cflags_missing(dest.read_text())
    assert got == want,(label,got,want)
    row={'case':label,'actual':got,'expected':want,'git_blob':blob_hash(content.encode()),'pass':True}
    results.append(row)
    print(label,got,'PASS')
groups = checker.CFLAGS_RE.findall('\n'.join(l for l in head.splitlines() if not l.lstrip().startswith('#')))
assert len(groups) == 2
assert all(all(flag in g for flag in checker.WARNING_FLAGS) for g in groups)
result={'head':HEAD,'real_checker_git_blob':blob_hash(path.read_bytes()),'groups':groups,'controls':results,'only_change':old+' -> '+new}
(OUT/'raw/parser-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Both CFLAGS groups:',groups)
print('Exact one-line insertion confirmed; macro, fixture and all other Makefile bytes unchanged.')
