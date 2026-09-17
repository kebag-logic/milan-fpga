#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gen_mac_tx_model.py - convert the SHIPPING MAC transmit chain to Verilog.

WHY THIS EXISTS. Issue #360 moves the gPTP egress timestamp from the first
accepted beat at the datapath's MAC boundary to the frame's observed launch,
because everything between those two points is a queue-dependent delay that
went straight into t1. Proving that repair needs the queue: a bench that
models the MAC proves what the model does, and a bench that replays a
recorded trace proves the bytes of that trace. So the transmit chain the
product builds is CONVERTED to Verilog here, and the closed loop in
`tb/verilator/gptp_txts` runs the real donor engine, the real plane, the real
PHC and this chain together at the true 125:50 clock ratio.

WHAT IS CONVERTED, and in which domains. Exactly the objects
`MilanMAC.__init__` builds between its supervised-reset block and its link
status CSR, with their product parameters:

  * the datapath AXIS crossing `mac_tx_cdc`, both halves, built by the
    PRODUCT's own `_axis_dp_cdc` in `cd_macdp` and `cd_macsys`;
  * the `last_be` conversion and the loopback mux, byte for byte the same
    expressions;
  * the store-and-forward `tx_sf` PacketFIFO in `cd_macsys`, 512 payload
    words and 8 frame slots, buffered;
  * `LiteEthMACCore` with preamble, CRC and padding, renamed onto
    `cd_macsys` and `cd_maceth_tx`;
  * the PHY's own transmit and receive register stages,
    `LiteEthPHYGMIITX`/`LiteEthPHYGMIIRX`, in `cd_eth_tx`/`cd_eth_rx`.

WHAT IS DELIBERATELY NOT CONVERTED. The PHY's clock and reset generator
(`LiteEthPHYGMIICRG`). It is clock generation, not datapath: it exists to
drive `cd_eth_tx` off the PHY's own pad clock through a vendor `BUFG` and to
forward `gtx` through a vendor `DDROutput`. The bench supplies those clocks
itself, at the true ratio and with a swept phase, which is the whole point of
running the two domains apart. Its RESET BEHAVIOUR is reproduced, not
skipped: `cd_eth_tx`/`cd_eth_rx` take `eth_rst` through the same
`AsyncResetSynchronizer` the CRG applies, and `cd_maceth_tx`/`cd_maceth_rx`
take it again exactly as `MilanMAC` does.

The gPTP launch observer is NOT instantiated here either. The product builds
it inside `MilanMAC` on `self.phy.sink`, and `sw/builder/test_builder.py`
gates that connection; this model EXPORTS that same seam so the bench can put
the real observer on it and an independent oracle on the pads, and so the one
register stage between them is measured rather than assumed.

HOW DRIFT IS CAUGHT. The manifest records the pinned migen, LiteX and LiteEth
revisions from `sw/litex/litex_pins.txt` and the SHA-256 of the `MilanMAC`
source region this file mirrors. `--check` regenerates and compares, so a
change to the product's transmit chain, or to any pin under it, is a red
before it is a wrong answer.

Usage:
    python3 sw/litex/gen_mac_tx_model.py          # regenerate the artifacts
    python3 sw/litex/gen_mac_tx_model.py --check  # refuse a stale artifact

Exit 0 = the generated Verilog and its manifest are current; 1 = they are
stale, or the product region moved; 2 = there is no usable LiteX interpreter,
which is a REFUSAL and never a silent skip.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SOC = REPO / "sw" / "litex" / "milan_soc.py"
PINS = REPO / "sw" / "litex" / "litex_pins.txt"
OUT_DIR = REPO / "tb" / "verilator" / "gptp_txts" / "generated"
OUT_V = OUT_DIR / "mac_tx_chain.v"
OUT_MANIFEST = OUT_DIR / "manifest.json"

#: The `MilanMAC` region this generator mirrors, delimited by two lines that
#: are already in the product source. Both are structural comments of the
#: class, so the region moves with the code rather than with a line number.
REGION_START = "        # MAC-path supervised reset (link-bounce wedge, 2026-07-19): the eth"
REGION_END = "        # ---- PHY/MAC link status (MAC_STATUS 0x110 / REQ-MAC-03) ---"

#: The product's transmit-chain shape, in one place so the generated model
#: and the manifest cannot disagree about it.
DATA_WIDTH = 64
TX_SF_PAYLOAD_DEPTH = 512
TX_SF_PARAM_DEPTH = 8

#: THE PINNED STACK, imported once. `--check` has to work on an interpreter
#: that does not carry it - it still compares the artifact against the
#: product source region, against the recorded pins and against its own
#: bytes, and says so - which is why a missing stack is recorded here and
#: refused at the one entry point that needs it, rather than raised at
#: import time.
sys.path.insert(0, str(REPO / "sw" / "litex"))
try:
    from migen import Module, Signal, ClockDomain, If, Mux, Record
    from migen.genlib.resetsync import AsyncResetSynchronizer
    from litex.gen import ClockDomainsRenamer, LiteXModule
    from litex.soc.interconnect.packet import PacketFIFO
    from liteeth.common import eth_phy_description
    from liteeth.mac.core import LiteEthMACCore
    from liteeth.phy.gmii import LiteEthPHYGMIITX, LiteEthPHYGMIIRX
    import milan_soc
    HAVE_LITEX = True
except ImportError:
    HAVE_LITEX = False


def product_region() -> str:
    """The `MilanMAC` transmit-chain source this model mirrors."""
    text = SOC.read_text(encoding="utf-8")
    start = text.find(REGION_START)
    end = text.find(REGION_END)
    if start < 0 or end < 0 or end <= start:
        raise SystemExit(
            f"{SOC}: the MilanMAC transmit-chain region could not be found "
            f"between its two anchors. This generator mirrors that region and "
            f"refuses to convert a chain it cannot locate: re-point "
            f"REGION_START/REGION_END at the moved anchors in the same change "
            f"that moved them.")
    return text[start:end]


def pinned_revisions() -> dict:
    """The pinned migen/LiteX/LiteEth revisions, read out of the pin file."""
    pins = {}
    for line in PINS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"git\+https://[^@]+/([^/@]+?)(?:\.git)?@([0-9a-f]{40})$",
                         line)
        if match:
            pins[match.group(1)] = match.group(2)
    for needed in ("migen", "litex", "liteeth"):
        if needed not in pins:
            raise SystemExit(
                f"{PINS}: no pinned revision for {needed}; the converted "
                f"chain would not name the sources it came from")
    return pins


if HAVE_LITEX:
    class _PhyStages(Module):
        """The PHY's own register stages, which is all of `LiteEthPHYGMII`
        that is datapath. `sink`/`source` are bound exactly as the product
        PHY binds them, so the MAC core connects to the same endpoints."""
        dw = 8
        tx_clk_freq = 125e6
        rx_clk_freq = 125e6

        def __init__(self, pads):
            self.submodules.tx = ClockDomainsRenamer("eth_tx")(
                LiteEthPHYGMIITX(pads))
            self.submodules.rx = ClockDomainsRenamer("eth_rx")(
                LiteEthPHYGMIIRX(pads))
            self.sink, self.source = self.tx.sink, self.rx.source

    class MacTxChain(LiteXModule):
        """The shipping MAC transmit chain, with its clocks and its two
        recovery levels brought to the boundary.

        A `LiteXModule` and not a plain migen `Module`, because the
        product's own `_axis_dp_cdc` registers the crossing it builds by
        plain attribute assignment - which is auto-submodule registration
        here and a silently discarded object anywhere else. The first
        version of this file was a plain `Module`, and the whole chain came
        out with an undriven ready.

        The four steps below are one construction split for reading only.
        Nothing is held between them on `self` that migen would register
        twice: what the last step needs, the one before it returns.
        """

        def __init__(self):
            self._declare_boundary()
            self._declare_domains()
            pads, phy = self._build_datapath()
            self._export_seams(pads, phy)

        def _declare_boundary(self):
            """The signals the bench drives and reads."""
            self.sys_clk = Signal()
            self.sys_rst = Signal()
            self.dp_clk = Signal()
            self.dp_rst = Signal()
            self.eth_tx_clk = Signal()
            self.eth_rx_clk = Signal()
            self.eth_phy_rst = Signal()
            self.reinit = Signal()
            self.eth_rst = Signal()
            self.loopback = Signal()

            self.dp_tdata = Signal(DATA_WIDTH)
            self.dp_tkeep = Signal(DATA_WIDTH // 8)
            self.dp_tvalid = Signal()
            self.dp_tlast = Signal()
            self.dp_tready = Signal()

            self.gmii_tx_en = Signal()
            self.gmii_tx_data = Signal(8)
            self.gmii_tx_er = Signal()

            #: THE OBSERVATION SEAM, exported: the stream the PHY's transmit
            #: register stage consumes. The product puts the launch observer
            #: here; the bench puts the same module here and its independent
            #: oracle on the pads above, so the one register stage between
            #: them is a measurement.
            self.phy_sink_valid = Signal()
            self.phy_sink_ready = Signal()
            self.phy_sink_data = Signal(8)
            self.phy_sink_last = Signal()
            #: the MAC transmit side's own reset, exported so the bench can
            #: hold the launch observer in exactly the reset the product
            #: holds it in - `ResetSignal("eth_tx") | eth_rst`, synchronised
            #: - rather than in one the bench invented
            self.maceth_tx_rst = Signal()

        def _declare_domains(self):
            """The product's shadow clock domains and their two resets."""
            # MilanMAC: macsys is `sys.rst | reinit`, macdp is
            # `milan_cd.rst | reinit`, and the two maceth domains are
            # `eth.rst | eth_rst`. The PHY's own eth domains take `eth_rst`
            # through the CRG's synchroniser first, which is why eth_rst
            # appears twice below and not once.
            self.clock_domains.cd_eth_tx = ClockDomain()
            self.clock_domains.cd_eth_rx = ClockDomain()
            self.clock_domains.cd_macsys = ClockDomain()
            self.clock_domains.cd_macdp = ClockDomain()
            self.clock_domains.cd_maceth_tx = ClockDomain()
            self.clock_domains.cd_maceth_rx = ClockDomain()
            resets = [
                (self.cd_eth_tx, self.eth_phy_rst | self.eth_rst),
                (self.cd_eth_rx, self.eth_phy_rst | self.eth_rst),
                (self.cd_macsys, self.sys_rst | self.reinit),
                (self.cd_macdp, self.dp_rst | self.reinit),
                (self.cd_maceth_tx, self.cd_eth_tx.rst | self.eth_rst),
                (self.cd_maceth_rx, self.cd_eth_rx.rst | self.eth_rst),
            ]
            self.comb += [
                self.cd_eth_tx.clk.eq(self.eth_tx_clk),
                self.cd_eth_rx.clk.eq(self.eth_rx_clk),
                self.cd_macsys.clk.eq(self.sys_clk),
                self.cd_macdp.clk.eq(self.dp_clk),
                self.cd_maceth_tx.clk.eq(self.eth_tx_clk),
                self.cd_maceth_rx.clk.eq(self.eth_rx_clk),
            ]
            self.specials += [AsyncResetSynchronizer(cd, src)
                              for cd, src in resets]

        def _build_datapath(self):
            """The chain itself, returning the two objects the seams read."""
            # ---- the PHY register stages and the MAC core ------------------
            pads = Record([("tx_en", 1), ("tx_data", 8), ("tx_er", 1),
                           ("rx_dv", 1), ("rx_data", 8), ("rx_er", 1)])
            self.submodules.phy = phy = _PhyStages(pads)
            self.submodules.core = ClockDomainsRenamer(
                {"sys": "macsys", "eth_tx": "maceth_tx",
                 "eth_rx": "maceth_rx"})(
                    LiteEthMACCore(phy=phy, dw=DATA_WIDTH,
                                   with_preamble_crc=True, with_padding=True))

            # ---- store and forward, in the product's own shape -------------
            self.submodules.tx_sf = ClockDomainsRenamer({"sys": "macsys"})(
                PacketFIFO(eth_phy_description(DATA_WIDTH),
                           payload_depth=TX_SF_PAYLOAD_DEPTH,
                           param_depth=TX_SF_PARAM_DEPTH,
                           buffered=True))
            self.comb += self.tx_sf.source.connect(self.core.sink)

            # ---- the datapath crossing, built by the PRODUCT's own helper --
            layout = [("data", DATA_WIDTH), ("keep", DATA_WIDTH // 8)]
            tx_dp = milan_soc._axis_dp_cdc(
                self, "mac_tx_cdc", layout, "macdp", to_datapath=False,
                rename={"sys": "macsys", "macdp": "macdp"})

            # ---- the boundary wiring, byte for byte the product's ----------
            self.comb += [
                tx_dp.dp.data.eq(self.dp_tdata),
                tx_dp.dp.keep.eq(self.dp_tkeep),
                tx_dp.dp.valid.eq(self.dp_tvalid),
                tx_dp.dp.last.eq(self.dp_tlast),
                self.dp_tready.eq(tx_dp.dp.ready),
                self.tx_sf.sink.data.eq(tx_dp.sys.data),
                self.tx_sf.sink.last.eq(tx_dp.sys.last),
                #: `last_be` is a one-hot pointer to the last valid byte and
                #: is only valid on the last beat, which is why the product
                #: gates it: driving the highest set bit unconditionally
                #: truncates every frame to its first beat. Same expression.
                self.tx_sf.sink.last_be.eq(
                    Mux(tx_dp.sys.last,
                        tx_dp.sys.keep & ~(tx_dp.sys.keep >> 1), 0)),
            ]
            self.comb += [
                If(self.loopback,
                   self.tx_sf.sink.valid.eq(0),
                   self.core.source.ready.eq(0),
                ).Else(
                   self.tx_sf.sink.valid.eq(tx_dp.sys.valid),
                   tx_dp.sys.ready.eq(self.tx_sf.sink.ready),
                   #: the product hands the core's RX source to the
                   #: datapath's own RX crossing; this model carries no RX
                   #: lane, so the source is drained rather than left to
                   #: back-pressure the core it is not part of
                   self.core.source.ready.eq(1),
                ),
            ]
            return pads, phy

        def _export_seams(self, pads, phy):
            """The observation seam, the pads and the observer's own reset."""
            self.comb += [
                self.phy_sink_valid.eq(phy.sink.valid),
                self.phy_sink_ready.eq(phy.sink.ready),
                self.phy_sink_data.eq(phy.sink.data),
                self.phy_sink_last.eq(phy.sink.last),
                self.gmii_tx_en.eq(pads.tx_en),
                self.gmii_tx_data.eq(pads.tx_data),
                self.gmii_tx_er.eq(pads.tx_er),
                self.maceth_tx_rst.eq(self.cd_maceth_tx.rst),
            ]


def build_chain() -> "MacTxChain":
    """The product transmit chain as a migen object.

    ONE object: it is what `build_verilog()` converts and what
    `sw/litex/test_gptp_tx_timestamp.py` simulates, as it stands. There is
    deliberately no simulation variant of it, because a second construction
    is a second thing that can be right about the conversion and wrong
    about the product. migen's own simulator drives the clock domains it is
    given a period for and lowers `AsyncResetSynchronizer` with its own
    model, so the boundary clock inputs and the reset specials above need
    no simulation spelling.
    """
    if not HAVE_LITEX:
        raise SystemExit(
            "this interpreter cannot import the pinned LiteX stack, so it "
            "cannot build the product's transmit chain; run it through "
            "$MILAN_LITEX_PYTHON")
    return MacTxChain()


def build_verilog() -> str:
    """Convert the product transmit chain to Verilog."""
    from migen.fhdl.verilog import convert
    from litex.build.sim.common import sim_special_overrides

    chain = build_chain()
    ios = {
        chain.sys_clk, chain.sys_rst, chain.dp_clk, chain.dp_rst,
        chain.eth_tx_clk, chain.eth_rx_clk, chain.eth_phy_rst,
        chain.reinit, chain.eth_rst, chain.loopback,
        chain.dp_tdata, chain.dp_tkeep, chain.dp_tvalid, chain.dp_tlast,
        chain.dp_tready,
        chain.gmii_tx_en, chain.gmii_tx_data, chain.gmii_tx_er,
        chain.phy_sink_valid, chain.phy_sink_ready, chain.phy_sink_data,
        chain.phy_sink_last, chain.maceth_tx_rst,
    }
    return str(convert(chain, ios=ios, name="mac_tx_chain",
                       special_overrides=sim_special_overrides))


def generate() -> tuple[str, dict]:
    """The Verilog and the manifest that says what it came from."""
    verilog = build_verilog()
    manifest = {
        "generator": "sw/litex/gen_mac_tx_model.py",
        "top": "mac_tx_chain",
        "data_width": DATA_WIDTH,
        "tx_sf_payload_depth": TX_SF_PAYLOAD_DEPTH,
        "tx_sf_param_depth": TX_SF_PARAM_DEPTH,
        "pins": pinned_revisions(),
        "milan_mac_region_sha256":
            hashlib.sha256(product_region().encode("utf-8")).hexdigest(),
        "verilog_sha256": hashlib.sha256(verilog.encode("utf-8")).hexdigest(),
    }
    return verilog, manifest


def check() -> int:
    """Refuse a stale artifact, at the strongest level this interpreter can.

    TWO LEVELS, and the report says which one ran. Both are real:

      * WITHOUT the pinned LiteX stack the artifact is compared against the
        product source region it was converted from, against the pins it
        records, and against its own recorded bytes. That catches the drift
        that matters - the product's transmit chain moved and the artifact
        did not - using nothing but this repository.
      * WITH the stack the chain is CONVERTED AGAIN and required to be byte
        identical, which additionally catches a converter or pin that moved
        under a product source that did not.

    A missing artifact is a failure at either level: the closed loop cannot
    be causal without it, and it is not regenerated silently by a check.
    """
    if not OUT_V.is_file() or not OUT_MANIFEST.is_file():
        print("STALE: the generated MAC transmit chain is not on disk; run "
              "sw/litex/gen_mac_tx_model.py with the pinned LiteX stack",
              file=sys.stderr)
        return 1
    recorded = json.loads(OUT_MANIFEST.read_text(encoding="utf-8"))
    verilog = OUT_V.read_text(encoding="utf-8")
    problems = []
    region = hashlib.sha256(product_region().encode("utf-8")).hexdigest()
    if recorded.get("milan_mac_region_sha256") != region:
        problems.append(
            f"the MilanMAC transmit-chain region is {region[:12]} and the "
            f"artifact was converted from "
            f"{str(recorded.get('milan_mac_region_sha256'))[:12]}")
    if recorded.get("verilog_sha256") != hashlib.sha256(
            verilog.encode("utf-8")).hexdigest():
        problems.append("the generated Verilog does not match its own "
                        "recorded hash")
    if recorded.get("pins") != pinned_revisions():
        problems.append("the recorded LiteX pins are not the pinned ones")

    level = "product source, pins and bytes"
    if HAVE_LITEX:
        fresh_v, fresh_m = generate()
        if fresh_v != verilog or fresh_m != recorded:
            problems.append("re-converting the product chain does not "
                            "reproduce the artifact byte for byte")
        level = "re-converted from the product source"

    if problems:
        print("STALE: the generated MAC transmit chain is not the chain the "
              "product builds. Regenerate it with "
              "sw/litex/gen_mac_tx_model.py and review the diff.",
              file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    print(f"generated MAC transmit chain: OK ({len(verilog.splitlines())} "
          f"lines, region {region[:12]}, checked by {level})")
    return 0


def main() -> int:
    """Regenerate, or refuse a stale artifact."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="refuse a stale artifact instead of writing one")
    args = parser.parse_args()

    if args.check:
        return check()

    if not HAVE_LITEX:
        print("REFUSED: this interpreter cannot import the pinned LiteX "
              "stack, so it cannot convert the product's transmit chain. "
              "The converted MAC is the only thing that makes the "
              "closed-loop bench causal, so this is a refusal and never a "
              "silent skip: install sw/litex/litex_pins.txt, or run this "
              "through $MILAN_LITEX_PYTHON.", file=sys.stderr)
        return 2

    verilog, manifest = generate()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_V.write_text(verilog, encoding="utf-8")
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True)
                            + "\n", encoding="utf-8")
    print(f"wrote {OUT_V.relative_to(REPO)} "
          f"({len(verilog.splitlines())} lines) and its manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
