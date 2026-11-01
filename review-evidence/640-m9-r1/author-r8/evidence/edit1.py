"""Round 8's exact-text edits; each old text must match once."""
import sys
R = "$LANES/640-mark2-charter/"
D = "https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030"
E = "https://github.com/kebag-logic/milan-fpga/blob/b61b3b8bc172e5688c3c6799a85790dde144403d/review-evidence/640-m9-r1/reviews/R757-7"

def edit(page, pairs):
    p = R + page
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit(f"{page}: expected one match, got {n}: {old[:80]!r}")
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)

edit("docs/reference/FR_NFR.md", [
    ("It does not show it for mixed channel counts (up to 95.867 µs at 48 kHz) or for [fewer reservations](../design/MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port) (123.337 µs with three co-phased eight-channel streams). Those derived bounds are accepted and published, and no connection is refused because of them. Verified by analysis",
     "It does not show it for mixed channel counts (up to 95.867 µs at 48 kHz). Those 16-reservation bounds are accepted and published. With [fewer reservations](../design/MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port) no maximum is derived, and the stream-engine lane [owes that derivation](../design/MARK_II_STREAM_ENGINES.md#open-design-items). The largest figure reached there is 143.347 µs, with six co-phased one-channel streams at 48 kHz; it is quoted as reached, not as a limit. No connection is refused because of any of these figures. Verified by analysis"),
    ("The bench measures against the target and reports each case; a case above 65 µs that stays inside its published bound is not a failure.",
     "The bench measures every case against the target and reports it; a case above 65 µs is reported, not failed. A case is graded against a bound only where one is derived, which is the 16-reservation table; there, a measurement above its bound contradicts the analysis and is a finding."),
])

edit("docs/design/MARK_II_STREAM_ENGINES.md", [
    ("""Derived bounds for mixed formats and fewer reservations are accepted.
They stay published below.

No connection is refused because of them.
No restriction to one base format applies.
""", """The derived bounds at 16 reservations are accepted.
They stay published below.

With fewer reservations no maximum is derived.
[Open design item 4](#open-design-items) owes it.

The bench measures every case against the target.
A case above 65 µs is reported, not failed.

A case is graded only against a derived bound.
A measurement above one contradicts the analysis: a finding.

No connection is refused because of these figures.
No restriction to one base format applies.
"""),
    ("""Alone, k co-phased streams wait about `(k - 1) x 125 / k` µs.

""", f"""Alone, k co-phased equal frames wait about `(k - 1) x 125 / k` µs.

That form gives no largest k.
It does not cover unequal frames.

These cases are also reached under the exact phase rule.
Each row names starts and stops that reach it.

| Rate | Running streams, no CRF | Reached by | Last frame's shaper wait | Total, with every fixed term | Against 65 µs |
|---|---|---|---:|---:|---|
| 48 kHz | Six one-channel in phase 0 | Start one one-channel, five eight-channel, two one-channel, five eight-channel, three one-channel; stop every eight-channel | 103.022 µs | 143.347 µs reached | Not met |
| 48 kHz | Eight-channel in phase 0, one-channel in phase 1 | Start one eight-channel, then two one-channel; stop the one in phase 3 | 71.310 µs | 111.635 µs reached | Not met |
| 96 kHz | Four one-channel in phase 0 | Start one one-channel, eleven eight-channel, three one-channel; stop every eight-channel | 92.935 µs | 125.426 µs reached | Not met |
| 192 kHz | Six-channel in phase 9, one-channel in phase 12 | Start five one-channel, then one six-channel; stop the one-channel streams in phases 0, 3, 6 and 18 | 83.941 µs | At least 102.034 µs reached, before the packetizer term | Not met |

The rows of both tables are examples.
None is a maximum.

Totals use the page's fixed terms, estimates included.
Nothing here is a measurement.

At 96 kHz those terms are 32.491 µs.
At 192 kHz they are 18.093 µs, without the packetizer.

The reviewer's [published probe]({E}/scripts/probe_fewer_bound.py) sampled these cases.
[Its output]({E}/receipts/model/probe_fewer_bound.out) lists them.

Its 192 kHz search left out eight-channel streams.
So that row may be low.

"""),
    ("That is the probe's result, not a design figure |\n",
     "That is the probe's result, not a design figure |\n"
     "| 4. Fewer-reservations maximum | With fewer than 16 reservations on a port, no maximum talker latency is derived. The lane derives it with the model at 48, 96 and 192 kHz, over every placement that starts and stops reach and every base format, with and without a CRF, eight-channel at 192 kHz included. The lane then cites it in NFR-LAT-03 | The model states whether its search is exact or bounds a superset, as the 16-reservation table does. The test fails if any case in the [fewer-reservations tables](#fewer-reservations-on-a-port) exceeds the result, in the queue recursion or the 8.6.8.2 simulation. Bench: the latency taps at the largest placement, against the result |\n"),
])

edit("docs/design/MARK_II_AREA_PLAN.md", [
    (f"not met with mixed formats or with [fewer reservations](MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port), whose bounds the [owner accepted]({D}) |",
     f"not met with mixed formats, whose derived bounds the [owner accepted]({D}); not met with [fewer reservations](MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port), where no maximum is derived and 143.347 µs is reached, not a limit |"),
    ("exceeded by mixed formats and by [fewer reservations](MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port); those bounds are accepted and published, and no connection is refused because of them |",
     "exceeded by mixed formats, whose derived bounds are accepted and published; exceeded by [fewer reservations](MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port), where no maximum is derived and 143.347 µs is reached, not a limit; no connection is refused because of these figures |"),
    ("| +2.75k | 65 µs taps on all talker streams; cable pulls;",
     "| +2.75k | Talker latency taps on all talker streams, measured against the 65 µs target; cable pulls;"),
])
