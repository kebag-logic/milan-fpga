"""Retain already-captured mutant output without changing its verdict."""
import json
import os
from pathlib import Path
import subprocess

_original_run = subprocess.run


def _record_run(*args, **kwargs):
    result = _original_run(*args, **kwargs)
    command = kwargs.get("args", args[0] if args else [])
    if isinstance(command, (list, tuple)) and command:
        executable = Path(command[0]).name
        if executable.startswith("Vengine_") and kwargs.get("capture_output"):
            directory = Path(os.environ["A281_MUTANT_RECEIPTS"])
            directory.mkdir(parents=True, exist_ok=True)
            tag = Path(kwargs["cwd"]).name.removeprefix("run_")
            output = result.stdout + result.stderr
            (directory / (tag + ".log")).write_text(output)
            (directory / (tag + ".json")).write_text(json.dumps({
                "returncode": result.returncode,
                "failures": [line for line in output.splitlines() if line.startswith("FAIL ")],
            }, indent=2) + "\n")
            print("recorded mutant run: " + tag, flush=True)
    return result


subprocess.run = _record_run
