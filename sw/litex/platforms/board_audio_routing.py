#
# WHICH AUDIO FRONT-END EACH TARGET BOARD ACTUALLY ROUTES - and the build-time
# refusal that goes with it.  Part of the Milan fully-FPGA SoC
# (sw/litex/milan_soc.py).
#
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# =============================================================================
#  WHY THIS FILE EXISTS
# =============================================================================
#
#  `--audio-interface tdmN` (and, once the master front-end lands,
#  `--audio-interface-master`) selects a capture front-end in milan_datapath.
#  Whether that front-end is REAL is a property of the BOARD, not of the config
#  and not of the tree: it is real exactly when the platform routes a `tdm`
#  resource to package pins.  Until 2026-07-28 nothing asked that question per
#  board, so an Arty build could be handed a TDM front-end and would:
#
#    (a) drive tdm bclk / fsync / dout into unconnected `Signal()`s and read
#        `i_tdm_data_i = 0`  ->  N channels of DIGITAL SILENCE; and
#    (b) rebind `o_i2s_mclk_o` away from the Pmod I2S2 - milan_datapath routes
#        the TDM master's MCLK out of the I2S mclk pin (one pin serves both
#        front-ends), so a master build MUST move that pin, and on a board with
#        no `tdm` pads it moves it to an unconnected `Signal()`.  pmoda:4 (ball
#        D13) is the MCLK of the CS5343 ADC, i.e. the ONLY working audio input
#        the Arty has, and the one the bench analog loop runs through.
#
#  Both were reported as a printed WARNING.  A warning is not enough:
#  docs/testing/methodology.md R5 - "a structural zero is not a measurement" -
#  a capability the fabric cannot back must read as UNSUPPORTED.  So this module
#  RAISES, and the build stops.
#
#  This is the same defect class item 00 exists to kill (a declaration that no
#  gate could compare against the wire), one layer down: there the talkers
#  advertised 8-channel AAF while the framer emitted stereo; here a front-end is
#  selected on a bus that reaches no pin.  It is also methodology escapes #3 and
#  #4 recurring - a front-end bound to a bus nothing drives, and a board with no
#  routed pins reading a constant zero.
#
# =============================================================================
#  THE ORACLE  (methodology R1)
# =============================================================================
#
#  THE PLATFORM - which pins actually exist on that board.  Read as TEXT out of
#  the sources this repo controls, never from a table maintained by hand, so
#  that the day a header is routed every answer that depends on it flips with no
#  edit here.  Two places can route a resource for a board:
#
#    1. the board's own platform file, when this repo ships it
#       (sw/litex/platforms/alinx_ax7101.py - the AX7101 is not in upstream
#       litex_boards);
#    2. a `plat.add_extension(...)` in sw/litex/milan_soc.py, which is how a
#       Pmod is attached to a STOCK litex_boards platform (the Arty's
#       `i2s_pmod_io("pmoda")` is exactly this).
#
#  NOT A SPEC QUESTION (methodology R3).  Nothing in IEEE 1722, IEEE 802.1BA or
#  Milan says which balls a board brings out; there is no clause to cite.  This
#  is a board-resource fact and the board is its only authority.
#
# =============================================================================
#  WHAT EACH BOARD ROUTES, AS MEASURED 2026-07-28
# =============================================================================
#
#  ALINX AX7101 - sw/litex/platforms/alinx_ax7101.py
#    i2s : NO.  `_connectors = []`, so there is no pmoda, so milan_soc.py's
#          connector-table gate leaves `i2s_pads = None` and `i_i2s_sdout_i = 0`
#          - a capture front-end clocking in a constant zero.  That is a KNOWN,
#          RECORDED item-00 finding owned by scripts/check_wire_accountability.py
#          and roadmap item 5; it is NOT re-litigated here (refusing it would
#          refuse the shipping 8x8 config), which is why only the TDM family is
#          hard-refused below.
#    tdm : whatever alinx_ax7101.py declares.  The 40-pin J11 expansion header
#          is the intended home; when its `tdm` resource is present this module
#          says yes on its own, with no edit.
#
#  DIGILENT ARTY A7-100 - litex_boards/platforms/digilent_arty.py (stock,
#  not in this repo) + the extensions milan_soc.py adds to it
#    i2s : YES.  `pmoda` = G13 B11 A11 D12 D13 B18 A18 K16, and milan_soc.py
#          adds `i2s_pmod_io("pmoda")` - Pmod I2S2 (CS5343 ADC + CS4344 DAC).
#          It consumes ALL EIGHT pmoda pins:
#            i2s_tx_mclk pmoda:0 G13     i2s_rx_mclk pmoda:4 D13
#            i2s_tx.sync pmoda:1 B11     i2s_rx.sync pmoda:5 B18
#            i2s_tx.clk  pmoda:2 A11     i2s_rx.clk  pmoda:6 A18
#            i2s_tx.tx   pmoda:3 D12     i2s_rx.rx   pmoda:7 K16
#    tdm : YES since HANDOVER 8.3b (USER DECISION 2026-07-28, superseding Lane
#          10's refusal): milan_soc.py adds `_arty_serial_io("tdm", "pmodb")`
#          on the arty path - mclk/bclk/fsync/din/dout on pmodb:0..4 (E15 E16
#          D15 C15 J17), a HIGH-SPEED Pmod (no 200 R series resistors, right
#          for a 12.288 MHz bclk).  Lane 10 refused a TDM front-end because a
#          SLAVE bus nothing drives frames silence and the mclk override
#          would have stolen D13; with real pins and a MASTER neither
#          applies - a master needs nobody to drive it, and the blend
#          (milan_datapath AUDIO_IF_I2S_PAIR_P -> KL_pair_blend) gives the
#          TDM header its OWN mclk pad so pmoda:4 (D13) never moves.  This
#          module answered "backed" the moment that line landed, with no
#          edit here - which is exactly how it was built to behave.
#
#  REMAINING FREE PINS ON THE ARTY: pmodc (U12 V12 V10 V11 U14 V14 T13 U13)
#  and pmodd (D4 D3 F4 F3 E2 D2 H2 G2) - 16 LVCMOS33 pins no resource claims -
#  plus pmodb:5..7 (J18 K15 J15) and the ck_io Arduino headers.  No TDM8
#  device is on the bench yet; until one is plugged into pmodb the TDM pairs
#  capture the header's idle level and the affected talkers frame silence
#  (KL_pair_zero_fill) - the scope acceptance is bclk 12.288 MHz and fsync
#  48.000 kHz on the header itself.

import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))

#: Platform source this repo ships for a board, if any. A board absent from this
#: map rides a stock litex_boards platform and can only gain a resource through
#: a milan_soc.py add_extension().
_REPO_PLATFORM = {"ax7101": "sw/litex/platforms/alinx_ax7101.py"}

_SOC_PY = "sw/litex/milan_soc.py"

#: The Arty's I2S MCLK pad, as the ONE fact the rest of the tree must not break.
#: pmoda index 4 of "G13 B11 A11 D12 D13 B18 A18 K16". Recorded here so a gate
#: can state it; verify_against_litex_boards() re-derives it from the real
#: platform whenever litex_boards is importable, which is what stops it from
#: being one more declaration.
ARTY_PMOD_CONNECTORS = {
    "pmoda": "G13 B11 A11 D12 D13 B18 A18 K16",
    "pmodb": "E15 E16 D15 C15 J17 J18 K15 J15",
    "pmodc": "U12 V12 V10 V11 U14 V14 T13 U13",
    "pmodd": "D4 D3 F4 F3 E2 D2 H2 G2",
}
ARTY_I2S_PMOD = "pmoda"
ARTY_I2S_RX_MCLK_INDEX = 4
ARTY_I2S_RX_MCLK_PIN = "D13"

#: Every connector the Arty brings out (the four Pmods plus the Arduino-shield
#: and XADC headers). Used to decide WHICH BOARD an add_extension lands on.
ARTY_CONNECTORS = tuple(ARTY_PMOD_CONNECTORS) + ("ck_io", "XADC")

#: Connector names that exist on any board this repo builds - the vocabulary
#: `_soc_adds_extension` uses to tell "placed on a connector" from "an ordinary
#: string argument".
_ALL_CONNECTOR_NAMES = frozenset(ARTY_CONNECTORS)

#: The audio-interface kinds that select a TDM front-end (milan_soc.py
#: --audio-interface choices). MIRRORS that argparse `choices` tuple; the gate
#: cross-checks the two so a new kind cannot be added on one side only.
TDM_KINDS = ("tdm8", "tdm16", "tdm32")


class UnroutedFrontEnd(Exception):
    """A build asked for an audio front-end the target board does not route."""


def _read(rel):
    try:
        with open(os.path.join(_ROOT, rel)) as fh:
            return fh.read()
    except OSError:
        return ""


def _strip_comments(text):
    """Drop `#` comments.

    These files document their pin choices in prose that quotes resource names
    and ball numbers - this very module does - and a DOCUMENTED resource must
    never read as a ROUTED one. Same discipline as the AX7101 taken-pin scan.
    """
    return "\n".join(l.split("#")[0] for l in text.split("\n"))


def _declares_routed_resource(text, name):
    """Does this platform source declare `("<name>", 0, ...)` with real pins?

    "Real" means at least one Subsignal (or bare Pins) carrying a non-empty
    package pin. An empty `Pins("")` is the `_connectors = []` defect wearing a
    resource name: the resource resolves, the pad goes nowhere.
    """
    body = _strip_comments(text)
    m = re.search(r'\(\s*["\']%s["\']\s*,\s*\d+\s*,' % re.escape(name), body)
    if not m:
        return False
    # The resource entry runs to the next top-level `("name", N,` or the end.
    nxt = re.search(r'\n\s{4}\(\s*["\'][\w]+["\']\s*,\s*\d+\s*,', body[m.end():])
    entry = body[m.end():m.end() + (nxt.start() if nxt else len(body))]
    return bool(re.search(r'Pins\(\s*["\'][A-Z]+\d+', entry))


def _board_connectors(board, plat_text):
    """The connector names `board` brings out.

    An add_extension is PLACED ON A CONNECTOR, so it reaches a board only if
    that board declares the connector. This is not a detail: milan_soc.py's
    `add_extension(i2s_pmod_io("pmoda"))` is one line serving both boards, and
    the AX7101 - `_connectors = []` - does not get an I2S front-end from it. Its
    own gate says so (`"pmoda" in ...connector_table`); this mirrors that gate
    rather than re-deciding it.
    """
    if board in _REPO_PLATFORM:
        body = _strip_comments(plat_text)
        m = re.search(r"_connectors\s*=\s*\[(.*?)\n\]", body, re.S)
        return set(re.findall(r'\(\s*["\']([\w]+)["\']\s*,', m.group(1))) \
            if m else set()
    # Stock litex_boards platform: the recorded connector table, re-derived by
    # verify_against_litex_boards() whenever the module can be imported.
    return set(ARTY_CONNECTORS) if board == "arty" else set()


def _soc_adds_extension(soc_text, board, name, plat_text=""):
    """Does milan_soc.py attach a `<name>` resource to `board`'s platform?

    An `add_extension` is how a Pmod reaches a STOCK litex_boards platform, so
    for a board whose platform this repo does not ship it is the only way a
    resource can appear. Comments are stripped first for the reason above -
    milan_soc.py's own prose names `tdm` dozens of times.
    """
    body = _strip_comments(soc_text)
    conns = _board_connectors(board, plat_text)
    for m in re.finditer(r"add_extension\(([^\n]*)", body):
        arg = m.group(1)
        if not re.search(r"\b%s\b" % re.escape(name), arg):
            continue
        # Which connector is it placed on? A quoted literal that names a
        # connector of ANY board is a placement; it must be one of THIS board's.
        placed = [q for q in re.findall(r'["\']([\w]+)["\']', arg)
                  if q in _ALL_CONNECTOR_NAMES]
        if placed and not (set(placed) & conns):
            continue
        return True
    return False


def routes(board, name, sources=None):
    """Does `board` route a `<name>` resource to real package pins?

    `sources` is an override dict {"plat": text, "soc": text} so a gate can hand
    this a mutated tree and prove each answer can flip (methodology R2). With no
    override it reads the working tree.

    `plat` is the text of a REPO-OWNED platform and is consulted only for a
    board that has one. Letting it answer for every board would make an AX7101
    header read as an Arty header - a per-board fact answered globally, which is
    the exact defect this module exists to stop.
    """
    if sources is None:
        plat = _read(_REPO_PLATFORM[board]) if board in _REPO_PLATFORM else ""
        soc = _read(_SOC_PY)
    else:
        plat = sources.get("plat", "") if board in _REPO_PLATFORM else ""
        soc = sources.get("soc", "")
    return (bool(plat) and _declares_routed_resource(plat, name)) \
        or _soc_adds_extension(soc, board, name, plat)


def routes_tdm(board, sources=None):
    """Does `board` bring a TDM bus out to pins?"""
    return routes(board, "tdm", sources)


def routes_i2s_pmod(board, sources=None):
    """Does `board` attach the Pmod I2S2 (the i2s_pmod_io extension)?"""
    return routes(board, "i2s_pmod_io", sources)


def assert_front_end_routed(board, audio_interface, audio_if_master=False,
                            sources=None):
    """REFUSE a build whose target board does not route the front-end it asks
    for.  Called from milan_soc.main() right after the platform is constructed,
    i.e. BEFORE anything elaborates, so the failure is a build failure and not a
    bitstream that emits zeros.

    Only the TDM family is refused.  The AX7101's pmoda-less I2S front-end is a
    named, owned item-00 finding (check_wire_accountability.py) and hard-
    refusing it here would refuse the shipping 8x8 config - out of scope, and a
    gate that refuses a config which demonstrably streams is the mistake already
    made and reverted once on 2026-07-27 (the `clusters`-derived format gate).
    """
    if audio_interface not in TDM_KINDS:
        return
    if routes_tdm(board, sources):
        return
    where = _REPO_PLATFORM.get(
        board, "litex_boards/platforms/digilent_arty.py (stock)")
    flags = "--audio-interface %s" % audio_interface
    if audio_if_master:
        flags += " --audio-interface-master"
    raise UnroutedFrontEnd(
        "--board {b} {f}: THE `tdm` RESOURCE DOES NOT EXIST ON THIS BOARD.\n"
        "  oracle: {w} declares no routed `tdm` resource, and {s} adds no TDM\n"
        "          extension on the {b} path.\n"
        "  building it would (a) drive tdm bclk/fsync/dout into unconnected\n"
        "          Signal()s and read tdm_data_i = 0 - digital SILENCE at the\n"
        "          declared width - and (b) rebind o_i2s_mclk_o off the I2S\n"
        "          front-end's pad{m}.\n"
        "  a capability the fabric cannot back must read as UNSUPPORTED, not\n"
        "          be warned about and then silently produce zeros\n"
        "          (docs/testing/methodology.md R5).\n"
        "  fix:    route a `tdm` resource for this board (and record the DEVICE\n"
        "          that plugs into it), or ask for a front-end it has:\n"
        "          --audio-interface i2s_philips.".format(
            b=board, f=flags, w=where, s=_SOC_PY,
            m=(" (Arty: pmoda:%d ball %s, the CS5343 MCLK and the only working\n"
               "          audio input this board has)"
               % (ARTY_I2S_RX_MCLK_INDEX, ARTY_I2S_RX_MCLK_PIN))
            if board == "arty" else ""))


def verify_against_litex_boards():
    """Re-derive the recorded Arty facts from the REAL platform module.

    Returns None when litex_boards is not importable (the plain-python gate
    environment), else raises AssertionError on any disagreement. A recorded
    fact that is never re-derived is just another declaration; this is the
    re-derivation.
    """
    try:
        from litex_boards.platforms import digilent_arty as _a
    except Exception:
        return None
    conn = dict((n, v) for n, v in _a._connectors)
    assert set(ARTY_CONNECTORS) == set(conn), \
        "arty connector table changed: recorded %r, platform %r" % (
            sorted(ARTY_CONNECTORS), sorted(conn))
    for name, pins in ARTY_PMOD_CONNECTORS.items():
        assert conn.get(name) == pins, \
            "arty %s pins moved: recorded %r, platform %r" % (
                name, pins, conn.get(name))
    got = conn[ARTY_I2S_PMOD].split()[ARTY_I2S_RX_MCLK_INDEX]
    assert got == ARTY_I2S_RX_MCLK_PIN, \
        "arty i2s_rx_mclk moved: recorded %s, platform %s" % (
            ARTY_I2S_RX_MCLK_PIN, got)
    src = open(_a.__file__).read()
    assert "tdm" not in src.lower(), \
        ("the stock Arty platform now mentions tdm - re-read it and update the "
         "routing record above rather than trusting this module")
    return True
