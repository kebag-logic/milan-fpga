"""Compare every tracked blob of a lane commit (and its pinned dependencies)
with the files of an external source export, by git blob hash."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

lane = Path("$LANES/645-ring-slip")
commit = sys.argv[1]
exports = [Path(p) for p in sys.argv[2:-1]]
out = Path(sys.argv[-1])


def tree(repo, rev):
    rows = subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-r", "-z", rev]).split(b"\0")
    for row in filter(None, rows):
        meta, path = row.split(b"\t", 1)
        mode, kind, sha = meta.decode().split()
        yield mode, kind, sha, path.decode()


def blob_sha(path: Path):
    data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


expected = {}
for mode, kind, sha, path in tree(lane, commit):
    if kind == "blob":
        expected[path] = sha
    elif kind == "commit":
        sub = lane / path
        top = subprocess.check_output(["git", "-C", str(sub), "rev-parse", "--show-toplevel"], text=True).strip()
        if Path(top) != sub:
            expected[path] = "uninitialised-gitlink:" + sha
            continue
        for _, k2, s2, p2 in tree(sub, sha):
            if k2 == "blob":
                expected[path + "/" + p2] = s2
report = {"commit": subprocess.check_output(["git", "-C", str(lane), "rev-parse", commit], text=True).strip(),
          "tracked_files": len(expected), "exports": {}}
rc = 0
for root in exports:
    diff, missing = [], []
    for path, sha in expected.items():
        p = root / path
        if sha.startswith("uninitialised-gitlink:"):
            if not p.is_dir():
                missing.append(path)
            continue
        if not (p.exists() or p.is_symlink()):
            missing.append(path)
        elif blob_sha(p) != sha:
            diff.append(path)
    report["exports"][str(root)] = {"differences": diff, "missing": missing}
    rc |= bool(diff or missing)
report["result"] = "IDENTICAL" if rc == 0 else "DIFFERENT"
out.write_text(json.dumps(report, indent=2) + "\n")
print(report["result"], {k: (len(v["differences"]), len(v["missing"])) for k, v in report["exports"].items()})
raise SystemExit(rc)
