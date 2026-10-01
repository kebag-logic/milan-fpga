"""Host-side transfer endpoints on the ECM address (imported by the run tools).

TftpReceiver: accepts WRQ uploads (octet mode, blksize option) into one
directory; the SoC board pushes captures with `tftp -p -b 1428`. Binary-safe,
unlike busybox `wget --post-file`, which sizes the body with strlen.
FileServer: HTTP GET of files from one directory; the SoC board streams the
DIN pattern with `wget -O -`.
TcpReceiver: one TCP upload, streamed by the SoC board while it records.
All run in daemon threads for the life of one locked action.
"""
import http.server
import socket
import struct
import threading
import time
from pathlib import Path

import os

HOST = os.environ["ECM_HOST"]            # this host's address on the SoC board's USB link


class TftpReceiver:
    def __init__(self, dest, port, on_done):
        self.dest, self.on_done = Path(dest), on_done
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, port))
        self.sock.settimeout(0.5)
        self.stop = False
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while not self.stop:
            try:
                pkt, peer = self.sock.recvfrom(2048)
            except socket.timeout:
                continue
            if struct.unpack(">H", pkt[:2])[0] != 2:
                continue
            parts = pkt[2:].split(b"\0")
            name, opts = Path(parts[0].decode()).name, parts[2:]
            threading.Thread(target=self.session, args=(name, opts, peer), daemon=True).start()

    def session(self, name, opts, peer):
        blk = 512
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, 0))
        s.settimeout(5)
        o = {opts[i].decode().lower(): opts[i + 1].decode() for i in range(0, len(opts) - 1, 2)}
        if "blksize" in o:
            blk = max(8, min(int(o["blksize"]), 1468))
            s.sendto(struct.pack(">H", 6) + b"blksize\0" + str(blk).encode() + b"\0", peer)
        else:
            s.sendto(struct.pack(">HH", 4, 0), peer)
        n, total, t0, ok = 1, 0, time.time(), False
        with open(self.dest / name, "wb") as f:
            while True:
                try:
                    pkt, p = s.recvfrom(blk + 4)
                except socket.timeout:
                    break
                op, bn = struct.unpack(">HH", pkt[:4])
                if op != 3:
                    break
                if bn == (n & 0xFFFF):
                    f.write(pkt[4:])
                    total += len(pkt) - 4
                    n += 1
                s.sendto(struct.pack(">HH", 4, bn), p)
                if len(pkt) - 4 < blk and bn == ((n - 1) & 0xFFFF):
                    ok = True
                    break
        s.close()
        self.on_done(name=name, bytes=total, complete=ok, seconds=round(time.time() - t0, 3), blksize=blk)

    def close(self):
        self.stop = True


class TcpReceiver:
    """One TCP upload into <dest>/<name>; the SoC board streams with bash's
    /dev/tcp redirection while it records (lane B4: no nc on the board, and a
    10-minute capture exceeds its temporary storage). Hashes on the fly and
    records the longest gap between received chunks."""

    def __init__(self, dest, port, name, on_done):
        import hashlib
        self.path, self.on_done, self.h = Path(dest) / name, on_done, hashlib.sha256()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8 << 20)
        self.sock.bind((HOST, port))
        self.sock.listen(1)
        self.sock.settimeout(0.5)
        self.stop = False
        self.done = threading.Event()
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        conn = None
        while not self.stop and conn is None:
            try:
                conn, peer = self.sock.accept()
            except socket.timeout:
                continue
        if conn is None:
            self.done.set()
            return
        conn.settimeout(1.0)
        total, t0, last, max_gap, gaps_100ms = 0, None, None, 0.0, 0
        with open(self.path, "wb") as f:
            while True:
                try:
                    d = conn.recv(1 << 20)
                except socket.timeout:
                    if self.stop:
                        break
                    continue
                now = time.time()
                if not d:
                    break
                if t0 is None:
                    t0 = now
                if last is not None:
                    g = now - last
                    max_gap = max(max_gap, g)
                    gaps_100ms += g >= 0.1
                last = now
                f.write(d)
                self.h.update(d)
                total += len(d)
        conn.close()
        self.on_done(name=self.path.name, bytes=total, sha256=self.h.hexdigest(),
                     first_t=t0, last_t=last, max_gap_s=round(max_gap, 4), gaps_ge_100ms=gaps_100ms,
                     closed_by_peer=not self.stop)
        self.done.set()

    def close(self, wait=10):
        self.done.wait(wait)
        self.stop = True
        self.thread.join(5)
        self.sock.close()


class FileServer:
    def __init__(self, root, port):
        root = str(root)

        class H(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **k):
                super().__init__(*a, directory=root, **k)

            def log_message(self, *a):
                pass

        self.srv = http.server.ThreadingHTTPServer((HOST, port), H)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()
