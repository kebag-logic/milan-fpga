#!/usr/bin/env python3
"""Documentation and builder gate for the writable corrections, on the bench branch."""
root = "$VALIDATION_STORAGE/829-a725/wt-bench/"
def patch(path, pairs):
    p = root + path
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old, s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)

WORD = ("**Unless the build sets `gptp.latency_writable` (#829).** With that key the word is live: `[15:0]` of a write is the "
        "correction the plane applies from the next plane clock, the build's value is only its reset value, `[31:16]` stores and "
        "reads back but is not applied, and `GPTP_LAT` (`0x7F0`) reads the result. ")
patch("docs/reference/REGISTER_MAP.md", [
("""| `0x540` | `PTP_INGRESS_LAT` | RW | `0` | 🟡 **Readable, inert scratch since `0x0056`.** A read returns the last written value; no timestamp-correction consumer reads the word at this VERSION. """,
 """| `0x540` | `PTP_INGRESS_LAT` | RW | `0` | 🟡 **Readable, inert scratch since `0x0056`.** A read returns the last written value; no timestamp-correction consumer reads the word at this VERSION. """ + WORD),
("""| `0x544` | `PTP_EGRESS_LAT` | RW | `0` | 🟡 **Readable, inert scratch since `0x0056`.** A read returns the last written value; no timestamp-correction consumer reads the word at this VERSION. """,
 """| `0x544` | `PTP_EGRESS_LAT` | RW | `0` | 🟡 **Readable, inert scratch since `0x0056`.** A read returns the last written value; no timestamp-correction consumer reads the word at this VERSION. """ + WORD),
("""constants and publishes what it applies at `GPTP_LAT` (`0x7F0`), because a
correction two layers could each apply is a correction applied twice.
""", """constants and publishes what it applies at `GPTP_LAT` (`0x7F0`), because a
correction two layers could each apply is a correction applied twice. A build
that sets `gptp.latency_writable` (#829) moves the source of those two values
to these two words and leaves the plane their one owner.
"""),
("""**This is the only live latency-correction publication.** `PTP_INGRESS_LAT`
(`0x540`) and `PTP_EGRESS_LAT` (`0x544`) remain readable, inert scratch with
no timestamp consumer, and that is deliberate: one owner cannot be two, and
a correction applied twice is worse than one applied nowhere. See the
""", """**This is the only live latency-correction publication.** `PTP_INGRESS_LAT`
(`0x540`) and `PTP_EGRESS_LAT` (`0x544`) remain readable, inert scratch with
no timestamp consumer, and that is deliberate: one owner cannot be two, and
a correction applied twice is worse than one applied nowhere. Under
`gptp.latency_writable` (#829) a write to either word moves what the plane
applies, and this word reads the applied pair after every write. See the
"""),
("""Elaboration constants, so the value is fixed for the bitstream and a write changes nothing. Option OFF reads zero.""",
 """Elaboration constants, so the value is fixed for the bitstream and a write changes nothing, unless the build sets `gptp.latency_writable` (#829): the pair is then the low halves of `0x540` and `0x544`, whose reset values are the build's. Option OFF reads zero."""),
])
patch("docs/design/GPTP_PLANE.md", [
("""`PTP_INGRESS_LAT` (`0x540`) stays readable, inert scratch.

So does `PTP_EGRESS_LAT` (`0x544`).

Neither has a timestamp consumer.

One owner cannot be two.

A correction two layers each apply is applied twice.
""", """`PTP_INGRESS_LAT` (`0x540`) stays readable, inert scratch.

So does `PTP_EGRESS_LAT` (`0x544`).

Neither has a timestamp consumer, unless the build sets the key below.

One owner cannot be two.

A correction two layers each apply is applied twice.
"""),
("""The builder REFUSES a board that omits either key.

A generated default looks exactly like a measured zero.
""", """The builder REFUSES a board that omits either key.

A generated default looks exactly like a measured zero.

#### Writable corrections

The key `gptp.latency_writable` is off unless a board states it (#829).

Off, the two corrections are the elaboration constants above, and no flop, port load or adder exists for them.

On, the same two values are only reset values.

A write to `0x540` or `0x544` then moves the correction, and `[15:0]` of the word is what is applied.

The applied value feeds the same arithmetic at the same point, with the same sign.

`GPTP_LAT` reads the applied pair after every write.

The plane is still the only consumer, so nothing applies a correction twice.

The CSR block and the plane share `axis_clk`, so the value crosses no clock domain and the crossing census has no new row.

A write takes effect within two plane clocks of the bus write: one for the ingress flop, one more for the egress net.

A stamp reads one register on one edge, so it carries the old value or the new one whole.

The arrival stamp reads the ingress value at the frame's first accepted beat.

The launch stamp reads the egress value where the record resolves, after the launch.

So a write inside an exchange spoils that exchange and no later one.

The two words are two bus writes, so a write of both can leave one exchange with one direction moved.

The neighbor rate ratio spans two exchanges, so the window across a write of `X` ns is off by `X` over that interval, for that window.

`make -C tb/verilator/gptp_txts run-latw` grades all of this at both link shapes, and `make -C tb/verilator/milan_dp gptp-latw` through the real CSR block.

The key is a bring-up and calibration lever, not a product surface.

A release board states its pair and leaves the key off.
"""),
])
patch("docs/design/TIME_SYNC.md", [
("""- `PTP_INGRESS_LAT` and `PTP_EGRESS_LAT` stay inert scratch.
""", """- `PTP_INGRESS_LAT` and `PTP_EGRESS_LAT` stay inert scratch, unless a build sets `gptp.latency_writable` (#829).
"""),
])
patch("docs/litex/CLOCK_DOMAINS.md", [
("""- No timestamp path consumes them at this VERSION.
- The live correction is the plane's, at `0x7F0` (#358).
""", """- No timestamp path consumes them at this VERSION, unless a build sets `gptp.latency_writable` (#829).
- That key's flops sit in `axis_clk`, the plane's own clock, so it adds no crossing.
- The live correction is the plane's, at `0x7F0` (#358).
"""),
])
patch("docs/fpga/DATAPLANE_WALKTHROUGH.md", [
("""| `PTP_INGRESS/EGRESS_LAT` `0x540`/`0x544` | readable, inert scratch: plain RW, the last written value returned, no timestamp-correction consumer at this VERSION |""",
 """| `PTP_INGRESS/EGRESS_LAT` `0x540`/`0x544` | readable, inert scratch: plain RW, the last written value returned, no timestamp-correction consumer at this VERSION unless a build sets `gptp.latency_writable` (#829) |"""),
])
patch("REQUIREMENTS.md", [
("""inert scratch (plain RW, the last written value returned, no
timestamp-correction consumer; the live publication is `GPTP_LAT` at `0x7F0`,
""", """inert scratch (plain RW, the last written value returned, no
timestamp-correction consumer unless a build sets `gptp.latency_writable`,
#829; the live publication is `GPTP_LAT` at `0x7F0`,
"""),
])
s = open(root + "docs/ENDSTATION_BUILDER.md", encoding="utf-8").read()
marker = "| 33a | AVB_INTERFACE interface_flags (generator-owned, no key) |"
assert s.count(marker) == 1
row = ("| 33e | `gptp.latency_writable` | Optional, false unless stated, and a YAML boolean or refused. True lets CSR `0x540` and `0x544` move the two "
       "corrections of row 33d at runtime (`milan_datapath` `GPTP_LAT_WRITABLE_P`, reached through `--gptp-lat-writable`), the stated pair being "
       "only their reset value. The flag and the parameter are emitted only when true, so a board that omits the key keeps a byte-identical argv "
       "and generated top `.v`. NOT part of the model hash, for the reason row 33d gives. | #829 | `milan_datapath` parameter |\n")
s = s.replace(marker, row + marker)
open(root + "docs/ENDSTATION_BUILDER.md", "w", encoding="utf-8").write(s)
patch("docs/testing/TESTING.md", [
("""The `gptp` and `gptp-lat` prerequisites run before the ordinary pool.
""", """The `gptp`, `gptp-lat` and `gptp-latw` prerequisites run before the ordinary pool.
"""),
])
patch("tb/verilator/gptp_txts/README.md", [
("""3770 ns, derived in
[GPTP_PLANE.md](../../../docs/design/GPTP_PLANE.md#the-100-mbs-mii-shape).
""", """3770 ns, derived in
[GPTP_PLANE.md](../../../docs/design/GPTP_PLANE.md#the-100-mbs-mii-shape).

`make run-latw` elaborates the plane with the writable corrections (#829), on
both shapes, and grades what the wire carries: a written pair moves t2 and t3 by
exactly that pair, and a write swept through an exchange leaves each stamp one
whole value and the next exchange the new pair.
"""),
("""one-octet-per-clock reading of #829, the first-symbol term, the transmit tick
and the history guard - and requires the suite to notice, restoring the exact
source afterwards.
""", """one-octet-per-clock reading of #829, the first-symbol term, the transmit tick
and the history guard, and on the writable build the wiring cut in each
direction and a reversed sign - and requires the suite to notice, restoring the
exact source afterwards.
"""),
])
patch("configs/endstation_arty_current.yaml", [
("""gptp:
  # ONE source (USER 2026-08-05): these values generate the AVB_INTERFACE
""", """gptp:
  # The two latency corrections below are only reset values on this board:
  # CSR 0x540 and 0x544 move them at runtime, and 0x7F0 reads what is applied
  # (#829). The AX7101 leaves this key off.
  latency_writable: true
  # ONE source (USER 2026-08-05): these values generate the AVB_INTERFACE
"""),
])
patch("sw/builder/test_builder.py", [
("""def test_gptp_latency_corrections_are_declared_and_carried() -> None:
""", """def test_gptp_latency_writable_key() -> None:
    \"\"\"Gate 36a (#829): off unless stated, and absent from what it leaves off.\"\"\"
    for name, path in CONFIGS.items():
        cfg = eb.load_config(path)
        writable = cfg["gptp"]["latency_writable"]
        argv = eb.emit_soc_argv(cfg)
        params = eb.datapath_params(cfg)
        assert ("--gptp-lat-writable" in argv) == writable, (
            f"gate 36a: {name}: argv and the key disagree: {argv}")
        assert ("GPTP_LAT_WRITABLE_P" in params) == writable, (
            f"gate 36a: {name}: datapath parameters and the key disagree")
        if name in GPTP_LAT_MEASURED:
            assert not writable, (
                f"gate 36a: {name} is a shipping AX7101 shape and must keep "
                f"its corrections elaboration constants")
    # A board that states the key off builds what one that omits it builds.
    base = eb.load_config(CONFIGS[BEHAVIOURAL_CFG])
    assert not base["gptp"]["latency_writable"]
    stated = _variant(CONFIGS[BEHAVIOURAL_CFG],
                      lambda c: c["gptp"].update(latency_writable=False))
    moved = _variant(CONFIGS[BEHAVIOURAL_CFG],
                     lambda c: c["gptp"].update(latency_writable=True))
    bad = _variant(CONFIGS[BEHAVIOURAL_CFG],
                   lambda c: c["gptp"].update(latency_writable=1))
    try:
        off = eb.load_config(stated)
        assert eb.emit_soc_argv(off) == eb.emit_soc_argv(base), (
            "gate 36a: stating the key off moved the SoC argv")
        on = eb.load_config(moved)
        assert eb.emit_soc_argv(on) == eb.emit_soc_argv(base) + ["--gptp-lat-writable"], (
            "gate 36a: the key on must add its flag and nothing else")
        assert on["model_id"]["hash"] == base["model_id"]["hash"], (
            "gate 36a: the key rotated entity_model_id, and it changes no "
            "descriptor (IEEE 1722.1 6.2.2.8)")
        try:
            eb.load_config(bad)
        except eb.ConfigError as exc:
            assert "latency_writable" in str(exc), (
                "gate 36a: a non-boolean key was refused for another reason")
        else:
            raise AssertionError("gate 36a: a non-boolean key was ACCEPTED")
    finally:
        stated.unlink()
        moved.unlink()
        bad.unlink()


def test_gptp_latency_corrections_are_declared_and_carried() -> None:
"""),
])
