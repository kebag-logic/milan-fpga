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

import math
import os
import sys

from behave import given, then, when

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tb", "tools"))

import avtp_wire_truth as wt  # noqa: E402
import thdn as hthdn  # noqa: E402
import torture_campaign as tc  # noqa: E402

THDN_MODULE = os.path.join(ROOT, "tb", "tools", "thdn.py")

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


def reference_thdn(x, rate, f0, *, window=None, exclude=1, coherent=True):
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

    def wgt(k):                     # interior bins of a one-sided spectrum
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
def step_ai_import(context):
    assert hasattr(wt, "check_walking_tone")
    assert hasattr(hthdn, "verdict")
    context.ai_pdus = []
    context.ai_verdicts = []
    context.ai_thdn = None


@given("a {ch:d}-channel AAF frame carrying a walking tone")
def step_ai_walking(context, ch):
    context.ai_pdus = [_frame(ch, _tag)]


@given("a {ch:d}-channel AAF frame whose channels {a:d} and {b:d} are swapped")
def step_ai_swapped(context, ch, a, b):
    order = list(range(ch))
    order[a], order[b] = order[b], order[a]
    context.ai_pdus = [_frame(ch, lambda c: _tag(order[c]))]


@given("a {ch:d}-channel AAF frame where channel {a:d} is duplicated onto "
       "channel {b:d}")
def step_ai_dup(context, ch, a, b):
    context.ai_pdus = [_frame(ch, lambda c: _tag(a if c == b else c))]


@given("a {ch:d}-channel AAF frame where channel {a:d} was dropped")
def step_ai_dropped(context, ch, a):
    context.ai_pdus = [_frame(ch, lambda c: 0 if c == a else _tag(c))]


@when("the identity check runs for {ch:d} channels")
def step_ai_check(context, ch):
    context.ai_verdicts = wt.check_walking_tone(context.ai_pdus, ch,
                                                tag_of=_tag)


@then("every identity verdict is PASS")
def step_ai_all_pass(context):
    bad = [(v.check, v.verdict, v.detail) for v in context.ai_verdicts
           if v.verdict != "PASS"]
    assert not bad, bad


@then('the identity check reports {want} on "{needle}"')
def step_ai_verdict(context, want, needle):
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
def step_ai_sent(context, a, b):
    # channel numbers here are the USER-facing 1-based pair the bench talks
    # about ("ch 1/2"); the wire is 0-based, so the mapping is explicit
    context.ai_sent_chans = (a - 1, b - 1)
    context.ai_wire_channels = max(context.ai_sent_chans) + 1
    context.ai_sent = {c: [_tag(c)] * 6 for c in context.ai_sent_chans}


@when("the peer returns the same channels unchanged")
def step_ai_return_same(context):
    context.ai_returned = _through_the_wire(context.ai_sent,
                                            context.ai_wire_channels)


@when("the peer returns the channels swapped")
def step_ai_return_swapped(context):
    a, b = context.ai_sent_chans
    crossed = {a: context.ai_sent[b], b: context.ai_sent[a]}
    context.ai_returned = _through_the_wire(crossed,
                                            context.ai_wire_channels)


@when("the peer returns channels {a:d} and {b:d} instead")
def step_ai_return_other(context, a, b):
    src = list(context.ai_sent_chans)
    moved = {a - 1: context.ai_sent[src[0]], b - 1: context.ai_sent[src[1]]}
    context.ai_returned = _through_the_wire(moved, max(a, b))


@when("the peer returns the same channels with sample {n:d} of channel {ch:d} "
      "altered by {delta:d}")
def step_ai_return_one_bit_off(context, n, ch, delta):
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
def step_ai_loop_ok(context):
    r = _loop_result(context)
    assert r["preserving"], r


@then("the loop is not channel-preserving")
def step_ai_loop_bad(context):
    r = _loop_result(context)
    assert not r["preserving"], r


@then("the crossed channel pair is reported")
def step_ai_loop_crossed(context):
    r = _loop_result(context)
    assert r["crossed"], r


@then("the returned samples are bit-exact with the sent samples")
def step_ai_bitexact(context):
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
def step_ai_not_bitexact(context):
    diff = {c: (vals, context.ai_returned.get(c))
            for c, vals in context.ai_sent.items()
            if context.ai_returned.get(c) != vals}
    assert diff, ("every returned channel is bit-exact with what was sent, so "
                  "the corruption this scenario injected was invisible - the "
                  "assertion cannot bite")


@then("de-interleaving by the wire count yields {n:d} channels")
def step_ai_wire_count(context, n):
    p = context.ai_pdus[0]
    chans = wt.channel_identity(p)
    assert len(chans) == n == p.channels_per_frame, \
        f"{len(chans)} channels from a {p.channels_per_frame}-channel frame"


@then("de-interleaving by a declared count of {n:d} is refused")
def step_ai_declared_count(context, n):
    p = context.ai_pdus[0]
    # channel >= channels_per_frame has no sample on the wire, and the decoder
    # says so instead of reading the neighbouring channel's octets
    assert p.sample(0, n - 1) is None, (
        "a channel beyond channels_per_frame returned a sample - the decoder "
        "is following the declaration and not the wire")


# ------------------------------------------------------------------- THD+N --
@given("a synthetic {n:d} kHz tone of {ns:d} samples at {rate:d} kHz")
def step_ai_tone_khz(context, n, ns, rate):
    context.ai_rate = rate * 1000
    context.ai_f0 = n * 1000
    context.ai_x = _tone(ns, context.ai_rate, context.ai_f0)


@given("a synthetic {n:d} kHz tone of {ns:d} samples at {rate:d} kHz with a "
       "{h3:d} dB third harmonic")
def step_ai_tone_h3(context, n, ns, rate, h3):
    context.ai_rate = rate * 1000
    context.ai_f0 = n * 1000
    context.ai_x = _tone(ns, context.ai_rate, context.ai_f0, h3_db=h3)


@when("the reference THD+N is measured coherently without a window")
def step_ai_thdn_coherent(context):
    context.ai_thdn = reference_thdn(context.ai_x, context.ai_rate,
                                     context.ai_f0)


@when("the reference THD+N is measured with a Hann window excluding only the "
      "fundamental bin")
def step_ai_thdn_hann(context):
    context.ai_thdn = reference_thdn(context.ai_x, context.ai_rate,
                                     context.ai_f0, window="hann", exclude=0)


@when("the reference THD+N is measured without truncating to whole periods")
def step_ai_thdn_noncoherent(context):
    context.ai_thdn = reference_thdn(context.ai_x, context.ai_rate,
                                     context.ai_f0, coherent=False)


@then("the reference THD+N is at most {limit:d} dB")
def step_ai_thdn_floor(context, limit):
    assert context.ai_thdn <= limit, \
        f"reference read {context.ai_thdn:.1f} dB, expected <= {limit}"


@then("the reference THD+N is worse than {limit:d} dB")
def step_ai_thdn_worse(context, limit):
    assert context.ai_thdn > limit, \
        f"reference read {context.ai_thdn:.1f} dB, expected worse than {limit}"


@then("the reference THD+N is {want:d} dB within {tol:d} dB")
def step_ai_thdn_near(context, want, tol):
    assert abs(context.ai_thdn - want) <= tol, \
        f"reference read {context.ai_thdn:.2f} dB, expected {want} +/- {tol}"


@then("the un-windowed measurement of the SAME samples is at most {limit:d} dB")
def step_ai_thdn_same_unwindowed(context, limit):
    got = reference_thdn(context.ai_x, context.ai_rate, context.ai_f0)
    assert got <= limit, f"un-windowed read {got:.1f} dB"


@then("{rate:d} Hz with a {f0:d} Hz tone is not an integer number of samples "
      "per period")
def step_ai_incoherent_rate(context, rate, f0):
    # the arithmetic precondition itself, asserted without needing the module
    # to be runnable: 44100/1000 = 44.1 samples per period, so no truncation
    # makes the capture coherent and the un-windowed method does not apply
    assert rate % f0 != 0, f"{rate}/{f0} IS an integer - pick a rate that is not"
    context.ai_bad_rate = (rate, f0)


@then("the production THD+N analyser carries both coherence guards in its "
      "source")
def step_ai_guards_present(context):
    body = open(THDN_MODULE).read().split("def analyse(")[1].split("\ndef ")[0]
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
def step_ai_prod_refuses_rate(context):
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
def step_ai_prod_refuses_short(context):
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
    def one(ch, db, clipped=False):
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
def step_ai_gate_set(context, spec):
    context.ai_results = _results(spec.strip())


@then("the THD+N gate verdict is {want} because {why}")
def step_ai_gate(context, want, why):
    ok, msg = hthdn.verdict(context.ai_results, -120.0)
    got = "PASS" if ok else "FAIL"
    assert got == want, f"{got} ({msg}) - expected {want} because {why}"


# ------------------------------------------------------- L1 module bindings --
@then("the harness THD+N module states that it applies NO WINDOW")
def step_ai_no_window_doc(context):
    src = open(THDN_MODULE).read()
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
def step_ai_truncates(context):
    src = open(THDN_MODULE).read()
    body = src.split("def analyse(")[1]
    assert "periods = len(x) // period" in body and "n = periods * period" in body, \
        "analyse() no longer truncates the capture to whole tone periods"


@then("the harness THD+N module excludes DC and the fundamental skirt")
def step_ai_excludes(context):
    src = open(THDN_MODULE).read()
    body = src.split("def analyse(")[1]
    assert "for k in (0, k0 - 1, k0, k0 + 1)" in body, \
        "analyse() no longer zeroes DC and the fundamental's own skirt"


@then("the harness THD+N module treats a clipped capture as invalid")
def step_ai_clipped(context):
    src = open(THDN_MODULE).read()
    assert "is clipped - the measurement is invalid" in src
    ok, msg = hthdn.verdict(_results("-140 clipped"), -120.0)
    assert not ok and "clipped" in msg, (ok, msg)


# ---------------------------------------------------------- L1 plan bindings --
def _audio_plan():
    return tc.plan_audio()


@then("the campaign audio area has an identity step")
def step_ai_plan_identity(context):
    assert any("identity" in s.sid for s in _audio_plan())


@then("the campaign audio area has a per-channel-distinct pattern")
def step_ai_plan_distinct(context):
    hits = [s for s in _audio_plan()
            if s.args.get("per_channel_distinct")]
    assert hits, ("no audio step drives a per-channel-DISTINCT pattern; a "
                  "pattern that repeats a value across channels cannot fail "
                  "on a swap (methodology R4)")


@then("the campaign audio area has a THD+N step that reuses the harness "
      "analyser")
def step_ai_plan_thdn(context):
    hits = [s for s in _audio_plan() if "thdn" in s.sid]
    assert hits, "no THD+N step in the audio area"
    assert "thdn.py" in hits[0].args.get("analyser", ""), (
        "the THD+N step does not name the harness analyser - reimplementing it "
        "is how the window trap comes back")


@then("the campaign audio area has a channel-preserving loop through the peer")
def step_ai_plan_loop(context):
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
def step_ai_plan_every_talker(context):
    ok, d = tc.area_covers_every_index(tc.build_plan(), "audio")
    assert ok, (f"the AUDIO area does not walk every index: missing "
                f"{d['missing']} (covered {d['covered']}, expected "
                f"{d['expected']}).  Index 0 is the LEAST representative index "
                f"on this fabric - the 0x800 window makes it a hard alias of "
                f"the flat registers - so an index-0-only audio area tests the "
                f"alias path and nothing else.")
    context.ai_area_cov = d


@then("the campaign audio area covers more than index {n:d}")
def step_ai_plan_not_index0(context, n):
    cov = context.ai_area_cov["covered"]
    assert cov["dut_talker"] != [n], cov
    assert len(cov["dut_talker"]) > 1, cov


@then("the per-area audit reddens on an index-0-only audio area")
def step_ai_plan_audit_bites(context):
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
