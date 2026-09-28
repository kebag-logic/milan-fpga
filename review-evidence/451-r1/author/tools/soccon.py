#!/usr/bin/env python3
"""SoC-board serial console runner (root shell already logged in).

usage: soccon.py <port> <transcript> <timeout_s> '<shell command>'

Sends one command wrapped in printf begin/end markers and waits for the end
marker. Only received bytes are written to the transcript. It never logs in:
a login or password prompt aborts with rc 3. A missing end marker returns 124
after one Ctrl-C to the foreground job. The caller holds the bench lock.
"""
import os, random, re, select, sys, termios, time


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
    fd = open_port(port)
    log = open(out, "ab")
    log.write(("\n### %s timeout=%s\n" % (time.strftime("%Y-%m-%dT%H:%M:%S%z"), timeout)).encode())
    buf = bytearray()

    def pump(t):
        r, _, _ = select.select([fd], [], [], t)
        if r:
            try:
                d = os.read(fd, 65536)
            except BlockingIOError:
                return
            buf.extend(d); log.write(d); log.flush()
            sys.stdout.buffer.write(d); sys.stdout.flush()

    def send(s):
        s = s.encode()
        for i in range(0, len(s), 32):
            os.write(fd, s[i:i + 32]); time.sleep(0.01)

    def expect(pats, t):
        end = time.time() + t
        while time.time() < end:
            for i, p in enumerate(pats):
                if re.search(p, bytes(buf)):
                    return i
            pump(0.2)
        for i, p in enumerate(pats):
            if re.search(p, bytes(buf)):
                return i
        return -1

    tag = "A403_%06d" % random.randint(0, 999999)
    send("\r")
    send("printf '%%s_READY\\n' %s\r" % tag)
    i = expect([(tag + r"_READY\r?\n").encode(), rb"login:\s*$", rb"Password:\s*$"], 15)
    if i != 0:
        sys.stderr.write("\n[soccon] no shell (login prompt or silence), rc 3\n")
        log.close(); os.close(fd); return 3
    buf.clear()
    send("printf '%%s_B\\n' %s; %s; printf '\\n%%s_E rc=%%s\\n' %s $?\r" % (tag, cmd, tag))
    i = expect([(tag + r"_E rc=(\d+)").encode()], timeout)
    if i < 0:
        sys.stderr.write("\n[soccon] timeout, sending one Ctrl-C\n")
        send("\x03"); pump(2)
        log.close(); os.close(fd); return 124
    m = re.search((tag + r"_E rc=(\d+)").encode(), bytes(buf))
    log.close(); os.close(fd)
    return 0 if m.group(1) == b"0" else 10 + min(int(m.group(1)), 100)


if __name__ == "__main__":
    sys.exit(main())
