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
import datetime
import os
import socket
import subprocess
import struct
import sys
import time
from pathlib import Path

BEAT = struct.Struct("<QBB")


class Subject:
    """WHAT a campaign puts under test, and WHERE its results belong.

    Four facts that always travel together: the DUT's one-line description, the
    RTL files it is built from, the folder `TEST_RESULTS.md` is written into,
    and the command that reproduces the run. They describe the artefact, not the
    run, and only `Report._write_results` reads them.
    """

    def __init__(self, dut=None, rtl_files=(), results_dir=None,
                 reproduce=None):
        self.dut = dut
        self.rtl_files = list(rtl_files)
        self.results_dir = results_dir
        self.reproduce = reproduce


class Report:
    """Pass/fail accounting with section grouping.

    Results are written as `TEST_RESULTS.md` **into the folder of the RTL
    under test** (`results_dir`), not into a scratch directory: someone
    opening `hdl/<clause>/<block>/doc/` should see that block's current
    verification status without knowing this campaign exists.
    """

    def __init__(self, title, verbose=None, **subject):
        """`**subject` is `Subject`'s fields, spelt at the call site.

        `dut`, `rtl_files`, `results_dir` and `reproduce` describe the ARTEFACT
        under test rather than the run, always travel together, and are read by
        nothing but `_write_results`, so they are one object and not four
        parameters. A name that is not one of `Subject`'s fields is a TypeError
        where the campaign is declared.
        """
        self.title = title
        self.npass = 0
        self.nfail = 0
        self.ngap = 0
        self.failures = []
        self.gaps = []
        self.sections = []          # [(name, npass, nfail, ngap)]
        self.checks = []            # [(section, label)] every asserted check
        self._section = None
        self._counts = None
        self.subject = Subject(**subject)
        self.verbose = (os.environ.get("TSN_FUZZ_VERBOSE", "0") == "1"
                        if verbose is None else verbose)
        print("== %s ==" % title)

    def section(self, name: str) -> None:
        """Close the running section and start counting into `name`."""
        self._close_section()
        self._section = name
        self._counts = [0, 0, 0]
        print("\n[%s]" % name)

    def _close_section(self):
        if self._section is not None and self._counts is not None:
            self.sections.append((self._section, *self._counts))

    def ck(self, what: str, ok: object, detail: str = "") -> bool:
        """Grade one check and return its verdict. `ok` is judged for TRUTH, not
        for type: a caller passing a masked flag word (`st[FLAGS] & FL_ASCAP`)
        means the same thing as one passing a comparison."""
        # Every asserted check is recorded, pass or fail: the graded SET is what
        # ran, not what passed. `_write_results` emits it so a model pin dropped
        # or swapped changes the committed artifact by NAME, not only by a count
        # (#150). Only the label is kept - the detail carries run-varying values
        # and would make the artifact non-reproducible.
        self.checks.append((self._section, what))
        if ok:
            self.npass += 1
            if self._counts:
                self._counts[0] += 1
            if self.verbose:
                print("  [ ok ] %-58s %s" % (what, detail))
        else:
            self.nfail += 1
            if self._counts:
                self._counts[1] += 1
            self.failures.append((self._section, what, detail))
            print("  [FAIL] %-58s %s" % (what, detail))
        return bool(ok)

    def eq(self, what: str, got: object, exp: object) -> bool:
        """Grade an equality, carrying both values into the failure line."""
        return self.ck(what, got == exp, "got=%s exp=%s" % (got, exp))

    def gap(self, what: str, detail: str = "") -> None:
        """A KNOWN spec-conformance gap: printed loudly, tracked, not a failure.

        Used where the RTL's behaviour is defensible but not strictly
        conformant, so the suite stays green while the gap stays visible and
        countable. Every gap must have an issue or a docs entry behind it.
        """
        self.ngap += 1
        if self._counts:
            self._counts[2] += 1
        self.gaps.append((self._section, what, detail))
        print("  [GAP ] %-58s %s" % (what, detail))

    def note(self, msg: str) -> None:
        """Say something on the console that is not a graded check."""
        print("  ..... %s" % msg)

    def _write_results(self):
        """Emit TEST_RESULTS.md beside the RTL this campaign validates."""
        if not self.subject.results_dir:
            return None
        try:
            results_dir = Path(self.subject.results_dir)
            results_dir.mkdir(parents=True, exist_ok=True)
            path = results_dir / "TEST_RESULTS.md"
            stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            verdict = "PASS" if self.nfail == 0 else "FAIL"
            out = ["<!--", "SPDX-FileCopyrightText: 2026 Kebag Logic",
                   "SPDX-License-Identifier: CERN-OHL-W-2.0", "-->",
                   "# %s" % self.title, "",
                   "**%s** — %d pass, %d fail, %d known gaps  ·  %s"
                   % (verdict, self.npass, self.nfail, self.ngap, stamp), "",
                   "Generated by the tsn-gen field campaign "
                   "(`tb/verilator/tsn_fuzz/`); this file is written into the "
                   "folder of the RTL it validates, so a reader of this block "
                   "sees its verification status in place. Do not hand-edit.", ""]
            if self.subject.dut:
                out += ["**DUT:** `%s`" % self.subject.dut, ""]
            if self.subject.rtl_files:
                out += ["**RTL under test:**", ""]
                out += ["* `%s`" % f for f in self.subject.rtl_files]
                out += [""]
            if self.subject.reproduce:
                out += ["**Reproduce:** `%s`" % self.subject.reproduce, ""]
            if self.sections:
                out += ["## Sections", "",
                        "| section | pass | fail | gaps |", "|---|---:|---:|---:|"]
                for name, p, f, g in self.sections:
                    out.append("| %s | %d | %d | %d |" % (name, p, f, g))
                out.append("")
            if self.checks:
                # The per-field graded set (#150): every check that ran, grouped
                # by section, labels sorted and de-duplicated so the list is
                # reproducible run to run. A model pin dropped or swapped for
                # another changes a line here even when the section counts do
                # not, so check_results_fresh's whole-file diff catches it and
                # names the field, closing the compensating-swap hole a
                # count-only compare leaves open.
                out += ["## Graded checks", "",
                        "The set of checks this campaign asserts, one per line. "
                        "This is committed and diffed, not just counted, so a "
                        "lost or swapped model pin is named. Do not hand-edit.",
                        ""]
                by_section, order = {}, []
                for sec, label in self.checks:
                    key = sec or "(top level)"
                    if key not in by_section:
                        by_section[key] = set()
                        order.append(key)
                    by_section[key].add(label)
                for key in order:
                    out += ["### %s" % key, ""]
                    out += ["* %s" % label for label in sorted(by_section[key])]
                    out.append("")
            if self.gaps:
                out += ["## Known gaps (tracked, not failures)", ""]
                for sec, what, detail in self.gaps:
                    out.append("* **%s** — %s _(%s)_" % (what, detail, sec))
                out.append("")
            if self.failures:
                out += ["## Failures", ""]
                for sec, what, detail in self.failures:
                    out.append("* **%s** — %s _(%s)_" % (what, detail, sec))
                out.append("")
            path.write_text("\n".join(out))
            return path
        except OSError as exc:
            print("  (could not write results: %s)" % exc)
            return None

    def done(self) -> int:
        """Write TEST_RESULTS.md, print the tally, and hand back the exit code
        the harness contract wants: non-zero iff something FAILED. A tracked gap
        is loud and is not a failure."""
        self._close_section()
        written = self._write_results()
        if written:
            #! Printed AS DECLARED, not re-relativised. Both campaigns declare
            #! `results_dir` relative to their own directory (fuzz_aaf.py,
            #! fuzz_ptp.py), which is where the campaign is run from, so this
            #! is the same text `os.path.relpath()` used to produce. A campaign
            #! that declared an absolute directory now sees it printed
            #! absolute, which is the path it asked for.
            print("\nresults -> %s" % written)
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
        self.binary = Path(binary)
        #! The socket is a real filesystem entry - it is stat-ed and unlinked
        #! here - so it is a `Path`. It crosses back out as a `str` in exactly
        #! two places, the child's argv and `connect()`, because both take an
        #! address and neither is a path operation.
        self.sock_path = Path(sock_path) if sock_path else Path(
            "/tmp/tsnfuzz_%s_%d.sock" % (self.binary.name, os.getpid()))
        self.sock_path.unlink(missing_ok=True)
        if not self.binary.is_file():
            raise FileNotFoundError("DUT binary not built: %s" % binary)
        self.proc = subprocess.Popen(
            [str(self.binary), str(self.sock_path), *map(str, args)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        deadline = time.time() + settle
        while not self.sock_path.exists():
            if self.proc.poll() is not None:
                err = self.proc.stderr.read().decode(errors="replace")[-500:]
                raise RuntimeError("DUT exited before serving: %s" % err)
            if time.time() > deadline:
                raise TimeoutError("DUT never created %s" % self.sock_path)
            time.sleep(0.02)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.extras = []
        self.sock.settimeout(30.0)
        self.sock.connect(str(self.sock_path))

    # ------------------------------------------------------------- transport
    def send(self, frame: bytes) -> None:
        """Push one frame as 8-byte AXI-Stream beats, tkeep marking the ragged
        tail and tlast the final beat."""
        n = len(frame)
        for off in range(0, n, 8):
            chunk = frame[off:off + 8]
            self.sock.sendall(BEAT.pack(
                int.from_bytes(chunk.ljust(8, b"\x00"), "little"),
                (1 << len(chunk)) - 1,
                1 if off + 8 >= n else 0))

    def recv(self) -> bytes:
        """One frame off the socket, tkeep-selected bytes only. A closed socket
        yields what arrived so far rather than blocking forever."""
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

    def xact_all(self, frame: bytes) -> list[bytes]:
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

    def xact(self, frame: bytes) -> bytes:
        """The reply to one command (b'' = silence).

        Extra frames (unsolicited notifications) are kept in `self.extras`
        for the caller to assert on rather than silently dropped.
        """
        frames = self.xact_all(frame)
        self.extras = frames[1:]
        return frames[0] if frames else b""

    def close(self) -> None:
        """Drop the socket, stop the DUT process and remove its socket file.
        Every step is best-effort: a campaign must not fail in its teardown."""
        try:
            self.sock.close()
        except OSError:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            self.proc.kill()
        try:
            self.sock_path.unlink(missing_ok=True)
        except OSError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


# ---- control frames (see cosim_axis.h): observe/steer the DUT in-band ----
CTRL_MAGIC = b"\xc0\x51"
CTRL_STATE, CTRL_TICK, CTRL_RESET, CTRL_EVENT = 1, 2, 3, 4


def ctrl(op: int, arg: int = 0) -> bytes:
    """A 4-byte control frame — never confusable with wire traffic."""
    return CTRL_MAGIC + bytes([op & 0xFF, arg & 0xFF])


def parse_state(frame: bytes) -> list[int]:
    """Decode a CTRL_STATE dump frame into a list of u32 (empty if not one)."""
    if len(frame) < 4 or frame[:2] != CTRL_MAGIC or frame[2] != CTRL_STATE:
        return []
    n = frame[3]
    return [int.from_bytes(frame[4 + 4 * i:8 + 4 * i], "big") for i in range(n)
            if len(frame) >= 8 + 4 * i]


def read_state(dut: Dut) -> list[int]:
    """Ask the DUT for its observable state right now."""
    return parse_state(dut.xact(ctrl(CTRL_STATE)))


def require_tsn_gen(report: Report, name: str = "AAF/AVTP field campaign") -> bool:
    """Skip cleanly (exit 0) when tsn-gen is not installed on this machine.

    The ``SUITE-SKIP:`` line is the machine-readable half, and it is REPORTING
    ONLY: ``scripts/suite_tally.py`` lists it so a reader can see why the
    campaign total is smaller, and that is the whole of its effect.  It does
    **not** keep this suite out of ``NOCOUNT`` -- the traceability contracts the
    Makefile counts on every run do that.  Do not give the marker that power: a
    suite that can declare its own way out of ``NOCOUNT`` can hide an entire
    campaign behind a green sweep, which is measured in that file's docstring.

    It deliberately carries NO pass/fail numbers either.  A skip worded as
    "0 pass, 0 fail" matches the campaign shape and would read as a campaign
    that ran and found nothing to check, which is how a smaller total becomes
    invisible.  Zero is a measurement; this is the absence of one, and the two
    must not look alike.
    """
    import tsn_model
    if tsn_model.available():
        return True
    print("  SKIP: tsn-gen not found at %s" % tsn_model.PACKET_GEN)
    print("        set TSN_GEN_ROOT / PACKET_GEN to enable the field campaign")
    print("SUITE-SKIP: %s (tsn-gen absent; set TSN_GEN_ROOT to enable)" % name)
    report.note("campaign skipped (tsn-gen absent), not a failure")
    sys.exit(0)
