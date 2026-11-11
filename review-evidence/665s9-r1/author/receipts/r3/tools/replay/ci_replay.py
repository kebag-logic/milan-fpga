#!/usr/bin/env python3
"""ci_replay.py - run every `run:` step of the workflows a pull_request to dev-soft-core triggers, natively, one
job instance at a time, each on its own clean clone of one head ([A760] reuses [A757]'s copy for #870; first written for #665 S6b).

usage:
  ci_replay.py plan <head>                          the job instances, their needs and whether they run
  ci_replay.py job <head> <workflow> <job> [<k>]    run one job instance (matrix index k), in this process
  ci_replay.py tick <head> <max-units>              launch every ready instance as its own unit, up to max-units
  ci_replay.py local <head>                         run ready instances one at a time in this process's own unit
  ci_replay.py table <head> <out.md> <not_run.json> the rc of every run: step, and why any did not run

The step list comes from the workflow in the clone, never from a list kept here. A step runs as GitHub runs a
`run:` step with no shell named (bash --noprofile --norc -eo pipefail). OVERRIDES (overrides.json, beside this
file) names each step that cannot run on this host, with its reason, or replaces it with the part that can, with
its reason; the table lists every one. ${{ }} expressions are evaluated against the event a ready pull_request to
dev-soft-core would carry, and against the steps and jobs already run. The scope steps take their replay branch
(ACT=true) against origin/dev-soft-core, because the head is not GitHub's merge commit.
"""
from __future__ import annotations

import fnmatch
import glob as globmod
import hashlib
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

LANE = Path("<lane>")
SCRATCH = Path("<scratch>/ci")
TMP = Path("<scratch>/tmpci")
WORKFLOWS = ("docs", "elaborate", "rtl-fast", "rtl")
REPO = "kebag-logic/milan-fpga"
BASE = "dev-soft-core"
#: every job venv's base: CPython 3.12.3, the runner image's version, whose pinned wheels (pyslang, the
#: Markdown renderer) exist for it; it was built without pidfd_open, so pidfd_shim.py provides the two calls
PY = Path("<tools>/uvpy/cpython-3.12.3-linux-x86_64-gnu/bin/python3.12")
LITEX_VENV = Path("<home>/litex-milan/venv/bin")
SDK = Path("<scratch>/sdk/br-milan-rv32")
TOOLS = ("<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:"
         "/usr/local/sbin:/usr/local/bin:/usr/bin:/bin")
OVERRIDES = json.loads(Path(__file__).with_name("overrides.json").read_text())
#: the job instances the LiteX tree's venv runs (the boundary gate's LiteX, the pinned tree the split image uses)
LITEX_JOBS = {"rtl-fast/firmware-boundary"}


# ---- GitHub expressions --------------------------------------------------------------------------------------

TOKEN = re.compile(r"\s*(?:(?P<str>'(?:[^']|'')*')|(?P<num>-?\d+(?:\.\d+)?)|(?P<op>==|!=|<=|>=|&&|\|\||[!<>()\[\],.])"
                   r"|(?P<id>[A-Za-z_][A-Za-z0-9_-]*|\*))")


def tokens(text: str) -> list[tuple[str, str]]:
    """The expression's tokens."""
    out, at = [], 0
    while at < len(text):
        m = TOKEN.match(text, at)
        if not m or m.end() == at:
            if text[at:].strip() == "":
                break
            raise ValueError(f"expression: cannot read {text[at:]!r}")
        kind = m.lastgroup
        out.append((kind, m.group(kind)))
        at = m.end()
    return out


class Expr:
    """A recursive-descent evaluator for the subset of GitHub's expression syntax the workflows use."""

    def __init__(self, text: str, ctx: dict) -> None:
        self.t = tokens(text)
        self.i = 0
        self.ctx = ctx

    def peek(self) -> str | None:
        return self.t[self.i][1] if self.i < len(self.t) else None

    def take(self) -> tuple[str, str]:
        self.i += 1
        return self.t[self.i - 1]

    def value(self) -> object:
        v = self.orexpr()
        if self.i != len(self.t):
            raise ValueError(f"expression: trailing {self.t[self.i:]}")
        return v

    def orexpr(self) -> object:
        v = self.andexpr()
        while self.peek() == "||":
            self.take()
            w = self.andexpr()
            v = v if truthy(v) else w
        return v

    def andexpr(self) -> object:
        v = self.notexpr()
        while self.peek() == "&&":
            self.take()
            w = self.notexpr()
            v = w if truthy(v) else v
        return v

    def notexpr(self) -> object:
        if self.peek() == "!":
            self.take()
            return not truthy(self.notexpr())
        return self.compare()

    def compare(self) -> object:
        v = self.primary()
        if self.peek() in ("==", "!=", "<", ">", "<=", ">="):
            op = self.take()[1]
            w = self.primary()
            a, b = loose(v), loose(w)
            if op in ("==", "!="):
                return (a == b) == (op == "==")
            a, b = number(a), number(b)
            return {"<": a < b, ">": a > b, "<=": a <= b, ">=": a >= b}[op]
        return v

    def primary(self) -> object:
        kind, tok = self.take()
        if tok == "(":
            v = self.orexpr()
            assert self.take()[1] == ")"
            return v
        if kind == "str":
            return tok[1:-1].replace("''", "'")
        if kind == "num":
            return float(tok) if "." in tok else int(tok)
        if tok in ("true", "false"):
            return tok == "true"
        if tok == "null":
            return None
        if self.peek() == "(":
            self.take()
            args = []
            while self.peek() != ")":
                args.append(self.orexpr())
                if self.peek() == ",":
                    self.take()
            self.take()
            return call(tok, args, self.ctx)
        v = self.ctx.get(tok)
        while self.peek() in (".", "["):
            if self.take()[1] == ".":
                key = self.take()[1]
            else:
                key = self.orexpr()
                assert self.take()[1] == "]"
            v = v.get(key) if isinstance(v, dict) else None
        return v


def truthy(v: object) -> bool:
    """GitHub's truthiness: '' 0 false null are false."""
    return v not in (None, False, 0, "", 0.0)


def loose(v: object) -> object:
    """GitHub's loose equality: strings compare case-insensitively."""
    return v.lower() if isinstance(v, str) else v


def number(v: object) -> float:
    """GitHub's numeric coercion for an ordering comparison: null and false 0, true 1, a string its number."""
    if v is None or v is False or v == "":
        return 0.0
    if v is True:
        return 1.0
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


def call(name: str, args: list, ctx: dict) -> object:
    """The functions the workflows call."""
    status = ctx.get("_status", "success")
    if name == "always":
        return True
    if name == "success":
        return status == "success"
    if name == "failure":
        return status == "failure"
    if name == "cancelled":
        return False
    if name == "toJSON":
        return json.dumps(args[0], indent=2)
    if name == "fromJSON":
        return json.loads(args[0])
    if name == "contains":
        return (str(args[1]).lower() in str(args[0]).lower()) if isinstance(args[0], str) else args[1] in args[0]
    if name == "startsWith":
        return str(args[0]).lower().startswith(str(args[1]).lower())
    if name == "endsWith":
        return str(args[0]).lower().endswith(str(args[1]).lower())
    if name == "format":
        return re.sub(r"\{(\d+)\}", lambda m: text(args[1 + int(m.group(1))]), args[0])
    if name == "hashFiles":
        return "0" * 64
    raise ValueError(f"expression: unknown function {name}")


def text(v: object) -> str:
    """A value as GitHub interpolates it."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v)
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def interpolate(s: object, ctx: dict) -> str:
    """Every ${{ }} of a string replaced by its value."""
    return re.sub(r"\$\{\{(.*?)\}\}", lambda m: text(Expr(m.group(1), ctx).value()), str(s), flags=re.S)


def condition(cond: object, ctx: dict, default: str = "success()") -> bool:
    """A job's or step's if:, with or without its ${{ }}."""
    c = str(cond).strip() if cond not in (None, "") else default
    if c.startswith("${{") and c.endswith("}}"):
        c = c[3:-2]
    if not re.search(r"\b(always|success|failure|cancelled)\(", c):
        c = f"success() && ({c})"
    return truthy(Expr(c, ctx).value())


# ---- the plan ------------------------------------------------------------------------------------------------

def workflow(head: str, wf: str) -> dict:
    """A workflow as the head carries it."""
    return yaml.safe_load(subprocess.run(["git", "show", f"{head}:.github/workflows/{wf}.yml"], cwd=LANE,
                                         check=True, capture_output=True, text=True).stdout)


def matrix(spec: dict) -> list[dict]:
    """A job's matrix combinations (one empty one without a matrix)."""
    m = (spec.get("strategy") or {}).get("matrix")
    if not m:
        return [{}]
    keys = [k for k in m if k not in ("include", "exclude")]
    combos = [dict(zip(keys, vals)) for vals in itertools.product(*[m[k] for k in keys])]
    return combos + list(m.get("include") or [])


def instances(head: str) -> list[dict]:
    """Every job instance of the four workflows."""
    out = []
    for wf in WORKFLOWS:
        for job, spec in workflow(head, wf)["jobs"].items():
            needs = spec.get("needs") or []
            needs = [needs] if isinstance(needs, str) else needs
            combos = matrix(spec)
            for k, combo in enumerate(combos):
                out.append({"wf": wf, "job": job, "k": k, "n": len(combos), "matrix": combo, "needs": needs,
                            "name": f"{wf}__{job}" + (f"__{k}" if len(combos) > 1 else "")})
    return out


def root(head: str) -> Path:
    """This head's replay directory."""
    return SCRATCH / head[:12]


def result(head: str, wf: str, job: str) -> dict | None:
    """A job's result once every instance of it finished: its status and its outputs (the first instance's)."""
    found = sorted((root(head) / "jobs").glob(f"{wf}__{job}*/result.json"))
    found = [p for p in found if re.fullmatch(rf"{re.escape(wf)}__{re.escape(job)}(__\d+)?", p.parent.name)]
    want = next(i["n"] for i in instances_cached(head) if i["wf"] == wf and i["job"] == job)
    if len(found) < want:
        return None
    rows = [json.loads(p.read_text()) for p in found]
    status = "failure" if any(r["result"] == "failure" for r in rows) else \
        "success" if any(r["result"] == "success" for r in rows) else "skipped"
    return {"result": status, "outputs": rows[0].get("outputs", {})}


_CACHE: dict = {}


def instances_cached(head: str) -> list[dict]:
    """instances(), read once."""
    if head not in _CACHE:
        _CACHE[head] = instances(head)
    return _CACHE[head]


def event(head: str) -> dict:
    """The github context of a ready pull_request from this lane's branch to dev-soft-core."""
    return {"event_name": "pull_request", "sha": head, "repository": REPO, "ref": "refs/pull/0/merge",
            "base_ref": BASE, "head_ref": "665-s9-split-image", "run_id": "0", "run_attempt": "1", "token": "",
            "server_url": "https://github.com", "actor": "replay", "repository_owner": REPO.split("/")[0],
            "event": {"before": "", "pull_request": {"draft": False, "base": {"ref": BASE},
                                                     "head": {"sha": head, "repo": {"full_name": REPO}}}}}


# ---- one job instance ------------------------------------------------------------------------------------------

def git(*args: str, cwd: Path) -> str:
    """One git command's output."""
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def clone(head: str, wt: Path, home: Path) -> None:
    """A clean clone of the head, its submodules from the lane's, origin/dev-soft-core and origin/dev as the lane
    last fetched them."""
    git("clone", "-q", "--shared", "--no-checkout", str(LANE), str(wt), cwd=wt.parent)
    git("fetch", "-q", str(LANE), head, "refs/remotes/origin/dev-soft-core:refs/remotes/origin/dev-soft-core",
        "refs/remotes/origin/dev:refs/remotes/origin/dev", cwd=wt)
    git("-c", "advice.detachedHead=false", "checkout", "-q", "--detach", head, cwd=wt)
    assert git("rev-parse", "HEAD", cwd=wt) == head and git("status", "--porcelain", cwd=wt) == ""
    for line in git("config", "--blob", f"{head}:.gitmodules", "--get-regexp", r"^submodule\..*\.path$",
                    cwd=wt).splitlines():
        dep = line.split()[1]
        # tsn-c-stack keeps its declared origin: the gate receipts refuse any other (ci_case_receipts.py)
        if dep != "third_party/tsn-c-stack" and (LANE / dep / ".git").exists():
            git("config", f"submodule.{dep}.url", str(LANE / dep), cwd=wt)
    git("remote", "set-url", "origin", f"https://github.com/{REPO}.git", cwd=wt)


#: git's settings for a job, as environment and with no config file written: the file protocol for the
#: submodules the clone points at the lane (GIT_ALLOW_PROTOCOL), and an identity (GIT_AUTHOR_*, GIT_COMMITTER_*).
#: No GIT_CONFIG_* variable: tb/verilator/gptp_shadow/private_inputs.py refuses one as injected configuration.
GIT_ENV = {"GIT_ALLOW_PROTOCOL": "file:https", "GIT_AUTHOR_NAME": "replay", "GIT_AUTHOR_EMAIL": "replay@invalid",
           "GIT_COMMITTER_NAME": "replay", "GIT_COMMITTER_EMAIL": "replay@invalid"}


def venv(inst: dict, work: Path) -> Path:
    """The job's python: a fresh venv in /tmp with PyYAML, as the runner image's system python carries it, or the
    LiteX tree's venv."""
    if f"{inst['wf']}/{inst['job']}" in LITEX_JOBS:
        return LITEX_VENV
    v = TMP / "venvs" / inst["name"]
    if v.exists():
        shutil.rmtree(v)
    subprocess.run([str(PY), "-m", "venv", str(v)], check=True)
    shutil.copy2(Path(__file__).with_name("pidfd_shim.py"), v / "lib/python3.12/site-packages/sitecustomize.py")
    # the runner image's system python carries PyYAML (python3-yaml); a bare venv does not
    subprocess.run([str(v / "bin/python3"), "-m", "pip", "install", "--quiet", "--cache-dir", str(TMP / "pip-cache"),
                    "pyyaml"], check=True)
    return v / "bin"


def upload(step: dict, ctx: dict, art: Path, wt: Path) -> int:
    """actions/upload-artifact: the paths' files under artifacts/<name>, relative to their common ancestor."""
    w = step.get("with") or {}
    name = interpolate(w["name"], ctx)
    paths = []
    for line in interpolate(w["path"], ctx).splitlines():
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        p = line if os.path.isabs(line) else str(wt / line)
        paths += globmod.glob(os.path.expanduser(p), recursive=True)
    if not paths:
        return 1 if w.get("if-no-files-found", "warn") == "error" else 0
    top = Path(os.path.commonpath(paths))
    top = top if top.is_dir() and len(paths) > 1 or Path(paths[0]).is_dir() and len(paths) == 1 else top.parent
    dest = art / name
    dest.mkdir(parents=True, exist_ok=True)
    for p in map(Path, paths):
        target = dest / p.relative_to(top) if p != top else dest
        if p.is_dir():
            shutil.copytree(p, target, dirs_exist_ok=True, symlinks=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
    return 0


def download(step: dict, ctx: dict, art: Path, wt: Path) -> int:
    """actions/download-artifact: one named artifact into path, or each matching one into path/<name>."""
    w = step.get("with") or {}
    path = Path(interpolate(w.get("path", "."), ctx))
    path = path if path.is_absolute() else wt / path
    if "name" in w:
        src = art / interpolate(w["name"], ctx)
        if not src.exists():
            return 1
        shutil.copytree(src, path, dirs_exist_ok=True, symlinks=True)
        return 0
    pattern = interpolate(w.get("pattern", "*"), ctx)
    for src in sorted(art.iterdir()) if art.exists() else []:
        if fnmatch.fnmatch(src.name, pattern):
            dest = path if w.get("merge-multiple") else path / src.name
            shutil.copytree(src, dest, dirs_exist_ok=True, symlinks=True)
    return 0


def env_file(path: Path) -> dict:
    """A GITHUB_ENV or GITHUB_OUTPUT file's assignments, heredoc form included."""
    out, lines, i = {}, path.read_text().splitlines() if path.exists() else [], 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([^=<]+)<<(.+)$", line)
        if m:
            key, mark, body = m.group(1), m.group(2), []
            i += 1
            while i < len(lines) and lines[i] != mark:
                body.append(lines[i])
                i += 1
            out[key] = "\n".join(body)
        elif "=" in line:
            k, v = line.split("=", 1)
            out[k] = v
        i += 1
    return out


def run_job(head: str, wf: str, job: str, k: int) -> int:
    """One job instance: its clone, its steps in order, its result."""
    inst = next(i for i in instances_cached(head) if i["wf"] == wf and i["job"] == job and i["k"] == k)
    spec = workflow(head, wf)["jobs"][job]
    work = root(head) / "jobs" / inst["name"]
    if (work / "result.json").exists():
        return 0
    if work.exists():
        shutil.rmtree(work)
    for d in ("wt", "home", "temp", "tmp", "logs"):
        (work / d).mkdir(parents=True)
    wt, home, temp, logs = work / "wt", work / "home", work / "temp", work / "logs"
    art = root(head) / "artifacts"
    art.mkdir(parents=True, exist_ok=True)
    needs = {n: result(head, wf, n) for n in inst["needs"]}
    ctx = {"github": event(head), "runner": {"temp": str(temp), "os": "Linux", "arch": "X64",
                                             "tool_cache": str(TMP / "toolcache")},
           "needs": needs, "matrix": inst["matrix"], "strategy": {"job-index": k, "job-total": inst["n"]},
           "job": {"status": "success"}, "steps": {}, "inputs": {}, "secrets": {}, "vars": {}, "env": {}}
    ctx["github"]["workspace"] = str(wt)
    rows: list[dict] = []
    status = "success" if all(v and v["result"] == "success" for v in needs.values()) else "failure"
    ctx["_status"] = status
    if not condition(spec.get("if"), ctx):
        (work / "result.json").write_text(json.dumps({"result": "skipped", "outputs": {}, "steps": []}, indent=1))
        return 0
    status = "success"
    ctx["_status"] = status
    clone(head, wt, home)
    (home / "opt" / "bin").mkdir(parents=True)
    (home / "opt" / "verilator").symlink_to("<tools>/verilator-v5.050")
    (home / "opt" / "yosys" / "bin").mkdir(parents=True)
    (home / "opt" / "yosys" / "bin" / "yosys").symlink_to("/usr/bin/yosys")
    (home / "opt" / "yosys" / "ABC_REV").write_text("host package yosys 0.66 at 86f2ddeb, ABC linked in\n")
    # actions/cache's hit for the sv2v archive (ci-sv2v-cache), from an archive a job here downloaded: the step
    # checks its sha256 as on a hit
    if (TMP / "cache" / "sv2v.zip").exists():
        (temp / "ci-sv2v-cache").mkdir()
        shutil.copy2(TMP / "cache" / "sv2v.zip", temp / "ci-sv2v-cache" / "sv2v.zip")
    py = venv(inst, work)
    gh_env, gh_path = work / "github_env", work / "github_path"
    gh_env.touch()
    gh_path.touch()
    base = {k2: v for k2, v in os.environ.items() if k2 in ("LANG", "LC_ALL", "USER", "TERM", "LOGNAME")}
    base.update(HOME=str(home), RUNNER_TEMP=str(temp), TMPDIR=str(work / "tmp"), GITHUB_WORKSPACE=str(wt),
                GITHUB_ENV=str(gh_env), GITHUB_PATH=str(gh_path), GITHUB_SHA=head, GITHUB_REPOSITORY=REPO,
                GITHUB_EVENT_NAME="pull_request", GITHUB_REF="refs/pull/0/merge", GITHUB_BASE_REF=BASE,
                GITHUB_HEAD_REF="665-s9-split-image", GITHUB_RUN_ID="0", GITHUB_RUN_ATTEMPT="1", GITHUB_JOB=job,
                GITHUB_ACTIONS="true", CI="true", ACT="true", RUNNER_OS="Linux", RUNNER_ARCH="X64",
                PIP_CACHE_DIR=str(TMP / "pip-cache"), PIP_DISABLE_PIP_VERSION_CHECK="1",
                VERILATOR="<tools>/pinned-verilator-5.050/verilator",
                TSN_GEN_ROOT="<home>/milan-fpga-management/tools/tsn-gen-deca300c", **GIT_ENV)
    wf_env = workflow(head, wf).get("env") or {}
    limit = 60 * 3 * int(interpolate(spec.get("timeout-minutes", 360), ctx) or 360)
    started = time.monotonic()
    for n, step in enumerate(spec["steps"]):
        sid = step.get("id") or f"step{n}"
        key = f"{wf}/{job}/{sid}"
        ctx["env"] = {**{a: interpolate(b, ctx) for a, b in wf_env.items()},
                      **{a: interpolate(b, ctx) for a, b in (spec.get("env") or {}).items()}, **env_file(gh_env)}
        row = {"step": sid, "name": step.get("name") or step.get("uses", ""), "kind": "run" if "run" in step else
               step.get("uses", "").split("@")[0]}
        if not condition(step.get("if"), ctx):
            row["rc"] = "skipped (if: false)"
            ctx["steps"][sid] = {"outcome": "skipped", "conclusion": "skipped", "outputs": {}}
            rows.append(row)
            continue
        out_file = work / f"output_{sid}"
        out_file.touch()
        e = dict(base)
        e.update(ctx["env"])
        e.update({a: interpolate(b, ctx) for a, b in (step.get("env") or {}).items()})
        paths = [p for p in gh_path.read_text().splitlines() if p.strip()]
        e["PATH"] = ":".join([*reversed(paths), str(home / "opt" / "bin"), str(py), TOOLS])
        e["GITHUB_OUTPUT"] = str(out_file)
        e["GITHUB_STEP_SUMMARY"] = str(work / "summary.md")
        rc = 0
        if "run" in step:
            override = override_for(key, row["name"])
            script, changed = transformed(interpolate(step["run"], ctx))
            if changed:
                row["transformed"] = TRANSFORMS_WHY
            if override and "skip" in override:
                row["rc"] = "not run"
                row["reason"] = override["skip"]
                rc = None
            else:
                if override:
                    script, row["replaced"] = override["replace"], override["reason"]
                (work / f"{sid}.sh").write_text(script)
                log = logs / f"{inst['name']}__{sid}.log"
                with log.open("w") as fh:
                    fh.write(f"# head {head} {key}: {row['name']}\n")
                    fh.flush()
                    cwd = wt / step["working-directory"] if step.get("working-directory") else wt
                    left = max(60, limit - int(time.monotonic() - started))
                    rc = subprocess.run(["timeout", "-k", "30", str(left), "bash", "--noprofile", "--norc", "-eo",
                                         "pipefail", str(work / f"{sid}.sh")], cwd=cwd, env=e, stdout=fh,
                                        stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL).returncode
                row["rc"] = rc
        elif override_for(key, row["name"]) and "skip" in override_for(key, row["name"]):
            row["rc"] = "not run"
            row["reason"] = override_for(key, row["name"])["skip"]
            rc = None
        elif row["kind"] == "actions/upload-artifact":
            rc = upload(step, ctx, art, wt)
            row["rc"] = rc
        elif row["kind"] == "actions/download-artifact":
            rc = download(step, ctx, art, wt)
            row["rc"] = rc
        else:
            row["rc"] = "action (checkout by the clone; cache and setup-python not replayed)"
        ok = rc in (0, None) or step.get("continue-on-error") is True
        ctx["steps"][sid] = {"outcome": "success" if rc in (0, None) else "failure",
                             "conclusion": "success" if ok else "failure", "outputs": env_file(out_file)}
        if not ok:
            status = "failure"
            ctx["_status"] = status
            ctx["job"]["status"] = status
        rows.append(row)
    outputs = {a: interpolate(b, ctx) for a, b in (spec.get("outputs") or {}).items()}
    try:
        after = git("status", "--porcelain", cwd=wt)
    except subprocess.CalledProcessError:
        after = "(no repository: a step removed .git)"
    (work / "result.json").write_text(json.dumps({"result": status, "outputs": outputs, "steps": rows,
                                                  "tree_after": after}, indent=1))
    # the scratch is capped (15 GB): a finished job keeps its logs, step scripts and result, not its clone,
    # home, temp or venv; its uploads were copied to the run's artifacts directory
    for d in ("wt", "home", "temp", "tmp"):
        shutil.rmtree(work / d, ignore_errors=True)
    if py != LITEX_VENV:
        shutil.rmtree(py.parent, ignore_errors=True)
    print(f"{inst['name']}: {status}")
    return 0


def override_for(key: str, name: str) -> dict | None:
    """The override of one step: by its exact key, a wildcard key (fnmatch over workflow/job/step), or its name."""
    if key in OVERRIDES:
        return OVERRIDES[key]
    found = next((v for k, v in OVERRIDES.items() if "*" in k and fnmatch.fnmatch(key, k)), None)
    return found or OVERRIDES.get(f"name:{name}")


#: what every script is rewritten by, because this host is not the runner: Arch rather than Ubuntu (no apt), no
#: root (the tools a step installs under /opt or /usr/local live in the job's own $HOME/opt), and the pinned tools
#: already built (TRANSFORMS_WHY, in the table beside each step a rule changed)
TRANSFORMS = (
    (r"(?m)^([ \t]*)sudo apt-get(?:[^\n]*\\\n)*[^\n]*", r"\1: # apt-get dropped: no apt on this host"),
    (r"dpkg-query -W libgtest-dev libgmock-dev", "pacman -Q gtest"),
    (r"/tmp/sv2v\b", "$RUNNER_TEMP/sv2v"),
    (r"/usr/local/bin/", "$HOME/opt/bin/"),
    (r"-C /opt\b", '-C "$HOME/opt"'),
    (r"/opt/(verilator|yosys|sbt)\b", r"$HOME/opt/\1"),
    (r"\bsudo ", ""),
    (r'(scripts/ci_rv32_sdk\.py --destination "\$HOME/br-milan-rv32/host")',
     r'\1 --archive <tools>/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz'),
)
TRANSFORMS_WHY = ("this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, "
                  "librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or "
                  "/usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of "
                  "its pinned archive (--archive; the installer checks its sha256) rather than downloaded again")


def transformed(script: str) -> tuple[str, bool]:
    """A script rewritten by TRANSFORMS, and whether any rule changed it."""
    out = script
    for pattern, repl in TRANSFORMS:
        out = re.sub(pattern, repl, out)
    return out, out != script


# ---- the units -------------------------------------------------------------------------------------------------

def active_units() -> set[str]:
    """The replay's units still running."""
    out = subprocess.run(["systemctl", "--user", "list-units", "--plain", "--no-legend", "milan-a760e-ci-*"],
                         capture_output=True, text=True).stdout
    return {line.split()[0].removesuffix(".service") for line in out.splitlines() if " active " in f" {line} "}


def mem_available_gb() -> float:
    """MemAvailable, in GB."""
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 1e6
    return 0.0


def unit_name(inst: dict) -> str:
    """The unit an instance runs in."""
    return "milan-a760e-ci-" + hashlib.sha1(inst["name"].encode()).hexdigest()[:10]


def tick(head: str, max_units: int, min_gb: float = 25.0) -> int:
    """Launch every ready instance, up to max_units at once and while memory allows; 0 when every instance has a
    result."""
    done = 0
    active = active_units()
    launched = 0
    used: set[str] = set()
    names = json.loads((root(head) / "units.json").read_text()) if (root(head) / "units.json").exists() else {}
    for inst in instances_cached(head):
        work = root(head) / "jobs" / inst["name"]
        if (work / "result.json").exists():
            done += 1
            continue
        unit = unit_name(inst)
        if unit in active or (root(head) / "claims" / inst["name"]).exists():
            continue
        if any(result(head, inst["wf"], n) is None for n in inst["needs"]):
            continue
        if len(active) + launched >= max_units or mem_available_gb() < min_gb:
            continue
        cpus = subprocess.run([sys.executable, "<home>/milan-fpga-management/2026-09-23/cpu_ranges.py", "pick"],
                              capture_output=True, text=True).stdout.strip()
        if not cpus or cpus in used:
            print("no free CPU range")
            break
        used.add(cpus)
        names[unit] = inst["name"]
        subprocess.run(["systemd-run", "--user", f"--unit={unit}", "--collect", "--property=MemoryMax=10G",
                        "--setenv=HOME=<home>", "/usr/bin/taskset", "-c", cpus, "/usr/bin/python3", str(Path(__file__)),
                        "job", head, inst["wf"], inst["job"], str(inst["k"])], check=True, capture_output=True)
        print(f"launched {inst['name']} as {unit} on {cpus}")
        launched += 1
        time.sleep(4)
    (root(head) / "units.json").write_text(json.dumps(names, indent=1))
    total = len(instances_cached(head))
    print(f"{done} of {total} instances done, {len(active) + launched} running, MemAvailable {mem_available_gb():.1f} GB")
    return 0 if done == total else 1


#: a local job starts only while this process's own unit holds less than this (the unit stays under 10 GB)
LOCAL_MEM_GB = 6.0


def own_memory_gb() -> float:
    """The anonymous and shared memory of this process's own unit, in GB: what its jobs hold, the page cache
    (which the kernel reclaims first) left out."""
    group = Path("/proc/self/cgroup").read_text().strip().split("::", 1)[-1]
    stat = dict(line.split() for line in Path(f"/sys/fs/cgroup{group}/memory.stat").read_text().splitlines())
    return (int(stat["anon"]) + int(stat["shmem"])) / 1e9


def local(head: str) -> int:
    """Run ready instances one at a time in this process's own unit (its CPUs and memory), each claimed first so
    tick never launches it too; 0 when every instance has a result."""
    claims = root(head) / "claims"
    claims.mkdir(parents=True, exist_ok=True)
    while True:
        insts = instances_cached(head)
        done = [i for i in insts if (root(head) / "jobs" / i["name"] / "result.json").exists()]
        if len(done) == len(insts):
            print("local: every instance has a result")
            return 0
        active = active_units()
        ready = [i for i in insts if i not in done and unit_name(i) not in active
                 and not (claims / i["name"]).exists()
                 and all(result(head, i["wf"], n) is not None for n in i["needs"])]
        if not ready or own_memory_gb() > LOCAL_MEM_GB:
            time.sleep(60)
            _CACHE.pop(head, None)
            continue
        inst = None
        for cand in ready:
            try:
                os.close(os.open(claims / cand["name"], os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            except FileExistsError:
                continue
            inst = cand
            break
        if inst is None:
            time.sleep(30)
            continue
        print(f"{time.strftime('%T')} local: {inst['name']}", flush=True)
        rc = subprocess.run([sys.executable, str(Path(__file__)), "job", head, inst["wf"], inst["job"],
                             str(inst["k"])]).returncode
        print(f"{time.strftime('%T')} local: {inst['name']} rc {rc}", flush=True)
        _CACHE.pop(head, None)


def table(head: str, out: Path, not_run: Path) -> int:
    """The rc of every step of every instance, and the not-run list with each reason."""
    lines = [f"# CI replay at {head}", "", "| Workflow / job | Step | Name | rc | Note |", "|---|---|---|---|---|"]
    skipped, failed, ran = [], 0, 0
    for inst in instances_cached(head):
        p = root(head) / "jobs" / inst["name"] / "result.json"
        if not p.exists():
            lines.append(f"| {inst['name']} | | | no result | |")
            failed += 1
            continue
        r = json.loads(p.read_text())
        if r["result"] == "skipped" and not r["steps"]:
            lines.append(f"| {inst['name']} | (job) | | skipped | the job's if: is false for this event |")
            skipped.append({"job": inst["name"], "reason": "the job's if: is false for a pull_request to "
                            f"{BASE} at this head (it runs only on another event)"})
            continue
        for s in r["steps"]:
            if s["kind"] != "run" and not str(s["rc"]).isdigit():
                continue
            note = s.get("reason") or (f"replaced: {s['replaced']}" if s.get("replaced") else "")
            note = note or (f"rewritten: {s['transformed']}" if s.get("transformed") else "")
            lines.append(f"| {inst['name']} | {s['step']} | {s['name'][:60]} | {s['rc']} | {note} |")
            if s["rc"] == "not run":
                skipped.append({"step": f"{inst['name']}/{s['step']}", "reason": s["reason"]})
            elif isinstance(s["rc"], int):
                ran += 1
                failed += s["rc"] != 0
    lines += ["", f"{ran} steps ran, {failed} failed or missing; {len(skipped)} not run, each with its reason"]
    out.write_text("\n".join(lines) + "\n")
    not_run.write_text(json.dumps({"head": head, "not_run": skipped}, indent=1) + "\n")
    print(lines[-1])
    return 0 if failed == 0 else 1


def main() -> int:
    """The verbs."""
    verb, head = sys.argv[1], sys.argv[2]
    if verb == "plan":
        for inst in instances_cached(head):
            print(inst["name"], "needs", inst["needs"])
        return 0
    if verb == "job":
        return run_job(head, sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 0)
    if verb == "again":
        # a job instance to run again: its directory moved aside, kept for the record
        work = root(head) / "jobs" / sys.argv[3]
        attempt = 1
        while (root(head) / "attempts" / f"{sys.argv[3]}.{attempt}").exists():
            attempt += 1
        (root(head) / "attempts").mkdir(exist_ok=True)
        work.rename(root(head) / "attempts" / f"{sys.argv[3]}.{attempt}")
        print(f"{sys.argv[3]}: attempt {attempt} kept under attempts/")
        return 0
    if verb == "tick":
        return tick(head, int(sys.argv[3]))
    if verb == "local":
        return local(head)
    if verb == "table":
        return table(head, Path(sys.argv[3]), Path(sys.argv[4]))
    raise SystemExit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
