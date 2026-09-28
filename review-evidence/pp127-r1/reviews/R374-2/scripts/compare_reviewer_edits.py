"""For each reviewer edit (round-1 textual edit, verbatim from the published
reviewer scripts), apply it to a copy of the head RTL and compare the result
byte-for-byte with the same copy after the committed tb/srp_top/mutations patch.
Usage: compare_reviewer_edits.py <head_tree> <r374_mutants.py> <r375_run.py> <scratch>"""
import pathlib, re, shutil, subprocess, sys, runpy, types
head, r374, r375, scratch = [pathlib.Path(a).resolve() for a in sys.argv[1:5]]
def load(path, anchor_start, anchor_end, env):
    src = path.read_text(); s = src.index(anchor_start); e = src.index(anchor_end, s)
    ns = dict(env); exec(src[s:e], ns); return ns
m1 = load(r374, "MUT = {", "names = sys.argv", {"T": "hdl/srp/KL_srp_top.sv", "E": "hdl/srp/KL_srp_encoder.sv", "TK": "hdl/srp/KL_srp_talker_fsm.sv"})["MUT"]
m2 = load(r375, "MUTANTS = {", "\n\n\ndef patch_tb", {"TOP": "hdl/srp/KL_srp_top.sv", "ENC": "hdl/srp/KL_srp_encoder.sv", "LS": "hdl/srp/KL_srp_listener_fsm.sv"})["MUTANTS"]
edits = {k: v for k, v in m1.items()}; edits.update({k: v[0] for k, v in m2.items()})
def tree_bytes(d):
    return {str(p.relative_to(d)): p.read_bytes() for p in sorted((d / "hdl").rglob("*")) if p.is_file()}
ok_all = True
for name, ed in sorted(edits.items()):
    a = scratch / "cmp-a"; b = scratch / "cmp-b"
    for d in (a, b):
        shutil.rmtree(d, ignore_errors=True); shutil.copytree(head / "hdl", d / "hdl")
    for f, x, y in ed:
        p = a / f; s = p.read_text(); assert s.count(x) == 1, (name, x); p.write_text(s.replace(x, y))
    patch = head / "tb/srp_top/mutations" / (name + ".patch")
    if not patch.exists():
        print(f"{name}: NO COMMITTED PATCH"); ok_all = False; continue
    subprocess.run(["git", "apply", str(patch)], cwd=b, check=True)
    same = tree_bytes(a) == tree_bytes(b)
    ok_all &= same or name.endswith("expiry-pulse") or name == "r-expiry-pulse-restored"
    print(f"{name}: {'IDENTICAL' if same else 'DIFFERS'} to committed patch")
print("ALL_REQUIRED_IDENTICAL" if ok_all else "MISMATCH")
