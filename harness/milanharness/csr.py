# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! CSR access: register offsets, BATCHED reads, and the window disciplines.
#!
#! Offsets are compiled in because they are the stable ABI of
#! `docs/reference/REGISTER_MAP.md`; only the window BASE is configuration.
#!
#! **Batching is not an optimisation, it is the design.** `devmem` costs about
#! 0.75 s per invocation on the softcore - 800 calls once took over ten minutes.
#! `snapshot()` therefore reads the whole window in ONE remote process, via a
#! board script that block-reads `/dev/mem` and falls back to per-register
#! `devmem` only if the block reader cannot prove itself against a known word.
#!
#! Two disciplines this module encodes so callers cannot get them wrong:
#!
#!   * **SNAP** (`0x800` window): write `SEL`, write `SNAP`, poll busy, then
#!     read. A SEL write invalidates the snapshots, and until a re-poll lands
#!     the snapshot-served words read a literal `0` - "not fresh yet", NOT "no
#!     bind". `window()` never returns unpolled values.
#!   * **`>= 0x800` carve-out**: the LTAP / APRB / PBK / MCSRV / CHMAP groups
#!     are live-read through a dedicated arm. They are legitimate reads, but a
#!     zero from them is only meaningful once the SNAP-free groups are known
#!     good - see `docs/reference/REGISTER_MAP.md`.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

BOARD_DIR = Path(__file__).resolve().parent.parent / "board"

# --------------------------------------------------------------------------
# Register offsets (ABI - docs/reference/REGISTER_MAP.md)
# --------------------------------------------------------------------------
REG = {
    "ID":              0x000,
    "VERSION":         0x004,
    "CAP":             0x008,
    "SCRATCH":         0x00C,
    "MAC_CTRL":        0x100,
    "MAC_STATUS":      0x110,
    "STATS_CTRL":      0x200,
    "STATS_CAP":       0x204,
    "CLS_CTRL":        0x300,
    "ADP_CTRL":        0x600,
    "AAF_CTRL":        0x654,
    "AAF_DMLO":        0x658,
    "AAF_DMHI":        0x65C,
    "AAF_FRAMES":      0x660,
    "LWSRP_CTRL":      0x680,
    "LWSRP_TSPEC":     0x690,
    "LWSRP_STATUS":    0x694,
    "ACMPL_STATE":     0x6A4,
    "ACMPL_TALKER_LO": 0x6A8,
    "ACMPL_TALKER_HI": 0x6AC,
    "ACMPL_CNT":       0x6B0,
    "ACMPL_TUID":      0x6B4,
    "AVTPRX_STAT":     0x6B8,
    "AVTPRX_FRX":      0x6BC,
    "AVTPRX_ERR":      0x6C0,
    "PCMRX_CNT":       0x6C4,
    "PCMRX_TS":        0x6C8,
    "MAAP_CTRL":       0x6CC,
    "MAAP_STAT0":      0x6D0,
    "MAAP_STAT1":      0x6D4,
    "I2SPB_STAT":      0x6D8,
    "TONE_CTRL":       0x6DC,
    "I2SPB_TRIM":      0x6E0,
    "GPTP_PDELAY":     0x6E4,
    "ACMPL_DBG":       0x6E8,
    "AVTPRX_TSD":      0x6EC,
    "TCAM_CTRL":       0x700,
    "LINK_CTRL":       0x71C,
    "RST_EPOCH":       0x720,
    "LPF_CTRL":        0x72C,
    "CRF_CTRL":        0x738,
    "CRF_SIDLO":       0x73C,
    "CRF_SIDHI":       0x740,
    "CRF_DELTA":       0x744,
    "CRF_RATE":        0x748,
    "CRF_STATUS":      0x74C,
    "CRFT_CTRL":       0x750,
    "CRFT_COUNT":      0x764,
    "LINKG_STAT":      0x774,
    "REST_CMD":        0x7B4,
    # 0x800 indexed per-stream window
    "A_STRM_SEL":      0x800,
    "A_STRM_SNAP":     0x804,
    "A_STRMW_CTRL":    0x810,
    "A_STRMW_SID_LO":  0x814,
    "A_STRMW_SID_HI":  0x818,
    "A_STRMW_DMAC_LO": 0x81C,
    "A_STRMW_DMAC_HI": 0x820,
    "A_STRMW_FMT_LO":  0x824,
    "A_STRMW_FMT_HI":  0x828,
    "A_STRMW_STATE":   0x82C,
    "A_STRMW_CNT0":    0x830,
    "A_STRMW_PDUS":    0x858,
    "A_STRMW_SRP":     0x85C,
    "A_STRMW_CTLR_LO": 0x860,
    "A_STRMW_BIND":    0x868,
    # >= 0x800 carve-out groups
    "LTAP_CTRL":       0x870,
    "LTAP_TX_EPOCH":   0x874,
    "LTAP_TX_INFO":    0x878,
    "LTAP_TX_D0":      0x87C,
    "LTAP_TX_D0_MIN":  0x880,
    "LTAP_TX_D1":      0x884,
    "LTAP_TX_D1_MIN":  0x888,
    "LTAP_TX_D2":      0x88C,
    "LTAP_TX_D2_MIN":  0x890,
    "LTAP_RX_EPOCH":   0x894,
    "LTAP_RX_INFO":    0x898,
    "LTAP_RX_D0":      0x89C,
    "LTAP_RX_D0_MIN":  0x8A0,
    "LTAP_RX_D1":      0x8A4,
    "LTAP_RX_D1_MIN":  0x8A8,
    "LTAP_RX_D2":      0x8AC,
    "LTAP_RX_D2_MIN":  0x8B0,
    "APRB_PARSED":     0x8B4,
    "APRB_MATCHED":    0x8B8,
    "APRB_SID_LO":     0x8BC,
    "APRB_SID_HI":     0x8C0,
    "APRB_INFO":       0x8C4,
    "PBK_STAT":        0x8C8,
    "PBK_FEEDS":       0x8CC,
    "PBK_RAILS":       0x8D0,
    "MCSRV_STAT":      0x8F8,
    "MCSRV_CTRL":      0x8FC,
    "CHMAP_CTRL":      0x900,
    "CHMAP_SEL":       0x904,
    "CHMAP_WORD":      0x908,
    "CHMAP_STAT":      0x90C,
}

#: RMON lane n lives at 0x210 + 4n; STATS_CAP bit n declares whether it is real.
RMON_LANE0 = 0x210
RMON_LANES = [
    "TX_ERROR_UNDERFLOW", "TX_FIFO_OVERFLOW", "TX_FIFO_BAD_FRAME",
    "TX_FIFO_GOOD_FRAME", "RX_ERROR_BAD_FRAME", "RX_ERROR_BAD_FCS",
    "RX_FIFO_OVERFLOW", "RX_FIFO_BAD_FRAME", "RX_FIFO_GOOD_FRAME",
]

#: The 0x800 window's snap block. CNT0..9 are the Table 7-157 STREAM_INPUT
#: counters at their spec word offsets - and the ONLY full-width path to them.
WINDOW_CNT = [
    "MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH",
    "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "UNSUPPORTED_FORMAT",
    "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX",
]

#: The poison value a window word reads when it is not backed for the selected
#: direction/index. Distinguishing it from a true zero is the whole point.
NOT_BACKED = 0xDEADDEAD

ID_MAGIC = 0x4D494C4E   # "MILN"


class CsrError(Exception):
    pass


class SafetyViolation(Exception):
    """A guarded operation was refused. Never softened into a warning."""


@dataclass(frozen=True)
class Snapshot:
    """One coherent read of a board's control plane."""
    board: str
    words: dict[int, int]         # offset -> value
    method: str                   # "block" | "devmem" (which board path served it)
    ts: str = ""

    def __getitem__(self, name_or_off) -> int:
        off = REG[name_or_off] if isinstance(name_or_off, str) else name_or_off
        try:
            return self.words[off]
        except KeyError:
            raise CsrError(f"{self.board}: offset 0x{off:03X} not in this snapshot") from None

    def get(self, name_or_off, default=None):
        off = REG[name_or_off] if isinstance(name_or_off, str) else name_or_off
        return self.words.get(off, default)

    def field(self, name: str, hi: int, lo: int) -> int:
        return (self[name] >> lo) & ((1 << (hi - lo + 1)) - 1)

    def rmon(self, lane: int) -> int:
        return self[RMON_LANE0 + 4 * lane]

    def rmon_supported(self, lane: int) -> bool:
        return bool(self["STATS_CAP"] >> lane & 1)

    def as_named(self) -> dict[str, int]:
        by_off = {v: k for k, v in REG.items()}
        out = {by_off[o]: v for o, v in self.words.items() if o in by_off}
        for n, lane in enumerate(RMON_LANES):
            off = RMON_LANE0 + 4 * n
            if off in self.words:
                out[f"RMON_{lane}"] = self.words[off]
        return out


def parse_kv(text: str) -> dict[int, int]:
    """Parse the `OFF=VALUE` lines every board script emits.

    Tolerant by design: a board script may interleave progress lines, and a
    truncated console must not lose the words that DID arrive.
    """
    out: dict[int, int] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or "=" not in line or line.startswith("#"):
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip()
        if not k.startswith("0x") and not k.startswith("0X"):
            continue
        try:
            out[int(k, 16)] = int(v, 0) & 0xFFFFFFFF
        except ValueError:
            continue
    return out


class Csr:
    """Board control plane. One instance per board."""

    def __init__(self, transport, board):
        self.t = transport
        self.b = board

    # ------------------------------------------------------------- primitives
    def read(self, name_or_off) -> int:
        """ONE register. Costs a remote round trip - prefer `snapshot()`."""
        off = REG[name_or_off] if isinstance(name_or_off, str) else name_or_off
        r = self.t.run(self.b.ssh, f"devmem {self.b.csr_base + off} 32",
                       via_jump=self.b.via_jump)
        if not r.ok:
            raise CsrError(f"{self.b.name}: read 0x{off:03X} failed: {r.err.strip()}")
        return int(r.out.strip(), 0) & 0xFFFFFFFF

    def write(self, name_or_off, value: int) -> None:
        off = REG[name_or_off] if isinstance(name_or_off, str) else name_or_off
        _guard_write(self, off, value)
        r = self.t.run(self.b.ssh,
                       f"devmem {self.b.csr_base + off} 32 0x{value & 0xFFFFFFFF:08X}",
                       via_jump=self.b.via_jump)
        if not r.ok:
            raise CsrError(f"{self.b.name}: write 0x{off:03X} failed: {r.err.strip()}")

    def write_many(self, pairs: list[tuple], *, guard: bool = True) -> None:
        """Several writes in ONE remote process - the batching rule applies to
        writes too (a 6-write provisioning sequence is 6 round trips otherwise)."""
        cmds = []
        for name_or_off, value in pairs:
            off = REG[name_or_off] if isinstance(name_or_off, str) else name_or_off
            if guard:
                _guard_write(self, off, value)
            cmds.append(f"devmem {self.b.csr_base + off} 32 0x{value & 0xFFFFFFFF:08X}")
        r = self.t.run(self.b.ssh, " && ".join(cmds), via_jump=self.b.via_jump)
        if not r.ok:
            raise CsrError(f"{self.b.name}: batched write failed: {r.err.strip()}")

    # -------------------------------------------------------------- snapshot
    def snapshot(self, *, timeout: int = 180) -> Snapshot:
        """The whole control plane in ONE remote process.

        The board script block-reads `/dev/mem` and self-validates against the
        `ID` magic before trusting the block path; if that check fails it falls
        back to per-register `devmem` and says so. The method is recorded, so a
        run can be re-read afterwards knowing which path produced the numbers.
        """
        r = self.t.push_sh(self.b.ssh, BOARD_DIR / "csr_snapshot.sh",
                           via_jump=self.b.via_jump, timeout=timeout,
                           args=[hex(self.b.csr_base)])
        words = parse_kv(r.out)
        method = "devmem"
        for line in r.out.splitlines():
            if line.startswith("#METHOD="):
                method = line.split("=", 1)[1].strip()
        if words.get(REG["ID"]) != ID_MAGIC:
            raise CsrError(
                f"{self.b.name}: snapshot ID reads "
                f"0x{words.get(REG['ID'], 0):08X}, expected 0x{ID_MAGIC:08X} - "
                f"the CSR plane is not answering (or the base is wrong)")
        return Snapshot(board=self.b.name, words=words, method=method)

    # ---------------------------------------------------------------- window
    def window(self, direction: str, idx: int, *, timeout: int = 120) -> dict:
        """SEL -> SNAP -> poll busy -> read, as ONE remote process.

        Returns a dict with the named block words plus `cnt` (the ten
        STREAM_INPUT counters) and `fresh`, which is False when the snapshot
        block still reads the not-fresh literal zero.
        """
        if direction not in ("listener", "talker"):
            raise CsrError(f"bad window direction {direction!r}")
        dirbit = 0 if direction == "listener" else 1
        r = self.t.push_sh(self.b.ssh, BOARD_DIR / "csr_window.sh",
                           via_jump=self.b.via_jump, timeout=timeout,
                           args=[hex(self.b.csr_base), str(idx), str(dirbit)])
        words = parse_kv(r.out)
        cnt = [words.get(REG["A_STRMW_CNT0"] + 4 * k) for k in range(10)]
        out = {
            "direction": direction,
            "index": idx,
            "ctrl": words.get(REG["A_STRMW_CTRL"]),
            "sid": _pair(words, "A_STRMW_SID_HI", "A_STRMW_SID_LO"),
            "dmac": _pair(words, "A_STRMW_DMAC_HI", "A_STRMW_DMAC_LO"),
            "fmt": _pair(words, "A_STRMW_FMT_HI", "A_STRMW_FMT_LO"),
            "state": words.get(REG["A_STRMW_STATE"]),
            "cnt": dict(zip(WINDOW_CNT, cnt)),
            "pdus": words.get(REG["A_STRMW_PDUS"]),
            "srp": words.get(REG["A_STRMW_SRP"]),
            "bind": words.get(REG["A_STRMW_BIND"]),
            "raw": words,
        }
        out["not_backed"] = [k for k in ("ctrl", "state", "pdus", "srp", "bind")
                             if out[k] == NOT_BACKED]
        # A whole-zero snap block right after a SEL means "not fresh yet", which
        # reads exactly like "no bind" and is the trap this flag exists for.
        out["fresh"] = not (out["state"] == 0 and all(v == 0 for v in cnt))
        return out


def _pair(words: dict, hi: str, lo: str):
    h, l = words.get(REG[hi]), words.get(REG[lo])
    if h is None or l is None:
        return None
    if h == NOT_BACKED or l == NOT_BACKED:
        return NOT_BACKED
    return (h << 32) | l


# --------------------------------------------------------------------------
# Safety rails - refusals, not warnings
# --------------------------------------------------------------------------

def _guard_write(csr: "Csr", off: int, value: int) -> None:
    """Refuse the writes that have taken a board off the network before.

    Rail 1 - **never arm a `t > 0` talker with the lwSRP engine off.** Class-A
    pacing on the extra-talker path comes from the reservation bandwidth gate,
    not a timer: with the engine off an armed extra context transmits UNPACED
    (measured ~56 k frames/s against the paced ~10.4 k/s) and drowns the peer.
    The same condition also silently DROPS the arm - with the engine off the
    provisioning coupling holds `wr_rdy` low and the CSR write completes on the
    bus with nothing stored - so the sequence is doubly wrong.

    Rail 2 - **never write `A_STRMW_CTRL` without staging a sid for THIS index**
    first. Committing an unstaged CTRL at index 0 is what detached the ACMP
    alias and produced the accept blocker (`VERSION 0x000F` fixed the RTL; the
    procedural rule stands for every board still carrying older gateware).
    """
    if off == REG["A_STRMW_CTRL"] and value & 1:
        state = getattr(csr, "_arm_state", {})
        if state.get("dir") == 1 and int(state.get("idx", 0)) > 0:
            if not state.get("lwsrp_on"):
                raise SafetyViolation(
                    "refusing to arm talker context t>0 with LWSRP_CTRL[0]=0: "
                    "the reservation IS the pacer, so the stream would run "
                    "unpaced (~56 kf/s) and take the peer board off the "
                    "network - and with the engine off the arm is silently "
                    "dropped anyway")
        if not state.get("sid_staged_for") == state.get("idx"):
            raise SafetyViolation(
                "refusing an A_STRMW_CTRL commit with no stream_id staged for "
                "this index: stage SID_LO/SID_HI first (an unstaged commit is "
                "what detached the entry-0 ACMP alias)")


def arm_context(csr: "Csr", direction: str, idx: int, sid: int, *,
                dmac: int | None = None, ctrl: int = 0x3,
                lwsrp_on: bool | None = None) -> None:
    """The ONLY supported way to arm a stream context.

    Does SEL -> stage sid (+ dmac) -> commit CTRL in one remote process, with
    both safety rails checked before anything is written. For `t > 0` it
    verifies `LWSRP_CTRL[0]` on the board rather than trusting the caller.
    """
    dirbit = 0 if direction == "listener" else 1
    if lwsrp_on is None:
        lwsrp_on = bool(csr.read("LWSRP_CTRL") & 1)
    csr._arm_state = {"dir": dirbit, "idx": idx, "lwsrp_on": lwsrp_on,
                      "sid_staged_for": idx}
    _guard_write(csr, REG["A_STRMW_CTRL"], ctrl)
    pairs = [("A_STRM_SEL", (dirbit << 8) | (idx & 0xF)),
             ("A_STRMW_SID_LO", sid & 0xFFFFFFFF),
             ("A_STRMW_SID_HI", (sid >> 32) & 0xFFFFFFFF)]
    if dmac is not None:
        pairs += [("A_STRMW_DMAC_LO", dmac & 0xFFFFFFFF),
                  ("A_STRMW_DMAC_HI", (dmac >> 32) & 0xFFFF)]
    pairs.append(("A_STRMW_CTRL", ctrl))
    csr.write_many(pairs, guard=False)


def release_to_alias(csr: "Csr", idx: int) -> None:
    """Disarm a listener override so entry `idx` returns to the ACMP record.

    `{en = 0, sid = 0}` is RELEASE-TO-ALIAS since `VERSION 0x000F`. This is the
    restore half of every destructive listener step.
    """
    csr._arm_state = {"dir": 0, "idx": idx, "lwsrp_on": True,
                      "sid_staged_for": idx}
    csr.write_many([("A_STRM_SEL", idx & 0xF),
                    ("A_STRMW_SID_LO", 0), ("A_STRMW_SID_HI", 0),
                    ("A_STRMW_CTRL", 0)], guard=False)
