"""Read-only source/pin integrity receipt; writes only the requested receipt."""
import datetime, hashlib, json, os, stat, subprocess, sys
from pathlib import Path
root, expected, output = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(where, *args):
    return subprocess.check_output(["git", "-C", str(where), *args], env=env)
def audit(where, head):
    assert git(where, "rev-parse", "HEAD").decode().strip() == head
    tree = git(where, "rev-parse", head + "^{tree}").decode().strip()
    assert git(where, "write-tree").decode().strip() == tree
    assert not git(where, "status", "--porcelain=v1").strip()
    checked, links = 0, {}
    for row in git(where, "ls-tree", "-rz", head).split(b"\0"):
        if not row: continue
        meta, rawpath = row.split(b"\t", 1)
        mode, kind, blob = meta.decode().split()
        relative = os.fsdecode(rawpath)
        if mode == "160000":
            links[relative] = blob
            continue
        path = where / relative
        if mode == "120000":
            assert path.is_symlink(), path
            data = os.fsencode(os.readlink(path))
        else:
            assert mode in {"100644", "100755"}, mode
            assert path.is_file() and not path.is_symlink(), path
            assert bool(path.stat().st_mode & 0o111) == (mode == "100755"), path
            data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == blob, path
        checked += 1
    return {"head": head, "tree": tree, "files_verified": checked, "gitlinks": links}
result = {"checked_at": datetime.datetime.now().astimezone().isoformat(), "root": str(root), "parent": audit(root, expected), "required_submodules": {}}
for name in ("third_party/verilog-axis", "protocol-processor", "gptp-processor"):
    pin = result["parent"]["gitlinks"][name]
    result["required_submodules"][name] = audit(root / name, pin)
result["optional_external"] = "Unused SSH-only external remains outside required local-gate population; no physical campaign evidence inferred."
result["result"] = "PASS"
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
