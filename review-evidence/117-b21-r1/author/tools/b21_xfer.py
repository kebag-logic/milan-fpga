#!/usr/bin/env python3
"""Lane B21: run lane B3's transfer endpoints (hostsrv.py, unchanged) for a bounded time.

usage: b21_xfer.py <serve_dir> <http_port> <recv_dir> <tftp_port> <seconds>
HTTP GET of files in <serve_dir> (the board fetches with `wget -O`), TFTP WRQ uploads into
<recv_dir> (the board pushes with `tftp -p -b 1428`). One JSON line per finished upload on stdout.
Environment: ECM_HOST (this host's address on the board's USB network link).
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hostsrv  # noqa: E402

serve, hport, recv, tport, secs = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
Path(recv).mkdir(parents=True, exist_ok=True)


def done(**kw):
    print(json.dumps(dict(t=round(time.time(), 3), kind="upload", **kw)), flush=True)


fs = hostsrv.FileServer(serve, hport)
rx = hostsrv.TftpReceiver(recv, tport, done)
print(json.dumps(dict(t=round(time.time(), 3), kind="listening", http=hport, tftp=tport)), flush=True)
end = time.time() + secs
while time.time() < end:
    time.sleep(0.5)
rx.close()
fs.close()
print(json.dumps(dict(t=round(time.time(), 3), kind="closed")), flush=True)
