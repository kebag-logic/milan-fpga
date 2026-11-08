#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_compare.py - the two-placement simulation's comparison (#665).

It reads the capture each half wrote (twin_fabric.cpp, twin_split.cpp: every
control frame its MAC sent, with the modeled millisecond it left at) and
compares them by the contract of the plan's section S6 as #665
issuecomment-6716584453 amends it:

  * ADP, ACMP, MAAP and AECP: each protocol's frames as an ordered sequence,
    raw bytes equal. Times are never compared between the halves.
  * AECP: equal apart from the F5 difference ledger (LEDGER below,
    sw/firmware/ctrl/aecp/README.md); each row asserts its exact fabric and
    split values, and a row that does not hold is a finding.
  * SRP: MSRP's decoded multiset per transmit opportunity, in order across
    opportunities, through sw/firmware/ctrl/test/srp_wire_compare.py; MVRP,
    whose MRPDU that decoder does not read, as an ordered raw-byte sequence.
  * Timing: what a standard leaves random or bounded is graded against that
    bound in each half on its own (TIMING below).

Both halves are compared as the wire carries them: a frame shorter than 60
bytes is padded with zeros to 60, as the SoC's MAC pads it (LiteEthMACCore
with_padding, sw/litex/milan_soc.py; IEEE 802.3-2018 3.2.7). An ADP or MAAP
frame one half sent past the other's last is not a difference when the other
half's next one was not yet due at the run's end (its bound, TAIL_MS).

  twin_compare.py FABRIC.json SPLIT.json [--report OUT.json] [--report-only]
      every finding as "[DIFF] ..." or "[TIME] ...", exit 1 on any (0 with
      --report-only, which only writes the plants' baseline)
  twin_compare.py FABRIC.json SPLIT.json --plant NAME --baseline BASE.json
      the split capture was planted (twin_split.cpp --plant NAME): exit 0 only
      when the comparison refuses it with the plant's words (PLANT_WORDS), in a
      finding the unplanted comparison (BASE.json, a --report) does not make
  twin_compare.py SPLIT.json PLANTED.json --plant NAME --self
      the control: the split capture against its planted copy, which must
      differ by exactly the plant's finding
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "sw/firmware/ctrl/test"))
import srp_wire_compare  # noqa: E402

MIN_FRAME = 60
AVTP = 0x22F0
SUBTYPES = {0xFA: "ADP", 0xFB: "AECP", 0xFC: "ACMP", 0xFE: "MAAP"}
ETHERTYPES = {0x22EA: "MSRP", 0x88F5: "MVRP"}
#: a periodic frame's latest next departure, for the tail rule: ADP's
#: advertise period and largest delay (Milan v1.2 Table 5.50), MAAP's
#: announce interval and its variation (IEEE 1722-2016 Table B.8)
TAIL_MS = {"ADP": 5000 + 4000, "MAAP": 30000 + 2000}
#: each plant's words (twin_split.cpp --plant), which its refusal must carry
PLANT_WORDS = {
    "byte-flip": "ADP frame 1 differs at byte 34",
    "srp-plus-k": "declares stream_id 0200000000010001",
    "missing-notification": "the fabric sent and the split did not: AECP AEM_RESPONSE u=1 GET_STREAM_INFO",
}
PLANTED_PROTOCOL = {"byte-flip": "ADP", "srp-plus-k": "MSRP", "missing-notification": "AECP"}


@dataclass(frozen=True)
class Sent:
    """One control frame: the millisecond it left at, its padded bytes and where its protocol PDU starts."""

    ms: int
    data: bytes
    at: int


@dataclass
class Capture:
    """One half's capture, its frames grouped by protocol in the order its MAC sent them."""

    placement: str
    run_ms: int
    notes: dict
    applied: list
    frames: dict[str, list[Sent]]


def classify(data: bytes) -> tuple[str, int] | None:
    """The protocol of a control frame and its PDU's offset, past an optional C-tag."""
    at = 12
    kind = int.from_bytes(data[at:at + 2], "big")
    if kind == 0x8100:
        at += 4
        kind = int.from_bytes(data[at:at + 2], "big")
    at += 2
    if kind in ETHERTYPES:
        return ETHERTYPES[kind], at
    if kind == AVTP and at < len(data) and data[at] in SUBTYPES:
        return SUBTYPES[data[at]], at
    return None


def load(path: Path) -> Capture:
    """Read a capture; every frame padded as the MAC pads it."""
    doc = json.loads(path.read_text())
    frames: dict[str, list[Sent]] = {}
    for entry in doc["frames"]:
        data = bytes.fromhex(entry["hex"])
        found = classify(data)
        if found is None:
            raise SystemExit(f"{path}: a frame of no compared protocol at ms {entry['ms']}")
        frames.setdefault(found[0], []).append(Sent(entry["ms"], data.ljust(MIN_FRAME, b"\0"), found[1]))
    return Capture(doc["placement"], doc["run_ms"], doc["notes"], doc["applied"], frames)


# ---- AECP's fields (IEEE 1722.1-2021 Figure 9-1, 9.2.1.2) ------------------

AEM_COMMANDS = {0x0004: "READ_DESCRIPTOR", 0x0008: "SET_STREAM_FORMAT", 0x0009: "GET_STREAM_FORMAT",
                0x000E: "SET_STREAM_INFO", 0x000F: "GET_STREAM_INFO", 0x0022: "START_STREAMING",
                0x0023: "STOP_STREAMING", 0x0024: "REGISTER_UNSOLICITED_NOTIFICATION", 0x0029: "GET_COUNTERS"}


@dataclass(frozen=True)
class Aecp:
    """The fields of one AECPDU the comparison names."""

    message_type: int
    status: int
    seq: int
    unsolicited: bool
    command: int
    descriptor: tuple[int, int]


def aecp(s: Sent) -> Aecp:
    """Decode the AECPDU at s.at."""
    d, at = s.data, s.at
    command = int.from_bytes(d[at + 22:at + 24], "big")
    return Aecp(d[at + 1] & 0x0F, d[at + 2] >> 3, int.from_bytes(d[at + 20:at + 22], "big"),
                bool(command & 0x8000), command & 0x7FFF,
                (int.from_bytes(d[at + 24:at + 26], "big"), int.from_bytes(d[at + 26:at + 28], "big")))


def describe(proto: str, s: Sent) -> str:
    """A frame as a finding names it."""
    if proto != "AECP":
        return f"{proto} message_type {s.data[s.at + 1] & 0x0F} at ms {s.ms}"
    f = aecp(s)
    if f.message_type != 1:
        return f"AECP message_type {f.message_type} status {f.status} sequence_id {f.seq} at ms {s.ms}"
    name = AEM_COMMANDS.get(f.command, f"command {f.command:#06x}")
    return (f"AECP AEM_RESPONSE u={int(f.unsolicited)} {name} descriptor {f.descriptor[0]:#06x}/"
            f"{f.descriptor[1]} status {f.status} sequence_id {f.seq} at ms {s.ms}")


def key(proto: str, s: Sent) -> tuple:
    """What two frames must share to be paired: the message, and for AECP its command and descriptor."""
    if proto != "AECP":
        return (s.data[s.at + 1] & 0x0F,)
    f = aecp(s)
    return (f.message_type, f.unsolicited, f.command, f.descriptor)


# ---- the F5 difference ledger -----------------------------------------------

@dataclass(frozen=True)
class Row:
    """One ledger row: the command it covers (by the stimulus's sequence_id), its clause, and its exact values."""

    name: str
    clause: str
    seq: int
    fabric: Callable[[list[Sent]], bool]
    split: Callable[[list[Sent]], bool]
    fabric_says: str
    split_says: str


def responses(frames: list[Sent], seq: int) -> list[Aecp]:
    """The solicited responses carrying one command's sequence_id."""
    return [f for f in map(aecp, frames) if f.seq == seq and not f.unsolicited]


#: SET_STREAM_INFO's response fields past its descriptor pair (IEEE 1722.1-2021 7.4.15.2): flags first
STREAM_INFO_FIELDS = slice(28, 28 + 80)


def stream_info_fields(frames: list[Sent], seq: int) -> list[bytes]:
    """The fields of each solicited response with that sequence_id."""
    return [s.data[s.at + STREAM_INFO_FIELDS.start:s.at + STREAM_INFO_FIELDS.stop] for s in frames
            if aecp(s).seq == seq and not aecp(s).unsolicited]


def current_stream_info(frames: list[Sent], descriptor: tuple[int, int]) -> bytes | None:
    """The fields of the last GET_STREAM_INFO notification for a descriptor: its current stream info."""
    found = [s for s in frames if aecp(s).command == 0x000F and aecp(s).descriptor == descriptor]
    return found[-1].data[found[-1].at + STREAM_INFO_FIELDS.start:found[-1].at + STREAM_INFO_FIELDS.stop] \
        if found else None


def holds_current(frames: list[Sent], seq: int, descriptor: tuple[int, int]) -> bool:
    """One response, whose fields are the descriptor's current stream info: its last notice's fields (the
    notice's shorter length), then zero."""
    fields, current = stream_info_fields(frames, seq), current_stream_info(frames, descriptor)
    return current is not None and len(fields) == 1 and fields[0][:len(current)] == current \
        and not any(fields[0][len(current):])


#: The rows this stimulus exercises (twin.hpp's sequence_ids 11, 12 and 14);
#: README rows it does not exercise are named in the milan_dp README.
LEDGER = (
    Row("root-configuration-index", "IEEE 1722.1-2021 7.4.5.1/2 (aecp/README.md, Observed difference row 1)", 11,
        lambda fr: [(x.status, x.descriptor) for x in responses(fr, 11)] == [(7, (1, 0))],
        lambda fr: [(x.status, x.descriptor) for x in responses(fr, 11)] == [(0, (0, 0))],
        "one response, BAD_ARGUMENTS, the received configuration_index 1",
        "one response, SUCCESS, the ENTITY descriptor at configuration_index 0"),
    Row("set-stream-info-current-fields", "IEEE 1722.1-2021 7.4.15.1 (aecp/README.md, Observed difference row 2)",
        12,
        lambda fr: [x.status for x in responses(fr, 12)] == [11] and stream_info_fields(fr, 12) == [bytes(80)],
        lambda fr: [x.status for x in responses(fr, 12)] == [11] and holds_current(fr, 12, (5, 0)),
        "one response, NOT_SUPPORTED, the command's fields echoed (all zero)",
        "one response, NOT_SUPPORTED, STREAM_INPUT 0's current fields (its last GET_STREAM_INFO notice's)"),
    Row("reserved-message-type", "IEEE 1722.1-2021 Table 9-1, 9.2.2.4 (aecp/README.md, Non-AEM contract)", 14,
        lambda fr: [(x.message_type, x.status) for x in responses(fr, 14)] == [(11, 1)],
        lambda fr: responses(fr, 14) == [],
        "one frame, message_type 11, status 1",
        "nothing"),
)


def apply_ledger(fab: list[Sent], spl: list[Sent]) -> tuple[list[Sent], list[Sent], list[str], list[str]]:
    """Each row's frames out of both sequences, each row checked; the remaining sequences, notes and findings."""
    notes: list[str] = []
    findings: list[str] = []
    for row in LEDGER:
        f, s = responses(fab, row.seq), responses(spl, row.seq)
        if row.fabric(fab) and row.split(spl):
            notes.append(f"[LEDGER] {row.name}: the fabric sends {row.fabric_says}, the split {row.split_says} "
                         f"({row.clause})")
        else:
            findings.append(f"[DIFF] AECP ledger row {row.name} does not hold: the fabric sent "
                            f"{[(x.message_type, x.status, x.descriptor) for x in f]} (the row: {row.fabric_says}), "
                            f"the split {[(x.message_type, x.status, x.descriptor) for x in s]} "
                            f"(the row: {row.split_says})")
        covered = {row.seq}
        fab = [x for x in fab if aecp(x).seq not in covered or aecp(x).unsolicited]
        spl = [x for x in spl if aecp(x).seq not in covered or aecp(x).unsolicited]
    return fab, spl, notes, findings


# ---- the ordered raw-byte comparison ---------------------------------------

def first_byte(a: bytes, b: bytes) -> int:
    """The first byte two frames differ at (the shorter one's length when one is a prefix)."""
    return next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))


def tail_allowed(proto: str, extra: list[Sent], other: list[Sent], run_ms: int) -> bool:
    """Unpaired trailing frames of a periodic protocol, the other half's next not yet due at the run's end."""
    if proto not in TAIL_MS or not other:
        return False
    return run_ms - other[-1].ms < TAIL_MS[proto] and extra[0].ms > other[-1].ms


def compare_ordered(proto: str, fab: list[Sent], spl: list[Sent], run_ms: int) -> tuple[list[str], list[str]]:
    """Pair the two sequences in order by key, then compare each pair's bytes; findings and notes."""
    findings: list[str] = []
    notes: list[str] = []
    matcher = difflib.SequenceMatcher(None, [key(proto, x) for x in fab], [key(proto, x) for x in spl],
                                      autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                if fab[i].data != spl[j].data:
                    at = first_byte(fab[i].data, spl[j].data)
                    findings.append(f"[DIFF] {proto} frame {i} differs at byte {at} (fabric "
                                    f"{fab[i].data[at:at + 8].hex()}, split {spl[j].data[at:at + 8].hex()}): "
                                    f"{describe(proto, fab[i])}")
            continue
        last = i2 == len(fab) and j2 == len(spl)
        if last and j1 == j2 and tail_allowed(proto, fab[i1:i2], spl, run_ms):
            notes.append(f"[TAIL] {proto}: the fabric's last {i2 - i1} frame(s), the split's next not yet due")
        elif last and i1 == i2 and tail_allowed(proto, spl[j1:j2], fab, run_ms):
            notes.append(f"[TAIL] {proto}: the split's last {j2 - j1} frame(s), the fabric's next not yet due")
        else:
            findings += [f"[DIFF] the fabric sent and the split did not: {describe(proto, x)}" for x in fab[i1:i2]]
            findings += [f"[DIFF] the split sent and the fabric did not: {describe(proto, x)}" for x in spl[j1:j2]]
    return findings, notes


# ---- SRP --------------------------------------------------------------------

def compare_msrp(fab: list[Sent], spl: list[Sent]) -> list[str]:
    """Each transmit opportunity's decoded multiset, in order across opportunities (srp_wire_compare.py)."""
    findings: list[str] = []
    for k, (a, b) in enumerate(zip(fab, spl)):
        ca = srp_wire_compare.canonical_opportunity([unpad_mrp(a.data)])
        cb = srp_wire_compare.canonical_opportunity([unpad_mrp(b.data)])
        if ca == cb:
            continue
        only_f = [e for e in ca["events"] if e not in cb["events"]]
        only_s = [e for e in cb["events"] if e not in ca["events"]]
        findings.append(f"[DIFF] MSRP opportunity {k} (ms {a.ms} and {b.ms}): the decoded multisets differ; "
                        f"fabric only {declared(only_f)}, split only {declared(only_s)}, LeaveAll fabric "
                        f"{ca['leave_all_types']} split {cb['leave_all_types']}")
    if len(fab) != len(spl):
        findings.append(f"[DIFF] MSRP: the fabric sent {len(fab)} transmit opportunities, the split {len(spl)}")
    return findings


def declared(evs: list) -> str:
    """Decoded events as a finding names them: AttributeType, the declaration it declares, its event."""
    return "[" + "; ".join(f"type {e[0]} declares stream_id {e[1][:16]} event {e[3]}" if e[0] in (1, 2, 3)
                           else f"type {e[0]} value {e[1]} event {e[3]}" for e in evs) + "]"


def unpad_mrp(data: bytes) -> bytes:
    """The MSRP frame up to its PDU EndMark (IEEE 802.1Q-2018 10.8.1.2), the MAC's pad dropped: each message
    is AttributeType, AttributeLength and AttributeListLength, then that many bytes. A frame that never
    reaches its EndMark is returned whole, for srp_wire_compare.py's decoder to refuse by name."""
    offset = 15
    while offset + 4 <= len(data) and data[offset:offset + 2] != b"\0\0":
        offset += 4 + int.from_bytes(data[offset + 2:offset + 4], "big")
    return data[:offset + 2] if offset + 2 <= len(data) else data


# ---- timing, each half against its bound ------------------------------------

def gaps(frames: list[Sent]) -> list[int]:
    """The milliseconds between consecutive frames."""
    return [b.ms - a.ms for a, b in zip(frames, frames[1:])]


def grade_adp(cap: Capture) -> tuple[list[str], dict]:
    """ADP's start delay, advertise interval and DISCOVER answer (Milan v1.2 5.6.3.5, Table 5.50; IEEE
    1722.1-2021 6.2.2.6 valid_time)."""
    adp = [x for x in cap.frames.get("ADP", []) if x.data[x.at + 1] & 0x0F == 0]
    boot = int(cap.notes.get("boot_ms", 0))
    found: list[str] = []
    if not adp:
        return [f"[TIME] {cap.placement} ADP: no ENTITY_AVAILABLE"], {}
    valid_ms = (adp[0].data[adp[0].at + 2] >> 3) * 2000
    if adp[0].ms - boot > 2000:
        found.append(f"[TIME] {cap.placement} ADP: the first ENTITY_AVAILABLE {adp[0].ms - boot} ms after the "
                     "entity started, past Milan v1.2 5.6.3.5.2's 2000 ms")
    found += [f"[TIME] {cap.placement} ADP: {g} ms between ENTITY_AVAILABLEs, past Milan v1.2 Table 5.50's "
              f"9000 ms or valid_time's {valid_ms} ms" for g in gaps(adp) if g > 9000 or g >= valid_ms]
    asked = [a["ms"] for a in cap.applied if a["what"].startswith("ADP ENTITY_DISCOVER")]
    for t in asked:
        answer = next((x.ms for x in adp if x.ms >= t), None)
        if answer is None or answer - t > 4000:
            found.append(f"[TIME] {cap.placement} ADP: the ENTITY_DISCOVER at ms {t} answered at {answer}, "
                         "past Milan v1.2 5.6.3.5.3's 4000 ms")
    return found, {"adp_start_ms": adp[0].ms - boot, "adp_gaps_ms": gaps(adp), "adp_valid_time_ms": valid_ms}


def grade_maap(cap: Capture) -> tuple[list[str], dict]:
    """MAAP's probe and announce intervals (IEEE 1722-2016 Table B.8)."""
    maap = cap.frames.get("MAAP", [])
    probes = [x for x in maap if x.data[x.at + 1] & 0x0F == 1]
    announces = [x for x in maap if x.data[x.at + 1] & 0x0F == 3]
    found = [f"[TIME] {cap.placement} MAAP: {g} ms between PROBEs, outside MAAP_PROBE_INTERVAL_BASE 500 + "
             "VARIATION 100" for g in gaps(probes) if not 500 <= g <= 600]
    found += [f"[TIME] {cap.placement} MAAP: {g} ms between ANNOUNCEs, outside MAAP_ANNOUNCE_INTERVAL_BASE "
              "30000 + VARIATION 2000" for g in gaps(announces) if not 30000 <= g <= 32000]
    return found, {"maap_probe_gaps_ms": gaps(probes), "maap_announce_gaps_ms": gaps(announces)}


def grade_aecp(cap: Capture) -> tuple[list[str], dict]:
    """Each AEM command's response within 240 ms (IEEE 1722.1-2021 9.3.2.6, as aecp.h cites it)."""
    asked = {k + 1: a["ms"] for k, a in enumerate(x for x in cap.applied if x["what"].startswith("AECP"))}
    took = {}
    for s in cap.frames.get("AECP", []):
        f = aecp(s)
        if not f.unsolicited and f.seq in asked and f.seq not in took:
            took[f.seq] = s.ms - asked[f.seq]
    found = [f"[TIME] {cap.placement} AECP: sequence_id {q} answered after {t} ms, past 240 ms"
             for q, t in took.items() if t > 240]
    return found, {"aecp_response_ms": took}


def grade(cap: Capture) -> tuple[list[str], dict]:
    """Every timing grade of one half."""
    found: list[str] = []
    measured: dict = {}
    for grader in (grade_adp, grade_maap, grade_aecp):
        f, m = grader(cap)
        found += f
        measured.update(m)
    return found, measured


# ---- the verdict --------------------------------------------------------------

#: SRP's two protocols repeat one difference at every transmit opportunity, so
#: their findings are listed to this many, then counted; every other
#: protocol's are listed whole
SRP_LISTED = 3


def capped(proto: str, findings: list[str]) -> list[str]:
    """An SRP protocol's first findings and the count of the rest; any other protocol's, whole."""
    if proto not in ("MSRP", "MVRP") or len(findings) <= SRP_LISTED:
        return findings
    return findings[:SRP_LISTED] + [f"[DIFF] {proto}: {len(findings) - SRP_LISTED} more difference(s), "
                                    "the first listed above"]

def compare(fab: Capture, spl: Capture, between_placements: bool = True) -> dict:
    """Every finding and note of the two captures. The ledger and the timing grades are the two placements'
    comparison's; the plants' control compares the split half with its own planted copy."""
    findings: list[str] = []
    notes: list[str] = []
    run_ms = min(fab.run_ms, spl.run_ms)
    for proto in ("ADP", "ACMP", "MAAP", "AECP", "MVRP"):
        f, s = fab.frames.get(proto, []), spl.frames.get(proto, [])
        if proto == "AECP" and between_placements:
            f, s, n, d = apply_ledger(f, s)
            notes += n
            findings += d
        d, n = compare_ordered(proto, f, s, run_ms)
        findings += capped(proto, d)
        notes += n
    findings += capped("MSRP", compare_msrp(fab.frames.get("MSRP", []), spl.frames.get("MSRP", [])))
    measured = {}
    if between_placements:
        for cap in (fab, spl):
            f, m = grade(cap)
            findings += f
            measured[cap.placement] = m
    return {"findings": findings, "notes": notes, "measured": measured,
            "counts": {c.placement: {p: len(v) for p, v in sorted(c.frames.items())} for c in (fab, spl)}}


def plant_verdict(report: dict, name: str, baseline: list[str] | None) -> int:
    """0 when the plant is refused by its words, in a finding the baseline does not make (or, for --self, with
    every finding about the planted protocol: a frame dropped between two of one key reads as a pair that
    differs and one missing)."""
    words = PLANT_WORDS[name]
    hits = [f for f in report["findings"] if words in f]
    if baseline is None:
        ok = bool(hits) and all(PLANTED_PROTOCOL[name] in f for f in report["findings"])
    else:
        ok = any(h not in baseline for h in hits)
    print(f"plant {name}: {'REFUSED' if ok else 'ESCAPED'} by \"{words}\"")
    return 0 if ok else 1


def main() -> int:
    """Compare two captures, or grade a plant."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("fabric", type=Path)
    parser.add_argument("split", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--plant", choices=sorted(PLANT_WORDS))
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--self", dest="self_control", action="store_true")
    parser.add_argument("--report-only", action="store_true",
                        help="write the report and exit 0: the plants' baseline, whose verdict is make twin's")
    args = parser.parse_args()
    fab, spl = load(args.fabric), load(args.split)
    report = compare(fab, spl, between_placements=not args.self_control)
    for line in report["notes"] + report["findings"]:
        print(line)
    if args.report:
        args.report.write_text(json.dumps(report, indent=1) + "\n")
    if args.plant:
        base = None if args.self_control else json.loads(args.baseline.read_text())["findings"]
        return plant_verdict(report, args.plant, base)
    print(f"twin: {len(report['findings'])} finding(s); counts {report['counts']}")
    return 1 if report["findings"] and not args.report_only else 0


if __name__ == "__main__":
    sys.exit(main())
