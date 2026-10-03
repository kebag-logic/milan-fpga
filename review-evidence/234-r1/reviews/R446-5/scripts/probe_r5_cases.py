#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 5): the name class at the exact head, case by case, through the command line.

Each case edits a copy of the committed baseline (route-1x1 input digest zeroed, so a figure change is judged) or
of one real route directory's image manifest (a symlink mirror, the manifest copied), runs the gate as a
subprocess with strict-ASCII standard streams, and compares rc with the rc the round-5 ruling implies: every key
of the baseline and the image manifest is of [A-Za-z0-9_.:/-]{1,128}; a record's sub-block scope name may also
hold [ and ]. Also: record --write of the real route into a copy (bracketed scope names written and re-read), and
the same with an endpoint name outside the class (refused, file unchanged).

Usage: probe_r5_cases.py <checkout> <real-route-dir> <scratch-dir>
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

REPO, REAL, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
GATE = REPO / "syn/ooc/pp_resource_gate.py"
BUDGET = REPO / "docs/design/AREA_BUDGET.md"
ENV = dict(os.environ, PYTHONIOENCODING="ascii:strict", PYTHONDONTWRITEBYTECODE="1")
BAD = 0


def baseline(name: str, edit) -> Path:
    data = json.loads((REPO / "syn/ooc/pp_resource_baseline.json").read_text())
    data["endpoints"]["route-1x1"]["record"]["inputs_sha256"] = "0" * 64
    edit(data)
    path = SCRATCH / f"{name}.json"
    path.write_text(json.dumps(data, indent=1))
    return path


def mirror(name: str, edit=None) -> Path:
    folder = SCRATCH / name
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for item in REAL.iterdir():
        (folder / item.name).symlink_to(item)
    if edit is not None:
        (folder / "baseline_images.json").unlink()
        images = json.loads((REAL / "baseline_images.json").read_text())
        (folder / "baseline_images.json").write_text(edit(images))
    return folder


def run(*args: object) -> tuple[int, str, bool]:
    proc = subprocess.run([sys.executable, "-B", str(GATE), *map(str, args)], capture_output=True, env=ENV)
    out = (proc.stdout + proc.stderr).decode("ascii", "replace")
    return proc.returncode, out.strip().splitlines()[-1][:170] if out.strip() else "", "Traceback" in out


def case(label: str, want: int, *args: object) -> None:
    global BAD
    rc, last, trace = run(*args)
    ok = rc == want and not trace
    BAD += not ok
    print(f"{'ok ' if ok else 'BAD'} rc={rc} want={want} traceback={trace} | {label} | "
          f"{last.replace(str(SCRATCH), '<scratch>')}")


def scope_key(key: str):
    def edit(data: dict) -> None:
        scopes = data["endpoints"]["route-1x1"]["record"]["scopes"]
        scopes[key] = dict(next(iter(scopes.values())))
    return edit


def both(label: str, want: int, path: Path) -> None:
    case(f"{label} (check)", want if want != 0 else 0, "check", mirror("clean"), "--endpoint", "route-1x1",
         "--baseline", path)
    case(f"{label} (check-baseline)", want, "check-baseline", "--baseline", path, "--budget", BUDGET)


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    both("control: committed shape, digest zeroed", 0, baseline("control", lambda data: None))
    both("scope name holding brackets only '[]'", 0, baseline("s1", scope_key("u_pp/g[]")))
    both("scope name with a space", 2, baseline("s2", scope_key("u_pp/g x")))
    both("empty scope name", 2, baseline("s3", scope_key("")))
    both("scope name of 129 characters with brackets", 2, baseline("s4", scope_key("g[1]" + "x" * 125)))
    both("scope name with a brace", 2, baseline("s5", scope_key("u_pp/{g}")))
    both("bracketed key at description/x/record/scopes (a note shaped like a record)", 2,
         baseline("n1", lambda data: data.update(description={"x": {"record": {"scopes": {"a[1]": 1}}}})))
    both("bracketed key in a note list of objects (measured)", 2,
         baseline("n2", lambda data: data["endpoints"]["ooc-8x8"].update(measured=[{"ok": 1}, {"b[2]": 2}])))
    both("bracketed key in schema replaced by an object", 2, baseline("n3", lambda data: data.update(schema={"y[0]": 0})))
    both("bracketed key in a ceiling", 2,
         baseline("p1", lambda data: data["endpoints"]["route-1x1"]["ceiling"].update({"BRAM_TILE[0]": 1.0})))
    both("bracketed key in identity", 2,
         baseline("p2", lambda data: data["endpoints"]["route-1x1"]["record"]["identity"].update({"t[0]": "x"})))
    both("bracketed key in record figures", 2,
         baseline("p3", lambda data: data["endpoints"]["route-1x1"]["record"]["figures"].update({"LUT[0]": 1})))
    both("bracketed key in a scope's counts", 2,
         baseline("p4", lambda data: next(iter(data["endpoints"]["route-1x1"]["record"]["scopes"].values()))
                  .update({"FF[0]": 1})))
    base = baseline("m0", lambda data: None)
    for label, want, edit in (
            ("manifest unchanged", 0, lambda images: json.dumps(images)),
            ("manifest entry with a named extra key", 0, lambda images: json.dumps([{**images[0], "bytes": 5},
                                                                                    *images[1:]])),
            ("manifest entry with a bracketed key", 2, lambda images: json.dumps([{**images[0], "x[1]": 5},
                                                                                 *images[1:]])),
            ("manifest entry with a nested object holding a bracketed key", 2,
             lambda images: json.dumps([{**images[0], "meta": {"g[1]": 1}}, *images[1:]])),
            ("manifest entry with a nested list of objects holding a space key", 2,
             lambda images: json.dumps([{**images[0], "meta": [{"a b": 1}]}, *images[1:]])),
            ("manifest entry key shaped like a scope path (endpoints/x/record/scopes is no path here)", 2,
             lambda images: json.dumps([{**images[0], "endpoints": {"x": {"record": {"scopes": {"g[1]": 1}}}}},
                                        *images[1:]]))):
        case(label, want, "check", mirror(label.replace(" ", "_")[:40], edit), "--endpoint", "route-1x1",
             "--baseline", base)
    copy = SCRATCH / "write.json"
    copy.write_text((REPO / "syn/ooc/pp_resource_baseline.json").read_text())
    case("record --write of the real route into a copy (bracketed scope names written)", 0,
         "record", mirror("clean"), "--endpoint", "route-1x1", "--baseline", copy, "--write")
    written = json.loads(copy.read_text())
    brackets = sum("[" in key for key in written["endpoints"]["route-1x1"]["record"]["scopes"])
    print(f"{'ok ' if brackets else 'BAD'} record --write kept {brackets} bracketed scope names")
    BAD_local = 0 if brackets else 1
    case("check-baseline of the written copy", 0, "check-baseline", "--baseline", copy, "--budget", BUDGET)
    before = copy.read_bytes()
    case("record --write under an endpoint name with brackets", 2,
         "record", mirror("clean"), "--endpoint", "copy[1]", "--baseline", copy, "--write")
    unchanged = copy.read_bytes() == before
    print(f"{'ok ' if unchanged else 'BAD'} the refused record --write left the file unchanged: {unchanged}")
    total = BAD + BAD_local + (not unchanged)
    print(f"probe_r5_cases: {total} not as expected")


if __name__ == "__main__":
    main()
