import ast, importlib.util, os, sys, time
from pathlib import Path
start,stop=map(int,sys.argv[1:3])
sys.argv=["sw/builder/test_builder.py","--require-rv32"]
path=Path(sys.argv[0])
main=next(n for n in ast.parse(path.read_text()).body if isinstance(n,ast.If) and "__main__" in ast.unparse(n.test))
loop=next(n for n in main.body if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=="fn")
spec=importlib.util.spec_from_file_location("builder_bank_subject",path)
module=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=module
spec.loader.exec_module(module)
for node in main.body:
 if isinstance(node,(ast.Import,ast.ImportFrom)):
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),"exec"),module.__dict__)
names=[n.id for n in loop.iter.elts]
for i,name in enumerate(names[start:stop],start):
 print(f"BANK {i}/{len(names)} {name}",flush=True)
 began=time.monotonic()
 module.__dict__[name]()
 print(f"PASS {i} {name} {time.monotonic()-began:.1f}s",flush=True)
for gate,why,kind in module.SKIPPED:
 print(f"NOT RUN {gate}: {why} ({kind})",flush=True)
print(f"BANK PASS [{start}:{stop}] / {len(names)}",flush=True)
