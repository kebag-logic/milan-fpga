#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The two SPECS a model can be built from: builtin, or a builder overlay.

Split out of `gen_aem_store.py` (Rule 12). A spec is the declarative shape -
how many streams, which formats, which clusters - in the one dict shape
`aem_assemble.build_model()` consumes. `builtin_spec()` writes the
compatibility model by hand; `spec_from_overlay()` derives the same shape
from what `sw/builder/endstation_builder.py` emitted for a config.

`gen_aem_store` re-exports every name here.
"""
from typing import Any

from aem_descriptors import (CLOCK_SOURCE, CRF_FORMATS, FORMATS, OUT_FORMATS,
                             RATES, STREAM_INPUT, firmware_version_string)

# ----------------------------------------------------------------- specs ----
def builtin_spec() -> dict[str, Any]:
    """The compatibility model expressed as a build_model() specification.

    The end-station builder's arty_current overlay maps onto this exact model
    and is test-gated. Current deployments use the selected config overlay.
    """
    return dict(
        entity=dict(name="Milan FPGA Talker",
                    firmware_version=firmware_version_string(),
                    group_name="", serial_number="AX7101-0001",
                    vendor_name="Kebag Logic"),
        rates=list(RATES), current_rate=RATES[0],
        rates_string="48/96/192 kHz",
        stream_inputs=[
            dict(name="Stream 1", kind="aaf", formats=list(FORMATS),
                 buffer=2126000),
            dict(name="CRF", kind="crf", formats=list(CRF_FORMATS),
                 buffer=2126000)],
        stream_outputs=[dict(name="Stream Output 0", formats=list(OUT_FORMATS))],
        clock_sources=[
            dict(name="Internal", cs_type=0x0000, raw_type="internal",
                 loc_type=CLOCK_SOURCE, loc_index=0),
            dict(name="Stream Clock", cs_type=0x0002, raw_type="input_stream",
                 loc_type=STREAM_INPUT, loc_index=0),
            dict(name="CRF Clock", cs_type=0x0002, raw_type="crf",
                 loc_type=STREAM_INPUT, loc_index=1)],
        # Milan v1.2 5.3.3.9: every Stream Port Input is dynamic and carries
        # no AUDIO_MAP descriptor. The output remains the compatibility
        # model's one static map, densely renumbered to descriptor index 0.
        ports_in=[dict(clusters=8, base_cluster=0, maps=0, base_map=0,
                       map_mode="dynamic", map_page=8)],
        ports_out=[dict(clusters=8, base_cluster=8, maps=1, base_map=0)],
        audio_maps=[[[0, ch, ch, 0] for ch in range(8)]],
        # D10 role names for the DEPLOYED arty shape, and the reason this
        # list is written out rather than computed: this spec is the
        # pre-builder model, and endstation_arty_current.yaml must reproduce
        # it byte-for-byte through the overlay path (test_builder gate 10).
        # The arty routes a 2-channel Philips I2S link (Pmod I2S2: CS4344 DAC
        # out, ADC in), so clusters 0..1 per direction are PHYSICAL and 2..7
        # are the virtual tail of the Milan 6.4 up-to-8 family.
        cluster_names_in=[f"I2S Out {n}" for n in range(2)]
                         + [f"Virtual Out {n}" for n in range(2, 8)],
        cluster_names_out=[f"I2S In {n}" for n in range(2)]
                          + [f"Virtual In {n}" for n in range(2, 8)],
        # The gPTP dataset of the DEPLOYED arty shape, written out for the
        # same reason as the cluster names: the overlay path must reproduce
        # it byte-for-byte (test_builder gate 10). The values are the fabric
        # engine's pinned Announce dataset ([R-parallel] on #228): the
        # builder derives them from gptp-processor/hdl/ucode/
        # gen_gptp_ucode.py and refuses a diverging config, so a drift here
        # breaks gate 10 loudly instead of shipping two clocks.
        gptp=dict(priority1=0xF8, priority2=0xF8, clock_class=0xF8,
                  clock_accuracy=0xFE, offset_scaled_log_variance=0x436A,
                  domain=0, log_sync_interval=-3, log_announce_interval=0,
                  log_pdelay_interval=0),
    )

def _out_identity_offset(p):
    """Identity image origin for a dynamic output port: the port-relative
    offset of its PRIMARY pool segment (the same segment the static map
    wired at power-on - the builder's primary_role, carried by the
    overlay). Ports without pools start at 0."""
    prim = p.get("primary_role")
    for g in p.get("pool", []):
        if g["role"] == prim:
            return int(g["offset"])
    return 0


def _out_cluster_sources(ovl, j, p):
    """Capture-crossbar source templates for a dynamic OUTPUT port's
    clusters, derived from the overlay's D8 role pool. One dict per
    cluster: {src, idxh, idx, half, valid} in KL_chan_map_capture bucket
    terms (2 PHYSICAL / 4 TONE / 5 LOOP). Encoding 3 is retired and remains
    reserved-zero in RTL. Bounds are the fabric's: 4 physical pairs and
    8 loopback streams x 4 pairs. Static ports need no templates and return
    None. A dynamic port without its builder-emitted role pool is ambiguous:
    counts alone cannot recover whether a cluster is physical, pilot,
    loopback, or virtual, so a stale/custom overlay must be regenerated."""
    if p.get("map_mode", "static") != "dynamic":
        return None
    if not p.get("pool"):
        raise ValueError(
            f"stream_ports.output[{j}]: dynamic output has no nonempty "
            "source pool; regenerate the AEM overlay so its source topology "
            "is explicit")
    # the received stream channel space, mirroring the builder's
    # cluster_names() walk: loopback cluster n of port j starts at rx
    # stream j channel 0
    rx = []
    for si, s in enumerate(ovl["stream_inputs"]):
        if s.get("kind", "aaf") != "aaf":
            continue
        ch = (int(s["formats"][0], 16) >> 22) & 0x3FF
        rx.extend((si, c) for c in range(ch))
    # task #65: what the BITSTREAM behind this model actually elaborates.
    # A template's `valid` is what the identity image below tests before it
    # wires a stream channel to a cluster, so this is the join between the
    # model and the gateware - and it is exactly what was missing when every
    # talker woke mapped to a loopback cluster no fabric could feed.
    fab = ovl.get("cluster_fabric") or {}
    lb_lane = bool(fab.get("loopback_lane", True))
    srcs = []
    for g in p["pool"]:
        for n in range(g["width"]):
            if g["role"] == "physical":
                # capture phys channel (role_pool first=0). UNIFORM across
                # every front-end shape, because milan_datapath feeds the
                # slot-indexed bucket from aafcap_* whatever the front end is,
                # and an I2S-only capture parks at slot 0.
                #
                # This used to special-case channels 0..1 onto src=1 (the
                # single-pair I2S hold) and the rest onto src=2 offset by two,
                # which described the Arty BLEND topology and nothing else. It
                # was wrong two ways on a solo TDM master: the first two
                # channels aliased one hold that ignores idx, and the rest were
                # offset past their real slots. Nothing caught it because no
                # shipping config reaches this branch - the role-pool shapes
                # declare 0 physical channels and the shapes that declare
                # physical channels use the default (non-pool) policy.
                a = n
                srcs.append(dict(src=2, idxh=0, idx=a // 2, half=a % 2,
                                 valid=a // 2 < 4))   # 4 pair holds in fabric
            elif g["role"] == "pilot":
                srcs.append(dict(src=4, idxh=0, idx=0, half=0, valid=True))
            elif g["role"] == "loopback":
                if rx:
                    start = next((k for k, (si, c) in enumerate(rx)
                                  if si == j and c == 0), 0)
                    si, c = rx[(start + n) % len(rx)]
                else:
                    si, c = 0, n
                srcs.append(dict(src=5, idxh=si, idx=c // 2, half=c % 2,
                                 # the LOOP bucket only exists when
                                 # milan_datapath was built with LOOPBACK_P
                                 valid=lb_lane and si < 8 and c < 8))
            elif g["role"] == "virtual":
                srcs.append(dict(src=0, idxh=0, idx=0, half=n % 2,
                                 valid=False))
            else:
                raise ValueError(f"unsupported output cluster role {g['role']!r}")
    return srcs


def spec_from_overlay(ovl: dict[str, Any]) -> dict[str, Any]:
    """Map a builder-emitted AEM overlay (kebag-logic/aem-overlay 2.x, see
    sw/builder/endstation_builder.py emit_aem_overlay) onto a build_model()
    spec. Structure (N ports/streams) is fully consumed, including a CRF
    Media Clock Output (Milan 7.2.3: stream_outputs entry kind "crf" —
    appended after the AAF talkers, no STREAM_PORT/cluster/map, mirroring
    the CRF sink). Multi-stream shapes additionally emit the per-descriptor
    format tables (AEM_STRIN_*/AEM_STROUT_*, gated behind the stream count
    so the deployed shape's svh stays byte-identical — see emit_svh)."""
    if ovl.get("_schema") != "kebag-logic/aem-overlay":
        raise ValueError("not a kebag-logic/aem-overlay document")
    if not str(ovl.get("_schema_version", "")).startswith("2."):
        raise ValueError(f"overlay schema {ovl.get('_schema_version')} "
                         "(this consumer speaks 2.x)")
    ent = ovl["entity"]
    rates_hz = [int(r) for r in ovl["sampling_rates_hz"]]
    if any(hz not in (48000, 96000, 192000) for hz in rates_hz):
        raise ValueError(f"unsupported sampling rates {rates_hz}")
    if "firmware_version" not in ent:
        # No default here on purpose: the "0.1.0" that used to sit in this
        # position is exactly how a shape with no declared version shipped a
        # wrong one to every controller.  An overlay that cannot say what
        # firmware it is does not get a descriptor set.
        raise ValueError(
            "overlay entity has no firmware_version - the builder derives it "
            "from hdl/common/csr/milan_csr.sv VERSION (firmware_version_"
            "string()); regenerate the overlay")
    if not any(s["kind"] == "crf" for s in ovl["stream_inputs"]):
        raise ValueError("overlay without a CRF sink is not expressible in "
                         "the svh consumer today (AEM_CRF_FMTS_C)")
    cs_type = {"internal": 0x0000, "input_stream": 0x0002, "crf": 0x0002}
    loc_type = {"CLOCK_SOURCE": CLOCK_SOURCE, "STREAM_INPUT": STREAM_INPUT}
    stream_flags_in = 0x0003
    return dict(
        entity=dict(name=ent["name"],
                    firmware_version=ent["firmware_version"],
                    group_name=ent.get("group_name", ""),
                    serial_number=ent["serial_number"],
                    vendor_name=ent.get("vendor_name", "Kebag Logic")),
        gptp=ovl.get("gptp"),           # AVB_INTERFACE clock attributes
                                        # (one source, the config overlay)
        rates=rates_hz,                 # pull-0 encoding == Hz value
        current_rate=int(ovl["current_sampling_rate_hz"]),
        rates_string="/".join(str(hz // 1000) for hz in rates_hz) + " kHz",
        stream_inputs=[
            dict(name=s["name"], kind=s["kind"],
                 formats=[int(f, 16) for f in s["formats"]],
                 buffer=int(s.get("buffer_length_ns", 2126000)))
            for s in ovl["stream_inputs"]],
        stream_outputs=[
            dict(name=s["name"], kind=s.get("kind", "aaf"),
                 formats=[int(f, 16) for f in s["formats"]])
            for s in ovl["stream_outputs"]],
        clock_sources=[
            dict(name=c["name"], cs_type=cs_type[c["type"]],
                 raw_type=c["type"],
                 loc_type=loc_type[c["location_type"]],
                 loc_index=int(c["location_index"]))
            for c in ovl["clock_sources"]],
        ports_in=[dict(clusters=p["clusters"], base_cluster=p["base_cluster"],
                       maps=p["maps"], base_map=p["base_map"],
                       map_mode=p.get("map_mode", "static"),
                       map_page=p.get("map_page"))
                  for p in ovl["stream_ports"]["input"]],
        ports_out=[dict(clusters=p["clusters"], base_cluster=p["base_cluster"],
                        maps=p["maps"], base_map=p["base_map"],
                        map_mode=p.get("map_mode", "static"),
                        stream_index=p.get("stream_index", j),
                        cluster_sources=_out_cluster_sources(ovl, j, p),
                        identity_offset=_out_identity_offset(p))
                   for j, p in enumerate(ovl["stream_ports"]["output"])],
        audio_maps=[m["mappings"] for m in
                    sorted(ovl["audio_maps"], key=lambda m: m["index"])],
        # D10 cluster names (overlay 2.1+). An older 2.0 overlay carries no
        # audio_clusters list and falls back to the pre-rename "Input"/
        # "Output", so a stale overlay still builds a valid - if mute - model.
        cluster_names_in=[c["name"] for c in
                          sorted(ovl.get("audio_clusters", []),
                                 key=lambda c: c["index"])
                          if c["direction"] == "input"] or None,
        cluster_names_out=[c["name"] for c in
                           sorted(ovl.get("audio_clusters", []),
                                  key=lambda c: c["index"])
                           if c["direction"] == "output"] or None,
        _stream_flags_in=stream_flags_in,
    )

