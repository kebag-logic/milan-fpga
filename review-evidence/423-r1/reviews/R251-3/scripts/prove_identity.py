#!/usr/bin/env python3
"""Prove exact ancestor, whole-tree and unchanged-function identity from Git objects."""
import argparse,ast,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("checkout",type=Path);p.add_argument("output",type=Path);a=p.parse_args()
old="b911c11671cae329a99f5e413133b4bf6357fa7f";head="4671e582cfa4bba4809b9e3a354ce5b6eb967f99";base="52711029f374650dc93830d5ea28e81cb5c8f410"
def git(*args): return subprocess.check_output(["git","--no-replace-objects","-C",str(a.checkout),*args])
assert git("rev-parse",head+"^").strip().decode()==old
subprocess.run(["git","-C",str(a.checkout),"merge-base","--is-ancestor",old,head],check=True)
def tree(rev):
    result={}
    for line in git("ls-tree","-rz",rev).split(b"\0"):
        if line:
            meta,path=line.split(b"\t",1);mode,kind,oid=meta.decode().split();result[path.decode()]={"mode":mode,"kind":kind,"oid":oid}
    return result
prev,current=tree(old),tree(head);assert prev.keys()==current.keys()
changed=[name for name in prev if prev[name]!=current[name]]
path="scripts/merge_containment_selftest_retention.py";assert changed==[path],changed
before=git("show",old+":"+path);after=git("show",head+":"+path)
new=b'        # _tree fixes the filename bytes independently of the process locale.\n        literal_path = os.fsdecode(path.encode("utf-8", "surrogateescape"))\n        fx.case("retention-" + name + "-path", repr(literal_path) in output, True,'
prior=b'        fx.case("retention-" + name + "-path", repr(path) in output, True,'
assert after.count(new)==1 and after.replace(new,prior)==before
old_ast=ast.parse(before);new_ast=ast.parse(after)
functions=lambda module:{node.name:ast.dump(node,include_attributes=False) for node in module.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
f1,f2=functions(old_ast),functions(new_ast);assert f1.keys()==f2.keys()
changed_functions=[n for n in f1 if f1[n]!=f2[n]];assert changed_functions==["_check"]
scopes=["AGENTS.md","CONTRIBUTING.md","REQUIREMENTS.md","docs/README.md","docs/reference/SUBMODULES.md","docs/overview/ARCHITECTURE.md","scripts/check_merge_containment.py","scripts/merge_containment_replay.py","scripts/merge_containment_selftest.py","scripts/merge_containment_selftest_locale.py","scripts/merge_containment_selftest_mutations.py","scripts/merge_containment_selftest_replay.py","scripts/run_all_suites.sh"]
record={"head":head,"ancestor":old,"direct_parent":True,"source_base":base,"old_tree":git("rev-parse",old+"^{tree}").decode().strip(),"tree":git("rev-parse",head+"^{tree}").decode().strip(),"tree_entries":len(current),"unchanged_entries":len(current)-len(changed),"only_changed_path":path,"old_entry":prev[path],"new_entry":current[path],"exact_assertion_restoration_equals_b911_blob":True,"changed_functions":changed_functions,"unchanged_retention_functions":[n for n in f1 if f1[n]==f2[n]],"scope_artifacts":{n:current[n] for n in scopes},"all_entries":current}
a.output.write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps({k:v for k,v in record.items() if k not in ("all_entries","scope_artifacts")},indent=2))
