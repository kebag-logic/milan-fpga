#!/usr/bin/env python3
"""Independent reviewer probe: the campaign's real identity/copy step
(`private_inputs.copy_inputs`, driven exactly as `mutants.main` drives it)
against real Git and real submodule checkouts, under Git environment arms.

Usage: probe_git_env.py CLONE SCRATCH OUTPUT_JSON

Two disposable checkouts are built from the review clone: an ordinary clone
and a linked worktree of it, each with the two required submodules
initialised at their pins from the clone's local module repositories. Each
arm runs in a fresh interpreter with the arm's environment and reports
accepted/refused, the refusal text, and whether every copied byte equals the
committed blob.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HEAD = "26353960ae2763cc09741d0f7bcc720621bd5148"

CHILD = r'''
import hashlib, json, os, sys, tempfile
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
here = repo / "tb/verilator/gptp_shadow"
sys.path.insert(0, str(here)); sys.path.insert(0, str(repo / "scripts"))
import mutants
from owned_process import OwnedProcesses
from private_inputs import InputRefused, copy_inputs
result = {}
try:
    with OwnedProcesses() as owner:
        with tempfile.TemporaryDirectory(prefix="probe-copy-") as scratch:
            target = Path(scratch)
            targets = {row[1] for row in mutants.MUTATIONS + mutants.NOT_SEPARATELY_OBSERVABLE}
            copy_inputs(repo, here, target, owner, targets)
            files = sorted(str(p.relative_to(target)) for p in target.rglob("*") if p.is_file())
            digest = {}
            for name in files:
                data = (target / name).read_bytes()
                digest[name] = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            result.update(verdict="ACCEPTED", files=len(files), digest=digest)
except InputRefused as exc:
    result.update(verdict="REFUSED", reason=str(exc))
except Exception as exc:
    result.update(verdict="ERROR", reason=f"{type(exc).__name__}: {exc}")
print(json.dumps(result))
'''


def run(argv, **kw):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(argv, env=env, capture_output=True, text=True, check=True, **kw)


def committed_blobs(checkout):
    """Blob ids of every file the copy may contain, from real Git at HEAD."""
    blobs = {}
    for repo, prefix in ((checkout, ""), (checkout / "gptp-processor", "gptp-processor/"),
                         (checkout / "third_party/verilog-axis", "third_party/verilog-axis/")):
        out = run(["git", "-C", str(repo), "ls-tree", "-r", "HEAD"]).stdout
        for line in out.splitlines():
            meta, name = line.split("\t", 1)
            blobs[prefix + name] = meta.split()[2]
    return blobs


def build(clone, scratch):
    primary = scratch / "primary"
    run(["git", "clone", "-q", "--no-local", "--no-checkout", str(clone), str(primary)])
    run(["git", "-C", str(primary), "checkout", "-q", "--detach", HEAD])
    wt = scratch / "worktree"
    run(["git", "-C", str(primary), "worktree", "add", "-q", "--detach", str(wt), HEAD])
    for checkout in (primary, wt):
        for name, module in (("gptp-processor", "gptp-processor"),
                             ("third_party/verilog-axis", "third_party/verilog-axis")):
            run(["git", "-C", str(checkout), "config", f"submodule.{name}.url", str(clone / ".git/modules" / module)])
            run(["git", "-C", str(checkout), "-c", "protocol.file.allow=always", "submodule", "update", "-q",
                 "--init", "--", name])
    return {"primary": primary, "worktree": wt}


def arms(checkout):
    gitdir = run(["git", "-C", str(checkout), "rev-parse", "--absolute-git-dir"]).stdout.strip()
    index = run(["git", "-C", str(checkout), "rev-parse", "--path-format=absolute", "--git-path", "index"]).stdout.strip()
    exec_path = run(["git", "--exec-path"]).stdout.strip()
    return {
        "none": {},
        "trace-stderr": {"GIT_TRACE": "1", "GIT_TRACE_SETUP": "1"},
        "trace2-file": {"GIT_TRACE2_EVENT": str(checkout.parent / "trace2.json")},
        "presentation": {"GIT_PAGER": "cat", "GIT_EDITOR": "true", "GIT_AUTHOR_NAME": "A",
                         "GIT_TERMINAL_PROMPT": "0", "GIT_SSH_COMMAND": "ssh"},
        "pathspec-flags": {"GIT_GLOB_PATHSPECS": "1", "GIT_ICASE_PATHSPECS": "1"},
        "noglob-pathspecs": {"GIT_NOGLOB_PATHSPECS": "1"},
        "discovery": {"GIT_CEILING_DIRECTORIES": "/", "GIT_DISCOVERY_ACROSS_FILESYSTEM": "0"},
        "optional-locks": {"GIT_OPTIONAL_LOCKS": "0"},
        "config-nosystem": {"GIT_CONFIG_NOSYSTEM": "1"},
        "namespace": {"GIT_NAMESPACE": "x"},
        "exec-path-bogus": {"GIT_EXEC_PATH": "/nonexistent"},
        "alias-context": {"GIT_EXEC_PATH": exec_path, "GIT_PREFIX": ""},
        "rebase-exec-context": {"GIT_EXEC_PATH": exec_path, "GIT_PREFIX": "", "GIT_SEQUENCE_EDITOR": "true",
                                "GIT_DIR": gitdir} if "worktrees" in gitdir else
                               {"GIT_EXEC_PATH": exec_path, "GIT_PREFIX": "", "GIT_SEQUENCE_EDITOR": "true"},
        "commit-hook-context": dict({"GIT_INDEX_FILE": index, "GIT_EDITOR": ":", "GIT_AUTHOR_NAME": "A",
                                     "GIT_EXEC_PATH": exec_path, "GIT_PREFIX": ""},
                                    **({"GIT_DIR": gitdir} if "worktrees" in gitdir else {})),
        "git-c-alias-context": {"GIT_CONFIG_PARAMETERS": "'color.ui'='never'", "GIT_EXEC_PATH": exec_path},
        "same-gitdir": {"GIT_DIR": gitdir},
        "same-index": {"GIT_INDEX_FILE": index},
        "config-count-zero": {"GIT_CONFIG_COUNT": "0"},
        "foreign-gitdir": {"GIT_DIR": "/nonexistent/.git"},
    }


def main():
    clone, scratch, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    (scratch / "child.py").write_text(CHILD)
    checkouts = build(clone, scratch)
    results = {}
    for label, checkout in checkouts.items():
        blobs = committed_blobs(checkout)
        for arm, extra in arms(checkout).items():
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(extra, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1")
            done = subprocess.run([sys.executable, "-I", str(scratch / "child.py"), str(checkout)], env=env,
                                  capture_output=True, text=True, timeout=300)
            try:
                res = json.loads(done.stdout.strip().splitlines()[-1])
            except (ValueError, IndexError):
                res = {"verdict": "ERROR", "reason": done.stdout[-500:] + done.stderr[-500:]}
            digest = res.pop("digest", None)
            if digest is not None:
                res["all_bytes_equal_committed_blobs"] = all(blobs.get(k) == v for k, v in digest.items())
                res["copied_names"] = sorted(digest)
            res["env"] = sorted(extra)
            results[f"{label}/{arm}"] = res
            print(f"{label:9s} {arm:22s} {res['verdict']:8s} files={res.get('files')} "
                  f"bytes_ok={res.get('all_bytes_equal_committed_blobs')} {res.get('reason', '')[:110]}", flush=True)
    output.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
