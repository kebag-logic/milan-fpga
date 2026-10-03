#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 4): try to break the gate's exit-code contract structurally.

Each case runs `pp_resource_gate.py` as a subprocess with standard output and
error in strict ASCII (PYTHONIOENCODING=ascii:strict), against a symlink mirror
of one real route measurement directory and a copy of the committed baseline
whose route-1x1 input digest is zeroed (so a figure change is judged, not
refused as identical inputs). Recorded per case: rc, whether a traceback
appeared, whether every output byte is printable ASCII or a line break, and the
last line. `want` is the rc the documented contract implies; `BAD` marks a case
whose rc differs or that printed a traceback or a non-ASCII byte.

Usage: probe_r4_structure.py <checkout> <real-route-dir> <scratch-dir>
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

REPO, REAL, SCRATCH = (Path(arg).resolve() for arg in sys.argv[1:4])
GATE = REPO / "syn/ooc/pp_resource_gate.py"
BASE = json.loads((REPO / "syn/ooc/pp_resource_baseline.json").read_text())
ENV = dict(os.environ, PYTHONIOENCODING="ascii:strict", PYTHONDONTWRITEBYTECODE="1")


def mirror(name: str, files: dict | None = None) -> Path:
    folder = SCRATCH / name
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for entry in REAL.iterdir():
        if entry.name not in (files or {}):
            (folder / entry.name).symlink_to(entry)
    for target, data in (files or {}).items():
        if callable(data):
            data(folder / target)
        else:
            (folder / target).write_bytes(data)
    return folder


def baseline(name: str, edit=None, text: str | None = None) -> Path:
    data = json.loads(json.dumps(BASE))
    data["endpoints"]["route-1x1"]["record"]["inputs_sha256"] = "0" * 64
    if edit:
        edit(data)
    path = SCRATCH / f"{name}.json"
    path.write_text(text if text is not None else json.dumps(data, indent=1) + "\n")
    return path


def run(*args: object, stdout=subprocess.PIPE) -> tuple[int, bool, bool, str]:
    result = subprocess.run([sys.executable, "-B", str(GATE), *map(str, args)], stdout=stdout,
                            stderr=subprocess.PIPE, env=ENV, timeout=300)
    out = (result.stdout or b"") + result.stderr
    ascii_ok = all(byte == 10 or 32 <= byte <= 126 for byte in out)
    lines = out.decode("ascii", "backslashreplace").strip().splitlines()
    return result.returncode, b"Traceback" in result.stderr, ascii_ok, (lines[-1] if lines else "")[:150]


def manifest(extra: dict | None = None, raw: str | None = None):
    def write(path: Path) -> None:
        if raw is not None:
            path.write_text(raw)
            return
        rows = json.loads((REAL / "baseline_images.json").read_text())
        rows[0].update(extra or {})
        path.write_text(json.dumps(rows))
    return write


def loop(path: Path) -> None:
    path.symlink_to(path.name)


def unreadable(path: Path) -> None:
    path.write_bytes((REAL / path.name).read_bytes())
    path.chmod(0)


def note(where: str, value: object):
    def edit(data: dict) -> None:
        (data if where == "file" else data["endpoints"]["route-1x1"])["description" if where == "file"
                                                                     else "measured"] = value
    return edit


def scope_rename(new: str):
    def edit(data: dict) -> None:
        scopes = data["endpoints"]["route-1x1"]["record"]["scopes"]
        scopes[new] = scopes.pop("u_pp/u_srp")
    return edit


def count_rename(new: str):
    def edit(data: dict) -> None:
        counts = data["endpoints"]["route-1x1"]["record"]["scopes"]["u_pp/u_srp"]
        counts[new] = counts.pop("CARRY4")
    return edit


def policy_rename(new: str):
    def edit(data: dict) -> None:
        tolerance = data["endpoints"]["route-1x1"]["tolerance"]
        tolerance[new] = 1
    return edit


def endpoint_rename(new: str):
    def edit(data: dict) -> None:
        data["endpoints"][new] = data["endpoints"].pop("ooc-8x8")
    return edit


def main() -> None:
    clean = mirror("clean")
    good = baseline("good")
    text = (SCRATCH / "good.json").read_text()
    raw_ff = os.fsencode(str(SCRATCH)) + b"/dir\xff"
    weird = Path(os.fsdecode(raw_ff))
    shutil.rmtree(weird, ignore_errors=True)
    shutil.copytree(clean, weird, symlinks=True)
    cases = [
        # (label, args, want, documented authority for want)
        ("control: committed shape", ("check", clean, "--endpoint", "route-1x1", "--baseline", good), 0),
        ("name class: a note object holding a bracketed key (file description)",
         ("check", clean, "--endpoint", "route-1x1", "--baseline", baseline("n1", note("file", {"x[1]": 1}))), 2),
        ("name class: a note object holding a bracketed key (endpoint measured)",
         ("check", clean, "--endpoint", "route-1x1", "--baseline", baseline("n2", note("ep", {"x[1]": 1}))), 2),
        ("name class: a note object holding a space key", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                                           baseline("n3", note("file", {"x y": 1}))), 2),
        ("name class: scope name with generate brackets (accepted exception)",
         ("check", clean, "--endpoint", "route-1x1", "--baseline", baseline("n4", scope_rename("u_pp/u_srp[3]"))), 0),
        ("name class: scope name with a space", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                                 baseline("n5", scope_rename("u_pp/u srp"))), 2),
        ("name class: scope count key with brackets", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                                       baseline("n6", count_rename("CARRY4[0]"))), 2),
        ("name class: policy figure with brackets", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                                     baseline("n7", policy_rename("LUT[0]"))), 2),
        ("name class: endpoint name with brackets", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                                     baseline("n8", endpoint_rename("ooc-8x8[0]"))), 2),
        ("name class: endpoint name with brackets via check-baseline",
         ("check-baseline", "--baseline", SCRATCH / "n8.json"), 2),
        ("name class: duplicate key", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                       baseline("n9", text=text.replace('"schema": 1,', '"schema": 1, "schema": 1,'))), 2),
        ("manifest: extra key with brackets", ("check", mirror("m1", {"baseline_images.json": manifest({"x[1]": 1})}),
                                               "--endpoint", "route-1x1", "--baseline", good), 0),
        ("manifest: extra key with a space", ("check", mirror("m2", {"baseline_images.json": manifest({"x y": 1})}),
                                              "--endpoint", "route-1x1", "--baseline", good), 2),
        ("manifest: duplicate key", ("check", mirror("m3", {"baseline_images.json": manifest(
            raw='[{"path": "a", "path": "b", "sha256": "0"}]')}), "--endpoint", "route-1x1", "--baseline", good), 2),
        ("manifest: 16-digit integer", ("check", mirror("m4", {"baseline_images.json": manifest(
            {"n": 10 ** 15})}), "--endpoint", "route-1x1", "--baseline", good), 2),
        ("input path: directory absent", ("check", SCRATCH / "absent", "--endpoint", "route-1x1", "--baseline", good), 2),
        ("input path: directory is a file", ("check", good, "--endpoint", "route-1x1", "--baseline", good), 2),
        ("input path: baseline is a directory", ("check", clean, "--endpoint", "route-1x1", "--baseline", clean), 2),
        ("input path: budget is a directory", ("check-baseline", "--baseline", good, "--budget", clean), 2),
        ("input path: report is a symlink loop", ("check", mirror("l1", {"baseline_timing.rpt": loop}),
                                                  "--endpoint", "route-1x1", "--baseline", good), 2),
        ("input path: route status a symlink loop", ("check", mirror("l2", {"alinx_ax7101_route_status.rpt": loop}),
                                                     "--endpoint", "route-1x1", "--baseline", good), 2),
        ("input path: hierarchy report unreadable (mode 000)",
         ("check", mirror("u1", {"baseline_hierarchy.rpt": unreadable}), "--endpoint", "route-1x1", "--baseline", good), 2),
        ("input path: route status unreadable (mode 000)",
         ("check", mirror("u2", {"alinx_ax7101_route_status.rpt": unreadable}), "--endpoint", "route-1x1",
          "--baseline", good), 2),
        ("emit: directory name holding a non-UTF-8 byte", ("check", weird, "--endpoint", "route-1x1", "--baseline", good), 0),
        ("emit: endpoint name with a lone surrogate on the command line",
         ("check", clean, "--endpoint", "route\udcff", "--baseline", good), 2),
        ("emit: record of a directory holding a non-UTF-8 byte", ("record", weird, "--endpoint", "route-1x1"), 0),
        ("baseline: UTF-8 BOM", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                 baseline("b1", text="﻿" + text)), 2),
        ("baseline: UTF-16", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                              (lambda p: (p.write_bytes(text.encode("utf-16")), p)[1])(SCRATCH / "b2.json")), 2),
        ("baseline: deep nesting in a note", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                              baseline("b3", text=text.replace('"schema": 1,', '"schema": '
                                                                                + "[" * 200000 + "]" * 200000 + ","))), 2),
        ("converter: 15-digit baseline figure (accepted, judged)",
         ("check", clean, "--endpoint", "route-1x1", "--baseline", baseline("c1", text=text.replace(
             '"LUT": 50128', '"LUT": 999999999999999', 1))), 0),
        ("converter: 16-digit baseline figure", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                                 baseline("c2", text=text.replace('"LUT": 50128', '"LUT": 1000000000000000', 1))), 2),
        ("converter: exponent past finite", ("check", clean, "--endpoint", "route-1x1", "--baseline",
                                             baseline("c3", text=text.replace('"WNS_ns": 0.063', '"WNS_ns": 1e400', 1))), 2),
    ]
    bad = 0
    for label, args, want in cases:
        status, trace, ascii_ok, last = run(*args)
        verdict = "ok " if status == want and not trace and ascii_ok else "BAD"
        bad += verdict == "BAD"
        print(f"{verdict} rc={status} want={want} traceback={trace} ascii={ascii_ok} | {label} | {last}")
    status, trace, ascii_ok, last = run("check", clean, "--endpoint", "route-1x1", "--baseline", good,
                                        stdout=open("/dev/full", "wb"))
    print(f"note rc={status} traceback={trace} | stdout is /dev/full (a failure of standard output itself; "
          f"disclosed limit, not counted) | {last}")
    shutil.rmtree(weird, ignore_errors=True)
    for folder in SCRATCH.iterdir():
        for path in folder.iterdir() if folder.is_dir() and not folder.is_symlink() else ():
            if not path.is_symlink():
                path.chmod(0o644)
    print(f"probe_r4_structure: {len(cases)} cases, {bad} BAD")


if __name__ == "__main__":
    main()
