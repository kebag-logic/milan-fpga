#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mermaid diagrams of the mechanisms the register reference explains (#797).

Every label is read from the model or checked against the source it shows: a
register's offset, a bit's position, the unlock key and a state name. A label
the RTL no longer backs is a refusal, so a diagram cannot outlive its mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass

from register_fields import Field, Register
from register_page import Model, acronym
from register_rtl import read_text
from register_sv import Refusal

LINK_GUARD = "hdl/common/KL_link_guard.sv"
SERVO = "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"


@dataclass
class Mechanism:
    """One diagram: where it goes, what it shows, the prose that explains it."""
    module: str
    title: str
    kind: str
    text: list[str]
    lines: list[str]


class Labels:
    """Diagram labels, each checked against the model as it is read."""

    def __init__(self, model: Model) -> None:
        self.model = model
        self.regs = {r.label: r for r in model.registers}

    def reg(self, label: str) -> Register:
        """A register the diagram names, or a refusal."""
        if label not in self.regs:
            raise Refusal(f"a mechanism diagram names register {label}, which the RTL lacks")
        return self.regs[label]

    def word(self, label: str) -> str:
        """`ACRONYM (0xNNN)`."""
        reg = self.reg(label)
        return f"{acronym(reg, self.model.descriptions)} (0x{reg.offset:03X})"

    def name(self, label: str) -> str:
        """The register's documented acronym."""
        return acronym(self.reg(label), self.model.descriptions)

    def field_at(self, label: str, bit: int) -> Field:
        """The field holding a bit, with write or read behaviour checked by the caller."""
        reg = self.reg(label)
        found = next((f for f in reg.fields if f.lo <= bit <= f.hi), None)
        if found is None:
            raise Refusal(f"a mechanism diagram names {label}[{bit}], which the RTL lacks")
        return found

    def bit(self, label: str, bit: int, access: str) -> str:
        """`ACRONYM[bit]`, refused unless the bit has the access the diagram assumes."""
        found = self.field_at(label, bit)
        if access not in found.access:
            raise Refusal(f"a mechanism diagram uses {label}[{bit}] as {access}; the RTL makes it {found.access}")
        return f"{self.name(label)}[{bit}]"

    def constant(self, name: str) -> str:
        """An RTL constant in hex."""
        return f"0x{self.model.wording.facts.sym.value(name):X}"

    def source_tokens(self, path: str, tokens: tuple[str, ...]) -> None:
        """A state name a diagram draws must still exist in the source it shows."""
        text = read_text(self.model.root, path)
        for token in tokens:
            if token not in text:
                raise Refusal(f"a mechanism diagram names {token}, which {path} lacks")

    def unlock_key(self) -> str:
        """ETH_GUARD's unlock word, from its write decode."""
        for effect in self.reg("ETH_GUARD").side_effects:
            kind, _, rest = effect.partition(":")
            if kind == "magic":
                return f"0x{int(rest.split(':', 1)[0], 16):08X}"
        raise Refusal("a mechanism diagram needs ETH_GUARD's unlock word, which its write decode lacks")


def read_path(lab: Labels) -> Mechanism:
    """Where a read's value comes from."""
    lab.reg("ID")
    return Mechanism("reading", "How a read is served", "flowchart", [
        "A read takes one of three paths. The address decides which.",
        "The shadow path serves plain-RW words from RAM. The defaults ROM loads it at reset.",
        "The live path reads status words from their source.",
    ], ["flowchart LR",
        "    A[AXI read] --> D{Address decode}",
        "    D -->|plain-RW or ROM word| S[Shadow RAM]",
        "    D -->|live arm or window word| L[Live read mux]",
        "    D -->|slow window word| C[Stream context RAM]",
        "    S --> R[Read data]",
        "    L --> R",
        "    C --> R",
        "    O[Defaults ROM] -->|sweep after reset| S"])


def stats_snapshot(lab: Labels) -> Mechanism:
    """The coherent statistics snapshot."""
    snap = lab.bit("STATS_CTRL", 0, "W1S")
    return Mechanism("stats", "How a statistics snapshot works", "sequenceDiagram", [
        "A snapshot makes the counters one coherent set.",
    ], ["sequenceDiagram",
        "    participant SW as Software",
        "    participant CSR as CSR block",
        "    participant MAC as MAC counters",
        f"    SW->>CSR: write 1 to {snap}",
        "    CSR->>MAC: pulse o_stats_snapshot",
        "    MAC-->>CSR: i_stats loaded into the snapshot",
        f"    SW->>CSR: read {lab.word('STATS_CAP')}",
        f"    SW->>CSR: read {lab.name('STATS')} words from 0x{lab.reg('STATS').offset:03X}"])


def tcam_commit(lab: Labels) -> Mechanism:
    """Writing one TCAM entry."""
    commit = lab.bit("TCAM_CMD", 16, "W1S")
    return Mechanism("tcam", "How a TCAM entry is written", "sequenceDiagram", [
        "The key, mask and action words are shadows. The commit moves them into one entry.",
    ], ["sequenceDiagram",
        "    participant SW as Software",
        "    participant CSR as CSR block",
        "    participant TCAM as RX filter",
        f"    SW->>CSR: write {lab.word('TCAM_KLO')}, {lab.word('TCAM_KHI')}",
        f"    SW->>CSR: write {lab.word('TCAM_MLO')}, {lab.word('TCAM_MHI')}",
        f"    SW->>CSR: write {lab.word('TCAM_ACT')}",
        f"    SW->>CSR: write {lab.word('TCAM_CMD')}: index, valid and {commit}",
        "    CSR->>TCAM: pulse o_tcam_wr_en with the key, mask and action"])


def link_guard(lab: Labels) -> Mechanism:
    """The link guard's episode."""
    lab.source_tokens(LINK_GUARD, ("RUN_S", "HOLD_S", "SETTLE_S"))
    return Mechanism("link", "How the link guard recovers", "stateDiagram-v2", [
        f"`{lab.name('LINKG_STAT')}[5:4]` reports this state.",
        "The MAC side is held in reset through `HOLD` and `SETTLE`.",
    ], ["stateDiagram-v2",
        "    [*] --> RUN",
        "    RUN --> HOLD: a clock dies",
        "    HOLD --> SETTLE: clocks back",
        "    SETTLE --> RUN: clean for SETTLE_CYC_C cycles"])


def eth_guard(lab: Labels) -> Mechanism:
    """The guard's two states."""
    key = lab.unlock_key()
    field = lab.field_at("ETH_GUARD", 0)
    if lab.reg("ETH_GUARD").reset_bits[0] != 1:
        raise Refusal("the ETH_GUARD diagram draws an armed reset; the RTL resets it disarmed")
    return Mechanism("guard", "How the guard arms and disarms", "stateDiagram-v2", [
        f"`{lab.name('ETH_GUARD')}[0]` is 1 while armed.",
        f"While armed, `{lab.name('PHY_RST')}` writes drop and `{lab.name('LINK_CTRL')}[1]` stores 0.",
    ], ["stateDiagram-v2",
        f"    [*] --> Armed: reset ({field.name} = 1)",
        f"    Armed --> Disarmed: write {key}",
        "    Disarmed --> Armed: write any other word",
        "    Armed --> Armed: write any other word"])


def stream_window(lab: Labels) -> Mechanism:
    """Select, snapshot, poll, read."""
    busy = lab.bit("STRM_SNAP", 0, "W1S")
    return Mechanism("strm", "How a stream snapshot is read", "sequenceDiagram", [
        "Select the stream and arm the snapshot. Poll busy, then read the block.",
    ], ["sequenceDiagram",
        "    participant SW as Software",
        "    participant CSR as CSR block",
        "    participant CTX as Stream context",
        f"    SW->>CSR: write {lab.word('STRM_SEL')}",
        f"    SW->>CSR: write 1 to {busy}",
        f"    CSR->>CTX: latch {lab.name('STRMW_STATE')}, {lab.name('STRMW_CNT')} and {lab.name('STRMW_PDUS')}",
        "    loop until the bit reads 0",
        f"        SW->>CSR: read {busy}",
        "    end",
        f"    SW->>CSR: read {lab.word('STRMW_STATE')} and the block"])


def latency_chain(lab: Labels) -> Mechanism:
    """The latency taps' two chains."""
    lab.reg("LTAP")
    return Mechanism("ltap", "Where the latency taps measure", "flowchart", [
        "Each chain records the delta between neighbouring stages.",
    ], ["flowchart LR",
        "    subgraph TX",
        "    T0[CAP] --> T1[PKT_SOF] --> T2[PKT_EOF] --> T3[MAC_TX]",
        "    end",
        "    subgraph RX",
        "    R0[MAC_RX] --> R1[ACCEPT] --> R2[DEPKT] --> R3[FABRIC_RENDER]",
        "    end"])


def servo(lab: Labels) -> Mechanism:
    """The media-clock servo's states."""
    lab.source_tokens(SERVO, ("IDLE_S", "VERIFY_S", "REPAIR_S", "ACQUIRE_S", "LOCKED_S", "HOLDOVER_S", "FAULT_S"))
    return Mechanism("mcsrv", "How the servo moves between states", "stateDiagram-v2", [
        f"`{lab.name('MCSRV_STAT')}[2:0]` reports this state.",
        "Deselecting the source returns any state to `IDLE`.",
    ], ["stateDiagram-v2",
        "    [*] --> IDLE",
        "    IDLE --> VERIFY: source selected and reference locked",
        "    VERIFY --> REPAIR: mismatch and auto-repair set",
        "    VERIFY --> ACQUIRE: verified",
        "    REPAIR --> ACQUIRE: reprogrammed",
        "    REPAIR --> FAULT: relock timeout",
        "    ACQUIRE --> LOCKED: inside the lock threshold",
        "    LOCKED --> ACQUIRE: lock count falls to 0",
        "    ACQUIRE --> HOLDOVER: reference unlocked",
        "    LOCKED --> HOLDOVER: reference unlocked",
        "    HOLDOVER --> ACQUIRE: reference back"])


def chmap_readback(lab: Labels) -> Mechanism:
    """Arm and read a channel-map entry."""
    arm = lab.bit("CHMAP_SNAP", 0, "W1S")
    return Mechanism("chmap", "How a map entry is read back", "sequenceDiagram", [
        f"`{lab.name('CHMAP_LOOP')}` reads the poison until a snapshot completes.",
        f"The watchdog gives up after {lab.constant('CHMAP_RD_WDOG_C')} clocks.",
    ], ["sequenceDiagram",
        "    participant SW as Software",
        "    participant CSR as CSR block",
        "    participant MAP as Map RAM",
        f"    SW->>CSR: write {lab.word('CHMAP_SEL')}",
        f"    SW->>CSR: write 1 to {arm}",
        "    CSR->>MAP: o_chmap_rd_en with side and index",
        "    alt the fabric answers",
        "        MAP-->>CSR: i_chmap_rd_valid and the data",
        f"        SW->>CSR: read {lab.word('CHMAP_LOOP')}",
        "        CSR-->>SW: the measurement, VALID = 1",
        "    else the watchdog expires",
        f"        SW->>CSR: read {lab.word('CHMAP_LOOP')}",
        f"        CSR-->>SW: {lab.constant('CHMAP_LOOP_POISON_C')}",
        "    end"])


def side_port(lab: Labels) -> Mechanism:
    """The posted side-port read."""
    busy = lab.bit("PP_STAT", 0, "R")
    return Mechanism("pp", "How a side-port read is posted", "sequenceDiagram", [
        "The side port is posted. One access is outstanding at a time.",
        f"A write to `{lab.name('PP_SPDATA')}` posts a write the same way.",
    ], ["sequenceDiagram",
        "    participant SW as Software",
        "    participant CSR as CSR block",
        "    participant PP as Protocol processor",
        f"    SW->>CSR: write {lab.word('PP_SPADDR')}",
        "    CSR->>PP: o_pp_req with the address",
        "    loop until the bit reads 0",
        f"        SW->>CSR: read {busy}",
        "    end",
        "    PP-->>CSR: i_pp_ack and i_pp_rdata",
        f"    SW->>CSR: read {lab.word('PP_SPDATA')}"])


BUILDERS = (read_path, stats_snapshot, tcam_commit, link_guard, eth_guard, stream_window, latency_chain, servo,
            chmap_readback, side_port)


def mechanisms(model: Model) -> list[Mechanism]:
    """Every generated mechanism diagram, in page order."""
    lab = Labels(model)
    return [build(lab) for build in BUILDERS]
