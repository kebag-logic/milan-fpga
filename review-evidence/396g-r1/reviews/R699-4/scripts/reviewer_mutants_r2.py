#!/usr/bin/env python3
"""Round-2 reviewer mutants for the #396 planner, ported to the new head.

Usage: python3 -I reviewer_mutants_r2.py <pristine export root> <work dir> [jobs]

Uses the round-1 driver (reviewer_mutants.py, beside this file) unchanged:
each mutant is one exact single-occurrence replacement in
tb/tools/torture_campaign.py; KILLED means the planner self-test or the plan
feature returned nonzero. The round-1 survivors G07, G12 and R03 are restated
against the new code; N01-N30 attack each round-2 item.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reviewer_mutants as rm  # noqa: E402

rm.MUTANTS = [
    ("G07 capture loss needs only one channel",
     'if sorted({e["channel"] for e in hits}) != counter_channels:', 'if not hits:'),
    ("G12 swap run extended across a partner change",
     'if (run is not None and run["class"] == cls and run.get("partner") == partner',
     'if (run is not None and run["class"] == cls'),
    ("R03 soft reset graded as a commit cut",
     '    if phase == "journal_commit":\n        return _release_commit_restored(',
     '    if phase == "journal_commit" or committed is not None:\n        return _release_commit_restored('),
    ("G08 arm tolerance widened by 100", "    return first - tolerance <= index <= last + tolerance",
     "    return first - tolerance <= index <= last + tolerance + 100"),
    ("G09 fast path compares one frame",
     "and column.tobytes() == _audio_expected_bytes(slot.tag, slot.position, count)):",
     "and column[:1].tobytes() == _audio_expected_bytes(slot.tag, slot.position, 1)):"),
    ("N01 pending-default guard removed", "    if pending_at_default:\n", "    if False:\n"),
    ("N02 cut window not checked", "    if not window[0] <= cut.cut_s < window[1]:\n", "    if False:\n"),
    ("N03 cut window closed at its end", "    if not window[0] <= cut.cut_s < window[1]:\n",
     "    if not window[0] <= cut.cut_s <= window[1]:\n"),
    ("N04 bare pending dict may pass",
     "    if refusal:\n        return \"NOT RUN\", dict(detail, restored=restored, why=refusal)",
     "    if refusal and cut is not None:\n        return \"NOT RUN\", dict(detail, restored=restored, why=refusal)"),
    ("N05 planted window only has to meet the read interval",
     'if event["window_s"][0] <= interval[0] and interval[1] <= event["window_s"][1]]',
     'if event["window_s"][0] <= interval[1] and interval[0] <= event["window_s"][1]]'),
    ("N06 losses do not advance the acquisition index",
     "        return index + sum(frames for at, frames in lost if at <= index)",
     "        return index"),
    ("N07 a loss at the event's own index not counted",
     "        return index + sum(frames for at, frames in lost if at <= index)",
     "        return index + sum(frames for at, frames in lost if at < index)"),
    ("N08 gPTP interpolated across a recorded step",
     "            elif any(here[1] < step <= there[1] for step in layout.gptp_steps_wall_s):",
     "            elif False:"),
    ("N09 times taken from the last anchor past it",
     "        if here[0] == index:\n            wall, gptp, timing = here[1], here[2], \"anchored\"",
     "        if here[0] == index or there is None:\n            wall, gptp, timing = here[1], here[2], \"anchored\""),
    ("N10 swap without reciprocity", "                return other if exchanged else None", "                return other"),
    ("N12 arm channel not followed through a swap", "        return found or [channel]", "        return [channel]"),
    ("N13 neighbour-duplicate rule removed",
     '        if span[0][0] == "bad" or _audio_duplicate(track, labels, k):',
     '        if span[0][0] == "bad":'),
    ("N14 burst one-mask rule removed",
     "    elif len({label[2] ^ _audio_due(track, label[1], current) for label in span}) > 1:",
     "    elif True:"),
    ("N15 located_within never reported", '    if first < index:\n        event["located_within"]',
     '    if False:\n        event["located_within"]'),
    ("N16 edges widened to halves", "AUDIO_ARM_EDGE_DIVISOR = 10", "AUDIO_ARM_EDGE_DIVISOR = 2"),
    ("N17 block code bit always zero",
     "    bit = (_audio_code(block) >> (offset % AUDIO_CODE_BITS)) & 1", "    bit = 0"),
    ("N19 unresolved flag dropped", '            if event["class"] in ("dropped", "repeated"):\n                event["unresolved"] = track.reason',
     '            if False:\n                event["unresolved"] = track.reason'),
    ("N20 static exchange graded as bit-flip", "                    if exchanged:\n", "                    if False:\n"),
    ("N21 loss size not checked", ' and e["n"] == loss["frames"] and _audio_at(e, loss["index"], 0)]',
     ' and _audio_at(e, loss["index"], 0)]'),
    ("N23 matches_channel never set", "        if len(matches) == 1 and None not in matches:", "        if False:"),
    ("N24 interpolation over stored frames",
     "            part = (acquired(index) - acquired(here[0])) / (acquired(there[0]) - acquired(here[0]))",
     "            part = (index - here[0]) / (there[0] - here[0])"),
    ("N25 inserted silence does not delay the track",
     "            current = current - extra if inserted else current", "            current = current"),
    ("N26 one planted event excuses many unlocks",
     "            for event in matches[:delta]:\n                unused.remove(event)",
     "            for event in matches[:0]:\n                unused.remove(event)"),
    ("N29 slips folded modulo one block", "    half = AUDIO_PERIOD_FRAMES // 2\n",
     "    half = AUDIO_BLOCK_FRAMES // 2\n"),
    ("N30 anchor wall clock may stand still", "                or anchor[1] <= previous[1]):", "                ):"),
    ("N31 anchor past the capture accepted",
     "    if index < AUDIO_CONFIRM_FRAMES or any(anchor[0] > index for anchor in layout.anchors):",
     "    if index < AUDIO_CONFIRM_FRAMES:"),
    ("N32 copied channel word read as a swap",
     "                exchanged = theirs and not theirs & AUDIO_ZERO_MASK and _audio_fields(theirs)[0] == own",
     "                exchanged = True"),
]

if __name__ == "__main__":
    sys.exit(rm.main())
