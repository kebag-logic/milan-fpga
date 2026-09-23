#!/usr/bin/env python3
"""Liveness check on a growing console_poll.py transcript (issue 117, A202).

Exit 0 when the newest console exchange is under <max_age_s> old and the
newest milan_status reply still carries the DUT's ID and VERSION; exit 1
otherwise. Used before every outlet off (no poll, no power action) and
6 s after the first one, so an outlet that feeds the DUT is turned back on
at once instead of after the hold.

usage: console_alive.py <transcript> <max_age_s>
"""
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HDR = re.compile(r"^### (\S+)Z cmd='([^']*)'", re.M)


def main() -> int:
    path = Path(sys.argv[1])
    if not path.exists():
        print("ALIVE=0 reason=no transcript")
        return 1
    text = path.read_text(errors="replace")
    heads = list(HDR.finditer(text))
    if not heads:
        print("ALIVE=0 reason=no exchanges")
        return 1
    last_t = datetime.strptime(heads[-1][1], "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc).timestamp()
    age = time.time() - last_t
    status = [h for h in heads if h[2] == "milan_status"]
    body = text[status[-1].end():] if status else ""
    ok_id = "ID=4d494c4e VERSION=00020060" in body
    alive = age < float(sys.argv[2]) and ok_id
    print(f"ALIVE={int(alive)} newest_age_s={age:.3f} id_version_ok={int(ok_id)} exchanges={len(heads)}")
    return 0 if alive else 1


if __name__ == "__main__":
    sys.exit(main())
