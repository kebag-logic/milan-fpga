#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The retained SoC crossings keep their function with RAM-friendly storage (#640 lane M2).

`milan_soc` stores two kinds of crossing differently from stock LiteX:

  * `_payload_in_block_ram`, which `MilanMAC` applies to the two MAC
    crossings `_axis_dp_cdc` builds (`mac_tx_cdc`, `mac_rx_cdc`): the 72-bit
    payload sits in block RAM and the two framing flags in distributed RAM;
  * `_cross_csr_bus`, the CSR crossing: the W and R channel FIFOs keep their
    payload in block RAM, while AW, B and AR are left as LiteX builds them.

Only storage moved. These checks hold every one of those seven arrays, built
by the product code, against a stock LiteX crossing with the documented
parameters, in one simulation, with the same stimulus, at two clock ratios:

  storage   the arrays are split and tagged as intended, and no other way;
  lockstep  every handshake and every valid beat equal the reference's, on
            every edge of both clocks;
  order     random traffic arrives exactly, once each, in order;
  depth     with the reader stalled the crossing takes exactly its capacity
            (16 + 1 output register for a MAC crossing, 4 for a CSR
            channel), and every one of those beats then drains intact;
  reset     a reset with beats in flight leaves nothing behind (no stale or
            phantom beat), and the crossing is exact and full-depth after it.
            The MAC crossings take LINK_CTRL[1]'s reinit on both sides
            together; the CSR crossing takes sys and milan resets, and must
            pass traffic untouched through a MAC reinit.

The controls then plant one defect each into a scratch copy of
`milan_soc.py` and require the named check to fail on the named arrays:
a storage array half as deep as its pointers, a crossing 8 beats deep, a MAC
crossing with only one side in its reinit domain, a CSR crossing whose
datapath side sits in the MAC's reinit domain, and a storage read port one
entry ahead. A control the checks do not catch is a failure here.

Usage:
    python3 sw/litex/test_retained_cdc_storage.py               # checks, then controls
    python3 sw/litex/test_retained_cdc_storage.py --no-controls
    python3 sw/litex/test_retained_cdc_storage.py --soc-dir DIR --no-controls
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from types import ModuleType

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

#: The domains of the four clocks the crossings use. `macsys` and `macdp`
#: run on the sys and milan clocks; only their resets differ.
DOMAINS = ("sys", "milan", "macsys", "macdp")
#: Clock periods (sys, milan) of the two runs: the shipping 2:1 shape with
#: an offset that walks the phase, and a milan clock faster than sys. Both
#: are even: migen's simulator toggles a clock every `period // 2`, so an
#: odd period would run faster than the generators' own time base.
RATIOS = ((10, 22), (14, 6))
MAC_LAYOUT = [("data", 64), ("keep", 8)]
MAC_DEPTH = 16                  # the documented `_AXIS_CDC_DEPTH`
MAC_CAPACITY = MAC_DEPTH + 1    # plus the buffered output register
CSR_CAPACITY = 4                # LiteX's AXI-Lite crossing default
CHECKS = ("storage", "lockstep", "order", "depth", "reset")

#: One scenario, in units of the slower clock's period: (start, writer, reader).
#: The writer offers `random`ly, `always`, or stays `idle`; the reader is
#: `random`, `ready` or `stall`. Resets fall inside the `reset` window.
PLAN = (
    (0, "random", "random"),     # traffic          - order
    (400, "idle", "ready"),      # drain
    (440, "always", "stall"),    # fill to capacity - depth
    (520, "idle", "ready"),      # drain it intact
    (600, "always", "stall"),    # beats in flight
    (640, "idle", "stall"),
    (650, "idle", "stall"),      # destructive reset, 650-660
    (660, "idle", "ready"),      # nothing may arrive
    (700, "random", "random"),   # exact after the reset
    (900, "idle", "ready"),
    (940, "always", "stall"),    # full depth after the reset
    (1020, "idle", "ready"),
    (1100, "random", "random"),  # CSR: MAC reinit at 1250-1260 is invisible
    (1400, "idle", "ready"),
)
END = 1440
DESTRUCTIVE_RESET = (650, 660)
REINIT_PULSE = (1250, 1260)


def phase(time: float) -> tuple[str, str]:
    """The (writer, reader) modes in force at a time in slow periods."""
    current = PLAN[0]
    for row in PLAN:
        if time >= row[0]:
            current = row
    return current[1], current[2]


@dataclass
class Channel:
    """One array under test: the product's crossing and its reference."""
    array: str
    write_cd: str
    read_cd: str
    dut_sink: object
    dut_source: object
    ref_sink: object
    ref_source: object
    capacity: int
    accepted: list = field(default_factory=list)
    delivered: list = field(default_factory=list)
    mismatches: list = field(default_factory=list)


def fields_of(endpoint: object) -> list:
    """The signals a beat carries: payload fields, then first and last."""
    return [s for s, _ in endpoint.payload.iter_flat()] + [endpoint.first, endpoint.last]


def beat(endpoint: object) -> Generator:
    """The current beat on an endpoint, as a tuple of field values."""
    values = []
    for signal in fields_of(endpoint):
        values.append((yield signal))
    return tuple(values)


def import_soc(soc_dir: Path) -> ModuleType:
    """`milan_soc` from the given directory, with the LiteX stack it needs."""
    sys.path.insert(0, str(soc_dir))
    import milan_soc  # noqa: E402  (imported from the chosen tree)
    if Path(milan_soc.__file__).resolve().parent != soc_dir.resolve():
        raise SystemExit(f"imported {milan_soc.__file__}, not one from {soc_dir}")
    return milan_soc


def build_benches(soc: ModuleType) -> list:
    """The three benches (MAC TX, MAC RX, CSR), each a module and its channels."""
    from migen import ClockDomain, ClockDomainsRenamer
    from litex.gen import LiteXModule
    from litex.soc.interconnect import axi, stream

    class Bench(LiteXModule):
        """Four clock domains, one product crossing and one reference."""

        def __init__(self) -> None:
            for name in DOMAINS:
                setattr(self, f"cd_{name}", ClockDomain(name))
            self.channels: list[Channel] = []

    def mac_bench(to_datapath: bool) -> Bench:
        """One MAC crossing as MilanMAC builds it, beside its reference."""
        bench = Bench()
        # as MilanMAC builds each crossing
        product = soc._axis_dp_cdc(bench, "dut", MAC_LAYOUT, "milan",
                                   to_datapath=to_datapath,
                                   rename=soc._mac_cdc_rename("milan"))
        soc._payload_in_block_ram(bench.dut)
        cd_from, cd_to = ("sys", "milan") if to_datapath else ("milan", "sys")
        reference = stream.ClockDomainCrossing(MAC_LAYOUT, cd_from=cd_from,
                                               cd_to=cd_to, depth=MAC_DEPTH,
                                               buffered=True)
        bench.ref = ClockDomainsRenamer({"sys": "macsys", "milan": "macdp"})(reference)
        if to_datapath:
            write_cd, read_cd, sink, source = "macsys", "macdp", product.sys, product.dp
        else:
            write_cd, read_cd, sink, source = "macdp", "macsys", product.dp, product.sys
        bench.channels.append(Channel("mac_rx" if to_datapath else "mac_tx",
                                      write_cd, read_cd, sink, source,
                                      bench.ref.sink, bench.ref.source,
                                      MAC_CAPACITY))
        bench.storage_roots = [bench.dut]
        return bench

    def csr_bench() -> Bench:
        """The CSR crossing as add_milan_datapath builds it, beside LiteX's."""
        bench = Bench()
        master = axi.AXILiteInterface(data_width=32, address_width=32)
        slave = soc._cross_csr_bus(bench, master, "milan")
        ref_master = axi.AXILiteInterface(data_width=32, address_width=32)
        ref_slave = axi.AXILiteInterface(data_width=32, address_width=32)
        bench.ref = axi.AXILiteClockDomainCrossing(ref_master, ref_slave,
                                                   cd_from="sys", cd_to="milan")
        for name in ("aw", "w", "b", "ar", "r"):
            forward = name in ("aw", "w", "ar")
            ends = (master, slave, ref_master, ref_slave) if forward else \
                   (slave, master, ref_slave, ref_master)
            bench.channels.append(Channel(
                f"csr_{name}", "sys" if forward else "milan",
                "milan" if forward else "sys",
                *(getattr(end, name) for end in ends), CSR_CAPACITY))
        bench.storage_roots = [bench.milan_axil_cdc]
        return bench

    return [mac_bench(False), mac_bench(True), csr_bench()]


# ---------------------------------------------------------------------------
# storage: the arrays the product builds, read off the module tree
# ---------------------------------------------------------------------------
def arrays_under(module: object) -> list[tuple[int, int, str | None]]:
    """(width, depth, ram_style) of every storage array below a module."""
    from migen import Memory
    found = []
    for special in module._fragment.specials:
        if isinstance(special, Memory):
            styles = [v for k, v in getattr(special, "attr", set()) if k == "ram_style"]
            found.append((special.width, special.depth, styles[0] if styles else None))
    for _, child in module._submodules:
        found += arrays_under(child)
    return sorted(found, key=lambda a: (a[0], a[1], a[2] or ""))


#: The arrays each bench's product crossing must hold, exactly.
EXPECTED_ARRAYS = {
    "mac": [(2, MAC_DEPTH, "distributed"), (72, MAC_DEPTH, "block")],
    "csr": sorted([(37, 4, None), (36, 4, "block"), (2, 4, "distributed"),
                   (4, 4, None), (37, 4, None), (34, 4, "block"),
                   (2, 4, "distributed")], key=lambda a: (a[0], a[1], a[2] or "")),
}


# ---------------------------------------------------------------------------
# the simulation
# ---------------------------------------------------------------------------
def drive(endpoints: list, values: tuple | None) -> Generator:
    """Offer one beat (or nothing) on several endpoints at once."""
    for endpoint in endpoints:
        yield endpoint.valid.eq(values is not None)
        if values is not None:
            for signal, value in zip(fields_of(endpoint), values):
                yield signal.eq(value)


def writer(ch: Channel, period: int, slow: int, rng: Random) -> Generator:
    """Offer beats to both sinks; record what the product accepts."""
    widths = [len(s) for s in fields_of(ch.dut_sink)]
    offered = None
    cycle = 0
    while cycle * period < END * slow:
        now = cycle * period / slow
        valid = yield ch.dut_sink.valid
        ready = yield ch.dut_sink.ready
        ref_ready = yield ch.ref_sink.ready
        if ready != ref_ready:
            ch.mismatches.append(f"sink ready {ready}/{ref_ready} at t={now:.1f}")
        if valid and ready:
            ch.accepted.append((now, (yield from beat(ch.dut_sink))))
            offered = None
        mode = phase(now)[0]
        if mode == "idle":
            offered = None
        elif offered is None and (mode == "always" or rng.random() < 0.6):
            offered = tuple(rng.getrandbits(w) for w in widths)
        yield from drive([ch.dut_sink, ch.ref_sink], offered)
        yield
        cycle += 1


def reader(ch: Channel, period: int, slow: int, rng: Random) -> Generator:
    """Take beats from both sources; compare them; record the product's."""
    cycle = 0
    while cycle * period < END * slow:
        now = cycle * period / slow
        valid = yield ch.dut_source.valid
        ref_valid = yield ch.ref_source.valid
        ready = yield ch.dut_source.ready
        if valid != ref_valid:
            ch.mismatches.append(f"source valid {valid}/{ref_valid} at t={now:.1f}")
        elif valid:
            got, want = (yield from beat(ch.dut_source)), (yield from beat(ch.ref_source))
            if got != want:
                ch.mismatches.append(f"source beat differs at t={now:.1f}")
        if valid and ready:
            ch.delivered.append((now, (yield from beat(ch.dut_source))))
        mode = phase(now)[1]
        take = mode == "ready" or (mode == "random" and rng.random() < 0.6)
        for endpoint in (ch.dut_source, ch.ref_source):
            yield endpoint.ready.eq(take)
        yield
        cycle += 1


def resetter(bench: object, kind: str, period: int, slow: int) -> Generator:
    """Assert the destructive reset and, for the CSR bench, the MAC reinit."""
    destructive = ("macsys", "macdp") if kind == "mac" else ("sys", "milan")
    cycle = 0
    while cycle * period < END * slow:
        now = cycle * period / slow
        on = set()
        if DESTRUCTIVE_RESET[0] <= now < DESTRUCTIVE_RESET[1]:
            on |= set(destructive)
        if kind == "csr" and REINIT_PULSE[0] <= now < REINIT_PULSE[1]:
            on |= {"macsys", "macdp"}
        for name in DOMAINS:
            yield getattr(bench, f"cd_{name}").rst.eq(name in on)
        yield
        cycle += 1


def window(log: list, lo: float, hi: float) -> list:
    """The beats of a log whose time falls in [lo, hi)."""
    return [values for time, values in log if lo <= time < hi]


def grade(ch: Channel, kind: str) -> dict[str, tuple[bool, str]]:
    """The four behavioural checks for one channel, each with its evidence."""
    acc, dlv = ch.accepted, ch.delivered
    fill, fill2 = window(acc, 440, 520), window(acc, 940, 1020)
    results = {
        "lockstep": (not ch.mismatches,
                     "; ".join(ch.mismatches[:3]) or "every edge equal"),
        "order": (window(dlv, 0, 440) == window(acc, 0, 440)
                  and len(window(acc, 0, 400)) > 100,
                  f"{len(window(acc, 0, 400))} random beats"),
        "depth": (len(fill) == ch.capacity and window(dlv, 440, 600) == fill,
                  f"took {len(fill)} of {ch.capacity} with the reader stalled"),
    }
    stale = window(dlv, 600, 700)
    after = window(dlv, 700, 940) == window(acc, 700, 940) and len(window(acc, 700, 900)) > 50
    full = len(fill2) == ch.capacity and window(dlv, 940, 1100) == fill2
    clean = window(dlv, 1100, END) == window(acc, 1100, END) if kind == "csr" else True
    results["reset"] = (not stale and after and full and clean,
                        f"{len(stale)} beat(s) after the reset, exact after: {after}, "
                        f"full depth after: {full}"
                        + (f", exact through a MAC reinit: {clean}" if kind == "csr" else ""))
    return results


def run(soc: ModuleType) -> dict[tuple[str, str], list[tuple[bool, str]]]:
    """Every bench at every ratio; {(array, check): [(ok, evidence), ...]}."""
    from migen import run_simulation
    verdicts: dict[tuple[str, str], list[tuple[bool, str]]] = defaultdict(list)
    if any(period % 2 for ratio in RATIOS for period in ratio):
        raise SystemExit("every simulated clock period must be even")
    for sys_period, milan_period in RATIOS:
        for bench in build_benches(soc):
            kind = "mac" if bench.channels[0].array.startswith("mac") else "csr"
            arrays = [a for root in bench.storage_roots for a in arrays_under(root)]
            for ch in bench.channels:
                ok = arrays == EXPECTED_ARRAYS[kind]
                verdicts[(ch.array, "storage")].append((ok, f"{arrays}"))
            periods = {"sys": sys_period, "milan": milan_period,
                       "macsys": sys_period, "macdp": milan_period}
            slow = max(sys_period, milan_period)
            generators = defaultdict(list)
            for ch in bench.channels:
                seed = f"{ch.array}-{sys_period}-{milan_period}"
                generators[ch.write_cd].append(
                    writer(ch, periods[ch.write_cd], slow, Random(seed + "w")))
                generators[ch.read_cd].append(
                    reader(ch, periods[ch.read_cd], slow, Random(seed + "r")))
            generators["sys"].append(resetter(bench, kind, sys_period, slow))
            run_simulation(bench, dict(generators), clocks=periods)
            for ch in bench.channels:
                for check, result in grade(ch, kind).items():
                    verdicts[(ch.array, check)].append(
                        (result[0], f"{sys_period}/{milan_period}: {result[1]}"))
    return verdicts


def report(verdicts: dict[tuple[str, str], list[tuple[bool, str]]]) -> list[str]:
    """Print every verdict; return the failing (array, check) names."""
    failing = []
    for (array, check), results in sorted(verdicts.items()):
        ok = all(r[0] for r in results)
        for passed, evidence in results:
            print(f"  [{'ok  ' if passed else 'FAIL'}] {array} {check}: {evidence}")
        print(f"VERDICT {array} {check} {'PASS' if ok else 'FAIL'}")
        if not ok:
            failing.append(f"{array} {check}")
    return failing


# ---------------------------------------------------------------------------
# controls: one planted defect each, in a scratch copy of milan_soc.py
# ---------------------------------------------------------------------------
#: (name, product text, planted text, {array: the check that must fail})
CONTROLS = (
    ("storage-half-depth",
     '        array = Memory(bits, storage.depth, name="storage")\n',
     '        array = Memory(bits, storage.depth // 2, name="storage")\n',
     {"mac_tx": "depth", "mac_rx": "depth", "csr_w": "depth", "csr_r": "depth"}),
    ("crossing-depth-8",
     "_AXIS_CDC_DEPTH = 16\n",
     "_AXIS_CDC_DEPTH = 8\n",
     {"mac_tx": "depth", "mac_rx": "depth"}),
    ("mac-reset-one-side",
     '    return {"sys": "macsys", milan_cd: "macdp"}\n',
     '    return {"sys": "macsys"}\n',
     {"mac_tx": "reset", "mac_rx": "reset"}),
    ("csr-reset-domain",
     '        axil, csr_axil, cd_from="sys", cd_to=milan_cd)\n',
     '        axil, csr_axil, cd_from="sys", cd_to="macdp")\n',
     {"csr_w": "reset", "csr_r": "reset"}),
    ("read-address-ahead",
     "            array_read.adr.eq(read.adr),\n",
     "            array_read.adr.eq(read.adr + 1),\n",
     {"mac_tx": "order", "mac_rx": "order", "csr_w": "order", "csr_r": "order"}),
)


def planted_tree(scratch: Path, old: str, new: str) -> Path:
    """A tree that is this checkout except for one planted `milan_soc.py`."""
    source = (HERE / "milan_soc.py").read_text(encoding="utf-8")
    if source.count(old) != 1:
        raise ValueError(f"the product text to plant over occurs {source.count(old)} times")
    for parent, keep in ((REPO, "sw"), (REPO / "sw", "litex"), (HERE, "milan_soc.py")):
        target = scratch / parent.relative_to(REPO)
        target.mkdir(parents=True, exist_ok=True)
        for entry in parent.iterdir():
            if entry.name not in (keep, "__pycache__"):
                (target / entry.name).symlink_to(entry)
    (scratch / "sw/litex/milan_soc.py").write_text(source.replace(old, new), encoding="utf-8")
    return scratch / "sw/litex"


def run_control(old: str, new: str) -> subprocess.CompletedProcess | str:
    """These checks against one planted copy, or why they could not run."""
    scratch = Path(tempfile.mkdtemp(prefix="retained-cdc-control-"))
    try:
        soc_dir = planted_tree(scratch, old, new)
        return subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()),
                               "--soc-dir", str(soc_dir), "--no-controls"],
                              capture_output=True, text=True, timeout=1800)
    except (ValueError, subprocess.TimeoutExpired) as error:
        return str(error)
    finally:
        shutil.rmtree(scratch)


def controls(jobs: int) -> list[str]:
    """Run every control; return the ones the checks failed to catch."""
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        runs = list(pool.map(lambda c: run_control(c[1], c[2]), CONTROLS))
    missed = []
    for (name, _, _, must_fail), run_ in zip(CONTROLS, runs):
        if isinstance(run_, str):
            print(f"  [FAIL] control {name}: {run_}")
            missed.append(name)
            continue
        failed = {tuple(line.split()[1:3]) for line in run_.stdout.splitlines()
                  if line.startswith("VERDICT ") and line.endswith(" FAIL")}
        uncaught = [f"{a} {c}" for a, c in must_fail.items() if (a, c) not in failed]
        caught = run_.returncode == 1 and not uncaught
        print(f"  [{'ok  ' if caught else 'FAIL'}] control {name}: exit {run_.returncode}, "
              f"fails {', '.join(sorted(' '.join(f) for f in failed)) or 'nothing'}")
        if not caught:
            print(f"         expected to fail: {', '.join(f'{a} {c}' for a, c in must_fail.items())}")
            missed.append(name)
    return missed


def main() -> int:
    """Checks, then controls; exit 1 naming each failure."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--soc-dir", type=Path, default=HERE,
                        help="import milan_soc from this directory")
    parser.add_argument("--no-controls", action="store_true",
                        help="run the checks only")
    parser.add_argument("--jobs", type=int, default=4,
                        help="controls run at once (default 4)")
    args = parser.parse_args()
    print("test_retained_cdc_storage: the retained crossings keep their function (#640 M2)")
    soc = import_soc(args.soc_dir)
    problems = report(run(soc))
    if not args.no_controls:
        problems += [f"control {name} not caught" for name in controls(args.jobs)]
    for problem in problems:
        print(f"FAIL: {problem}", file=sys.stderr)
    print(f"test_retained_cdc_storage: {len(problems)} failure(s)")
    # the aggregate reads this line as the verdict, beside the exit status
    print(f"RESULT: {'PASS' if not problems else 'FAIL'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
