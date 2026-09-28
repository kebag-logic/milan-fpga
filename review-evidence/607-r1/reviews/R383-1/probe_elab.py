#!/usr/bin/env python3
"""[R383] Does the real shipping AX7101 elaboration install the #607 hook?

Runs under the LiteX interpreter. Execs <tree>/sw/litex/milan_soc.py (with an
optional one-shot text mutation), records every add_eth_constraints call and
the toolchain state it leaves, and stops the elaboration at the
Instance("milan_datapath") construction, before Builder or Vivado.
Usage: probe_elab.py <tree> <out-dir-that-must-stay-empty> [<old> <new>]
"""
import contextlib, io, json, logging, os, sys, types

tree, outdir = sys.argv[1], sys.argv[2]
soc_path = os.path.join(tree, "sw/litex/milan_soc.py")
source = open(soc_path, encoding="utf-8").read()
if len(sys.argv) > 3:
    old, new = sys.argv[3], sys.argv[4]
    assert source.count(old) == 1, f"mutation anchor count {source.count(old)}"
    source = source.replace(old, new)
logging.disable(logging.CRITICAL)
sys.path.insert(0, os.path.dirname(soc_path))
mod = types.ModuleType("milan_soc_probe")
mod.__file__ = soc_path
sys.modules[mod.__name__] = mod
exec(compile(source, soc_path, "exec"), mod.__dict__)


class Reached(Exception):
    pass


calls = []
real_add = mod.add_eth_constraints


def add_spy(platform, crg, eth_rx):
    real_add(platform, crg, eth_rx)
    tc = platform.toolchain
    calls.append({
        "toolchain": type(tc).__name__, "bounded_eth": tc.bounded_eth,
        "eth_rx_is_requested_rx": any(eth_rx is getattr(r, "rx", None)
                                      for r, *_ in platform.constraint_manager.matched),
        "bounded_is_sys_milan": [crg.eth_bounded_clocks[0] is crg.cd_sys.clk,
                                 len(crg.eth_bounded_clocks) > 1
                                 and crg.eth_bounded_clocks[1] is crg.cd_milan.clk],
        "n_bounded": len(crg.eth_bounded_clocks), "n_async": len(crg.eth_async_clocks),
        "pre_optimize": [str(c[0] if isinstance(c, tuple) else c)[:120]
                         for c in getattr(tc.pre_optimize_commands, "commands",
                                          list(tc.pre_optimize_commands))],
    })


mod.add_eth_constraints = add_spy
real_instance = mod.Instance


def inst_spy(*args, **kwargs):
    if args and args[0] == "milan_datapath":
        raise Reached()
    return real_instance(*args, **kwargs)


mod.Instance = inst_spy
argv = ("--board ax7101 --milan-clk-freq 50e6 --gtx-tx-invert --floorplan --eth-port e1 "
        "--no-i2s-playback --no-render-lpf --num-streams 1 --audio-interface tdm8 "
        "--audio-interface-master --audio-interface-render 8 --talker-wire-chans 8 "
        "--loopback-lane --fabric-gptp --gptp-ingress-lat-ns 656 --gptp-egress-lat-ns 219 "
        "--cpu vexiiriscv --software-profile baremetal --xlen 32 --full --with-spiflash "
        "--flashboot baremetal --timing-opt --l2-bytes 0 --uart-baudrate 115200 --cpu-count 1").split()
argv += ["--entity-gen-dir", os.path.join(tree, "configs/generated/endstation_ax7101_1x1_tdm8"),
         "--synth-directive", "AreaOptimized_high", "--opt-directive", "ExploreArea",
         "--place-directive", "AltSpreadLogic_high", "--vivado-max-threads", "16",
         "--build", "--output-dir", outdir]
sys.argv = ["milan_soc.py"] + argv
sink = io.StringIO()
try:
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        mod.main()
    result = "no milan_datapath instance reached"
except Reached:
    result = "reached milan_datapath (stopped before Builder)"
except BaseException as exc:
    result = f"ERROR {type(exc).__name__}: {exc}"
# Child generators may write to fd 1, so the result is one marked line.
print("RESULT: " + json.dumps({"result": result, "add_eth_constraints_calls": calls,
                              "outdir_left": sorted(os.listdir(outdir))}))
