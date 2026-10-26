#!/usr/bin/env python3
"""Run named gate commands in the checkout, one log each, and append rc/duration rows to a table.

usage: gates.py <checkout> <receipt-dir> <python> <table-name> <name>=<shell command>...

Each command runs under bash -e in the checkout with <python>'s directory first
on PATH, so `python3` is that interpreter. Never piped: the command's own exit
status is the row's rc. Logs replace the checkout, the interpreter directory and
the scratch roots with placeholders.
"""

import pathlib
import subprocess
import sys
import time


def main() -> int:
    """Run every gate in order; the exit status is 1 when any gate's rc is non-zero."""
    checkout, receipts, python, table = sys.argv[1:5]
    receipts_dir = pathlib.Path(receipts)
    receipts_dir.mkdir(parents=True, exist_ok=True)
    bindir = str(pathlib.Path(python).parent)
    env_path = bindir + ":/usr/local/bin:/usr/bin:/bin"
    rows = []
    worst = 0
    for spec in sys.argv[5:]:
        name, command = spec.split("=", 1)
        started = time.monotonic()
        result = subprocess.run(
            ["bash", "-e", "-c", command], cwd=checkout, capture_output=True, text=True, check=False,
            env={"PATH": env_path, "HOME": str(pathlib.Path.home()), "LANG": "C.UTF-8"},
        )
        seconds = time.monotonic() - started
        text = (f"$ {command}\n" + result.stdout + result.stderr + f"\n[rc={result.returncode}]\n")
        for raw, placeholder in ((checkout, "<checkout>"), (bindir, "<python-bin>"),
                                 (str(pathlib.Path.home()), "<home>"), ("/tmp/", "<tmp>/")):
            text = text.replace(raw, placeholder)
        (receipts_dir / f"{name}.log").write_text(text, encoding="utf-8")
        rows.append(f"| {name} | `{command.replace(chr(10), '; ')}` | {result.returncode} | {seconds:.1f} |")
        worst = worst or (1 if result.returncode else 0)
        print(f"{name}: rc={result.returncode} {seconds:.1f}s", flush=True)
    with (receipts_dir / f"{table}.md").open("a", encoding="utf-8") as stream:
        stream.write("\n".join(rows) + "\n")
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
