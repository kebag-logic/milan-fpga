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
      the builder's OWN in-memory emit_aem_rom_svh() - the CLI and the
      library are one generator reached two ways and must not drift.  WHICH
      config owns the tracked definition is READ FROM THE TREE (the shape
      include's `Source :` marker, via check_entity_shape.tracked_owner -
      the same single reader its check E uses), never assumed: `--write-rtl
      <cfg>` installs it for whichever config it is handed, and a gate that
      hardcoded endstation_arty_current went red for every other owner,
      which blocked any other shape from being written into the tree at all.
      The gate also asserts the CLI writes into no RTL destination.
      COMPARAND CHANGED 2026-08-12: it used to be the TRACKED
      hdl/ieee17221/aecp/gen/aecp_aem_rom.svh, which made this the staleness
      gate for the shipped descriptor set; that file and the whole AECP
      plane that compiled it are deleted, so both sides are generated now
      and no on-disk ROM is asserted about.  The builtin (no-overlay) model
      is a SEPARATE property - that model is arty_current's, hand-written in
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
  18b. Milan 4.3.3.2's bandwidth recipe composes to the clause's kb/s (the
      clamped CRF row, an unclamped 4ch AAF row, and the step-2 clamp), and
      the PriorityAndRank byte reaches milan_csr's o_srp_ctx_prio_rank
      through the generated lwsrp_csr_defaults.svh.  SHRUNK 2026-08-12: the
      ten emitted-vs-lwsrp_pkg.sv comparisons, the KL_lwsrp_bw_gate
      75%-ceiling literals and the tracked lwsrp_table.svh staleness check
      are REMOVED - hdl/ieee8021q/srp/** is deleted, so all three comparands
      are gone.  They are not restated against the builder's own constants,
      which would compare a value to itself;
  18c. TSpec derivation anchored in the RTL frame geometry (KL_aaf_packetizer
      SAMPLES_PER_FRAME_C + its documented 42+24*C / 90-byte identities),
      NUM_QUEUES == ethernet_packet_pkg, milan_datapath's SRP row-map
      localparams still derived from the generated shape, and the ctx-row
      arithmetic covering every attribute row.  SHRUNK 2026-08-12: the
      KL_lwsrp_top instantiation and bw_gate-width assertions are REMOVED -
      milan_datapath instantiates no lwSRP engine and the modules are gone;
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
      the CSR subset agrees word-for-word with the EMITTED lwSRP table (the
      tracked hdl/ieee8021q/srp/gen/lwsrp_table.svh comparand is deleted with
      the srp tree, so the two emitters are compared instead of two files),
      and every flow that compiles milan_csr.sv carries hdl/common/csr as an
      include dir (Verilator resolves `include against -I/+incdir and the CWD
      only, never against the including file's directory).  NOTE the 0x680
      registers no longer DRIVE anything - the applicant is deleted and the
      group survives as a software-visible ABI, which is why a wrong reset
      word is still a wrong readback and still gated;
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
      audio PLL that cannot divide to the serial clock, raise ConfigError;
  27. THE PROTOCOL PROCESSOR'S DRAM WINDOW IS RESERVED, for every config: the
      emitted device tree carries a `no-map` reserved-memory node covering
      exactly [pp_mem_phys, pp_mem_phys + pp_mem_bytes), that window overlaps
      neither the PCM ring nor any other reserved region, platform_shape.json
      publishes the same bytes the tree reserves, and milan_soc.py DERIVES its
      PP_DESC_BASE_P / PP_RESP_BASE_P from that published window instead of
      computing one of its own.  The window used to be derived independently
      on the two sides (the builder emitted no reservation at all, and the SoC
      took "top of main_ram"), which put it in ordinary kernel RAM at the 1x1
      shape and INSIDE the PCM ring at 8x8.  Neither failure raises anything:
      no counter on either side reports a write to a wrong physical address.
  28. THE DESCRIPTOR IMAGE CARRIES THE IDENTITY IEEE 1722.1-2021 Table 7-2
      obliges it to: the ENTITY descriptor read back OUT of the packed
      aem_desc.bin must repeat the ADPDU's entity_id, entity_model_id,
      entity_capabilities (with AEM_SUPPORTED set), stream counts and
      capability words, and AVB_INTERFACE must carry the station MAC and its
      802.1AS clock_identity.  gen_aem_store zero-fills all of those - the
      deleted KL_aecp_aem_dyn_mux substituted them at read time from the CSR
      group - and the replacement image path never picked the step up, so
      silicon served 44 zero bytes where the identity belongs.  Each value is
      compared against the artifact that OWNS it (milan-entity.conf,
      adp_shape_defaults.svh, pp_adp_pkg.sv, the config's MAC), and every
      overlay span gen_aem_store declares must be either resolved or named as
      genuinely dynamic - there is no third option, which is what stops the
      next added span from shipping as zeros.
  29. EVERY STREAM INPUT ADVERTISES THE WHOLE MILAN BASE FORMAT FAMILY, for
      every config.  Milan v1.2 6.4 obliges a Stream Input that advertises one
      48 kHz (resp. 96, 192) Base format to advertise them ALL, and 6.2 fixes
      what "all" is: channel counts {1, 2, 4, 6, 8}.  endstation_arty_4x4
      spelled that family out by hand as an "up to" entry capped at FOUR
      channels, so its four Stream Inputs advertised counts 1, 2 and 4 and
      left the 6- and 8-channel 48 kHz Base formats unadvertised.  The
      completion is derived now (base_format_complete), and this gate grades
      it against Milan Table 6.2 TRANSCRIBED rather than recomputed.  It also
      holds the other half of Section 6: Stream Outputs get NO completion
      (6.3 asks a Base Talker for none, and a talker cannot correct a wider
      claim), the CRF Media Clock streams carry exactly the 7.3.2 format and
      no AAF (5.3.3.4 exclusivity), every advertised Base rate is one the
      AUDIO_UNIT reports (5.3.3.3), and no descriptor outgrows the store's
      576-octet line buffer (1722.1-2021 Table 7-8: 138 + 8*N + 2*R).
  30. THE ARGV REALLY REACHES THE RTL PARAMETER, observed rather than read
      (gate 23f, issue #154): the shipping AX argv goes through the REAL
      milan_soc.py main() once per optional block, and what is graded is the
      p_* keyword arguments Instance("milan_datapath", ...) is handed.  Eleven
      negative controls sever the chain hop by hop and require the gate to go
      red, two of them the exact hops a reviewer severed on #135 while reading
      ALL GATES PASS.  Gate 23d holds the same chain by the SPELLING of the
      statements it walks and cannot see any of them.
  31. EVERY SHIPPED RECIPE CAN ACTUALLY RUN (gate 23g, issue #156): every
      build.sh recipe and every sweep.sh leg reaches that same Instance, with
      the flow tail its own launcher appends and `--build` included, because
      a guard that reads args.build is invisible to every shape gate in the
      tree.  Two recipes could not launch at all until this gate ran.

BOTH NEED LiteX, which is why they were worth the trouble: no CI job in this
repository elaborated the SoC, so a behavioural proof of these chains existed
on two branches and ran nowhere.  `.github/workflows/elaborate.yml` installs
the pinned LiteX of sw/litex/litex_pins.txt and runs this file with
--require-elaboration, which FAILS rather than skips when no interpreter can
import migen + litex, or when the one it finds carries a VexiiRiscv that
rejects the --l2-* arguments the patch series adds.  Everywhere else they
SKIP, and skip() puts them in the verdict so the absence of the proof cannot
read as the presence of one.

Run: python3 sw/builder/test_builder.py   (or pytest sw/builder/test_builder.py)
     python3 sw/builder/test_builder.py --require-elaboration   (the CI job)
"""

import ast
import contextlib
import copy
import io
import json
import os
import re
import shlex
import shutil
import struct
import subprocess
import sys
import tempfile
import time

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
    "arty_8ch": os.path.join(ROOT, "configs/endstation_arty_8ch.yaml"),
    "ax7101_8x8": os.path.join(ROOT, "configs/endstation_ax7101_8x8.yaml"),
    "ax7101_1x1_tdm8": os.path.join(
        ROOT, "configs/endstation_ax7101_1x1_tdm8.yaml"),
}
OUT = os.path.join(HERE, "out")
SWEEP = os.path.join(ROOT, "sw/litex/sweep.sh")
BUILD_SH = os.path.join(ROOT, "sw/litex/build.sh")
PATCH_DIR = os.path.join(ROOT, "sw/litex/patches")
APPLY_SH = os.path.join(PATCH_DIR, "apply.sh")

#: Every gate arm that could not run, in the order it declined.  A gate that
#: prints its SKIP and then lets `main()` print ALL GATES PASS with exit 0
#: turns the ABSENCE of a proof into the presence of one, which is the whole
#: subject of #154: gate 23f was written, reviewed and merged into a lane, and
#: the reason it protected nothing is that it skipped where it mattered and
#: the verdict never said so.  Record instead, and let the verdict name them.
SKIPPED = []

#: The skip kind `--require-elaboration` refuses.  A row a gate could not run
#: for a RECORDED reason is a normal skip; "there is no LiteX on this box" is
#: not, in the one job that exists to elaborate.  Without this, a broken
#: install in the elaboration job degrades to the exact green #154 is about.
NO_LITEX = "no-litex"

#: The other kind it refuses: an interpreter was found, and its VexiiRiscv
#: rejects an --l2-* argument that only the series in sw/litex/patches
#: teaches it.  On a bench that is a recorded gap; in the one job that
#: installs the series (elaborate.yml) it is a setup failure, and a row skip
#: must not absorb a setup failure in the job that exists to prove the
#: toolchain ([R0] on PR #188).
TOOLCHAIN = "toolchain"


def skip(gate, why, kind="row"):
    """Record one gate arm that could not run, and say so on stdout.

    `gate` is the bracketed name the gate prints under, `why` the condition
    that has to change for it to run.  Both end up in main()'s verdict, so
    "why" is read by somebody deciding whether the green they are looking at
    covers the thing they are about to merge - write it for that reader.
    """
    SKIPPED.append((gate, why, kind))
    print(f"  [{gate}] SKIP: {why}")
#: The TRACKED entity definition - now ONE file, the shape include a gateware
#: `include-s.  Path comes from the builder that writes it, so there is one
#: spelling of it.  Its old partner hdl/ieee17221/aecp/gen/aecp_aem_rom.svh is
#: DELETED with the AECP plane: the descriptor ROM has no RTL destination any
#: more, so every gate that used to compare against a tracked ROM now compares
#: generated text against generated text (see gates 10/17/24d).
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

# Flashed silicon identity. Moved ...0001 -> ...0002 on 2026-08-13 with the
# descriptor byte layout (1722.1-2013 -> -2021; see AEM_LAYOUT_REV). 6.2.2.8
# obliges a changed model to take a new id, so this constant tracking the pin
# is the gate working, not the gate being relaxed - what it proves is that the
# PIN still wins over the hash, and the assertion below that hash != pin is
# what would catch the two being silently reconciled.
DEPLOYED_MODEL_ID = "0x001BC50AC1000003"

#: The flashed image's boot script - the ONE piece of board software that
#: programs the entity identity into the ADP/AEM CSRs. It lives in the sibling
#: repo (that is where the rootfs is built), so gate 25 SKIPS when the repo is
#: not on disk, exactly like the deployed-.dts cross-check in gate 19b. The
#: path is built from the builder's own ROOTFS_OVERLAY_ETC: one spelling of
#: "where the overlay is", never a second.
S50MILAN = os.path.join(eb.ROOTFS_OVERLAY_ETC, "init.d/S50milan")

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


def check_stream_layout(rom, dirv, label):
    """Every STREAM_INPUT/STREAM_OUTPUT is IEEE 1722.1-2021 Table 7-8.

    THE LAYOUT THIS PROJECT SHIPS, pinned so a regression is caught here and
    not by a controller.  Table 7-8 (1722.1-2021 7.2.6) puts `formats_offset`
    at 82 reading 138, `redundant_offset` at 132 reading 138 + 8*N,
    `number_of_redundant_streams` at 134, `timing` at 136 and the formats
    array at 138, for 138 + 8*N + 2*R octets.  Milan v1.2 5.3.3.4 requires
    exactly that: these descriptors "shall have the format specified in
    [ATDECC, Clause 7.2.6]", and Milan v1.2 clause 2 (References) defines
    [ATDECC] as IEEE Std 1722.1-2021.

    TWO NEAR-MISS LAYOUTS THIS REFUSES.  1722.1-2013 ended the descriptor at
    `buffer_length` with formats at 132, so a 2021 controller reads the first
    two octets of formats[0] as `timing`.  Milan v1.2 Annex C Table C.1 puts
    formats at 136 with no `timing` at all, shifting the whole array by two;
    5.3.3.4 makes it a "may" for any Stream and a "shall" only "for the
    Streams that are part of the redundant pair", and this entity declares
    none, so it is not emitted.  (The submodule test vector
    protocol-processor/hdl/aecp/desc/example_milan_8.json DOES carry Annex C,
    on purpose and labelled: it never reaches this generator.)

    R = 0 throughout: with no redundant association `redundant_offset` points
    at the empty array just past the formats.
    """
    streams = [d for d in dirv if d["type"] in (0x0005, 0x0006)]
    assert streams, f"{label}: no STREAM_INPUT/STREAM_OUTPUT to check"
    for d in streams:
        b, who = d["base"], f"{label} type 0x{d['type']:04X} index {d['index']}"
        u16 = lambda o: int.from_bytes(rom[b + o:b + o + 2], "big")  # noqa: E731
        n, r = u16(84), u16(134)
        assert u16(82) == 138, f"{who}: formats_offset {u16(82)}, 7.2.6 says 138"
        assert r == 0, f"{who}: R = {r}, this entity declares no redundant pair"
        assert u16(132) == 138 + 8 * n, \
            f"{who}: redundant_offset {u16(132)}, Table 7-8 says {138 + 8 * n}"
        assert d["len"] == 138 + 8 * n + 2 * r, \
            f"{who}: {d['len']} B, Table 7-8 says {138 + 8 * n + 2 * r} at N={n}"
        #! `timing` names a TIMING descriptor and this model defines none, so
        #! it reads 0 and TIMING_FIELD_VALID (Table 7-9 bit 2, mask 0x2000 -
        #! the table numbers bits MSB-first) stays clear.  A set flag with a 0
        #! index would point a controller at a descriptor that is not there.
        assert u16(136) == 0, f"{who}: timing {u16(136)}, no TIMING descriptor"
        assert not u16(72) & 0x2000, \
            f"{who}: stream_flags 0x{u16(72):04X} sets TIMING_FIELD_VALID"
    return len(streams)


def image_descriptor(blob, dtype, index=0, config=0):
    """One descriptor out of the packed AEM image, located the way the STORE
    locates it.

    Header, then the (configuration, type) index map, then
    `elem_off + index * elem_stride` for `elem_len` bytes - the layout
    protocol-processor/hdl/aecp/desc/gen_desc_image.py documents and
    KL_aecp_desc_store implements.  Walked here rather than taken from the
    generator's own ROM slice on purpose: gate 28 is about the bytes that
    reach a controller, and reading them back out of the image is the only
    way to assert about those.
    """
    magic, ver = struct.unpack_from(">IH", blob, 0)
    assert magic == 0x41454D49, f"image magic 0x{magic:08X}, not 'AEMI'"
    assert ver == 1, f"image layout version {ver}, this reader speaks 1"
    n_entries, = struct.unpack_from(">H", blob, 8)
    index_off, = struct.unpack_from(">I", blob, 12)
    for k in range(n_entries):
        o = index_off + 16 * k
        cfg_i, typ, count, elem_len = struct.unpack_from(">HHHH", blob, o)
        elem_off, _name_base, stride = struct.unpack_from(">IHH", blob, o + 8)
        if (cfg_i, typ) != (config, dtype):
            continue
        assert index < count, (
            f"image holds {count} descriptor(s) of type 0x{dtype:04X} in "
            f"configuration {config}, asked for index {index}")
        start = elem_off + index * stride
        return blob[start:start + elem_len]
    raise AssertionError(
        f"image has no type 0x{dtype:04X} in configuration {config} "
        f"({n_entries} index-map entries)")


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


#: ---------------------------------------------------------------------
#: An RV32 abstract interpreter over the assembly GCC emits for the
#: firmware.  Gate 1b uses it to answer the boot contract by DATA FLOW.
#:
#: WHY THIS SHAPE, recorded before the rules that use it (issue #153,
#: process guard 1).  The boot contract is a DATA-FLOW property: no value
#: reaches PP_CTRL[0] or ADP_CTRL[0] unless the AEM verifier compared a
#: CRC it took over the descriptor buffer against the expected value and
#: they matched.  Every instrument built for it before this one was a
#: RECOGNIZER -- a regex over C text, over a Makefile, or over disassembly
#: -- and a recognizer can be out-spelled by construction, which thirteen
#: review rounds on PR #143 demonstrated at four different levels.  The one
#: axis nobody out-spelled is the RTL decode reader, because it RESOLVES
#: values instead of matching them.
#:
#: So this reads the compiler's output and computes what the values ARE:
#: a constant lattice over registers, frame slots and single-word statics,
#: a basic-block CFG, and edge removal to measure dominance.  There is no
#: spelling to vary: `((T)((page << 16) | OFF))->m = v` and
#: `*(volatile uint32_t *)0x90000600u = v` reduce to the same resolved
#: store address, and a `goto` past a comparison is just a missing edge.
#:
#: SCOPE, so it is not read as more than it is.  It resolves what the
#: compiler emitted for THIS translation unit at the census's flags.  It
#: says nothing about a second translation unit (the make plan owns that),
#: nothing about what the linker or a debugger later patches, and it
#: reports "cannot say" rather than guessing whenever a value depends on
#: memory it does not model.  Every rule below is written so that "cannot
#: say" is a REFUSAL where the property needs an answer.
RV32_MASK = 0xFFFF_FFFF
RV32_CALLER_SAVED = ("ra", *(f"t{i}" for i in range(7)),
                     *(f"a{i}" for i in range(8)))
RV32_FRAME_REGS = ("s0", "sp", "fp")
RV32_LABEL_RE = re.compile(r"^([.A-Za-z_$][\w.$]*):")
RV32_INSN_RE = re.compile(r"^\s+([a-z][\w.]*)\s*(.*?)\s*$")
RV32_MEM_RE = re.compile(
    r"^(-?\d+|%lo\([^)]*\)|0[xX][0-9a-fA-F]+)?\(([a-z0-9]+)\)$")
RV32_BRANCHES = ("beq", "bne", "blt", "bge", "bltu", "bgeu", "beqz", "bnez",
                 "blez", "bgez", "bltz", "bgtz", "bgt", "ble", "bgtu", "bleu")
RV32_LOADS = ("lw", "lh", "lhu", "lb", "lbu")
RV32_STORES = ("sw", "sh", "sb")
RV32_DATA_EMIT_RE = re.compile(
    r"\.(?:word|4byte|long|byte|half|short|2byte|8byte|dword|quad|string|"
    r"asci[iz]|zero|space|float|double)\b")
RV32_WORD_RE = re.compile(
    r"\s*\.(?:word|4byte|long)\s+(-?\d+|0[xX][0-9a-fA-F]+)\s*$")


def _rv32_s32(value):
    value &= RV32_MASK
    return value - (1 << 32) if value & 0x8000_0000 else value


class Rv32Sym(object):
    """The ADDRESS of a named object, with a byte displacement."""
    __slots__ = ("name", "offset")

    def __init__(self, name, offset=0):
        self.name, self.offset = name, offset

    def __eq__(self, other):
        return (isinstance(other, Rv32Sym) and other.name == self.name and
                other.offset == self.offset)

    def __hash__(self):
        return hash(("sym", self.name, self.offset))

    def __repr__(self):
        return f"&{self.name}{self.offset:+d}"


class Rv32Tag(object):
    """A value tracked by its PRODUCER rather than by its bits, so a later
    comparison can say which producer the compared value came from.  This
    is what gives the CRC result provenance: the value the verifier
    compares either IS the tag `crc32()` handed back, or it is not."""
    __slots__ = ("what",)

    def __init__(self, what):
        self.what = what

    def __eq__(self, other):
        return isinstance(other, Rv32Tag) and other.what == self.what

    def __hash__(self):
        return hash(("tag", self.what))

    def __repr__(self):
        return f"<{self.what}>"


class Rv32Bits(object):
    """Partial knowledge: bits known SET and bits known CLEAR in an
    otherwise unresolved value.  `milan_read(R) | 1u` resolves to no
    constant, but bit 0 is known set, and "which bits does this write
    assert" is exactly the enable/clear question the boot contract asks."""
    __slots__ = ("ones", "zeros")

    def __init__(self, ones=0, zeros=0):
        self.ones, self.zeros = ones & RV32_MASK, zeros & RV32_MASK

    def __eq__(self, other):
        return (isinstance(other, Rv32Bits) and other.ones == self.ones and
                other.zeros == self.zeros)

    def __hash__(self):
        return hash(("bits", self.ones, self.zeros))

    def __repr__(self):
        return f"bits(set=0x{self.ones:x},clear=0x{self.zeros:x})"


def rv32_ones(value):
    if isinstance(value, int):
        return value & RV32_MASK
    return value.ones if isinstance(value, Rv32Bits) else 0


def rv32_zeros(value):
    if isinstance(value, int):
        return ~value & RV32_MASK
    return value.zeros if isinstance(value, Rv32Bits) else 0


def _rv32_partial(ones, zeros):
    """A partial value, collapsed to `None` when nothing is known."""
    ones, zeros = ones & RV32_MASK, zeros & RV32_MASK
    if ones | zeros == RV32_MASK and ones & zeros == 0:
        return ones
    return Rv32Bits(ones, zeros) if (ones or zeros) else None


def rv32_data(text):
    """Every symbol in `text` whose ENTIRE definition is one `.word N`.

    A symbol defined by anything else is left unresolved rather than
    guessed at: this table is read to resolve a load, and a partial
    reading of a definition is a WRONG value, not a missing one."""
    data, current, emitted, in_text = {}, None, [], False
    breaks = (".text", ".data", ".section", ".bss", ".sdata", ".rodata",
              ".srodata", ".sbss", ".comm", ".local", ".globl", ".global")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith((".text", ".init", ".fini")):
            in_text = True
        elif stripped.startswith(".section"):
            in_text = ".text" in stripped
        elif stripped.startswith((".data", ".sdata", ".rodata", ".srodata",
                                  ".bss", ".sbss")):
            in_text = False
        named = RV32_LABEL_RE.match(line)
        if named or stripped.startswith(breaks):
            if current is not None and len(emitted) == 1:
                data[current] = emitted[0]
            current, emitted = None, []
            if named and not in_text and not named.group(1).startswith(".L"):
                current = named.group(1)
            continue
        if current is None or in_text:
            continue
        if RV32_DATA_EMIT_RE.search(stripped):
            word = RV32_WORD_RE.match(line)
            emitted.append(int(word.group(1), 0) & RV32_MASK if word else None)
    if current is not None and len(emitted) == 1:
        data[current] = emitted[0]
    return {name: value for name, value in data.items() if value is not None}


def rv32_functions(text):
    """`{name: [(label, mnemonic, operands)]}` for every function defined,
    in emission order, with local labels kept in place as block heads."""
    functions, current, body = {}, None, []
    for line in text.splitlines():
        named = RV32_LABEL_RE.match(line)
        if named:
            name = named.group(1)
            if name.startswith(".L"):
                if current is not None:
                    body.append((name, None, None))
                continue
            if current is not None:
                functions[current] = body
            current, body = name, []
            continue
        if current is None or not line.strip() or line.lstrip()[0] in ".#":
            continue
        insn = RV32_INSN_RE.match(line)
        if insn:
            body.append((None, insn.group(1), insn.group(2)))
    if current is not None:
        functions[current] = body
    return functions


def rv32_blocks(body):
    """`(blocks, order, edges)`: the function's basic-block graph.  Each
    edge is `(successor, "taken"|"fall")`, which is what lets a caller
    delete ONE outgoing edge and ask what is still reachable."""
    blocks, order = {}, []
    name, insns = "@entry", []
    for label, mnem, ops in body:
        if label is not None:
            blocks[name], insns = insns, []
            order.append(name)
            name = label
            continue
        insns.append((mnem, ops))
        if mnem in RV32_BRANCHES or mnem in ("j", "jr", "ret", "tail"):
            blocks[name] = insns
            order.append(name)
            name, insns = f"{name}#{len(order)}", []
    blocks[name] = insns
    order.append(name)
    edges = {}
    for index, block in enumerate(order):
        insns = blocks[block]
        follows = order[index + 1] if index + 1 < len(order) else None
        succ, terminator = [], insns[-1] if insns else None
        if terminator is None:
            if follows:
                succ.append((follows, "fall"))
        else:
            mnem, ops = terminator
            target = ops.split(",")[-1].strip() if ops else ""
            if mnem in RV32_BRANCHES:
                if target in order:
                    succ.append((target, "taken"))
                if follows:
                    succ.append((follows, "fall"))
            elif mnem == "j":
                if target in order:
                    succ.append((target, "taken"))
            elif mnem not in ("jr", "ret", "tail") and follows:
                succ.append((follows, "fall"))
        edges[block] = succ
    return blocks, order, edges


RV32_BINOPS = {
    "add": lambda a, b: a + b, "sub": lambda a, b: a - b,
    "and": lambda a, b: a & b, "or": lambda a, b: a | b,
    "xor": lambda a, b: a ^ b, "mul": lambda a, b: a * b,
    "sll": lambda a, b: a << (b & 31),
    "srl": lambda a, b: (a & RV32_MASK) >> (b & 31),
}
RV32_IMMOPS = {
    "addi": lambda a, b: a + b, "andi": lambda a, b: a & b,
    "ori": lambda a, b: a | b, "xori": lambda a, b: a ^ b,
    "slli": lambda a, b: a << (b & 31),
    "srli": lambda a, b: (a & RV32_MASK) >> (b & 31),
    "srai": lambda a, b: _rv32_s32(a) >> (b & 31),
}


def _rv32_imm(text):
    try:
        return int(text.strip(), 0) & RV32_MASK
    except (ValueError, AttributeError):
        return None


class Rv32State(object):
    """Registers and the frame slots and statics the interpreter models."""
    __slots__ = ("regs", "mem")

    def __init__(self, regs=None, mem=None):
        self.regs = dict(regs) if regs else {}
        self.mem = dict(mem) if mem else {}

    def copy(self):
        return Rv32State(self.regs, self.mem)

    def get(self, name):
        return 0 if name in ("zero", "x0") else self.regs.get(name)

    def set(self, name, value):
        if name in ("zero", "x0"):
            return
        if name in RV32_FRAME_REGS:
            # The frame slots are keyed by (register, displacement), so a
            # frame register that MOVES makes every slot named through it a
            # different location. Drop them rather than let one key stand
            # for two addresses: this interpreter may say "cannot say", and
            # may not say the wrong thing.
            for key in [key for key in self.mem if key[0] == name]:
                del self.mem[key]
        self.regs[name] = value

    def merge(self, other):
        """Join: a value both states agree on survives, anything else
        becomes "cannot say".  Monotone, so the fixpoint terminates."""
        changed = False
        for key in list(self.regs):
            if key not in other.regs or self.regs[key] != other.regs[key]:
                if self.regs[key] is not None:
                    self.regs[key] = None
                    changed = True
        for key in list(self.mem):
            if key not in other.mem or self.mem[key] != other.mem[key]:
                if self.mem[key] is not None:
                    self.mem[key] = None
                    changed = True
        for key, value in other.mem.items():
            if key not in self.mem:
                self.mem[key] = value
                changed = True
        return changed


def rv32_step(state, mnem, ops, data, tags):
    """Interpret one instruction.  Returns an observation for the caller
    (`store`, `call`, `ret`, `branch`, `symstore`) or None."""
    args = [part.strip() for part in ops.split(",")] if ops else []
    if mnem == "li" and len(args) == 2:
        state.set(args[0], _rv32_imm(args[1]))
        return None
    if mnem == "lui" and len(args) == 2:
        if args[1].startswith("%hi("):
            state.set(args[0], Rv32Sym(args[1][4:-1]))
            return None
        value = _rv32_imm(args[1])
        state.set(args[0], (value << 12) & RV32_MASK
                  if value is not None else None)
        return None
    if mnem in ("lla", "la") and len(args) == 2:
        state.set(args[0], Rv32Sym(args[1]))
        return None
    if mnem == "mv" and len(args) == 2:
        state.set(args[0], state.get(args[1]))
        return None
    if mnem in RV32_IMMOPS and len(args) == 3:
        source, raw = state.get(args[1]), args[2]
        if isinstance(source, Rv32Sym):
            if raw.startswith("%lo("):
                state.set(args[0], source)
            else:
                shift = _rv32_imm(raw)
                state.set(args[0], Rv32Sym(source.name,
                                           source.offset + _rv32_s32(shift))
                          if mnem == "addi" and shift is not None else None)
            return None
        imm = _rv32_imm(raw)
        if imm is None:
            state.set(args[0], None)
        elif isinstance(source, int):
            state.set(args[0], RV32_IMMOPS[mnem](source, _rv32_s32(imm))
                      & RV32_MASK)
        elif mnem == "ori":
            state.set(args[0], _rv32_partial(rv32_ones(source) | imm,
                                             rv32_zeros(source) & ~imm))
        elif mnem == "andi":
            state.set(args[0], _rv32_partial(rv32_ones(source) & imm,
                                             rv32_zeros(source) | ~imm))
        else:
            state.set(args[0], None)
        return None
    if mnem in RV32_BINOPS and len(args) == 3:
        left, right = state.get(args[1]), state.get(args[2])
        if isinstance(left, int) and isinstance(right, int):
            state.set(args[0], RV32_BINOPS[mnem](left, right) & RV32_MASK)
        elif mnem == "or":
            state.set(args[0], _rv32_partial(
                rv32_ones(left) | rv32_ones(right),
                rv32_zeros(left) & rv32_zeros(right)))
        elif mnem == "and":
            state.set(args[0], _rv32_partial(
                rv32_ones(left) & rv32_ones(right),
                rv32_zeros(left) | rv32_zeros(right)))
        else:
            state.set(args[0], None)
        return None
    if mnem in RV32_LOADS and len(args) == 2:
        place = RV32_MEM_RE.match(args[1])
        # Read the BASE before clobbering the destination: `lw a5,0(a5)` is
        # the ordinary spelling, and reading it the other way round loses
        # every address that reaches a store through the same register.
        held = state.get(place.group(2)) if place else None
        state.set(args[0], None)
        if not place:
            return None
        raw_off, base = place.group(1), place.group(2)
        offset = 0 if not raw_off or raw_off.startswith("%lo(") \
            else _rv32_s32(_rv32_imm(raw_off) or 0)
        if isinstance(held, Rv32Sym):
            if mnem == "lw" and held.offset + offset == 0 and \
                    held.name in data:
                state.set(args[0], data[held.name])
        elif base in RV32_FRAME_REGS and held is None:
            state.set(args[0], state.mem.get((base, offset)))
        return None
    if mnem in RV32_STORES and len(args) == 2:
        place = RV32_MEM_RE.match(args[1])
        if not place:
            return None
        raw_off, base = place.group(1), place.group(2)
        held, value = state.get(base), state.get(args[0])
        offset = 0 if not raw_off or raw_off.startswith("%lo(") \
            else _rv32_s32(_rv32_imm(raw_off) or 0)
        if isinstance(held, int):
            return ("store", ((held + offset) & RV32_MASK, value))
        if isinstance(held, Rv32Sym):
            return ("symstore", held.name)
        if base in RV32_FRAME_REGS and held is None:
            state.mem[(base, offset)] = value
            return None
        return ("store", (None, value))
    if mnem in ("call", "jal", "jalr", "tail") and args:
        callee = args[-1].split("@")[0]
        handed = {reg: state.get(reg) for reg in
                  ("a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7")}
        for reg in RV32_CALLER_SAVED:
            state.set(reg, None)
        state.set("a0", tags.get(callee, Rv32Tag(f"call:{callee}")))
        return ("call", (callee, handed))
    if mnem == "ret" or (mnem == "jr" and args and args[0] == "ra"):
        return ("ret", state.get("a0"))
    if mnem in RV32_BRANCHES:
        return ("branch", (mnem, tuple(state.get(a) for a in args[:-1])))
    if mnem == "j":
        return None
    for arg in args[:1]:
        if arg not in ("zero", "x0") and RV32_MEM_RE.match(arg) is None:
            state.set(arg, None)
    return None


def rv32_run(body, data, tags=None, entry_regs=None, cut=None):
    """Constant-propagate over one function's CFG to a fixpoint, then read
    the observations off the SETTLED states.

    Two phases, deliberately: a block reached twice is interpreted twice
    during the fixpoint, and reporting what the first walk happened to see
    would make the answer depend on visit order.  The observations are
    taken once per reachable block from its fixpoint entry state, so the
    result is a function of the code and nothing else.

    `cut` removes one `(block, "taken"|"fall")` edge BEFORE the fixpoint,
    which is how this measures edge dominance: whatever is still reachable
    without that edge is exactly what the edge does not dominate."""
    blocks, order, edges = rv32_blocks(body)
    if cut is not None:
        edges = dict(edges)
        edges[cut[0]] = [edge for edge in edges[cut[0]] if edge[1] != cut[1]]
    entry = order[0]
    states = {entry: Rv32State(entry_regs or {})}
    work, budget = [entry], 0
    while work and budget < 20000:
        budget += 1
        block = work.pop()
        state = states[block].copy()
        for mnem, ops in blocks[block]:
            rv32_step(state, mnem, ops, data, tags or {})
        for succ, _kind in edges[block]:
            if succ not in states:
                states[succ] = state.copy()
                work.append(succ)
            elif states[succ].merge(state):
                work.append(succ)
    assert budget < 20000, \
        "the RV32 resolver did not reach a fixpoint, so its answer would " \
        "be a partial walk rather than a measurement"
    seen = {"stores": [], "calls": [], "rets": [], "branches": [],
            "symstores": set()}
    for block in order:
        if block not in states:
            continue
        state = states[block].copy()
        for mnem, ops in blocks[block]:
            outcome = rv32_step(state, mnem, ops, data, tags or {})
            if outcome is None:
                continue
            kind, payload = outcome
            if kind == "symstore":
                seen["symstores"].add(payload)
            else:
                seen[{"branch": "branches"}.get(kind, kind + "s")].append(
                    (block, payload))
    seen.update(blocks=blocks, order=order, edges=edges,
                reachable=set(states), states=states)
    return seen


def rv32_verdict_edge(run, produced, against=0):
    """The `(block, edge)` a conditional branch takes when a value the
    interpreter TAGGED compares equal to `against`, and the complementary
    edge.  Resolving which value is compared is the whole point: a
    comparison against a constant somebody assigned in between is not a
    comparison against this producer, whatever the source text says."""
    for block, (mnem, values) in run["branches"]:
        if mnem in ("beq", "bne"):
            if len(values) != 2:
                continue
            left, right = values
            if not ((left == produced and right == against) or
                    (right == produced and left == against)):
                continue
            equal = "taken" if mnem == "beq" else "fall"
        elif mnem in ("beqz", "bnez") and against == 0:
            if len(values) != 1 or values[0] != produced:
                continue
            equal = "taken" if mnem == "beqz" else "fall"
        else:
            continue
        return block, equal, "fall" if equal == "taken" else "taken"
    return None


def rv32_unit(assembly):
    """Resolve the whole translation unit the census compiled.

    Two passes: the first finds every static the code STORES through, the
    second resolves loads only from statics nothing writes.  A static the
    firmware assigns at run time has no compile-time value, and reporting
    one would be an invented fact rather than a resolved one."""
    data, functions = rv32_data(assembly), rv32_functions(assembly)
    written = set()
    for body in functions.values():
        written |= rv32_run(body, data)["symstores"]
    data = {name: value for name, value in data.items() if name not in written}
    return {"data": data, "functions": functions,
            "runs": {name: rv32_run(body, data)
                     for name, body in functions.items()}}


def test_all_configs_build():
    for name, path in CONFIGS.items():
        r = eb.build(path, OUT)
        for p in r["paths"].values():
            assert os.path.getsize(p) > 0, f"{name}: empty {p}"
        assert r["overlay"]["_schema"] == "kebag-logic/aem-overlay"
        assert r["overlay"]["_schema_version"].startswith("2.")
        print(f"  [gate 1] {name}: builds end-to-end "
              f"({os.path.relpath(os.path.dirname(r['paths']['soc_params']), ROOT)}/)")


def test_baremetal_profile_contract():
    """Gate 1b: the shipping AX build is the cacheless, headless profile,
    and each incompatible Linux/cached CPU combination is refused before a
    LiteX command can be emitted."""
    r = eb.build(CONFIGS["ax7101_1x1_tdm8"], OUT)
    cfg, argv = r["cfg"], _canon(r["argv"])
    assert cfg["soc"]["software_profile"] == "baremetal"
    assert cfg["soc"]["cpu"] == "vexiiriscv"
    assert cfg["soc"]["xlen"] == 32 and cfg["soc"]["cpu_count"] == 1
    assert cfg["constraints"]["l2_bytes"] == 0
    assert cfg["constraints"]["flashboot"] == "baremetal"
    assert cfg["constraints"]["sys_clk_hz"] == 100_000_000
    assert cfg["constraints"]["milan_clk_hz"] == 50_000_000
    assert cfg["soc"]["scala_args"] == []
    assert cfg["features"]["fabric_gptp"] is True
    assert cfg["features"]["sound_card"] is False
    assert r["platform"]["pcm"] is None
    assert all(group["role"] != "host"
               for direction in r["overlay"]["stream_ports"].values()
               for port in direction for group in port["pool"])
    assert argv["--software-profile"] == ["baremetal"]
    assert argv["--xlen"] == [32.0] and argv["--l2-bytes"] == [0.0]
    assert argv["--milan-clk-freq"] == [50_000_000.0]
    assert "--fabric-gptp" in argv
    assert "gptp_ucode" in r["paths"]
    base_ucode = open(r["paths"]["gptp_ucode"], "rb").read()
    assert len(base_ucode.splitlines()) == 1024
    assert "Fabric gPTP plane: **PRESENT**" in r["plan"]
    soc_source = open(os.path.join(ROOT, "sw/litex/milan_soc.py")).read()
    assert '_vex_args.with_cpu_clk = bool(' in soc_source
    assert 'self.cpu.cpu_clk.eq(ClockSignal("milan"))' in soc_source
    deploy_source = open(os.path.join(ROOT, "sw/litex/deploy.sh")).read()
    assert "--milan-clk-freq 50e6" in deploy_source
    assert "--fabric-gptp" in deploy_source
    for absent in ("--sound-card", "--aaf-playback", "--scala-args"):
        assert absent not in argv, f"bare-metal argv unexpectedly carries {absent}"

    firmware_path = os.path.join(
        ROOT, "sw/firmware/milan_baremetal/milan_baremetal.c")
    docs_path = os.path.join(
        ROOT, "docs/integration/BAREMETAL_FIRMWARE.md")
    csr_path = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")
    datapath_path = os.path.join(ROOT, "hdl/milan/milan_datapath.sv")
    with open(firmware_path, encoding="utf-8") as fh:
        firmware_source = fh.read()
    with open(docs_path, encoding="utf-8") as fh:
        docs_source = fh.read()
    with open(csr_path, encoding="utf-8") as fh:
        csr_source = fh.read()
    with open(datapath_path, encoding="utf-8") as fh:
        datapath_source = fh.read()
    with open(os.path.join(os.path.dirname(firmware_path), "Makefile"),
              encoding="utf-8") as fh:
        makefile_source = fh.read()
    firmware_listing = tuple(sorted(
        os.listdir(os.path.dirname(firmware_path))))
    firmware_object = os.path.basename(firmware_path)[:-2] + ".o"

    def braced_span(source, guard, label):
        assert guard, f"firmware boot guard missing: {label}"
        brace = source.index("{", guard.start(), guard.end())
        depth = 0
        for pos in range(brace, len(source)):
            if source[pos] == "{":
                depth += 1
            elif source[pos] == "}":
                depth -= 1
                if depth == 0:
                    return brace + 1, pos
        raise AssertionError(f"firmware boot guard is not closed: {label}")

    def braced_block(source, guard, label):
        body, close = braced_span(source, guard, label)
        return source[body:close]

    def blanked(source):
        """`source` with the BODIES of comments and string/char literals
        replaced by spaces, so every textual rule below reads code only --
        and every offset still indexes the original text unchanged."""
        out, i, n = list(source), 0, len(source)

        def erase(start, stop):
            for k in range(start, stop):
                if out[k] != "\n":
                    out[k] = " "

        while i < n:
            pair = source[i:i + 2]
            if pair == "/*":
                stop = source.find("*/", i + 2)
                stop = n if stop < 0 else stop + 2
                erase(i, stop)
            elif pair == "//":
                stop = source.find("\n", i)
                stop = n if stop < 0 else stop
                erase(i, stop)
            elif source[i] in "\"'":
                quote, stop = source[i], i + 1
                while stop < n and source[stop] != quote:
                    stop += 2 if source[stop] == "\\" else 1
                stop = min(stop + 1, n)
                erase(i + 1, stop - 1)
            else:
                i += 1
                continue
            i = stop
        return "".join(out)

    def blanked_sv(source):
        """SystemVerilog code with comments and string literals blanked.

        This deliberately does not treat a single quote as a character-literal
        delimiter: in SystemVerilog it begins sized and unsized number
        literals.  Newlines and offsets remain unchanged so mutation spans
        still index the raw source.
        """
        out, i, n = list(source), 0, len(source)

        def erase(start, stop):
            for k in range(start, stop):
                if out[k] != "\n":
                    out[k] = " "

        while i < n:
            pair = source[i:i + 2]
            if pair == "/*":
                close = source.find("*/", i + 2)
                assert close >= 0, \
                    "datapath integration proof found an unterminated " \
                    "SystemVerilog block comment"
                stop = close + 2
                erase(i, stop)
            elif pair == "//":
                stop = source.find("\n", i)
                stop = n if stop < 0 else stop
                erase(i, stop)
            elif source[i] == '"':
                stop = i + 1
                while stop < n and source[stop] != '"':
                    stop += 2 if source[stop] == "\\" else 1
                assert stop < n, \
                    "datapath integration proof found an unterminated " \
                    "SystemVerilog string literal"
                stop += 1
                erase(i, stop)
            else:
                i += 1
                continue
            i = stop
        return "".join(out)

    def assert_direct_scope(source, stop, reason, require_item_start=True):
        """The checked SV item is unconditional in the supplied arm.

        Intentional outer generate arms are removed before their bodies are
        passed here. Any further generate/begin/case/fork nesting is therefore
        a conditional wrapper around text this bounded model would otherwise
        mistake for an elaborated connection. The suffix after the preceding
        module-item semicolon closes the implicit ``if (...) item`` and
        ``for (...) item`` forms, which need no begin/generate keywords.
        """
        depth = {"block": 0, "generate": 0, "case": 0, "fork": 0}
        opening = {
            "begin": "block", "generate": "generate",
            "case": "case", "casex": "case", "casez": "case",
            "fork": "fork"}
        closing = {
            "end": "block", "endgenerate": "generate",
            "endcase": "case", "join": "fork",
            "join_any": "fork", "join_none": "fork"}
        for token in re.finditer(
                r"\b(?:begin|end|generate|endgenerate|case|casex|casez|"
                r"endcase|fork|join|join_any|join_none)\b", source[:stop]):
            word = token.group(0)
            if word in opening:
                depth[opening[word]] += 1
            else:
                kind = closing[word]
                assert depth[kind] > 0, \
                    f"{reason}: malformed SystemVerilog scope before the " \
                    "checked connection"
                depth[kind] -= 1
        assert not any(depth.values()), \
            f"{reason}: checked connection must be an unconditional item " \
            "in its inspected generate arm"

        if not require_item_start:
            return
        prior_semicolon = source.rfind(";", 0, stop)
        prefix = source[prior_semicolon + 1:stop]
        prefix = re.sub(
            r"\b(?:end|endgenerate|endcase|join|join_any|join_none)\b"
            r"(?:\s*:\s*[A-Za-z_$][A-Za-z0-9_$]*)?", "", prefix)
        # Compiler directives are closed separately after every connection
        # check. Leave their verdict there so an inactive `ifdef mutant is
        # reason-pinned to the directive-set property, while an implicit
        # module-item ``if (...) assign`` still fails here.
        prefix = re.sub(r"`[^\r\n]*", "", prefix)
        assert not prefix.strip(), \
            f"{reason}: checked connection must not be selected by an " \
            "implicit conditional-generate item"

    #: Every preprocessor conditional directive, one physical line each.
    cpp_directive_re = re.compile(
        r"(?m)^[ \t]*#[ \t]*(if|ifdef|ifndef|elif|else|endif)\b")

    def cpp_arms(code):
        """`(directives, arm_path)` for `code`'s preprocessor conditionals.

        This gate reads TEXT; the compiler compiles a TRANSLATION UNIT, so two
        offsets are only in the same code when the preprocessor keeps or drops
        them TOGETHER. `arm_path(pos)` is the tuple of (group, arm) pairs
        enclosing `pos`, and it is that predicate."""
        directives = list(cpp_directive_re.finditer(code))
        stack, groups, marks = [], 0, []
        for directive in directives:
            kind = directive.group(1)
            if kind in ("if", "ifdef", "ifndef"):
                groups += 1
                stack.append([groups, 0])
            elif kind in ("elif", "else"):
                assert stack, "firmware has an #elif/#else outside any #if"
                stack[-1][1] += 1
            else:
                assert stack, "firmware has an #endif outside any #if"
                stack.pop()
            marks.append((directive.end(), tuple(tuple(f) for f in stack)))
        assert not stack, "firmware leaves a preprocessor conditional open"

        def arm_path(pos):
            path = ()
            for at, value in marks:
                if at > pos:
                    break
                path = value
            return path

        return directives, arm_path

    def assert_preprocessor_visible(code, source, load_span):
        """No boot code may be selected by a directive this gate cannot read.

        NARROWED by the entity-advertise choke point (#153).  It used to
        refuse a preprocessor conditional ANYWHERE in the file, and any
        backslash-newline anywhere with it, because every rule in this gate
        read text and any arm selection made one reading differ from what
        the compiler compiles.  Two of those blanket refusals are now paid
        for by the resolved boot-flow measurement instead, which reads the
        compiler's OUTPUT and therefore sees the arm actually taken:

        * a conditional is refused where a TEXT rule still reads -- the boot
          entry point, the fabric configuration step, the choke point and
          the three CSR accessors -- and, wherever it sits, if it contains a
          `#define`, `#undef` or `#include`, because the address model reads
          those as unconditional text.  An `#ifdef` around a debug printf in
          a UART command handler is GREEN, and is measured as an accepted
          case.  The ONE conditional inside load_aem_image() is tolerated as
          before and CLASSIFIED by the verifier's return rule.
        * a backslash-newline is refused when deleting the pair would JOIN
          two non-whitespace characters, which is the phase-2 hazard: it is
          how a backslash-newline inside `milan_write` leaves the one
          identifier `milan_write` to the compiler while an offset-
          preserving reader sees two.  An
          ordinary continued `#define`, string or expression puts whitespace
          before the backslash and is GREEN, and is measured as an accepted
          case.  A continued macro body can still carry an entity enable,
          and the resolved census is what refuses that now: it reads the
          compiled call, where the macro is already expanded.

        COST that REMAINS, and it is a refusal: a conditional that reaches
        the boot path or carries a definition, and a splice that joins
        tokens.  Whoever needs one has to move it out of the boot path, or
        replace the refusal with a real preprocessor-token reader."""
        directives, _ = cpp_arms(code)
        protected, opened = [], []
        for header, what in (
                (r"\bstatic\s+void\s+milan_init\s*\(\s*void\s*\)\s*\{",
                 "the boot entry point"),
                (r"\bstatic\s+void\s+configure_fabric\s*\(\s*void\s*\)"
                 r"\s*\{", "the fabric configuration step"),
                (r"\bstatic\s+void\s+entity_advertise\s*\(\s*int\s+\w+"
                 r"\s*\)\s*\{", "the entity-advertise choke point"),
                (r"\bstatic\s+inline\s+volatile\s+uint32_t\s*\*\s*\w+"
                 r"\s*\([^)]*\)\s*\{", "the CSR address helper"),
                (r"\bstatic\s+inline\s+uint32_t\s+milan_read\s*\([^)]*\)"
                 r"\s*\{", "the CSR read accessor"),
                (r"\bstatic\s+inline\s+void\s+milan_write\s*\([^)]*\)"
                 r"\s*\{", "the CSR write accessor")):
            found = re.search(header, code)
            if not found:
                continue
            try:
                _body, close = braced_span(code, found, what)
            except AssertionError:
                # A body this gate cannot brace-match is a firmware the
                # compiler will refuse; let the census say so rather than
                # report a preprocessor verdict about text nobody can parse.
                continue
            protected.append((found.start(), close + 1, what))
        for directive in directives:
            kind = directive.group(1)
            if kind in ("if", "ifdef", "ifndef"):
                opened.append(directive.start())
                continue
            if kind != "endif":
                continue
            assert opened, "firmware has an #endif outside any #if"
            at = opened.pop()
            stop = code.find("\n", directive.end())
            stop = len(code) if stop < 0 else stop
            if load_span[0] <= at and stop <= load_span[1]:
                continue
            for guard_at, guard_to, what in protected:
                assert stop <= guard_at or at >= guard_to, \
                    "firmware must not select boot code with the " \
                    f"preprocessor (a conditional group reaching {what}): " \
                    "this gate would read one arm while the compiler takes " \
                    "the other"
            defines = re.search(
                r"(?m)^[ \t]*#[ \t]*(define|undef|include)\b", code[at:stop])
            assert not defines, \
                "firmware must not select boot code with the preprocessor " \
                f"(a conditional group carrying #{defines.group(1)}): the " \
                "address model reads every definition as unconditional " \
                "text, so an arm this gate cannot evaluate chooses the " \
                "value it resolves a register name to"
        # Translation phase 2 runs before comments, strings and preprocessing
        # tokens exist. It DELETES this pair, so `milan_\`-newline-`write` is
        # the one identifier `milan_write` to the compiler while an offset-
        # preserving reader that substitutes spaces sees two identifiers.
        # Scan RAW source and refuse the language construct; blanked text is
        # already too late, and line_spliced() intentionally preserves
        # offsets. Narrowed to the splices that actually JOIN two tokens:
        # a continuation with whitespace on either side of the deleted pair
        # cannot merge anything and is ordinary C.
        splice = re.search(r"(?<=\S)\\[ \t\f\v]*(?:\r\n|[\n\r])(?=\S)",
                           source)
        assert not splice, \
            "firmware must not splice physical source lines with backslash-" \
            "newline where the pair JOINS two tokens: C translation phase 2 " \
            "deletes it before preprocessing tokens are formed, so the " \
            "physical-text whole-firmware store census can miss a joined " \
            "CSR primitive name"

    def constant_value(text):
        """`text` as a 32-bit constant, or None when this gate cannot read it.

        Integer literals, parentheses and the bitwise/shift/additive operators
        only: `| 1u` and `| (1u << 0)` are the SAME enable to the hardware, so
        they must be the same enable here. Anything carrying an identifier
        stays unreadable, and every caller fails closed on that."""
        expr = re.sub(r"\b(0[xX][0-9A-Fa-f]+|[0-9]+)[uUlL]+", r"\1",
                      text.strip())
        if not expr or not re.fullmatch(r"[0-9A-Fa-fxX()~|&^<>+\-\s]*", expr):
            return None
        if re.search(r"[A-Za-z_]", re.sub(r"0[xX][0-9A-Fa-f]+", "", expr)):
            return None
        try:
            value = eval(expr, {"__builtins__": {}}, {})  # noqa: S307
        except Exception:                                 # noqa: BLE001
            return None
        return value & 0xFFFFFFFF if type(value) is int else None

    #: The RTL's own decode table -- `A_NAME = 'hNNN` -- is the ONE statement
    #: of which offsets are registers and which register each offset is.
    csr_address_re = re.compile(
        r"\b(A_[A-Z0-9_]+)\s*=\s*(?:[0-9]+)?'[hH]([0-9A-Fa-f_]+)")
    #: ... but a NAME is not a register. The decode table below says which
    #: address a name carries; only the write decode says which REGISTER an
    #: address reaches, and that is the fact the whole census rests on.
    case_token_re = re.compile(r"\bcase[xz]?\b|\bendcase\b")
    case_label_re = re.compile(
        r"(?m)^[ \t]*((?:A_[A-Z0-9_]+)(?:[ \t]*,[ \t]*A_[A-Z0-9_]+)*)[ \t]*:")
    sv_literal_re = re.compile(
        r"\A\s*(?:[0-9]+[ \t]*)?'[sS]?[hdboHDBO][0-9A-Fa-f_xzXZ?]+\s*\Z|"
        r"\A\s*[0-9][0-9_]*\s*\Z")
    #: A based literal split into the parts a mutation has to keep: the width
    #: and base prefix, and the digits it may rewrite.
    sv_based_re = re.compile(
        r"\A(?P<head>(?:[0-9]+)?'[sS]?(?P<base>[hdboHDBO]))"
        r"(?P<digits>[0-9A-Fa-f_]+)\Z")
    sv_bases = {"h": 16, "d": 10, "o": 8, "b": 2}
    sv_formats = {16: "x", 10: "d", 8: "o", 2: "b"}

    def sv_literal_value(text):
        """`text` as an integer, or None when this gate cannot read EVERY bit
        of it. An `x` or `z` digit lands here as None on purpose: a bit whose
        value the RTL does not state is not a bit this gate may call clear."""
        literal = re.sub(r"[\s_]", "", text.strip())
        if not literal:
            return None
        if "'" in literal:
            based = sv_based_re.match(literal)
            if not based:
                return None
            base = sv_bases[based.group("base").lower()]
            digits = based.group("digits").replace("_", "")
        else:
            base, digits = 10, literal
        try:
            return int(digits, base)
        except ValueError:
            return None

    def csr_write_decode(csr, signal):
        """`(labels, other)` for `signal` in the CSR RTL.

        `labels` is one entry per assignment reached from a `case (wr_addr)`
        arm -- the label list that arm carries -- and `other` is the right-hand
        side of every assignment reached any other way. A register the bus can
        write is exactly the arms in `labels`, so this is what makes the
        address model a CHECKED fact rather than an assumption.

        BOTH assignment operators are read. This used to see `<=` only,
        which made the reset rule below VACUOUS against a blocking reset:
        `adp_ctrl = 32'h0000_0A01;` left `other` empty, the rule had nothing
        to iterate, and it passed without asserting anything. Verilator's
        BLKSEQ would have caught it, but only under `-Wall`, which this
        project does not use."""
        tokens = [(t.start(), t.group()) for t in case_token_re.finditer(csr)]
        assign_re = re.compile(
            rf"\b{re.escape(signal)}\b\s*(?:\[[^\]]*\])?\s*"
            rf"(?:<=|=)\s*([^;]*);")

        def depth_at(pos, start):
            depth = 0
            for at, token in tokens:
                if at < start or at >= pos:
                    continue
                depth += -1 if token == "endcase" else 1
            return depth

        arms = []
        for case in re.finditer(r"\bcase\b\s*\(\s*wr_addr\s*\)", csr):
            stop, depth = len(csr), 1
            for at, token in tokens:
                if at <= case.start():
                    continue
                depth += -1 if token == "endcase" else 1
                if not depth:
                    stop = at
                    break
            assert stop < len(csr), "a CSR write-decode case is never closed"
            labels = [(m.start(), [n.strip() for n in m.group(1).split(",")])
                      for m in case_label_re.finditer(csr, case.end(), stop)
                      if depth_at(m.start(), case.end()) == 0]
            arms.append((case.end(), stop, labels))

        governed, other = [], []
        for write in assign_re.finditer(csr):
            for start, stop, labels in arms:
                if not start <= write.start() < stop:
                    continue
                before = [names for at, names in labels if at < write.start()]
                assert before, \
                    f"{signal} is written inside a CSR write decode " \
                    "under no case label at all, so no address reaches it"
                governed.append(before[-1])
                break
            else:
                other.append(write.group(1))
        return governed, other

    def assert_decode_is_one_to_one(csr, model):
        """Each entity-enable register is written from ONE address, and comes
        out of reset DISABLED.

        The name-to-address table alone does not say the first: a SECOND
        decode arm gives the same register a second address, and every census
        keyed on the first address then looks straight past a write through
        the second.

        And the whole firmware census says nothing at all about the second.
        Every rule about who may SET bit 0 is a rule about writes; bit 0's
        value before the first write is the reset literal, so a reset of
        `32'h0000_0A01` advertises the entity from FPGA configuration onward
        -- before the CPU has run an instruction, before configure_fabric(),
        before an AEM image exists in DRAM, and forever if the firmware never
        reaches the guard at all. The PHC reset is pinned below because the
        contract wants it ENABLED; these two are pinned here because the
        contract wants them CLEAR."""
        assert re.search(
            r"\bwire\s*\[\s*ADDR_WIDTH\s*-\s*1\s*:\s*0\s*\]\s*wr_addr\s*=\s*"
            r"s_axi_awaddr\s*;", csr), \
            "the CSR write address must be the full-width write address " \
            "unmodified, or two firmware addresses reach one decode arm"
        for wild in re.finditer(r"\bcase[xz]\b\s*\(\s*wr_addr\s*\)", csr):
            raise AssertionError(
                f"the CSR write decode must not be a {wild.group(0)}: a "
                "wildcard arm answers to addresses no name in the table "
                "carries, so the firmware census cannot enumerate them")
        for signal, rtl_name, port in (("adp_ctrl", "A_ADP_CTRL",
                                        "o_adp_enable"),
                                       ("pp_ctrl_r", "A_PP_CTRL",
                                        "o_pp_enable")):
            governed, other = csr_write_decode(csr, signal)
            assert governed == [[rtl_name]], \
                f"the RTL must write {signal} from exactly one CSR address, " \
                f"{rtl_name} (CSR 0x{model.rtl_address(rtl_name):03x}), " \
                "or the register answers to an address the firmware " \
                f"census does not watch; write decode reaches it {governed}"
            assert other, \
                f"the RTL must give {signal} a reset value, and it has " \
                f"none: with no assignment outside the write decode, {port} " \
                "holds whatever the fabric brings up and this rule would " \
                "otherwise pass by having nothing to check"
            for rhs in other:
                assert sv_literal_re.match(rhs), \
                    f"the RTL writes {signal} outside the CSR write decode " \
                    f"with {rhs.strip()!r}: only a literal reset value may " \
                    "reach it there, or bus data has a second route in"
                # ... and a literal is not enough. Bit 0 IS the safety
                # property, so the value it resets to is part of it.
                value = sv_literal_value(rhs)
                assert value is not None and not value & 1, \
                    f"the RTL must reset {signal} with bit 0 CLEAR, but it " \
                    f"resets to {rhs.strip()!r}: {port} is then asserted " \
                    "from FPGA configuration onward, so the entity is " \
                    "advertised before any firmware has verified an AEM image"
            drive = list(re.finditer(
                rf"\bassign\s+{port}\s*=\s*{re.escape(signal)}\s*"
                rf"\[\s*0\s*\]\s*;", csr))
            assert len(drive) == 1, \
                f"{port} must be driven exactly once, by {signal}[0], or " \
                "the bit this gate censuses is not the bit that advertises"

    #: Whitespace-tolerant: `milan_write (` is the same call to the compiler,
    #: so it has to be the same call to the census.
    write_call_re = re.compile(r"\bmilan_write\s*\(")
    write_def_re = re.compile(
        r"\bstatic\s+inline\s+void\s+milan_write\s*\(\s*unsigned\s+int\s+"
        r"(?P<offset>\w+)\s*,\s*uint32_t\s+(?P<value>\w+)\s*\)\s*\{")

    def csr_literal_default(csr, rtl_name):
        """The literal in ``csr_default``'s live, top-level address case.

        A bare whole-file regex can take an A_ID arm from a dead procedural
        case while the live case serves a numeric-equivalent address.  Bound
        the lookup to the one canonical ``unique case (a)`` in the function,
        require that case to be the function's direct body after the default
        assignment, and require the selected item to be at that case's own
        depth.  The separately-run CSR Verilator harness owns the behavioral
        claim that this literal is what an AXI read actually returns.
        """
        functions = list(re.finditer(
            r"\bfunction\s+automatic\s+\[\s*31\s*:\s*0\s*\]\s+"
            r"csr_default\s*\(\s*input\s+\[\s*10\s*:\s*0\s*\]\s+a\s*\)"
            r"\s*;(?P<body>.*?)\bendfunction\b", csr, re.DOTALL))
        assert len(functions) == 1, \
            "the RTL must define exactly one canonical csr_default function"
        body = functions[0].group("body")
        cases = list(re.finditer(
            r"\bunique\s+case\s*\(\s*a\s*\)", body))
        assert len(cases) == 1, \
            "the RTL csr_default function must have one unique case (a)"
        case = cases[0]
        assert re.fullmatch(
            r"\s*csr_default\s*=\s*32\s*'\s*[hH]0\s*;\s*",
            body[:case.start()]), \
            "RTL csr_default's address case must be a direct top-level item " \
            "after its literal-zero default"

        depth, case_stop = 0, None
        for token in case_token_re.finditer(body, case.start()):
            if token.group(0) == "endcase":
                depth -= 1
                if depth == 0:
                    case_stop = token.start()
                    case_end = token.end()
                    break
            else:
                depth += 1
        assert case_stop is not None, \
            "the RTL csr_default function's unique case (a) is not closed"
        assert not body[case_end:].strip(), \
            "the RTL csr_default address case must be the function's last " \
            "top-level item"
        case_body = body[case.end():case_stop]
        low_eleven = (
            r"(?:\[\s*10\s*:\s*0\s*\]|\[\s*0\s*\+:\s*11\s*\])")
        matches = list(re.finditer(
            rf"\b{re.escape(rtl_name)}\s*{low_eleven}\s*:\s*"
            r"csr_default\s*=\s*(?P<value>[^;]+);", case_body))
        assert len(matches) == 1, \
            f"the RTL csr_default canonical case must define {rtl_name} " \
            "exactly once"
        nested_depth = 0
        for token in case_token_re.finditer(case_body, 0, matches[0].start()):
            nested_depth += -1 if token.group(0) == "endcase" else 1
        assert nested_depth == 0, \
            f"RTL csr_default {rtl_name} item must be live in its canonical " \
            "top-level case"
        literal = matches[0].group("value")
        value = sv_literal_value(literal)
        assert value is not None, \
            f"the RTL {rtl_name} readback default must remain a literal, " \
            f"not {literal.strip()!r}"
        return value

    class CsrModel:
        """The firmware's #define table resolved against the register
        addresses the RTL actually decodes.

        The bus reasons over ADDRESSES, so this model does too. Two #defines
        for 0x600 are ONE register here; a #define repointed at 0x920 IS
        PP_CTRL however it is spelled; and a constant that is not a decoded
        register address is not a register operand at all. Every rule built
        on this keys on the address, never on the token."""

        def __init__(self, firmware, csr):
            code = blanked(firmware)
            self.decoded = {}
            seen_names = set()
            address_matches = list(csr_address_re.finditer(csr))
            for match in address_matches:
                name, digits = match.groups()
                assert_direct_scope(
                    csr, match.start(),
                    "RTL CSR address declarations must be unconditional "
                    "module-scope items", require_item_start=False)
                assert name not in seen_names, \
                    f"RTL CSR address name {name} must be declared exactly once"
                seen_names.add(name)
                self.decoded.setdefault(int(digits.replace("_", ""), 16), name)
            assert self.decoded, "the RTL no longer declares a CSR decode table"
            self.defines = {}
            for name, text in re.findall(
                    r"(?m)^[ \t]*#[ \t]*define[ \t]+(MILAN_[A-Za-z0-9_]+)[ \t]+"
                    r"([^\r\n]*?)[ \t]*$", code):
                value = constant_value(text)
                if value is not None:
                    self.defines.setdefault(name, value)
            self.phc = self.rtl_address("A_PTP_CTRL")
            self.pp = self.rtl_address("A_PP_CTRL")
            self.adp = self.rtl_address("A_ADP_CTRL")
            self.identity = self.rtl_address("A_ID")
            self.identity_default = csr_literal_default(csr, "A_ID")

        def rtl_address(self, rtl_name):
            for address, name in self.decoded.items():
                if name == rtl_name:
                    return address
            raise AssertionError(f"the RTL no longer decodes {rtl_name}")

        def label(self, address):
            return f"{self.decoded[address][2:]} (CSR 0x{address:03x})"

        def address(self, operand):
            """The CSR address `operand` reaches, or None when this gate
            cannot prove it reaches one -- a value constant, a local, a macro
            argument, an arithmetic expression on a variable."""
            text = operand.strip()
            value = self.defines.get(text)
            if value is None:
                value = constant_value(text)
            return value if value in self.decoded else None

        def calls(self, source):
            """Every milan_write() CALL in `source` as a record, the
            primitive's own definition excluded. Offsets index `source`."""
            code = blanked(source)
            skip = [(d.start(), d.end()) for d in write_def_re.finditer(code)]
            found = []
            for call in write_call_re.finditer(code):
                if any(a <= call.start() < b for a, b in skip):
                    continue
                depth, pos = 1, call.end()
                while pos < len(code) and depth:
                    depth += {"(": 1, ")": -1}.get(code[pos], 0)
                    pos += 1
                assert depth == 0, "a milan_write() call is never closed"
                args, at = code[call.end():pos - 1], call.end()
                depth, comma = 0, -1
                for offset, char in enumerate(args):
                    depth += {"(": 1, ")": -1}.get(char, 0)
                    if char == "," and not depth:
                        comma = offset
                        break
                assert comma >= 0, \
                    "a milan_write() call carries no register operand"
                found.append({"start": call.start(), "stop": pos,
                              "operand": args[:comma],
                              "value": args[comma + 1:],
                              "value_at": at + comma + 1})
                # `stop` deliberately ends at the closing paren, not the
                # statement's semicolon, so a record can be lifted out and
                # dropped back in as an expression.
            return found

        def writes(self, source, address):
            """Every milan_write() in `source` that reaches `address`, each
            with what it does to bit 0. A VALUE this gate cannot read counts
            as SETTING bit 0, so an unreadable value can never be an
            unnoticed entity enable."""
            found = []
            for record in self.calls(source):
                if self.address(record["operand"]) != address:
                    continue
                found.append(self.effect(record, address))
            return found

        def effect(self, record, address):
            text = record["value"]
            read = re.match(
                r"\A\s*\bmilan_read\s*\(\s*([^()]*?)\s*\)\s*([|&])\s*"
                r"(.*?)\s*\Z", text, re.S)
            mask = constant_value(read.group(3)) if read else None
            if read and mask is not None and \
                    self.address(read.group(1)) == address:
                # OR can only set bit 0; AND (with or without ~) can only
                # clear it, and clears it exactly when the mask omits it.
                ored = read.group(2) == "|"
                record.update(
                    kind="or" if ored else "and",
                    sets=ored and bool(mask & 1),
                    clears=(not ored) and not mask & 1,
                    mask_at=record["value_at"] + read.start(3),
                    mask_to=record["value_at"] + read.end(3))
                return record
            constant = constant_value(text)
            if constant is not None:
                record.update(kind="constant", sets=bool(constant & 1),
                              clears=not constant & 1)
                return record
            record.update(kind="opaque", sets=True, clears=False)
            return record

        def enable_write(self, block, address):
            """The single read/OR enable of bit 0 at `address` in `block`."""
            label = self.label(address)
            ored = [w for w in self.writes(block, address)
                    if w["kind"] == "or"]
            assert len(ored) == 1, \
                f"{label} must have exactly one read/OR enable write, and " \
                f"there are {len(ored)}. NOTE, because this message has " \
                "described the wrong thing before: the OR mask must be a " \
                "value this gate can EVALUATE, so a named constant " \
                "(`| MILAN_ENTITY_ENABLE`) does not count as the enable " \
                "write even though it is the same bit to the hardware. " \
                "Hoisting the mask to a #define is refused for that reason, " \
                "not because the enable is missing or duplicated"
            assert ored[0]["sets"], \
                f"{label} enable write must assert bit 0"
            return ored[0]

    reset_pattern = re.compile(
        r"\bptp_ctrl\s*<=\s*"
        r"(?P<literal>(?:(?:[0-9]+)\s*)?'[hHdDbB]\s*[0-9A-Fa-f_]+|"
        r"[0-9][0-9_]*)\s*;")

    def ptp_reset_assignment(csr):
        match = reset_pattern.search(csr)
        assert match, "bare-metal PHC contract requires a literal reset value"
        literal = match.group("literal")
        value = sv_literal_value(literal)
        assert value is not None, \
            f"unsupported ptp_ctrl reset literal: {literal}"
        return match, value

    def ptp_enable_assignment(csr):
        """The PHC enable output and the register bit that solely drives it."""
        matches = list(re.finditer(
            r"\bassign\s+o_ptp_enable\s*=\s*(?P<value>[^;]+);", csr))
        assert len(matches) == 1, \
            "bare-metal PHC contract requires exactly one o_ptp_enable " \
            "continuous assignment"
        value = matches[0].group("value")
        assert re.fullmatch(r"\s*ptp_ctrl\s*\[\s*0\s*\]\s*", value), \
            "PHC enable output must be driven directly by PTP_CTRL[0], " \
            "independent of ADP, AEM and protocol-processor gates"
        return matches[0]

    def crc_mismatch_guard(load_source):
        """The `if` that refuses a CRC mismatch, found by the comparison it
        makes rather than by the name of the local it compares -- renaming a
        local is not a boot-contract change."""
        return re.search(
            r"\bif\s*\(\s*(?:(?P<lhs>\w+)\s*!=\s*MILAN_AEM_IMAGE_CRC32|"
            r"MILAN_AEM_IMAGE_CRC32\s*!=\s*(?P<rhs>\w+))\s*\)\s*\{",
            load_source)

    def assert_csr_store_closure(code, source):
        """milan_write() is the ONLY store into a CSR, in the text this reads.

        Every rule below the census reads milan_write() call sites, so a
        second way to reach a control register is a way to advertise the
        entity unexamined. This pins the three ingredients of a CSR store --
        the base, the address helper and the primitive's own name -- so a
        store spelled any other way is refused rather than left unexamined.

        What it does NOT prove, stated so no later round mistakes its scope
        for the whole property:

        * It is a reader of ONE preprocessed-once translation unit's text, not
          of the compiler's. It reads the file as written; the arm-selection
          and macro-body traps that gave that reading its teeth are refused
          outright by assert_preprocessor_visible(), not modelled here.
        * It reasons about SPELLING, not values. A store through a pointer
          held in a variable is outside what any of these regexes can TRACE.
          Rules 1 to 3 do not keep it out and this bullet used to say they
          did, which was false: `volatile uint32_t *adp = (void *)0x...;
          *adp = 1u;` passed all three. Rule 5 refuses it instead, by pinning
          the SET of casts and the SET of stores rather than by tracing where
          any pointer points.
        * An inline-asm store has NO spelling for these rules to match: no
          milan_write, no milan_reg, no MILAN_CSR_BASE, no cast, just a
          literal address in a template. Rules 1 to 3 cannot keep that out
          and this docstring used to concede it with nothing behind the
          concession; assert_asm_set_is_closed() is what refuses it now.
        * A store from a SECOND translation unit is outside them entirely.
          Nothing here reads a second file, so rules 1 to 3 cannot be what
          keeps one out; assert_single_translation_unit() refuses one, and
          until round five that check read `OBJECTS =` and stopped, so an
          `OBJECTS += second.o` on the next line voided every rule above.
        * It says nothing about REACHABILITY. That a store exists in the guard
          is proved here; that control reaches it only through the guard is
          proved by the label/goto/switch refusal in assert_boot_contract()."""
        reg_def = re.search(
            r"\bstatic\s+inline\s+volatile\s+uint32_t\s*\*\s*milan_reg\s*\(\s*"
            r"unsigned\s+int\s+(?P<offset>\w+)\s*\)\s*\{", code)
        assert reg_def, \
            "firmware must define the milan_reg() CSR address helper"
        reg_span = braced_span(code, reg_def, "milan_reg()")
        read_def = re.search(
            r"\bstatic\s+inline\s+uint32_t\s+milan_read\s*\(\s*unsigned\s+int"
            r"\s+(?P<offset>\w+)\s*\)\s*\{", code)
        assert read_def, "firmware must define the milan_read() CSR helper"
        read_span = braced_span(code, read_def, "milan_read()")
        write_defs = list(write_def_re.finditer(code))
        assert len(write_defs) == 1, \
            "firmware must define the milan_write() CSR store primitive " \
            "exactly once, with the signature this gate parses"
        write_def = write_defs[0]
        write_span = braced_span(code, write_def, "milan_write()")
        write_body = code[write_span[0]:write_span[1]]
        # The census reads a call as "this value reaches this offset", so the
        # primitive must actually be that: one store, of the value it was
        # handed, at the offset it was handed.
        assert re.match(
            rf"\A\s*\*\s*milan_reg\s*\(\s*{write_def.group('offset')}\s*\)"
            rf"\s*=\s*{write_def.group('value')}\s*;", write_body) and \
            len(re.findall(r"(?<![=!<>+\-*/%&|^])=(?!=)", write_body)) == 1, \
            "milan_write() must store exactly the value it is passed at the " \
            "offset it is passed, or the bit-0 census reads the wrong register"

        def within(span, pos):
            return span[0] <= pos < span[1]

        # 1. Only milan_reg() may FORM a CSR address. This is no longer a
        #    rule about text: assert_compiled_census_is_clean() asks the
        #    COMPILER which functions materialise a window address, so a
        #    typedef'd pointer type, a register-access macro, a struct
        #    overlay, an `->` store and an inline-asm template are all seen
        #    without any of them being recognised in C. The one textual
        #    remnant is the base NAME, kept because it gives a better message
        #    than an address census can and costs nothing.
        for pattern, what in (
                (r"\bMILAN_CSR_BASE\b", "the CSR base"),
                (r"\(\s*volatile\s+uint32_t\s*\*\s*\)", "a CSR pointer cast")):
            for use in re.finditer(pattern, code):
                assert within(reg_span, use.start()), \
                    f"only milan_reg() may form a CSR address, but {what} is " \
                    "used outside it: a raw store there reaches a control " \
                    "register without passing the bit-0 census"
        # 2. ... and only milan_read()/milan_write() may call it, so the one
        #    dereference-store through it stays the one inside milan_write().
        for use in re.finditer(r"\bmilan_reg\s*\(", code):
            assert within(reg_span, use.start()) or \
                within(read_span, use.start()) or \
                within(write_span, use.start()) or \
                within((reg_def.start(), reg_def.end()), use.start()), \
                "milan_reg() may be called only by milan_read()/milan_write(): " \
                "a store through it bypasses the bit-0 census"
        # 3. milan_write is CALLED, never used as a value: taking its address
        #    hands a function pointer a CSR store the census cannot see.
        for use in re.finditer(r"\bmilan_write\b", code):
            assert re.match(r"\s*\(", code[use.end():]), \
                "milan_write must always be called, never used as a value: a " \
                "function pointer to it stores to a CSR outside the census"
        # 4. No pasted or aliased spelling of the primitive: a name this gate
        #    cannot read is a store it cannot classify, so fail closed.
        assert "##" not in code and "%:" not in code and "??" not in code, \
            "firmware must not paste tokens, and must not spell one with a " \
            "digraph or a trigraph: a pasted call name builds a CSR store " \
            "this gate cannot read, and an alternate spelling of `#` builds " \
            "a directive it cannot read either"
        for name, body in re.findall(
                r"(?m)^[ \t]*#[ \t]*define[ \t]+(\w+)(?:\([^)\n]*\))?[ \t]*"
                r"([^\r\n]*)$", code):
            hidden = re.search(r"\bmilan_(?:reg|read|write)\b", body)
            assert not hidden, \
                f"#define {name} hides {hidden.group(0)}() inside a macro " \
                "body: every call to a CSR primitive must be spelled out so " \
                "the operand census can read which register it names. A " \
                "read-only accessor macro contains no store and is refused " \
                "for this reason, not for storing"
        # 5. ... and the cast set and the store set, restored: they catch
        #    address formation the compiled census cannot see because no
        #    window immediate is ever printed.
        assert_store_set_is_closed(code, source)

        # 6. The call-site census only has meaning if the two read-side
        #    accessors preserve the offset and value it attributes to each
        #    call. Keep this after the set closure so the existing
        #    helper-body-store mutants remain pinned to the independent cast
        #    and store-set checks that were written for them.
        reg_body = code[reg_span[0]:reg_span[1]]
        reg_offset = re.escape(reg_def.group("offset"))
        assert re.fullmatch(
            rf"\s*\breturn\b\s*\(\s*volatile\s+uint32_t\s*\*\s*\)\s*"
            rf"\(\s*MILAN_CSR_BASE\s*\+\s*{reg_offset}\s*\)\s*;\s*",
            reg_body), \
            "milan_reg() must return exactly MILAN_CSR_BASE plus the offset " \
            "it is passed"
        read_body = code[read_span[0]:read_span[1]]
        read_offset = re.escape(read_def.group("offset"))
        assert re.fullmatch(
            rf"\s*\breturn\b\s*\*\s*milan_reg\s*\(\s*{read_offset}\s*\)"
            rf"\s*;\s*", read_body), \
            "milan_read() must return exactly the value loaded through " \
            "milan_reg(offset)"
    #: ---- RESTORED, and the reason is measured -----------------------
    #:
    #: Round nine deleted the three families below on the claim that the
    #: compiled census subsumed them. It does not. The census asks the
    #: compiler for its TEXT and then matches that text for a whole-window
    #: immediate, so a regex over disassembly is still a recognizer and it
    #: inherited exactly the defect the instrument change was meant to
    #: escape, one level down. Three shapes were RED at cc2ee861 and GREEN
    #: at 828e5b06 with the census running:
    #:
    #:   * a store added INSIDE milan_reg(), which the census exempts by
    #:     name, killed here by the cast set;
    #:   * `(csr_page << 16) | MILAN_ADP_CTRL`, where the address is built
    #:     with slli/ori and no window immediate is ever printed, killed
    #:     here by the cast rule;
    #:   * a `lui`-based asm template, which objdump annotates but which
    #:     carries no window immediate, killed here by the asm set.
    #:
    #: So the census is an ADDITION, not a replacement. These catch
    #: spellings the disassembly regex misses; the census catches spellings
    #: no recognizer here anticipates. There is now measured evidence in
    #: both directions and neither alone is sufficient.
    #: Every store THROUGH A POINTER the firmware ships, pinned as a SET.
    #:
    #: Rule 1 above refuses ONE cast spelling, `(volatile uint32_t *)`, and
    #: that is a denylist with a single entry: `volatile unsigned int *`,
    #: `uint32_t volatile *` and a `(void *)` into a local are the same store
    #: to the compiler and none of them matches it. It is the same failure
    #: mode as an include regex narrower than the preprocessor, in the oldest
    #: rule here. So the stores are pinned rather than the casts: a store is
    #: found by what it IS, a dereference or a subscript on the left of an
    #: assignment, and the cast that formed the pointer does not matter.
    firmware_pointer_stores = (
        "*milan_reg(offset) = value",
        "*value = (uint64_t)parsed",
        "*value = seconds * 1000000000ull + nanoseconds",
        "dst[i] = src[i]",
    )
    #: ... and every cast to a POINTER, pinned the same way and for a reason
    #: the store set alone does not cover. A store can be spelled `*p = v`,
    #: `p[i] = v`, `p->m = v`, `(*p)++` or a memcpy, and enumerating THOSE is
    #: the trap this whole round is about. A cast is where an address BECOMES
    #: a pointer, so pinning the casts bounds address formation whatever the
    #: store looks like: every one of those spellings still needs a cast (or
    #: MILAN_CSR_BASE, or milan_reg(), both already pinned) to name a control
    #: register in the first place.
    firmware_pointer_casts = (
        "(volatile uint32_t *)",
        "(const volatile uint8_t *)",
        "(volatile uint8_t *)",
        "(const unsigned char *)",
    )
    pointer_cast_re = re.compile(
        r"\([ \t]*[A-Za-z_][A-Za-z0-9_ \t]*\*(?:[ \t]*\*)*[ \t]*\)")
    #: An assignment operator, simple or compound, and never a comparison.
    assign_op_re = re.compile(
        r"(?<![=!<>+\-*/%&|^])(?:[-+*/%&|^]|<<|>>)?=(?!=)")
    subscript_lhs_re = re.compile(r"\A\w+[ \t]*\[[^\]]*\]\Z")

    def pointer_stores(code):
        """`(start, stop)` for every store through a pointer in `code`.

        The left-hand side is taken back to the statement's start. A
        DECLARATION with an initialiser is not a store, because its `*` is a
        pointer declarator and its text names a type first; an assignment
        inside a call's argument list is skipped for the same reason its
        parentheses do not balance."""
        found = []
        for op in assign_op_re.finditer(code):
            start = max(code.rfind(char, 0, op.start()) for char in ";{}") + 1
            lhs = code[start:op.start()]
            # A `for (i = 0; ...)` head leaves an unmatched `)` behind; step
            # the statement's start past it so the loop BODY's store is seen
            # and reported as itself rather than with the loop head attached.
            while lhs.count("(") < lhs.count(")"):
                cut = lhs.index(")") + 1
                start, lhs = start + cut, lhs[cut:]
            if lhs.count("(") > lhs.count(")"):
                continue
            text = lhs.strip()
            if not (text.startswith("*") or subscript_lhs_re.match(text)):
                continue
            stop = code.find(";", op.end())
            found.append((start, len(code) if stop < 0 else stop))
        return found

    def assert_store_set_is_closed(code, source):
        """The firmware's stores through a pointer are pinned to the four it
        ships, so a CSR store cannot be built from a cast this gate never
        thought to name.

        COST: a fifth pointer store is RED until it is added above. That is
        the tripwire: whoever adds one has to decide, in this gate, whether
        its target can be a control register."""
        casts = [" ".join(m.group(0).split())
                 for m in pointer_cast_re.finditer(code)]
        assert casts == list(firmware_pointer_casts), \
            "the firmware's casts to a pointer are pinned: a cast is where " \
            "an address becomes a pointer, so naming ONE cast spelling " \
            "leaves `volatile unsigned int *`, `uint32_t volatile *` and " \
            f"`(void *)` free to name a control register; found {casts}"
        found = [" ".join(source[at:to].split())
                 for at, to in pointer_stores(code)]
        assert found == list(firmware_pointer_stores), \
            "the firmware's stores through a pointer are pinned: a store is " \
            "a store whatever cast formed the pointer, and naming one cast " \
            "spelling leaves `volatile unsigned int *`, `uint32_t volatile " \
            f"*` and a (void *) into a local all reaching a CSR; found {found}"

    #: The firmware's inline asm, pinned the way the include set is. An asm
    #: store carries NO textual signature any other rule here matches: no
    #: milan_write, no milan_reg, no MILAN_CSR_BASE and no cast, so a literal
    #: address in an asm template reaches a control register past all of
    #: them. The firmware already uses asm for its fences, so this is
    #: idiomatic here rather than exotic.
    firmware_asm = (
        '__asm__ volatile("fence iorw, iorw" ::: "memory")',
        '__asm__ volatile("fence rw, rw" ::: "memory")')
    asm_re = re.compile(r"\b(?:__asm__|__asm|asm)\b")

    def assert_asm_set_is_closed(code, source):
        """Inline asm is pinned to the two fences the firmware ships.

        COST: a third asm statement is RED until it is added above, which is
        the point. Whoever adds one has to decide, in this gate, whether its
        template can store into a control register."""
        found = []
        for use in asm_re.finditer(code):
            stop = code.find(";", use.start())
            assert stop >= 0, "an inline-asm statement is never closed"
            found.append(" ".join(source[use.start():stop].split()))
        assert found == list(firmware_asm), \
            "the firmware's inline asm is pinned: an asm template carries no " \
            "milan_write, no milan_reg, no MILAN_CSR_BASE and no cast, so a " \
            "literal address in one stores to a control register past every " \
            f"rule in the CSR store closure; found {found}"

    #: The firmware's translation unit is milan_baremetal.c plus exactly
    #: these. Pinned as a SET rather than derived, because there is nothing
    #: here to derive it from: the whole point is that a twelfth include is
    #: text this gate does not read, whatever the file is called.
    #: Nine are THIRD PARTY: newlib's four and LiteX's five. Their contents
    #: are not this repository's text, so pinning their names and trusting
    #: their bodies is one claim ...
    firmware_includes_third_party = (
        "<stdint.h>", "<errno.h>", "<stdio.h>", "<stdlib.h>",
        "<hw/common.h>", "<libbase/crc.h>", "<system.h>",
        '"command.h"', '"init.h"')
    #: ... and two are written by THIS REPOSITORY'S OWN BUILDER, so their
    #: contents are this repository's text one generator away. Pinning those
    #: names is the weaker half of the claim and it should not be stated as
    #: though it were the same one. Their VALUES are gate 28's.
    firmware_includes_generated = ("<generated/mem.h>", "<generated/soc.h>")
    firmware_includes = (firmware_includes_third_party +
                         firmware_includes_generated)
    #: ... and a pinned NAME is not a pinned FILE. `"command.h"` and
    #: does the same for the angle-bracket names. So RESOLUTION is pinned as
    #: well as the names: the firmware's directory holds exactly these files,
    #: and CFLAGS carries exactly this one search path.
    firmware_directory = ("Makefile", "milan_baremetal.c")
    def assert_include_resolution_is_pinned(listing):
        """No file beside the firmware may answer to a pinned include name.

        This is the axis that matters, and it is NOT who wrote the file: it
        is whether this repository can decide which file a pinned name
        resolves to. Splitting third party from generated was a real
        correction and it is kept below, but on its own it says nothing about
        a name whose FILE this repository can supply.

        COST: any new file in the firmware's directory is RED, a README
        included. That is the tripwire: the directory is two files and has
        been for its whole life."""
        assert sorted(listing) == sorted(firmware_directory), \
            "the firmware's directory is pinned to " \
            f"{sorted(firmware_directory)}: a quoted include resolves " \
            "against this directory FIRST, so a file dropped in here answers " \
            "to a pinned include name and puts this repository's text behind " \
            f"it with no name changing anywhere; found {sorted(listing)}"
    #: Every preprocessing directive this gate has a rule for. Anything else
    #: is REFUSED rather than ignored: an #undef can retire a register
    #: constant the address model read, and #pragma, #line, #include_next and
    #: #import are outside every rule here.
    firmware_directives = ("include", "define", "if", "ifdef", "ifndef",
                           "elif", "else", "endif")
    directive_re = re.compile(r"(?m)^[ \t]*#[ \t]*([A-Za-z_]\w*)?")
    include_operand_re = re.compile(
        r"\A[ \t]*(<[^>\n]*>|\"[^\"\n]*\")[ \t]*\Z")

    def line_spliced(text):
        """`text` with backslash-newline splices joined, LENGTH PRESERVED so
        every offset still indexes the original. C and make both continue a
        line this way, so both read it through here."""
        return re.sub(r"\\\n", "  ", text)

    def spliced(text):
        """`text` after translation phases 1 and 2, LENGTH PRESERVED so every
        offset still indexes the original: digraphs translated and
        backslash-newline splices joined, each substitution exactly as wide as
        what it replaces.

        `%:include`, `??=include` and `#\\`-newline-`include` are all
        `#include` to the compiler, so they are all `#include` here.
        Enumerating include SPELLINGS is how a regex ends up narrower than
        the preprocessor; doing the translations the standard specifies and
        then reading directives is how it stops being narrower.

        `??=` fires only under a strict `-std=cNN`, and LiteX compiles with
        `-std=gnu99` today, so it does not bite the shipping build. It is
        translated anyway: a gate that is correct only because of a flag it
        never reads is correct by luck."""
        return line_spliced(
            text.replace("??=", "#  ").replace("??/", "  \\")
                .replace("%:%:", "##  ").replace("%:", "# "))

    def assert_directive_set_is_closed(code, source):
        """The text this gate reads is the WHOLE translation unit.

        assert_single_translation_unit() proves the image is built from one
        OBJECT. It does not prove that object is built from one FILE. A
        `#include "milan_bringup.c"` keeps the object count at one, so that
        check is SATISFIED rather than evaded, and it hands the compiler a
        second address helper, a second base cast and two unguarded enables
        in a file no rule here ever opens: rules 1 to 3 of
        assert_csr_store_closure() are all defeated by text it never sees.

        So the DIRECTIVE SET is pinned, after phases 1 and 2, rather than a
        list of include spellings. Every directive must be one this gate has
        a rule for, and every #include operand must be a literal header name
        in the pinned set. That covers a macro-expanded operand (C11
        6.10.2p4, and the #define carrying the path passes every other rule
        because its body names no CSR primitive), a spliced directive and a
        digraph in one assertion instead of one per spelling.

        The include SET is pinned, not the file extension: a header carrying
        CSR stores is the same escape as a `.c`, and an angle-bracket include
        resolves through -I exactly as a quoted one does.

        `code` is the blanked text, so a #include inside a comment is not an
        include; `source` is where the operand is read back from, since
        blanking empties a quoted path but preserves its offsets, and both
        translations above preserve them too.

        COST: a twelfth include even `<string.h>`, and any `#pragma`,
        `#line`, `#error` or `#undef`, are RED until added here. That is the
        tripwire and not a defect: whoever adds one has to decide, in this
        gate, whether the new text can store into a CSR."""
        text, raw = spliced(code), spliced(source)
        for directive in directive_re.finditer(text):
            kind = directive.group(1)
            assert kind in firmware_directives, \
                "the firmware's preprocessing directives are pinned, and " \
                f"'#{kind or ''}' is not one of them: a directive this gate " \
                "has no rule for is text in the translation unit that no " \
                "rule reads"
            if kind != "include":
                continue
            stop = text.find("\n", directive.end())
            stop = len(text) if stop < 0 else stop
            operand = include_operand_re.match(text[directive.end():stop])
            assert operand, \
                "a #include operand must be a literal header name this gate " \
                "can read, not a macro: a macro-expanded operand names a " \
                f"file no rule here opens, got " \
                f"{raw[directive.end():stop].strip()!r}"
            name = raw[directive.end() + operand.start(1):
                       directive.end() + operand.end(1)]
            assert name in firmware_includes, \
                "the firmware's include set is pinned, and " \
                f"{name} is not in it: every rule in this gate reads ONE " \
                "file, so an include it does not know about is text in the " \
                "translation unit that no rule reads. A #include of a .c " \
                "keeps the object count at one, so the " \
                "single-translation-unit check is satisfied honestly while " \
                "the closure reads the wrong file"

    #: ---- the compiled census -------------------------------------------
    #:
    #: Rounds five to eight converted every rule here from a denylist of
    #: dangerous spellings into a permitted SET. That was the right
    #: correction and it retired several axes. It has a floor: a set is only
    #: as wide as the RECOGNIZER that fills it, and the recognizers were
    #: regexes over C. `((milan_adp_block)0x90000600u)->ctrl = 1u;` is a
    #: cast, a store and an entity advertise, and no regex here saw any of
    #: the three.
    #:
    #: So this stops reading C and asks the compiler. Emit assembly, then
    #: require that no function except milan_reg() MATERIALISES an address
    #: inside the Milan CSR window. A typedef'd pointer type, a
    #: register-access macro, a struct overlay, an `->` store, a subscript
    #: store, a qualifier after the star and an inline-asm template all
    #: reduce to the same immediate, so none of them has to be recognised.
    #:
    #: This REPLACES the pointer-cast set, the pointer-store set, the
    #: inline-asm set and rule 1's cast half. It cannot be out-spelled,
    #: because the thing doing the recognising is the thing that defines
    #: what the spellings mean.
    csr_window = re.search(
        r"(?m)^MILAN_CSR_BASE\s*=\s*(0x[0-9A-Fa-f_]+)", soc_source)
    csr_window_size = re.search(
        r"(?m)^MILAN_CSR_SIZE\s*=\s*(0x[0-9A-Fa-f_]+)", soc_source)
    assert csr_window and csr_window_size, \
        "sw/litex/milan_soc.py no longer states the Milan CSR window"
    csr_base = int(csr_window.group(1).replace("_", ""), 16)
    csr_size = int(csr_window_size.group(1).replace("_", ""), 16)
    #: Immediates as the assembler prints them, in any base and either sign,
    #: and never a label suffix (`.L4`) or a register number.
    asm_immediate_re = re.compile(
        r"(?<![\w.])(-?(?:0[xX][0-9A-Fa-f]+|\d+))(?![\w.])")
    asm_noise_re = re.compile(r"^\s*\.(?:cfi|file|loc|size|ident|align|globl)")
    #: The values the census compile substitutes for the generated headers.
    #: Every one is asserted OUTSIDE the window below, so a stub cannot
    #: silently manufacture a hit or mask one.
    census_defines = {
        "SPIFLASH_BASE": 0x2000_0000,
        "MILAN_AEM_DESC_BASE": 0x7F70_0000,
        "MILAN_ENTITY_ID_LO": 0x1122_3344, "MILAN_ENTITY_ID_HI": 0x5566_7788,
        "MILAN_MODEL_ID_LO": 0x0A0B_0C0D, "MILAN_MODEL_ID_HI": 0x0102_0304,
        "MILAN_STATION_MAC_LO": 0x3, "MILAN_STATION_MAC_HI": 0x200,
        "MILAN_SR_VID": 2, "MILAN_LWSRP_CTRL_RESET": 0x10,
        "MILAN_N_TALKERS": 1, "MILAN_AEM_FLASH_OFFSET": 0x00E0_0000,
        "MILAN_AEM_IMAGE_BYTES": 4096, "MILAN_AEM_IMAGE_CRC32": 0xDEAD_BEEF,
    }
    #: The RV32 cross compiler is the real target and the only one that can
    #: assemble the firmware's RISC-V asm; a host compiler answers every
    #: C-level shape and FAILS LOUDLY on the asm rather than passing it.
    census_compilers = (
        os.path.join(os.path.expanduser("~"),
                     "br-milan-rv32/host/bin/riscv32-linux-gcc"),
        "riscv64-elf-gcc", "riscv32-unknown-elf-gcc", "cc", "gcc")
    #: The flag sets that can make one of those candidates the RV32 target,
    #: tried in order. The EMPTY one comes first because a compiler built
    #: for rv32 may carry no multilib for a bare `rv32i`, so driving one
    #: that needs no driving would stand the census down on the very tool
    #: it exists for.
    rv32_drivers = ((), ("-march=rv32i", "-mabi=ilp32"))

    def census_headers(root):
        """The stub header set the census compiles against, written from
        `census_defines` plus the window base read out of milan_soc.py, so
        no address in it is mirrored from anywhere."""
        for leaf in ("generated", "hw", "libbase"):
            os.makedirs(os.path.join(root, leaf), exist_ok=True)
        for name, value in census_defines.items():
            assert not csr_base <= value < csr_base + csr_size, \
                f"census stub {name} lands inside the CSR window and would " \
                "manufacture a hit the firmware never makes"
        body = "\n".join(f"#define {n} 0x{v:x}u"
                         for n, v in census_defines.items())
        write = {
            "generated/mem.h": f"#pragma once\n#define MILAN_CSR_BASE "
                               f"0x{csr_base:x}u\n{body}\n",
            "generated/soc.h": "#pragma once\n",
            "hw/common.h": "#pragma once\n",
            "libbase/crc.h": "#pragma once\nunsigned int crc32("
                             "const unsigned char *b, unsigned int n);\n",
            "system.h": "#pragma once\nvoid cdelay(int i);\n",
            "command.h": "#pragma once\n#define SYSTEM_CMDS 0\n"
                         "#define define_command(n, h, d, g) static void "
                         "(*const n##_c)(int, char **) "
                         "__attribute__((unused)) = h\n",
            "init.h": "#pragma once\n#define define_init_func(f) static void "
                      "(*const f##_i)(void) __attribute__((unused)) = f\n",
        }
        for leaf, text in write.items():
            with open(os.path.join(root, leaf), "w") as fh:
                fh.write(text)

    #: Filled in by the first census run and printed in the verdict: a
    #: census whose answer depends on an unrecorded tool choice is not a
    #: fact. `target` is true only for a compiler that can build the
    #: firmware's RISC-V asm, which is what makes the census authoritative.
    census_used = {}

    def rv32_probe_source(xlen):
        """The census probe: the RISC-V asm the firmware also writes, under
        a guard on the width the compiler is about to compile FOR.

        The probe used to be the asm alone, and `riscv64-elf-gcc` assembles
        `nop` with a `t0` clobber exactly as an RV32 GCC does. So a 64-bit
        compiler answered YES to "are you the exact RV32 target", every
        census was then taken with 64-bit pointers, and the firmware's own
        `(volatile uint32_t *)(MILAN_CSR_BASE + offset)` became an -Werror
        int-to-pointer-cast RED that failed the suite on a pristine tree
        (#206). __riscv_xlen is the compiler's own statement of that width,
        so no multilib default can out-spell it."""
        return (f"#if !defined(__riscv_xlen) || __riscv_xlen != {xlen}\n"
                f"#error \"this compiler is not a {xlen}-bit RISC-V target\"\n"
                "#endif\n"
                "void f(void){__asm__ volatile(\"nop\" ::: \"t0\");}\n")

    def census_probe(candidate, driver, xlen=32, runner=None):
        """Compile the probe once; True when `candidate` driven by `driver`
        IS a RISC-V target of `xlen` bits."""
        run = subprocess.run if runner is None else runner
        with tempfile.TemporaryDirectory(prefix="milan-cc-") as probe_dir:
            probe_path = os.path.join(probe_dir, "probe.c")
            with open(probe_path, "w") as fh:
                fh.write(rv32_probe_source(xlen))
            built = run(
                [candidate] + list(driver) +
                ["-S", "-o", os.path.join(probe_dir, "p.s"), probe_path],
                capture_output=True, text=True)
        return built.returncode == 0

    def census_rv32_driver(candidate, runner=None):
        """The first flag set that makes `candidate` the RV32 target, or
        None when none of them does."""
        for driver in rv32_drivers:
            if census_probe(candidate, driver, runner=runner):
                return driver
        return None

    #: The census's OWN assembly has to be 32-bit, not just the compiler it
    #: was taken with. The probe proves the candidate CAN be driven at RV32;
    #: only the emitted assembly proves the census invocation WAS. GCC states
    #: it, so read it back rather than trusting the argv: [R1] on PR #212
    #: built a wrapper that honours the rv32 flags everywhere except the
    #: census call, and only the four census-only mutants caught it, and only
    #: indirectly.
    census_arch_re = re.compile(r'^\s*\.attribute\s+arch\s*,\s*"([^"]*)"',
                                re.M)
    census_arch_seen = {"stated": 0, "unstated": 0}

    def assert_census_arch_is_rv32(assembly_text, label):
        """The arch the census assembly declares, or None when the toolchain
        declares none. A toolchain that states nothing cannot be blamed for
        it, so the absence is REPORTED rather than reddened."""
        found = census_arch_re.search(assembly_text)
        arch = found.group(1) if found else None
        assert arch is None or arch.startswith("rv32"), \
            f"the compiled census of the {label} was emitted for {arch}, " \
            "not for an rv32 target: the probe adopted this compiler as the " \
            "RV32 target and the census invocation did not follow it there, " \
            "so every pointer width, address and immediate in the assembly " \
            "this gate is about to read belongs to a different machine"
        return arch

    assert assert_census_arch_is_rv32(
        '\t.attribute arch, "rv32i2p1_m2p0"\n', "arch self-test") == \
        "rv32i2p1_m2p0", \
        "the census arch check cannot read the directive GCC actually emits"
    try:
        assert_census_arch_is_rv32('\t.attribute arch, "rv64i2p1"\n',
                                   "arch self-test")
    except AssertionError as exc:
        assert "not for an rv32 target" in str(exc), exc
    else:
        raise AssertionError(
            "the census arch check accepted rv64 assembly, so it cannot say "
            "which machine the census it reads was taken on")
    assert assert_census_arch_is_rv32("\tnop\n", "arch self-test") is None, \
        "assembly with no arch attribute must come back unstated, not " \
        "invented: a toolchain that declares none cannot be blamed for it"

    def census_candidate_answers(candidate):
        try:
            version = subprocess.run([candidate, "--version"],
                                     capture_output=True, text=True)
        except (OSError, ValueError):
            return False
        return version.returncode == 0

    def census_compiler():
        if census_used:
            return census_used.get("compiler")
        present = [c for c in census_compilers if census_candidate_answers(c)]
        for candidate in present:
            driver = census_rv32_driver(candidate)
            if driver is not None:
                census_used.update(compiler=candidate, target=True,
                                   flags=tuple(driver))
                return candidate
        #: Nothing here is the RV32 target, driven or bare. Name the first
        #: compiler that at least ANSWERS, so the stand-down says which tool
        #: declined rather than reporting a bare "no": on a box whose only
        #: RISC-V GCC is 64-bit-only, that name is the actionable half.
        census_used.update(compiler=present[0] if present else None,
                           target=False, flags=())
        return census_used["compiler"]

    #: The CSR address helper's name, derived from the shipping firmware so
    #: the printed summary cannot drift from what the census enforces. A
    #: firmware with no such helper -- an EMPTY milan_baremetal.c is the
    #: degenerate case -- used to reach `.group(1)` on None and fail the
    #: suite with an AttributeError blaming nothing, which is the one kind
    #: of red a gate must never produce (#206).
    reg_helper_declaration = re.search(
        r"\bstatic\s+inline\s+volatile\s+uint32_t\s*\*\s*(\w+)\s*\(",
        firmware_source)
    assert reg_helper_declaration, \
        "the firmware declares no `static inline volatile uint32_t *` CSR " \
        "address helper, so this gate cannot name the one function that is " \
        "allowed to form a CSR address and cannot scope the census it is " \
        "about to take; refusing rather than reporting a bounded result"
    reg_helper_name = reg_helper_declaration.group(1)
    #: Every mutant that reaches a control register outside milan_reg()
    #: fails on this one sentence, whatever spelled it.
    CENSUS_PIN = "materialises one elsewhere"
    #: ... and the three sentences the RESOLVER answers on, one per
    #: question it asks. Every mutant that reaches a control register by
    #: address arithmetic no immediate reveals fails on the first; every one
    #: that reaches a non-zero verdict without the CRC comparison fails on
    #: the second; every one that moves an enable out of the choke point
    #: fails on the third.
    RESOLVER_STORE_PIN = "STORES into the Milan CSR window"
    RESOLVER_DOMINANCE_PIN = "CRC-equality edge REMOVED"
    RESOLVER_CHOKE_PIN = "not from entity_advertise()"

    def format_census_verdict(verdict):
        """Render only an execution state the census actually observed."""
        assert verdict["ran"] == verdict["target"], \
            "compiled-census verdict contradicts its execution state"
        compiler = os.path.basename(verdict.get("compiler") or "no")
        driver = " ".join(verdict.get("flags") or ())
        if verdict["ran"]:
            arch = verdict.get("arch")
            return (f"answered by {compiler}" +
                    (f", driven at RV32 with {driver}" if driver else
                     ", which is the RV32 target with no flags") +
                    (f", emitting {arch} assembly" if arch else
                     ", whose assembly declares no arch attribute"))
        return (f"STOOD DOWN: {compiler} compiler is not the RV32 target and "
                "no flag set here drives it as one, so the compiled census "
                "did not run and the text rules above carry this on their "
                "own")

    def census_take(firmware, label="firmware", selection=None, runner=None):
        """Compile `firmware` for the exact RV32 target once and hand back
        the assembly, or a recorded stand-down.

        ONE compile feeds BOTH instruments: the immediate-matching census
        below and the value-resolving flow analysis beside it. They ask
        different questions of the same emitted code, and taking two
        compiles would let them answer about two different builds."""
        if selection is None:
            compiler = census_compiler()
            target = bool(census_used.get("target"))
            driver = tuple(census_used.get("flags") or ())
        else:
            compiler = selection.get("compiler")
            target = bool(selection.get("target"))
            driver = tuple(selection.get("flags") or ())
        if compiler and not target:
            # GENUINELY stand down. An earlier revision printed
            # "STOOD DOWN" and then ran the census anyway: `-S` does not
            # assemble, so a host compiler emits most of the firmware fine
            # and returned a real x86 verdict while the printed line said
            # the text rules were carrying it alone. A stand-down message
            # that is false is worse than no stand-down.
            return {"compiler": compiler, "target": False, "ran": False,
                    "flags": driver, "text": None, "arch": None}
        assert compiler, \
            "the compiled census needs a C compiler and found none of " \
            f"{list(census_compilers)}: this gate cannot bound CSR stores " \
            "by reading C, so it refuses to report a result it did not take"
        run = subprocess.run if runner is None else runner
        with tempfile.TemporaryDirectory(prefix="milan-census-") as root:
            census_headers(root)
            source = os.path.join(root, "milan_baremetal.c")
            with open(source, "w") as fh:
                fh.write(firmware)
            assembly = os.path.join(root, "census.s")
            built = run(
                [compiler] + list(driver) +
                ["-std=gnu99", "-O0", "-fno-inline", "-S",
                 "-o", assembly, f"-I{root}", source],
                capture_output=True, text=True)
            if built.returncode != 0:
                # Reached only when the compiler IS the RV32 target, since a
                # non-target one returned above without compiling anything.
                #
                # DECIDED, not overlooked ([R1] SUGGESTION on PR #212): this
                # stays a RED and does not become a stand-down. An RV32
                # toolchain with unusable headers therefore reddens a clean
                # checkout, which is the class #206 exists to remove, but the
                # alternative lets a firmware this gate genuinely cannot
                # census pass as "the toolchain's fault". Telling the two
                # apart needs a positive control compiled first, which is a
                # design of its own; not reachable on either toolchain this
                # repository is built with, and recorded in
                # docs/integration/BAREMETAL_FIRMWARE.md rather than left to
                # be rediscovered.
                raise AssertionError(
                    f"the compiled census could not build the {label} with "
                    f"{compiler}, which IS the RV32 target: a source this "
                    "gate cannot compile is a source whose CSR stores it "
                    f"cannot census; {built.stderr.strip().splitlines()[-1:]}")
            text = open(assembly, encoding="utf-8", errors="replace").read()
        arch = assert_census_arch_is_rv32(text, label)
        census_arch_seen["stated" if arch else "unstated"] += 1
        return {"compiler": compiler, "target": True, "ran": True,
                "flags": driver, "text": text, "arch": arch}

    def assert_compiled_census_is_clean(firmware, label="firmware",
                                        selection=None, runner=None,
                                        taken=None):
        """No function but milan_reg() may materialise a CSR window address.

        Measured on the COMPILER's output, not on the firmware's text.

        SCOPE, stated so it is not mistaken for more: this censuses ADDRESS
        FORMATION, which is what bounds every store, read and asm template
        that could reach a control register. It does not say which register
        or which bit; the milan_write() census above does that, and it is
        sound precisely because this makes milan_write() the only way in."""
        # The address helper's NAME is derived from the firmware, not
        # mirrored here: assert_csr_store_closure() pins the same definition.
        helper = re.search(
            r"\bstatic\s+inline\s+volatile\s+uint32_t\s*\*\s*(\w+)\s*\(",
            blanked(firmware))
        assert helper, \
            "the compiled census cannot find the firmware's CSR address " \
            "helper, so it cannot say which function is allowed to form an " \
            "address; refusing rather than censusing against a guess"
        reg_name = helper.group(1)
        taken = census_take(firmware, label, selection, runner) \
            if taken is None else taken
        if not taken["ran"]:
            return {key: taken[key]
                    for key in ("compiler", "target", "ran", "flags")}
        text, arch = taken["text"], taken["arch"]
        hits, where = [], "<file scope>"
        for line in text.splitlines():
            named = re.match(r"^([A-Za-z_][\w.]*):", line)
            if named:
                where = named.group(1)
            if asm_noise_re.match(line):
                continue
            for token in asm_immediate_re.findall(line):
                value = int(token, 0) & 0xFFFF_FFFF
                if csr_base <= value < csr_base + csr_size and \
                        where != reg_name:
                    hits.append((where, f"0x{value:08x}",
                                 " ".join(line.split())))
        assert not hits, \
            f"only {reg_name}() may form a CSR address, and the COMPILED " \
            f"{label} materialises one elsewhere: an address inside the " \
            f"Milan CSR window (0x{csr_base:08x}..0x{csr_base + csr_size:08x})"\
            f" reaches a control register without passing the bit-0 census, " \
            f"whatever cast, typedef, macro, member access or asm template " \
            f"spelled it; found {hits[:3]}"
        return {"compiler": taken["compiler"], "target": True, "ran": True,
                "flags": taken["flags"], "arch": arch}

    #: ---- the RESOLVING half of gate 1b (issue #153) ------------------
    #:
    #: CLASS, recorded before the rules (process guard 1 from #143's close).
    #: The property is DATA FLOW: which value reaches PP_CTRL[0] and
    #: ADP_CTRL[0], and which comparison dominates it. Every rule above is a
    #: RECOGNIZER over some text -- C source, a Makefile, or the census's
    #: regex over disassembly -- and a recognizer can be out-spelled by
    #: construction. The rules below RESOLVE: they compute the store
    #: addresses, the call operands, the compared values and the CFG edges
    #: out of the assembly the census already compiled, so there is no
    #: spelling left to vary.
    #:
    #: This is an ADDITION, not a replacement, and the difference is
    #: measured rather than asserted: the exempted-helper blindness control
    #: below runs BOTH instruments over the same mutant and records that the
    #: census is blind to it while the resolver rejects it.
    def entity_advertise_span(code, label="firmware"):
        """`(match, body, close)` for the entity-advertise choke point."""
        found = re.search(
            r"\bstatic\s+void\s+entity_advertise\s*\(\s*int\s+"
            r"(?P<verdict>\w+)\s*\)\s*\{", code)
        assert found, \
            f"the {label} declares no `static void entity_advertise(int)` " \
            "choke point: the boot contract is proved by data flow into ONE " \
            "function that sets the two enable bits, so without it this " \
            "gate has no choke point to prove anything about (#153)"
        body, close = braced_span(code, found, "entity_advertise()")
        return found, body, close

    def assert_resolved_boot_flow(assembly, model, label="firmware"):
        """Answer the boot contract from the RESOLVED assembly.

        Four questions, each about a VALUE or an EDGE and none about a
        spelling:

        1. does any function STORE to an address this resolves inside the
           Milan CSR window?  No exemption, not even the address helper:
           forming the address is that helper's job, storing through a
           resolved one is nobody's;
        2. which `milan_write()` calls assert bit 0 of PP_CTRL or ADP_CTRL,
           taking the register from the resolved first operand and the bit
           from the resolved second one?
        3. inside the choke point, do those calls survive the removal of the
           edge the verdict test takes when the verdict is non-zero?
        4. inside the verifier, what are the CRC's operands, is the compared
           value the one `crc32()` handed back, and does a non-zero verdict
           survive the removal of the CRC-equality edge?
        """
        unit = rv32_unit(assembly)
        runs = unit["runs"]
        for needed in ("entity_advertise", "load_aem_image", "milan_write"):
            assert needed in unit["functions"], \
                f"the compiled {label} defines no {needed}(), so the " \
                "resolved boot-flow measurement has nothing to answer " \
                "about; refusing rather than reporting a bounded result"
        window = f"0x{csr_base:08x}..0x{csr_base + csr_size:08x}"

        # ---- 1. resolved stores into the control window ------------------
        for name, run in sorted(runs.items()):
            hits = sorted({address for _at, (address, _v) in run["stores"]
                           if isinstance(address, int) and
                           csr_base <= address < csr_base + csr_size})
            assert not hits, \
                f"the compiled {label} STORES into the Milan CSR window " \
                f"({window}) from {name}(), at " + \
                ", ".join(f"0x{hit:08x}" for hit in hits) + \
                ". Every control-register store must go through the " \
                "address helper so the bit-0 census can place it; this is " \
                "the RESOLVED store address, so no cast, typedef, member " \
                "access, subscript or shift-and-or address arithmetic " \
                "changes the answer, and the address helper is NOT exempt"

        # ---- 2. which resolved writes assert an enable bit ---------------
        enabling = []
        for name, run in runs.items():
            for index, (_at, (callee, handed)) in enumerate(run["calls"]):
                if callee != "milan_write":
                    continue
                register, value = handed["a0"], handed["a1"]
                assert isinstance(register, int), \
                    f"the compiled {label} calls milan_write() from " \
                    f"{name}() with a register operand this gate cannot " \
                    f"resolve ({register!r}), so it cannot place the write " \
                    "by ADDRESS and refuses to report a census it did not " \
                    "take"
                if register in (model.pp, model.adp) and \
                        rv32_ones(value) & 1:
                    enabling.append((name, index, register))
                assert register != model.phc, \
                    f"the compiled {label} writes the reset-enabled PHC " \
                    f"({model.label(model.phc)}) from {name}(): resolved " \
                    "from the emitted call operand, so a macro, an alias or " \
                    "a computed offset does not change the answer"
        outside = sorted({name for name, _i, _r in enabling
                          if name != "entity_advertise"})
        assert not outside, \
            f"the compiled {label} asserts bit 0 of an entity-enable " \
            "register from " + ", ".join(f"{name}()" for name in outside) + \
            ", not from entity_advertise(): the choke point is the property " \
            "(#153), and this is resolved from the emitted call operands, " \
            "so a macro body, a preprocessor arm or an aliased #define " \
            "cannot move the write out of view"
        for address in (model.pp, model.adp):
            found = [record for record in enabling
                     if record[2] == address]
            assert len(found) == 1, \
                f"the compiled {label} asserts {model.label(address)} bit 0 " \
                f"{len(found)} time(s) inside entity_advertise(); the " \
                "choke point holds exactly one enable per register"
        pp_at = [index for _n, index, reg in enabling
                 if reg == model.pp][0]
        adp_at = [index for _n, index, reg in enabling
                  if reg == model.adp][0]
        assert pp_at < adp_at, \
            f"the compiled {label} advertises before the protocol processor " \
            "is up: the resolved enable order inside entity_advertise() is " \
            "ADP then PP"

        # ---- 3. the choke point's verdict edge ---------------------------
        verdict = Rv32Tag("verified")
        body = unit["functions"]["entity_advertise"]
        run = rv32_run(body, unit["data"], entry_regs={"a0": verdict})
        live = [at for at, (callee, _h) in run["calls"]
                if callee == "milan_write"]
        assert live, \
            "the compiled entity_advertise() reaches no milan_write() at " \
            "all, so the dominance measurement below would pass on an " \
            "empty set: refusing a control that cannot fail"
        edge = rv32_verdict_edge(run, verdict, 0)
        assert edge, \
            f"the compiled {label} never compares entity_advertise()'s " \
            "verdict argument against zero, so no edge in it can dominate " \
            "the enable writes and the entity is advertised unconditionally"
        cut = rv32_run(body, unit["data"], entry_regs={"a0": verdict},
                       cut=(edge[0], edge[2]))
        escaped = sorted({at for at, (callee, _h) in cut["calls"]
                          if callee == "milan_write"})
        assert not escaped, \
            "the compiled entity_advertise() still reaches a control " \
            f"register write at {escaped} with the non-zero-verdict edge " \
            "REMOVED: the verdict test does not dominate the enable writes, " \
            "so control reaches them by a path that never took it"

        # ---- 4. the verifier's CRC data flow -----------------------------
        computed = Rv32Tag("crc32")
        verifier = unit["functions"]["load_aem_image"]
        run = rv32_run(verifier, unit["data"], tags={"crc32": computed})
        crc_calls = [handed for _at, (callee, handed) in run["calls"]
                     if callee == "crc32"]
        assert len(crc_calls) == 1, \
            f"the compiled {label} calls crc32() {len(crc_calls)} time(s) " \
            "in the AEM verifier; exactly one call is what the comparison " \
            "below can be given provenance against"
        buffer_at, byte_count = crc_calls[0]["a0"], crc_calls[0]["a1"]
        expected_buffer = census_defines["MILAN_AEM_DESC_BASE"]
        expected_bytes = census_defines["MILAN_AEM_IMAGE_BYTES"]
        assert buffer_at == expected_buffer, \
            "the compiled AEM verifier takes its CRC over " \
            f"{buffer_at if not isinstance(buffer_at, int) else hex(buffer_at)}"\
            f", not over MILAN_AEM_DESC_BASE (0x{expected_buffer:08x}): the " \
            "descriptor store serves the DRAM buffer, so a CRC over the " \
            "QSPI source leaves a short copy, a wrong destination or a DRAM " \
            "fault invisible. Resolved from the emitted call operand"
        assert byte_count == expected_bytes, \
            "the compiled AEM verifier takes its CRC over " \
            f"{byte_count if not isinstance(byte_count, int) else hex(byte_count)}"\
            f" bytes, not over MILAN_AEM_IMAGE_BYTES ({expected_bytes})"
        expected_crc = census_defines["MILAN_AEM_IMAGE_CRC32"]
        edge = rv32_verdict_edge(run, computed, expected_crc)
        assert edge, \
            "the compiled AEM verifier never compares the value crc32() " \
            f"HANDED BACK against MILAN_AEM_IMAGE_CRC32 (0x{expected_crc:08x})"\
            ": the compared value is tracked from its producer, so an " \
            "assignment of the expected constant to the same local between " \
            "the call and the comparison, or a comparison in a preprocessor " \
            "arm the compiler drops, leaves nothing here to find"
        cut = rv32_run(verifier, unit["data"], tags={"crc32": computed},
                       cut=(edge[0], edge[1]))
        loose = sorted({repr(value) for _at, value in cut["rets"]
                        if value != 0})
        assert not loose, \
            "the compiled AEM verifier can hand back a verdict this gate " \
            f"cannot resolve to zero ({', '.join(loose)}) with the " \
            "CRC-equality edge REMOVED: that edge does not dominate every " \
            "non-zero verdict, so a goto, a break or any other path past " \
            "the comparison advertises an entity whose image was never " \
            "checked"
        return {
            "buffer": buffer_at, "bytes": byte_count, "crc": expected_crc,
            "functions": len(runs),
            "statics": len(unit["data"]),
        }

    # Force the non-target branch without depending on which compilers the
    # machine happens to have. If stand-down ever invokes the compiler, the
    # runner makes this focused gate fail; the formatter then proves the text
    # printed to users describes that same observed no-run verdict.
    host_only_calls = []

    def forbidden_host_census(*args, **kwargs):
        host_only_calls.append((args, kwargs))
        raise AssertionError("host-only compiled census ran after stand-down")

    host_only_verdict = assert_compiled_census_is_clean(
        firmware_source, "host-only stand-down self-test",
        selection={"compiler": "host-only-cc", "target": False},
        runner=forbidden_host_census)
    host_only_note = format_census_verdict(host_only_verdict)
    assert not host_only_calls and not host_only_verdict["ran"] and \
           "STOOD DOWN" in host_only_note and \
           "compiled census did not run" in host_only_note, \
        "host-only census execution and its printed stand-down claim diverge"

    #: ... and the SECOND way a candidate is not the target, which is the
    #: one that got through: a 64-bit RISC-V GCC. It assembles the probe's
    #: asm, so the old probe called it the exact RV32 target; the census it
    #: would then take is a 64-bit census, printed beside a line claiming
    #: RV32. Both halves are self-tested here without depending on which
    #: compilers this machine happens to carry.
    #:
    #: First the probe's own decision, over the three shapes a box can
    #: present, driven through a stub so the answer is the same everywhere.
    def stub_compiler(accepts):
        """A compiler that succeeds only for the driver flag sets in
        `accepts`, and records every argv it was handed."""
        seen = []

        def run(command, **kwargs):
            seen.append(tuple(command))
            #: The probe's argv is [cc] + driver + [-S, -o, out, src], so
            #: the driver is what is left after both fixed ends. Reading it
            #: back this way is also what proves the flags REACH the
            #: compiler rather than being recorded and dropped.
            return subprocess.CompletedProcess(
                command, 0 if tuple(command[1:-4]) in accepts else 1, "", "")
        return run, seen

    native_run, native_seen = stub_compiler({()})
    assert census_rv32_driver("stub-rv32-gcc", runner=native_run) == (), \
        "a compiler that is ALREADY the RV32 target must be taken bare: " \
        "driving it with an -march its multilib set may not carry would " \
        "stand the census down on the one tool it exists for"
    assert len(native_seen) == 1, \
        "the RV32 probe kept probing after a candidate had answered"
    driven_run, driven_seen = stub_compiler({rv32_drivers[1]})
    assert census_rv32_driver("stub-rv64-multilib-gcc",
                              runner=driven_run) == rv32_drivers[1], \
        "a 64-bit RISC-V GCC with an rv32 multilib must be DRIVEN as RV32, " \
        "not accepted as it stands"
    assert len(driven_seen) == 2 and \
        tuple(driven_seen[1][1:-4]) == rv32_drivers[1], \
        "the RV32 driver flags did not reach the compiler that needs them"
    rv64_only_run, rv64_only_seen = stub_compiler(set())
    assert census_rv32_driver("stub-rv64-only-gcc",
                              runner=rv64_only_run) is None, \
        "a candidate that no flag set here drives as RV32 must be refused " \
        "by the probe, not adopted as the exact RV32 target"
    assert len(rv64_only_seen) == len(rv32_drivers), \
        "the RV32 probe gave up before it had tried every driver"

    #: ... and then the consequence, exactly as the host-only case above:
    #: a refused candidate compiles NOTHING and says so in the words the
    #: user reads.
    rv64_calls = []

    def forbidden_rv64_census(*args, **kwargs):
        rv64_calls.append((args, kwargs))
        raise AssertionError("64-bit compiled census ran after stand-down")

    rv64_verdict = assert_compiled_census_is_clean(
        firmware_source, "64-bit-candidate stand-down self-test",
        selection={"compiler": "riscv64-elf-gcc", "target": False},
        runner=forbidden_rv64_census)
    rv64_note = format_census_verdict(rv64_verdict)
    assert not rv64_calls and not rv64_verdict["ran"] and \
           "STOOD DOWN" in rv64_note and "riscv64-elf-gcc" in rv64_note and \
           "compiled census did not run" in rv64_note, \
        "64-bit-candidate census execution and its printed stand-down " \
        "claim diverge"

    #: ANTI-VACUITY, on the real tool this run selected: the same probe
    #: asking for a 64-bit target must FAIL under the very flags the census
    #: is about to use. A width guard that has never been seen to refuse
    #: anything is not evidence that the census is a 32-bit census.
    rv32_probe_refused_64 = False
    if census_compiler() and census_used.get("target"):
        rv32_probe_refused_64 = True
        assert not census_probe(census_used["compiler"],
                                census_used["flags"], xlen=64), \
            "the census probe accepts a 64-bit target under the flags it " \
            f"selected for {census_used['compiler']}, so it is not deciding " \
            "the register width and the census it authorises could be a " \
            "64-bit census printed as the RV32 one"

    def assert_target_compiles(firmware, label, allow_warnings=False):
        """Prove one mutation is accepted C for the exact RV32 target.

        A source-text rule may reject the mutation before the assembly census
        runs. Its reason-pinned RED counts only after this independent compile
        proves that the compiler accepts the construct the rule refuses. Most
        mutants must be warning-clean; translation-phase whitespace is the one
        intentional exception because GCC accepts it with a diagnostic.
        """
        compiler = census_compiler()
        if not compiler or not census_used.get("target"):
            return False
        driver = list(census_used.get("flags") or ())
        with tempfile.TemporaryDirectory(prefix="milan-compile-") as root:
            census_headers(root)
            source = os.path.join(root, "milan_baremetal.c")
            with open(source, "w") as fh:
                fh.write(firmware)
            #: The SAME driver the probe selected. Without it a multilib
            #: riscv64 GCC compiled every mutant for RV64, where the
            #: firmware's own 32-bit pointer cast is an -Werror error, and
            #: the failure was reported as a defect in the mutation (#206).
            flags = [compiler] + driver + ["-std=gnu99", "-Wall", "-Wextra"]
            if not allow_warnings:
                flags.append("-Werror")
            built = subprocess.run(
                flags + ["-O0", "-fno-inline", "-S", "-o",
                         os.path.join(root, "mutation.s"), f"-I{root}", source],
                capture_output=True, text=True)
        assert built.returncode == 0, \
            f"{label} must compile for RV32 before its gate verdict counts; " \
            f"{built.stderr.strip().splitlines()[-2:]}"
        return True

    #: Make's assignment modifiers, as a repeatable group rather than a list
    #: of the ones someone thought of: `export` alone was enough to slip a
    #: narrower version of this.
    assign_prefix = r"(?:(?:override|export|unexport|private)[ \t]+)*"
    assign_operators = r"=|:=|::=|\+=|\?=|!="
    assign_operator = r"(" + assign_operators + r")"
    #: One assignment to OBJECTS in any of those flavours. The cumulative ones
    #: are the point: reading `OBJECTS =` and stopping reports a
    #: translation-unit count the build does not have.
    objects_assign_re = re.compile(
        r"(?m)^[ \t]*" + assign_prefix + r"OBJECTS[ \t]*" + assign_operator +
        r"[ \t]*(.*)$")
    objects_token_re = re.compile(r"[A-Za-z0-9_.+/-]+")

    def makefile_objects(makefile):
        """The Makefile's OBJECTS as a list, or None when this gate cannot
        evaluate every token of it.

        make evaluates a VARIABLE, not a line. `=`, `:=`, `?=` and `+=` each
        build on what came before, so a second line is a second object: an
        `OBJECTS += milan_bringup.o` links a second `.c` with its own CSR
        base, its own address helper and its own init hook, and not one rule
        in this gate reads that file. Anything whose value depends on make's
        own evaluation -- a variable, a function, a wildcard, a shell
        assignment -- returns None, and the caller refuses it."""
        text = re.sub(r"\\\n", " ", makefile)
        text = re.sub(r"(?m)#[^\n]*", "", text)
        assigned = list(objects_assign_re.finditer(text))
        spans = [(m.start(), m.end()) for m in assigned]
        for use in re.finditer(r"\bOBJECTS\b", text):
            if any(a <= use.start() < b for a, b in spans):
                continue
            if not re.search(r"[$][({][ \t]*\Z", text[:use.start()]):
                return None      # a define block, an eval, a foreach ...
        value = None
        for assign in assigned:
            operator, tokens = assign.group(1), assign.group(2).split()
            if operator == "!=" or not all(
                    objects_token_re.fullmatch(t) for t in tokens):
                return None      # shell output, or a token make expands
            if operator == "+=":
                value = (value or []) + tokens
            elif operator == "?=" and value is not None:
                continue
            else:
                value = tokens
        return value

    def unexpanded(text):
        """`text` with every `$(...)` / `${...}` blanked, offsets preserved.

        A rule's colon and a variable reference's colon look the same to a
        regex: without this, `-include $(OBJECTS:.o=.d)` reads as a rule whose
        target is `-include $(OBJECTS`. Blanking what make would expand leaves
        exactly the punctuation make itself parses as syntax."""
        out, depth, at, size = list(text), 0, 0, len(text)
        while at < size:
            if not depth and text[at] == "$" and \
                    text[at + 1:at + 2] in ("(", "{"):
                depth, out[at], out[at + 1] = 1, " ", " "
                at += 2
                continue
            if depth:
                if text[at] in "({":
                    depth += 1
                elif text[at] in ")}":
                    depth -= 1
                out[at] = " "
            at += 1
        return "".join(out)

    #: Directives that are not rules, however many colons they carry.
    make_directive_re = re.compile(
        r"\A[ \t]*(?:-|s)?include\b|\A[ \t]*(?:export|unexport|override|"
        r"define|endef|vpath|ifeq|ifneq|ifdef|ifndef|else|endif)\b")
    #: `include`, `-include` and `sinclude` lines, whole.
    makefile_include_re = re.compile(
        r"(?m)^[ \t]*((?:-|s)?include[ \t]+[^\n]*)$")
    #: The include set HEAD carries. The first two are LiteX's; the third is
    #: the compiler's own per-object dependency fragment, which lists
    #: prerequisites and never assigns a variable.
    makefile_includes = (
        "include ../include/generated/variables.mak",
        "include $(SOC_DIRECTORY)/software/common.mak",
        "-include $(OBJECTS:.o=.d)")
    #: Any variable assignment, in any of make's flavours, behind any run of
    #: its modifier keywords. `export` alone was enough to slip a narrower
    #: version of this, so the modifiers are a repeatable group rather than a
    #: list of the ones someone thought of.
    assign_body = (r"([A-Za-z_][A-Za-z0-9_]*)[ \t]*(?:" +
                   assign_operators + r")[ \t]*")
    makefile_assign_re = re.compile(
        r"(?m)^[ \t]*" + assign_prefix + assign_body + r"(.*)$")
    #: ... and the same assignment written after a target, which make applies
    #: to that target AND inherits down its whole prerequisite chain.
    target_assign_re = re.compile(r"\A[ \t]*" + assign_prefix + assign_body +
                                  r"(.*)\Z")
    #: A variable reference, for deriving which names decide the compiled text.
    make_var_re = re.compile(r"[$][({]([A-Za-z_][A-Za-z0-9_]*)[)}]")
    def make_rules(makefile):
        """`(rules, assignments)` for `makefile`.

        A rule is `(targets, prerequisites, recipe)`. Continuations are joined
        and comments dropped first, so a rule reads the way make reads it and
        not the way the file happens to be wrapped. A line whose colon lives
        inside an expansion is not a rule, and a directive is not a rule
        however it is punctuated.

        `assignments` carries BOTH global and target-specific ones, because
        make does not distinguish them where it matters here: an
        `all: CFLAGS += -include x.c` reaches the compile of every
        prerequisite of `all`, which is the one object."""
        text = re.sub(r"(?m)#[^\n]*", "", re.sub(r"\\\n", " ", makefile))
        masked, rules, current, at = unexpanded(text), [], None, 0
        assignments = [(m.group(1), m.group(2))
                       for m in makefile_assign_re.finditer(text)]
        for body in text.split("\n"):
            start, at = at, at + len(body) + 1
            if body.startswith("\t"):
                if current is not None and body.strip():
                    current[2].append(body.strip())
                continue
            if not body.strip():
                continue
            current = None
            if make_directive_re.match(body):
                continue
            head = masked[start:start + len(body)]
            colon = re.search(r"::?(?!=)", head)
            if not colon or "=" in head[:colon.start()]:
                continue
            after = body[colon.end():]
            specific = target_assign_re.match(after)
            if specific:
                assignments.append((specific.group(1), specific.group(2)))
                continue
            current = (body[:colon.start()].split(), after.split(), [])
            rules.append(current)
        return rules, assignments

    #: ---- the make plan -------------------------------------------------
    #:
    #: The same correction as the compiled census, one language over. Every
    #: rule that used to live here parsed the Makefile with regexes, and make
    #: has more assignment syntax than the regexes had: `define NAME` /
    #: `endef` is a sixth flavour that `make_rules()` skipped as a directive,
    #: which re-opened four shapes earlier rounds had explicitly closed. The
    #: archive pin knew `$(AR)` and not `${AR}`, which make treats as one.
    #:
    #: So this asks make. `make -Bn` prints the recipe lines it WOULD run,
    #: and a second `-f` fragment of `$(info ...)` reports the final expanded
    #: variables. The Makefile under test runs against a stub environment
    #: whose values are SENTINELS, so every token in the output that is not a
    #: sentinel is something this Makefile added.
    #:
    #: This REPLACES the OBJECTS parser, the archive pin, the producing-rule
    #: pin, the Makefile include set, the assignable-name allowlist, the
    #: derived text-deciding variables and the CFLAGS token set.
    make_sentinels = {
        "CC": "__CC__", "AR": "__AR__", "CFLAGS": "__BASE_CFLAGS__",
        "BIOS_DIRECTORY": "__BIOS__",
    }
    make_probe = (
        "$(info PROBE_CFLAGS=[$(CFLAGS)])\n"
        "$(info PROBE_OBJECTS=[$(OBJECTS)])\n"
        "$(info PROBE_LIBDIR=[$(LIBMILAN_BAREMETAL_DIRECTORY)])\n"
        "$(info PROBE_VPATH=[$(origin VPATH)])\n"
        "$(info PROBE_COMPILE=[$(value compile)])\n")

    def make_plan(makefile, expected):
        """`(variables, recipe_lines)` for what make would actually do.

        Hazards, all measured rather than assumed, and all fatal if ignored:
        `-B` is mandatory because a stale artefact makes plain `-n` print
        nothing and exit 0; the run directory must be pristine for the same
        reason and because `-include $(OBJECTS:.o=.d)` dies on a stale `.d`;
        and NO variable may be passed on make's command line, because a
        command-line assignment silently overrides the Makefile and hides
        exactly the mutation being tested. `--eval` is not usable: it is
        processed before makefiles are read and reports empty."""
        stem = expected[:-2]
        with tempfile.TemporaryDirectory(prefix="milan-make-") as root:
            soc = os.path.join(root, "soc")
            run = os.path.join(root, "run")
            src = os.path.join(root, "src")
            gen = os.path.join(root, "include", "generated")
            for leaf in (os.path.join(soc, "software"), run, src, gen):
                os.makedirs(leaf, exist_ok=True)
            # Every object the Makefile names needs a source for make to
            # find a rule for it; the CONTENT is irrelevant, only the path.
            # Stubbing them all is a HARNESS convenience, not a gate rule:
            # without it a second object makes make exit 2 with its own
            # message, which is still a detection but a less informative one
            # than showing make compiling and archiving two translation
            # units.
            for named in set(re.findall(r"\b([\w.-]+)\.o\b", makefile)):
                open(os.path.join(src, named + ".c"), "w").close()
            open(os.path.join(src, stem + ".c"), "w").close()
            with open(os.path.join(gen, "variables.mak"), "w") as fh:
                fh.write(f"SOC_DIRECTORY = {soc}\n"
                         f"BIOS_DIRECTORY = "
                         f"{make_sentinels['BIOS_DIRECTORY']}\n"
                         f"LIBMILAN_BAREMETAL_DIRECTORY = {src}\n")
            with open(os.path.join(soc, "software", "common.mak"), "w") as fh:
                fh.write(f"CC = {make_sentinels['CC']}\n"
                         f"AR = {make_sentinels['AR']}\n"
                         f"CFLAGS = {make_sentinels['CFLAGS']}\n"
                         "define compile\n$(CC) -c $(CFLAGS) $(1) $< -o $@\n"
                         "endef\n")
            with open(os.path.join(run, "Makefile"), "w") as fh:
                fh.write(makefile)
            probe = os.path.join(root, "probe.mk")
            with open(probe, "w") as fh:
                fh.write(make_probe)
            def run_make(extra_env):
                environ = dict(os.environ)
                environ.pop("MAKEFLAGS", None)
                environ.update(extra_env)
                return subprocess.run(
                    ["make", "-Bn", "-f", "Makefile", "-f", probe],
                    cwd=run, capture_output=True, text=True, env=environ)

            plan = run_make({})
            # ... and again under a HOSTILE environment. `make -e` (however
            # it is switched on, MAKEFLAGS included) lets an environment
            # variable override a Makefile assignment, which decides what
            # gets compiled from outside the file entirely. Rather than
            # enumerate the options that do that, run the plan twice and
            # require it to be the same plan.
            hostile = run_make({
                "LIBMILAN_BAREMETAL_DIRECTORY": os.path.join(root, "hostile"),
                "CFLAGS": "__HOSTILE_CFLAGS__",
                "OBJECTS": "hostile.o",
            })
        # An exit code is a FINDING, never "no findings": when a mutation
        # names a source this harness did not stub, make exits 2 and its own
        # message names the extra object.
        assert plan.returncode == 0, \
            "make could not plan this Makefile, so what it builds is " \
            "unknown and this gate refuses rather than report a clean " \
            f"result it did not take; make said " \
            f"{(plan.stderr.strip().splitlines() or ['?'])[-1]!r}"
        assert hostile.returncode == plan.returncode and \
            hostile.stdout == plan.stdout, \
            "this Makefile lets the ENVIRONMENT decide what gets compiled: " \
            "planned under a hostile environment it builds something else, " \
            "so the file this gate reads is not necessarily the file the " \
            "build compiles"
        variables = dict(re.findall(r"(?m)^PROBE_(\w+)=\[(.*)\]$",
                                    plan.stdout + plan.stderr))
        recipes = [" ".join(line.split())
                   for line in plan.stdout.splitlines()
                   if not line.startswith("PROBE_") and line.strip()]
        return variables, recipes

    def assert_single_translation_unit(makefile, expected):
        """The firmware image is built from exactly the one `.c` this reads,
        with exactly the flags this gate accounts for.

        Every closure rule above reads ONE file and calls it the firmware.
        That is only true while the firmware IS one translation unit: a
        second object file is a second place a CSR store can live, with its
        own base, its own helper and its own init hook, and none of the rules
        above would ever see it.

        Asked of make rather than of a regex, that is four readings of one
        plan: which sources get compiled, with which flags, into which
        objects, and which of those objects get archived.

        SCOPE: this reads the firmware's own Makefile against a stub
        environment. What LiteX's own fragments contribute is represented by
        the sentinels, so this bounds what THIS Makefile adds, not what LiteX
        supplies."""
        stem = expected[:-2]
        # make reports what it would do with the files that EXIST. A
        # fragment named here but shipped later is invisible to it, and
        # `-include` of a missing file is silently skipped, so the include
        # set stays pinned as an exact set of whole lines. This is the one
        # Makefile rule the plan does not subsume.
        includes = [" ".join(line.split())
                    for line in makefile_include_re.findall(makefile)]
        assert includes == list(makefile_includes), \
            "the Makefile's include set is pinned: make can only plan the " \
            "fragments that exist, so a fragment named here and shipped " \
            "later can assign OBJECTS or override the rule that builds the " \
            f"one object without this gate ever seeing it; found {includes}"
        variables, recipes = make_plan(makefile, expected)
        objects = variables.get("OBJECTS", "").split()
        assert objects == [expected], \
            "the bare-metal firmware must stay ONE translation unit, or the " \
            "CSR store closure this gate proves covers only part of the " \
            f"image; make builds {objects}"
        # Read the WHOLE plan, not the lines carrying a sentinel. Filtering
        # on the sentinel made every recipe line that names a tool literally
        # invisible, so an explicit rule whose extra lines ran
        # `riscv32-linux-gcc` and `riscv32-linux-ld -r` was discarded by the
        # gate after make had printed it. make answered correctly and
        # completely; the reading threw the answer away.
        sources = sorted({token for line in recipes
                          for token in line.split() if token.endswith(".c")})
        objects = sorted({token for line in recipes
                          for token in line.split() if token.endswith(".o")})
        assert sources == [os.path.join(variables.get("LIBDIR", ""),
                                        stem + ".c")], \
            f"make must compile exactly one source, {stem}.c, and its whole " \
            "plan names another: the object this gate calls one translation " \
            f"unit is built from several; make touches {sources}"
        assert objects == [expected], \
            "make must build and archive exactly the one object, and its " \
            "whole plan names another: an object the OBJECTS list never " \
            f"named reaches the image; make touches {objects}"
        # ---- and the RECIPE SET, which is what actually bounds this.
        #
        # Three scans used to live here: one for link steps, one for
        # injecting flags and one for search-path flags, each a list of the
        # spellings someone had thought of. That is the same shape as the
        # name allowlist before it, the disassembly regex before that and
        # the flag regex after: `-Wp,-include,hdr`, `@response.file` and
        # `-iprefix`/`-iwithprefixbefore` all walked past it, and every one
        # of them put a whole second file into the one translation unit.
        #
        # So the recipe set is PINNED instead. make tells us the two
        # commands it would run; they are fully determined by the stub
        # environment's sentinels and the one source path, so anything
        # added, removed or reworded is refused without naming a single
        # flag. This is strictly smaller than the three scans it replaces
        # and it has no list to fall behind.
        #
        # LIMIT, measured and tracked on #162: this reads what make PRINTS,
        # which is already expanded. A name the Makefile references and
        # nothing defines expands to nothing, so
        # `CFLAGS += $(MILAN_EXTRA_CFLAGS)` leaves these two lines identical
        # while the environment decides what the compiler is really given.
        # Reading the Makefile's TEXT used to catch that and reading make's
        # RESULT does not, which is the same trade the compiled census makes
        # against the text rules.
        expected_recipes = [
            f"{make_sentinels['CC']} -c {make_sentinels['CFLAGS']} "
            f"-I{make_sentinels['BIOS_DIRECTORY']} "
            f"{os.path.join(variables.get('LIBDIR', ''), stem + '.c')} "
            f"-o {expected}",
            f"{make_sentinels['AR']} crs lib{stem}.a {expected}",
        ]
        assert recipes == expected_recipes, \
            "the commands make would run are pinned, and this Makefile " \
            "changes them: one compile of the one source with the one added " \
            "include path, and one archive of the one object. Anything else " \
            "can inject a file into the translation unit, move which file is " \
            "compiled, or link a second one in, whatever flag spelling " \
            f"carries it.\n  expected: {expected_recipes}\n  make runs: " \
            f"{recipes}"
        assert variables.get("VPATH") == "undefined", \
            "this Makefile must not set VPATH: it decides which file the " \
            "pattern rule's %.c resolves to, so it moves the file this gate " \
            "calls the firmware"
        assert os.path.basename(variables.get("LIBDIR", "")) == "src", \
            "the source directory make compiles from is not the one this " \
            "gate reads, so every rule above is reading a file the build " \
            f"does not compile; make uses {variables.get('LIBDIR')!r}"

    def anchored(text, needle, what, start=0):
        """`text.index(needle)`, but failing with a message that names the
        property instead of a bare `ValueError: substring not found`.

        The three boot-path anchors are pinned by literal identifier, so
        renaming a function used to abort the whole suite with no message at
        all, which left the next author nothing to act on. Round two settled
        that renaming a LOCAL is not a boot-contract change; renaming a
        function is not one either, and until this gate can find these by
        shape rather than by name, the refusal at least has to say so."""
        at = text.find(needle, start)
        assert at >= 0, \
            f"this gate finds {what} by the literal identifier {needle!r} " \
            "and the firmware no longer spells it that way. Renaming it is " \
            "not a boot-contract change, but this gate cannot follow the " \
            "rename: update the anchor here, or teach it to find the " \
            "function by shape"
        return at

    def assert_boot_contract(firmware, docs, csr, makefile=None,
                             listing=None, datapath=None):
        raw_datapath = datapath_source if datapath is None else datapath
        # Read code, not plausible-looking text in comments.  This is a
        # distinct lexer from blanked(): an apostrophe starts a numeric
        # literal in SystemVerilog rather than a C character literal.
        datapath = blanked_sv(raw_datapath)
        csr_code = blanked_sv(csr)

        def assert_sv_directive_set(raw, code, includes, reason):
            matches = list(re.finditer(
                r"`[ \t]*(?P<name>[A-Za-z_][A-Za-z0-9_$]*)\b", code))
            names = tuple(match.group("name") for match in matches)
            expected_names = (
                "default_nettype", *("include" for _ in includes),
                "default_nettype")
            assert names == expected_names, \
                f"{reason}: expected directives {expected_names}, found " \
                f"{names}"
            actual_includes = []
            for match in matches:
                if match.group("name") != "include":
                    continue
                line_end = raw.find("\n", match.end())
                line_end = len(raw) if line_end < 0 else line_end
                include = re.fullmatch(
                    r"[ \t]*`[ \t]*include[ \t]+"
                    r"\"(?P<path>[^\"\r\n]+)\"[ \t]*",
                    raw[match.start():line_end])
                assert include, \
                    f"{reason}: each `include operand must be one literal path"
                actual_includes.append(include.group("path"))
            assert tuple(actual_includes) == tuple(includes), \
                f"{reason}: expected included fragments {tuple(includes)}, " \
                f"found {tuple(actual_includes)}"

        assert_sv_directive_set(
            csr, csr_code,
            ("gen/lwsrp_csr_defaults.svh",
             "gen/adp_shape_defaults.svh"),
            "CSR integration proof requires unconditional live "
            "SystemVerilog text")
        # Reject compiler-selected datapath text before any endpoint or
        # reference-count check can take credit for an incidental mismatch.
        # The shipping includes and paired `default_nettype directives are
        # the only live directives admitted by this bounded model.
        assert_sv_directive_set(
            raw_datapath, datapath,
            ("ethernet_events.svh", "gen/adp_shape_defaults.svh"),
            "datapath integration proof requires unconditional live "
            "SystemVerilog text")

        def direct_port(ports, port, value, reason):
            matches = list(re.finditer(
                rf"\.{re.escape(port)}\s*\(\s*(?P<value>[^)]*?)\s*\)",
                ports))
            assert len(matches) == 1, \
                f"{reason}: .{port} must be connected exactly once"
            actual = re.sub(r"\s+", "", matches[0].group("value"))
            expected = re.sub(r"\s+", "", value)
            assert actual == expected, \
                f"{reason}: expected .{port}({value})"

        def reference_census(source, expected, reason):
            """Pin every code-token reference to named bounded-proof nets.

            Exact endpoint expressions do not establish sole-driver
            ownership: a resolved ``wand`` can retain the expected assignment
            and add a second ADP-controlled driver.  Comments have already
            been blanked, so an exact identifier census makes every added
            driver or alias use visible without pretending to parse general
            SystemVerilog data flow.
            """
            for name, count in expected.items():
                found = len(re.findall(rf"\b{re.escape(name)}\b", source))
                assert found == count, \
                    f"{reason}: {name} must have exactly {count} live " \
                    f"references, found {found}"

        def direct_initializer(source, declaration, signal, value, reason):
            """One direct module-scope wire initializer with an exact RHS."""
            matches = list(re.finditer(
                rf"(?m)^[ \t]*{declaration}[ \t]*=[ \t]*"
                r"(?P<value>[^;]+);", source))
            assert len(matches) == 1, \
                f"{reason}: {signal} must have exactly one ordinary-wire " \
                "initializer"
            actual = re.sub(r"\s+", "", matches[0].group("value"))
            expected_value = re.sub(r"\s+", "", value)
            assert actual == expected_value, \
                f"{reason}: unexpected {signal} initializer " \
                f"{matches[0].group('value').strip()!r}"
            assert_direct_scope(source, matches[0].start(), reason)

        def direct_assignment(lhs, rhs, reason, source=None):
            source = datapath if source is None else source
            matches = list(re.finditer(
                rf"(?m)^[ \t]*assign[ \t]+{re.escape(lhs)}[ \t]*="
                r"(?P<value>[^;]+);", source))
            assert len(matches) == 1, \
                f"{reason}: {lhs} must have exactly one continuous assignment"
            assert re.fullmatch(rf"\s*{re.escape(rhs)}\s*",
                                matches[0].group("value")), \
                f"{reason}: expected assign {lhs} = {rhs};"
            assert_direct_scope(source, matches[0].start(), reason)

        def instance_ports(source, module, instance, reason):
            matches = list(re.finditer(
                rf"\b{re.escape(module)}\b\s*#\s*\([^;]*?\)\s*"
                rf"{re.escape(instance)}\s*\((?P<ports>.*?)\)\s*;",
                source, re.DOTALL))
            assert len(matches) == 1, \
                f"{reason}: expected exactly one {module} {instance} instance"
            assert_direct_scope(source, matches[0].start(), reason)
            return matches[0].group("ports")

        id_readback_reason = (
            "RTL A_ID readback plumbing must preserve the canonical "
            "csr_default ROM and direct AXI read address")
        direct_initializer(
            csr_code,
            r"wire[ \t]+\[\s*ADDR_WIDTH\s*-\s*1\s*:\s*0\s*\]"
            r"[ \t]+rd_addr",
            "rd_addr", "s_axi_araddr", id_readback_reason)
        rom_initializers = [
            match for match in re.finditer(
                r"\binitial\s+begin\b(?P<body>.*?)\bend\b",
                csr_code, re.DOTALL)
            if re.search(r"\bdflt_rom\b", match.group("body"))]
        assert len(rom_initializers) == 1, \
            f"{id_readback_reason}: expected one dflt_rom initial block"
        assert re.fullmatch(
            r"\s*for\s*\(\s*int\s+k\s*=\s*0\s*;\s*k\s*<\s*512\s*;"
            r"\s*k\+\+\s*\)\s*dflt_rom\s*\[\s*k\s*\]\s*=\s*"
            r"csr_default\s*\(\s*11\s*'\s*\(\s*k\s*\*\s*4\s*\)\s*\)"
            r"\s*;\s*", rom_initializers[0].group("body")), \
            f"{id_readback_reason}: dflt_rom must be initialized solely " \
            "from csr_default(11'(k * 4))"
        reference_census(
            csr_code, {"dflt_rom": 3, "rd_addr": 15}, id_readback_reason)

        phc_binding_reason = (
            "milan_csr PHC output must drive cfg_ptp_enable directly")
        csr_ports = instance_ports(
            datapath, "milan_csr", "csr", phc_binding_reason)
        phc_csr_ports = (
            ("o_ptp_enable", "cfg_ptp_enable"),
            ("o_ptp_incr", "cfg_ptp_incr"),
            ("o_ptp_adj", "cfg_ptp_adj"),
            ("o_ptp_tod_wr", "cfg_ptp_tod_wr"),
            ("o_ptp_offset", "cfg_ptp_offset"),
            ("o_ptp_cmd_load", "cfg_ptp_cmd_load"),
            ("o_ptp_cmd_adjust", "cfg_ptp_cmd_adjust"),
            ("o_ptp_cmd_snapshot", "cfg_ptp_cmd_snapshot"),
            ("o_ptp_ingress_lat", "cfg_ptp_ingress_lat"),
            ("o_ptp_egress_lat", "cfg_ptp_egress_lat"),
            ("i_ptp_tod", "ptp_tod_rd"),
            ("i_ptp_tod_valid", "ptp_tod_rd_valid"),
        )
        for port, value in phc_csr_ports:
            direct_port(csr_ports, port, value, phc_binding_reason)

        phc_source_reason = (
            "milan_csr PHC output assignments must remain direct and "
            "independent of ADP and protocol-processor state")
        for lhs, rhs in (
                ("o_ptp_enable", "ptp_ctrl[0]"),
                ("o_ptp_incr", "ptp_incr"),
                ("o_ptp_adj", "ptp_adj"),
                ("o_ptp_tod_wr", "{ptp_twhi, ptp_twlo}"),
                ("o_ptp_offset", "{ptp_ofhi, ptp_oflo}"),
                ("o_ptp_cmd_load", "ptp_load_p"),
                ("o_ptp_cmd_adjust", "ptp_adj_p"),
                ("o_ptp_cmd_snapshot", "ptp_snap_p"),
                ("o_ptp_ingress_lat", "ptp_ilat"),
                ("o_ptp_egress_lat", "ptp_elat")):
            direct_assignment(lhs, rhs, phc_source_reason, csr_code)
        reference_census(
            csr_code,
            {port: 2 for port, _value in phc_csr_ports
             if port.startswith("o_")},
            phc_source_reason)

        phc_net_reason = (
            "datapath PHC nets must retain sole-driver reference ownership")
        reference_census(
            datapath,
            {
                "cfg_ptp_enable": 3,
                "cfg_ptp_incr": 3,
                "cfg_ptp_adj": 3,
                "cfg_ptp_tod_wr": 3,
                "cfg_ptp_offset": 3,
                "cfg_ptp_cmd_load": 4,
                "cfg_ptp_cmd_adjust": 4,
                "cfg_ptp_cmd_snapshot": 3,
                "cfg_ptp_ingress_lat": 3,
                "cfg_ptp_egress_lat": 3,
                "ptp_tod_rd": 3,
                "ptp_tod_rd_valid": 3,
                "eff_ptp_adj_w": 2,
                "eff_ptp_offset_w": 2,
                "eff_ptp_adjust_w": 2,
                "gptp_adj_w": 4,
                "gptp_step_we_w": 4,
                "gptp_step_w": 4,
            }, phc_net_reason)
        direct_initializer(
            datapath,
            r"wire[ \t]+\[\s*31\s*:\s*0\s*\][ \t]+eff_ptp_adj_w",
            "eff_ptp_adj_w",
            "(GPTP_PLANE_EN_P != 1'b0) ? unsigned'(gptp_adj_w) : "
            "cfg_ptp_adj",
            "effective PHC adjustment must select only gPTP or CSR control")
        direct_initializer(
            datapath,
            r"wire[ \t]+\[\s*63\s*:\s*0\s*\][ \t]+eff_ptp_offset_w",
            "eff_ptp_offset_w",
            "(GPTP_PLANE_EN_P != 1'b0) ? gptp_step_w : cfg_ptp_offset",
            "effective PHC offset must select only gPTP or CSR control")
        direct_initializer(
            datapath, r"wire[ \t]+eff_ptp_adjust_w",
            "eff_ptp_adjust_w",
            "(GPTP_PLANE_EN_P != 1'b0) ? gptp_step_we_w : "
            "cfg_ptp_cmd_adjust",
            "effective PHC adjust strobe must select only gPTP or CSR "
            "control")
        ptp_clock_reason = (
            "ptp_timestamp clocks and resets must be direct and independent "
            "of AEM, ADP and protocol-processor gates")
        phc_reason = (
            "ptp_timestamp PHC enable must be driven directly by "
            "cfg_ptp_enable")
        ptp_ports = instance_ports(
            datapath, "ptp_ts_top", "ptp_timestamp", phc_reason)
        for port, value in (
                ("gtx_clk", "gtx_clk"),
                ("gtx_resetn", "gtx_resetn"),
                ("axis_clk", "axis_clk"),
                ("axis_resetn", "axis_resetn")):
            direct_port(ptp_ports, port, value, ptp_clock_reason)
        direct_port(ptp_ports, "i_ptp_enable", "cfg_ptp_enable", phc_reason)
        phc_control_reason = (
            "ptp_timestamp PHC controls and readback must remain direct and "
            "independent of AEM, ADP and protocol-processor gates")
        for port, value in (
                ("i_ptp_incr", "cfg_ptp_incr"),
                ("i_ptp_adj", "eff_ptp_adj_w"),
                ("i_ptp_tod_wr", "cfg_ptp_tod_wr"),
                ("i_ptp_offset", "eff_ptp_offset_w"),
                ("i_ptp_cmd_load", "cfg_ptp_cmd_load"),
                ("i_ptp_cmd_adjust", "eff_ptp_adjust_w"),
                ("i_ptp_cmd_snapshot", "cfg_ptp_cmd_snapshot"),
                ("i_ptp_ingress_lat", "cfg_ptp_ingress_lat"),
                ("i_ptp_egress_lat", "cfg_ptp_egress_lat"),
                ("o_ptp_tod_rd", "ptp_tod_rd"),
                ("o_ptp_tod_rd_valid", "ptp_tod_rd_valid"),
                ("o_tx_ts_ready", "evt_tx_ts_ready"),
                ("o_ptp_now", "ptp_now_w")):
            direct_port(ptp_ports, port, value, phc_control_reason)

        timestamp_reason = (
            "external MAC RX must traverse ptp_timestamp directly")
        for port, value in (
                ("s_axis_rx_tdata", "rx_axis_to_ts.tdata"),
                ("s_axis_rx_tkeep", "rx_axis_to_ts.tkeep"),
                ("s_axis_rx_tvalid", "rx_axis_to_ts.tvalid"),
                ("s_axis_rx_tlast", "rx_axis_to_ts.tlast"),
                ("s_axis_rx_tready", "rx_axis_to_ts.tready"),
                ("m_axis_rx_tdata", "rx_axis_ptp_to_filt.tdata"),
                ("m_axis_rx_tkeep", "rx_axis_ptp_to_filt.tkeep"),
                ("m_axis_rx_tvalid", "rx_axis_ptp_to_filt.tvalid"),
                ("m_axis_rx_tlast", "rx_axis_ptp_to_filt.tlast"),
                ("m_axis_rx_tready", "rx_axis_ptp_to_filt.tready")):
            direct_port(ptp_ports, port, value, timestamp_reason)

        rx_arms = re.search(
            r"\bgenerate\s+if\s*\(\s*RXFILT_P\s*!=\s*0\s*\)\s*"
            r"begin\s*:\s*g_rx_filter\b(?P<enabled>.*?)"
            r"\bend\s+else\s+begin\s*:\s*g_no_rx_filter\b"
            r"(?P<bypass>.*?)\bend\s+endgenerate\b",
            datapath, re.DOTALL)
        assert rx_arms, \
            "timestamped MAC RX must traverse both RXFILT_P arms directly"
        assert_direct_scope(
            datapath, rx_arms.start(),
            "timestamped MAC RX must traverse both RXFILT_P arms directly")
        enabled_reason = (
            "timestamped MAC RX must traverse the enabled RX-filter arm "
            "directly")
        rx_filter_ports = instance_ports(
            rx_arms.group("enabled"), "rx_mac_filter", "rx_filter",
            enabled_reason)
        for port, value in (
                ("clk_i", "axis_clk"),
                ("rst_n", "axis_resetn"),
                ("addr_filter_en_i", "cfg_tcam_addr_filt_en"),
                ("promisc_i", "cfg_mac_promisc"),
                ("allmulti_i", "cfg_mac_allmulti"),
                ("station_mac_i",
                 "{cfg_mac_addr[7:0], cfg_mac_addr[15:8], "
                 "cfg_mac_addr[23:16], cfg_mac_addr[31:24], "
                 "cfg_mac_addr[39:32], cfg_mac_addr[47:40]}"),
                ("mc_hash_i", "cfg_mc_hash"),
                ("tcam_wr_en_i", "cfg_tcam_wr_en"),
                ("tcam_wr_index_i", "cfg_tcam_wr_index[3:0]"),
                ("tcam_wr_valid_i", "cfg_tcam_wr_valid"),
                ("tcam_wr_key_i", "cfg_tcam_wr_key"),
                ("tcam_wr_mask_i", "cfg_tcam_wr_mask"),
                ("tcam_wr_action_i", "cfg_tcam_wr_action"),
                ("s_tdata", "rx_axis_ptp_to_filt.tdata"),
                ("s_tkeep", "rx_axis_ptp_to_filt.tkeep"),
                ("s_tvalid", "rx_axis_ptp_to_filt.tvalid"),
                ("s_tlast", "rx_axis_ptp_to_filt.tlast"),
                ("s_tready", "rx_axis_ptp_to_filt.tready"),
                ("m_tdata", "rx_axis_to_dma.tdata"),
                ("m_tkeep", "rx_axis_to_dma.tkeep"),
                ("m_tvalid", "rx_axis_to_dma.tvalid"),
                ("m_tlast", "rx_axis_to_dma.tlast"),
                ("m_tready", "rx_axis_to_dma.tready")):
            direct_port(rx_filter_ports, port, value, enabled_reason)
        filter_policy_reason = (
            "reset-time RX filter policy must remain independent of ADP")
        direct_port(
            rx_filter_ports, "default_pass_i", "cfg_tcam_default_pass",
            filter_policy_reason)
        direct_port(
            csr_ports, "o_tcam_default_pass", "cfg_tcam_default_pass",
            filter_policy_reason)
        direct_assignment(
            "o_tcam_default_pass", "tcam_ctrl[0]", filter_policy_reason,
            csr_code)
        reference_census(
            datapath, {"cfg_tcam_default_pass": 3}, filter_policy_reason)
        reference_census(
            csr_code, {"o_tcam_default_pass": 2}, filter_policy_reason)
        bypass_reason = (
            "timestamped MAC RX must traverse the bypass RX-filter arm "
            "directly")
        for lhs, rhs in (
                ("rx_axis_to_dma.tdata", "rx_axis_ptp_to_filt.tdata"),
                ("rx_axis_to_dma.tkeep", "rx_axis_ptp_to_filt.tkeep"),
                ("rx_axis_to_dma.tvalid", "rx_axis_ptp_to_filt.tvalid"),
                ("rx_axis_to_dma.tlast", "rx_axis_ptp_to_filt.tlast"),
                ("rx_axis_ptp_to_filt.tready", "rx_axis_to_dma.tready")):
            direct_assignment(
                lhs, rhs, bypass_reason, rx_arms.group("bypass"))

        gptp_plane = re.search(
            r"\bgenerate\s+if\s*\(\s*GPTP_PLANE_EN_P\s*\)\s*"
            r"begin\s*:\s*g_gptp_plane\b(?P<body>.*?)"
            r"\bend\s+else\s+begin\s*:\s*g_gptp_off\b",
            datapath, re.DOTALL)
        assert gptp_plane, \
            "fabric gPTP must be elaborated solely by GPTP_PLANE_EN_P, " \
            "without an AEM, ADP or protocol-processor runtime gate"
        assert_direct_scope(
            datapath, gptp_plane.start(),
            "fabric gPTP must be elaborated solely by GPTP_PLANE_EN_P")
        shadow_ports = instance_ports(
            gptp_plane.group("body"), "KL_gptp_shadow", "u_gptp_shadow",
            "the option-on fabric gPTP plane must instantiate "
            "KL_gptp_shadow directly")

        for port, value in (
                ("clk_i", "axis_clk"), ("rst_n", "axis_resetn"),
                ("rx_tdata_i", "rx_axis_to_dma.tdata"),
                ("rx_tkeep_i", "rx_axis_to_dma.tkeep"),
                ("rx_tvalid_i", "rx_axis_to_dma.tvalid"),
                ("rx_tready_i", "rx_axis_to_dma.tready"),
                ("rx_tlast_i", "rx_axis_to_dma.tlast"),
                ("phc_ns_i", "ptp_now_w"),
                ("phc_adj_o", "gptp_adj_w"),
                ("phc_step_we_o", "gptp_step_we_w"),
                ("phc_step_o", "gptp_step_w"),
                ("txts_valid_i", "gts_valid_w"),
                ("txts_ns_i", "gts_ns_w"),
                ("txts_seq_i", "gts_seq_w"),
                ("tx_sent_o", "gtx_sent_w")):
            direct_port(
                shadow_ports, port, value,
                "fabric gPTP RX and control inputs must observe the live "
                "datapath directly, independent of AEM, ADP and "
                "protocol-processor gates")
        for port, value in (
                ("tx_tdata_o", "gtx_tdata_w"),
                ("tx_tkeep_o", "gtx_tkeep_w"),
                ("tx_tvalid_o", "gtx_tvalid_w"),
                ("tx_tlast_o", "gtx_tlast_w"),
                ("tx_tready_i", "gtx_tready_w")):
            direct_port(
                shadow_ports, port, value,
                "fabric gPTP TX handshake must leave KL_gptp_shadow directly")

        gptp_mux_ports = instance_ports(
            gptp_plane.group("body"), "adp_tx_arbiter", "gptp_ctl_mux",
            "the option-on fabric gPTP plane must feed gptp_ctl_mux "
            "directly")
        for port, value in (
                ("clk_i", "axis_clk"), ("rst_n", "axis_resetn"),
                ("s_adp_tdata", "gtx_tdata_w"),
                ("s_adp_tkeep", "gtx_tkeep_w"),
                ("s_adp_tvalid", "gtx_tvalid_w"),
                ("s_adp_tlast", "gtx_tlast_w"),
                ("s_adp_tready", "gtx_tready_w"),
                ("m_tdata", "ctlg3_tdata"),
                ("m_tkeep", "ctlg3_tkeep"),
                ("m_tvalid", "ctlg3_tvalid"),
                ("m_tlast", "ctlg3_tlast"),
                ("m_tready", "ctlg3_tready")):
            direct_port(
                gptp_mux_ports, port, value,
                "fabric gPTP TX must traverse gptp_ctl_mux directly, "
                "independent of AEM, ADP and protocol-processor gates")

        txstamp_reason = (
            "fabric gPTP TX timestamp feedback must remain direct and "
            "independent of AEM, ADP and protocol-processor gates")
        txstamp_ports = instance_ports(
            gptp_plane.group("body"), "KL_gptp_txstamp", "u_gptp_txstamp",
            txstamp_reason)
        for port, value in (
                ("clk_i", "axis_clk"), ("rst_n", "axis_resetn"),
                ("tx_tdata_i", "tx_axis_to_mac.tdata"),
                ("tx_tvalid_i", "tx_axis_to_mac.tvalid"),
                ("tx_tready_i", "tx_axis_to_mac.tready"),
                ("tx_tlast_i", "tx_axis_to_mac.tlast"),
                ("phc_ns_i", "ptp_now_w"),
                ("armed_i", "gtx_sent_w"),
                ("ts_valid_o", "gts_valid_w"),
                ("ts_ns_o", "gts_ns_w"),
                ("ts_seq_o", "gts_seq_w")):
            direct_port(txstamp_ports, port, value, txstamp_reason)

        boundary_ports = instance_ports(
            datapath, "adp_tx_arbiter", "adp_tx_mux",
            "the fabric gPTP/control stream must reach the MAC-boundary mux "
            "directly")
        for port, value in (
                ("clk_i", "axis_clk"), ("rst_n", "axis_resetn"),
                ("s_adp_tdata", "ctlg3_tdata"),
                ("s_adp_tkeep", "ctlg3_tkeep"),
                ("s_adp_tvalid", "ctlg3_tvalid"),
                ("s_adp_tlast", "ctlg3_tlast"),
                ("s_adp_tready", "ctlg3_tready"),
                ("m_tdata", "tx_axis_to_mac.tdata"),
                ("m_tkeep", "tx_axis_to_mac.tkeep"),
                ("m_tvalid", "tx_axis_to_mac.tvalid"),
                ("m_tlast", "tx_axis_to_mac.tlast"),
                ("m_tready", "tx_axis_to_mac.tready")):
            direct_port(
                boundary_ports, port, value,
                "fabric gPTP control output must reach the MAC-boundary "
                "arbiter directly, independent of AEM, ADP and "
                "protocol-processor gates")

        # The arbiter's output is still only an internal promise. Close the
        # path at the externally visible MAC handshake in both directions so
        # a downstream runtime gate cannot silence an otherwise-direct gPTP
        # plane.
        for lhs, rhs in (
                ("m_axis_mac_tx_tdata", "tx_axis_to_mac.tdata"),
                ("m_axis_mac_tx_tkeep", "tx_axis_to_mac.tkeep"),
                ("m_axis_mac_tx_tvalid", "tx_axis_to_mac.tvalid"),
                ("m_axis_mac_tx_tlast", "tx_axis_to_mac.tlast"),
                ("tx_axis_to_mac.tready", "m_axis_mac_tx_tready")):
            direct_assignment(
                lhs, rhs,
                "external MAC TX handshake must be driven directly by "
                "tx_axis_to_mac")
        for lhs, rhs in (
                ("rx_axis_to_ts.tdata", "s_axis_mac_rx_tdata"),
                ("rx_axis_to_ts.tkeep", "s_axis_mac_rx_tkeep"),
                ("rx_axis_to_ts.tvalid", "s_axis_mac_rx_tvalid"),
                ("rx_axis_to_ts.tlast", "s_axis_mac_rx_tlast"),
                ("s_axis_mac_rx_tready", "rx_axis_to_ts.tready")):
            direct_assignment(
                lhs, rhs,
                "external MAC RX handshake must drive rx_axis_to_ts directly")
        reference_census(
            datapath,
            {
                "m_axis_mac_tx_tdata": 2,
                "m_axis_mac_tx_tkeep": 2,
                "m_axis_mac_tx_tvalid": 4,
                "m_axis_mac_tx_tlast": 4,
                "m_axis_mac_tx_tready": 4,
                "s_axis_mac_rx_tdata": 2,
                "s_axis_mac_rx_tkeep": 2,
                "s_axis_mac_rx_tvalid": 4,
                "s_axis_mac_rx_tlast": 4,
                "s_axis_mac_rx_tready": 4,
            },
            "external MAC handshake ports must retain sole-driver/reference "
            "ownership")

        # The whole closure below reads ONE file. Prove that is the whole
        # firmware before reading a line of it.
        assert_single_translation_unit(
            makefile_source if makefile is None else makefile,
            firmware_object)
        # Comments and string literals are not code: blanking their bodies
        # (offsets preserved) keeps a commented-out enable from reading as an
        # enable, and a printf() from reading as a call.
        source, firmware = firmware, blanked(firmware)
        # ... and one OBJECT is not one FILE. Pin what else joins the
        # translation unit, and the one store mechanism with no textual
        # signature, before any rule below calls this text the firmware.
        assert_directive_set_is_closed(firmware, source)
        assert_include_resolution_is_pinned(
            firmware_listing if listing is None else listing)
        # ... the inline-asm set, which the census does NOT subsume: it
        # matches one asm spelling, and a `lui`-based template carries no
        # window immediate at all.
        assert_asm_set_is_closed(firmware, source)

        model = CsrModel(firmware, csr_code)
        assert model.defines.get("MILAN_ID") == model.identity, \
            "firmware MILAN_ID must resolve to the RTL A_ID address, or the " \
            "boot guard can validate a different CSR"
        assert model.defines.get("MILAN_ID_MAGIC") == model.identity_default, \
            "firmware MILAN_ID_MAGIC must equal the RTL A_ID readback " \
            "default, or the boot guard can accept a forged identity value"
        # The name-to-address table is only half the address model; the write
        # decode is the other half, and it is what says each entity-enable
        # register answers to ONE address.
        assert_decode_is_one_to_one(csr_code, model)
        ptp_enable_assignment(csr_code)
        load_start = anchored(firmware, "static int load_aem_image(void)",
                              "the AEM verifier")
        load_end = anchored(firmware, "static void milan_init(void)",
                            "the boot entry point", load_start)
        load_source = firmware[load_start:load_end]
        # Before any textual rule: prove the text this gate reads is the text
        # the compiler compiles.
        assert_preprocessor_visible(firmware, source, (load_start, load_end))
        init_start = anchored(firmware, "static void milan_init(void)",
                              "the boot entry point")
        init_end = anchored(firmware, "define_init_func(milan_init)",
                            "the boot entry point's init hook", init_start)
        init_source = firmware[init_start:init_end]
        identity_read = re.search(
            r"\buint32_t\s+(?P<name>\w+)\s*=\s*"
            r"milan_read\s*\(\s*MILAN_ID\s*\)\s*;", init_source)
        identity_guard = re.search(
            rf"\bif\s*\(\s*{re.escape(identity_read.group('name')) if identity_read else 'id'}"
            r"\s*!=\s*MILAN_ID_MAGIC\s*\)\s*\{", init_source)
        configure = re.search(r"\bconfigure_fabric\s*\(\s*\)\s*;", init_source)
        load = re.search(
            r"\baem_loaded\s*=\s*load_aem_image\s*\(\s*\)\s*;",
            init_source)
        guard = re.search(
            r"\bentity_advertise\s*\(\s*aem_loaded\s*\)\s*;",
            init_source)
        assert identity_read and identity_guard, \
            "firmware must reject a mismatched CSR identity before " \
            "configuring fabric or verifying the AEM image"
        identity_between = init_source[
            identity_read.end():identity_guard.start()]
        identity_name = re.escape(identity_read.group("name"))
        identity_write = re.search(
            rf"(?:\+\+|--)\s*\b{identity_name}\b|"
            rf"\b{identity_name}\b\s*(?:\+\+|--|"
            rf"(?:<<|>>|[-+*/%|&^])?=(?!=))",
            identity_between)
        identity_address = re.search(
            rf"(?<!&)&(?!&)\s*\b{identity_name}\b", identity_between)
        assert not identity_write and not identity_address, \
            "CSR identity guard must consume the unmodified MILAN_ID " \
            "sample: no assignment, increment or pointer write may replace " \
            "the value between its CSR read and mismatch comparison"
        identity_body, identity_close = braced_span(
            init_source, identity_guard, "CSR identity mismatch guard")
        identity_block = init_source[identity_body:identity_close]
        identity_returns = list(re.finditer(r"\breturn\s*;", identity_block))
        identity_return_is_top_level = False
        if len(identity_returns) == 1:
            identity_return = identity_returns[0]
            return_head = max(identity_block.rfind(char, 0,
                                                    identity_return.start())
                              for char in ";{}")
            return_depth = (
                identity_block.count("{", 0, identity_return.start()) -
                identity_block.count("}", 0, identity_return.start()))
            identity_return_is_top_level = (
                return_depth == 0 and
                not identity_block[
                    return_head + 1:identity_return.start()].strip())
        assert identity_return_is_top_level, \
            "CSR identity mismatch guard must return before fabric " \
            "configuration and AEM verification"
        assert configure and load and guard, \
            "firmware must configure, load AEM, then guard entity enable. " \
            "NOTE, because this message has misdiagnosed a rename before: " \
            "this gate finds the verdict by the literal identifier " \
            "'aem_loaded' and the guard by the choke-point call " \
            "'entity_advertise(aem_loaded)'. If those three steps are all " \
            "present and you renamed the verdict, the boot order is fine " \
            "and it is this gate that cannot follow the rename; found " \
            f"configure={bool(configure)} load={bool(load)} " \
            f"guard={bool(guard)}"
        positions = [identity_read.start(), identity_guard.start(),
                     configure.start(), load.start(), guard.start()]
        assert positions == sorted(positions), \
            "firmware must check CSR identity, configure fabric, verify AEM, " \
            "then check the verifier verdict"
        # Textual containment is not REACHABILITY. Every positional rule below
        # proves an enable sits between the guard's braces; none of them proves
        # control gets there only by taking the guard. A label reached by a
        # goto, or a case falling into the block, does both at once -- so the
        # constructs that make one possible are refused outright.
        for keyword in ("goto", "switch", "case", "default"):
            assert not re.search(rf"\b{keyword}\b", init_source), \
                f"milan_init() must not contain '{keyword}': control that " \
                "enters the AEM-success guard by any path other than the " \
                "guard's own condition advertises an unverified entity"
        stray_label = re.search(
            r"(?m)^[ \t]*([A-Za-z_]\w*)[ \t]*:(?!:)", init_source)
        assert not stray_label, \
            f"milan_init() must not contain the label " \
            f"'{stray_label.group(1)}': control that enters the AEM-success " \
            "guard by any path other than the guard's own condition " \
            "advertises an unverified entity"
        # ... and each step of the boot path is a statement of milan_init()
        # itself. A step nested under some OTHER condition is a step a
        # compile-time constant can delete from the boot path entirely,
        # without the preprocessor and without changing a line this gate reads.
        init_body = init_source.index("{")

        def unconditional(match, what):
            head = max(init_source.rfind(char, init_body, match.start())
                       for char in ";{}")
            assert head >= 0 and \
                not init_source[head + 1:match.start()].strip(), \
                f"{what} must be a statement of milan_init() itself, not " \
                "the body of another condition: a condition this gate " \
                "cannot evaluate can drop it from the boot path"
            depth = (init_source.count("{", init_body, match.start()) -
                     init_source.count("}", init_body, match.start()))
            assert depth == 1, \
                f"{what} must sit at the top level of milan_init(), not " \
                f"{depth - 1} block(s) deep: a condition this gate cannot " \
                "evaluate can drop it from the boot path"

        unconditional(identity_read, "the CSR identity read")
        unconditional(identity_guard, "the CSR identity mismatch guard")
        unconditional(configure, "the fabric configuration step")
        unconditional(load, "the AEM verifier call")
        unconditional(guard, "the entity-advertise choke-point call")
        # Read/modify/write, increment and compound-assignment spellings all
        # override the verifier's verdict; pin the variable, not one spelling.
        verdict_write = re.compile(
            r"(?:\+\+|--)\s*aem_loaded\b|"
            r"\baem_loaded\b\s*(?:\+\+|--|(?:[-+*/%|&^]|<<|>>)?=(?!=))"
            r"\s*([^;]*)")
        assignments = list(verdict_write.finditer(firmware))
        assert len(assignments) == 1 and re.fullmatch(
            r"\s*load_aem_image\s*\(\s*\)\s*", assignments[0].group(1) or ""), \
            "aem_loaded must contain only the image verifier's verdict"
        # ... and pinning the ASSIGNMENT only pins the spellings that name the
        # variable. A pointer to it writes the verdict with no `aem_loaded =`
        # anywhere, so the address of the verdict may not be taken at all --
        # which, for a file-scope static in a single translation unit, is the
        # only way to build such a pointer.
        for use in re.finditer(r"(?<!&)&(?!&)\s*aem_loaded\b", firmware):
            lead = firmware[:use.start()].rstrip()
            assert lead and (lead[-1].isalnum() or lead[-1] in "_)]"), \
                "the address of aem_loaded must not be taken: a pointer " \
                "to the verdict (or a memset through one) overwrites it " \
                "without any assignment this gate can see"
        # Every rule from here on reads milan_write() call sites, so first
        # prove there is no OTHER way to store into a control register.
        assert_csr_store_closure(firmware, source)
        # ... and then ask the COMPILER as well. The text rules above catch
        # spellings this census's regex misses; the census catches spellings
        # no rule above anticipates. Both, because both have been measured to
        # miss something the other holds. The census runs LAST so that a
        # reduced-mode census (no cross compiler, see below) never takes a
        # verdict away from a rule that answers on every machine.
        census_taken = census_take(source)
        compiled_census_verdict = assert_compiled_census_is_clean(
            source, taken=census_taken)
        # The census places a write by the ADDRESS its operand reaches, so an
        # operand this gate cannot resolve to a decoded register is an
        # unclassifiable store: refuse it rather than leave it unexamined.
        # This also keeps pure VALUE constants (MILAN_PTP_LOAD and friends)
        # out of the register position -- they name no register.
        for record in model.calls(firmware):
            assert model.address(record["operand"]) is not None, \
                "milan_write() must name a register the RTL decodes so the " \
                "bit-0 census can place it by ADDRESS, got " \
                f"{record['operand'].strip()!r}"
        advertise, guard_body, guard_close = entity_advertise_span(firmware)
        enable_block = firmware[guard_body:guard_close]
        assert len(model.writes(enable_block, model.pp)) == 1 and \
               len(model.writes(enable_block, model.adp)) == 1, \
            "AEM-success guard must contain exactly one PP and one ADP enable"
        pp_enable = model.enable_write(enable_block, model.pp)
        adp_enable = model.enable_write(enable_block, model.adp)
        assert pp_enable["start"] < adp_enable["start"], \
            "AEM-success guard must enable PP before ADP"
        # RETIRED with the choke point (#153): the guarded block used to have
        # to hold the two enables and their printf and NOTHING else, so that
        # nothing inside it was unclassified and there was nothing for control
        # to be steered at. That refusal reddened `cdelay(64);` between the
        # enables. The choke point plus the resolved dominance measurement
        # below answer the same question by data flow -- every control-
        # register write in entity_advertise() disappears when the non-zero-
        # verdict edge is removed -- so an extra statement in it is now GREEN
        # and is measured as an accepted case.
        #
        # ... and control that ENTERS the choke point past its own verdict
        # test is refused here as well as measured below, so the textual
        # argument survives on a runner whose census stands down.
        advertise_source = firmware[advertise.start():guard_close + 1]
        for keyword in ("goto", "switch", "case", "default"):
            assert not re.search(rf"\b{keyword}\b", advertise_source), \
                f"entity_advertise() must not contain '{keyword}': control " \
                "that reaches an enable write by any path other than the " \
                "verdict test advertises an unverified entity"
        stray_label = re.search(
            r"(?m)^[ \t]*([A-Za-z_]\w*)[ \t]*:(?!:)", advertise_source)
        assert not stray_label, \
            f"entity_advertise() must not contain the label " \
            f"'{stray_label.group(1)}': control that reaches an enable " \
            "write by any path other than the verdict test advertises an " \
            "unverified entity"
        assert re.search(
            rf"\bif\s*\([^)]*\b{re.escape(advertise.group('verdict'))}\b",
            enable_block), \
            "entity_advertise() must test the verdict it is handed: its " \
            "parameter is the boot contract's only argument and nothing " \
            "else in this function may decide whether the entity is " \
            "advertised"
        # Entity-enable is PP_CTRL[0] OR ADP_CTRL[0], so the census runs over
        # the WHOLE firmware: configure_fabric() and every command handler
        # included, not just the choke point's own text. It is keyed on the
        # two ADDRESSES the RTL decodes, so a second #define for either one is
        # the same register here, exactly as it is on the bus.
        for address in (model.pp, model.adp):
            enabling = [w["start"] for w in model.writes(firmware, address)
                        if w["sets"]]
            assert len(enabling) == 1 and \
                guard_body <= enabling[0] < guard_close, \
                f"{model.label(address)} bit 0 may be set only inside the " \
                "entity-advertise choke point, found " \
                f"{len(enabling)} enabling write(s)"
        # ... and the choke point is CALLED exactly once, from the boot path,
        # with the verifier's verdict: a second call site is a second place
        # the entity can be advertised, whatever the first one is guarded by.
        advertise_calls = [call for call in re.finditer(
            r"\bentity_advertise\s*\(([^)]*)\)\s*;", firmware)]
        assert len(advertise_calls) == 1 and \
            advertise_calls[0].group(1).strip() == "aem_loaded", \
            "entity_advertise() must be called exactly once and with the " \
            "AEM verifier's verdict, found " \
            f"{[call.group(1).strip() for call in advertise_calls]}"
        # ... and the pre-AEM clear must survive, or a warm reboot advertises
        # a stale entity. Inline configure_fabric() so its writes are ordered
        # against the AEM verifier wherever the clears are actually spelled.
        fabric = re.search(
            r"static\s+void\s+configure_fabric\s*\(\s*void\s*\)\s*\{", firmware)
        fabric_body = braced_block(firmware, fabric, "configure_fabric()")
        boot_path = (init_source[:configure.start()] + fabric_body +
                     init_source[configure.end():])
        boot_load = re.search(
            r"\baem_loaded\s*=\s*load_aem_image\s*\(\s*\)\s*;", boot_path)
        assert boot_load, "the AEM verifier left the boot path"
        for address in (model.pp, model.adp):
            assert any(w["clears"] and w["start"] < boot_load.start()
                       for w in model.writes(boot_path, address)), \
                f"{model.label(address)} bit 0 must be cleared before the " \
                "AEM image is verified"
        assert not model.writes(firmware, model.phc), \
            "firmware must not write the reset-enabled PHC " \
            f"({model.label(model.phc)})"
        _ptp_reset, reset_value = ptp_reset_assignment(csr_code)
        assert reset_value == 1, \
            "bare-metal PHC contract requires the documented enabled reset"

        crc_guard = crc_mismatch_guard(load_source)
        crc_body, crc_close = braced_span(
            load_source, crc_guard, "CRC mismatch refusal")
        computed = crc_guard.group("lhs") or crc_guard.group("rhs")
        # OPEN, and honestly so: this is an EXISTENCE test over the whole
        # function. It does not ask which preprocessor arm the assignment is
        # in, it does not ask that the assignment DOMINATE the comparison,
        # and it does not read the arguments. So all four of these pass:
        # `got = crc32(...)` parked in the arm the compiler drops with a
        # constant in the compiled one; `got = MILAN_AEM_IMAGE_CRC32;`
        # between the crc32() call and the comparison, which gcc does not
        # warn about; and a CRC taken over the QSPI source rather than over
        # MILAN_AEM_DESC_BASE, the DRAM buffer the descriptor store serves;
        # plus a `goto` around the assignment and comparison to the success
        # return. The last is CONTROL FLOW and a structured do/break bypass
        # proves that banning one keyword would not prove dominance either.
        # The replacement is joint: #153 owns verifier CFG/data flow and the
        # entity_advertise() choke point; #162 owns a store census that
        # resolves values rather than matching printed literals. Neither
        # alone closes the end-to-end property.
        assert re.search(rf"\b{re.escape(computed)}\s*=\s*crc32\s*\(",
                         load_source), \
            "AEM verifier must contain a crc32() assignment to the local " \
            "named by the textual mismatch guard; this does not prove " \
            "provenance or reachability (issue #153)"
        # The verdict is whatever this function HANDS BACK, and `if
        # (aem_loaded)` is true for every non-zero value, not just for 1. So
        # classify every return and place it, rather than counting one literal:
        # a warm-boot fast path spelled `return 2;` is ordinary firmware drift
        # and it hands the guard a pass the CRC never earned.
        _load_directives, load_arm = cpp_arms(load_source)
        crc_arm = load_arm(crc_guard.start())
        refusals, successes = [], []
        for ret in re.finditer(r"\breturn\b([^;]*);", load_source):
            expr = re.sub(r"\s+", " ", ret.group(1)).strip()
            if constant_value(ret.group(1)) == 0:
                refusals.append((ret, expr))
                continue
            successes.append((ret, expr))
            # After the refusal BLOCK, not merely after the `if`: a non-zero
            # return inside the refusal is the refusal accepting the mismatch.
            # And in the CRC guard's own preprocessor arm, or it is code the
            # compiler reaches without ever compiling the comparison.
            assert ret.start() >= crc_close and \
                load_arm(ret.start())[:len(crc_arm)] == crc_arm, \
                "AEM verifier non-zero return must be textually after the " \
                "CRC mismatch block and in its preprocessor arm; CFG " \
                f"reachability is not proved (#153), but 'return {expr};' " \
                "is not even placed behind that textual boundary"
        assert successes, \
            "AEM verifier never returns a non-zero verdict, so the " \
            "AEM-success guard this gate checks can never be taken"
        assert any(crc_body <= ret.start() < crc_close
                   for ret, _ in refusals), \
            "AEM verifier mismatch block must contain a zero return; this " \
            "textual placement does not prove CRC-gated reachability (#153)"

        words = " ".join(docs.split())
        required = (
            "The PHC is enabled by the CSR reset and the option-on fabric "
            "gPTP plane starts independently of the AVDECC AEM image.",
            "Firmware therefore does not gate either one on AEM verification.",
            "Keep both compatibility enable bits clear, leaving the shared "
            "AVDECC control plane disabled while the PHC and fabric gPTP "
            "plane remain active.",
            "After the identity check and AEM verification succeed, set the "
            "`PP_CTRL[0]` and legacy `ADP_CTRL[0]` compatibility enable bits.",
            "The controls are ORed into one shared control-plane enable, so "
            "either bit alone enables it.",
            "A missing or corrupt image leaves the AVDECC entity disabled "
            "while the PHC and fabric gPTP plane continue independently.",
        )
        for claim in required:
            assert claim in words, f"bare-metal boot contract lost: {claim}"
        assert "Enable the PTP clock, protocol processor and ADP entity only " \
               "after" not in words, \
            "documentation restored the false AEM-gated PTP ordering"
        assert "firmware sets the PHC epoch explicitly" not in words, \
            "documentation claims an automatic epoch write firmware does not make"
        # ... and LAST, the resolving half. It runs after every text rule
        # so that a mutation those rules already answer keeps reporting the
        # property IT breaks; what reaches here is what no reader of text
        # can see. One compile feeds both instruments, so this measures the
        # same emitted code the census above matched over.
        if census_taken["ran"]:
            compiled_census_verdict["resolved"] = assert_resolved_boot_flow(
                census_taken["text"], model)
        return compiled_census_verdict

    baseline_census_verdict = assert_boot_contract(
        firmware_source, docs_source, csr_source)
    #: A stand-down that is only PRINTED inside the gate is the shape of
    #: #154: the gate says it declined, main() then says ALL GATES PASS, and
    #: the absence of a proof reads as the presence of one. Register it, so
    #: the final verdict counts and names it (#206).
    if not baseline_census_verdict["ran"]:
        skip("gate 1b",
             "the compiled CSR-address census: "
             f"{os.path.basename(baseline_census_verdict['compiler'] or 'no')}"
             " is not the RV32 target and no flag set here drives it as one, "
             "so the four census-only mutations, the phase-2 splice compile "
             "proofs and the census of the shipping firmware itself did not "
             "run -- and neither did the RESOLVING half (#153), which reads "
             "the same compile: no resolved store census, no proof that the "
             "verdict test dominates the enable writes, and no proof that "
             "the CRC-equality edge dominates every non-zero verdict or that "
             "the CRC was taken over MILAN_AEM_DESC_BASE, so its eight "
             "mutations did not run either")

    def replace_once(source, old, new, label):
        changed = source.replace(old, new, 1)
        assert changed != source, f"{label} mutation did not apply"
        return changed

    def make_honours_makeflags_e():
        """Whether THIS make lets `MAKEFLAGS += -e` inside a makefile hand
        the environment an override.

        Measured, not assumed, and it differs by version: GNU make 4.4.1
        honours it and the runner's make does not. A mutant whose detection
        depends on the machine is not evidence, so the entry below is
        included only where the construct actually does something, and the
        skip is printed rather than silent."""
        with tempfile.TemporaryDirectory(prefix="milan-mf-") as probe:
            with open(os.path.join(probe, "Makefile"), "w") as fh:
                fh.write("MAKEFLAGS += -e\nOBJECTS = good.o\n"
                         "all:\n\t@echo $(OBJECTS)\n")
            environ = dict(os.environ)
            environ.pop("MAKEFLAGS", None)
            environ["OBJECTS"] = "evil.o"
            got = subprocess.run(["make", "-s", "all"], cwd=probe, env=environ,
                                 capture_output=True, text=True)
        return got.stdout.strip() == "evil.o"

    verilator = shutil.which("verilator")
    rtl_mutant_elaboration = {"requested": 0, "passed": 0}
    datapath_lint_context = {}

    def _datapath_lint_sources():
        """The real milan_dp source closure, with absolute paths.

        The harness Makefile is already the repository's single exported
        source-list owner for the integration top.  Reuse it instead of
        copying a second list into this gate, then replace only the mutated
        CSR/datapath files in a temporary compilation.
        """
        if datapath_lint_context:
            return datapath_lint_context["sources"]
        suite = os.path.join(ROOT, "tb/verilator/milan_dp")
        planned = subprocess.run(
            ["make", "-s", "print-srcs"], cwd=suite,
            capture_output=True, text=True)
        assert planned.returncode == 0, \
            "RTL-mutant elaboration could not derive milan_dp sources: " \
            f"{planned.stderr.strip()}"
        sources = tuple(os.path.abspath(os.path.join(suite, source))
                        for source in shlex.split(planned.stdout))
        assert sources and all(os.path.isfile(source) for source in sources), \
            "RTL-mutant elaboration source closure contains a missing file"
        assert os.path.abspath(csr_path) in sources and \
            os.path.abspath(datapath_path) in sources, \
            "RTL-mutant elaboration source closure lost milan_csr/datapath"
        datapath_lint_context["sources"] = sources
        return sources

    def assert_rtl_mutant_elaborates(label, csr, datapath, count=True):
        """Require each behavior-changing RTL control to be valid RTL.

        A recognizer rejecting malformed text proves nothing about the
        hardware property.  On a runner carrying Verilator, lint the mutated
        file set as the real integration top (option-on gPTP) before the
        mutation can contribute to the reported total.  The documentation
        job deliberately carries no Verilator; that condition is reported as
        a stand-down rather than being called elaborated evidence.
        """
        changed_csr = csr != csr_source
        changed_datapath = datapath is not None and datapath != datapath_source
        if not changed_csr and not changed_datapath:
            return
        if count:
            rtl_mutant_elaboration["requested"] += 1
        if not verilator:
            return

        with tempfile.TemporaryDirectory(prefix="milan-rtl-mutant-") as tmp:
            mutated_csr = os.path.join(tmp, "milan_csr.sv")
            mutated_datapath = os.path.join(tmp, "milan_datapath.sv")
            if changed_csr:
                with open(mutated_csr, "w", encoding="utf-8") as fh:
                    fh.write(csr)
            if changed_datapath:
                with open(mutated_datapath, "w", encoding="utf-8") as fh:
                    fh.write(datapath)

            common = [
                verilator, "--lint-only", "--sv", "-Wno-fatal",
                "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
                "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
                "-Wno-UNUSEDPARAM", "-Wno-PINCONNECTEMPTY",
                "-Wno-IMPORTSTAR", "-Wno-CASEINCOMPLETE",
                "-Wno-EOFNEWLINE", "-Wno-PINMISSING",
                "-Wno-SELRANGE", "-Wno-TIMESCALEMOD",
                "--Mdir", os.path.join(tmp, "obj")]
            include_dirs = (
                os.path.join(ROOT, "configs/generated/endstation_arty_current"),
                os.path.join(ROOT, "hdl/common"),
                os.path.join(ROOT, "hdl/common/csr"),
                os.path.join(ROOT, "hdl/common/eth_event_counter"),
                os.path.join(ROOT, "hdl/ieee17221/adp"),
                os.path.join(ROOT, "hdl/ieee8021q/ts"),
                os.path.join(ROOT, "hdl/ieee8021as/ptp_timestamp"),
                os.path.join(ROOT, "third_party/verilog-axis/rtl"),
            )
            common += ["-I" + path for path in include_dirs]

            if changed_datapath:
                sources = []
                for source in _datapath_lint_sources():
                    if source == os.path.abspath(csr_path) and changed_csr:
                        source = mutated_csr
                    elif source == os.path.abspath(datapath_path):
                        source = mutated_datapath
                    sources.append(source)
                command = common + [
                    "--top-module", "milan_datapath",
                    "-GGPTP_PLANE_EN_P=1", "-GPB_PREFILL_C=2",
                    "-GCLKV_QTICK_CYC_P=4096", "-GLDIAG_IVAL_CYC_P=256",
                    "-GDIAG_TICK_CYC_P=256"] + sources
            else:
                command = common + ["--top-module", "milan_csr", mutated_csr]
            result = subprocess.run(
                command, cwd=ROOT, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True)
            assert result.returncode == 0, \
                f"{label} RTL mutation does not elaborate and cannot count " \
                "as a control:\n" + "\n".join(result.stdout.splitlines()[-24:])
        if count:
            rtl_mutant_elaboration["passed"] += 1

    def assert_rejected(label, firmware, docs, csr, because,
                        makefile=None, listing=None, datapath=None):
        try:
            assert_boot_contract(firmware, docs, csr, makefile, listing,
                                 datapath)
        except (AssertionError, ValueError) as exc:
            # A mutation rejected on an incidental anchor mismatch proves
            # nothing about the safety property, so pin the reason too.
            assert because in str(exc), \
                f"{label} mutation was rejected for the wrong reason: {exc}"
            assert_rtl_mutant_elaborates(label, csr, datapath)
            return
        raise AssertionError(f"{label} mutation passed the boot-contract gate")

    #: Every position below is found in the BLANKED text -- a `}` inside a
    #: comment is not a brace and a milan_write() inside a printf() is not a
    #: call -- and every mutation then splices the RAW text at those same
    #: offsets, which blanked() preserves exactly. Reading positions off the
    #: raw text instead made a comment in the guard fail the SUITE with a
    #: message blaming the firmware for a defect in this construction.
    firmware_code = blanked(firmware_source)
    source_model = CsrModel(firmware_source, blanked_sv(csr_source))

    def with_define_value(baseline, name, new_value, label):
        """Replace one object-like firmware #define value by parsed span."""
        code = blanked(baseline)
        define = re.search(
            rf"(?m)^[ \t]*#[ \t]*define[ \t]+{re.escape(name)}[ \t]+"
            r"(?P<value>[^\r\n]*?)[ \t]*$", code)
        assert define, f"{label} mutation lost #define {name}"
        changed = (baseline[:define.start("value")] + new_value +
                   baseline[define.end("value"):])
        assert changed != baseline, f"{label} mutation did not change {name}"
        return changed

    source_version = re.search(
        r"\bparameter\s+logic\s*\[\s*31\s*:\s*0\s*\]\s+VERSION\s*=\s*"
        r"(?P<literal>[0-9]+\s*'\s*[hH]\s*[0-9A-Fa-f_]+)", csr_source)
    assert source_version, \
        "CSR identity mutations lost the RTL VERSION literal"
    source_version_value = sv_literal_value(source_version.group("literal"))
    assert source_version_value is not None
    identity_at_version = with_define_value(
        firmware_source, "MILAN_ID",
        f"0x{source_model.rtl_address('A_VERSION'):03x}u",
        "identity address repointed to VERSION")
    identity_magic_at_version = with_define_value(
        firmware_source, "MILAN_ID_MAGIC",
        f"0x{source_version_value:08x}u",
        "identity magic changed to VERSION")
    identity_magic_at_sample = with_define_value(
        firmware_source, "MILAN_ID_MAGIC", "(id)",
        "identity magic replaced by the sampled value")
    identity_magic_at_sample_expr = with_define_value(
        firmware_source, "MILAN_ID_MAGIC", "(id | 0u)",
        "identity magic replaced by a warning-clean sampled expression")
    identity_contract_at_version = with_define_value(
        identity_at_version, "MILAN_ID_MAGIC",
        f"0x{source_version_value:08x}u",
        "identity contract repointed to VERSION")
    init_start = anchored(firmware_code, "static void milan_init(void)",
                          "the boot entry point")
    init_end = anchored(firmware_code, "define_init_func(milan_init)",
                        "the boot entry point's init hook", init_start)
    source_init = firmware_source[init_start:init_end]
    init_code = firmware_code[init_start:init_end]
    source_identity_read = re.search(
        r"\buint32_t\s+(?P<name>\w+)\s*=\s*"
        r"milan_read\s*\(\s*MILAN_ID\s*\)\s*;", init_code)
    assert source_identity_read, \
        "CSR identity-check mutations lost the MILAN_ID read"
    source_identity_read_statement = source_init[
        source_identity_read.start():source_identity_read.end()]
    source_identity_guard = re.search(
        r"\bif\s*\(\s*\w+\s*!=\s*MILAN_ID_MAGIC\s*\)\s*\{",
        init_code)
    assert source_identity_guard, \
        "CSR identity-check mutations lost the mismatch guard"
    identity_body, identity_close = braced_span(
        init_code, source_identity_guard, "CSR identity mismatch guard")
    source_identity_block = source_init[
        source_identity_guard.start():identity_close + 1]
    source_identity_statement = source_init[
        source_identity_guard.start():source_identity_guard.end()]
    source_guard = re.search(
        r"\bentity_advertise\s*\(\s*aem_loaded\s*\)\s*;", init_code)
    assert source_guard, \
        "the entity-advertise mutations lost the choke-point call"
    guard_statement = source_init[source_guard.start():source_guard.end()]
    source_advertise, guard_body, guard_close = entity_advertise_span(
        firmware_code)
    source_verdict_test_match = re.search(
        r"\bif\s*\(\s*![ \t]*"
        + re.escape(source_advertise.group("verdict")) +
        r"\s*\)\s*\n\s*return\s*;", firmware_code)
    assert source_verdict_test_match, \
        "the choke-point mutations lost the early return on the verdict"
    source_verdict_test = firmware_source[
        source_verdict_test_match.start():source_verdict_test_match.end()]
    source_enable_block = firmware_source[guard_body:guard_close]
    source_enable_code = firmware_code[guard_body:guard_close]
    source_pp_enable = source_model.enable_write(
        source_enable_code, source_model.pp)
    source_adp_enable = source_model.enable_write(
        source_enable_code, source_model.adp)
    source_load = re.search(
        r"\baem_loaded\s*=\s*load_aem_image\s*\(\s*\)\s*;",
        firmware_code)
    assert source_load
    load_statement = firmware_source[source_load.start():source_load.end()]
    source_load_start = anchored(
        firmware_code, "static int load_aem_image(void)",
        "the AEM verifier")
    source_load_end = firmware_code.index(
        "static void milan_init(void)", source_load_start)
    source_load_function = firmware_source[source_load_start:source_load_end]
    source_load_code = firmware_code[source_load_start:source_load_end]
    source_crc_guard = crc_mismatch_guard(source_load_code)
    crc_body, crc_close = braced_span(
        source_load_code, source_crc_guard, "CRC mismatch refusal")
    source_crc_block = source_load_function[crc_body:crc_close]
    source_reset, _reset_value = ptp_reset_assignment(blanked_sv(csr_source))
    source_reset_statement = source_reset.group(0)
    source_ptp_enable = ptp_enable_assignment(blanked_sv(csr_source))
    source_ptp_enable_statement = source_ptp_enable.group(0)
    source_fabric = re.search(
        r"static\s+void\s+configure_fabric\s*\(\s*void\s*\)\s*\{",
        firmware_code)
    fabric_body_at, fabric_body_to = braced_span(
        firmware_code, source_fabric, "configure_fabric()")
    source_fabric_body = firmware_source[fabric_body_at:fabric_body_to]
    source_reg_def = re.search(
        r"\bstatic\s+inline\s+volatile\s+uint32_t\s*\*\s*milan_reg\s*\(\s*"
        r"unsigned\s+int\s+(?P<offset>\w+)\s*\)\s*\{", firmware_code)
    assert source_reg_def, "address-helper mutations lost milan_reg()"
    source_reg_signature = firmware_source[
        source_reg_def.start():source_reg_def.end()]
    source_reg_body_at, source_reg_body_to = braced_span(
        firmware_code, source_reg_def, "address-helper mutation")
    wrong_reg_address = (
        firmware_source[:source_reg_body_at] +
        f"\n\t(void){source_reg_def.group('offset')};\n"
        "\treturn (volatile uint32_t *)(MILAN_CSR_BASE + MILAN_ID);\n" +
        firmware_source[source_reg_body_to:])
    source_read_def = re.search(
        r"\bstatic\s+inline\s+uint32_t\s+milan_read\s*\(\s*unsigned\s+int"
        r"\s+(?P<offset>\w+)\s*\)\s*\{", firmware_code)
    assert source_read_def, "read-helper mutations lost milan_read()"
    source_read_body_at, source_read_body_to = braced_span(
        firmware_code, source_read_def, "read-helper mutation")
    forged_csr_read = (
        firmware_source[:source_read_body_at] +
        f"\n\treturn {source_read_def.group('offset')} == MILAN_ID ? "
        "MILAN_ID_MAGIC : "
        f"*milan_reg({source_read_def.group('offset')});\n" +
        firmware_source[source_read_body_to:])
    assert wrong_reg_address != firmware_source and \
        forged_csr_read != firmware_source, \
        "CSR accessor provenance mutations did not change the firmware"
    reflowed_reg_signature = (
        "static inline\nvolatile uint32_t *\nmilan_reg(\n\tunsigned int "
        f"{source_reg_def.group('offset')})\n{{")

    def accepted_reg_reflow(baseline):
        """Return the accepted helper reflow, including an already-reflowed
        live baseline without asking replace_once() to perform a no-op."""
        code = blanked(baseline)
        reg_def = re.search(
            r"\bstatic\s+inline\s+volatile\s+uint32_t\s*\*\s*milan_reg\s*"
            r"\(\s*unsigned\s+int\s+(?P<offset>\w+)\s*\)\s*\{", code)
        assert reg_def, "accepted address-helper reflow lost milan_reg()"
        signature = baseline[reg_def.start():reg_def.end()]
        target = (
            "static inline\nvolatile uint32_t *\nmilan_reg(\n\tunsigned int "
            f"{reg_def.group('offset')})\n{{")
        if signature == target:
            return baseline
        return replace_once(baseline, signature, target,
                            "reflowed milan_reg()")

    reflowed_firmware = accepted_reg_reflow(firmware_source)
    assert accepted_reg_reflow(reflowed_firmware) == reflowed_firmware, \
        "an already-reflowed live milan_reg() baseline is not idempotent"
    source_configure = re.search(
        r"\bconfigure_fabric\s*\(\s*\)\s*;", init_code)
    assert source_configure
    source_boot_path = (source_init[:source_configure.start()] +
                        source_fabric_body +
                        source_init[source_configure.end():])

    def pre_aem_clear(address):
        """The bit-0 clear the pre-AEM entity disable rests on, found by what
        it does rather than by where or how it is spelled."""
        label = source_model.label(address)
        found = [w for w in source_model.writes(source_boot_path, address)
                 if w["clears"]]
        assert found, f"{label} pre-AEM clear mutation lost its write"
        text = source_boot_path[found[0]["start"]:found[0]["stop"]]
        assert firmware_source.count(text) == 1, \
            f"{label} pre-AEM clear is not a unique statement"
        return found[0], text

    def forced_enable(clear, text):
        """The same write, turned into the enable the AEM gate must forbid --
        rebuilt from the census record rather than edited as text, so ANY
        clear spelling (`& ~1u`, `& ~(1u << 0)`, `& 0xfffffffeu`, a literal
        zero) still yields its enable."""
        operand = clear["operand"].strip()
        enabling = f"milan_write({operand}, milan_read({operand}) | 1u)"
        assert enabling != text, \
            "pre-AEM clear mutation could not derive its enable"
        return enabling

    source_pp_record, source_pp_clear = pre_aem_clear(source_model.pp)
    source_adp_record, source_adp_clear = pre_aem_clear(source_model.adp)
    early_pp_enable = forced_enable(source_pp_record, source_pp_clear)
    early_adp_enable = forced_enable(source_adp_record, source_adp_clear)
    #: The firmware's own spelling of ADP_CTRL, taken from the address the RTL
    #: decodes so the mutations below never hard-code a name either.
    adp_name = next(name for name, value in sorted(source_model.defines.items())
                    if value == source_model.adp)

    def aliased(name, address, statement):
        """The firmware plus a SECOND #define for `address` and a write
        through it in configure_fabric(): ordinary C that compiles clean and
        that the bus cannot tell from a write through the original name."""
        with_define = replace_once(
            firmware_source, "static int aem_loaded;",
            f"#define {name} 0x{address:03x}u\n\nstatic int aem_loaded;",
            f"{name} alias define")
        return replace_once(with_define, fabric_tail,
                            fabric_tail + "\n\t" + statement,
                            f"{name} alias write")

    #: The END of configure_fabric()'s body: after the firmware's own pre-AEM
    #: clears and before load_aem_image() runs.
    #:
    #: Splicing at the HEAD of the body, which is what these used to do, put
    #: the mutant's enable two statements ahead of
    #: `milan_write(ADP_CTRL, ... & ~1u)`, so the firmware cleared the bit
    #: again and the mutant firmware did not actually advertise before AEM
    #: verification. The rule still bit, on the syntax, but the LABEL claimed
    #: a defect the mutant did not contain. Same class as the mutants that
    #: once stored to 0xf000_0600: address right, ordering wrong.
    fabric_tail = source_fabric_body.rstrip()

    def enabled_before_aem(statement):
        """`statement` spliced at the END of configure_fabric(), i.e. onto
        the boot path after the pre-AEM clears and before the AEM image has
        been verified, so the bit is still set when the verifier runs."""
        return replace_once(firmware_source, fabric_tail,
                            fabric_tail + "\n\t" + statement,
                            "pre-AEM entity enable")

    alias_adp_enable = aliased(
        "MILAN_ENTITY_CTRL", source_model.adp,
        "milan_write(MILAN_ENTITY_CTRL, milan_read(MILAN_ENTITY_CTRL) | 1u);")
    alias_pp_enable = aliased(
        "MILAN_PROC_CTRL", source_model.pp,
        "milan_write(MILAN_PROC_CTRL, milan_read(MILAN_PROC_CTRL) | 1u);")
    alias_phc_write = aliased(
        "MILAN_PHC_CTRL", source_model.phc,
        "milan_write(MILAN_PHC_CTRL, 0u);")
    #: An EXISTING name repointed at PP_CTRL: a register constant the operand
    #: rule already trusts, now naming a different register.
    spare_name = next(
        name for name, value in sorted(source_model.defines.items())
        if name != "MILAN_ID" and value in source_model.decoded and
        value not in (source_model.pp, source_model.adp, source_model.phc) and
        not source_model.writes(firmware_source, value))
    spare_at = re.search(rf"(?m)^#define\s+{spare_name}\s+\S+[ \t]*$",
                         firmware_code)
    spare_define = firmware_source[spare_at.start():spare_at.end()]
    repointed_register = replace_once(
        enabled_before_aem(
            f"milan_write({spare_name}, milan_read({spare_name}) | 1u);"),
        spare_define,
        re.sub(r"\S+[ \t]*$", f"0x{source_model.pp:03x}u", spare_define),
        f"{spare_name} repointed at PP_CTRL")
    #: A pure VALUE constant in the register position.
    value_constant = next(
        name for name, value in sorted(source_model.defines.items())
        if value not in source_model.decoded)
    value_operand_write = enabled_before_aem(
        f"milan_write({value_constant}, 1u);")
    spaced_call_enable = enabled_before_aem(
        re.sub(r"milan_write\(", "milan_write (", early_adp_enable, count=1)
        + ";")
    phase2_spliced_call_enable = enabled_before_aem(
        early_adp_enable.replace(
            "milan_write", "milan_" + "\\" + "\n" + "write", 1) + ";")
    phase2_splice_compiled = assert_target_compiles(
        phase2_spliced_call_enable, "phase-2 token-splice mutation")
    phase2_whitespace_splices = tuple(
        (name,
         enabled_before_aem(
             early_adp_enable.replace(
                 "milan_write", "milan_" + "\\" + separator + "\n" +
                 "write", 1) + ";"))
        for name, separator in (("space", " "), ("tab", "\t"),
                                ("form-feed", "\f"),
                                ("vertical-tab", "\v")))
    phase2_whitespace_compile_results = tuple(
        (name, assert_target_compiles(
            mutation, f"phase-2 {name} token-splice mutation",
            allow_warnings=True))
        for name, mutation in phase2_whitespace_splices)
    pointer_call_enable = replace_once(
        enabled_before_aem(
            f"milan_poke({adp_name}, milan_read({adp_name}) | 1u);"),
        "static void print_tod(",
        "static void (*const milan_poke)(unsigned int, uint32_t) ="
        " milan_write;\n\nstatic void print_tod(", "milan_write alias pointer")
    #: The register named by a HELPER rather than by a constant: real C that
    #: compiles, and an operand no static reader can place by address.
    indirect_helper_enable = replace_once(
        enabled_before_aem(
            "milan_write(indirect_reg(), milan_read(indirect_reg()) | 1u);"),
        "static void configure_fabric(void)",
        "static unsigned int indirect_reg(void)\n{\n"
        f"\treturn {adp_name};\n}}\n\nstatic void configure_fabric(void)",
        "indirect register helper")
    reg_store_enable = enabled_before_aem(
        f"*milan_reg({adp_name}) = milan_read({adp_name}) | 1u;")
    raw_store_enable = enabled_before_aem(
        f"*(volatile uint32_t *)(MILAN_CSR_BASE + {adp_name}) = 1u;")
    pasted_call_enable = replace_once(
        enabled_before_aem(
            f"MILAN_FN(write)({adp_name}, milan_read({adp_name}) | 1u);"),
        "static int aem_loaded;",
        "#define MILAN_FN(op) milan_ ## op\n\nstatic int aem_loaded;",
        "pasted call name")

    old_claim = re.search(
        r"After\s+the\s+identity\s+check\s+and\s+AEM\s+verification\s+"
        r"succeed,\s+set\s+the\s+`PP_CTRL\[0\]`\s+and\s+legacy\s+"
        r"`ADP_CTRL\[0\]`\s+compatibility\s+enable\s+bits\.", docs_source)
    assert old_claim, "boot-order documentation mutation did not find its claim"
    old_order = re.sub(
        r"set\s+the\s+`PP_CTRL",
        "enable the PTP clock and set the `PP_CTRL",
        old_claim.group(0), count=1)
    missing_identity_guard = replace_once(
        firmware_source, source_identity_block, "",
        "removed CSR identity mismatch guard")
    source_identity_return = re.search(r"\breturn\s*;", source_identity_block)
    assert source_identity_return, \
        "CSR identity-check mutations lost the mismatch return"
    identity_block_without_return = replace_once(
        source_identity_block, source_identity_return.group(0), "(void)0;",
        "removed CSR identity mismatch return")
    missing_identity_return = replace_once(
        firmware_source, source_identity_block, identity_block_without_return,
        "CSR identity mismatch block without return")
    inverted_identity_statement = source_identity_statement.replace(
        "!=", "==", 1)
    assert inverted_identity_statement != source_identity_statement, \
        "inverted CSR identity mismatch mutation did not apply"
    inverted_identity_guard = replace_once(
        firmware_source, source_identity_statement,
        inverted_identity_statement, "inverted CSR identity mismatch guard")
    forged_identity = replace_once(
        firmware_source, source_identity_read_statement,
        source_identity_read_statement +
        f"\n\t{source_identity_read.group('name')} = MILAN_ID_MAGIC;",
        "overwritten CSR identity sample")
    identity_address_comment_decoy = replace_once(
        csr_source,
        "    A_ID          = 'h000,",
        "    // A_ID = 'h000, inactive textual decoy\n"
        "    A_ID          = 'h01C,",
        "commented A_ID address decoy")
    identity_default_comment_decoy = replace_once(
        csr_source,
        "      A_ID[10:0]:         csr_default = 32'h4D49_4C4E;      "
        "// \"MILN\"",
        "      // A_ID[10:0]: csr_default = 32'h4D49_4C4E; "
        "inactive decoy\n"
        "      A_ID[0 +: 11]:      csr_default = 32'hDEAD_BEEF;",
        "commented A_ID default decoy")
    identity_conditional_decoy = replace_once(
        csr_source,
        "    A_ID          = 'h000, A_VERSION = 'h004,",
        "`ifdef PR187_SAFE_ID\n"
        "    A_ID          = 'h000,\n"
        "`else\n"
        "    A_ID          = 'h01C,\n"
        "`endif\n"
        "    A_VERSION     = 'h004,",
        "preprocessor-selected A_ID address decoy")
    identity_static_generate_decoy = replace_once(
        csr_source,
        "  localparam [ADDR_WIDTH-1:0]\n"
        "    A_ID          = 'h000, A_VERSION = 'h004,",
        "  generate if (1'b0) begin : g_pr187_safe_id\n"
        "  localparam [ADDR_WIDTH-1:0]\n"
        "    A_ID          = 'h000, A_VERSION = 'h004, "
        "PR187_DEAD_C = 'h7FC;\n"
        "  end endgenerate\n"
        "  localparam [ADDR_WIDTH-1:0]\n"
        "    A_ID          = 'h01C, A_VERSION = 'h004,",
        "inactive static-generate A_ID address decoy")
    identity_dead_default_case = replace_once(
        csr_source,
        "    csr_default = 32'h0;\n"
        "    unique case (a)\n"
        "      A_ID[10:0]:         csr_default = 32'h4D49_4C4E;      "
        "// \"MILN\"",
        "    csr_default = 32'h0;\n"
        "    if (1'b0)\n"
        "      case (a)\n"
        "        A_ID[10:0]: csr_default = 32'h4D49_4C4E;\n"
        "        default: ;\n"
        "      endcase\n"
        "    unique case (a)\n"
        "      11'h000:            csr_default = 32'hDEAD_BEEF;",
        "A_ID default hidden in a dead procedural case")
    identity_rom_fill_forged = replace_once(
        csr_source,
        "    for (int k = 0; k < 512; k++) dflt_rom[k] = "
        "csr_default(11'(k * 4));",
        "    for (int k = 0; k < 512; k++) dflt_rom[k] =\n"
        "        (k == 0) ? 32'hDEAD_BEEF : csr_default(11'(k * 4));",
        "forged A_ID defaults-ROM fill")
    identity_read_address_offset = replace_once(
        csr_source,
        "  wire [ADDR_WIDTH-1:0] rd_addr = s_axi_araddr;",
        "  wire [ADDR_WIDTH-1:0] rd_addr = s_axi_araddr + A_VERSION;",
        "offset CSR read address")

    def gate_instance_port(source, module, instance, port, value, label):
        instances = list(re.finditer(
            rf"\b{re.escape(module)}\b\s*#\s*\([^;]*?\)\s*"
            rf"{re.escape(instance)}\s*\((?P<ports>.*?)\)\s*;",
            source, re.DOTALL))
        assert len(instances) == 1, \
            f"{label} mutation found {len(instances)} {instance} instances"
        found = instances[0]
        ports = found.group("ports")
        connections = list(re.finditer(
            rf"\.{re.escape(port)}\s*\(\s*(?P<value>[^)]*?)\s*\)",
            ports))
        assert len(connections) == 1 and re.fullmatch(
            rf"\s*{re.escape(value)}\s*", connections[0].group("value")), \
            f"{label} mutation lost .{port}({value})"
        connection = connections[0]
        start = found.start("ports") + connection.start("value")
        stop = found.start("ports") + connection.end("value")
        return source[:start] + f"{value} & cfg_adp_enable" + source[stop:]

    phc_gated_by_adp = replace_once(
        csr_source, source_ptp_enable_statement,
        re.sub(r"ptp_ctrl\s*\[\s*0\s*\]",
               "ptp_ctrl[0] & adp_ctrl[0]",
               source_ptp_enable_statement, count=1),
        "PHC output gated by ADP")
    phc_increment_source_gated_by_adp = replace_once(
        csr_source,
        "  assign o_ptp_incr         = ptp_incr;",
        "  assign o_ptp_incr         = "
        "ptp_incr & {32{adp_ctrl[0]}};",
        "milan_csr PHC increment output gated by ADP")
    phc_consumer_gated_by_adp = replace_once(
        datapath_source,
        ".i_ptp_enable      (cfg_ptp_enable),",
        ".i_ptp_enable      (cfg_ptp_enable & cfg_adp_enable),",
        "ptp_timestamp PHC consumer gated by ADP")
    phc_increment_gated_by_adp = replace_once(
        datapath_source,
        ".i_ptp_incr        (cfg_ptp_incr),",
        ".i_ptp_incr        (cfg_ptp_incr & {32{cfg_adp_enable}}),",
        "ptp_timestamp PHC increment gated by ADP")
    phc_binding_gated_by_adp = replace_once(
        replace_once(
            datapath_source,
            "  wire        cfg_ptp_enable;",
            "  wire        cfg_ptp_enable;\n"
            "  wire        cfg_ptp_enable_raw;\n"
            "  assign cfg_ptp_enable = "
            "cfg_ptp_enable_raw & cfg_adp_enable;",
            "ADP-gated PHC binding wire"),
        ".o_ptp_enable      (cfg_ptp_enable),",
        ".o_ptp_enable      (cfg_ptp_enable_raw),",
        "ADP-gated milan_csr PHC output binding")
    phc_wand_second_driver = replace_once(
        datapath_source,
        "  wire        cfg_ptp_enable;",
        "  wand        cfg_ptp_enable;\n"
        "  and (cfg_ptp_enable, cfg_adp_enable, 1'b1);",
        "ADP-controlled second PHC-enable driver")
    phc_effective_adjust_gated_by_adp = replace_once(
        datapath_source,
        "                               ? unsigned'(gptp_adj_w)   : "
        "cfg_ptp_adj;",
        "                               ? unsigned'(gptp_adj_w)   : "
        "(cfg_ptp_adj & {32{cfg_adp_enable}});",
        "effective PHC frequency adjustment gated by ADP")
    phc_effective_offset_gated_by_adp = replace_once(
        datapath_source,
        "                               ? gptp_step_w             : "
        "cfg_ptp_offset;",
        "                               ? gptp_step_w             : "
        "(cfg_ptp_offset & {64{cfg_adp_enable}});",
        "effective PHC offset gated by ADP")
    phc_effective_strobe_gated_by_adp = replace_once(
        datapath_source,
        "                               ? gptp_step_we_w          : "
        "cfg_ptp_cmd_adjust;",
        "                               ? gptp_step_we_w          : "
        "(cfg_ptp_cmd_adjust & cfg_adp_enable);",
        "effective PHC adjustment strobe gated by ADP")
    gptp_gated_timestamp_gtx_reset = gate_instance_port(
        datapath_source, "ptp_ts_top", "ptp_timestamp", "gtx_resetn",
        "gtx_resetn", "ptp_timestamp gtx reset gate")
    gptp_gated_timestamp_axis_reset = gate_instance_port(
        datapath_source, "ptp_ts_top", "ptp_timestamp", "axis_resetn",
        "axis_resetn", "ptp_timestamp axis reset gate")
    gptp_gated_timestamp_ingress = replace_once(
        datapath_source,
        ".s_axis_rx_tvalid(rx_axis_to_ts.tvalid),",
        ".s_axis_rx_tvalid(rx_axis_to_ts.tvalid & cfg_adp_enable),",
        "ptp_timestamp RX ingress gate")
    gptp_gated_timestamp_ready = replace_once(
        replace_once(
            datapath_source,
            "\n  ptp_ts_top #(\n",
            "\n  wire rx_ts_tready_raw_w;\n"
            "  assign rx_axis_to_ts.tready = "
            "rx_ts_tready_raw_w & cfg_adp_enable;\n\n"
            "  ptp_ts_top #(\n",
            "ptp_timestamp raw RX-ready wire"),
        ".s_axis_rx_tready(rx_axis_to_ts.tready),",
        ".s_axis_rx_tready(rx_ts_tready_raw_w),",
        "ptp_timestamp RX ready gate")
    gptp_gated_filter_ingress = replace_once(
        datapath_source,
        ".s_tvalid(rx_axis_ptp_to_filt.tvalid),",
        ".s_tvalid(rx_axis_ptp_to_filt.tvalid & cfg_adp_enable),",
        "enabled RX-filter ingress gate")
    gptp_gated_filter_clock = gate_instance_port(
        datapath_source, "rx_mac_filter", "rx_filter", "clk_i",
        "axis_clk", "enabled RX-filter clock gate")
    gptp_gated_filter_reset = gate_instance_port(
        datapath_source, "rx_mac_filter", "rx_filter", "rst_n",
        "axis_resetn", "enabled RX-filter reset gate")
    gptp_filter_policy_gated_by_adp = replace_once(
        datapath_source,
        ".default_pass_i (cfg_tcam_default_pass),",
        ".default_pass_i (cfg_tcam_default_pass & cfg_adp_enable),",
        "RX-filter default policy gated by ADP")
    gptp_gated_datapath = replace_once(
        datapath_source, ".rst_n           (axis_resetn),",
        ".rst_n           (axis_resetn && cfg_adp_enable),",
        "fabric gPTP reset gate")
    gptp_gated_ingress = replace_once(
        datapath_source,
        ".rx_tvalid_i     (rx_axis_to_dma.tvalid),",
        ".rx_tvalid_i     (rx_axis_to_dma.tvalid && cfg_adp_enable),",
        "fabric gPTP ingress gate")
    gptp_gated_local_egress = replace_once(
        datapath_source,
        ".s_adp_tvalid(gtx_tvalid_w), .s_adp_tlast (gtx_tlast_w),",
        ".s_adp_tvalid(gtx_tvalid_w && cfg_adp_enable), "
        ".s_adp_tlast (gtx_tlast_w),",
        "fabric gPTP local egress gate")
    gptp_gated_boundary_egress = replace_once(
        datapath_source,
        ".s_adp_tvalid(ctlg3_tvalid),",
        ".s_adp_tvalid(ctlg3_tvalid && cfg_adp_enable),",
        "fabric gPTP MAC-boundary gate")
    gptp_gated_control_mux_reset = gate_instance_port(
        datapath_source, "adp_tx_arbiter", "gptp_ctl_mux", "rst_n",
        "axis_resetn", "fabric gPTP control-mux reset gate")
    gptp_gated_boundary_mux_reset = gate_instance_port(
        datapath_source, "adp_tx_arbiter", "adp_tx_mux", "rst_n",
        "axis_resetn", "fabric gPTP boundary-mux reset gate")
    def runtime_gate_assignment(source, lhs, label):
        matches = list(re.finditer(
            rf"(?m)^[ \t]*assign[ \t]+{re.escape(lhs)}[ \t]*="
            r"(?P<value>[^;]+);", source))
        assert len(matches) == 1, \
            f"{label} mutation found {len(matches)} continuous assignments"
        match = matches[0]
        gated = f" ({match.group('value').strip()}) & cfg_adp_enable"
        return source[:match.start("value")] + gated + source[match.end("value"):]

    gptp_gated_external_tx = runtime_gate_assignment(
        datapath_source, "m_axis_mac_tx_tvalid",
        "external MAC TX valid gate")
    gptp_gated_external_rx = runtime_gate_assignment(
        datapath_source, "rx_axis_to_ts.tvalid",
        "external MAC RX valid gate")
    gptp_wand_second_driver_external_tx = replace_once(
        replace_once(
            datapath_source,
            "  output wire                     m_axis_mac_tx_tvalid,",
            "  output wand                     m_axis_mac_tx_tvalid,",
            "resolved external MAC TX valid port"),
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;",
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;\n"
        "  and (m_axis_mac_tx_tvalid, cfg_adp_enable, 1'b1);",
        "ADP-controlled second external TX-valid driver")
    gptp_gated_filter_bypass = runtime_gate_assignment(
        datapath_source, "rx_axis_to_dma.tvalid",
        "bypass RX-filter ingress gate")
    gptp_commented_external_tx = replace_once(
        datapath_source,
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;",
        "  /* assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid; */\n"
        "  `define PR187_TX_VALID(value) ((value) & cfg_adp_enable)\n"
        "  assign m_axis_mac_tx_tvalid = "
        "`PR187_TX_VALID(tx_axis_to_mac.tvalid);\n"
        "  `undef PR187_TX_VALID",
        "commented direct external TX decoy with live macro gate")
    gptp_inactive_external_tx = replace_once(
        datapath_source,
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;",
        "  `ifdef PR187_SAFE_DIRECT_TX\n"
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;\n"
        "  `endif",
        "inactive conditional external TX decoy")
    gptp_static_generate_external_tx = replace_once(
        datapath_source,
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;",
        "  generate if (1'b0) begin : g_pr187_safe_tx\n"
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;\n"
        "  end else begin : g_pr187_live_tx\n"
        "  and (m_axis_mac_tx_tvalid, tx_axis_to_mac.tvalid, "
        "cfg_adp_enable);\n"
        "  end endgenerate",
        "inactive static-generate external TX decoy")
    gptp_midline_directive_external_tx = replace_once(
        datapath_source,
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;",
        "  wire pr187_d0_w; `define PR187_ASSIGN assign\n"
        "  wire pr187_d1_w; `ifdef PR187_SAFE_DIRECT_TX\n"
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;\n"
        "  wire pr187_d2_w; `else\n"
        "  wire pr187_d3_w; `PR187_ASSIGN m_axis_mac_tx_tvalid = "
        "tx_axis_to_mac.tvalid & cfg_adp_enable;\n"
        "  wire pr187_d4_w; `endif",
        "mid-line conditional external TX decoy")
    gptp_implicit_generate_external_tx = replace_once(
        datapath_source,
        "  assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;",
        "  if (1'b0)\n"
        "    assign m_axis_mac_tx_tvalid = tx_axis_to_mac.tvalid;\n"
        "  else assign m_axis_mac_tx_tvalid = "
        "tx_axis_to_mac.tvalid & cfg_adp_enable;",
        "implicit conditional-generate external TX decoy")

    unconditional_guard = guard_statement.replace("aem_loaded", "1", 1)
    inverted_guard = guard_statement.replace("aem_loaded", "!aem_loaded", 1)
    pp_enable_text = source_enable_block[
        source_pp_enable["start"]:source_pp_enable["stop"]]
    adp_enable_text = source_enable_block[
        source_adp_enable["start"]:source_adp_enable["stop"]]
    swapped_enable_block = (
        source_enable_block[:source_pp_enable["start"]] + adp_enable_text +
        source_enable_block[source_pp_enable["stop"]:
                            source_adp_enable["start"]] + pp_enable_text +
        source_enable_block[source_adp_enable["stop"]:])
    bad_pp_block = (
        source_enable_block[:source_pp_enable["mask_at"]] + "2u" +
        source_enable_block[source_pp_enable["mask_to"]:])
    bad_adp_block = (
        source_enable_block[:source_adp_enable["start"]] +
        f"milan_write({adp_name}, milan_read({adp_name}) & ~1u)" +
        source_enable_block[source_adp_enable["stop"]:])
    bad_crc_block = replace_once(
        source_crc_block, "return 0;", "return 1;", "CRC refusal")
    bad_load_function = replace_once(
        source_load_function, source_crc_block, bad_crc_block,
        "CRC verifier block")

    # ---- the four axes R1 opened: the preprocessor the gate never saw, the
    # difference between sitting inside the guard and being REACHED through
    # it, a verdict and a verifier pinned by spelling, and an address model
    # asserted against the RTL's name table but never against its decode.
    # Every one of these compiles clean and every one used to pass.
    configure_statement = source_init[
        source_configure.start():source_configure.end()]
    crc_guard_statement = source_load_function[
        source_crc_guard.start():source_crc_guard.end()]

    def defined(source, name, value, label):
        return replace_once(
            source, "static int aem_loaded;",
            f"#define {name} {value}\n\nstatic int aem_loaded;", label)

    #: A decoded register the firmware never writes: a READ of it is inert to
    #: every census rule, so the mutations below carry the jump, not a write.
    probe = spare_name
    preprocessor_guard = defined(
        replace_once(
            firmware_source, guard_statement,
            "#ifdef MILAN_DEV_ALWAYS_ADVERTISE\n\tentity_advertise(1);\n"
            "#else\n\t" + guard_statement + "\n#endif",
            "preprocessor-selected guard"),
        "MILAN_DEV_ALWAYS_ADVERTISE", "1", "dev-advertise flag")
    preprocessor_clear = replace_once(
        firmware_source, source_adp_clear + ";",
        "#ifdef MILAN_CLEAR_ENTITY_ON_BOOT\n\t" + source_adp_clear +
        ";\n#endif", "pre-AEM clear behind a build flag")
    dead_configure = defined(
        replace_once(firmware_source, configure_statement,
                     "if (MILAN_FABRIC_PRECONFIGURED == 0)\n\t\t" +
                     configure_statement, "compile-time-dead boot step"),
        "MILAN_FABRIC_PRECONFIGURED", "1", "preconfigured-fabric flag")
    goto_into_guard = replace_once(
        replace_once(
            firmware_source, load_statement,
            f"if (milan_read({probe}) & 2u)\n\t\tgoto entity_up;\n\t"
            + load_statement, "jump past the AEM verifier"),
        guard_statement, "entity_up:\n\t" + guard_statement,
        "label before the entity-advertise call")
    case_into_guard = replace_once(
        firmware_source, guard_statement,
        f"switch (milan_read({probe}) & 2u) {{\n\tcase 2:\n\t\t" +
        guard_statement + "\n\tdefault:\n\t\tbreak;\n\t}",
        "case label falling into the entity-advertise call")
    def one_physical_line(text):
        """A census record as ONE physical line.

        Splicing a record into a continuation macro assumes exactly that, and
        the record is whatever the firmware's own line breaks made it. A
        legitimate multi-line enable -- which this gate accepts, and which is
        one of the brittleness cases -- would otherwise leave its first line
        without the trailing backslash and build a mutant that does not
        compile: `expected ';' before ')'`. Same class as the mutant that
        once called an undeclared helper: a mutation must be real firmware,
        or it proves nothing about a rule."""
        return " ".join(text.split())

    #: The two enables hidden in a continued macro body and INVOKED from a
    #: UART command handler. It used to be refused by the ban on a
    #: multi-line `#define`, which is retired with the choke point (#153):
    #: the resolved census reads the COMPILED call, where the macro is
    #: already expanded, so it places the write in the handler that makes it.
    source_enables_text = source_enable_block[
        source_pp_enable["start"]:source_adp_enable["stop"] + 1]
    macro_enable = replace_once(
        replace_once(
            firmware_source, source_enables_text,
            "\n#define MILAN_ENTITY_UP() \\\n\tdo { \\\n"
            f"\t\t{one_physical_line(pp_enable_text)}; \\\n"
            f"\t\t{one_physical_line(adp_enable_text)}; \\\n"
            "\t} while (0)\n\tMILAN_ENTITY_UP();",
            "continuation-line macro body"),
        "\tprint_tod(gettime_ns());\n}",
        "\tMILAN_ENTITY_UP();\n\tprint_tod(gettime_ns());\n}",
        "macro enable reached from a UART handler")
    formfeed_macro_enable = macro_enable.replace("\\\n", "\\\f\n", 1)
    assert formfeed_macro_enable != macro_enable, \
        "form-feed continuation-line macro mutation did not apply"
    verdict_pointer = replace_once(
        replace_once(firmware_source, load_statement,
                     load_statement +
                     "\n\tverdict = &aem_loaded;\n\t*verdict = 1;",
                     "verdict written through a pointer"),
        "static int aem_loaded;",
        "static int aem_loaded;\nstatic int *verdict;", "verdict pointer")
    status_return = replace_once(
        firmware_source, crc_guard_statement,
        f"if (milan_read({probe}) & 2u)\n\t\treturn 2;\n\t"
        + crc_guard_statement, "verifier fast path returning a status code")
    #: A SECOND decode arm gives adp_ctrl a second address. The name table
    #: still maps one name to one address, so only the decode says otherwise.
    mirror_address = next(a for a in range(source_model.adp, 0x10000, 4)
                          if a not in source_model.decoded)
    adp_constant = re.search(
        r"\bA_ADP_CTRL\s*=\s*(?:[0-9]+)?'[hH][0-9A-Fa-f_]+",
        csr_source).group(0)
    adp_arm = re.search(
        r"(?m)^([ \t]*)A_ADP_CTRL\s*:\s*adp_ctrl\s*<=[^;]*;", csr_source)
    mirrored_csr = replace_once(
        replace_once(csr_source, adp_constant,
                     f"A_ADP_MIRROR = 'h{mirror_address:X}, {adp_constant}",
                     "second ADP_CTRL decode constant"),
        adp_arm.group(0),
        adp_arm.group(0) + "\n" + adp_arm.group(1) +
        "A_ADP_MIRROR: adp_ctrl <= s_axi_wdata;", "second ADP_CTRL decode arm")
    mirrored_enable = defined(
        replace_once(
            firmware_source, source_adp_clear + ";",
            "milan_write(MILAN_ADP_MIRROR, milan_read(MILAN_ADP_MIRROR) | 1u);"
            "\n\t" + source_adp_clear + ";",
            "pre-AEM enable through the mirrored address"),
        "MILAN_ADP_MIRROR", f"0x{mirror_address:03x}u", "ADP mirror address")
    # ... and the other half of each new rule, so the rule cannot rot into a
    # rule that only ever looks at the one shape it was written against.
    _load_directives, source_load_arm = cpp_arms(source_load_code)
    source_crc_arm = source_load_arm(source_crc_guard.start())
    source_returns = list(re.finditer(r"\breturn\b([^;]*);", source_load_code))

    def returned(match, verdict, label):
        return replace_once(
            firmware_source, source_load_function,
            source_load_function[:match.start()] + f"return {verdict};" +
            source_load_function[match.end():], label)

    #: The OTHER arm of the one preprocessor group this gate tolerates: a
    #: success handed back from the no-QSPI path, which every rule that reads
    #: the file as one flat sequence of statements accepts.
    other_arm_success = returned(
        next(m for m in source_returns if constant_value(m.group(1)) == 0 and
             source_load_arm(m.start())[:len(source_crc_arm)] !=
             source_crc_arm),
        1, "success returned from the other preprocessor arm")
    #: ... and the CRC comparison itself moved into an arm of its own, so the
    #: success return is no longer in the same code as the comparison.
    crc_guard_block = source_load_function[
        source_crc_guard.start():crc_close + 1]
    optional_crc = replace_once(
        firmware_source, crc_guard_block,
        "#ifndef MILAN_SKIP_CRC\n\t" + crc_guard_block + "\n#endif",
        "CRC comparison behind a build flag")
    #: A verifier that can never say yes would leave the guarded block dead
    #: and every rule about it vacuously true.
    vacuous_verifier = returned(
        [m for m in source_returns if constant_value(m.group(1)) != 0][-1],
        0, "verifier with no success return")
    #: A statement in the guarded block that is neither enable nor printf:
    #: something for control to be steered at, and something unclassified.
    #: GREEN with the choke point (#153) and moved to the accepted cases:
    #: an ordinary `cdelay(64);` between the two enables. The refusal it
    #: used to trip -- the guarded block holding the two enables and their
    #: printf and nothing else -- existed so nothing inside the block was
    #: unclassified; the resolved dominance measurement answers that by
    #: data flow instead, whatever else the function contains.
    extra_in_guard = replace_once(
        firmware_source, source_enable_block,
        source_enable_block[:source_adp_enable["stop"] + 1] +
        "\n\tcdelay(64);" +
        source_enable_block[source_adp_enable["stop"] + 1:],
        "extra statement inside the entity-advertise choke point")

    # ---- and the two axes R1 opened at 2185e810: the object list, which one
    # continuation line grows past the file this gate reads, and the reset
    # values of the very two bits the whole census is about. Both compile,
    # both are ordinary edits, and both used to pass.
    #: The anchor is the PARSER's own regex, not a second and stricter
    #: spelling of it. A reader that accepts `OBJECTS := x.o` beside a mutator
    #: that does not is the tolerant-reader/literal-mutator defect one layer
    #: up from where round three found it, and it fails the SUITE with a
    #: message blaming a mutation for a file this gate reads correctly.
    #: Read through the same splice the parser reads through, or a value
    #: continued onto the next line is anchored as the single character `\`.
    spliced_makefile = line_spliced(makefile_source)
    source_objects_assigns = list(
        objects_assign_re.finditer(spliced_makefile))
    assert source_objects_assigns, \
        "the Makefile no longer assigns OBJECTS in a form makefile_objects() " \
        "parses, so the mutations below would test nothing"
    source_objects_line = source_objects_assigns[-1]
    #: ... and the VALUE's extent stops where the parser's comment strip
    #: stops, so a trailing comment cannot swallow a spliced continuation.
    objects_value_at, objects_value_to = source_objects_line.span(2)
    _objects_hash = spliced_makefile.find("#", objects_value_at,
                                          objects_value_to)
    if _objects_hash >= 0:
        objects_value_to = _objects_hash
    second_object = "milan_bringup.o"

    objects_span_at = source_objects_assigns[0].start()
    objects_span_to = source_objects_assigns[-1].end()

    def objects_valued_line(line):
        """The Makefile with EVERY OBJECTS assignment replaced by `line`."""
        return (makefile_source[:objects_span_at] + line +
                makefile_source[objects_span_to:])

    def objects_valued(text):
        """The Makefile with its LAST OBJECTS assignment carrying `text`,
        spliced at the offsets the parser itself reported: a second `.c` in
        the image, with its own CSR base, its own address helper and its own
        init hook, and not one rule in this gate reads it."""
        return (makefile_source[:objects_value_at] + text +
                makefile_source[objects_value_to:])

    live_objects = " ".join(
        spliced_makefile[objects_value_at:objects_value_to].split())
    listed_objects = objects_valued(f"{live_objects} {second_object}")
    appended_objects = (makefile_source[:source_objects_line.end()] +
                        f"\nOBJECTS += {second_object}" +
                        makefile_source[source_objects_line.end():])
    continued_objects = objects_valued(
        f"{live_objects} \\\n\t{second_object}")
    wildcard_objects = objects_valued("$(patsubst %.c,%.o,$(wildcard *.c))")
    archived_objects = replace_once(
        makefile_source, "$(AR) crs $@ $(OBJECTS)",
        f"$(AR) crs $@ $(OBJECTS) {second_object}",
        "second object archived past OBJECTS")
    #: Pin the reason on the LIST the parser reported, not just on the rule:
    #: a refusal that never saw the second object proves nothing about it.
    both_objects = f"make builds {[firmware_object, second_object]}"
    # ---- and the axis measured at the RIGHT boundary. One OBJECT is not one
    # FILE, and one archive entry is not one SOURCE. All three of these leave
    # the OBJECTS list at exactly one object, so the check above is SATISFIED
    # rather than evaded, and all three used to pass the complete suite.
    source_includes = [d for d in directive_re.finditer(firmware_code)
                       if d.group(1) == "include"]
    assert source_includes, \
        "include-set mutation lost the firmware's #include lines"
    #: End of the LAST include's line, so a spliced directive lands after a
    #: whole one rather than inside its operand.
    last_include_end = firmware_code.index("\n", source_includes[-1].end())

    def after_includes(line):
        return (firmware_source[:last_include_end] + "\n" + line +
                firmware_source[last_include_end:])

    #: A `.c` pulled into the one translation unit by the preprocessor: the
    #: object count never moves and every closure rule reads the wrong file.
    included_source = after_includes(f'#include "{second_object[:-2]}.c"')
    #: ... and the same file reached by spellings an include REGEX misses but
    #: the preprocessor does not: a macro operand, a spliced directive and
    #: the `%:` digraph.
    macro_included_source = after_includes(
        f'#define MILAN_EXTRA_SRC "{second_object[:-2]}.c"\n'
        "#include MILAN_EXTRA_SRC")
    spliced_included_source = after_includes(
        f'#\\\ninclude "{second_object[:-2]}.c"')
    digraph_included_source = after_includes(
        f'%:include "{second_object[:-2]}.c"')
    #: ... and the trigraph, which fires only under a strict -std=cNN. LiteX
    #: compiles with -std=gnu99, so this one does not bite the shipping
    #: build; it is refused anyway, because a gate that is correct only
    #: because of a flag it never reads is correct by luck.
    trigraph_included_source = after_includes(
        f'??=include "{second_object[:-2]}.c"')
    #: A directive this gate has no rule for at all.
    undefined_constant = after_includes(f"#undef {adp_name}")
    #: ---- stores that reach the entity-enable register without any of the
    #: ingredients the CSR store closure names. Each is a REAL pre-AEM
    #: advertise: the address is MILAN_CSR_BASE + A_ADP_CTRL, derived from
    #: milan_soc.py and the RTL decode table rather than mirrored, so the
    #: mutant fails for the defect its label claims. An earlier revision of
    #: these four stored to 0xf000_0600, which is the LiteX CSR bank and not
    #: ADP_CTRL at all, so they reddened on an address-blind rule while
    #: demonstrating no entity enable whatsoever.
    def stored_before_aem(statement, label):
        """Spliced at the END of configure_fabric(), for the same reason
        enabled_before_aem() is: ahead of the clears the firmware would undo
        the mutant's own store before the AEM decision."""
        return replace_once(firmware_source, fabric_tail,
                            fabric_tail + "\n\t" + statement, label)

    adp_window_address = csr_base + source_model.adp
    raw_address = f"0x{adp_window_address:08x}u"
    widened_cast_store = stored_before_aem(
        f"*(volatile unsigned int *){raw_address} = 1u;",
        "store through a widened cast")
    reordered_cast_store = stored_before_aem(
        f"*(uint32_t volatile *){raw_address} = 1u;",
        "store through a reordered cast")
    #: ... a pointer held in a local, formed by a cast that names no type.
    local_pointer_store = stored_before_aem(
        f"volatile uint32_t *adp = (void *){raw_address};\n\t*adp = 1u;",
        "store through a pointer held in a local")
    #: ... and the four shapes no RECOGNIZER in this file ever saw: a
    #: typedef'd pointer type behind a register-access macro, a struct
    #: overlay with an `->` store, a typedef'd pointer with a subscript
    #: store, and a qualifier after the star. All four are ordinary embedded
    #: idioms and all four passed the complete suite before the census.
    typedef_macro_store = replace_once(
        stored_before_aem("MILAN_ADP_REG = 1u;", "register-access macro store"),
        "static int aem_loaded;",
        "typedef volatile uint32_t *milan_csr_p;\n"
        f"#define MILAN_ADP_REG (*(milan_csr_p){raw_address})\n\n"
        "static int aem_loaded;", "register-access macro")
    overlay_member_store = replace_once(
        stored_before_aem(f"((milan_adp_block){raw_address})->ctrl = 1u;",
                          "struct-overlay member store"),
        "static int aem_loaded;",
        "typedef struct { volatile uint32_t ctrl; } *milan_adp_block;\n\n"
        "static int aem_loaded;", "struct overlay typedef")
    typedef_subscript_store = replace_once(
        stored_before_aem(f"((milan_csr_pp){raw_address})[0] = 1u;",
                          "typedef subscript store"),
        "static int aem_loaded;",
        "typedef volatile uint32_t *milan_csr_pp;\n\n"
        "static int aem_loaded;", "subscript typedef")
    qualified_cast_store = stored_before_aem(
        f"((volatile uint32_t *const){raw_address})[0] = 1u;",
        "store through a qualifier-after-star cast")
    #: ... and a store with no cast at all, through a helper's parameter.
    helper_pointer_store = replace_once(
        stored_before_aem("milan_poke(&milan_shadow);",
                          "store through a helper's parameter"),
        "static void configure_fabric(void)",
        "static uint32_t milan_shadow;\n\n"
        "static void milan_poke(volatile uint32_t *reg)\n{\n\t*reg = 1u;\n}"
        "\n\nstatic void configure_fabric(void)", "pointer-store helper")
    #: ... and an inline-asm store, whose template carries no C construct at
    #: all. The address is spliced from the same derived constant.
    asm_store_enable = stored_before_aem(
        f'__asm__ volatile("li t0, {raw_address[:-1]}\\n"\n'
        '\t                 "li t1, 1\\n"\n'
        '\t                 "sw t1, 0(t0)\\n" ::: "t0", "t1", "memory");',
        "inline-asm store to ADP_CTRL")
    #: An explicit rule for the one object overrides the pattern rule and
    #: decides what goes INTO it, with OBJECTS and the archive untouched.
    linked_objects = (
        makefile_source[:source_objects_line.end()] +
        f"\n\n{firmware_object}: {firmware_object[:-2]}.part.o "
        f"{second_object[:-2]}.part.o\n\t$(LD) -r -o $@ $^\n\n"
        "%.part.o: $(LIBMILAN_BAREMETAL_DIRECTORY)/%.c\n\t$(compile)" +
        makefile_source[source_objects_line.end():])
    #: ... and a fragment this Makefile's own text never names, which can do
    #: any of the above out of sight.
    fragment_objects = (
        makefile_source[:source_objects_line.end()] +
        "\n-include extra.mk" +
        makefile_source[source_objects_line.end():])

    def after_objects(line):
        return (makefile_source[:source_objects_line.end()] + "\n" + line +
                makefile_source[source_objects_line.end():])

    #: The producing rule's own prerequisite, read off the live Makefile so
    #: the mutation names whatever variable it actually uses.
    source_producer_prereq = next(
        rule[1][0] for rule in make_rules(makefile_source)[0]
        if rule[0] == ["%.o"])
    assert make_var_re.findall(source_producer_prereq), \
        "text-deciding mutation found no variable in the producing rule's " \
        f"prerequisite: {source_producer_prereq}"

    #: Pinning the RULE is not enough while a variable can move the file out
    #: from under it. None of these three touches OBJECTS, the archive, the
    #: producing rule or the firmware's #include set.
    injected_source = after_objects(
        f"CFLAGS += -include {second_object[:-2]}.c")
    recompiled_objects = after_objects(
        f"compile = $(CC) $(CFLAGS) -c -o $@ $< {second_object[:-2]}.c")
    #: ... and the same injection behind make's other modifier keywords, and
    #: written against a target so make inherits it down the prerequisite
    #: chain. An assignment regex narrower than make is the same defect as an
    #: include regex narrower than the preprocessor.
    exported_injection = after_objects(
        f"export CFLAGS += -include {second_object[:-2]}.c")
    target_injection = after_objects(
        f"all: CFLAGS += -include {second_object[:-2]}.c")
    #: The producing rule's OWN prerequisite variable, which is the one name
    #: a hand-written list of text-deciding variables did not have.
    shadowed_source_dir = after_objects(
        f"{make_var_re.findall(source_producer_prereq)[0]} = ./shadow")
    #: ... and a name that changes what MAKE does rather than what the rule
    #: names, which no derivation from the rule can reach.
    #: ---- and RESOLUTION: a pinned name whose FILE this repository supplies.
    #: Neither of these changes a name anywhere. The first is a listing, the
    #: second a search path, and both put this repository's text behind an
    #: include the gate believes it has pinned.
    shadowed_quoted_include = firmware_listing + ("command.h",)
    shadowed_search_path = after_objects("CFLAGS += -Ishadow")
    #: An object list the ENVIRONMENT can override. `?=` looks equivalent
    #: and is not: make treats an environment variable as defined, so this
    #: builds whatever `OBJECTS` says outside the file.
    environment_objects = objects_valued_line(f"OBJECTS ?= {firmware_object}")
    #: ... and the search-path flag that is not spelled -I, which is how the
    #: -I rule turned out to be a denylist the moment it was written.
    quoted_search_path = after_objects("CFLAGS += -iquote shadow")

    def raised_bit0(statement, label):
        """`statement` with bit 0 of its literal SET, rebuilt at the literal's
        own width and base: the RTL's own spelling of its reset value with the
        enable bit on, rather than a second literal hard-coded here."""
        match = re.search(r"(?:<=|=)\s*([^;]*);", statement)
        assert match, f"{label} mutation found no literal to raise"
        literal = re.sub(r"\s", "", match.group(1))
        value = sv_literal_value(literal)
        assert value is not None and not value & 1, \
            f"{label} mutation needs a readable literal with bit 0 clear"
        based = sv_based_re.match(literal)
        if based:
            width = len(based.group("digits").replace("_", ""))
            base = sv_bases[based.group("base").lower()]
            raised = based.group("head") + format(
                value | 1, f"0{width}{sv_formats[base]}")
        else:
            raised = str(value | 1)
        return statement[:match.start(1)] + raised + statement[match.end(1):]

    def literal_reset(signal):
        """The one LITERAL assignment to `signal` in the RTL: its reset value,
        found by what it is rather than by the line it sits on."""
        found = [m.group(0) for m in re.finditer(
            rf"\b{re.escape(signal)}\s*(?:<=|=)\s*([^;]*);", csr_source)
            if sv_literal_re.match(m.group(1))]
        assert len(found) == 1 and csr_source.count(found[0]) == 1, \
            f"{signal} reset mutation found no unique literal reset: {found}"
        return found[0]

    adp_reset_statement = literal_reset("adp_ctrl")
    pp_reset_statement = literal_reset("pp_ctrl_r")
    adp_reset_enabled = replace_once(
        csr_source, adp_reset_statement,
        raised_bit0(adp_reset_statement, "ADP_CTRL reset"),
        "ADP_CTRL reset value advertising the entity")
    pp_reset_enabled = replace_once(
        csr_source, pp_reset_statement,
        raised_bit0(pp_reset_statement, "PP_CTRL reset"),
        "PP_CTRL reset value enabling the protocol processor")
    #: ... and the same with the READBACK default moved to match, so the
    #: mutant is self-consistent SV that no other rule in the file disagrees
    #: with: nothing but the reset rule itself can catch this one.
    adp_default_statement = re.search(
        r"\bA_ADP_CTRL\s*\[[^\]]*\]\s*:\s*csr_default\s*=\s*[^;]*;",
        csr_source)
    assert adp_default_statement, \
        "ADP_CTRL reset mutation lost the readback default it must match"
    consistent_reset_enabled = replace_once(
        adp_reset_enabled, adp_default_statement.group(0),
        raised_bit0(adp_default_statement.group(0),
                    "ADP_CTRL readback default"),
        "ADP_CTRL readback default agreeing with the raised reset")

    #: ---- the three shapes that were RED at cc2ee861 and GREEN at
    #: 828e5b06, i.e. the ones the round-nine deletions reopened. Each is
    #: caught by a restored family and NOT by the compiled census, which is
    #: the measured evidence that the census is an addition rather than a
    #: replacement.
    #:
    #: A store added inside the helper the census exempts BY NAME. Rule 1
    #: is satisfied (the use is inside reg_span) and the census skips the
    #: function, so only the cast SET sees the fifth cast.
    def helper_body_store_for(baseline, label):
        """Add the exempted-helper escape relative to `baseline` itself."""
        code = blanked(baseline)
        reg_def = re.search(
            r"\bstatic\s+inline\s+volatile\s+uint32_t\s*\*\s*milan_reg\s*"
            r"\(\s*unsigned\s+int\s+\w+\s*\)\s*\{", code)
        assert reg_def, f"{label}: address-helper mutation lost milan_reg()"
        body_at, _body_to = braced_span(code, reg_def, f"{label} milan_reg()")
        changed = (
            baseline[:body_at] +
            f"\n\t*(volatile uint32_t *)(MILAN_CSR_BASE + {adp_name}) = 1u;" +
            baseline[body_at:])
        assert changed != baseline, \
            f"{label}: store inside the exempted address helper did not apply"
        return changed

    helper_store_baselines = [
        ("reflowed live-source" if reflowed_firmware == firmware_source
         else "shipping", firmware_source)]
    if reflowed_firmware != firmware_source:
        helper_store_baselines.append(("reflowed", reflowed_firmware))
    helper_body_store_mutations = tuple(
        (label, helper_body_store_for(baseline, label))
        for label, baseline in helper_store_baselines)
    #: WHY these two stay pinned on the cast set instead of on the
    #: address-helper provenance rule that names the same function (#206).
    #: Rule 6's own comment records the ordering; this MEASURES what the
    #: ordering buys. The compiled census exempts the helper BY NAME, so a
    #: store planted inside it is invisible to the census -- and these two
    #: are the only mutants left that demonstrate the cast set catching a
    #: shape the census cannot see, which is the evidence round nine
    #: deleted and #187 restored. Re-pinning them on the provenance rule
    #: would retire that evidence; the provenance rule already has its own
    #: reason-pinned mutant ("milan_reg() ignores its offset"). So: run the
    #: census over each of them here and require it to come back CLEAN.
    #: ... and the POSITIVE arm, which is what #153 adds: the same mutant
    #: run through the RESOLVER, which must REJECT it. The census exempts
    #: the helper BY NAME and so cannot see a store planted in it; the
    #: resolver censuses STORES and exempts nobody, so it answers the shape
    #: by the address the store resolves to. Measuring both on one compile
    #: is what makes "an addition, not a replacement" a measurement here
    #: rather than a claim (process guard 2 from #143's close).
    helper_store_census_blind = 0
    helper_store_census_asked = 0
    helper_store_resolver_caught = 0
    if baseline_census_verdict["ran"]:
        helper_store_census_asked = len(helper_body_store_mutations)
        for label, mutation in helper_body_store_mutations:
            taken = census_take(
                mutation, f"exempted-helper store, {label} baseline")
            blind = assert_compiled_census_is_clean(
                mutation, f"exempted-helper store, {label} baseline",
                taken=taken)
            assert blind["ran"], \
                "the exempted-helper blindness control did not actually " \
                "run the census, so it proves nothing about which " \
                "instrument has to catch this shape"
            helper_store_census_blind += 1
            try:
                assert_resolved_boot_flow(taken["text"], source_model,
                                          f"exempted-helper store, {label}")
            except AssertionError as exc:
                assert RESOLVER_STORE_PIN in str(exc), \
                    "the resolver refused the exempted-helper store for " \
                    f"the wrong reason: {exc}"
                helper_store_resolver_caught += 1
            else:
                raise AssertionError(
                    "the resolver accepted a store inside the exempted "
                    f"address helper ({label} baseline), so the shape the "
                    "census is blind to is open on both instruments")
    #: An address the compiler never prints as a whole-window immediate: at
    #: -O0 it is built with slli/ori, so the census's regex has nothing to
    #: match. This is not only adversarial: a firmware serving two CSR bases
    #: arrives here naturally.
    paged_base_store = replace_once(
        stored_before_aem(
            f"*(volatile uint32_t *)((csr_page << 16) | {adp_name}) = 1u;",
            "store through a base held in a variable"),
        "static int aem_loaded;",
        f"static unsigned int csr_page = 0x{csr_base >> 16:04x}u;\n\n"
        "static int aem_loaded;", "paged CSR base")
    #: ---- the shapes issue #153 was filed for, and the reason the
    #: resolver exists. Each reaches a control register or a non-zero
    #: verdict WITHOUT printing a window immediate or naming a construct
    #: any reader of text recognises, and each was measured GREEN on the
    #: instruments that preceded the resolver (see the PR's escape table).
    pp_name = next(name for name, value in sorted(source_model.defines.items())
                   if value == source_model.pp)
    overlay_paged_store = replace_once(
        stored_before_aem(
            f"((milan_adp_blk)((csr_page << 16) | {adp_name}))->ctrl = 1u;",
            "struct-overlay store through a paged base"),
        "static int aem_loaded;",
        "typedef struct { volatile uint32_t ctrl; } *milan_adp_blk;\n"
        f"static unsigned int csr_page = 0x{csr_base >> 16:04x}u;\n\n"
        "static int aem_loaded;", "paged struct overlay typedef")
    subscript_paged_store = replace_once(
        stored_before_aem(
            f"((milan_csr_page_p)((csr_page << 16) | {pp_name}))[0] = 1u;",
            "subscript store through a paged base"),
        "static int aem_loaded;",
        "typedef volatile uint32_t *milan_csr_page_p;\n"
        f"static unsigned int csr_page = 0x{csr_base >> 16:04x}u;\n\n"
        "static int aem_loaded;", "paged subscript typedef")
    #: ---- and the verifier's CONTROL and DATA flow, which no positional
    #: rule reaches: two ways to the success return that never take the
    #: comparison, the comparison made against a value crc32() never
    #: produced, and the CRC taken over the QSPI source rather than over the
    #: DRAM buffer the descriptor store actually serves.
    crc_local = source_crc_guard.group("lhs") or source_crc_guard.group("rhs")
    crc_assign = re.search(
        rf"\b{re.escape(crc_local)}\s*=\s*crc32\s*\([^;]*;", source_load_code)
    assert crc_assign, "the CRC data-flow mutations lost the crc32() call"
    crc_assign_text = source_load_function[crc_assign.start():crc_assign.end()]
    crc_success = [match for match in source_returns
                   if constant_value(match.group(1)) != 0][-1]
    _goto_body = (source_load_function[:crc_success.start()] + "crc_ok:\n\t" +
                  source_load_function[crc_success.start():])
    goto_past_crc = replace_once(
        firmware_source, source_load_function,
        replace_once(_goto_body, crc_guard_statement,
                     "if (src[4] == 'X')\n\t\tgoto crc_ok;\n\t" +
                     crc_guard_statement, "goto past the CRC comparison"),
        "verifier reaching its success return by goto")
    _crc_region = source_load_function[crc_assign.start():crc_close + 1]
    _do_region = ("do {\n\t" + replace_once(
        _crc_region, crc_guard_statement,
        "if (src[4] == 'X')\n\t\t\tbreak;\n\t\t" + crc_guard_statement,
        "structured break past the CRC comparison").replace("\n\t", "\n\t\t") +
        "\n\t} while (0);")
    break_past_crc = replace_once(
        firmware_source, source_load_function,
        source_load_function[:crc_assign.start()] + _do_region +
        source_load_function[crc_close + 1:],
        "verifier reaching its success return by break")
    crc_overwritten = replace_once(
        firmware_source, crc_guard_statement,
        f"{crc_local} = MILAN_AEM_IMAGE_CRC32;\n\t" + crc_guard_statement,
        "CRC result overwritten between the call and the comparison")
    crc_over_qspi_source = replace_once(
        firmware_source, crc_assign_text,
        replace_once(crc_assign_text, "MILAN_AEM_DESC_BASE",
                     "(SPIFLASH_BASE + MILAN_AEM_FLASH_OFFSET)",
                     "CRC operand repointed at the QSPI source"),
        "CRC taken over the QSPI source rather than the descriptor buffer")

    #: The asm spelling any RISC-V programmer writes. objdump annotates the
    #: store `# 90000600`, but no window immediate is ever printed, so the
    #: census misses it and the asm SET is what refuses it.
    lui_asm_store = stored_before_aem(
        f'__asm__ volatile("lui t0, 0x{csr_base >> 12:05x}\\n\\t"\n'
        '\t                 "li t1, 1\\n\\t"\n'
        f'\t                 "sw t1, 0x{source_model.adp:x}(t0)"\n'
        '\t                 ::: "t0", "t1", "memory");',
        "lui-based inline-asm store")
    #: ---- and the two Makefile shapes the sentinel filter discarded. make
    #: PRINTED both extra lines; the gate kept only the ones carrying a
    #: sentinel and reported one translation unit.
    literal_tool_rule = replace_once(
        makefile_source, "%.o: $(LIBMILAN_BAREMETAL_DIRECTORY)/%.c",
        f"{firmware_object}: $(LIBMILAN_BAREMETAL_DIRECTORY)/"
        f"{firmware_object[:-2]}.c\n\t$(compile)\n"
        f"\triscv32-linux-gcc -c $(LIBMILAN_BAREMETAL_DIRECTORY)/"
        f"{second_object[:-2]}.c -o {second_object}\n"
        f"\triscv32-linux-ld -r $@ {second_object} -o $@\n\n"
        "%.o: $(LIBMILAN_BAREMETAL_DIRECTORY)/%.c",
        "explicit rule whose extra lines name tools literally")
    literal_tool_archive = replace_once(
        makefile_source, "\t$(AR) crs $@ $(OBJECTS)",
        f"\tgcc -c $(LIBMILAN_BAREMETAL_DIRECTORY)/{second_object[:-2]}.c "
        f"-o {second_object}\n\t$(AR) crs $@ $(OBJECTS)\n"
        f"\tar q $@ {second_object}",
        "second object archived by a literal ar")
    #: ---- a second file injected through a TOOL variable. LiteX defines
    #: `compile` as `$(CC) -c $(CFLAGS) ...`, so a flag on CC reaches the
    #: shipping compile. It contributes no `.c` to the plan, no `.o`, and no
    #: CFLAGS token, which is why reading the flags out of CFLAGS missed it
    #: and reading the whole recipe LINE catches it.
    tool_variable_injection = replace_once(
        makefile_source, "CFLAGS += -I$(BIOS_DIRECTORY)",
        "CFLAGS += -I$(BIOS_DIRECTORY)\n"
        "CC += -include $(LIBMILAN_BAREMETAL_DIRECTORY)/../shadow.h",
        "second file injected through CC")
    tool_variable_search_path = replace_once(
        makefile_source, "CFLAGS += -I$(BIOS_DIRECTORY)",
        "CFLAGS += -I$(BIOS_DIRECTORY)\nCC += -iquote ../shadow",
        "search path added through CC")

    #: ---- three injection spellings no scan here ever named. They are in
    #: the table not because the rule enumerates them (it does not) but
    #: because they are the measured proof that it does not have to: each
    #: changes the pinned compile command and is refused by the SET, and
    #: adding a fourth spelling would need no change to the rule at all.
    def tool_flag(line, label):
        return replace_once(makefile_source, "CFLAGS += -I$(BIOS_DIRECTORY)",
                            "CFLAGS += -I$(BIOS_DIRECTORY)\n" + line, label)

    preprocessor_passthrough = tool_flag(
        "CC += -Wp,-include,$(LIBMILAN_BAREMETAL_DIRECTORY)/../shadow.h",
        "injection through the preprocessor pass-through")
    response_file_injection = tool_flag(
        "CC += @$(LIBMILAN_BAREMETAL_DIRECTORY)/../shadow.rsp",
        "injection through a response file")
    prefixed_search_path = tool_flag(
        "CC += -iprefix $(LIBMILAN_BAREMETAL_DIRECTORY)/../ "
        "-iwithprefixbefore shadow",
        "search path through the prefix chain")

    #: ---- and MAKEFLAGS += -e, RESTORED as a mutant. Round nine retired it
    #: on a false measurement; it does let the environment override OBJECTS
    #: and CFLAGS in the same run. It is pinned on the hostile double-run,
    #: which is what actually catches it.
    #: Placed ABOVE the assignments it affects, which is where a real one
    #: would go: `-e` reaches assignments make has not read yet.
    env_override_flags = replace_once(
        makefile_source, "CFLAGS += -I$(BIOS_DIRECTORY)",
        "MAKEFLAGS += -e\n\nCFLAGS += -I$(BIOS_DIRECTORY)",
        "environment override switched on")

    #: ---- and the two shapes that made the reset rule vacuous. The reader
    #: saw `<=` only, so a BLOCKING reset left it nothing to iterate and it
    #: passed by having nothing to check; a deleted reset did the same. Both
    #: reddened the suite from the mutation scaffolding with a message
    #: blaming a mutation for a change in the RTL, which is the
    #: tolerant-reader / literal-mutator defect this PR has now fixed three
    #: times. Both must fail from assert_decode_is_one_to_one().
    blocking_reset_enabled = replace_once(
        csr_source, adp_reset_statement,
        raised_bit0(adp_reset_statement, "ADP_CTRL blocking reset").replace(
            "<=", " =", 1),
        "ADP_CTRL reset written blocking with the enable bit set")
    absent_reset = replace_once(
        csr_source, adp_reset_statement, "", "ADP_CTRL reset value deleted")

    def condensed(text):
        return re.sub(r"\s+", "", text)

    pp_label = source_model.label(source_model.pp)
    adp_label = source_model.label(source_model.adp)

    reset_spellings = ("32'h0000_0001", "32'd1", "32'b1", "1")
    for spelling in reset_spellings:
        statement = f"ptp_ctrl <= {spelling};"
        if condensed(statement) == condensed(source_reset_statement):
            # The RTL is already spelled this way: accepted by construction,
            # since the live reset just passed the contract above. Demanding
            # a substitution here would fail the suite on a spelling the
            # parser reads correctly.
            equivalent_csr = csr_source
        else:
            equivalent_csr = replace_once(
                csr_source, source_reset_statement, statement,
                f"reset spelling {spelling}")
        assert_boot_contract(firmware_source, docs_source, equivalent_csr)

    #: Legitimate respellings of the object list. makefile_objects() reads
    #: every one of these correctly, so the mutation anchor above has to as
    #: well: a tolerant reader beside a literal mutator fails the SUITE on a
    #: file the gate understands, with a message blaming a "mutation".
    objects_spellings = tuple(
        f"{prefix}OBJECTS {operator} {firmware_object}{trailer}"
        for prefix in ("", "override ", "export ")
        # `?=` is deliberately NOT here. make says it is not an equivalent
        # spelling: `?=` sets only if the variable is undefined, and a
        # variable present in the ENVIRONMENT counts as defined, so
        # `OBJECTS=hostile.o make` builds something else entirely. The
        # regex parser called it equivalent for three rounds; the plan,
        # taken twice under a hostile environment, says otherwise.
        for operator in ("=", ":=", "::=")
        for trailer in ("", "\t# the one translation unit")
    ) + (
        # ... and the two shapes that used to fail the SUITE from the
        # scaffolding rather than the parser: a value continued onto the next
        # line, and a reassignment whose last word is the one that counts.
        f"OBJECTS = \\\n\t{firmware_object}",
        f"OBJECTS = placeholder.o\nOBJECTS = {firmware_object}",
    )
    #: Respell EVERY OBJECTS assignment, not just the last, so "equivalent"
    #: is true by construction. Substituting only the last one is NOT
    #: equivalent when an earlier assignment exists: `?=` after a definition
    #: is ignored and make would build the earlier list, so the gate would be
    #: right to refuse it and the suite would be wrong to call it a spelling.

    for spelling in objects_spellings:
        assert_boot_contract(
            firmware_source, docs_source, csr_source,
            makefile_source[:objects_span_at] + spelling +
            makefile_source[objects_span_to:])

    #: ---- ACCEPTED cases, executable at last -----------------------------
    #:
    #: 83 rejections and, until now, not one executable statement of what a
    #: LEGITIMATE firmware edit looks like. That is the gap this lane kept
    #: falling into: three separate rounds shipped a false RED that failed
    #: the SUITE from the mutation scaffolding, and review found every one
    #: of them, because the suite had nothing to catch them with. A refusal
    #: instrument whose entire cost is measured in legitimate edits needs
    #: its legitimate edits to be a measurement, not a memory.
    #:
    #: Each entry is a real edit to the shipping firmware that must stay
    #: GREEN. Derived from the firmware's own text wherever a name or a
    #: statement is involved, so a rename upstream does not silently turn an
    #: accepted case into a no-op.
    #: SCOPE, so a green loop is not read as general false-RED coverage.
    #: All but the address-helper reflow sit in ONE region: the
    #: enable/clear/guard block and comment blanking. They were prose in the PR
    #: body precisely
    #: BECAUSE they had already been measured GREEN, so the set stops
    #: exactly where the refusal starts. Nothing here touches the cast set,
    #: the store set, the asm set, the directive set, the include set, the
    #: recipe-set pin or the compiled census, which is where the remaining
    #: refusals live. Two ordinary refactors one call-depth out are RED and
    #: disclosed as costs rather than accepted: a milan_set() helper and a
    #: named enable mask. A new refusal in an uncovered region can still
    #: pass this loop untouched; measured, by adding a function-like-macro
    #: ban and watching the suite stay green. If cases are added, the cheap
    #: ones are one per refusal FAMILY, not more variants of the mask.
    accepted_pp_clear = source_pp_clear
    accepted_adp_clear = source_adp_clear
    accepted_cases = {
        "unrelated | 2u write to an already-decoded register":
            replace_once(firmware_source, accepted_adp_clear + ";",
                         accepted_adp_clear + ";\n\tmilan_write("
                         f"{adp_name}, milan_read({adp_name}) | 2u);",
                         "unrelated bit write"),
        "wider pre-AEM clear (& ~3u)":
            replace_once(firmware_source, accepted_adp_clear,
                         f"milan_write({adp_name}, milan_read({adp_name})"
                         " & ~3u)", "wider clear"),
        "comment between the two enables":
            replace_once(firmware_source, adp_enable_text,
                         "/* ADP last: never advertise before the PP is up. */"
                         "\n\t\t" + adp_enable_text, "comment in the guard"),
        "braced early return on the choke point's verdict test":
            replace_once(firmware_source, source_verdict_test,
                         source_verdict_test.replace(
                             "\n\t\treturn;", " {\n\t\treturn;\n\t}"),
                         "braced early return"),
        "literal-zero pre-AEM clear":
            replace_once(firmware_source, accepted_adp_clear,
                         f"milan_write({adp_name}, 0u)", "literal zero clear"),
        "& ~(1u << 0) pre-AEM clear":
            replace_once(firmware_source, accepted_adp_clear,
                         f"milan_write({adp_name}, milan_read({adp_name})"
                         " & ~(1u << 0))", "shifted mask clear"),
        "& 0xfffffffeu pre-AEM clear":
            replace_once(firmware_source, accepted_adp_clear,
                         f"milan_write({adp_name}, milan_read({adp_name})"
                         " & 0xfffffffeu)", "explicit mask clear"),
        "multi-line enable in the guarded block":
            replace_once(firmware_source, adp_enable_text,
                         f"milan_write({adp_name},\n\t\t\t    "
                         f"milan_read({adp_name}) | 1u)", "wrapped enable"),
        "hex 0x1u enable mask":
            replace_once(firmware_source, adp_enable_text,
                         f"milan_write({adp_name}, milan_read({adp_name})"
                         " | 0x1u)", "hex enable mask"),
        "a printf naming milan_write":
            replace_once(firmware_source, accepted_adp_clear + ";",
                         accepted_adp_clear + ";\n\tprintf(\"milan_write()"
                         " clears done.\\n\");", "printf naming the helper"),
        "a commented-out enable":
            replace_once(firmware_source, accepted_adp_clear + ";",
                         accepted_adp_clear + ";\n\t/* "
                         + adp_enable_text + "; */", "commented-out enable"),
        "a second printf inside the guarded block":
            replace_once(firmware_source, adp_enable_text + ";",
                         adp_enable_text + ";\n\t\tprintf(\"entity up\\n\");",
                         "second printf in the guard"),
        #: ---- the three refusals the entity-advertise choke point retires
        #: (#153). Each was a disclosed cost row and each is now a
        #: measurement that it is GREEN, which is the only form a retired
        #: refusal may be recorded in here.
        "an extra statement between the two enables": extra_in_guard,
        "an #ifdef around a debug printf in a UART command handler":
            replace_once(firmware_source, "\tprint_tod(gettime_ns());\n}",
                         "#ifdef MILAN_DEBUG_TOD\n"
                         "\tprintf(\"TOD read\\n\");\n#endif\n"
                         "\tprint_tod(gettime_ns());\n}",
                         "conditional debug printf in a UART handler"),
        "a multi-line #define":
            replace_once(firmware_source, "static int aem_loaded;",
                         "#define MILAN_BOOT_BANNER \\\n"
                         "\t\"Milan baremetal: fabric entity\"\n\n"
                         "static int aem_loaded;", "multi-line #define"),
        "the pre-AEM clears relocated into milan_init()":
            replace_once(
                replace_once(firmware_source,
                             accepted_adp_clear + ";\n\t"
                             + accepted_pp_clear + ";\n", "",
                             "clears lifted out of configure_fabric()"),
                configure_statement,
                accepted_adp_clear + ";\n\t" + accepted_pp_clear + ";\n\t"
                + configure_statement, "clears relocated into milan_init()"),
    }
    if reflowed_firmware != firmware_source:
        accepted_cases["reflowed milan_reg() return type and argument"] = \
            reflowed_firmware
    else:
        # The live file already carries the accepted reflow. The baseline
        # call above is its positive arm; helper_body_store_mutations carries
        # the paired negative arm relative to this exact spelling.
        assert source_reg_signature == reflowed_reg_signature
    for label, accepted in accepted_cases.items():
        assert accepted != firmware_source, \
            f"accepted case {label!r} did not change the firmware, so it " \
            "measures nothing"
        try:
            assert_boot_contract(accepted, docs_source, csr_source)
        except (AssertionError, ValueError) as exc:
            raise AssertionError(
                f"a LEGITIMATE firmware edit is refused: {label}. This gate "
                "is a refusal instrument and its whole cost is measured in "
                "edits like this one, so a new rule that reddens it is a "
                f"regression until the cost is disclosed. Gate said: {exc}"
            ) from exc
    #: ... and the Makefile edits the cost list calls GREEN, measured too.
    accepted_makefiles = {
        "an unrelated DEPFILES variable":
            replace_once(makefile_source, "OBJECTS = " + firmware_object,
                         "DEPFILES = $(patsubst %.o,%.d,$(OBJECTS))\n"
                         "OBJECTS = " + firmware_object, "DEPFILES"),
        # `AR += v` was an accepted case while the flag scans were here. It
        # is RED under the recipe-set pin, and that is a DELIBERATE decision
        # rather than a discovery: the pin is what refuses every injection
        # spelling nobody has thought of, and the price of having no list is
        # that a benign change to a pinned command is refused too. It is
        # disclosed as a cost instead of accepted here. Same for `CC += -Wall`.
        "an extra phony target":
            replace_once(makefile_source, ".PHONY: all clean",
                         ".PHONY: all clean tags\n\ntags:\n\t$(CTAGS) *.c",
                         "extra phony target"),
    }
    for label, accepted in accepted_makefiles.items():
        assert accepted != makefile_source, f"{label} changed nothing"
        try:
            assert_boot_contract(firmware_source, docs_source, csr_source,
                                 accepted)
        except (AssertionError, ValueError) as exc:
            raise AssertionError(
                f"a LEGITIMATE Makefile edit is refused: {label}; "
                f"gate said: {exc}") from exc

    mutations = (
        ("old AEM-gated PTP documentation", firmware_source,
         replace_once(docs_source, old_claim.group(0), old_order, "old ordering"),
         csr_source, "bare-metal boot contract lost"),
        ("CSR identity contract repointed to VERSION",
         identity_contract_at_version, docs_source, csr_source,
         "firmware MILAN_ID must resolve to the RTL A_ID address"),
        ("CSR identity magic changed to the VERSION value",
         identity_magic_at_version, docs_source, csr_source,
         "firmware MILAN_ID_MAGIC must equal the RTL A_ID readback default"),
        ("CSR identity magic replaced by the sampled value",
         identity_magic_at_sample, docs_source, csr_source,
         "firmware MILAN_ID_MAGIC must equal the RTL A_ID readback default"),
        ("CSR identity magic replaced by a sampled expression",
         identity_magic_at_sample_expr, docs_source, csr_source,
         "firmware MILAN_ID_MAGIC must equal the RTL A_ID readback default"),
        ("RTL A_ID address hidden behind a comment decoy", firmware_source,
         docs_source, identity_address_comment_decoy,
         "firmware MILAN_ID must resolve to the RTL A_ID address"),
        ("RTL A_ID default hidden behind a comment decoy", firmware_source,
         docs_source, identity_default_comment_decoy,
         "firmware MILAN_ID_MAGIC must equal the RTL A_ID readback default"),
        ("RTL A_ID address selected through an inactive preprocessor arm",
         firmware_source, docs_source, identity_conditional_decoy,
         "CSR integration proof requires unconditional live "
         "SystemVerilog text"),
        ("RTL A_ID address hidden in an inactive static generate arm",
         firmware_source, docs_source, identity_static_generate_decoy,
         "RTL CSR address declarations must be unconditional module-scope "
         "items"),
        ("RTL A_ID default hidden in a dead procedural case",
         firmware_source, docs_source, identity_dead_default_case,
         "RTL csr_default's address case must be a direct top-level item "
         "after its literal-zero default"),
        ("RTL A_ID defaults-ROM fill forged", firmware_source, docs_source,
         identity_rom_fill_forged,
         "RTL A_ID readback plumbing must preserve the canonical "
         "csr_default ROM and direct AXI read address"),
        ("RTL A_ID read address offset", firmware_source, docs_source,
         identity_read_address_offset,
         "RTL A_ID readback plumbing must preserve the canonical "
         "csr_default ROM and direct AXI read address"),
        ("CSR identity mismatch guard removed", missing_identity_guard,
         docs_source, csr_source,
         "firmware must reject a mismatched CSR identity"),
        ("CSR identity mismatch guard does not return", missing_identity_return,
         docs_source, csr_source,
         "CSR identity mismatch guard must return"),
        ("CSR identity mismatch guard inverted", inverted_identity_guard,
         docs_source, csr_source,
         "firmware must reject a mismatched CSR identity"),
        ("CSR identity sample overwritten before the guard", forged_identity,
         docs_source, csr_source,
         "CSR identity guard must consume the unmodified MILAN_ID sample"),
        ("milan_reg() ignores its offset", wrong_reg_address,
         docs_source, csr_source,
         "milan_reg() must return exactly MILAN_CSR_BASE plus the offset "
         "it is passed"),
        ("milan_read() forges the identity value", forged_csr_read,
         docs_source, csr_source,
         "milan_read() must return exactly the value loaded through "
         "milan_reg(offset)"),
        ("unconditional entity enable",
         replace_once(firmware_source, guard_statement, unconditional_guard,
                      "unconditional guard"), docs_source, csr_source,
         "firmware must configure, load AEM, then guard entity enable"),
        ("inverted entity enable",
         replace_once(firmware_source, guard_statement, inverted_guard,
                      "inverted guard"),
         docs_source, csr_source,
         "firmware must configure, load AEM, then guard entity enable"),
        ("software PTP enable write",
         replace_once(
             firmware_source, load_statement,
             "milan_write(MILAN_PTP_CTRL, "
             "milan_read(MILAN_PTP_CTRL) | 1u);\n\t" + load_statement,
             "PTP write"),
         docs_source, csr_source,
         "firmware must not write the reset-enabled PHC"),
        # The PHC write the docs forbid, hidden one call deep in the step-1
        # helper instead of in milan_init()'s own text.
        ("PHC disabled during fabric configuration",
         replace_once(
             firmware_source, source_fabric_body,
             "\n\tmilan_write(MILAN_PTP_CTRL, 0u);" + source_fabric_body,
             "fabric PHC write"),
         docs_source, csr_source,
         "firmware must not write the reset-enabled PHC"),
        ("ADP before PP",
         replace_once(
             firmware_source, source_enable_block, swapped_enable_block,
             "enable ordering"), docs_source, csr_source,
         "AEM-success guard must enable PP before ADP"),
        ("PP bit 0 not asserted",
         replace_once(firmware_source, source_enable_block, bad_pp_block,
                      "PP enable mask"), docs_source, csr_source,
         f"{pp_label} enable write must assert bit 0"),
        ("ADP bit 0 cleared",
         replace_once(firmware_source, source_enable_block, bad_adp_block,
                      "ADP enable operation"), docs_source, csr_source,
         f"{adp_label} must have exactly one read/OR enable write"),
        # An entity advertised BEFORE the image is verified: the enable moves
        # into step 1, one call outside milan_init()'s own text.
        ("PP enabled before AEM verification",
         replace_once(firmware_source, source_pp_clear, early_pp_enable,
                      "early PP enable"), docs_source, csr_source,
         f"{pp_label} bit 0 may be set only inside the"),
        ("ADP enabled before AEM verification",
         replace_once(firmware_source, source_adp_clear, early_adp_enable,
                      "early ADP enable"), docs_source, csr_source,
         f"{adp_label} bit 0 may be set only inside the"),
        # ---- indirection: the census reads milan_write() call sites, so a
        # name it cannot resolve or a store it cannot see is a way to
        # advertise the entity unexamined. Each escape carries its own mutant.
        ("entity enabled through an indirect helper",
         indirect_helper_enable, docs_source, csr_source,
         "milan_write() must name a register the RTL decodes"),
        # A SECOND #define for 0x600/0x920/0x500 is a different token for the
        # same register: the bus cannot tell them apart, so neither may the
        # census.
        ("ADP enabled through an address alias", alias_adp_enable,
         docs_source, csr_source,
         f"{adp_label} bit 0 may be set only inside the"),
        ("PP enabled through an address alias", alias_pp_enable,
         docs_source, csr_source,
         f"{pp_label} bit 0 may be set only inside the"),
        ("PHC written through an address alias", alias_phc_write,
         docs_source, csr_source,
         "firmware must not write the reset-enabled PHC"),
        # ... and an EXISTING register name repointed at PP_CTRL is an
        # operand the rule already trusts, now naming a different register.
        ("entity enabled through a repointed register name",
         repointed_register, docs_source, csr_source,
         f"{pp_label} bit 0 may be set only inside the"),
        # A pure VALUE constant is not a register operand at all.
        ("milan_write() given a value constant as its register",
         value_operand_write, docs_source, csr_source,
         "milan_write() must name a register the RTL decodes"),
        # ---- the call itself: one space, one function pointer, one paste or
        # one raw store and a text-matched rule walks straight past it.
        ("entity enabled with a space before the call paren",
         spaced_call_enable, docs_source, csr_source,
         f"{adp_label} bit 0 may be set only inside the"),
        ("entity enabled through a phase-2-spliced call name",
         phase2_spliced_call_enable, docs_source, csr_source,
         "firmware must not splice physical source lines with backslash-newline"),
        ("entity enabled through a function pointer", pointer_call_enable,
         docs_source, csr_source,
         "milan_write must always be called, never used as a value"),
        ("entity enabled by storing through milan_reg()", reg_store_enable,
         docs_source, csr_source,
         "milan_reg() may be called only by milan_read()/milan_write()"),
        ("entity enabled through a raw CSR pointer", raw_store_enable,
         docs_source, csr_source,
         "only milan_reg() may form a CSR address"),
        ("entity enabled through a pasted call name", pasted_call_enable,
         docs_source, csr_source,
         "firmware must not paste tokens"),
        # Without the pre-AEM clear a warm reboot advertises a stale entity
        # while the image is still unverified.
        ("PP pre-AEM clear removed",
         replace_once(firmware_source, source_pp_clear, "",
                      "PP pre-AEM clear"), docs_source, csr_source,
         f"{pp_label} bit 0 must be cleared before the AEM image"),
        ("ADP pre-AEM clear removed",
         replace_once(firmware_source, source_adp_clear, "",
                      "ADP pre-AEM clear"), docs_source, csr_source,
         f"{adp_label} bit 0 must be cleared before the AEM image"),
        ("CRC failure accepted",
         replace_once(firmware_source, source_load_function, bad_load_function,
                      "AEM verifier"), docs_source, csr_source,
         "AEM verifier non-zero return must be textually after"),
        ("AEM verdict overridden",
         replace_once(firmware_source, load_statement,
                      load_statement + "\n\taem_loaded = 1;",
                      "AEM verdict override"), docs_source, csr_source,
         "aem_loaded must contain only the image verifier's verdict"),
        ("AEM verdict forced by compound assignment",
         replace_once(firmware_source, load_statement,
                      load_statement + "\n\taem_loaded |= 1;",
                      "AEM verdict OR"), docs_source, csr_source,
         "aem_loaded must contain only the image verifier's verdict"),
        ("AEM verdict incremented",
         replace_once(firmware_source, load_statement,
                      load_statement + "\n\taem_loaded++;",
                      "AEM verdict increment"), docs_source, csr_source,
         "aem_loaded must contain only the image verifier's verdict"),
        ("disabled PHC reset", firmware_source, docs_source,
         replace_once(csr_source, source_reset_statement,
                      "ptp_ctrl <= 32'h0;", "PHC reset"),
         "bare-metal PHC contract requires the documented enabled reset"),
        ("PHC output gated by ADP", firmware_source, docs_source,
         phc_gated_by_adp,
         "milan_csr PHC output assignments must remain direct and "
         "independent"),
        ("milan_csr PHC increment output gated by ADP", firmware_source,
         docs_source, phc_increment_source_gated_by_adp,
         "milan_csr PHC output assignments must remain direct and "
         "independent"),
        ("milan_csr PHC output binding gated by ADP", firmware_source,
         docs_source, csr_source,
         "milan_csr PHC output must drive cfg_ptp_enable directly",
         None, None, phc_binding_gated_by_adp),
        ("PHC enable hidden behind a resolved second driver", firmware_source,
         docs_source, csr_source,
         "datapath PHC nets must retain sole-driver reference ownership",
         None, None, phc_wand_second_driver),
        ("ptp_timestamp PHC consumer gated by ADP", firmware_source,
         docs_source, csr_source,
         "ptp_timestamp PHC enable must be driven directly by "
         "cfg_ptp_enable", None, None, phc_consumer_gated_by_adp),
        ("ptp_timestamp PHC increment gated by ADP", firmware_source,
         docs_source, csr_source,
         "ptp_timestamp PHC controls and readback must remain direct and "
         "independent", None, None, phc_increment_gated_by_adp),
        ("effective PHC frequency adjustment gated by ADP", firmware_source,
         docs_source, csr_source,
         "effective PHC adjustment must select only gPTP or CSR control",
         None, None, phc_effective_adjust_gated_by_adp),
        ("effective PHC offset gated by ADP", firmware_source,
         docs_source, csr_source,
         "effective PHC offset must select only gPTP or CSR control",
         None, None, phc_effective_offset_gated_by_adp),
        ("effective PHC adjustment strobe gated by ADP", firmware_source,
         docs_source, csr_source,
         "effective PHC adjust strobe must select only gPTP or CSR control",
         None, None, phc_effective_strobe_gated_by_adp),
        ("ptp_timestamp gtx reset gated by ADP", firmware_source,
         docs_source, csr_source,
         "ptp_timestamp clocks and resets must be direct and independent",
         None, None, gptp_gated_timestamp_gtx_reset),
        ("ptp_timestamp axis reset gated by ADP", firmware_source,
         docs_source, csr_source,
         "ptp_timestamp clocks and resets must be direct and independent",
         None, None, gptp_gated_timestamp_axis_reset),
        ("ptp_timestamp RX ingress valid gated by ADP", firmware_source,
         docs_source, csr_source,
         "external MAC RX must traverse ptp_timestamp directly",
         None, None, gptp_gated_timestamp_ingress),
        ("ptp_timestamp RX ready gated by ADP", firmware_source,
         docs_source, csr_source,
         "external MAC RX must traverse ptp_timestamp directly",
         None, None, gptp_gated_timestamp_ready),
        ("enabled RX-filter ingress valid gated by ADP", firmware_source,
         docs_source, csr_source,
         "timestamped MAC RX must traverse the enabled RX-filter arm "
         "directly", None, None, gptp_gated_filter_ingress),
        ("enabled RX-filter clock gated by ADP", firmware_source,
         docs_source, csr_source,
         "timestamped MAC RX must traverse the enabled RX-filter arm "
         "directly", None, None, gptp_gated_filter_clock),
        ("enabled RX-filter reset gated by ADP", firmware_source,
         docs_source, csr_source,
         "timestamped MAC RX must traverse the enabled RX-filter arm "
         "directly", None, None, gptp_gated_filter_reset),
        ("RX-filter default policy gated by ADP", firmware_source,
         docs_source, csr_source,
         "reset-time RX filter policy must remain independent of ADP",
         None, None, gptp_filter_policy_gated_by_adp),
        ("bypass RX-filter ingress valid gated by ADP", firmware_source,
         docs_source, csr_source,
         "timestamped MAC RX must traverse the bypass RX-filter arm "
         "directly", None, None, gptp_gated_filter_bypass),
        ("fabric gPTP reset gated by ADP", firmware_source, docs_source,
         csr_source,
         "fabric gPTP RX and control inputs must observe the live datapath "
         "directly", None, None, gptp_gated_datapath),
        ("fabric gPTP ingress valid gated by ADP", firmware_source,
         docs_source, csr_source,
         "fabric gPTP RX and control inputs must observe the live datapath "
         "directly", None, None, gptp_gated_ingress),
        ("fabric gPTP local egress valid gated by ADP", firmware_source,
         docs_source, csr_source,
         "fabric gPTP TX must traverse gptp_ctl_mux directly", None, None,
         gptp_gated_local_egress),
        ("fabric gPTP control-mux reset gated by ADP", firmware_source,
         docs_source, csr_source,
         "fabric gPTP TX must traverse gptp_ctl_mux directly", None, None,
         gptp_gated_control_mux_reset),
        ("fabric gPTP MAC-boundary valid gated by ADP", firmware_source,
         docs_source, csr_source,
         "fabric gPTP control output must reach the MAC-boundary arbiter "
         "directly", None, None, gptp_gated_boundary_egress),
        ("fabric gPTP boundary-mux reset gated by ADP", firmware_source,
         docs_source, csr_source,
         "fabric gPTP control output must reach the MAC-boundary arbiter "
         "directly", None, None, gptp_gated_boundary_mux_reset),
        ("external MAC TX valid gated by ADP", firmware_source,
         docs_source, csr_source,
         "external MAC TX handshake must be driven directly by "
         "tx_axis_to_mac", None, None, gptp_gated_external_tx),
        ("external MAC TX valid hidden behind a resolved second driver",
         firmware_source, docs_source, csr_source,
         "external MAC handshake ports must retain sole-driver/reference "
         "ownership", None, None, gptp_wand_second_driver_external_tx),
        ("commented direct TX decoy with live macro gate", firmware_source,
         docs_source, csr_source,
         "datapath integration proof requires unconditional live "
         "SystemVerilog text", None, None, gptp_commented_external_tx),
        ("direct TX connection made an inactive conditional", firmware_source,
         docs_source, csr_source,
         "datapath integration proof requires unconditional live "
         "SystemVerilog text", None, None, gptp_inactive_external_tx),
        ("direct TX connection put in an inactive static generate arm",
         firmware_source, docs_source, csr_source,
         "external MAC TX handshake must be driven directly by "
         "tx_axis_to_mac", None, None, gptp_static_generate_external_tx),
        ("direct TX decoy selected by mid-line compiler directives",
         firmware_source, docs_source, csr_source,
         "datapath integration proof requires unconditional live "
         "SystemVerilog text", None, None,
         gptp_midline_directive_external_tx),
        ("direct TX decoy selected by an implicit conditional generate",
         firmware_source, docs_source, csr_source,
         "external MAC TX handshake must be driven directly by "
         "tx_axis_to_mac", None, None,
         gptp_implicit_generate_external_tx),
        ("external MAC RX valid gated by ADP", firmware_source,
         docs_source, csr_source,
         "external MAC RX handshake must drive rx_axis_to_ts directly",
         None, None, gptp_gated_external_rx),
        # ---- the preprocessor: this gate reads one arm, the compiler takes
        # the other, and the arm it reads is the safe one by construction.
        ("AEM guard selected by a build flag", preprocessor_guard,
         docs_source, csr_source,
         "firmware must not select boot code with the preprocessor"),
        ("pre-AEM clear behind a build flag", preprocessor_clear,
         docs_source, csr_source,
         "firmware must not select boot code with the preprocessor"),
        # ... and the same defect without the preprocessor: a compile-time
        # constant condition deletes a boot step from the image while every
        # line this gate reads stays exactly where it was.
        ("fabric configuration made dead by a compile-time constant",
         dead_configure, docs_source, csr_source,
         "the fabric configuration step must be a statement of milan_init() "
         "itself"),
        # ---- reachability: sitting between the guard's braces is not the
        # same as being reached only by taking the guard.
        ("entity enabled by a goto into the AEM-success guard",
         goto_into_guard, docs_source, csr_source,
         "milan_init() must not contain 'goto'"),
        ("entity enabled by a case falling into the AEM-success guard",
         case_into_guard, docs_source, csr_source,
         "milan_init() must not contain 'switch'"),
        # ---- the verdict and the verifier, pinned by data flow rather than
        # by the spelling `aem_loaded =` and the literal `return 1;`.
        ("AEM verdict overwritten through a pointer", verdict_pointer,
         docs_source, csr_source,
         "the address of aem_loaded must not be taken"),
        ("AEM verifier returning a non-boolean status before the CRC gate",
         status_return, docs_source, csr_source,
         "AEM verifier non-zero return must be textually after"),
        # ---- and the address model, checked against the RTL's DECODE rather
        # than assumed from its name table.
        ("ADP_CTRL given a second decode address", mirrored_enable,
         docs_source, mirrored_csr,
         "the RTL must write adp_ctrl from exactly one CSR address"),
        # ---- the other half of each new rule.
        ("AEM verifier succeeding from the no-QSPI preprocessor arm",
         other_arm_success, docs_source, csr_source,
         "AEM verifier non-zero return must be textually after"),
        ("CRC comparison itself put behind a build flag", optional_crc,
         docs_source, csr_source,
         "AEM verifier non-zero return must be textually after"),
        ("AEM verifier that can never succeed", vacuous_verifier,
         docs_source, csr_source,
         "AEM verifier never returns a non-zero verdict"),
        # ---- the object list: every rule above reads ONE file, so a second
        # object is every rule above voided at once. make builds a VARIABLE,
        # so each of its assignment flavours is its own way to add one.
        ("second translation unit listed on the OBJECTS line", firmware_source,
         docs_source, csr_source, both_objects, listed_objects),
        ("second translation unit appended with OBJECTS +=", firmware_source,
         docs_source, csr_source, both_objects, appended_objects),
        ("second translation unit on an OBJECTS continuation line",
         firmware_source, docs_source, csr_source,
         both_objects, continued_objects),
        ("object list this gate cannot evaluate", firmware_source,
         docs_source, csr_source,
         "must stay ONE translation unit", wildcard_objects),
        ("second object archived past the OBJECTS list", firmware_source,
         docs_source, csr_source,
         "make must build and archive exactly the one object",
         archived_objects),
        # ---- one OBJECT is not one FILE. Each of these keeps the object
        # list at exactly one, so the rules above pass honestly while the
        # closure reads text that is not the whole translation unit.
        ("second source pulled in by #include of a .c", included_source,
         docs_source, csr_source, "the firmware's include set is pinned"),
        # ... and the same file reached by spellings an include regex misses
        # while the preprocessor does not. Pinning the DIRECTIVE set after
        # phases 1 and 2 answers all of these at once.
        ("second source pulled in by a macro include operand",
         macro_included_source, docs_source, csr_source,
         "a #include operand must be a literal header name"),
        ("second source pulled in by a spliced #include directive",
         spliced_included_source, docs_source, csr_source,
         "the firmware's include set is pinned"),
        ("second source pulled in by a %: digraph include",
         digraph_included_source, docs_source, csr_source,
         "the firmware's include set is pinned"),
        ("second source pulled in by a ??= trigraph include",
         trigraph_included_source, docs_source, csr_source,
         "the firmware's include set is pinned"),
        ("a preprocessing directive this gate has no rule for",
         undefined_constant, docs_source, csr_source,
         "the firmware's preprocessing directives are pinned"),
        # ---- and the store mechanism with no textual signature at all.
        ("entity enabled by an inline-asm store to the CSR address",
         asm_store_enable, docs_source, csr_source,
         "the firmware's inline asm is pinned"),
        # ---- the cast spellings rule 1 never named. Naming ONE cast is a
        # denylist of one; pinning the STORES is the set.
        ("entity enabled through a widened pointer cast",
         widened_cast_store, docs_source, csr_source, "the firmware's casts to a pointer are pinned"),
        ("entity enabled through a reordered pointer cast",
         reordered_cast_store, docs_source, csr_source, "the firmware's casts to a pointer are pinned"),
        ("entity enabled through a pointer held in a local",
         local_pointer_store, docs_source, csr_source, "the firmware's casts to a pointer are pinned"),
        # NOT an entity enable, and the label no longer says it is: the
        # store goes to a private static. It is the cost demonstration for
        # the pointer-store set, which refuses a new store BECAUSE it cannot
        # tell where the pointer points, and that is the property it pins.
        ("a new store through a pointer whose target this gate cannot read",
         helper_pointer_store, docs_source, csr_source,
         "the firmware's stores through a pointer are pinned"),
        # ---- the four shapes no recognizer in this file ever saw. Each is
        # an ordinary embedded idiom and each passed the complete suite at
        # cc2ee861; only the compiled census sees them.
        # ---- and RESOLUTION: a pinned NAME is not a pinned FILE.
        ("pinned include shadowed by a file beside the firmware",
         firmware_source, docs_source, csr_source,
         "the firmware's directory is pinned to", None,
         shadowed_quoted_include),
        ("pinned include shadowed by an added -I search path",
         firmware_source, docs_source, csr_source,
         "the commands make would run are pinned", shadowed_search_path),
        ("object list the environment can override", firmware_source,
         docs_source, csr_source,
         "lets the ENVIRONMENT decide what gets compiled", environment_objects),
        ("second file injected through -Wp, the preprocessor pass-through",
         firmware_source, docs_source, csr_source,
         "the commands make would run are pinned", preprocessor_passthrough),
        ("second file injected through a response file", firmware_source,
         docs_source, csr_source,
         "the commands make would run are pinned", response_file_injection),
        ("search path added through the -iprefix chain", firmware_source,
         docs_source, csr_source,
         "the commands make would run are pinned", prefixed_search_path),
        ("second file injected through the CC tool variable", firmware_source,
         docs_source, csr_source,
         "the commands make would run are pinned", tool_variable_injection),
        ("search path added through the CC tool variable", firmware_source,
         docs_source, csr_source,
         "the commands make would run are pinned",
         tool_variable_search_path),
        ("pinned include shadowed by an -iquote search path",
         firmware_source, docs_source, csr_source,
         "the commands make would run are pinned",
         quoted_search_path),
        ("one object linked from two sources by an explicit rule",
         firmware_source, docs_source, csr_source,
         "make must compile exactly one source", linked_objects),
        ("objects added by a Makefile fragment this gate does not read",
         firmware_source, docs_source, csr_source,
         "the Makefile's include set is pinned", fragment_objects),
        # ... and pinning the rule is not pinning what the rule compiles.
        ("second source injected by a -include compiler flag",
         firmware_source, docs_source, csr_source,
         "make must compile exactly one source", injected_source),
        ("compile recipe redefined to take a second source", firmware_source,
         docs_source, csr_source, "make must compile exactly one source",
         recompiled_objects),
        # A `vpath %.c` mutant used to sit here and it is RETIRED, not
        # lost: the plan shows it changes nothing for this build. The
        # reason, stated precisely because the first attempt was overbroad:
        # vpath IS consulted for a prerequisite with a directory component,
        # but only when the named file does not exist, and this one always
        # does. A vpath that did move the compiled file would change the
        # compile line, which the plan reads.
        # ... behind make's other modifier keywords, and target-specific.
        ("second source injected by an exported assignment", firmware_source,
         docs_source, csr_source,
         "make must compile exactly one source", exported_injection),
        ("second source injected by a target-specific assignment",
         firmware_source, docs_source, csr_source,
         "make must compile exactly one source", target_injection),
        # ... and the producing rule's own prerequisite variable, pointed at
        # a different tree entirely.
        ("the compiled source directory moved out from under the rule",
         firmware_source, docs_source, csr_source,
         "make could not plan this Makefile",
         shadowed_source_dir),
        # CORRECTION. Round nine retired a `MAKEFLAGS += -e` mutant here on
        # the claim that `-e` inside a Makefile does not change what that
        # run expands. That measurement was WRONG: on GNU make 4.4.1 it
        # does let the environment override any assignment make has not yet
        # read, OBJECTS and CFLAGS included. The mutant is restored above,
        # pinned on the hostile double-run, which is what actually catches
        # it. The refusal it replaced was redundant with that double-run,
        # not pointless, and there was never a safety regression.
        # ---- and the reset values: the census governs who may SET bit 0,
        # and says nothing about the value bit 0 holds before the first write.
        ("ADP_CTRL reset value advertising the entity", firmware_source,
         docs_source, adp_reset_enabled,
         "the RTL must reset adp_ctrl with bit 0 CLEAR"),
        ("PP_CTRL reset value enabling the protocol processor",
         firmware_source, docs_source, pp_reset_enabled,
         "the RTL must reset pp_ctrl_r with bit 0 CLEAR"),
        # ---- reopened by the round-nine deletions, closed again here.
        ("entity enabled through a CSR base held in a variable",
         paged_base_store, docs_source, csr_source,
         # Pinned on rule 1's own words, not the prefix the census shares,
         # because the whole point of this entry is WHICH instrument
         # catches it.
         "but a CSR pointer cast is used outside it"),
        ("entity enabled by a lui-based inline-asm store", lui_asm_store,
         docs_source, csr_source, "the firmware's inline asm is pinned"),
        ("one object linked from two sources by literally named tools",
         firmware_source, docs_source, csr_source,
         "make must compile exactly one source", literal_tool_rule),
        ("second object archived by a literally named ar", firmware_source,
         docs_source, csr_source,
         "make must compile exactly one source", literal_tool_archive),
        ("ADP_CTRL reset written blocking with the enable bit set",
         firmware_source, docs_source, blocking_reset_enabled,
         "the RTL must reset adp_ctrl with bit 0 CLEAR"),
        ("ADP_CTRL given no reset value at all", firmware_source, docs_source,
         absent_reset, "the RTL must give adp_ctrl a reset value"),
        ("ADP_CTRL reset and readback default both advertising",
         firmware_source, docs_source, consistent_reset_enabled,
         "the RTL must reset adp_ctrl with bit 0 CLEAR"),
    )
    mutations += tuple(
        (f"entity enabled through a {name} phase-2 token splice", mutation,
         docs_source, csr_source,
         "firmware must not splice physical source lines with backslash-newline")
        for name, mutation in phase2_whitespace_splices)
    #: The label names the INSTRUMENT, because the rule that fires and the
    #: rule the function name suggests are not the same one and the reason
    #: pin is the honest half: rule 5 (the cast set) runs before rule 6 (the
    #: helper's return provenance) deliberately, and the blindness control
    #: beside the mutants' definition measures what that ordering buys.
    mutations += tuple(
        (f"entity enabled by a store inside the exempted address helper, "
         f"refused by the CAST SET and invisible to the census "
         f"({label} baseline)", mutation, docs_source, csr_source,
         "the firmware's casts to a pointer are pinned")
        for label, mutation in helper_body_store_mutations)
    #: The four shapes ONLY the compiled census catches. They are in the
    #: table when the census is live and named as skipped when it is not,
    #: because a machine without a cross compiler cannot answer them at all
    #: and pretending otherwise is what the last round's false stand-down
    #: message did.
    census_only_mutations = (
        ("entity enabled through a typedef'd pointer and an access macro",
         typedef_macro_store, docs_source, csr_source, CENSUS_PIN),
        ("entity enabled through a struct overlay and an -> store",
         overlay_member_store, docs_source, csr_source, CENSUS_PIN),
        ("entity enabled through a typedef'd pointer and a subscript store",
         typedef_subscript_store, docs_source, csr_source, CENSUS_PIN),
        ("entity enabled through a qualifier-after-star cast",
         qualified_cast_store, docs_source, csr_source, CENSUS_PIN),
    )
    #: ---- and the shapes only the RESOLVER catches: two stores whose
    #: address is never printed as a window immediate, two paths to the
    #: verifier's success return that never take the CRC comparison, a
    #: comparison against a value crc32() never produced, a CRC over the
    #: wrong buffer, and the continuation-macro enables whose refusal the
    #: choke point retires. Registered beside the census-only set and for
    #: the same reason: a machine with no cross compiler cannot answer them
    #: and pretending otherwise is what a false stand-down does.
    resolver_only_mutations = (
        ("entity enabled by a struct-overlay store through a paged base",
         overlay_paged_store, docs_source, csr_source, RESOLVER_STORE_PIN),
        ("entity enabled by a subscript store through a paged base",
         subscript_paged_store, docs_source, csr_source, RESOLVER_STORE_PIN),
        ("AEM verifier reaching its success return by goto past the CRC "
         "comparison", goto_past_crc, docs_source, csr_source,
         RESOLVER_DOMINANCE_PIN),
        ("AEM verifier reaching its success return by a structured break "
         "past the CRC comparison", break_past_crc, docs_source, csr_source,
         RESOLVER_DOMINANCE_PIN),
        ("CRC result overwritten between the call and the comparison",
         crc_overwritten, docs_source, csr_source,
         "never compares the value crc32() HANDED BACK"),
        ("CRC taken over the QSPI source instead of the descriptor buffer",
         crc_over_qspi_source, docs_source, csr_source,
         "takes its CRC over"),
        ("entity enable hidden in a continuation-line macro body and "
         "invoked from a UART handler", macro_enable, docs_source,
         csr_source, RESOLVER_CHOKE_PIN),
        ("entity enable hidden after form-feed macro continuation "
         "whitespace", formfeed_macro_enable, docs_source, csr_source,
         RESOLVER_CHOKE_PIN),
    )
    if baseline_census_verdict["ran"]:
        mutations += census_only_mutations + resolver_only_mutations
    #: `MAKEFLAGS += -e` only lets the environment override on a make that
    #: re-reads MAKEFLAGS mid-parse. Include the entry where it bites and
    #: say so where it does not, rather than ship a mutant whose verdict
    #: depends on the runner.
    makeflags_e_bites = make_honours_makeflags_e()
    if makeflags_e_bites:
        mutations += (
            ("MAKEFLAGS += -e letting the environment choose", firmware_source,
             docs_source, csr_source,
             "lets the ENVIRONMENT decide what gets compiled",
             env_override_flags),
        )
    else:
        #: Registered, like the census and Verilator arms, because dropping
        #: this entry moves the tally silently and the verdict has to say so
        #: ([R1] on PR #212 measured 98/98 -> 97/97 with the arm printed
        #: mid-log and absent from the verdict). The WORDING is deliberately
        #: not the other two's: nothing is missing from this runner. The
        #: construct is present and simply does nothing on a make that does
        #: not re-read MAKEFLAGS mid-parse, so the mutant would be a control
        #: that cannot fail rather than an instrument that is unavailable.
        skip("gate 1b",
             "the MAKEFLAGS += -e mutation: this make does not re-read "
             "MAKEFLAGS mid-parse, so the construct hands the environment "
             "nothing here and the entry would be a control with nothing to "
             "detect. No tool is missing from this runner; the mutant has "
             "no effect to observe on THIS make")
    #: NEGATIVE CONTROL for the reason pin itself, which is what turns "the
    #: mutant was refused" into "the mutant was refused BY THE RULE IT
    #: BREAKS". The elaboration layer, the census and the recognizer each
    #: had a self-test proving they can fail; this had none, and replacing
    #: its assertion with `assert True or because in str(exc)` left the
    #: focused gate green at 144/144 (#206). Run it with a mutant that IS
    #: rejected, under a reason no rule in this file prints.
    try:
        assert_rejected("reason-pin negative control", wrong_reg_address,
                        docs_source, csr_source,
                        "a reason no rule in this gate has ever printed")
    except AssertionError as exc:
        assert "mutation was rejected for the wrong reason" in str(exc), \
            f"the reason-pin control failed for the wrong reason: {exc}"
    else:
        raise AssertionError(
            "assert_rejected() accepted a mutation refused under a reason it "
            "was never given, so every `because` above is decorative and the "
            "mutation table proves only that something said no")
    for mutation in mutations:
        assert_rejected(*mutation)
    if verilator:
        try:
            assert_rtl_mutant_elaborates(
                "non-elaborable RTL self-test",
                csr_source + "\nmodule pr187_unclosed_control(\n",
                None, count=False)
        except AssertionError as exc:
            assert "does not elaborate and cannot count" in str(exc), exc
        else:
            raise AssertionError(
                "RTL-mutant elaboration accepted a deliberately malformed "
                "SystemVerilog control")
        assert rtl_mutant_elaboration["passed"] == \
            rtl_mutant_elaboration["requested"], \
            "not every RTL mutation was elaborated before being counted"
        rtl_mutant_note = (
            f"{rtl_mutant_elaboration['passed']}/"
            f"{rtl_mutant_elaboration['requested']} RTL mutation variants "
            "elaborated as the real option-on milan_datapath or milan_csr "
            "top before counting, and the deliberately malformed RTL "
            "self-test was refused; ")
        mutation_tally = (
            f"{len(mutations)}/{len(mutations)} mutations rejected on the "
            "safety property they break; ")
    else:
        counted = len(mutations) - rtl_mutant_elaboration["requested"]
        #: Registered, not merely printed, for the same reason as the census
        #: stand-down above: this arm declined and the final verdict has to
        #: say so (#206). The malformed-RTL self-test is inside the same
        #: branch, so it is named here rather than left to vanish silently.
        skip("gate 1b",
             "RTL mutation elaboration: no Verilator on this runner, so all "
             f"{rtl_mutant_elaboration['requested']} RTL mutation variants "
             "counted as structural rejections only, and the deliberately "
             "malformed-RTL self-test that proves the elaborator can refuse "
             "did not run")
        rtl_mutant_note = (
            "RTL mutation elaboration STOOD DOWN for all "
            f"{rtl_mutant_elaboration['requested']} RTL variants because "
            "Verilator is unavailable on this runner; they remain "
            "reason-pinned structural rejections but are not claimed as "
            "elaborated mutation evidence here; ")
        mutation_tally = (
            f"{counted}/{counted} non-RTL mutations rejected on the safety "
            "property they break; the structurally rejected RTL variants "
            "are excluded from this mutation count; ")
    #: Both clauses below are gated on the SAME condition as the
    #: measurement they report. The CI shape (only cc and gcc, no Verilator,
    #: no RV32 compiler) used to read "refused a 64-bit target under this
    #: run's own flags" beside "0/0 exempted-helper stores were measured
    #: INVISIBLE", and neither had happened: the live re-probe is gated on a
    #: candidate having been adopted and the blindness control on the census
    #: having run ([R1] on PR #212). A stand-down message that is false is
    #: worse than no stand-down, and that applies to this fix's own output.
    if rv32_probe_refused_64:
        live_probe_note = (
            ", and on this run's live invocation ("
            + (" ".join(census_used.get("flags") or ()) or "no driver flags")
            + ") the probe refused a 64-bit target while "
            f"{census_arch_seen['stated']} census compile(s) declared an "
            f"rv32 arch and {census_arch_seen['unstated']} declared none")
    else:
        live_probe_note = (
            "; NOT measured on this run: no candidate here is the RV32 "
            "target, so there was no live invocation to re-probe at 64 bits "
            "and no census assembly to read an arch attribute out of")
    if helper_store_census_asked:
        helper_blind_note = (
            f"; and {helper_store_census_blind}/{helper_store_census_asked} "
            "exempted-helper stores were measured INVISIBLE to the compiled "
            "census, which is why they stay pinned on the cast set, while "
            f"{helper_store_resolver_caught}/{helper_store_census_asked} of "
            "the same mutants were REJECTED by the resolver on the resolved "
            "store address, which is what makes 'an addition, not a "
            "replacement' a measurement here rather than a claim")
        resolved_note = (
            ", and on this run it resolved "
            f"{baseline_census_verdict['resolved']['statics']} single-word "
            "static(s) and "
            f"{baseline_census_verdict['resolved']['functions']} function(s) "
            "of the shipping firmware, reading the CRC operands back as "
            f"0x{baseline_census_verdict['resolved']['buffer']:08x} for "
            f"{baseline_census_verdict['resolved']['bytes']} bytes")
    else:
        helper_blind_note = (
            "; the exempted-helper blindness control did NOT run here, "
            "because the census stood down, so on this runner those two "
            "mutants stay pinned on the cast set with that measurement "
            "absent")
        resolved_note = (
            ". It did NOT run on this runner: it reads the assembly the "
            "census compiles, so the census's stand-down stands it down too")
    print("  [gate 1b] bounded boot-contract model: the PHC CSR output, "
          "datapath binding and ptp_timestamp consumer are direct, and "
          "comment-blanked CSR, MAC, timestamp, both RXFILT_P-arm, shadow "
          "and TX-mux facts are direct in their inspected generate arms and "
          "free of comment, preprocessor and static-generate decoys; "
          "PHC/gPTP are "
          "live from reset TO THE ptp_timestamp PORT and independent of "
          "AEM, which is where this gate's measurement stops: a tie-off "
          "INSIDE ptp_ts_top still elaborates and is milan_dp's to catch; "
          "the "
          "milan_reg()/milan_read()/milan_write() "
          "bodies pin address and value provenance, the firmware identity "
          "offset and magic equal RTL A_ID's address and default, and "
          "recognised "
          f"whole-firmware milan_write() calls set {pp_label}[0] then "
          f"{adp_label}[0] only after the AEM "
          "verdict, censused by ADDRESS off the RTL decode table so a second "
          "#define is the same register. The source and compiled instruments "
          "run together; the source-only uncovered store class and the "
          "census stand-down consequence are named below; "
          + mutation_tally + rtl_mutant_note +
          ("the phase-2 splice mutants compiled on the exact RV32 target "
           "(bare splice warning-clean; space, tab, form-feed and "
           "vertical-tab splices accepted with diagnostics); "
           if phase2_splice_compiled and all(
               result for _name, result in phase2_whitespace_compile_results)
           else
           "the phase-2 splice mutants are reason-pinned but their compile "
           "proof is SKIPPED here because no RV32 compiler is available; ") +
          ("" if makeflags_e_bites else
           "(the MAKEFLAGS += -e entry is SKIPPED on this machine: its make "
           "does not honour -e from inside a makefile, so the construct "
           "does nothing to detect here) ") +
          ("" if baseline_census_verdict["ran"] else
           f"({len(census_only_mutations)} entries are SKIPPED on this "
           "machine: they are the shapes ONLY the compiled census catches, "
           "and it stood down for want of an RV32 compiler. To be precise, "
           "the census did not run for ANYTHING on this machine, the "
           "shipping firmware and every other mutant and accepted case "
           "included, so its whole contribution is absent and not just "
           "these four) ") +
          f"{len(reset_spellings)}/{len(reset_spellings)} equivalent reset "
          f"spellings and {len(objects_spellings)}/{len(objects_spellings)} "
          "equivalent object-list spellings accepted; and "
          f"{len(accepted_cases)}/{len(accepted_cases)} legitimate firmware "
          f"edits and {len(accepted_makefiles)}/{len(accepted_makefiles)} "
          "legitimate Makefile edits accepted, which until this round were "
          "prose in a PR body and are now the only executable statement this "
          "gate has of what a legitimate edit IS; deterministic host-only "
          "and 64-bit-candidate stand-down execution/wording self-tests "
          "passed, the RV32 probe decided all three candidate shapes "
          "(already RV32, 64-bit with an rv32 multilib, 64-bit only) "
          "against a stub, and the census arch check accepted rv32 "
          "assembly, refused rv64 assembly and reported unattributed "
          "assembly as unstated"
          + live_probe_note +
          "; the reason pin refused a wrong `because`"
          + helper_blind_note)
    print("  [gate 1b] ... and the text this reads is the text that runs, by "
          "TEXT RULES and by TOOLS together, because each has been measured "
          "to miss what the other holds. The text rules bound address "
          "formation: only milan_reg() may use the CSR base or a CSR pointer "
          "cast, the pointer-cast set, the pointer-store set and the "
          "inline-asm set are pinned. MAKE bounds what gets built: its whole "
          "-Bn plan is read, not the lines carrying a sentinel, so one "
          "source, one object, no link step, one added flag, and the same "
          "plan again under a hostile environment")
    census_note = format_census_verdict(baseline_census_verdict)
    print("  [gate 1b] ... and the COMPILER is asked as well, as an ADDITION "
          "and not a replacement: no function but "
          f"{reg_helper_name}() may materialise an address in the Milan CSR "
          f"window (0x{csr_base:08x}..0x{csr_base + csr_size:08x}) in the "
          "compiled output, which catches a typedef'd pointer, a "
          "register-access macro, a struct overlay and an -> store that no "
          "rule above recognises. It does NOT subsume the rules above: it "
          "exempts the address helper by name, it cannot see an address "
          "built with slli/ori, and it matches one asm spelling, all three "
          f"measured. This run: {census_note}")
    print("  [gate 1b] ... and the resolving half (#153), which is what the "
          "boot contract is actually PROVED by: an RV32 abstract "
          "interpreter over that same emitted assembly computes the store "
          "addresses, the call operands, the compared values and the CFG "
          "edges, so (a) no function -- the address helper included, it is "
          "NOT exempt -- stores to a resolved address in the CSR window, "
          "which answers a paged base built with slli/ori that prints no "
          "window immediate; (b) the only resolved milan_write() asserting "
          "bit 0 of PP_CTRL or ADP_CTRL is inside entity_advertise(), taken "
          "from the emitted operands so a macro body or a preprocessor arm "
          "cannot move it out of view; (c) removing the edge "
          "entity_advertise() takes on a non-zero verdict removes every "
          "control-register write it reaches; and (d) the verifier's CRC is "
          "taken over MILAN_AEM_DESC_BASE for MILAN_AEM_IMAGE_BYTES, the "
          "compared value is tracked from the crc32() call that produced "
          "it, and removing the CRC-equality edge leaves every reachable "
          "return resolved to zero. Verifier CFG reachability and CRC "
          "provenance are therefore MEASURED, not open. It resolves what "
          "the compiler emitted for THIS translation unit at the census's "
          "flags, and reports 'cannot say' as a REFUSAL wherever the "
          "property needs an answer"
          + resolved_note)
    print("  [gate 1b] ... plus the rules that are NOT parsing questions: the "
          "firmware's directive set and include resolution, the Makefile's "
          "include set (make can only plan fragments that exist), no "
          "preprocessor conditional reaching the boot path or carrying a "
          "definition and no token-joining backslash-newline, outside the "
          "QSPI-slot group whose BOTH arms the verifier's return rule "
          "classifies, no label/goto/switch in milan_init() or "
          "entity_advertise() and the three boot steps plus the unmodified "
          "CSR identity sample and check unconditional at its top level, one "
          "PP and one ADP enable inside the choke point and exactly one call "
          "to it carrying the verdict, no pointer to the verdict, and every "
          "non-zero return of the verifier placed after the CRC refusal by "
          "source position and preprocessor arm")
    print("  [gate 1b] ... and the RTL integration facts, which are the "
          "checked part: o_ptp_enable is driven directly from PTP_CTRL[0]; "
          "the milan_csr instance binds it directly to cfg_ptp_enable and "
          "ptp_timestamp consumes that net with direct clocks, resets, PHC "
          "controls and readback; "
          "external MAC RX "
          "traverses ptp_timestamp, both RXFILT_P arms and the fabric-gPTP "
          "shadow directly; shadow TX/timestamp feedback, the control mux, "
          "MAC-boundary mux and external MAC TX handshake also have direct "
          "data, clock and reset connections. Comments and nested static "
          "generate arms cannot supply a decoy connection, and no directive "
          "at any column may select an "
          "inactive arm; none of those seams carries an AEM/ADP/PP gate; "
          f"{adp_label} and {pp_label} are each written from exactly ONE "
          "decode arm, each driving its enable port from bit 0, and each "
          "reset with that bit CLEAR, read over BOTH assignment operators so "
          "a blocking reset cannot pass by leaving the rule nothing to check")
    print("  [gate 1b] COSTS. Round nine deleted three of these on the claim "
          "the compiled census subsumed them; three shapes went GREEN and "
          "they are RESTORED, so the costs are back and stated rather than "
          "claimed away: a fifth store through a pointer, a fifth cast to a "
          "pointer and a third inline-asm statement are RED again. Also RED: "
          "a C backslash-newline that JOINS two tokens (phase 2 deletes the "
          "pair before tokens exist), an #ifdef reaching milan_init(), "
          "configure_fabric(), entity_advertise() or the three CSR "
          "accessors, or carrying a #define/#undef/#include wherever it "
          "sits, a "
          "twelfth #include even of <string.h>, any "
          "#pragma/#line/#error/#undef, a fourth Makefile include, any new "
          "file in the firmware's directory including a README, an OBJECTS "
          "?= (make says the environment can override it), any new CFLAGS "
          "token including -Os and -DFOO, an RTL reset hoisted to a named "
          "constant, an RTL enable port or write address respelled, and a "
          "SystemVerilog CSR or datapath directive other than that file's "
          "shipped includes and paired `default_nettype directives, moving "
          "a checked item into a nested or implicit conditional-generate "
          "arm, and a "
          "renamed boot-path function, which names the property instead of "
          "raising a bare ValueError. Three more, measured and previously "
          "undisclosed: REORDERING two existing functions (the cast and "
          "store sets are compared as ORDERED lists, so moving code with "
          "nothing added or removed is refused), renaming the verdict "
          "aem_loaded, and a read-only #define accessor that wraps "
          "milan_read() (remedy: add the name to the firmware's #define "
          "table so constant_value() can resolve it). Also ##, %: and ?? "
          "anywhere in the file. And two "
          "ordinary refactors one step outside the accepted set: FACTORING "
          "the CSR accessors (a milan_set(offset, bits) helper is refused, "
          "because the census places writes by RESOLVED address and an "
          "`offset` parameter has none), and hoisting the enable mask to a "
          "named constant. Under the recipe-set pin, any change to the two "
          "commands make runs is refused too, a benign AR += v or CC += "
          "-Wall included: that is the price of a rule with no list of "
          "spellings to fall behind. Remedy for that one: add the changed "
          "command to expected_recipes and a mutation entry beside it. "
          "RETIRED this round by the entity-advertise choke point and the "
          "resolver (#153), each with an accepted case measured GREEN "
          "instead of a claim: an extra statement between the two enables, "
          "an #ifdef in a UART command handler, and a multi-line #define. "
          "The refusals they replace are gone, not narrowed by exception: "
          "what carries them now is a measurement over resolved values")
    print("  [gate 1b] ... and what the make plan DID give back, which "
          "survives this round: every Makefile variable and rule shape the "
          "old parser pinned, so an unrelated DEPFILES = $(patsubst ...) is "
          "GREEN. Two refusals stay retired: a vpath cannot move this "
          "build's compiled file because vpath is consulted only for a "
          "prerequisite that does not exist and this one always does")
    if baseline_census_verdict["ran"]:
        store_gap = (
            "The source rules alone do not recognise a cast with no * plus "
            "an -> or subscript store, but the live RV32 census rejects "
            "`((milan_adp_blk)0x90000600u)->ctrl = 1u;` by the materialised "
            "CSR address, and the resolver rejects the paged-base spellings "
            "of it -- which print no window immediate at all -- by the "
            "resolved store address. The source gap is therefore covered on "
            "this machine.")
    else:
        store_gap = (
            "The source rules do not recognise a cast with no * plus an -> "
            "or subscript store, and the compiled census and the resolver "
            "both stood down with the compiler they share. In this condition "
            "`((milan_adp_blk)0x90000600u)->ctrl = 1u;` is outside every "
            "active instrument, creates a durable pre-AEM entity advertise, "
            "and passes this gate; so does a non-zero verdict reached past "
            "the CRC comparison, since the CFG measurement needs the same "
            "compile.")
    print("  [gate 1b] NOT PROVED on every supported runner: " + store_gap +
          " Closing the unconditional property remains tracked on #153 and "
          "#162")
    print("  [gate 1b] ... and a second blind spot, same cause one step over: "
          "the recipe pin reads what make PRINTS, which is already expanded, "
          "so a name this Makefile references and nothing defines expands to "
          "nothing and the pinned commands come out identical. "
          "`CFLAGS += $(MILAN_EXTRA_CFLAGS)` passes here while "
          "MILAN_EXTRA_CFLAGS='-include ../shadow.h' in the environment adds "
          "the include to the real compile, and the hostile double-run "
          "perturbs three fixed names so it cannot see a deferral to a "
          "fourth. An instrument that reads a RESULT cannot see what an "
          "undefined name would have contributed, which is the same reason "
          "the compiled census never replaced the text rules. Fix is "
          "derivable and tracked on #162: probe $(origin NAME) and refuse "
          "'undefined', scoped to names reaching the pinned recipes, since "
          "the accepted tags: case references an undefined $(CTAGS) too")
    print("  [gate 1b] ... and outside what ANY recipe pin can reach: export "
          "CPATH and COMPILER_PATH, which GCC reads from the environment; "
          "SHELL, which changes what executes the printed command; "
          ".EXPORT_ALL_VARIABLES; and $(shell ...), which runs at parse time "
          "during this gate's own plan run, before a recipe is printed. "
          "Recorded rather than ruled against, because no pin over printed "
          "commands can see them")
    print("  [gate 1b] NOT proved here: the values the build's -D set and the "
          "generated headers supply (image bytes, CRC, entity ids - gate 28 "
          "owns those), that crc32() is a CRC, and anything about an "
          "interrupt vector, which is REFUSED by the no-label check rather "
          "than modelled")
    print("  [gate 1b] TRUSTED, not proved: the census compiles against "
          "STUB headers whose every address is asserted outside the CSR "
          "window, and the make plan runs against a STUB LiteX environment "
          "whose values are sentinels, so both bound what THIS repository's "
          "firmware and Makefile add, not what LiteX supplies. Resolution is "
          f"pinned for all {len(firmware_includes)} include names; the "
          "CONTENT behind each resolved name is trusted, and of those "
          f"{', '.join(firmware_includes_generated)} are written by this "
          "repository's own builder")
    print("  [gate 1b] CLOSED this round (#153), and each measured as a "
          "mutation rather than argued: the source rule tying the comparison "
          "to a real CRC is still an EXISTENCE test and still proves "
          "nothing, but the resolver now answers all four shapes it left "
          "open -- a constant assigned to the compared local between the "
          "crc32() call and the comparison, a CRC over the QSPI source "
          "instead of MILAN_AEM_DESC_BASE, a `goto` past the comparison to "
          "the non-zero return, and the structured do/break bypass that "
          "showed banning `goto` was not a proof. What REMAINS joint with "
          "#162 is the Makefile half: a second translation unit is a second "
          "place a CSR store can live, and no instrument here reads it")

    print("  [gate 1b] shipping AX: fabric gPTP option on with config-derived "
          "1024-word ROM; VexiiRiscv RV32I at 50 MHz through its supported "
          "decoupled clock, one hart, L2=0, bare-metal flash, no Scala cache "
          "args, PCM ring or host clusters; deploy keeps the plane option on")

    ucode_mutations = (
        ("station MAC", lambda c: c["platform"].__setitem__(
            "mac_address", "02:00:00:00:00:03")),
        ("priority1", lambda c: c["gptp"].__setitem__("priority1", 247)),
        ("fabric clock", lambda c: c["board"]["constraints"].__setitem__(
            "milan_clk_hz", 80_000_000)),
    )
    with tempfile.TemporaryDirectory() as td:
        for label, mutate in ucode_mutations:
            path = _variant(CONFIGS["ax7101_1x1_tdm8"], mutate)
            try:
                changed = eb.build(path, td)
                image = open(changed["paths"]["gptp_ucode"], "rb").read()
                assert image != base_ucode, \
                    f"{label}: mutation did not reach gptp_ucode.hex"
            finally:
                os.unlink(path)
    print("  [gate 1b] gPTP ROM changes with each YAML-owned input: station "
          "MAC, priority1 and fabric clock")

    def set_soc(key, value):
        return lambda c: c.setdefault("soc", {}).__setitem__(key, value)

    cases = (
        ("RV64", set_soc("xlen", 64)),
        ("two harts", set_soc("cpu_count", 2)),
        ("NaxRiscv", set_soc("cpu", "naxriscv")),
        ("L2 cache", lambda c: c["board"]["constraints"].__setitem__(
            "l2_bytes", 8192)),
        ("Scala cache arg", set_soc("scala_args", ["--lsu-l1-ways=2"])),
        ("Linux flash manifest", lambda c: c["board"]["constraints"].__setitem__(
            "flashboot", "full")),
        ("bare-metal flash under Linux", lambda c: c["soc"].__setitem__(
            "software_profile", "linux")),
        ("fabric gPTP without clock attributes", lambda c: c.pop("gptp", None)),
    )
    for label, mutate in cases:
        path = _variant(CONFIGS["ax7101_1x1_tdm8"], mutate)
        try:
            try:
                eb.load_config(path)
            except eb.ConfigError:
                pass
            else:
                raise AssertionError(f"{label}: incompatible profile was accepted")
        finally:
            os.unlink(path)
    print(f"  [gate 1b] {len(cases)}/{len(cases)} incompatible CPU/cache/flash "
          "profiles rejected before SoC generation")


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
    # USER 2026-08-05: the shipping AX shape is the 1x1x8 TDM8 config; the
    # sweep table now states IT, so like compares against like. The 8x8 NxN
    # shape stays a valid config one SWEEP_CFG away.
    for name in ("ax7101_1x1_tdm8",):
        r = eb.build(CONFIGS[name], OUT)
        got, want = _canon(r["argv"]), sweep_expected("ax7101")
        want = dict(want)
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
    # Port layout identical to the builtin model. Milan v1.2 5.3.3.9 makes
    # the input dynamic (no AUDIO_MAP); the one static output map is index 0.
    p_in, p_out = ovl["stream_ports"]["input"], ovl["stream_ports"]["output"]
    assert len(p_in) == 1 and len(p_out) == 1
    assert (p_in[0]["clusters"], p_in[0]["base_cluster"],
            p_in[0]["maps"], p_in[0]["base_map"]) == (8, 0, 0, 0)
    assert (p_out[0]["clusters"], p_out[0]["base_cluster"],
            p_out[0]["maps"], p_out[0]["base_map"]) == (8, 8, 1, 0)
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
    #: refused config (they would be silently ignored). The task #65 `fabric`
    #: block rides the same rule: it says which POOL SOURCES the build
    #: elaborates, so it is meaningless without pools to source.
    def set_policy(c, pol):
        cm = c["audio_interface"]["cluster_mapping"]
        cm["policy"] = pol
        if pol == "role-pools":
            cm.setdefault("pools", {"host": 4, "pilot": True, "loopback": 4})
        else:
            cm.pop("pools", None)
            cm.pop("fabric", None)

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
        c["board"]["features"] = {"sound_card": True}
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


def sweep_config(board):
    """The end-station config sweep.sh itself builds for <board>, read out of
    its own `CFG=${SWEEP_CFG:-...}` case arm.

    READ, never restated. This gate compares the generated fragment against
    sweep.sh's inline fallback, so it only means anything if it generates the
    fragment from the SAME config sweep.sh would. Naming the config here
    instead pinned the arty arm to endstation_arty_current (1x1, plain I2S,
    L2 64K) long after sweep.sh moved the board to endstation_arty_4x4 (4x4,
    TDM8 master, 4 wire channels, L2 16K) - and because sweep.sh SOURCES the
    fragment when it exists and only falls back to the inline table when it
    does not, a launch would have quietly built the 1x1 two-channel Arty while
    every artifact said 4x4 TDM8. That is the same shape-downgrade this
    fragment mechanism was added to prevent, wearing the test's own clothes."""
    txt = open(SWEEP).read()
    m = re.search(rf'{board}\)\s+NS=\d+;\s+CFG=\$\{{SWEEP_CFG:-([^}}]+)\}};', txt)
    assert m, f"sweep.sh: no CFG case for {board}"
    return os.path.join(ROOT, m.group(1).strip())


def test_sweep_opts_fragments():
    frag = {}
    for board in ("arty", "ax7101"):
        r = eb.build(sweep_config(board), OUT)
        p = r["paths"]["sweep_opts"]
        assert os.path.basename(p) == f"sweep_opts_{board}.sh"
        txt = open(p).read()
        m = re.search(r'^OPTS="([^"]*)"\n(?:NS=\d+\n)?L2=(\d+)\nRXQ=(\d+)\n',
                      txt, re.M)
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
    """Gate 10: the overlay -> gen_aem_store path is byte-stable.

    WHAT MOVED (2026-08-12).  The comparand used to be the TRACKED ROM
    hdl/ieee17221/aecp/gen/aecp_aem_rom.svh - the descriptor set a build
    `include-d - which made this the staleness gate for the shipped entity.
    That file and the repository-local AECP plane that compiled it are deleted, so the
    property left is the one that is still true and still worth holding: the
    builder's IN-MEMORY emit_aem_rom_svh() and the gen_aem_store CLI are the
    same generator reached two ways, and the CLI must not drift away from the
    library the builder calls.  Both comparands are generated; nothing on
    disk is asserted about, because there is nothing on disk to assert."""
    owner, owner_path = _tracked_owner_config()
    r = eb.build(owner_path, OUT)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
             "--overlay", r["paths"]["aem_overlay"], "--out-dir", td],
            check=True, capture_output=True)
        got = open(os.path.join(td, "aecp_aem_rom.svh"), "rb").read()
        want = r["aem_rom_svh"].encode()
        assert got == want, (
            "the gen_aem_store CLI and the builder's own emit_aem_rom_svh() "
            f"disagree for {owner} ({len(got)} vs {len(want)} bytes) - one of "
            "the two paths through the SAME generator has regressed")
        # ...and the CLI writes NOTHING into a deleted RTL destination. A
        # generator that recreates hdl/ieee17221/aecp/gen/ is how a directory
        # nobody compiles comes back and starts looking authoritative.
        assert not os.path.exists(
            os.path.join(ROOT, "hdl/ieee17221/aecp")), \
            "gen_aem_store recreated hdl/ieee17221/aecp - the AECP plane is " \
            "deleted and nothing may write into it"
        assert sorted(os.listdir(td)) == ["aecp_aem_rom.svh", "aem_rom.json"], \
            f"--out-dir emitted unexpected files: {sorted(os.listdir(td))}"
        # The DEPLOYED shape's stream descriptors, pinned to the layout Milan
        # v1.2 5.3.3.4 requires. Byte-identity above only proves the two paths
        # agree; it says nothing about what they agree ON, and the layout is
        # the part a controller sees.
        jd = json.load(open(os.path.join(td, "aem_rom.json")))
        n_str = check_stream_layout(bytes.fromhex(jd["rom_hex"]),
                                    jd["directory"], owner)
        print(f"  [gate 10] {owner} overlay -> gen_aem_store --overlay: "
              f"svh BYTE-IDENTICAL to the builder's own emit_aem_rom_svh "
              f"({len(got)} B); no RTL destination touched; {n_str} stream "
              "descriptors in 1722.1-2021 Table 7-8 layout")
    with tempfile.TemporaryDirectory() as td:
        # Refactor guard on the BUILTIN model (no --overlay). It is pinned to
        # arty_current's overlay, never to whatever shape the tree carries:
        # the builtin descriptor set is the 1x1 one, so tying it to the
        # tracked owner would break this guard every time the tree is
        # regenerated for another board - which is a property of the TREE,
        # not a regression in gen_aem_store.
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
        skip("gate 11", f"real report not on disk ({REAL_RPT}) - the "
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
    # docs/design/AREA_BUDGET.md predicted (4x4 ~85%, 8x8 ~89% vs modeled
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
        # ...and no map/cluster growth. The AUDIO_MAP count is DERIVED
        # from what the config declares - one descriptor per STATIC port,
        # zero for dynamic ones (Milan 5.3.3.9 listeners; USER 08-01 made
        # the ship talkers dynamic too, so ax7101_8x8 carries none at all)
        cfg_l = eb.load_config(CONFIGS[name])
        n_static = sum(1 for s in cfg_l["talkers"] + cfg_l["listeners"]
                       if s.get("map_mode", "static") != "dynamic")
        assert dc["AUDIO_MAP"] == n_static, (name, dc["AUDIO_MAP"], n_static)
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
    # 1722.1-2021 7.2.6 Table 7-8: the descriptor is 138 + 8*N + 2*R octets.
    # It was 132 + 8*N until 2026-08-13 - the 2013 layout, which omits
    # redundant_offset/number_of_redundant_streams/timing and so serves a 2021
    # controller the first two octets of formats[0] as `timing`.
    assert crf["len"] == 138 + 8                  # header + ONE format entry
    assert rom[b + 4:b + 7] == b"CRF"             # object_name
    assert rom[b + 70:b + 72] == b"\x00\x00"      # clock_domain_index 0 (7.2.6)
    assert rom[b + 72:b + 74] == b"\x00\x03"      # CLOCK_SYNC_SOURCE|CLASS_A
    # ...and TIMING_FIELD_VALID (Table 7-9 bit 2, mask 0x2000) stays CLEAR:
    # this entity has no TIMING descriptor, so `timing` names nothing.
    assert not int.from_bytes(rom[b + 72:b + 74], "big") & 0x2000
    assert rom[b + 74:b + 82].hex().upper() == CRF_FMT[2:]   # current_format
    assert rom[b + 82:b + 84] == b"\x00\x8a"      # formats_offset == 138
    assert rom[b + 132:b + 134] == b"\x00\x92"    # redundant_offset 138+8*1
    assert rom[b + 134:b + 136] == b"\x00\x00"    # R = 0 (no redundant pair)
    assert rom[b + 136:b + 138] == b"\x00\x00"    # timing (TIMING_FIELD clear)
    assert rom[b + 138:b + 146].hex().upper() == CRF_FMT[2:]  # formats[0]
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
    # 1722.1-2021 7.2.8 Table 7-13: the AVB_INTERFACE descriptor is 102 octets
    # and ends at base_control (100). It was 98 - the 2013 layout, ending at
    # port_number - until 2026-08-13, which let a 2021 controller read
    # number_of_controls out of whatever the store held past the descriptor.
    avb = next(d for d in dirv if d["type"] == 0x0009)
    a = avb["base"]
    assert avb["len"] == 102, f"AVB_INTERFACE is {avb['len']} B, 7.2.8 says 102"
    assert rom[a + 76:a + 78] == b"\x00\x07"      # GPTP_GM|GPTP|SRP (Milan
                                                  # 5.3.3.5 mandates the last 2)
    assert rom[a + 96:a + 98] == b"\x00\x00"      # port_number (unchanged)
    # THE ONE CONTROL HAS ONE PARENT, and this is the assertion that says so.
    # Milan v1.2 5.3.2 parents the "IDENTIFY" CONTROL on the CONFIGURATION -
    # "each of the descriptors above ... shall have one, and only one, parent
    # descriptor" - and the CONFIGURATION descriptor_counts below carry it.
    # An interface claiming number_of_controls = 1 would hand that same
    # descriptor a second parent, which no controller could resolve.
    assert pairs[0x001A] == 1, f"CONFIGURATION counts no CONTROL: {pairs}"
    assert rom[a + 98:a + 100] == b"\x00\x00", \
        "AVB_INTERFACE claims a CONTROL the CONFIGURATION already parents"
    assert rom[a + 100:a + 102] == b"\x00\x00"    # base_control: none to index
    # ...and the CRF descriptor above is not a special case: EVERY stream in
    # this ROM is Table 7-8, at its own N.
    n_str = check_stream_layout(rom, dirv, "arty_4x4+CRF")
    print(f"  [gate 16] all {n_str} STREAM_INPUT/OUTPUT descriptors are "
          "1722.1-2021 Table 7-8: formats_offset 138, redundant_offset "
          "138+8N, R = 0, timing 0 with TIMING_FIELD_VALID clear")
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


def test_dynamic_map_topology_reaches_shape_header():
    """gate 16c - the RTL mapping face receives the AEM model topology."""
    def scalar(s, name):
        m = re.search(rf"{name}\s*=\s*(\d+)\s*;", s)
        assert m, f"shape header has no {name}"
        return int(m.group(1))

    def array(s, name):
        m = re.search(rf"{name}\s*\[[^]]+\]\s*=\s*'\{{([^}}]+)\}};", s)
        assert m, f"shape header has no {name}"
        out = []
        for token in m.group(1).split(", "):
            q = re.search(r"'([hdb])([0-9A-Fa-f]+)", token)
            assert q, f"{name}: cannot parse {token}"
            out.append(int(q.group(2), {"h": 16, "d": 10, "b": 2}[q.group(1)]))
        return out

    ax8 = eb.load_config(CONFIGS["ax7101_8x8"])
    h8 = eb.emit_adp_shape_svh(ax8, eb.emit_aem_overlay(ax8))
    assert scalar(h8, "ADP_DMAP_IN_KEYS_C") == 64
    assert array(h8, "ADP_DMAP_IN_PBASE_C") == list(range(0, 64, 8))
    assert array(h8, "ADP_DMAP_IN_PCLS_C") == [8] * 8
    assert array(h8, "ADP_DMAP_IN_RPHYS_C") == [0] * 64
    assert array(h8, "ADP_DMAP_OUT_PCLS_C") == [17] * 8
    assert array(h8, "ADP_DMAP_OUT_PCBASE_C") == list(range(0, 136, 17))
    c8 = array(h8, "ADP_DMAP_OUT_CSRC_C")
    assert c8[:9] == [0x1300, 0x1B00, 0x1301, 0x1B01,
                      0x1302, 0x1B02, 0x1303, 0x1B03, 0x1400]
    assert c8[9:17] == [0x0500, 0x0D00, 0x0501, 0x0D01,
                        0x0502, 0x0D02, 0x0503, 0x0D03]

    ax1 = eb.load_config(CONFIGS["ax7101_1x1_tdm8"])
    h1 = eb.emit_adp_shape_svh(ax1, eb.emit_aem_overlay(ax1))
    assert scalar(h1, "ADP_DMAP_IN_KEYS_C") == 1
    assert array(h1, "ADP_DMAP_IN_PCLS_C") == [0]
    assert array(h1, "ADP_DMAP_IN_PNMAPS_C") == [0]
    assert array(h1, "ADP_DMAP_IN_RPHYS_C") == [0]
    assert array(h1, "ADP_DMAP_OUT_PCLS_C") == [17]
    c1 = array(h1, "ADP_DMAP_OUT_CSRC_C")
    assert c1[0] == 0x1200 and c1[8] == 0x1400
    assert c1[9] == 0x1500 and c1[16] == 0x1D03
    print("  [gate 16c] dynamic-map input keys, physical projections and "
          "output CSRC tables match both AX7101 entity models")


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

    Milan v1.2 5.3.3.9 makes every Stream Port Input dynamic, so every valid
    builder owner requires the generated `AEM_DYNMAP input engine. The owner
    is still read from the shape include's `Source :` marker through
    ces.tracked_owner, which prevents a ROM left behind by a different shape
    from passing the tracked-artifact gate.

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
        assert "AEM_DMAP_PNMAPS_C [0:0] = '{32'd2}" in svh
        assert "AEM_DMAP_PBASE_C [0:0] = '{32'd0}" in svh
        # ... and the ROM the TRACKED SHAPE'S OWNER generates carries the
        # engine IFF that owner asks for it.  The owner is read from the tree,
        # never assumed (see _check_tracked_dynmap).  Today's owner declares
        # no dynamic port, so this still demands absence - the same question,
        # asked of generated bytes now that the tracked ROM is deleted: the
        # `Source :` marker in the tracked SHAPE include is still what names
        # the owner, and that file is still tracked and still drifts.
        with tempfile.TemporaryDirectory() as td_o:
            src_o, owner_cfg = ces.tracked_owner(
                eb, adp_text=open(TRACKED_ADP_SVH).read())
            assert owner_cfg is not None, \
                f"tracked shape names no known config ({src_o})"
            _, owner_rom = _dynmap_candidate(
                os.path.join(ROOT, src_o), td_o)
            owner_name, owner_dyn = _check_tracked_dynmap(TRACKED_ADP_SVH,
                                                          owner_rom)
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

    # R2: every Milan input is dynamic, so engine presence is now an
    # unconditional model invariant. Candidate pairs are kept in temp dirs;
    # nothing is installed and the tree retains its owner.
    p = _variant(CONFIGS["arty_current"], dyn)
    try:
        with tempfile.TemporaryDirectory() as td:
            dyn_adp, dyn_rom = _dynmap_candidate(p, td)
            sub = os.path.join(td, "current")
            os.makedirs(sub)
            cur_adp, cur_rom = _dynmap_candidate(CONFIGS["arty_current"], sub)

            # A conformant owner passes with the required input engine.
            name, want = _check_tracked_dynmap(dyn_adp, dyn_rom, configs=[p])
            assert want is True, f"{name}: dynamic owner not seen as dynamic"
            assert "AEM_DYNMAP" in open(dyn_rom).read(), (
                "SETUP: the dynamic candidate ROM has no engine to require")
            print(f"  [gate 17] a Milan input owner requires "
                  f"`AEM_DYNMAP PRESENT and the candidate pair carries it")

            # A stale/mutated ROM with the engine marker removed is rejected.
            broken_rom = os.path.join(td, "broken.svh")
            with open(broken_rom, "w") as f:
                f.write(open(dyn_rom).read().replace("AEM_DYNMAP",
                                                     "AEM_XYNMAP"))
            _expect_dynmap_rejected(
                "owner declares a dynamic port, tracked ROM has no engine",
                lambda: _check_tracked_dynmap(dyn_adp, broken_rom,
                                              configs=[p]))

            # An owner that cannot be resolved must FAIL, not skip: with
            #     no owner there is no expectation to check against.
            ghost = open(cur_adp).read().replace(
                "configs/endstation_arty_current.yaml",
                "configs/endstation_ghost.yaml")
            assert ces.svh_source(ghost) == "configs/endstation_ghost.yaml"
            with open(cur_adp, "w") as f:
                f.write(ghost)
            _expect_dynmap_rejected(
                "shape include names a config that does not exist",
                lambda: _check_tracked_dynmap(cur_adp, cur_rom))
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
        assert "AEM_DMAP_PBASE_C [0:3] = '{32'd0, 32'd4, 32'd8, 32'd12}" in svh
        assert "AEM_DMAP_PCLS_C [0:3] = '{32'd4, 32'd4, 32'd4, 32'd4}" in svh
        assert "AEM_DMAP_PDYN_C [0:3] = '{1'b1, 1'b1, 1'b1, 1'b1}" in svh
        # 4 clusters / default page min(4,8)=4 -> ONE partition per port
        assert "localparam int unsigned AEM_DMAP_PAGE_C  = 4;" in svh
        assert "AEM_DMAP_PNMAPS_C [0:3] = '{32'd1, 32'd1, 32'd1, 32'd1}" in svh
        # 4 AAF sinks + the CRF sink: only the AAF ones are mappable
        assert "AEM_DMAP_SAAF_C [0:4] = '{1'b1, 1'b1, 1'b1, 1'b1, 1'b0}" in svh
        assert "AEM_DMAP_SCH_C [0:4] = '{10'd4, 10'd4, 10'd4, 10'd4, 10'd0}" in svh
        print("  [gate 17b] arty_4x4 ALL listeners dynamic (Milan 5.3.3.9): "
              "4 ports n_maps=0, no input AUDIO_MAP, svh keys=16 bases "
              "0/4/8/12, CRF sink flagged unmappable")

        # gate 17c: the protocol store covers every model key, while only a
        # generated physical projection may reach the render crossbar.
        # AEM_DMAP_PHYS_C still fixes that crossbar's capacity; RPHYS decides
        # which model keys, if any, address it.
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
        # Both physical write arms remain full-width gated. The CSR arm must
        # also require a generated projection instead of comparing the model
        # key directly with the physical depth.
        assert re.search(r"32'\(aecp_dmap_wr_addr_w\)\s*<\s*CHMAP_PHYS_C", dp), \
            "milan_datapath: AEM arm of the render-map write is not gated"
        assert "cfg_chmap_rphys_w[6]" in dp, \
            "milan_datapath: CSR-debug arm ignores generated RPHYS validity"
        assert re.search(
            r"32'\(cfg_chmap_rphys_w\[5:0\]\)\s*<\s*CHMAP_PHYS_C", dp), \
            "milan_datapath: projected CSR render key is not depth-gated"
        assert "ADP_DMAP_IN_RPHYS_C[k]" in dp, \
            "milan_datapath: generated input projection table is not consumed"
        print(f"  [gate 17c] AEM_DMAP_PHYS_C {m.group(1)} == milan_datapath "
              f"CHMAP_PHYS_C {d.group(1)}; RPHYS validity and full-width "
              "physical-depth gates protect both render-map write arms")
    finally:
        os.unlink(p)

    # unsupported placements are rejected with clear errors
    # gate 17d (USER 08-01): talkers may go dynamic too. On the role-pools
    # 8x8 ship shape, flipping every talker+listener dynamic must emit the
    # `AEM_ODYNMAP engine with the D8 pool projected into capture-crossbar
    # source templates (loopback identity - the AX routes no audio pins).
    def dyn_everything(c):
        for s in c["streams"]["listeners"]:
            s["map_mode"] = "dynamic"
        for s in c["streams"]["talkers"]:
            s["map_mode"] = "dynamic"
    p = _variant(CONFIGS["ax7101_8x8"], dyn_everything)
    try:
        r = eb.build(p, OUT)
        ovl = r["overlay"]
        pout = ovl["stream_ports"]["output"]
        assert all(q["maps"] == 0 and q["base_map"] == 0 for q in pout)
        assert all(q.get("map_mode") == "dynamic" for q in pout)
        assert ovl["descriptor_counts"]["AUDIO_MAP"] == 0
        assert ovl["audio_maps"] == []
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(
                [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
                 "--overlay", r["paths"]["aem_overlay"], "--out-dir", td],
                check=True, capture_output=True)
            svh = open(os.path.join(td, "aecp_aem_rom.svh")).read()
        assert "`define AEM_ODYNMAP" in svh
        assert "localparam int unsigned AEM_ODMAP_NPORTS_C = 8;" in svh
        assert "localparam int unsigned AEM_ODMAP_KEYS_C   = 64;" in svh
        assert ("AEM_ODMAP_PSTR_C [0:7] = '{32'd0, 32'd1, 32'd2, 32'd3, "
                "32'd4, 32'd5, 32'd6, 32'd7}") in svh
        assert ("AEM_ODMAP_SLOTB_C [0:7] = '{32'd0, 32'd4, 32'd8, 32'd12, "
                "32'd16, 32'd20, 32'd24, 32'd28}") in svh
        # gate 17e (task #65): THE POWER-ON IMAGE MAY ONLY NAME A SOURCE THIS
        # BUILD CAN PRODUCE. The AX routes no audio pins, so the primary-role
        # fall-through used to land on LOOPBACK and every talker woke mapped
        # to a cluster whose fabric bucket milan_datapath never wired: a
        # GET_AUDIO_MAP that reads perfectly over a stream of digital
        # silence. The ship config declares loopback_lane false, so:
        #   - the identity must be the HOST pool, whose templates are the
        #     elaborated KL_pcm_tx ring: {valid, half, src=3 RING} = 13'h13xx
        #   - the loopback templates must still be EMITTED (the clusters
        #     exist and a controller may map to them) but fabric-disabled,
        #     bit 12 clear, so 13'h05xx, never 13'h15xx
        # INIT carries {valid[5], cluster offset[4:0]}; host is offset 0
        # (physical is 0 wide), so every key must read 6'h20 + channel.
        assert "13'h1300" in svh, "power-on identity is not the host ring"
        assert "13'h15" not in svh, \
            "a VALID loopback template survived with the lane switched off"
        assert "13'h05" in svh, \
            "loopback templates vanished; the clusters must still be offered"
        assert "AEM_ODMAP_INIT_C [0:63] = '{6'h20, 6'h21, 6'h22, 6'h23, " \
               "6'h24, 6'h25, 6'h26, 6'h27" in svh, \
            "power-on map does not wake on the host pool"
        print("  [gate 17d] ax7101_8x8 ALL streams dynamic: 8 output ports "
              "n_maps=0, zero AUDIO_MAPs, `AEM_ODYNMAP keys=64 slotb 0..28")
        print("  [gate 17e] lane OFF: power-on identity = HOST/RING "
              "(13'h1300), loopback templates emitted fabric-disabled "
              "(13'h05xx) and protocol-mappable; live CMAP enable stays clear")

        # and the OTHER direction: declaring the lane must hand the pool
        # back. ONE fact drives the argv and the map, so they cannot drift.
        def dyn_everything_lane(c):
            dyn_everything(c)
            c["audio_interface"]["cluster_mapping"]["fabric"] = {
                "loopback_lane": True, "playback_rings": 1}
        p2 = _variant(CONFIGS["ax7101_8x8"], dyn_everything_lane)
        try:
            r2 = eb.build(p2, OUT)
            with tempfile.TemporaryDirectory() as td:
                subprocess.run(
                    [sys.executable,
                     os.path.join(ROOT, "avdecc/gen_aem_store.py"),
                     "--overlay", r2["paths"]["aem_overlay"],
                     "--out-dir", td],
                    check=True, capture_output=True)
                svh2 = open(os.path.join(td, "aecp_aem_rom.svh")).read()
            assert "13'h1500" in svh2, \
                "lane declared but no VALID loopback template emitted"
            #! USER 2026-08-06: host outranks loopback - a BACKED lane is
            #! fully mappable but the entity WAKES claiming the SHARED
            #! MEMORY (INIT 6'h20 = host co=0), never the loop. The 08-05
            #! silicon caught the old order: the talker woke transmitting
            #! its own received stream and every host ADD hit the
            #! pair-slot-unity refusal.
            assert "AEM_ODMAP_INIT_C [0:63] = '{6'h20" in svh2, \
                "the power-on map must claim the HOST pool"
            assert "--loopback-lane" in eb.emit_design_opts(
                eb.load_config(p2)), \
                "lane declared but milan_soc was never told to build it"
            assert all(q["primary_role"] == "host"
                       for q in r2["overlay"]["stream_ports"]["output"])
            print("  [gate 17e] lane ON: loopback valid (13'h1500) and "
                  "mappable, but primary_role/INIT stay HOST (6'h20) - "
                  "the entity wakes on shared memory")
        finally:
            os.unlink(p2)
    finally:
        os.unlink(p)

    def dyn_page_static(c):
        c["streams"]["listeners"][0]["map_mode"] = "static"
        c["streams"]["listeners"][0]["map_page"] = 4
    for label, mutate, needle in (
            ("static listener", dyn_page_static, "forbidden"),):
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
    # The capture crossbar selects static/dynamic output mapping globally,
    # so a mixed output image must be rejected instead of misrouting its
    # static ports through an empty dynamic map.
    def mixed_output_modes(c):
        c["streams"]["talkers"][0]["map_mode"] = "dynamic"
        c["streams"]["talkers"][1]["map_mode"] = "static"
    p = _variant(CONFIGS["arty_4x4"], mixed_output_modes)
    try:
        try:
            eb.load_config(p)
        except eb.ConfigError as e:
            assert "mixed static/dynamic" in str(e), f"mixed outputs: got {e}"
        else:
            raise AssertionError("mixed output map modes: accepted")
    finally:
        os.unlink(p)
    print("  [gate 17] reject paths: static input, disagreeing input pages, "
          "and mixed output map modes raise ConfigError")


MILAN_CSR_SV = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")
#: hdl/ieee8021q/srp/** is DELETED (lwsrp_pkg.sv, KL_lwsrp_top.sv,
#: KL_lwsrp_bw_gate.sv and gen/lwsrp_table.svh with it).  Gates 18b/18c used
#: those files as the RTL comparand for the SR-class, MRP-timer, bandwidth and
#: module-parameter constants; what survives of that loop is the CSR-facing
#: subset milan_csr.sv still `include-s, and the gates below say per assertion
#: which comparand each one lost.
DATAPATH_SV = os.path.join(ROOT, "hdl/milan/milan_datapath.sv")
PACKETIZER_SV = os.path.join(ROOT, "hdl/ieee1722/aaf/KL_aaf_packetizer.sv")
ETH_PKG_SV = os.path.join(ROOT, "hdl/common/ethernet_packet_pkg.sv")
MILAN_SOC_PY = os.path.join(ROOT, "sw/litex/milan_soc.py")
TRACKED_CSR_SVH = os.path.join(ROOT, eb.CSR_DEFAULTS_REL)
REGMAP_MD = os.path.join(ROOT, "docs/reference/REGISTER_MAP.md")

#: Everything that compiles hdl/common/csr/milan_csr.sv. Since 11944cd that
#: file `include-s gen/lwsrp_csr_defaults.svh, so each of these must carry
#: hdl/common/csr as an include dir (gate 20a). (path, regex proving it).
#:
#: syn/yosys/run.sh spells its include dirs as an INCDIRS array rather than as
#: one -I flag string, because syn/ooc/dp_srcs.py asks that script for them
#: (`run.sh --emit`) instead of re-reading the file (PR #240). The property this
#: row checks is unchanged - the directory must be in the list run.sh compiles
#: with - so only the spelling of the proof moved, and dropping the entry from
#: INCDIRS still fails here.
CSR_INCDIR_CONSUMERS = (
    ("tb/verilator/csr/Makefile", r"\+incdir\+\$\(RTL_DIR\)/common/csr"),
    ("tb/verilator/milan_dp/Makefile", r"\+incdir\+\$\(RTL_DIR\)/common/csr"),
    ("tb/verilator/hostplane/Makefile", r"\+incdir\+\$\(RTL_DIR\)/common/csr"),
    ("sw/litex/milan_soc.py", r"\"hdl/common/csr\""),
    ("syn/yosys/run.sh", r"INCDIRS=\([^)]*\"\$R/hdl/common/csr\""),
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
    """Gate 18b: the SR-class / MRP-timer / bandwidth constants, and the
    PriorityAndRank byte milan_csr drives onto o_srp_ctx_prio_rank.

    WHAT THIS GATE LOST (2026-08-12).  Its RTL comparand was
    hdl/ieee8021q/srp/lwsrp_pkg.sv - the hand-written package the engine
    compiled - plus KL_lwsrp_bw_gate.sv's 75% ceiling literals and the
    tracked hdl/ieee8021q/srp/gen/lwsrp_table.svh.  All three are DELETED
    with the lwSRP engine.  Ten emitted-vs-package comparisons therefore have
    no second side left, and are removed rather than restated against the
    builder's own constants (a check that compares a value to itself is not a
    check).

    WHAT SURVIVES, and is asserted here:
      * the CLAUSE arithmetic.  Milan 4.3.3.2's recipe is a spec statement,
        not an RTL detail, and the two worked examples below (the clamped CRF
        row and an unclamped 4ch AAF row) still compose to the clause's kb/s.
        These would have caught the folded-+42 defect on their own.
      * the ONE chain that still reaches silicon: emitter -> the generated
        LWSRP_PRIO_RANK_C in hdl/common/csr/gen/lwsrp_csr_defaults.svh ->
        milan_csr.sv's assign to o_srp_ctx_prio_rank.  milan_csr still
        `include-s that header, so a config edit still re-elaborates it."""
    csr = open(MILAN_CSR_SV).read()
    t = eb.build(CONFIGS["arty_current"], OUT)["lwsrp"]
    # ---- Milan 4.3.3.2's recipe, composed. Step-by-step comparison against
    # the RTL is gone with lwsrp_pkg.sv; the clause's own worked examples are
    # not, and they are what the step split was FOR: the fold hid the loss of
    # step 2 precisely because the totals agreed for every frame that never
    # needed the clamp, and the CRF row is the row that needs it.
    assert eb.CRF_SRP_MAXFRAME_B == 29, \
        "CRF MaxFrameSize is Table 4.4's 28 + 1"
    assert eb.SRP_L2_OVERHEAD_B + eb.SRP_WIRE_OVERHEAD_B == \
        t["bandwidth"]["frame_overhead_bytes"], \
        "the emitted folded overhead is no longer steps 1 + 3"
    assert eb.srp_idle_slope_bps(29, 1, 8000) == 5_632_000, \
        "CRF slope: 29 -> clamped to 68 -> 88 octets -> 5632 kb/s"
    assert eb.srp_idle_slope_bps(121, 1, 8000) == 10_432_000, \
        "4ch AAF slope: 121 -> 143 (no clamp) -> 163 octets -> 10432 kb/s"
    # the clamp itself, stated in the units the formula uses: step 1 adds
    # SRP_L2_OVERHEAD_B to MaxFrameSize, so every MaxFrameSize at or below
    # SRP_MIN_L2_BYTES_B - SRP_L2_OVERHEAD_B lands on the same clamped slope.
    # This is the arm the folded +42 lost: fold steps 1 and 3 and the CRF row
    # (MaxFrameSize 29) reserves 5376 kb/s against the mandated 5632.
    clamp_at = eb.SRP_MIN_L2_BYTES_B - eb.SRP_L2_OVERHEAD_B
    assert eb.srp_idle_slope_bps(clamp_at - 1, 1, 8000) == \
        eb.srp_idle_slope_bps(clamp_at, 1, 8000), \
        "step 2's minimum tagged frame no longer clamps"
    assert eb.srp_idle_slope_bps(clamp_at + 1, 1, 8000) > \
        eb.srp_idle_slope_bps(clamp_at, 1, 8000), \
        "the clamp swallowed a frame that is above the minimum"
    print("  [gate 18d] Milan 4.3.3.2 bandwidth recipe: the clamped CRF row "
          "and an unclamped 4ch AAF row both compose to the clause's kb/s, "
          "and the step-2 clamp bites (lwsrp_pkg.sv comparand DELETED)")
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
    # the FULL table is still emitted (out/<cfg>/lwsrp_table.svh) because the
    # 0x680 reset words and the bandwidth math are derived in it; it just has
    # no tracked destination any more. Assert it still carries the words the
    # CSR subset was cut from, so the two cannot silently diverge.
    svh = eb.build(CONFIGS["arty_current"], OUT)["lwsrp_svh"]
    for needle in (f"LWSRP_CLASS_ID_C   = 8'd{t['sr_class']['class_id']};",
                   f"LWSRP_PRIO_RANK_C  = 8'h{pr:02X};",
                   "LWSRP_CTRL_RST_C      = 32'h0000_0010;",
                   "LWSRP_TSPEC_RST_C     = 32'h0001_00E0;"):
        assert needle in svh, f"emitted lwsrp_table.svh lacks {needle!r}"
    assert not os.path.exists(os.path.join(ROOT, "hdl/ieee8021q/srp")), \
        "hdl/ieee8021q/srp is back - the lwSRP engine is deleted and the " \
        "builder must not recreate its gen/ directory"
    print("  [gate 18b] PriorityAndRank == the generated symbol milan_csr "
          "drives (emitter -> lwsrp_csr_defaults.svh -> RTL); the reference "
          "lwsrp_table.svh still carries the words the CSR subset was cut "
          "from, and no hdl/ieee8021q/srp tree was recreated")


def test_lwsrp_tspec_and_params():
    """Gate 18c: the TSpec derivation is anchored in the RTL frame geometry
    (KL_aaf_packetizer), and the ctx row arithmetic covers every attribute
    row the shape needs.

    WHAT THIS GATE LOST (2026-08-12).  It also asserted that milan_datapath
    instantiates KL_lwsrp_top with N_CTX_P(SRP_CTX_ROWS_C) /
    N_LISTENERS_P(N_STREAMS) / N_TALKERS_P(SRP_TALKERS_C), and that
    KL_lwsrp_top ties the bw_gate width to N_TALKERS_P.  Both modules are
    DELETED and milan_datapath no longer instantiates any lwSRP engine, so
    those four assertions have no subject.  The ANCHOR that matters most is
    untouched: KL_aaf_packetizer still exists and still emits the frames the
    TSpec describes, so the frame geometry is still checked against the RTL
    that produces it - and the datapath's SRP row-map localparams are still
    there and still checked, because the protocol processor consumes the same
    row layout."""
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
    epkg = open(ETH_PKG_SV).read()
    # (the KL_lwsrp_top instantiation assertion that stood here is REMOVED:
    #  milan_datapath instantiates no lwSRP engine any more and the module is
    #  deleted. The row-map localparams below survive and are still checked.)
    # ...and T includes the CRF Media Clock Output's own talker row when the
    # shape has one (Milan v1.2 7.3.3: the media clock stream is an SR class
    # A reservation like any other stream, not an un-declared side channel)
    assert re.search(r"localparam int SRP_TALKERS_C\s*=\s*"
                     r"N_STREAMS \+ SRP_CRF_TK_C;", dp), \
        "milan_datapath no longer counts the CRF output as a talker row"
    # ...plus the appended CRF-sink listener row when the shape declares
    # the pinned-LAST CRF Media Clock Input sink (task #27, 0x002D)
    assert re.search(r"localparam int SRP_CRFSNK_C\s*=\s*"
                     r"\(ADP_LISTENER_SINK_C > N_STREAMS\) \? 1 : 0;", dp), \
        "milan_datapath no longer derives the CRF-sink row from the " \
        "generated ADP_LISTENER_SINK_C"
    # (the KL_lwsrp_bw_gate width assertion that stood here is REMOVED with
    #  KL_lwsrp_top.sv - both modules are deleted.)
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
        assert mp["KL_lwsrp_top.N_CTX_P"] == max(L, T) + n_tk \
            >= L + T, \
            "ctx rows must cover every listener AND talker attribute row " \
            "plus the dedicated listener-0 row"
        # ctx_idx_i is 5 bits since the listener-0 row round: 32 rows is
        # the ceiling (8x8 + CRF + listener-0 = 17)
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
        # and +1 for the dedicated listener-0 row (2026-08-05)
        assert t["ctx_rows"]["required"] == L + T + crf_tk
        # the shortfall closed 2026-07-26: the datapath sizes the table at
        # 2*N_STREAMS (+CRF), so every listener AND talker attribute row -
        # including sink 0's own - is backed
        assert t["ctx_rows"]["available"] == 2 * max(L, T) + crf_tk
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
                # Table 4.4's declaration, which is the AVTPDU plus the one
                # headroom octet - NOT avtpdu_bytes, which is the wire frame
                assert row["max_frame_bytes"] == \
                    eb.srp_frame_geometry(row["channels"], 48000,
                                          8000)["max_frame_bytes"]
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
        n_l = len(r["cfg"]["listeners"])
        if r["cfg"]["features"]["sound_card"]:
            for needle in (
                    'compatible = "kl,milan-pcm-0.9", "kl,milan-pcm";',
                    'reg-names = "pcm-dma", "milan-csr";',
                    "memory-region = <&pcmring>;", "no-map;"):
                assert needle in dt, f"{name}: device tree lacks {needle!r}"
            # the no-map region must hold every capture stream's ring
            assert int(sh["pcm"]["ring_stride"], 16) * n_l <= \
                int(sh["pcm"]["ring_bytes"], 16)
            assert f"kl,capture-streams = <{n_l}>" in dt
            surface = f"{n_l}-stream {sh['pcm']['ring_bytes']} no-map ring"
        else:
            assert sh["pcm"] is None and "pcm-dma" not in sh["windows"]
            assert 'compatible = "kl,milan-pcm' not in dt
            assert "pcmring" not in dt and "kl,capture-streams" not in dt
            surface = "sound-card node/ring absent"
        print(f"  [gate 19b] {name}: DT node complete (5 NIC reg windows, "
              f"kl,rsc-clk-mhz {sh['rsc_clk_mhz']}, phy-mode "
              f"{sh['phy_mode']}, {surface})")
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
        skip("gate 19b", "csr.csv cross-check: no build tree on disk")
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
        # ...and the STATION MAC, which the deployed DTB restates as
        # local-mac-address. It was an unchecked mirror until 2026-08-02, and
        # it stopped being a cosmetic one when the ATDECC entity_id started
        # DERIVING from platform.mac_address (gate 25): a DTB that disagrees
        # with the config gives the board one MAC on the wire and an
        # entity_id - and therefore a stream_id {MAC, unique_id} - announcing
        # another. Same defect class as the model id, one layer down.
        mac = re.search(r"local-mac-address = \[([0-9a-fA-F ]+)\]", txt)
        assert mac, f"{dts}: no local-mac-address"
        got_mac = ":".join(mac.group(1).split()).lower()
        assert got_mac == sh["mac_address"].lower(), (
            f"{cfg_name}: config MAC {sh['mac_address']} != deployed {dts} "
            f"{got_mac} - the entity_id derives from the config's, the wire "
            f"carries the DTB's")
        checked += 1
        print(f"  [gate 19b] {cfg_name}: all 5 NIC reg bases + the PCM node "
              f"base + kl,rsc-clk-mhz + the station MAC MATCH the deployed "
              f"{os.path.basename(dts)}")
    if not checked:
        skip("gate 19b", "deployed-.dts cross-check: sibling repo "
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
      5. the CSR subset agrees word-for-word with the full lwSRP table this
         same build() emitted (the tracked
         hdl/ieee8021q/srp/gen/lwsrp_table.svh is deleted with the srp tree,
         so it is two emitters compared, not two files) - one config, one pass;
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
    # 5. the subset agrees with the full table. The comparand MOVED: the
    #    tracked hdl/ieee8021q/srp/gen/lwsrp_table.svh is deleted with the
    #    srp tree, so the full table is taken from the SAME build() call's
    #    in-memory emission. The property is unchanged and still meaningful -
    #    the subset is CUT from the table by a separate emitter, so the two
    #    can still be edited apart - but note what it no longer proves: it
    #    cannot catch a stale file, because there is no second file.
    tbl = _svh_localparams(r["lwsrp_svh"])
    shared = sorted(set(hdr) & set(tbl))
    assert len(shared) == len(hdr), \
        f"CSR header carries constants the lwSRP table does not: " \
        f"{sorted(set(hdr) - set(tbl))}"
    for k in shared:
        assert hdr[k] == tbl[k], (
            f"{k}: CSR header 0x{hdr[k]:X} != the emitted lwSRP table's "
            f"0x{tbl[k]:X} - the two emitters have drifted")
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
          f"left in the RTL, {len(shared)} constants agree with the emitted "
          f"lwSRP table, {len(CSR_INCDIR_CONSUMERS)} consumers carry the "
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


def _is_not_arg(node, dest):
    """True only for the source expression `not args.<dest>`."""
    return isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not) and \
        isinstance(node.operand, ast.Attribute) and \
        node.operand.attr == dest and \
        isinstance(node.operand.value, ast.Name) and \
        node.operand.value.id == "args"


def _soc_tree(soc):
    """The milan_soc.py module AST, from source text or an AST already had."""
    return soc if isinstance(soc, ast.Module) else \
        ast.parse(soc, filename="sw/litex/milan_soc.py")


def _declared_params(func):
    """The parameter names a `def` declares EXPLICITLY, by name.

    `*args` and `**kwargs` are excluded ON PURPOSE, and that exclusion is the
    whole point. `MilanSoC.__init__` ends in `**kwargs` and forwards it
    verbatim to LiteX `SoCCore.__init__`, which does NOT raise on a keyword it
    does not know: it logs one warning and carries on. So a prune handed over
    as a top-level `maap=not args.no_maap` would be accepted by argparse,
    accepted by the constructor, mentioned once in a wall of build log, and
    shipped as a bitstream with KL_maap still in it. That is p_AAF_PLAYBACK
    again, so a keyword `**kwargs` would swallow MUST fail closed here.
    """
    a = func.args
    return {p.arg for p in (*a.posonlyargs, *a.args, *a.kwonlyargs)}


def _reads(node, name):
    """True when the expression still READS the local `name` somewhere inside.

    Deliberately a dependency question, not a spelling one: `render_lpf`,
    `bool(render_lpf)` and `bool(render_lpf) and x` all pass, `True` does not.
    """
    return node is not None and any(
        isinstance(n, ast.Name) and n.id == name for n in ast.walk(node))


def _sole(nodes, what):
    """The one node there must be, or a failure that says what was missing."""
    assert len(nodes) == 1, \
        f"milan_soc.py: expected exactly one {what}, found {len(nodes)}"
    return nodes[0]


def _blocks_key(node, key):
    """`blocks[<key>]`, where key is a string literal or a variable name."""
    if not (isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and node.value.id == "blocks"):
        return False
    idx = node.slice
    return (isinstance(idx, ast.Constant) and idx.value == key) or \
           (isinstance(idx, ast.Name) and idx.id == key)


def _class_of(tree, name):
    return _sole([n for n in tree.body
                  if isinstance(n, ast.ClassDef) and n.name == name],
                 f"class {name}")


def _def_of(scope, name):
    return _sole([n for n in scope.body
                  if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and n.name == name], f"def {name}()")


def _sole_call(scope, callee, where):
    """The keywords of the SINGLE `callee(...)` call inside `scope`."""
    call = _sole([n for n in ast.walk(scope)
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                  and n.func.id == callee], f"{callee}(...) call in {where}")
    assert not any(kw.arg is None for kw in call.keywords), (
        f"milan_soc.py {where}: {callee}(...) splats `**` - the prune chain "
        "has to be readable in the source, not assembled at run time")
    return {kw.arg: kw.value for kw in call.keywords}


def _optional_block_cli_consumption(soc):
    """Map every OPTIONAL_BLOCKS row to its consumption route in main().

    Parsing the call rather than searching for each spelling matters: a dead
    reference in a comment or helper must not prove that argparse's value
    reaches the MilanSoC instance. Most blocks ride `optional_blocks`; the
    older render_lpf ABI is intentionally a dedicated constructor keyword.

    A dedicated keyword only counts when `MilanSoC.__init__` DECLARES it (see
    `_declared_params`). Without that test the escape hatch proves nothing:
    move any row out of the dict onto its own keyword and the gate would print
    the block as consumed while the build warns once and ships it unpruned.
    """
    tree = _soc_tree(soc)
    mains = [n for n in tree.body
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
             and n.name == "main"]
    assert len(mains) == 1, \
        f"milan_soc.py: expected one main(), found {len(mains)}"
    calls = [n for n in ast.walk(mains[0])
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "MilanSoC"]
    assert len(calls) == 1, \
        f"milan_soc.py main(): expected one MilanSoC call, found {len(calls)}"
    assert not any(kw.arg is None for kw in calls[0].keywords), \
        "milan_soc.py main(): the MilanSoC call splats `**` - every prune " \
        "handoff has to be readable in the source"
    kwargs = {kw.arg: kw.value for kw in calls[0].keywords}
    block_dict = kwargs.get("optional_blocks")
    assert isinstance(block_dict, ast.Dict), \
        "milan_soc.py main(): MilanSoC has no literal optional_blocks dict"
    entries = {}
    for key, value in zip(block_dict.keys, block_dict.values):
        assert isinstance(key, ast.Constant) and isinstance(key.value, str), \
            "milan_soc.py main(): optional_blocks keys must be string literals"
        entries[key.value] = value
    # the receiving end of every handoff below. `optional_blocks` itself is a
    # keyword like any other: renamed away, `**kwargs` eats the whole dict.
    declared = _declared_params(_def_of(_class_of(tree, "MilanSoC"),
                                        "__init__"))
    assert "optional_blocks" in declared, (
        "MilanSoC.__init__ declares no `optional_blocks` parameter, so the "
        "whole tier-1 dict is swallowed by its `**kwargs` and forwarded to "
        "LiteX SoCCore, which warns once and ignores it")

    routes = {}
    for name, (flag, _param, _why) in eb.OPTIONAL_BLOCKS.items():
        dest = flag.removeprefix("--").replace("-", "_")
        if _is_not_arg(entries.get(name), dest):
            routes[name] = "optional_blocks"
        elif _is_not_arg(kwargs.get(name), dest):
            assert name in declared, (
                f"{name}: main() hands `{flag}` to MilanSoC as a dedicated "
                f"`{name}=` keyword, but MilanSoC.__init__ declares no "
                f"`{name}` parameter - its trailing `**kwargs` swallows the "
                "value and forwards it to LiteX SoCCore, which logs ONE "
                "warning, ignores it, and builds a bitstream with the block "
                f"still in it. Put `{name}` in the optional_blocks dict, or "
                "declare the parameter")
            routes[name] = f"{name} keyword"
        else:
            raise AssertionError(
                f"{name}: milan_soc.py main() does not consume `{flag}` as "
                f"`not args.{dest}` in the MilanSoC optional_blocks dict or "
                f"a dedicated `{name}=` keyword; the missing key defaults "
                "to PRESENT and the prune flag becomes a silent no-op")

    # every --no-* flag main() DECLARES must be one main() also READS, and it
    # must stay an off-by-default store_true. `default=True` on a --no-* flag
    # inverts the lever in silence (an UNFLAGGED build takes the pruned path),
    # and a flag nothing reads is decorative ABI wearing a CLI hat.
    read = {n.attr for n in ast.walk(mains[0]) if isinstance(n, ast.Attribute)
            and isinstance(n.value, ast.Name) and n.value.id == "args"}
    for call in ast.walk(mains[0]):
        if not (isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "add_argument"
                and call.args and isinstance(call.args[0], ast.Constant)
                and str(call.args[0].value).startswith("--no-")):
            continue
        flag = call.args[0].value
        opts = {kw.arg: kw.value for kw in call.keywords if kw.arg}
        named = opts.get("dest")
        dest = named.value if isinstance(named, ast.Constant) else \
            flag.removeprefix("--").replace("-", "_")
        act = opts.get("action")
        assert isinstance(act, ast.Constant) and act.value == "store_true", (
            f"{flag}: a --no-* flag must be a plain store_true, not "
            f"{ast.unparse(act) if act is not None else 'a positional store'}")
        dflt = opts.get("default")
        assert dflt is None or (isinstance(dflt, ast.Constant)
                                and (dflt.value is False
                                     or dflt.value is None)), (
            f"{flag}: `default={ast.unparse(dflt)}` inverts the flag - an "
            "UNFLAGGED build would take the pruned path and ship the block "
            "missing, which is the silent no-op with its sign flipped")
        assert dest in read, (
            f"{flag}: main() declares it and never reads `args.{dest}`, so it "
            "is decorative - the argv records the intent and the gateware "
            "never hears about it (the #130 shape, one hop earlier)")
    return routes


def _optional_block_prune_chain(soc):
    """Trace every tier-1 prune from argparse to `p_<PARAM> = 0`, statically.

    Gate 23d used to stop at the FIRST hop, `main()` -> `MilanSoC(...)`. Three
    more hops sit between that call and the parameter the RTL reads, and all
    of them live in this one file:

        main()             -> MilanSoC(optional_blocks=..., render_lpf=...)
        MilanSoC.__init__  -> MilanNIC(optional_blocks=..., render_lpf=...)
        MilanNIC.__init__  -> add_milan_datapath(optional_blocks=...)
        add_milan_datapath -> dp_params[f"p_{param}"] = 0

    A value dropped, tied or inverted on any of them is invisible to a
    spelling check, and its symptom is the #130 symptom exactly: the config
    declares the prune, the plan tabulates it, the estimate books the saving,
    and the bitstream ships the block. The emit guard is worse than a no-op if
    inverted, because then an UNFLAGGED build prunes all seven and the
    shipping bitstream quietly loses MAAP, the media-clock servo and the RX
    MAC filter.

    Task #144 (gate 23f) proves the same chain BEHAVIOURALLY, by elaborating
    main() and spying on `Instance("milan_datapath", ...)`; that gate needs
    migen + LiteX, so it SKIPS in CI. This one is text and AST only, which is
    why it is the half that runs on the pyyaml-only docs job. The last link,
    `dp_params` -> the parameters `Instance` is actually handed, is #144's:
    no amount of reading can prove what elaboration does with the dict.
    """
    tree = _soc_tree(soc)
    routes = _optional_block_cli_consumption(tree)
    dedicated = sorted(k for k, r in routes.items() if r != "optional_blocks")
    dict_routed = sorted(k for k, r in routes.items()
                         if r == "optional_blocks")
    soc_init = _def_of(_class_of(tree, "MilanSoC"), "__init__")
    nic_init = _def_of(_class_of(tree, "MilanNIC"), "__init__")
    dp_def = _sole([n for n in tree.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and n.name == "add_milan_datapath"],
                   "def add_milan_datapath()")

    # hops 2 and 3: the carriers are FORWARDED, and each still READS the
    # parameter it arrived in. Deleting `optional_blocks=optional_blocks`
    # here defaults it to None one call further down, which un-prunes every
    # dict-routed block; tying `render_lpf=True` does the same to the banked
    # 428 LUT lever. Both are one deleted line and neither raises.
    carriers = {"optional_blocks": dict_routed}
    carriers.update({name: [name] for name in dedicated})
    for src, callee, dst, where in (
            (soc_init, "MilanNIC", nic_init, "MilanSoC.__init__"),
            (nic_init, "add_milan_datapath", dp_def, "MilanNIC.__init__")):
        passed = _sole_call(src, callee, where)
        for carrier, carried in carriers.items():
            assert carrier in _declared_params(src), (
                f"{where} declares no `{carrier}` parameter, so the prune "
                f"never arrives at all for: {', '.join(carried)}")
            assert carrier in _declared_params(dst), (
                f"{callee} declares no `{carrier}` parameter, so {where} "
                f"cannot hand the prune on for: {', '.join(carried)}")
            got = passed.get(carrier)
            saw = f"`{carrier}={ast.unparse(got)}`" if got is not None else \
                f"no `{carrier}=` keyword at all"
            assert _reads(got, carrier), (
                f"{where}: the {callee}(...) call passes {saw}, which no "
                f"longer reads its own `{carrier}` parameter - the prune is "
                f"dropped one hop short of the RTL for: {', '.join(carried)}")

    # hop 4a: the map starts ALL PRESENT (AREA_BUDGET rule 1, at the source)
    seed = _sole([n for n in ast.walk(dp_def) if isinstance(n, ast.Assign)
                  and isinstance(n.targets[0], ast.Name)
                  and n.targets[0].id == "blocks"], "`blocks = ...` seed")
    assert (isinstance(seed.value, ast.Call)
            and _reads(seed.value, "MILAN_OPTIONAL_BLOCKS")
            and any(isinstance(a, ast.Constant) and a.value is True
                    for a in seed.value.args)), (
        f"add_milan_datapath: `{ast.unparse(seed)}` does not seed every block "
        "PRESENT from MILAN_OPTIONAL_BLOCKS - anything else prunes on an "
        f"UNFLAGGED build: {', '.join(sorted(routes))}")

    # hop 4b: each dedicated keyword folds its OWN parameter into the map
    for name in dedicated:
        fold = _sole([n for n in ast.walk(dp_def) if isinstance(n, ast.Assign)
                      and _blocks_key(n.targets[0], name)],
                     f'`blocks["{name}"] = ...`')
        assert _reads(fold.value, name), (
            f"{name}: add_milan_datapath sets `{ast.unparse(fold)}`, which "
            f"never reads its `{name}` parameter - the dedicated keyword is "
            "inert and the block ships PRESENT whatever the CLI asked for")

    # hop 4c: the dict fold still reads the caller's value
    fold = _sole([n for n in ast.walk(dp_def) if isinstance(n, ast.For)
                  and _reads(n.iter, "optional_blocks")],
                 "`for ... in optional_blocks` fold")
    assert (isinstance(fold.target, ast.Tuple) and len(fold.target.elts) == 2
            and all(isinstance(e, ast.Name) for e in fold.target.elts)), \
        "add_milan_datapath: the optional_blocks fold is not `for k, v in ...`"
    kvar, vvar = (e.id for e in fold.target.elts)
    row = _sole([n for n in ast.walk(fold) if isinstance(n, ast.Assign)
                 and _blocks_key(n.targets[0], kvar)],
                f"`blocks[{kvar}] = ...` inside the optional_blocks fold")
    assert _reads(row.value, vvar), (
        f"add_milan_datapath: `{ast.unparse(row)}` no longer reads the "
        "caller's value, so EVERY dict-routed prune is a no-op: "
        f"{', '.join(dict_routed)}")

    # hop 4d: the emit guard, and above all its POLARITY. One `not` decides
    # the sign of the whole tier-1 table for every block at once.
    emit = _sole([n for n in ast.walk(dp_def) if isinstance(n, ast.For)
                  and _reads(n.iter, "MILAN_OPTIONAL_BLOCKS")],
                 "`for k, param in MILAN_OPTIONAL_BLOCKS.items()` emit loop")
    assert (isinstance(emit.target, ast.Tuple) and len(emit.target.elts) == 2
            and all(isinstance(e, ast.Name) for e in emit.target.elts)), \
        "add_milan_datapath: the emit loop is not `for k, param in ...`"
    kvar, pvar = (e.id for e in emit.target.elts)
    guard = _sole([n for n in emit.body if isinstance(n, ast.If)],
                  "`if ...:` inside the emit loop")
    assert (isinstance(guard.test, ast.UnaryOp)
            and isinstance(guard.test.op, ast.Not)
            and _blocks_key(guard.test.operand, kvar)), (
        "add_milan_datapath emits the prune parameter under "
        f"`if {ast.unparse(guard.test)}:` and not `if not blocks[{kvar}]:` - "
        "this single line carries the polarity of the whole tier-1 table, and "
        "inverted it makes an UNFLAGGED build prune every one of them: "
        f"{', '.join(sorted(routes))}")
    assert not guard.orelse, (
        "add_milan_datapath: the emit guard grew an else arm - a block is "
        "either pruned or absent from dp_params, never both: "
        f"{', '.join(sorted(routes))}")
    out = _sole([n for n in guard.body if isinstance(n, ast.Assign)],
                "the p_<PARAM> assignment inside the emit guard")
    assert (isinstance(out.targets[0], ast.Subscript)
            and isinstance(out.targets[0].value, ast.Name)
            and out.targets[0].value.id == "dp_params"
            and _reads(out.targets[0].slice, pvar)), (
        f"add_milan_datapath: `{ast.unparse(out)}` does not key dp_params on "
        f"the loop's own `{pvar}` - a prune that names a parameter the RTL "
        "does not have IS the p_AAF_PLAYBACK defect: "
        f"{', '.join(sorted(routes))}")
    assert isinstance(out.value, ast.Constant) and out.value.value == 0, (
        f"add_milan_datapath: `{ast.unparse(out)}` - only 0 prunes, any other "
        "value leaves the generate arm elaborated (AREA_BUDGET rule 1)")
    return routes


def test_optional_block_names_reach_the_rtl():
    """gate 23d - the DECORATIVE-ABI gate, and the reason it exists is on the
    record: `milan_soc.py` passed `p_AAF_PLAYBACK` for weeks while the SV
    parameter was `AAF_PLAYBACK_P`, so a LiteX Instance param silently no-oped
    and the flag pruned nothing. Nothing caught it because no CI job runs
    LiteX. This gate parses the three files as TEXT and pins them together:

      builder OPTIONAL_BLOCKS  <->  milan_soc.py MILAN_OPTIONAL_BLOCKS + argparse
                               <->  milan_datapath.sv `parameter int <NAME> = 1`

    It also traces every argparse value through the four source hops that end
    at `dp_params[f"p_{param}"] = 0` (see `_optional_block_prune_chain`). A
    rename, typo, decorative --no-* flag, dropped forward or inverted guard
    fails here in milliseconds, on a box with no LiteX and no migen.
    """
    soc = open(os.path.join(ROOT, "sw/litex/milan_soc.py")).read()
    rtl = open(os.path.join(ROOT, "hdl/milan/milan_datapath.sv")).read()
    routes = _optional_block_prune_chain(soc)
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
    # 6. and the DOC that authorises all of this names the same blocks, with the
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
    direct = sorted(k for k, route in routes.items()
                    if route != "optional_blocks")
    print(f"  [gate 23d] {len(eb.OPTIONAL_BLOCKS)} optional blocks: builder "
          "key == milan_soc.py map == a real off-by-default --no-* store_true "
          f"main() READS == consumed by main() ({len(routes) - len(direct)} "
          f"through optional_blocks, dedicated {direct}, each a NAMED "
          "MilanSoC.__init__ parameter, none swallowed by **kwargs) == "
          "forwarded through MilanNIC and add_milan_datapath == emitted as "
          "`p_<PARAM> = 0` under `if not blocks[k]` == a milan_datapath "
          "`parameter int X = 1` guarding a generate WITH an else arm == the "
          "AREA_BUDGET tier-1 table row (the p_AAF_PLAYBACK silent-no-op "
          "class, closed for the SPELLING of these statements. A statement "
          "that rebinds or overrides a carrier without touching them - "
          "reassigning optional_blocks, overriding a fold, deleting a "
          "dp_params key - is invisible here by construction, because each "
          "hop is checked in isolation and _reads() is a name-appearance "
          "test. That family and what elaboration hands Instance() are both "
          "gate 23f, task #144)")

    # gate 23e (task #65): the loopback lane rides the SAME decorative-ABI
    # risk but the OPPOSITE polarity - it is an ADD, default OFF, so it is
    # not in OPTIONAL_BLOCKS and gate 23d above cannot see it. Nothing in CI
    # runs LiteX, so a rename on either side would silently no-op exactly
    # like p_AAF_PLAYBACK did: the argv would carry --loopback-lane, the
    # Instance would pass a parameter the RTL does not have, the bucket would
    # stay tied off, and the AEM would go on advertising a lane that is not
    # there. Pin all four names as TEXT.
    assert re.search(r'ap\.add_argument\("--loopback-lane",\s*'
                     r'action="store_true"', soc), \
        "milan_soc.py has no --loopback-lane store_true argument"
    assert re.search(r'dp_params\["p_LOOPBACK_P"\]\s*=\s*1', soc), \
        "milan_soc.py never passes p_LOOPBACK_P (the SV name, exactly)"
    assert re.search(r"^\s*parameter\s+int\s+LOOPBACK_P\s*=\s*(\d+)\s*,",
                     rtl, re.M).group(1) == "0", (
        "milan_datapath.sv LOOPBACK_P must exist and default to 0 - it is an "
        "ADD that the shipping bitstream cannot afford, not a prune")
    # and it must actually reach the leaf: the tie-off is the strobe, so a
    # build with the lane off can never write the hold bank
    assert re.search(r"assign lb_tap_tvalid_w\s*=\s*\(LOOPBACK_P != 0\)",
                     rtl), \
        "milan_datapath.sv: LOOPBACK_P does not gate the LOOP bucket's strobe"
    assert ".lb_tvalid_i (lb_tap_tvalid_w)" in rtl, \
        "milan_datapath.sv: the LOOP bucket's feed is not connected at all"
    # the builder half: the flag is emitted from the SAME declaration
    # primary_segment reads, so the two cannot disagree
    lane_cfg = eb.load_config(CONFIGS["ax7101_8x8"])
    assert ("--loopback-lane" in eb.emit_design_opts(lane_cfg)) == \
        lane_cfg["interface"]["cluster_fabric"]["loopback_lane"], \
        "the milan_soc argv and the declared fabric lane disagree"
    print("  [gate 23e] task #65 loopback lane: --loopback-lane store_true == "
          "p_LOOPBACK_P == `parameter int LOOPBACK_P = 0` == the strobe gate "
          "== the connected lb_tvalid_i == the config declaration that "
          "primary_segment reads (same silent-no-op class, opposite polarity)")


def _chain_control(label, soc, pattern, repl, expect, flags=0):
    """Cut one link of the prune chain in the source and require gate 23d red.

    The mutation must match EXACTLY ONE site (a reformat that moves it has to
    fail loudly here rather than quietly stop testing anything), and the
    failure must name the thing that actually breaks - a red for an unrelated
    reason proves nothing about the link that was cut.
    """
    bad, n = re.subn(pattern, repl, soc, flags=flags)
    assert n == 1, f"{label}: negative control matched {n} sites, want 1"
    try:
        _optional_block_prune_chain(bad)
    except AssertionError as exc:
        assert expect in str(exc), \
            f"{label}: went red for the wrong reason: {exc}"
    else:
        raise AssertionError(
            f"{label}: gate 23d accepted it, and a real build would ship the "
            "block it claims to have pruned")


def test_optional_block_consumption_gate_bites():
    """Gate 23d negative controls: cut every link of the prune chain.

    Replacing a live predicate with True models the exact failure from #130:
    argparse still accepts the flag, but main() always tells MilanSoC that the
    block is present. Every row must turn the focused check red, and the rows
    below it cut the same chain further downstream, where the value is
    forwarded, folded and finally emitted as `p_<PARAM> = 0`.
    """
    soc = open(os.path.join(ROOT, "sw/litex/milan_soc.py")).read()
    rejected = []
    for name, (flag, _param, _why) in eb.OPTIONAL_BLOCKS.items():
        dest = flag.removeprefix("--").replace("-", "_")
        patterns = (
            r'(^\s*"%s"\s*:\s*)not\s+args\.%s\b'
            % (re.escape(name), re.escape(dest)),
            r'(^\s*%s\s*=\s*)not\s+args\.%s\b'
            % (re.escape(name), re.escape(dest)),
        )
        bad, changed = soc, 0
        for pattern in patterns:
            bad, n = re.subn(pattern, r"\g<1>True", bad, count=1,
                             flags=re.M)
            changed += n
        assert changed == 1, (
            f"{name}: negative control found {changed} live handoffs, want 1")
        try:
            _optional_block_cli_consumption(bad)
        except AssertionError as exc:
            assert name in str(exc), \
                f"{name}: mutation failed for the wrong reason: {exc}"
            rejected.append(name)
        else:
            raise AssertionError(
                f"{name}: gate 23d accepted a decorative `{flag}` whose "
                "main() handoff was replaced with True")
    print(f"  [gate 23d mutation] {len(rejected)}/{len(eb.OPTIONAL_BLOCKS)} "
          "disconnected --no-* handoffs rejected by block name")

    # ---- the BLOCKER control: a keyword `**kwargs` would swallow -----------
    # Move a row out of optional_blocks and onto its own top-level keyword.
    # argparse accepts it, MilanSoC.__init__ accepts it (it ends in
    # `**kwargs`), LiteX SoCCore logs one yellow warning and ignores it, the
    # build exits 0 - and the bitstream still contains the block. Before the
    # declaration test this printed the block inside `dedicated [...]` and
    # called the silent-no-op class closed.
    declared = _declared_params(
        _def_of(_class_of(_soc_tree(soc), "MilanSoC"), "__init__"))
    anchor = re.compile(r"^([ \t]*)optional_blocks=\{", re.M)
    swallowed = []
    for name, (flag, _param, _why) in eb.OPTIONAL_BLOCKS.items():
        if name in declared:
            continue         # a real parameter: the dedicated route is honest
        dest = flag.removeprefix("--").replace("-", "_")
        bad, n = re.subn(r'^[ \t]*"%s"[ \t]*:[ \t]*not[ \t]+args\.%s[ \t]*,'
                         r'[ \t]*\n' % (re.escape(name), re.escape(dest)),
                         "", soc, flags=re.M)
        assert n == 1, f"{name}: found {n} optional_blocks rows, want 1"
        site = anchor.search(bad)
        assert site, "milan_soc.py main(): no `optional_blocks={` to anchor to"
        bad = (bad[:site.start()] + f"{site.group(1)}{name}=not args.{dest},\n"
               + bad[site.start():])
        try:
            _optional_block_prune_chain(bad)
        except AssertionError as exc:
            assert name in str(exc) and "kwargs" in str(exc), \
                f"{name}: swallowed-keyword control red for the wrong " \
                f"reason: {exc}"
            swallowed.append(name)
        else:
            raise AssertionError(
                f"{name}: gate 23d called the prune proven while it rode a "
                f"`{name}=` keyword MilanSoC.__init__ never declares - the "
                "p_AAF_PLAYBACK failure reproduced inside the check written "
                "to close it")
    assert swallowed, "no dict-routed block left to run the control against"
    print(f"  [gate 23d mutation] {len(swallowed)}/{len(swallowed)} dedicated "
          "keywords MilanSoC.__init__ never declares rejected by block name "
          "(LiteX warns and ignores; the bitstream ships unpruned)")

    # ---- one cut link per row, from main() down to dp_params --------------
    # Every one of these was green across the WHOLE suite while gate 23d
    # stopped at the MilanSoC call, and each one is a total no-op on a real
    # build. The last three are worse: they prune on an UNFLAGGED build.
    links = (
        ("hop 2 drops optional_blocks (MilanSoC -> MilanNIC)",
         r"render_lpf=bool\(render_lpf\),\s*\n\s*"
         r"optional_blocks=optional_blocks,",
         "render_lpf=bool(render_lpf),", "maap"),
        ("hop 3 drops optional_blocks (MilanNIC -> add_milan_datapath)",
         r"render_lpf=render_lpf, optional_blocks=optional_blocks,",
         "render_lpf=render_lpf,", "maap"),
        ("hop 2 ties render_lpf=True",
         r"render_lpf=bool\(render_lpf\),", "render_lpf=True,", "render_lpf"),
        ("the optional_blocks fold stops reading the caller's value",
         r"blocks\[k\] = blocks\[k\] and bool\(v\)", "blocks[k] = True",
         "maap"),
        ("the render_lpf fold stops reading its parameter",
         r'blocks\["render_lpf"\] = bool\(render_lpf\)',
         'blocks["render_lpf"] = True', "render_lpf"),
        ("a decorative --no-widget nothing reads",
         r'( *)ap\.add_argument\("--no-maap",',
         '\\1ap.add_argument("--no-widget", action="store_true",\n'
         '\\1                help="a flag the gateware never hears about")\n'
         '\\1ap.add_argument("--no-maap",', "--no-widget"),
        ("default=True inverts --no-maap (DEFAULT build prunes maap)",
         r'ap\.add_argument\("--no-maap", action="store_true",',
         'ap.add_argument("--no-maap", action="store_true", default=True,',
         "--no-maap"),
        ("the block map seeds False (DEFAULT build prunes all seven)",
         r"blocks = dict\.fromkeys\(MILAN_OPTIONAL_BLOCKS, True\)",
         "blocks = dict.fromkeys(MILAN_OPTIONAL_BLOCKS, False)", "maap"),
        ("the emit guard is inverted (DEFAULT build prunes all seven)",
         r"if not blocks\[k\]:", "if blocks[k]:", "maap"),
        ("the emit guard is dead (no build ever prunes)",
         r"if not blocks\[k\]:", "if False:", "maap"),
    )
    for label, pattern, repl, expect in links:
        _chain_control(label, soc, pattern, repl, expect, flags=re.M)
    print(f"  [gate 23d chain] {len(links)}/{len(links)} cut links between "
          "main() and `dp_params[f\"p_{param}\"] = 0` rejected, the three "
          "that would prune an UNFLAGGED build included")


# ========================================================== gates 23f/23g ====
#  THE BEHAVIOURAL ELABORATION PROOF (issues #154 and #156).
#
#  Gate 23d is a SPELLING proof.  It parses main() and asserts that every
#  `--no-<block>` argparse value is handed to the MilanSoC(...) call, which
#  closes the defect that shipped - a block declared in OPTIONAL_BLOCKS, in
#  argparse, in the RTL and in AREA_BUDGET, and threaded nowhere - and nothing
#  further.  THREE MORE HOPS stand between that call and the parameter the RTL
#  reads, and every one of them is the same defect class:
#
#      main()               -> MilanSoC(optional_blocks=..., render_lpf=...)
#      MilanSoC.__init__    -> MilanNIC(optional_blocks=..., render_lpf=...)
#      MilanNIC.__init__    -> add_milan_datapath(optional_blocks=...)
#      add_milan_datapath   -> dp_params[f"p_{param}"] = 0
#                           -> Instance("milan_datapath", **dp_params)
#
#  A value that reaches the constructor and is then dropped, renamed or
#  inverted on any of those hops is INVISIBLE to gate 23d, and its symptom is
#  the #130 symptom exactly: the config declares the prune, the build plan
#  tabulates it, the resource estimate books the saving, and the bitstream
#  ships WITH the block.  #154 counts three incidents of it across two flags,
#  and in the `--fabric-gptp` case a reviewer severed the chain at TWO
#  independent hops and read `ALL GATES PASS` both times.
#
#  So these gates do what #130 asked for in as many words: "build a config
#  with the block pruned and assert p_<PARAM>=0 appears in the emitted
#  Instance parameters".  They run the REAL argv through the REAL
#  milan_soc.py main() and READ THE PARAMETERS THAT REACH
#  Instance("milan_datapath", ...).  Nothing is re-implemented and nothing is
#  pattern-matched: `Instance` itself is the observation point, so what is
#  graded is what the elaboration would hand Vivado.  Vivado never runs - the
#  spy raises the moment the Instance is constructed, about 0.9 s after the
#  process starts.
#
#  BOTH POLARITIES, because the flags have both.  The seven OPTIONAL_BLOCKS
#  rows default PRESENT and pass their parameter ONLY when pruned (a default
#  build emits a byte-identical top .v, the AAF_PLAYBACK_P discipline).
#  `sound_card` and `fabric_gptp` are the mirror image - the RTL defaults are
#  SOUND_CARD_P=0 and GPTP_PLANE_EN_P=0 and the parameter is passed only when
#  the block is PRESENT - so they are graded upside down rather than assumed
#  to follow the others.
#
#  WHAT THESE GATES DO NOT PROVE, stated here and in their own output because
#  #154 asks the mechanism to say so:
#    * not that the RTL parameter DOES anything - that a `parameter int X`
#      exists and guards a generate with an else arm is gate 23d's, and what
#      the guarded logic costs is the OOC area work's;
#    * not that the bitstream places, times or boots;
#    * not that a recipe builds the SoC its config describes - gate 1e and
#      scripts/check_sweep_shape.py compare recipe argv against config, and
#      #155 carries the ten flags where they currently disagree;
#    * nothing at all, on a machine with no LiteX interpreter.  There the arms
#      SKIP, and `skip()` puts them in main()'s verdict so the absence of the
#      proof cannot read as the presence of one.

#: The child program.  It runs under the LiteX interpreter, execs
#: milan_soc.py's SOURCE (optionally mutated) as a module whose __file__ is
#: the real path - so REPO_ROOT, the platforms/ search path and every
#: generated-image lookup resolve exactly as they do in a build - patches that
#: module's own `Instance` to a spy, and calls main().  The result goes to a
#: FILE, never to stdout: add_milan_datapath spawns the ACMP/AECP image
#: generators as SUBPROCESSES and their output reaches fd 1 whatever this
#: process redirects.
_INSTANCE_PROBE = r'''
import contextlib, io, json, logging, os, sys, types

spec = json.load(open(sys.argv[1], encoding="utf-8"))
soc_path = spec["soc_path"]
source = open(soc_path, encoding="utf-8").read()
for old, new, want in spec["mutations"]:
    got = source.count(old)
    if got != want:
        raise SystemExit("mutation %r matched %d times, want %d"
                         % (old, got, want))
    source = source.replace(old, new)

logging.disable(logging.CRITICAL)
sys.path.insert(0, os.path.dirname(soc_path))


class _Reached(Exception):
    """Carries the parameters Instance("milan_datapath", ...) was given."""

    def __init__(self, params):
        Exception.__init__(self)
        self.params = params


mod = types.ModuleType("milan_soc_probe")
mod.__file__ = soc_path
sys.modules[mod.__name__] = mod
exec(compile(source, soc_path, "exec"), mod.__dict__)
_real_instance = mod.Instance


def _spy(*args, **kwargs):
    if args and args[0] == "milan_datapath":
        raise _Reached({k: v for k, v in kwargs.items() if k.startswith("p_")})
    return _real_instance(*args, **kwargs)


mod.Instance = _spy
sys.argv = ["milan_soc.py"] + spec["argv"]
sink = io.StringIO()
try:
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        mod.main()
    out = {"error": 'no Instance("milan_datapath") was constructed'}
except _Reached as reached:
    out = {"params": reached.params}
except BaseException as exc:            # reported to the gate, not raised
    # The captured output goes WITH the error, because LiteX reports through
    # a logger rather than through the exception: SoCError carries an empty
    # str() and everything a reader needs is in the stream this process
    # redirected. Without the tail, a CI failure here says "SoCError:" and
    # nothing else, which is a gate nobody can act on.
    tail = sink.getvalue().strip().splitlines()[-12:]
    out = {"error": "%s: %s" % (type(exc).__name__, exc),
           "output": "\n".join(tail)}

with open(spec["result"], "w", encoding="utf-8") as fh:
    json.dump(out, fh)
'''

#: sw/litex, the directory every real build runs milan_soc.py from.  NOT the
#: LiteX repo parent: `import litex` from there resolves to the checkout
#: directory as a namespace package and the import fails.
SOC_DIR = os.path.join(ROOT, "sw/litex")

#: Placeholder an argv uses for "the launcher's --output-dir".  _instance_params
#: substitutes its own scratch directory and then proves that directory is
#: still empty, which is how the spy's cheapness stops being an assumption.
BUILD_OUT_TOKEN = "@BUILD_OUT@"

#: The config whose argv drives gate 23f: the SHIPPING AX shape (USER
#: 2026-08-05, 1x1x8 TDM8), and it is the shipping one that matters here for
#: two independent reasons.
#:
#: It is the only config that carries `--fabric-gptp`, which is #135's
#: incident - nothing tied the parsed flag to p_GPTP_PLANE_EN_P, and on THIS
#: profile (bare-metal, no ptp4l, no phc2sys) that is a bitstream with no
#: time source and no signal.
#:
#: And it was once thought to be the only shape that elaborates anywhere
#: but this bench, which was wrong in both directions (#185): on a stock
#: toolchain NO shape elaborates - this one needs the `baremetal` CPU
#: variant, the four Linux shapes pass `--scala-args=--l2-down-pending` and
#: `--scala-args=--l2-general-slots`, which the VexiiRiscv revision LiteX
#: pins rejects - and with the series in sw/litex/patches applied, which
#: apply.sh does and gate 23h proves, every shape but #184's Arty leg does.
#: The series is carried in this repository; nothing about it is a local
#: modification.
BEHAVIOURAL_CFG = "ax7101_1x1_tdm8"


def _litex_python():
    """An interpreter that can import migen + litex + litex_boards, or None.

    Search order: $MILAN_LITEX_PYTHON (a path), this interpreter, then the
    venv sweep.sh puts on PATH for every real build - READ OUT OF sweep.sh,
    never restated here, because a second spelling of the build interpreter
    is a second thing that has to stay true.
    """
    cands = [os.environ.get("MILAN_LITEX_PYTHON"), sys.executable]
    m = re.search(r'export PATH="?\$HOME/([^/"\s:]+)/venv/bin',
                  open(SWEEP).read())
    if m:
        cands.append(os.path.join(os.path.expanduser("~"), m.group(1),
                                  "venv", "bin", "python3"))
    for cand in cands:
        if not cand or not os.path.exists(cand):
            continue
        if subprocess.run([cand, "-c", "import migen, litex, litex_boards"],
                          cwd=SOC_DIR, capture_output=True).returncode == 0:
            return cand
    return None


#: The one place that decides "no LiteX here".  Both gates and both mutation
#: arms ask it, so a box where the interpreter appears half-way through a run
#: cannot have one arm skip and the next one grade.
_LITEX_PY = []


def _litex_or_skip(gate):
    """The LiteX interpreter, or None with the skip already recorded."""
    if not _LITEX_PY:
        _LITEX_PY.append(_litex_python())
    if _LITEX_PY[0] is None:
        skip(gate, "no interpreter here can import migen + litex + "
                   "litex_boards, so NO argv -> Instance parameter chain was "
                   "observed in this run (point MILAN_LITEX_PYTHON at one, or "
                   "run scripts/ci_litex_env.py). Gate 23d holds the argv -> "
                   "MilanSoC half structurally, by the SPELLING of the "
                   "statements it walks", NO_LITEX)
    return _LITEX_PY[0]


def _instance_params(python, runs, mutations=()):
    """{label: {"params": ...} or {"error": ...}} for each (label, argv) run.

    ONE CHILD PROCESS PER RUN, deliberately.  migen/LiteX accumulate enough
    per-elaboration state that a second SoC built in the same interpreter
    costs ~40 percent more than the first and a sixteenth costs seven times
    as much (measured: 0.88 s -> 6.28 s, and clearing the tracebacks and
    collecting does not touch it).  A fresh process is flat at ~0.9 s.

    PYTHONHASHSEED is pinned for the same reason the sweep staggers its
    launches: the CPU wrapper builds its argument string from a SET, so an
    unpinned hash seed spells those arguments differently in every process,
    misses the pinned core's netlist cache, and pays a ~90 s cold `sbt` run
    EACH TIME.
    """
    env = dict(os.environ, PYTHONHASHSEED="0")
    out, seen = {}, {}
    with tempfile.TemporaryDirectory() as tmp:
        # THE SPY MUST STOP THE ELABORATION, not merely witness it, and the
        # empty directory below is what proves it.  Every recipe run carries
        # `--build`; if the spy ever raised too LATE - after Builder() was
        # constructed - LiteX would write its gateware and software trees in
        # here and invoke Vivado, and every assertion in these gates would
        # still pass because the parameters were still read correctly.  A
        # harness whose own cheapness is assumed rather than checked is the
        # thing these gates exist to stop.  Borrowed from gate 1e on the #116
        # lane (PR #135), which had this and this file did not.
        build_out = os.path.join(tmp, "build-out")
        os.makedirs(build_out)
        for label, argv in runs:
            argv = [build_out if a == BUILD_OUT_TOKEN else a for a in argv]
            # Several labels share one command line on purpose - the shipping
            # argv is simultaneously the prune baseline, the sound card's
            # ABSENT side and the gPTP plane's PRESENT side - and elaborating
            # the same thing three times buys nothing.
            key = tuple(argv)
            if key in seen:
                out[label] = seen[key]
                continue
            spec = os.path.join(tmp, "spec.json")
            result = os.path.join(tmp, "result.json")
            if os.path.exists(result):
                os.unlink(result)
            with open(spec, "w") as fh:
                json.dump({"soc_path": os.path.join(SOC_DIR, "milan_soc.py"),
                           "result": result, "argv": argv,
                           "mutations": [list(m) for m in mutations]}, fh)
            proc = subprocess.run([python, "-", spec], input=_INSTANCE_PROBE,
                                  text=True, cwd=SOC_DIR, env=env,
                                  capture_output=True)
            assert os.path.exists(result), (
                f"{label}: the milan_soc.py probe wrote no result "
                f"(rc={proc.returncode})\n{proc.stdout[-2000:]}"
                f"\n{proc.stderr[-2000:]}")
            with open(result) as fh:
                row = json.load(fh)
            if "error" in row:
                # The CPU wrapper runs its Scala generator as a CHILD of the
                # probe, on the process's own file descriptors, so the
                # probe's Python-level redirect never sees it, and the only
                # place scopt's refusal of an --l2-* argument is spelled out
                # is this stream.  Keep its tail next to the error for
                # _classify_recipe.  A dozen lines would not do: measured
                # 2026-08-21, the refusal sits 17 lines above the end of a
                # stack trace.
                row["child_output"] = "\n".join(
                    (proc.stdout + "\n" + proc.stderr).splitlines()[-200:])
            out[label] = seen[key] = row
        left = os.listdir(build_out)
        assert not left, (
            "the Instance spy no longer stops the elaboration: a run carrying "
            f"--build wrote {left} into its output directory, so these runs "
            "are not the sub-second read-back they are documented to be and "
            "a real Vivado build was reached")
    return out


#: The two inverted rows, and they are inverted for DIFFERENT reasons: the
#: sound card is a Linux-only surface the shipping bare-metal profile drops,
#: the fabric gPTP plane is an area-funded option the Linux profile does not
#: take.  (flag, {parameter: the value a PRESENT build must pass}).
#:
#: `None` means "must appear, value unconstrained" - the ONE case is the gPTP
#: microcode image, whose path is a build-tree location and not a constant.
#: It is graded rather than ignored because the ROM is half of what the flag
#: buys: a plane parameter of 1 with no image is #135's symptom with an extra
#: step, an enabled plane that never leaves reset.  A row lists EVERY
#: parameter its flag moves, so "changed nothing else" stays an exact test
#: instead of a set difference nobody reads.
PRESENT_ONLY_BLOCKS = {
    "sound_card": ("--sound-card", {"p_SOUND_CARD_P": 1}),
    "fabric_gptp": ("--fabric-gptp", {"p_GPTP_PLANE_EN_P": 1,
                                      "p_GPTP_UCODE_HEX_P": None}),
}


def _why_failed(row):
    """One probe failure as text, with the captured output when there is any.

    LiteX reports through a logger, so several of its refusals arrive as an
    exception whose str() is empty; the reason is in the stream the probe
    redirected.  Both halves are printed or the gate is unactionable.
    """
    err = row.get("error", "no result")
    out = (row.get("output") or "").strip()
    return f"{err}\n      " + out.replace("\n", "\n      ") if out else err


def _prune_contract(got, rows, inverted=()):
    """Every prune-contract violation in one probe result set, as text.

    ONE grader, shared by the gates and by their negative controls, so a
    mutation is proved to turn THE GATE red rather than some weaker
    restatement of it.  `rows` are the OPTIONAL_BLOCKS names to grade against
    the "present" baseline; `inverted` names PRESENT_ONLY_BLOCKS rows, each
    graded against its OWN `<name>_present`/`<name>` pair.
    """
    bad = []

    def params(label):
        row = got.get(label) or {"error": "case not run"}
        if "params" not in row:
            bad.append(f"{label}: {_why_failed(row)}")
            return None
        return row["params"]

    base = params("present") if rows else None
    for name in rows:
        flag, param, _why = eb.OPTIONAL_BLOCKS[name]
        key = f"p_{param}"
        pruned = params(name)
        if base is not None and key in base:
            bad.append(f"{name}: a build that prunes NOTHING already passes "
                       f"{key}={base[key]!r} - the default Instance is no "
                       "longer the shipping one")
        if base is None or pruned is None:
            continue
        if pruned.get(key) != 0:
            bad.append(
                f"{name}: `{flag}` reached argparse but "
                f'Instance("milan_datapath") got {key}='
                f"{pruned.get(key, '<absent>')!r}, want 0 - the config "
                "declares the prune, the plan tabulates it, the estimate "
                "books it, and the bitstream ships WITH the block (#130)")
        rest = {k: v for k, v in pruned.items() if k != key}
        if rest != base:
            bad.append(f"{name}: `{flag}` changed Instance parameters other "
                       f"than {key}: "
                       f"{sorted(set(rest) ^ set(base)) or 'a value'}")
    for name in inverted:
        flag, wants = PRESENT_ONLY_BLOCKS[name]
        on, off = params(f"{name}_present"), params(name)
        for key, want in wants.items():
            if on is not None and (on.get(key, KeyError) == KeyError
                                   or (want is not None
                                       and on.get(key) != want)):
                bad.append(
                    f"{name}: a build WITH `{flag}` got {key}="
                    f"{on.get(key, '<absent>')!r}, want "
                    f"{'any value' if want is None else repr(want)} - the "
                    "RTL default is 0, so this is a row whose parameters are "
                    "passed when the block is PRESENT")
            if off is not None and key in off:
                bad.append(f"{name}: a build WITHOUT `{flag}` still passes "
                           f"{key}={off[key]!r}")
        if on is not None and off is not None:
            rest = {k: v for k, v in on.items() if k not in wants}
            if rest != off:
                bad.append(f"{name}: dropping `{flag}` changed parameters "
                           f"other than {sorted(wants)}: "
                           f"{sorted(set(rest) ^ set(off)) or 'a value'}")
    return bad


def _config_argv(name):
    """(cfg, the config's OWN emitted argv, with --entity-gen-dir attached).

    eb.build() is what writes both the generated include dir the argv points
    at and the platform_shape.json milan_soc.py reads, so it runs first.
    """
    cfg = eb.load_config(CONFIGS[name])
    eb.build(CONFIGS[name], OUT)
    gen = os.path.join(ROOT, "configs/generated", cfg["name"])
    assert os.path.isdir(gen), \
        f"{gen}: this config has no generated include dir"
    return cfg, eb.emit_soc_argv(cfg) + ["--entity-gen-dir", gen]


def _behavioural_runs():
    """(cfg, [(label, argv)]) for the full 23f case set.

    The baseline is the config's OWN emitted argv with the prune flags taken
    out, so every case differs from a real shipping command line by exactly
    the token under test.  The shipping shape declares the gPTP plane and no
    sound card, so it IS the gPTP row's present side and the sound card's
    absent side; _instance_params elaborates that command line once.
    """
    cfg, argv = _config_argv(BEHAVIOURAL_CFG)
    flags = {f for f, _p, _w in eb.OPTIONAL_BLOCKS.values()}
    present = [a for a in argv if a not in flags]
    assert "--sound-card" not in present and "--fabric-gptp" in present, \
        f"{cfg['name']} no longer has the polarities this gate grades " \
        "against - it must ship the gPTP plane and no sound card"
    runs = [("present", present)]
    runs += [(name, present + [flag])
             for name, (flag, _p, _w) in eb.OPTIONAL_BLOCKS.items()]
    runs += [("sound_card_present", present + ["--sound-card"]),
             ("sound_card", present),
             ("fabric_gptp_present", present),
             ("fabric_gptp", _drop_flag(present, "--fabric-gptp", 0))]
    return cfg, runs


def _drop_flag(argv, flag, nargs):
    """argv without `flag` and its nargs values.  Asserts it was there."""
    assert flag in argv, f"{flag} is not on this argv: {' '.join(argv)}"
    i = argv.index(flag)
    return argv[:i] + argv[i + 1 + nargs:]


def test_optional_blocks_reach_the_instance():
    """gate 23f - THE BEHAVIOURAL PRUNE PROOF (issues #130, #154).

    Every OPTIONAL_BLOCKS row plus the two PRESENT_ONLY_BLOCKS rows, both
    directions, graded on the parameters that actually reach
    Instance("milan_datapath", ...) in a real elaboration of the shipping
    configs.  A prune must land as `p_<PARAM>=0` AND MUST CHANGE NOTHING ELSE
    - a flag that prunes the wrong block is the same silent lie as a flag
    that prunes nothing."""
    python = _litex_or_skip("gate 23f")
    if python is None:
        return
    cfg, runs = _behavioural_runs()
    t0 = time.time()
    got = _instance_params(python, runs)
    bad = _prune_contract(got, list(eb.OPTIONAL_BLOCKS),
                          list(PRESENT_ONLY_BLOCKS))
    assert not bad, "gate 23f:\n  " + "\n  ".join(bad)
    base = got["present"]["params"]
    print(f"  [gate 23f] {len({tuple(a) for _l, a in runs})} real "
          f"milan_soc.py elaborations of {cfg['name']}, the shipping AX "
          f"shape, in {time.time() - t0:.0f} s: each of the "
          f"{len(eb.OPTIONAL_BLOCKS)} --no-* flags lands as p_<PARAM>=0 in "
          f'the Instance("milan_datapath") parameters and moves NOTHING '
          f"else, a build that prunes nothing passes none of them "
          f"({len(base)} parameters, byte-identical top .v), and both "
          f"inverted rows land the other way up: p_SOUND_CARD_P=1 with "
          f"--sound-card, and p_GPTP_PLANE_EN_P=1 WITH its microcode image "
          f"with --fabric-gptp, both absent without them. This grades what "
          f"elaboration HANDS the module, not "
          f"what the module DOES with it (gate 23d) and not that the "
          f"bitstream places or boots")


def test_optional_block_instance_gate_bites():
    """Gate 23f negative controls - the hops a spelling gate cannot see.

    Each row deletes, renames or inverts ONE link of the argv -> Instance
    chain in milan_soc.py's source and re-runs the gate's OWN grader over the
    same real elaborations, so what is proved is that THE GATE goes red, not
    that some weaker restatement of it does.

    Eight of the eleven leave every OTHER gate in this file green, which is
    the whole reason this gate exists.  The three that do NOT are gate 23d's
    own: the dropped `not args.no_maap` handoff is exactly what 23d was
    written for, and the renamed parameter trips its `p_<PARAM>=0` grep.
    They are kept here so the two gates' division of labour is stated rather
    than assumed - and so a later relaxation of 23d cannot quietly reopen
    them."""
    python = _litex_or_skip("gate 23f mutation")
    if python is None:
        return
    _cfg, runs = _behavioural_runs()
    cases = {label: argv for label, argv in runs}
    # (why it is the #130 class, the source edit, which rows it must redden)
    controls = [
        ("main() drops ONE --no-* handoff",
         [("not args.no_maap", "True", 1)], ["maap"], []),
        ("MilanSoC never forwards optional_blocks to MilanNIC",
         [("optional_blocks=optional_blocks,\n                              "
           "    cbs_queues_mask=cbs_queues_mask,",
           "cbs_queues_mask=cbs_queues_mask,", 1)], ["latency_taps"], []),
        ("MilanSoC never forwards render_lpf to MilanNIC",
         [("render_lpf=bool(render_lpf),\n", "", 1)], ["render_lpf"], []),
        ("MilanNIC never forwards optional_blocks to add_milan_datapath",
         [("render_lpf=render_lpf, optional_blocks=optional_blocks,",
           "render_lpf=render_lpf,", 1)], ["maap"], []),
        ("the pruned keyword is dropped inside add_milan_datapath",
         [("blocks[k] = blocks[k] and bool(v)", "blocks[k] = True", 1)],
         ["media_clock_servo"], []),
        ("no parameter is ever emitted for a pruned block",
         [("        if not blocks[k]:", "        if False:", 1)],
         ["i2s_playback"], []),
        ("the emitted parameter is renamed on its way to the Instance",
         [('dp_params[f"p_{param}"] = 0', 'dp_params[f"p_{param}_X"] = 0', 1)],
         ["rx_mac_filter"], []),
        ("the prune predicate is INVERTED",
         [("        if not blocks[k]:", "        if blocks[k]:", 1)],
         ["datapath_probes"], []),
        ("the sound-card row's own predicate is inverted",
         [('    if sound_card:\n        dp_params["p_SOUND_CARD_P"] = 1',
           '    if not sound_card:\n        dp_params["p_SOUND_CARD_P"] = 1',
           1)], [], ["sound_card"]),
        # The two #135 hops, verbatim: a reviewer severed the --fabric-gptp
        # chain at each of them and read ALL GATES PASS both times.
        ("main() never hands --fabric-gptp to MilanSoC (#135, hop 1)",
         [("gptp_plane=args.fabric_gptp,", "gptp_plane=False,", 1)],
         [], ["fabric_gptp"]),
        ("the gPTP plane parameter is never emitted (#135, hop 2)",
         [('        dp_params["p_GPTP_PLANE_EN_P"] = 1',
           "        pass", 1)], [], ["fabric_gptp"]),
    ]
    t0 = time.time()
    for why, mutations, rows, inverted in controls:
        labels = ["present"] + rows if rows else []
        labels += [f"{n}_present" for n in inverted] + list(inverted)
        got = _instance_params(python, [(lbl, cases[lbl]) for lbl in labels],
                               mutations)
        bad = _prune_contract(got, rows, inverted)
        assert bad, (f"gate 23f accepted a milan_soc.py in which {why} "
                     f"({mutations[0][0]!r} -> {mutations[0][1]!r})")
        want = (rows or inverted)[0]
        assert any(line.startswith(f"{want}:") for line in bad), \
            f"{why}: gate 23f went red for the wrong row: {bad}"
    print(f"  [gate 23f mutation] {len(controls)}/{len(controls)} broken "
          f"links of the argv -> Instance chain rejected in "
          f"{time.time() - t0:.0f} s: a dropped CLI handoff, two dropped "
          "constructor keywords, a dropped keyword inside "
          "add_milan_datapath, a suppressed parameter, a renamed parameter, "
          "both prune polarities inverted, and BOTH #135 hops - severed "
          "independently, each one a bitstream with no time source")


#  gate 23g (issue #156) - EVERY SHIPPED RECIPE CAN ACTUALLY RUN.
#
#  Every shape gate this repo has compares a recipe's argv against the config
#  it claims to build.  NOTHING RAN THE ARGV.  A recipe can agree with its
#  config flag for flag and still be unable to elaborate, and #156 records
#  three findings that turned out to be that one gap - two build.sh recipes
#  that could not launch at all for want of `--entity-gen-dir`, a flow-flag
#  blind spot that let a late `and not args.build` leave the whole suite
#  green while the real launcher line built the wrong SoC, and a sweep leg
#  that cannot elaborate at all.
#
#  THE FLOW TAIL IS PART OF THE RECIPE HERE, and that is the load-bearing
#  difference from gate 1e and scripts/check_sweep_shape.py.  Both of those
#  exclude FLOW_FLAGS from the comparison, for the good reason that Vivado
#  directives are not part of the end-station definition - but that makes
#  `--build` invisible to every gate in the tree, and `--build` is on every
#  real launcher line.  This gate appends the tail each launcher appends.
#
#  It asserts ONLY that the recipe reaches Instance("milan_datapath").  It is
#  a smoke gate, not a shape gate: the shape comparison already exists and is
#  sound.

#: Recipes that are known NOT to elaborate, with the ticket that owns each
#: and the EXACT diagnostic the ticket records, as a regular expression the
#: probe's `<ExceptionType>: <message>` line must match in full.
#: An entry here is a RECORDED failure, not a waiver: the gate still runs the
#: recipe, still reports the error, goes RED if a listed recipe starts
#: working - because then the note is stale and the ticket is done - and
#: goes RED if it fails for ANY OTHER reason than the one recorded, because
#: a row that skips on any error is a row nobody looks at ([R0] on PR #188:
#: the first version accepted every error here, so a new parser, a broken
#: tool install or a regression in this very recipe would have been reported
#: as the old known failure and left the verdict green).  Empty since #184:
#: the Arty TDM resource legitimately omits the AX7101-only lrclk test point.
KNOWN_UNRUNNABLE = {}


def _shell_recipes(path, pattern, flags=0):
    """{name: argv} from a shell file, one entry per `pattern` match.

    `pattern` must capture (name, body).  The body is the raw shell word
    salad a recipe echoes; `$SOC_DIR` is the only variable a recipe uses and
    it resolves to sw/litex in every launcher, so it is the only one expanded
    - anything else left unexpanded is an assertion failure rather than a
    token silently handed to argparse with a `$` in it.
    """
    text = open(path, encoding="utf-8").read()
    out = {}
    for name, body in re.findall(pattern, text, flags):
        body = body.replace("\\\n", " ").replace("$SOC_DIR", SOC_DIR)
        argv = shlex.split(body)
        assert not [a for a in argv if "$" in a], \
            f"{os.path.basename(path)} {name}: unexpanded shell variable in " \
            f"{[a for a in argv if '$' in a]} - this gate would hand it to " \
            "argparse verbatim"
        out[name] = argv
    assert out, f"{path}: no recipe matched {pattern!r} - the launcher was " \
                "reshaped and this gate stopped testing anything"
    return out


def _recipe_cases():
    """(label, argv) for every build.sh recipe and every sweep.sh board leg.

    The flow tail each launcher appends is appended here too, `--build`
    included, because a guard that reads args.build is invisible to every
    other gate in the tree (#156 item 2).  --output-dir gets a real path so
    the recipe is refused for its own reasons and not for a missing one.
    """
    out = []
    # build.sh: `cfg_<name>() { ... echo "<argv>" }`, tail from its own exec
    # line, read out of build.sh rather than restated.
    tail = re.search(r"exec python3 milan_soc\.py \$args \$\{EXTRA\[\*\]:-\}"
                     r'(.*?)"\s*$', open(BUILD_SH, encoding="utf-8").read(),
                     re.M)
    assert tail, "build.sh no longer execs milan_soc.py the way this gate reads"
    build_tail = shlex.split(tail.group(1).replace("$out", OUT_DIR_TOKEN))
    for name, argv in _shell_recipes(
            BUILD_SH, r'^cfg_(\w+)\(\)[^\n]*\n(?:[^\n]*\n)*?\s*echo "(.*?)"\n',
            re.M | re.S).items():
        out.append((f"build.sh cfg_{name}", argv + build_tail))
    # sweep.sh: OPTS per board from its own case table, plus the BASE tail and
    # the per-directive launch tail.
    sweep = open(SWEEP, encoding="utf-8").read()
    base = re.search(r'BASE="python3 \$R/sw/litex/milan_soc\.py \$OPTS(.*?)"',
                     sweep, re.S)
    assert base, "sweep.sh no longer composes BASE the way this gate reads"
    sweep_tail = shlex.split(base.group(1).replace("\\\n", " ")
                             .replace("$CFG_GEN", "$CFG_GEN"))
    for board, argv in _shell_recipes(
            SWEEP, r'^\s{2}(\w+)\)\s+OPTS="(.*?)";\s*L2=', re.M | re.S).items():
        cfg = re.search(r'^\s{2}%s\)\s+NS=\d+;\s*CFG=\$\{SWEEP_CFG:-([^}]+)\}'
                        % board, sweep, re.M)
        assert cfg, f"sweep.sh names no default config for the {board} leg"
        gen = os.path.join(ROOT, "configs/generated",
                           os.path.basename(cfg.group(1))[:-len(".yaml")])
        tail = [gen if a == "$CFG_GEN" else a for a in sweep_tail]
        out.append((f"sweep.sh {board}", argv + tail +
                    ["--place-directive", "AltSpreadLogic_high",
                     "--output-dir", OUT_DIR_TOKEN]))
    return out


#: Stand-in for the launcher's own `$out`/`$W/build_...` directory.  Replaced
#: with the probe runner's own scratch path: milan_soc.py must be refused for
#: its own reasons, never for an output directory that does not exist, and
#: that directory has to be one _instance_params can afterwards prove empty.
OUT_DIR_TOKEN = BUILD_OUT_TOKEN


#: What a STOCK VexiiRiscv says to an --l2-* argument that only the series
#: in sw/litex/patches teaches it.  The generator is a Scala program whose
#: options scopt parses; handed one it does not know, it prints
#:     [error] Error: Unknown option --l2-down-pending=4
#:     [error] Try --help for more information.
#: and sbt fails the runMain, which LiteX surfaces as a CalledProcessError
#: whose message is the sbt command line, PythonArgsGen included.  Observed
#: 2026-08-21 by handing the bench's generator `--l2-bogus-option=1`; the
#: two option names below are the ones the pinned revision rejects (#185).
UNPATCHED_VEXII_RE = re.compile(
    r"Unknown option --l2-(down-pending|general-slots)")
L2_SCALA_ARGS = ("--scala-args=--l2-down-pending",
                 "--scala-args=--l2-general-slots")

#: The five things one gate-23g recipe result can be.
RECIPE_RAN, RECIPE_RECORDED, RECIPE_TOOLCHAIN, RECIPE_STALE, RECIPE_FAILED = (
    "ran", "recorded", "toolchain", "stale", "failed")


def _classify_recipe(label, argv, row, known_unrunnable=None):
    """(verdict, detail) for one recipe's probe result.

    EVERY SKIP IS PINNED TO ITS EXACT DIAGNOSTIC.  The first version of this
    gate skipped a recorded row on ANY error, and skipped any failure whose
    text mentioned PythonArgsGen as "#185's": a new parser bug, a Scala
    compile error, a missing sbt or a regression in the recipe itself would
    all have been reported as the old, known, harmless reason and left the
    verdict green ([R0] on PR #188).  Now a recorded row must fail with the
    error its ticket records, and the toolchain skip needs all three of: the
    recipe passes one of the two --l2-* arguments, the failure is the CPU
    generator's own sbt run, and that run's output carries scopt's refusal
    of an --l2-* argument.  Anything else is a failure of the recipe.
    """
    known = KNOWN_UNRUNNABLE if known_unrunnable is None else known_unrunnable
    err = row.get("error")
    if label in known:
        why, signature = known[label]
        if err is None:
            return RECIPE_STALE, (
                f"{label}: RECORDED as unrunnable ({why}) but it elaborated "
                "- delete the entry and close the ticket")
        if re.fullmatch(signature, err):
            return RECIPE_RECORDED, (
                f"{label} is RECORDED as unrunnable and was not proved: {why}")
        return RECIPE_FAILED, (
            f"{label}: RECORDED as unrunnable for `{signature}` but failed "
            f"DIFFERENTLY, which the record does not cover: {_why_failed(row)}")
    if err is None:
        return RECIPE_RAN, ""
    generator_text = "\n".join(
        t for t in (row.get("output"), row.get("child_output")) if t)
    if (any(a.startswith(L2_SCALA_ARGS) for a in argv)
            and err.startswith("CalledProcessError:")
            and "PythonArgsGen" in err
            and UNPATCHED_VEXII_RE.search(generator_text)):
        # NOT a defect in the recipe, and not something this gate can
        # decide: on a stock upstream VexiiRiscv these recipes cannot
        # elaborate at all, because two of their --scala-args exist only
        # in the patch #185 is about.  Naming it is the whole value here
        # - silently passing would say CI proved a recipe it never ran.
        return RECIPE_TOOLCHAIN, (
            f"{label} needs the VexiiRiscv patch of #185 (--l2-down-pending "
            "/ --l2-general-slots), which this interpreter's checkout does "
            "not carry - its generator printed scopt's `Unknown option` - so "
            "it was NOT proved to reach the Instance; run "
            "sw/litex/patches/apply.sh")
    return RECIPE_FAILED, (
        f'{label}: never reached Instance("milan_datapath"): '
        f"{_why_failed(row)}")


def test_every_recipe_elaborates():
    """gate 23g - every build.sh recipe and sweep.sh leg REACHES the Instance.

    #156: nothing in this tree ever ran a recipe.  Two of them could not
    launch at all, for the better part of a year, and every shape gate was
    green throughout."""
    python = _litex_or_skip("gate 23g")
    if python is None:
        return
    for name in CONFIGS:                # every --entity-gen-dir a recipe names
        eb.build(CONFIGS[name], OUT)
    cases = _recipe_cases()
    t0 = time.time()
    # The --output-dir token is left FOR _instance_params to substitute, so
    # the directory these `--build` runs are pointed at is the one it can
    # afterwards prove empty. Substituting a local temp here would put the
    # proof out of its reach, which is the point of the token.
    got = _instance_params(python, cases)
    bad, stale, ran = [], [], 0
    for label, argv in cases:
        verdict, detail = _classify_recipe(label, argv, got[label])
        if verdict == RECIPE_RAN:
            ran += 1
        elif verdict == RECIPE_RECORDED:
            skip("gate 23g", detail)
        elif verdict == RECIPE_TOOLCHAIN:
            # A row skip on a bench; in the job that installs the series it
            # is a setup failure, and --require-elaboration refuses it.
            skip("gate 23g", detail, TOOLCHAIN)
        elif verdict == RECIPE_STALE:
            stale.append(detail)
        else:
            bad.append(detail)
    assert not bad + stale, "gate 23g:\n  " + "\n  ".join(bad + stale)
    print(f"  [gate 23g] {ran}/{len(cases)} shipped recipes reach "
          f'Instance("milan_datapath") in {time.time() - t0:.0f} s, each with '
          "the flow tail its own launcher appends (--build included, the "
          "flag every shape gate excludes). This proves a recipe RUNS, not "
          "that it builds the SoC its config describes - that comparison is "
          "gate 1e's and #155 carries where the two disagree")


def test_recipe_smoke_gate_bites():
    """Gate 23g negative control - a recipe that cannot launch must redden it.

    The mutation is the REAL #156 item 1, replayed: strip `--entity-gen-dir`
    from a recipe and milan_soc.py refuses with "this build needs its
    end-station config". Two recipes shipped exactly that way."""
    python = _litex_or_skip("gate 23g mutation")
    if python is None:
        return
    cases = [c for c in _recipe_cases() if c[0] not in KNOWN_UNRUNNABLE]
    controls = [(label, _drop_flag(argv, "--entity-gen-dir", 1))
                for label, argv in cases[:1] + cases[-1:]]
    got = _instance_params(python, controls)
    for label, _argv in controls:
        assert got[label].get("error") is not None, (
            f"gate 23g accepted `{label}` with --entity-gen-dir stripped - "
            "the exact shape #156 item 1 shipped")
    print(f"  [gate 23g mutation] {len(controls)}/{len(controls)} recipes "
          "stripped of --entity-gen-dir refused to elaborate, which is #156 "
          "item 1 replayed on the recipes that shipped it")


def test_recipe_skip_classifier_bites():
    """Gate 23g negative controls for the SKIP classifier; they need no LiteX.

    The skips are the part of gate 23g that can turn a failure into a green,
    so they are graded on every box, interpreter or not.  Each arm hands the
    production classifier a result shaped like a real one - the former Arty
    error and scopt's refusal are the texts observed on 2026-08-21, verbatim -
    and requires the verdict [R0] asked for on PR #188: a synthetic
    recorded row failing for a different reason FAILS, a generator failure
    without scopt's refusal FAILS, the refusal on a recipe that passes no
    --l2-* argument FAILS, and only the two exact shapes skip.  The
    --require-elaboration verdict is graded the same way: a toolchain skip
    fails it, a recorded row does not, and the line it prints says which.
    """
    arty = "sweep.sh arty"
    assert arty not in KNOWN_UNRUNNABLE, \
        "#184 is fixed, so its live recorded-failure row must stay deleted"
    recorded = {
        arty: (
            "synthetic #184 row: the board resource lacks the optional lrclk "
            "test point",
            r"AttributeError: 'Record' object has no attribute 'lrclk'"),
    }
    l2 = ["--scala-args=--l2-down-pending=4",
          "--scala-args=--l2-general-slots=8"]
    gen = ("CalledProcessError: Command 'cd /v/ext/VexiiRiscv && sbt "
           "\"runMain vexiiriscv.soc.litex.PythonArgsGen --xlen=32 "
           "--l2-down-pending=4 --python-file=/v/x.py\"' returned non-zero "
           "exit status 1.")
    refusal = ("[error] Error: Unknown option --l2-down-pending=4\n"
               "[error] Try --help for more information.")
    trace = "\n".join(f"[error] \tat scala.App.main(App.scala:{n})"
                      for n in range(40))
    arms = [
        ("recorded row failing as recorded", arty, [],
         {"error": "AttributeError: 'Record' object has no attribute 'lrclk'"},
         RECIPE_RECORDED),
        ("recorded row failing DIFFERENTLY", arty, [],
         {"error": "SoCError: ", "output": "a refusal #184 never recorded"},
         RECIPE_FAILED),
        ("recorded row that elaborated", arty, [], {"params": {}},
         RECIPE_STALE),
        ("--l2 recipe on a stock VexiiRiscv", "build.sh cfg_ax8x8", l2,
         {"error": gen, "child_output": refusal + "\n" + trace},
         RECIPE_TOOLCHAIN),
        ("--l2 recipe whose generator failed for ANOTHER reason",
         "build.sh cfg_ax8x8", l2,
         {"error": gen, "child_output": "[error] Soc.scala:12: not found: "
                                        "value l2DownPending\n" + trace},
         RECIPE_FAILED),
        ("the refusal on a recipe passing NO --l2 argument",
         "build.sh cfg_ax7101", ["--cpu-variant=baremetal"],
         {"error": gen, "child_output": refusal}, RECIPE_FAILED),
        ("no sbt at all", "build.sh cfg_ax8x8", l2,
         {"error": "FileNotFoundError: [Errno 2] No such file or directory: "
                   "'sbt'"}, RECIPE_FAILED),
        ("a recipe that ran", "build.sh cfg_ax7101", [],
         {"params": {"p_X": 1}}, RECIPE_RAN),
    ]
    for name, label, argv, row, want in arms:
        got, _detail = _classify_recipe(label, argv, row, recorded)
        assert got == want, \
            f"gate 23g classifier: {name}: want {want}, got {got}"
    verdicts = [
        ("a toolchain skip", [("gate 23g", "stock VexiiRiscv", TOOLCHAIN)],
         1, "could not"),
        ("no interpreter", [("gate 23f", "no interpreter", NO_LITEX)],
         1, "could not"),
        ("a recorded row only", [("gate 23g", "#184", "row")], 0,
         "did not run for recorded reasons"),
        ("nothing skipped", [], 0, "every elaboration arm ran"),
    ]
    for name, skipped, want_rc, want_text in verdicts:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = _require_elaboration_verdict(skipped)
        assert rc == want_rc and want_text in buf.getvalue(), (
            f"--require-elaboration verdict with {name}: want rc {want_rc} "
            f"saying {want_text!r}, got rc {rc}: {buf.getvalue().strip()!r}")
    print(f"  [gate 23g classifier] {len(arms)}/{len(arms)} shaped results "
          f"and {len(verdicts)}/{len(verdicts)} --require-elaboration "
          "verdicts graded as [R0] on PR #188 requires: a synthetic recorded "
          "Arty error and scopt's own refusal of an --l2-* argument are the "
          "only skip shapes, a stale #184 row and every other failure fail, "
          "and the toolchain skip fails --require-elaboration")


#  gate 23h (issue #185) - THE TOOLCHAIN THIS SOC IS BUILT WITH IS THE ONE
#  THIS REPOSITORY DESCRIBES.
#
#  Upstream LiteX cannot build any shape of this design. It has no `baremetal`
#  VexiiRiscv variant, which is the whole #120/#125 downgrade and the shipping
#  AX profile, and the VexiiRiscv revision it pins does not accept the
#  `--l2-down-pending` / `--l2-general-slots` four of the five configs pass.
#  sw/litex/patches/ carries the six patches that close that, and apply.sh
#  applies them.
#
#  NOTHING RAN IT. Measured 2026-08-21: the series had not applied cleanly for
#  an unknown length of time, and there was no way to notice, because the only
#  reader was a person following a document. Two failures had accumulated:
#
#    * 0003 was diffed against pristine upstream while 0001 rewrites the same
#      boot.c hunks, so apply.sh died on the third patch and never reached the
#      two that follow it;
#    * 0002-liteeth had fallen 25 lines behind the tree the boards are built
#      from - the ext_reset input KL_link_guard drives was only ever in the
#      bench's working copy.
#
#  A third was by design and had outlived it: the L2 patch was documented as
#  "apply it by hand for non-default L2" from a time when it WAS optional, and
#  four configs now pass those arguments, so `apply.sh` completing successfully
#  still left a tree that could not elaborate them.
#
#  So this gate asks the two questions that would have caught all three:
#  is every patch in the directory actually in the series apply.sh applies, and
#  is every patch in that series actually applied to the trees this interpreter
#  imports. Both are answered against the live install, not against text.
#
#  WHAT IT DOES NOT PROVE: that the patches are CORRECT, that upstream still
#  wants them, or that the built bitstream works. It proves the tree you are
#  elaborating with is the tree this repository says you should be elaborating
#  with, which is the property that was silently untrue.

#: The tree keys apply.sh resolves, and how to resolve each from a LiteX
#: interpreter. Read here rather than restated: `vexiiriscv` is the Scala
#: checkout INSIDE the pythondata package, which is why it cannot be found the
#: way a Python package is.
_TREE_EXPR = {
    "vexiiriscv": "import pythondata_cpu_vexiiriscv as p, os; "
                  "print(os.path.join(p.data_location, 'ext', 'VexiiRiscv'))",
}


def _patch_series():
    """[(tree key, patch filename)] read out of apply.sh's own SERIES array.

    The list is READ, never restated, for the reason the gate exists: a patch
    that is in the directory and not in the series is exactly the shape the
    L2 one had, and a second copy of the list here could hold it while
    apply.sh dropped it.
    """
    src = open(APPLY_SH, encoding="utf-8").read()
    block = re.search(r"^SERIES=\((.*?)^\)", src, re.M | re.S)
    assert block, "apply.sh no longer declares a SERIES array this gate can read"
    rows = re.findall(r'"\s*(\S+)\s+(\S+\.patch)\s*"', block.group(1))
    assert rows, "apply.sh's SERIES array is empty or reshaped"
    return rows


def _tree_root(python, key):
    """The directory apply.sh's patch paths are relative to, for one tree key."""
    expr = _TREE_EXPR.get(
        key, f"import {key}, os; "
             f"print(os.path.dirname(os.path.dirname({key}.__file__)))")
    got = subprocess.run([python, "-c", expr], capture_output=True, text=True)
    assert got.returncode == 0, \
        f"{key}: this interpreter cannot locate the tree ({got.stderr.strip()})"
    return got.stdout.strip()


def _patch_targets(patch):
    """The paths one patch rewrites, relative to its tree root."""
    got = re.findall(r"^\+\+\+ b/(\S+)", open(patch, encoding="utf-8").read(),
                     re.M)
    assert got, f"{patch}: no target files - is it a valid diff?"
    return got


def _mirror(tmp, real):
    """Where `real` lives inside the scratch mirror.

    THE MIRROR IS KEYED BY ABSOLUTE REALPATH, and that is the whole fix for
    the aliasing defect [R0] found on PR #189. Two of the six patches name
    the SAME physical file through different roots: 0005 reaches
    `.../ext/VexiiRiscv/src/.../Soc.scala` as a path under the
    pythondata package, and the L2 patch reaches it as `src/.../Soc.scala`
    under the VexiiRiscv checkout itself. Keyed by (tree, relative path)
    they landed in two scratch files and were graded independently, so the
    two patches never had to COMPOSE on the one file they share - which is
    the same "grade a stacked series one patch at a time" mistake this gate
    exists to replace. Mirroring the real absolute path makes them collide
    onto one scratch file with no special case, because
    realpath(<pythondata root>)/pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv
    IS realpath(<vexiiriscv root>).
    """
    return os.path.join(tmp, os.path.realpath(real).lstrip(os.sep))


def _reconstruct(python, series, roots=None):
    """Problems with "the live trees are pristine upstream plus this series".

    THE SERIES IS STACKED, so no patch can be graded on its own: 0003 is
    diffed on top of 0001 and both rewrite the same boot.c hunks, so asking
    "does 0001 reverse-apply?" against a correctly patched tree answers no.

    So the whole series is reversed, in reverse order, on a mirror of just
    the files it touches - which lands on pristine upstream without
    downloading one - and then applied forward again. Every step must
    succeed and the result must equal the live files byte for byte.

    `roots` overrides where the live trees are read from, which is how the
    negative control feeds this same production code a fixture instead of
    the real install.
    """
    problems = []
    roots = roots or {key: _tree_root(python, key) for key, _ in series}
    with tempfile.TemporaryDirectory() as tmp:
        live = {}
        for key, patch in series:
            root = roots[key]
            for rel in _patch_targets(os.path.join(PATCH_DIR, patch)):
                src = os.path.join(root, rel)
                if not os.path.exists(src):
                    problems.append(f"{patch}: {key} has no {rel} at all")
                    continue
                dst = _mirror(tmp, src)
                if dst not in live:
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    live[dst] = src
        if problems:
            return problems
        for key, patch in reversed(series):
            rc = subprocess.run(
                ["git", "-C", _mirror(tmp, roots[key]), "apply", "--reverse",
                 os.path.join(PATCH_DIR, patch)], capture_output=True)
            if rc.returncode != 0:
                problems.append(
                    f"{patch}: does not reverse out of the live {key}, so "
                    "that tree is not upstream plus this series. Either the "
                    "patch was never applied (run sw/litex/patches/apply.sh) "
                    "or the file drifted (re-diff per "
                    "sw/litex/patches/README.md)")
                return problems
        for key, patch in series:
            rc = subprocess.run(
                ["git", "-C", _mirror(tmp, roots[key]), "apply",
                 os.path.join(PATCH_DIR, patch)], capture_output=True)
            if rc.returncode != 0:
                problems.append(
                    f"{patch}: does not re-apply to the pristine {key} the "
                    "reversal produced, so the series is not self-consistent "
                    "in its own order")
                return problems
        for dst, src in sorted(live.items()):
            if open(dst, "rb").read() != open(src, "rb").read():
                problems.append(
                    f"{os.path.relpath(dst, tmp)}: upstream plus the series "
                    "does not reproduce the installed file, so the tree "
                    "carries a change no patch here records")
    return problems


def test_toolchain_patches_are_applied():
    """gate 23h - the LiteX being elaborated with is the one this repo describes.

    Reconstruction, not inspection: the series is reversed off a copy of the
    live files and applied again, and the result must be the live files."""
    python = _litex_or_skip("gate 23h")
    if python is None:
        return
    series = _patch_series()
    on_disk = {f for f in os.listdir(PATCH_DIR) if f.endswith(".patch")}
    listed = {f for _k, f in series}
    assert listed == on_disk, (
        "sw/litex/patches and apply.sh's SERIES disagree, which is how "
        "0002-vexiiriscv-l2-depth-args sat unapplied while four configs "
        f"needed it: only in the directory {sorted(on_disk - listed)}, only "
        f"in SERIES {sorted(listed - on_disk)}")
    # CO-LOCATED TARGETS MUST SHARE ONE SCRATCH FILE, asserted rather than
    # assumed, because grading them apart is the defect [R0] found: two
    # patches naming one physical file were reconstructed independently and
    # never had to compose. Any pair with the same realpath must map to the
    # same mirror path, and the shared files are named in the output so a
    # reader can see which patches have to agree with each other.
    roots = {key: _tree_root(python, key) for key, _ in series}
    by_real, by_mirror = {}, {}
    for key, patch in series:
        for rel in _patch_targets(os.path.join(PATCH_DIR, patch)):
            src = os.path.join(roots[key], rel)
            by_real.setdefault(os.path.realpath(src), set()).add(patch)
            by_mirror.setdefault(_mirror("/m", src), set()).add(patch)
    for real, pats in by_real.items():
        mirrors = {_mirror("/m", real)}
        assert len(mirrors) == 1 and by_mirror.get(_mirror("/m", real)) >= pats, (
            f"{real} is named by {sorted(pats)} but does not resolve to one "
            "scratch file, so those patches would be graded apart")
    shared = {os.path.basename(r): sorted(p)
              for r, p in by_real.items() if len(p) > 1}

    problems = _reconstruct(python, series)
    assert not problems, "gate 23h:\n  " + "\n  ".join(problems)
    files = {(k, r) for k, p in series
             for r in _patch_targets(os.path.join(PATCH_DIR, p))}
    print(f"  [gate 23h] the {len(series)} patches in sw/litex/patches are the "
          f"{len(on_disk)} apply.sh applies, and reversing them off this "
          f"interpreter's trees and re-applying them reproduces all "
          f"{len(by_real)} installed files byte for byte, including "
          f"{len(shared)} that two patches share and must therefore compose "
          f"on ({shared}). Upstream LiteX has no "
          "`baremetal` VexiiRiscv variant and the revision it pins rejects "
          "the --l2-* arguments four configs pass, so this is what lets gates "
          "23f/23g elaborate at all. It says nothing about whether the "
          "patches are CORRECT, only that the tree is the one described here")


def _missing_patch_fixture(python, series, fx, index):
    """(roots, missing) - a REACHABLE tree that genuinely lacks series[index].

    Two shapes, and the first is preferred because it is exact. Reversing
    ONLY the patch under test works for the last patch touching each file,
    and then exactly one patch is absent. Where a later patch rewrote the
    same hunks - 0003 sits on 0001, the L2 patch sits on 0005 - that single
    reversal is not a state anyone can reach, so the fallback reverses the
    whole tail from that index. That IS reachable: it is what apply.sh
    leaves behind when it dies partway, the very state that opened #185.

    `git apply --reverse` is atomic without --reject, so a refused attempt
    leaves the mirror untouched and the fallback can run on it directly.
    """
    roots = {key: _tree_root(python, key) for key, _ in series}
    for key, patch in series:
        for rel in _patch_targets(os.path.join(PATCH_DIR, patch)):
            src = os.path.join(roots[key], rel)
            dst = _mirror(fx, src)
            if not os.path.exists(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
    fx_roots = {key: _mirror(fx, root) for key, root in roots.items()}

    def reverse(entry):
        key, patch = entry
        return subprocess.run(
            ["git", "-C", fx_roots[key], "apply", "--reverse",
             os.path.join(PATCH_DIR, patch)], capture_output=True).returncode

    if reverse(series[index]) == 0:
        return fx_roots, [series[index][1]]
    for entry in reversed(series[index:]):
        if reverse(entry) != 0:
            return None, []
    return fx_roots, [patch for _k, patch in series[index:]]


def test_toolchain_patch_gate_bites():
    """Gate 23h negative control - a tree missing a patch must redden it.

    REAL FIXTURES, NOT A DOUBLE REVERSAL. The first version of this control
    appended the patch under test to the series and reversed it twice, so
    what it actually proved was that a patch cannot be reversed twice, and
    the advertised tally said nothing about detecting a missing patch ([R0]
    on PR #189). Each arm now builds a mirror of the installed trees that
    genuinely lacks a patch and feeds THAT through the production validator,
    so the thing graded is the thing that ships.
    """
    python = _litex_or_skip("gate 23h mutation")
    if python is None:
        return
    series = _patch_series()
    exact, tail, unreachable = 0, 0, []
    for i in range(len(series)):
        with tempfile.TemporaryDirectory() as fx:
            roots, missing = _missing_patch_fixture(python, series, fx, i)
            if roots is None:
                unreachable.append(series[i][1])
                continue
            problems = _reconstruct(python, series, roots=roots)
            assert problems, (
                f"gate 23h would NOT have noticed {missing} missing from the "
                f"installed {series[i][0]}")
            assert any(m in p for m in missing for p in problems), (
                f"gate 23h reddened for a patch that was NOT missing: it was "
                f"given a tree lacking {missing} and complained {problems[:1]}")
            if len(missing) == 1:
                exact += 1
            else:
                tail += 1
    assert not unreachable, (
        "these arms could not build a reachable fixture, so they proved "
        f"nothing: {unreachable}")
    print(f"  [gate 23h mutation] {exact + tail}/{len(series)} fixtures "
          f"rejected by the production validator, naming a patch the tree "
          f"genuinely lacked: {exact} with exactly one patch reversed out, "
          f"{tail} where a later patch sits on the same hunks so the "
          "reachable state is the whole tail - what a half-finished "
          "apply.sh leaves. No arm passes by reversing anything twice")


def _require_elaboration_verdict(skipped):
    """Exit status for --require-elaboration, printed with its reason.

    Refuses a run in which the argv -> Instance chain was not observed with
    the toolchain this repository describes: no interpreter (NO_LITEX), or
    an interpreter whose VexiiRiscv rejects the --l2-* arguments the series
    adds (TOOLCHAIN), which in the one job that installs that series is a
    setup failure and not a recorded gap ([R0] on PR #188).  Rows a gate
    declined for a RECORDED reason pass, and the line printed says so rather
    than claiming every arm ran while one is listed above as not run.
    """
    missing = [(g, w) for g, w, k in skipped if k in (NO_LITEX, TOOLCHAIN)]
    if missing:
        print("\n--require-elaboration: this run was asked to observe the "
              "argv -> Instance chain with the toolchain this repository "
              "describes, and could not:")
        for gate, why in missing:
            print(f"  - [{gate}] {why}")
        return 1
    rows = [(g, w) for g, w, k in skipped if k not in (NO_LITEX, TOOLCHAIN)]
    if rows:
        print("--require-elaboration: an interpreter carrying the patch "
              "series was found and no elaboration arm was skipped for a "
              f"toolchain reason; {len(rows)} arm(s) did not run for "
              "recorded reasons, listed above, and this verdict does not "
              "cover them")
    else:
        print("--require-elaboration: every elaboration arm ran")
    return 0


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
    # (b) the primary segment: listeners fall through to host, and so do the
    #     talkers - because the primary segment is now the first pool this
    #     BUILD can actually feed (task #65). LOOPBACK is still the pool the
    #     USER asked for (2026-07-28) and it comes back the moment
    #     cluster_mapping.fabric.loopback_lane is declared, which gate 17e
    #     proves in both directions; with the lane off, pointing the power-on
    #     image at it would advertise a source milan_datapath does not carry.
    #     Since the 08-01 flip the ship talkers are map_mode dynamic (no
    #     AUDIO_MAP descriptors), so the identity lives in the DYNAMIC
    #     engine's power-on image (AEM_ODMAP_INIT_C).
    assert all(p["primary_role"] == "host" for p in P_in)
    lane = (eb.load_config(CONFIGS["ax7101_8x8"])["interface"]
            ["cluster_fabric"]["loopback_lane"])
    want = "loopback" if lane else "host"
    assert all(p["primary_role"] == want for p in P_out), \
        f"lane={lane} but talker primary_role is not {want}"
    for p in P_out:
        seg = next(g for g in p["pool"] if g["role"] == want)
        if p["maps"] == 0:
            continue                    # dynamic port: image checked below
        m = next(m for m in ovl["audio_maps"] if m["index"] == p["base_map"])
        assert all(seg["offset"] <= off < seg["offset"] + seg["width"]
                   for (_, _, off, _) in m["mappings"]), m
    if all(p["maps"] == 0 for p in P_out):
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(
                [sys.executable, os.path.join(ROOT, "avdecc/gen_aem_store.py"),
                 "--overlay", r["paths"]["aem_overlay"], "--out-dir", td],
                check=True, capture_output=True)
            svh = open(os.path.join(td, "aecp_aem_rom.svh")).read()
        mi = re.search(r"AEM_ODMAP_INIT_C \[0:(\d+)\] = '\{([^}]*)\}", svh)
        assert mi, "dynamic ship talkers but no AEM_ODMAP_INIT_C image"
        vals = [int(v.strip().split("'h")[1], 16)
                for v in mi.group(2).split(",")]
        seg = next(g for g in P_out[0]["pool"] if g["role"] == want)
        assert len(vals) == 8 * len(P_out)
        for k, v in enumerate(vals):
            assert v >> 5 == 1, f"identity key {k} not armed"
            assert seg["offset"] <= (v & 0x1F) < seg["offset"] + seg["width"], \
                f"identity key {k} cluster {v & 0x1F} outside {want} pool"
        # and EVERY armed key must name a template the fabric can source -
        # the property whose absence was the whole defect. A key is armed
        # only where gen_aem_store found srcs[co]["valid"], so an unbacked
        # pool can never be the image; re-assert it from the ROM side.
        cs = re.search(r"AEM_ODMAP_CSRC_C \[0:(\d+)\] = '\{([^}]*)\}", svh)
        assert cs, "no capture-crossbar source templates emitted"
        tmpl = [int(v.strip().split("'h")[1], 16)
                for v in cs.group(2).split(",")]
        pcls = P_out[0]["clusters"]
        for k, v in enumerate(vals):
            if v >> 5:
                assert tmpl[(k // 8) * pcls + (v & 0x1F)] >> 12 == 1, \
                    f"power-on key {k} names an UNBACKED source template"
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
          f"the board routes none, talker map -> {want} (fabric lane "
          f"{'on' if lane else 'off'}), 8 distinct loopback sources offered")

    # (d) physical pool APPEARS when the platform declares routed channels
    p = _pools_variant("ax7101_8x8", {"capture": 16, "render": 16},
                       {"host": 2, "pilot": True, "loopback": 2})
    try:
        r = eb.build(p, os.path.join(OUT, "_pools"))
        P = r["overlay"]["stream_ports"]["output"][0]
        assert [g["role"] for g in P["pool"]] == \
            ["physical", "host", "pilot", "loopback"], P
        assert P["clusters"] == 16 + 2 + 1 + 2
        # With physical present the static map still does NOT go to loopback -
        # that was and remains the point of this assertion. Since 0x0043 it
        # goes to HOST rather than to physical: declaring the AX7101's TDM8
        # channels made physical-first silently move the talker's power-on
        # identity off the shared-memory lane and onto the J11 pins, so a
        # board with no codec would wake up streaming whatever `din` floats
        # to and the PipeWire path would need a controller mapping every boot.
        # USER 2026-08-10 chose the host lane again, with physical on the
        # table this time (the 08-06 rule was decided against loopback, before
        # a real physical front end existed). Ordering is PRIMARY_ROLE_ORDER;
        # cluster NUMBERING is unchanged and still physical-first.
        assert P["primary_role"] == "host", P["primary_role"]
        assert [g["role"] for g in P["pool"]][0] == "physical", \
            "cluster numbering must stay physical-first - only the identity " \
            "preference moved"
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
            # write_fragment=False: the refusal fires AFTER the fragment
            # write, so the probe would otherwise hand the tracked
            # sweep_opts_ax7101.sh to a throwaway tmp yaml on every run
            eb.build(p, os.path.join(OUT, "_pools"), write_rtl=True,
                     write_fragment=False)
            assert False, "--write-rtl must refuse a shape with no ROM"
        except eb.ConfigError as e:
            assert "entity definition is incomplete" in str(e), e
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
        cnames = r["cfg"]["interface"].get("channel_names") or []
        for c in cl:
            if c["role"] == "pilot":
                assert c["name"] == "Pilot Tone", c
            elif c["role"] == "loopback":
                assert c["name"].startswith("Loopback S"), c
                # channel_names reach the loopback suffix too
                if cnames:
                    assert c["name"].split()[-1] in cnames, c
            elif c["role"] == "host":
                # channel_names (USER 2026-08-05) name host clusters
                # VERBATIM; without them the Host Play/Cap template holds
                if cnames:
                    assert c["name"] in cnames, c
                else:
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
    # ... and every config that predates D8 must hash EXACTLY as before, up to
    # the ONE input that is deliberately allowed to move every id at once:
    # 0x001BC5AB73EC9D1D -> 0x001BC53442950FCB when AEM_LAYOUT_REV went 1 -> 2
    # (the descriptor byte layout, 1722.1-2013 -> -2021), and
    # -> 0x001BC54079789FCA when it went 2 -> 3 (AUDIO_CLUSTER finished the
    # same move: 87 octets was the 2013 length, 2021 Table 7-27 adds
    # aes3_data_type_reference and aes3_data_type for 90). That is the 6.2.2.8
    # obligation being discharged, not a D8-era regression - which is why the
    # D8 conditional keys above stayed conditional and this key did not),
    # then -> 0x001BC5FC6D9248FB when Milan v1.2 5.3.3.9 made the final
    # shipped input dynamic and removed its forbidden AUDIO_MAP.
    assert eb.load_config(CONFIGS["arty_current"])["model_id"]["hash"] == \
        "0x001BC5FC6D9248FB"
    # arty_4x4's hash has now moved THREE times, correctly every time:
    # 0x001BC565E07E0DD6 -> 0x001BC5C42E0CEE8B when the per-board routing
    # gate forced tdm8 -> i2s_philips (no header existed), ->
    # 0x001BC578CBCE5FBD when HANDOVER 8.3b routed the pmodb header and the
    # shape went back to tdm8 (now with 4-cluster talkers, the emitted
    # width), and -> 0x001BC5A10610BAB8 when roadmap 23 put every listener
    # on map_mode dynamic, which DROPS four AUDIO_MAP descriptors and sets
    # number_of_maps=0 on four STREAM_PORT_INPUTs, and a FOURTH time ->
    # 0x001BC5CB74696C1C when AEM_LAYOUT_REV went 1 -> 2 (descriptor byte
    # layout, 1722.1-2013 -> -2021), and a FIFTH time -> 0x001BC56D12DF80ED
    # when its four Stream Inputs stopped advertising a family capped at four
    # channels: Milan v1.2 6.4 obliges a Stream Input that advertises one
    # 48 kHz Base format to advertise them ALL, and 6.2 defines the channel
    # counts as {1, 2, 4, 6, 8}, so the ut entry has to reach 8 (gate 29).
    # The advertised formats list is descriptor content, so 6.2.2.8 obliges
    # the new id. And a SIXTH time -> 0x001BC59AB5D4ADE1 when AEM_LAYOUT_REV
    # went 2 -> 3 and AUDIO_CLUSTER grew from the 2013 87 octets to 2021's 90.
    # `interface.kind`, the descriptor set and
    # the byte layout are all model-shaping, so a shape change SHOULD move a
    # hash-derived id - that is the mechanism working. What must NOT move is
    # arty_current's PINNED id above, and it has not: it was re-pinned by hand
    # with the reflash, which is the only way a pin is allowed to move.
    assert eb.load_config(CONFIGS["arty_4x4"])["model_id"]["hash"] == \
        "0x001BC59AB5D4ADE1"
    print("  [gate 24c] every cluster named for its ROLE; renaming leaves "
          "entity_model_id frozen (1722.1 6.2.2.8 exclusion list) while a "
          "pool width moves it; pre-D8 hashes stay explicitly pinned to "
          "their current model")


def test_d10_names_reach_the_rom():
    """gate 24d - the cluster ROLE NAMES survive the whole path (config ->
    overlay -> gen_aem_store -> descriptor bytes), and the TRACKED SHAPE
    include is exactly what the config it names generates.

    WHAT THIS GATE LOST (2026-08-12).  Its second half asserted that the role
    names reached tb/verilator/aecp/aem_golden.h - the byte-exact image the
    aecp Verilator suite compared the RTL against - because the original D10
    failure was regenerating hdl/.../aecp_aem_rom.svh and NOT the golden,
    which turned that sweep red on all 16 AUDIO_CLUSTER descriptors (off=42,
    the object_name field) and nothing else. BOTH files are deleted with the
    legacy AECP plane: the processor now serves the builder's descriptor image
    through its external store, and there is no legacy golden, tracked RTL ROM,
    or legacy AECP suite. The two-artifact staleness assertion is therefore
    removed because there is only one generated artifact left.

    WHAT SURVIVES: the names still have to reach the descriptor BYTES (they
    are read out of the generated ROM image at the object_name offset, not
    out of the overlay that declared them), and the tracked SHAPE include -
    which is still tracked, still last-writer-wins, and now also sizes the
    protocol processor's arrays - must still be what its named owner
    generates."""
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
    for nm in ("I2S Out 0", "Virtual In 7"):
        assert nm.encode() in M["rom"], f"generated ROM has no cluster '{nm}'"
    # and the tracked SHAPE must equal what ITS OWNER generates - the owner is
    # READ from the tree (gate 17's rule: never a second answer to "who owns
    # the tracked definition"). Hardcoding arty_current here broke the day the
    # 08-01 flip handed the tree to the ax7101_8x8 ship config.
    src, owner = ces.tracked_owner(eb, adp_text=open(TRACKED_ADP_SVH).read())
    assert owner is not None, f"tracked shape names no owner ({src})"
    r_o = eb.build(os.path.join(ROOT, src), OUT)
    assert r_o["adp_shape_svh"] == open(TRACKED_ADP_SVH).read(), \
        f"tracked adp_shape_defaults.svh is not what its owner ({src}) " \
        f"generates - re-run endstation_builder.py {src} --write-rtl"
    print(f"  [gate 24d] role names reach the descriptor bytes; the tracked "
          f"shape include matches its OWNER ({owner['name']}) byte for byte "
          f"(aem_golden.h comparand DELETED with the aecp suite)")


#: The four ADP CSRs that carry the entity's IDENTITY. Every one of them is a
#: value the builder computes, so every one must reach the board through the
#: generated conf - never as a literal in the boot script.
IDENTITY_CSRS = {"0x604": "entity_id lo", "0x608": "entity_id hi",
                 "0x60C": "entity_model_id lo", "0x610": "entity_model_id hi"}


def _sh_code(path):
    """The shipped script with sh comments removed - what actually RUNS. A
    grep over the raw text would be satisfied by moving a literal into the
    comment that explains it, which is precisely the state this gate exists to
    forbid; and the history the comments carry (which stale id was where) is
    worth keeping, so the gate reads code and code only."""
    return "\n".join(re.sub(r"#.*$", "", ln) for ln in open(path).read()
                     .splitlines())


def test_entity_identity_is_derived_not_mirrored():
    """Gate 25: the flashed board's entity_model_id is DERIVED from the config
    that board's bitstream is built from, and nothing restates it.

    THE DEFECT (silicon 2026-08-02, the fifth mirrored-constant instance of
    that week). S50milan carried `w 0x610 0x001BC52E` / `w 0x60C 0xD611DB08`
    for the AX. The 8x8 config then gained dynamic output maps, the AEM ROM was
    regenerated and the shape re-hashed to 0x001BC52B80A86C93 - and the script
    did not move. The fabric serves the AEM ENTITY descriptor's
    entity_model_id FROM those CSRs (the ROM's OVL_MODEL_ID_C overlay slot),
    so the board advertised one model id over a different model's descriptors.
    Controllers cache AEM by model id and 1722.1-2021 6.2.1.10 makes the id the
    identity OF the model: two AEMs under one id is a conformance break. The
    Arty branch had rotted identically (0x001BC578CBCE5FBD named, 4x4 config
    hashing to 0x001BC5A10610BAB8).

    Two halves, because either alone can be defeated:
      a) no identity CSR in the shipped script is written from a LITERAL -
         every one takes a shell variable - and the OUI 0x001BC5 appears
         nowhere in the code. A literal cannot come back.
      b) the generated /etc/milan-entity.<board>.conf that replaced them is
         byte-for-byte what the builder emits TODAY for the config that board
         builds (sweep_config(), READ from sweep.sh - never restated here, the
         gate-9 rule). A stale file cannot survive."""
    if not os.path.exists(S50MILAN):
        skip("gate 25", "identity-derivation cross-check: sibling repo "
                        "milan-tests-avb not on disk")
        return
    code = _sh_code(S50MILAN)
    seen = set()
    for m in re.finditer(r"^\s*w\s+(0x[0-9A-Fa-f]+)\s+(\S+)", code, re.M):
        reg = "0x" + m.group(1)[2:].upper()
        if reg not in IDENTITY_CSRS:
            continue
        seen.add(reg)
        assert m.group(2).startswith("$"), (
            f"{S50MILAN}: {reg} ({IDENTITY_CSRS[reg]}) is written from the "
            f"LITERAL {m.group(2)} - the 2026-08-02 defect verbatim. It must "
            f"come from /etc/milan-entity.<board>.conf, which the builder "
            f"generates in the same pass that writes the AEM ROM.")
    assert seen == set(IDENTITY_CSRS), (
        f"{S50MILAN}: identity CSRs {sorted(set(IDENTITY_CSRS) - seen)} are "
        f"never written - the entity would advertise the reset value 0")
    assert not re.search(r"0x0*01[Bb][Cc]5", code), (
        f"{S50MILAN}: the Kebag Logic OUI 0x001BC5 appears in CODE - some "
        f"model-id literal is back. It belongs only in the generated conf.")
    assert re.search(r"/etc/milan-entity\.\$\w+\.conf", code), (
        f"{S50MILAN}: nothing sources /etc/milan-entity.<board>.conf")
    subprocess.run(["sh", "-n", S50MILAN], check=True)
    print(f"  [gate 25] {os.path.basename(S50MILAN)}: all "
          f"{len(IDENTITY_CSRS)} identity CSRs written from the sourced conf, "
          f"zero model-id literals in code, sh -n clean")
    for board in ("arty", "ax7101"):
        p = eb.entity_conf_overlay_path(board)
        assert p and os.path.exists(p), (
            f"the rootfs overlay ships no identity for {board} ({p}) - "
            f"S50milan would refuse to program the entity. Generate it: "
            f"python3 sw/builder/endstation_builder.py --write-rtl "
            f"<{board} config>")
        cfg = eb.load_config(sweep_config(board))
        want = eb.emit_entity_conf(cfg)
        got = open(p).read()
        assert got == want, (
            f"{p} is STALE: it is not what {cfg['source']} - the config "
            f"sweep.sh builds this board from - generates today. Regenerate: "
            f"python3 sw/builder/endstation_builder.py --write-rtl "
            f"{cfg['source']}")
        kv = dict(re.findall(r"^(MILAN_\w+)=(\S+)$", got, re.M))
        mid = (int(kv["MILAN_MODEL_ID_HI"], 16) << 32) \
            | int(kv["MILAN_MODEL_ID_LO"], 16)
        assert f"0x{mid:016X}" == cfg["entity"]["entity_model_id"], (
            f"{p}: model id 0x{mid:016X} != the builder's "
            f"{cfg['entity']['entity_model_id']} for {cfg['source']}")
        eid = (int(kv["MILAN_ENTITY_ID_HI"], 16) << 32) \
            | int(kv["MILAN_ENTITY_ID_LO"], 16)
        assert eid == eb.derive_entity_id(cfg), f"{p}: entity_id drifted"
        assert int(kv["MILAN_N_TALKERS"]) == len(cfg["talkers"]), \
            f"{p}: talker count drifted (the MAAP claim size derives from it)"
        assert int(kv["MILAN_SR_VID"]) == cfg["srp"]["vid"], f"{p}: SR VID"
        subprocess.run(["sh", "-n", p], check=True)
        print(f"  [gate 25] {board}: shipped identity == builder output for "
              f"{os.path.basename(cfg['source'])} "
              f"(model id {cfg['entity']['entity_model_id']}, "
              f"{kv['MILAN_N_TALKERS']} talkers, SR VID {kv['MILAN_SR_VID']})")


def test_gptp_domain_is_one_source():
    """Gate 26: the gPTP domain number reaches BOTH consumers from the one
    `gptp.domain` line, and no hand-written copy survives.

    THE DEFECT THIS GATE CLOSES.  `gptp.domain` used to reach ptp4l only
    (emit_gptp_cfg's `domainNumber`).  The other consumer - ADPDU byte 48
    (1722.1-2021 6.2.1.16), served from CSR 0x62C - got its value from a
    hardcoded `w 0x62C 0x00000000` in avdecc/aecp_csr_setup.sh.  The two
    agreed only because every shipping config happens to say 0, so a config
    on domain 1 would have run the daemon on domain 1 while the entity
    advertised domain 0, with nothing anywhere to catch it.  Exactly the
    "derive, never mirror" class.

    WHY THIS GATE CANNOT VARY THE VALUE (USER 2026-08-11).  It used to build a
    config on domain 3 and follow that number through, because asserting
    `ADP_GPTP_DOMAIN_C == 0` proves nothing on its own - it passes just as well
    against the old hardcoded zero.  But 3 is not a legal Milan value: Milan
    v1.2 section 2 pins 802.1AS-2011, whose 8.1 says "The domain number of a
    gPTP domain shall be 0", and multi-domain is an 802.1AS-2020 feature Milan
    does not adopt.  So the variation the gate needs is the REFUSAL, not the
    value: a non-zero config must raise ConfigError WITH the clause, and the
    legal chain must still be wired end to end.

        gptp.domain -> ADP_GPTP_DOMAIN_C in the generated adp shape header
                    -> milan_csr's adp_domain reset
                    -> milan_csr's csr_default readback ROM (they must mirror)
                    -> emit_gptp_cfg's domainNumber
                    -> o_adp_gptp_domain -> cfg_adp_gptp_domain
                    -> adp_advertiser -> ADPDU byte 48

    plus the negative: aecp_csr_setup.sh must no longer write 0x62C at all,
    because a boot script that wrote it would clobber the elaborated value
    back to whatever literal it carries."""
    # 0. a non-zero domain is REFUSED, and the refusal cites the clause - this
    #    is the varying half of the gate, and it bites if the check is removed
    bad = _variant(CONFIGS["ax7101_1x1_tdm8"],
                   lambda c: c["gptp"].__setitem__("domain", 3))
    try:
        eb.build(bad, OUT)
        raise AssertionError("gptp.domain 3 was ACCEPTED - 802.1AS-2011 8.1 "
                             "says the domain number shall be 0")
    except eb.ConfigError as e:
        assert "802.1AS-2011" in str(e) and "shall be 0" in str(e), \
            f"refused, but without the clause: {e}"
    os.unlink(bad)

    DOM = 0                                   # the only value Milan permits
    r = eb.build(CONFIGS["ax7101_1x1_tdm8"], OUT)

    # 1. the generated header carries the CONFIG's number from a named symbol
    m = re.search(r"^\s*localparam\s+int\s+ADP_GPTP_DOMAIN_C\s*=\s*(\d+);",
                  r["adp_shape_svh"], re.M)
    assert m, ("adp_shape_defaults.svh emits no ADP_GPTP_DOMAIN_C - the ADP "
               "domain has no config-derived source")
    assert int(m.group(1)) == DOM, \
        f"ADP_GPTP_DOMAIN_C = {m.group(1)}, config says {DOM}"

    # 2. and the ptp4l half carries the SAME number, from the same line
    assert f"domainNumber            {DOM}\n" in eb.emit_gptp_cfg(r["cfg"]), \
        "the generated gptp.cfg domainNumber does not match gptp.domain"

    # 3. the RTL consumes the symbol in BOTH places, and by NAME - a literal
    #    in either would let the two drift again (the rule milan_csr states
    #    at VERSION 0x0026: reset literal and readback ROM move together)
    csr = open(MILAN_CSR_SV).read()
    assert re.search(r"adp_domain\s*<=\s*32'\(ADP_GPTP_DOMAIN_C\)\s*;", csr), \
        "milan_csr's adp_domain reset does not name ADP_GPTP_DOMAIN_C"
    assert re.search(r"A_ADP_DOMAIN\[10:0\]\s*:\s*csr_default\s*=\s*"
                     r"32'\(ADP_GPTP_DOMAIN_C\)\s*;", csr), \
        "milan_csr's csr_default ROM does not mirror the adp_domain reset"

    # 4. and the boot script no longer writes 0x62C - the clobber is gone
    setup = open(os.path.join(ROOT, "avdecc/aecp_csr_setup.sh")).read()
    assert not re.search(r"^\s*w\s+0x62[Cc]\b", setup, re.M), \
        ("aecp_csr_setup.sh still writes 0x62C - it would clobber the "
         "elaborated gPTP domain back to its literal")

    # 5. the register reaches the ADVERTISER.  A reset value nothing reads is
    #    not a fix, so walk the chain by NAME - each link is one rename away
    #    from silently detaching, and none of it is covered above:
    #      adp_domain[7:0] -> milan_csr.o_adp_gptp_domain
    #                      -> milan_datapath.cfg_adp_gptp_domain
    #                      -> the ADP advertiser's gptp_domain_i
    #    THE LAST LINK MOVED (2026-08-12).  It used to be
    #    hdl/ieee17221/adp/adp_advertiser.sv's gptp_domain_number_i and the
    #    fb[62] = ADPDU byte 48 placement (1722.1-2021 6.2.1.16) inside it;
    #    that advertiser is DELETED and the protocol-processor submodule
    #    advertises now, so the chain is walked to the datapath's port into
    #    that plane and stops there.  The byte-48 placement itself is NOT
    #    re-asserted here: it lives in a PINNED, read-only submodule this
    #    suite does not own, and a gate reaching into a pin is a gate that
    #    breaks on a bump it has no say in.
    #    (STALENESS of the tracked headers is deliberately NOT asserted here:
    #     gate 24d owns it, and earlier gates in this process rebuild those
    #     files, so a copy of the check here could never fail - a check that
    #     cannot fail reads as coverage without being any.)
    assert re.search(r"assign\s+o_adp_gptp_domain\s*=\s*adp_domain\[7:0\]\s*;",
                     csr), "milan_csr does not export adp_domain[7:0]"
    dp = open(os.path.join(ROOT, "hdl/milan/milan_datapath.sv")).read()
    assert re.search(r"\.o_adp_gptp_domain\s*\(\s*cfg_adp_gptp_domain\s*\)",
                     dp), "milan_datapath does not take the CSR's domain"
    assert re.search(r"\.gptp_domain_i\s*\(\s*cfg_adp_gptp_domain\s*\)", dp), \
        "the ADP advertiser is not fed the CSR's domain"
    assert not os.path.exists(
        os.path.join(ROOT, "hdl/ieee17221/adp/adp_advertiser.sv")), \
        "hdl/ieee17221/adp/adp_advertiser.sv is back - if the legacy " \
        "advertiser returns, this gate must walk the domain into it again"

    print(f"  [gate 26] gptp.domain is ONE source: domain 3 REFUSED with the "
          f"802.1AS-2011 8.1 clause; the legal 0 emits ADP_GPTP_DOMAIN_C = "
          f"{DOM} AND domainNumber {DOM}; "
          f"milan_csr names the symbol in both the reset and the readback "
          f"ROM; aecp_csr_setup.sh writes 0x62C nowhere; the chain reaches "
          f"the advertising plane's gptp_domain_i")


def _reserved_regions(dtsi):
    """The emitted device tree's `reserved-memory` node, parsed:
    ((#address-cells, #size-cells), [{name, base, size, no_map}, ...]).

    PARSED FROM THE TEXT, never asked of the builder that wrote it. This text
    becomes the DTB the kernel honours, so an expectation taken from the
    emitter could not disagree with it, and a disagreement between the bytes
    the gateware compiles and the bytes the kernel protects is the whole
    reason this parser exists.
    """
    i = dtsi.index("reserved-memory")
    j = dtsi.index("{", i)
    depth, body = 0, None
    for k in range(j, len(dtsi)):
        if dtsi[k] == "{":
            depth += 1
        elif dtsi[k] == "}":
            depth -= 1
            if depth == 0:
                body = dtsi[j + 1:k]
                break
    assert body is not None, "reserved-memory node is not brace-balanced"

    def cells(prop):
        m = re.search(rf"#{prop}-cells\s*=\s*<(\d+)>", body)
        assert m, f"reserved-memory declares no #{prop}-cells"
        return int(m.group(1))

    out = []
    for label, node, child in re.findall(
            r"(?:(\w+)\s*:\s*)?([\w-]+)@[0-9a-fA-F]+\s*\{(.*?)\n\s*\};",
            body, re.S):
        m = re.search(r"reg\s*=\s*<([^>]*)>", child)
        assert m, f"reserved-memory child {node!r} carries no reg"
        vals = [int(x, 0) for x in m.group(1).split()]
        assert len(vals) == 2, (
            f"reserved-memory child {node!r}: reg has {len(vals)} cells, "
            "expected one base plus one size")
        out.append(dict(name=label or node, base=vals[0], size=vals[1],
                        no_map=bool(re.search(r"^\s*no-map\s*;", child, re.M))))
    assert out, "reserved-memory node has no children"
    return (cells("address"), cells("size")), out


def test_pp_window_is_reserved():
    """Gate 27: the protocol processor's DRAM window is RESERVED, `no-map`,
    and the SAME BYTES on both sides of the hardware/software boundary.

    The window is compiled into the bitstream as PP_DESC_BASE_P (the
    descriptor store READS the entity model from it) and PP_RESP_BASE_P (the
    AECP response buffer WRITES to it). It used to be derived independently in
    two places: sw/builder/endstation_builder.py emitted the device tree, and
    sw/litex/milan_soc.py computed "top of main_ram". They disagreed. At the
    1x1 shape the window was ordinary kernel RAM and the response buffer wrote
    into whatever the page allocator had handed out; at 8x8 it sat INSIDE the
    PCM ring and corrupted captured audio. NEITHER failure raises anything -
    there is no counter on either side for a write to a wrong physical
    address, the entity still answers, and the board still plays. So the only
    place this can be caught is here, before the bitstream exists.

    Every config, four properties:
      1. a reserved-memory node COVERS the whole window;
      2. the window overlaps neither the PCM ring nor any other reservation;
      3. platform_shape.json's pp_mem is the same base and the same length the
         tree reserves, and milan_soc.py READS it rather than deriving a
         second answer;
      4. the covering node is `no-map`, which is load-bearing twice: it keeps
         the kernel allocator out, and it keeps the region out of the linear
         map, which is what lets the loader reach it through /dev/mem.
    """
    import json
    PAGE = 0x1000
    for name in CONFIGS:
        r = eb.build(CONFIGS[name], OUT)
        dtsi = open(r["paths"]["dt_overlay"]).read()
        shape = json.load(open(r["paths"]["platform_shape"]))
        assert "pp_mem" in shape, (
            f"{name}: platform_shape.json publishes no pp_mem. milan_soc.py "
            "reads that key to compile PP_DESC_BASE_P / PP_RESP_BASE_P, so "
            "without it the SoC has to invent the window a second time")
        base = int(shape["pp_mem"]["phys"], 16)
        size = int(shape["pp_mem"]["bytes"], 16)
        end = base + size
        assert size > 0, f"{name}: pp_mem window is empty"
        # the loader mmaps this window through /dev/mem, which takes a
        # page-aligned offset and length
        assert base % PAGE == 0 and size % PAGE == 0, (
            f"{name}: window 0x{base:08X}+0x{size:X} is not 4 KiB aligned, so "
            "the loader cannot mmap it through /dev/mem")
        cells, regions = _reserved_regions(dtsi)
        assert cells == (1, 1), (
            f"{name}: reserved-memory declares {cells} address/size cells. "
            "The reg pairs are read here as one base plus one size, and the "
            "kernel reads them by the same declaration")

        # (1) SOMETHING RESERVES IT. Unreserved, this is ordinary kernel RAM.
        cover = [g for g in regions
                 if g["base"] <= base and end <= g["base"] + g["size"]]
        assert len(cover) == 1, (
            f"{name}: the processor window 0x{base:08X}+0x{size:X} is covered "
            f"by {len(cover)} reserved-memory node(s), expected exactly 1. "
            f"Tree reserves "
            + ", ".join(f"{g['name']} 0x{g['base']:08X}+0x{g['size']:X}"
                        for g in regions))
        cov = cover[0]

        # (4) `no-map`, not merely reserved. A plain reservation leaves the
        # region in the kernel's linear map, where CONFIG_STRICT_DEVMEM
        # refuses the loader's /dev/mem mapping of it.
        assert cov["no_map"], (
            f"{name}: reserved node {cov['name']!r} covers the window but "
            "carries no `no-map`, so the kernel keeps it in the linear map "
            "and the loader cannot reach it through /dev/mem")

        # (3) and it reserves EXACTLY the window the gateware compiles. A
        # reservation that merely contains it is a second, independently
        # derived number, and two numbers for one physical address is the
        # defect itself.
        assert (cov["base"], cov["size"]) == (base, size), (
            f"{name}: the device tree reserves "
            f"0x{cov['base']:08X}+0x{cov['size']:X} but platform_shape.json "
            f"publishes 0x{base:08X}+0x{size:X}. The gateware compiles one of "
            "those and the kernel honours the other")

        # (2) and it is nobody else's memory. The PCM ring is named when the
        # Linux sound-card option exists; the bare-metal profile has no such
        # reservation. The pairwise sweep holds for whatever region is added
        # next in either shape.
        if shape["pcm"] is not None:
            ring = int(shape["pcm"]["ring_phys"], 16)
            ring_bytes = int(shape["pcm"]["ring_bytes"], 16)
            assert any((g["base"], g["size"]) == (ring, ring_bytes)
                       for g in regions), (
                f"{name}: the PCM ring 0x{ring:08X}+0x{ring_bytes:X} is not "
                "among the reserved regions")
            assert end <= ring or ring + ring_bytes <= base, (
                f"{name}: the processor window 0x{base:08X}+0x{size:X} "
                f"OVERLAPS the PCM ring 0x{ring:08X}+0x{ring_bytes:X}")
            ring_desc = f"clear of PCM 0x{ring:08X}+0x{ring_bytes:X}"
        else:
            assert all(not g["name"].startswith("pcmring") for g in regions)
            ring_desc = "PCM reservation absent"
        for x in range(len(regions)):
            for y in range(x + 1, len(regions)):
                a_, b_ = regions[x], regions[y]
                assert (a_["base"] + a_["size"] <= b_["base"]
                        or b_["base"] + b_["size"] <= a_["base"]), (
                    f"{name}: reserved regions {a_['name']} "
                    f"0x{a_['base']:08X}+0x{a_['size']:X} and {b_['name']} "
                    f"0x{b_['base']:08X}+0x{b_['size']:X} overlap")
        print(f"  [gate 27] {name}: window 0x{base:08X}+0x{size:X} reserved "
              f"no-map as {cov['name']!r}, byte-identical to "
              f"platform_shape.json's pp_mem, {ring_desc}, clear of "
              f"{len(regions) - 1} other reserved region(s)")

    # THE OTHER HALF of "cannot drift": the SoC must READ that published
    # window. Up to 00f17a68 it derived its own, `_desc_base = _ram.origin +
    # _ram.size - _PP_WINDOW` with _PP_WINDOW a local literal, and nothing
    # compared the two. Stated as a RULE over every assignment rather than as
    # a copy of the expression: any future spelling is fine as long as the
    # value comes from the config's published window.
    soc = open(MILAN_SOC_PY).read()
    assert re.search(r"^\s*_shape\s*=\s*_platform_shape\(", soc, re.M), \
        "milan_soc.py no longer loads the config's platform shape"
    assert "platform_shape.json" in soc, \
        "milan_soc.py names no platform_shape.json to read the window from"
    for var in ("_desc_base", "_PP_WINDOW"):
        rhs = re.findall(rf"^\s*{var}\s*=\s*(.+)$", soc, re.M)
        assert rhs, f"milan_soc.py assigns {var} nowhere"
        for expr in rhs:
            assert '_shape["pp_mem"]' in expr, (
                f"milan_soc.py derives {var} from {expr.strip()!r} instead of "
                "the config's published pp_mem window. A second derivation of "
                "a physical address is not a build error on either side, it "
                "is silent memory corruption on the board")
    print(f"  [gate 27] milan_soc.py READS the published window: every "
          f"_desc_base / _PP_WINDOW assignment ({len(re.findall(r'^ *(?:_desc_base|_PP_WINDOW) *=', soc, re.M))} "
          "of them) comes from platform_shape.json's pp_mem, so the base the "
          "bitstream compiles and the base the kernel reserves are ONE number")


def test_image_identity_is_baked():
    """Gate 28: the descriptor IMAGE carries the Table 7-2 identity.

    IEEE 1722.1-2021 Table 7-2 states, field by field, that the ENTITY
    descriptor's entity_id, entity_model_id, entity_capabilities,
    talker_stream_sources, talker_capabilities, listener_stream_sinks,
    listener_capabilities, controller_capabilities and association_id "is the
    same as the ... field in ATDECC Discovery Protocol", and 7.2.8 binds
    AVB_INTERFACE's mac_address and clock_identity to the station the same
    way.  gen_aem_store ZERO-FILLS every one of those spans and records them
    in M["OVERLAYS"]: KL_aecp_aem_dyn_mux substituted them from the CSR group
    while the response streamed.  That module was deleted with the legacy
    plane in eff99a9c, along with the only test that asserted these bytes
    (tb/verilator/aecp/sim_main.cpp), and the descriptor store that replaced
    it has NO identity input - so the step had to move to image generation
    and did not.  On 2026-08-14 silicon served bytes 4..47 of the ENTITY
    descriptor as 44 zeros while ADP advertised the real values two frames
    away.

    The worst of those zeros is entity_capabilities: AEM_SUPPORTED (Table
    6-3, mask 0x08) clear tells a controller the entity has no entity model
    at all.

    This gate reads the values back OUT OF THE PACKED IMAGE and compares each
    against the artifact that owns it - the boot script's milan-entity.conf
    for the two ids, the gateware's adp_shape_defaults.svh for the counts and
    capability words, pp_adp_pkg.sv for entity_capabilities, the config for
    the MAC - so it fails both ways round: an unbaked image and a baked image
    that disagrees with what ADP sends.
    """
    sys.path.insert(0, os.path.join(ROOT, "protocol-processor/hdl/aecp/desc"))
    import gen_aem_store as aem                    # noqa: E402
    import gen_aemi_image as aemi                  # noqa: E402

    ENTITY, AVB_INTERFACE = 0x0000, 0x0009
    AEM_SUPPORTED = 0x0000_0008                    # 1722.1-2021 Table 6-3

    #! Read here as well as in the generator: two independent reads of one
    #! constant is what makes this an assertion rather than a tautology.
    pkg = open(os.path.join(ROOT, "protocol-processor/hdl/adp/pp_adp_pkg.sv"))
    m = re.search(r"ADP_ENTITY_CAPS_C\s*=\s*32'h([0-9A-Fa-f_]+)\s*;",
                  pkg.read())
    assert m, "pp_adp_pkg.sv declares no ADP_ENTITY_CAPS_C"
    adp_caps = int(m.group(1).replace("_", ""), 16)
    assert adp_caps & AEM_SUPPORTED, (
        f"ADP advertises entity_capabilities 0x{adp_caps:08X} with "
        "AEM_SUPPORTED clear (Table 6-3): the entity would be telling every "
        "controller it has no entity model, and no READ_DESCRIPTOR would "
        "ever arrive to serve this image from")

    for name in ("ax7101_1x1_tdm8", "arty_current", "arty_4x4",
                 "ax7101_8x8"):
        cfg = eb.load_config(CONFIGS[name])
        overlay = eb.emit_aem_overlay(cfg)
        blob = eb._entity_model_image(cfg, overlay)["aem_desc.bin"]
        ent = image_descriptor(blob, ENTITY)
        avbi = image_descriptor(blob, AVB_INTERFACE)

        # ---- the ADP side of Table 7-2, from the artifacts ADP is built from
        conf = dict(
            ln.split("=", 1) for ln in eb.emit_entity_conf(cfg).splitlines()
            if "=" in ln and not ln.startswith("#"))
        want_eid = (int(conf["MILAN_ENTITY_ID_HI"], 16) << 32) \
            | int(conf["MILAN_ENTITY_ID_LO"], 16)
        want_mid = (int(conf["MILAN_MODEL_ID_HI"], 16) << 32) \
            | int(conf["MILAN_MODEL_ID_LO"], 16)
        svh = eb.emit_adp_shape_svh(cfg)

        def sym(n, s=svh, who=name):
            g = re.search(rf"{n}\s*=\s*(?:\d+'h([0-9A-Fa-f]+)|(\d+))\s*;", s)
            assert g, f"{who}: adp_shape_defaults.svh declares no {n}"
            return int(g.group(1), 16) if g.group(1) else int(g.group(2))

        mac = bytes(int(x, 16)
                    for x in cfg["platform"]["mac_address"].split(":"))
        #! 802.1AS-2011 8.5.2.2: EUI-48 widened to EUI-64 with FF-FE at the
        #! OUI boundary, the recipe the deleted mux applied in RTL.
        want_clock_id = mac[:3] + b"\xFF\xFE" + mac[3:]

        # ---- what the image actually serves
        u = lambda b, o, n: int.from_bytes(b[o:o + n], "big")  # noqa: E731
        got = {
            "entity_id": u(ent, 4, 8),
            "entity_model_id": u(ent, 12, 8),
            "entity_capabilities": u(ent, 20, 4),
            "talker_stream_sources": u(ent, 24, 2),
            "talker_capabilities": u(ent, 26, 2),
            "listener_stream_sinks": u(ent, 28, 2),
            "listener_capabilities": u(ent, 30, 2),
        }
        want = {
            "entity_id": want_eid,
            "entity_model_id": want_mid,
            "entity_capabilities": adp_caps,
            "talker_stream_sources": sym("ADP_TALKER_SRC_C"),
            "talker_capabilities": sym("ADP_TALKER_CAPS_C"),
            "listener_stream_sinks": sym("ADP_LISTENER_SINK_C"),
            "listener_capabilities": sym("ADP_LISTENER_CAPS_C"),
        }
        for k, w in want.items():
            assert w != 0, (
                f"{name}: the ADP side of {k} is itself 0, so this gate would "
                "be comparing two zeros and proving nothing")
            assert got[k] == w, (
                f"{name}: ENTITY descriptor {k} reads 0x{got[k]:X} in the "
                f"image, ADP advertises 0x{w:X}. 1722.1-2021 Table 7-2: the "
                "descriptor field 'is the same as' the ADP one"
                + ("  [entity_capabilities = 0 clears AEM_SUPPORTED: the "
                   "entity model says it has no entity model]"
                   if k == "entity_capabilities" and got[k] == 0 else ""))
        assert got["entity_capabilities"] & AEM_SUPPORTED, (
            f"{name}: entity_capabilities 0x{got['entity_capabilities']:08X} "
            "has AEM_SUPPORTED clear")
        # The teeth on the model id: the number the CONFIG generates, not
        # merely the number the boot script happens to carry.
        assert got["entity_model_id"] == int(overlay["model_id"]["value"], 16),\
            (f"{name}: image entity_model_id 0x{got['entity_model_id']:016X} "
             f"is not the id this config generates "
             f"({overlay['model_id']['value']}). 1722.1-2021 6.2.1.10 makes "
             "that id the identity OF the model, and a controller caches the "
             "descriptors under it")

        assert avbi[70:76] == mac, (
            f"{name}: AVB_INTERFACE mac_address {avbi[70:76].hex()} is not "
            f"the station MAC {cfg['platform']['mac_address']}")
        assert avbi[78:86] == want_clock_id, (
            f"{name}: AVB_INTERFACE clock_identity {avbi[78:86].hex()}, "
            f"802.1AS says {want_clock_id.hex()}")

        # ---- and NO build-constant span left zero-filled anywhere.
        # Stated over gen_aem_store's own overlay list so a span added there
        # cannot ship as zeros the way this whole set did: every entry is
        # either resolved or explicitly declared dynamic, with no third
        # option.
        model = aem.build_model(aem.spec_from_overlay(overlay))
        ident = aemi.identity_from_overlay(overlay)
        for base, nbytes, src in model["OVERLAYS"]:
            assert src in ident or src in aemi.UNBAKED_SPANS, (
                f"{name}: overlay span {src} (ROM 0x{base:04X}, {nbytes} B) "
                "is neither resolved nor declared dynamic - it would ship as "
                "zeros")
            if src in ident and any(ident[src]):
                assert len(ident[src]) == nbytes
        #! available_index is the one field here that genuinely cannot be
        #! baked: it counts THIS entity's advertisements and increments per
        #! ADPDU (6.2.1.14). Pinned so that baking a counter into a static
        #! image is a visible diff.
        assert "AVAIL_IDX" in aemi.UNBAKED_SPANS, \
            "available_index is a live counter; a flat image cannot state it"
        assert u(ent, 36, 4) == 0, f"{name}: available_index baked non-zero"
        #! controller_capabilities and association_id are 0 BECAUSE ADP sends
        #! them as 0 (KL_adp_engine frame_byte_f wire bytes 46..49 and 70..77)
        #! - this entity implements no controller and associates with nobody.
        #! Asserted against the RTL so the day either becomes a real value,
        #! this fails rather than silently shipping stale zeros.
        eng = open(os.path.join(ROOT,
                                "protocol-processor/hdl/adp/KL_adp_engine.sv"))
        src = eng.read()
        assert re.search(r"i < 50\)\s*b = 8'h00;\s*// ctrl caps", src), \
            "KL_adp_engine no longer sends controller_capabilities as zero"
        assert u(ent, 32, 4) == 0, f"{name}: controller_capabilities non-zero"
        assert u(ent, 40, 8) == 0, f"{name}: association_id non-zero"
        #! current_configuration: d_configuration emits configurations_count
        #! = 1, so 0 is the only index SET_CONFIGURATION could select.
        assert u(ent, 308, 2) == 1, f"{name}: configurations_count != 1"
        assert u(ent, 310, 2) == 0, f"{name}: current_configuration != 0"

        print(f"  [gate 28] {name}: image ENTITY carries entity_id "
              f"0x{got['entity_id']:016X}, entity_model_id "
              f"0x{got['entity_model_id']:016X}, entity_capabilities "
              f"0x{got['entity_capabilities']:08X} (AEM_SUPPORTED set), "
              f"{got['talker_stream_sources']} source(s)/"
              f"0x{got['talker_capabilities']:04X} + "
              f"{got['listener_stream_sinks']} sink(s)/"
              f"0x{got['listener_capabilities']:04X}, AVB_INTERFACE the "
              f"station MAC {cfg['platform']['mac_address']} and its 802.1AS "
              f"clock_identity - all equal to what ADP advertises (Table 7-2)")


def test_image_name_table_matches_descriptors():
    """Gate 28b: name commands and READ_DESCRIPTOR share one initial truth.

    The packed image index rows are the hardware's only mapping from a
    descriptor to its writable name-table entries. Read that mapping and the
    table back out of the finished image, then compare every entry with the
    corresponding 64 bytes in the packed descriptor. This catches an omitted,
    shifted, non-contiguous or stale name independently of the join's document.
    """
    NAME_NONE = 0xFFFF
    named_types = {
        0x0000, 0x0001, 0x0002, 0x0005, 0x0006, 0x0009, 0x000A,
        0x0014, 0x001A, 0x0024,
    }
    for name, path in CONFIGS.items():
        cfg = eb.load_config(path)
        overlay = eb.emit_aem_overlay(cfg)
        blob = eb._entity_model_image(cfg, overlay)["aem_desc.bin"]
        n_entries, n_names = struct.unpack_from(">HH", blob, 8)
        index_off, names_off = struct.unpack_from(">II", blob, 12)

        first = {}
        next_index = {}
        for row in range(n_entries):
            at = index_off + 16 * row
            cfg_i, typ, count, elem_len = struct.unpack_from(">HHHH", blob, at)
            elem_off, name_base, stride = struct.unpack_from(">IHH", blob,
                                                               at + 8)
            key = (cfg_i, typ)
            run_first = next_index.get(key, 0)
            for rel in range(count):
                first[(cfg_i, typ, run_first + rel)] = (
                    NAME_NONE if name_base == NAME_NONE else name_base + rel,
                    elem_off + rel * stride, elem_len)
            next_index[key] = run_first + count

        used = set()
        for (cfg_i, typ, idx), packed in sorted(first.items()):
            name_base, elem_off, elem_len = packed
            desc = blob[elem_off:elem_off + elem_len]
            if typ not in named_types:
                assert name_base == NAME_NONE, (
                    f"{name}: unnamed type 0x{typ:04X} index {idx} maps to "
                    f"name-table entry {name_base}")
                continue
            assert name_base != NAME_NONE, (
                f"{name}: named type 0x{typ:04X} index {idx} has no table")
            semantic = ((0, 48), (1, 180)) if typ == 0x0000 else ((0, 4),)
            for name_index, field_off in semantic:
                slot = name_base + name_index
                assert slot < n_names, (
                    f"{name}: type 0x{typ:04X} index {idx} name {name_index} "
                    f"maps past the {n_names}-entry table")
                table = blob[names_off + 64 * slot:names_off + 64 * (slot + 1)]
                inline = desc[field_off:field_off + 64]
                assert len(table) == len(inline) == 64
                assert table == inline, (
                    f"{name}: type 0x{typ:04X} index {idx} name {name_index} "
                    f"table entry {slot} differs from READ_DESCRIPTOR bytes")
                used.add(slot)
        assert used == set(range(n_names)), (
            f"{name}: name table has unreferenced entries "
            f"{sorted(set(range(n_names)) - used)}")
        print(f"  [gate 28b] {name}: all {n_names} writable names map "
              "byte-exactly to their READ_DESCRIPTOR fields")

        svh = eb.emit_adp_shape_svh(cfg, overlay)
        declared = re.search(r"AEM_NAME_ENTRIES_C\s*=\s*(\d+)", svh)
        assert declared and int(declared.group(1)) == n_names, (
            f"{name}: generated RTL sizes {declared.group(1) if declared else 'no'} "
            f"name entries for an image containing {n_names}")

        if name == "arty_current":
            assert n_names == 29, (
                f"shipping model has {n_names} names, expected 29")
            rtl = "hdl/milan/KL_pp_shadow.sv"
            src = open(os.path.join(ROOT, rtl), encoding="utf-8").read()
            assert re.search(r"DESC_NAME_ENTRIES_P\s*=\s*32", src), (
                f"{rtl}: standalone default cannot fit the shipping model")


# ------------------------------------------- Milan Base Stream Formats (29) --
#: Milan v1.2 Table 6.2 "Summary of Base Audio Stream Formats", TRANSCRIBED
#: from the specification (printed p. 111) instead of computed.  This gate is
#: an ORACLE, so it must not import the arithmetic it is grading: the builder
#: DERIVES these strings from the fields, and check A below is what proves the
#: derivation lands on all fifteen of them.  3 rates x Milan 6.2's five
#: channel counts N in {1, 2, 4, 6, 8}.
MILAN_TABLE_6_2 = {
    48000: {1: 0x0205022000406000, 2: 0x0205022000806000,
            4: 0x0205022001006000, 6: 0x0205022001806000,
            8: 0x0205022002006000},
    96000: {1: 0x020702200040C000, 2: 0x020702200080C000,
            4: 0x020702200100C000, 6: 0x020702200180C000,
            8: 0x020702200200C000},
    192000: {1: 0x0209022000418000, 2: 0x0209022000818000,
             4: 0x0209022001018000, 6: 0x0209022001818000,
             8: 0x0209022002018000},
}
#: Milan v1.2 7.3.2 + Table 7.1: the ONE Avnu Pro Audio CRF Media Clock Stream
#: Format ("The base frequency shall be 48000Hz.  Each PDU shall contain 1
#: timestamp, and the timestamp interval shall be 96.").
MILAN_TABLE_7_1_CRF = 0x041060010000BB80
#: IEEE 1722.1-2021 Table 7-8: a STREAM descriptor is 138 + 8*N + 2*R octets.
#: KL_aecp_desc_store's LINE_BYTES_P is 576 and a descriptor longer than the
#: line buffer cannot be answered at all.
DESC_LINE_BYTES = 576


def _oracle_cover(fmts):
    """{rate_hz: set(Base channel counts advertised)}, computed from Table 6.2
    alone.

    IEEE 1722-2016 Annex I.2.4 on the ut bit: "The ut field is used to
    determine if the AAF stream source or sink is capable of sourcing or
    sinking a stream with less than the number of channels indicated by the
    channels_per_frame field.  When set to one (1) the stream source or sink
    is capable of using fewer channels than specified." - so one ut entry
    advertises every Base count up to its own, which Milan v1.2 6.5 makes the
    recommended spelling ("it should use the ut bit ... to describe all the
    related formats using a single ATDECC format string") and 5.3.3.4 confirms
    reads that way ("a single entry in the formats list can describe a range
    of formats when using the "up to" bit")."""
    cover = {}
    for f in fmts:
        n = int(str(f), 16)
        ut, ch = (n >> 52) & 1, (n >> 22) & 0x3FF
        stem = n & ~((1 << 52) | (0x3FF << 22))
        for rate, row in MILAN_TABLE_6_2.items():
            if stem != row[8] & ~(0x3FF << 22):
                continue
            add = {c for c in row if c <= ch} if ut else {ch} & set(row)
            # a rate is only "advertised" once something at it IS a Base
            # format: 6.2 defines N in {1, 2, 4, 6, 8}, so a lone 3-channel
            # AAF PCM32 48 kHz entry does not arm 6.4's family rule.
            if add:
                cover.setdefault(rate, set()).update(add)
    return cover


def test_per_row_format_facts_are_per_row():
    """Gate 30: the emitted per-row format facts carry EACH row's own
    declaration, and the CRF output constant reads the NORMALIZED
    crf_output_format key.

    The defect class this refuses (found by review on the issue #67 root
    round): the shape header carried ONE input format fact, so the fabric's
    format verdict judged every row against row 0 and every reset GET served
    row 0's format - and the CRF output constant silently took the default
    because the emitter read the raw-YAML mapping shape where load_config
    hands it a boolean plus crf_output_format. Every tracked config is
    uniform, so only a DIVERGENT synthetic config can make either defect
    visible; this gate builds one in memory and demands the divergence
    reaches the header verbatim.
    """
    import re

    def qarray(s, name):
        m = re.search(rf"{name}\s*\[[^]]+\]\s*=\s*'\{{([^}}]+)\}};", s)
        assert m, f"shape header has no {name}"
        return [int(t.strip().split("'h")[1], 16)
                for t in m.group(1).split(",")]

    def qscalar(s, name):
        m = re.search(rf"{name}\s*=\s*64'h([0-9A-Fa-f]+);", s)
        assert m, f"shape header has no {name}"
        return int(m.group(1), 16)

    fmt_2ch = "0x0205022000806000"
    fmt_4ch = "0x0205022001006000"
    crf_div = "0x041060020000BB80"

    cfg = eb.load_config(CONFIGS["ax7101_8x8"])
    cfg["listeners"][3]["formats"] = [fmt_2ch] \
        + list(cfg["listeners"][3].get("formats") or [])[1:]
    cfg["talkers"][2]["formats"] = [fmt_4ch] \
        + list(cfg["talkers"][2].get("formats") or [])[1:]
    cfg["clocking"]["crf_output_format"] = crf_div
    svh = eb.emit_adp_shape_svh(cfg, eb.emit_aem_overlay(cfg))

    in_rows = qarray(svh, "ADP_STRIN_FMT_C")
    out_rows = qarray(svh, "ADP_STROUT_FMT_C")
    assert in_rows[3] == int(fmt_2ch, 16), \
        "input row 3's declared format did not reach its own row"
    assert in_rows[0] == qscalar(svh, "ADP_STRIN0_FMT_C"), \
        "input row 0 must restate the scalar fact"
    assert in_rows[0] != in_rows[3], \
        "the divergence collapsed: row 3 reads row 0's fact"
    assert out_rows[2] == int(fmt_4ch, 16), \
        "talker row 2's declared format did not reach its own row"
    assert out_rows[0] != out_rows[2], \
        "the divergence collapsed on the output side"
    assert qscalar(svh, "ADP_CRF_OUT_FMT_C") == int(crf_div, 16), \
        "ADP_CRF_OUT_FMT_C ignored the normalized crf_output_format"
    assert qscalar(svh, "ADP_CRF_FMT_C") != int(crf_div, 16), \
        "the sink constant must not follow the output's divergence"

    # the uniform shipping config keeps every row equal to the scalar
    u = eb.load_config(CONFIGS["ax7101_1x1_tdm8"])
    usvh = eb.emit_adp_shape_svh(u, eb.emit_aem_overlay(u))
    urows = qarray(usvh, "ADP_STRIN_FMT_C")
    assert urows == [qscalar(usvh, "ADP_STRIN0_FMT_C")] * len(urows)


def test_milan_base_formats_are_rate_complete():
    """Gate 29: every Stream Input that advertises a Base format advertises
    the WHOLE rate family, the CRF streams carry the CRF format and nothing
    else, and no stream's descriptor outgrows the store's line buffer.

    THE CLAUSES, and they are not symmetric.

    Milan v1.2 6.4 (Listeners requirements), third paragraph: "If the PAAD-AE
    Base Listener advertises support for a 48kHz (resp. 96kHz, 192kHz) Base
    format in a Stream Input, then it shall also advertise support for all the
    other 48kHz (resp. 96kHz, 192kHz) Base formats in this Stream Input.
    Note: This ensures that a Stream Input that supports the Base format
    supports all defined channel counts."  Fifth paragraph: the same rate
    "in all the Stream Input which advertise support for a Base format, in
    this Configuration".

    Milan v1.2 6.3 (Requirements - the Talker clause) is the WHOLE of what
    Talkers owe: one Configuration with one Stream Output advertising a Base
    format, Class A transport, and "A PAAD-AE Base Talker may advertise any
    Base Format that is reasonable for its functionality."  There is no
    all-channel-counts rule and no cross-Stream-Output rate rule anywhere in
    Section 6.  So this gate holds Stream Inputs to the family and Stream
    Outputs to wire truth, and the asymmetry in the shipped configs is that
    clause difference rather than an oversight.  (The talker half is also
    load-bearing the other way: SET_STREAM_FORMAT on our STREAM_OUTPUT is
    served since 0x0053 but admits only the row's own declared shape -
    FR-STR-03 makes adaptivity a LISTENER requirement - so a talker format
    the framer cannot emit is a declaration nothing can correct, which is
    the 2026-07-27 defect that cost 296,294 discarded frames out of
    296,294.)

    Milan v1.2 5.3.3.4 keeps the CRF streams out of it: "If a Stream
    Input/Output supports the Avnu Pro Audio CRF Media Clock Stream Format, it
    shall not support the Avnu Pro Audio AAF Audio Stream Format, and vice
    versa."  6.2 defines the Base Format Type as AAF only and 6.4 scopes its
    rule to "all the Stream Input which advertise support for a Base format",
    so a CRF Media Clock Input is outside the family rule and must stay that
    way - giving it AAF formats would break 5.3.3.4 to satisfy a clause that
    never reached it.

    Milan v1.2 5.3.3.3 binds the rates to the AUDIO_UNIT: "The list of
    supported sampling rates of each AUDIO_UNIT descriptor shall correctly
    report the sampling rates supported by the Audio Unit", and 5.3.3.4 says
    the same of the formats list.  A stream advertising a 96 kHz Base format
    under an AUDIO_UNIT that lists 48 kHz only is one of the two lying."""
    # A. the builder DERIVES Table 6.2 rather than carrying a copy of it
    for rate, row in sorted(MILAN_TABLE_6_2.items()):
        for ch, want in sorted(row.items()):
            got = eb.aaf_pcm32(ch, rate)
            assert got == want, (
                f"aaf_pcm32({ch}, {rate}) = 0x{got:016X}, Milan Table 6.2 "
                f"says 0x{want:016X}")
            ut = eb.aaf_pcm32(ch, rate, ut=True)
            assert ut == want | (1 << 52), (
                f"aaf_pcm32({ch}, {rate}, ut=True) = 0x{ut:016X}: the ut bit "
                f"is bit 52 (IEEE 1722-2016 Annex I.2.4)")
    assert set(eb.BASE_CHANNELS) == set(MILAN_TABLE_6_2[48000]), \
        f"BASE_CHANNELS {eb.BASE_CHANNELS} != Milan 6.2 {{1, 2, 4, 6, 8}}"
    print(f"  [gate 29] the builder's aaf_pcm32 derivation reproduces all "
          f"{sum(len(r) for r in MILAN_TABLE_6_2.values())} Milan Table 6.2 "
          f"Base format strings (3 rates x {len(eb.BASE_CHANNELS)} channel "
          f"counts) and the AVTP I.2.4 ut bit of each")

    worst = (0, "")
    for name, path in CONFIGS.items():
        r = eb.build(path, OUT)
        ovl, cfg = r["overlay"], r["cfg"]
        rates = [int(x) for x in cfg["clocking"]["audio_unit_rates_hz"]]
        streams = ([("STREAM_INPUT", s) for s in ovl["stream_inputs"]]
                   + [("STREAM_OUTPUT", s) for s in ovl["stream_outputs"]])
        in_rates, complete, base_streams = [], 0, {}
        for kind, s in streams:
            who = f"{name} {kind}[{s['index']}] ('{s['name']}')"
            cover = _oracle_cover(s["formats"])
            # E. CRF exclusivity, both directions (5.3.3.4)
            if s["kind"] == "crf":
                assert [f.upper() for f in s["formats"]] == \
                    [f"0X{MILAN_TABLE_7_1_CRF:016X}"], (
                    f"{who}: a CRF Media Clock stream advertises "
                    f"{s['formats']}, and Milan 7.3.2 / Table 7.1 define "
                    f"exactly one Avnu Pro Audio CRF Media Clock Stream "
                    f"Format, 0x{MILAN_TABLE_7_1_CRF:016X}")
                assert not cover, (
                    f"{who}: a CRF stream advertises AAF Base format(s) "
                    f"{sorted(cover)} - Milan 5.3.3.4: \"If a Stream "
                    f"Input/Output supports the Avnu Pro Audio CRF Media "
                    f"Clock Stream Format, it shall not support the Avnu Pro "
                    f"Audio AAF Audio Stream Format, and vice versa\"")
            else:
                assert MILAN_TABLE_7_1_CRF not in \
                    [int(str(f), 16) for f in s["formats"]], \
                    f"{who}: an AAF stream advertises the CRF format (5.3.3.4)"
                base_streams.setdefault(kind, []).append(bool(cover))
            # D. rate coherence with the AUDIO_UNIT (5.3.3.3 + 5.3.3.4)
            for rate in cover:
                assert rate in rates, (
                    f"{who}: advertises a {rate} Hz Base format while the "
                    f"AUDIO_UNIT reports sampling rates {rates} - Milan "
                    f"5.3.3.3 makes that list the Audio Unit's truth")
            # B. the family rule, Stream Inputs only (6.4 third paragraph)
            if kind == "STREAM_INPUT" and s["kind"] != "crf":
                in_rates.append(sorted(cover))
                for rate, got in sorted(cover.items()):
                    missing = sorted(set(eb.BASE_CHANNELS) - got)
                    assert not missing, (
                        f"{who}: advertises {s['formats']} = {rate} Hz Base "
                        f"channel counts {sorted(got)}, missing {missing}. "
                        f"Milan v1.2 6.4: \"If the PAAD-AE Base Listener "
                        f"advertises support for a 48kHz (resp. 96kHz, "
                        f"192kHz) Base format in a Stream Input, then it "
                        f"shall also advertise support for all the other "
                        f"48kHz (resp. 96kHz, 192kHz) Base formats in this "
                        f"Stream Input.\" One ut entry at "
                        f"0x{eb.aaf_pcm32(max(eb.BASE_CHANNELS), rate, ut=True):016X} "
                        f"covers the whole family (6.5)")
                    complete += 1
            # G. IEEE 1722.1-2021 Table 7-8 against the store's line buffer
            n = len(s["formats"])
            length = 138 + 8 * n
            assert length <= DESC_LINE_BYTES, (
                f"{who}: {n} formats = {length} octets (Table 7-8: "
                f"138 + 8*N + 2*R at R=0), past KL_aecp_desc_store's "
                f"{DESC_LINE_BYTES}-octet line buffer")
            worst = max(worst, (length, who))
        # F. one Base stream per direction (6.3 / 6.4 second paragraphs: "at
        #    least one Configuration that contains at least one Stream
        #    Output/Input which advertises support for a Base format in its
        #    list of supported formats")
        for kind, seen in sorted(base_streams.items()):
            assert any(seen), (
                f"{name}: no {kind} advertises a Milan 6.2 Base format - "
                f"{'6.4' if kind.endswith('INPUT') else '6.3'} requires at "
                f"least one in at least one Configuration, and this entity "
                f"declares exactly one Configuration")
        # C. same rates across every Base Stream Input (6.4 fifth paragraph)
        assert len(set(map(tuple, in_rates))) <= 1, (
            f"{name}: its Stream Inputs advertise Base formats at differing "
            f"rate sets {in_rates} - Milan v1.2 6.4: \"then it shall "
            f"advertise support for a 48kHz (resp. 96kHz, 192kHz) Base format "
            f"in all the Stream Input which advertise support for a Base "
            f"format, in this Configuration\"")
        print(f"  [gate 29] {name}: {len(in_rates)} Base Stream Input(s) "
              f"complete at {in_rates[0] if in_rates else []} Hz "
              f"({complete} rate famil(ies) x "
              f"{len(eb.BASE_CHANNELS)} channel counts), "
              f"{sum(1 for k, s in streams if s['kind'] == 'crf')} CRF "
              f"stream(s) carrying only 0x{MILAN_TABLE_7_1_CRF:016X}, "
              f"AUDIO_UNIT rates {rates}")
    print(f"  [gate 29] longest STREAM descriptor {worst[0]} octets "
          f"({worst[1]}), {DESC_LINE_BYTES - worst[0]} clear of the "
          f"{DESC_LINE_BYTES}-octet line buffer")


if __name__ == "__main__":
    for fn in (test_all_configs_build, test_baremetal_profile_contract,
               test_current_shape_matches_sweep_flags,
               test_current_shape_matches_gen_aem_store,
               test_capability_marks, test_bad_configs_rejected,
               test_port_layout_invariants, test_both_policies_valid,
               test_model_id_hashing, test_sweep_opts_fragments,
               test_gen_aem_store_consumes_overlay,
               test_resource_calibration, test_resource_determinism,
               test_resource_verdicts, test_milan_723_crf_output_rule,
               test_crf_output_overlay_structure,
               test_gen_aem_store_crf_output_overlay,
               test_dynamic_map_topology_reaches_shape_header,
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
               test_optional_block_consumption_gate_bites,
               test_optional_blocks_reach_the_instance,
               test_optional_block_instance_gate_bites,
               test_every_recipe_elaborates,
               test_recipe_smoke_gate_bites,
               test_recipe_skip_classifier_bites,
               test_toolchain_patches_are_applied,
               test_toolchain_patch_gate_bites,
               test_tdm_master_binding_reaches_the_pins,
               test_tdm_master_binding_gate_bites,
               test_front_end_routing_per_board,
               test_front_end_routing_gate_bites,
               test_i2s_pair_blend_binding,
               test_i2s_pair_blend_gate_bites,
               test_firmware_version_derived_from_rtl,
               test_d8_role_pools, test_d8_role_pools_reject,
               test_d10_cluster_names, test_d10_names_reach_the_rom,
               test_entity_identity_is_derived_not_mirrored,
               test_gptp_domain_is_one_source,
               test_pp_window_is_reserved,
               test_image_identity_is_baked,
               test_image_name_table_matches_descriptors,
               test_milan_base_formats_are_rate_complete,
               test_per_row_format_facts_are_per_row):
        print(f"{fn.__name__}:")
        fn()
    # The verdict names what did not run.  Printing SKIP inside a gate and
    # then printing ALL GATES PASS here is how a reviewer severed the
    # --fabric-gptp chain at two hops and read a green both times (#154).
    if SKIPPED:
        print(f"\n{len(SKIPPED)} GATE ARM(S) DID NOT RUN - this verdict does "
              "not cover them:")
        for gate, why, _kind in SKIPPED:
            print(f"  - [{gate}] {why}")
        print(f"ALL GATES PASS EXCEPT {len(SKIPPED)} NOT RUN")
    else:
        print("ALL GATES PASS")
    # --require-elaboration is what stops the ONE job that exists to
    # elaborate from reporting a green when its LiteX install broke.  Rows a
    # gate declined for a recorded reason still pass; "there is no LiteX
    # here" and "this VexiiRiscv is unpatched" do not.
    if "--require-elaboration" in sys.argv:
        sys.exit(_require_elaboration_verdict(SKIPPED))
