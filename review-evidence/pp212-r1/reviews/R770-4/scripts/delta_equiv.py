#!/usr/bin/env python3
"""Rebuild the round-4 files from the round-3 blobs by the three stated splits
alone and compare bytes with the round-4 blobs. Usage: delta_equiv.py <repo>"""
import subprocess, sys
repo = sys.argv[1]
R3, R4 = "834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1", "6162885ffee5d8e8897732be6479982b8dceaec9"
def blob(rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, check=True).stdout
edits = {
    "tb/pp_top/sim_main.cpp": [(b"    int e = -1, q = -1;\n", b"    int e = -1;\n    int q = -1;\n", 2)],
    "tb/srp_stream_fsms/sim_main.cpp": [
        (b"  const int sinks[] = {0, 3};\n", b"  const int sink_a = 0;\n  const int sink_b = 3;\n", 1),
        (b"h.l_decl(sinks[0]) == 2 && h.l_decl(sinks[1]) == 2", b"h.l_decl(sink_a) == 2 && h.l_decl(sink_b) == 2", 1)],
}
ok = True
for path, subs in edits.items():
    old, new = blob(R3, path), blob(R4, path)
    for a, b, n in subs:
        c = old.count(a)
        print(f"{path}: {a.strip().decode()!r} occurs {c} (expected {n})")
        ok &= c == n
        old = old.replace(a, b)
    same = old == new
    print(f"{path}: rebuilt == round-4 blob: {same}")
    ok &= same
    for tok in (b"sinks[", b"sink_a", b"sink_b"):
        print(f"  {tok.decode()} in round-4 file: {new.count(tok)}")
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
