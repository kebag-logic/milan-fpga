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
  10. gen_aem_store.py CONSUMES the OWNING config's overlay (--overlay,
      subprocess) and the generated aecp_aem_rom.svh is byte-identical to
      the tracked hdl/ieee17221/aecp/gen/aecp_aem_rom.svh - THE key
      no-regression gate.  WHICH config owns the tracked ROM is READ FROM
      THE TREE (the shape include's `Source :` marker, via
      check_entity_shape.tracked_owner - the same single reader its check E
      uses), never assumed: `--write-rtl <cfg>` installs the pair for
      whichever config it is handed, and a gate that hardcoded
      endstation_arty_current went red for every other owner, which blocked
      any other shape from being written into the tree at all.  The gate
      ships its own mutations (cross-config ROM, forged marker, unowned
      marker, a one-field ROM edit) so "follows the owner" cannot decay into
      "accepts anything".  The default (no-overlay) builtin path is a
      SEPARATE property - that model is arty_current's, hand-written in
      gen_aem_store.py and pinned there by gate 3 - so it is compared
      against arty_current's overlay-built ROM, which does not move when the
      tracked owner does;
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
      AUDIO_MAP (1722.1-2021 7.2.13 number_of_maps=0) and emits the
      `AEM_DYNMAP engine constants.  The engine is CONDITIONAL codegen, so
      the tracked ROM must carry it IF AND ONLY IF the config that OWNS the
      tracked pair declares a dynamic port - the owner is read from the tree
      (the shape include's `Source :` marker, via the same
      check_entity_shape.tracked_owner gate 10 uses), never assumed.  The
      old form hardcoded the negative ("the tracked svh has no engine"),
      which reads the tracked artifact under an assumption about its owner
      and would go red the day a dynamic config legitimately owns it - gate
      10's defect in the other polarity.  Both directions are proven on
      candidate pairs in temp dirs (a dynamic owner REQUIRES the engine, a
      static one FORBIDS it, an unresolvable owner FAILS); reject paths;
  18a. lwSRP table emitter: the emitted 0x680 reset words + CSR offsets are
      the words milan_csr.sv elaborates - the gate walks emitted word ->
      the generated LWSRP_*_RST_C symbol -> milan_csr's reset block ->
      milan_csr's csr_default readback table -> the REGISTER_MAP Reset
      column (all parsed at test time);
  18b. the emitted SR-class / MRP-timer / bandwidth constants equal the
      lwsrp_pkg.sv localparams, the PriorityAndRank byte milan_csr drives
      onto o_srp_ctx_prio_rank, and the KL_lwsrp_bw_gate 75%-ceiling literals;
      the tracked hdl/ieee8021q/srp/gen/lwsrp_table.svh regenerates
      BYTE-IDENTICALLY (the staleness gate);
  18c. TSpec derivation anchored in the RTL frame geometry (KL_aaf_packetizer
      SAMPLES_PER_FRAME_C + its documented 42+24*C / 90-byte identities),
      idleSlope == the bw_gate formula, module params == what milan_datapath
      passes (N_CTX_P = N_STREAMS, bw_gate width = N_CTX_P, NUM_QUEUES ==
      ethernet_packet_pkg), and the NxN ctx-row shortfall (L+T-1 rows in
      max(L,T) contexts) surfaces as a planned mark;
  18d. reject paths: class B, VID 0/4095, class_queue 8, a unicast stream
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
      boot_chain_pin (5ce9a13 verbatim) raises ConfigError;
  20a. THE LOOP IS CLOSED: milan_csr.sv `include-s the generated
      hdl/common/csr/gen/lwsrp_csr_defaults.svh instead of hand-keeping the
      0x680 literals. The tracked header regenerates byte-identically, every
      emitted word equals the FROZEN pre-switch literal (so the switch is a
      provable zero-change refactor), no 0x680 literal survives in the RTL,
      the CSR subset agrees word-for-word with lwsrp_table.svh, and every
      flow that compiles milan_csr.sv carries hdl/common/csr as an include
      dir (Verilator resolves `include against -I/+incdir and the CWD only,
      never against the including file's directory);
  20b. reject paths for the newly RTL-consumed word: a non-boolean
      enable_at_reset / talker_declare_at_reset (2 << 1 used to land silently
      in class_queue[0]) or rtl_table raises ConfigError;
  21a. `audio_interface.kind: aes3|spdif` is a REAL config switch: the
      biphase-mark ser/des landed (KL_aes3_rx + KL_aes3_tx), one core serves
      both transports, and the config picks CONSUMER_P (channel-status
      dialect), WORD_BITS_P (16/20/24) and the serial clock the transport
      forces (rate x 128 UI/frame x oversample, an exact audio-PLL divide).
      Parameter names, RTL defaults and the 192-frame block are PARSED from
      the modules; the non-biphase kinds emit nothing;
  21b. reject paths: a word length the AES3 subframe cannot carry, and an
      audio PLL that cannot divide to the serial clock, raise ConfigError.

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
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import yaml  # noqa: E402

import endstation_builder as eb  # noqa: E402
#: The ONE reader of "which config owns the tracked entity definition"
#: (gate 10).  Imported rather than re-implemented: a second answer to that
#: question is how gate 10 came to assume a config in the first place.
import check_entity_shape as ces  # noqa: E402

CONFIGS = {
    "arty_current": os.path.join(ROOT, "configs/endstation_arty_current.yaml"),
    "arty_4x4": os.path.join(ROOT, "configs/endstation_arty_4x4.yaml"),
    "ax7101_8x8": os.path.join(ROOT, "configs/endstation_ax7101_8x8.yaml"),
}
OUT = os.path.join(HERE, "out")
SWEEP = os.path.join(ROOT, "sw/litex/sweep.sh")
#: The TRACKED entity definition - the pair a gateware `include-s.  Paths come
#: from the builder that writes them, so there is one spelling of each.
TRACKED_SVH = os.path.join(ROOT, eb.AEM_ROM_REL)
TRACKED_ADP_SVH = os.path.join(ROOT, eb.ADP_SHAPE_REL)

# Flow flags: sweep.sh mechanics, never part of the end-station definition.
# synth/opt directives joined 2026-07-28 when the reference flow gained
# AreaOptimized_high + ExploreArea (the only recipe that packs the 0x0019
# fabric) - they shape the IMPLEMENTATION, not the design, so the config
# argv rightly never carries them.
FLOW_FLAGS = {"--build": 0, "--vivado-max-threads": 1,
              "--place-directive": 1, "--output-dir": 1,
              "--synth-directive": 1, "--opt-directive": 1,
              # where the build READS its generated entity from is sweep
              # mechanics (the 2026-07-28 concurrent-sweep change), not a
              # property of the end-station definition
              "--entity-gen-dir": 1}

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
    port with port-relative in-range rows.

    The map-ROW rule is policy-dependent and that is the point of D8, so it
    is stated per policy rather than loosened for everybody:

      legacy policies - the port's cluster block IS the stream's channel
        space, so the map is the IDENTITY over the whole block (unchanged,
        still exact).
      role-pools - the block is a SELECTION SET (physical + host + pilot +
        loopback), so only the primary segment is wired at power-on: rows
        land inside that segment, one per stream channel, and NEVER cover
        the whole block. A role-pools shape that emitted an identity map
        would be claiming every pool feeds the stream at once.

    Both forms are checked against the 1722.1-2021 7.2.19 uniqueness rules
    (input: at most one entry per cluster channel; output: at most one entry
    per stream channel).

    A map_mode-dynamic port (Milan v1.2 5.3.3.9) owns NO AUDIO_MAP at all:
    1722.1-2021 7.2.13 has it advertise number_of_maps=0 with base_map
    ignored, so it is excluded from every map rule here and the remaining
    STATIC maps stay densely numbered."""
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
    dyn = [p for p in P_in + P_out if p.get("map_mode") == "dynamic"]
    static = [p for p in P_in + P_out if p.get("map_mode") != "dynamic"]
    # dynamic ports: the 7.2.13 capability signal, nothing else
    for p in dyn:
        assert p["maps"] == 0 and p["base_map"] == 0, \
            f"dynamic port must advertise n_maps=0/base_map=0: {p}"
    # map bases: unique, one per STATIC port, densely covering 0..n_maps-1
    bases = [p["base_map"] for p in static]
    assert sorted(bases) == list(range(len(bases))), f"map bases overlap: {bases}"
    assert all(p["maps"] == 1 for p in static)
    assert dc["AUDIO_MAP"] == len(bases) == len(ovl["audio_maps"])
    # every cluster carries exactly one role segment, segments tile the block
    for p in P_in + P_out:
        off = 0
        for g in p["pool"]:
            assert g["offset"] == off, f"pool not contiguous: {p}"
            assert g["width"] >= 1 and g["role"] in eb.CLUSTER_ROLES, p
            off += g["width"]
        assert off == p["clusters"], f"pool does not tile the block: {p}"
    # D10: one name per cluster, in global descriptor-index order
    clusters = sorted(ovl["audio_clusters"], key=lambda c: c["index"])
    assert [c["index"] for c in clusters] == list(range(dc["AUDIO_CLUSTER"]))
    assert all(c["name"] and c["role"] in eb.CLUSTER_ROLES for c in clusters)
    pooled = ovl["cluster_policy"] == "role-pools"
    # per-map rows: correct stream, port-relative offsets in range
    by_index = {m["index"]: m for m in ovl["audio_maps"]}
    for direction, ports in (("input", P_in), ("output", P_out)):
        for p in ports:
            if p.get("map_mode") == "dynamic":
                continue
            m = by_index[p["base_map"]]
            assert m["direction"] == direction and m["port_index"] == p["index"]
            prim = next(g for g in p["pool"] if g["role"] == p["primary_role"])
            if pooled:
                assert 0 < len(m["mappings"]) <= prim["width"], \
                    f"role-pools map {m['index']} outside its primary segment"
            else:
                assert len(m["mappings"]) == p["clusters"]
            seen = set()
            for (si, ch, off, cch) in m["mappings"]:
                assert si == p["stream_index"]
                assert 0 <= off < p["clusters"], \
                    f"map {m['index']}: offset {off} outside port ({p})"
                if pooled:
                    assert prim["offset"] <= off < prim["offset"] + prim["width"], \
                        f"map {m['index']}: offset {off} outside primary {prim}"
                assert cch == 0
                # 7.2.19 uniqueness: input keyed by cluster channel, output
                # keyed by stream channel
                key = (off, cch) if direction == "input" else (si, ch)
                assert key not in seen, \
                    f"map {m['index']}: 7.2.19 duplicate key {key}"
                seen.add(key)


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
    # The shipping Arty shape is the 4x4 tdm8-master since 2026-07-28 (the
    # 8.3b flash decision); sweep.sh's arty table says so, and this gate
    # compares like against like. arty_current remains a valid config (and
    # build.sh cfg_arty's), it just no longer owns the sweep table.
    r = eb.build(CONFIGS["arty_4x4"], OUT)
    got, want = _canon(r["argv"]), sweep_expected("arty")
    assert got == want, f"arty argv mismatch:\n got  {got}\n want {want}"
    print("  [gate 2] arty_4x4 argv == sweep.sh arty design flags "
          f"({len(got)} flags)")
    for name in ("ax7101_8x8",):
        r = eb.build(CONFIGS[name], OUT)
        got, want = _canon(r["argv"]), sweep_expected("ax7101")
        # NXN_ARCHITECTURE P0: multi-stream shapes additionally carry
        # --num-streams (the milan_datapath N_STREAMS parameter); sweep.sh
        # tracks today's 1x1 build, so the flag rides on top of its OPTS.
        want = dict(want)
        want["--num-streams"] = [8.0]
        # item-4 audio-interface family: tdm kinds ride on top of the OPTS as
        # the front-end generate select (default i2s emits nothing) - BUT ONLY
        # WHEN THE FABRIC BACKS THEM. That question is NOT hardcoded here: it
        # is asked of endstation_builder, which reads it out of milan_soc.py,
        # so this gate states the RULE and stays true on both sides of the
        # 2026-07-28 change rather than needing an edit when the answer moves.
        #
        #   unbacked (a PLACEHOLDER) - USER 2026-07-27, "the tdm can be a
        #     placeholder": the declaration stays, because it states what the
        #     product will be, but the flag is WITHHELD so the bitstream
        #     elaborates the I2S front-end the board actually has. A build
        #     carrying --audio-interface on a bus tied to zero has talkers that
        #     emit NO FRAME AT ALL - fsync never toggles, KL_tdm_capture yields
        #     no pairs. Withholding it is exactly how the shipping bitstream
        #     was hand-built.
        #   backed - since 2026-07-28 the fabric MASTERS the bus
        #     (KL_tdm_capture_master generates bclk/fsync off its own MMCM
        #     output), so the front-end is real and the flag is emitted,
        #     together with --audio-interface-master and the raised
        #     --talker-wire-chans the front-end can now feed.
        kind = eb.load_config(CONFIGS[name])["interface"]["kind"]
        if eb.interface_is_placeholder(eb.load_config(CONFIGS[name])):
            assert "--audio-interface" not in got, (
                f"placeholder {kind} must NOT reach the soc argv while nothing "
                f"in the fabric drives that bus")
        else:
            want["--audio-interface"] = [kind]
            if eb.tdm_bus_master():
                want["--audio-interface-master"] = []      # a bare store_true
            chans = eb.framer_wire_channels(eb.load_config(CONFIGS[name]))
            if chans != eb.WIRE_CHANS_MIN:
                want["--talker-wire-chans"] = [float(chans)]
        assert got == want, f"{name} argv mismatch:\n got  {got}\n want {want}"
        # The port is NOT pinned to a literal here. It is a property of the
        # BENCH (which socket the cable is in), not of the design, and pinning
        # it to `e2` is what let the config and sweep.sh disagree until a
        # bitstream was built for a port with no cable in it. What must hold is
        # that every source agrees with the config - which the `got == want`
        # comparison above already enforces, since `want` is derived from it.
        assert got["--eth-port"] in (["e1"], ["e2"]), \
            f"ax7101 --eth-port must be e1 or e2, got {got['--eth-port']}"
        print(f"  [gate 2] {name} argv == sweep.sh ax7101 design flags "
              f"({len(got)} flags, --eth-port {got['--eth-port'][0]} == the config)")


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
        # item-4 audio-interface family. THE MARK MUST STATE THE FABRIC FACT,
        # and TWO independent questions decide which fact:
        #
        #   (a) does this config DECLARE a tdm front-end at all? Keyed off the
        #       config's own `kind`, never a hardcoded list of config names
        #       (methodology R4). A config declaring no tdm front-end must NOT
        #       be required to carry a tdm mark - endstation_arty_4x4 stopped
        #       declaring tdm8 on 2026-07-28 because the Arty routes no `tdm`
        #       resource and has no TDM device, and once the master made
        #       tdm_bus_wired() globally true that declaration would have
        #       emitted --audio-interface tdm8 --audio-interface-master on a
        #       board where it frames digital silence AND takes i2s_mclk off
        #       pmoda:4 (D13). See gates 24c/24d + board_audio_routing.py.
        #   (b) if it does declare one, is anything DRIVING it?
        #       UNDRIVEN: milan_soc.py ties i_tdm_bclk_i/i_tdm_fsync_i/
        #         i_tdm_data_i to 0 and no platform provides pads, so the
        #         SLAVE's fsync never toggles and it yields no pairs. The
        #         ser/des is supported and the INTERFACE is a placeholder, so
        #         the mark names which half is missing (the aes3/spdif shape).
        #         The declaration stays (USER: "the tdm can be a placeholder").
        #       MASTERED (KL_tdm_capture_master): the fabric generates
        #         bclk/fsync off its own MMCM output, so nobody has to drive it.
        #         The mark must name the MASTER module - "KL_tdm_capture" alone
        #         would describe the slave path that is still dead.
        #
        # Both asked of the builder rather than hardcoded, so this gate states
        # the rule and needs no edit when either answer moves again.
        cfg_obj = eb.load_config(CONFIGS[name])
        kind = cfg_obj["interface"]["kind"]
        tdm = [m for m in r["marks"]
               if m[0].startswith("audio interface tdm")]
        if kind in ("tdm8", "tdm16", "tdm32"):
            assert tdm, f"{name}: declares {kind} but has no tdm mark at all"
            if eb.interface_is_placeholder(cfg_obj):
                assert tdm[0][1].startswith("planned (item 4"), \
                    f"{name}: an undriven tdm bus must be a planned mark: {tdm}"
                assert "KL_tdm_capture" in tdm[0][2] and \
                       "NOTHING DRIVES IT" in tdm[0][2], \
                    f"{name}: the tdm mark must name the ser/des AND the " \
                    f"missing half: {tdm}"
            else:
                assert tdm[0][1] == "supported", \
                    f"{name}: a backed tdm bus must not be planned: {tdm}"
                assert "KL_tdm_capture_master" in tdm[0][2], \
                    f"{name}: a MASTERED bus must name the master module, not " \
                    f"the slave that is still undriven: {tdm}"
        else:
            assert not tdm, \
                f"{name}: declares {kind} but carries a tdm mark: {tdm}"
        assert "planned (item 5" in r["plan"], f"{name}: plan lacks marker"
        print(f"  [gate 4] {name}: {len(planned)} planned mark(s) (item 5"
              + (", tdm mark = " + tdm[0][1] if tdm else "")
              + f"), declared interface {kind}, no failure")
    # aes3/spdif: the biphase-mark ser/des LANDED (KL_aes3_rx + KL_aes3_tx),
    # so the transport itself is supported and only the datapath/SoC plumbing
    # is still a planned mark - the mark must say WHICH half is missing.
    for kind in ("aes3", "spdif"):
        v = _variant(CONFIGS["arty_current"],
                     lambda c, k=kind: c["audio_interface"].__setitem__("kind", k))
        try:
            r = eb.build(v, OUT)
        finally:
            os.unlink(v)
        serdes = [m for m in r["marks"] if m[0].endswith("ser/des")]
        assert serdes and serdes[0][1] == "supported" \
            and eb.AES3_RX_MODULE in serdes[0][2] \
            and eb.AES3_TX_MODULE in serdes[0][2], \
            f"{kind}: ser/des must be supported now: {serdes}"
        integ = [m for m in r["marks"] if m[0].endswith("datapath integration")]
        assert integ and integ[0][1].startswith("planned (item 4") \
            and "milan_datapath" in integ[0][2] \
            and "milan_soc.py" in integ[0][2], \
            f"{kind}: SoC plumbing must stay an HONEST planned mark: {integ}"
        print(f"  [gate 4] {kind} variant: ser/des supported "
              f"({eb.AES3_RX_MODULE} + {eb.AES3_TX_MODULE}), datapath/SoC "
              f"plumbing still planned")
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
    #: pools are read ONLY by role-pools, so switching a config's policy has
    #: to move them with it - declaring pools under another policy is a
    #: refused config (they would be silently ignored).
    def set_policy(c, pol):
        cm = c["audio_interface"]["cluster_mapping"]
        cm["policy"] = pol
        if pol == "role-pools":
            cm.setdefault("pools", {"host": 4, "pilot": True, "loopback": 4})
        else:
            cm.pop("pools", None)

    for name, (nl, nt) in (("arty_4x4", (4, 4)), ("ax7101_8x8", (8, 8))):
        for pol in eb.CLUSTER_POLICIES:
            p = _variant(CONFIGS[name],
                         lambda c, pol=pol: set_policy(c, pol))
            try:
                r = eb.build(p, os.path.join(OUT, "_policy_variants"))
                check_port_layout(r["overlay"], nl, nt)
                assert r["overlay"]["cluster_policy"] == pol
            finally:
                os.unlink(p)
        print(f"  [gate 7] {name}: all {len(eb.CLUSTER_POLICIES)} cluster "
              "policies -> valid layouts")
    # cap-at-interface must actually CAP: 8ch listeners on a 2ch i2s
    def to_i2s(c):
        c["audio_interface"]["kind"] = "i2s_philips"
        # an i2s interface implies a DAC: the mutated variant must not carry
        # the AX's 2026-07-28 i2s_playback/render_lpf area prunes, which
        # validate_features rightly refuses next to a declared DAC
        c["board"].pop("features", None)
        set_policy(c, "cap-at-interface")
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
        set_policy(c, "cluster-per-stream-channel")
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
        # arty_4x4's talkers default to clusters == channels == 4 since the
        # 8.3b tdm8 shape, so the mutation must move AWAY from 4 to shape
        ("talker clusters", lambda c: c["streams"]["talkers"][0]
         .__setitem__("clusters", 2)),
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


def _tracked_owner_config():
    """Which config owns the tracked entity definition RIGHT NOW.

    The tracked ROM is ONE config's, whole - whichever config was last
    regenerated into hdl/. Hardcoding arty_current here made this gate and
    check_entity_shape.py's --built-config gate MUTUALLY UNSATISFIABLE the
    moment the tree was regenerated for the 8x8 ship shape: one demanded the
    tracked ROM be 1x1, the other demanded it be the config being built. A
    gate that forces the tree to carry the WRONG entity definition is worse
    than no gate - that is the 2026-07-27 defect (an 8x8 gateware carrying a
    1x1 descriptor set) with the layers swapped. Read the same `Source :`
    marker check_entity_shape.py reads, and hold whoever owns it to account."""
    adp = open(os.path.join(ROOT, eb.ADP_SHAPE_REL)).read()
    m = re.search(r"//\s*Source\s*:\s*(\S+)", adp)
    assert m, f"{eb.ADP_SHAPE_REL}: no `Source :` marker - cannot tell which "
    src = m.group(1)
    for name, path in CONFIGS.items():
        if eb.load_config(path)["source"] == src:
            return name, path
    raise AssertionError(
        f"tracked entity definition names {src!r}, which is not a known "
        f"config ({', '.join(sorted(CONFIGS))}) - regenerate hdl/ from a "
        f"tracked config with sw/builder/endstation_builder.py --write-rtl")


def test_gen_aem_store_consumes_overlay():
    owner, owner_path = _tracked_owner_config()
    r = eb.build(owner_path, OUT)
    tracked = open(TRACKED_SVH, "rb").read()
    with tempfile.TemporaryDirectory() as td:
        # THE key no-regression gate: builder overlay -> gen_aem_store ->
        # byte-identical ROM svh for the shape the tree actually carries
        subprocess.run(
            [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
             "--overlay", r["paths"]["aem_overlay"], "--out-dir", td],
            check=True, capture_output=True)
        got = open(os.path.join(td, "aecp_aem_rom.svh"), "rb").read()
        assert got == tracked, (
            "overlay-built aecp_aem_rom.svh differs from the tracked ROM "
            f"({len(got)} vs {len(tracked)} bytes) for its OWN source config "
            f"{owner} - the tracked pair is internally inconsistent")
        print(f"  [gate 10] {owner} overlay -> gen_aem_store --overlay: "
              f"svh BYTE-IDENTICAL to tracked ROM ({len(got)} B)")
    with tempfile.TemporaryDirectory() as td:
        # Refactor guard on the default (builtin) path. It is pinned to
        # arty_current's overlay, NOT to the tracked ROM: the builtin
        # descriptor set is the 1x1 one, so tying it to whatever shape is
        # tracked would break this guard every time the tree is regenerated
        # for another board - which is a property of the TREE, not a
        # regression in gen_aem_store.
        ref = eb.build(CONFIGS["arty_current"], OUT)
        subprocess.run(
            [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
             "--out-dir", td], check=True, capture_output=True)
        got = open(os.path.join(td, "aecp_aem_rom.svh"), "rb").read()
        with tempfile.TemporaryDirectory() as td2:
            subprocess.run(
                [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
                 "--overlay", ref["paths"]["aem_overlay"], "--out-dir", td2],
                check=True, capture_output=True)
            want = open(os.path.join(td2, "aecp_aem_rom.svh"), "rb").read()
        assert got == want, (
            "default-path svh regressed: the builtin descriptor set no longer "
            f"equals arty_current's overlay ({len(got)} vs {len(want)} bytes)")
        print("  [gate 10] gen_aem_store default path == arty_current overlay "
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
        # ...and no map/cluster growth. Both NxN shapes run map_mode
        # dynamic on every listener (Milan 5.3.3.9), so only the n talker
        # ports carry AUDIO_MAP descriptors.
        assert dc["AUDIO_MAP"] == n
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


def _dynmap_candidate(cfg_path, td):
    """The tracked pair `--write-rtl <cfg>` WOULD install for cfg_path,
    written to td.  Same technique as gate 10's candidate pairs - the real
    tree is never touched.  It takes a PATH rather than a CONFIGS key
    because the DYNAMIC owner this gate has to reason about does not exist
    under configs/ and must not be added there: it is a temp-dir fixture."""
    r = eb.build(cfg_path, OUT)
    assert r["aem_rom_svh"] is not None, (
        f"{cfg_path}: no descriptor ROM can be generated for this shape "
        f"({r['aem_rom_unsupported']}) - it could never own the tracked pair")
    adp_p = os.path.join(td, "adp_shape_defaults.svh")
    rom_p = os.path.join(td, "aecp_aem_rom.svh")
    with open(adp_p, "w") as f:
        f.write(r["adp_shape_svh"])
    with open(rom_p, "w") as f:
        f.write(r["aem_rom_svh"])
    return adp_p, rom_p


def _check_tracked_dynmap(adp_path, rom_path, configs=None):
    """Gate 17's engine-presence check, asked of ANY tracked pair.

    THE PROPERTY IS UNCHANGED: `AEM_DYNMAP is CONDITIONAL codegen.  The
    dynamic-map engine constants are in a generated descriptor ROM IF AND
    ONLY IF the config that ROM was generated from declares a dynamic
    audio-map port - that is what `map_mode: dynamic` means (1722.1-2021
    7.2.13 / Milan v1.2 5.4.2.27-28: a dynamically-mapped port carries no
    AUDIO_MAP descriptor and advertises number_of_maps = 0).  A static shape
    must not drag the engine into a gateware that has no use for it.

    WHAT MOVED is the EXPECTATION.  It used to be the constant "absent" -
    `assert "AEM_DYNMAP" not in open(TRACKED_SVH).read()` - which reads the
    TRACKED artifact while ASSUMING which config owns it.  Harmless while
    all three shipped configs are static, red the day a `map_mode: dynamic`
    config legitimately owns the tracked pair, and red for a reason that has
    nothing to do with conditional codegen.  This is gate 10's defect in the
    other polarity, so it gets gate 10's fix: the owner is READ from the
    shape include's `Source :` marker through ces.tracked_owner - the ONE
    reader of that question in this repo - and the expectation is DERIVED
    from what that config declares.  Two answers to "who owns the tracked
    ROM" is exactly how this defect class propagates.

    The standard is SILENT on which config owns a build artifact; that part
    is build hygiene, not conformance.  What the standard fixes is the
    meaning of the declaration the expectation is derived from.

    configs overrides the search list so a caller can ask the question of a
    CANDIDATE pair (a temp-dir fixture) without installing it in the tree.
    Returns (owner name, expected engine presence).
    """
    adp = open(adp_path).read()
    src, owner = ces.tracked_owner(eb, adp_text=adp, configs=configs)
    assert src is not None, (
        f"{adp_path}: no `Source :` marker - the tree does not record WHICH "
        "config owns the tracked entity definition, so there is nothing to "
        "derive an `AEM_DYNMAP expectation from")
    assert owner is not None, (
        f"{adp_path}: `Source : {src}` names no config - the tracked entity "
        "definition has no owner, so whether it MAY carry `AEM_DYNMAP is "
        "unanswerable.  A gate that cannot find the owner stops, it does "
        "not shrug and pass")
    # "declares a dynamic port" is read from the OWNER.  load_config confines
    # map_mode dynamic to listeners[0] (the reject paths below are the proof),
    # so scanning the listener list is complete today and stays correct if the
    # RTL engine's scope widens.
    want = any(s.get("map_mode", "static") == "dynamic"
               for s in owner["listeners"])
    got = "AEM_DYNMAP" in open(rom_path).read()
    assert got == want, (
        f"{rom_path}: `AEM_DYNMAP {'present' if got else 'absent'} but its "
        f"owner {owner['name']} ({src}) declares "
        f"{'a dynamic' if want else 'NO dynamic'} audio-map port - the "
        f"engine constants must be emitted IF AND ONLY IF the owning config "
        f"asks for them")
    return owner["name"], want


def _expect_dynmap_rejected(label, fn):
    """R2: a check that cannot fail is not a check."""
    try:
        fn()
    except AssertionError as e:
        print(f"  [gate 17] MUTATION rejected: {label}\n"
              f"            ({str(e).splitlines()[0][:100]})")
        return
    raise AssertionError(f"gate 17 ACCEPTED a tracked ROM it must reject: "
                         f"{label}")


def test_dynamic_audio_map_overlay():
    # gaps item 8: listeners[0] map_mode dynamic drops the port's AUDIO_MAP
    # (7.2.13 number_of_maps=0) and the overlay -> gen_aem_store path emits
    # the `AEM_DYNMAP engine constants; a config that declares no dynamic
    # port never does.
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
        assert "localparam int unsigned AEM_DMAP_NPORTS_C = 1;" in svh
        assert "AEM_DMAP_PNMAPS_C [0:0] = '{2}" in svh
        assert "AEM_DMAP_PBASE_C [0:0] = '{0}" in svh
        # ... and the TRACKED pair carries the engine IFF ITS OWNER asks for
        # it.  The owner is read from the tree, never assumed (see
        # _check_tracked_dynmap).  Today's owner declares no dynamic port, so
        # this still demands absence - the same bytes, a different question.
        owner_name, owner_dyn = _check_tracked_dynmap(TRACKED_ADP_SVH,
                                                      TRACKED_SVH)
        # a dynamic listener changes the model hash (capability change) and
        # the conditional key keeps every static config's hash untouched
        assert r["overlay"]["entity"] is not None
        print("  [gate 17] dynamic audio map: listeners[0] map_mode dynamic "
              "-> port n_maps=0, input AUDIO_MAP dropped (output renumbered "
              "to 0), svh emits `AEM_DYNMAP keys=8 page=4 nmaps=[2]")
        print(f"  [gate 17] tracked entity definition is owned by "
              f"{owner_name} (read from its own `Source : marker); it "
              f"declares {'a' if owner_dyn else 'NO'} dynamic port, so its "
              f"svh must be `AEM_DYNMAP-{'bearing' if owner_dyn else 'free'} "
              f"- and is")
    finally:
        os.unlink(p)

    # R2 - BOTH directions of the iff, on CANDIDATE pairs in temp dirs.
    # Nothing is installed: --write-rtl is never run and the tree keeps its
    # owner.  A gate that only ever sees a static owner cannot tell "derived
    # from the owner" from "hardcoded absent", which is the whole defect.
    p = _variant(CONFIGS["arty_current"], dyn)
    try:
        with tempfile.TemporaryDirectory() as td:
            dyn_adp, dyn_rom = _dynmap_candidate(p, td)
            sub = os.path.join(td, "static")
            os.makedirs(sub)
            st_adp, st_rom = _dynmap_candidate(CONFIGS["arty_current"], sub)

            # (1) a DYNAMIC owner passes the SAME check with the expectation
            #     FLIPPED to "present".  The old hardcoded negative REJECTED
            #     exactly this - a correct tree, refused for a reason that is
            #     not what the gate is about.
            name, want = _check_tracked_dynmap(dyn_adp, dyn_rom, configs=[p])
            assert want is True, f"{name}: dynamic owner not seen as dynamic"
            assert "AEM_DYNMAP" in open(dyn_rom).read(), (
                "SETUP: the dynamic candidate ROM has no engine to require")
            print(f"  [gate 17] a tracked pair owned by a map_mode-dynamic "
                  f"config passes the SAME check with the expectation "
                  f"FLIPPED to `AEM_DYNMAP PRESENT - the gate follows the "
                  f"owner instead of hardcoding absence")

            # (2) and it still BITES in both directions.  Both mutations are
            #     the realistic failure - a ROM left over from the previous
            #     owner while the shape include already moved.
            _expect_dynmap_rejected(
                "owner declares a dynamic port, tracked ROM has no engine",
                lambda: _check_tracked_dynmap(dyn_adp, st_rom, configs=[p]))
            _expect_dynmap_rejected(
                "owner declares NO dynamic port, tracked ROM carries the "
                "engine",
                lambda: _check_tracked_dynmap(st_adp, dyn_rom))

            # (3) an owner that cannot be resolved must FAIL, not skip: with
            #     no owner there is no expectation to check against.
            ghost = open(st_adp).read().replace(
                "configs/endstation_arty_current.yaml",
                "configs/endstation_ghost.yaml")
            assert ces.svh_source(ghost) == "configs/endstation_ghost.yaml"
            with open(st_adp, "w") as f:
                f.write(ghost)
            _expect_dynmap_rejected(
                "shape include names a config that does not exist",
                lambda: _check_tracked_dynmap(st_adp, st_rom))
    finally:
        os.unlink(p)

    # roadmap 23: Milan v1.2 5.3.3.9 makes dynamic mappings a SHALL on
    # EVERY Stream Port Input, so all N listeners must go dynamic together
    # and the svh must describe each port's own cluster block.
    def dyn_all(c):
        for s in c["streams"]["listeners"]:
            s["map_mode"] = "dynamic"
    p = _variant(CONFIGS["arty_4x4"], dyn_all)
    try:
        r = eb.build(p, OUT)
        ovl = r["overlay"]
        pin = ovl["stream_ports"]["input"]
        assert len(pin) == 4
        assert all(q["maps"] == 0 and q["base_map"] == 0 for q in pin)
        assert [q["base_cluster"] for q in pin] == [0, 4, 8, 12]
        # NO input AUDIO_MAP survives; the 4 talker maps renumber from 0
        assert [m["direction"] for m in ovl["audio_maps"]] == ["output"] * 4
        assert [m["index"] for m in ovl["audio_maps"]] == [0, 1, 2, 3]
        assert ovl["descriptor_counts"]["AUDIO_MAP"] == 4
        check_port_layout(ovl, 4, 4)          # invariants hold when dynamic
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(
                [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
                 "--overlay", r["paths"]["aem_overlay"], "--out-dir", td],
                check=True, capture_output=True)
            svh = open(os.path.join(td, "aecp_aem_rom.svh")).read()
        assert "localparam int unsigned AEM_DMAP_NPORTS_C = 4;" in svh
        # keys span every dynamic port's clusters: 4 ports x 4 = 16
        assert "localparam int unsigned AEM_DMAP_KEYS_C  = 16;" in svh
        assert "AEM_DMAP_PBASE_C [0:3] = '{0, 4, 8, 12}" in svh
        assert "AEM_DMAP_PCLS_C [0:3] = '{4, 4, 4, 4}" in svh
        assert "AEM_DMAP_PDYN_C [0:3] = '{1'b1, 1'b1, 1'b1, 1'b1}" in svh
        # 4 clusters / default page min(4,8)=4 -> ONE partition per port
        assert "localparam int unsigned AEM_DMAP_PAGE_C  = 4;" in svh
        assert "AEM_DMAP_PNMAPS_C [0:3] = '{1, 1, 1, 1}" in svh
        # 4 AAF sinks + the CRF sink: only the AAF ones are mappable
        assert "AEM_DMAP_SAAF_C [0:4] = '{1'b1, 1'b1, 1'b1, 1'b1, 1'b0}" in svh
        assert "AEM_DMAP_SCH_C [0:4] = '{10'd4, 10'd4, 10'd4, 10'd4, 10'd0}" in svh
        print("  [gate 17b] arty_4x4 ALL listeners dynamic (Milan 5.3.3.9): "
              "4 ports n_maps=0, no input AUDIO_MAP, svh keys=16 bases "
              "0/4/8/12, CRF sink flagged unmappable")

        # gate 17c: the AEM refusal and the fabric write gate must agree on
        # WHICH KEYS EXIST, or the model accepts a mapping the crossbar drops
        # (or refuses one it would have taken). AEM_DMAP_PHYS_C is emitted by
        # the codegen; CHMAP_PHYS_C is a milan_datapath localparam; this is
        # the only thing tying the two together.
        m = re.search(r"localparam int unsigned AEM_DMAP_PHYS_C\s*=\s*(\d+);",
                      svh)
        assert m, "svh emits no AEM_DMAP_PHYS_C"
        dp = open(DATAPATH_SV).read()
        d = re.search(r"localparam int CHMAP_PHYS_C\s*=\s*(\d+);", dp)
        assert d, "milan_datapath has no CHMAP_PHYS_C localparam"
        assert int(m.group(1)) == int(d.group(1)), (
            f"AEM_DMAP_PHYS_C {m.group(1)} != milan_datapath CHMAP_PHYS_C "
            f"{d.group(1)}: the AEM refusal and the render-map write gate "
            "would disagree about which cluster keys are reachable")
        # and the write gate itself must be present on BOTH arms, full-width
        assert re.search(r"32'\(aecp_dmap_wr_addr_w\)\s*<\s*CHMAP_PHYS_C", dp), \
            "milan_datapath: AEM arm of the render-map write is not gated"
        assert re.search(r"32'\(cfg_chmap_wr_addr\)\s*<\s*CHMAP_PHYS_C", dp), \
            "milan_datapath: CSR-debug arm of the render-map write is not gated"
        print(f"  [gate 17c] AEM_DMAP_PHYS_C {m.group(1)} == milan_datapath "
              f"CHMAP_PHYS_C {d.group(1)}, and BOTH render-map write arms "
              "(AEM projector + CSR 0x900 debug port) carry the full-width "
              "< CHMAP_PHYS_C gate")
    finally:
        os.unlink(p)

    # unsupported placements are rejected with clear errors
    def dyn_talker(c):
        c["streams"]["talkers"][0]["map_mode"] = "dynamic"
    def dyn_page_static(c):
        c["streams"]["listeners"][0]["map_page"] = 4
    for label, mutate, needle in (
            ("talker dynamic", dyn_talker, "listener stream ports only"),
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
    # one RTL partition constant: two dynamic ports may not DECLARE
    # different map_page values (left unset they resolve to one default)
    def dyn_split_page(c):
        for n, s in enumerate(c["streams"]["listeners"]):
            s["map_mode"] = "dynamic"
            s["map_page"] = 2 if n else 4
    p = _variant(CONFIGS["arty_4x4"], dyn_split_page)
    try:
        try:
            eb.build(p, OUT)
        except eb.ConfigError as e:
            assert "SAME map_page" in str(e), f"split page: got {e}"
        else:
            raise AssertionError("split map_page: accepted")
    finally:
        os.unlink(p)
    print("  [gate 17] reject paths: talker map_mode dynamic, stray "
          "map_page, and disagreeing map_page across dynamic listeners "
          "all raise ConfigError")


MILAN_CSR_SV = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")
LWSRP_PKG_SV = os.path.join(ROOT, "hdl/ieee8021q/srp/lwsrp_pkg.sv")
LWSRP_TOP_SV = os.path.join(ROOT, "hdl/ieee8021q/srp/KL_lwsrp_top.sv")
DATAPATH_SV = os.path.join(ROOT, "hdl/milan/milan_datapath.sv")
PACKETIZER_SV = os.path.join(ROOT, "hdl/ieee1722/aaf/KL_aaf_packetizer.sv")
ETH_PKG_SV = os.path.join(ROOT, "hdl/common/ethernet_packet_pkg.sv")
MILAN_SOC_PY = os.path.join(ROOT, "sw/litex/milan_soc.py")
TRACKED_SRP_SVH = os.path.join(ROOT, "hdl/ieee8021q/srp/gen/lwsrp_table.svh")
TRACKED_CSR_SVH = os.path.join(ROOT, eb.CSR_DEFAULTS_REL)
REGMAP_MD = os.path.join(ROOT, "docs/reference/REGISTER_MAP.md")

#: Everything that compiles hdl/common/csr/milan_csr.sv. Since 11944cd that
#: file `include-s gen/lwsrp_csr_defaults.svh, so each of these must carry
#: hdl/common/csr as an include dir (gate 20a). (path, regex proving it).
CSR_INCDIR_CONSUMERS = (
    ("tb/verilator/csr/Makefile", r"\+incdir\+\$\(RTL_DIR\)/common/csr"),
    ("tb/verilator/milan_dp/Makefile", r"\+incdir\+\$\(RTL_DIR\)/common/csr"),
    ("tb/verilator/hostplane/Makefile", r"\+incdir\+\$\(RTL_DIR\)/common/csr"),
    ("sw/litex/milan_soc.py", r"\"hdl/common/csr\""),
    ("syn/yosys/run.sh", r"-I \$R/hdl/common/csr"),
)

#: Real build trees / sibling repo used by the optional cross-check gates.
#: Absent in a bare container -> those assertions SKIP with a message.
CSR_CSV_2Q = os.path.expanduser(
    "~/litex-milan/work/build_arty_eppo_milanfinal53e/csr.csv")
#: The AX went rx_queues 2 on 2026-07-28 (the D7 fix), so its reference
#: artifact is the FIRST 2-queue build tree - which does not exist until the
#: 8.2 sweep runs. The exists() guard makes this row SKIP until then and BITE
#: from the first build on; the old 1-queue tree
#: (~/milan-avb-multiwork/build_ax8x8_rxq1fix_eppo/csr.csv) must never be
#: compared against a 2-queue config - it would refuse the migration itself.
CSR_CSV_AX2Q = os.path.expanduser(
    "~/milan-avb-multiwork/build_ax8x8_rxq2_eppo/csr.csv")
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


def _svh_localparams(txt):
    """{NAME: int} for every `localparam [W:0] NAME = W'hXXXX_XXXX;` line of a
    generated include (the only form the emitters produce for the scalars)."""
    out = {}
    for m in re.finditer(r"^\s*localparam\s+\[[^\]]+\]\s+(\w+)\s*=\s*"
                         r"\d+'h([0-9A-Fa-f_]+);", txt, re.M):
        out[m.group(1)] = int(m.group(2).replace("_", ""), 16)
    return out


def test_lwsrp_reset_words_match_rtl():
    """Gate 18a: the emitted 0x680 reset words are the words milan_csr.sv
    actually elaborates. Since the RTL `include-s the GENERATED header there
    is no second hand-written copy left to compare against, so the chain the
    gate walks is: emitted word -> the LWSRP_*_RST_C symbol in the tracked
    hdl/common/csr/gen/lwsrp_csr_defaults.svh -> the symbol milan_csr's reset
    block assigns -> the symbol its csr_default readback table returns -> the
    REGISTER_MAP Reset column. Every link must name the SAME constant, so a
    hand edit anywhere still fails here."""
    csr = open(MILAN_CSR_SV).read()
    reg = open(REGMAP_MD).read()
    r = eb.build(CONFIGS["arty_current"], OUT)
    got = r["lwsrp"]["reset_words"]
    hdr = _svh_localparams(open(TRACKED_CSR_SVH).read())
    # (emitter name, milan_csr storage reg, milan_csr A_* enum, doc reset)
    rows = [("LWSRP_CTRL", "lwsrp_ctrl", "A_LWSRP_CTRL", "0x10"),
            ("LWSRP_VID", "lwsrp_vid", "A_LWSRP_VID", "2"),
            ("LWSRP_DMAC_LO", "lwsrp_dmlo", "A_LWSRP_DMLO", "0xF000_FE01"),
            ("LWSRP_DMAC_HI", "lwsrp_dmhi", "A_LWSRP_DMHI", "0x91E0"),
            ("LWSRP_TSPEC", "lwsrp_tspec", "A_LWSRP_TSPEC", "0x0001_00E0"),
            ("LWSRP_LATENCY", "lwsrp_lat", None, "0")]
    for name, storage, enum, doc in rows:
        sym = name + "_RST_C"
        assert sym in hdr, f"{sym} missing from {eb.CSR_DEFAULTS_REL}"
        want = hdr[sym]
        assert int(got[name], 16) == want, (
            f"{name}: emitted {got[name]} != the tracked header's 0x{want:08X} "
            f"- regenerate {eb.CSR_DEFAULTS_REL}")
        # the reset block must ASSIGN the generated symbol, never a literal
        assert re.search(rf"{storage}\s*<=\s*{sym};", csr), (
            f"milan_csr reset block no longer assigns {storage} <= {sym} - "
            f"the CSR block has stopped consuming the generated header")
        if enum:
            assert re.search(rf"{enum}\[10:0\]:\s*csr_default = {sym};", csr), \
                f"milan_csr csr_default {enum} no longer returns {sym}"
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
    print(f"  [gate 18a] arty_current lwSRP reset words == the generated "
          f"{os.path.basename(TRACKED_CSR_SVH)} == the symbols milan_csr's "
          f"reset block and csr_default table use == the REGISTER_MAP Reset "
          f"column ({len(rows)} registers, {len(eb.SRP_CSR_OFFSETS)} offsets)")


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
    # milan_csr's literal duplicate is GONE: it drives o_srp_ctx_prio_rank from
    # the generated LWSRP_PRIO_RANK_C, so the chain is emitter -> header -> RTL.
    hdr = _svh_localparams(open(TRACKED_CSR_SVH).read())
    assert pr == hdr["LWSRP_PRIO_RANK_C"], \
        "PriorityAndRank: emitter vs the generated CSR header"
    assert re.search(r"assign o_srp_ctx_prio_rank\s*=\s*LWSRP_PRIO_RANK_C;",
                     csr), \
        "milan_csr no longer drives o_srp_ctx_prio_rank from the generated " \
        "LWSRP_PRIO_RANK_C"
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
                   "LWSRP_CTRL_RST_C      = 32'h0000_0010;",
                   "LWSRP_TSPEC_RST_C     = 32'h0001_00E0;"):
        assert needle in svh, f"tracked svh lacks {needle!r}"
    print(f"  [gate 18b] {len(checks)} SR-class/timer/bandwidth constants == "
          "lwsrp_pkg.sv, PriorityAndRank == the generated symbol milan_csr "
          "drives, bw_gate 75% ceilings agree; tracked lwsrp_table.svh "
          "regenerates byte-identically")


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
                     r"\s*\.N_CTX_P\(SRP_CTX_ROWS_C\),"
                     r"\s*\.N_LISTENERS_P\(N_STREAMS\),"
                     r"\s*\.N_TALKERS_P\(SRP_TALKERS_C\)\)", dp), \
        "milan_datapath no longer sizes the ctx table at L+T-1"
    # ...and T includes the CRF Media Clock Output's own talker row when the
    # shape has one (Milan v1.2 7.3.3: the media clock stream is an SR class
    # A reservation like any other stream, not an un-declared side channel)
    assert re.search(r"localparam int SRP_TALKERS_C\s*=\s*"
                     r"N_STREAMS \+ SRP_CRF_TK_C;", dp), \
        "milan_datapath no longer counts the CRF output as a talker row"
    assert re.search(r"localparam int SRP_CTX_ROWS_C\s*=\s*"
                     r"N_STREAMS \+ SRP_TALKERS_C - 1;", dp), \
        "milan_datapath ctx rows are no longer L+T-1"
    assert re.search(r"KL_lwsrp_bw_gate #\(\.N_STREAMS_P\(N_TALKERS_P\)\)", top), \
        "KL_lwsrp_top no longer ties the bw_gate width to N_TALKERS_P"
    nq = _sv_int(epkg, r"NUMBER_OF_QUEUES\s*=\s*(\d+);", "ethernet_packet_pkg")
    for name, (L, T) in (("arty_current", (1, 1)), ("arty_4x4", (4, 4)),
                         ("ax7101_8x8", (8, 8))):
        r = eb.build(CONFIGS[name], OUT)
        t, cfg = r["lwsrp"], r["cfg"]
        mp = t["module_params"]
        # attribute rows = L + T - 1, where T counts the CRF Media Clock
        # Output's own talker row (Milan v1.2 7.3.3) when the shape has one
        crf_tk = 1 if cfg["clocking"]["crf_output"] else 0
        n_tk = max(L, T) + crf_tk
        assert mp["KL_lwsrp_top.N_TALKERS_P"] == n_tk, \
            "the CRF Media Clock Output must own a talker attribute row"
        assert mp["KL_lwsrp_top.N_CTX_P"] == max(L, T) + n_tk - 1 \
            >= L + T - 1, \
            "ctx rows must cover every listener AND talker attribute row"
        # ctx_idx_i is 4 bits: 16 rows is the hard ceiling, and 8x8 with a
        # CRF output lands EXACTLY on it
        assert mp["KL_lwsrp_top.N_CTX_P"] <= 2 ** eb.SRP_CTX_IDX_BITS, \
            f"{name}: {mp['KL_lwsrp_top.N_CTX_P']} rows exceed the " \
            f"{eb.SRP_CTX_IDX_BITS}-bit ctx index"
        assert max(L, T) == mp["milan_datapath.N_STREAMS"]
        assert mp["KL_lwsrp_bw_gate.N_STREAMS_P"] == \
            mp["KL_lwsrp_top.N_TALKERS_P"], \
            "the bw-gate must budget the CRF stream's slope too"
        assert mp["KL_lwsrp_top.CLK_FREQ_HZ_P"] == \
            cfg["constraints"]["milan_clk_hz"] == \
            mp["milan_datapath.MILAN_CLK_FREQ_HZ"]
        assert mp["milan_csr.N_LISTENERS_P"] == L
        assert mp["milan_csr.N_TALKERS_P"] == T
        assert mp["milan_csr.NUM_QUEUES"] == nq, \
            f"{name}: num_queues != ethernet_packet_pkg NUMBER_OF_QUEUES {nq}"
        # the class-A queue must be a real queue
        assert 0 <= cfg["srp"]["class_queue"] < nq
        # T counts the CRF Media Clock Output's talker row too (2026-07-28)
        assert t["ctx_rows"]["required"] == L + T + crf_tk - 1
        # the shortfall closed 2026-07-26: the datapath sizes the table at
        # 2*N_STREAMS-1, so every listener AND talker attribute row is backed
        assert t["ctx_rows"]["available"] == 2 * max(L, T) - 1 + crf_tk
        assert t["ctx_rows"]["available"] >= t["ctx_rows"]["required"], \
            "lwSRP ctx table must back every row the 0x800 window can select"
        b = t["bandwidth"]
        assert b["total_idle_slope_bps"] <= b["limit_bps"]
        # the CRF media clock reserves class A bandwidth like any stream
        # (Milan v1.2 7.3.3) and the bw-gate sums it into the same Sigma, so
        # the static total must carry it - a shape that only fits WITHOUT its
        # mandatory media clock does not fit
        assert b["crf_idle_slope_bps"] == (
            eb.srp_idle_slope_bps(eb.CRF_SRP_MAXFRAME_B, 1, 8000)
            if crf_tk else 0), "the CRF class A slope is not accounted"
        assert b["total_idle_slope_bps"] == b["crf_idle_slope_bps"] + sum(
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
    # the NxN row shortfall CLOSED 2026-07-26 (datapath sizes the ctx table at
    # 2*N_STREAMS-1). The mark must now read `supported` for every shape - if a
    # future change reopens the shortfall the mark flips back to `planned`,
    # which this asserts against, so the regression cannot be silent.
    for name in ("arty_current", "arty_4x4", "ax7101_8x8"):
        marks = eb.build(CONFIGS[name], OUT)["marks"]
        row_marks = [m for m in marks if "lwSRP attribute row" in m[0]]
        assert row_marks, f"{name}: ctx rows not marked at all"
        assert all(m[1] == "supported" for m in row_marks), \
            f"{name}: ctx-row shortfall reopened -> {row_marks}"
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
        ("queue 8 (3-bit field)",
         lambda c: c["srp"].__setitem__("class_queue", 8), "LWSRP_CTRL[4:2]"),
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
    # over-subscription. Since the TSpec follows the WIRE (802.1Q 35.2.2.8.4
    # a) - the frame the talker WILL PRODUCE), a fat DECLARATION no longer
    # inflates the reservation: the old 32ch mutation derives the producible
    # 8ch MSDU and lands under the ceiling, which is the tie working, not
    # the gate failing. Real over-subscription is COUNT x wire MSDU: eight
    # 8-channel talkers on the 100 Mb/s arty port = 8 x (216+42) x 8 x 8000
    # = 132 Mb/s against the 75 Mb/s class-A ceiling.
    def fat(c):
        base = dict(c["streams"]["talkers"][0])
        base["channels"] = 8
        base["formats"] = ["0x0205022002006000"]
        c["streams"]["talkers"] = [
            dict(base, name=f"Fat Out {i}") for i in range(8)]
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
                          (CSR_CSV_AX2Q, "ax7101_8x8")):
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
    # sweep.sh set 1 for both boards while the deployed arty carries 2).
    # The AX went to rx_queues 2 on 2026-07-28 (the D7 fix), so its refused
    # flip is now DOWN to 1 - same defect shape, opposite direction.
    for cfg_name, flip in (("arty_current", 1), ("ax7101_8x8", 1)):
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


def test_csr_defaults_header_consumed():
    """Gate 20a: the RTL CONSUMES the generated header - the loop is closed.

    Up to 11944cd the emitters only *compared* against milan_csr.sv's
    hand-written 0x680 literals; the generated .svh was included by no RTL, so
    the two could still be edited apart. milan_csr.sv now `include-s
    hdl/common/csr/gen/lwsrp_csr_defaults.svh, which makes the config the only
    source of those words. This gate asserts, in order:
      1. the tracked header regenerates BYTE-IDENTICALLY (staleness);
      2. milan_csr.sv carries the `include, with the path spelled exactly as
         the emitter documents it;
      3. every emitted value equals the FROZEN pre-switch literal, i.e. the
         switch was a refactor with zero functional change (a config edit that
         would move a deployed reset word fails HERE, loudly, instead of
         silently re-elaborating the CSR block);
      4. no hand-written 0x680 literal survives in milan_csr.sv;
      5. the CSR subset agrees word-for-word with the full lwSRP table
         (hdl/ieee8021q/srp/gen/lwsrp_table.svh) - one config, one pass;
      6. every build/sim/synth flow that compiles milan_csr.sv carries
         hdl/common/csr as an include dir, so the `include always resolves
         (Verilator searches -I/+incdir and the CWD only, NEVER the including
         file's directory)."""
    r = eb.build(CONFIGS["arty_current"], OUT)
    csr = open(MILAN_CSR_SV).read()
    # 1. staleness
    assert open(TRACKED_CSR_SVH).read() == r["csr_defaults_svh"], \
        f"{eb.CSR_DEFAULTS_REL} is STALE - regenerate it"
    # 2. the include, exactly as the emitter documents it
    inc = f'`include "{eb.CSR_DEFAULTS_INCLUDE}"'
    assert inc in csr, f"milan_csr.sv does not {inc}"
    # 3. byte-identical behaviour: emitted == the frozen pre-switch literals
    got = {k: int(v, 16) for k, v in r["lwsrp"]["reset_words"].items()}
    assert got == eb.SRP_FROZEN_RESETS, (
        "the deployed 0x680 reset words MOVED: "
        + ", ".join(f"{k} 0x{got[k]:08X} != 0x{v:08X}"
                    for k, v in eb.SRP_FROZEN_RESETS.items() if got[k] != v))
    hdr = _svh_localparams(open(TRACKED_CSR_SVH).read())
    for k, v in eb.SRP_FROZEN_RESETS.items():
        assert hdr[k + "_RST_C"] == v, f"{k}_RST_C != the frozen 0x{v:08X}"
    assert hdr["LWSRP_PRIO_RANK_C"] == eb.SRP_FROZEN_PRIO_RANK
    # 4. no hand-written literal left behind
    for storage in ("lwsrp_ctrl", "lwsrp_vid", "lwsrp_dmlo", "lwsrp_dmhi",
                    "lwsrp_tspec", "lwsrp_lat"):
        assert not re.search(rf"{storage}\s*<=\s*\d+'h", csr), \
            f"milan_csr.sv still resets {storage} from a LITERAL"
    assert not re.search(r"A_LWSRP_\w+\[10:0\]:\s*csr_default = \d+'h", csr), \
        "milan_csr.sv csr_default still returns a LITERAL for a 0x680 register"
    assert "SRP_PRIO_RANK_C = 8'h" not in csr, \
        "milan_csr.sv still declares its own PriorityAndRank literal"
    # 5. the subset agrees with the full table
    tbl = _svh_localparams(open(TRACKED_SRP_SVH).read())
    shared = sorted(set(hdr) & set(tbl))
    assert len(shared) == len(hdr), \
        f"CSR header carries constants the lwSRP table does not: " \
        f"{sorted(set(hdr) - set(tbl))}"
    for k in shared:
        assert hdr[k] == tbl[k], (
            f"{k}: CSR header 0x{hdr[k]:X} != lwsrp_table.svh 0x{tbl[k]:X} - "
            "the two generated headers have drifted")
    # 6. every consumer can resolve the include
    for rel, pat in CSR_INCDIR_CONSUMERS:
        p = os.path.join(ROOT, rel)
        assert os.path.exists(p), f"{rel} is gone - is it still building?"
        txt = open(p).read()
        assert "milan_csr" in txt, f"{rel} no longer names milan_csr"
        assert re.search(pat, txt), (
            f"{rel} compiles milan_csr.sv but has no hdl/common/csr include "
            f"dir - `include \"{eb.CSR_DEFAULTS_INCLUDE}\" cannot resolve")
    print(f"  [gate 20a] milan_csr.sv `include-s {eb.CSR_DEFAULTS_INCLUDE}; "
          f"{len(eb.SRP_FROZEN_RESETS)} reset words + PriorityAndRank == the "
          f"FROZEN literals (LWSRP_CTRL moved TWICE for the queue map: "
          f"0x0C -> 0x14 at 6 queues, 0x14 -> 0x10 at 5), 0 literals "
          f"left in the RTL, {len(shared)} constants agree with "
          f"lwsrp_table.svh, {len(CSR_INCDIR_CONSUMERS)} consumers carry the "
          f"include dir")


def test_csr_defaults_rejects():
    """Gate 20b: a config that would emit a MALFORMED header - one milan_csr
    would silently compile into the wrong reset word - raises ConfigError.

    LWSRP_CTRL[0]/[1] are single bits: `talker_declare_at_reset: 2` used to
    emit 2 << 1 = 0b100, i.e. it quietly rewrote class_queue[0] and shipped."""
    cases = [
        ("enable_at_reset: 'yes' (string)",
         lambda c: c["srp"].__setitem__("enable_at_reset", "yes"),
         "must be a boolean"),
        ("talker_declare_at_reset: 2 (shifts into class_queue)",
         lambda c: c["srp"].__setitem__("talker_declare_at_reset", 2),
         "shifts into class_queue"),
        ("rtl_table: 'true' (string)",
         lambda c: c["srp"].__setitem__("rtl_table", "true"),
         eb.CSR_DEFAULTS_REL),
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
    # and the emitted LWSRP_CTRL word really is bit-exact for the legal shape
    def enable(c):
        c["srp"]["enable_at_reset"] = True
        c["srp"]["talker_declare_at_reset"] = True
    p = _variant(CONFIGS["arty_current"], enable)
    try:
        cfg = eb.load_config(p)
        w = eb.srp_reset_words(cfg)["LWSRP_CTRL"]
        assert w == 0x00000013, f"LWSRP_CTRL {w:#010x} != 0x00000013"
    finally:
        os.unlink(p)
    print(f"  [gate 20b] {len(cases)}/{len(cases)} malformed LWSRP_CTRL "
          "sources rejected with ConfigError; en+talker+q4 emits 0x00000013")


AES3_RX_SV = os.path.join(ROOT, "hdl/ieee1722/aaf/KL_aes3_rx.sv")
AES3_TX_SV = os.path.join(ROOT, "hdl/ieee1722/aaf/KL_aes3_tx.sv")
AES3_TB_MK = os.path.join(ROOT, "tb/verilator/aes3/Makefile")


def _sv_param_default(txt, name):
    """Default of `parameter [type] NAME = <value>` in an SV module header."""
    m = re.search(rf"parameter\s+(?:bit|int\s+unsigned|int)\s+{name}\s*=\s*"
                  r"(?:1'b)?([0-9_]+)", txt)
    assert m, f"no parameter {name} in the RTL"
    return int(m.group(1).replace("_", ""))


def test_aes3_interface_switch():
    """Gate 21a: `audio_interface.kind: aes3|spdif` is a REAL switch now.

    One core (KL_aes3_rx / KL_aes3_tx) carries both transports, so the config
    has to pick the parameters - and the parameters it picks must be the ones
    the RTL actually declares. Everything here is parsed out of the RTL at
    test time: the parameter names, the defaults the emitter reuses
    (OVERSAMPLE_P, LOCK_BLOCKS_P), the CONSUMER_P dialect split, and the
    serial-clock arithmetic the transport forces."""
    rx = open(AES3_RX_SV).read()
    tx = open(AES3_TX_SV).read()
    # the parameters the emitter names must EXIST on the modules it names
    for p in ("CONSUMER_P", "WORD_BITS_P", "LOCK_BLOCKS_P"):
        assert re.search(rf"parameter\s+\S+.*?\b{p}\b", rx), f"{p} not on the rx"
    for p in ("CONSUMER_P", "WORD_BITS_P", "OVERSAMPLE_P"):
        assert re.search(rf"parameter\s+\S+.*?\b{p}\b", tx), f"{p} not on the tx"
    assert eb.AES3_OVERSAMPLE == _sv_param_default(tx, "OVERSAMPLE_P")
    assert eb.AES3_LOCK_BLOCKS == _sv_param_default(rx, "LOCK_BLOCKS_P")
    # the transport's own arithmetic, stated in both places
    assert re.search(r"BLOCK_FRAMES_C\s*=\s*(\d+)", rx).group(1) == \
        str(eb.AES3_BLOCK_FRAMES)
    assert re.search(r"BLOCK_FRAMES_C\s*=\s*(\d+)", tx).group(1) == \
        str(eb.AES3_BLOCK_FRAMES)
    # the suite the mark points at must exist and compile these two modules
    mk = open(AES3_TB_MK).read()
    for m in (eb.AES3_RX_MODULE, eb.AES3_TX_MODULE):
        assert f"{m}.sv" in mk, f"tb/verilator/aes3 does not build {m}"
    seen = []
    for kind, consumer in (("aes3", 0), ("spdif", 1)):
        for wl in (16, 20, 24):
            def mutate(c, k=kind, w=wl):
                c["audio_interface"]["kind"] = k
                c["audio_interface"]["word_length_bits"] = w
            v = _variant(CONFIGS["arty_current"], mutate)
            try:
                r = eb.build(v, OUT)
            finally:
                os.unlink(v)
            ip = r["interface_params"]
            assert ip["family"] == "aes3" and ip["kind"] == kind
            assert ip["rx_module"] == eb.AES3_RX_MODULE
            assert ip["tx_module"] == eb.AES3_TX_MODULE
            # THE switch: one core, two dialects, chosen by the config
            assert ip["params"]["CONSUMER_P"] == consumer, \
                f"{kind}: CONSUMER_P {ip['params']['CONSUMER_P']} != {consumer}"
            assert ip["params"]["WORD_BITS_P"] == wl
            # serial clock = rate x 128 UI/frame x oversample, an exact
            # integer divide of the audio PLL
            rate = r["cfg"]["clocking"]["sampling_rate_hz"]
            pll = r["cfg"]["clocking"]["audio_pll_hz"]
            assert ip["serial_clk_hz"] == rate * eb.AES3_UI_PER_FRAME \
                * eb.AES3_OVERSAMPLE
            assert ip["serial_clk_div"] * ip["serial_clk_hz"] == pll
            assert f"`WORD_BITS_P={wl}`" in r["plan"]
            assert f"{ip['serial_clk_hz']} Hz" in r["plan"]
            seen.append((kind, wl))
    # the kinds that take no ser/des parameters must emit nothing at all
    for name in CONFIGS:
        assert eb.build(CONFIGS[name], OUT)["interface_params"] is None, \
            f"{name}: a non-biphase interface emitted ser/des parameters"
    print(f"  [gate 21a] {len(seen)} aes3/spdif shapes: one core, CONSUMER_P "
          f"picks the dialect, WORD_BITS_P 16/20/24, serial clock "
          f"{eb.AES3_UI_PER_FRAME}x{eb.AES3_OVERSAMPLE}x rate = an exact PLL "
          f"divide; RTL defaults (OVERSAMPLE_P={eb.AES3_OVERSAMPLE}, "
          f"LOCK_BLOCKS_P={eb.AES3_LOCK_BLOCKS}, {eb.AES3_BLOCK_FRAMES} "
          f"frames/block) parsed from the modules themselves")


def test_aes3_rejects():
    """Gate 21b: an AES3/S-PDIF shape the RTL could not actually clock, or a
    word length the transport cannot carry, raises ConfigError - it is never
    emitted as a ser/des that would transmit at the wrong rate."""
    cases = [
        ("word_length_bits 32 (AES3 subframe is 24 bits max)",
         lambda c: (c["audio_interface"].__setitem__("kind", "aes3"),
                    c["audio_interface"].__setitem__("word_length_bits", 32)),
         "word_length_bits 32 invalid for aes3"),
        ("audio PLL cannot divide to the serial clock",
         lambda c: (c["audio_interface"].__setitem__("kind", "spdif"),
                    c["clocking"].__setitem__("audio_pll_hz", 25_000_000)),
         "not an integer divide"),
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
    # the shipping 24.576 MHz PLL DOES carry 48 kHz AES3 (divide by 1)
    p = _variant(CONFIGS["arty_current"],
                 lambda c: c["audio_interface"].__setitem__("kind", "aes3"))
    try:
        cfg = eb.load_config(p)
        assert cfg["interface"]["serial_clk_hz"] == 24_576_000
        assert cfg["interface"]["serial_clk_div"] == 1
    finally:
        os.unlink(p)
    print(f"  [gate 21b] {len(cases)}/{len(cases)} unclockable AES3 shapes "
          "rejected with ConfigError; 48 kHz AES3 rides the shipping "
          "24.576 MHz audio PLL exactly (divide 1)")


# ---------------------------------------------------------------------------
#  Gate 22 - the CBS reset slope/credit table has FOUR copies and they must
#  agree. It is hand-written in two places in the RTL and re-tabulated in two
#  markdown pages; a hand-maintained table is a future contradiction, so pin
#  every copy against ethernet_packet_pkg (the single source of truth) here.
#
#    ethernet_packet_pkg::IDLE_SLOPE_1G / IDLE_SLOPE_100M / NUMBER_OF_QUEUES
#      -> milan_csr::CBS_IDLE_RST / CBS_HI_RST / CBS_LO_RST / CBS_EN_RST
#      -> docs/reference/REGISTER_MAP.md      section 0x400 table
#      -> docs/reference/EGRESS_QUEUE_MAP.md  "CBS reset slopes" table
#
#  hi/lo credit are RE-DERIVED here from the slopes with the package's own
#  calc_hi_credit/calc_lo_credit arithmetic (MAX_FRAME_SIZE 1522, trunc toward
#  zero), so a slope edit that forgets its credits fails even if all four
#  copies were edited consistently-but-wrongly.
# ---------------------------------------------------------------------------
EPKG_SV = os.path.join(ROOT, "hdl/common/ethernet_packet_pkg.sv")
EGRESS_MD = os.path.join(ROOT, "docs/reference/EGRESS_QUEUE_MAP.md")
MAX_FRAME_SIZE = 1522
PORT_RATE_1G = 1_000_000_000


def _sv_int_array(txt, name, label):
    """Elements of `parameter/localparam int NAME [0:k] = '{a, b, ...};`."""
    m = re.search(rf"{name}\s*\[0:[^\]]*\]\s*=\s*'\{{(.*?)\}}\s*;", txt, re.S)
    assert m, f"{label}: no array {name}"
    # strip trailing // comments FIRST - they contain commas ("45 %, CBS ...")
    body = "\n".join(re.sub(r"//.*", "", ln) for ln in m.group(1).splitlines())
    out = []
    for tok in body.split(","):
        tok = tok.strip().replace("_", "")
        if not tok:
            continue
        assert re.fullmatch(r"-?\d+", tok), f"{label}: {name} element {tok!r}"
        out.append(int(tok))
    return out


def _md_table_ints(md, header_re, ncols):
    """Rows of the first markdown table whose header line matches header_re."""
    lines = md.splitlines()
    for i, ln in enumerate(lines):
        if re.search(header_re, ln):
            rows, j = [], i + 2          # skip the |---|---| separator
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                if len(cells) == ncols:
                    rows.append(cells)
                j += 1
            return rows
    assert False, f"no markdown table matching {header_re}"


def _num(cell):
    """First signed integer in a markdown cell (handles the U+2212 minus)."""
    t = cell.replace("\u2212", "-").replace(",", "").replace("_", "")
    m = re.search(r"-?\d+", t)
    assert m, f"no number in {cell!r}"
    return int(m.group(0))


def test_cbs_reset_table_single_source():
    epkg = open(EPKG_SV).read()
    csr = open(MILAN_CSR_SV).read()
    reg = open(REGMAP_MD).read()
    egr = open(EGRESS_MD).read()

    nq = _sv_int(epkg, r"NUMBER_OF_QUEUES\s*=\s*(\d+);", "ethernet_packet_pkg")
    s1g = _sv_int_array(epkg, "IDLE_SLOPE_1G", "ethernet_packet_pkg")
    s100 = _sv_int_array(epkg, "IDLE_SLOPE_100M", "ethernet_packet_pkg")
    assert len(s1g) == len(s100) == nq, (
        f"IDLE_SLOPE_1G/100M have {len(s1g)}/{len(s100)} entries, "
        f"NUMBER_OF_QUEUES is {nq}")

    # 802.1Q-2018 34.3.1 / REQ-CBS-03: the ceiling is 75 %, at BOTH link rates,
    # and class A must outrank class B in bandwidth as well as in queue order.
    assert sum(s1g) <= 0.75 * PORT_RATE_1G, f"sum(IDLE_SLOPE_1G) {sum(s1g)} > 75 %"
    assert sum(s100) <= 0.75 * PORT_RATE_1G / 10, f"sum(IDLE_SLOPE_100M) {sum(s100)} > 75 %"
    assert all(a == b * 10 for a, b in zip(s1g, s100)), \
        "IDLE_SLOPE_100M is not IDLE_SLOPE_1G/10 - the two rate tables disagree"
    assert s1g[nq - 1] > s1g[nq - 2], \
        "class A (top queue) slope must exceed class B (the one below it)"

    # milan_csr's reset arrays must BE the package tables, and its credits must
    # be the package's calc_hi/lo_credit of those slopes.
    ci = _sv_int_array(csr, "CBS_IDLE_RST", "milan_csr")
    ch = _sv_int_array(csr, "CBS_HI_RST", "milan_csr")
    cl = _sv_int_array(csr, "CBS_LO_RST", "milan_csr")
    assert ci == s1g, f"milan_csr CBS_IDLE_RST {ci} != ethernet_packet_pkg {s1g}"
    want_hi = [MAX_FRAME_SIZE * s // PORT_RATE_1G for s in s1g]
    want_lo = [-((MAX_FRAME_SIZE * (PORT_RATE_1G - s)) // PORT_RATE_1G) for s in s1g]
    assert ch == want_hi, f"CBS_HI_RST {ch} != calc_hi_credit {want_hi}"
    assert cl == want_lo, f"CBS_LO_RST {cl} != calc_lo_credit {want_lo}"

    # REQ-CBS-02 / CBS_DEFAULT_SHAPING_BUG.md: EVERY queue powers up UNSHAPED.
    # Shaping q0 at reset once paced all best-effort TX to ~250 Mbit/s on
    # silicon (2026-07-07), so this is a standing invariant, not a default.
    m = re.search(r"CBS_EN_RST\s*=\s*(\d+)'b([01]+)\s*;", csr)
    assert m, "milan_csr: no CBS_EN_RST"
    assert int(m.group(1)) == nq, f"CBS_EN_RST is {m.group(1)} bits, want {nq}"
    assert set(m.group(2)) == {"0"}, \
        f"CBS_EN_RST {m.group(2)} shapes a queue at reset (REQ-CBS-02)"

    # Both markdown tables, row by row, highest queue first.
    reg_rows = _md_table_ints(reg, r"\|\s*q\s*\|\s*class\s*\|\s*idleSlope", 7)
    assert len(reg_rows) == nq, f"REGISTER_MAP 0x400 table has {len(reg_rows)} rows, want {nq}"
    for r in reg_rows:
        q = _num(r[0])
        assert _num(r[2]) * 1_000_000 == s1g[q], f"REGISTER_MAP q{q} idleSlope"
        assert _num(r[4]) == want_hi[q], f"REGISTER_MAP q{q} hiCredit"
        assert _num(r[5]) == want_lo[q], f"REGISTER_MAP q{q} loCredit"
        assert _num(r[6]) == 0, f"REGISTER_MAP q{q} shaped-at-reset must be 0"

    egr_rows = _md_table_ints(egr, r"\|\s*Queue\s*\|\s*idleSlope @ 1 Gb/s", 5)
    assert len(egr_rows) == nq, f"EGRESS_QUEUE_MAP slope table has {len(egr_rows)} rows, want {nq}"
    for r in egr_rows:
        q = _num(r[0])
        assert _num(r[1]) * 1_000_000 == s1g[q], f"EGRESS_QUEUE_MAP q{q} idleSlope"
        assert _num(r[3]) == want_hi[q], f"EGRESS_QUEUE_MAP q{q} hiCredit"
        assert _num(r[4]) == want_lo[q], f"EGRESS_QUEUE_MAP q{q} loCredit"

    print(f"  [gate 22] CBS reset table single-sourced: {nq} queues, "
          f"sum(IDLE_SLOPE_1G) = {sum(s1g)/1e6:.0f} Mb/s "
          f"({sum(s1g)/PORT_RATE_1G*100:.1f} % <= 75 %), SR A+B = "
          f"{(s1g[nq-1]+s1g[nq-2])/1e6:.0f} Mb/s; milan_csr CBS_*_RST == the "
          f"package (credits re-derived, not copied), CBS_EN_RST = {nq}'b"
          f"{'0'*nq}, and both REGISTER_MAP 0x400 and EGRESS_QUEUE_MAP agree "
          f"row for row")


def _prune(cfg, **feats):
    """board.features mutation helper for the tier-1 prune gates."""
    cfg.setdefault("board", {}).setdefault("features", {}).update(feats)


def test_optional_blocks_default_present():
    """gate 23a - rule 1 (default PRESENT) enforced, not asserted: a block is
    pruned ONLY where a config says so in as many words.

    Not "no prune flag ever". `ax7101_8x8` deliberately SPENDS one - it
    declares `board.constraints.render_lpf: false`, the only Vivado-priced
    lever of the 2026-07-27 area round - and a gate that forbade every prune
    flag would have made that spend unlandable. What must hold is that the
    emitted flags are EXACTLY the declared ones, so an undeclared prune (the
    real hazard: a block silently vanishing from a shipping build) still
    fails."""
    # The prunes each shipped config declares IN AS MANY WORDS. Pinned here
    # so an edit that prunes (or restores) a block on a shipping board must
    # ALSO state that intent in this gate - two files or it didn't happen.
    # ax7101_8x8's three: render_lpf (07-27, the Vivado-priced 428-LUT
    # lever) + latency_taps + i2s_playback (07-28, the DRC UTLZ-1 round -
    # 66,290 LUT vs 63,400 sites once the 0x0019 compliance fabric landed;
    # both "dead when" levers on a board with no DAC pads). The Arty ships
    # every block, INCLUDING the taps the AX gave up (item-11 telemetry
    # lives on the board with the analog loop).
    SHIPPED_PRUNES = {
        "arty_current": set(),
        "arty_4x4": set(),
        "ax7101_8x8": {"latency_taps", "i2s_playback", "render_lpf",
                       "datapath_probes"},
    }
    for name in ("arty_current", "arty_4x4", "ax7101_8x8"):
        r = eb.build(CONFIGS[name], OUT)
        cfg = eb.load_config(CONFIGS[name])
        declared_keys = {key for key in eb.OPTIONAL_BLOCKS
                         if not cfg["features"].get(key, True)
                         or not cfg.get("constraints", {}).get(key, True)}
        assert declared_keys == SHIPPED_PRUNES[name], (
            f"{name}: config declares prunes {sorted(declared_keys)}, this "
            f"gate expects {sorted(SHIPPED_PRUNES[name])} - a shipping "
            f"board's block posture changed without changing the gate")
        declared = {eb.OPTIONAL_BLOCKS[k][0] for k in declared_keys}
        emitted = {f for f, _p, _w in eb.OPTIONAL_BLOCKS.values()} & set(r["argv"])
        assert emitted == declared, (
            f"{name}: argv prune flags {sorted(emitted)} do not match what the "
            f"config declares {sorted(declared)} - a block is being pruned "
            f"(or kept) that nothing asked for")
        rows = dict(eb.resource_instances(cfg, r["overlay"]))
        # a subtractive row is counted only where that block is declared pruned
        for k in ("media_clock_servo", "latency_taps", "render_lpf"):
            want = 1 if eb.OPTIONAL_BLOCKS[k][0] in declared else 0
            assert rows[f"prune_{k}"] == want, \
                f"{name}: prune_{k} row is {rows[f'prune_{k}']}, expected {want}"
        # ...and the blocks that have POSITIVE rows are charged for exactly
        # when present, i.e. pruning does not quietly stop (or keep) counting
        want_i2s = 0 if "i2s_playback" in declared_keys else 1
        assert rows["rx_filter"] == 1 and rows["maap_claim_ctx"] == 1 and \
            rows["i2s_renderer"] == want_i2s, \
            f"{name}: a block's estimate row disagrees with its declared posture"
        if declared_keys:
            for k in declared_keys:
                assert f"`{k}`" in r["plan"], \
                    f"{name}: build plan must list the `{k}` prune"
            assert "ALL PRESENT" not in r["plan"]
        else:
            assert "ALL PRESENT" in r["plan"], \
                f"{name}: build plan must state the optional-block posture"
    # ...and the argv gate 2 above already pins arty/ax7101 byte-for-byte
    # against sweep.sh, so this gate's declared==emitted plus gate 2's
    # argv==sweep.sh closes the loop: fragment, argv, plan and config all
    # name the same prunes.
    print(f"  [gate 23a] 3 shipped configs: prune posture == the declared "
          f"table exactly (arty_current/arty_4x4 ALL PRESENT; ax7101_8x8 "
          f"spends render_lpf + latency_taps + i2s_playback), argv flags == "
          f"declared prunes, and every estimate row follows its block's "
          f"declared posture")


def test_optional_block_gates_bite():
    """gate 23b - THE GATE (AREA_BUDGET rule 5). Each case is a config that
    asks for a feature the prune removed; every one must raise ConfigError.
    The paired POSITIVE case proves the same prune is ACCEPTED once the
    config stops asking - otherwise the gate would just be a ban."""
    cases = [
        # (label, feature(s) pruned, extra mutation, must-raise?)
        ("servo pruned but CRF/input-stream clocking offered",
         dict(media_clock_servo=False), lambda c: None, True),
        ("servo pruned, internal-only clocking",
         dict(media_clock_servo=False),
         # crf_output STAYS on: emitting a CRF stream from the INTERNAL
         # clock (Milan 7.2.3, mandatory at >=2 listeners) is KL_crf_tx and
         # needs no servo - the servo is the SINK-side actuator.
         lambda c: c["clocking"].update(media_clock_sources=["internal"],
                                        default_source="internal",
                                        crf_sink=False), False),
        ("taps pruned but strip_probes false",
         dict(latency_taps=False),
         lambda c: c["board"]["constraints"].update(strip_probes=False), True),
        ("taps pruned, probes stripped",
         dict(latency_taps=False),
         lambda c: c["board"]["constraints"].update(strip_probes=True), False),
        ("MAAP pruned but stream DMACs are MAAP-allocated",
         dict(maap=False),
         lambda c: c.setdefault("srp", {}).update(stream_dmac_base="maap"),
         True),
        ("MAAP pruned, static DMAC base",
         dict(maap=False), lambda c: None, False),
        ("playback pruned but the interface is i2s_philips",
         dict(i2s_playback=False, render_lpf=False),
         lambda c: c["audio_interface"].update(kind="i2s_philips"), True),
        ("playback+LPF pruned, TDM interface",
         dict(i2s_playback=False, render_lpf=False), lambda c: None, False),
        ("filter pruned but rx_address_filter is hardware",
         dict(rx_mac_filter=False), lambda c: None, True),
        ("filter pruned, filtering declared in software",
         dict(rx_mac_filter=False),
         lambda c: c.setdefault("platform", {}).update(
             rx_address_filter="software"), False),
        # the mirror-image lie: a filter with nothing behind it. The AX base
        # config prunes render_lpf itself since 2026-07-28, so keeping the
        # filter now takes BOTH spellings said out loud - which is exactly
        # the config this case wants: LPF kept, playback gone.
        ("playback pruned but the render LPF kept",
         dict(i2s_playback=False, render_lpf=True),
         lambda c: c["board"]["constraints"].update(render_lpf=True), True),
        ("unknown feature name",
         dict(no_such_block=False), lambda c: None, True),
        ("non-boolean feature value",
         dict(maap="false"), lambda c: None, True),
        ("bad rx_address_filter value", {},
         lambda c: c.setdefault("platform", {}).update(
             rx_address_filter="firmware"), True),
    ]
    n_bad = n_ok = 0
    for label, feats, mutate, must_raise in cases:
        def m(c, feats=feats, mutate=mutate):
            _prune(c, **feats)
            mutate(c)
        p = _variant(CONFIGS["ax7101_8x8"], m)
        try:
            try:
                cfg = eb.load_config(p)
            except eb.ConfigError as ex:
                assert must_raise, f"{label}: ConfigError on a VALID config: {ex}"
                n_bad += 1
                continue
            assert not must_raise, f"{label}: accepted a config that asks " \
                                   "for a feature the prune removed"
            n_ok += 1
            # a valid prune must actually reach the argv and the estimate
            for k, v in feats.items():
                if v is False:
                    flag, param, _w = eb.OPTIONAL_BLOCKS[k]
                    argv = eb.emit_soc_argv(cfg)
                    assert flag in argv, f"{label}: {flag} missing from argv"
                    assert cfg["features"][k] is False
        finally:
            os.unlink(p)
    print(f"  [gate 23b] {n_bad}/{n_bad} contradictory prune configs REFUSED "
          f"with ConfigError; {n_ok}/{n_ok} honest prunes accepted and their "
          "--no-* flags reach the soc argv")


def test_optional_block_prune_accounting():
    """gate 23c - a pruned config's estimate must go DOWN by the banked
    figure, the plan must name the block, its milan_datapath parameter and
    the re-measurement it forces, and the estimate must stay labelled an
    ESTIMATE."""
    def m(c):
        _prune(c, media_clock_servo=False, latency_taps=False, maap=False,
               i2s_playback=False, rx_mac_filter=False, render_lpf=False)
        c["clocking"].update(media_clock_sources=["internal"],
                             default_source="internal", crf_sink=False)
        c["board"]["constraints"].update(strip_probes=True)
        c.setdefault("platform", {}).update(rx_address_filter="promiscuous")
    p = _variant(CONFIGS["ax7101_8x8"], m)
    try:
        base = eb.build(CONFIGS["ax7101_8x8"], OUT)
        pruned = eb.build(p, OUT)
    finally:
        os.unlink(p)
    b, q = base["resource_estimate"], pruned["resource_estimate"]
    # the CRF sink also goes with internal-only clocking, so compare against
    # the sum of the banked prune rows PLUS the crf_rx row the config drops.
    want_lut = sum(-eb.RESOURCE_COSTS[f"prune_{k}"]["lut"]
                   for k in ("media_clock_servo", "latency_taps",
                             "render_lpf")) \
        + eb.RESOURCE_COSTS["rx_filter"]["lut"] \
        + eb.RESOURCE_COSTS["i2s_renderer"]["lut"] \
        + eb.RESOURCE_COSTS["maap_claim_ctx"]["lut"]
    got_lut = b["totals"]["lut"] - q["totals"]["lut"]
    assert got_lut >= want_lut, \
        f"pruned estimate fell by {got_lut} LUT, want at least {want_lut}"
    assert q["totals"]["lut"] < b["totals"]["lut"]
    assert q["totals"]["ff"] < b["totals"]["ff"]
    plan = pruned["plan"]
    for k, (flag, param, _w) in eb.OPTIONAL_BLOCKS.items():
        assert f"`{k}`" in plan, f"plan does not name {k}"
        assert f"`{param}=0`" in plan, f"plan does not name {param}=0"
        assert flag in plan, f"plan does not name {flag}"
    assert "RE-MEASURE" in plan and "yosys estimate" in plan
    assert "ALL PRESENT" not in plan
    print(f"  [gate 23c] all-pruned ax7101_8x8: estimate -{got_lut} LUT / "
          f"-{b['totals']['ff'] - q['totals']['ff']} FF (banked rows "
          f"-{want_lut} LUT), plan names every block, its parameter, its "
          "flag and the re-measurement it forces, labelled ESTIMATE")


#: The five signals the TDM master binding is made of, as
#: (milan_soc.py Instance port, milan_datapath.sv port, platform subsignal).
#: `i2s_mclk_o` is deliberately in the list: milan_datapath routes the TDM
#: master's MCLK out of the I2S mclk pin (one pin serves both front-ends, and a
#: TDM build parks i2s_sclk/lrck), so on a master build that pin IS the TDM
#: MCLK and the SoC must rebind it away from the I2S Pmod.
TDM_MASTER_BINDING = [
    ("o_tdm_bclk_o",  "tdm_bclk_o",  "bclk"),
    ("o_tdm_fsync_o", "tdm_fsync_o", "fsync"),
    ("i_tdm_data_i",  "tdm_data_i",  "din"),
    ("o_tdm_dout_o",  "tdm_dout_o",  "dout"),
    ("o_i2s_mclk_o",  "i2s_mclk_o",  "mclk"),
]


def test_tdm_master_binding_reaches_the_pins():
    """gate 24 - THE L1 BINDING GATE for the item-4 TDM master.

    LEVEL 1 (module <-> wrapper <-> platform binding).  ORACLE: the fabric
    itself - the SoC glue and the platform pad table, parsed as text.  This is
    not a declaration checked against another declaration: every assertion
    below is "the thing that must be there is there, named exactly as the
    consumer names it".

    WHY IT EXISTS, three times over, all measured:

      * `p_AAF_PLAYBACK` was passed for WEEKS while the SV parameter was
        `AAF_PLAYBACK_P`. LiteX does not diagnose a parameter the module does
        not have - it drops it - so the flag pruned nothing and every gate
        stayed green. Gate 23d closed that for the six prune parameters; this
        one closes it for `AUDIO_IF_MASTER_P` / `AUDIO_IF_CLK_HZ_P`.
      * `i_tdm_bclk_i = 0, i_tdm_fsync_i = 0, i_tdm_data_i = 0` on every SoC in
        the tree: a TDM front-end bound to a bus nothing drove, whose talkers
        emitted NO FRAME AT ALL, while the config declared the interface and
        every gate agreed with every other gate.
      * the AX7101's `_connectors = []`: no pmoda, so `i2s_pads = None` and
        `i_i2s_sdout_i = 0` - a front-end clocking in a constant zero on a
        board with no routed pins.

    So: if the pads vanish from the platform, if bclk/fsync stop being driven
    OUT to them, or if a parameter name stops matching the RTL, this fails."""
    _tdm_master_binding(*_tdm_sources())
    print(f"  [gate 24] TDM master L1 binding: 2 parameters name-matched into "
          f"milan_datapath, KL_tdm_capture_master instantiated on clk_tdm_i, "
          f"{len(TDM_MASTER_BINDING)} signals RTL-port -> SoC -> AX7101 J11 "
          f"ball, collision-free, loose-requested")


def _tdm_sources():
    return (open(os.path.join(ROOT, "sw/litex/milan_soc.py")).read(),
            open(os.path.join(ROOT, "hdl/milan/milan_datapath.sv")).read(),
            open(os.path.join(ROOT,
                              "sw/litex/platforms/alinx_ax7101.py")).read())


def _tdm_master_binding(soc, rtl, plat):
    """The gate-24 assertions, over SOURCE TEXT rather than files, so gate 24b
    can hand them a mutated tree and prove each one can fail."""
    # 1. the RTL declares both parameters, and the MASTER defaults to OFF so
    #    every build that does not ask for one is byte-identical.
    for param, dflt in (("AUDIO_IF_MASTER_P", "0"),
                        ("AUDIO_IF_CLK_HZ_P", None)):
        m = re.search(r"^\s*parameter\s+int\s+%s\s*=\s*(\d+)\s*[,)]"
                      % re.escape(param), rtl, re.M)
        assert m, f"milan_datapath.sv has no `parameter int {param}`"
        if dflt is not None:
            assert m.group(1) == dflt, (
                f"{param} defaults to {m.group(1)}; it must default to {dflt} "
                f"so a build that does not ask for a TDM master elaborates "
                f"the shape that ships today")
        # 2. and milan_soc.py passes THAT NAME, character for character.
        assert re.search(r'dp_params\[\s*["\']p_%s["\']\s*\]\s*=' % param, soc), \
            (f"milan_soc.py never assigns dp_params['p_{param}'] - a LiteX "
             f"Instance parameter the module does not have is SILENTLY "
             f"DROPPED, which is exactly how p_AAF_PLAYBACK pruned nothing "
             f"for weeks")

    # 3. the CLI flag is a real, off-by-default store_true.
    assert re.search(r'ap\.add_argument\("--audio-interface-master",\s*'
                     r'action="store_true"', soc), \
        "milan_soc.py has no `--audio-interface-master` store_true argument"

    # 4. the master front-end is actually INSTANTIATED under that parameter,
    #    and it is the MASTER module - naming the slave here would bind the
    #    dead path.
    g = re.search(r"end else if \(AUDIO_IF_MASTER_P != 0\) begin : (\w+)", rtl)
    assert g, ("milan_datapath.sv: AUDIO_IF_MASTER_P guards no front-end "
               "generate arm")
    arm = rtl[g.end():rtl.find("end else begin :", g.end())]
    assert "KL_tdm_capture_master" in arm, (
        "the AUDIO_IF_MASTER_P arm does not instantiate KL_tdm_capture_master "
        "- KL_tdm_capture is the SLAVE, whose bclk/fsync are tied to 0")
    # the clock it divides must be the DEDICATED one, not clk_audio_i: 24.576
    # MHz is a contract (KL_crf_tx /512, KL_i2s_playback, the servo).
    assert re.search(r"\.clk_audio_i\s*\(\s*clk_tdm_i\s*\)", arm), (
        "the TDM master is not fed clk_tdm_i - re-rating clk_audio_i would "
        "silently move the CRF event rate, the DAC and the servo")

    # 5. every signal of the binding: declared in the RTL as the right
    #    DIRECTION, connected by the SoC, and resolved to a platform pad.
    for soc_port, rtl_port, sub in TDM_MASTER_BINDING:
        want_dir = "output" if soc_port.startswith("o_") else "input"
        assert re.search(r"^\s*%s\s+(wire|logic|reg)?\s*[\[\w].*?\b%s\b"
                         % (want_dir, re.escape(rtl_port)), rtl, re.M), \
            (f"milan_datapath.sv declares no `{want_dir} ... {rtl_port}` - "
             f"a port's DIRECTION cannot be parameterized in SystemVerilog, "
             f"so a master build needs its own output pins")
        m = re.search(r"%s\s*=\s*\(?\s*self\.tdm_pads\.%s\b"
                      % (re.escape(soc_port), re.escape(sub)), soc)
        assert m, (f"milan_soc.py never binds {soc_port} to self.tdm_pads."
                   f"{sub} - the master would generate a bus into an "
                   f"unconnected Signal() and the board would see nothing, "
                   f"which is the `_connectors = []` defect with new pins")
        # 6. and the PLATFORM really routes that subsignal to a ball.
        m = re.search(r'Subsignal\("%s",\s*Pins\("([A-Z]+\d+)"\)'
                      % re.escape(sub), plat)
        assert m, (f"alinx_ax7101.py declares no `tdm` Subsignal '{sub}' with "
                   f"a package pin - a pad that is not routed is a front-end "
                   f"clocking in a constant zero")
        assert m.group(1) not in _ax7101_taken_pins(plat, sub), \
            f"tdm.{sub} pin {m.group(1)} collides with an existing resource"

    # 7. the resource is requested LOOSELY, so a board without the header
    #    still elaborates rather than asserting at constraint resolution
    #    (the AX7101 'pmoda' break, 2026-07-13).
    assert re.search(r'platform\.request\("tdm",\s*loose=True\)', soc), \
        ("milan_soc.py must request the tdm pads with loose=True - a missing "
         "resource asserts at constraint RESOLUTION, far outside any except")


#: gate 24b negative controls: (label, which source, anchor, mutation).
#: Each one reproduces a MEASURED escape class, so the gate is not merely
#: asserted to be able to fail - it is shown to, on the exact defects that got
#: through before. R2: a check that cannot fail is not a check.
TDM_BINDING_MUTATIONS = [
    ("p_AAF_PLAYBACK class: the SoC passes a name the RTL does not have",
     "soc", 'dp_params["p_AUDIO_IF_MASTER_P"] = 1',
     'dp_params["p_AUDIO_IF_MASTER"] = 1'),
    ("the master reverts to clk_audio_i (24.576 MHz is a CRF/DAC contract)",
     "rtl", ".clk_audio_i (clk_tdm_i),", ".clk_audio_i (clk_audio_i),"),
    ("the master arm instantiates the SLAVE, whose bus is tied to 0",
     "rtl", "KL_tdm_capture_master #(", "KL_tdm_capture #("),
    ("bclk is generated but never bound to a pad",
     "soc", "o_tdm_bclk_o  = (self.tdm_pads.bclk if self.tdm_pads",
     "o_tdm_bclk_o  = (Signal() if self.tdm_pads"),
    ("_connectors = [] class: the platform stops routing fsync",
     "plat", 'Subsignal("fsync", Pins("F19")),',
     'Subsignal("fsync", Pins("")),'),
    ("AUDIO_IF_MASTER_P defaults ON, so existing builds silently change",
     "rtl", "parameter int AUDIO_IF_MASTER_P = 0,",
     "parameter int AUDIO_IF_MASTER_P = 1,"),
    ("the pads are requested strictly, so a headerless board stops building",
     "soc", 'platform.request("tdm", loose=True)', 'platform.request("tdm")'),
]


def test_tdm_master_binding_gate_bites():
    """gate 24b - prove every gate-24 assertion can FAIL.

    LEVEL 1, same oracle. Seven mutations of the real sources, each the shape
    of a defect this repo actually shipped or nearly shipped; every one must be
    REJECTED. Run in memory, so nothing is written to the tree."""
    base = dict(zip(("soc", "rtl", "plat"), _tdm_sources()))
    for label, which, anchor, mutant in TDM_BINDING_MUTATIONS:
        assert anchor in base[which], \
            f"gate 24b setup: anchor for '{label}' no longer exists in {which}"
        src = dict(base)
        src[which] = base[which].replace(anchor, mutant, 1)
        try:
            _tdm_master_binding(src["soc"], src["rtl"], src["plat"])
        except AssertionError:
            continue
        raise AssertionError(
            f"gate 24 ACCEPTED a mutated tree - it cannot detect: {label}")
    print(f"  [gate 24b] {len(TDM_BINDING_MUTATIONS)}/"
          f"{len(TDM_BINDING_MUTATIONS)} binding mutations REJECTED "
          f"(name mismatch, wrong clock, slave-instead-of-master, unbound "
          f"pad, unrouted pin, default-on, strict request)")


def _ax7101_taken_pins(plat, exclude_sub):
    """Every package pin the AX7101 platform claims OUTSIDE the tdm resource.

    Comments are stripped first: this file documents its pin choices in prose
    that quotes ball names, and a documented ball must not read as a claimed
    one."""
    body = "\n".join(l.split("#")[0] for l in plat.split("\n"))
    tdm = body[body.index('("tdm", 0,'):] if '("tdm", 0,' in body else ""
    tdm = tdm[:tdm.index("),\n", tdm.index("IOStandard"))] if tdm else ""
    taken = set()
    for m in re.finditer(r'Pins\("([^"]+)"\)', body):
        if m.start() >= (body.index(tdm) if tdm else len(body)) and \
           tdm and m.start() < body.index(tdm) + len(tdm):
            continue                       # inside the tdm resource itself
        taken.update(m.group(1).split())
    return taken


def test_optional_block_names_reach_the_rtl():
    """gate 23d - the DECORATIVE-ABI gate, and the reason it exists is on the
    record: `milan_soc.py` passed `p_AAF_PLAYBACK` for weeks while the SV
    parameter was `AAF_PLAYBACK_P`, so a LiteX Instance param silently no-oped
    and the flag pruned nothing. Nothing caught it because no CI job runs
    LiteX. This gate parses the three files as TEXT and pins them together:

      builder OPTIONAL_BLOCKS  <->  milan_soc.py MILAN_OPTIONAL_BLOCKS + argparse
                               <->  milan_datapath.sv `parameter int <NAME> = 1`

    A rename or a typo in any one of them fails here in milliseconds."""
    soc = open(os.path.join(ROOT, "sw/litex/milan_soc.py")).read()
    rtl = open(os.path.join(ROOT, "hdl/milan/milan_datapath.sv")).read()
    # 1. the SoC's own keyword -> parameter map, parsed from the literal
    soc_map = dict(re.findall(r'^\s*"([a-z0-9_]+)":\s*"([A-Z0-9_]+)",',
                              soc[soc.index("MILAN_OPTIONAL_BLOCKS = {"):
                                  soc.index("}", soc.index(
                                      "MILAN_OPTIONAL_BLOCKS = {"))],
                              re.M))
    assert soc_map, "milan_soc.py: MILAN_OPTIONAL_BLOCKS did not parse"
    for name, (flag, param, _why) in eb.OPTIONAL_BLOCKS.items():
        assert soc_map.get(name) == param, (
            f"{name}: builder says {param}, milan_soc.py says "
            f"{soc_map.get(name)!r}")
        # 2. the CLI flag really exists, as an off-by-default store_true
        m = re.search(r'ap\.add_argument\("%s",\s*action="store_true"'
                      % re.escape(flag), soc)
        assert m, f"{name}: milan_soc.py has no `{flag}` store_true argument"
        # 3. the RTL parameter exists AND DEFAULTS TO 1 (rule 1, at the source)
        m = re.search(r"^\s*parameter\s+int\s+%s\s*=\s*(\d+)\s*[,)]"
                      % re.escape(param), rtl, re.M)
        assert m, f"{name}: milan_datapath.sv has no `parameter int {param}`"
        assert m.group(1) == "1", (
            f"{param} defaults to {m.group(1)} in milan_datapath.sv - every "
            "prune parameter MUST default to 1 = PRESENT (AREA_BUDGET rule 1)")
        # 4. it actually gates a generate, and the generate has an else arm
        #    (an inert tie-off, rule 3) - a parameter that guards nothing is
        #    the same lie in a different costume
        g = re.search(r"generate if \(%s != 0\) begin : (\w+)"
                      % re.escape(param), rtl)
        assert g, f"{param} guards no `generate if` in milan_datapath.sv"
        tail = rtl[g.end():]
        nxt = tail.find("generate if (")
        arm = tail[:nxt if nxt > 0 else len(tail)]
        assert re.search(r"end else begin : \w+", arm), \
            f"{param}: generate has no else arm - a pruned block must tie " \
            "its outputs to an inert value, not float them"
        # 5. the Instance passes the parameter ONLY to prune (p_<PARAM> = 0)
        assert f'dp_params[f"p_{{param}}"] = 0' in soc or \
               re.search(r'dp_params\[f?"p_\{?param\}?"\]\s*=\s*0', soc), \
            "milan_soc.py must emit p_<PARAM>=0 only when pruning"
    # 6. and the DOC that authorises all of this names the same six, with the
    #    same parameter and the same flag. A prune table that drifts from the
    #    RTL is how a banked lever becomes folklore.
    doc = open(os.path.join(ROOT, "docs/design/AREA_BUDGET.md")).read()
    for name, (flag, param, _why) in eb.OPTIONAL_BLOCKS.items():
        row = re.search(r"^\|[^|\n]+\| `%s` \| `%s` \| `%s` \|"
                        % (re.escape(param), re.escape(flag),
                           re.escape(name)), doc, re.M)
        assert row, (f"AREA_BUDGET.md tier-1 table has no row mapping "
                     f"`{param}` / `{flag}` / `{name}`")
    # the three subtractive estimator rows must quote the doc's figures
    for k in ("media_clock_servo", "latency_taps", "render_lpf"):
        lut = -eb.RESOURCE_COSTS[f"prune_{k}"]["lut"]
        assert re.search(r"\| %s \|" % lut, doc) or f"{lut}" in doc, \
            f"AREA_BUDGET.md does not carry the banked {lut} LUT for {k}"
    print(f"  [gate 23d] {len(eb.OPTIONAL_BLOCKS)} optional blocks: builder "
          "key == milan_soc.py map == a real --no-* store_true == a "
          "milan_datapath `parameter int X = 1` guarding a generate WITH an "
          "else arm == the AREA_BUDGET tier-1 table row (the "
          "p_AAF_PLAYBACK silent-no-op class, closed)")


# ======================================================== gates 24c / 24d ====
#  PER-BOARD AUDIO FRONT-END ROUTING - the L1 binding, one board at a time.
#
#  Gate 24/24b prove the TDM master binding reaches the AX7101's pins. They say
#  nothing about the OTHER board, and the binding is not board-independent: on
#  2026-07-28 endstation_arty_4x4.yaml declared `kind: tdm8` while the Arty
#  routes no `tdm` resource at all, and the answer to "is a TDM front-end real"
#  was being computed GLOBALLY - endstation_builder.tdm_bus_wired() asks "can
#  ANY SoC in this tree build a TDM master", which turns true for EVERY board
#  the moment the master lands. A per-board fact answered once for the whole
#  tree. The consequence on the Arty:
#
#    (a) bclk / fsync / dout drive unconnected Signal()s and tdm_data_i reads 0
#        -> 8 channels of DIGITAL SILENCE; and
#    (b) o_i2s_mclk_o is rebound off the Pmod I2S2 - milan_datapath routes the
#        TDM master's MCLK out of the I2S mclk pin - taking the CS5343 MCLK off
#        pmoda:4 (ball D13). That is the ONLY working audio input the Arty has
#        and the one the board-to-board analog loop runs through
#        (docs/findings/BENCH_TOPOLOGY.md); endstation_arty_current.yaml streams
#        through it to a Milan-validated reference device with zero
#        unsupported-format frames. It is the project's negative control.
#
#  It was reported as a printed warning. methodology R5 - a structural zero is
#  not a measurement - says a capability the fabric cannot back must read as
#  UNSUPPORTED, so it is now a refusal.
#
#  ORACLE (R1): the platform - which pins actually exist on that board - read as
#  text by sw/litex/platforms/board_audio_routing.py. NOT a spec question (R3):
#  no clause in 1722/802.1BA/Milan says which balls a board brings out.
#
#  R4: the checks below are shaped like the property. Two layers, because the
#  defect has two:
#    L-decl  a config may DECLARE a TDM front-end only for a board that can
#            have one - routed today, or on a platform this repo owns and can
#            route. The Arty rides a stock upstream platform and has no TDM
#            extension, so it satisfies neither.
#    L-argv  and no config's argv may SELECT a TDM front-end for a board that
#            does not route one. This is the layer the global tdm_bus_wired()
#            breaks, so it is exercised in BOTH tree states - today's, and a
#            synthesized "the master has landed" tree.

sys.path.insert(0, os.path.join(ROOT, "sw/litex/platforms"))
import board_audio_routing as bar  # noqa: E402


def _routing_sources():
    return {"plat": open(os.path.join(
                ROOT, "sw/litex/platforms/alinx_ax7101.py")).read(),
            "soc": open(os.path.join(ROOT, "sw/litex/milan_soc.py")).read()}


def _argv_under(cfg_path, wired):
    """This config's soc argv with tdm_bus_wired() FORCED.

    `wired=True` synthesizes the tree in which the TDM master front-end has
    landed - the state that turns the Arty's placeholder declaration into a
    real `--audio-interface tdm8 --audio-interface-master` build. Testing only
    today's tree would be testing the one state in which the defect is dormant.
    """
    saved = dict(eb._TDM_WIRED_CACHE)
    try:
        eb._TDM_WIRED_CACHE["cached"] = wired
        return eb.emit_soc_argv(eb.load_config(cfg_path))
    finally:
        eb._TDM_WIRED_CACHE.clear()
        eb._TDM_WIRED_CACHE.update(saved)


def _board_can_have_tdm(board, src):
    """Can this board back a TDM front-end at all?

    True when it routes a `tdm` resource today, OR when its platform is one
    this repo ships - in which case the header is ours to declare and the pins
    are a decision, not a wish. False for a board riding a STOCK upstream
    platform with no TDM extension: nothing in this tree can route it.
    """
    return bar.routes_tdm(board, src) or board in bar._REPO_PLATFORM


def _front_end_routing(src, cfg_paths, argv_of=None):
    """The gate-24c assertions over SOURCE TEXT plus config paths, so 24d can
    hand them a mutated tree and prove each one can fail.

    `argv_of(path, wired) -> argv` is injectable for the same reason: the L-ARGV
    layer below can only be shown to fail if something can hand it an argv that
    selects a TDM front-end on a headerless board, and no config in the tree
    does that (which is the point). A stub supplies one."""
    argv_of = argv_of or _argv_under
    soc, plat = src["soc"], src["plat"]

    # 0. the vocabulary the refusal keys on must be the SoC's own --audio-
    #    interface choices, minus the non-TDM ones. A kind added on one side
    #    only would walk straight past every check below.
    m = re.search(r'"--audio-interface",\s*\n?\s*.*?choices=\(([^)]*)\)',
                  soc, re.S)
    assert m, "milan_soc.py has no --audio-interface choices tuple"
    soc_kinds = set(re.findall(r'["\'](\w+)["\']', m.group(1)))
    assert set(bar.TDM_KINDS) == {k for k in soc_kinds if k.startswith("tdm")}, \
        (f"board_audio_routing.TDM_KINDS {bar.TDM_KINDS} != the SoC's tdm "
         f"choices {sorted(k for k in soc_kinds if k.startswith('tdm'))}")

    # 1. THE REFUSAL EXISTS AND RUNS BEFORE THE PLATFORM IS BUILT. A check
    #    after elaboration is a check that already emitted the bitstream.
    call = soc.find("board_audio_routing.assert_front_end_routed(")
    assert call != -1, \
        ("milan_soc.py never calls board_audio_routing.assert_front_end_routed "
         "- an unbackable front-end would be a printed warning and then a "
         "bitstream that emits zeros (methodology R5)")
    built = soc.find("platform = digilent_arty.Platform(")
    assert built != -1 and call < built, \
        ("the front-end routing refusal must run BEFORE the platform is "
         "constructed, so an unroutable request fails the BUILD")
    assert re.search(r"assert_front_end_routed\(\s*\n?\s*args\.board,\s*"
                     r"args\.audio_interface", soc), \
        "the refusal must be keyed on args.board AND args.audio_interface"
    assert 'getattr(args, "audio_interface_master", False)' in soc, \
        ("the refusal must read the master flag defensively - it exists in the "
         "tree that lands the TDM master and not in the one before it")

    # 2a. L-DECL: a config may declare a TDM front-end only for a board that can
    #     HAVE one - it routes a header today, or its pinout is this repo's to
    #     declare one in (`_REPO_PLATFORM`: the AX7101 is not in upstream
    #     litex_boards, so we ship and own its `_io`). A board on a STOCK
    #     upstream platform with no TDM extension is neither: nothing here can
    #     route it, and declaring a front-end for it is a claim about hardware
    #     that does not exist and is not being built.
    for name, path in cfg_paths.items():
        cfg = eb.load_config(path)
        board, kind = cfg["board_target"], cfg["interface"]["kind"]
        if kind not in bar.TDM_KINDS:
            continue
        assert _board_can_have_tdm(board, src), (
            f"{name} declares `{kind}` for board `{board}`, which routes no "
            f"`tdm` resource and whose platform this repo does not own - there "
            f"is nowhere to declare one and no device to plug in. A "
            f"declaration the board can never back is the item-00 defect one "
            f"layer down.")

    # 2b. and a repo-owned platform that DOES declare a `tdm` resource must
    #     route every one of its subsignals to a real ball. `Pins("")` resolves
    #     and reaches nowhere - the `_connectors = []` defect wearing a
    #     resource name.
    body = "\n".join(l.split("#")[0] for l in plat.split("\n"))
    if '("tdm", 0,' in body:
        entry = body[body.index('("tdm", 0,'):]
        entry = entry[:entry.index("),\n\n")] if "),\n\n" in entry else entry
        subs = re.findall(r'Subsignal\("(\w+)",\s*Pins\("([^"]*)"\)', entry)
        assert subs, "the platform's `tdm` resource declares no Subsignals"
        for sub, pins in subs:
            assert re.match(r"^[A-Z]+\d+", pins), (
                f"platform tdm.{sub} has Pins({pins!r}) - a pad that is not "
                f"routed is a front-end clocking in a constant zero")

    # 3. L-ARGV: no config's argv may SELECT a TDM front-end for a board that
    #    cannot back one. Checked in BOTH reachable tree states, with the
    #    strength each state can actually know:
    #      wired=False  THIS tree. Strict: the header must EXIST today.
    #      wired=True   the tree the TDM master creates - and the master is only
    #                   meaningful alongside the platform work that routes the
    #                   header, which for a repo-owned platform lands together
    #                   (gate 24/24b is what proves it really did). So the
    #                   weaker "can have one" applies, which is still enough to
    #                   refuse a board whose pinout is not ours - the Arty.
    #    This second pass is the whole point: tdm_bus_wired() answers a GLOBAL
    #    question ("can ANY SoC here build a master?") and so turns true for
    #    EVERY board at once, while whether a front-end reaches a pin is PER
    #    BOARD. Testing only today's tree tests the one state in which the
    #    defect is dormant.
    for wired, ok in ((False, bar.routes_tdm), (True, _board_can_have_tdm)):
        for name, path in cfg_paths.items():
            board = eb.load_config(path)["board_target"]
            argv = argv_of(path, wired)
            sel = [argv[i + 1] for i, a in enumerate(argv[:-1])
                   if a == "--audio-interface"]
            master = "--audio-interface-master" in argv
            if not any(k in bar.TDM_KINDS for k in sel) and not master:
                continue
            assert ok(board, src), (
                f"{name} (board {board}) emits --audio-interface "
                f"{' '.join(sel) or '?'}{' --audio-interface-master' * master} "
                f"with tdm_bus_wired()={wired}, but that board routes no `tdm` "
                f"resource and cannot be given one here: bclk/fsync/dout would "
                f"drive unconnected Signal()s, tdm_data_i would read 0 "
                f"(digital silence at the declared width) and o_i2s_mclk_o "
                f"would be rebound off the I2S pad.")

    # 4. i2s_mclk STAYS ON THE PMOD on every build that uses the I2S front-end.
    #    Requirement in its own right: the Arty's Pmod I2S2 is the one
    #    known-good audio path in the project. Every binding of o_i2s_mclk_o
    #    must be either the I2S Pmod pad or a TDM master pad - never an
    #    unconditional bare Signal(), which is how (b) happened.
    binds = re.findall(r"o_i2s_mclk_o\s*=\s*([^\n]*)", soc)
    assert binds, "milan_soc.py binds o_i2s_mclk_o nowhere"
    assert any("self.i2s_pads[0]" in b for b in binds), \
        ("no build binds o_i2s_mclk_o to self.i2s_pads[0] - the Pmod I2S2 "
         "MCLK (pmoda:4, ball D13) feeds the CS5343 ADC; without it the "
         "board's only working audio input is dead")
    for b in binds:
        assert "self.i2s_pads[0]" in b or "tdm_pads" in b, (
            f"o_i2s_mclk_o is bound to `{b.strip()}` - it may only ever reach "
            f"the I2S Pmod pad or a TDM master pad. Binding it to a bare "
            f"Signal() takes the MCLK off pmoda:4 (D13) on a board whose I2S "
            f"front-end is the one that streams to a qualified listener.")

    # 5. and the Arty pad record must still agree with the real platform,
    #    whenever the real platform can be imported.
    assert bar.verify_against_litex_boards() in (None, True)


def test_front_end_routing_per_board():
    """gate 24c - a config may not request a front-end its board does not route.

    LEVEL 1 (config <-> wrapper <-> platform binding). ORACLE: the platform pad
    tables, parsed as text. Every assertion is "the pin the consumer names is
    really there on THAT board"."""
    src = _routing_sources()
    _front_end_routing(src, CONFIGS)
    routed = {b: bar.routes_tdm(b, src) for b in ("arty", "ax7101")}
    print(f"  [gate 24c] per-board front-end routing: tdm routed {routed}; "
          f"3 configs checked at BOTH tdm_bus_wired() states; the refusal runs "
          f"before the platform is built; o_i2s_mclk_o binds only to "
          f"i2s_pads[0] (pmoda:4 D13) or tdm_pads; Arty pad record re-derived "
          f"from litex_boards" if bar.verify_against_litex_boards()
          else f"  [gate 24c] per-board front-end routing: tdm routed {routed}; "
               f"3 configs checked at BOTH tdm_bus_wired() states; the refusal "
               f"runs before the platform is built; o_i2s_mclk_o binds only to "
               f"i2s_pads[0] (pmoda:4 D13) or tdm_pads")


#: gate 24d negative controls. Each is a MEASURED defect shape, not an invented
#: one, so the gate is not merely asserted to be able to fail - it is shown to,
#: on the thing that actually happened. R2: a check that cannot fail is not a
#: check.  (label, kind, payload) where kind is "soc" | "plat" | "cfg".
ROUTING_MUTATIONS = [
    # THE 2026-07-28 DEFECT, preserved from the other side. arty_4x4 SHIPS
    # kind: tdm8 since HANDOVER 8.3b, backed by the one add_extension line in
    # milan_soc.py's arty path. Delete that line and this is exactly the
    # pre-8.3b tree again - a front-end selected on a board that routes no
    # pins - and the refusal must fire. (tdm16/tdm32 variants were dropped
    # with the 8.3b flip: routing is a pad fact and the pads now exist; a
    # slot count is not a routing question and is owned by the clocking
    # guards.)
    ("arty_4x4 declares tdm8 and the Arty's tdm extension is DELETED",
     "soc", ('plat.add_extension(_arty_serial_io("tdm", "pmodb"))',
             "pass")),
    # THE (b) HALF: i2s_mclk moved off the Pmod.
    ("i2s_mclk is bound to a bare Signal() - off pmoda:4 (D13), the CS5343 "
     "MCLK, on the board whose I2S path is the project's negative control",
     "soc", ("o_i2s_mclk_o = self.i2s_pads[0] if self.i2s_pads else Signal(),",
             "o_i2s_mclk_o = Signal(),")),
    # THE REFUSAL ITSELF.
    ("the refusal is deleted and the warning comes back",
     "soc", ("board_audio_routing.assert_front_end_routed(",
             "_deleted_assert_front_end_routed(")),
    ("the refusal stops being keyed on the BOARD - a per-board fact answered "
     "globally is the whole defect",
     "soc", ("assert_front_end_routed(\n        args.board,",
             "assert_front_end_routed(\n        None,")),
    ("the refusal runs AFTER the platform is built, i.e. too late to refuse",
     "soc_move", None),
    ("the refusal stops reading the master flag defensively",
     "soc", ('getattr(args, "audio_interface_master", False)',
             "False")),
    # THE _connectors = [] CLASS, on the AX side of the same rule.
    ("a routed tdm resource loses its pins (Pins(\"\") resolves, reaches "
     "nowhere)", "plat_tdm", None),
    # A NEW INTERFACE KIND ADDED ON ONE SIDE ONLY.
    ("milan_soc gains a tdm kind the routing module does not know about",
     "soc", ('choices=("i2s_philips", "tdm8", "tdm16", "tdm32")',
             'choices=("i2s_philips", "tdm8", "tdm16", "tdm32", "tdm64")')),
    # THE L-ARGV LAYER, which the declaration mutations above never reach
    # because L-DECL catches them first. Since 8.3b the tdm8 argv for the
    # Arty is the SHIPPING argv, so the leak is only a defect on a tree whose
    # arty extension is gone - the mutation pairs the two, which is the argv
    # the original defect actually produced on the original tree state.
    ("L-ARGV: the tdm8+master argv reaches an Arty whose tdm extension is "
     "deleted (tdm_bus_wired() answers for the whole tree at once)",
     "argv_soc", (('plat.add_extension(_arty_serial_io("tdm", "pmodb"))',
                   "pass"),
                  (True, ["--board", "arty", "--audio-interface", "tdm8",
                          "--audio-interface-master"]))),
]


#: gate 24e: the 8.3b BLEND bindings - (label, which, regex) that must all
#: hold, and each is mutated below to prove it can fail. The blend is three
#: bindings: the parameter NAME reaches the RTL (the p_AAF_PLAYBACK class),
#: the I2S mclk goes BACK to the Pmod (D13, the CS5343 - the pin that must
#: not move), and the TDM header gets the master's mclk on its OWN pad.
BLEND_BINDINGS = [
    ("RTL declares AUDIO_IF_I2S_PAIR_P defaulting OFF", "rtl",
     r"parameter\s+int\s+AUDIO_IF_I2S_PAIR_P\s*=\s*0\s*,"),
    ("the SoC passes THAT name, character for character", "soc",
     r'dp_params\[\s*["\']p_AUDIO_IF_I2S_PAIR_P["\']\s*\]\s*='),
    ("RTL declares the dedicated tdm_mclk_o output", "rtl",
     r"^\s*output\s+wire\s+.*\btdm_mclk_o\b"),
    ("the blend rebinds o_i2s_mclk_o to the Pmod (D13)", "soc",
     # the pads live on MilanDMA, reached via getattr (a migen Module raises
     # AttributeError for never-assigned names - the AX tdm32 build has no
     # i2s front-end at all, found 2026-07-28)
     r'dp_ports\[\s*["\']o_i2s_mclk_o["\']\s*\]\s*=\s*_dma_i2s\[0\]'),
    ("the blend binds o_tdm_mclk_o to the header's own mclk pad", "soc",
     r'dp_ports\[\s*["\']o_tdm_mclk_o["\']\s*\]\s*=\s*self\.tdm_pads\.mclk'),
    ("the arty tdm extension names its five subsignals", "soc",
     r'Subsignal\("mclk",\s*Pins\(f"\{pmod\}:0"\)\)'),
]


def _blend_binding(soc, rtl):
    for label, which, rx in BLEND_BINDINGS:
        src = soc if which == "soc" else rtl
        assert re.search(rx, src, re.M), f"8.3b blend binding missing: {label}"


def test_i2s_pair_blend_binding():
    """gate 24e - L1 binding for the 8.3b I2S+TDM blend.

    LEVEL 1, oracle = the fabric (SoC glue + RTL text). The blend is what
    keeps the Arty's ONE known-good audio path alive on a tdm8 build: without
    the o_i2s_mclk_o rebind the master steals pmoda:4 (ball D13, the CS5343
    MCLK) and the bench analog loop dies silently - the (b) half of the
    original 2026-07-28 defect, reachable again through the blend."""
    soc, rtl, _ = _tdm_sources()
    _blend_binding(soc, rtl)
    assert eb.i2s_pair_blended(eb.load_config(CONFIGS["arty_4x4"])), \
        "arty_4x4 does not blend - framer_pair_supply loses the I2S pair"
    assert eb.framer_pair_supply(
        eb.load_config(CONFIGS["arty_4x4"])) == 5, \
        "arty_4x4 pair supply != 5 (4 TDM8 pairs + the I2S pair at slot 0)"
    assert not eb.i2s_pair_blended(eb.load_config(CONFIGS["ax7101_8x8"])), \
        "the AX7101 must stay a solo master (no pmoda, nothing to blend)"
    print("  [gate 24e] 8.3b blend: "
          f"{len(BLEND_BINDINGS)} bindings held; arty_4x4 supplies 5 pairs "
          "(I2S at slot 0), AX7101 stays solo")


def test_i2s_pair_blend_gate_bites():
    """gate 24e-b - every blend binding can FAIL (R2)."""
    soc, rtl, _ = _tdm_sources()
    base = {"soc": soc, "rtl": rtl}
    n = 0
    for label, which, rx in BLEND_BINDINGS:
        src = dict(base)
        m = re.search(rx, src[which], re.M)
        assert m, f"gate 24e-b setup: '{label}' anchor gone"
        src[which] = src[which].replace(m.group(0), "# mutated", 1)
        try:
            _blend_binding(src["soc"], src["rtl"])
        except AssertionError:
            n += 1
            continue
        raise AssertionError(
            f"gate 24e ACCEPTED a mutated tree - cannot detect: {label}")
    print(f"  [gate 24e-b] {n}/{len(BLEND_BINDINGS)} blend-binding "
          "mutations REJECTED")


def test_front_end_routing_gate_bites():
    """gate 24d - prove every gate-24c assertion can FAIL.

    LEVEL 1, same oracle. Config mutations are written to a temp file (the
    builder loads by path); source mutations run in memory, so nothing is
    written to the tree."""
    base = _routing_sources()
    #: the AX with the J11 header Lane 1 routes - the tree state in which the
    #: `Pins("")` mutation is meaningful at all. Without a routed resource to
    #: break, that negative control would be vacuous.
    j11 = ('    ("tdm", 0,\n'
           '        Subsignal("mclk",  Pins("B22")),\n'
           '        Subsignal("dout",  Pins("A20")),\n'
           '        Subsignal("bclk",  Pins("B20")),\n'
           '        Subsignal("din",   Pins("F20")),\n'
           '        Subsignal("fsync", Pins("F19")),\n'
           '        IOStandard("LVCMOS33"),\n'
           '    ),\n')
    plat_j11 = base["plat"].replace('    ("ddram", 0,', j11 + '    ("ddram", 0,')
    assert bar.routes_tdm("ax7101", dict(base, plat=plat_j11)), \
        "gate 24d setup: the synthesized J11 header does not read as routed"
    # 8.3b: the Arty routes tdm through its OWN one-line soc extension; the
    # per-board isolation property is tested on a tree with that line gone -
    # an AX header must still never answer for the Arty.
    _ARTY_TDM_EXT = 'plat.add_extension(_arty_serial_io("tdm", "pmodb"))'
    assert _ARTY_TDM_EXT in base["soc"], \
        "gate 24d setup: the Arty tdm extension line moved - update the anchor"
    assert bar.routes_tdm("arty", base), \
        "gate 24d setup: the Arty must route tdm via its soc extension (8.3b)"
    soc_no_arty = base["soc"].replace(_ARTY_TDM_EXT, "pass")
    assert not bar.routes_tdm("arty", dict(base, plat=plat_j11,
                                           soc=soc_no_arty)), \
        "gate 24d setup: an AX header must not make the ARTY route tdm"

    n = 0
    for label, which, payload in ROUTING_MUTATIONS:
        src, cfgs, tmp, argv_of = dict(base), dict(CONFIGS), None, None
        try:
            if which == "argv":
                at, argv = payload

                def argv_of(path, wired, _at=at, _argv=argv):
                    if wired == _at and path == CONFIGS["arty_4x4"]:
                        return list(_argv)
                    return _argv_under(path, wired)
            elif which == "argv_soc":
                (anchor, mutant), (at, argv) = payload
                assert anchor in src["soc"], \
                    f"gate 24d setup: anchor for '{label}' gone from soc"
                src["soc"] = src["soc"].replace(anchor, mutant, 1)

                def argv_of(path, wired, _at=at, _argv=argv):
                    if wired == _at and path == CONFIGS["arty_4x4"]:
                        return list(_argv)
                    return _argv_under(path, wired)
            elif which == "cfg":
                name, anchor, mutant = payload
                raw = open(CONFIGS[name]).read()
                assert anchor in raw, \
                    f"gate 24d setup: anchor for '{label}' gone from {name}"
                fd, tmp = tempfile.mkstemp(suffix=".yaml")
                with os.fdopen(fd, "w") as fh:
                    fh.write(raw.replace(anchor, mutant, 1))
                cfgs[name] = tmp
            elif which == "soc_move":
                # RELOCATE the refusal to after the platform is constructed.
                # Deleting a word would not test the ORDER; moving the call is
                # the only mutation whose sole effect is lateness.
                blk = re.search(r"\n    board_audio_routing\."
                                r"assert_front_end_routed\((?:[^\n]*\n){2}",
                                src["soc"])
                assert blk, "gate 24d setup: cannot locate the refusal block"
                anchor = "        platform = alinx_ax7101.Platform()\n"
                assert anchor in src["soc"], \
                    "gate 24d setup: platform construction anchor moved"
                src["soc"] = src["soc"].replace(blk.group(0), "\n", 1) \
                                       .replace(anchor, anchor + blk.group(0), 1)
            elif which == "plat_tdm":
                # break the ROUTED header rather than the absent one
                src["plat"] = plat_j11
                for ball in ("B22", "A20", "B20", "F20", "F19"):
                    src["plat"] = src["plat"].replace('Pins("%s")' % ball,
                                                      'Pins("")')
                cfgs = {"ax7101_8x8": CONFIGS["ax7101_8x8"]}
            else:
                anchor, mutant = payload
                assert anchor in src[which], \
                    f"gate 24d setup: anchor for '{label}' gone from {which}"
                src[which] = src[which].replace(anchor, mutant, 1)
            try:
                _front_end_routing(src, cfgs, argv_of)
            except AssertionError:
                n += 1
                continue
            raise AssertionError(
                f"gate 24c ACCEPTED a mutated tree - it cannot detect: {label}")
        finally:
            if tmp:
                os.unlink(tmp)
    print(f"  [gate 24d] {n}/{len(ROUTING_MUTATIONS)} routing mutations "
          f"REJECTED (arty tdm8/16/32 re-declared, i2s_mclk off the Pmod, "
          f"refusal deleted / mis-keyed / late / undefended, a routed header "
          f"losing its pins, a kind added on one side only, and the argv "
          f"itself selecting TDM for the Arty in BOTH tree states)")

def test_firmware_version_derived_from_rtl():
    """Gate 24: the version a controller reads is the version the fabric is.

    The ENTITY descriptor's firmware_version (IEEE 1722.1-2021 7.2.1
    Table 7-2, offset 116, 64 octets) is DERIVED from the gateware's own
    VERSION parameter, never declared beside it. Until 2026-07-28 all three
    configs hardcoded "0.1.0" while milan_csr said 0x0001_0016, so every
    board we ship told Hive it ran firmware 0.1.0.

    The literal is read out of the RTL here, so this gate follows a VERSION
    bump instead of pinning one - a hardcoded expectation would be the same
    second copy the gate exists to forbid."""
    csr = open(os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")).read()
    m = re.search(r"parameter\s+logic\s*\[31:0\]\s+VERSION\s*=\s*"
                  r"32'h([0-9A-Fa-f_]+)", csr)
    assert m, "milan_csr.sv has no VERSION parameter"
    v = int(m.group(1).replace("_", ""), 16)
    major, minor = (v >> 16) & 0xFFFF, v & 0xFFFF
    want = f"{major}.{minor}.0"

    # every shipped config derives it, and none of them declares it
    ids = {}
    for name, path in CONFIGS.items():
        raw = yaml.safe_load(open(path))["entity"]
        assert "firmware_version" not in raw, \
            f"{name}: config re-declares entity.firmware_version"
        cfg = eb.load_config(path)
        assert cfg["entity"]["firmware_version"] == want, \
            (f"{name}: firmware_version {cfg['entity']['firmware_version']!r} "
             f"!= {want!r} derived from VERSION 0x{v:08X}")
        assert cfg["entity"]["firmware_rev"] == 0
        ids[name] = cfg["entity"]["entity_model_id"]

    # 1722.1-2021 6.2.2.8 EXCLUDES firmware_version from what makes an entity
    # model "changed" ("In the ENTITY descriptor: available_index,
    # association_id, entity_name, firmware_version, group_name,
    # serial_number and current_configuration"), so no entity_model_id may
    # move with it - least of all arty_current's PINNED deployed identity.
    assert "firmware_version" not in eb.model_shape(
        eb.load_config(CONFIGS["arty_4x4"])), \
        "firmware_version leaked into the model-id hash input (6.2.2.8)"
    assert ids["arty_current"] == DEPLOYED_MODEL_ID
    assert eb.load_config(CONFIGS["arty_current"])["model_id"]["source"] == "pin"

    # the rev knob moves the string and NOTHING else
    p = _variant(CONFIGS["arty_4x4"],
                 lambda c: c["entity"].__setitem__("firmware_rev", 7))
    try:
        r = eb.load_config(p)
        assert r["entity"]["firmware_version"] == f"{major}.{minor}.7"
        assert r["entity"]["entity_model_id"] == ids["arty_4x4"], \
            "firmware_rev moved the entity_model_id (6.2.2.8 violation)"
    finally:
        os.unlink(p)

    # and it reaches the descriptor bytes at the standard's offset
    sys.path.insert(0, os.path.join(ROOT, "avdecc"))
    import gen_aem_store as g
    for name in CONFIGS:
        cfg = eb.load_config(CONFIGS[name])
        M = g.build_model(g.spec_from_overlay(eb.emit_aem_overlay(cfg)))
        base = next(b for (t, i, b, _l) in M["directory"] if (t, i) == (0, 0))
        fld = M["rom"][base + 116: base + 116 + 64]
        assert fld == want.encode() + bytes(64 - len(want)), \
            f"{name}: ENTITY+116 is not a zero-padded {want!r} (7.2/7.2.1)"

    # rejections: a declared version, and a rev that is not a count
    bad = [("declared firmware_version", "firmware_version", "0.1.0"),
           ("negative rev", "firmware_rev", -1),
           ("non-integer rev", "firmware_rev", "3"),
           ("bool rev", "firmware_rev", True)]
    for label, key, val in bad:
        p = _variant(CONFIGS["arty_4x4"],
                     lambda c, k=key, x=val: c["entity"].__setitem__(k, x))
        try:
            try:
                eb.load_config(p)
            except eb.ConfigError:
                pass
            else:
                raise AssertionError(f"{label}: accepted")
        finally:
            os.unlink(p)

    print(f"  [gate 24] firmware_version DERIVED from milan_csr VERSION "
          f"0x{major:04X}_{minor:04X} -> {want!r}: 3/3 configs derive it and "
          f"declare none, it lands zero-padded at ENTITY+116 in all 3 ROMs "
          f"(1722.1 7.2.1 Table 7-2), no entity_model_id moves with it "
          f"(6.2.2.8 exclusion; arty_current still pinned "
          f"{DEPLOYED_MODEL_ID}), firmware_rev 7 -> {major}.{minor}.7 with "
          f"the same id, 4/4 bad declarations refused")
def _pools_variant(base, phys, pools, mutate=None):
    def m(c):
        c["audio_interface"]["physical_channels"] = phys
        c["audio_interface"]["cluster_mapping"] = {"policy": "role-pools",
                                                   "pools": pools}
        if mutate:
            mutate(c)
    return _variant(CONFIGS[base], m)


def test_d8_role_pools():
    """gate 24a - D8: the port's cluster block is the sum of its declared
    role pools, every width derived from the platform declaration, and the
    static AUDIO_MAP falls through to the pool that can actually source the
    stream. The AX case (a board that routes NO audio pins) is the one the
    round exists for."""
    # (a) the AX shape as shipped: 0 physical, host 8, pilot, loopback 8
    r = eb.build(CONFIGS["ax7101_8x8"], OUT)
    ovl = r["overlay"]
    check_port_layout(ovl, 8, 8)
    assert ovl["cluster_policy"] == "role-pools"
    assert ovl["physical_binding"]["physical_channels"] == \
        {"capture": 0, "render": 0}, "the AX routes no audio pins"
    P_in, P_out = ovl["stream_ports"]["input"], ovl["stream_ports"]["output"]
    assert all(p["clusters"] == 8 for p in P_in), P_in         # host only
    assert all(p["clusters"] == 17 for p in P_out), P_out      # 8 + 1 + 8
    assert ovl["descriptor_counts"]["AUDIO_CLUSTER"] == 8*8 + 8*17 == 200
    assert all(g["role"] != "physical" for p in P_in + P_out for g in p["pool"]), \
        "a board with 0 routed channels must emit NO physical clusters"
    # (b) the primary segment: listeners fall through to host, talkers to
    #     LOOPBACK - which is the whole point (USER 2026-07-28)
    assert all(p["primary_role"] == "host" for p in P_in)
    assert all(p["primary_role"] == "loopback" for p in P_out)
    for p in P_out:
        m = next(m for m in ovl["audio_maps"] if m["index"] == p["base_map"])
        lb = next(g for g in p["pool"] if g["role"] == "loopback")
        assert all(lb["offset"] <= off < lb["offset"] + lb["width"]
                   for (_, _, off, _) in m["mappings"]), m
    # (c) per-talker DISTINCT loopback sources: talker t defaults to rx
    #     stream t, so eight talkers see eight different sources
    byport = {}
    for c in ovl["audio_clusters"]:
        if c["role"] == "loopback":
            byport.setdefault(c["port_index"], []).append(c["name"])
    assert len(byport) == 8
    assert byport[0][0] == "Loopback S0 ch 0" and byport[7][0] == "Loopback S7 ch 0"
    assert len({tuple(v) for v in byport.values()}) == 8, \
        "every talker port must offer a DIFFERENT loopback source set"
    print(f"  [gate 24a] ax7101_8x8 role-pools: 200 AUDIO_CLUSTERs "
          f"(8x host8 in; 8x host8+pilot1+loopback8 out), 0 physical because "
          f"the board routes none, talker map -> loopback, 8 distinct sources")

    # (d) physical pool APPEARS when the platform declares routed channels
    p = _pools_variant("ax7101_8x8", {"capture": 16, "render": 16},
                       {"host": 2, "pilot": True, "loopback": 2})
    try:
        r = eb.build(p, os.path.join(OUT, "_pools"))
        P = r["overlay"]["stream_ports"]["output"][0]
        assert [g["role"] for g in P["pool"]] == \
            ["physical", "host", "pilot", "loopback"], P
        assert P["clusters"] == 16 + 2 + 1 + 2
        # with physical present the static map goes THERE, not to loopback
        assert P["primary_role"] == "physical"
        names = [c["name"] for c in r["overlay"]["audio_clusters"]
                 if c["port_index"] == 0 and c["direction"] == "output"]
        # Derived from the variant's own interface kind, not hardcoded: the
        # ax7101 shape moved tdm16 -> tdm32 when the MASTER front-end landed
        # (USER: "do not use TDM8 use TDM32 then"), and a role name that
        # restates the config is a test that breaks on a legitimate change
        # rather than on a defect (methodology R4).
        pfx = eb.load_config(p)["interface"]["kind"].upper()
        assert names[:2] == [f"{pfx} In 0", f"{pfx} In 1"], (names[:4], pfx)
        assert "Pilot Tone" in names
    finally:
        os.unlink(p)
    print("  [gate 24a] declaring routed channels re-introduces the physical "
          "pool AND moves the static map onto it (primary-role fallthrough)")

    # (e) BOUNDARY: a 64-wide loopback pool is the shape D8 sketches and D6
    #     predicted could not be stored - it must VALIDATE and be marked, not
    #     crash and not silently wrap the 16-bit ROM address space.
    p = _pools_variant("ax7101_8x8", {"capture": 16, "render": 16},
                       {"host": 8, "pilot": True, "loopback": 64})
    try:
        r = eb.build(p, os.path.join(OUT, "_pools"))
        assert r["overlay"]["descriptor_counts"]["AUDIO_CLUSTER"] == \
            8*(16+8) + 8*(16+8+1+64), r["overlay"]["descriptor_counts"]
        assert r["aem_rom_svh"] is None, "a 64 KiB+ ROM must NOT be emitted"
        assert "16-bit" in r["aem_rom_unsupported"], r["aem_rom_unsupported"]
        # builder contract: it VALIDATES and lands in the plan, never errors
        assert "planned" in r["plan"]
        try:
            eb.build(p, os.path.join(OUT, "_pools"), write_rtl=True)
            assert False, "--write-rtl must refuse a shape with no ROM"
        except eb.ConfigError as e:
            assert "cannot be built" in str(e), e
    finally:
        os.unlink(p)
    print("  [gate 24a] the full 64-wide D8 pool VALIDATES, exceeds the "
          "16-bit AEM store address space, is marked rather than emitted, "
          "and --write-rtl REFUSES it (D6 is the owner)")


def test_d8_role_pools_reject():
    """gate 24b - the NEGATIVE control. Every one of these configs is wrong
    in a way that would otherwise ship a model the fabric cannot back."""
    bad = [
        # pools under a policy that does not read them = two meanings at once
        ("pools ignored by policy", "ax7101_8x8",
         lambda c: c["audio_interface"]["cluster_mapping"].__setitem__(
             "policy", "cap-at-interface")),
        # more routed channels than the interface family carries
        # ONE MORE than whatever this interface family actually carries -
        # derived, not the literal 17 that was right only while the shape was
        # tdm16. It moved to tdm32 when the MASTER front-end landed, and a
        # fixture that restates the config stops testing the rule the moment
        # the config legitimately changes (methodology R4).
        ("physical > interface width", "ax7101_8x8",
         lambda c: c["audio_interface"].__setitem__(
             "physical_channels",
             {"capture": eb.INTERFACES[c["audio_interface"]["kind"]]["channels"] + 1,
              "render": 0})),
        ("negative physical", "ax7101_8x8",
         lambda c: c["audio_interface"].__setitem__(
             "physical_channels", {"capture": -1, "render": 0})),
        ("physical_channels not a mapping", "ax7101_8x8",
         lambda c: c["audio_interface"].__setitem__("physical_channels", 8)),
        ("unknown physical_channels key", "ax7101_8x8",
         lambda c: c["audio_interface"].__setitem__(
             "physical_channels", {"capture": 0, "playback": 0})),
        ("unknown pool key", "ax7101_8x8",
         lambda c: c["audio_interface"]["cluster_mapping"].__setitem__(
             "pools", {"host": 8, "tdm": 8})),
        # every pool zero => a STREAM_PORT with no cluster block at all
        ("all pools zero", "ax7101_8x8",
         lambda c: c["audio_interface"]["cluster_mapping"].__setitem__(
             "pools", {"host": 0, "pilot": False, "loopback": 0})),
        ("unknown policy", "ax7101_8x8",
         lambda c: c["audio_interface"]["cluster_mapping"].__setitem__(
             "policy", "role-pool")),
    ]
    for why, base, mut in bad:
        p = _variant(CONFIGS[base], mut)
        try:
            eb.build(p, os.path.join(OUT, "_pools_bad"))
            assert False, f"accepted a config it must refuse: {why}"
        except eb.ConfigError:
            pass
        finally:
            os.unlink(p)
    print(f"  [gate 24b] {len(bad)}/{len(bad)} contradictory pool configs "
          "REFUSED with ConfigError")


def test_d10_cluster_names():
    """gate 24c - D10: every AUDIO_CLUSTER is named for what it IS, and the
    rename does NOT move entity_model_id.

    1722.1-2021 6.2.2.8 lists `object_name` among the fields that do NOT
    constitute "the structure of an ATDECC Entity data model" (alongside
    entity_name, firmware_version, serial_number, current_format, ...), so a
    name change must keep the id AND controllers must be able to SET_NAME it
    at runtime. This gate proves both directions: names change -> id frozen;
    pool shape changes -> id moves."""
    for name in CONFIGS:
        r = eb.build(CONFIGS[name], OUT)
        ovl = r["overlay"]
        cl = sorted(ovl["audio_clusters"], key=lambda c: c["index"])
        assert len(cl) == ovl["descriptor_counts"]["AUDIO_CLUSTER"]
        assert all(c["name"] not in ("Input", "Output") for c in cl), \
            f"{name}: a cluster is still named the pre-D10 placeholder"
        assert all(len(c["name"].encode()) <= 63 for c in cl), \
            "object_name must fit the 64-byte field (7.2.16)"
        # role and name must agree - a "Pilot Tone" string on a host cluster
        # would be exactly the lie D10 exists to remove
        for c in cl:
            if c["role"] == "pilot":
                assert c["name"] == "Pilot Tone", c
            elif c["role"] == "loopback":
                assert c["name"].startswith("Loopback S"), c
            elif c["role"] == "host":
                assert c["name"].startswith("Host "), c
            elif c["role"] == "virtual":
                assert c["name"].startswith("Virtual "), c
            else:
                assert c["name"].split()[0] in eb.IFACE_LABEL.values(), c
    # the DEPLOYED arty shape: physical first, virtual tail (the wire-truth
    # rule is stated per DIRECTION, and the Pmod I2S2 is a 2-channel link)
    ovl = eb.build(CONFIGS["arty_current"], OUT)["overlay"]
    names = [c["name"] for c in sorted(ovl["audio_clusters"],
                                       key=lambda c: c["index"])]
    assert names == ["I2S Out 0", "I2S Out 1"] \
        + [f"Virtual Out {n}" for n in range(2, 8)] \
        + ["I2S In 0", "I2S In 1"] \
        + [f"Virtual In {n}" for n in range(2, 8)], names

    # 6.2.2.8: renaming must NOT move the id ...
    base = eb.load_config(CONFIGS["ax7101_8x8"])
    p = _variant(CONFIGS["ax7101_8x8"],
                 lambda c: c["streams"]["talkers"][0].__setitem__(
                     "name", "Renamed Talker"))
    try:
        assert eb.load_config(p)["model_id"]["hash"] == \
            base["model_id"]["hash"], "a stream NAME moved the model id"
    finally:
        os.unlink(p)
    # ... but a pool WIDTH must, because it changes the descriptor set
    p = _pools_variant("ax7101_8x8", {"capture": 0, "render": 0},
                       {"host": 8, "pilot": True, "loopback": 4})
    try:
        assert eb.load_config(p)["model_id"]["hash"] != \
            base["model_id"]["hash"], "a pool WIDTH left the model id frozen"
    finally:
        os.unlink(p)
    # ... and every config that predates D8 must hash EXACTLY as before
    assert eb.load_config(CONFIGS["arty_current"])["model_id"]["hash"] == \
        "0x001BC5AB73EC9D1D"
    # arty_4x4's hash has now moved THREE times, correctly every time:
    # 0x001BC565E07E0DD6 -> 0x001BC5C42E0CEE8B when the per-board routing
    # gate forced tdm8 -> i2s_philips (no header existed), ->
    # 0x001BC578CBCE5FBD when HANDOVER 8.3b routed the pmodb header and the
    # shape went back to tdm8 (now with 4-cluster talkers, the emitted
    # width), and -> 0x001BC5A10610BAB8 when roadmap 23 put every listener
    # on map_mode dynamic, which DROPS four AUDIO_MAP descriptors and sets
    # number_of_maps=0 on four STREAM_PORT_INPUTs. `interface.kind` and the
    # descriptor set both ARE model-shaping, so a shape change SHOULD move a
    # hash-derived id - that is the mechanism working. What must NOT move is
    # arty_current's PINNED id above (it stays static), and it has not.
    assert eb.load_config(CONFIGS["arty_4x4"])["model_id"]["hash"] == \
        "0x001BC5A10610BAB8"
    print("  [gate 24c] every cluster named for its ROLE; renaming leaves "
          "entity_model_id frozen (1722.1 6.2.2.8 exclusion list) while a "
          "pool width moves it; the two pre-D8 shapes hash unchanged")


def test_d10_names_reach_the_rom():
    """gate 24d - the names survive the WHOLE path (overlay ->
    gen_aem_store -> ROM bytes), and the ROM the TB compares against is
    regenerated with it.

    This gate exists because of HOW the first attempt failed: the builder's
    `--write-rtl` writes hdl/.../aecp_aem_rom.svh but NOT
    tb/verilator/aecp/aem_golden.h, whose only writer is
    `python3 avdecc/gen_aem_store.py`. Regenerating one and not the other
    turned the aecp byte-exact sweep red on all 16 AUDIO_CLUSTER
    descriptors (off=42 - the object_name field) and nothing else."""
    sys.path.insert(0, os.path.join(ROOT, "avdecc"))
    import gen_aem_store as g
    ovl = eb.build(CONFIGS["arty_current"], OUT)["overlay"]
    M = g.build_model(g.spec_from_overlay(ovl))
    # find the AUDIO_CLUSTER images and read their object_name out of the ROM
    got = []
    for (t, i, base, ln) in M["directory"]:
        if t == 0x0014:
            got.append(M["rom"][base+4:base+4+64].split(b"\0")[0].decode())
    assert got == [c["name"] for c in sorted(ovl["audio_clusters"],
                                             key=lambda c: c["index"])], got
    # the TRACKED artifacts must both carry them (the aem_golden.h lesson)
    rom = open(TRACKED_SVH, "rb").read()
    gpath = os.path.join(ROOT, "tb/verilator/aecp/aem_golden.h")
    gtext = open(gpath).read()
    body = gtext.split("AEM_ROM[] = {", 1)[1].split("};", 1)[0]
    gbytes = bytes(int(x, 16) for x in re.findall(r"0x([0-9A-Fa-f]{2})", body))
    assert gbytes == M["rom"], \
        (f"{gpath} does not match the ROM this config generates ("
         f"{len(gbytes)} vs {len(M['rom'])} B) - it is STALE. Its ONLY "
         "writer is `python3 avdecc/gen_aem_store.py`; the builder's "
         "--write-rtl writes hdl/.../aecp_aem_rom.svh and NOT this file, "
         "which is exactly how the first D10 attempt turned the aecp "
         "byte-exact sweep red on all 16 AUDIO_CLUSTER descriptors.")
    for nm in ("I2S Out 0", "Virtual In 7"):
        assert nm.encode() in gbytes, f"golden ROM has no cluster '{nm}'"
    # and the generated svh must equal the tracked one byte for byte
    assert g.emit_svh_text(M).encode() == rom, \
        "tracked aecp_aem_rom.svh is not what this config generates"
    print("  [gate 24d] role names reach the ROM bytes; the tracked svh AND "
          "tb/verilator/aecp/aem_golden.h both carry them (the file the "
          "builder's --write-rtl does NOT write)")


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
               test_platform_dt_and_driver_shape, test_platform_rejects,
               test_csr_defaults_header_consumed, test_csr_defaults_rejects,
               test_aes3_interface_switch, test_aes3_rejects,
               test_cbs_reset_table_single_source,
               test_optional_blocks_default_present,
               test_optional_block_gates_bite,
               test_optional_block_prune_accounting,
               test_optional_block_names_reach_the_rtl,
               test_tdm_master_binding_reaches_the_pins,
               test_tdm_master_binding_gate_bites,
               test_front_end_routing_per_board,
               test_front_end_routing_gate_bites,
               test_i2s_pair_blend_binding,
               test_i2s_pair_blend_gate_bites,
               test_firmware_version_derived_from_rtl,
               test_d8_role_pools, test_d8_role_pools_reject,
               test_d10_cluster_names, test_d10_names_reach_the_rom):
        print(f"{fn.__name__}:")
        fn()
    print("ALL GATES PASS")
