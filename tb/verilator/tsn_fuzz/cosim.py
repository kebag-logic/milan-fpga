#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
Verilator co-simulation runtime: DUT process, AXI-Stream socket, reporting.

Each DUT is a Verilator binary built from the REAL RTL that serves an
AF_UNIX socket speaking tsn-gen's packed 10-byte beat
(`uint64 tdata` little-lane, `uint8 tkeep`, `uint8 tlast`). One frame in,
one frame out (empty = the DUT deliberately stayed silent).

`Report` is deliberately dumb-but-loud: every check prints, failures carry
the offending values, and the exit code is the gate — the same contract the
C++ harnesses use, so `make` treats them identically.
"""
import os
import socket
import subprocess
import struct
import sys
import time

BEAT = struct.Struct("<QBB")


class Report:
    """Pass/fail accounting with section grouping."""

    def __init__(self, title, verbose=None):
        self.title = title
        self.npass = 0
        self.nfail = 0
        self.ngap = 0
        self.failures = []
        self.gaps = []
        self._section = None
        self.verbose = (os.environ.get("TSN_FUZZ_VERBOSE", "0") == "1"
                        if verbose is None else verbose)
        print("== %s ==" % title)

    def section(self, name):
        self._section = name
        print("\n[%s]" % name)

    def ck(self, what, ok, detail=""):
        if ok:
            self.npass += 1
            if self.verbose:
                print("  [ ok ] %-58s %s" % (what, detail))
        else:
            self.nfail += 1
            self.failures.append((self._section, what, detail))
            print("  [FAIL] %-58s %s" % (what, detail))
        return bool(ok)

    def eq(self, what, got, exp):
        return self.ck(what, got == exp, "got=%s exp=%s" % (got, exp))

    def gap(self, what, detail=""):
        """A KNOWN spec-conformance gap: printed loudly, tracked, not a failure.

        Used where the RTL's behaviour is defensible but not strictly
        conformant, so the suite stays green while the gap stays visible and
        countable. Every gap must have an issue or a docs entry behind it.
        """
        self.ngap += 1
        self.gaps.append((self._section, what, detail))
        print("  [GAP ] %-58s %s" % (what, detail))

    def note(self, msg):
        print("  ..... %s" % msg)

    def done(self):
        print("\n== %s: %d pass, %d fail, %d known gaps =="
              % (self.title, self.npass, self.nfail, self.ngap))
        if self.gaps:
            print("known spec-conformance gaps (tracked, not failures):")
            for sec, what, detail in self.gaps:
                print("  %-22s %-52s %s" % (sec or "-", what, detail))
        if self.failures:
            print("failing checks:")
            for sec, what, detail in self.failures[:40]:
                print("  %-22s %-52s %s" % (sec or "-", what, detail))
        return 1 if self.nfail else 0


class Dut:
    """A Verilator cosim binary plus its AXI-Stream socket."""

    def __init__(self, binary, sock_path=None, args=(), settle=10.0):
        self.binary = binary
        self.sock_path = sock_path or ("/tmp/tsnfuzz_%s_%d.sock"
                                       % (os.path.basename(binary), os.getpid()))
        if os.path.exists(self.sock_path):
            os.unlink(self.sock_path)
        if not os.path.isfile(binary):
            raise FileNotFoundError("DUT binary not built: %s" % binary)
        self.proc = subprocess.Popen([binary, self.sock_path, *map(str, args)],
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.PIPE)
        deadline = time.time() + settle
        while not os.path.exists(self.sock_path):
            if self.proc.poll() is not None:
                err = self.proc.stderr.read().decode(errors="replace")[-500:]
                raise RuntimeError("DUT exited before serving: %s" % err)
            if time.time() > deadline:
                raise TimeoutError("DUT never created %s" % self.sock_path)
            time.sleep(0.02)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.extras = []
        self.sock.settimeout(30.0)
        self.sock.connect(self.sock_path)

    # ------------------------------------------------------------- transport
    def send(self, frame):
        n = len(frame)
        for off in range(0, n, 8):
            chunk = frame[off:off + 8]
            self.sock.sendall(BEAT.pack(
                int.from_bytes(chunk.ljust(8, b"\x00"), "little"),
                (1 << len(chunk)) - 1,
                1 if off + 8 >= n else 0))

    def recv(self):
        out = bytearray()
        while True:
            b = b""
            while len(b) < 10:
                got = self.sock.recv(10 - len(b))
                if not got:
                    return bytes(out)
                b += got
            tdata, tkeep, tlast = BEAT.unpack(b)
            for i in range(8):
                if tkeep & (1 << i):
                    out.append((tdata >> (8 * i)) & 0xFF)
            if tlast:
                return bytes(out)

    def xact_all(self, frame):
        """All frames one command produced, in order (may be empty).

        The DUT terminates every command's reply burst with an empty frame,
        so a silent command, a normal reply and a reply-plus-unsolicited-
        notification are all unambiguous on the wire.
        """
        self.send(frame)
        frames = []
        while True:
            f = self.recv()
            if not f:                      # end-of-responses terminator
                return frames
            frames.append(f)

    def xact(self, frame):
        """The reply to one command (b'' = silence).

        Extra frames (unsolicited notifications) are kept in `self.extras`
        for the caller to assert on rather than silently dropped.
        """
        frames = self.xact_all(frame)
        self.extras = frames[1:]
        return frames[0] if frames else b""

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            self.proc.kill()
        if os.path.exists(self.sock_path):
            try:
                os.unlink(self.sock_path)
            except OSError:
                pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


# ---- control frames (see cosim_axis.h): observe/steer the DUT in-band ----
CTRL_MAGIC = b"\xc0\x51"
CTRL_STATE, CTRL_TICK, CTRL_RESET, CTRL_EVENT = 1, 2, 3, 4


def ctrl(op, arg=0):
    """A 4-byte control frame — never confusable with wire traffic."""
    return CTRL_MAGIC + bytes([op & 0xFF, arg & 0xFF])


def parse_state(frame):
    """Decode a CTRL_STATE dump frame into a list of u32 (empty if not one)."""
    if len(frame) < 4 or frame[:2] != CTRL_MAGIC or frame[2] != CTRL_STATE:
        return []
    n = frame[3]
    return [int.from_bytes(frame[4 + 4 * i:8 + 4 * i], "big") for i in range(n)
            if len(frame) >= 8 + 4 * i]


def read_state(dut):
    """Ask the DUT for its observable state right now."""
    return parse_state(dut.xact(ctrl(CTRL_STATE)))


def require_tsn_gen(report):
    """Skip cleanly (exit 0) when tsn-gen is not installed on this machine."""
    import tsn_model
    if tsn_model.available():
        return True
    print("  SKIP: tsn-gen not found at %s" % tsn_model.PACKET_GEN)
    print("        set TSN_GEN_ROOT / PACKET_GEN to enable the field campaign")
    report.note("campaign skipped (tsn-gen absent) — not a failure")
    sys.exit(0)
