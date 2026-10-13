#!/usr/bin/env python3
"""Independent [R632] round-4 scope probe for PR #735 (issue #734).

Executes the three shipping PR-scope shell bodies (rtl.yml full-ci-gate/gate,
rtl-fast.yml changes/scope, elaborate.yml elaborate/scope), read from the
candidate checkout with a YAML parser, against lane histories built in a
disposable repository with hermetic Git.  Each case runs in the hosted form
(synthetic two-parent merge, first parent = live base, ACT unset) and the
replay form (PR head checked out, ACT=true, refs/remotes/origin/dev = live).
Rule-removal mutations of the bodies and of the classifier must each break
at least one control.  Optional B16 reproduction against a real Git dir.

Usage: python3 -I probe_r632_4.py <candidate-checkout> <out.json> [<b16-gitdir>]
Needs PyYAML.  Writes only under a temporary directory and <out.json>.
"""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

import yaml

SCOPES = (("rtl.yml", "full-ci-gate", "gate"),
          ("rtl-fast.yml", "changes", "scope"),
          ("elaborate.yml", "elaborate", "scope"))
SELFTEST = "python3 scripts/ci_scope.py --selftest"


def hermetic(home: pathlib.Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k not in ("HOME", "XDG_CONFIG_HOME", "ACT")}
    env.update(HOME=str(home), XDG_CONFIG_HOME=str(home), GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_SYSTEM=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               GIT_AUTHOR_NAME="Probe", GIT_AUTHOR_EMAIL="probe@example.invalid",
               GIT_COMMITTER_NAME="Probe", GIT_COMMITTER_EMAIL="probe@example.invalid",
               GIT_AUTHOR_DATE="2002-02-02T00:00:00+0000",
               GIT_COMMITTER_DATE="2002-02-02T00:00:00+0000",
               GIT_CONFIG_COUNT="3", GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="false",
               GIT_CONFIG_KEY_1="maintenance.auto", GIT_CONFIG_VALUE_1="false",
               GIT_CONFIG_KEY_2="gc.auto", GIT_CONFIG_VALUE_2="0")
    return env


class Repo:
    def __init__(self, root: pathlib.Path, home: pathlib.Path):
        self.root, self.env = root, hermetic(home)

    def git(self, *args: str, check: bool = True) -> str:
        r = subprocess.run(["git", "-C", str(self.root), *args], env=self.env,
                           capture_output=True, text=True)
        if check and r.returncode:
            raise RuntimeError(f"git {args}: {r.stdout}{r.stderr}")
        return r.stdout.strip()

    def at(self, rev: str) -> None:
        self.git("checkout", "--quiet", "--detach", rev)

    def commit(self, msg: str, paths: list[str] | None = None) -> str:
        # Stage only named paths: the fixture's gitlink has no checkout, so a
        # tree-wide add would record it as deleted.
        if paths is None:
            self.git("add", "-A")
        elif paths:
            self.git("add", "-A", "--", *paths)
        self.git("commit", "--quiet", "--allow-empty", "-m", msg)
        return self.git("rev-parse", "HEAD")

    def write(self, path: str, text: str) -> None:
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def change(self, parent: str, edits: dict[str, str | None], msg: str = "c") -> str:
        self.at(parent)
        for path, text in edits.items():
            if text is None:
                self.git("rm", "--quiet", path)
            else:
                self.write(path, text)
        return self.commit(msg, [p for p, t in edits.items() if t is not None])

    def merge_into(self, ours: str, theirs: str, resolve: dict[str, str] | None = None) -> str:
        self.at(ours)
        r = subprocess.run(["git", "-C", str(self.root), "merge", "--no-ff", "--no-edit",
                            "--quiet", theirs], env=self.env, capture_output=True, text=True)
        if r.returncode:
            assert resolve, r.stdout + r.stderr
            for path, text in resolve.items():
                self.write(path, text)
            self.git("add", "--", *resolve)
            self.git("commit", "--quiet", "--no-edit")
        return self.git("rev-parse", "HEAD")

    def github_merge(self, live: str, head: str) -> str:
        """Model refs/pull/N/merge: always a two-parent commit, first parent live."""
        tree = self.git("merge-tree", "--write-tree", live, head)
        return self.git("commit-tree", tree.splitlines()[0], "-p", live, "-p", head,
                        "-m", f"Merge {head} into {live}")


def bodies(cand: pathlib.Path) -> dict[str, str]:
    out = {}
    for wf, job, sid in SCOPES:
        doc = yaml.safe_load((cand / ".github/workflows" / wf).read_text())
        steps = [s for s in doc["jobs"][job]["steps"] if s.get("id") == sid]
        assert len(steps) == 1, wf
        run = steps[0]["run"]
        assert run.count(SELFTEST) == 1, wf
        env = steps[0]["env"]
        assert env.get("PR_BASE_REF") == "${{ github.event.pull_request.base.ref }}", wf
        assert env.get("PR_HEAD_SHA") == "${{ github.event.pull_request.head.sha }}", wf
        assert "PR_BASE_SHA" not in env, wf
        out[wf] = run.replace(SELFTEST, ":")
    return out


def execute(repo_dir: pathlib.Path, git_env: dict[str, str], body: str, *, mode: str,
            recorded: str, head: str, sha: str, event: str = "pull_request",
            before: str = "", work_tree_dir: pathlib.Path | None = None) -> dict:
    with tempfile.TemporaryDirectory(prefix="r632-4-step-") as raw:
        tmp = pathlib.Path(raw)
        (tmp / "bin").mkdir()
        (tmp / "bin/python3").symlink_to(sys.executable)
        env = dict(git_env)
        env.pop("ACT", None)
        env.update(EVENT_NAME=event, PR_DRAFT="false", PR_BASE_REF="dev", PR_HEAD_SHA=head,
                   PR_BASE_SHA=recorded, GITHUB_SHA=sha, PUSH_BEFORE_SHA=before,
                   GITHUB_OUTPUT=str(tmp / "out"), RUNNER_TEMP=str(tmp),
                   PATH=str(tmp / "bin") + os.pathsep + os.environ["PATH"])
        if mode == "replay":
            env["ACT"] = "true"
        script = tmp / "step.sh"
        script.write_text(body)
        r = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", str(script)],
                           cwd=work_tree_dir or repo_dir, env=env, capture_output=True, text=True)
        outputs = {}
        if (tmp / "out").exists():
            outputs = dict(l.split("=", 1) for l in (tmp / "out").read_text().splitlines() if "=" in l)
        changed = sorted(tmp.glob("changed*"))
        paths = changed[0].read_text().splitlines() if changed else None
        return {"rc": r.returncode, "rtl": outputs.get("rtl"), "paths": paths,
                "stderr_tail": r.stderr.strip().splitlines()[-2:] if r.returncode else []}


def build(repo: Repo, cand: pathlib.Path) -> tuple[list[dict], dict]:
    page = "".join(f"line {n}\n" for n in range(30))
    repo.git("init", "--quiet")
    repo.write("scripts/ci_scope.py", (cand / "scripts/ci_scope.py").read_text())
    repo.write("scripts/tool.py", "x = 1\n")
    repo.write("hdl/x.sv", "// x original\n")
    repo.write("hdl/a.sv", "// a original\n")
    repo.write("docs/page.md", page)
    repo.write("docs/a.md", "doc a\n")
    repo.write("README.md", "readme\n")
    repo.write(".gitmodules", '[submodule "protocol-processor"]\n\tpath = protocol-processor\n'
               '\turl = https://example.invalid/pp.git\n'
               '[submodule "ptr"]\n\tpath = docs/ptr.md\n\turl = https://example.invalid/ptr.git\n')
    c0 = repo.commit("base")
    repo.git("update-index", "--add", "--cacheinfo", f"160000,{c0},protocol-processor")
    repo.git("update-index", "--add", "--cacheinfo", f"160000,{c0},docs/ptr.md")
    repo.git("commit", "--quiet", "-m", "pointer")
    b0 = repo.git("rev-parse", "HEAD")
    # dev moves on with unrelated tooling and RTL (makes two-dot diffs noisy)
    d1 = repo.change(b0, {"scripts/tool.py": "x = 2\n", "hdl/b.sv": "// dev b\n"}, "dev d1")
    dx = repo.change(d1, {"hdl/x.sv": "// x newer dev\n"}, "dev edits x")
    de = repo.change(dx, {"hdl/later.sv": "// later dev\n"}, "dev later E")
    cases = []

    def case(label, recorded, live, head, paths, rtl):
        cases.append(dict(label=label, recorded=recorded, live=live, head=head,
                          paths=sorted(paths), rtl=rtl))

    docs = repo.change(b0, {"docs/a.md": "doc a lane\n"}, "lane docs")
    case("C1 stale-base docs-only", b0, d1, docs, ["docs/a.md"], "false")
    rtl = repo.change(b0, {"hdl/a.sv": "// lane rtl\n"}, "lane rtl")
    case("C2 stale-base RTL", b0, d1, rtl, ["hdl/a.sv"], "true")
    repo.at(b0)
    repo.git("update-index", "--cacheinfo", f"160000,{d1},protocol-processor")
    repo.git("commit", "--quiet", "-m", "lane pointer")
    ptr = repo.git("rev-parse", "HEAD")
    case("C3 submodule pointer", b0, d1, ptr, ["protocol-processor"], "true")
    repo.at(b0)
    repo.git("update-index", "--cacheinfo", f"160000,{d1},docs/ptr.md")
    repo.git("commit", "--quiet", "-m", "lane doc-shaped pointer")
    dptr = repo.git("rev-parse", "HEAD")
    case("C3b documentation-shaped submodule pointer", b0, d1, dptr, ["docs/ptr.md"], "true")
    t = repo.change(b0, {"docs/a.md": "tmp\n"}, "tmp")
    empty = repo.change(t, {"docs/a.md": "doc a\n"}, "revert tmp")
    case("C4 empty net delta", b0, d1, empty, [], "true")
    m = repo.merge_into(docs, dx)
    r1 = repo.change(m, {"hdl/x.sv": "// x original\n"}, "restore x")
    rev = repo.change(r1, {"docs/a.md": "doc a lane final\n"}, "docs")
    case("C5 REV", b0, dx, rev, ["docs/a.md", "hdl/x.sv"], "true")
    case("C6 REV+E", b0, de, rev, ["docs/a.md", "hdl/x.sv"], "true")
    k1 = repo.change(b0, {"hdl/a.sv": "// buried rtl\n"}, "rtl first")
    k2 = repo.change(k1, {"docs/a.md": "d1\n"}, "docs 1")
    k3 = repo.change(k2, {"docs/page.md": page + "more\n"}, "docs 2")
    buried = repo.change(k3, {"README.md": "readme 2\n"}, "docs 3")
    case("C7 RTL buried under later docs commits", b0, de, buried,
         ["README.md", "docs/a.md", "docs/page.md", "hdl/a.sv"], "true")
    dele = repo.change(b0, {"hdl/a.sv": None}, "delete rtl")
    case("C8 RTL deletion", b0, d1, dele, ["hdl/a.sv"], "true")
    repo.at(b0)
    repo.git("mv", "hdl/a.sv", "docs/a_moved.md")
    mv = repo.commit("rename rtl into docs", [])
    case("C9 RTL renamed into docs", b0, d1, mv, ["docs/a_moved.md", "hdl/a.sv"], "true")
    repo.at(b0)
    (repo.root / "hdl/a.sv").chmod(0o755)
    mode = repo.commit("mode only", ["hdl/a.sv"])
    case("C10 RTL mode-only", b0, d1, mode, ["hdl/a.sv"], "true")
    lx = repo.change(b0, {"hdl/x.sv": "// x lane\n"}, "lane x")
    lm = repo.merge_into(lx, dx, resolve={"hdl/x.sv": "// x lane\n"})
    keep = repo.change(lm, {"docs/a.md": "after merge\n"}, "docs")
    case("C11 conflict resolved to lane RTL", b0, dx, keep, ["docs/a.md", "hdl/x.sv"], "true")
    pm = repo.merge_into(docs, dx)
    plain = repo.change(pm, {"docs/a.md": "lane after plain merge\n"}, "docs")
    case("C12 lane merged dev cleanly, own change docs", b0, dx, plain, ["docs/a.md"], "false")
    uni = repo.change(b0, {"hdl/é.sv": "// unicode\n"}, "unicode rtl")
    case("C13 non-ASCII RTL path (quoted)", b0, d1, uni, ['"hdl/\\303\\251.sv"'], "true")
    gm = repo.change(b0, {".gitmodules": '[submodule "protocol-processor"]\n\tpath = protocol-processor\n'
                          '\turl = https://example.invalid/other.git\n'}, "gitmodules")
    case("C14 .gitmodules only", b0, d1, gm, [".gitmodules"], "true")
    repo.at(d1)
    (repo.root / "docs/reference").mkdir(parents=True, exist_ok=True)
    repo.git("mv", "docs/page.md", "docs/reference/REGISTER_MAP.md")
    ren = repo.commit("dev renames page into gate-read path", [])
    ed = repo.change(b0, {"docs/page.md": page.replace("line 7", "line seven")}, "lane edits page")
    case("C15 base-side rename into gate-read doc", b0, ren, ed,
         ["docs/reference/REGISTER_MAP.md"], "true")
    extras = dict(b0=b0, d1=d1, dx=dx, de=de, buried=buried, docs=docs)
    return cases, extras


MUTANTS = {
    "MH1 hosted two-dot frozen base": ('"$GITHUB_SHA^1" "$GITHUB_SHA"', '"$PR_BASE_SHA" "$GITHUB_SHA"'),
    "MH2 hosted frozen merge-base": ('"$GITHUB_SHA^1" "$GITHUB_SHA"', '"$PR_BASE_SHA...$PR_HEAD_SHA"'),
    "MH3 hosted head first-parent only": ('"$GITHUB_SHA^1" "$GITHUB_SHA"', '"$PR_HEAD_SHA^1" "$PR_HEAD_SHA"'),
    "MR1 replay frozen recorded base": ('"refs/remotes/origin/$PR_BASE_REF"', '"$PR_BASE_SHA"'),
    "MR2 replay head-only merge-base": ('"refs/remotes/origin/$PR_BASE_REF" "$merged"', '"$base" "$PR_HEAD_SHA"'),
    "MR3 replay live-to-head two-dot": ('"refs/remotes/origin/$PR_BASE_REF" "$merged"',
                                        '"refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA"'),
}
CLASSIFIER_MUTANTS = {
    "MC1 hdl/ treated as docs": ('DOC_PREFIXES = ["LICENSES/"]', 'DOC_PREFIXES = ["LICENSES/", "hdl/"]'),
    "MC2 submodule rule removed": ("is_submodule_path(clean) or ", ""),
    "MC3 empty-diff rule removed": ("not changed or ", ""),
}


def run_case(repo: Repo, body: str, c: dict, mode: str) -> dict:
    if mode == "hosted":
        merge = repo.github_merge(c["live"], c["head"])
        repo.at(merge)
        repo.git("update-ref", "refs/remotes/origin/dev", c["live"])
        return execute(repo.root, repo.env, body, mode=mode, recorded=c["recorded"],
                       head=c["head"], sha=merge)
    repo.at(c["head"])
    repo.git("update-ref", "refs/remotes/origin/dev", c["live"])
    return execute(repo.root, repo.env, body, mode=mode, recorded=c["recorded"],
                   head=c["head"], sha=c["head"])


def ok(c: dict, r: dict) -> bool:
    return r["rc"] == 0 and r["rtl"] == c["rtl"] and sorted(r["paths"] or []) == c["paths"]


def b16(gitdir: pathlib.Path, cand: pathlib.Path, scratch: pathlib.Path, home: pathlib.Path) -> dict:
    head, recorded = "f1b2489f5b1c929e81eeae79a469b2b27c47e340", "49da9fd974e8805d56c90e29dcfcb67994c2c430"
    landed = "6c810c45ac4ac7d5b45797430753020c9ea31d86"
    env = hermetic(home)
    env["GIT_DIR"] = str(gitdir)

    def g(*a):
        return subprocess.run(["git", *a], env=env, capture_output=True, text=True, check=True).stdout

    live = g("rev-parse", f"{landed}^1").strip()
    assert g("rev-parse", f"{landed}^2").strip() == head
    res = {"head": head, "recorded": recorded, "landed_merge": landed, "live_first_parent": live,
           "two_dot_default_renames": len(g("diff", "--name-only", recorded, head).split()),
           "two_dot_no_renames": len(g("diff", "--no-renames", "--name-only", recorded, head).split()),
           "three_dot_no_renames": g("diff", "--no-renames", "--name-only", f"{recorded}...{head}").split()}
    # Execute the shipping bodies with GIT_DIR pointing at the real history and a
    # work dir holding only the candidate classifier and the landed .gitmodules.
    wd = scratch / "b16-work"
    shutil.rmtree(wd, ignore_errors=True)
    (wd / "scripts").mkdir(parents=True)
    shutil.copyfile(cand / "scripts/ci_scope.py", wd / "scripts/ci_scope.py")
    (wd / ".gitmodules").write_text(g("show", f"{landed}:.gitmodules"))
    subprocess.run(["git", "update-ref", "refs/remotes/origin/dev", live], env=env, check=True)
    runs = {}
    for wf, body in bodies(cand).items():
        runs[wf] = {
            "hosted(real landed merge)": execute(wd, env, body, mode="hosted", recorded=recorded,
                                                 head=head, sha=landed, work_tree_dir=wd),
            "replay(live=first parent)": execute(wd, env, body, mode="replay", recorded=recorded,
                                                 head=head, sha=head, work_tree_dir=wd),
        }
    subprocess.run(["git", "update-ref", "-d", "refs/remotes/origin/dev"], env=env, check=True)
    res["runs"] = runs
    res["ok"] = all(r["rc"] == 0 and r["rtl"] == "false" and len(r["paths"]) == 2
                    and all(p.startswith("docs/findings/") for p in r["paths"])
                    for w in runs.values() for r in w.values())
    return res


def main() -> int:
    cand, out = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2])
    gitdir = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
    report: dict = {"candidate": cand.as_posix(), "results": [], "mutants": [], "push": []}
    failures = 0
    with tempfile.TemporaryDirectory(prefix="r632-4-probe-") as raw:
        base = pathlib.Path(raw)
        (base / "home").mkdir()
        repo = Repo(base / "repo", base / "home")
        repo.root.mkdir()
        cases, extras = build(repo, cand)
        shipped = bodies(cand)
        for wf, body in shipped.items():
            for c in cases:
                for mode in ("hosted", "replay"):
                    r = run_case(repo, body, c, mode)
                    good = ok(c, r)
                    failures += not good
                    report["results"].append(dict(workflow=wf, case=c["label"], mode=mode,
                                                  expected=[c["paths"], c["rtl"]], got=r, ok=good))
            # replay must refuse a criss-cross (ambiguous) ancestry, never answer docs-only
            l1 = repo.change(extras["b0"], {"docs/l.md": "l\n"}, "left")
            r1 = repo.change(extras["b0"], {"docs/r.md": "r\n"}, "right")
            x1 = repo.merge_into(l1, r1)
            x2 = repo.merge_into(r1, l1)
            cc = dict(label="criss-cross", recorded=extras["b0"], live=x1, head=x2, paths=[], rtl="true")
            rr = run_case(repo, body, cc, "replay")
            good = rr["rc"] != 0 and rr["rtl"] is None
            failures += not good
            report["results"].append(dict(workflow=wf, case="C16 criss-cross replay refuses",
                                          mode="replay", got=rr, ok=good))
            # replay must refuse a merge conflict
            cl = repo.change(extras["b0"], {"hdl/x.sv": "// live conflict\n"}, "live conflict")
            ch = repo.change(extras["b0"], {"hdl/x.sv": "// head conflict\n"}, "head conflict")
            cf = dict(label="conflict", recorded=extras["b0"], live=cl, head=ch, paths=[], rtl="true")
            rr = run_case(repo, body, cf, "replay")
            good = rr["rc"] != 0 and rr["rtl"] is None
            failures += not good
            report["results"].append(dict(workflow=wf, case="C17 conflict replay refuses",
                                          mode="replay", got=rr, ok=good))
            # Diagnostic only: the hosted branch run on a bare PR head (as if the
            # replay marker were absent) sees only the head's last commit.
            repo.at(extras["buried"])
            diag = execute(repo.root, repo.env, body, mode="hosted", recorded=extras["b0"],
                           head=extras["buried"], sha=extras["buried"])
            report["results"].append(dict(workflow=wf, case="D1 diagnostic: hosted branch on bare head",
                                          mode="hosted-without-merge", got=diag, ok=None))
            # Push events keep their behaviour.
            repo.at(extras["dx"])
            pr = execute(repo.root, repo.env, body, mode="hosted", recorded="", head="",
                         sha=extras["dx"], event="push", before=extras["d1"])
            p0 = execute(repo.root, repo.env, body, mode="hosted", recorded="", head="",
                         sha=extras["dx"], event="push", before="0" * 40)
            if wf == "rtl-fast.yml":
                good = (pr["rc"] == 0 and pr["paths"] == ["hdl/x.sv"] and pr["rtl"] == "true"
                        and p0["rc"] == 0 and p0["rtl"] == "true" and len(p0["paths"]) > 5)
            else:
                good = pr["rc"] == 0 and pr["rtl"] == "true" and p0["rc"] == 0 and p0["rtl"] == "true"
            failures += not good
            report["push"].append(dict(workflow=wf, before_diff=pr, zero_before=p0, ok=good))
            # Mutations of the step body: each must break at least one control.
            for name, (old, new) in MUTANTS.items():
                assert body.count(old) >= 1, (wf, name)
                mbody = body.replace(old, new)
                broken = []
                for c in cases:
                    for mode in ("hosted", "replay"):
                        if ("MH" in name) != (mode == "hosted"):
                            continue
                        if not ok(c, run_case(repo, mbody, c, mode)):
                            broken.append(f"{c['label']}/{mode}")
                killed = bool(broken)
                failures += not killed
                report["mutants"].append(dict(workflow=wf, mutant=name, killed_by=broken, killed=killed))
            # Classifier rule removals.
            clf = repo.root / "scripts/ci_scope.py"
            for name, (old, new) in CLASSIFIER_MUTANTS.items():
                broken = []
                for c in cases:
                    for mode in ("hosted", "replay"):
                        if mode == "hosted":
                            merge = repo.github_merge(c["live"], c["head"])
                            repo.at(merge)
                        else:
                            repo.at(c["head"])
                            repo.git("update-ref", "refs/remotes/origin/dev", c["live"])
                        pristine = clf.read_text()
                        assert pristine.count(old) == 1, name
                        clf.write_text(pristine.replace(old, new))
                        try:
                            r = execute(repo.root, repo.env, body, mode=mode, recorded=c["recorded"],
                                        head=c["head"], sha=merge if mode == "hosted" else c["head"])
                        finally:
                            repo.git("checkout", "--quiet", "--", "scripts/ci_scope.py")
                        if not ok(c, r):
                            broken.append(f"{c['label']}/{mode}")
                killed = bool(broken)
                failures += not killed
                report["mutants"].append(dict(workflow=wf, mutant=name, killed_by=broken, killed=killed))
        if gitdir:
            report["b16"] = b16(gitdir, cand, base, base / "home")
            failures += not report["b16"]["ok"]
    report["failures"] = failures
    out.write_text(json.dumps(report, indent=1, sort_keys=True))
    for r in report["results"]:
        flag = "ok  " if r["ok"] else ("diag" if r["ok"] is None else "FAIL")
        print(f"{flag} {r['workflow']:14s} {r['mode']:22s} {r['case']}: rc={r['got']['rc']} "
              f"rtl={r['got']['rtl']} paths={r['got']['paths']}")
    for p in report["push"]:
        print(f"{'ok  ' if p['ok'] else 'FAIL'} {p['workflow']:14s} push events: before-diff rtl="
              f"{p['before_diff']['rtl']} paths={p['before_diff']['paths']}; zero-before rtl={p['zero_before']['rtl']}")
    for m in report["mutants"]:
        print(f"{'ok  ' if m['killed'] else 'FAIL'} {m['workflow']:14s} {m['mutant']}: killed by {m['killed_by']}")
    if gitdir:
        b = report["b16"]
        print(f"B16: two-dot(default renames)={b['two_dot_default_renames']} two-dot(--no-renames)="
              f"{b['two_dot_no_renames']} three-dot={b['three_dot_no_renames']} live={b['live_first_parent']}")
        for wf, runs in b["runs"].items():
            for mode, r in runs.items():
                print(f"  B16 {wf} {mode}: rc={r['rc']} rtl={r['rtl']} paths={r['paths']}")
        print(f"{'ok  ' if b['ok'] else 'FAIL'} B16 docs-only in every executed shipping body")
    print("probe:", "PASS" if failures == 0 else f"{failures} FAILURE(S)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
