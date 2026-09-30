#!/usr/bin/env python3
"""Assert the outcome of every review probe and census mutant run at one head.

usage: check_review_runs.py <repo> <work>
<work> holds the byte-identical snapshot of <repo> the runs copied from
(<work>/clone) and the logs each review's scripts wrote, run unchanged from
copies of those scripts:
  r412-3/receipts/   the round-3 internal review: probe_all.sh (25 early probes,
                     3 through the whole gate 1b) and census_mutants_run.sh (M1-M9)
  r413-4/receipts/r413/  the round-4 external review: r413_census_stop_run.sh
                     (N1-N4 and the unmutated head), r413_probe.sh (9 plants) and
                     r413_mutant_probe.sh (N1 with the +2 and +3 plants)
  r412-4/            the round-4 internal review: its probe sets through
                     patch_probe_hook.py (probes/), two plants through the whole
                     gate function (whole/, whole_batch.out) and run_mutants.py
                     (mutants/: N0, K0-K8, B1, B2)
  own/receipts/      this round's drop-one-byte mutants D0-D3 and premise mutants
                     Q2, Q3 (and the previous round's P1, P2), by stop_run.sh
Exit 0 only when the snapshot is at <repo>'s HEAD and every log names that head
where its script records one, and each outcome is the one tabled below.
"""
import re
import subprocess
import sys
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()


def head_of(where: Path) -> str:
    """HEAD of the repository at `where`."""
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=where, check=True, capture_output=True,
                          text=True).stdout.strip()


head = head_of(repo)
WRITE = "a store lands on aem_loaded's storage other than milan_init()'s one store"
ESCAPE = "the linked image forms the full address of aem_loaded's storage"
NAME = "another symbol of the linked image is on aem_loaded's storage"
ADDRESS = "the address of aem_loaded is taken"
SOURCE_WRITE = "aem_loaded must contain only the image verifier's verdict"
UNPLACED = "a STORE this gate cannot PLACE"
LIMIT = ("a called function writing through any pointer with no relocation on its storage is outside "
         "these pins, whatever the pointer's origin")
BYTES = "refused 17/17 planted pin breaks on the verdict, each naming its pins, 3 of them reaching it at " \
        "one byte each, +1, +2, +3 of its storage"
ACCEPTED = None
#: probe -> ACCEPTED, or (texts the refusal must carry, image pins it must NOT name)
R412_3_EARLY = {
    "base": ACCEPTED, "nbr_after_sscanf": ACCEPTED, "arr_overrun_sscanf": ACCEPTED,
    "nbr_runtime_sscanf": ACCEPTED, "pre_overrun_sscanf": ACCEPTED,
    "plain_write": ((SOURCE_WRITE,), ()), "bcp_write": ((SOURCE_WRITE,), ()),
    "pie_write": ((SOURCE_WRITE,), ()), "optimize_write": ((SOURCE_WRITE,), ()),
    "block_extern_sscanf": (("the address of aem_loaded must not be taken",), ()),
    "nbr_runtime_store": ((UNPLACED,), ()),
    "nbr_memset": (("identity-sample absence rule",), ()),
    "splice_write": ((WRITE,), ()), "paste_write": ((WRITE,), ()),
    "m_macro_set": ((WRITE,), ()), "m_macro_addr": ((WRITE, ADDRESS), ()),
    "alias_write": ((WRITE, NAME), ()), "static_alias_write": ((WRITE, NAME), ()),
    "alias_sscanf": ((ESCAPE, NAME), ()), "weakref_sscanf": ((ESCAPE, NAME), ()),
    "static_alias_sscanf": ((ESCAPE, NAME), ()), "alias_decl_only": ((NAME,), ()),
    "m_macro_addr_sscanf": ((ESCAPE, ADDRESS), ()),
    "nbr_before_sscanf": ((ESCAPE,), (WRITE, NAME, ADDRESS)),
    "nbr_byte_sscanf": ((ESCAPE,), (WRITE, NAME, ADDRESS)),
}
R413_4_EARLY = {
    "own_local_under_store": ACCEPTED, "own_callee_store": ACCEPTED, "data_word_nbr_sscanf": ACCEPTED,
    "own_folded_store": ((WRITE, ESCAPE), (NAME, ADDRESS)),
    "own_runtime_store": ((UNPLACED,), ()), "data_word_nbr_store": ((UNPLACED,), ()),
    "interior_b1_store": ((WRITE, ESCAPE), (NAME, ADDRESS)),
    "interior_b2_sscanf": ((ESCAPE,), (WRITE, NAME, ADDRESS)),
    "interior_b3_sscanf": ((ESCAPE,), (WRITE, NAME, ADDRESS)),
}
#: the round-4 external review's range mutants: None is the unmutated head
R413_4_STOP = {"N1_first_two_bytes": "folded onto byte +2 of aem_loaded",
               "N2_first_three": "folded onto byte +3 of aem_loaded",
               "N3_skip_first_byte": "the compiled firmware enters entity_advertise() with [None]",
               "N4_second_byte_only": "folded onto byte +2 of aem_loaded", "none": None}
#: the round-4 internal review's hook probes: ACCEPTED, or texts the refusal must carry
R412_4_PROBES = {
    "pre_overrun_sscanf": ACCEPTED, "nbr_runtime_sscanf": ACCEPTED, "nbr_fold_own": ACCEPTED,
    "own_store_localptr": ACCEPTED, "own_store_pre_array_local": ACCEPTED,
    "csr_pointer_sscanf": ACCEPTED, "parsed_pointer_sscanf": ACCEPTED, "literal_sscanf": ACCEPTED,
    "stack_runtime_sscanf": ACCEPTED, "unplanted": ACCEPTED,
    "nbr_fold_byte0": (ESCAPE,), "nbr_fold_byte1": (ESCAPE,), "nbr_fold_byte2": (ESCAPE,),
    "nbr_fold_byte3": (ESCAPE,), "pre_fold_byte2": (ESCAPE,),
    "own_store_fold": (WRITE, ESCAPE), "own_store_runtime": (UNPLACED,),
    "own_store_bounded_loop": (UNPLACED,),
    "r3_pre_overrun_sscanf": ACCEPTED, "r3_nbr_runtime_sscanf": ACCEPTED, "r3_nbr_byte_sscanf": (ESCAPE,),
}
R412_4_MUTANTS = {f"K{n}": None for n in range(9)}
R412_4_MUTANTS.update({"B1": "land on byte(s) [] of aem_loaded's storage, not on byte +1 alone",
                       "B2": "land on byte(s) [0] of aem_loaded's storage, not on byte +1 alone",
                       "K7": "folded onto byte +1 of aem_loaded", "K8": "folded onto byte +1 of aem_loaded"})
OWN = {"D0_drop_byte0": "the compiled firmware enters entity_advertise() with [None]",
       "D1_drop_byte1": "the resolver accepted a neighbour's address folded onto byte +1 of aem_loaded",
       "D2_drop_byte2": "the resolver accepted a neighbour's address folded onto byte +2 of aem_loaded",
       "D3_drop_byte3": "the resolver accepted a neighbour's address folded onto byte +3 of aem_loaded",
       "Q2_on_neighbour": "the interior-byte +2 break's references from nvm_boot() land on byte(s) [] ",
       "Q3_on_byte1": "the interior-byte +3 break's references from nvm_boot() land on byte(s) [1] ",
       "P1_on_neighbour": "the interior-byte +1 break's references from nvm_boot() land on byte(s) [] ",
       "P2_on_first_byte": "the interior-byte +1 break's references from nvm_boot() land on byte(s) [0] "}
failures = []


def fail(message: str) -> None:
    """Record one failure."""
    failures.append(message)


def read(path: Path, first: str | None) -> tuple[str, int | None]:
    """The log at `path` and its exit code, after checking it names this head."""
    text = path.read_text(errors="replace")
    if first is not None and not text.startswith(f"{first} head={head}"):
        fail(f"{path.name}: not a run at {head}")
    codes = re.findall(r"(?m)^rc=(\d+)", text)
    return text, int(codes[-1]) if codes else None


def refusal(text: str) -> str:
    """Every GATE1B REFUSED line of a log, joined."""
    return "\n".join(line for line in text.splitlines() if line.startswith("GATE1B REFUSED"))


def early(path: Path, first: str, want: tuple[tuple[str, ...], tuple[str, ...]] | None) -> str:
    """Check one early-stopped probe log against `want`; return its table cell."""
    text, rc = read(path, first)
    if want is ACCEPTED:
        ok = rc == 0 and "R412 gate-1b verdict ran=True kept=['aem_loaded']" in text
        cell = "ACCEPTED, kept=['aem_loaded']"
    else:
        must, must_not = want
        said = refusal(text)
        ok = rc == 1 and all(t in said for t in must) and not any(t in said for t in must_not)
        cell = "REFUSED, naming " + "; ".join(t[:40] for t in must)
    if not ok:
        fail(f"{path.name}: rc={rc}, expected {cell}")
    return cell


if head_of(work / "clone") != head:
    fail(f"the snapshot {work / 'clone'} is not at {head}")
r3 = work / "r412-3" / "receipts"
for probe, want in R412_3_EARLY.items():
    print(f"R412-3 early {probe}: {early(r3 / f'gate1b_early_{probe}.log', f'probe={probe}', want)}")
for probe in ("base", "nbr_runtime_sscanf", "pre_overrun_sscanf"):
    text, rc = read(r3 / f"gate1b_full_{probe}.log", f"probe={probe}")
    passed = rc == 0 and "GATE1B PASS" in text and "kept the slot of aem_loaded across a call" in text \
        and BYTES in text and LIMIT in text
    print(f"R412-3 full {probe}: {'GATE1B PASS, slot kept, 17/17 at +1, +2, +3' if passed else 'NOT AS EXPECTED'}")
    if not passed:
        fail(f"gate1b_full_{probe}.log: rc={rc}, expected the whole gate 1b to pass")
for mutant in ("M1_no_escape", "M2_no_name", "M3_no_local", "M4_no_auipc", "M5_no_image_store",
               "M6_no_resolver_store", "M7_addi_in_place", "M8_no_image", "M9_by_name_only"):
    text, rc = read(r3 / f"census_mutant_{mutant}.log", f"mutant={mutant}")
    said = refusal(text)
    killed = rc == 1 and bool(said)
    if mutant == "M9_by_name_only":
        killed = killed and "accepted a neighbour's address folded onto byte +1 of aem_loaded" in said
    print(f"R412-3 mutant {mutant}: {'KILLED' if killed else 'SURVIVED'}: {said[16:150]}")
    if not killed:
        fail(f"census_mutant_{mutant}.log: rc={rc}, expected KILLED")

r4 = work / "r413-4" / "receipts" / "r413"
for mutant, killer in R413_4_STOP.items():
    text, rc = read(r4 / f"census_stop_{mutant}.log", f"mutant={mutant}")
    if killer is None:
        ok = rc == 0 and "refused=17/17 interior_bytes=[1, 2, 3]" in text and "kept=['aem_loaded']" in text
        cell = "PASSES the verdict controls, slot kept, 17/17, bytes [1, 2, 3]"
    else:
        ok = rc == 1 and killer in refusal(text)
        cell = f"KILLED: {killer}"
    print(f"R413-4 stop {mutant}: {cell}")
    if not ok:
        fail(f"census_stop_{mutant}.log: rc={rc}, expected {cell}")
for probe, want in R413_4_EARLY.items():
    print(f"R413-4 early {probe}: {early(r4 / f'gate1b_early_{probe}.log', f'probe={probe}', want)}")
for probe in ("interior_b2_sscanf", "interior_b3_sscanf"):
    name = f"mutant_probe_N1_first_two_bytes_{probe}.log"
    cell = early(r4 / name, f"mutant=N1_first_two_bytes probe={probe}", ACCEPTED)
    print(f"R413-4 N1 + {probe} (early stop, before the verdict controls): {cell}")

r5 = work / "r412-4"
if head_of(work / "clone") == head:
    for name in ("probe_run", "probe_run_r3shapes"):
        text, rc = read(r5 / "probes" / f"{name}.log", f"probes={name}")
        if not re.search(r"(?m)^rc=0 ", text):
            fail(f"{name}.log: the probe run did not exit 0")
    outcomes = {}
    for name in ("probe_run", "probe_run_r3shapes"):
        for line in (r5 / "probes" / f"{name}.log").read_text().splitlines():
            found = re.match(r"PROBE (\w+): (ACCEPTED|REFUSED|ERROR)(.*)", line)
            if found:
                outcomes[found[1]] = (found[2], found[3])
    for probe, want in R412_4_PROBES.items():
        verdict, rest = outcomes.get(probe, ("MISSING", ""))
        ok = (verdict == "ACCEPTED" and "kept=['aem_loaded']" in rest) if want is ACCEPTED else \
            (verdict == "REFUSED" and all(t in rest for t in want))
        print(f"R412-4 probe {probe}: {verdict}{'' if want is ACCEPTED else ', naming ' + '; '.join(t[:40] for t in want)}")
        if not ok:
            fail(f"R412-4 probe {probe}: {verdict}, expected {'ACCEPTED' if want is ACCEPTED else want}")
    batch = (r5 / "whole_batch.out").read_text()
    for probe in ("csr_pointer_sscanf", "stack_runtime_sscanf"):
        text = (r5 / "whole" / f"{probe}.log").read_text(errors="replace")
        ok = f"{probe}: RETURNED" in batch and "R412 GATE FUNCTION RETURNED" in text and LIMIT in text \
            and BYTES in text
        print(f"R412-4 whole gate function with {probe} planted: {'RETURNED, the class printed' if ok else 'NOT AS EXPECTED'}")
        if not ok:
            fail(f"whole/{probe}.log: expected the whole gate function to return and print the class")
    short = head[:9]
    for mutant, killer in {**R412_4_MUTANTS, "N0": None}.items():
        text = (r5 / "mutants" / f"a461_{short}_{mutant}.log").read_text(errors="replace")
        if mutant == "N0":
            ok = "R412 STOP AFTER RESOLVED NOTE" in text and BYTES in text and LIMIT in text
            cell = "PASSES through gate 1b's resolved note, 17/17 at +1, +2, +3"
        else:
            errors = [line for line in text.splitlines() if line.startswith("AssertionError")]
            ok = "R412 STOP AFTER RESOLVED NOTE" not in text and bool(errors) and \
                (killer is None or killer in errors[-1])
            cell = f"KILLED{': ' + killer if killer else ''}"
        print(f"R412-4 mutant {mutant}: {cell}")
        if not ok:
            fail(f"a461_{short}_{mutant}.log: expected {cell}")

own = work / "own" / "receipts"
for mutant, killer in OWN.items():
    text, rc = read(own / f"stop_{mutant}.log", f"mutant={mutant}")
    ok = rc == 1 and killer in refusal(text)
    print(f"own {mutant}: {'KILLED' if ok else 'NOT KILLED AS EXPECTED'}: {killer}")
    if not ok:
        fail(f"stop_{mutant}.log: rc={rc}, expected KILLED by {killer}")

if failures:
    print("REVIEW RUNS NOT AS EXPECTED:", *failures, sep="\n  ")
    sys.exit(1)
print(f"REVIEW RUNS AS EXPECTED at {head}: R412-3 {len(R412_3_EARLY)} early probes, 3 whole-gate probes and "
      f"M1-M9; R413-4 N1-N4 and the head, {len(R413_4_EARLY)} plants and 2 N1 plants; R412-4 "
      f"{len(R412_4_PROBES)} probes, 2 whole-gate plants, N0, K0-K8, B1, B2; this round's D0-D3, Q2, Q3, P1, P2")
