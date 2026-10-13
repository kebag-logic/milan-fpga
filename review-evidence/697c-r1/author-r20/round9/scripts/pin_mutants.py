"""Mutants of the pin proof, patched in-process; each must make its own control(s) ESCAPE.
usage: python3 -B pin_mutants.py <checkout> <work>"""
import os, stat, subprocess, sys, io, contextlib, shutil, hashlib
from pathlib import Path
root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_build, ctrl_pin

orig = {n: getattr(ctrl_build, n) for n in ("git_env", "blob_id", "on_disk")}

def env_without(name):
    return lambda: {k: v for k, v in orig["git_env"]().items() if k != name}

def filtered_blob(path, algorithm):
    # hash through git's filters and attributes, as `git hash-object <path>` does
    rel = path.relative_to(path.parents[1]) if path.parent.name else path
    res = subprocess.run(["git", "-C", str(path.parent), "hash-object", path.name], capture_output=True, text=True)
    return res.stdout.strip()

def no_modes(stack, algorithm):
    found = orig["on_disk"](stack, algorithm)
    return {k: (("100644" if v[0] == "100755" else v[0]),) + v[1:] for k, v in found.items()}

def follow_links(stack, algorithm):
    found = {}
    for here, dirs, files in os.walk(stack):
        if Path(here) == stack:
            dirs[:] = [d for d in dirs if d != ".git"]
            files = [f for f in files if f != ".git"]
        for name in dirs + files:
            path = Path(here) / name
            rel = path.relative_to(stack).as_posix()
            if path.is_dir():
                found[rel] = ("040000", "tree", "")
            else:
                data = path.read_bytes()
                mode = path.stat().st_mode
                found[rel] = ("100755" if mode & stat.S_IXUSR else "100644", "blob",
                              hashlib.new(algorithm, b"blob %d\0" % len(data) + data).hexdigest())
    return found

PROVEN = ("src", "include", "tests", "examples", "scripts", "cmake", "CMakeLists.txt")
def proven_only(stack, algorithm):
    found = orig["on_disk"](stack, algorithm)
    return {k: v for k, v in found.items() if k.split("/", 1)[0] in PROVEN}
orig_git = ctrl_build.git
def proven_git(directory, *args, stdin=None):
    if args[:1] == ("ls-tree",) and "--full-tree" in args:
        args = (*args, "--", *PROVEN)
    return orig_git(directory, *args, stdin=stdin)

mutants = [
    ("helper without GIT_NO_REPLACE_OBJECTS", "git_env", env_without("GIT_NO_REPLACE_OBJECTS")),
    ("helper without GIT_GRAFT_FILE", "git_env", env_without("GIT_GRAFT_FILE")),
    ("disk hashed through git's filters (hash-object)", "blob_id", filtered_blob),
    ("modes not compared", "on_disk", no_modes),
    ("symbolic links followed (type not compared)", "on_disk", follow_links),
    ("only the parts a gate builds compared (round 8's path set)", "on_disk", proven_only),
]
orig["git"] = orig_git
for name, attr, fn in mutants:
    setattr(ctrl_build, attr, fn)
    if attr == "git_env":
        ctrl_pin.git_env = fn
    if fn is proven_only:
        ctrl_build.git = proven_git
    w = work / name.split()[0]
    shutil.rmtree(w, ignore_errors=True); w.mkdir(parents=True)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        bad, n = ctrl_pin.pin_controls(w, [])
    census = ctrl_pin.proof_census()
    setattr(ctrl_build, attr, orig[attr])
    ctrl_pin.git_env = orig["git_env"]
    ctrl_build.git = orig_git
    escaped = [ln for ln in out.getvalue().splitlines() if ln.startswith("[ESCAPED]")]
    print(f"MUTANT {name}: {bad} of {n} controls misbehaved")
    for ln in escaped:
        print("   ", ln[:220])
    print("    the gate's census:", census or "no finding")
