from pathlib import Path
import subprocess

root=Path("$LANES/545-crf-servo-slew")
def git(*args):
    return subprocess.check_output(["git",*args],cwd=root,text=True,timeout=120).strip()
head="ddf8151c478fc54c98608589c1afe9525739d6a4"
assert git("rev-parse","HEAD")==head
assert git("branch","--show-current")=="545-crf-servo-slew"
assert git("remote","get-url","origin")=="https://github.com/kebag-logic/milan-fpga.git"
assert git("rev-parse","origin/dev")=="5c78ce2e9d831e588e759b696ed549804327e4d8"
assert git("show","-s","--format=%P","HEAD")=="4538d7c03dc4f56d7ed4c971603e15bda82050a8 5c78ce2e9d831e588e759b696ed549804327e4d8"
assert git("show","-s","--format=%B","HEAD")=="Merge dev into 545-crf-servo-slew"
assert not git("status","--porcelain=v1")
assert not git("submodule","foreach","--quiet","--recursive","git status --porcelain=v1")
status=git("submodule","status","--recursive")
assert all(not line.startswith(("-","+","U")) for line in status.splitlines())
print("Head:",head)
print("Remote, branch, parents, one-line commit, clean root and submodules: PASS")
print(status)
