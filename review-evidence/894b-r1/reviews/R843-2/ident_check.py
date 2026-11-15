"""Compare two trees' changed files: Python ASTs without docstrings, C/C++ token streams without comments."""
import ast, subprocess, sys
from pathlib import Path
a, b = Path(sys.argv[1]), Path(sys.argv[2])
def strip(t):
    for n in ast.walk(t):
        if isinstance(n,(ast.Module,ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)) and n.body and isinstance(n.body[0],ast.Expr) and isinstance(getattr(n.body[0],'value',None),ast.Constant) and isinstance(n.body[0].value.value,str):
            n.body[0]=ast.Pass()
    return ast.dump(t)
def ctoks(p):
    return subprocess.run(['gcc','-fpreprocessed','-dD','-E','-P','-x','c++',str(p)],capture_output=True,text=True).stdout.split()
for f in sorted(p for p in b.rglob('*') if p.is_file()):
    r=f.relative_to(b); o=a/r
    if f.suffix=='.py': same = strip(ast.parse(o.read_text()))==strip(ast.parse(f.read_text())); kind='ast'
    elif f.suffix in ('.c','.h','.cpp','.hpp'): same = ctoks(o)==ctoks(f); kind='tokens'
    else: same=None; kind='other'
    print(f"{'SAME' if same else 'DIFF' if same is False else 'N/A '} {kind} {r}")
