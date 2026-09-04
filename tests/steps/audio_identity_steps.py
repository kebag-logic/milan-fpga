# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for audio_walking_tone_identity.feature.
#
# TWO deliberate design choices, both from docs/testing/methodology.md.
#
# 1. IDENTITY uses tb/tools/avtp_wire_truth.py - the production decoder and the
#    production identity check - over payloads built by hand from IEEE 1722-2016
#    Figure 26. So the thing under test is the code the bench will run.
#
# 2. THD+N is implemented TWICE on purpose. The production analyser is
#    tb/tools/thdn.py and it needs numpy, which is not installed in
#    the interpreter this suite runs under. Rather than skip - a skipped audio
#    check is how audio gets forgotten - these steps carry an INDEPENDENT exact
#    coherent DFT derived from the DEFINITION of THD+N, in pure Python. It is
#    the oracle: it validates the METHOD (coherent, un-windowed, whole periods)
#    and it demonstrates, with numbers, both ways the method can be broken. The
#    production module's pure-Python parts - the acceptance gate and the
#    documented method - are then checked directly, so nothing about it is
#    assumed.
#
#    The reference DFT is O(n^2) and that is fine: 480 samples is 0.03 s, and an
#    FFT here would be a second implementation of the thing being validated.

from __future__ import annotations

import math
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from behave import given, then, when

# The annotations below are strings (PEP 563, imported above), so `Context` -
# the object behave hands every step - is wanted by a type checker and never at
# run time; importing it eagerly would bind a name no line of this file uses.
if TYPE_CHECKING:
    from behave.runner import Context

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tb" / "tools"))

import avtp_wire_truth as wt  # noqa: E402
import thdn as hthdn  # noqa: E402
import torture_campaign as tc  # noqa: E402

THDN_MODULE = ROOT / "tb" / "tools" / "thdn.py"


def _thdn_source():
    """The production THD+N analyser's source text, read and closed."""
    return THDN_MODULE.read_text()


def _thdn_analyse_body():
    """Just `analyse()`'s body out of that source, up to the next `def`."""
    return _thdn_source().split("def analyse(")[1].split("\ndef ")[0]


#: The walking pattern: channel c carries 1 << c on every sample event.  Every
#: channel is DISTINCT and every value names its own channel, so a swap, a
#: duplicate and a drop are three different failures.
def _tag(c):
    return 1 << c


def _frame(channels, per_channel, sample_frames=6):
    """One AAF frame whose channel c carries per_channel(c) on every event."""
    samples = [[per_channel(c) for c in range(channels)]
               for _ in range(sample_frames)]
    raw = wt.build_aaf_frame(channels=channels, sample_frames=sample_frames,
                             samples=samples)
    return wt.decode_aaf(wt.decode_eth(raw).payload)


# ---------------------------------------------------------------- reference --
def _dft_mag(x):
    """Exact DFT magnitudes for bins 0..n/2.  No FFT: an FFT here would be a
    second implementation of the transform whose result is under test."""
    n = len(x)
    out = []
    for k in range(n // 2 + 1):
        re = im = 0.0
        for i, v in enumerate(x):
            a = 2.0 * math.pi * k * i / n
            re += v * math.cos(a)
            im -= v * math.sin(a)
        out.append(math.hypot(re, im))
    return out


def reference_thdn(x: Sequence[float], rate: int, f0: int, *,
                   window: str | None = None, exclude: int = 1,
                   coherent: bool = True) -> float:
    """THD+N from the definition: residual power over fundamental power.

    `coherent` truncates to whole tone periods (what the production analyser
    does).  `window` and `exclude` exist ONLY so the two ways of breaking the
    method can be demonstrated rather than asserted.
    """
    period = rate // f0
    n = (len(x) // period) * period if coherent else len(x)
    if n < period:
        raise ValueError("not even one whole period")
    y = list(x[:n])
    if window == "hann":
        y = [v * 0.5 * (1.0 - math.cos(2.0 * math.pi * i / n))
             for i, v in enumerate(y)]
    mag = _dft_mag(y)

    def wgt(k: int) -> float:
        """The power weight of bin k: an interior bin of a one-sided spectrum
        stands for two of the two-sided transform, DC and Nyquist for one."""
        return 2.0 if 0 < k < n // 2 else 1.0

    k0 = round(f0 * n / rate)
    fund = wgt(k0) * mag[k0] ** 2
    resid = sum(wgt(k) * m * m for k, m in enumerate(mag)
                if k != 0 and abs(k - k0) > exclude)
    return 10.0 * math.log10(max(resid, 1e-300) / max(fund, 1e-300))


def _tone(n, rate=48000, f0=1000, h3_db=None):
    x = [math.sin(2.0 * math.pi * f0 * i / rate) for i in range(n)]
    if h3_db is not None:
        a = 10.0 ** (h3_db / 20.0)
        x = [v + a * math.sin(2.0 * math.pi * 3 * f0 * i / rate)
             for i, v in enumerate(x)]
    return x


# ------------------------------------------------------------------ fixtures --
@given("the audio identity model is importable")
def step_ai_import(context: Context) -> None:
    """The two production entry points exist before any scenario leans on
    them, and the per-scenario state starts empty rather than inherited."""
    assert hasattr(wt, "check_walking_tone")
    assert hasattr(hthdn, "verdict")
    context.ai_pdus = []
    context.ai_verdicts = []
    context.ai_thdn = None


@given("a {ch:d}-channel AAF frame carrying a walking tone")
def step_ai_walking(context: Context, ch: int) -> None:
    """The clean fixture: one frame of the walking pattern over `ch` channels,
    built by the production packer rather than by hand here."""
    context.ai_pdus = [_frame(ch, _tag)]


@given("a {ch:d}-channel AAF frame whose channels {a:d} and {b:d} are swapped")
def step_ai_swapped(context: Context, ch: int, a: int, b: int) -> None:
    """The same walking frame with two channels exchanged - the fault a
    pattern repeated across channels could never expose."""
    order = list(range(ch))
    order[a], order[b] = order[b], order[a]
    context.ai_pdus = [_frame(ch, lambda c: _tag(order[c]))]


@given("a {ch:d}-channel AAF frame where channel {a:d} is duplicated onto "
       "channel {b:d}")
def step_ai_dup(context: Context, ch: int, a: int, b: int) -> None:
    """A frame where one channel's tag arrives on two channels, which the
    identity check must tell apart from a swap."""
    context.ai_pdus = [_frame(ch, lambda c: _tag(a if c == b else c))]


@given("a {ch:d}-channel AAF frame where channel {a:d} was dropped")
def step_ai_dropped(context: Context, ch: int, a: int) -> None:
    """A frame where one channel carries silence instead of its own tag."""
    context.ai_pdus = [_frame(ch, lambda c: 0 if c == a else _tag(c))]


@when("the identity check runs for {ch:d} channels")
def step_ai_check(context: Context, ch: int) -> None:
    """Runs the PRODUCTION identity check - the code the bench will run - over
    the frames this scenario built."""
    context.ai_verdicts = wt.check_walking_tone(context.ai_pdus, ch,
                                                tag_of=_tag)


@then("every identity verdict is PASS")
def step_ai_all_pass(context: Context) -> None:
    """No verdict may be anything but PASS, and the ones that are get named."""
    bad = [(v.check, v.verdict, v.detail) for v in context.ai_verdicts
           if v.verdict != "PASS"]
    assert not bad, bad


@then('the identity check reports {want} on "{needle}"')
def step_ai_verdict(context: Context, want: str, needle: str) -> None:
    """The check whose name contains `needle` reached `want`; when it did not,
    the other verdicts and their details are printed rather than hidden."""
    hits = [v for v in context.ai_verdicts if needle in v.check]
    assert hits, f"no identity verdict matching {needle!r}: " \
                 f"{[v.check for v in context.ai_verdicts]}"
    got = {v.verdict for v in hits}
    assert want in got, f"{needle}: {sorted(got)} (details " \
                        f"{[v.detail for v in hits]})"


# ------------------------------------------------------- the preserving loop --
#
# THE DEFECT THIS SECTION WAS REWRITTEN TO REMOVE.  The return leg used to be
# built as `context.ai_returned = dict(context.ai_sent)` - a SHALLOW copy, so
# both dicts held THE SAME LIST OBJECTS - and the bit-exactness assertion then
# compared those objects with themselves.  `assert x == x` cannot fail, and there
# was no negative counterpart anywhere, so the scenario claiming bit-exactness of
# a channel-preserving loop was decoration.
#
# Now the return leg goes through the PRODUCTION DECODE PATH: the sent samples
# are packed into a real AAF frame by build_aaf_frame() (written from IEEE
# 1722-2016 Figure 26, not from our packetizer), the frame is decoded by
# decode_eth()/decode_aaf(), and the per-channel sample lists come back out of
# wt.channel_identity().  Every value therefore survives an encode, a wire
# layout, a 24-in-32 left-justification and a decode - which is what the bench
# loop actually does to it - and a single altered octet reddens the assertion.
def _through_the_wire(per_channel: dict, channels: int) -> dict:
    """Pack {channel: [samples]} into an AAF frame, decode it back, and return
    the decoded per-channel lists.  The oracle is the wire layout."""
    n = len(next(iter(per_channel.values())))
    grid = [[per_channel.get(c, [0] * n)[f] for c in range(channels)]
            for f in range(n)]
    raw = wt.build_aaf_frame(channels=channels, sample_frames=n, samples=grid)
    pdu = wt.decode_aaf(wt.decode_eth(raw).payload)
    chans = wt.channel_identity(pdu)
    return {c: list(chans[c]) for c in per_channel}


@given("a walking tone sent on channels {a:d} and {b:d}")
def step_ai_sent(context: Context, a: int, b: int) -> None:
    """The outbound leg: the bench's 1-based channel pair mapped onto the
    0-based wire, each channel carrying its own tag."""
    # channel numbers here are the USER-facing 1-based pair the bench talks
    # about ("ch 1/2"); the wire is 0-based, so the mapping is explicit
    context.ai_sent_chans = (a - 1, b - 1)
    context.ai_wire_channels = max(context.ai_sent_chans) + 1
    context.ai_sent = {c: [_tag(c)] * 6 for c in context.ai_sent_chans}


@when("the peer returns the same channels unchanged")
def step_ai_return_same(context: Context) -> None:
    """The return leg through the production encode/decode path, unaltered."""
    context.ai_returned = _through_the_wire(context.ai_sent,
                                            context.ai_wire_channels)


@when("the peer returns the channels swapped")
def step_ai_return_swapped(context: Context) -> None:
    """The return leg with the two channels exchanged on the wire."""
    a, b = context.ai_sent_chans
    crossed = {a: context.ai_sent[b], b: context.ai_sent[a]}
    context.ai_returned = _through_the_wire(crossed,
                                            context.ai_wire_channels)


@when("the peer returns channels {a:d} and {b:d} instead")
def step_ai_return_other(context: Context, a: int, b: int) -> None:
    """The return leg arriving on a different channel pair than it left on."""
    src = list(context.ai_sent_chans)
    moved = {a - 1: context.ai_sent[src[0]], b - 1: context.ai_sent[src[1]]}
    context.ai_returned = _through_the_wire(moved, max(a, b))


@when("the peer returns the same channels with sample {n:d} of channel {ch:d} "
      "altered by {delta:d}")
def step_ai_return_one_bit_off(context: Context, n: int, ch: int, delta: int) -> None:
    """THE NEGATIVE CONTROL for bit-exactness.  One sample, one channel, one
    increment - the smallest possible corruption of an otherwise perfect
    channel-preserving loop.  If the assertion cannot see this, it cannot see
    anything, and it could not: it was comparing a list to itself."""
    c = ch - 1
    mutated = {k: list(v) for k, v in context.ai_sent.items()}
    mutated[c][n] = mutated[c][n] + delta
    context.ai_returned = _through_the_wire(mutated,
                                            context.ai_wire_channels)


def _loop_result(context):
    sent, got = context.ai_sent, context.ai_returned
    same_keys = set(sent) == set(got)
    crossed = [c for c in sent if c in got and got[c] != sent[c]]
    return {"preserving": same_keys and not crossed,
            "crossed": sorted(crossed),
            "sent_channels": sorted(sent),
            "returned_channels": sorted(got)}


@then("the loop is channel-preserving")
def step_ai_loop_ok(context: Context) -> None:
    """The returned channel set is the sent one, value for value."""
    r = _loop_result(context)
    assert r["preserving"], r


@then("the loop is not channel-preserving")
def step_ai_loop_bad(context: Context) -> None:
    """The loop must NOT be channel-preserving here - the negative counterpart
    the bit-exactness scenario had no way to state before."""
    r = _loop_result(context)
    assert not r["preserving"], r


@then("the crossed channel pair is reported")
def step_ai_loop_crossed(context: Context) -> None:
    """The crossing is not merely detected but NAMED, so a bench report says
    which pair swapped instead of only that something did."""
    r = _loop_result(context)
    assert r["crossed"], r


@then("the returned samples are bit-exact with the sent samples")
def step_ai_bitexact(context: Context) -> None:
    """The loop's bit-exactness verdict, channel by channel, naming the index
    of the first differing sample on any channel that broke."""
    bad = {}
    for c, vals in context.ai_sent.items():
        got = context.ai_returned.get(c)
        # the two must be DISTINCT objects, or this assertion is comparing a
        # list with itself and can never fail (which is what it used to do)
        assert got is not vals, (
            f"channel {c}'s returned samples are THE SAME OBJECT as the sent "
            f"samples, so bit-exactness is unfalsifiable here")
        if got != vals:
            bad[c] = {"sent": vals, "returned": got,
                      "first_difference": next(
                          (i for i, (x, y) in enumerate(zip(vals, got or []))
                           if x != y), None)}
    assert not bad, bad


@then("the returned samples are NOT bit-exact with the sent samples")
def step_ai_not_bitexact(context: Context) -> None:
    """At least one returned channel differs from what was sent, or the
    corruption this scenario injected was invisible and the positive
    assertion above proves nothing."""
    diff = {c: (vals, context.ai_returned.get(c))
            for c, vals in context.ai_sent.items()
            if context.ai_returned.get(c) != vals}
    assert diff, ("every returned channel is bit-exact with what was sent, so "
                  "the corruption this scenario injected was invisible - the "
                  "assertion cannot bite")


@then("de-interleaving by the wire count yields {n:d} channels")
def step_ai_wire_count(context: Context, n: int) -> None:
    """De-interleaving follows channels_per_frame off the wire, and the wire
    agrees with the count the scenario states."""
    p = context.ai_pdus[0]
    chans = wt.channel_identity(p)
    assert len(chans) == n == p.channels_per_frame, \
        f"{len(chans)} channels from a {p.channels_per_frame}-channel frame"


@then("de-interleaving by a declared count of {n:d} is refused")
def step_ai_declared_count(context: Context, n: int) -> None:
    """The complement of the step above: a count the frame cannot support
    yields nothing, so de-interleaving cannot be satisfied by over-reading."""
    p = context.ai_pdus[0]
    # channel >= channels_per_frame has no sample on the wire, and the decoder
    # says so instead of reading the neighbouring channel's octets
    assert p.sample(0, n - 1) is None, (
        "a channel beyond channels_per_frame returned a sample - the decoder "
        "is following the declaration and not the wire")


# ------------------------------------------------------------------- THD+N --
@given("a synthetic {n:d} kHz tone of {ns:d} samples at {rate:d} kHz")
def step_ai_tone_khz(context: Context, n: int, ns: int, rate: int) -> None:
    """A mathematically perfect sine, coherently sampled - the input whose
    true THD+N is the arithmetic floor and nothing else."""
    context.ai_rate = rate * 1000
    context.ai_f0 = n * 1000
    context.ai_x = _tone(ns, context.ai_rate, context.ai_f0)


@given("a synthetic {n:d} kHz tone of {ns:d} samples at {rate:d} kHz with a "
       "{h3:d} dB third harmonic")
def step_ai_tone_h3(context: Context, n: int, ns: int, rate: int, h3: int) -> None:
    """The same tone with a third harmonic at a KNOWN level, so the measured
    THD+N has a value to be right about and not just a shape."""
    context.ai_rate = rate * 1000
    context.ai_f0 = n * 1000
    context.ai_x = _tone(ns, context.ai_rate, context.ai_f0, h3_db=h3)


@when("the reference THD+N is measured coherently without a window")
def step_ai_thdn_coherent(context: Context) -> None:
    """The reference measurement by the documented method: whole tone periods,
    no window - what the production analyser claims to do."""
    context.ai_thdn = reference_thdn(context.ai_x, context.ai_rate,
                                     context.ai_f0)


@when("the reference THD+N is measured with a Hann window excluding only the "
      "fundamental bin")
def step_ai_thdn_hann(context: Context) -> None:
    """The same samples measured with a Hann window and only the fundamental
    bin excluded: the first of the two ways this method breaks."""
    context.ai_thdn = reference_thdn(context.ai_x, context.ai_rate,
                                     context.ai_f0, window="hann", exclude=0)


@when("the reference THD+N is measured without truncating to whole periods")
def step_ai_thdn_noncoherent(context: Context) -> None:
    """The same samples measured without truncating to whole periods: the
    second way, where the fundamental's own leakage becomes the residual."""
    context.ai_thdn = reference_thdn(context.ai_x, context.ai_rate,
                                     context.ai_f0, coherent=False)


@then("the reference THD+N is at most {limit:d} dB")
def step_ai_thdn_floor(context: Context, limit: int) -> None:
    """The measurement is at or below the stated limit - the shape a correct
    method gives on a clean tone, in dB and not in adjectives."""
    assert context.ai_thdn <= limit, \
        f"reference read {context.ai_thdn:.1f} dB, expected <= {limit}"


@then("the reference THD+N is worse than {limit:d} dB")
def step_ai_thdn_worse(context: Context, limit: int) -> None:
    """The measurement is WORSE than the limit, which is how a broken method
    is demonstrated with a number instead of asserted."""
    assert context.ai_thdn > limit, \
        f"reference read {context.ai_thdn:.1f} dB, expected worse than {limit}"


@then("the reference THD+N is {want:d} dB within {tol:d} dB")
def step_ai_thdn_near(context: Context, want: int, tol: int) -> None:
    """The measurement lands on the level the harmonic was injected at: the
    reference is RIGHT, not merely self-consistent."""
    assert abs(context.ai_thdn - want) <= tol, \
        f"reference read {context.ai_thdn:.2f} dB, expected {want} +/- {tol}"


@then("the un-windowed measurement of the SAME samples is at most {limit:d} dB")
def step_ai_thdn_same_unwindowed(context: Context, limit: int) -> None:
    """The SAME samples re-measured without the window read clean, so the
    worse number above was the window's and not the signal's."""
    got = reference_thdn(context.ai_x, context.ai_rate, context.ai_f0)
    assert got <= limit, f"un-windowed read {got:.1f} dB"


@then("{rate:d} Hz with a {f0:d} Hz tone is not an integer number of samples "
      "per period")
def step_ai_incoherent_rate(context: Context, rate: int, f0: int) -> None:
    """Establishes the incoherent rate/tone pair the production-analyser steps
    below reuse, and proves it really is incoherent before they do."""
    # the arithmetic precondition itself, asserted without needing the module
    # to be runnable: 44100/1000 = 44.1 samples per period, so no truncation
    # makes the capture coherent and the un-windowed method does not apply
    assert rate % f0 != 0, f"{rate}/{f0} IS an integer - pick a rate that is not"
    context.ai_bad_rate = (rate, f0)


@then("the production THD+N analyser carries both coherence guards in its "
      "source")
def step_ai_guards_present(context: Context) -> None:
    """Both coherence guards are still in analyse(), and records - for the two
    steps below - whether a host without numpy could ever reach them."""
    body = _thdn_analyse_body()
    assert "if rate_hz % f0_hz:" in body, (
        "the coherence guard (rate_hz % f0_hz) is gone from analyse() - without "
        "it an incoherent capture gets a number instead of a refusal")
    assert "if periods < 8:" in body, (
        "the minimum-periods guard is gone from analyse()")
    # and the finding this scenario exists to record: the guards are BELOW the
    # numpy import, so they are unreachable on a host without numpy
    pre = body.split("if rate_hz % f0_hz:")[0]
    context.ai_guard_after_numpy = "import numpy" in pre


def _numpy_available():
    try:
        import numpy  # noqa: F401
        return True
    except ImportError:
        return False


@then("the production THD+N analyser refuses an incoherent rate where numpy "
      "exists")
def step_ai_prod_refuses_rate(context: Context) -> None:
    """The production analyser refuses an incoherent rate where numpy exists;
    where it does not, the guard being unreachable is what gets asserted,
    so the absence of numpy can never read as a pass."""
    rate, f0 = getattr(context, "ai_bad_rate", (44100, 1000))
    if not _numpy_available():
        assert context.ai_guard_after_numpy, (
            "numpy is absent AND the guard is not behind the numpy import, so "
            "it should have been reachable - re-check why it did not run")
        return
    try:
        hthdn.analyse([0.0] * 4096, rate_hz=rate, f0_hz=f0)
    except hthdn.ThdnError as e:
        assert "coherently" in str(e) or "integer" in str(e), str(e)
        return
    raise AssertionError("a non-integer samples-per-period was accepted")


@then("the production THD+N analyser refuses a capture shorter than 8 periods "
      "where numpy exists")
def step_ai_prod_refuses_short(context: Context) -> None:
    """The production analyser refuses a capture shorter than eight periods,
    on the same numpy-dependent terms as the rate guard above."""
    if not _numpy_available():
        assert context.ai_guard_after_numpy
        return
    try:
        hthdn.analyse([0.0] * (48 * 7), rate_hz=48000, f0_hz=1000)
    except hthdn.ThdnError as e:
        assert "8" in str(e), str(e)
        return
    raise AssertionError("a 7-period capture was accepted")


# ------------------------------------------------------------ the THD+N gate --
def _results(spec):
    """Build ThdnResult sets from the scenario's shorthand."""
    def one(ch: int, db: str, clipped: bool = False) -> hthdn.ThdnResult:
        """One result row: the shorthand's dB figure on one channel, with
        the surrounding fields fixed at values the gate does not weigh."""
        return hthdn.ThdnResult(channel=ch, thdn_dbfs=float(db),
                                fundamental_dbfs=-0.1, f0_hz=1000.0,
                                bins_used=241, samples_used=480, periods=10,
                                dc_dbfs=-300.0, clipped=clipped)
    if spec == "empty":
        return []
    if spec.endswith("clipped"):
        return [one(0, spec.split()[0], clipped=True)]
    return [one(i, v) for i, v in enumerate(spec.replace(" and ", " ").split())]


@given("a THD+N result set {spec}")
def step_ai_gate_set(context: Context, spec: str) -> None:
    """Builds the ThdnResult set the scenario describes in shorthand."""
    context.ai_results = _results(spec.strip())


@then("the THD+N gate verdict is {want} because {why}")
def step_ai_gate(context: Context, want: str, why: str) -> None:
    """The production acceptance gate's verdict on that set, with the
    scenario's own reason printed when the gate disagrees with it."""
    ok, msg = hthdn.verdict(context.ai_results, -120.0)
    got = "PASS" if ok else "FAIL"
    assert got == want, f"{got} ({msg}) - expected {want} because {why}"


# ------------------------------------------------------- L1 module bindings --
@then("the harness THD+N module states that it applies NO WINDOW")
def step_ai_no_window_doc(context: Context) -> None:
    """The analyser still SAYS it applies no window and still applies none: a
    window reintroduced silently makes every future number worse by
    construction, and nothing else in the tree would notice."""
    src = _thdn_source()
    assert "NO WINDOW" in src, (
        "the harness THD+N module no longer states that it applies no window; "
        "a window silently reintroduced makes every future number worse by "
        "construction and nothing else in the tree would notice")
    body = src.split("def analyse(")[1].split("\ndef ")[0]
    for banned in ("hanning", "hamming", "blackman", "bartlett", "kaiser",
                   "get_window", "np.hann"):
        assert banned not in body, (
            f"analyse() applies a {banned} window to a coherently sampled "
            f"tone; the scenarios above measure what that costs - about -3 dB "
            f"of manufactured distortion on a mathematically perfect sine")


@then("the harness THD+N module truncates to whole periods")
def step_ai_truncates(context: Context) -> None:
    """analyse() still truncates the capture to whole tone periods."""
    src = _thdn_source()
    body = src.split("def analyse(")[1]
    assert "periods = len(x) // period" in body and "n = periods * period" in body, \
        "analyse() no longer truncates the capture to whole tone periods"


@then("the harness THD+N module excludes DC and the fundamental skirt")
def step_ai_excludes(context: Context) -> None:
    """analyse() still zeroes DC and the fundamental's own skirt before it
    sums the residual."""
    src = _thdn_source()
    body = src.split("def analyse(")[1]
    assert "for k in (0, k0 - 1, k0, k0 + 1)" in body, \
        "analyse() no longer zeroes DC and the fundamental's own skirt"


@then("the harness THD+N module treats a clipped capture as invalid")
def step_ai_clipped(context: Context) -> None:
    """A clipped capture is INVALID rather than merely bad: the gate refuses
    it and says so, instead of reporting the distortion clipping caused."""
    src = _thdn_source()
    assert "is clipped - the measurement is invalid" in src
    ok, msg = hthdn.verdict(_results("-140 clipped"), -120.0)
    assert not ok and "clipped" in msg, (ok, msg)


# ---------------------------------------------------------- L1 plan bindings --
def _audio_plan():
    return tc.plan_audio()


@then("the campaign audio area has an identity step")
def step_ai_plan_identity(context: Context) -> None:
    """The campaign's audio area still carries an identity step at all."""
    assert any("identity" in s.sid for s in _audio_plan())


@then("the campaign audio area has a per-channel-distinct pattern")
def step_ai_plan_distinct(context: Context) -> None:
    """...and drives a per-channel-DISTINCT pattern: one that repeats a value
    across channels cannot fail on a swap (methodology R4)."""
    hits = [s for s in _audio_plan()
            if s.args.get("per_channel_distinct")]
    assert hits, ("no audio step drives a per-channel-DISTINCT pattern; a "
                  "pattern that repeats a value across channels cannot fail "
                  "on a swap (methodology R4)")


@then("the campaign audio area has a THD+N step that reuses the harness "
      "analyser")
def step_ai_plan_thdn(context: Context) -> None:
    """...and a THD+N step that names the harness analyser, because
    reimplementing it is how the window trap comes back."""
    hits = [s for s in _audio_plan() if "thdn" in s.sid]
    assert hits, "no THD+N step in the audio area"
    assert "thdn.py" in hits[0].args.get("analyser", ""), (
        "the THD+N step does not name the harness analyser - reimplementing it "
        "is how the window trap comes back")


@then("the campaign audio area has a channel-preserving loop through the peer")
def step_ai_plan_loop(context: Context) -> None:
    """...and a channel-preserving loop through the peer, on the channel pair
    the bench actually cables."""
    hits = [s for s in _audio_plan() if "loop" in s.sid]
    assert hits, "no channel-preserving loop step in the audio area"
    assert hits[0].args.get("channels") == [1, 2], hits[0].args
    assert "peer" in hits[0].args, hits[0].args


# ---------------------------------------- L1: the audio area's OWN coverage --
#
# WHY THIS IS AUDITED PER AREA. plan_covers_every_index() is computed over the
# WHOLE plan, and the matrix area walks every index - so the matrix's coverage
# MASKED the audio area completely, and the audio area was index-0-only
# (talker 0, peer listener 0, peer talker 0) under a green coverage report. That
# is the same structural blindness as an assertion that cannot fail: the audit
# could not say no about the area it was asked about.
@then("the campaign audio area walks every AAF talker index")
def step_ai_plan_every_talker(context: Context) -> None:
    """The audio area walks EVERY AAF talker index.  Index 0 is a hard alias
    of the flat registers on this fabric, so an index-0-only audio area
    tests the alias path and nothing else."""
    ok, d = tc.area_covers_every_index(tc.build_plan(), "audio")
    assert ok, (f"the AUDIO area does not walk every index: missing "
                f"{d['missing']} (covered {d['covered']}, expected "
                f"{d['expected']}).  Index 0 is the LEAST representative index "
                f"on this fabric - the 0x800 window makes it a hard alias of "
                f"the flat registers - so an index-0-only audio area tests the "
                f"alias path and nothing else.")
    context.ai_area_cov = d


@then("the campaign audio area covers more than index {n:d}")
def step_ai_plan_not_index0(context: Context, n: int) -> None:
    """The covered talker set is more than the single index named, so a plan
    that shrank back to one index cannot pass the step above by accident."""
    cov = context.ai_area_cov["covered"]
    assert cov["dut_talker"] != [n], cov
    assert len(cov["dut_talker"]) > 1, cov


@then("the per-area audit reddens on an index-0-only audio area")
def step_ai_plan_audit_bites(context: Context) -> None:
    """The negative control for the audit itself: an index-0-only audio area
    must redden the AUDIO audit while the MATRIX audit stays green - which
    is exactly what the whole-plan audit could not do."""
    # THE NEGATIVE CONTROL for the audit itself: prune the audio area down to
    # its .t0 steps and the AUDIO audit must say no while the MATRIX audit stays
    # green - which is exactly what the whole-plan audit could not do.
    plan = tc.build_plan()
    lonely = [s for s in plan if s.area != "audio"
              or s.sid.endswith(".t0") or s.sid == "audio.thdn"]
    ok, d = tc.area_covers_every_index(lonely, "audio")
    assert not ok, ("an index-0-only audio area passed the audit, so the audit "
                    "cannot say no")
    assert d["missing"]["dut_talker"], d
    assert tc.area_covers_every_index(lonely, "matrix")[0], (
        "the matrix audit went red too, so this is not isolating the audio area")
    # and the WHOLE-PLAN audit is still green over the same plan: the masking
    whole = tc.plan_covers_every_index(lonely)
    assert whole["dut_talker"] == tc.ARTY.talker_indices(), whole
