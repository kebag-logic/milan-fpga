"""Round 7, commit 1: the 2026-11-01 owner decision. Each replacement must match exactly once."""
import sys
R = "$LANES/640-mark2-charter/docs/"
D = "https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030"

def edit(page, pairs):
    p = R + page
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit(f"{page}: expected one match, got {n}: {old[:80]!r}")
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)

edit("reference/FR_NFR.md", [
 ("to the first bit of its frame on the wire MUST be below 65 µs, and as short as possible (",
  "to the first bit of its frame on the wire SHOULD be below 65 µs, and as short as possible ("),
 ("2026-10-31; the owner called 65 µs the ideal target). The interval covers",
  f"2026-10-31; the owner called 65 µs the ideal target; the [owner decision of 2026-11-01]({D}) makes 65 µs a target that does not bind every legal stream setup). The interval covers"),
 ("(123.337 µs with three co-phased eight-channel streams): for those this requirement is not met by the design, and the reading is an open owner question there. Verified by",
  "(123.337 µs with three co-phased eight-channel streams). Those derived bounds are accepted and published, and no connection is refused because of them. Verified by"),
 ("on every talker stream, on the bench, at 32x32, with one format and with mixed formats per port. | M | A,T |",
  "on every talker stream, on the bench, at 32x32, with one format and with mixed formats per port. The bench measures against the target and reports each case; a case above 65 µs that stays inside its published bound is not a failure. | S | A,T |"),
])

edit("design/MARK_II_STREAM_ENGINES.md", [
 (") sets 65 µs for every talker stream.\n", ") sets a 65 µs target for every talker stream.\n"),
 ("called that target ideal on 2026-10-31.\n\nA CRF stream",
  "called that target ideal on 2026-10-31.\n\n"
  f"The [owner decided]({D}) on 2026-11-01 that 65 µs is a target.\n"
  "It does not bind every legal stream setup.\n\n"
  "Derived bounds for mixed formats and fewer reservations are accepted.\n"
  "They stay published below.\n\n"
  "No connection is refused because of them.\n"
  "No restriction to one base format applies.\n\n"
  "A CRF stream"),
 ("Mixed formats do not; the [open questions](#open-questions) list it.\n",
  "Mixed formats do not; the [owner's decision](#talker-latency-budget) accepts their bounds.\n"),
 ("""1. **Talker latency with mixed formats or fewer reservations.**
   - At 16 mixed reservations, every rate exceeds 65 µs.
   - At 48 kHz a reached mix needs 92.530 µs.
   - No 16-stream 48 kHz mix exceeds 95.867 µs.
   - Three co-phased streams alone wait 83.012 µs for credit.
   - The owner called 65 µs ideal; the choices include these:
     - accept the derived bounds for those cases;
     - restrict each port to one base format;
     - re-phase a running stream, accepting an audio gap;
     - change the stagger or shape decision.
2. **Save bursts.**""", "1. **Save bursts.**"),
 ("3. **Block RAM.**\n", "2. **Block RAM.**\n"),
 ("4. **Debounce windows.**\n", "3. **Debounce windows.**\n"),
 ("5. **gPTP on two ports.**\n", "4. **gPTP on two ports.**\n"),
 ("6. **Commit timeout.**\n", "5. **Commit timeout.**\n"),
 ("7. **Engine headroom at 192 kHz.**\n", "6. **Engine headroom at 192 kHz.**\n"),
])

edit("design/MARK_II_AREA_PLAN.md", [
 ("| Talker latency | Below 65 µs for every talker stream ([NFR-LAT-03](../reference/FR_NFR.md#31-performance--real-time)); derived as met with one base format at 16 reservations per port; not met with mixed formats or with [fewer reservations](MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port) ([open](MARK_II_STREAM_ENGINES.md#open-questions)) |",
  f"| Talker latency | Target: below 65 µs for every talker stream, as short as possible ([NFR-LAT-03](../reference/FR_NFR.md#31-performance--real-time)); derived as met with one base format at 16 reservations per port; not met with mixed formats or with [fewer reservations](MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port), whose bounds the [owner accepted]({D}) |"),
 ("as fast as possible, ideally below 65 µs | NFR-LAT-03; met with one base format at 16 reservations per port; exceeded by mixed formats and by [fewer reservations](MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port); an open owner question |",
  f"as fast as possible, ideally below 65 µs; [owner, 2026-11-01]({D}): 65 µs is a target | NFR-LAT-03; met with one base format at 16 reservations per port; exceeded by mixed formats and by [fewer reservations](MARK_II_STREAM_ENGINES.md#fewer-reservations-on-a-port); those bounds are accepted and published, and no connection is refused because of them |"),
])
