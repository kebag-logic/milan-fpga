#!/usr/bin/env python3
import ast,json,re,sys
from pathlib import Path
root,packet=map(Path,sys.argv[1:])
tree=ast.parse((root/'sw/builder/test_builder.py').read_text())
forms=next(ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='unit_asm_forms' for t in n.targets))
pattern=re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_$][\w$]*|[^\s]',re.ASCII)
normalize=lambda x:tuple(pattern.findall(x))
prod=json.loads((packet/'public-inputs/author-r3/production-preprocess.json').read_text())['asm_statements']
census=json.loads((packet/'public-inputs/author-r3/census-production-asm.json').read_text())
assert set(map(normalize,forms))==set(map(normalize,prod+census))
print(json.dumps(dict(allowlist_count=len(forms),production_unique=len(set(map(normalize,prod))),census_unique=len(set(map(normalize,census))),union_exact=True),indent=2))
