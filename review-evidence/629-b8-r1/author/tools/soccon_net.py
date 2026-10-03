#!/usr/bin/env python3
"""SoC-board console runner with the reply over the board's USB network link (lane B6; lanes B7 and B8 change only the tag prefix).

usage: soccon_net.py <port> <transcript> <timeout_s> '<shell command>'

Lane B5's soccon.py reads the reply from the serial console. In this session another
terminal on this host has the console open and consumes what the board prints, so this
runner uses the console for input only. It types one short line at the root prompt:

    wget -qO- http://<ECM_HOST>:<h>/<tag>.sh | bash

and serves that script from this host for this one request. The script sends its own
output back over a TCP connection to this host (bash /dev/tcp), between begin and end
markers, and ends with the command's exit status:

    exec >/dev/tcp/<ECM_HOST>/<t> 2>&1; printf '<tag>_B\\n'; <command>; printf '\\n<tag>_E rc=%s\\n' $?

It never logs in. If no script request and no reply connection arrive within 15 s
(a login prompt, a password prompt or no shell), it returns rc 3 and types nothing else.
A missing end marker returns 124 after one Ctrl-C to the console's foreground job.
Only received bytes are written to the transcript, after a header that records the
typed line and the served script. The caller holds the bench lock.

Environment: ECM_HOST (this host's address on the link).
"""
import http.server
import os
import random
import re
import select
import socket
import sys
import termios
import threading
import time

HOST = os.environ["ECM_HOST"]


def open_port(port):
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    a = termios.tcgetattr(fd)
    a[0] = 0; a[1] = 0
    a[2] = termios.CS8 | termios.CREAD | termios.CLOCAL
    a[3] = 0
    a[4] = a[5] = termios.B115200
    a[6][termios.VMIN] = 0; a[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, a)
    return fd


def main():
    port, out, timeout, cmd = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    tag = "A521_%06d" % random.randint(0, 999999)
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((HOST, 0))
    lsock.listen(1)
    tport = lsock.getsockname()[1]
    script = (f"exec >/dev/tcp/{HOST}/{tport} 2>&1\nprintf '%s_B\\n' {tag}\n{cmd}\n"
              f"printf '\\n%s_E rc=%s\\n' {tag} $?\n").encode()
    served = []

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            served.append(dict(path=self.path, client=self.client_address[0], t=time.time()))
            if self.path != f"/{tag}.sh":
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Length", str(len(script)))
            self.end_headers()
            self.wfile.write(script)

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer((HOST, 0), H)
    hport = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    line = f"wget -qO- http://{HOST}:{hport}/{tag}.sh | bash"
    log = open(out, "ab")
    log.write(("\n### %s timeout=%s typed=%r\n### script:\n%s### reply:\n"
               % (time.strftime("%Y-%m-%dT%H:%M:%S%z"), timeout, line, script.decode())).encode())
    log.flush()
    fd = open_port(port)
    try:
        s = (line + "\r").encode()
        for i in range(0, len(s), 32):
            os.write(fd, s[i:i + 32]); time.sleep(0.01)
        r, _, _ = select.select([lsock], [], [], 15.0)
        if not r:
            log.write(f"\n[soccon_net] no reply connection in 15 s; script requests: {served}; rc 3\n".encode())
            sys.stderr.write("[soccon_net] no reply connection (no shell at the console), rc 3\n")
            return 3
        conn, peer = lsock.accept()
        conn.setblocking(False)
        buf = bytearray()
        end = time.time() + timeout
        pat = re.compile((tag + r"_E rc=(\d+)").encode())
        eof = False
        while time.time() < end:
            rr, _, _ = select.select([conn], [], [], 0.2)
            if rr:
                try:
                    d = conn.recv(65536)
                except BlockingIOError:
                    continue
                if not d:
                    eof = True
                    break
                buf.extend(d); log.write(d); log.flush()
                sys.stdout.buffer.write(d); sys.stdout.flush()
                if pat.search(bytes(buf)):
                    break
        m = pat.search(bytes(buf))
        if m is None:
            log.write(f"\n[soccon_net] no end marker (eof={eof}); one Ctrl-C to the console\n".encode())
            os.write(fd, b"\x03")
            time.sleep(1)
            conn.close()
            return 124
        conn.close()
        log.write(f"\n[soccon_net] reply from {peer[0]}; script requests {len(served)}\n".encode())
        return 0 if m.group(1) == b"0" else 10 + min(int(m.group(1)), 100)
    finally:
        log.close()
        os.close(fd)
        srv.shutdown()
        srv.server_close()
        lsock.close()


if __name__ == "__main__":
    sys.exit(main())
