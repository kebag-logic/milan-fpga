#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""hive_compliance.py - check an ATDECC entity the way Hive checks it.

    sudo ./hive_compliance.py --iface enp6s0 --target-eid 020000FFFE000001 \
                              --target-mac 02:00:00:00:00:01

WHY THIS EXISTS. On 2026-07-27 every one of our own gates was green - 57/57
Verilator suites, yosys 48/48, behave 113/113, lint at ratchet - while Hive
called our entity "not fully Milan compliant" fifteen times. Our raw-socket
tools (avdecc_ctl.py, avdecc_l2.py) missed it because they read the STATUS
byte and moved on; Hive also validates the RESPONSE FRAME ITSELF. Two tools
written from the same reading of the spec share the same blind spots, so this
one deliberately re-implements the checks a real controller stack makes:

  C1 PAYLOAD SIZE ON NON-SUCCESS RESPONSES.  A non-success AEM response must
     be the SAME SIZE as a SUCCESS response for that command - the status
     changes, the frame shape does not.  The rule is CALIBRATED per device
     from a real SUCCESS response rather than hardcoded, because the first
     version of this check asserted "echoes the COMMAND" and the negative
     control refuted it: the Milan-validated reference device answers a
     non-existent descriptor with 68 bytes (its GET_STREAM_INFO response
     size), not with the 24-byte command, and Hive accepts that. We answer
     with 16 - truncated - which is what Hive rejects.  Hive reported
     "Received an invalid non-success GET_STREAM_INFO AEM response (Incorrect
     payload size)" 15 times against us and only kept going because it was
     built with IGNORE_INVALID_NON_SUCCESS_AEM_RESPONSES; a strict controller
     DROPS the response and the entity looks dead rather than incomplete.
  C2 DESCRIPTOR SELF-CONSISTENCY.  Every descriptor READ_DESCRIPTOR serves
     must also answer its dynamic-info command.  We served STREAM_OUTPUT.4
     byte-for-byte and then returned NO_SUCH_DESCRIPTOR for GET_STREAM_INFO on
     the same index - the device contradicting itself between two commands.
  C3 ADVERTISED SHAPE == ADDRESSABLE SHAPE.  ADP talker_stream_sources /
     listener_stream_sinks must equal the number of descriptors that actually
     answer.  Advertising 9 and answering 1 is the 0x0015 defect's next layer.
  C4 MILAN RESERVED BITS.  Milan v1.2 5.4.2.10.1: StreamInfoFlags bit 24 is
     reserved and shall be 0 (this is the check Hive raised against the
     reference device, not against us - keep it so we never regress into it).
  C5 NON-SUCCESS SIZE, EVERY COMMAND.  C1 generalised past GET_STREAM_INFO:
     each AEM getter has a response format fixed by its own 1722.1 clause,
     and an error status does not shrink it.  Fixed-size commands are
     calibrated per device from their own SUCCESS response (the C1 method);
     variable-length ones (GET_AVB_INFO's msrp_mappings list, GET_AS_PATH's
     path_sequence, GET_AUDIO_MAP's mappings) are checked against the
     clause-defined MINIMUM instead, because equality is not the rule there -
     the reference device answers GET_AVB_INFO SUCCESS with 36 and its error
     with 32, and both are correct.  NOT_IMPLEMENTED is the one status that
     REFLECTS THE COMMAND rather than the response (see the size rule below).
  C6 DYNAMIC-INFO COVERAGE, EVERY COMMAND.  C2 generalised: a STREAM
     descriptor READ_DESCRIPTOR serves must answer GET_STREAM_FORMAT and
     GET_COUNTERS as well as GET_STREAM_INFO.
  C7 THE FRAME IS AS LONG AS IT CLAIMS.  control_data_length (1722.1-2021
     9.2.1.1.6) counts the bytes after it; a response whose frame is SHORTER
     than 14 + 4 + control_data_length is malformed however correct its
     status byte is.  This is the failure mode a status-only tool cannot see
     at all - our SET/GET_NAME lock path declared 84 and put 20 on the wire.
  C8 RESPONSE HEADER.  9.2.2.4 / 9.2.2.8-9: a solicited answer is an
     AEM_RESPONSE with u = 0 carrying the SAME command_type as the command.
     A wrong command_type orphans the controller's pending-command table.
  C9 AUDIO_MAP INDICES ARE PORT-RELATIVE AND IN RANGE.  1722.1-2021 7.2.19
     Table 7-162: mapping_cluster_offset is "the index of the cluster
     OFFSET FROM base_cluster" of the STREAM_PORT that answered - it is not
     a global AUDIO_CLUSTER index - and each of the four fields is bounded
     by a different descriptor:
       mapping_stream_index   < the STREAM_INPUT/OUTPUT descriptors that
                                direction actually answers  (7.2.13)
       mapping_stream_channel < that stream's CURRENT FORMAT channel count
                                (7.2.6 current_format / IEEE 1722-2016 AAF
                                channels_per_frame)
       mapping_cluster_offset < the answering STREAM_PORT's
                                number_of_clusters            (7.2.13)
       mapping_cluster_channel < channel_count of AUDIO_CLUSTER
                                [base_cluster + cluster_offset]  (7.2.16)
     This is the ONLY check here that catches a model written with GLOBAL
     cluster indices where the clause requires port-relative ones - two
     ports legitimately carry the SAME offsets onto DIFFERENT clusters, so
     a global-index regression stays inside every other check's blind spot.
     It SKIPS - never fails - on NOT_SUPPORTED or NO_SUCH_DESCRIPTOR.
     NOT_SUPPORTED is the SPECIFIED answer on an output port with a map;
     see C11 for the quoted sentence. Failing there would file conformance
     as a defect (methodology R3).
     ONE CAVEAT ON THE stream_channel BOUND, recorded rather than silently
     relied on: it uses the CURRENT format, which is the only channel count
     that exists on the wire, but a STATIC Audio Map is a property of the
     PORT and outlives any one SET_STREAM_FORMAT. Reading the texts settled
     what "no clause in reach" used to mean here: 1722.1-2021 7.2.19 and
     7.2.13 bound a static map's mapping_stream_channel by NOTHING, and the
     only normative sentence is Milan v1.2 5.4.2.27 on the ADD_AUDIO_MAPPINGS
     COMMAND - "A PAAD-AE shall treat as invalid a mapping that references a
     channel of a Stream Input/Output that does not exist in the currently set
     format for this Stream Input/Output." For the descriptor the standard is
     SILENT. That is why the model-tier twin of this bound
     (avdecc/gen_aem_store.py static_map_tables) uses the WIDEST format the
     descriptor advertises and records rather than raises. Neither the
     reference device nor our board trips this one today; it is not the bound
     that caught anything.
  C11 MILAN'S DIRECTION SPLIT ON GET_AUDIO_MAP. Milan v1.2 5.4.2.26,
     verbatim: "For each Stream Port Input and for each Stream Port Output
     that has no Audio Map, the PAAD-AE shall implement the GET_AUDIO_MAP
     command as specified in [ATDECC, Clause 7.4.44]. If a PAAD-AE receives a
     GET_AUDIO_MAP command for a Stream Port Output that has Audio Map(s),
     the PAAD-AE shall reply with the NOT_SUPPORTED error code."
     So the check is per direction, and it is decided by the port's OWN
     number_of_maps (7.2.13), not by a guess: an output port declaring
     number_of_maps >= 1 must refuse with NOT_SUPPORTED, an input port must
     answer. On the board this is not a cosmetic status: the port that
     over-read a 24-octet descriptor by 48 octets on 2026-07-28 was an
     output port that should never have served a map at all.
     Also 7.4.44.1: "If the map_index is beyond the range of available maps
     then it returns a BAD_ARGUMENT status in the response." - so an
     in-range port asked for a page it does not have owes BAD_ARGUMENTS,
     not NO_SUCH_DESCRIPTOR.
  C10 THE MAP SERVED IS THE PORT'S OWN MAP, WHOLE AND NO MORE. Bounds are
     not enough. A map served out of the WRONG descriptor passes every
     bounds check whenever the neighbouring descriptor happens to hold
     in-range numbers, so C10 compares the served mappings against the
     AUDIO_MAP that THIS port's own base_map names (7.2.13), read back with
     READ_DESCRIPTOR - the entity's own answer to another command, not a
     second declaration of the shape. Three things are asserted, each of
     which the 2026-07-28 defect broke:
       the response CARRIES what it declares  (7.4.44.2: the payload is
                                               12 + 8*number_of_mappings)
       the descriptor HOLDS what it declares  (7.2.19: number_of_mappings
                                               8-octet rows after
                                               mappings_offset)
       every served mapping IS in that map    (7.2.19: the map belongs to
                                               the port)
     Order is NOT asserted - no clause in reach fixes one, so requiring it
     would be inventing a rule (methodology R3) - and the comparison is a
     multiset. What it catches that C9 cannot: on gateware 0x0001_0016 the
     entity answered STREAM_PORT_OUTPUT[0] out of AUDIO_MAP[1], which is
     STREAM_PORT_INPUT[1]'s map, with a hardcoded 8 mappings and a hardcoded
     64-octet region taken out of a descriptor that is 24 octets long: 48
     octets of whatever followed it in the descriptor ROM went on the wire
     to any controller that asked.
  C12 THE FORMAT IS ONE FORMAT (re-added 2026-07-28; born as C5 in e076647,
     lost to a merge numbering collision).  A STREAM descriptor's
     current_format (1722.1-2021 7.2.6, octets 74..81) and the
     GET_STREAM_FORMAT (0x0009) answer are the SAME fact stated twice and
     must agree - a controller runs Milan 5.5.1.2's compatibility check
     against whichever it read first, so a disagreement is a bind that
     succeeds against a format the talker will not send.
  C13 ADVERTISED == EMITTED, ON THE WIRE (opt-in, --wire-*; born as C6 in
     e076647).  THE CHECK THAT WOULD HAVE CAUGHT 2026-07-27: binds a REAL
     listener (the reference device) to our talker over ACMP and reads THAT
     device's Table 7-156 counters - UNSUPPORTED_FORMAT stays 0 while
     FRAMES_RX advances, or the fabric is not emitting the
     channels_per_frame the entity advertises.  LEVEL 5; needs a second
     Milan device and ~6 s of streaming.
     NEITHER IS CALIBRATED against the reference device yet - the 8.3.2
     rule applies: if one fails there first, the CHECK is wrong until a
     clause says otherwise.

WHERE THE CLAUSES COME FROM. Earlier rounds of this file said the IEEE and
Milan texts were paywalled and unavailable. They are on this machine, in
~/standards (1722.1-2021.pdf, 1722-2016.pdf, Milan v1.2); the
environment variable $STANDARDS_DIR that pointed at them is simply unset,
and that is what produced the "paraphrase only" discipline. Every clause in
C9/C10/C11 is now quoted from the text, extracted with pdftotext -layout.
ONE TRAP if you re-extract: the hexadecimal VALUE column of Table 7-1 comes
out mangled (leading digits dropped, letter glyphs shifted by one - LOCALE
reads "D16" where the value is 0xC). Take descriptor type codes from the
CLAUSE column instead, which is intact: AUDIO_CLUSTER is the 7.2.16 row
(0x0014) and AUDIO_MAP the 7.2.19 row (0x0017). Quote PROSE, verify numbers.

THE SIZE RULE AND WHERE IT COMES FROM. The size rule is NOT quoted from the
standard, because the standard does not state one for error responses; it is
taken from the controller stack that emits the log line above -
L-Acoustics avdecc, src/protocol/protocolAemPayloads.cpp,
checkResponsePayload():

    if (status == NotImplemented)   -> expect the COMMAND payload length
    else                            -> expect >= the RESPONSE payload length

and its per-command size constants carry the clause they came from (e.g.
"GET_STREAM_INFO Response - IEEE1722.1-2013 Clause 7.4.16.2", "Milan 1.2
Clause 7.3.10" = 56 B). What the standard fixes is the response MESSAGE
FORMAT per clause 7.4.x; it defines no truncated error variant. Everything
below is additionally calibrated against the Milan-validated reference
device, which must stay at zero failures - a check that only ever fails
against us proves as little as one that only ever passes.

--self-test runs C9's bounds predicate AND C10's over-read predicate over
crafted good/bad vectors with no network at all: the negative control for
checks whose live subject may legitimately return zero mappings (methodology
R2 - a check that cannot fail is not a check, and a vacuous pass against the
reference device is not proof that it can).

A VACUOUS PASS IS THE FAILURE MODE THIS FILE KEEPS HITTING. C9's
cluster_channel bound read AUDIO_CLUSTER as descriptor type 0x0016 (which is
SENSOR_CLUSTER; 1722.1-2021 Table 7.1 says AUDIO_CLUSTER is 0x0014), so every
cluster READ_DESCRIPTOR came back NO_SUCH_DESCRIPTOR, the channel-count map
stayed empty and that bound was never asserted against anything. It reported
[ok] on both devices for the same reason a disconnected cable does. Fixed
2026-07-28; the offset it reads (AC_CHANNEL_COUNT_OFF = 84) was verified
against the generated ROM rather than counted from the clause a second time.

LEVEL AND ORACLE (every check in this file): LEVEL 4 - what an INDEPENDENT
controller sees. The oracle is a FOREIGN implementation (Hive / la_avdecc)
plus a QUALIFIED REFERENCE DEVICE, never our own RTL or our own model. That
is the whole reason this tool exists: two of our tools written from the same
reading of the spec agreed with each other and missed fifteen defects.

RULE FOR ADDING A CHECK HERE: run it against the reference device first. IF A
CHECK FAILS AGAINST THE REFERENCE, THE CHECK IS WRONG until a clause proves
otherwise. Baselines measured 2026-07-28: reference 3CC0C60102030000 = 52
checks / 0 failures; our AX board on gateware 0x0001_0016 = 53 checks / 39
failures (29 C1 + 2 C2 + 2 C3 + 4 C5 + 2 C6).

C10, C11 AND THE D_AUDIO_CLUSTER FIX HAVE NOT BEEN RUN AGAINST EITHER DEVICE.
They were added 2026-07-28 from a Verilator reproduction (tb/verilator/aecp/
sim_amap.cpp, 48 of 218 checks failing on the pre-fix RTL) and the boards were
not available in that session. All three are therefore UNCALIBRATED against the
reference device, which is the one thing this file's own rule demands: run
    sudo ./hive_compliance.py --iface <if> --target-eid 3CC0C60102030000 \
                              --target-mac 3c:c0:c6:01:02:03
FIRST, and if any of them fails there, THE CHECK IS WRONG until a clause says
otherwise. C11 is the one to watch: it is quoted from Milan 5.4.2.26 rather
than inferred, but it asserts a REFUSAL, and a check that demands an error
status is exactly the kind that can be right about the clause and wrong about
the device (e.g. if the reference device's output ports carry no Audio Map, C11
takes its other branch there and proves nothing - read the printed n_maps).
Expected reading on our own board after a rebuild+reflash carrying this fix:
C9 STREAM_PORT_OUTPUT 1 -> 0 failures, C10 and C11 clean. On the flashed
0x0001_0016 image C9, C10 and C11 all fail on STREAM_PORT_OUTPUT.

Exit code 0 = clean, 1 = at least one FAIL. Run it against OUR board AND the
reference device: a check that only ever passes proves nothing.
"""
import argparse
import socket
import struct
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# The predicates and the transport live beside this file; see their module
# docstrings for the split. `aecp_cmd` and `xchg` are re-exported here on
# purpose - `hive_compliance_clusters.py` imports the calibrated transport as
# `from hive_compliance import open_sock, aecp_cmd, xchg, resp_parts`, and
# that spelling is the one recorded in its socket-recipe comment.
from hive_compliance_oracle import (aaf_channels,             # noqa: E402
                                    audio_map_overreads,
                                    audio_map_violations,
                                    self_test)
from hive_compliance_wire import (                            # noqa: E402,F401
    AC_CHANNEL_COUNT_OFF, ADV, AM_HDR, AM_NUM_MAPPINGS_OFF, AM_ROWS_OFF,
    BAD_INDEX, CHECKS, CMD_GET_AS_PATH, CMD_GET_AUDIO_MAP, CMD_GET_AVB_INFO,
    CMD_GET_CLOCK_SOURCE, CMD_GET_COUNTERS, CMD_GET_NAME,
    CMD_GET_SAMPLING_RATE, CMD_GET_STREAM_FORMAT, CMD_GET_STREAM_INFO,
    CMD_READ_DESCRIPTOR, DESC, DESCRIPTOR_OFF, D_AUDIO_CLUSTER, D_AUDIO_MAP,
    D_AUDIO_UNIT, D_AVB_INTERFACE, D_CLOCK_DOMAIN, D_STREAM_PORT_INPUT,
    D_STREAM_PORT_OUTPUT, FAILS, RD_DESC_OFF, SEEN, SP_BASE_CLUSTER_OFF,
    SP_BASE_MAP_OFF, SP_NUM_CLUSTERS_OFF, SP_NUM_MAPS_OFF,
    STATUS_NOT_IMPLEMENTED, STATUS_NOT_SUPPORTED, STATUS_NO_SUCH_DESCRIPTOR,
    STREAM_CURRENT_FORMAT_OFF, Binding, Peers, Probe, acmp, aecp_cmd, ck,
    open_sock, peer_counters, resp_parts, sniff_adp, xchg)


def _await_advertisement(pr):
    """Seed the advertised shape; sniff_adp keeps it fed for the rest of the run."""
    a, s, tgt = pr.args, pr.sock, pr.tgt
    # ---- C3 part 1: seed the advertised shape (kept fed by sniff_adp) ----
    end = time.time() + a.adp_wait
    while time.time() < end and not ADV:
        try:
            sniff_adp(s.recv(2048), tgt)
        except socket.timeout:
            continue


def _probe_descriptor_type(pr, dname, dcode, fmts):
    """C1/C2/C4/C6/C12 for one descriptor type -> its (served, answered) indices.

    `fmts` gains this type's per-index current_format, which C12 compares
    against GET_STREAM_FORMAT and C13 reads for the talker it binds.
    """
    a, do = pr.args, pr.do
    print(f"\n-- {dname} --")
    served, answered, ok_cdl = [], [], []
    fmt_ok, cnt_ok = [], []
    for i in range(a.max_index):
        # READ_DESCRIPTOR: cfg(2) res(2) type(2) index(2)
        r, _ = do(f"READ_DESCRIPTOR {dname}.{i}", CMD_READ_DESCRIPTOR,
                  struct.pack('!HHHH', 0, 0, dcode, i))
        if r and resp_parts(r)[0] == 0:
            served.append(i)
            pl = resp_parts(r)[2]
            o = DESCRIPTOR_OFF + STREAM_CURRENT_FORMAT_OFF
            if len(pl) >= o + 8:
                fmts.setdefault(dname, {})[i] = \
                    struct.unpack('!Q', pl[o:o + 8])[0]

        # GET_STREAM_INFO: type(2) index(2)
        r, _ = do(f"GET_STREAM_INFO {dname}.{i}", CMD_GET_STREAM_INFO,
                  struct.pack('!HH', dcode, i))
        if not r:
            continue
        st, rcdl, pl = resp_parts(r)
        if st == 0:
            answered.append(i)
            ok_cdl.append(rcdl)
            # C4: Milan 5.4.2.10.1 - StreamInfoFlags bit 24 reserved = 0
            if len(pl) >= 8:
                flags = struct.unpack('!I', pl[4:8])[0]
                ck(((flags >> 24) & 1) == 0,
                   f"C4 {dname}.{i} StreamInfoFlags bit24 reserved=0",
                   f"flags=0x{flags:08X}")
        else:
            # C1: a NON-SUCCESS response must still echo the command's
            # control_data_length. This is the check our own tools skipped
            # and Hive flagged 15 times.
            want = ok_cdl[0] if ok_cdl else None
            if want is None:
                print(f"  [skip] C1 {dname}.{i}: no SUCCESS response yet "
                      f"to calibrate the expected size against")
            else:
                ck(rcdl == want,
                   f"C1 {dname}.{i} non-success size == success size",
                   f"status={st} resp_cdl={rcdl} success_cdl={want}")

    # C6: the OTHER dynamic-info commands owe the same descriptors an
    # answer. GET_STREAM_FORMAT = 1722.1 7.4.10, GET_COUNTERS = 7.4.42;
    # both are addressed by {descriptor_type, descriptor_index} exactly
    # like GET_STREAM_INFO, so "the descriptor exists" cannot differ
    # between them.
    for i in served:
        r, _ = do(f"GET_STREAM_FORMAT {dname}.{i}", CMD_GET_STREAM_FORMAT,
                  struct.pack('!HH', dcode, i))
        if r and resp_parts(r)[0] == 0:
            fmt_ok.append(i)
            # C12: the descriptor's current_format (1722.1-2021 7.2.6)
            # and the GET_STREAM_FORMAT answer are the SAME fact stated
            # twice - a disagreement means Milan 5.5.1.2's format check
            # ran against a format the talker will not send.
            desc_fmt = fmts.get(dname, {}).get(i)
            if desc_fmt is not None and len(resp_parts(r)[2]) >= 12:
                gsf = struct.unpack('!Q', resp_parts(r)[2][4:12])[0]
                nch = aaf_channels(desc_fmt)
                ck(gsf == desc_fmt,
                   f"C12 {dname}.{i} descriptor current_format == "
                   f"GET_STREAM_FORMAT",
                   f"descriptor=0x{desc_fmt:016X} "
                   f"GET_STREAM_FORMAT=0x{gsf:016X}"
                   + (f" ({nch}ch AAF)" if nch is not None
                      else " (non-AAF)"))
        r, _ = do(f"GET_COUNTERS {dname}.{i}", CMD_GET_COUNTERS,
                  struct.pack('!HH', dcode, i))
        if r and resp_parts(r)[0] == 0:
            cnt_ok.append(i)

    # C2: anything READ_DESCRIPTOR serves must answer GET_STREAM_INFO
    missing = [i for i in served if i not in answered]
    ck(not missing, f"C2 {dname} every served descriptor answers "
                    f"GET_STREAM_INFO",
       f"served={len(served)} answered={len(answered)} missing={missing}")
    for cname, got in (("GET_STREAM_FORMAT", fmt_ok),
                       ("GET_COUNTERS", cnt_ok)):
        miss = [i for i in served if i not in got]
        ck(not miss, f"C6 {dname} every served descriptor answers {cname}",
           f"served={len(served)} answered={len(got)} missing={miss}")

    print(f"     served={served}")
    print(f"     answered={answered}")

    return served, answered


def _descriptor_sweep(pr, fmts):
    """dname -> (served, answered) for every descriptor type, C3 and C9's input."""
    _await_advertisement(pr)
    shape = {}
    for dname, dcode in DESC.items():
        shape[dname] = _probe_descriptor_type(pr, dname, dcode, fmts)
    return shape


def _advertised_shape_checks(pr, shape):
    """C3: the ADP advertisement and the descriptors must agree."""
    a, s, tgt = pr.args, pr.sock, pr.tgt
    # ---- C3: advertised shape == addressable shape ----------------------
    # The ADP count is what a controller sizes its enumeration loop from; a
    # descriptor set larger or smaller than the advertisement is a
    # contradiction between the discovery protocol and the model, and a set
    # that ENUMERATES but does not ANSWER is the same contradiction one layer
    # down - that is exactly the 0x0016 defect.
    print("\n-- C3 advertised shape == addressable shape --")
    if not ADV:
        # xchg() returns the instant its response arrives, so the sniffing it
        # does covers only microseconds per command. The AX board advertises
        # roughly every 7 s; listen properly rather than skip the check.
        print(f"  no ADPDU yet - listening {a.adp_wait * 3:.0f}s for one")
        end = time.time() + a.adp_wait * 3
        while time.time() < end and not ADV:
            try:
                sniff_adp(s.recv(2048), tgt)
            except socket.timeout:
                continue
    if not ADV:
        ck(False, "C3 an ADPDU from the target was seen",
           f"none in {a.adp_wait * 4:.0f}s - the entity is not advertising")
    else:
        print(f"  ADP talker_stream_sources={ADV['STREAM_OUTPUT']} "
              f"listener_stream_sinks={ADV['STREAM_INPUT']}")
        for dname, (served, answered) in shape.items():
            ck(ADV[dname] == len(served),
               f"C3 {dname} ADP count == descriptors served",
               f"adp={ADV[dname]} served={len(served)}")
            ck(ADV[dname] == len(answered),
               f"C3 {dname} ADP count == descriptors answering GET_STREAM_INFO",
               f"adp={ADV[dname]} answered={len(answered)}")


def _non_success_size_checks(pr):
    """C5: an error status does not shrink a response."""
    do = pr.do
    # ------------------------------------------------------------------ #
    # C5: the size rule, generalised past GET_STREAM_INFO.
    #
    # mode 'fixed': the clause fixes the whole response, so a non-success
    #   response must be the SAME size as this device's own SUCCESS response
    #   (calibrated, never hardcoded).
    # mode 'min':   the response carries a variable-length list, so only the
    #   clause-defined minimum can be asserted. The reference device answers
    #   GET_AVB_INFO SUCCESS with cdl 36 and its error with cdl 32 (the 20 B
    #   minimum, msrp_mappings_count = 0) and both are correct - which is
    #   exactly why equality is NOT the rule for these.
    # min_payload values are the clause field lists, mirrored by la_avdecc's
    # protocolAemPayloadSizes.hpp constants (each tagged with its clause).
    # ------------------------------------------------------------------ #
    print("\n-- C5 non-success size, per command --")
    C5 = [
        # label, cmd, clause, mode, min_payload, descriptor type, good index,
        # extra payload after {type,index}
        ("GET_STREAM_INFO", CMD_GET_STREAM_INFO, "7.4.16.2 / Milan 7.3.10",
         "fixed", 48, DESC['STREAM_INPUT'], 0, b''),
        ("GET_STREAM_FORMAT", CMD_GET_STREAM_FORMAT, "7.4.10.2",
         "fixed", 12, DESC['STREAM_INPUT'], 0, b''),
        ("GET_NAME", CMD_GET_NAME, "7.4.18.2",
         "fixed", 72, DESC['STREAM_INPUT'], 0, struct.pack('!HH', 0, 0)),
        ("GET_SAMPLING_RATE", CMD_GET_SAMPLING_RATE, "7.4.22.2",
         "fixed", 8, D_AUDIO_UNIT, 0, b''),
        ("GET_CLOCK_SOURCE", CMD_GET_CLOCK_SOURCE, "7.4.24.2",
         "fixed", 8, D_CLOCK_DOMAIN, 0, b''),
        ("GET_COUNTERS", CMD_GET_COUNTERS, "7.4.42.2",
         "fixed", 136, DESC['STREAM_INPUT'], 0, b''),
        ("GET_AVB_INFO", CMD_GET_AVB_INFO, "7.4.40.2",
         "min", 20, D_AVB_INTERFACE, 0, b''),
        ("GET_AS_PATH", CMD_GET_AS_PATH, "7.4.41.2",
         "min", 4, D_AVB_INTERFACE, 0, b''),
        ("GET_AUDIO_MAP", CMD_GET_AUDIO_MAP, "7.4.44.2",
         "min", 12, D_STREAM_PORT_INPUT, 0, struct.pack('!H', 0)),
    ]
    for label, cmd, clause, mode, minpl, dt, gidx, extra in C5:
        good, _ = do(f"{label} good", cmd, struct.pack('!HH', dt, gidx) + extra)
        bad, ccdl = do(f"{label} bad", cmd,
                       struct.pack('!HH', dt, BAD_INDEX) + extra)
        if bad is None:
            print(f"  [skip] C5 {label}: no response to the error probe")
            continue
        bst, bcdl, _ = resp_parts(bad)
        if bst == 0:
            print(f"  [skip] C5 {label}: index {BAD_INDEX} answered SUCCESS, "
                  f"no error status to size")
            continue
        if bst == STATUS_NOT_IMPLEMENTED:
            # the ONE status that reflects the command, not the response
            ck(bcdl == ccdl,
               f"C5 {label} NOT_IMPLEMENTED reflects the command ({clause})",
               f"resp_cdl={bcdl} cmd_cdl={ccdl}")
            continue
        if mode == "fixed":
            gst, gcdl, _ = resp_parts(good) if good else (None, None, None)
            if good is None or gst != 0:
                print(f"  [skip] C5 {label}: no SUCCESS response to calibrate "
                      f"against (got status {gst})")
                continue
            ck(bcdl == gcdl,
               f"C5 {label} non-success size == success size ({clause})",
               f"status={bst} resp_cdl={bcdl} success_cdl={gcdl}")
        else:
            ck(bcdl >= 12 + minpl,
               f"C5 {label} non-success >= clause minimum ({clause})",
               f"status={bst} resp_cdl={bcdl} min_cdl={12 + minpl}")


def _stream_channel_counts(pr, sname, n_streams):
    """index -> channels_per_frame from each stream's current format (C9 bound)."""
    do = pr.do
    # this direction's per-stream current-format channel counts
    stream_channels = {}
    for i in range(n_streams):
        r, _ = do(f"GET_STREAM_FORMAT {sname}.{i} (C9)",
                  CMD_GET_STREAM_FORMAT,
                  struct.pack('!HH', DESC[sname], i))
        if r and resp_parts(r)[0] == 0 and len(r) >= 50:
            ch = aaf_channels(struct.unpack('!Q', r[42:50])[0])
            if ch:
                stream_channels[i] = ch
    return stream_channels


def _port_own_map(pr, pname, pi, n_maps, base_map):
    """C10's oracle: (rows, length, declared count) of the port's OWN AUDIO_MAP.

    All three are None when the port declares no map descriptor, and
    `rows` stops short of `declared` when the descriptor is truncated - the
    overread predicate reports both.
    """
    do = pr.do
    # C10's oracle: THE PORT'S OWN AUDIO_MAP, the one ITS base_map
    # names. 7.2.13 number_of_maps = 0 means there is no descriptor
    # (the mappings are dynamic state) - then only the response's
    # self-consistency can be checked.
    desc_rows, desc_len, desc_declared = None, None, None
    if n_maps:
        rm, _ = do(f"READ_DESCRIPTOR AUDIO_MAP.{base_map} "
                   f"({pname}.{pi} base_map)", CMD_READ_DESCRIPTOR,
                   struct.pack('!HHHH', 0, 0, D_AUDIO_MAP, base_map))
        if rm and resp_parts(rm)[0] == 0:
            _st_m, cdl_m, pl_m = resp_parts(rm)
            dm = pl_m[RD_DESC_OFF:]
            # length from control_data_length, NOT len(frame): the
            # 60-octet Ethernet minimum pads short frames and would
            # make a truncated descriptor look complete.
            desc_len = cdl_m - 12 - RD_DESC_OFF
            if desc_len >= AM_ROWS_OFF:
                desc_declared = struct.unpack(
                    '!H', dm[AM_NUM_MAPPINGS_OFF:
                             AM_NUM_MAPPINGS_OFF + 2])[0]
                desc_rows = []
                for k in range(desc_declared):
                    o = AM_ROWS_OFF + 8 * k
                    if o + 8 > min(desc_len, len(dm)):
                        break          # truncated: (b) reports it
                    desc_rows.append(struct.unpack('!HHHH',
                                                   dm[o:o + 8]))
    return desc_rows, desc_len, desc_declared


def _cluster_channel_counts(pr, maps, n_clusters, base_cluster):
    """cluster offset -> that AUDIO_CLUSTER's channel_count, for the rows served."""
    do = pr.do
    # cluster channel counts, addressed base_cluster + offset
    cluster_channels = {}
    for _si, _sc, co, _cc in maps:
        if co in cluster_channels or co >= n_clusters:
            continue
        rc, _ = do(f"READ_DESCRIPTOR AUDIO_CLUSTER."
                   f"{base_cluster + co}", CMD_READ_DESCRIPTOR,
                   struct.pack('!HHHH', 0, 0, D_AUDIO_CLUSTER,
                               base_cluster + co))
        if rc and resp_parts(rc)[0] == 0:
            dc = rc[38 + RD_DESC_OFF:]
            if len(dc) >= AC_CHANNEL_COUNT_OFF + 2:
                cluster_channels[co] = struct.unpack(
                    '!H', dc[AC_CHANNEL_COUNT_OFF:
                             AC_CHANNEL_COUNT_OFF + 2])[0]
    return cluster_channels


def _audio_map_checks(pr, shape):
    """C9/C10/C11: AUDIO_MAP bounds, ownership and direction split."""
    a, do = pr.args, pr.do
    # ------------------------------------------------------------------ #
    # C9: AUDIO_MAP mapping bounds. Each of the four fields is bounded by a
    # DIFFERENT descriptor, and cluster_offset is port-RELATIVE (7.2.19
    # Table 7-162) - two STREAM_PORTs may legitimately publish the same
    # offsets onto different global clusters, which is why nothing else here
    # can see a global-index regression.
    # ------------------------------------------------------------------ #
    print("\n-- C9 AUDIO_MAP indices are port-relative and in range --")
    for pname, pcode, sname in (("STREAM_PORT_INPUT", D_STREAM_PORT_INPUT,
                                 'STREAM_INPUT'),
                                ("STREAM_PORT_OUTPUT", D_STREAM_PORT_OUTPUT,
                                 'STREAM_OUTPUT')):
        n_streams = len(shape.get(sname, ([], []))[0])
        stream_channels = _stream_channel_counts(pr, sname, n_streams)

        checked, skipped, viol = 0, 0, []
        over = []                              # C10 violations, this direction
        milan = []                             # C11 violations, this direction
        for pi in range(a.max_index):
            r, _ = do(f"READ_DESCRIPTOR {pname}.{pi}", CMD_READ_DESCRIPTOR,
                      struct.pack('!HHHH', 0, 0, pcode, pi))
            if not r or resp_parts(r)[0] != 0:
                break
            d = r[38 + RD_DESC_OFF:]           # the descriptor bytes
            if len(d) < 20:
                continue
            n_clusters = struct.unpack('!H', d[SP_NUM_CLUSTERS_OFF:
                                               SP_NUM_CLUSTERS_OFF + 2])[0]
            base_cluster = struct.unpack('!H', d[SP_BASE_CLUSTER_OFF:
                                                 SP_BASE_CLUSTER_OFF + 2])[0]
            n_maps = struct.unpack('!H', d[SP_NUM_MAPS_OFF:
                                           SP_NUM_MAPS_OFF + 2])[0]
            base_map = struct.unpack('!H', d[SP_BASE_MAP_OFF:
                                             SP_BASE_MAP_OFF + 2])[0]
            desc_rows, desc_len, desc_declared = _port_own_map(
                pr, pname, pi, n_maps, base_map)
            for mi in range(max(n_maps, 1)):
                r, _ = do(f"GET_AUDIO_MAP {pname}.{pi}.{mi}", CMD_GET_AUDIO_MAP,
                          struct.pack('!HHH', pcode, pi, mi))
                if r is None:
                    skipped += 1
                    continue
                st, cdl_g, pl = resp_parts(r)
                # C11: Milan v1.2 5.4.2.26's direction split, decided by this
                # port's OWN number_of_maps. Only map_index 0 is asked here;
                # a paged port's later indices are C9's business.
                if mi == 0:
                    if pcode == D_STREAM_PORT_OUTPUT and n_maps >= 1:
                        if st != STATUS_NOT_SUPPORTED:
                            milan.append(
                                f"{pname}.{pi}: has {n_maps} Audio Map(s) and "
                                f"answered status {st}; Milan 5.4.2.26 - a "
                                "GET_AUDIO_MAP for a Stream Port Output that "
                                "has Audio Map(s) 'shall reply with the "
                                "NOT_SUPPORTED error code'")
                    elif st != 0:
                        milan.append(
                            f"{pname}.{pi}: Milan 5.4.2.26 requires this port "
                            f"to implement GET_AUDIO_MAP; status {st}")
                if st in (STATUS_NOT_SUPPORTED, STATUS_NO_SUCH_DESCRIPTOR):
                    # Milan 5.4.2.28: NOT_SUPPORTED is the CONFORMANT answer
                    # on a static-map port. Skipping is the point.
                    skipped += 1
                    continue
                if st != 0 or len(pl) < AM_HDR:
                    skipped += 1
                    continue
                n_map = struct.unpack('!H', pl[8:10])[0]
                maps = []
                for k in range(n_map):
                    off = AM_HDR + 8 * k
                    if len(pl) < off + 8:
                        break
                    maps.append(struct.unpack('!HHHH', pl[off:off + 8]))
                cluster_channels = _cluster_channel_counts(
                    pr, maps, n_clusters, base_cluster)
                checked += len(maps)
                for v in audio_map_violations(maps, n_streams, stream_channels,
                                              n_clusters, cluster_channels):
                    viol.append(f"{pname}.{pi}.{mi}: {v}")
                # C10: ...and it is THIS port's map, whole and no more. Only
                # map_index 0 has a descriptor to compare against on a
                # number_of_maps = 1 port; a paged port is left to C9.
                if mi == 0:
                    for v in audio_map_overreads(
                            maps, n_map, cdl_g - 12, desc_rows, desc_len,
                            desc_declared):
                        over.append(f"{pname}.{pi}.{mi}: {v}")
        ck(not viol, f"C9 {pname} mappings within their port-relative bounds",
           f"mappings={checked} skipped={skipped} "
           f"streams={n_streams} violations={viol[:6]}")
        ck(not over, f"C10 {pname} serves its OWN AUDIO_MAP, whole and no more",
           f"violations={over[:6]}")
        ck(not milan, f"C11 {pname} follows Milan 5.4.2.26's direction split",
           f"ports={pi} violations={milan[:6]}")


def _whole_frame_checks():
    """C7/C8: the two rules every response collected owes at once."""
    # ------------------------------------------------------------------ #
    # C7/C8 run over EVERY response this tool collected, so they cost one
    # check each and cover the whole session.
    # ------------------------------------------------------------------ #
    print("\n-- C7/C8 whole-frame checks over every response --")
    # C7: 1722.1-2021 9.2.1.1.6 - control_data_length counts the octets after
    # it, so the frame must hold 14 (Ethernet) + 4 (AVTP common) + cdl. Short
    # frames are what a strict parser drops even when the status byte is right.
    short = [f"{lbl}(cdl={resp_parts(r)[1]},frame={len(r)})"
             for lbl, _c, _cc, r in SEEN
             if len(r) < 18 + resp_parts(r)[1]]
    ck(not short, "C7 every response frame is >= 18 + control_data_length",
       f"responses={len(SEEN)} short={short[:6]}")
    # C8: 9.2.2.4 message_type AEM_RESPONSE, and 7.4 - the response carries
    # the command's own command_type with u = 0 for a solicited answer.
    badhdr = []
    for lbl, cmd, _cc, r in SEEN:
        mt = r[15] & 0x0F
        u = (r[36] >> 7) & 1
        rc = ((r[36] & 0x7F) << 8) | r[37]
        if mt != 1 or u != 0 or rc != cmd:
            badhdr.append(f"{lbl}(msg={mt},u={u},cmd=0x{rc:04X})")
    ck(not badhdr, "C8 every response is AEM_RESPONSE u=0 with the command's "
                   "command_type",
       f"responses={len(SEEN)} bad={badhdr[:6]}")


def _wire_oracle_checks(pr, fmts):
    """C13: bind a real peer to our talker and read ITS counters."""
    a, s, src, ctl, tgt, nx = (pr.args, pr.sock, pr.src, pr.ctl,
                               pr.tgt, pr.nx)
    # C13: ADVERTISED == EMITTED, ON THE WIRE (opt-in). THE CHECK THAT WOULD
    # HAVE CAUGHT 2026-07-27: every other check compares a declaration
    # against another declaration; this one binds a REAL listener (the
    # reference device) to our talker and reads THAT device's Table 7-156
    # counters - UNSUPPORTED_FORMAT must stay 0 while FRAMES_RX advances.
    # Baseline for the defect it exists for: 296,294 of 296,294 frames
    # unsupported when the 8x8 advertised 8ch and the framer emitted 2.
    if a.wire_peer_eid:
        print(f"\n-- C13 wire oracle: bind peer {a.wire_peer_eid} and count --")
        peid = bytes.fromhex(a.wire_peer_eid)
        pmac = bytes.fromhex((a.wire_peer_mac or '').replace(':', ''))
        fmt = fmts.get('STREAM_OUTPUT', {}).get(a.wire_talker)
        nch = aaf_channels(fmt) if fmt is not None else None
        if nch is None:
            ck(False, f"C13 talker {a.wire_talker} advertises an AAF format",
               f"current_format={'none' if fmt is None else hex(fmt)}")
        else:
            print(f"     talker {a.wire_talker} advertises 0x{fmt:016X} "
                  f"= {nch}-channel AAF (IEEE 1722-2016 7.3.3)")
            # DISCONNECT first: a sink left bound by an earlier run reports
            # the OLD stream's counters and every number below would be a
            # measurement of the previous experiment.
            bind = Binding(ctl, tgt, peid, a.wire_talker, a.wire_sink)
            acmp(s, src, 0x02, nx(), bind)
            r = acmp(s, src, 0x00, nx(), bind)
            st = None if r is None else (r[16] >> 3) & 0x1F
            ck(st == 0, f"C13 ACMP CONNECT_RX talker {a.wire_talker} -> peer "
                        f"sink {a.wire_sink} returns SUCCESS", f"status={st}")
            if st == 0:
                sink = Peers(src, pmac, peid, ctl)
                c0 = peer_counters(s, sink, nx(),
                                   DESC['STREAM_INPUT'], a.wire_sink)
                time.sleep(a.wire_seconds)
                c1 = peer_counters(s, sink, nx(),
                                   DESC['STREAM_INPUT'], a.wire_sink)
                if not c0 or not c1:
                    ck(False, "C13 peer answered GET_COUNTERS on its sink",
                       f"before={c0} after={c1}")
                else:
                    rx = (c1['FRAMES_RX'] or 0) - (c0['FRAMES_RX'] or 0)
                    uf = (c1['UNSUPPORTED_FORMAT'] or 0) - \
                         (c0['UNSUPPORTED_FORMAT'] or 0)
                    ck(rx > 0, "C13 peer FRAMES_RX advances (the talker "
                               "emits)", f"+{rx} in {a.wire_seconds}s")
                    ck(uf == 0,
                       f"C13 peer UNSUPPORTED_FORMAT == 0 for the "
                       f"{nch}-channel format we advertise",
                       f"+{uf} unsupported of +{rx} received")
            acmp(s, src, 0x02, nx(), bind)


def main() -> int:
    """Run every block against a live entity; 1 when any check went red."""
    p = argparse.ArgumentParser()
    p.add_argument('--self-test', action='store_true',
                   help="run C9's bounds predicate over crafted good/bad "
                        "vectors and exit (no network, no device)")
    if '--self-test' in sys.argv:
        print("=== hive_compliance C9 self-test (AUDIO_MAP bounds) ===")
        return self_test()
    p.add_argument('--iface', required=True)
    p.add_argument('--target-eid', required=True)
    p.add_argument('--target-mac', required=True)
    p.add_argument('--controller-eid', default='0011223344556677')
    p.add_argument('--max-index', type=int, default=16,
                   help='highest descriptor index to probe (default 16)')
    p.add_argument('--wire-peer-eid', default=None,
                   help='C13 wire oracle: EID of a SECOND (reference) Milan '
                        'device to bind as the listener (e.g. '
                        '3CC0C60102030000). Enables C13.')
    p.add_argument('--wire-peer-mac', default=None)
    p.add_argument('--wire-talker', type=int, default=0)
    p.add_argument('--wire-sink', type=int, default=0)
    p.add_argument('--wire-seconds', type=float, default=6.0)
    p.add_argument('--adp-wait', type=float, default=6.0,
                   help='seconds to wait for the target ADPDU (C3)')
    a = p.parse_args()

    tgt = bytes.fromhex(a.target_eid)
    ctl = bytes.fromhex(a.controller_eid)
    dst = bytes.fromhex(a.target_mac.replace(':', ''))
    s = open_sock(a.iface)
    pr = Probe(s, s.getsockname()[4][:6], dst, tgt, ctl, a)

    print(f"=== hive_compliance {a.target_eid} on {a.iface} ===")
    fmts = {}   # dname -> {index: current_format} (C12/C13)

    shape = _descriptor_sweep(pr, fmts)
    _advertised_shape_checks(pr, shape)
    _non_success_size_checks(pr)
    _audio_map_checks(pr, shape)
    _whole_frame_checks()
    _wire_oracle_checks(pr, fmts)

    print(f"\n----------------------------------------")
    print(f"checks: {CHECKS[0]}   failures: {len(FAILS)}")
    for f in FAILS:
        print(f"  FAIL {f}")
    print("RESULT:", "PASS" if not FAILS else "FAIL")
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
