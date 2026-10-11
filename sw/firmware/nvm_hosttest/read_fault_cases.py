# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check 13's cases, the boot-line rule they are graded by, and the #671 plants.

A library of `test_nvm_firmware.py`, which grades the shipping writer with
them, kept apart so neither file outgrows a reader: what each slot holds,
which boot reads a planted read fault answers wrongly, on a cold boot or on
a writer restart without a fabric reset, what the boot line and the reads it
opened must then say, and the writer defects `--self-test` plants into a
copy of the firmware, each with the words of the finding that must catch it
(#671).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

#: the #671 defects: label -> (every (text, replacement) pair the plant
#: makes, each text occurring exactly once, and the words of the finding
#: that must catch it)
READ_FAULT_MUTATIONS = {
    # an unread slot no longer holds the writer: the restart at sequence 0
    "restart_at_zero": (
        (("\tif (!nvm_unread) {\n\t\tnvm_ready = 1;",
          "\tif (1) {\n\t\tnvm_ready = 1;"),),
        "was lost on the clean reboot"),
    "unbounded_retry": (
        (("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK ||",
          "\tfor (n = 0; ; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK ||"),),
        "over the bound"),
    "generation_from_refused_slot": (
        (("\tif (rd.vd == VD_OK)\n\t\trd.seq = nvm_seq_of(NVM_STG);\n\telse\n",
          "\trd.seq = nvm_seq_of(NVM_STG);\n\tif (rd.vd != VD_OK)\n"),
         ("\t\tnvm_seq = 0;\n", "\t\tnvm_seq = (seq_a > seq_b) ? seq_a : seq_b;\n")),
        "generation was taken from a refused slot"),
    # R501-3's probe on #665: two refusals alike by verdict, not by bytes
    "verdict_only_agreement": (
        (("\treturn a.vd == b.vd && a.digest == b.digest && a.bytes == b.bytes;",
          "\treturn a.vd == b.vd;"),),
        "was lost on the clean reboot"),
    # R603-1's: a refusal's digest spans the header alone, so two reads whose
    # record areas differ agree, and a refusal decided after the header stands
    "r_digest_header_only": (
        (("\t\trd.digest = nvm_crc32(NVM_STG, rd.bytes);",
          "\t\trd.digest = nvm_crc32(NVM_STG, KLJ2_HDR);"),),
        "on reads that returned different bytes"),
    # R603-1's: the window filled by a fresh read of the slot, as before #671,
    # not from the stage that was judged. The read is one the rule does not
    # make, after the boot's last; the generated windows reach it, and the
    # exact read count sees it on every boot that fills the window
    "r_fill_from_flash": (
        (("\tif (chosen == NVM_SLOT_NONE)\n\t\tnvm_stage_blank_image();\n"
          "\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\tNVM_IMG[i] = NVM_STG[i];\n",
          "\tif (chosen != NVM_SLOT_NONE) {\n"
          "\t\tconst volatile uint8_t *src = nvm_slot(chosen);\n\n"
          "\t\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\t\tNVM_IMG[i] = src[i];\n"
          "\t} else {\n\t\tnvm_stage_blank_image();\n"
          "\t\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\t\tNVM_IMG[i] = NVM_STG[i];\n\t}\n"),),
        "want exactly"),
    # R603-1's: a pick that never reads back offers nothing, not the other slot
    "r_restage_fail_offers_none": (
        (("\t\tchosen = nvm_pick_slot(nvm_verdict_a, seq_a, nvm_verdict_b, seq_b);\n\t}\n",
          "\t\tchosen = NVM_SLOT_NONE;\n\t}\n"),),
        "yet the boot offered"),
    # R602-1's: a pick that never reads back is not marked UNREAD, so the
    # writer goes live behind it
    "restage_fail_not_unread": (
        (("\t\tnvm_unread |= (chosen == NVM_SLOT_A) ? 1u : 2u;\n\t\tif (chosen == NVM_SLOT_A) {\n",
          "\t\tif (chosen == NVM_SLOT_A) {\n"),),
        "yet the boot line does not name it unread"),
    # R603-1's S3: the re-stage takes any OK read, whatever sequence it names,
    # so a read answered with the other slot's container is loaded
    "r_restage_any_seq": (
        (("\t\tif (rd.vd == VD_OK && rd.seq == seq)\n\t\t\treturn 1;",
          "\t\tif (rd.vd == VD_OK && (rd.seq == seq || 1))\n\t\t\treturn 1;"),),
        "another valid container than the one the boot offered"),
    # R603-2's F1: a writer restart without a fabric reset (the re-attach
    # path) goes live with a slot unread, while the cold boot still holds
    "r_reattach_goes_live": (
        (("\t\tnvm_publish(verdict);\n\t\tnvm_go_live();\n\t\tprintf(\"Milan NVM: writer restarted",
          "\t\tnvm_publish(verdict);\n\t\tnvm_ready = 1;\n\t\tprintf(\"Milan NVM: writer restarted"),),
        "yet the writer re-attached live"),
    # R603-2's S1: a judgement takes four reads, over the stated three, which
    # the total bound alone does not see
    "r_judge_four_tries": (
        (("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK ||",
          "\tfor (n = 0; n < NVM_READ_TRIES + 1u; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK ||"),),
        "want exactly"),
    # R602-3's F1 probe: the re-stage loses its bound, so a fault that starts
    # after the judgement reads the slot until it ends
    "p_restage_unbounded": (
        (("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
          "\tfor (n = 0; n != 0xffffffffu; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)"),),
        "want exactly"),
    # R603-3's F1 probe: a re-stage takes four reads, over the stated three
    "r_restage_four_tries": (
        (("\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
          "\tfor (n = 0; n < NVM_READ_TRIES + 1u; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
          "\t\tif (rd.vd == VD_OK && rd.seq == seq)"),),
        "want exactly"),
}

#: the product shapes, which the #671 controls are planted into besides the
#: first shape
PRODUCT_SHAPES = ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8")
#: check 13's boots that retire the writer for a cause of their own: the cause,
#: the harness options, the boot's line for it, and what `milan_nvm` reports
RETIRE_CAUSES = (
    ("the backend's contract", ("--boot-backend", "contract"),
     "does not carry saved-state contract 3", "writer disabled"),
    ("no accepted load", ("--boot-backend", "over"),
     "no window load was accepted in this boot", "writer retired"),
    ("a window gone live", ("--boot-backend", "live"),
     "the window went live without a validated load", "writer retired"),
    ("refused loads", ("--refuse-loads", "4"),
     "refused 4 window loads; the window is not validated", "writer retired"))

#: the sequences the ticket names (1, far above 1, the int32 half-range and
#: the wrap value); with both slots valid, the newer container's sequence, the
#: older one below it, so 0 is the wrap (the newer at 0, the older at 0xFFFFFFFF)
FAULT_SEQS = (1, 0x5A5A5, 0x8000_0000, 0xFFFF_FFFF)
BOTH_VALID_SEQS = (0x5A5A5, 0)
#: the firmware's NVM_READ_TRIES, and the most reads a boot may open: the AEM
#: image, then NVM_READ_TRIES judgements and as many re-stages of each slot
READ_TRIES = 3
BOOT_READ_BOUND = 1 + 4 * READ_TRIES
#: the fault window that lasts the whole boot (the first SKIP reads clean, the
#: next COUNT faulty)
WHOLE = (0, 64)
#: check 13's fault groups (#671): whether the other slot holds an older
#: container (else it is blank), the slot the fault answers wrongly (the valid
#: or newer one, or the other), its manners of fault, and the sequences the
#: newer container takes in turn. A byte fault flips the magic
#: byte, the top byte of the sequence word or a record-area byte, by another
#: value on each faulty read; --read-ff reads the slot all 0xFF; --read-other
#: answers with the other slot's bytes, an address fault (R603-3).
GROUPS = ((False, "valid", ("magic", "seq", "body", "--read-ff"), FAULT_SEQS),
          (False, "other", ("magic", "--read-other"), FAULT_SEQS),
          (True, "valid", ("magic", "body", "--read-other"), BOTH_VALID_SEQS),
          (True, "other", ("magic", "body"), BOTH_VALID_SEQS))
#: a flipped byte: its offset (None is the record area's middle byte, which
#: depends on the shape) and the first faulty read's XOR
FLIPS = {"magic": (0, 8), "seq": (0x0B, 0x80), "body": (None, 8)}
HELD_LINE = "the writer is HELD until reset"
#: what a held writer restart prints on re-attaching (R603-2-S2)
REATTACH_HELD = "re-attached and HELD"
UNREAD_RE = re.compile(r"; read faults=(\d+) unread=(\d+)\.")
SEQ_MASK = 0xFFFF_FFFF


@dataclass(frozen=True)
class FaultCase:
    """One check-13 case: what each slot holds, the fault, and its window."""

    valid: str                  # the slot holding the (newer) valid container
    older: bool                 # the other slot holds an older one, else it is blank
    seq: int                    # the (newer) container's sequence
    fault: tuple[str, str]      # the harness option and its argument
    skip: int
    count: int
    restart: bool = False       # the fault meets a writer restart, not the cold boot

    @property
    def other(self) -> str:
        """The slot that does not hold the (newer) valid container."""
        return "b" if self.valid == "a" else "a"

    @property
    def name(self) -> str:
        """How a finding names the case."""
        held = (f"slot {self.valid.upper()} newer at seq {self.seq:#x}, the other older"
                if self.older else f"slot {self.valid.upper()} valid at seq {self.seq:#x}")
        return f"{held}, {self.fault[0]} {self.fault[1]}" + (" on a writer restart" if self.restart else "")

    def truth(self) -> dict[str, tuple[str, int]]:
        """Each slot's verdict and sequence, as its bytes read cleanly."""
        other = ("VD_OK", (self.seq - 1) & SEQ_MASK) if self.older else ("VD_BLANK", 0)
        return {self.valid.upper(): ("VD_OK", self.seq), self.other.upper(): other}


def windows(bound: int) -> tuple[tuple[int, int], ...]:
    """Check 13's fault windows, generated, never picked (R602-3-F1,
    R603-3-F1): the window that lasts the whole boot, and every read a boot
    may open as the first faulty one, times every length from one read to one
    past NVM_READ_TRIES, the most reads one judgement or one re-stage gives a
    slot, the longest first. Enumerate the whole boot or restart bound,
    including starts a clean boot never reaches; runtime never removes a
    window from the campaign."""
    return (WHOLE,) + tuple((skip, count) for count in range(READ_TRIES + 1, 0, -1) for skip in range(bound))


def fault_cases(body: int) -> list[FaultCase]:
    """Check 13's cases: each group's every manner of fault over every
    window, both ways round, on a writer restart and on a cold boot. A
    group's sequences are taken in turn, so the sequence set is spread over
    the windows, not crossed with them (the full cross exceeds the suite's
    time). A case outside the rule's stated detection limit is not run, and
    every window keeps its byte faults, which are always inside it: there
    two faulty reads of one judgement return the same bytes (all 0xFF
    twice), or a faulty read returns the other slot's valid container and it
    stands, and no rule over the bytes sees either (`expect`). The groups'
    lists are interleaved, so a planted control meets every group early.
    `body` is the shape's record-area byte."""
    lists = []
    for restart in (True, False):
        for older, faulted, manners, seqs in GROUPS:
            for turn, valid in enumerate("ab"):
                slot = valid if faulted == "valid" else ("b" if valid == "a" else "a")
                bound = BOOT_READ_BOUND - int(restart)
                cases = (FaultCase(valid, older, seqs[(w + m + turn) % len(seqs)],
                                   fault(manner, slot, skip, count, body), skip, count, restart)
                         for w, (skip, count) in enumerate(windows(bound))
                         for m, manner in enumerate(manners))
                lists.append([case for case in cases if expect(case).within])
    return [lst[n] for n in range(max(map(len, lists))) for lst in lists if n < len(lst)]


def fault(manner: str, slot: str, skip: int, count: int, body: int) -> tuple[str, str]:
    """The harness option and argument for one manner of fault."""
    if manner.startswith("--"):
        return manner, f"{slot}:{skip}:{count}"
    off, base = FLIPS[manner]
    return "--read-fault", f"{slot}:{body if off is None else off}:{skip}:{count}:{base}"


@dataclass(frozen=True)
class Expect:
    """What the reference model says a case's boot (or restart) does."""

    reads: int                  # the flash reads it opens
    unread: str                 # the slots it leaves UNREAD: "", "A", "B" or "AB"
    unstaged: str               # of those, the ones judged that did not read back as judged
    within: bool                # every slot ends as its bytes say, or UNREAD


def expect(case: FaultCase) -> Expect:
    """The reference model of the writer's reads (#671), written once from
    the rule and not from the firmware. A cold boot reads the AEM image
    first. Each slot, A then B, is judged by at most READ_TRIES reads: a
    VD_OK read stands alone, any other verdict on a read that returned the
    same bytes as an earlier one; a slot with no standing verdict is UNREAD.
    The newer VD_OK slot (A on a tie) is re-staged by at most READ_TRIES
    reads until one is VD_OK at the sequence it was judged at; one that is
    never so is UNREAD, and the other VD_OK slot is re-staged in turn. A
    clean read returns the slot's container or blank; a faulty one returns
    bytes no other read returns, a blank read, or the other slot's clean
    read, as the case's option says."""
    clean = {case.valid.upper(): ("OK", case.seq, "newer"),
             case.other.upper(): ("OK", (case.seq - 1) & SEQ_MASK, "older") if case.older else ("BLANK",)}
    option, arg = case.fault
    reads = 0 if case.restart else 1

    def read(slot: str) -> tuple:
        """The next read of `slot`, as the case's fault answers it."""
        nonlocal reads
        reads += 1
        if slot != arg[0].upper() or not case.skip <= reads - 1 < case.skip + case.count:
            return clean[slot]
        return {"--read-fault": ("REFUSED", reads), "--read-ff": ("BLANK",)}.get(
            option, clean["BA"["AB".index(slot)]])

    def judge(slot: str) -> tuple:
        """The slot's standing verdict, or UNREAD."""
        seen = []
        for _ in range(READ_TRIES):
            got = read(slot)
            if got[0] == "OK" or got in seen:
                return got
            seen.append(got)
        return ("UNREAD",)

    verdict = {slot: judge(slot) for slot in "AB"}
    unstaged, staged = "", None
    while staged is None and any(v[0] == "OK" for v in verdict.values()):
        ok = [slot for slot in "AB" if verdict[slot][0] == "OK"]
        pick = ok[0] if len(ok) == 1 or (verdict["A"][1] - verdict["B"][1]) & SEQ_MASK < 0x8000_0000 else "B"
        staged = next((got for got in (read(pick) for _ in range(READ_TRIES))
                       if got[0] == "OK" and got[1] == verdict[pick][1]), None)
        if staged is None:
            verdict[pick], unstaged = ("UNREAD",), unstaged + pick
        elif staged != clean[pick]:
            verdict[pick] = staged
    unread = "".join(slot for slot in "AB" if verdict[slot] == ("UNREAD",))
    return Expect(reads, unread, "".join(sorted(unstaged)),
                  all(verdict[slot] in (clean[slot], ("UNREAD",)) for slot in "AB"))


def judged(case: FaultCase, boot: re.Match, unread: int) -> list[str]:
    """Each slot's boot verdict is what its bytes say when read cleanly, or
    the slot is UNREAD: VD_LEN, no sequence, its bit in `unread=`. Every
    case check 13 runs is inside the rule's detection limit (`fault_cases`),
    so no other verdict may stand."""
    findings = []
    for n, letter in enumerate("AB"):
        vd, seq, bit = boot.group(1 + 2 * n), int(boot.group(2 + 2 * n)), (unread >> n) & 1
        want_vd, want_seq = case.truth()[letter]
        if (vd, bit) == ("VD_LEN", 1) or ((vd, seq, bit) == (want_vd, want_seq, 0)):
            continue
        if vd == "VD_LEN" and want_vd != "VD_LEN":
            findings.append(f"{case.name}: slot {letter} did not read back as it was judged, "
                            f"yet the boot line does not name it unread: {boot.group(0)}")
        elif vd != want_vd:
            findings.append(f"{case.name}: slot {letter} was taken as {vd} on reads that "
                            f"returned different bytes: {boot.group(0)}")
        else:
            findings.append(f"{case.name}: slot {letter} reads {vd} seq {seq:#x} unread bit {bit}, "
                            f"but holds {want_vd} seq {want_seq:#x}: {boot.group(0)}")
    return findings


def line_findings(case: FaultCase, boot: re.Match, unread: int) -> list[str]:
    """What a boot line must say: each slot as `judged`, and the offer the
    slots it accepts make."""
    f = judged(case, boot, unread)
    want, got = offer(boot), (boot.group(5), int(boot.group(6)))
    if got != want:
        f.append(f"{case.name}: by the slots its boot line accepts the offer is {want[0]} seq "
                 f"{want[1]:#x}, yet the boot offered {got[0]} seq {got[1]:#x}: {boot.group(0)}")
    return f


def read_findings(case: FaultCase, reads: int) -> list[str]:
    """The reads a boot opened: never over the bound, and exactly the reads
    the reference model opens for the case (R602-3-F1, R603-3-F1), so each
    judgement's and each re-stage's bound is pinned from both sides."""
    first = 0 if case.restart else 1
    what = "writer restart" if case.restart else "boot"
    if reads > BOOT_READ_BOUND - 1 + first:
        return [f"{case.name}: the {what} read the flash {reads} times, "
                f"over the bound of {BOOT_READ_BOUND - 1 + first}"]
    want = expect(case).reads
    if reads != want:
        return [f"{case.name}: the {what} read the flash {reads} times, want exactly {want}"]
    return []


def hold_findings(case: FaultCase, held: bool, unread: int, out: str) -> list[str]:
    """Whether a boot (or restart) held, by its own line's tally and by the
    reference model: a slot left unread holds the writer, a fault the bound
    resolves never does, and a held boot's console names each slot it left
    unread and why, a missing verdict or a re-stage that did not read back
    as judged (R603-3-S1)."""
    e = expect(case)
    if held and not e.unread:
        what = "one faulty read" if case.count == 1 else "a fault the bound resolves"
        return [f"{case.name}: {what} held the writer; the bound must resolve it"]
    if not held:
        if not (unread or e.unread or (case.skip, case.count) == WHOLE):
            return []
        return [f"{case.name}: " + ("the restart left a slot unread, yet the writer re-attached live"
                                    if case.restart else "a slot no read returned twice did not hold the writer")]
    want = "Milan NVM: " + " and ".join(
        f"slot {s} {'did not read back as it was judged' if s in e.unstaged else 'gave no standing verdict'} "
        f"in {READ_TRIES} reads" for s in e.unread) + "; its authority is unknown"
    return [] if want in out else [f"{case.name}: the hold names another cause than its reads gave: want {want!r}"]


def restart_findings(case: FaultCase, restart: str, boot: re.Match | None,
                     before: dict[str, int], after: dict[str, int]) -> tuple[list[str], bool]:
    """A writer restart's transcript, and the harness state when it began
    and after its change and debounce (#671 on the re-attach path). The
    line and the hold are graded as a cold boot's. A held restart says so,
    erases, programs, starts, acknowledges and heartbeats nothing more, and
    the fabric revokes nvm_backed. Otherwise the change commits. Returns the
    findings and whether the restart held."""
    f = read_findings(case, after.get("restart_reads", 0))
    if boot is None:
        return f + [f"{case.name}: the writer restart printed no boot line"], False
    tally = UNREAD_RE.search(restart)
    unread = int(tally.group(2)) if tally else 0
    held = HELD_LINE in restart
    f += line_findings(case, boot, unread) + hold_findings(case, held, unread, restart)
    if not held:
        if after.get("acks") != before.get("acks", 0) + 1 or after.get("dirty") != 0:
            f.append(f"{case.name}: the change was neither committed nor refused: {after}")
        return f, held
    moved = [k for k in ("hb", "erases", "programs", "starts", "acks") if after.get(k) != before.get(k)]
    if moved or (after.get("backed"), after.get("stale"), after.get("dirty")) != (0, 1, 1):
        f.append(f"{case.name}: the held writer persisted something or kept its claim after the "
                 f"restart ({', '.join(moved) or 'no count'} moved): {after}")
    if REATTACH_HELD not in restart:
        f.append(f"{case.name}: the held restart printed that it re-attached, not that it is held")
    return f, held


def offer(boot: re.Match) -> tuple[str, int]:
    """The slot a boot must offer by what its own line accepts, and the
    sequence: the newer VD_OK slot by the wrap-safe compare (A on a tie), or
    none at sequence 0."""
    accepted = [(letter, int(boot.group(2 + 2 * n))) for n, letter in enumerate("AB")
                if boot.group(1 + 2 * n) == "VD_OK"]
    if len(accepted) == 2:
        (_, seq_a), (_, seq_b) = accepted
        return accepted[0] if (seq_a - seq_b) & SEQ_MASK < 0x8000_0000 else accepted[1]
    return accepted[0] if accepted else ("-", 0)
