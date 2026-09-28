#!/usr/bin/env python3
"""R372-4 reviewer composition probe (read-only; writes nothing in the checkout).

Question: at the merge head, do the #395 timing-grade declaration and the
post-route corner reporting compose with #582's contract clock?

Method: run the real `milan_soc.main()` for (a) every tracked end-station
configuration's builder-emitted argv and (b) the shipping `sweep.sh` AX7101
argv, intercepting the real `_CRG` constructor: the real _CRG is built, then a
sentinel stops elaboration.  From the captured objects, assert:
  1. effective Milan/CPU clock == recipe CPU_HZ == builder BAREMETAL_CLK_HZ ==
     configured milan_clk_hz, and parsed sys clock == configured sys_clk_hz;
  2. _CRG received exactly the parsed clocks;
  3. AX7101: platform part == TIMING_GRADE part; PLL VCO range is the -2 one
     derived from that part; the real PLL solver yields every requested
     output EXACTLY (margin 0) - these PLL outputs are what Vivado derives the
     reported clocks from;
  4. AX7101: pre-placement commands == configure_commands() (no clock literal)
     and the first bitstream command is the corner-report hook.
Negative controls (each must be refused BEFORE _CRG is reached):
  N1 recipe clock patched to 40 MHz; N2 shipping argv with --milan-clk-freq 100e6;
  N3 shipping argv with --milan-clk-freq 0 (falls back to the 100 MHz sys default).
Positive control P1: changed TIMING_GRADE part -> PLL VCO range changes.

Usage: <litex-python> -B probe_composition.py <repo-root>
"""
import contextlib
import io
import re
import shlex
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(ROOT / "sw/builder"), str(ROOT / "sw/litex")]
import endstation_builder as eb  # noqa: E402
import milan_soc  # noqa: E402
from tb.verilator.nvm_capture_cpu.recipe import CPU_HZ  # noqa: E402
from platforms.ax7101_timing import TIMING_GRADE, configure_commands  # noqa: E402

FAIL = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


class Stop(Exception):
    pass


def run_main(argv, recipe_hz=None):
    """Return ('crg', captured) or ('refused', stderr) or ('other', text)."""
    captured = {}
    real_crg = milan_soc._CRG
    real_parse = milan_soc.argparse.ArgumentParser.parse_args

    def parse(self, *a, **k):
        ns = real_parse(self, *a, **k)
        captured["args"] = ns
        return ns

    def crg(platform, sys_clk_freq, **kw):
        obj = real_crg(platform, sys_clk_freq, **kw)
        captured.update(platform=platform, sys=sys_clk_freq, kw=kw, crg=obj)
        raise Stop

    err = io.StringIO()
    ctx = [patch.object(sys, "argv", ["milan_soc.py", *argv]),
           patch.object(milan_soc, "_CRG", crg),
           patch.object(milan_soc.argparse.ArgumentParser, "parse_args", parse),
           contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO())]
    if recipe_hz is not None:
        ctx.append(patch.object(milan_soc, "BAREMETAL_CLK_HZ", recipe_hz))
    with contextlib.ExitStack() as st:
        for c in ctx:
            st.enter_context(c)
        try:
            milan_soc.main()
        except Stop:
            return "crg", captured
        except SystemExit as exc:
            return "refused", f"code={exc.code} {err.getvalue().strip().splitlines()[-1:]}"
        except Exception as exc:  # noqa: BLE001
            return "other", f"{type(exc).__name__}: {exc}"
    return "other", "main returned without reaching _CRG"


def pll_plan(crg_obj):
    pll = crg_obj.pll
    cfg = pll.compute_config()
    outs = {}
    for n, clkout in sorted(pll.clkouts.items()):
        outs[n] = (clkout.freq, cfg[f"clkout{n}_freq"], clkout.margin)
    return pll, cfg, outs


def verify(label, argv, clocks, board):
    print(f"[{label}] argv clock options: "
          f"{[a for i, a in enumerate(argv) if 'clk-freq' in a or (i and 'clk-freq' in argv[i-1])]}")
    kind, cap = run_main(argv)
    check(kind == "crg", f"{label}: real CLI reaches _CRG ({kind}: {cap if kind != 'crg' else ''})")
    if kind != "crg":
        return None
    args = cap["args"]
    eff = args.milan_clk_freq or args.sys_clk_freq
    check(eff == CPU_HZ == eb.BAREMETAL_CLK_HZ,
          f"{label}: effective Milan/CPU clock {eff:g} == recipe CPU_HZ {CPU_HZ} == builder {eb.BAREMETAL_CLK_HZ}")
    if clocks is not None:
        check(args.milan_clk_freq == clocks["milan_clk_hz"],
              f"{label}: parsed milan {args.milan_clk_freq:g} == configured {clocks['milan_clk_hz']}")
        check(args.sys_clk_freq == clocks["sys_clk_hz"],
              f"{label}: parsed sys {args.sys_clk_freq:g} == configured {clocks['sys_clk_hz']}")
    check(cap["sys"] == args.sys_clk_freq and cap["kw"].get("milan_clk_freq") == args.milan_clk_freq
          and cap["kw"].get("board") == board,
          f"{label}: _CRG got sys={cap['sys']:g} milan={cap['kw'].get('milan_clk_freq')} board={cap['kw'].get('board')}")
    try:
        pll, cfg, outs = pll_plan(cap["crg"])
    except ValueError as exc:
        if board == "ax7101":
            check(False, f"{label}: PLL plan solves ({exc})")
        else:
            # Outside #395 (AX7101 only) and unchanged by either merge side.
            print(f"  OBSERVATION {label}: out-of-scope board PLL plan does not solve at margin 0: {exc}")
        return args
    for n, (req, got, margin) in outs.items():
        check(req == got and margin == 0, f"{label}: PLL clkout{n} requested {req:g} solved {got:g} margin {margin}")
    reqs = {req for req, _, _ in outs.values()}
    check(cap["sys"] in reqs and (not args.milan_clk_freq or args.milan_clk_freq in reqs),
          f"{label}: sys and Milan clocks are PLL outputs ({sorted(reqs)})")
    print(f"  info {label}: vco={cfg['vco']:g} vco_range={pll.vco_freq_range} device={cap['platform'].device}")
    if board == "ax7101":
        p = cap["platform"]
        check(p.device == TIMING_GRADE["part"], f"{label}: platform part {p.device} == declared {TIMING_GRADE['part']}")
        grade = -int(TIMING_GRADE["part"].rsplit("-", 1)[1])
        ref = milan_soc.S7PLL(speedgrade=grade).vco_freq_range
        check(pll.vco_freq_range == ref, f"{label}: PLL VCO range {pll.vco_freq_range} == S7PLL(speedgrade={grade})")
        pre = [c.format(build_name="candidate") for c in p.toolchain.pre_placement_commands.resolve(None)]
        check(pre == configure_commands(), f"{label}: pre-placement == configure_commands()")
        check(not any(re.search(r"\d+e6|MHz|clk", c) for c in pre), f"{label}: grade setup carries no clock literal")
        bit = [c.format(build_name="candidate") for c in p.toolchain.bitstream_commands]
        check(bit[0] == "kl_timing_grade_reports candidate_signoff", f"{label}: corner-report hook first ({bit[0]})")
    return args


print(f"recipe CPU_HZ={CPU_HZ} builder BAREMETAL_CLK_HZ={eb.BAREMETAL_CLK_HZ} TIMING_GRADE={TIMING_GRADE}")
configs = sorted((ROOT / "configs").glob("endstation_*.yaml"))
check(len(configs) == 5, f"{len(configs)} tracked configurations")
for path in configs:
    cfg = eb.load_config(path)
    clocks = cfg["constraints"]
    print(f"[{path.stem}] configured pair sys={clocks['sys_clk_hz']} milan={clocks['milan_clk_hz']}")
    argv = eb.emit_soc_argv(cfg) + ["--entity-gen-dir", str(ROOT / "configs/generated" / path.stem)]
    verify(path.stem, argv, clocks, cfg["board_target"])

# The shipping launch: sweep.sh's AX7101 literal argv, unchanged by either side of the merge.
sweep = (ROOT / "sw/litex/sweep.sh").read_text()
opts = shlex.split(re.search(r'ax7101\) OPTS="([^"]+)"', sweep).group(1))
ship = opts + ["--entity-gen-dir", str(ROOT / "configs/generated/endstation_ax7101_1x1_tdm8")]
ship_cfg = eb.load_config(ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml")["constraints"]
verify("sweep.sh ax7101 (shipping)", ship, ship_cfg, "ax7101")

print("[negative controls: each must be refused before _CRG]")
for label, argv, hz in (
        ("N1 recipe clock 40 MHz", ship, 40_000_000),
        ("N2 --milan-clk-freq 100e6", ship + ["--milan-clk-freq", "100e6"], None),
        ("N3 --milan-clk-freq 0", ship + ["--milan-clk-freq", "0"], None)):
    kind, detail = run_main(argv, hz)
    check(kind == "refused" and "baremetal clock" in detail, f"{label}: {kind} {detail}")

print("[positive control P1: changed declared part reaches the PLL]")
with patch.dict(TIMING_GRADE, part="xc7a100t-fgg484-1"):
    kind, cap = run_main(ship)
    check(kind == "crg" and cap["platform"].device == "xc7a100t-fgg484-1"
          and cap["crg"].pll.vco_freq_range == milan_soc.S7PLL(speedgrade=-1).vco_freq_range
          and milan_soc.S7PLL(speedgrade=-1).vco_freq_range != milan_soc.S7PLL(speedgrade=-2).vco_freq_range,
          f"P1: part -1 -> VCO range {cap['crg'].pll.vco_freq_range if kind == 'crg' else kind}")

print(f"RESULT {'PASS' if not FAIL else 'FAIL'} failures={len(FAIL)}")
sys.exit(1 if FAIL else 0)
