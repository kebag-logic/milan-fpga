#!/usr/bin/env python3
"""Run the existing runtime recipe with the known independent SDK hardening default disabled.
Only the runtime recipe's compiler invocations receive -fno-stack-protector.
No repository or installed source is edited.
"""
import pathlib,runpy,subprocess,sys
root=pathlib.Path.cwd();recipe=root/"sw/firmware/ctrl/test/ctrl_image_runtime.py"
sys.path[:0]=[str(recipe.parent),str(root/"sw/firmware/gtest")]
original=subprocess.run
def run(argv,*args,**kwargs):
 if isinstance(argv,list) and str(argv[0]).endswith("gcc") and "-c" in argv:argv=[argv[0],"-fno-stack-protector",*argv[1:]]
 return original(argv,*args,**kwargs)
subprocess.run=run
sys.argv=[str(recipe),*sys.argv[1:]]
runpy.run_path(str(recipe),run_name="__main__")
