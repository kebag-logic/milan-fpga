#!/usr/bin/env python3
"""Reviewer-owned black-box workflow mutation probes for issue 439.

Usage: python3 probe_workflow_mutations.py <head-clone> <work-dir> [jobs]

Copies the four workflow files, the policy page and the checker from the
head clone into <work-dir>/tmpl (checker bytes are hash-compared), then for
every scoped run step (seven RTL jobs + full-ci-gate's SHA-pin step, scope
taken from the issue text, not from the checker) rewrites the YAML TEXT of
that one run scalar and runs `ci_events.py --check --root <probe>` from the
copied checker. Each refusal probe must exit 1 AND print the content
comparison's own diagnostic naming job, step position/name and the first
differing normalized line. Identity probes (body rewritten to its own
normalized lines) must exit 0. Output: one TSV line per probe on stdout.
"""
import concurrent.futures
import hashlib
import itertools
import pathlib
import re
import shutil
import subprocess
import sys

import yaml

SEVEN = {
    ".github/workflows/rtl.yml": ("verilator-shards", "verilator-suites",
                                  "yosys-shards", "yosys-portability"),
    ".github/workflows/rtl-fast.yml": ("verilator-lint", "bdd-conformance",
                                       "yosys-elaboration"),
}
SHA_STEP = "Print the event and pin the one SHA this run validates"
FILES = (".github/workflows/rtl.yml", ".github/workflows/rtl-fast.yml",
         ".github/workflows/docs.yml", ".github/workflows/elaborate.yml",
         "docs/testing/CI_WORKFLOWS.md")


def norm(text):
    text = text.replace("\\\n", "")
    out = []
    for raw in text.split("\n"):
        line = " ".join(w for w in re.split(r"[ \t]+", raw) if w)
        if line:
            out.append(line)
    return out


def scoped_steps(text, rel):
    """(jid, index, name, run_value_node, run_key_node) for scoped steps."""
    root = yaml.compose(text)
    jobs = dict((k.value, v) for k, v in root.value)["jobs"]
    out = []
    for jk, jv in jobs.value:
        jid = jk.value
        want = jid in SEVEN.get(rel, ()) or (
            rel.endswith("rtl.yml") and jid == "full-ci-gate")
        if not want:
            continue
        steps = dict((k.value, v) for k, v in jv.value)["steps"]
        for at, snode in enumerate(steps.value):
            m = {k.value: (k, v) for k, v in snode.value}
            if "run" not in m:
                continue
            name = m["name"][1].value if "name" in m else None
            if jid == "full-ci-gate" and name != SHA_STEP:
                continue
            out.append((jid, at, name, m["run"][1], m["run"][0]))
    return out


def replace_run(text, vnode, knode, lines):
    indent = " " * (knode.start_mark.column + 2)
    block = "|\n" + "".join(indent + l + "\n" for l in lines)
    start, end = vnode.start_mark.index, vnode.end_mark.index
    tail = text[end:]
    if not vnode.style or vnode.style not in "|>":
        # plain/quoted scalar: drop the rest of the physical line's newline
        tail = tail[1:] if tail.startswith("\n") else tail
    return text[:start] + block + tail


def first_diff(a, b):
    for i, (x, y) in enumerate(itertools.zip_longest(a, b), 1):
        if x != y:
            return i
    return None


def build(head, work):
    tmpl = work / "tmpl"
    if tmpl.exists():
        shutil.rmtree(tmpl)
    for rel in FILES + ("scripts/ci_events.py",):
        dst = tmpl / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(head / rel, dst)
    a = hashlib.sha256((head / "scripts/ci_events.py").read_bytes()).hexdigest()
    b = hashlib.sha256((tmpl / "scripts/ci_events.py").read_bytes()).hexdigest()
    assert a == b, "checker copy differs"
    return tmpl, a


def probes(tmpl):
    out = []
    for rel in SEVEN:
        text = (tmpl / rel).read_text()
        for jid, at, name, vnode, knode in scoped_steps(text, rel):
            lines = norm(vnode.value)
            what = f"job `{jid}` step {at + 1} (`{name}`)"
            edits = [("identity", lines)]
            for n, line in enumerate(lines):
                edits.append((f"swallow-line-{n + 1}",
                              [*lines[:n], line + " || true", *lines[n + 1:]]))
                edits.append((f"delete-line-{n + 1}",
                              [*lines[:n], *lines[n + 1:]]))
                edits.append((f"replace-line-{n + 1}-by-true",
                              [*lines[:n], "true", *lines[n + 1:]]))
            edits.append(("append-command", [*lines, "echo appended"]))
            edits.append(("append-bare-true", [*lines, "true"]))
            edits.append(("body-is-true", ["true"]))
            if jid == "full-ci-gate":
                s = lines.index('if [ "$head" != "$GITHUB_SHA" ]; then')
                e = lines.index("fi", s)
                x = lines.index("exit 1", s)
                edits.append(("drop-checkout-mismatch-block",
                              [*lines[:s], *lines[e + 1:]]))
                edits.append(("exit1-becomes-true",
                              [*lines[:x], "true", *lines[x + 1:]]))
                edits.append(("exit1-becomes-exit0",
                              [*lines[:x], "exit 0", *lines[x + 1:]]))
                edits.append(("condition-inverted",
                              [*lines[:s], 'if [ "$head" = "$GITHUB_SHA" ]; then',
                               *lines[s + 1:]]))
            for lever, new in edits:
                if lever != "identity" and new == lines:
                    continue
                k = first_diff(lines, new)
                if lever == "identity":
                    expect = None
                else:
                    want = lines[k - 1] if k <= len(lines) else None
                    expect = (f"{what} script is not the canonical form: "
                              f"line {k} must be {want!r}")
                out.append((rel, jid, at + 1, lever,
                            replace_run(text, vnode, knode, new), expect))
    return out


def run_one(args):
    idx, tmpl, work, rel, jid, step, lever, newtext, expect = args
    pdir = work / "probes" / f"p{idx:04d}"
    if pdir.exists():
        shutil.rmtree(pdir)
    for f in FILES:
        d = pdir / f
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(tmpl / f, d)
    (pdir / rel).write_text(newtext)
    proc = subprocess.run(
        [sys.executable, "-B", str(tmpl / "scripts/ci_events.py"), "--check",
         "--root", str(pdir)], capture_output=True, text=True)
    outp = proc.stdout + proc.stderr
    fails = [l for l in outp.splitlines() if l.startswith("  FAIL ")]
    if expect is None:
        ok = proc.returncode == 0
    else:
        ok = proc.returncode == 1 and any(expect in l for l in fails)
    shutil.rmtree(pdir)
    first = fails[0][7:200] if fails else outp.strip().splitlines()[-1][:200]
    return (idx, "PASS" if ok else "UNEXPECTED", proc.returncode, jid, step,
            lever, len(fails), first.replace("\t", " "))


def main():
    head, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    tmpl, digest = build(head, work)
    print(f"# checker sha256 {digest}")
    ps = probes(tmpl)
    args = [(i, tmpl, work, *p) for i, p in enumerate(ps)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(jobs, 8)) as ex:
        results = sorted(ex.map(run_one, args))
    bad = 0
    for r in results:
        print("\t".join(str(x) for x in r))
        bad += r[1] != "PASS"
    steps = {(r[3], r[4]) for r in results}
    print(f"# probes={len(results)} unexpected={bad} scoped_steps={len(steps)}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
