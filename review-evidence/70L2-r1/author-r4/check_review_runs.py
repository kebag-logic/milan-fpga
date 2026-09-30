#!/usr/bin/env python3
"""Assert the outcome of every round-3 review probe and census mutant run at one head.

usage: check_review_runs.py <repo> <receipts>
<receipts> holds the logs R412-3's probe_all.sh (early and full modes) and
census_mutants_run.sh wrote, run unchanged from a copy of that review's scripts,
plus this round's probe_a460.sh logs. Every log must name <repo>'s HEAD. Exit 0
only when each probe is accepted or refused as the table below states, each
refusal naming the text listed, every census mutant M1-M9 is KILLED (M9 by the
interior-byte break), and the whole gate 1b passes the unplanted head with the
slot kept, 15/15 breaks refused and the interior byte printed.
"""
import re
import subprocess
import sys
from pathlib import Path

repo, receipts = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True,
                      text=True).stdout.strip()
WRITE = "a store lands on aem_loaded's storage other than milan_init()'s one store"
ESCAPE = "the linked image forms the full address of aem_loaded's storage"
NAME = "another symbol of the linked image is on aem_loaded's storage"
ADDRESS = "the address of aem_loaded is taken"
SOURCE_WRITE = "aem_loaded must contain only the image verifier's verdict"
IMAGE_PINS = (WRITE, ESCAPE, NAME, ADDRESS)
ACCEPTED = None
#: probe -> ACCEPTED, or (texts the refusal must carry, image pins it must NOT name)
EARLY = {
    "base": ACCEPTED, "nbr_after_sscanf": ACCEPTED, "arr_overrun_sscanf": ACCEPTED,
    "nbr_runtime_sscanf": ACCEPTED, "pre_overrun_sscanf": ACCEPTED,
    "plain_write": ((SOURCE_WRITE,), ()), "bcp_write": ((SOURCE_WRITE,), ()),
    "pie_write": ((SOURCE_WRITE,), ()), "optimize_write": ((SOURCE_WRITE,), ()),
    "block_extern_sscanf": (("the address of aem_loaded must not be taken",), ()),
    "nbr_runtime_store": (("a STORE this gate cannot PLACE",), ()),
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
OWN = {"unit_under_store": ACCEPTED, "unit_over_store": ACCEPTED,
       "interior_const": ((ESCAPE,), (WRITE, NAME, ADDRESS))}
FULL = ("base", "nbr_runtime_sscanf", "pre_overrun_sscanf")
MUTANTS = ("M1_no_escape", "M2_no_name", "M3_no_local", "M4_no_auipc", "M5_no_image_store",
           "M6_no_resolver_store", "M7_addi_in_place", "M8_no_image", "M9_by_name_only")
failures = []


def read(name: str, first: str) -> tuple[str, int | None]:
    """The log `name` and its exit code, after checking it names this head."""
    text = (receipts / name).read_text(errors="replace")
    if not text.startswith(f"{first} head={head}"):
        failures.append(f"{name}: not a run at {head}")
    codes = re.findall(r"(?m)^rc=(\d+)$", text)
    return text, int(codes[-1]) if codes else None


def early(name: str, probe: str, want: tuple[tuple[str, ...], tuple[str, ...]] | None) -> str:
    """Check one early-mode probe log against `want`; return its table cell."""
    text, rc = read(name, f"probe={probe}")
    if want is ACCEPTED:
        ok = rc == 0 and "R412 gate-1b verdict ran=True kept=['aem_loaded']" in text
        cell = "ACCEPTED, kept=['aem_loaded']"
    else:
        refusal = "\n".join(line for line in text.splitlines() if line.startswith("GATE1B REFUSED"))
        must, must_not = want
        ok = rc == 1 and all(t in refusal for t in must) and not any(t in refusal for t in must_not)
        cell = "REFUSED, naming " + "; ".join(t[:48] for t in must)
    if not ok:
        failures.append(f"{name}: rc={rc}, expected {cell}")
    return cell


for probe, want in EARLY.items():
    print(f"early {probe}: {early(f'gate1b_early_{probe}.log', probe, want)}")
for probe, want in OWN.items():
    print(f"early (this round) {probe}: {early(f'gate1b_early_a460_{probe}.log', probe, want)}")
for probe in FULL:
    text, rc = read(f"gate1b_full_{probe}.log", f"probe={probe}")
    passed = rc == 0 and "GATE1B PASS" in text and \
        "kept the slot of aem_loaded across a call" in text
    if probe == "base":
        passed = passed and "refused 15/15 planted pin breaks on the verdict" in text and \
            "reaching it only at byte(s) +1 of its storage" in text
    print(f"full {probe}: {'GATE1B PASS, slot kept' if passed else 'NOT AS EXPECTED'}")
    if not passed:
        failures.append(f"gate1b_full_{probe}.log: rc={rc}, expected the whole gate 1b to pass")
for mutant in MUTANTS:
    text, rc = read(f"census_mutant_{mutant}.log", f"mutant={mutant}")
    refusal = next((line for line in text.splitlines() if line.startswith("GATE1B REFUSED")), "")
    killed = rc == 1 and bool(refusal)
    if mutant == "M9_by_name_only":
        killed = killed and "accepted a neighbour's address folded onto an interior byte" in refusal
    print(f"mutant {mutant}: {'KILLED' if killed else 'SURVIVED'}: {refusal[16:200]}")
    if not killed:
        failures.append(f"census_mutant_{mutant}.log: rc={rc}, expected KILLED")
if failures:
    print("REVIEW RUNS NOT AS EXPECTED:", *failures, sep="\n  ")
    sys.exit(1)
print(f"REVIEW RUNS AS EXPECTED at {head}: {len(EARLY)} review probes and {len(OWN)} of this round's "
      f"early, {len(FULL)} through the whole gate 1b, and census mutants M1-M9 all killed")
