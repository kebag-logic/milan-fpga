#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
tsn-gen protocol-model access — the field/constraint oracle for the campaign.

tsn-gen carries the SPEC FIELD MODEL of every 1722.1 PDU: each field's bit
width plus its spec constraint (`expected:` value / values / range / mask,
exactly ONE kind per field -- see `kind_conflict`). This module turns that
model into test material:

  * `Message.fields`          ordered (name, bits, constraint) for a PDU
  * `Message.legal(field)`    spec-LEGAL probe values for one field
  * `Message.illegal(field)`  spec-ILLEGAL probe values for one field
  * `Message.random(n, seed)` constrained-random field sets via `packet_gen`
                              (reproducible: same seed -> same sequence)
  * `decode_pdu(...)`         packet_gen's independent dissection of bytes

Why a model instead of hand-written cases: the constraint lives with the
spec, so a field added or re-scoped in tsn-gen automatically grows the
campaign, and every probe traces to a normative statement rather than to a
test author's memory.

WIRE-LAYOUT CAVEAT — measured 2026-07-25, do not delete
-------------------------------------------------------
tsn-gen's 1722.1 PDU models omit the AVTPDU `sv`(1) + `version`(3) nibble:
the ADP model declares 532 bits where the real ADPDU-after-subtype is 536,
and every `atdecc_aecp_*` model re-declares `message_type` that the
`avtp_control_header` layer already spent a byte on. Consequences, both
reproduced against real frames:

  * a `--stack-file` frame is 4 bits WIDE of the real wire after the AVTP
    header (a real READ_DESCRIPTOR decodes control_data_length=320 instead
    of 20, command_type=64 instead of 4);
  * the same model applied at the real PDU offset is 4 bits SHORT.

So the models are used here as the FIELD/CONSTRAINT oracle only. Bytes on
the wire are built and parsed by `wire.py`, whose layout is the one the
silicon-proven RTL testbenches and the deployed boards use. `decode_pdu()`
re-inserts the missing nibble so tsn-gen still cross-checks field VALUES as
an independent decoder.
"""
import json
import os
import subprocess

import yaml

TSN_GEN_ROOT = os.environ.get("TSN_GEN_ROOT", os.path.expanduser("~/tsn-gen"))
PACKET_GEN = os.environ.get(
    "PACKET_GEN", os.path.join(TSN_GEN_ROOT, "build", "traffic-gen", "packet_gen"))
#: repo-local protocol models (ACMP lives here, not in tsn-gen)
REPO_PROTOCOLS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tests", "protocols")


def available():
    """True when the tsn-gen binary and model tree are usable."""
    return os.path.isfile(PACKET_GEN) and os.access(PACKET_GEN, os.X_OK)


#: the constraint kinds the model grammar allows under `expected:`. Upstream
#: reads exactly these four (tsn-gen parser/src/protocol.cpp) and nothing else.
CONSTRAINT_KINDS = ("value", "values", "range", "mask")


def kind_conflict(name, con):
    """ONE CONSTRAINT KIND PER FIELD, decided here and nowhere else (#151).

    `con` is a field's `expected:` mapping. Returns None when it declares at
    most one kind, else the refusal message naming the field and every kind
    it declares. Every reader that dispatches on the kind -- `legal()`,
    `illegal()` and fuzz_ptp's `grade_tx()` -- asks this first, so a field
    carrying two kinds is refused the same way by all three instead of being
    resolved three ways.

    Why refuse rather than merge: the producer resolves a combination by its
    own precedence (packet_builder.cpp::pickValue draws from value+values if
    either is present, else from range, and applies mask only to an
    unconstrained draw), and every consumer here used to take the first kind
    the if/elif chain met. Those agree only while no field declares two; the
    day one did, a frame the generator calls legal would be graded RED and
    the failure would blame the DUT. There is no meaning for a field carrying
    two kinds that three components could be trusted to share, so the
    ambiguity is refused at the source rather than re-resolved.

    Every key of the mapping counts as a declared kind. A key outside the
    grammar already fails closed in grade_tx when it stands alone (#146);
    beside a known kind it used to be ignored in silence, and now it is
    refused by this rule with its name in the message.
    """
    kinds = sorted(con)
    if len(kinds) < 2:
        return None
    return ("field %s declares %d constraint kinds (%s); a field takes exactly "
            "one of %s, so it is refused"
            % (name, len(kinds), ", ".join(kinds), "/".join(CONSTRAINT_KINDS)))


class Message:
    """One PDU's spec field model, loaded from its tsn-gen YAML."""

    def __init__(self, yaml_path, interface=None, yaml_dir=None):
        self.path = yaml_path
        with open(yaml_path) as fh:
            doc = yaml.safe_load(fh)
        self.service = doc["service"]
        self.yaml_dir = yaml_dir or os.path.dirname(yaml_path)
        #: {name: (bits, constraint-dict)} in declaration order
        self.vars = {}
        for v in doc.get("vars", []):
            self.vars[v["var"]] = (int(v["size"]), v.get("expected", {}) or {})
        # the interface fixes WHICH vars appear, in wire order
        self.interface = interface or self._first_interface(doc)
        self.order = self._iface_vars(doc, self.interface)

    # ---------------------------------------------------------------- model
    @staticmethod
    def _first_interface(doc):
        for ent in doc.get("entities", []):
            for iface in ent.get("interfaces", []):
                return "%s::%s::%s" % (doc["service"], ent["entity"], iface["interface"])
        raise ValueError("no interface in model")

    def _iface_vars(self, doc, qualified):
        want = qualified.split("::")[-1]
        for ent in doc.get("entities", []):
            for iface in ent.get("interfaces", []):
                if iface["interface"] == want:
                    return [v["var_ref"] for v in iface.get("vars", [])]
        raise ValueError("interface %s not in %s" % (want, self.path))

    @property
    def fields(self):
        """[(name, bits, constraint)] in wire order."""
        return [(n, self.vars[n][0], self.vars[n][1]) for n in self.order
                if n in self.vars]

    def width(self, name):
        return self.vars[name][0]

    def mask(self, name):
        return (1 << self.vars[name][0]) - 1

    # --------------------------------------------------------------- probes
    def legal(self, name):
        """Spec-LEGAL probe values for one field (deduped, width-clamped).

        Raises ValueError when the field declares more than one constraint
        kind: `kind_conflict` is the one rule, and this is one of its readers.
        """
        bits, exp = self.vars[name]
        refused = kind_conflict(name, exp)
        if refused:
            raise ValueError(refused)
        full = (1 << bits) - 1
        out = []
        if "value" in exp:
            out = [int(exp["value"])]
        elif "values" in exp:
            out = [int(v) for v in exp["values"]]
        elif "range" in exp:
            lo, hi = int(exp["range"][0]), int(exp["range"][1])
            out = sorted({lo, (lo + hi) // 2, hi})
        elif "mask" in exp:
            m = int(exp["mask"][0])
            # 0, the full defined set, and each single defined bit
            out = [0, m] + [1 << b for b in range(bits) if m & (1 << b)]
        else:
            # unconstrained: exercise the width's corners
            out = [0, 1, full // 2, full]
        return sorted({v & full for v in out})

    def illegal(self, name):
        """Spec-ILLEGAL probe values (empty when the field is unconstrained).

        Raises ValueError on a field declaring more than one kind, exactly as
        `legal()` does and for the same reason.
        """
        bits, exp = self.vars[name]
        refused = kind_conflict(name, exp)
        if refused:
            raise ValueError(refused)
        full = (1 << bits) - 1
        out = []
        if "value" in exp:
            v = int(exp["value"])
            out = [x for x in (v + 1, v ^ full, full, 0) if x != v]
        elif "values" in exp:
            ok = {int(v) for v in exp["values"]}
            out = [x for x in range(0, min(full, 255) + 1) if x not in ok][:6]
            if full > 255 and full not in ok:
                out.append(full)
        elif "range" in exp:
            lo, hi = int(exp["range"][0]), int(exp["range"][1])
            out = [x for x in (lo - 1, hi + 1, full) if 0 <= x <= full and not lo <= x <= hi]
        elif "mask" in exp:
            m = int(exp["mask"][0])
            undef = (~m) & full
            if undef:
                out = [undef] + [1 << b for b in range(bits) if undef & (1 << b)][:4]
        return sorted({v & full for v in out})

    # ------------------------------------------------------- random via CLI
    def random(self, count, seed):
        """Constrained-random field sets straight from packet_gen (reproducible)."""
        cmd = [PACKET_GEN, "--yaml-dir", self.yaml_dir, "--interface", self.interface,
               "--count", str(count), "--seed", str(seed), "--output", "json"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        out = []
        for line in res.stdout.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                out.append(json.loads(line)["fields"])
            except (ValueError, KeyError):
                continue
        return out


def decode_pdu(yaml_dir, interface, pdu_bytes):
    """packet_gen's independent dissection of a REAL PDU (offset-corrected).

    `pdu_bytes` starts at the AVTPDU byte holding sv/version/message_type.
    The model omits sv+version (see the module caveat), so the nibble is
    stripped before handing the bytes over: shift the whole PDU left 4 bits
    and the model's first field (message_type) lands on the real one.
    """
    if not pdu_bytes:
        return {}
    n = int.from_bytes(pdu_bytes, "big")
    # shift the whole PDU left one nibble: the sv+version bits fall off the
    # top and the model's first field (message_type) lands on the real one.
    # Verified 2026-07-25: with this correction tsn-gen decodes a real
    # READ_DESCRIPTOR exactly (message_type/status/CDL/command_type/seq).
    n = (n << 4) & ((1 << (len(pdu_bytes) * 8)) - 1)
    shifted = n.to_bytes(len(pdu_bytes), "big")
    cmd = [PACKET_GEN, "--yaml-dir", yaml_dir, "--interface", interface,
           "--decode", "--hex", shifted.hex()]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return {}
    for line in res.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if "fields" in d:
            return d["fields"]
        for lyr in d.get("layers", []):
            if lyr.get("fields"):
                return lyr["fields"]
    return {}


def decode_ptp(yaml_dir, interface, pdu_bytes):
    """packet_gen's independent dissection of an 802.1AS PDU — NO shift.

    The missing-nibble caveat above is a 1722.1 defect only: the 8021as_*
    models declare the FULL common header from transport_specific down, so
    the model layout and the wire layout agree bit-for-bit (measured
    2026-08-19: a wire.py Sync decodes exactly — seq, flags, identity).
    `pdu_bytes` starts at the header byte holding transportSpecific.
    """
    if not pdu_bytes:
        return {}
    cmd = [PACKET_GEN, "--yaml-dir", yaml_dir, "--interface", interface,
           "--decode", "--hex", bytes(pdu_bytes).hex()]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return {}
    for line in res.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if "fields" in d:
            return d["fields"]
        for lyr in d.get("layers", []):
            if lyr.get("fields"):
                return lyr["fields"]
    return {}


# ------------------------------------------------------------------ catalogue
AECP_DIR = os.path.join(TSN_GEN_ROOT, "protocols", "application", "1722_1", "aecp")
ADP_DIR = os.path.join(TSN_GEN_ROOT, "protocols", "application", "1722_1", "adp")
AVTP_DIR = os.path.join(TSN_GEN_ROOT, "protocols", "data_link", "1722")
PTP_DIR = os.path.join(TSN_GEN_ROOT, "protocols", "data_link", "ptp")
ACMP_DIR = os.path.join(REPO_PROTOCOLS, "acmp")


def load(kind, yaml_name, interface=None):
    """Load a model by family: 'aecp' | 'adp' | 'avtp' | 'ptp' | 'acmp'."""
    d = {"aecp": AECP_DIR, "adp": ADP_DIR, "avtp": AVTP_DIR, "ptp": PTP_DIR,
         "acmp": ACMP_DIR}[kind]
    return Message(os.path.join(d, yaml_name), interface, yaml_dir=d)
