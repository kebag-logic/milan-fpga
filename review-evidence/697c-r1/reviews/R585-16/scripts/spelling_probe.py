"""Independent superproject key-spelling probe of the tsn-c-stack pin proof's gitlink read (#697, round 17).

Usage: python3 -I spelling_probe.py <ctrl-test-dir> <scratch-dir> <pin>
<ctrl-test-dir> holds the ctrl_build.py under test (head, or an older one extracted with its tree).
The Git used is the first `git` on PATH, for the setup, the raw sensitivity read and the proof alike.

Each case builds, from nothing, a superproject whose sparse index holds the gitlink third_party/tsn-c-stack = <pin>
inside a sparse directory whose tree object is then deleted, then writes one configuration spelling as raw text into
its own .git/config (or an included / work-tree file). Each spelling reaches a recorder program (an ext:: transport
or upload-pack) if Git tries to fetch the missing tree. For each case it prints:
  RAW   : what plain `git ls-files --stage` (the same Git, environment GIT_CONFIG_NOSYSTEM/GLOBAL only, no
          GIT_NO_LAZY_FETCH) does: RAN=<n> recorder starts; shows the spelling is a live route on this Git;
  PROOF : ctrl_build.stack_gitlink(<superproject>): ACCEPTED <gitlink> or REFUSED <text>, and RAN=<n>.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

test_dir, scratch, pin = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
GITLINK = "third_party/tsn-c-stack"
BASE_ENV = {"PATH": os.environ["PATH"], "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            "HOME": str(scratch), "LANG": "C"}


def g(cwd: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, env=BASE_ENV, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"setup failed: git {' '.join(args)}: {r.stderr}")
    return r.stdout


def recorder(own: Path) -> Path:
    prog = own / "recorder"
    prog.write_text('#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexit 1\n')
    prog.chmod(0o755)
    return prog


def ran(own: Path) -> int:
    f = own / "ran"
    n = len(f.read_text().splitlines()) if f.exists() else 0
    f.unlink(missing_ok=True)
    return n


def sparse_top(own: Path) -> Path:
    origin, top = own / "origin", own / "top"
    g(own, "init", "-q", str(origin))
    (origin / "kept").mkdir()
    (origin / "kept/file").write_text("kept\n")
    g(origin, "add", "kept/file")
    g(origin, "update-index", "--add", "--cacheinfo", f"160000,{pin},{GITLINK}")
    g(origin, "-c", "user.name=p", "-c", "user.email=p@invalid", "commit", "-qm", "p")
    g(own, "init", "-q", str(top))
    g(top, "-c", "fetch.unpackLimit=1000000", "fetch", "-q", "--no-tags", str(origin), "HEAD")
    g(top, "update-ref", "HEAD", "FETCH_HEAD")
    g(top, "sparse-checkout", "set", "--cone", "--sparse-index", "kept")
    g(top, "checkout", "-q")
    tree = g(top, "rev-parse", "HEAD:third_party").strip()
    (top / ".git/objects" / tree[:2] / tree[2:]).unlink()
    return top


def cases(rec: Path, own: Path):
    ext = f"ext::{rec} %S"
    tail = f'[protocol "ext"]\n\tallow = always\n[url "{ext}"]\n\tinsteadOf = \n'
    named = f'[remote "o"]\n\turl = {ext}\n'
    return [
        ("C00 clean sparse superproject (control: expect gitlink not readable, no recorder)", "", None),
        ("C01 [remote] promisor = true (no subsection)", "[remote]\n\tpromisor = true\n" + tail, None),
        ("C02 [remote] partialCloneFilter = tree:0 (no subsection)", "[remote]\n\tpartialCloneFilter = tree:0\n" + tail, None),
        ("C03 [remote \"\"] promisor = true (empty subsection)", '[remote ""]\n\tpromisor = true\n' + tail, None),
        ("C04 [remote] promisor (no value: boolean true)", "[remote]\n\tpromisor\n" + tail, None),
        ("C05 [REMOTE] PROMISOR = TRUE (upper case)", "[REMOTE]\n\tPROMISOR = TRUE\n" + tail, None),
        ("C06 [remote.o] promisor = true (old-style subsection)", "[remote.o]\n\tpromisor = true\n" + named + tail, None),
        ("C07 [remote \"a.b\"] promisor = true (dotted subsection)",
         f'[remote "a.b"]\n\turl = {ext}\n\tpromisor = true\n' + tail, None),
        ("C08 [remote \"o\"] partialclonefilter only (named)", named + "\tpartialclonefilter = tree:0\n" + tail, None),
        ("C09 extensions.partialClone = o alone (format 1)",
         "[core]\n\trepositoryformatversion = 1\n[extensions]\n\tpartialClone = o\n" + named + tail, None),
        ("C10 [remote] promisor in a file included by includeIf gitdir", tail, "includeIf"),
        ("C11 [remote] promisor in the work tree's own configuration", tail, "worktree"),
        ('C12 [remote ""] partialCloneFilter (empty subsection)', '[remote ""]\n\tpartialCloneFilter = tree:0\n' + tail, None),
    ]


sys.path.insert(0, str(test_dir))
import ctrl_build  # noqa: E402

out = []
for name, text, where in cases(Path("/nonexistent"), scratch):
    own = scratch / name.split()[0]
    shutil.rmtree(own, ignore_errors=True)
    own.mkdir(parents=True)
    rec = recorder(own)
    text = text.replace("/nonexistent", str(rec))
    top = sparse_top(own)
    cfg = top / ".git/config"
    with cfg.open("a") as f:
        f.write(text)
    if where == "includeIf":
        (own / "inc").write_text("[remote]\n\tpromisor = true\n")
        with cfg.open("a") as f:
            f.write(f'[includeIf "gitdir:{top}/.git"]\n\tpath = {own / "inc"}\n')
    elif where == "worktree":
        g(top, "config", "extensions.worktreeConfig", "true")
        (top / ".git/config.worktree").write_text("[remote]\n\tpromisor = true\n")
    listed = g(top, "config", "--list", "--show-scope")
    parsed = [(scope, *ctrl_build.parsed_key(key)) for scope, *_, key, _v in ctrl_build.configuration(top)
              if scope != "command"] if hasattr(ctrl_build, "parsed_key") else []
    # the proof first, so that nothing a raw lazy fetch writes into the configuration (partial_clone_register)
    # reaches it; then the raw read, which shows the spelling is a live route on this Git
    try:
        verdict = f"ACCEPTED {ctrl_build.stack_gitlink(top)}"
    except ctrl_build.Refusal as exc:
        verdict = f"REFUSED {exc}"
    proof_ran = ran(own)
    raw = subprocess.run(["git", "ls-files", "--stage", "--", GITLINK], cwd=top, env=BASE_ENV, capture_output=True,
                         text=True)
    raw_ran = ran(own)
    row = {"case": name, "raw_rc": raw.returncode, "raw_ran": raw_ran, "raw_out": raw.stdout.strip(),
           "verdict": verdict, "proof_ran": proof_ran, "listed": listed.splitlines(), "parsed": parsed}
    out.append(row)
    print(f"{name}\n  RAW   rc={raw.returncode} RAN={raw_ran} {raw.stdout.strip()[:60]}\n  PROOF {verdict} RAN={proof_ran}",
          flush=True)
(scratch / "rows.json").write_text(json.dumps(out, indent=1))
