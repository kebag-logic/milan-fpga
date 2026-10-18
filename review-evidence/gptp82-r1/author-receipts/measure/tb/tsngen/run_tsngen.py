#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""tsn-gen cross-check of the gPTP engine, both wire directions.

Frames the engine TRANSMITS are decoded by tsn-gen's packet_gen against
the 802.1AS protocol YAMLs (the same tool that validates the reference
embedded peer) and every field the standard pins is enforced from the YAML's
own `expected` values — an independent implementation of the bit
layout, not this repo's C++ mirror. Frames packet_gen GENERATES (seeded,
reproducible) are fed into the engine and the published outcome is
checked against a Python model of BTCA-lite and the offset arithmetic.

Skips cleanly (exit 0) when the tsn-gen checkout or binary is absent —
set TSAGEN_DIR to the checkout (default: ~/prjs/tsn-gen, then
~/tsn-gen).
"""

import json
import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUR_MAC = 0x02A1B2C3D4E5
OUR_CID = 0x02A1B2FFFEC3D4E5
OUR_CQ = 0xF8FE436A
PD_NS = 700


# ---------------------------------------------------------------------------
# tsn-gen location — the milan-fpga convention (TSAGEN_DIR), skip clean
# ---------------------------------------------------------------------------
def _tsagen_root() -> Path | None:
    """The tsn-gen checkout to cross-check against, or None when there is none.

    TSAGEN_DIR is taken as given even when it names nothing, so a typo skips
    with the reason rather than silently cross-checking against whichever
    default checkout happens to exist.
    """
    named = os.environ.get("TSAGEN_DIR", "")
    if named:
        return Path(named)
    for cand in ("~/prjs/tsn-gen", "~/tsn-gen"):
        root = Path(cand).expanduser()
        if root.is_dir():
            return root
    return None


TSAGEN = _tsagen_root()
PG = TSAGEN / "build/traffic-gen/packet_gen" if TSAGEN else None
YD = TSAGEN / "protocols/data_link/ptp" if TSAGEN else None
if not (PG and PG.is_file() and YD and YD.is_dir()):
    print("SKIP: tsn-gen checkout/binary not found (set TSAGEN_DIR)")
    sys.exit(0)

import yaml  # noqa: E402 — after the skip so a bare tree needs no PyYAML

IFACE = {
    "eth": "as_ethernet_header::AS_ETH::AS_ETH_IF",
    "sync": "as_sync::AS_SYNC::AS_SYNC_IF",
    "fu": "as_follow_up::AS_FOLLOW_UP::AS_FOLLOW_UP_IF",
    "ann": "as_announce::AS_ANNOUNCE::AS_ANNOUNCE_IF",
    "ann_pt1": "as_announce::AS_ANNOUNCE::AS_ANNOUNCE_PT1_IF",
    "pdreq": "as_pdelay_req::AS_PDELAY_REQ::AS_PDELAY_REQ_IF",
    "pdresp": "as_pdelay_resp::AS_PDELAY_RESP::AS_PDELAY_RESP_IF",
    "pdrfu": "as_pdelay_resp_fu::AS_PDELAY_RESP_FU::AS_PDELAY_RESP_FU_IF",
}

# The values 802.1AS-2011 pins on the wire, by clause — cross-checked
# below against the YAMLs' own `expected: value` entries so neither
# copy can drift.
#
# The flags words are 11.4.2.3 and Table 11-4, which override the common
# flags field of 10.5.2.2.6 for the five Ethernet messages of 11.4.1:
# twoStepFlag for Sync and Pdelay_Resp, every other bit FALSE. Announce is
# outside that list and keeps the common ptpTimescale. These are TRANSMIT
# values; the received frames built further down deliberately carry the
# reserved bit, which 11.4.1 has the receiver ignore (FPGA-gPTP #64).
HDR_COMMON = {"transport_specific": 1, "reserved0": 0, "version_ptp": 2,
              "domain_number": 0, "reserved1": 0, "reserved2": 0}
SPEC = {
    "sync": dict(HDR_COMMON, message_type=0x0, message_length=44,
                 flags=0x0200, correction_field=0, control=0x00,
                 log_message_interval=0xFD, origin_timestamp=0),
    "fu": dict(HDR_COMMON, message_type=0x8, message_length=76,
               flags=0x0000, control=0x02, log_message_interval=0xFD,
               tlv_type=0x0003, tlv_length=28, tlv_org_id=0x0080C2,
               tlv_org_subtype=1),
    "ann_pt1": dict(HDR_COMMON, message_type=0xB, message_length_pt1=76,
                    flags=0x0008, correction_field=0, control=0x05,
                    log_message_interval=0x00, reserved3=0, reserved4=0,
                    pt_tlv_type=0x0008, pt_tlv_length=8),
    "pdreq": dict(HDR_COMMON, message_type=0x2, message_length=54,
                  flags=0x0000, correction_field=0, control=0x05,
                  log_message_interval=0x00, reserved3=0, reserved4=0),
    "pdresp": dict(HDR_COMMON, message_type=0x3, message_length=54,
                   flags=0x0200, control=0x05, log_message_interval=0x7F),
    "pdrfu": dict(HDR_COMMON, message_type=0xA, message_length=54,
                  flags=0x0000, control=0x05, log_message_interval=0x7F),
}


class Tally:
    """The run's verdict so far, owned by an object rather than the module.

    Every arm below reports through one instance, so the counts cannot be
    reached from anywhere that did not ask for them, and a second scenario in
    the same process would start its own rather than inherit this one's.
    """

    def __init__(self) -> None:
        self.checks = 0
        self.fails = 0

    def expect(self, what: str, got: object, exp: object) -> None:
        """Record one comparison, and print it only when the two disagree.

        The check count grows on every call and the failure count only on a
        mismatch, so the transcript is exactly the list of disagreements and
        the tally at the end says how much agreement they are set against.
        """
        self.checks += 1
        if got != exp:
            self.fails += 1
            print(f"FAIL {what}: got {got!r} exp {exp!r}")


tally = Tally()


def pg(*args: str) -> str:
    """packet_gen's stdout for one invocation, against the 802.1AS YAMLs.

    A non-zero exit raises: the cross-check's independence rests on this
    decoder, so a run where it refused has measured nothing and must stop
    rather than record the frames it did manage.
    """
    # `str(...)` because these two cross into an argv, where a Path would be
    # stringified anyway and by a rule this file does not own.
    r = subprocess.run([str(PG), "--yaml-dir", str(YD), *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"packet_gen {args}: {r.stderr[:400]}")
    return r.stdout.strip()


def pg_gen(key: str, seed: int) -> tuple[str, dict[str, int]]:
    """The (wire hex, decoded fields) of the frame packet_gen builds for `seed`.

    Seeded and reproducible: the same interface and seed give the same bytes
    on every host, so a failure below names a frame anyone can rebuild.
    """
    out = pg("--interface", IFACE[key], "--seed", str(seed))
    d = json.loads(out.splitlines()[0])
    return d["hex"], d["fields"]


def pg_decode(key: str, hexstr: str) -> dict[str, int]:
    """The fields packet_gen reads out of `hexstr`, decoded as interface `key`.

    This is the whole point of the suite: nothing here parses a PDU itself,
    so the layout every check below is stated in is an independent
    implementation's and not this repository's C++ mirror.
    """
    out = pg("--interface", IFACE[key], "--hex", hexstr)
    return json.loads(out.splitlines()[0])["fields"]


# ---------------------------------------------------------------------------
# 1: the YAML pins and the clause table must agree exactly
# ---------------------------------------------------------------------------
def yaml_pins() -> dict[str, dict[str, int]]:
    """Every field value the 802.1AS YAMLs pin, as {service: {field: value}}.

    These are tsn-gen's own `expected: value` entries. SPEC below states the
    same values from the clauses, and the two are compared field by field, so
    neither copy can drift without the run saying which one moved.
    """
    pins: dict[str, dict[str, int]] = {}
    for doc_path in YD.glob("*.yaml"):
        doc = yaml.safe_load(doc_path.read_text())
        for v in doc.get("vars", []):
            exp = v.get("expected") or {}
            if "value" in exp:
                pins.setdefault(doc["service"], {})[v["var"]] = exp["value"]
    return pins


PINS = yaml_pins()
for key, svc in (("sync", "as_sync"), ("fu", "as_follow_up"),
                 ("ann_pt1", "as_announce"), ("pdreq", "as_pdelay_req"),
                 ("pdresp", "as_pdelay_resp"),
                 ("pdrfu", "as_pdelay_resp_fu")):
    got = PINS.get(svc, {})
    # the YAMLs pin fewer fields than they used to (the Sync and Follow_Up
    # flags moved to a documented two-value exception, which is a tsn-gen
    # question and not this repository's); agreement is enforced on the
    # intersection, and a floor on the pin count catches a YAML whose
    # expectations vanish entirely. SPEC above states the strict clause
    # values, so a YAML that pins `flags` again is compared against them
    shared = [f for f in SPEC[key] if f in got]
    tally.expect(f"yaml pin coverage {svc}", len(shared) >= 5, True)
    for f in shared:
        tally.expect(f"yaml pin {svc}.{f}", got[f], SPEC[key][f])

# ---------------------------------------------------------------------------
# build the scripted scenario: every input frame is packet_gen output
# ---------------------------------------------------------------------------
def eth(seed: int) -> tuple[str, dict[str, int]]:
    """A generated Ethernet header, as (wire hex, decoded fields).

    Every frame handed to the engine gets one of these rather than a constant
    written here, so the header on the wire is the generator's too.
    """
    return pg_gen("eth", seed)


def patch(hexstr: str, byte_off: int, newbyte: int) -> str:
    """`hexstr` with the byte at `byte_off` replaced and every other kept.

    How a generated frame is steered into a specific arm - a stepsRemoved
    small enough to qualify, a priority1 that has to win - while the rest of
    the frame stays whatever the generator chose.
    """
    return hexstr[:2 * byte_off] + f"{newbyte:02x}" + hexstr[2 * byte_off + 2:]


script = ["BOOT", "TXDUMP"]
expected_pubs = []

# responder-role stimulus: a generated Pdelay_Req
REQ_RX_TS = 2_000_000
req_eth, _ = eth(11)
req_hex, req_f = pg_gen("pdreq", 12)
script += [f"RX {req_eth}{req_hex} {REQ_RX_TS}", "TXDUMP"]

script += ["MASTER", "RUN 3000000", "TXDUMP"]

# BTCA sweep: seeded announces, outcome mirrored in python
ANN_SEEDS = [(101, "ann_pt1"), (102, "ann"), (103, "ann_pt1"),
             (104, "ann"), (105, "ann_pt1"), (106, "ann"),
             (107, "ann_pt1"), (108, "ann")]
OUR_VEC = (248 << 56) | (OUR_CQ << 24) | (248 << 16)


class BmcaModel:
    """PortAnnounceReceive (10.3.10) qualification + PortAnnounceInformation
    (10.3.11) classification, mirroring the µcode exactly: the comparison
    TARGET is the incumbent portPriority for an announce from a different
    grandmaster, and our own vector when there is no incumbent or when the
    incumbent itself is re-announcing."""

    def __init__(self) -> None:
        self.master = True
        self.gm = OUR_CID
        self.parent = OUR_CID
        self.parent_port = 1
        self.ppv = None
        self.annq = 0

    def feed(self, af: dict[str, int],
             path: list[int]) -> dict[str, int]:
        """The publication this Announce should produce, having applied it.

        `af` is the decoded Announce and `path` its pathSequence. An announce
        that fails 10.3.10.2.1 qualification changes nothing and the previous
        publication is returned unchanged; a qualified one moves the raw
        announce word before the compare, so annq marches even through a
        refusal to adopt, exactly as the handler's first write does.
        """
        vec = ((af["gm_priority1"] << 56) | (af["gm_clock_quality"] << 24)
               | (af["gm_priority2"] << 16))
        qualified = (af["source_clock_identity"] != OUR_CID
                     and af["steps_removed"] < 255
                     and OUR_CID not in path
                     and len(path) <= 8)
        if qualified:
            # the raw vector is the handler's first write, before the
            # compare, so it moves for every qualified announce and
            # holds through a refusal
            self.annq = ((af["current_utc_offset"] << 48)
                         | (af["gm_priority1"] << 40)
                         | (af["gm_clock_quality"] << 8) | af["gm_priority2"])
            cand = (vec, af["gm_identity"])
            if self.master:                       # no incumbent
                if cand < (OUR_VEC, OUR_CID):
                    self._adopt(af, vec)
            elif af["gm_identity"] == self.gm:    # repeated
                if cand < (OUR_VEC, OUR_CID):
                    self._refresh(af, vec)
                else:
                    self._become()
            else:                                 # other announcer
                if cand < (self.ppv, self.gm):
                    self._adopt(af, vec)
        return {"gm": self.gm, "parent": self.parent, "annq": self.annq,
                "flags_lo": 0x7 if self.master else 0x5}

    def _adopt(self, af: dict[str, int], vec: int) -> None:
        self.master = False
        self.gm = af["gm_identity"]
        self._refresh(af, vec)

    def _refresh(self, af: dict[str, int], vec: int) -> None:
        self.parent = af["source_clock_identity"]
        self.parent_port = af["source_port_number"]
        self.ppv = vec

    def _become(self) -> None:
        self.master = True
        self.gm = OUR_CID
        self.parent = OUR_CID
        self.ppv = None


bmca = BmcaModel()
rxts = 40_000_000
for i, (seed, kind) in enumerate(ANN_SEEDS):
    ehex, _ = eth(seed)
    ahex, _ = pg_gen(kind, seed)
    # steps_removed is announce PDU bytes 61..62; the generated 16-bit
    # value is >= 255 for ~99.6% of seeds and 10.3.10.2.1 refuses those,
    # so pin it small to exercise the compare arms. A PATH_TRACE variant
    # must also be structurally conformant or the parser refuses it
    # before the compare: pathSequence length is stepsRemoved+1 (one
    # element here, so steps 0) and pathSequence[0] is the
    # grandmasterIdentity (PDU bytes 68..75 := bytes 53..60). Re-decode
    # through packet_gen so the model reads what is really on the wire.
    steps = 0 if kind == "ann_pt1" else i % 4
    ahex = patch(patch(ahex, 61, 0), 62, steps)
    if kind == "ann_pt1":
        ahex = ahex[:2 * 68] + ahex[2 * 53:2 * 61] + ahex[2 * 76:]
    af = pg_decode(kind, ahex)
    tally.expect(f"ann[{i}] steps pinned", af["steps_removed"], steps)
    if kind == "ann_pt1":
        tally.expect(f"ann[{i}] path head is gm", af["path0"], af["gm_identity"])
    script.append(f"RX {ehex}{ahex} {rxts}")
    script.append("PUB")
    rxts += 1_000_000
    path = [af["path0"]] if kind == "ann_pt1" else []
    expected_pubs.append(bmca.feed(af, path))

# force slave under an unbeatable master: a generated announce with
# priority1 patched to 0, re-decoded through packet_gen to stay honest
sehex, _ = eth(200)
sahex, _ = pg_gen("ann_pt1", 201)
sahex = patch(sahex, 47, 0)                    # gm_priority1 at PDU byte 47
sahex = patch(patch(sahex, 61, 0), 62, 0)      # steps_removed = hops - 1
sahex = sahex[:2 * 68] + sahex[2 * 53:2 * 61] + sahex[2 * 76:]
saf = pg_decode("ann_pt1", sahex)
tally.expect("patched p1", saf["gm_priority1"], 0)
tally.expect("patched steps", saf["steps_removed"], 0)
tally.expect("patched path head", saf["path0"], saf["gm_identity"])
script.append(f"RX {sehex}{sahex} {rxts}")
script.append("PUB")
expected_pubs.append(bmca.feed(saf, [saf["path0"]]))
tally.expect("forced slave in model", expected_pubs[-1]["flags_lo"], 0x5)
rxts += 1_000_000

# offset arithmetic: generated Sync + Follow_Up pairs against the model
FU_SEEDS = [301, 302, 303]
expected_offsets = []
for seed in FU_SEEDS:
    syehex, _ = eth(seed)
    syhex, _ = pg_gen("sync", seed)
    # flags are PDU bytes 6..7. These are RECEIVED frames, and 11.4.1 has
    # the receiver ignore reserved fields, so they deliberately carry
    # 0x0208 and 0x0008 - twoStepFlag plus the bit 11.4.2.3 takes out of a
    # transmitted Sync, and the shape a peer was captured sending. The
    # suite therefore keeps a receive-tolerance input while SPEC above
    # stays strict about what this plane transmits.
    #
    # The engine pairs a Follow_Up with its pending Sync by sequenceId AND
    # sourcePortIdentity (11.2.14), and two independently generated
    # frames carry unrelated random sources, so pin both (PDU bytes
    # 20..29) to one identity - the adopted parent, the identity a
    # conformant master would transmit.
    src_hex = f"{bmca.parent:016x}{bmca.parent_port:04x}"
    syhex = patch(patch(syhex, 6, 0x02), 7, 0x08)
    syhex = syhex[:2 * 20] + src_hex + syhex[2 * 30:]
    syf = pg_decode("sync", syhex)
    tally.expect(f"sync rx flags pinned [{seed}]", syf["flags"], 0x0208)
    tally.expect(f"sync from parent [{seed}]",
           syf["source_clock_identity"], bmca.parent)
    fuehex, _ = eth(seed + 50)
    fuhex, _ = pg_gen("fu", seed + 50)
    fuhex = patch(patch(fuhex, 6, 0x00), 7, 0x08)
    fuhex = fuhex[:2 * 20] + src_hex + fuhex[2 * 30:]
    # 11.2.13 MDSyncReceive pairs on sequenceId (PDU bytes 30..31)
    seq = syf["sequence_id"]
    fuhex = patch(patch(fuhex, 30, seq >> 8), 31, seq & 0xFF)
    fuf = pg_decode("fu", fuhex)
    tally.expect(f"fu rx flags pinned [{seed}]", fuf["flags"], 0x0008)
    tally.expect(f"fu seq paired [{seed}]", fuf["sequence_id"], seq)
    trx = rxts
    script.append(f"RX {syehex}{syhex} {trx}")
    script.append(f"RX {fuehex}{fuhex} {trx + 500}")
    script.append("PUB")
    origin = fuf["precise_origin_seconds"] * 1_000_000_000 \
        + fuf["precise_origin_ns"]
    corr = fuf["correction_field"]
    if corr >= 1 << 63:
        corr -= 1 << 64
    corr >>= 16
    off = (trx - (origin + corr + PD_NS)) & 0xFFFFFFFF
    expected_offsets.append(off - (1 << 32) if off >= 1 << 31 else off)
    rxts += 2_000_000

# ---------------------------------------------------------------------------
# run the DUT
# ---------------------------------------------------------------------------
scr_path = HERE / "obj_dir" / "scenario.txt"
scr_path.write_text("\n".join(script) + "\n")
# `str(...)` because both cross into an argv, where a Path would be
# stringified anyway and by a rule this file does not own.
r = subprocess.run([str(HERE / "obj_dir" / "Vtsngen"), str(scr_path)],
                   capture_output=True, text=True)
if r.returncode != 0:
    print(f"FAIL harness rc={r.returncode}\n{r.stderr[:800]}")
    sys.exit(1)
lines = r.stdout.splitlines()


def take_txdump(it: Iterator[str]) -> list[tuple[str, int]]:
    """The (frame hex, timestamp) pairs of one TXDUMP block, up to its ENDTX.

    The iterator is consumed through the terminator, so the dumps of one run
    are read in order from a single stream. A stream that ends first raises
    rather than returning what it had: a truncated dump is indistinguishable
    from a port that transmitted nothing, and the two mean opposite things.
    """
    frames = []
    for ln in it:
        if ln == "ENDTX":
            return frames
        if ln.startswith("TX "):
            _, h, ts = ln.split()
            frames.append((h, int(ts.split("=")[1])))
    raise RuntimeError("truncated TXDUMP")


it = iter(lines)
tally.expect("BOOT ok", next(it), "OK BOOT")
dump1 = take_txdump(it)
dump2 = take_txdump(it)
tally.expect("MASTER ok", next(it), "OK MASTER")
dump3 = take_txdump(it)
pubs = [ln for ln in it if ln.startswith("PUB ")]


def pub_fields(ln: str) -> dict[str, int]:
    """One PUB line's key=value tokens, with the identity fields read as hex.

    gm, parent, annq and flags are published in hexadecimal and everything
    else in decimal, so each value reads the way the engine's register does.
    """
    d = {}
    for tok in ln.split()[1:]:
        k, v = tok.split("=")
        d[k] = int(v, 16) if k in ("gm", "parent", "annq",
                                   "flags") else int(v)
    return d


def frames_of(dump: list[tuple[str, int]],
              mtype: int) -> list[tuple[str, int]]:
    """The frames of one messageType in a TXDUMP, in transmission order.

    Frame byte 14 is the PTP common header's first octet and its low nibble
    is the messageType, which is hex character 29 of the dumped frame.
    """
    return [(h, ts) for h, ts in dump if len(h) > 30
            and int(h[29], 16) == mtype]


def check_tx(tag: str, hexfrm: str, key: str,
             extra: dict[str, int]) -> dict[str, int]:
    """Decode one of OUR frames with packet_gen and enforce the YAML
    pins plus the scenario-derived fields."""
    ef = pg_decode("eth", hexfrm[:28])
    tally.expect(f"{tag} eth dst", ef["dst_mac"], 0x0180C200000E)
    tally.expect(f"{tag} eth type", ef["ethertype"], 0x88F7)
    tally.expect(f"{tag} eth src", ef["src_mac"], OUR_MAC)
    f = pg_decode(key, hexfrm[28:])
    for name, v in SPEC[key].items():
        tally.expect(f"{tag} {name}", f[name], v)
    for name, v in extra.items():
        tally.expect(f"{tag} {name}", f[name], v)
    return f


# --- our Pdelay_Req ---
reqs = frames_of(dump1, 0x2)
tally.expect("boot sent pdreq", len(reqs) >= 1, True)
if reqs:
    check_tx("pdreq", reqs[0][0], "pdreq",
             {"source_clock_identity": OUR_CID, "source_port_number": 1})

# --- our Pdelay_Resp + Resp_FU for the generated request ---
resps = frames_of(dump2, 0x3)
rfus = frames_of(dump2, 0xA)
tally.expect("resp sent", len(resps), 1)
tally.expect("rfu sent", len(rfus), 1)
if resps:
    check_tx("pdresp", resps[0][0], "pdresp", {
        "sequence_id": req_f["sequence_id"],
        "requesting_clock_identity": req_f["source_clock_identity"],
        "requesting_port_number": req_f["source_port_number"],
        "request_receipt_seconds": REQ_RX_TS // 1_000_000_000,
        "request_receipt_ns": REQ_RX_TS % 1_000_000_000,
        "source_clock_identity": OUR_CID})
if rfus:
    t3 = resps[0][1]
    check_tx("pdrfu", rfus[0][0], "pdrfu", {
        "sequence_id": req_f["sequence_id"],
        "requesting_clock_identity": req_f["source_clock_identity"],
        "requesting_port_number": req_f["source_port_number"],
        "response_origin_seconds": t3 // 1_000_000_000,
        "response_origin_ns": t3 % 1_000_000_000,
        "source_clock_identity": OUR_CID})

# --- our Announce / Sync / Follow_Up as master ---
anns = frames_of(dump3, 0xB)
syncs = frames_of(dump3, 0x0)
fus = frames_of(dump3, 0x8)
tally.expect("announce sent", len(anns) >= 1, True)
tally.expect("sync sent", len(syncs) >= 1, True)
tally.expect("fu sent", len(fus) >= 1, True)
if anns:
    check_tx("ann", anns[0][0], "ann_pt1", {
        "source_clock_identity": OUR_CID, "current_utc_offset": 37,
        "gm_priority1": 248, "gm_clock_quality": OUR_CQ,
        "gm_priority2": 248, "gm_identity": OUR_CID,
        "steps_removed": 0, "time_source": 0xA0, "path0": OUR_CID})
if syncs and fus:
    sf = check_tx("sync", syncs[0][0], "sync",
                  {"source_clock_identity": OUR_CID})
    fmatch = [(h, ts) for h, ts in fus
              if pg_decode("fu", h[28:])["sequence_id"] == sf["sequence_id"]]
    tally.expect("fu pairs its sync", len(fmatch) >= 1, True)
    if fmatch:
        check_tx("fu", fmatch[0][0], "fu", {
            "source_clock_identity": OUR_CID,
            "precise_origin_seconds": syncs[0][1] // 1_000_000_000,
            "precise_origin_ns": syncs[0][1] % 1_000_000_000,
            "cumulative_scaled_rate_offset": 0})

# --- BTCA sweep + forced adopt ---
n_btca = len(expected_pubs)
tally.expect("pub count", len(pubs), n_btca + len(FU_SEEDS))
for i, exp_pub in enumerate(expected_pubs):
    if i >= len(pubs):
        break
    got = pub_fields(pubs[i])
    tag = f"btca[{i}]"
    tally.expect(f"{tag} gm", got["gm"], exp_pub["gm"])
    tally.expect(f"{tag} parent", got["parent"], exp_pub["parent"])
    tally.expect(f"{tag} annq", got["annq"], exp_pub["annq"])
    tally.expect(f"{tag} flags", got["flags"] & 0x7, exp_pub["flags_lo"])

# --- offset arithmetic from generated Sync+FU ---
for i, off in enumerate(expected_offsets):
    idx = n_btca + i
    if idx >= len(pubs):
        break
    got = pub_fields(pubs[idx])
    tally.expect(f"offset[{i}]", got["offset"], off)
    tally.expect(f"offset[{i}] syncOk", got["flags"] & 0x8, 0x8)

print(f"{tally.checks} checks: {tally.checks - tally.fails} PASS,"
      f" {tally.fails} FAIL")
sys.exit(1 if tally.fails else 0)
