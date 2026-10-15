"""Probe P4: rerun the head's exec-ABI and exec-target controls on the host under the head's audit
(its TRAMPOLINE and NON_PATH sources, its audit_step), skipping only the step that writes /usr/local/bin.

Usage: python3 -I p4_abi_target.py <checkout> <scratch>"""
import json, os, shutil, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); base = Path(sys.argv[2]).resolve()
shutil.rmtree(base, ignore_errors=True); base.mkdir(parents=True)
sys.path.insert(0, str(root / "ci/image"))
import exec_audit as A, exec_audit_selftest as S
names = A.allowlist()
env = {"PATH": os.environ["PATH"], "HOME": str(base), "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
def step(label, command, expect):
    r = A.audit_step({"job": "probe", "label": label, "argv": ["bash", "-e", "-c", command], "text": command},
                     names, base, env)
    reasons = [f["reason"] for f in r["findings"]]
    hit = any(expect in x for x in reasons) if expect else not reasons
    print(json.dumps({"control": label, "expect": expect, "met": hit, "findings": reasons}), flush=True)
    return r
marker = base / "marker"
(base / "marker-stub").write_text(f"#!/bin/sh\ntouch {marker}\n"); (base / "marker-stub").chmod(0o755)
for abi, define, expect in (("i386", "", "i386 system call refused: 11"), ("x32", "-DX32 ", "x32 system call refused: 520")):
    (base / f"{abi}.c").write_text(S.TRAMPOLINE % (base / "marker-stub"))
    step(f"{abi} trampoline", f"gcc -static {define}-o {base}/{abi} {base}/{abi}.c && {base}/{abi}", expect)
    print(json.dumps({"marker_ran_after": abi, "value": marker.exists()}))
(base / "static.c").write_text("int main(void) { return 0; }\n")
step("static build output runs clean", f"gcc -static -o {base}/static {base}/static.c && {base}/static", None)
(base / "non_path.py").write_text(S.NON_PATH)
for how, expect in (("memfd", "exec of a descriptor that is not a file on a path: /memfd:zz_hidden"),
                    ("deleted", "exec of a descriptor that is not a file on a path"),
                    ("linked", f"exec through {A.PROCESS_ROOT}: not a file on a path")):
    step(f"non-path {how}", f"python3 {base}/non_path.py {how} {base} {A._record('self', 'fd')}", expect)
