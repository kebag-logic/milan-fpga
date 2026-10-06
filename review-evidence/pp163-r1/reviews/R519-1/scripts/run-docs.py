#!/usr/bin/env python3
import argparse,pathlib,subprocess
ap=argparse.ArgumentParser();ap.add_argument("--repo",required=True);a=ap.parse_args()
p=pathlib.Path(__file__).resolve().parents[1];tree=p/"scratch/docs"
if not (tree/".git").exists():
 subprocess.run(["git","clone","--shared","--no-checkout",a.repo,str(tree)],check=True)
 subprocess.run(["git","-C",str(tree),"checkout","--detach","cd9825c947cf67b735d26cc1c42541ccd9d7f637"],check=True)
with (p/"receipts/docs-check.log").open("w") as f:r=subprocess.run(["make","-j16","check"],cwd=tree,stdout=f,stderr=subprocess.STDOUT)
(p/"receipts/docs-check.rc").write_text(str(r.returncode)+"\n");print("Documentation check rc",r.returncode)
raise SystemExit(r.returncode)
