#!/usr/bin/env python3
"""Lane B16, round 3: a neutral receipt of the tone playback's retained logs.

usage: r3_playback_logs.py <out.json> <lane>=<log> [<lane>=<log> ...]

Each log is the playback's own output (tone_play_b16.sh writes it beside the loop, in the lane's private
directory). It names the tone source's device and its playback layout, so it stays private; this receipt
names neither. Per log: its SHA-256, its modification time (CEST), the number of lines that report an
underrun, whether the playback ended on the stop signal, and its exit line. Lane B16b's log is not
retained: lane B16c's start overwrote it, and the receipt says so.
"""
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

CEST = datetime.timezone(datetime.timedelta(hours=2))


def main() -> int:
    out = Path(sys.argv[1])
    logs = {}
    for arg in sys.argv[2:]:
        lane, path = arg.split("=", 1)
        p = Path(path)
        raw = p.read_bytes()
        text = raw.decode(errors="replace")
        lines = text.splitlines()
        logs[lane] = dict(
            sha256=hashlib.sha256(raw).hexdigest(),
            bytes="withheld: the log names the tone source's device and playback layout",
            modified=datetime.datetime.fromtimestamp(p.stat().st_mtime, CEST).strftime("%H:%M:%S"),
            underrun_lines=sum(1 for x in lines if re.search(r"underrun", x, re.I)),
            ended_on_stop_signal=any("Aborted by signal Terminated" in x for x in lines),
            exit_line=lines[-1] if lines else None)
    logs["b16b"] = dict(retained=False, note="overwritten when lane B16c started the playback; HANDOFF.md step b17 "
                                             "is the only record of its underruns")
    out.write_text(json.dumps(dict(tool="r3_playback_logs.py", logs=logs), indent=1) + "\n")
    print(json.dumps({k: v.get("underrun_lines") for k, v in logs.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
