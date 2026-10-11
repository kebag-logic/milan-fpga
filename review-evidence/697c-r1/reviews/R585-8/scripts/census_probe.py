#!/usr/bin/env python3
"""Exercise the census with a real Git call that derives the program name from the helper."""
import argparse, os, sys, types
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("checkout",type=Path); p.add_argument("work",type=Path)
a=p.parse_args(); root=a.checkout.resolve(); work=a.work.resolve(); work.mkdir(parents=True,exist_ok=True)
os.chdir(root); sys.dont_write_bytecode=True; sys.path.insert(0,str(root/"sw/firmware/ctrl/test"))
import ctrl_build, ctrl_pin
text=(root/"sw/firmware/ctrl/test/ctrl_build.py").read_text()
old='tree = git(stack, "ls-tree", "-r", "-t", "-z", "--full-tree", pin)'
new='tree = run([git.__name__, "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin])'
assert text.count(old)==1
mutant=text.replace(old,new)
(work/"ctrl_build_mutant.py").write_text(mutant)
texts={"sw/firmware/ctrl/test/ctrl_build.py":mutant,
       "sw/firmware/ctrl/test/ctrl_pin.py":(root/"sw/firmware/ctrl/test/ctrl_pin.py").read_text()}
findings=ctrl_pin.census(texts,ctrl_build.git_env())
print("mutant census findings:", findings, flush=True)
module=types.ModuleType("review_pin_mutant"); module.__file__=str(root/"sw/firmware/ctrl/test/ctrl_build.py")
sys.modules[module.__name__]=module
exec(compile(mutant,module.__file__,"exec"),module.__dict__)
clone=ctrl_pin.Clone(work,ctrl_build.stack_gitlink())
for case,plant in (("replacement tree",clone.replaced_tree),("replacement commit",clone.replaced_commit)):
    clone.fresh(); plant()
    print(case,"original:",clone.direct(),flush=True)
    try: answer=module.stack_pin(clone.path,clone.pin); accepted=True
    except ctrl_build.Refusal as exc: answer=str(exc); accepted=False
    print(case,"mutant accepted:",accepted,"answer:",answer,flush=True)
    assert accepted and not findings, "Probe no longer reproduces the census escape"
print("REPRODUCED: the census accepts a bypass that reads replacement objects",flush=True)
