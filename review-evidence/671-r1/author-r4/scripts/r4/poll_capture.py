"""Report capture progress and collect a completed inherited launcher's child status."""
import datetime
import json
import os
import signal
import sys
from pathlib import Path

root = Path(sys.argv[1])
ledger = root / "supervised.json"
rows = json.loads(ledger.read_text())
for row in rows:
    if "rc" in row:
        continue
    stat = Path(f"/proc/{row['child']}/stat").read_text().split()
    assert int(stat[3]) == row["parent"]
    if stat[2] != "Z":
        continue
    status = int(stat[51])
    rc = os.waitstatus_to_exitcode(status)
    stamp = datetime.datetime.now().astimezone().isoformat()
    with (root / row["log"]).open("a") as log:
        log.write(f"END {row['arm']} rc={rc} {stamp} (completed child status collected)\n")
    row["rc"] = rc
    os.kill(row["parent"], signal.SIGTERM)
    os.kill(row["parent"], signal.SIGCONT)
    print(f"Completed {row['arm']}: rc={rc}")
ledger.write_text(json.dumps(rows, indent=2) + "\n")
for arm in ("8x8-50-on", "8x8-50-off", "8x8-100-on", "8x8-100-off", "1x1-50-on", "1x1-50-off"):
    directory = root / arm / f"capture-{arm}"
    receipt = directory / "measurement.json"
    if receipt.exists():
        data = json.loads(receipt.read_text())
        print(arm, "complete", len(data["rows"]), "captures", data["maximum_ms"], "ms")
        continue
    log = directory / "capture.log"
    count = sum(line.strip().startswith("CAPTURE index=") for line in log.read_text(errors="replace").splitlines()) if log.exists() else 0
    print(arm, count, "/ 16")
if any(row.get("rc", 0) for row in rows):
    raise SystemExit(1)
