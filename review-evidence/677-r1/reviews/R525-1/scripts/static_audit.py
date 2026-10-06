#!/usr/bin/env python3
"""Verify retained mutation definitions, exclusions and firmware-only source scope."""
import ast,json,pathlib,subprocess,sys
repo=pathlib.Path(sys.argv[1]).resolve();base="6714181d0c8a16e2983f85b724f4d688f5111835";head="6c94e9f5f496ac25f8c4e31f9e3685c725de29f3"
def git(*args): return subprocess.check_output(["git","-C",str(repo),*args],text=True)
def old(path):return git("show",base+":"+path)
def mutants(text):
    tree=ast.parse(text)
    value=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="MUTANTS" for t in n.targets))
    return {ast.literal_eval(c.args[0]):ast.dump(c,include_attributes=False) for c in value.elts}
result={"head":head,"base":base,"mutants":{}}
for tag,path in (("ctrl","sw/firmware/ctrl/test/ctrl_mutants.py"),("nvm","sw/firmware/ctrl_nvm/test/nvm_mutants.py")):
    before=mutants(old(path));after=mutants((repo/path).read_text())
    assert all(after.get(k)==v for k,v in before.items())
    result["mutants"][tag]={"base":len(before),"head":len(after),"all_existing_definitions_unchanged":True,"added":sorted(set(after)-set(before))}
path="sw/firmware/gtest/README.md"
def exclusions(text):
    return [tuple(p.strip() for p in ln.split("|")[1:5]) for ln in text.splitlines() if ln.startswith("| `sw/firmware/")]
before=exclusions(old(path));after=exclusions((repo/path).read_text());assert before==after
result["exclusions"]={"count":len(after),"file_function_statement_and_uncovered_items_unchanged":True}
paths=git("diff","--name-only",base,head).splitlines();assert all(p.startswith("sw/firmware/") for p in paths)
result["changed_paths"]=paths
result["rtl_config_build_workflow_and_submodule_delta"]=False
result["shipping_Makefile"]="sw/firmware/milan_baremetal/Makefile"
subprocess.run(["git","-C",str(repo),"diff","--check",base,head],check=True)
print(json.dumps(result,indent=2))
