#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Unit-sim of the MilanMAC TX store-and-forward FIFO (`tx_sf`, milan_soc.py).

`tx_sf` is a LiteX PacketFIFO(eth_phy_description(64), payload_depth=512,
param_depth=8, buffered=True). It exists because the bare LiteEthMACCore is
CUT-THROUGH and GMII has no mid-frame flow control: one `valid` bubble becomes
a tx_en glitch and the peer NIC silently discards the fragment. So the FIFO
owes the wire exactly two things - hold a frame until it is COMPLETE, then
drain it with NO bubble - and this file pins both.

It also pins the reason `buffered=True` is there at all. The default fwft
SyncFIFO reads its storage ASYNCHRONOUSLY, and an asynchronous read can only
be distributed RAM: the 512 x 82 payload array synthesized as RAM64M x224 =
896 LUTRAM LUTs, ~224 SLICEMs whose LUTs cannot LUT-combine, which was the
single biggest packing consumer on the AX7101 and the reason four place
directives all missed by 22..53 slices. `buffered=True` selects migen's
SyncFIFOBuffered, whose read port is SYNCHRONOUS, so the array becomes block
RAM. That is a ONE-CYCLE latency change and nothing else - which is precisely
the kind of edit that rots silently, hence the negative control below.

Run: cd sw/litex && python3 test_tx_sf_gapless.py
"""
import ast
import pathlib
import sys

from migen import *
from migen.fhdl.specials import Memory

from litex.soc.interconnect.packet import PacketFIFO
from liteeth.common import eth_phy_description

DW    = 64                    # MilanMAC datapath width
LIMIT = 4000                  # sim wall clock

SOC = pathlib.Path(__file__).resolve().with_name("milan_soc.py")


def soc_tx_sf_kwargs():
    """READ the real `tx_sf` construction out of milan_soc.py.

    Deliberately NOT a copy of the numbers. A test that restates its subject's
    parameters agrees with it on day one and then diverges in silence - and the
    parameter this file exists to defend (`buffered`) is exactly one keyword,
    so a revert would otherwise sail straight past a green run.
    """
    tree  = ast.parse(SOC.read_text())
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and getattr(n.func, "id", None) == "PacketFIFO"]
    assert len(calls) == 1, (
        f"expected exactly one PacketFIFO() in {SOC.name}, found {len(calls)} "
        f"- this test can no longer tell which one is tx_sf")
    return {k.arg: ast.literal_eval(k.value) for k in calls[0].keywords}


_KW     = soc_tx_sf_kwargs()
DEPTH   = _KW["payload_depth"]        # 4 KB >= 2 max-size frames
PARAM_D = _KW["param_depth"]          # frame slots
BUFFERED = _KW.get("buffered", False) # the block-RAM lever, AS SHIPPED


def tx_sf(buffered):
    """The FIFO exactly as milan_soc.py's `MilanMAC` builds it."""
    return PacketFIFO(eth_phy_description(DW), payload_depth=DEPTH,
                      param_depth=PARAM_D, buffered=buffered)


# ---- 1. the storage contract: every read port SYNCHRONOUS (=> block RAM) -----
def read_port_modes(buffered):
    """[(depth, width, ['sync'|'async', ...]), ...] for each inferred Memory."""
    frag = tx_sf(buffered).get_fragment()
    out  = []
    for m in frag.specials:
        if isinstance(m, Memory):
            out.append((m.depth, m.width,
                        ["async" if p.async_read else "sync" for p in m.ports]))
    return sorted(out)


def test_storage_is_block_ram_compatible():
    # AS SHIPPED - not a hardcoded True. Reverting milan_soc.py's
    # `buffered=True` lands here, which is the whole point.
    mems = read_port_modes(buffered=BUFFERED)
    assert mems, "no Memory inferred - the FIFO shape changed under this test"
    payload = [m for m in mems if (m[0], m[1]) == (DEPTH, 82)]
    assert payload, f"no {DEPTH} x 82 payload array; got {mems}"
    for depth, width, modes in mems:
        assert "async" not in modes, (
            f"{depth} x {width} memory still has an ASYNCHRONOUS read port "
            f"({modes}). An async read cannot be block RAM, so this array is "
            f"back in LUTRAM and the ~224 SLICEMs are lost again.")
    print(f"PASS storage block-RAM compatible  {mems}")

    # ---- negative control: the bite ----------------------------------------
    # Reverting `buffered=True` MUST be caught, not silently absorbed. Prove
    # the assertion above actually discriminates rather than passing on
    # anything it is handed.
    unbuf = read_port_modes(buffered=False)
    async_payload = [m for m in unbuf if (m[0], m[1]) == (DEPTH, 82)
                     and "async" in m[2]]
    assert async_payload, (
        "negative control FAILED: buffered=False no longer produces an "
        "asynchronous read port, so the check above no longer bites and "
        "cannot defend the block-RAM contract.")
    print(f"PASS negative control - buffered=False is async {async_payload}")


# ---- 2. the wire contract: store-and-forward, then a GAPLESS drain -----------
class Bench(Module):
    def __init__(self, buffered):
        self.submodules.dut = tx_sf(buffered)


def simulate(buffered, beats, bubbles):
    """Push one frame through a STARVED source; watch the drain cycle by cycle.

    `beats` is [(data, last_be), ...]. Returns the per-cycle trace plus the
    frame the FIFO actually emitted.
    """
    b   = Bench(buffered)
    dut = b.dut
    rec = {"in_last": None, "out": [], "src_valid": [], "out_last": None}

    def feeder():
        yield dut.sink.error.eq(0)
        for i, (data, last_be) in enumerate(beats):
            # starve mid-frame: this is the condition the FIFO exists for
            for _ in range(bubbles):
                yield dut.sink.valid.eq(0)
                yield
            yield dut.sink.valid.eq(1)
            yield dut.sink.first.eq(1 if i == 0 else 0)
            yield dut.sink.last.eq(1 if i == len(beats) - 1 else 0)
            yield dut.sink.data.eq(data)
            yield dut.sink.last_be.eq(last_be)
            yield
            while not (yield dut.sink.ready):
                yield
        yield dut.sink.valid.eq(0)
        yield dut.sink.last.eq(0)
        yield dut.sink.first.eq(0)

    def monitor():
        yield dut.source.ready.eq(1)
        for t in range(LIMIT):
            yield
            if (yield dut.sink.valid) and (yield dut.sink.ready) \
                    and (yield dut.sink.last) and rec["in_last"] is None:
                rec["in_last"] = t
            v = yield dut.source.valid
            rec["src_valid"].append(v)
            if v and (yield dut.source.ready):
                rec["out"].append(((yield dut.source.data),
                                   (yield dut.source.last_be)))
                if (yield dut.source.last):
                    rec["out_last"] = t
                    # settle a few cycles so a late spurious beat is still seen
                    for _ in range(8):
                        yield
                        rec["src_valid"].append((yield dut.source.valid))
                    return

    run_simulation(b, [feeder(), monitor()])
    return rec


def frame(tag, n):
    beats = [(((tag << 56) | i) & ((1 << DW) - 1), 0xFF) for i in range(n)]
    beats[-1] = (beats[-1][0], 0x0F)          # a non-x8 tail length
    return beats


def check_frame(buffered, nbeats, bubbles):
    beats = frame(0xA5, nbeats)
    rec   = simulate(buffered, beats, bubbles)

    assert rec["out_last"] is not None, "frame never drained"
    assert rec["out"] == beats, (
        f"payload corrupted\n  in : {beats}\n  out: {rec['out']}")

    t_in, t_out = rec["in_last"], rec["out_last"]
    assert t_in is not None, "sink last beat never accepted"

    # (a) STORE-AND-FORWARD: nothing may leave before the frame is complete.
    early = [t for t, v in enumerate(rec["src_valid"]) if v and t < t_in]
    assert not early, (
        f"store-and-forward broken: source.valid at {early[:4]} but the "
        f"frame's last beat was only accepted at cycle {t_in}")

    # (b) GAPLESS: from the first emitted beat to `last`, valid every cycle.
    first_out = next(t for t, v in enumerate(rec["src_valid"]) if v)
    window    = rec["src_valid"][first_out:t_out + 1]
    assert all(window), (
        f"BUBBLE in the drain: source.valid low at cycles "
        f"{[first_out + i for i, v in enumerate(window) if not v]} between "
        f"{first_out} and {t_out}. GMII has no mid-frame flow control, so "
        f"this is a tx_en glitch and the peer discards the fragment.")

    # (c) nothing trails the frame
    assert not any(rec["src_valid"][t_out + 1:]), "spurious beat after last"

    return first_out - t_in


def test_gapless_drain():
    for nbeats in (1, 2, 8, 190):            # 190 beats = a max-size frame
        for bubbles in (0, 1, 5):
            lat = check_frame(BUFFERED, nbeats, bubbles)
            assert lat >= 1, f"latency {lat} - source cannot precede the frame"
    print("PASS gapless store-and-forward drain (1/2/8/190 beats, 0/1/5 bubbles)")


# ---- 3. the cycle contract: buffered costs exactly ONE extra cycle -----------
def test_costs_exactly_one_cycle():
    """`buffered=True` is defensible only because it is +1 cycle and no more.

    Pin the shift itself: if a future edit re-times the FIFO by some other
    amount the claim in milan_soc.py stops being true and this fails.
    """
    for nbeats in (1, 8, 190):
        unbuf = check_frame(False, nbeats, 0)
        buf   = check_frame(True,  nbeats, 0)
        assert buf == unbuf + 1, (
            f"{nbeats}-beat frame: buffered adds {buf - unbuf} cycles, not 1 "
            f"(unbuffered {unbuf}, buffered {buf}). The block-RAM read is "
            f"exactly one pipeline stage; anything else means the FIFO was "
            f"re-timed and milan_soc.py's comment is now wrong.")
    print("PASS buffered costs exactly +1 cycle of latency")


if __name__ == "__main__":
    test_storage_is_block_ram_compatible()
    test_gapless_drain()
    test_costs_exactly_one_cycle()
    print("ALL PASS")
    sys.exit(0)
