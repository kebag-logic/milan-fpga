#!/usr/bin/env python3
"""[R632] round-2 independent scope probe for issue #734 / PR #735.

Builds lane histories in a disposable repository, extracts each shipping scope
step body with a YAML parser (independent of the candidate's own extractor),
and executes it the way the hosted job (synthetic merge, ACT unset) and the
act replay (PR head checkout, ACT=true, refs/remotes/origin/dev = live tip)
would. Prints one line per case/workflow/mode and exits non-zero on any
unexpected verdict.

Usage: python3 -I probe_r632_2.py <shipping-checkout> <empty-work-dir> [mutant]
mutant (optional) rewrites the extracted step body before execution:
  hosted-frozen2   hosted uses "$PR_BASE_SHA" "$GITHUB_SHA" (pre-#734 shape)
  hosted-frozen3   hosted uses "$PR_BASE_SHA...$GITHUB_SHA" (round-1 shape)
  replay-frozen    replay merge-base uses $PR_BASE_SHA instead of the live ref
  replay-2dot      replay diffs the live tip tree against the head tree
  no-all           merge-base without --all
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import tempfile

import yaml

SCOPES = (("rtl.yml", "full-ci-gate", "gate"),
          ("rtl-fast.yml", "changes", "scope"),
          ("elaborate.yml", "elaborate", "scope"))

MUTANTS = {
    "hosted-frozen2": ('"$GITHUB_SHA^1" "$GITHUB_SHA"', '"$PR_BASE_SHA" "$GITHUB_SHA"'),
    "hosted-frozen3": ('"$GITHUB_SHA^1" "$GITHUB_SHA"', '"$PR_BASE_SHA...$GITHUB_SHA"'),
    "replay-frozen": ('"refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA"',
                      '"$PR_BASE_SHA" "$PR_HEAD_SHA"'),
    "replay-2dot": ('"$base" "$PR_HEAD_SHA"', '"refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA"'),
    "no-all": ("git merge-base --all", "git merge-base"),
}


def git(root, *args):
    return subprocess.check_output(
        ["git", "-c", "core.hooksPath=/dev/null", "-c", "user.name=probe",
         "-c", "user.email=probe@example.invalid", "-c", "init.defaultBranch=main",
         "-c", "commit.gpgsign=false", "-C", str(root), *args],
        text=True, stderr=subprocess.STDOUT).strip()


def step_body(shipping, wf, job, sid):
    doc = yaml.safe_load((shipping / ".github/workflows" / wf).read_text())
    steps = [s for s in doc["jobs"][job]["steps"] if s.get("id") == sid]
    assert len(steps) == 1, (wf, sid)
    body = steps[0]["run"]
    assert body.count("python3 scripts/ci_scope.py --selftest") == 1
    return body.replace("python3 scripts/ci_scope.py --selftest", ":")


class Repo:
    def __init__(self, root, shipping):
        self.root = root
        git(root, "init", "--quiet")
        (root / "scripts").mkdir()
        (root / "scripts/ci_scope.py").write_bytes((shipping / "scripts/ci_scope.py").read_bytes())
        (root / "hdl").mkdir()
        (root / "hdl/x.sv").write_text("module x; endmodule // R\n")
        (root / "hdl/z.sv").write_text("module z; endmodule\n")
        (root / "docs").mkdir()
        (root / "docs/a.md").write_text("A\n")
        (root / ".gitmodules").write_text(
            '[submodule "protocol-processor"]\n\tpath = protocol-processor\n'
            '\turl = https://example.invalid/pp.git\n')
        git(root, "add", ".")
        git(root, "commit", "-qm", "R0")
        r0 = self.head()
        git(root, "update-index", "--add", "--cacheinfo", f"160000,{r0},protocol-processor")
        git(root, "commit", "-qm", "R gitlink")
        self.R = self.head()

    def head(self):
        return git(self.root, "rev-parse", "HEAD")

    def commit(self, parent, changes, msg="c"):
        git(self.root, "checkout", "-q", "--detach", parent)
        for path, text in changes.items():
            p = self.root / path
            if text is None:
                git(self.root, "rm", "-q", path)
                continue
            if isinstance(text, tuple):  # gitlink
                git(self.root, "update-index", "--cacheinfo", f"160000,{text[0]},{path}")
                continue
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
            git(self.root, "add", path)
        git(self.root, "commit", "-qm", msg, "--allow-empty")
        return self.head()

    def merge(self, ours, theirs, extra=None):
        git(self.root, "checkout", "-q", "--detach", ours)
        if extra is None:
            git(self.root, "merge", "-q", "--no-ff", "--no-edit", theirs)
            return self.head()
        git(self.root, "merge", "-q", "--no-ff", "--no-commit", theirs)
        for path, text in extra.items():
            (self.root / path).write_text(text)
            git(self.root, "add", path)
        git(self.root, "commit", "-qm", "evil merge")
        return self.head()

    def gh_merge(self, live, head):
        """GitHub's refs/pull/N/merge: always two parents, first = live base tip."""
        tree = git(self.root, "merge-tree", "--write-tree", live, head).splitlines()[0]
        return git(self.root, "commit-tree", tree, "-p", live, "-p", head, "-m", "Merge")


def run_step(repo, body, env_over):
    with tempfile.TemporaryDirectory(prefix="probe-run-") as raw:
        out = pathlib.Path(raw) / "out"
        env = {"PATH": os.environ["PATH"], "HOME": raw, "GITHUB_OUTPUT": str(out),
               "RUNNER_TEMP": raw, "EVENT_NAME": "pull_request", "PR_DRAFT": "false",
               "PR_BASE_REF": "dev", "GIT_CONFIG_NOSYSTEM": "1"}
        env.update(env_over)
        p = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", body], cwd=repo.root,
                           env=env, capture_output=True, text=True)
        if p.returncode != 0:
            return ("REFUSED", None)
        files = sorted(pathlib.Path(raw).glob("changed*"))
        paths = files[0].read_text().splitlines() if files else None
        kv = dict(l.split("=", 1) for l in out.read_text().splitlines())
        return (kv.get("rtl"), paths)


def hosted(repo, body, recorded, live, head):
    m = repo.gh_merge(live, head)
    git(repo.root, "checkout", "-q", "--detach", m)
    return run_step(repo, body, {"GITHUB_SHA": m, "PR_BASE_SHA": recorded, "PR_HEAD_SHA": head})


def replay(repo, body, recorded, live, head):
    git(repo.root, "checkout", "-q", "--detach", head)
    git(repo.root, "update-ref", "refs/remotes/origin/dev", live)
    return run_step(repo, body, {"GITHUB_SHA": head, "PR_BASE_SHA": recorded,
                                 "PR_HEAD_SHA": head, "ACT": "true"})


def build(repo):
    R = repo.R
    c = {}
    # Dev history: D edits hdl/x.sv; E unrelated later RTL; G gitlink bump; Y identical RTL.
    D = repo.commit(R, {"hdl/x.sv": "module x; endmodule // D\n"}, "dev D")
    E = repo.commit(D, {"hdl/later.sv": "module later; endmodule\n"}, "dev E")
    # stale-base docs / RTL: lane forked at R, dev moved to E.
    docs = repo.commit(R, {"docs/b.md": "lane docs\n"})
    c["stale-docs"] = (R, E, docs, "false")
    c["stale-rtl"] = (R, E, repo.commit(R, {"hdl/pr.sv": "module pr; endmodule\n"}), "true")
    c["stale-rtl-delete"] = (R, E, repo.commit(R, {"hdl/z.sv": None}), "true")
    c["gitlink"] = (R, E, repo.commit(R, {"protocol-processor": (D,)}), "true")
    c["empty"] = (R, E, R, "true")
    c["rename-rtl-to-docs"] = (R, E, repo.commit(R, {"hdl/z.sv": None, "docs/z.md": "module z; endmodule\n"}), "true")
    # REV: lane opens at R, merges D, restores hdl/x.sv, then a docs edit.
    m = repo.merge(docs, D)
    rest = repo.commit(m, {"hdl/x.sv": "module x; endmodule // R\n"}, "restore")
    rev = repo.commit(rest, {"docs/b.md": "lane docs 2\n"})
    c["REV"] = (R, D, rev, "true")
    c["REV+E"] = (R, E, rev, "true")
    # REV-evil: the restore happens inside the merge commit itself.
    evil = repo.merge(docs, D, {"hdl/x.sv": "module x; endmodule // R\n"})
    evil = repo.commit(evil, {"docs/b.md": "lane docs 3\n"})
    c["REV-evil+E"] = (R, E, evil, "true")
    # REV-ff: lane fast-forwards to D (no merge commit), restores, docs.
    ff = repo.commit(D, {"hdl/x.sv": "module x; endmodule // R\n"}, "restore ff")
    ff = repo.commit(ff, {"docs/b.md": "ff docs\n"})
    c["REV-ff+E"] = (R, E, ff, "true")
    # REV-gitlink: dev bumps the pointer, lane merges it and restores the old pointer.
    G = repo.commit(E, {"protocol-processor": (D,)}, "dev G pointer")
    gm = repo.merge(docs, G)
    gr = repo.commit(gm, {"protocol-processor": (R,)}, "restore pointer")
    gr = repo.commit(gr, {"docs/b.md": "g docs\n"})
    c["REV-gitlink"] = (R, G, gr, "true")
    # Lane's own RTL edit, later merged dev, then docs: own RTL still visible.
    own = repo.commit(R, {"hdl/own.sv": "module own; endmodule\n"})
    own = repo.commit(repo.merge(own, E), {"docs/b.md": "own docs\n"})
    c["own-rtl-then-merge-dev"] = (R, E, own, "true")
    # Divergence probe: the PR's RTL edit also landed identically on dev (Y).
    Y = repo.commit(E, {"hdl/y.sv": "module y; endmodule\n"}, "dev Y identical")
    same = repo.commit(R, {"hdl/y.sv": "module y; endmodule\n", "docs/c.md": "c\n"})
    c["identical-on-dev"] = (R, Y, same, ("false", "true"))
    return c


def main(argv):
    shipping = pathlib.Path(argv[1]).resolve()
    work = pathlib.Path(argv[2]).resolve()
    mutant = argv[3] if len(argv) > 3 else None
    work.mkdir(parents=True, exist_ok=True)
    assert not any(work.iterdir()), "work dir must be empty"
    repo = Repo(work, shipping)
    cases = build(repo)
    bad = 0
    for wf, job, sid in SCOPES:
        body = step_body(shipping, wf, job, sid)
        if mutant:
            old, new = MUTANTS[mutant]
            assert body.count(old) >= 1, (wf, mutant)
            body = body.replace(old, new)
        for label, (rec, live, head, want) in cases.items():
            want_h, want_r = want if isinstance(want, tuple) else (want, want)
            h = hosted(repo, body, rec, live, head)
            r = replay(repo, body, rec, live, head)
            ok = h[0] == want_h and r[0] == want_r
            bad += not ok
            print(f"{'ok  ' if ok else 'MISS'} {wf:14} {label:24} hosted={h[0]} {h[1]} "
                  f"replay={r[0]} {r[1]} want={want_h}/{want_r}")
    # Push behaviour: rtl.yml and elaborate.yml publish rtl=true for any non-PR
    # event; rtl-fast diffs before..after, falling back to every tracked file.
    D = git(repo.root, "rev-parse", "HEAD")
    for wf, job, sid in SCOPES:
        body = step_body(shipping, wf, job, sid)
        git(repo.root, "checkout", "-q", "--detach", cases["stale-docs"][2])
        for before, want in ((repo.R, "false"), ("0" * 40, "true"), ("", "true")):
            res = run_step(repo, body, {"EVENT_NAME": "push", "GITHUB_SHA": cases["stale-docs"][2],
                                        "PUSH_BEFORE_SHA": before})
            if wf != "rtl-fast.yml":
                want = "true"
            ok = res[0] == want
            bad += not ok
            print(f"{'ok  ' if ok else 'MISS'} {wf:14} push before={before[:8] or 'empty':8} "
                  f"rtl={res[0]} paths={None if res[1] is None else len(res[1])} want={want}")
    print(f"probe: {'PASS' if not bad else f'{bad} MISS'}{' (mutant ' + mutant + ')' if mutant else ''}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
