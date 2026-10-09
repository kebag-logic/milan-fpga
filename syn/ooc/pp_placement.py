#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Name selected measurement populations without changing acceptance records.

The post-synthesis and post-route census proves engine presence, not firmware
ownership or mailbox wiring. Parent integration must establish those before a
selected image is eligible for measurement (Mark II M0s, issue #640).
"""

from pathlib import Path
import re


PLACEMENTS = ("all-fabric", "f0-f4", "full-split")
MARKER = "# baseline placement: "
REPORT = "baseline_placement.tsv"
HEADER = "placement\trole\tcount"
# Both MAAP implementations must disappear when firmware owns MAAP.
MODULES = {
    "wrapper": "KL_pp_shadow",
    "adp": "KL_adp_engine",
    "acmp-listener": "KL_pp_acmp_listener",
    "acmp-talker": "KL_acmp_talker",
    "srp": "KL_srp_top",
    "maap": "KL_maap",
    "processor-maap": "KL_pp_maap",
    "aecp": "KL_aecp_engine",
    "notify": "KL_aecp_notify",
    "mailbox": "KL_mbx",
    "gptp": "KL_gptp_shadow",
}


def limits(placement: str, role: str) -> tuple[int, int]:
    """Expected shipping, one-interface population at each selected placement."""
    if placement not in PLACEMENTS:
        raise ValueError(f"unknown placement: {placement}")
    if placement == "all-fabric":
        count = 0 if role in ("mailbox", "processor-maap") else 1
        return count, count
    if role in ("mailbox", "gptp"):
        return 1, 1
    if placement == "f0-f4":
        if role == "wrapper":
            return 0, 1  # AECP may remain wrapped or be instantiated directly.
        if role in ("aecp", "notify"):
            return 1, 1
    return 0, 0


def selection(script: str, requested: str) -> bool:
    """Require explicit split intent; legacy recipes identify only all-fabric."""
    if requested not in PLACEMENTS:
        raise ValueError(f"unknown placement: {requested}")
    markers = [line[len(MARKER):] for line in script.splitlines() if line.startswith(MARKER)]
    if not markers and requested == "all-fabric":
        return False
    if markers != [requested]:
        raise ValueError(f"wrong placement: requested {requested}, recipe names {markers or 'all-fabric'}")
    return True


def validate(directory: Path, script: str, requested: str) -> None:
    """Refuse incomplete, duplicated or wrong-placement engine censuses by name."""
    if not selection(script, requested):
        return
    lines = (directory / REPORT).read_text().splitlines()
    if not lines or lines[0] != HEADER:
        raise ValueError(f"placement {requested}: missing {REPORT} header")
    counts = {}
    for line in lines[1:]:
        fields = line.split("\t")
        if len(fields) != 3 or fields[0] != requested:
            raise ValueError(f"wrong placement row: {line!r}; expected {requested}")
        _, role, value = fields
        if role not in MODULES or role in counts or not re.fullmatch(r"[0-9]{1,15}", value):
            raise ValueError(f"placement {requested}: invalid or duplicate role/count: {line!r}")
        counts[role] = int(value)
    if counts.keys() != MODULES.keys():
        raise ValueError(f"placement {requested}: missing roles {sorted(MODULES.keys() - counts.keys())}")
    for role, count in counts.items():
        low, high = limits(requested, role)
        if not low <= count <= high:
            raise ValueError(f"wrong placement {requested}: {role} ({MODULES[role]}) count {count}, "
                             f"expected {low}..{high}")


def census_tcl(placement: str, report: bool = False) -> str:
    """Check actual retained module identities; optionally retain the final census."""
    lines = [f"set baseline_placement {{{placement}}}"]
    if report:
        lines += [f"set placement_file [open {REPORT} w]", f'puts $placement_file "{HEADER}"']
    for role, module in MODULES.items():
        low, high = limits(placement, role)
        lines += [
            "set placement_cells [get_cells -quiet -hier -filter "
            f"{{ORIG_REF_NAME == {module} || REF_NAME == {module}}}]",
            "set placement_count [llength $placement_cells]",
            f"if {{$placement_count < {low} || $placement_count > {high}}} {{",
            f'  error "wrong placement {placement}: {role} ({module}) count $placement_count, expected {low}..{high}"',
            "}",
        ]
        if report:
            lines.append(f'puts $placement_file "{placement}\t{role}\t$placement_count"')
    if report:
        lines.append("close $placement_file")
    return "\n".join(lines) + "\n"


def scope_timing_tcl() -> str:
    """Report image-internal timing without assuming a protocol wrapper exists."""
    return '''
set regs [get_cells -hier -filter {IS_SEQUENTIAL == 1}]
set worst [get_timing_paths -from $regs -to $regs -max_paths 1]
if {[llength $worst] != 1} { error "No internal timing path for selected image" }
set tf [open baseline_scope_timing.tsv w]
puts $tf "instance\\tsequential_cells\\tinternal_WNS_ns"
puts $tf "image\\t[llength $regs]\\t[get_property SLACK $worst]"
close $tf
'''
