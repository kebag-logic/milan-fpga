# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! The mock bench that `--dry-run` runs against.
#!
#! This is not a stub that returns "ok". It is a small simulator of the board's
#! shell: it interprets the `devmem` / `dd | od` / `cat /sys/...` command lines
#! the real board scripts emit, keeps a register file that responds to writes,
#! advances free-running counters with time, and honours the SNAP and SEL
#! disciplines. That is what makes a dry run a real exercise of every phase's
#! control flow rather than a walk through the happy path.
#!
#! It can also be told to misbehave, which is how the FAILED path, the forensic
#! bundle, the one-shot alert and the FAILED/BLOCKED split get tested with no
#! bench: `faults={"item": "es-4.7"}` makes that item fail, `faults={"outage":
#! N}` makes the next N transport calls unreachable.

from __future__ import annotations

import re
import time

from .csr import ID_MAGIC, REG, RMON_LANE0
from .transport import Result


class MockBench:
    """A fake far side for `Transport`. Install with `Transport(cfg, runner=...)`."""

    def __init__(self, *, version: int = 0x00010013, faults: dict | None = None,
                 clock=None):
        self.faults = dict(faults or {})
        self.clock = clock or time.monotonic
        self.t0 = self.clock()
        self.calls: list[str] = []
        self.detached: dict[str, tuple[int, str]] = {}
        self.regs: dict[int, int] = {}
        self.sel = 0
        self.captures: dict[str, bytes] = {}
        self._seed_registers(version)

    # ------------------------------------------------------------------ setup
    def _seed_registers(self, version: int) -> None:
        r = self.regs
        r[REG["ID"]] = ID_MAGIC
        r[REG["VERSION"]] = version
        r[REG["CAP"]] = 0x0007_7106
        r[REG["MAC_CTRL"]] = 0x13
        r[REG["MAC_STATUS"]] = 0x3
        r[REG["STATS_CAP"]] = 0x1B8            # LiteEth build: 5 real lanes
        r[REG["CLS_CTRL"]] = 0x5
        r[REG["AAF_CTRL"]] = 0x0002_0003       # VID 2 preserved
        r[REG["LWSRP_CTRL"]] = 0x1
        r[REG["LWSRP_STATUS"]] = 0x37E
        r[REG["ACMPL_STATE"]] = 0x0002_E07F    # bound, active, RSV_OK
        r[REG["LINKG_STAT"]] = 0x0000_00C3     # rx_alive|tx_alive|act_recent
        r[REG["RST_EPOCH"]] = 1
        r[REG["TONE_CTRL"]] = 1
        r[REG["CRF_STATUS"]] = 0x0100_0000
        r[REG["LTAP_CTRL"]] = 0x2
        r[REG["CHMAP_CTRL"]] = 1
        r[REG["CHMAP_STAT"]] = 32
        # PBK_STAT: crossbar selected [16], pcm_tx walking [17], playback
        # enabled [18], phys{0,1} backed by the render map [19]. Zero disarmed
        # -render frames in [15:0], i.e. the map is not empty.
        r[REG["PBK_STAT"]] = (1 << 16) | (1 << 17) | (1 << 18) | (1 << 19)
        # Latency taps, in cycles at 100 MHz: the shape measured on silicon.
        r[REG["LTAP_RX_D0"]] = (52 << 16) | 50
        r[REG["LTAP_RX_D0_MIN"]] = 49
        r[REG["LTAP_RX_D1"]] = (33 << 16) | 30
        r[REG["LTAP_RX_D1_MIN"]] = 29
        r[REG["LTAP_RX_D2"]] = (12541 << 16) | 12500
        r[REG["LTAP_RX_D2_MIN"]] = 10378
        r[REG["LTAP_RX_INFO"]] = 4096
        r[REG["LTAP_TX_D0"]] = (12504 << 16) | 12500
        r[REG["LTAP_TX_D0_MIN"]] = 1
        r[REG["LTAP_TX_D1"]] = (120 << 16) | 110
        r[REG["LTAP_TX_D1_MIN"]] = 110
        r[REG["LTAP_TX_D2"]] = (900 << 16) | 800
        r[REG["LTAP_TX_D2_MIN"]] = 8
        r[REG["LTAP_TX_INFO"]] = 4096
        for lane in range(9):
            r[RMON_LANE0 + 4 * lane] = 0

    # ------------------------------------------------------- free-running view
    def _elapsed(self) -> float:
        """Wall time PLUS a virtual tick per call.

        A dry run skips its sleeps, so wall time barely moves and every
        free-running counter would look frozen - which the harness would
        correctly report as a dead bench. The per-call tick makes the mock
        behave like a board that keeps running between two reads, so the dry
        run exercises the healthy path instead of a fabricated stall.
        """
        return max(0.0, self.clock() - self.t0) + 0.01 * len(self.calls)

    def _live(self, off: int) -> int:
        """Counters that must MOVE for a known-good verdict to be possible."""
        e = self._elapsed()
        if off == REG["APRB_PARSED"]:
            return 10000 + int(e * 9600)
        if off == REG["APRB_MATCHED"]:
            return 9800 + int(e * 9600)
        if off == REG["AVTPRX_FRX"]:
            return 20000 + int(e * 9600)
        if off == REG["AAF_FRAMES"]:
            return 30000 + int(e * 10400)
        if off == REG["PBK_FEEDS"]:
            return 1000 + int(e * 48000)
        if off == RMON_LANE0 + 4 * 3:      # TX_FIFO_GOOD_FRAME
            return 5000 + int(e * 10500)
        if off == RMON_LANE0 + 4 * 8:      # RX_FIFO_GOOD_FRAME
            return 5000 + int(e * 9700)
        return self.regs.get(off, 0)

    def read(self, addr: int, base: int) -> int:
        off = addr - base
        if base != 0x90000000:
            # The LiteX CSR space (DMA rings, TS ring, MAC loopback) is a
            # separate window with its own layout. Ring offsets advance; a
            # control word reads back what was written.
            if off in self.regs:
                return self.regs[off]
            return int(self._elapsed() * 8000) & 0xFFFFFFFF
        if 0x800 <= off <= 0x86C:
            return self._window_word(off)
        return self._live(off) if off in _LIVE_OFFS else self.regs.get(off, 0)

    def _window_word(self, off: int) -> int:
        idx = self.sel & 0xF
        dirbit = (self.sel >> 8) & 1
        if off == REG["A_STRM_SEL"]:
            return self.sel
        if off == REG["A_STRM_SNAP"]:
            return 0                       # never busy in the mock
        # Talker direction: several words are structurally not backed.
        if dirbit == 1 and off in (REG["A_STRMW_FMT_LO"], REG["A_STRMW_FMT_HI"],
                                   REG["A_STRMW_CTLR_LO"], 0x864, REG["A_STRMW_BIND"]):
            return 0xDEADDEAD
        if dirbit == 1 and REG["A_STRMW_CNT0"] <= off <= REG["A_STRMW_CNT0"] + 36:
            return 0xDEADDEAD
        key = (dirbit, idx, off)
        if key in self.regs:
            return self.regs[key]
        if off == REG["A_STRMW_CTRL"]:
            return 0x3 if idx == 0 else 0
        if off in (REG["A_STRMW_SID_LO"],):
            return 0x00020000 if idx == 0 else 0
        if off in (REG["A_STRMW_SID_HI"],):
            return 0x02000000 if idx == 0 else 0
        if off == REG["A_STRMW_STATE"]:
            return 0x0002_E07F if (dirbit == 0 and idx == 0) else (0x9 if dirbit else 0)
        if REG["A_STRMW_CNT0"] <= off <= REG["A_STRMW_CNT0"] + 36:
            k = (off - REG["A_STRMW_CNT0"]) // 4
            base = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0][k]
            return base + (int(self._elapsed() * 9600) if k == 9 else 0)
        if off == REG["A_STRMW_PDUS"]:
            return int(self._elapsed() * 9600) & 0xFFFF
        if off == REG["A_STRMW_SRP"]:
            return 0x37E if idx == 0 else 0x3E
        return 0

    def write(self, addr: int, base: int, value: int) -> None:
        off = addr - base
        if off == REG["A_STRM_SEL"]:
            self.sel = value & 0x1FF
            return
        if 0x810 <= off <= 0x86C:
            self.regs[((self.sel >> 8) & 1, self.sel & 0xF, off)] = value
            return
        self.regs[off] = value

    # --------------------------------------------------------------- dispatch
    def __call__(self, argv: list[str], timeout: int, stdin: str) -> Result:
        """The `Transport` runner hook."""
        line = " ".join(argv)
        self.calls.append(line)
        if self.faults.get("outage", 0) > 0:
            self.faults["outage"] -= 1
            return Result(255, "", "mock: ssh: connect: Network is unreachable", 0.0, 1)
        # The remote command is the last argv element for our ssh shape.
        cmd = argv[-1] if argv else ""
        if stdin.strip():
            return self._run_script(cmd, stdin)
        return self._run_cmd(cmd)

    def _run_cmd(self, cmd: str) -> Result:
        out = []
        rc = 0
        for part in re.split(r"\s*&&\s*", cmd.strip()):
            part = part.strip()
            if not part:
                continue
            m = re.match(r"devmem\s+(\S+)\s+32(?:\s+(\S+))?$", part)
            if m:
                addr = int(m.group(1), 0)
                base = addr & ~0xFFFF
                if m.group(2) is None:
                    out.append(f"0x{self.read(addr, base):08X}")
                else:
                    self.write(addr, base, int(m.group(2), 0))
                continue
            if part.startswith("cat /tmp/mh-"):
                tag = re.search(r"/tmp/mh-([\w-]+)\.done", part)
                if tag and tag.group(1) in self.detached:
                    code, body = self.detached[tag.group(1)]
                    out.append(str(code))
                    out.append("---")
                    out.append(body)
                    continue
                out.append("")
                out.append("---")
                continue
            if part.startswith("cat /sys/class/net"):
                out.append(str(100000 + int(self._elapsed() * 1200)))
                continue
            if part.startswith("ping "):
                continue
            m = re.match(r"echo\s+(.*)$", part)
            if m:
                out.append(m.group(1).strip("'\""))
                continue
            if part.startswith("test "):
                continue
            out.append("")
        return Result(rc, "\n".join(out) + "\n", "", 0.0, 1)

    def _run_script(self, cmd: str, body: str) -> Result:
        if "DETACHED" in cmd or "setsid" in cmd:
            m = re.search(r"/tmp/mh-([\w-]+)", cmd)
            tag = m.group(1) if m else "step"
            # The detached launcher runs `sh /tmp/mh-<tag>.sh <args> > ...`.
            am = re.search(r"sh /tmp/mh-[\w-]+\.sh([^>]*)", cmd)
            args = am.group(1).split() if am else []
            self.detached[tag] = (0, self._script_output(body, args))
            return Result(0, f"DETACHED /tmp/mh-{tag}\n", "", 0.0, 1)
        args = cmd.split(" -- ", 1)[1].split() if " -- " in cmd else []
        return Result(0, self._script_output(body, args), "", 0.0, 1)

    def _script_output(self, body: str, args: list[str]) -> str:
        if "csr_snapshot.sh" in body or "BLOCK_WORDS" in body:
            base = int(args[0], 0) if args else 0x90000000
            lines = ["#METHOD=block"]
            for off in sorted(set(list(REG.values())
                                  + [RMON_LANE0 + 4 * n for n in range(9)]
                                  + [REG["A_STRMW_CNT0"] + 4 * k for k in range(10)])):
                lines.append(f"0x{off:03X}=0x{self.read(base + off, base):08X}")
            return "\n".join(lines) + "\n"
        if "csr_window.sh" in body or "SNAP_POLLS" in body:
            base = int(args[0], 0) if len(args) > 0 else 0x90000000
            idx = int(args[1]) if len(args) > 1 else 0
            dirbit = int(args[2]) if len(args) > 2 else 0
            self.sel = (dirbit << 8) | idx
            lines = ["#SNAP_POLLS=0", f"#SEL_READBACK=0x{self.sel:08X}"]
            offs = [0x810, 0x814, 0x818, 0x81C, 0x820, 0x824, 0x828, 0x82C]
            offs += [0x830 + 4 * k for k in range(10)]
            offs += [0x858, 0x85C, 0x860, 0x864, 0x868]
            for off in offs:
                lines.append(f"0x{off:03X}=0x{self.read(base + off, base):08X}")
            return "\n".join(lines) + "\n"
        if "KNOWN_GOOD" in body:
            fail = self.faults.get("known_good_fail")
            checks = ["csr-id", "csr-version", "aaf-vid", "safety-rail",
                      "link-guard", "host-plane", "media-plane"]
            lines = []
            bad = 0
            for c in checks:
                if fail == c:
                    lines.append(f"CHECK {c}: FAIL (mock-injected)")
                    bad += 1
                else:
                    lines.append(f"CHECK {c}: PASS")
            lines.append("KNOWN_GOOD: " + ("FAIL" if bad else "PASS"))
            return "\n".join(lines) + "\n"
        if "FLASHLOG" in body:
            return "#PROC_MTD_PRESENT=0\n#FLASHLOG=absent (/user is not a directory) - host-only logging\n"
        if "CAPTURE_BYTES" in body:
            return ("#CAPTURE_FILE=/tmp/mh-capture.raw\n#CAPTURE_BYTES=3840000\n"
                    "#CAPTURE_EXPECT=3840000\n#CAPTURE_RC=0\n")
        if "REVERT_VERIFY" in body:
            what = args[1] if len(args) > 1 else ""
            if what in ("macreinit", "linkfreeze"):
                # A real guard episode is ONE bounce. Modelling it as exactly
                # one is what lets the `==1` predicate (rather than `>=1`) be
                # exercised - the +2-per-flap defect is the reason it matters.
                self.regs[REG["LINKG_STAT"]] += 1 << 16
            return ("ORIG=0x00000000\nWATCHDOG=armed +25s\n"
                    f"APPLIED={what or 'mock'}\n"
                    f"LINKG_STAT=0x{self.regs[REG['LINKG_STAT']]:08X}\n"
                    "RESTORED=0x00000000\nREVERT_VERIFY: PASS\n")
        return "#MOCK=unrecognised-script\n"


_LIVE_OFFS = {
    REG["APRB_PARSED"], REG["APRB_MATCHED"], REG["AVTPRX_FRX"],
    REG["AAF_FRAMES"], REG["PBK_FEEDS"],
    RMON_LANE0 + 4 * 3, RMON_LANE0 + 4 * 8,
}


def synth_tone(*, rate_hz: int, f0_hz: int, seconds: float, channels: int,
               amplitude: float = 0.5, thd_at_db: float | None = None) -> bytes:
    """Synthesise an exact-period S32_BE capture, for the dry run and the tests.

    `thd_at_db` injects one second harmonic at a KNOWN level, which is what
    makes the THD+N unit test an actual check rather than a smoke test.
    """
    import math
    import struct

    n = int(rate_hz * seconds)
    h = 0.0 if thd_at_db is None else amplitude * (10 ** (thd_at_db / 20.0))
    buf = bytearray()
    for i in range(n):
        ph = 2.0 * math.pi * f0_hz * i / rate_hz
        v = amplitude * math.sin(ph) + h * math.sin(2 * ph)
        s = max(-2147483648, min(2147483647, int(round(v * 2147483648.0))))
        for _ in range(channels):
            buf += struct.pack(">i", s)
    return bytes(buf)
