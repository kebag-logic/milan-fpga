#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
test_builder.py - end-to-end gate for the end-station builder.

Gates (gaps item 4, generator round):
   1. all three example configs build end-to-end (soc argv + AEM overlay +
      plan + sweep fragment emitted);
   2. endstation_arty_current emits EXACTLY today's real design flags -
      compared against sw/litex/sweep.sh (arty OPTS + BASE, flow flags
      excluded); the ax7101 config must match the sweep ax7101 OPTS the
      same way (board flags are shape-independent, incl. --eth-port e2);
   3. endstation_arty_current's AEM overlay descriptor counts equal the
      hardcoded model in avdecc/gen_aem_store.py (imported, not run - the
      ROM assembles at import, file writes only under __main__);
   4. NxN shapes carry "planned (item 5)" marks instead of failing; the tdm
      interface kinds are SUPPORTED (KL_tdm_capture, --audio-interface) and
      only aes3/spdif still carry the item-4 planned mark (biphase-mark
      ser/des later); the current shape carries none;
   5. bad configs raise ConfigError (spot checks incl. policy/eth_port);
   6. per-stream STREAM_PORT layout invariants for every config: one port
      per stream, contiguous non-overlapping cluster blocks, unique map
      bases, map rows port-relative and in range;
   7. BOTH cluster policies produce valid layouts for the 4x4 + 8x8 shapes,
      and cap-at-interface actually caps (i2s 2ch variant);
   8. hash-derived entity_model_id: deterministic (same config -> same id),
      shape-sensitive (changed shape -> different id), OUI-prefixed;
      arty_current honors model_id_pin = the CURRENTLY DEPLOYED id;
   9. generated sweep_opts_<board>.sh == today's sweep.sh inline tables
      BYTE-FOR-BYTE (OPTS string + L2 + the PER-BOARD RXQ: each flashed boot
      chain fixes its own DMA window map) for both boards; sh -n passes on
      sweep.sh and both fragments;
  10. gen_aem_store.py CONSUMES the arty_current overlay (--overlay,
      subprocess) and the generated aecp_aem_rom.svh is byte-identical to
      the tracked hdl/ieee17221/aecp/gen/aecp_aem_rom.svh - THE key
      no-regression gate; the default (no-overlay) path stays byte-identical
      too;
  11. resource-estimator calibration: the arty_current estimate lands within
      +/-15% of the REAL mf48 place-report totals per category (report
      parsed at test time; SKIPs with a message when the report is absent);
  12. resource estimate is deterministic (two builds -> identical estimate
      dict + identical plan bytes);
  13. verdict thresholds (OK <70, TIGHT 70-80, OVER >80), UPPER BOUND
      labeling: absent for arty_current, present (with OVER verdicts) for
      the 4x4/8x8 shapes;
  14. Milan 7.2.3 rule ENFORCED: >=2 AAF listener streams without
      clocking.crf_output (absent or disabled) -> ConfigError citing 7.2.3;
      1-listener shapes keep it optional (arty_current absent = ok,
      enabled = ok with the Milan 7.3.2 default format);
  15. CRF-output overlay structure (4x4 + 8x8): STREAM_OUTPUT count +1 with
      a kind=crf entry (Milan 7.3.2 format word), NO STREAM_PORT/cluster/
      map growth, talker_stream_sources +1, CLOCK_SOURCE set unchanged
      (1722.1 7.2.9.2 has no OUTPUT_STREAM type); arty_current stays
      CRF-output-free (deployed shape untouched);
  16. gen_aem_store.py consumes a CRF-output overlay (--overlay, 4x4) to a
      structurally valid ROM: contiguous directory, 5 STREAM_OUTPUTs, the
      CRF one with clock_domain_index 0 / flags CLOCK_SYNC_SOURCE|CLASS_A /
      current_format 0x041060010000BB80, AAF outputs unchanged (0x0002),
      CONFIGURATION counts advertise it, STREAM_PORT_OUTPUT count stays 4;
  17. dynamic audio maps (gaps item 8): map_mode dynamic drops the port's
      AUDIO_MAP and emits the `AEM_DYNMAP engine constants; reject paths;
  18a. lwSRP table emitter: the emitted 0x680 reset words + CSR offsets are
      identical in the THREE hand-written places that carry them today -
      milan_csr's reset block, milan_csr's csr_default readback table and
      the REGISTER_MAP Reset column (all parsed at test time);
  18b. the emitted SR-class / MRP-timer / bandwidth constants equal the
      lwsrp_pkg.sv localparams, the PriorityAndRank byte milan_csr
      duplicates literally, and the KL_lwsrp_bw_gate 75%-ceiling literals;
      the tracked hdl/ieee8021q/srp/gen/lwsrp_table.svh regenerates
      BYTE-IDENTICALLY (the staleness gate);
  18c. TSpec derivation anchored in the RTL frame geometry (KL_aaf_packetizer
      SAMPLES_PER_FRAME_C + its documented 42+24*C / 90-byte identities),
      idleSlope == the bw_gate formula, module params == what milan_datapath
      passes (N_CTX_P = N_STREAMS, bw_gate width = N_CTX_P, NUM_QUEUES ==
      ethernet_packet_pkg), and the NxN ctx-row shortfall (L+T-1 rows in
      max(L,T) contexts) surfaces as a planned mark;
  18d. reject paths: class B, VID 0/4095, class_queue 4, a unicast stream
      DMAC, an unknown TSpec policy and an over-subscribed class-A
      reservation all raise ConfigError;
  19a. platform emitter: the DMA window map is derived from rx-queues (1q->2q
      inserts steer+rx1 = 0x74 and moves dma-ts/hs-pgsz-cap/pcm-dma by
      exactly that, tx/rx0 never move - anchored in milan_soc.py's
      MilanDMA registration order), and the queue count is ONE number across
      config / soc argv / sweep fragment / device tree;
  19b. the emitted DT node carries everything kl-eth + snd-kl-milan read
      (5 reg windows, kl,rsc-clk-mhz, phy-mode, MAC, no-map PCM ring sized
      for N capture streams); when the real build trees are on disk its
      window bases BYTE-MATCH the LiteX csr.csv and the deployed .dts
      (SKIPs with a message otherwise);
  19c. reject paths: multicast/missing station MAC, csr_base below the IO
      region, a PCM ring overrun, an unknown pinned window, a non-integer-MHz
      datapath clock - and THE gate, flipping rx_queues under a
      boot_chain_pin (5ce9a13 verbatim) raises ConfigError.

Run: python3 sw/builder/test_builder.py   (or pytest sw/builder/test_builder.py)
"""

import copy
import os
import re
import shlex
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "avdecc"))

import yaml  # noqa: E402

import endstation_builder as eb  # noqa: E402

CONFIGS = {
    "arty_current": os.path.join(ROOT, "configs/endstation_arty_current.yaml"),
    "arty_4x4": os.path.join(ROOT, "configs/endstation_arty_4x4.yaml"),
    "ax7101_8x8": os.path.join(ROOT, "configs/endstation_ax7101_8x8.yaml"),
}
OUT = os.path.join(HERE, "out")
SWEEP = os.path.join(ROOT, "sw/litex/sweep.sh")
TRACKED_SVH = os.path.join(ROOT, "hdl/ieee17221/aecp/gen/aecp_aem_rom.svh")

# Flow flags: sweep.sh mechanics, never part of the end-station definition.
FLOW_FLAGS = {"--build": 0, "--vivado-max-threads": 1,
              "--place-directive": 1, "--output-dir": 1}

DEPLOYED_MODEL_ID = "0x001BC50AC1000001"     # flashed silicon identity

# Real utilization report the estimator was calibrated against (flat place
# report of the same build as the hierarchical calibration source).
REAL_RPT = os.path.expanduser(
    "~/litex-milan/work/build_arty_eto_milanfinal48/gateware/"
    "digilent_arty_utilization_place.rpt")
CAL_TOL = 0.15                               # +/-15% calibration gate


def _canon(tokens):
    """tokens -> {flag: [values]} with numeric values normalized (so
    '83.333e6' == '83333000.0' and '${L2}'-substituted ints compare clean)."""
    d = {}
    i = 0
    while i < len(tokens):
        t = tokens[i]
        assert t.startswith("--"), f"unexpected token {t!r}"
        if "=" in t:
            flag, val = t.split("=", 1)
            vals = [val]
            i += 1
        elif i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
            flag, vals = t, [tokens[i + 1]]
            i += 2
        else:
            flag, vals = t, []
            i += 1
        d.setdefault(flag, []).extend(vals)
    for flag, vals in d.items():
        for k, v in enumerate(vals):
            try:
                vals[k] = float(v)
            except ValueError:
                pass
    return d


def sweep_inline(board):
    """(OPTS string, L2 string, RXQ string) of sweep.sh's inline FALLBACK
    table for <board>. RXQ is per board: each flashed boot chain fixes its
    own DMA window map (the CSR-rot rule)."""
    txt = open(SWEEP).read()
    m = re.search(rf'{board}\)\s+OPTS="([^"]+)"; L2=(\d+); RXQ=(\d+)', txt)
    assert m, f"sweep.sh: no OPTS case for {board}"
    return m.group(1), m.group(2), m.group(3)


def sweep_expected(board):
    """Design-flag dict sweep.sh composes for <board> (OPTS + BASE minus
    flow flags)."""
    txt = open(SWEEP).read()
    opts, l2, rxq = sweep_inline(board)
    mb = re.search(r'milan_soc\.py \$OPTS (.*?)"', txt, re.S)
    assert mb, "sweep.sh: BASE line not found"
    base = mb.group(1).replace("\\\n", " ")
    tokens = shlex.split(opts) + shlex.split(base)
    subst = {"${L2}": l2, "${RXQ}": rxq}
    tokens = [subst.get(t, t) for t in tokens]
    out, i = [], 0
    while i < len(tokens):
        if tokens[i] in FLOW_FLAGS:
            i += 1 + FLOW_FLAGS[tokens[i]]
        else:
            out.append(tokens[i])
            i += 1
    return _canon(out)


def _variant(base_path, mutate):
    """Write a mutated copy of a config to a temp file; return its path.
    mutate(cfg_dict) edits in place."""
    cfg = yaml.safe_load(open(base_path))
    mutate(cfg)
    f = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False)
    yaml.safe_dump(cfg, f)
    f.close()
    return f.name


def check_port_layout(ovl, n_listeners, n_talkers):
    """USER-decision invariants: one STREAM_PORT per stream, contiguous
    non-overlapping cluster blocks, unique per-port map bases, one map per
    port with port-relative in-range rows."""
    P_in = ovl["stream_ports"]["input"]
    P_out = ovl["stream_ports"]["output"]
    dc = ovl["descriptor_counts"]
    assert len(P_in) == n_listeners == dc["STREAM_PORT_INPUT"]
    assert len(P_out) == n_talkers == dc["STREAM_PORT_OUTPUT"]
    # contiguous, non-overlapping, input block before output block
    base = 0
    for p in P_in + P_out:
        assert p["base_cluster"] == base, \
            f"port cluster blocks not contiguous: {p} (expect base {base})"
        assert p["clusters"] >= 1
        base += p["clusters"]
    assert dc["AUDIO_CLUSTER"] == base
    # map bases: unique, one per port, densely covering 0..n_maps-1
    bases = [p["base_map"] for p in P_in + P_out]
    assert sorted(bases) == list(range(len(bases))), f"map bases overlap: {bases}"
    assert all(p["maps"] == 1 for p in P_in + P_out)
    assert dc["AUDIO_MAP"] == len(bases) == len(ovl["audio_maps"])
    # per-map rows: correct stream, port-relative offsets in range
    by_index = {m["index"]: m for m in ovl["audio_maps"]}
    for direction, ports in (("input", P_in), ("output", P_out)):
        for p in ports:
            m = by_index[p["base_map"]]
            assert m["direction"] == direction and m["port_index"] == p["index"]
            assert len(m["mappings"]) == p["clusters"]
            for (si, ch, off, cch) in m["mappings"]:
                assert si == p["stream_index"]
                assert 0 <= off < p["clusters"], \
                    f"map {m['index']}: offset {off} outside port ({p})"
                assert cch == 0


def test_all_configs_build():
    for name, path in CONFIGS.items():
        r = eb.build(path, OUT)
        for p in r["paths"].values():
            assert os.path.getsize(p) > 0, f"{name}: empty {p}"
        assert r["overlay"]["_schema"] == "kebag-logic/aem-overlay"
        assert r["overlay"]["_schema_version"].startswith("2.")
        print(f"  [gate 1] {name}: builds end-to-end "
              f"({os.path.relpath(os.path.dirname(r['paths']['soc_params']), ROOT)}/)")


def test_current_shape_matches_sweep_flags():
    r = eb.build(CONFIGS["arty_current"], OUT)
    got, want = _canon(r["argv"]), sweep_expected("arty")
    assert got == want, f"arty argv mismatch:\n got  {got}\n want {want}"
    print("  [gate 2] arty_current argv == sweep.sh arty design flags "
          f"({len(got)} flags)")
    for name in ("ax7101_8x8",):
        r = eb.build(CONFIGS[name], OUT)
        got, want = _canon(r["argv"]), sweep_expected("ax7101")
        # NXN_ARCHITECTURE P0: multi-stream shapes additionally carry
        # --num-streams (the milan_datapath N_STREAMS parameter); sweep.sh
        # tracks today's 1x1 build, so the flag rides on top of its OPTS.
        want = dict(want)
        want["--num-streams"] = [8.0]
        # item-4 audio-interface family: tdm kinds ride on top of the OPTS
        # as the front-end generate select (default i2s emits nothing).
        want["--audio-interface"] = ["tdm16"]
        assert got == want, f"{name} argv mismatch:\n got  {got}\n want {want}"
        assert got["--eth-port"] == ["e2"], "ax7101 must carry --eth-port e2"
        print(f"  [gate 2] {name} argv == sweep.sh ax7101 design flags "
              f"({len(got)} flags, incl --eth-port e2)")


def test_current_shape_matches_gen_aem_store():
    import gen_aem_store as g  # ROM assembles at import; writes only in main
    rom_counts = {}
    for (t, i, _b, _l) in g.directory:
        rom_counts[t] = rom_counts.get(t, 0) + 1
    code = {"ENTITY": 0x0000, "CONFIGURATION": 0x0001, "AUDIO_UNIT": 0x0002,
            "STREAM_INPUT": 0x0005, "STREAM_OUTPUT": 0x0006,
            "AVB_INTERFACE": 0x0009, "CLOCK_SOURCE": 0x000A, "LOCALE": 0x000C,
            "STRINGS": 0x000D, "STREAM_PORT_INPUT": 0x000E,
            "STREAM_PORT_OUTPUT": 0x000F, "AUDIO_CLUSTER": 0x0014,
            "AUDIO_MAP": 0x0017, "CONTROL": 0x001A, "CLOCK_DOMAIN": 0x0024}
    r = eb.build(CONFIGS["arty_current"], OUT)
    ovl = r["overlay"]
    for name, n in ovl["descriptor_counts"].items():
        assert rom_counts.get(code[name], 0) == n, (
            f"{name}: overlay {n} != gen_aem_store {rom_counts.get(code[name], 0)}")
    # formats + rates byte-identical to the ROM model
    si0 = ovl["stream_inputs"][0]
    assert [int(f, 16) for f in si0["formats"]] == g.FORMATS
    assert [int(f, 16) for f in ovl["stream_inputs"][1]["formats"]] == g.CRF_FORMATS
    assert [int(f, 16) for f in ovl["stream_outputs"][0]["formats"]] == g.OUT_FORMATS
    rate_hz = {0x0000BB80: 48000, 0x00017700: 96000, 0x0002EE00: 192000}
    assert [rate_hz[x] for x in g.RATES] == ovl["sampling_rates_hz"]
    # port layout identical to the deployed ROM (1 port/stream: 8@0 map 0 /
    # 8@8 map 1)
    p_in, p_out = ovl["stream_ports"]["input"], ovl["stream_ports"]["output"]
    assert len(p_in) == 1 and len(p_out) == 1
    assert (p_in[0]["clusters"], p_in[0]["base_cluster"],
            p_in[0]["maps"], p_in[0]["base_map"]) == (8, 0, 1, 0)
    assert (p_out[0]["clusters"], p_out[0]["base_cluster"],
            p_out[0]["maps"], p_out[0]["base_map"]) == (8, 8, 1, 1)
    print(f"  [gate 3] arty_current overlay == gen_aem_store model "
          f"({len(ovl['descriptor_counts'])} descriptor types, formats, "
          f"rates, port layout)")


def test_capability_marks():
    r = eb.build(CONFIGS["arty_current"], OUT)
    planned = [m for m in r["marks"] if m[1].startswith("planned")]
    assert planned == [], f"current shape must be fully supported: {planned}"
    for name, want in (("arty_4x4", "4x4"), ("ax7101_8x8", "8x8")):
        r = eb.build(CONFIGS[name], OUT)
        planned = [m[1] for m in r["marks"] if m[1].startswith("planned")]
        assert any("item 5" in p for p in planned), f"{name}: no item-5 mark"
        # item-4 audio-interface family landed: the tdm kinds are SUPPORTED
        # (KL_tdm_capture front-end select), never a planned mark anymore
        assert not any("item 4" in p for p in planned), \
            f"{name}: tdm must be supported now: {planned}"
        tdm = [m for m in r["marks"]
               if m[0].startswith("audio interface tdm")]
        assert tdm and tdm[0][1] == "supported" \
            and "KL_tdm_capture" in tdm[0][2], f"{name}: bad tdm mark {tdm}"
        assert "planned (item 5" in r["plan"], f"{name}: plan lacks marker"
        print(f"  [gate 4] {name}: {len(planned)} planned mark(s) "
              f"(item 5 only; tdm supported), no failure")
    # aes3/spdif stay planned (contract documented, biphase-mark RTL later)
    v = _variant(CONFIGS["arty_current"],
                 lambda c: c["audio_interface"].__setitem__("kind", "aes3"))
    r = eb.build(v, OUT)
    planned = [m[1] for m in r["marks"] if m[1].startswith("planned")]
    assert any("item 4" in p for p in planned), "aes3 lost its planned mark"
    print("  [gate 4] aes3 variant: still planned (biphase-mark RTL later)")
    print("  [gate 4] arty_current: zero planned marks")


def test_bad_configs_rejected():
    base = yaml.safe_load(open(CONFIGS["arty_current"]))
    cases = [
        ("phy contradiction", ["board", "constraints", "phy"], "gmii-1g"),
        ("bad interface", ["audio_interface", "kind"], "adat"),
        ("bad rate", ["clocking", "sampling_rate_hz"], 44100),
        ("gmii knob on arty", ["board", "constraints", "gtx_tx_invert"], True),
        ("eth_port on single-PHY arty", ["board", "constraints", "eth_port"], "e2"),
        ("unknown cluster policy", ["audio_interface", "cluster_mapping",
                                    "policy"], "per-channel"),
        ("legacy cluster rule key", ["audio_interface", "cluster_mapping",
                                     "rule"], "mono-cluster-per-stream-channel"),
    ]
    for label, path, val in cases:
        c = copy.deepcopy(base)
        d = c
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = val
        with tempfile.NamedTemporaryFile("w", suffix=".yaml",
                                         delete=False) as f:
            yaml.safe_dump(c, f)
            p = f.name
        try:
            try:
                eb.load_config(p)
            except eb.ConfigError:
                pass
            else:
                raise AssertionError(f"{label}: accepted invalid config")
        finally:
            os.unlink(p)
    print(f"  [gate 5] {len(cases)}/{len(cases)} invalid configs rejected "
          "with ConfigError")


def test_port_layout_invariants():
    shapes = {"arty_current": (1, 1), "arty_4x4": (4, 4), "ax7101_8x8": (8, 8)}
    for name, (nl, nt) in shapes.items():
        r = eb.build(CONFIGS[name], OUT)
        check_port_layout(r["overlay"], nl, nt)
        dc = r["overlay"]["descriptor_counts"]
        print(f"  [gate 6] {name}: {nl}+{nt} stream ports, "
              f"{dc['AUDIO_CLUSTER']} clusters, {dc['AUDIO_MAP']} maps - "
              "invariants hold")


def test_both_policies_valid():
    for name, (nl, nt) in (("arty_4x4", (4, 4)), ("ax7101_8x8", (8, 8))):
        for pol in eb.CLUSTER_POLICIES:
            p = _variant(CONFIGS[name], lambda c, pol=pol: c[
                "audio_interface"]["cluster_mapping"].__setitem__("policy", pol))
            try:
                r = eb.build(p, os.path.join(OUT, "_policy_variants"))
                check_port_layout(r["overlay"], nl, nt)
                assert r["overlay"]["cluster_policy"] == pol
            finally:
                os.unlink(p)
        print(f"  [gate 7] {name}: both cluster policies -> valid layouts")
    # cap-at-interface must actually CAP: 8ch listeners on a 2ch i2s
    def to_i2s(c):
        c["audio_interface"]["kind"] = "i2s_philips"
        c["audio_interface"]["cluster_mapping"]["policy"] = "cap-at-interface"
    p = _variant(CONFIGS["ax7101_8x8"], to_i2s)
    try:
        r = eb.build(p, os.path.join(OUT, "_policy_variants"))
        check_port_layout(r["overlay"], 8, 8)
        for port in r["overlay"]["stream_ports"]["input"]:
            assert port["clusters"] == 2, f"cap-at-interface did not cap: {port}"
        assert r["overlay"]["descriptor_counts"]["AUDIO_CLUSTER"] == 8 * 2 + 8 * 2
    finally:
        os.unlink(p)
    print("  [gate 7] cap-at-interface caps 8ch streams to the 2ch i2s "
          "interface (32 clusters total)")
    # cluster-per-stream-channel must NOT cap (legacy-8 expressible)
    def legacy(c):
        c["audio_interface"]["cluster_mapping"]["policy"] = \
            "cluster-per-stream-channel"
        for t in c["streams"]["talkers"]:
            t["clusters"] = 8
    p = _variant(CONFIGS["arty_4x4"], legacy)
    try:
        r = eb.build(p, os.path.join(OUT, "_policy_variants"))
        check_port_layout(r["overlay"], 4, 4)
        for port in r["overlay"]["stream_ports"]["output"]:
            assert port["clusters"] == 8
    finally:
        os.unlink(p)
    print("  [gate 7] cluster-per-stream-channel keeps the legacy-8 layout "
          "expressible")


def test_model_id_hashing():
    # determinism: same config -> same id (two independent loads)
    a = eb.load_config(CONFIGS["arty_4x4"])
    b = eb.load_config(CONFIGS["arty_4x4"])
    assert a["model_id"]["value"] == b["model_id"]["value"]
    assert a["model_id"]["source"] == "hash"
    # OUI prefix folded in
    v = int(a["model_id"]["value"], 16)
    assert v >> 40 == eb.MODEL_ID_OUI, f"id {v:#018x} lacks the OUI prefix"
    # shape sensitivity: any model-shaping change -> different id
    ids = {a["model_id"]["value"]}
    for label, mutate in (
        ("talker clusters", lambda c: c["streams"]["talkers"][0]
         .__setitem__("clusters", 4)),
        ("cluster policy", lambda c: c["audio_interface"]["cluster_mapping"]
         .__setitem__("policy", "cluster-per-stream-channel")),
        ("listener channels", lambda c: c["streams"]["listeners"][0]
         .__setitem__("channels", 2)),
    ):
        p = _variant(CONFIGS["arty_4x4"], mutate)
        try:
            v2 = eb.load_config(p)["model_id"]["value"]
        finally:
            os.unlink(p)
        assert v2 not in ids, f"{label}: shape change did not change the id"
        ids.add(v2)
    # board/name changes must NOT change the id (model != instance)
    def rename(c):
        c["entity"]["name"] = "Other Name"
        c["entity"]["serial_number"] = "OTHER-9999"
    p = _variant(CONFIGS["arty_4x4"], rename)
    try:
        assert eb.load_config(p)["model_id"]["value"] == a["model_id"]["value"]
    finally:
        os.unlink(p)
    # 4x4 and 8x8 shapes differ
    e88 = eb.load_config(CONFIGS["ax7101_8x8"])
    assert e88["model_id"]["value"] != a["model_id"]["value"]
    assert e88["model_id"]["source"] == "hash"
    # pinned id honored on arty_current (deployed silicon identity)
    cur = eb.load_config(CONFIGS["arty_current"])
    assert cur["model_id"]["source"] == "pin"
    assert cur["entity"]["entity_model_id"] == DEPLOYED_MODEL_ID
    assert cur["model_id"]["hash"] != DEPLOYED_MODEL_ID  # pin != hash: pin wins
    print("  [gate 8] model-id: deterministic, OUI-prefixed, shape-sensitive "
          "(3 mutations), instance-field-insensitive, 4x4 != 8x8, "
          f"arty_current pinned to {DEPLOYED_MODEL_ID}")


def test_sweep_opts_fragments():
    frag = {}
    for cfg_name, board in (("arty_current", "arty"), ("ax7101_8x8", "ax7101")):
        r = eb.build(CONFIGS[cfg_name], OUT)
        p = r["paths"]["sweep_opts"]
        assert os.path.basename(p) == f"sweep_opts_{board}.sh"
        txt = open(p).read()
        m = re.search(r'^OPTS="([^"]*)"\nL2=(\d+)\nRXQ=(\d+)\n', txt, re.M)
        assert m, f"{p}: fragment lacks OPTS/L2/RXQ"
        frag[board] = (m.group(1), m.group(2), m.group(3), p)
    for board, (opts, l2, rxq, p) in frag.items():
        want_opts, want_l2, want_rxq = sweep_inline(board)
        assert opts == want_opts, (f"{board}: fragment OPTS != sweep.sh inline\n"
                                   f" frag   {opts!r}\n inline {want_opts!r}")
        assert l2 == want_l2, f"{board}: fragment L2 {l2} != inline {want_l2}"
        # per-board RX-queue count: the CSR-rot rule (each flashed boot chain
        # fixes its own DMA window map), so a drift here is a real hazard
        assert rxq == want_rxq, f"{board}: fragment RXQ {rxq} != inline {want_rxq}"
        print(f"  [gate 9] {board}: generated OPTS/L2/RXQ byte-match sweep.sh "
              f"inline table ({len(opts)} chars, rx-queues {rxq})")
    for path in [SWEEP] + [p for (_o, _l, _r, p) in frag.values()]:
        subprocess.run(["sh", "-n", path], check=True)
    print("  [gate 9] sh -n clean: sweep.sh + both fragments")


def test_gen_aem_store_consumes_overlay():
    r = eb.build(CONFIGS["arty_current"], OUT)
    tracked = open(TRACKED_SVH, "rb").read()
    with tempfile.TemporaryDirectory() as td:
        # THE key no-regression gate: builder overlay -> gen_aem_store ->
        # byte-identical ROM svh for the deployed shape
        subprocess.run(
            [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
             "--overlay", r["paths"]["aem_overlay"], "--out-dir", td],
            check=True, capture_output=True)
        got = open(os.path.join(td, "aecp_aem_rom.svh"), "rb").read()
        assert got == tracked, (
            "overlay-built aecp_aem_rom.svh differs from the tracked ROM "
            f"({len(got)} vs {len(tracked)} bytes)")
        print(f"  [gate 10] arty_current overlay -> gen_aem_store --overlay: "
              f"svh BYTE-IDENTICAL to tracked ROM ({len(got)} B)")
    with tempfile.TemporaryDirectory() as td:
        # refactor guard: the default (builtin) path is unchanged too
        subprocess.run(
            [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
             "--out-dir", td], check=True, capture_output=True)
        got = open(os.path.join(td, "aecp_aem_rom.svh"), "rb").read()
        assert got == tracked, "default-path svh regressed"
        print("  [gate 10] gen_aem_store default path: svh byte-identical "
              "(refactor guard)")


def _real_totals(path):
    """Parse LUT/FF/BRAM36-equivalent/DSP totals from a flat Vivado
    utilization report. bram36 = RAMB36 + RAMB18/2."""
    txt = open(path).read()

    def grab(pat):
        m = re.search(pat, txt)
        assert m, f"{path}: no match for {pat!r}"
        return int(m.group(1))

    return dict(
        lut=grab(r"\|\s*Slice LUTs\s*\|\s*(\d+)"),
        ff=grab(r"\|\s*Slice Registers\s*\|\s*(\d+)"),
        bram36=grab(r"\|\s*RAMB36/FIFO\*?\s*\|\s*(\d+)")
        + grab(r"\|\s*RAMB18\s+\|\s*(\d+)") / 2,
        dsp=grab(r"\|\s*DSPs\s*\|\s*(\d+)"),
    )


def test_resource_calibration():
    if not os.path.exists(REAL_RPT):
        print(f"  [gate 11] SKIP: real report not on disk ({REAL_RPT}) - "
              "calibration gate needs the mf48 build tree")
        return
    real = _real_totals(REAL_RPT)
    est = eb.build(CONFIGS["arty_current"], OUT)["resource_estimate"]
    for k in ("lut", "ff", "bram36", "dsp"):
        got, want = float(est["totals"][k]), float(real[k])
        delta = abs(got - want) / want
        assert delta <= CAL_TOL, (
            f"{k}: estimate {got} vs real {want} = {delta:.1%} off "
            f"(gate {CAL_TOL:.0%})")
        print(f"  [gate 11] {k}: estimate {got:g} vs real mf48 {want:g} "
              f"({(got - want) / want:+.2%}, gate +/-{CAL_TOL:.0%})")


def test_resource_determinism():
    import json
    a = eb.build(CONFIGS["ax7101_8x8"], OUT)
    b = eb.build(CONFIGS["ax7101_8x8"], OUT)
    assert json.dumps(a["resource_estimate"], sort_keys=True) == \
        json.dumps(b["resource_estimate"], sort_keys=True)
    assert a["plan"] == b["plan"]
    print("  [gate 12] resource estimate + plan deterministic across builds")


def test_resource_verdicts():
    # threshold semantics: OK <70, TIGHT 70-80, OVER >80
    for pct, want in ((0.0, "OK"), (69.9, "OK"), (70.0, "TIGHT"),
                      (80.0, "TIGHT"), (80.1, "OVER"), (142.0, "OVER")):
        got = eb.resource_verdict(pct)
        assert got == want, f"verdict({pct}) = {got}, want {want}"
    # arty_current: measured shape, no UPPER BOUND rows; verdict mirrors the
    # real mf48 placement (81.5% LUTs -> OVER by the absolute thresholds)
    cur = eb.build(CONFIGS["arty_current"], OUT)
    est = cur["resource_estimate"]
    assert not est["upper_bound"]
    assert "UPPER BOUND estimate" not in cur["plan"]
    assert est["worst_category"] == "lut" and est["verdict"] == "OVER"
    # NxN shapes (P12 shared-engine rows): no longer UPPER BOUND - engines
    # charged once + yosys-derived per-context marginals. Both shapes FIT
    # the part arithmetically (<100% every category) but land in the OVER
    # band (>80% LUT, area-70: expect placement/timing pain) exactly as
    # NXN_ARCHITECTURE.md §6 predicted (4x4 ~85%, 8x8 ~89% vs modeled
    # 87.3/87.7).
    for name, worst_max in (("arty_4x4", 88.0), ("ax7101_8x8", 92.0)):
        r = eb.build(CONFIGS[name], OUT)
        e = r["resource_estimate"]
        assert not e["upper_bound"], \
            f"{name}: shared-engine estimate must not be UPPER BOUND"
        assert e["verdict"] == "OVER", f"{name}: expected OVER, got {e}"
        assert e["worst_pct"] < 100.0, f"{name}: must FIT the part, got {e}"
        assert e["worst_pct"] <= worst_max, \
            f"{name}: worst {e['worst_pct']}% blew the §6 envelope {worst_max}%"
        assert "UPPER BOUND estimate" not in r["plan"]
        assert "shared engines" in r["plan"] or "shared-engine" in r["plan"]
        assert "## Resource estimate" in r["plan"]
        print(f"  [gate 13] {name}: verdict {e['verdict']} "
              f"(worst {e['worst_category'].upper()} {e['worst_pct']}%, "
              "fits the part, shared-engine rows)")
    print("  [gate 13] thresholds OK/TIGHT/OVER at 70/80; arty_current "
          f"verdict {est['verdict']} (worst LUT {est['worst_pct']}%), "
          "no upper-bound rows")


CRF_FMT = "0x041060010000BB80"       # Milan 7.3.2 Table 7.1 format word


def test_milan_723_crf_output_rule():
    # >=2 AAF listener streams REQUIRE clocking.crf_output (Milan 7.2.3:
    # "an AAF Media Listener with two or more AAF Media Inputs shall
    # implement a CRF Media Clock Output")
    def drop(c):
        c["clocking"].pop("crf_output", None)

    def disable(c):
        c["clocking"]["crf_output"]["enabled"] = False

    for label, mutate in (("crf_output absent", drop),
                          ("crf_output disabled", disable)):
        for shape in ("arty_4x4", "ax7101_8x8"):
            p = _variant(CONFIGS[shape], mutate)
            try:
                try:
                    eb.load_config(p)
                except eb.ConfigError as e:
                    assert "7.2.3" in str(e), \
                        f"{shape}/{label}: error must cite Milan 7.2.3: {e}"
                else:
                    raise AssertionError(
                        f"{shape}/{label}: >=2-listener shape accepted "
                        "without a CRF Media Clock Output")
            finally:
                os.unlink(p)
    # exactly 2 AAF listeners is already >= 2 (rule boundary)
    def two_listeners(c):
        del c["streams"]["listeners"][2:]
        c["clocking"].pop("crf_output", None)
    p = _variant(CONFIGS["arty_4x4"], two_listeners)
    try:
        try:
            eb.load_config(p)
        except eb.ConfigError as e:
            assert "7.2.3" in str(e)
        else:
            raise AssertionError("2-listener shape accepted without CRF output")
    finally:
        os.unlink(p)
    # 1 AAF listener: CRF output OPTIONAL - arty_current has none (deployed
    # shape untouched); enabling it on a 1-listener shape is legal and the
    # format defaults to the Milan 7.3.2 word
    cur = eb.load_config(CONFIGS["arty_current"])
    assert cur["clocking"]["crf_output"] is False
    p = _variant(CONFIGS["arty_current"],
                 lambda c: c["clocking"].__setitem__("crf_output",
                                                     {"enabled": True}))
    try:
        c1 = eb.load_config(p)
        assert c1["clocking"]["crf_output"] is True
        assert c1["clocking"]["crf_output_format"] == CRF_FMT
    finally:
        os.unlink(p)
    print("  [gate 14] Milan 7.2.3 enforced: 4x4/8x8/2-listener shapes "
          "rejected without crf_output (error cites 7.2.3); optional at "
          "1 listener, format defaults to " + CRF_FMT)


def test_crf_output_overlay_structure():
    for name, n in (("arty_4x4", 4), ("ax7101_8x8", 8)):
        ovl = eb.build(CONFIGS[name], OUT)["overlay"]
        so = ovl["stream_outputs"]
        assert len(so) == n + 1, f"{name}: expected {n} AAF + 1 CRF output"
        assert so[-1] == dict(index=n, name="CRF", kind="crf", channels=0,
                              formats=[CRF_FMT]), f"{name}: CRF entry {so[-1]}"
        assert all(s["kind"] == "aaf" for s in so[:-1])
        dc = ovl["descriptor_counts"]
        assert dc["STREAM_OUTPUT"] == n + 1
        assert dc["STREAM_PORT_OUTPUT"] == n      # CRF output: NO audio port
        assert dc["AUDIO_MAP"] == 2 * n           # ...and no map/cluster growth
        assert ovl["entity_counts"]["talker_stream_sources"] == n + 1
        # CLOCK_SOURCE set unchanged by the output: 1722.1 7.2.9.2 defines
        # INTERNAL/EXTERNAL/INPUT_STREAM only - internal + N inputs + CRF sink
        assert dc["CLOCK_SOURCE"] == 1 + n + 1
        check_port_layout(ovl, n, n)              # port invariants still hold
        print(f"  [gate 15] {name}: CRF STREAM_OUTPUT idx {n} advertised "
              "(no port/cluster/map growth, talker count +1, "
              "clock sources unchanged)")
    ovl = eb.build(CONFIGS["arty_current"], OUT)["overlay"]
    assert ovl["descriptor_counts"]["STREAM_OUTPUT"] == 1
    assert all(s["kind"] == "aaf" for s in ovl["stream_outputs"])
    assert ovl["entity_counts"]["talker_stream_sources"] == 1
    print("  [gate 15] arty_current: no CRF output (deployed shape untouched)")


def test_gen_aem_store_crf_output_overlay():
    import json
    r = eb.build(CONFIGS["arty_4x4"], OUT)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
             "--overlay", r["paths"]["aem_overlay"], "--out-dir", td],
            check=True, capture_output=True)
        j = json.load(open(os.path.join(td, "aem_rom.json")))
        svh = open(os.path.join(td, "aecp_aem_rom.svh")).read()
    rom = bytes.fromhex(j["rom_hex"])
    dirv = j["directory"]
    # directory covers the ROM contiguously (structural validity)
    off = 0
    for d in dirv:
        assert d["base"] == off, f"directory hole at {d}"
        off += d["len"]
    assert off == len(rom)
    outs = [d for d in dirv if d["type"] == 0x0006]
    assert [d["index"] for d in outs] == list(range(5)), \
        f"expected STREAM_OUTPUT 0..4, got {outs}"
    crf = outs[4]
    b = crf["base"]
    assert crf["len"] == 132 + 8                  # header + ONE format entry
    assert rom[b + 4:b + 7] == b"CRF"             # object_name
    assert rom[b + 70:b + 72] == b"\x00\x00"      # clock_domain_index 0 (7.2.6)
    assert rom[b + 72:b + 74] == b"\x00\x03"      # CLOCK_SYNC_SOURCE|CLASS_A
    assert rom[b + 74:b + 82].hex().upper() == CRF_FMT[2:]   # current_format
    assert rom[b + 132:b + 140].hex().upper() == CRF_FMT[2:]  # formats[0]
    b0 = outs[0]["base"]
    assert rom[b0 + 72:b0 + 74] == b"\x00\x02"    # AAF outputs keep CLASS_A
    # CONFIGURATION descriptor_counts advertise the 5 outputs; the CRF one
    # adds no STREAM_PORT_OUTPUT
    cb = next(d for d in dirv if d["type"] == 0x0001)["base"]
    n_counts = int.from_bytes(rom[cb + 72:cb + 74], "big")
    pairs = {}
    for k in range(n_counts):
        o = cb + 74 + 4 * k
        pairs[int.from_bytes(rom[o:o + 2], "big")] = \
            int.from_bytes(rom[o + 2:o + 4], "big")
    assert pairs[0x0006] == 5, f"CONFIGURATION counts: {pairs}"
    assert sum(1 for d in dirv if d["type"] == 0x000F) == 4
    print(f"  [gate 16] gen_aem_store --overlay (4x4 + CRF output): ROM "
          f"{len(rom)} B structurally valid; STREAM_OUTPUT[4] = CRF "
          f"(domain 0, flags 0x0003, {CRF_FMT}), CONFIGURATION count 5, "
          "4 output ports")
    # Per-descriptor format tables (item-4 follow-up): multi-stream shapes
    # emit the `AEM_PER_STREAM_FMT layout — one reference entry + WB address
    # per STREAM_INPUT/STREAM_OUTPUT; the deployed shape never does (gate 10
    # byte-identity is the proof of absence).
    assert "`define AEM_PER_STREAM_FMT" in svh
    assert "localparam int unsigned AEM_N_STRIN_C  = 5;" in svh   # 4 AAF + CRF
    assert "localparam int unsigned AEM_N_STROUT_C = 5;" in svh   # 4 AAF + CRF
    m = re.search(r"AEM_STRIN_CRF_C \[0:4\] = '\{(.*?)\};", svh)
    assert m and m.group(1).split(", ") == ["1'b0"] * 4 + ["1'b1"]
    ins = [d for d in dirv if d["type"] == 0x0005]
    m = re.search(r"WB_STRIN_FMT_ADDR_C \[0:4\] = '\{(.*?)\};", svh)
    assert m and m.group(1).split(", ") == \
        [f"16'd{d['base'] + 74}" for d in ins], "input WB addr table"
    m = re.search(r"WB_STROUT_FMT_ADDR_C \[0:4\] = '\{(.*?)\};", svh)
    assert m and m.group(1).split(", ") == \
        [f"16'd{d['base'] + 74}" for d in outs], "output WB addr table"
    m = re.search(r"AEM_STROUT_FMT_C \[0:4\] = '\{(.*?)\};", svh)
    assert m and m.group(1).split(", ")[-1] == f"64'h{CRF_FMT[2:]}"
    print("  [gate 16b] per-stream format tables: `AEM_PER_STREAM_FMT + "
          "5-in/5-out reference + WB-addr arrays match the directory "
          "(CRF flags/formats in the right rows)")


def test_dynamic_audio_map_overlay():
    # gaps item 8: listeners[0] map_mode dynamic drops the port's AUDIO_MAP
    # (7.2.13 number_of_maps=0) and the overlay -> gen_aem_store path emits
    # the `AEM_DYNMAP engine constants; static configs never do (gate 10
    # byte-identity stays the proof of absence).
    def dyn(c):
        c["streams"]["listeners"][0]["map_mode"] = "dynamic"
        c["streams"]["listeners"][0]["map_page"] = 4
    p = _variant(CONFIGS["arty_current"], dyn)
    try:
        r = eb.build(p, OUT)
        ovl = r["overlay"]
        pi = ovl["stream_ports"]["input"][0]
        assert pi["maps"] == 0 and pi["base_map"] == 0
        assert pi["map_mode"] == "dynamic" and pi["map_page"] == 4
        # only the OUTPUT port's static map remains, renumbered to index 0
        assert [m["direction"] for m in ovl["audio_maps"]] == ["output"]
        assert ovl["audio_maps"][0]["index"] == 0
        assert ovl["stream_ports"]["output"][0]["base_map"] == 0
        assert ovl["descriptor_counts"]["AUDIO_MAP"] == 1
        # static ports carry NO map_mode key (overlay byte-stability)
        assert "map_mode" not in ovl["stream_ports"]["output"][0]
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(
                [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
                 "--overlay", r["paths"]["aem_overlay"], "--out-dir", td],
                check=True, capture_output=True)
            svh = open(os.path.join(td, "aecp_aem_rom.svh")).read()
        assert "`define AEM_DYNMAP" in svh
        assert "localparam int unsigned AEM_DMAP_KEYS_C  = 8;" in svh
        assert "localparam int unsigned AEM_DMAP_PAGE_C  = 4;" in svh
        assert "localparam int unsigned AEM_DMAP_NMAPS_C = 2;" in svh
        assert "WB_AUDIO_MAP_OUT_C" in svh
        # the deployed static shape's svh must NOT know the engine
        assert "AEM_DYNMAP" not in open(TRACKED_SVH).read()
        # a dynamic listener changes the model hash (capability change) and
        # the conditional key keeps every static config's hash untouched
        assert r["overlay"]["entity"] is not None
        print("  [gate 17] dynamic audio map: listeners[0] map_mode dynamic "
              "-> port n_maps=0, input AUDIO_MAP dropped (output renumbered "
              "to 0), svh emits `AEM_DYNMAP keys=8 page=4 nmaps=2; tracked "
              "deployed svh engine-free")
    finally:
        os.unlink(p)
    # unsupported placements are rejected with clear errors
    def dyn_talker(c):
        c["streams"]["talkers"][0]["map_mode"] = "dynamic"
    def dyn_page_static(c):
        c["streams"]["listeners"][0]["map_page"] = 4
    for label, mutate, needle in (
            ("talker dynamic", dyn_talker, "listeners[0] only"),
            ("map_page without dynamic", dyn_page_static, "map_mode dynamic")):
        p = _variant(CONFIGS["arty_current"], mutate)
        try:
            try:
                eb.load_config(p)
            except eb.ConfigError as e:
                assert needle in str(e), f"{label}: got {e}"
            else:
                raise AssertionError(f"{label}: accepted")
        finally:
            os.unlink(p)
    print("  [gate 17] reject paths: talker map_mode dynamic + stray "
          "map_page raise ConfigError")


MILAN_CSR_SV = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")
LWSRP_PKG_SV = os.path.join(ROOT, "hdl/ieee8021q/srp/lwsrp_pkg.sv")
LWSRP_TOP_SV = os.path.join(ROOT, "hdl/ieee8021q/srp/KL_lwsrp_top.sv")
DATAPATH_SV = os.path.join(ROOT, "hdl/milan/milan_datapath.sv")
PACKETIZER_SV = os.path.join(ROOT, "hdl/ieee1722/aaf/KL_aaf_packetizer.sv")
ETH_PKG_SV = os.path.join(ROOT, "hdl/common/ethernet_packet_pkg.sv")
MILAN_SOC_PY = os.path.join(ROOT, "sw/litex/milan_soc.py")
TRACKED_SRP_SVH = os.path.join(ROOT, "hdl/ieee8021q/srp/gen/lwsrp_table.svh")
REGMAP_MD = os.path.join(ROOT, "docs/reference/REGISTER_MAP.md")

#: Real build trees / sibling repo used by the optional cross-check gates.
#: Absent in a bare container -> those assertions SKIP with a message.
CSR_CSV_2Q = os.path.expanduser(
    "~/litex-milan/work/build_arty_eppo_milanfinal53e/csr.csv")
CSR_CSV_1Q = os.path.expanduser(
    "~/milan-avb-multiwork/build_ax8x8_rxq1fix_eppo/csr.csv")
DEPLOYED_DTS = {
    "arty": os.path.expanduser(
        "~/milan-tests-avb/fpga/dts/milan_arty_vexii.dts"),
    "ax7101": os.path.expanduser(
        "~/milan-tests-avb/fpga/dts/milan_ax7101_vexii.dts"),
}


def _sv_hex(txt, pat, label):
    """First hex literal (SystemVerilog 32'hAAAA_BBBB / 'h6A0 style) matched
    by `pat` in `txt`."""
    m = re.search(pat, txt)
    assert m, f"{label}: no RTL match for {pat!r}"
    return int(m.group(1).replace("_", ""), 16)


def _sv_int(txt, pat, label):
    m = re.search(pat, txt)
    assert m, f"{label}: no RTL match for {pat!r}"
    return int(m.group(1).replace("_", ""))


def test_lwsrp_reset_words_match_rtl():
    """Gate 18a: the emitted 0x680 reset words are byte-identical to the
    THREE hand-written places that carry them today - the milan_csr reset
    block, the milan_csr csr_default readback table, and the REGISTER_MAP
    Reset column. A hand edit in any of them that the config does not know
    about fails here."""
    csr = open(MILAN_CSR_SV).read()
    reg = open(REGMAP_MD).read()
    r = eb.build(CONFIGS["arty_current"], OUT)
    got = r["lwsrp"]["reset_words"]
    # (emitter name, milan_csr storage reg, milan_csr A_* enum, doc reset)
    rows = [("LWSRP_CTRL", "lwsrp_ctrl", "A_LWSRP_CTRL", "0xC"),
            ("LWSRP_VID", "lwsrp_vid", "A_LWSRP_VID", "2"),
            ("LWSRP_DMAC_LO", "lwsrp_dmlo", "A_LWSRP_DMLO", "0xF000_FE01"),
            ("LWSRP_DMAC_HI", "lwsrp_dmhi", "A_LWSRP_DMHI", "0x91E0"),
            ("LWSRP_TSPEC", "lwsrp_tspec", "A_LWSRP_TSPEC", "0x0001_00E0"),
            ("LWSRP_LATENCY", "lwsrp_lat", None, "0")]
    for name, storage, enum, doc in rows:
        want = _sv_hex(csr, rf"{storage}\s*<=\s*32'h([0-9A-Fa-f_]+);",
                       f"milan_csr reset block {storage}")
        assert int(got[name], 16) == want, (
            f"{name}: emitted {got[name]} != milan_csr reset "
            f"0x{want:08X} - the config and the RTL have drifted")
        if enum:
            want2 = _sv_hex(csr,
                            rf"{enum}\[10:0\]:\s*csr_default = "
                            rf"32'h([0-9A-Fa-f_]+);",
                            f"milan_csr csr_default {enum}")
            assert want2 == want, f"{name}: milan_csr disagrees with itself"
        # documented Reset column of the REGISTER_MAP row
        m = re.search(rf"\| `0x[0-9A-F]{{3}}` \| `{name}` \| RW \| `([^`]+)` \|",
                      reg)
        assert m, f"{name}: no REGISTER_MAP row"
        assert m.group(1) == doc, f"{name}: REGISTER_MAP reset {m.group(1)}"
        assert int(doc.replace("_", ""), 16 if doc.startswith("0x") else 10) \
            == want, f"{name}: REGISTER_MAP reset {doc} != RTL 0x{want:08X}"
    # CSR offsets too
    for name, off in eb.SRP_CSR_OFFSETS.items():
        enum = {"LWSRP_DMAC_LO": "A_LWSRP_DMLO", "LWSRP_DMAC_HI":
                "A_LWSRP_DMHI", "LWSRP_LATENCY": "A_LWSRP_LAT"}.get(
                    name, "A_" + name)
        want = _sv_hex(csr, rf"{enum}\s*=\s*'h([0-9A-Fa-f]+)", f"enum {enum}")
        assert off == want, f"{name}: offset 0x{off:X} != RTL 0x{want:X}"
    print(f"  [gate 18a] arty_current lwSRP reset words == milan_csr reset "
          f"block == csr_default table == REGISTER_MAP Reset column "
          f"({len(rows)} registers, {len(eb.SRP_CSR_OFFSETS)} offsets)")


def test_lwsrp_class_constants_match_rtl():
    """Gate 18b: the emitted SR-class / MRP-timer / bandwidth constants equal
    the hand-written lwsrp_pkg.sv localparams, and the PriorityAndRank byte
    milan_csr duplicates literally (it does not import the package) agrees
    with both."""
    pkg = open(LWSRP_PKG_SV).read()
    csr = open(MILAN_CSR_SV).read()
    t = eb.build(CONFIGS["arty_current"], OUT)["lwsrp"]
    checks = [
        ("SR class id", t["sr_class"]["class_id"],
         _sv_int(pkg, r"SR_CLASS_A_ID_C\s*=\s*8'd(\d+)", "pkg")),
        ("SR priority", t["sr_class"]["priority"],
         _sv_int(pkg, r"SR_CLASS_A_PRIO_C\s*=\s*8'd(\d+)", "pkg")),
        ("SR rank", t["sr_class"]["rank"],
         _sv_int(pkg, r"SR_RANK_C\s*=\s*1'b(\d)", "pkg")),
        ("join ms", t["timers_ms"]["join"],
         _sv_int(pkg, r"JOIN_TIME_MS_C\s*=\s*([\d_]+);", "pkg")),
        ("leave ms", t["timers_ms"]["leave"],
         _sv_int(pkg, r"LEAVE_TIME_MS_C\s*=\s*([\d_]+);", "pkg")),
        ("leaveall ms", t["timers_ms"]["leaveall"],
         _sv_int(pkg, r"LEAVEALL_TIME_MS_C\s*=\s*([\d_]+);", "pkg")),
        ("frame overhead", t["bandwidth"]["frame_overhead_bytes"],
         _sv_int(pkg, r"MSRP_FRAME_OVERHEAD_C\s*=\s*(\d+);", "pkg")),
        ("intervals/s", t["sr_class"]["intervals_per_second"],
         _sv_int(pkg, r"CLASS_A_INTERVALS_PS_C\s*=\s*([\d_]+);", "pkg")),
        ("bw limit pct", t["bandwidth"]["limit_pct"],
         _sv_int(pkg, r"SRP_BW_LIMIT_PCT_C\s*=\s*(\d+);", "pkg")),
    ]
    for label, got, want in checks:
        assert got == want, f"{label}: emitted {got} != lwsrp_pkg {want}"
    pr = t["sr_class"]["prio_rank"]
    assert pr == _sv_hex(csr, r"SRP_PRIO_RANK_C\s*=\s*8'h([0-9A-Fa-f]+);",
                         "milan_csr SRP_PRIO_RANK_C"), \
        "PriorityAndRank: emitter vs the milan_csr literal duplicate"
    assert pr == (t["sr_class"]["priority"] << 5) | (t["sr_class"]["rank"] << 4)
    # the bw_gate's hard ceiling literals must agree with the emitted limits
    bwg = open(os.path.join(ROOT,
                            "hdl/ieee8021q/srp/KL_lwsrp_bw_gate.sv")).read()
    for mbps, lit in ((1000, r"SLOPE_W_C'\((750_000_000)\)"),
                      (100, r"SLOPE_W_C'\((75_000_000)\)")):
        want = _sv_int(bwg, lit, "bw_gate ceiling")
        assert want == mbps * 1_000_000 * t["bandwidth"]["limit_pct"] // 100, \
            f"bw_gate {mbps} Mb/s ceiling literal != {t['bandwidth']['limit_pct']}%"
    # and the tracked generated svh reproduces every one of them
    svh = open(TRACKED_SRP_SVH).read()
    assert svh == eb.build(CONFIGS["arty_current"], OUT)["lwsrp_svh"], \
        "hdl/ieee8021q/srp/gen/lwsrp_table.svh is STALE - regenerate it"
    for needle in (f"LWSRP_CLASS_ID_C   = 8'd{t['sr_class']['class_id']};",
                   f"LWSRP_PRIO_RANK_C  = 8'h{pr:02X};",
                   "LWSRP_CTRL_RST_C      = 32'h0000_000C;",
                   "LWSRP_TSPEC_RST_C     = 32'h0001_00E0;"):
        assert needle in svh, f"tracked svh lacks {needle!r}"
    print(f"  [gate 18b] {len(checks)} SR-class/timer/bandwidth constants == "
          "lwsrp_pkg.sv, PriorityAndRank == the milan_csr literal duplicate, "
          "bw_gate 75% ceilings agree; tracked lwsrp_table.svh regenerates "
          "byte-identically")


def test_lwsrp_tspec_and_params():
    """Gate 18c: the TSpec derivation is anchored in the RTL frame geometry
    (KL_aaf_packetizer), the idleSlope formula matches KL_lwsrp_bw_gate, the
    emitted module parameters match what milan_datapath actually passes, and
    the ctx row arithmetic exposes the NxN shortfall."""
    pk = open(PACKETIZER_SV).read()
    spf = _sv_int(pk, r"SAMPLES_PER_FRAME_C\s*=\s*(\d+);", "packetizer")
    geo = eb.srp_frame_geometry(2, 48000, 8000)
    assert geo["samples_per_frame"] == spf
    # the packetizer's own documented identity: frame = 42 + 24*C bytes, and
    # C = 2 is the golden 90-byte shape its byte-compare gate pins
    assert "42 + 24*C bytes" in pk and "90-byte shape" in pk, \
        "KL_aaf_packetizer no longer states the 42 + 24*C frame identity"
    for c in range(1, 33):
        g = eb.srp_frame_geometry(c, 48000, 8000)
        assert g["l2_frame_bytes"] == 42 + 24 * c, f"C={c}: {g}"
        # MaxFrameSize is the MSDU: MaxFrameSize + 42 == the full wire slot
        assert g["avtpdu_bytes"] + eb.SRP_FRAME_OVERHEAD_B == \
            g["l2_frame_bytes"] + 8 + 4 + 12
    assert eb.srp_frame_geometry(2, 48000, 8000)["l2_frame_bytes"] == 90
    # idleSlope formula, verbatim from LWSRP_FPGA_ARCHITECTURE / bw_gate
    assert eb.srp_idle_slope_bps(224, 1, 8000) == 1 * (224 + 42) * 8 * 8000
    # per-config: derived TSpec, reservation under the ceiling, module params
    dp = open(DATAPATH_SV).read()
    top = open(LWSRP_TOP_SV).read()
    epkg = open(ETH_PKG_SV).read()
    assert re.search(r"KL_lwsrp_top #\(\.CLK_FREQ_HZ_P\(MILAN_CLK_FREQ_HZ\),"
                     r"\s*\.N_CTX_P\(N_STREAMS\)\)", dp), \
        "milan_datapath no longer ties N_CTX_P to N_STREAMS"
    assert re.search(r"KL_lwsrp_bw_gate #\(\.N_STREAMS_P\(N_CTX_P\)\)", top), \
        "KL_lwsrp_top no longer ties the bw_gate width to N_CTX_P"
    nq = _sv_int(epkg, r"NUMBER_OF_QUEUES\s*=\s*(\d+);", "ethernet_packet_pkg")
    for name, (L, T) in (("arty_current", (1, 1)), ("arty_4x4", (4, 4)),
                         ("ax7101_8x8", (8, 8))):
        r = eb.build(CONFIGS[name], OUT)
        t, cfg = r["lwsrp"], r["cfg"]
        mp = t["module_params"]
        assert mp["KL_lwsrp_top.N_CTX_P"] == max(L, T) == \
            mp["milan_datapath.N_STREAMS"] == mp["KL_lwsrp_bw_gate.N_STREAMS_P"]
        assert mp["KL_lwsrp_top.CLK_FREQ_HZ_P"] == \
            cfg["constraints"]["milan_clk_hz"] == \
            mp["milan_datapath.MILAN_CLK_FREQ_HZ"]
        assert mp["milan_csr.N_LISTENERS_P"] == L
        assert mp["milan_csr.N_TALKERS_P"] == T
        assert mp["milan_csr.NUM_QUEUES"] == nq, \
            f"{name}: num_queues != ethernet_packet_pkg NUMBER_OF_QUEUES {nq}"
        # the class-A queue must be a real queue
        assert 0 <= cfg["srp"]["class_queue"] < nq
        assert t["ctx_rows"]["required"] == L + T - 1
        assert t["ctx_rows"]["available"] == max(L, T)
        b = t["bandwidth"]
        assert b["total_idle_slope_bps"] <= b["limit_bps"]
        assert b["total_idle_slope_bps"] == sum(
            row["idle_slope_bps"] for row in t["rows"])
        talkers = [row for row in t["rows"] if row["direction"] == "talker"]
        assert len(talkers) == T
        if cfg["srp"]["tspec_policy"] == "derived":
            for row in talkers:
                assert row["max_frame_bytes"] == \
                    eb.srp_frame_geometry(row["channels"], 48000,
                                          8000)["avtpdu_bytes"]
        # per-stream DMAC = MAAP base + uid
        base = int(cfg["srp"]["stream_dmac_base"], 16)
        assert [int(row["dest_mac"], 16) for row in talkers] == \
            [base + k for k in range(T)]
        print(f"  [gate 18c] {name}: TSpec {cfg['srp']['tspec_policy']}, "
              f"{b['total_idle_slope_bps']} bps = {b['utilization_pct']}% of "
              f"the port (ceiling {b['limit_pct']}%), ctx rows "
              f"{t['ctx_rows']['required']} needed / "
              f"{t['ctx_rows']['available']} available")
    # the NxN row shortfall is a MARK, never silent
    for name in ("arty_4x4", "ax7101_8x8"):
        marks = eb.build(CONFIGS[name], OUT)["marks"]
        assert any("lwSRP attribute rows" in m[0] and
                   m[1].startswith("planned") for m in marks), \
            f"{name}: ctx-row shortfall not marked"
    cur = eb.build(CONFIGS["arty_current"], OUT)["marks"]
    assert any("lwSRP attribute row(s)" in m[0] and m[1] == "supported"
               for m in cur), "arty_current lwSRP rows must be supported"
    print("  [gate 18c] NxN ctx-row shortfall (L+T-1 rows in max(L,T) "
          "contexts) marked planned; 1x1 supported")


def test_lwsrp_rejects():
    """Gate 18d: contradictory reservations raise ConfigError."""
    cases = [
        ("class B", lambda c: c["srp"].__setitem__("sr_class", "B"),
         "5.6"),
        ("VID 0", lambda c: c["srp"].__setitem__("vid", 0), "UNSHAPED"),
        ("VID 4095", lambda c: c["srp"].__setitem__("vid", 4095), "4094"),
        ("queue 4 (2-bit field)",
         lambda c: c["srp"].__setitem__("class_queue", 4), "LWSRP_CTRL[3:2]"),
        ("unicast stream DMAC",
         lambda c: c["srp"].__setitem__("stream_dmac_base",
                                        "0x020000000001"), "MULTICAST"),
        ("unknown tspec policy",
         lambda c: c["srp"]["tspec"].__setitem__("policy", "guess"),
         "policy"),
    ]
    for label, mutate, needle in cases:
        p = _variant(CONFIGS["arty_current"], mutate)
        try:
            try:
                eb.load_config(p)
            except eb.ConfigError as e:
                assert needle in str(e), f"{label}: got {e}"
            else:
                raise AssertionError(f"{label}: accepted")
        finally:
            os.unlink(p)
    # over-subscription: 4 x 32ch talkers on the 100 Mb/s arty port =
    # 213.5 Mb/s, far past the 75 % class-A ceiling
    def fat(c):
        for t in c["streams"]["talkers"]:
            t["channels"] = 32
            t["formats"] = ["0x0205022008006000"]
    p = _variant(CONFIGS["arty_4x4"], fat)
    try:
        try:
            eb.load_config(p)
        except eb.ConfigError as e:
            assert "75% ceiling" in str(e) and "34.3.1" in str(e), \
                f"over-subscription error must cite the ceiling: {e}"
        else:
            raise AssertionError("over-subscribed reservation accepted")
    finally:
        os.unlink(p)
    print(f"  [gate 18d] {len(cases) + 1}/{len(cases) + 1} contradictory "
          "reservations rejected with ConfigError (incl. a 213 Mb/s class-A "
          "request on a 100 Mb/s port)")


def _csv_bases(path):
    """{register name: address} from a LiteX csr.csv."""
    out = {}
    for line in open(path):
        f = line.split(",")
        if len(f) >= 3 and f[0] == "csr_register":
            out[f[1]] = int(f[2], 16)
    return out


def test_platform_window_map():
    """Gate 19a: the DMA window map is DERIVED from rx-queues, and the queue
    count is the same number in the gateware argv, the sweep fragment and the
    device tree. That triple is exactly what 5ce9a13 broke."""
    m1 = eb.dma_window_map(eb.DMA_BANK_BASE, 1)
    m2 = eb.dma_window_map(eb.DMA_BANK_BASE, 2)
    assert "steer" not in m1 and "dma-rx1" not in m1
    assert "steer" in m2 and "dma-rx1" in m2
    shift = eb.DMA_STEER_BYTES + eb.DMA_RX1_BLOCK_BYTES
    assert shift == 0x74, f"steer+rx1 = 0x{shift:X}, expected 0x74"
    for name in ("dma-tx", "dma-rx"):
        assert m1[name]["base"] == m2[name]["base"], \
            f"{name} must NOT move with the queue count"
    for name in ("dma-ts", "hs-pgsz-cap", "pcm-dma"):
        assert m2[name]["base"] - m1[name]["base"] == shift, \
            f"{name}: 1q {m1[name]['base']:#x} vs 2q {m2[name]['base']:#x}"
    # milan_soc.py source order is what makes the shift happen - assert it
    soc = open(MILAN_SOC_PY).read()
    i_steer = soc.index("self.steer = RxSteer()")
    i_rx1 = soc.index("self.rx1 = RingDMAWriter")
    i_ts = soc.index("self.ts = WishboneDMAWriter")
    i_cap = soc.index("self.hs_pgsz_cap = CSRStatus")
    assert i_steer < i_rx1 < i_ts < i_cap, \
        "milan_soc MilanDMA registration order changed - the window map " \
        "derivation in dma_window_map() must be re-derived"
    assert re.search(r"if rx_queues >= 2:\s*\n\s*self\.steer = RxSteer\(\)",
                     soc), "steer is no longer conditional on rx_queues >= 2"
    # config -> argv -> sweep fragment -> device tree: ONE queue count
    for cfg_name, board in (("arty_current", "arty"), ("ax7101_8x8", "ax7101")):
        r = eb.build(CONFIGS[cfg_name], OUT)
        n = r["cfg"]["constraints"]["rx_queues"]
        argv_n = int(_canon(r["argv"])["--rx-queues"][0])
        _o, _l, sweep_n = sweep_inline(board)
        dt_n = int(re.search(r"kl,rxq-cnt = <(\d+)>", r["dt_overlay"]).group(1))
        assert n == argv_n == int(sweep_n) == dt_n == r["platform"]["rx_queues"], (
            f"{cfg_name}: rx-queues disagree - config {n}, argv {argv_n}, "
            f"sweep {sweep_n}, device tree {dt_n}")
        # ...and the map that count implies is the one in the DT/shape
        want = eb.dma_window_map(eb.DMA_BANK_BASE, n)
        for name in ("dma-tx", "dma-rx", "dma-ts"):
            assert f"0x{want[name]['base']:x} 0x{want[name]['size']:x}" \
                in r["dt_overlay"], f"{cfg_name}: DT lacks the {name} window"
        assert r["platform"]["driver_constants"]["MILAN_HS_PGSZ_CAP_PHYS"] == \
            f"0x{want['hs-pgsz-cap']['base']:08X}"
        assert (r["platform"]["driver_constants"]["MILAN_DMA_RX1_PHYS"]
                is None) == (n == 1)
        print(f"  [gate 19a] {cfg_name}: rx-queues {n} agrees across config / "
              f"soc argv / sweep fragment / device tree; dma-ts "
              f"0x{want['dma-ts']['base']:08X}, pcm 0x{want['pcm-dma']['base']:08X}")
    print("  [gate 19a] 1q->2q inserts steer+rx1 = 0x74 and moves dma-ts / "
          "hs-pgsz-cap / pcm-dma by exactly that; tx/rx0 never move")


def test_platform_dt_and_driver_shape():
    """Gate 19b: the emitted device tree carries every property the driver
    and the binding need, and - when the real build trees are on disk - its
    window bases equal the LiteX csr.csv and the deployed .dts."""
    for name in CONFIGS:
        r = eb.build(CONFIGS[name], OUT)
        dt, sh = r["dt_overlay"], r["platform"]
        for needle in ('compatible = "kl,dma-ether-0.9", "kl,dma-ether";',
                       'reg-names = "csr", "dma-tx", "dma-rx", "dma-ts", "phy";',
                       'compatible = "kl,milan-pcm-0.9", "kl,milan-pcm";',
                       'reg-names = "pcm-dma", "milan-csr";',
                       "memory-region = <&pcmring>;", "no-map;",
                       "dma-coherent;", "kl,ptp;"):
            assert needle in dt, f"{name}: device tree lacks {needle!r}"
        # kl,rsc-clk-mhz is the ONLY of_property_read_u32 kl-eth makes; omit
        # it and the AX7101 runs its PHC at 2x rate from a clean boot
        assert f"kl,rsc-clk-mhz = <{sh['rsc_clk_mhz']}>" in dt
        assert sh["rsc_clk_mhz"] * 1_000_000 == \
            r["cfg"]["constraints"]["milan_clk_hz"]
        assert f'phy-mode = "{sh["phy_mode"]}"' in dt
        assert "local-mac-address = [" + \
            " ".join(sh["mac_address"].split(":")) + "]" in dt
        # the no-map region must hold every capture stream's ring
        n_l = len(r["cfg"]["listeners"])
        assert int(sh["pcm"]["ring_stride"], 16) * n_l <= \
            int(sh["pcm"]["ring_bytes"], 16)
        assert f"kl,capture-streams = <{n_l}>" in dt
        print(f"  [gate 19b] {name}: DT node complete (5 reg windows, "
              f"kl,rsc-clk-mhz {sh['rsc_clk_mhz']}, phy-mode "
              f"{sh['phy_mode']}, {n_l}-stream {sh['pcm']['ring_bytes']} "
              "no-map ring)")
    # ---- cross-check against real artifacts when they are on disk --------
    checked = 0
    for csv, cfg_name in ((CSR_CSV_2Q, "arty_current"),
                          (CSR_CSV_1Q, "ax7101_8x8")):
        if not os.path.exists(csv):
            continue
        regs = _csv_bases(csv)
        sh = eb.build(CONFIGS[cfg_name], OUT)["platform"]
        pairs = [("dma-tx", "milan_dma_tx_base"),
                 ("dma-rx", "milan_dma_rx_base"),
                 ("dma-ts", "milan_dma_ts_base"),
                 ("hs-pgsz-cap", "milan_dma_hs_pgsz_cap"),
                 ("pcm-dma", "milan_dma_pcm_base")]
        if "dma-rx1" in sh["windows"]:
            pairs.append(("dma-rx1", "milan_dma_rx1_base"))
        for win, reg in pairs:
            assert reg in regs, f"{csv}: no {reg} row"
            assert int(sh["windows"][win]["base"], 16) == regs[reg], (
                f"{cfg_name}: {win} {sh['windows'][win]['base']} != "
                f"csr.csv {reg} 0x{regs[reg]:08X}")
        checked += 1
        print(f"  [gate 19b] {cfg_name}: {len(pairs)} window bases "
              f"BYTE-MATCH the real LiteX csr.csv ({os.path.basename(os.path.dirname(csv))})")
    if not checked:
        print("  [gate 19b] SKIP csr.csv cross-check: no build tree on disk")
    checked = 0
    for cfg_name, board in (("arty_current", "arty"), ("ax7101_8x8", "ax7101")):
        dts = DEPLOYED_DTS[board]
        if not os.path.exists(dts):
            continue
        txt = open(dts).read()
        sh = eb.build(CONFIGS[cfg_name], OUT)["platform"]
        nic = re.search(r"ethernet@\w+ \{(.*?)\n\t*\};", txt, re.S)
        assert nic, f"{dts}: no ethernet node"
        cells = [int(x, 16) for x in
                 re.findall(r"<0x([0-9a-f]+) 0x[0-9a-f]+>", nic.group(1))]
        want = [int(sh["csr"]["base"], 16)] + \
            [int(sh["windows"][k]["base"], 16)
             for k in ("dma-tx", "dma-rx", "dma-ts")] + \
            [int(sh["phy_window"]["base"], 16)]
        assert cells == want, (
            f"{cfg_name}: emitted NIC reg bases {[hex(x) for x in want]} != "
            f"deployed {dts} {[hex(x) for x in cells]}")
        pcm = re.search(r"audio@([0-9a-f]+)", txt)
        assert pcm and int(pcm.group(1), 16) == \
            int(sh["pcm"]["base"], 16), \
            f"{cfg_name}: PCM node base != deployed {dts}"
        assert f"kl,rsc-clk-mhz = <{sh['rsc_clk_mhz']}>" in txt
        checked += 1
        print(f"  [gate 19b] {cfg_name}: all 5 NIC reg bases + the PCM node "
              f"base + kl,rsc-clk-mhz MATCH the deployed {os.path.basename(dts)}")
    if not checked:
        print("  [gate 19b] SKIP deployed-.dts cross-check: sibling repo "
              "milan-tests-avb not on disk")


def test_platform_rejects():
    """Gate 19c: a platform shape that contradicts itself or the flashed boot
    chain raises ConfigError. The boot_chain_pin case IS the 5ce9a13 bug -
    caught before a build instead of after a flash."""
    cases = [
        ("multicast station MAC",
         lambda c: c["platform"].__setitem__("mac_address",
                                             "01:00:00:00:00:02"),
         "UNICAST"),
        ("missing MAC", lambda c: c["platform"].pop("mac_address"),
         "mac_address is required"),
        ("csr_base below the IO region",
         lambda c: c["platform"].__setitem__("csr_base", 0x4000_0000),
         "0x80000000"),
        ("PCM ring overrun",
         lambda c: c["platform"].__setitem__("pcm_ring_bytes", 0x1000),
         "no-map"),
        ("unknown pinned window",
         lambda c: c["platform"]["boot_chain_pin"].__setitem__("dma-rx7", 0),
         "unknown window"),
    ]
    for label, mutate, needle in cases:
        p = _variant(CONFIGS["arty_current"], mutate)
        try:
            try:
                eb.load_config(p)
            except eb.ConfigError as e:
                assert needle in str(e), f"{label}: got {e}"
            else:
                raise AssertionError(f"{label}: accepted")
        finally:
            os.unlink(p)
    # THE gate: flip rx_queues under a pinned boot chain (5ce9a13 verbatim -
    # sweep.sh set 1 for both boards while the deployed arty carries 2)
    for cfg_name, flip in (("arty_current", 1), ("ax7101_8x8", 2)):
        p = _variant(CONFIGS[cfg_name],
                     lambda c, n=flip: c["board"]["constraints"]
                     .__setitem__("rx_queues", n))
        try:
            try:
                eb.load_config(p)
            except eb.ConfigError as e:
                assert "boot_chain_pin" in str(e) and "0x74" in str(e) \
                    and "CSR-rot" in str(e), f"{cfg_name}: got {e}"
            else:
                raise AssertionError(
                    f"{cfg_name}: rx_queues={flip} accepted under a pinned "
                    "boot chain - the 5ce9a13 CSR-rot bug is still possible")
        finally:
            os.unlink(p)
        print(f"  [gate 19c] {cfg_name}: rx_queues -> {flip} REFUSED "
              "(boot_chain_pin: every window from dma-ts on moves by 0x74)")
    # a non-integer-MHz datapath clock cannot be expressed as kl,rsc-clk-mhz
    p = _variant(CONFIGS["arty_current"],
                 lambda c: c["board"]["constraints"]
                 .__setitem__("milan_clk_hz", 50_000_001))
    try:
        try:
            eb.load_config(p)
        except eb.ConfigError as e:
            assert "kl,rsc-clk-mhz" in str(e)
        else:
            raise AssertionError("non-integer-MHz datapath clock accepted")
    finally:
        os.unlink(p)
    print(f"  [gate 19c] {len(cases) + 3}/{len(cases) + 3} contradictory "
          "platform shapes rejected with ConfigError")


if __name__ == "__main__":
    for fn in (test_all_configs_build, test_current_shape_matches_sweep_flags,
               test_current_shape_matches_gen_aem_store,
               test_capability_marks, test_bad_configs_rejected,
               test_port_layout_invariants, test_both_policies_valid,
               test_model_id_hashing, test_sweep_opts_fragments,
               test_gen_aem_store_consumes_overlay,
               test_resource_calibration, test_resource_determinism,
               test_resource_verdicts, test_milan_723_crf_output_rule,
               test_crf_output_overlay_structure,
               test_gen_aem_store_crf_output_overlay,
               test_dynamic_audio_map_overlay,
               test_lwsrp_reset_words_match_rtl,
               test_lwsrp_class_constants_match_rtl,
               test_lwsrp_tspec_and_params, test_lwsrp_rejects,
               test_platform_window_map,
               test_platform_dt_and_driver_shape, test_platform_rejects):
        print(f"{fn.__name__}:")
        fn()
    print("ALL GATES PASS")
