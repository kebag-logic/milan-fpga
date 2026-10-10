# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""census_rules.py - every rule of the publication census, each a switch its self-test removes in turn.

Each rule census_elab.py and publication_census.py state is named here once
and enforced at the places that test ``live(name)``, and nowhere else. The
self-test's mutation check (census_selftest.py) removes each rule in turn,
judges again every arm planted against it, and fails unless at least one of
those arms is then accepted: a rule whose loss no arm notices is a rule the
self-test does not prove, and that fails CI (#665, comment 6100024293). A
name tested in the census's code but missing here, or named here and tested
nowhere, fails the same check.
"""

from __future__ import annotations

RULES = {
    # ---- the shapes ---------------------------------------------------------
    "shapes": "--check elaborates every configs/*.yaml the builder builds, beside the recipe's own shape",
    "shape-params": "a configuration's shape binds the datapath parameters the builder states for it",
    "shape-header": "a configuration's shape reads its generated header directory in place of the recipe's",
    "same-across-shapes": "every shape has the same population, the same reads and, per read, the same "
                          "classes of cone end",
    # ---- the tools ----------------------------------------------------------
    "pins": "sv2v and Yosys are the versions .github/workflows/rtl-fast.yml pins",
    "opener-guard": "an escaped name holding // or /* is refused before elaboration",
    "keep-names": "insbuf runs before proc_prune, before proc_dff and last, and proc's closing opt_expr does "
                  "not, so every read keeps its source name",
    # ---- the population -----------------------------------------------------
    "one-wrapper": "the datapath holds one KL_pp_shadow cell, named pp_shadow",
    "csr-cell": "the datapath holds a milan_csr cell named csr",
    "face-listed": "an output under a class-D heading of the wrapper's port list that CLASS_D_PORTS lacks fails",
    "face-declared": "a CLASS_D_PORTS entry the wrapper's class-D face does not declare fails",
    "face-placed": "an output the wrapper's port list names twice, or never, fails",
    "started-port": "the wrapper declares the started level's port, aecp_strm_started_o",
    "port-connected": "each class-D port is connected",
    "port-one-net": "each class-D port drives one whole named net",
    "ports-distinct": "no two class-D ports drive one net",
    "sole-driver": "a population net has no driver but its class-D port",
    "two-drivers": "no bit of the datapath has two drivers",
    # ---- the cone -----------------------------------------------------------
    "every-input": "a cell leads from every input bit, a select, enable or clock included, to every output bit",
    "memory": "a memory's write leads to its reads",
    "output-is-wire": "a datapath output is the wire",
    "no-output-end": "a cell with no output is the wire",
    "terminal-cell": "only the cells csr and pp_shadow, each of its module, end a cone short of the wire",
    "csr-readback": "only the CSR_READBACK inputs of csr end a cone as CSR read-back",
    "processor-face": "only the PROCESSOR_FACE inputs of pp_shadow end a cone as the processor's answer face",
    # ---- the census ---------------------------------------------------------
    "unmapped": "a read no row names fails",
    "unknown-field": "a row naming a field the publication block does not define fails",
    "field-on-wire": "a field row whose read reaches no wire fails",
    "off-wire": "a status or processor row whose read reaches the wire fails",
    "status-not-processor": "a status row whose read reaches the processor wrapper fails",
    "stale-row": "a row no read matches fails",
}

#: The rules the mutation check has removed; empty in every other run.
OFF: set[str] = set()


def live(rule: str) -> bool:
    """Whether rule is enforced in this run; a KeyError for a name RULES does not hold."""
    if rule not in RULES:
        raise KeyError(f"census_rules.RULES names no rule {rule}")
    return rule not in OFF
