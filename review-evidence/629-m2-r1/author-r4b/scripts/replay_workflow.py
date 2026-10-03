#!/usr/bin/env python3
"""Replay one hosted workflow job's steps at the checked-out head, as the
workflow file spells them, under GNU make 4.3 (the hosted runner's make).

Every `run:` step runs VERBATIM (bash -e, the runner's default shell) with
the workflow, job and step env and its `${{ }}` expressions resolved, unless
the substitution file names the step: then the recorded substitute runs and
the log says so. A substitute exists only for steps that provision the
runner (sudo, /opt, apt) and cannot run on this host as written. A `uses:`
step is recorded with its local meaning. A `make` shim first on PATH logs
every make invocation of every step (cwd, argv) and execs GNU make 4.3, so
the receipt states which make ran each step and how often.

Usage: replay_workflow.py --repo R --workflow W --job J --out D
         [--matrix k=v ...] [--needs job.key=value ...] [--subst S.json]
         [--prefix-path DIR ...] [--keep-going]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

MAKE43 = Path("$VALIDATION_STORAGE/629-a517/make43/bin/make")
EXPR_RE = re.compile(r"\$\{\{\s*(.*?)\s*\}\}")


def make_shim(bindir: Path, log: Path) -> None:
    """A `make` that records each invocation, then runs GNU make 4.3."""
    bindir.mkdir(parents=True, exist_ok=True)
    shim = bindir / "make"
    shim.write_text(
        "#!/bin/sh\n"
        f"printf '%s\\t%s\\t%s\\n' \"${{REPLAY_STEP:-?}}\" \"$PWD\" \"$*\" >> {log}\n"
        f"exec {MAKE43} \"$@\"\n")
    shim.chmod(0o755)


class Context:
    """The expression context a GitHub Actions run would resolve."""

    def __init__(self, args: argparse.Namespace, head: str, runner_temp: Path):
        self.values = {
            "github.event_name": "pull_request",
            "github.sha": head,
            "github.ref": "refs/pull/634/merge",
            "github.token": "",
            "github.workflow": "",
            "github.repository": "kebag-logic/milan-fpga",
            "github.event.pull_request.base.ref": "dev",
            "github.event.pull_request.base.sha": args.base_sha,
            "github.event.pull_request.draft": "false",
            "github.event.pull_request.number": "634",
            "github.event.before": "",
            "runner.temp": str(runner_temp),
            "runner.os": "Linux",
            "runner.arch": "X64",
        }
        for item in args.matrix:
            key, value = item.split("=", 1)
            self.values[f"matrix.{key}"] = value
        for item in args.needs:
            key, value = item.split("=", 1)
            job, out = key.split(".", 1)
            self.values[f"needs.{job}.outputs.{out}"] = value
        for item in args.value:
            key, value = item.split("=", 1)
            self.values[key] = value
        self.env: dict[str, str] = {}

    def lookup(self, name: str) -> str:
        """One dotted name: env.X, steps.id.outputs.k or a fixed value."""
        if name.startswith("env."):
            return self.env.get(name[4:], "")
        return self.values.get(name, "")

    @staticmethod
    def split_top(expr: str, op: str) -> list[str]:
        """`expr` split on `op` outside parentheses and quotes."""
        parts, depth, quoted, start, i = [], 0, False, 0, 0
        while i < len(expr):
            ch = expr[i]
            if ch == "'":
                quoted = not quoted
            elif not quoted and ch == "(":
                depth += 1
            elif not quoted and ch == ")":
                depth -= 1
            elif not quoted and depth == 0 and expr.startswith(op, i):
                parts.append(expr[start:i])
                start = i + len(op)
                i += len(op)
                continue
            i += 1
        parts.append(expr[start:])
        return parts

    def evaluate(self, expr: str) -> str:
        """The subset of the expression language the four workflows use."""
        expr = expr.strip()
        for op in ("||", "&&"):
            parts = self.split_top(expr, op)
            if len(parts) > 1:
                hits = [self.truthy(self.evaluate(p)) for p in parts]
                ok = any(hits) if op == "||" else all(hits)
                return "true" if ok else "false"
        if expr.startswith("(") and expr.endswith(")") and \
                len(self.split_top(expr[1:-1], ")")) == 1:
            return self.evaluate(expr[1:-1])
        if expr.startswith("!"):
            return "false" if self.truthy(self.evaluate(expr[1:])) else "true"
        m = re.fullmatch(r"(.+?)\s*(==|!=)\s*(.+)", expr)
        if m:
            left, op, right = (self.evaluate(m.group(1)),
                               m.group(2), self.evaluate(m.group(3)))
            same = left == right
            return "true" if (same if op == "==" else not same) else "false"
        if expr in ("always()", "true"):
            return "true"
        if expr in ("cancelled()", "false", "failure()"):
            return "false"
        if expr == "success()":
            return "true"
        if re.fullmatch(r"'[^']*'", expr):
            return expr[1:-1]
        if re.fullmatch(r"-?\d+", expr):
            return expr
        return self.lookup(expr)

    @staticmethod
    def truthy(value: str) -> bool:
        """GitHub truthiness for the values these expressions produce."""
        return value not in ("", "false", "0")

    def substitute(self, text: str) -> str:
        """Every `${{ }}` in a string, resolved."""
        return EXPR_RE.sub(lambda m: self.evaluate(m.group(1)), text)


def run_step(name: str, script: str, cwd: Path, env: dict, log: Path) -> int:
    """Run one step's script as the runner does (bash -e {0})."""
    script_file = log.with_suffix(".sh")
    script_file.write_text(script)
    with log.open("w", encoding="utf-8") as handle:
        handle.write(f"### step: {name}\n### cwd: {cwd}\n")
        handle.flush()
        proc = subprocess.run(["bash", "-e", str(script_file)], cwd=cwd, env=env,
                              stdout=handle, stderr=subprocess.STDOUT, check=False)
    return proc.returncode


def parse_kv_file(path: Path) -> dict[str, str]:
    """A GITHUB_OUTPUT / GITHUB_ENV file (key=value lines; heredoc form too)."""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    lines = path.read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "<<" in line and "=" not in line.split("<<", 1)[0]:
            key, delim = line.split("<<", 1)
            body = []
            i += 1
            while i < len(lines) and lines[i] != delim:
                body.append(lines[i])
                i += 1
            out[key] = "\n".join(body)
        elif "=" in line:
            key, value = line.split("=", 1)
            out[key] = value
        i += 1
    return out


def make_record(shim_log: Path, step_tag: str) -> tuple[int, set[str]]:
    """How many make invocations a step made, and the directories."""
    if not shim_log.exists():
        return 0, set()
    rows = [r.split("\t") for r in shim_log.read_text().splitlines()]
    mine = [r for r in rows if r and r[0] == step_tag]
    return len(mine), {r[1] for r in mine if len(r) > 1}


def main() -> int:
    """Replay the job; exit 1 if any executed step failed."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--workflow", required=True)
    ap.add_argument("--job", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--matrix", action="append", default=[])
    ap.add_argument("--needs", action="append", default=[])
    ap.add_argument("--value", action="append", default=[],
                    help="NAME=VALUE: any other expression value (needs.J.result)")
    ap.add_argument("--subst", type=Path)
    ap.add_argument("--prefix-path", action="append", default=[])
    ap.add_argument("--base-sha", default="")
    ap.add_argument("--keep-going", action="store_true")
    ap.add_argument("--map", action="append", default=[],
                    help="SRC=DST path mapping applied to every run script")
    ap.add_argument("--home", type=Path, help="HOME for every step")
    ap.add_argument("--seed", action="append", default=[],
                    help="REL=SRC: link SRC at RUNNER_TEMP/REL (a download step's output)")
    args = ap.parse_args()

    repo = args.repo.resolve()
    out = args.out.resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    runner_temp = out / "runner_temp"
    runner_temp.mkdir()
    for item in args.seed:
        rel, src = item.split("=", 1)
        (runner_temp / rel).parent.mkdir(parents=True, exist_ok=True)
        (runner_temp / rel).symlink_to(Path(src).resolve())
    bindir = out / "bin"
    shim_log = out / "make_invocations.tsv"
    make_shim(bindir, shim_log)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    ctx = Context(args, head, runner_temp)
    workflow = yaml.safe_load((repo / args.workflow).read_text())
    job = workflow["jobs"][args.job]
    subst = json.loads(args.subst.read_text()) if args.subst else {}

    ctx.env.update({k: str(v) for k, v in (workflow.get("env") or {}).items()})
    ctx.env.update({k: ctx.substitute(str(v)) for k, v in (job.get("env") or {}).items()})
    extra_path: list[str] = []
    base_path = [str(bindir), *args.prefix_path, os.environ["PATH"]]
    summary = []
    failed = 0
    print(f"replay {args.workflow} :: {args.job} at {head}")
    print(f"HOME: {args.home or os.environ['HOME']}; maps: {args.map or 'none'}")
    print(f"make on PATH: {shutil.which('make', path=os.pathsep.join(base_path))}"
          f" -> {MAKE43} ({subprocess.run([str(MAKE43), '--version'], capture_output=True, text=True).stdout.splitlines()[0]})")
    for index, step in enumerate(job["steps"], start=1):
        name = step.get("name") or step.get("uses") or f"step {index}"
        tag = f"{index:02d}"
        cond = step.get("if")
        if cond is not None:
            verdict = ctx.evaluate(EXPR_RE.sub(lambda m: m.group(1), str(cond)))
            if not ctx.truthy(verdict):
                summary.append((tag, name, "SKIPPED (if: false)", 0, 0.0))
                print(f"[{tag}] SKIP  {name}  (if: {cond})")
                continue
        if "uses" in step:
            meaning = subst.get(f"uses:{step['uses'].split('@')[0]}", "recorded, not executed")
            summary.append((tag, name, f"ACTION: {meaning}", 0, 0.0))
            print(f"[{tag}] USES  {name}: {meaning}")
            if step.get("id") and "cache" in step["uses"]:
                ctx.values[f"steps.{step['id']}.outputs.cache-hit"] = "true"
            continue
        script = ctx.substitute(step["run"])
        how = "verbatim"
        if name in subst:
            script = ctx.substitute(subst[name].replace("@BIN@", str(bindir))
                                    .replace("@OUT@", str(out)))
            how = "SUBSTITUTED (runner provisioning)"
        step_env = dict(os.environ)
        step_env.update(ctx.env)
        step_env.update({k: ctx.substitute(str(v)) for k, v in (step.get("env") or {}).items()})
        out_file, env_file, path_file = (runner_temp / f"out_{tag}", runner_temp / f"env_{tag}",
                                         runner_temp / f"path_{tag}")
        step_env.update({
            "PATH": os.pathsep.join([str(bindir), *extra_path, *base_path[1:]]),
            "GITHUB_OUTPUT": str(out_file), "GITHUB_ENV": str(env_file),
            "GITHUB_PATH": str(path_file), "GITHUB_SHA": head,
            "GITHUB_EVENT_NAME": "pull_request", "GITHUB_REF": ctx.values["github.ref"],
            "GITHUB_REPOSITORY": ctx.values["github.repository"],
            "RUNNER_TEMP": str(runner_temp), "RUNNER_OS": "Linux", "CI": "true",
            "GITHUB_ACTIONS": "true", "REPLAY_STEP": tag, "PYTHONDONTWRITEBYTECODE": "1",
        })
        for item in args.map:
            src, dst = item.split("=", 1)
            if src in script:
                script = script.replace(src, dst)
                how += f", mapped {src} -> {dst}"
        if args.home:
            step_env["HOME"] = str(args.home.resolve())
        cwd = repo / step.get("working-directory", ".")
        found = shutil.which("make", path=step_env["PATH"])
        start = time.monotonic()
        rc = run_step(name, script, cwd, step_env, out / f"step_{tag}.log")
        took = time.monotonic() - start
        calls, dirs = make_record(shim_log, tag)
        if step.get("id"):
            for key, value in parse_kv_file(out_file).items():
                ctx.values[f"steps.{step['id']}.outputs.{key}"] = value
        ctx.env.update(parse_kv_file(env_file))
        if path_file.exists():
            extra_path = [p for p in path_file.read_text().splitlines() if p] + extra_path
        state = "PASS" if rc == 0 else "FAIL"
        failed += rc != 0
        make_note = (f"make: {calls} call(s), all GNU Make 4.3 via {found}" if calls
                     else f"make: not invoked (PATH make = {found}, GNU Make 4.3)")
        summary.append((tag, name, f"{state} rc={rc} [{how}] {make_note}", rc, took))
        print(f"[{tag}] {state}  rc={rc}  {took:7.1f}s  {name}  [{how}]  {make_note}", flush=True)
        if rc and not args.keep_going:
            break
    (out / "summary.json").write_text(json.dumps(
        {"head": head, "workflow": args.workflow, "job": args.job,
         "steps": [{"step": t, "name": n, "result": r, "rc": c, "seconds": round(s, 1)}
                   for t, n, r, c, s in summary]}, indent=1))
    print(f"steps: {len(summary)}  failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
