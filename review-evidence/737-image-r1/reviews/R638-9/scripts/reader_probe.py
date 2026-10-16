#!/usr/bin/env python3
"""Disposable reviewer probe: compare exec_operands' reading of an interpreter command line with what the
real interpreter runs. Each probe plants marker code where only a non-program source could run it.

Usage: python3 -I reader_probe.py <checkout> <scratch-dir>
"""
import json, os, subprocess, sys, sysconfig
from pathlib import Path

checkout, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "ci/image"))
from exec_operands import operands, interpreter  # noqa: E402

home = scratch / "home"
site = home / ".local/lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
site.mkdir(parents=True, exist_ok=True)
(site / "zzmod.py").write_text("import sys\nsys.stderr.write('MARKER: zzmod imported by the interpreter\\n')\nclass X(Warning): pass\n")
(home / ".bash_profile").write_text("echo 'MARKER: ~/.bash_profile ran' >&2\n")
(home / ".profile").write_text("echo 'MARKER: ~/.profile ran' >&2\n")
env = {"PATH": os.environ["PATH"], "HOME": str(home), "LC_ALL": "C.UTF-8"}

PROBES = [
    # (label, executable, argv0, argv[1:], stdin)
    ("python -W category imports a module", "python3", "python3", ["-W", "ignore::zzmod.X", "-c", "print('program ran')"], None),
    ("python -Wignore::module.X bundled", "python3", "python3", ["-Wignore::zzmod.X", "-c", "print('program ran')"], None),
    ("bash run as -su reads login files", "bash", "-su", ["-c", "echo 'program ran'"], None),
    ("bash run as -bash (control)", "bash", "-bash", ["-c", "echo 'program ran'"], None),
    ("perl two -e lines", "perl", "perl", ["-le", "print 1", "-e", "print 2"], None),
    ("node -p X -e Y (last wins)", "node", "node", ["-p", "'X'", "-e", "console.log('Y')"], None),
    ("node --eval X -p Y", "node", "node", ["--eval", "console.log('X')", "-p", "'Y'"], None),
    ("tclsh -encoding name file", "tclsh", "tclsh", ["-encoding", "utf-8", "prog.tcl"], None),
    ("tclsh option then stdin", "tclsh", "tclsh", ["-x"], "puts stdin-ran\n"),
]

(scratch / "prog.tcl").write_text("puts file-ran\n")
results = []
for label, exe, argv0, rest, stdin in PROBES:
    words = [argv0, *rest]
    family = interpreter(exe)
    read = operands(family, words)
    run = subprocess.run(["bash", "-c", 'exec -a "$0" "$@"', argv0, exe, *rest], input=stdin, cwd=scratch, env=env,
                         capture_output=True, text=True, timeout=60)
    markers = [line for line in run.stderr.splitlines() if line.startswith("MARKER")]
    results.append({"probe": label, "argv": words, "reader": read, "rc": run.returncode,
                    "stdout": run.stdout.strip(), "markers": markers})
    print(json.dumps(results[-1]))
