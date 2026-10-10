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
    # not from the stage that was judged
    "r_fill_from_flash": (
        (("\tif (chosen == NVM_SLOT_NONE)\n\t\tnvm_stage_blank_image();\n"
          "\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\tNVM_IMG[i] = NVM_STG[i];\n",
          "\tif (chosen != NVM_SLOT_NONE) {\n"
          "\t\tconst volatile uint8_t *src = nvm_slot(chosen);\n\n"
          "\t\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\t\tNVM_IMG[i] = src[i];\n"
          "\t} else {\n\t\tnvm_stage_blank_image();\n"
          "\t\tfor (i = 0; i < NVM_IMG_LEN; ++i)\n\t\t\tNVM_IMG[i] = NVM_STG[i];\n\t}\n"),),
        "is not the container it judged"),
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
#: the wrap value), and the fault windows (the first SKIP reads from
#: power-on clean, the next COUNT faulty) that walk a fault over every boot
#: read of both slots, plus one window that lasts the whole boot
FAULT_SEQS = (1, 0x5A5A5, 0x8000_0000, 0xFFFF_FFFF)
WHOLE = (0, 64)
FAULT_WINDOWS = tuple((skip, count) for skip in range(6) for count in (1, 2, 3)) + (WHOLE,)
#: both slots valid: the newer container's sequence, the older one below it,
#: so 0 is the wrap (the newer at 0, the older at 0xFFFFFFFF)
BOTH_VALID_SEQS = (0x5A5A5, 0)
#: the newer slot's re-stage reads when both slots are valid: read 0 is the
#: AEM image and reads 1 and 2 judge A and B
RESTAGE_WINDOWS = ((3, 1), (3, 2), (3, 3))
#: a writer restart's reads, counted from its first (a restart reads no AEM
#: image): one faulty read at each of the first four, which reach both slots'
#: judgements and the re-stage, and with both slots valid the newer slot's
#: three re-stage reads after one judgement read of each
RESTART_WINDOWS = tuple((skip, 1) for skip in range(4))
RESTART_RESTAGE = (2, 3)
#: the firmware's NVM_READ_TRIES, and the most reads a boot may open: the AEM
#: image, then NVM_READ_TRIES judgements and as many re-stages of each slot
READ_TRIES = 3
BOOT_READ_BOUND = 1 + 4 * READ_TRIES
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


def restart_cases(body: int) -> list[FaultCase]:
    """Check 13's cases on a writer restart without a fabric reset, the
    re-attach path (#671), both ways round, each after a clean cold boot.
    With the other slot blank, the valid slot is faulted for the whole
    restart at every sequence by a header byte and once by `body`, and by
    one faulty read at each of the restart's first four; with both slots
    valid, the newer is faulted for the whole restart or on its re-stage."""
    cases = []
    for valid in "ab":
        cases += [FaultCase(valid, False, seq, ("--read-fault", f"{valid}:0:0:64"), *WHOLE, True)
                  for seq in FAULT_SEQS]
        cases.append(FaultCase(valid, False, 0x5A5A5, ("--read-fault", f"{valid}:{body}:0:64"), *WHOLE, True))
        cases += [FaultCase(valid, False, 0x5A5A5, ("--read-fault", f"{valid}:11:{skip}:{count}:128"),
                            skip, count, True) for skip, count in RESTART_WINDOWS]
        cases += [FaultCase(valid, True, seq, ("--read-fault", f"{valid}:0:{skip}:{count}"), skip, count, True)
                  for seq in BOTH_VALID_SEQS for skip, count in (WHOLE, RESTART_RESTAGE)]
    return cases


def fault_cases(body: int) -> list[FaultCase]:
    """Check 13's cases, both ways round: the writer restarts first, then
    the cold boots. With the other slot blank, the
    valid slot is faulted at every sequence and window, by one byte of its
    header or sequence word and by `body`, a byte of its record area, which
    only the CRC over every byte read refuses; the blank slot is faulted at
    one sequence; and one all-0xFF read is walked over the boot. With both
    slots valid, the newer is faulted over every window and the older over
    the whole boot, and the newer's re-stage reads are answered with the
    older's container."""
    cases = restart_cases(body)
    for valid in "ab":
        other = "b" if valid == "a" else "a"
        for seq in FAULT_SEQS:
            for skip, count in FAULT_WINDOWS:
                byte, base = (0x0B, 0x80) if (skip + count) % 2 else (0, 8)
                cases += [FaultCase(valid, False, seq,
                                    ("--read-fault", f"{valid}:{off}:{skip}:{count}:{base}"),
                                    skip, count) for off in (byte, body)]
        for skip, count in FAULT_WINDOWS:
            cases.append(FaultCase(valid, False, 0x5A5A5,
                                   ("--read-fault", f"{other}:0:{skip}:{count}"), skip, count))
        for skip in range(6):
            cases.append(FaultCase(valid, False, 0x5A5A5, ("--read-ff", f"{valid}:{skip}:1"), skip, 1))
        for seq in BOTH_VALID_SEQS:
            for skip, count in FAULT_WINDOWS:
                off = 0 if (skip + count) % 2 else body
                cases.append(FaultCase(valid, True, seq,
                                       ("--read-fault", f"{valid}:{off}:{skip}:{count}"), skip, count))
            cases.append(FaultCase(valid, True, seq, ("--read-fault", f"{other}:{body}:0:64"), 0, 64))
            cases += [FaultCase(valid, True, seq, ("--read-other", f"{valid}:{skip}:{count}"),
                                skip, count) for skip, count in RESTAGE_WINDOWS]
    return cases


def judged(case: FaultCase, boot: re.Match, unread: int) -> list[str]:
    """Each slot's boot verdict is what its bytes say when read cleanly, or
    the slot is UNREAD: VD_LEN, no sequence, its bit in `unread=`. Every
    fault the cases plant returns other bytes on every faulty read, so no
    other verdict may stand."""
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
    """The reads a boot opened: never over the bound, and with one slot
    faulted for the whole boot exactly the AEM image (a restart reads none),
    three of that slot and two of the other, two agreeing blank reads or a
    judgement and a re-stage (R603-2-S1), so the per-slot bound is pinned."""
    first = 0 if case.restart else 1
    what = "writer restart" if case.restart else "boot"
    if reads > BOOT_READ_BOUND - 1 + first:
        return [f"{case.name}: the {what} read the flash {reads} times, "
                f"over the bound of {BOOT_READ_BOUND - 1 + first}"]
    if (case.skip, case.count) == WHOLE and reads != first + READ_TRIES + 2:
        return [f"{case.name}: with one slot faulted on every read the {what} read the flash "
                f"{reads} times, want exactly {first + READ_TRIES + 2}"]
    return []


def restart_findings(case: FaultCase, restart: str, boot: re.Match | None,
                     before: dict[str, int], after: dict[str, int]) -> tuple[list[str], bool]:
    """A writer restart's transcript, and the harness state when it began
    and after its change and debounce (#671 on the re-attach path). The
    line is graded as a cold boot's. A slot left unread, or a fault lasting
    the whole restart, HOLDS the writer: it says so, erases, programs,
    starts, acknowledges and heartbeats nothing more, and the fabric
    revokes nvm_backed. Otherwise the change commits. Returns the findings
    and whether the restart held."""
    f = read_findings(case, after.get("restart_reads", 0))
    if boot is None:
        return f + [f"{case.name}: the writer restart printed no boot line"], False
    tally = UNREAD_RE.search(restart)
    unread = int(tally.group(2)) if tally else 0
    held = HELD_LINE in restart
    f += line_findings(case, boot, unread)
    if case.count == 1 and held:
        f.append(f"{case.name}: one faulty read held the writer; the bound must resolve it")
    if (unread or (case.skip, case.count) == WHOLE) and not held:
        f.append(f"{case.name}: the restart left a slot unread, yet the writer re-attached live")
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
