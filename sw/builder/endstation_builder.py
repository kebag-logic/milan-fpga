#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
endstation_builder.py - software-defined Milan End-Station builder.

docs/MILAN_COMPLIANCE_GAPS.md attack item 4: ONE declarative definition
drives gateware elaboration, AEM ROM, lwSRP tables and DT/driver shape
consistently. This round turns the scaffold into the working generator:
the emitted AEM overlay is CONSUMED by avdecc/gen_aem_store.py (--overlay)
and, for the current shape, reproduces the tracked aecp_aem_rom.svh
byte-identically; the emitted sweep_opts fragment is SOURCED by
sw/litex/sweep.sh (single source for the per-board design OPTS/L2).

Input:  a YAML end-station config (schema kebag-logic/milan-endstation-config,
        see configs/endstation_*.yaml for annotated examples).

Outputs (into OUTDIR/<config-stem>/):
  soc_params.json   - the sw/litex/milan_soc.py argv this config implies
                      (design flags only; flow flags like --build /
                      --vivado-max-threads / --place-directive belong to
                      sweep.sh, not to the end-station definition).
  aem_overlay.json  - AEM model overlay (descriptor counts, stream formats,
                      per-stream STREAM_PORT/cluster/map layout) consumed by
                      avdecc/gen_aem_store.py --overlay.
  build_plan.md     - human-readable build plan. Shapes beyond current RTL
                      capability (NxN streams, TDM/AES3/SPDIF interfaces,
                      non-48k rates) VALIDATE but are marked "planned".
Plus (into configs/generated/, board-level, shared by all configs of a board):
  sweep_opts_<board>.sh - shell fragment (OPTS/L2) sourced by
                      sw/litex/sweep.sh; the inline tables there are the
                      loud FALLBACK only.

Usage:
  python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml
  python3 sw/builder/endstation_builder.py <cfg.yaml> -o <outdir>

Schema summary (see the example configs for the annotated normative form):
  schema / schema_version      - "kebag-logic/milan-endstation-config" / 1.1.x
  entity:                      - identity: name, entity_model_id
                                 ("hash-derived" | EUI-64 hex), model_id_pin
                                 (optional EUI-64 hex override - pins the id
                                 of already-flashed silicon), entity_id
                                 ("mac-derived" | EUI-64 hex), vendor_name,
                                 firmware_version, serial_number, group_name
  board: target + constraints  - arty | ax7101; physical facts the SoC argv
                                 derives from (sys/milan clk, l2, phy, flash,
                                 uart, rx queues, hs page, probes, GMII knobs,
                                 eth_port for multi-port boards)
  clocking:                    - sampling_rate_hz, audio_unit_rates_hz,
                                 media_clock_sources (internal | input_stream
                                 | crf), default_source, crf_sink (+format),
                                 audio_pll_hz (clean MMCM audio clock)
  audio_interface:             - kind: tdm8|tdm16|tdm32|i2s_philips|aes3|spdif
                                 word_length_bits, cluster_mapping.policy
                                 (cap-at-interface |
                                  cluster-per-stream-channel)
  streams:                     - listeners[] / talkers[]: name, channels,
                                 formats (AAF 64-bit hex), buffer_length_ns,
                                 clusters (SINGLE AUTHORITY for the stream's
                                 cluster count; default = channels)

entity_model_id derivation ("hash-derived", the default path; exact recipe,
also in sw/builder/README-parameters.md):
  1. shape = the model-shaping fields only (stream counts/formats/clusters/
     buffers, cluster policy, derived per-stream port layout, audio
     interface kind/channels/word length, sampling rates, CRF sink+format) -
     NO board flags, names or serials, so two boards with the same audio
     shape share a model id (AEM semantics).
  2. canon = json.dumps(shape, sort_keys=True, separators=(",", ":"))
  3. id = (MODEL_ID_OUI << 40) | (int.from_bytes(sha256(canon)[:8]) & (2^40-1))
     i.e. top-8-bytes of the sha256, folded under the base EUI-64 prefix
     MODEL_ID_OUI = 0x001BC5 (Kebag Logic OUI, kept HERE in the schema).
  Same shape -> same id; any shape change -> new id. entity.model_id_pin
  overrides the hash (already-flashed silicon keeps its identity).
"""

import argparse
import hashlib
import json
import os
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("endstation_builder: PyYAML required (python3 -m pip install pyyaml)")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

SCHEMA_ID = "kebag-logic/milan-endstation-config"
SCHEMA_MAJOR = "1"

OVERLAY_SCHEMA_ID = "kebag-logic/aem-overlay"
OVERLAY_SCHEMA_VERSION = "2.0.0"     # 2.x: per-stream STREAM_PORT layout

# Base EUI-64 prefix for hash-derived entity_model_id values (see module
# docstring step 3). Schema-level constant: changing it re-identifies every
# hash-derived model - never change it casually.
MODEL_ID_OUI = 0x001BC5              # Kebag Logic vendor OUI (00-1B-C5)
MODEL_ID_HASH_BITS = 40              # EUI-64 bits taken from the sha256

CLUSTER_POLICIES = ("cap-at-interface", "cluster-per-stream-channel")


class ConfigError(Exception):
    """Raised for any config that violates the schema or board physics."""


# ------------------------------------------------------------------ tables --
# Board physical truth (cross-checked against configs; the config carries the
# values so the emitted argv is reviewable, the table rejects impossibilities).
BOARDS = {
    "arty": dict(
        phy="mii-100", link_mbps=100,
        sys_clk_hz_default=100_000_000,      # milan_soc.py --sys-clk-freq default
        gmii_knobs=False,                    # --gtx-tx-invert is a GMII fix
        eth_ports=(),                        # single PHY: no --eth-port choice
    ),
    "ax7101": dict(
        phy="gmii-1g", link_mbps=1000,
        sys_clk_hz_default=100_000_000,
        gmii_knobs=True,
        eth_ports=("e1", "e2"),              # e2 = ship port since 2026-07-22
    ),
}

# Physical audio interfaces (item-4 subtask). channels = per direction.
# Only i2s_philips exists in RTL today (KL_i2s_playback / aaf_talker_i2s).
INTERFACES = {
    "i2s_philips": dict(channels=2,  word_bits=(16, 24),     rtl="present"),
    "tdm8":        dict(channels=8,  word_bits=(16, 24, 32), rtl="planned"),
    "tdm16":       dict(channels=16, word_bits=(16, 24, 32), rtl="planned"),
    "tdm32":       dict(channels=32, word_bits=(16, 24, 32), rtl="planned"),
    "aes3":        dict(channels=2,  word_bits=(16, 20, 24), rtl="planned"),
    "spdif":       dict(channels=2,  word_bits=(16, 20, 24), rtl="planned"),
}

# SoC-glue policy defaults (overridable via the optional `soc:` section).
# These mirror today's ship recipe = sw/litex/sweep.sh BASE (design flags).
SOC_DEFAULTS = dict(
    cpu="vexiiriscv",
    cpu_count=1,
    all_blocks=True,
    coherent_dma=True,
    timing_opt=True,
    scala_args=[
        "--lsu-l1-refill-count=8",
        "--lsu-hardware-prefetch=rpt",
        "--l2-down-pending=8",
        "--l2-general-slots=16",
    ],
)

# What the RTL supports TODAY (milan_datapath.sv). Anything beyond validates
# but lands in the plan as "planned", never as an error (builder contract).
RTL_TODAY = dict(
    max_aaf_listeners=1,
    max_talkers=1,
    crf_sink=True,
    interfaces={"i2s_philips"},
    render_channels=2,          # wire-truth rule: extra stream chans virtual
    sampling_rates={48000},
)

CRF_FORMAT_DEFAULT = "0x041060010000BB80"     # CRF AUDIO_SAMPLE 48k, gen_aem_store
BUFLEN_DEFAULT_NS = 2126000


def aaf_pcm32_48k(channels, ut=False):
    """AAF PCM 32-bit 48k-base stream format qword (channels at bits [31:22]
    of the low word; ut = bit 52 'up-to' family bit). Reproduces the
    gen_aem_store.py constants: 2ch=0x0205022000806000, 8ch=0x0205022002006000,
    ut8=0x0215022002006000."""
    base = 0x0205022000006000
    if ut:
        base |= 1 << 52
    return base | (channels << 22)


# --------------------------------------------------------------- validation --
def _req(d, key, ctx):
    if key not in d:
        raise ConfigError(f"{ctx}: missing required key '{key}'")
    return d[key]


def _eui64(v, ctx):
    try:
        n = int(str(v), 16)
    except ValueError:
        raise ConfigError(f"{ctx}: '{v}' is not a hex EUI-64")
    if not 0 <= n <= 0xFFFFFFFFFFFFFFFF:
        raise ConfigError(f"{ctx}: '{v}' out of EUI-64 range")
    return n


def _fmt64(v, ctx):
    n = _eui64(v, ctx)
    return f"0x{n:016X}"


def _pow2(v, ctx):
    if not (isinstance(v, int) and v > 0 and (v & (v - 1)) == 0):
        raise ConfigError(f"{ctx}: {v} must be a power of two")
    return v


def _streams(lst, ctx, direction):
    if not isinstance(lst, list) or not lst:
        raise ConfigError(f"{ctx}: needs at least one {direction} stream")
    if len(lst) > 16:
        raise ConfigError(f"{ctx}: {len(lst)} streams (max 16 per direction)")
    out = []
    for k, s in enumerate(lst):
        sctx = f"{ctx}[{k}]"
        ch = _req(s, "channels", sctx)
        if not (isinstance(ch, int) and 1 <= ch <= 32):
            raise ConfigError(f"{sctx}: channels {ch} outside 1..32")
        fmts = s.get("formats") or [f"0x{aaf_pcm32_48k(ch):016X}"]
        fmts = [_fmt64(f, f"{sctx}.formats") for f in fmts]
        clusters = s.get("clusters", ch)
        if not (isinstance(clusters, int) and 1 <= clusters <= 32):
            raise ConfigError(f"{sctx}: clusters {clusters} outside 1..32")
        out.append(dict(
            name=s.get("name", f"Stream {'In' if direction == 'listener' else 'Out'} {k}"),
            channels=ch, formats=fmts, clusters=clusters,
            buffer_length_ns=s.get("buffer_length_ns", BUFLEN_DEFAULT_NS),
        ))
    return out


# --------------------------------------------------- cluster/port layout ----
def cluster_layout(listeners, talkers, policy, iface_channels):
    """USER decision: ONE STREAM_PORT per stream. Each listener stream gets a
    STREAM_PORT_INPUT, each talker stream a STREAM_PORT_OUTPUT; every port
    owns a contiguous AUDIO_CLUSTER block and exactly one AUDIO_MAP whose
    cluster offsets are RELATIVE to the port's base_cluster (1722.1-2021
    7.2.19). AUDIO_MAP descriptor indexes: input ports first (map i = port
    i), then output ports (map len(L)+j = port j).

    Cluster-count policy (USER decision, config-selectable):
      cluster-per-stream-channel - the stream's `clusters` field verbatim
        (default = channels; the legacy/pipewire-reference layout).
      cap-at-interface - min(clusters, physical interface channels/direction):
        clusters model real endpoints, never more than the wire has.
    Returns (ports_in, ports_out)."""
    if policy not in CLUSTER_POLICIES:
        raise ConfigError(f"cluster policy '{policy}' not in {CLUSTER_POLICIES}")

    def eff(s):
        if policy == "cap-at-interface":
            return min(s["clusters"], iface_channels)
        return s["clusters"]

    ports_in, base = [], 0
    for i, s in enumerate(listeners):
        n = eff(s)
        ports_in.append(dict(index=i, stream_index=i, clusters=n,
                             base_cluster=base, maps=1, base_map=i))
        base += n
    ports_out = []
    for j, s in enumerate(talkers):
        n = eff(s)
        ports_out.append(dict(index=j, stream_index=j, clusters=n,
                              base_cluster=base, maps=1,
                              base_map=len(listeners) + j))
        base += n
    return ports_in, ports_out


# ------------------------------------------------------- model-id hashing ---
def model_shape(cfg):
    """The model-shaping fields ONLY (no board flags / names / serials): the
    input to the hash-derived entity_model_id. Any key added here changes
    every hash-derived id - extend deliberately."""
    i, clk = cfg["interface"], cfg["clocking"]
    return {
        "cluster_policy": i["cluster_policy"],
        "interface": {"kind": i["kind"], "channels": i["channels"],
                      "word_length_bits": i["word_length_bits"]},
        "rates_hz": clk["audio_unit_rates_hz"],
        "current_rate_hz": clk["sampling_rate_hz"],
        "crf_sink": clk["crf_sink"],
        "crf_format": clk["crf_format"],
        "listeners": [{"channels": s["channels"], "formats": s["formats"],
                       "clusters": s["clusters"],
                       "buffer_length_ns": s["buffer_length_ns"]}
                      for s in cfg["listeners"]],
        "talkers": [{"channels": s["channels"], "formats": s["formats"],
                     "clusters": s["clusters"]} for s in cfg["talkers"]],
        "ports_in": [[p["base_cluster"], p["clusters"], p["base_map"]]
                     for p in cfg["ports_in"]],
        "ports_out": [[p["base_cluster"], p["clusters"], p["base_map"]]
                      for p in cfg["ports_out"]],
    }


def derive_model_id(shape):
    """Deterministic EUI-64 from the model shape (recipe in the module
    docstring + sw/builder/README-parameters.md)."""
    canon = json.dumps(shape, sort_keys=True, separators=(",", ":")).encode()
    top8 = int.from_bytes(hashlib.sha256(canon).digest()[:8], "big")
    mask = (1 << MODEL_ID_HASH_BITS) - 1
    return (MODEL_ID_OUI << MODEL_ID_HASH_BITS) | (top8 & mask)


def load_config(path):
    """Load + validate + normalize a YAML end-station config. Returns the
    normalized config dict; raises ConfigError on any violation."""
    with open(path) as f:
        cfg = yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise ConfigError(f"{path}: not a YAML mapping")

    if cfg.get("schema") != SCHEMA_ID:
        raise ConfigError(f"{path}: schema must be '{SCHEMA_ID}'")
    ver = str(cfg.get("schema_version", ""))
    if not ver.startswith(SCHEMA_MAJOR + "."):
        raise ConfigError(f"{path}: schema_version {ver} (need {SCHEMA_MAJOR}.x)")

    # entity (entity_model_id resolved AFTER streams/interface: hash needs
    # the derived layout)
    ent = _req(cfg, "entity", path)
    n = dict(
        name=_req(ent, "name", "entity"),
        vendor_name=ent.get("vendor_name", "Kebag Logic"),
        firmware_version=ent.get("firmware_version", "0.1.0"),
        serial_number=_req(ent, "serial_number", "entity"),
        group_name=ent.get("group_name", ""),
    )
    eid = ent.get("entity_id", "mac-derived")
    n["entity_id"] = eid if eid == "mac-derived" else _fmt64(eid, "entity.entity_id")
    for k in ("name", "serial_number", "group_name", "firmware_version"):
        if len(str(n[k]).encode()) > 63:
            raise ConfigError(f"entity.{k}: exceeds 63 bytes (AEM cstr64)")
    entity = n

    # board
    brd = _req(cfg, "board", path)
    target = _req(brd, "target", "board")
    if target not in BOARDS:
        raise ConfigError(f"board.target '{target}' not in {sorted(BOARDS)}")
    binfo = BOARDS[target]
    c = _req(brd, "constraints", "board")
    cons = dict(
        sys_clk_hz=int(c.get("sys_clk_hz", binfo["sys_clk_hz_default"])),
        milan_clk_hz=int(_req(c, "milan_clk_hz", "board.constraints")),
        l2_bytes=_pow2(_req(c, "l2_bytes", "board.constraints"),
                       "board.constraints.l2_bytes"),
        phy=_req(c, "phy", "board.constraints"),
        gtx_tx_invert=bool(c.get("gtx_tx_invert", False)),
        floorplan=bool(c.get("floorplan", False)),
        flashboot=c.get("flashboot", "full"),
        uart_baudrate=int(c.get("uart_baudrate", 115200)),
        rx_queues=int(c.get("rx_queues", 2)),
        hs_page_bytes=_pow2(c.get("hs_page_bytes", 16384),
                            "board.constraints.hs_page_bytes"),
        strip_probes=bool(c.get("strip_probes", True)),
        eth_port=c.get("eth_port"),
    )
    if cons["phy"] != binfo["phy"]:
        raise ConfigError(f"board.constraints.phy '{cons['phy']}' contradicts "
                          f"{target} ({binfo['phy']})")
    if cons["gtx_tx_invert"] and not binfo["gmii_knobs"]:
        raise ConfigError(f"gtx_tx_invert is a GMII knob; {target} is {binfo['phy']}")
    if cons["flashboot"] not in ("none", "kernel", "full"):
        raise ConfigError(f"flashboot '{cons['flashboot']}' not none|kernel|full")
    if not 1 <= cons["rx_queues"] <= 2:
        raise ConfigError(f"rx_queues {cons['rx_queues']} outside 1..2")
    if not cons["milan_clk_hz"] <= cons["sys_clk_hz"]:
        raise ConfigError("milan_clk_hz must not exceed sys_clk_hz")
    if cons["eth_port"] is not None and cons["eth_port"] not in binfo["eth_ports"]:
        raise ConfigError(f"board.constraints.eth_port '{cons['eth_port']}' "
                          f"invalid for {target} (choices {binfo['eth_ports'] or '(none)'})")

    # clocking
    clk = _req(cfg, "clocking", path)
    rate = int(_req(clk, "sampling_rate_hz", "clocking"))
    if rate not in (48000, 96000, 192000):
        raise ConfigError(f"sampling_rate_hz {rate} not an AAF base rate")
    srcs = clk.get("media_clock_sources", ["internal", "input_stream", "crf"])
    bad = set(srcs) - {"internal", "input_stream", "crf"}
    if bad:
        raise ConfigError(f"media_clock_sources: unknown {sorted(bad)}")
    dflt = clk.get("default_source", srcs[0])
    if dflt not in srcs:
        raise ConfigError(f"default_source '{dflt}' not in media_clock_sources")
    clocking = dict(
        sampling_rate_hz=rate,
        audio_unit_rates_hz=[int(r) for r in
                             clk.get("audio_unit_rates_hz", [rate])],
        media_clock_sources=list(srcs),
        default_source=dflt,
        crf_sink=bool(clk.get("crf_sink", True)),
        crf_format=_fmt64(clk.get("crf_format", CRF_FORMAT_DEFAULT),
                          "clocking.crf_format"),
        audio_pll_hz=int(clk.get("audio_pll_hz", 24_576_000)),
    )
    if rate not in clocking["audio_unit_rates_hz"]:
        raise ConfigError("sampling_rate_hz must appear in audio_unit_rates_hz")
    if clocking["crf_sink"] and "crf" not in srcs:
        raise ConfigError("crf_sink needs 'crf' in media_clock_sources")

    # audio interface
    aif = _req(cfg, "audio_interface", path)
    kind = _req(aif, "kind", "audio_interface")
    if kind not in INTERFACES:
        raise ConfigError(f"audio_interface.kind '{kind}' not in {sorted(INTERFACES)}")
    iinfo = INTERFACES[kind]
    wl = int(aif.get("word_length_bits", 24))
    if wl not in iinfo["word_bits"]:
        raise ConfigError(f"word_length_bits {wl} invalid for {kind} "
                          f"(allowed {iinfo['word_bits']})")
    cm = aif.get("cluster_mapping") or {}
    if "rule" in cm:
        raise ConfigError("cluster_mapping.rule was replaced by "
                          "cluster_mapping.policy in schema 1.1 "
                          f"(choices {CLUSTER_POLICIES})")
    policy = cm.get("policy", "cluster-per-stream-channel")
    if policy not in CLUSTER_POLICIES:
        raise ConfigError(f"cluster_mapping.policy '{policy}' not in "
                          f"{CLUSTER_POLICIES}")
    interface = dict(
        kind=kind, channels=iinfo["channels"], word_length_bits=wl,
        cluster_policy=policy,
    )

    # streams
    st = _req(cfg, "streams", path)
    listeners = _streams(_req(st, "listeners", "streams"), "streams.listeners",
                         "listener")
    talkers = _streams(_req(st, "talkers", "streams"), "streams.talkers",
                       "talker")

    # soc policy overrides
    soc = dict(SOC_DEFAULTS, **(cfg.get("soc") or {}))
    if soc["cpu"] not in ("vexiiriscv", "naxriscv"):
        raise ConfigError(f"soc.cpu '{soc['cpu']}' unknown")

    out = dict(
        source=os.path.relpath(path, ROOT),
        name=os.path.splitext(os.path.basename(path))[0],
        entity=entity, board_target=target, constraints=cons,
        clocking=clocking, interface=interface,
        listeners=listeners, talkers=talkers, soc=soc,
    )

    # per-stream port layout (needed by the model-id hash and the overlay)
    out["ports_in"], out["ports_out"] = cluster_layout(
        listeners, talkers, policy, interface["channels"])

    # entity_model_id resolution: pin > hash-derived > literal
    shape = model_shape(out)
    hashed = derive_model_id(shape)
    raw = _req(ent, "entity_model_id", "entity")
    pin = ent.get("model_id_pin")
    if pin is not None:
        mid, src = _eui64(pin, "entity.model_id_pin"), "pin"
    elif raw == "hash-derived":
        mid, src = hashed, "hash"
    else:
        mid, src = _eui64(raw, "entity.entity_model_id"), "literal"
    entity["entity_model_id"] = f"0x{mid:016X}"
    out["model_id"] = dict(value=f"0x{mid:016X}", source=src,
                           hash=f"0x{hashed:016X}")
    return out


# ----------------------------------------------------- RTL capability marks --
def rtl_capability_marks(cfg):
    """(element, status, note) per config element; status is 'supported' or a
    'planned (...)' marker - NEVER an error (the builder validates NxN shapes,
    the RTL catches up in items 5/4-audio)."""
    marks = []
    n_l, n_t = len(cfg["listeners"]), len(cfg["talkers"])
    if n_l > RTL_TODAY["max_aaf_listeners"]:
        marks.append((f"{n_l} AAF listener streams",
                      "planned (item 5 - NxN AAF streams)",
                      f"RTL today: {RTL_TODAY['max_aaf_listeners']} AAF listener "
                      f"+ CRF sink; needs per-stream ACMP/MAAP/monitor contexts"))
    else:
        marks.append((f"{n_l} AAF listener stream(s)", "supported", ""))
    if n_t > RTL_TODAY["max_talkers"]:
        marks.append((f"{n_t} AAF talker streams",
                      "planned (item 5 - NxN AAF streams)",
                      f"RTL today: {RTL_TODAY['max_talkers']} talker"))
    else:
        marks.append((f"{n_t} AAF talker stream(s)", "supported", ""))
    if cfg["clocking"]["crf_sink"]:
        marks.append(("CRF media-clock sink", "supported", "KL_crf_rx"))
    kind = cfg["interface"]["kind"]
    if kind in RTL_TODAY["interfaces"]:
        marks.append((f"audio interface {kind}", "supported",
                      "KL_i2s_playback / aaf_talker_i2s"))
    else:
        marks.append((f"audio interface {kind}",
                      "planned (item 4 subtask - audio interfaces + cluster mapping)",
                      "needs ser/des RTL family selection under the "
                      "spec-aligned tree (TDM slots / biphase-mark for AES3-SPDIF)"))
    rate = cfg["clocking"]["sampling_rate_hz"]
    if rate in RTL_TODAY["sampling_rates"]:
        marks.append((f"{rate} Hz media clock", "supported", ""))
    else:
        marks.append((f"{rate} Hz media clock",
                      "planned (item 6 - MMCM-DRP media-clock servo)",
                      "render path is 48k-only today"))
    max_ch = max(s["channels"] for s in cfg["listeners"])
    if max_ch > RTL_TODAY["render_channels"] and kind in RTL_TODAY["interfaces"]:
        marks.append((f"{max_ch}ch listener formats on a "
                      f"{cfg['interface']['channels']}ch physical interface",
                      "supported",
                      "wire-truth 1-to-1 rule: physical channels bind in "
                      "order, extra stream channels render as virtual"))
    return marks


# ------------------------------------------------------------ soc_params ----
def _freq(hz):
    """Render a frequency the way the build scripts write it (83.333e6)."""
    return f"{hz / 1e6:g}e6"


def emit_board_opts(cfg):
    """The board-specific design-flag prefix of the argv = EXACTLY the OPTS
    string sw/litex/sweep.sh keeps per board (test-gated byte match)."""
    c, binfo = cfg["constraints"], BOARDS[cfg["board_target"]]
    opts = ["--board", cfg["board_target"]]
    if c["sys_clk_hz"] != binfo["sys_clk_hz_default"]:
        opts += ["--sys-clk-freq", _freq(c["sys_clk_hz"])]
    opts += ["--milan-clk-freq", _freq(c["milan_clk_hz"])]
    if c["gtx_tx_invert"]:
        opts += ["--gtx-tx-invert"]
    if c["floorplan"]:
        opts += ["--floorplan"]
    if c["eth_port"]:
        opts += ["--eth-port", c["eth_port"]]
    return opts


def emit_soc_argv(cfg):
    """The milan_soc.py DESIGN argv this config implies (flow flags -
    --build/--vivado-max-threads/--place-directive/--output-dir - are
    sweep.sh's business, not the end-station definition's)."""
    c, soc = cfg["constraints"], cfg["soc"]
    argv = list(emit_board_opts(cfg))
    argv += ["--cpu", soc["cpu"]]
    if soc["all_blocks"]:
        argv += ["--all-blocks"]
    if soc["coherent_dma"]:
        argv += ["--coherent-dma"]
    if c["flashboot"] != "none":
        argv += ["--with-spiflash", "--flashboot", c["flashboot"]]
    if soc["timing_opt"]:
        argv += ["--timing-opt"]
    argv += ["--l2-bytes", str(c["l2_bytes"])]
    argv += [f"--scala-args={a}" for a in soc["scala_args"]]
    argv += ["--uart-baudrate", str(c["uart_baudrate"])]
    argv += ["--rx-queues", str(c["rx_queues"])]
    if c["strip_probes"]:
        argv += ["--strip-probes"]
    argv += ["--hs-page-bytes", str(c["hs_page_bytes"])]
    argv += ["--cpu-count", str(soc["cpu_count"])]
    return argv


# ------------------------------------------------------------ sweep opts ----
def emit_sweep_opts(cfg):
    """Shell fragment sourced by sw/litex/sweep.sh: the per-board design
    OPTS/L2, single-sourced from the end-station config. The inline case
    tables in sweep.sh are the FALLBACK only; the builder test gate asserts
    fragment == fallback byte-for-byte on the OPTS/L2 values."""
    opts = " ".join(emit_board_opts(cfg))
    return (
        "# GENERATED by sw/builder/endstation_builder.py - DO NOT EDIT.\n"
        f"# Board-level design OPTS/L2 for {cfg['board_target']} (from the\n"
        "# board.constraints of any configs/endstation_*.yaml of this board;\n"
        "# header kept config-agnostic so identical constraints emit\n"
        "# identical bytes). Sourced by sw/litex/sweep.sh when present; its\n"
        "# inline tables are the fallback. Regenerate:\n"
        "#   python3 sw/builder/endstation_builder.py <cfg.yaml>\n"
        f'OPTS="{opts}"\n'
        f"L2={cfg['constraints']['l2_bytes']}\n")


# ----------------------------------------------------------- aem_overlay ----
def emit_aem_overlay(cfg):
    """AEM model overlay: descriptor counts + per-descriptor content that the
    config controls, consumed by avdecc/gen_aem_store.py --overlay. Layout:
    ONE STREAM_PORT per stream (cluster_layout above); every port owns its
    cluster block + one AUDIO_MAP with port-relative cluster offsets
    (1722.1-2021 7.2.19). All input clusters precede all output clusters;
    physical interface channels bind in order to the first clusters of each
    direction (wire-truth rule)."""
    L, T, clk = cfg["listeners"], cfg["talkers"], cfg["clocking"]
    P_in, P_out = cfg["ports_in"], cfg["ports_out"]
    n_crf = 1 if clk["crf_sink"] else 0
    in_clusters = sum(p["clusters"] for p in P_in)
    out_clusters = sum(p["clusters"] for p in P_out)

    stream_inputs = [dict(index=i, name=s["name"], kind="aaf",
                          channels=s["channels"], formats=s["formats"],
                          buffer_length_ns=s["buffer_length_ns"])
                     for i, s in enumerate(L)]
    if n_crf:
        stream_inputs.append(dict(index=len(L), name="CRF", kind="crf",
                                  channels=0, formats=[clk["crf_format"]],
                                  buffer_length_ns=BUFLEN_DEFAULT_NS))

    # CLOCK_SOURCE set mirrors media_clock_sources (internal first, then one
    # per AAF listener stream, then CRF - gen_aem_store order)
    clock_sources = []
    if "internal" in clk["media_clock_sources"]:
        clock_sources.append(dict(index=len(clock_sources), name="Internal",
                                  type="internal",
                                  location_type="CLOCK_SOURCE",
                                  location_index=len(clock_sources)))
    if "input_stream" in clk["media_clock_sources"]:
        for i in range(len(L)):
            nm = "Stream Clock" if len(L) == 1 else f"Stream Clock {i}"
            clock_sources.append(dict(index=len(clock_sources), name=nm,
                                      type="input_stream",
                                      location_type="STREAM_INPUT",
                                      location_index=i))
    if n_crf:
        clock_sources.append(dict(index=len(clock_sources), name="CRF Clock",
                                  type="crf",
                                  location_type="STREAM_INPUT",
                                  location_index=len(L)))

    # one AUDIO_MAP per port; rows = (stream_index, stream_channel,
    # cluster_offset RELATIVE to the port's base_cluster, cluster_channel)
    audio_maps = []
    for p in P_in:
        audio_maps.append(dict(
            index=p["base_map"], direction="input", port_index=p["index"],
            mappings=[[p["stream_index"], ch, ch, 0]
                      for ch in range(p["clusters"])]))
    for p in P_out:
        audio_maps.append(dict(
            index=p["base_map"], direction="output", port_index=p["index"],
            mappings=[[p["stream_index"], ch, ch, 0]
                      for ch in range(p["clusters"])]))
    audio_maps.sort(key=lambda m: m["index"])

    return {
        "_schema": OVERLAY_SCHEMA_ID,
        "_schema_version": OVERLAY_SCHEMA_VERSION,
        "_generated_by": "sw/builder/endstation_builder.py",
        "_source_config": cfg["source"],
        "entity": cfg["entity"],
        "model_id": cfg["model_id"],
        "sampling_rates_hz": clk["audio_unit_rates_hz"],
        "current_sampling_rate_hz": clk["sampling_rate_hz"],
        "entity_counts": {
            "talker_stream_sources": len(T),
            "listener_stream_sinks": len(L) + n_crf,
        },
        "descriptor_counts": {
            "ENTITY": 1, "CONFIGURATION": 1, "AUDIO_UNIT": 1,
            "STREAM_INPUT": len(L) + n_crf,
            "STREAM_OUTPUT": len(T),
            "AVB_INTERFACE": 1,
            "CLOCK_SOURCE": len(clock_sources),
            "CLOCK_DOMAIN": 1, "CONTROL": 1, "LOCALE": 1, "STRINGS": 1,
            "STREAM_PORT_INPUT": len(P_in),
            "STREAM_PORT_OUTPUT": len(P_out),
            "AUDIO_CLUSTER": in_clusters + out_clusters,
            "AUDIO_MAP": len(P_in) + len(P_out),
        },
        "stream_inputs": stream_inputs,
        "stream_outputs": [dict(index=i, name=s["name"], kind="aaf",
                                channels=s["channels"], formats=s["formats"])
                           for i, s in enumerate(T)],
        "clock_sources": clock_sources,
        "stream_ports": {"input": P_in, "output": P_out},
        "audio_maps": audio_maps,
        "cluster_format": "MBLA-mono",
        "cluster_policy": cfg["interface"]["cluster_policy"],
        "physical_binding": {
            "interface": cfg["interface"]["kind"],
            "channels_per_direction": cfg["interface"]["channels"],
            "rule": "first-N-clusters-per-direction; extra stream channels "
                    "virtual, missing physical channels render 0 "
                    "(USER wire-truth 1-to-1 rule)",
        },
    }


# ------------------------------------------------------------- build plan ---
def emit_build_plan(cfg, argv, overlay, marks):
    c, e, i = cfg["constraints"], cfg["entity"], cfg["interface"]
    ln = []
    a = ln.append
    a(f"# Build plan - {cfg['name']}")
    a("")
    a(f"Source config: `{cfg['source']}` "
      f"(schema {SCHEMA_ID} v{SCHEMA_MAJOR}.x)")
    a("Generated by sw/builder/endstation_builder.py - do not edit.")
    a("")
    a("## Entity")
    a("")
    a(f"- name: {e['name']}  (serial {e['serial_number']}, "
      f"fw {e['firmware_version']})")
    a(f"- entity_id: {e['entity_id']}, entity_model_id: {e['entity_model_id']} "
      f"({cfg['model_id']['source']}; shape hash {cfg['model_id']['hash']})")
    a("")
    a("## Board")
    a("")
    a(f"- target: {cfg['board_target']} ({c['phy']}), sys {_freq(c['sys_clk_hz'])} Hz"
      f" / milan {_freq(c['milan_clk_hz'])} Hz, L2 {c['l2_bytes']} B,"
      f" flashboot {c['flashboot']}"
      + (f", eth port {c['eth_port']}" if c["eth_port"] else ""))
    a("")
    a("## Clocking")
    a("")
    clk = cfg["clocking"]
    a(f"- media clock {clk['sampling_rate_hz']} Hz, sources "
      f"{clk['media_clock_sources']} (default {clk['default_source']}), "
      f"CRF sink {'on' if clk['crf_sink'] else 'off'}, audio PLL "
      f"{_freq(clk['audio_pll_hz'])} Hz")
    a("")
    a("## Audio interface")
    a("")
    a(f"- {i['kind']}: {i['channels']} ch/direction, {i['word_length_bits']}-bit"
      f" words, cluster policy {i['cluster_policy']}")
    a("")
    a("## Streams")
    a("")
    a("| Dir | Index | Name | Channels | Clusters (cfg) | Formats |")
    a("|-----|-------|------|----------|----------------|---------|")
    for k, s in enumerate(cfg["listeners"]):
        a(f"| listener | {k} | {s['name']} | {s['channels']} | {s['clusters']} "
          f"| {', '.join(s['formats'])} |")
    if clk["crf_sink"]:
        a(f"| listener | {len(cfg['listeners'])} | CRF | - | - "
          f"| {clk['crf_format']} |")
    for k, s in enumerate(cfg["talkers"]):
        a(f"| talker | {k} | {s['name']} | {s['channels']} | {s['clusters']} "
          f"| {', '.join(s['formats'])} |")
    a("")
    a("## Stream ports (one per stream)")
    a("")
    a("| Port | Stream | Clusters | base_cluster | AUDIO_MAP index |")
    a("|------|--------|----------|--------------|-----------------|")
    for p in cfg["ports_in"]:
        a(f"| STREAM_PORT_INPUT {p['index']} | STREAM_INPUT {p['stream_index']}"
          f" | {p['clusters']} | {p['base_cluster']} | {p['base_map']} |")
    for p in cfg["ports_out"]:
        a(f"| STREAM_PORT_OUTPUT {p['index']} | STREAM_OUTPUT {p['stream_index']}"
          f" | {p['clusters']} | {p['base_cluster']} | {p['base_map']} |")
    a("")
    a("## AEM descriptor counts")
    a("")
    a("| Descriptor | Count |")
    a("|------------|-------|")
    for t, n in overlay["descriptor_counts"].items():
        a(f"| {t} | {n} |")
    a("")
    a("## milan_soc.py parameter set")
    a("")
    a("```")
    a("python3 sw/litex/milan_soc.py " + " ".join(argv))
    a("```")
    a("")
    a("(design flags only - --build / --vivado-max-threads / --place-directive "
      "stay in sw/litex/sweep.sh; sweep.sh sources the generated "
      f"configs/generated/sweep_opts_{cfg['board_target']}.sh for OPTS/L2)")
    a("")
    a("## RTL capability")
    a("")
    a("| Element | Status | Note |")
    a("|---------|--------|------|")
    for el, status, note in marks:
        a(f"| {el} | {status} | {note} |")
    planned = [m for m in marks if m[1].startswith("planned")]
    a("")
    if planned:
        a(f"**{len(planned)} element(s) beyond current RTL - the config "
          "VALIDATES and the AEM overlay is complete, but gateware for the "
          "marked rows lands with the referenced roadmap items.**")
    else:
        a("**All elements buildable with today's RTL.**")
    a("")
    return "\n".join(ln)


# ------------------------------------------------------------------ driver --
def build(config_path, outdir=None):
    """Run the full pipeline for one config. Returns dict with the emitted
    paths + in-memory artifacts (for tests)."""
    cfg = load_config(config_path)
    argv = emit_soc_argv(cfg)
    overlay = emit_aem_overlay(cfg)
    marks = rtl_capability_marks(cfg)
    plan = emit_build_plan(cfg, argv, overlay, marks)
    sweep = emit_sweep_opts(cfg)

    outdir = outdir or os.path.join(HERE, "out")
    d = os.path.join(outdir, cfg["name"])
    os.makedirs(d, exist_ok=True)
    p_soc = os.path.join(d, "soc_params.json")
    with open(p_soc, "w") as f:
        json.dump({"milan_soc": "sw/litex/milan_soc.py", "argv": argv,
                   "_source_config": cfg["source"]}, f, indent=1)
        f.write("\n")
    p_ovl = os.path.join(d, "aem_overlay.json")
    with open(p_ovl, "w") as f:
        json.dump(overlay, f, indent=1)
        f.write("\n")
    p_plan = os.path.join(d, "build_plan.md")
    with open(p_plan, "w") as f:
        f.write(plan)
        f.write("\n")
    # board-level sweep fragment: canonical location, shared by every config
    # of the board (content depends only on board constraints)
    gen_dir = os.path.join(ROOT, "configs/generated")
    os.makedirs(gen_dir, exist_ok=True)
    p_sweep = os.path.join(gen_dir, f"sweep_opts_{cfg['board_target']}.sh")
    with open(p_sweep, "w") as f:
        f.write(sweep)
    return dict(cfg=cfg, argv=argv, overlay=overlay, marks=marks, plan=plan,
                sweep_opts=sweep,
                paths=dict(soc_params=p_soc, aem_overlay=p_ovl,
                           build_plan=p_plan, sweep_opts=p_sweep))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("config", help="end-station YAML config")
    ap.add_argument("-o", "--outdir", default=None,
                    help="output root (default sw/builder/out/)")
    args = ap.parse_args()
    try:
        r = build(args.config, args.outdir)
    except ConfigError as e:
        sys.exit(f"CONFIG ERROR: {e}")
    n_planned = sum(1 for m in r["marks"] if m[1].startswith("planned"))
    print(f"[endstation_builder] {r['cfg']['name']}: "
          f"{len(r['cfg']['listeners'])}x{len(r['cfg']['talkers'])} AAF + "
          f"{'CRF' if r['cfg']['clocking']['crf_sink'] else 'no CRF'}, "
          f"{r['cfg']['interface']['kind']}, "
          f"{r['overlay']['descriptor_counts']['AUDIO_CLUSTER']} clusters "
          f"({r['cfg']['interface']['cluster_policy']}), "
          f"model_id {r['cfg']['entity']['entity_model_id']} "
          f"({r['cfg']['model_id']['source']}); "
          f"{n_planned} planned element(s)")
    for p in r["paths"].values():
        print(f"  wrote {os.path.relpath(p, ROOT)}")


if __name__ == "__main__":
    main()
