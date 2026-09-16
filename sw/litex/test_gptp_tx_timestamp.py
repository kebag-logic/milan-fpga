#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The converted MAC transmit chain must behave like the chain it came from.

WHY THIS EXISTS (issue #360). The gPTP egress timestamp moved from the first
accepted beat at the datapath's MAC boundary to the frame's observed launch,
because everything between those two points is queueing delay that went
straight into t1. The bench that proves that repair -
`tb/verilator/gptp_txts` - is only causal because the MAC inside it is the
PRODUCT's transmit chain, converted to Verilog by
`sw/litex/gen_mac_tx_model.py`. That claim has two halves, and both have to
be checked or the closed loop is grading a model:

  * "the artifact is the conversion of THIS source" is a hash, and the
    generator's own `--check` carries it - it re-converts the chain and
    compares byte for byte;
  * "the conversion BEHAVES like the source" is this file. One fixed
    stimulus is driven through the converted Verilog (Verilator, through
    `tb/verilator/gptp_txts/pad_trace_main.cpp`) and through the migen
    objects themselves (`run_simulation`), and the two pad traces have to
    agree.

WHAT IS COMPARED. Every frame that reached the pads, as octets, and the
inter-frame gap in front of each frame after the first. Preamble, start-of
frame delimiter, padding to the minimum frame length, the frame check
sequence and the inter-frame gap are all inside that comparison, because the
chain produces all of them and a converter that lost any of them would still
pass a hash. The LEADING idle is outside it: the two runs begin recording at
different instants, which is a property of the two harnesses and not of the
chain.

WHY THE TWO RUNS ARE COMPARABLE AT ALL. Both drive the same five frames in
the same order at the same boundary, and both run the three clocks at the
product's periods AND at the same phases: migen's simulator raises a clock
of period p first at p/2, so the Verilator harness does the same, and no two
of the 8 ns, 10 ns and 20 ns edges ever coincide. The one difference is
deliberate: migen's simulator lowers `AsyncResetSynchronizer` with its own
combinational model while the conversion lowers it to the two-flop release,
so reset leaves the two chains one domain cycle apart. Both are then left
idle for four hundred nanoseconds before the first octet is offered, which
is where that difference goes.

WHAT THIS IS NOT. It is not a second timestamp oracle and it makes no timing
claim. The launch reference, the reconstruction bound, the queue invariance
and the recovery behaviour are graded in the closed loop, which has the
plane, the observer, the PHC and the engine in it. This file has the MAC,
and only asks whether its two spellings are the same MAC.

Usage:
    python3 sw/litex/test_gptp_tx_timestamp.py
    python3 sw/litex/test_gptp_tx_timestamp.py --keep <dir>   # keep traces

WHAT HAPPENS WITHOUT VERILATOR. The converted half of the comparison is a
Verilator build, so a host without Verilator cannot run this comparison at
all. That is a DECLARED SKIP (`RESULT: SKIP`, exit 0), the shape
scripts/run_litex_sims.sh counts as skipped and never as a pass: an absent
tool is not evidence either way, and reporting a comparison that did not
happen as a failure buries a real one. The skip is narrow on purpose. It is
declared ONLY when the Verilator executable is not on PATH; Verilator present
and the build failing stays a FAIL, because that is a broken conversion, a
broken artifact or a broken suite, and each of those is a finding. The
comparison itself is never relaxed.

Exit 0 = the two traces agree, or the comparison was declared skipped for
want of Verilator; 1 = they do not agree, or a trace could not be produced on
a host that has the tool to produce it.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SUITE = REPO / "tb" / "verilator" / "gptp_txts"
PAD_SIM = SUITE / "obj_pad" / "Vmac_tx_chain_pads"
#: The suite Makefile's own `VERILATOR ?= verilator`, read the same way, so a
#: host that points the suite at another build is asked about THAT build.
VERILATOR = os.environ.get("VERILATOR", "verilator")

#: The stimulus, in payload octets. It is the list
#: `tb/verilator/gptp_txts/pad_trace_main.cpp` drives, and the two are
#: reconciled below rather than trusted: a frame the converted side did not
#: send is a finding, not a silently shorter comparison.
#:
#: 46 is below the minimum frame length, so the chain's padding stage is in
#: the comparison; 67 is not a whole number of 64-bit beats, so the
#: `last_be` conversion the product writes by hand is too; 1518 is the
#: largest frame the product carries.
#:
#: THE LARGEST FRAME IS FIRST on purpose. It holds the wire for twelve
#: microseconds while the remaining three hundred octets arrive in one, so
#: the source is never what the wire is waiting for and every later gap is
#: the chain's own inter-frame gap - a property of the chain, and equal in
#: the two runs. Starved of data the gap instead measures the phase between
#: a harness's source and the wire, and the two harnesses' phases differ by
#: the one cycle their reset models differ by (see above), which is a
#: property of the simulators. Both were measured: with the largest frame
#: last, every octet of every frame still agreed and that one gap was 155
#: cycles against 154.
FRAME_LENGTHS = (1518, 46, 64, 67, 128)
#: the product's clock periods, in nanoseconds
DP_PERIOD_NS = 20
SYS_PERIOD_NS = 10
ETH_PERIOD_NS = 8
#: reset, then quiet, before the first octet is offered - the same two spans
#: the Verilator harness uses, in datapath cycles
RESET_DP_CYCLES = 400 // DP_PERIOD_NS
SETTLE_DP_CYCLES = 400 // DP_PERIOD_NS
#: Wire cycles the migen run records. The stimulus needs about 2 100 of
#: them; an unterminated last frame is reported rather than compared, so a
#: window that turned out to be too short cannot pass as agreement.
TRACE_CYCLES = 3000

TALLY = {"checks": 0, "fails": 0}


def check(name: str, ok: bool, detail: str = "") -> None:
    """One graded observation, in the shape the sweep reads."""
    TALLY["checks"] += 1
    if ok:
        print(f"  [ ok ] {name}")
        return
    TALLY["fails"] += 1
    print(f"  [FAIL] {name}" + (f": {detail}" if detail else ""))


def background_frame(length: int, tag: int) -> bytes:
    """A frame that is not gPTP; byte for byte the one the harness drives."""
    body = bytearray([tag & 0xFF] * length)
    body[0:6] = bytes((0x02, 0x11, 0x22, 0x33, 0x44, 0x55))
    body[6:12] = bytes((0x02, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE))
    body[12] = 0x22
    body[13] = 0xF0
    return bytes(body)


def frames_of(trace: list[tuple[int, int]]) -> tuple[list, bool]:
    """(gap before, octets) per frame, and whether the trace ended mid-frame.

    The gap is counted in wire cycles of idle immediately before the frame.
    A trace that stopped with the enable still high is reported, because the
    truncated frame it ends with would otherwise be compared as if it were
    short.
    """
    out: list[tuple[int, bytes]] = []
    gap = 0
    current = bytearray()
    for enable, data in trace:
        if enable:
            current.append(data)
        else:
            if current:
                out.append((gap, bytes(current)))
                current = bytearray()
                gap = 0
            gap += 1
    return out, bool(current)


def read_trace(path: Path) -> list[tuple[int, int]]:
    """A pad trace file: one `<enable> <octet>` line per wire cycle."""
    samples = []
    for line in path.read_text(encoding="utf-8").splitlines():
        enable, data = line.split()
        samples.append((int(enable), int(data, 16)))
    return samples


def converted_trace(path: Path) -> list[tuple[int, int]]:
    """Build and run the converted chain, and read back what its pads did."""
    build = subprocess.run(["make", "-s", "padtrace"], cwd=SUITE, check=False)
    if build.returncode != 0 or not PAD_SIM.is_file():
        print(f"the converted chain could not be built: "
              f"`make -C {SUITE.relative_to(REPO)} padtrace` returned "
              f"{build.returncode}. That build needs Verilator and the "
              f"generated artifact; without it there is nothing to compare "
              f"the migen source against.", file=sys.stderr)
        return []
    subprocess.run([str(PAD_SIM), str(path)], cwd=SUITE, check=True)
    return read_trace(path)


def migen_trace() -> list[tuple[int, int]]:
    """The same stimulus through the migen objects the chain was converted
    from - the same `build_chain()`, with no simulation variant of it."""
    sys.path.insert(0, str(REPO / "sw" / "litex"))
    from migen import run_simulation
    import gen_mac_tx_model as model

    dut = model.build_chain()
    trace: list[tuple[int, int]] = []

    def _drive():
        """Reset, wait, then offer the frames back to back."""
        yield dut.sys_rst.eq(1)
        yield dut.dp_rst.eq(1)
        yield dut.eth_phy_rst.eq(1)
        for _ in range(RESET_DP_CYCLES - 1):
            yield
        yield dut.sys_rst.eq(0)
        yield dut.dp_rst.eq(0)
        yield dut.eth_phy_rst.eq(0)
        for _ in range(SETTLE_DP_CYCLES):
            yield
        for index, length in enumerate(FRAME_LENGTHS):
            payload = background_frame(length, 0xA0 + index)
            for offset in range(0, len(payload), 8):
                chunk = payload[offset:offset + 8]
                yield dut.dp_tdata.eq(int.from_bytes(chunk.ljust(8, b"\x00"),
                                                     "little"))
                yield dut.dp_tkeep.eq((1 << len(chunk)) - 1)
                yield dut.dp_tvalid.eq(1)
                yield dut.dp_tlast.eq(1 if offset + 8 >= len(payload) else 0)
                #: a generator reads BEFORE the edge and writes for after
                #: it, so this is the handshake the chain itself sees
                yield
                while not (yield dut.dp_tready):
                    yield
        yield dut.dp_tvalid.eq(0)
        yield dut.dp_tlast.eq(0)

    def _sample():
        """The pads, once per wire cycle.

        `yield` first and read after, so each sample is the value the pads
        held AFTER the edge - the same instant the Verilator harness records
        and the same one a receiver would see.
        """
        for _ in range(TRACE_CYCLES):
            yield
            trace.append(((yield dut.gmii_tx_en), (yield dut.gmii_tx_data)))

    run_simulation(dut, {"macdp": _drive(), "eth_tx": _sample()},
                   clocks={"macdp": DP_PERIOD_NS, "macsys": SYS_PERIOD_NS,
                           "maceth_tx": ETH_PERIOD_NS,
                           "maceth_rx": ETH_PERIOD_NS,
                           "eth_tx": ETH_PERIOD_NS,
                           "eth_rx": ETH_PERIOD_NS})
    return trace


def expected_wire_length(payload: int) -> int:
    """What the chain owes the wire for a payload of `payload` octets.

    Seven preamble octets and the start-of-frame delimiter, the payload
    padded up to the minimum frame length, and four octets of frame check
    sequence. This is the stimulus reconciliation, not a model of the chain:
    it only has to catch the two runs having driven different frames.
    """
    return 8 + max(payload, 60) + 4


def compare(converted: list, source: list) -> None:
    """Grade the two traces against each other, frame by frame."""
    check("both runs put the same number of frames on the pads",
          len(converted) == len(source),
          f"converted {len(converted)}, migen {len(source)}")
    check("the converted run drove the whole stimulus",
          len(converted) == len(FRAME_LENGTHS),
          f"{len(converted)} frame(s) for {len(FRAME_LENGTHS)} lengths - the "
          f"two stimulus definitions have drifted apart")
    for index, (left, right) in enumerate(zip(converted, source)):
        gap_left, bytes_left = left
        gap_right, bytes_right = right
        first = next((i for i, (x, y) in enumerate(zip(bytes_left, bytes_right))
                      if x != y), min(len(bytes_left), len(bytes_right)))
        check(f"frame {index}: the same octets left the pads",
              bytes_left == bytes_right,
              f"{len(bytes_left)} octets against {len(bytes_right)}, first "
              f"difference at octet {first}")
        if index < len(FRAME_LENGTHS):
            want = expected_wire_length(FRAME_LENGTHS[index])
            check(f"frame {index}: it is the stimulus frame, framed",
                  len(bytes_left) == want,
                  f"{len(bytes_left)} octets on the wire, {want} expected for "
                  f"a {FRAME_LENGTHS[index]}-octet payload")
        if index > 0:
            check(f"frame {index}: the same inter-frame gap",
                  gap_left == gap_right,
                  f"{gap_left} wire cycles against {gap_right}")


def main() -> int:
    """Drive one stimulus through both spellings of the chain."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--keep", type=Path, default=None,
                        help="write both traces into this directory")
    args = parser.parse_args()

    if shutil.which(VERILATOR) is None:
        print(f"the converted half of this comparison is a Verilator build "
              f"and `{VERILATOR}` is not on PATH, so there is nothing to "
              f"compare the migen source against here.")
        print("\ntest_gptp_tx_timestamp: 0 checks: 0 PASS, 0 FAIL")
        print(f"RESULT: SKIP (no {VERILATOR} on PATH; this comparison needs "
              f"it to build the converted chain)")
        return 0

    scratch = tempfile.TemporaryDirectory()
    out = args.keep if args.keep else Path(scratch.name)
    out.mkdir(parents=True, exist_ok=True)

    print("converted chain (Verilator, the artifact the closed loop uses):")
    converted_samples = converted_trace(out / "pads_converted.txt")
    if not converted_samples:
        print("\ntest_gptp_tx_timestamp: 0 checks: 0 PASS, 1 FAIL")
        print("RESULT: FAIL")
        return 1

    print("migen source (run_simulation, the objects it was converted from):")
    source_samples = migen_trace()
    (out / "pads_migen.txt").write_text(
        "".join(f"{e} {d:02x}\n" for e, d in source_samples), encoding="utf-8")

    converted, converted_open = frames_of(converted_samples)
    source, source_open = frames_of(source_samples)
    print(f"  converted: {len(converted)} frame(s), "
          f"{sum(len(f) for _g, f in converted)} octets in "
          f"{len(converted_samples)} wire cycles")
    print(f"  migen:     {len(source)} frame(s), "
          f"{sum(len(f) for _g, f in source)} octets in "
          f"{len(source_samples)} wire cycles")
    check("the converted trace ends between frames", not converted_open,
          "it stops with the transmit enable still high")
    check("the migen trace ends between frames", not source_open,
          f"it stops with the transmit enable still high - {TRACE_CYCLES} "
          f"wire cycles did not cover the stimulus")
    compare(converted, source)

    checks, fails = TALLY["checks"], TALLY["fails"]
    print(f"\ntest_gptp_tx_timestamp: {checks} checks: "
          f"{checks - fails} PASS, {fails} FAIL")
    print("RESULT:", "FAIL" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
