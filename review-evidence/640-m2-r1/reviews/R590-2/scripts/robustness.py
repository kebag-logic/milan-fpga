#!/usr/bin/env python3
"""R590-2 reviewer robustness and emitter probes for the M2 helpers.

Run with the pinned LiteX interpreter:
  robustness.py SOC_DIR [--emit-dir DIR --tag TAG]

Prints one line per probe ("[ok  ]" or "[FAIL]") and exits 1 on any FAIL.
With --emit-dir, also writes the LiteX- and migen-emitted Verilog of the lane
test's three benches (every framing flag a port), for byte comparison across
trees (timestamps stripped).
"""
import argparse
import re
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("soc_dir", type=Path)
    ap.add_argument("--emit-dir", type=Path)
    ap.add_argument("--tag", default="head")
    ap.add_argument("--lane-test", type=Path, required=True,
                    help="the head's test_retained_cdc_storage.py (benches and emit)")
    ap.add_argument("--emit-only", action="store_true")
    args = ap.parse_args()
    sys.path.insert(0, str(args.soc_dir))
    import milan_soc as soc
    assert Path(soc.__file__).resolve().parent == args.soc_dir.resolve()
    from migen import Module, Memory, ClockDomain
    from litex.soc.interconnect import stream, axi

    fails = 0
    if args.emit_only:
        return emit_benches(args, soc, re)

    def report(ok, what):
        nonlocal fails
        fails += 0 if ok else 1
        print(f"  [{'ok  ' if ok else 'FAIL'}] {what}")

    def raises(fn):
        try:
            fn()
        except ValueError as e:
            return str(e)
        return None

    layout = [("data", 64), ("keep", 8)]

    # R1: all-sys MilanMAC builds no crossing and the helper is not called.
    try:
        mac = soc.MilanMAC(soc.alinx_ax7101.Platform(), data_width=64, milan_cd="sys")
        report(not hasattr(mac, "mac_tx_cdc") or mac.mac_tx_cdc is None,
               "R1 MilanMAC(milan_cd='sys') elaborates with no MAC crossing")
    except Exception as e:  # noqa: BLE001
        report(False, f"R1 MilanMAC(milan_cd='sys') raised {type(e).__name__}: {e}")

    # R2: _cross_csr_bus in sys returns the bus itself and adds nothing.
    host = Module()
    bus = axi.AXILiteInterface(data_width=32, address_width=32)
    report(soc._cross_csr_bus(host, bus, "sys") is bus and not host._submodules,
           "R2 _cross_csr_bus(..., 'sys') returns the CPU bus and adds no crossing")

    # R3: a second placement on the same crossing is refused, not doubled.
    cdc = stream.ClockDomainCrossing(layout, cd_from="a", cd_to="b", depth=16, buffered=True)
    soc._payload_in_block_ram(cdc)
    msg = raises(lambda: soc._payload_in_block_ram(cdc))
    report(msg is not None, f"R3 a second _payload_in_block_ram is refused ({msg})")

    # R4: a same-domain crossing (no FIFO) is refused.
    same = stream.ClockDomainCrossing(layout, cd_from="a", cd_to="a")
    msg = raises(lambda: soc._payload_in_block_ram(same))
    report(msg is not None, f"R4 a same-domain crossing is refused ({msg})")

    # R5: a crossing with params splits payload+params into the block array.
    desc = stream.EndpointDescription([("data", 32)], [("tag", 5)])
    par = stream.ClockDomainCrossing(desc, cd_from="a", cd_to="b", depth=8)
    soc._payload_in_block_ram(par)
    core = par._submodules[0][1].fifo
    widths = sorted((m.width, sorted(v for _, v in m.attr)) for m in core._fragment.specials
                    if isinstance(m, Memory))
    report(widths == [(2, ["distributed"]), (37, ["block"])],
           f"R5 a param-carrying crossing splits as payload+params / flags: {widths}")

    # R6: with_common_rst crossings are still one AsyncFIFO and are accepted.
    com = stream.ClockDomainCrossing(layout, cd_from="a", cd_to="b", depth=16,
                                     with_common_rst=True)
    msg = raises(lambda: soc._payload_in_block_ram(com))
    report(msg is None, f"R6 a with_common_rst crossing is accepted ({msg})")

    # R7: a non-crossing module is refused.
    msg = raises(lambda: soc._payload_in_block_ram(Module()))
    report(msg is not None, f"R7 a module with no AsyncFIFO is refused ({msg})")

    # R8: storage arrays carry no init/reset (as stock LiteX), and the original
    # one-array ports no longer appear as specials.
    cdc2 = stream.ClockDomainCrossing(layout, cd_from="a", cd_to="b", depth=16, buffered=True)
    stock_core = cdc2._submodules[0][1].fifo.fifo
    stock = [s for s in stock_core._fragment.specials if isinstance(s, Memory)][0]
    stock_ports = set(stock.ports)
    soc._payload_in_block_ram(cdc2)
    left = [s for s in stock_core._fragment.specials if s in stock_ports or s is stock]
    mems = [s for s in stock_core._fragment.specials if isinstance(s, Memory)]
    report(not left and all(m.init is None for m in mems) and len(mems) == 2,
           "R8 the stock array and its ports are removed; the split arrays have no init")

    if args.emit_dir:
        emit_benches(args, soc, re)

    print(f"robustness: {fails} failure(s)")
    return 1 if fails else 0


def emit_benches(args, soc, re):
    import importlib.util
    spec = importlib.util.spec_from_file_location("lane_test", args.lane_test)
    lane = importlib.util.module_from_spec(spec)
    sys.modules["lane_test"] = lane
    spec.loader.exec_module(lane)
    args.emit_dir.mkdir(parents=True, exist_ok=True)
    for emitter in ("litex", "migen"):
        for bench in lane.build_benches(soc):
            kind = bench.channels[0].array
            text = lane.emit(bench, emitter)
            text = re.sub(r"(?m)^//.*(Date|date|Auto-Generated|sha1).*$", "", text)
            (args.emit_dir / f"{args.tag}-{emitter}-{kind}.v").write_text(text)
    print(f"  emitted benches to {args.emit_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
