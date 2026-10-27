"""Run a list of recorded gates through gate.py, one after another.

usage: gate-list.py <out-dir> <cwd> <list.json>

<list.json> is [[label, cmd, args...], ...]. Every gate runs whatever the
previous one returned; <out-dir>/DONE.json records each label's status.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out, cwd, listing = sys.argv[1:]
    done = {}
    for label, *cmd in json.loads(Path(listing).read_text()):
        rc = subprocess.run([sys.executable, str(HERE / "gate.py"), out, label,
                             cwd, *cmd]).returncode
        done[label] = rc
        (Path(out) / "DONE.partial.json").write_text(json.dumps(done, indent=1) + "\n")
    (Path(out) / "DONE.json").write_text(json.dumps(done, indent=1) + "\n")
    raise SystemExit(int(any(done.values())))


if __name__ == "__main__":
    main()
