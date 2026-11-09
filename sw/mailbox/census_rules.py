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
    # ---- every port of the wrapper (census_ports.py) -------------------------
    "port-unmapped": "a port of the pp_shadow cell no class names fails",
    "port-one-class": "a port two classes name fails",
    "port-stale": "a port row naming a port the wrapper does not declare fails",
    "port-class-d": "class C is exactly the class-D census's population",
    "port-contract": "an F, R or E row's carrier is defined by contract 2.3, an M row's is a port of KL_mbx",
    "port-width": "an F, R or E carrier is as wide as its port, per stream where the row says so, for no more "
                  "streams than the contract carries",
    "g-on-wire": "a G output whose cone reaches the wire fails",
    "g-csr-terminal": "only the G_CSR inputs of the cell csr end a G cone at the CSR block",
    "g-memory-terminal": "only the G_MEMORY datapath outputs end a G cone at the main-memory bridge",
    "g-shim-terminal": "pp_maap_shim ends a G cone only while each of its outputs reaches pp_shadow's inputs alone",
    "g-exclusion-stale": "each net the exclusion names is reached by a G cone of the shape",
    "g-exclusion-amr": "each net the exclusion names is a net of the map writer and restore",
    # ---- the split datapath's control face (census_split.py) ------------------
    "split-placement": "the split datapath holds no KL_pp_shadow, KL_maap or KL_pp_maap_shim cell, none of the "
                       "exclusion's map-writer nets, and one KL_ctrl_split cell",
    "split-unmapped": "a ctl port of the split datapath no row names fails",
    "split-one-class": "a ctl port two classes name fails",
    "split-stale": "a split row naming a port the split datapath does not declare fails",
    "split-contract": "a split row's carrier, and each ruled non-port field, is defined by the contract",
    "split-width": "a split port is as wide as its carrier, CTRL_ENTRIES_P entries of a per-entry carrier",
    "split-every-field": "every publication field and every face field and event is a split row's carrier or "
                         "ruled a non-port",
    "split-face": "each split row stands for wrapper ports of its class and carrier, and every carried wrapper "
                  "port is stood for or ruled",
    "split-drives": "a wrapper output's net is driven by exactly the ports standing for it, bit for bit where one "
                    "port drives it, and a ctl output by the net the wrapper input read",
    "split-tied": "a G output's net and a class-D net the block does not carry are constants in the split, or "
                  "the ruled source",
    "split-frame-block": "KL_ctrl_split carries the wrapper's frame ports and counters net for net, and the M "
                         "rows reach its ports",
    "split-field-reads": "each field read of the census holds in the split and reaches the wire",
    "split-consumed": "every bit of a split input row, for the shape's own entries, reaches a cone end",
    "split-beyond": "no bit of an entry past the shape's own is read",
}

#: The rules the mutation check has removed; empty in every other run.
OFF: set[str] = set()


def live(rule: str) -> bool:
    """Whether rule is enforced in this run; a KeyError for a name RULES does not hold."""
    if rule not in RULES:
        raise KeyError(f"census_rules.RULES names no rule {rule}")
    return rule not in OFF
