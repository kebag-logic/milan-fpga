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
      BYTE-FOR-BYTE (OPTS string + L2) for both boards; sh -n passes on
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
  19a. platform emitter: platform_shape.json contains exactly the one
      configuration fact its gateware consumer reads - the aligned
      protocol-processor memory reservation - plus provenance metadata;
  19b. every checked configuration publishes its exact base and the fixed
      extent, with no duplicate hardware inventory;
  19c. reject paths: an unknown or retired platform key and an unaligned
      processor-memory window all raise ConfigError;
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
  27. THE PROTOCOL PROCESSOR'S MEMORY WINDOW IS SINGLE-SOURCED for every
      config: platform_shape.json publishes the configured base and extent,
      and milan_soc.py derives PP_DESC_BASE_P / PP_RESP_BASE_P from that
      published window instead of computing one of its own.
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
import binascii
import contextlib
import copy
import gzip
import io
import json
import os
import pathlib
import re
import shlex
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SOC_DIR = os.path.join(ROOT, "sw/litex")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "avdecc"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, SOC_DIR)

import yaml  # noqa: E402

import endstation_builder as eb  # noqa: E402
import check_gptp_owner_pair as gptp_pair  # noqa: E402
import qspi_owner_transition as qspi_transition  # noqa: E402
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
#: gate 24d's pin of the cluster namer: every object_name the builder produces
#: for a loopback-bearing config and for the channel_names config, per
#: direction and STREAM_PORT, in offset order. Generated from the
#: implementation by `python3 sw/builder/test_builder.py --write-cluster-golden`;
#: a deliberate naming change regenerates it, and the diff of that file is what
#: a reviewer reads.
CLUSTER_NAMES_GOLDEN = os.path.join(HERE, "cluster_names_golden.json")
CLUSTER_NAMES_GOLDEN_CONFIGS = ("ax7101_8x8", "ax7101_1x1_tdm8")
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
    """(OPTS string, L2 string) of sweep.sh's inline FALLBACK table."""
    txt = open(SWEEP).read()
    m = re.search(rf'{board}\)\s+OPTS="([^"]+)"; L2=(\d+)', txt)
    assert m, f"sweep.sh: no OPTS case for {board}"
    return m.group(1), m.group(2)


def sweep_expected(board):
    """Design-flag dict sweep.sh composes for <board> (OPTS + BASE minus
    flow flags)."""
    txt = open(SWEEP).read()
    opts, l2 = sweep_inline(board)
    mb = re.search(r'milan_soc\.py \$OPTS (.*?)"', txt, re.S)
    assert mb, "sweep.sh: BASE line not found"
    base = mb.group(1).replace("\\\n", " ")
    tokens = shlex.split(opts) + shlex.split(base)
    subst = {"${L2}": l2}
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
      role-pools - the block is a SELECTION SET (physical + pilot +
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
        # #259: a port whose backing pool was retired owns ZERO clusters
        # (the 8x8 inputs after the external audio surface left). Such a port
        # must be fully empty-handed: dynamic map mode, no pool, so no
        # cluster, map or template can dangle off it.
        if p["clusters"] == 0:
            assert p["pool"] == [] and p.get("map_mode") == "dynamic", p
        else:
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


class Rv32Stack(object):
    """A STACK address: a frame register the prologue set and never moved,
    displaced into a general register.

    Kept as a VALUE rather than modelled as a frame slot, because the frame
    it names may belong to a CALLER: `parse_u64(text, &seconds)` hands one
    down, and keying it into the callee's own slot table would let two
    different addresses share one key.  What it buys is the store census:
    a store through it lands on the stack, which the linker places outside
    the Milan CSR window, so the census can PLACE that store instead of
    refusing it."""
    __slots__ = ()

    def __eq__(self, other):
        return isinstance(other, Rv32Stack)

    def __hash__(self):
        return hash("stack")

    def __repr__(self):
        return "<stack>"


class Rv32Where(object):
    """WHERE a store landed when its address did NOT resolve to a number:
    the class of base it went through, plus what is known about that base.

    A store the resolver cannot place is not a store it may drop.  The
    earlier revision reported only `(int_address, value)` pairs and the
    census filtered on `isinstance(address, int)`, so every store through
    an unresolved base vanished before it was ever asked about, and the
    gate reported a clean census over the subset it happened to understand
    ([R0] BLOCKER on PR #241).  Every store now arrives here classified,
    and the census either PROVES the class lands outside the control window
    or REFUSES."""
    __slots__ = ("kind", "detail")

    def __init__(self, kind, detail=None):
        self.kind, self.detail = kind, detail

    def __eq__(self, other):
        return (isinstance(other, Rv32Where) and other.kind == self.kind and
                other.detail == self.detail)

    def __hash__(self):
        return hash(("where", self.kind, self.detail))

    def __repr__(self):
        return (f"{self.kind}({self.detail})" if self.detail is not None
                else f"{self.kind}(-)")


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


class Rv32Range(object):
    """A value known only to lie in [lo, hi], unsigned and inclusive.

    Produced by BRANCH REFINEMENT: on the edge an unsigned conditional
    branch takes, the branch's own comparison holds, so a value the meet
    could only call unknown is bounded by the emitted bound.  This is what
    PLACES the AEM copy loop's store: the loop index is unknown at the
    join, but on the `bltu` edge into the body it is inside the bound the
    compiler emitted, so base plus index is a bounded range rather than an
    address this census must refuse.  A residual entry keyed by function,
    class and count bound neither the store's base nor its value, so the
    shipping copy store could be REDIRECTED onto a control register while
    the key set and count stayed byte-identical ([R0] 2026-08-25T05:46Z
    and [R2] BLOCKER on PR #241); a range is the fact itself."""
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        assert 0 <= lo <= hi <= RV32_MASK, \
            f"a range that wraps or inverts is not a value: [{lo}, {hi}]"
        self.lo, self.hi = lo, hi

    def __eq__(self, other):
        return (isinstance(other, Rv32Range) and other.lo == self.lo and
                other.hi == self.hi)

    def __hash__(self):
        return hash(("range", self.lo, self.hi))

    def __repr__(self):
        return f"[0x{self.lo:x}..0x{self.hi:x}]"


def _rv32_range_bounded(lo, hi):
    """A range value, collapsed to the int when it is one point, and to
    None when it leaves 32 bits: a sum that can wrap is not a bounded
    address, and reporting the unwrapped half would be an invented fact."""
    if not 0 <= lo <= hi <= RV32_MASK:
        return None
    return lo if lo == hi else Rv32Range(lo, hi)


def _rv32_range_add(value, delta):
    """`value + delta` for a range and a signed displacement, fail-closed
    on wrap."""
    return _rv32_range_bounded(value.lo + delta, value.hi + delta)


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


def asm_int(text):
    """The integer grammar of COMPILER-EMITTED assembly, not Python's:
    `0x`/`0X` is hex, anything else all-digits is decimal, zero-padded
    spellings included. `int(x, 0)` refuses `03118564` as a malformed
    octal literal, so a VALID emitted immediate could fail the census by
    spelling alone and the mandatory gate went red nondeterministically
    ([R-retest] on PR #228). Signs pass through; anything else raises
    ValueError for the caller to classify as unresolved."""
    tok = text.strip()
    sign = 1
    if tok and tok[0] in "+-":
        sign = -1 if tok[0] == "-" else 1
        tok = tok[1:]
    if tok[:2].lower() == "0x":
        return sign * int(tok, 16)
    if tok.isdigit():
        return sign * int(tok, 10)
    raise ValueError("not an emitted-assembly integer: %r" % (text,))


#: Immediates as the assembler prints them, in any base and either sign,
#: and never a label suffix (`.L4`) or a register number. Module scope so
#: the deterministic fixtures below replay the EXACT regex+parser pair the
#: compiled census uses.
ASM_IMMEDIATE_RE = re.compile(
    r"(?<![\w.])(-?(?:0[xX][0-9A-Fa-f]+|\d+))(?![\w.])")

#: Deterministic parser fixtures ([R-retest] on PR #228): zero-padded
#: decimal, plain and signed decimal, and hexadecimal spellings must parse
#: to the same value on every process, and the census replay forces the
#: exact token shape the nondeterministic red run tripped on through the
#: production regex+parser pair.
for _tok, _want in (("03118564", 3118564), ("007", 7), ("42", 42),
                    ("-42", -42), ("0x7F700000", 0x7F700000),
                    ("-0X10", -16)):
    assert asm_int(_tok) == _want, (_tok, asm_int(_tok))
for _bad in ("", "0o17", "1_2", ".L4", "a5"):
    try:
        asm_int(_bad)
    except ValueError:
        pass
    else:
        raise AssertionError("asm_int accepted %r" % (_bad,))
_census_replay = "entity_store:\n\tli\ta5,03118564\n\tsw\ta4,0(a5)\n"
assert [asm_int(_t) & 0xFFFF_FFFF
        for _t in ASM_IMMEDIATE_RE.findall(_census_replay)] == [3118564, 0], \
    "the census replay no longer parses the zero-padded immediate shape"


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
            emitted.append(asm_int(word.group(1)) & RV32_MASK if word else None)
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
        return asm_int(text) & RV32_MASK
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

    def meet(self, other):
        """Greatest lower bound with `other`: a value BOTH sides carry, and
        agree on, survives; everything else becomes "cannot say".

        Absent and unknown are the SAME reading here -- `get()` and the
        frame-slot load both read a missing key as `None` -- so a key
        missing on either side meets to unknown, which is what makes this
        commutative and idempotent.

        THE DEFECT THIS REPLACES ([R0] MAJOR on PR #241).  The earlier
        `merge()` copied a slot IN from `other` when `self` did not have
        it, so a value stored on ONE incoming path survived a join whenever
        that path happened to be visited first.  The same program then
        resolved differently under a different block layout, and CRC
        provenance and return values could be invented by traversal order
        alone.  `rv32_run()` below now takes this meet over ALL of a
        block's predecessors rather than folding predecessors in one at a
        time, so the answer is a function of the code and nothing else."""
        for key, value in list(self.regs.items()):
            if value is not None and (key not in other.regs or
                                      other.regs[key] != value):
                self.regs[key] = None
        for key, value in list(self.mem.items()):
            if value is not None and (key not in other.mem or
                                      other.mem[key] != value):
                self.mem[key] = None
        return self

    def frozen(self):
        """The state as a comparable value, with absent and unknown spelled
        the same way -- which is how every reader of it reads them.  This is
        what the fixpoint compares, so "did this block's entry change" is
        answered on MEANING rather than on dictionary shape."""
        return (frozenset((key, value) for key, value in self.regs.items()
                          if value is not None),
                frozenset((key, value) for key, value in self.mem.items()
                          if value is not None))


def rv32_meet(states):
    """The meet of a list of states.  No states at all means nothing is
    known, which is the safe reading for a block with no reachable
    predecessor.  Order-independent: `Rv32State.meet()` is commutative and
    idempotent, so this is a set operation written as a fold."""
    out = None
    for state in states:
        out = state.copy() if out is None else out.meet(state)
    return out if out is not None else Rv32State()


#: The relation that holds between the two compared registers on the TAKEN
#: edge of each unsigned conditional branch.  Signed branches are left
#: unrefined: their constraint does not translate into one unsigned
#: interval, and no refinement is always sound.
RV32_UNSIGNED_BRANCHES = {"bltu": "<", "bgeu": ">=", "bleu": "<=",
                          "bgtu": ">"}
#: ... its negation, which holds on the FALL edge ...
_RV32_REL_NEGATED = {"<": ">=", ">=": "<", "<=": ">", ">": "<="}
#: ... and the same relation read from the second operand's side.
_RV32_REL_FLIPPED = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}


def _rv32_constrained(value, relation, bound):
    """`value` refined by `value RELATION bound` (unsigned), or `value`
    unchanged when the constraint adds nothing this lattice can hold.  A
    constraint nothing satisfies leaves the value alone rather than
    inventing emptiness: the edge is then unreachable, and any state
    over-approximates no executions."""
    lo, hi = {"<": (0, bound - 1), "<=": (0, bound),
              ">=": (bound, RV32_MASK), ">": (bound + 1, RV32_MASK)}[relation]
    refined = _rv32_range_bounded(lo, hi)
    if refined is None:
        return value
    if value is None:
        return refined
    if isinstance(value, Rv32Range) and isinstance(refined, Rv32Range):
        met = _rv32_range_bounded(max(value.lo, refined.lo),
                                  min(value.hi, refined.hi))
        return met if met is not None else value
    return value


def _rv32_slot_mirror(insns, reg):
    """The frame slot `reg` still MIRRORS at the end of `insns`, or None.

    Walking back from the terminator: if the last write to `reg` is a full
    `lw` from a frame slot and nothing after it could have moved the slot
    out from under the register -- no store of any class, no call, no write
    to `reg` or to a frame register -- then refining the register refines
    the slot too.  Anything this walk cannot rule out returns None, which
    refines nothing: refinement may only ever ADD a fact, never invent
    one."""
    for mnem, ops in reversed(insns[:-1]):
        args = [part.strip() for part in ops.split(",")] if ops else []
        if mnem == "lw" and len(args) == 2 and args[0] == reg:
            place = RV32_MEM_RE.match(args[1])
            if place and place.group(2) in RV32_FRAME_REGS:
                raw_off = place.group(1)
                if not raw_off or raw_off.startswith("%lo("):
                    return (place.group(2), 0)
                offset = _rv32_imm(raw_off)
                return (place.group(2), _rv32_s32(offset)) \
                    if offset is not None else None
            return None
        if mnem in RV32_STORES or \
                mnem in ("call", "jal", "jalr", "tail", "jr", "ret"):
            return None
        if args and (args[0] == reg or args[0] in RV32_FRAME_REGS):
            return None
    return None


def rv32_edge_refined(exit_state, insns, kind):
    """`exit_state` as it holds ON one outgoing edge.

    For an unsigned conditional branch whose other operand is resolved,
    the branch's own comparison (on the taken edge) or its negation (on
    the fall edge) is a fact about the compared register, and about the
    frame slot it still mirrors.  This is what bounds a loop index: the
    index is unknown at the join, but the edge into the body is taken only
    under the bound the compiler emitted.  Every other terminator hands
    the exit state on unchanged."""
    if kind not in ("taken", "fall") or not insns:
        return exit_state
    mnem, ops = insns[-1]
    if mnem not in RV32_UNSIGNED_BRANCHES:
        return exit_state
    args = [part.strip() for part in ops.split(",")] if ops else []
    if len(args) != 3:
        return exit_state
    relation = RV32_UNSIGNED_BRANCHES[mnem]
    if kind == "fall":
        relation = _RV32_REL_NEGATED[relation]
    refined_state = exit_state
    for this, rel in ((args[0], relation),
                      (args[1], _RV32_REL_FLIPPED[relation])):
        other = args[1] if this == args[0] else args[0]
        bound = exit_state.get(other)
        if not isinstance(bound, int) or this in ("zero", "x0") or \
                this in RV32_FRAME_REGS:
            continue
        held = exit_state.get(this)
        refined = _rv32_constrained(held, rel, bound)
        if refined is held:
            continue
        if refined_state is exit_state:
            refined_state = exit_state.copy()
        refined_state.set(this, refined)
        slot = _rv32_slot_mirror(insns, this)
        if slot is not None:
            refined_state.mem[slot] = refined
    return refined_state


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
        #: A frame register the prologue set and never moved, displaced
        #: into a general register, IS a stack address: `addi a5,s0,-36` is
        #: how `&seconds` reaches a callee. Only when the destination is
        #: NOT itself a frame register, so the prologue's own
        #: `addi s0,sp,32` keeps meaning "this function's frame" and the
        #: slot model below is untouched.
        if mnem == "addi" and source is None and \
                args[1] in RV32_FRAME_REGS and args[0] not in RV32_FRAME_REGS:
            state.set(args[0], Rv32Stack())
            return None
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
        elif mnem == "addi" and isinstance(source, Rv32Range):
            state.set(args[0], _rv32_range_add(source, _rv32_s32(imm)))
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
        elif mnem == "add" and isinstance(left, Rv32Range) and \
                isinstance(right, int):
            state.set(args[0], _rv32_range_add(left, right))
        elif mnem == "add" and isinstance(left, int) and \
                isinstance(right, Rv32Range):
            state.set(args[0], _rv32_range_add(right, left))
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
            #: A static this unit WRITES has no compile-time value, but a
            #: word this function stored into it and reads back before the
            #: next call IS a value, and that round trip is exactly how the
            #: boot path hands the AEM verdict to the choke point ([R0]
            #: BLOCKER on PR #241, third round). Only `lw`: a byte or
            #: half-word read of the slot is a partial reading, which is a
            #: WRONG value rather than a missing one.
            place_at = held.offset + offset
            if mnem == "lw" and place_at == 0 and held.name in data:
                state.set(args[0], data[held.name])
            elif mnem == "lw":
                state.set(args[0],
                          state.mem.get(("sym", held.name, place_at)))
        elif base in RV32_FRAME_REGS and held is None:
            state.set(args[0], state.mem.get((base, offset)))
        return None
    if mnem in RV32_STORES:
        #: EVERY store is reported, classified by the base it goes through.
        #: The two silent drops that used to live here -- an operand this
        #: regex cannot read, and a base that resolved to nothing -- are
        #: what let a store leave the census without ever being asked about
        #: ([R0] BLOCKER on PR #241). A store the resolver cannot read is
        #: the one it must refuse hardest, so it is reported as `unreadable`
        #: rather than skipped.
        place = RV32_MEM_RE.match(args[1]) if len(args) == 2 else None
        if place is None:
            _rv32_forget_symbols(state)
            return ("store", (Rv32Where("unreadable", f"{mnem} {ops}"), None))
        raw_off, base = place.group(1), place.group(2)
        held, value = state.get(base), state.get(args[0])
        offset = 0 if not raw_off or raw_off.startswith("%lo(") \
            else _rv32_s32(_rv32_imm(raw_off) or 0)
        if isinstance(held, int):
            return ("store", ((held + offset) & RV32_MASK, value))
        if isinstance(held, Rv32Range):
            #: A store to a BOUNDED range is reported as the range itself,
            #: so the census can judge it by address the way it judges a
            #: resolved number.  Conservative on both sides: a displacement
            #: that could wrap makes it unplaced, and the symbol slots drop
            #: because a ranged store may cover one of this unit's statics.
            _rv32_forget_symbols(state)
            placed = _rv32_range_add(held, offset)
            if placed is not None:
                return ("store", (placed, value))
            return ("store", (Rv32Where("unplaced", repr(held)), value))
        if isinstance(held, Rv32Sym):
            state.mem[("sym", held.name, held.offset + offset)] = \
                value if mnem == "sw" else None
            return ("symstore", (held.name, value))
        if isinstance(held, Rv32Stack):
            return ("store", (Rv32Where("stack"), value))
        if base in RV32_FRAME_REGS and held is None:
            state.mem[(base, offset)] = value
            return None
        if isinstance(held, Rv32Tag) and held.what.startswith("call:"):
            _rv32_forget_symbols(state)
            return ("store", (Rv32Where("call", held.what[5:]), value))
        _rv32_forget_symbols(state)
        return ("store", (Rv32Where("unplaced", repr(held)), value))
    #: `jr <reg>` that is not the return is a tail transfer through a
    #: register, which is the same unplaceable edge as `jalr <reg>` and is
    #: reported as one; `jr ra` falls through to the return below.
    if (mnem in ("call", "jal", "jalr", "tail") or
            (mnem == "jr" and args and args[0] not in ("ra", "x1"))) and args:
        callee = args[-1].split("@")[0]
        handed = {reg: state.get(reg) for reg in
                  ("a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7")}
        #: A callee may write any static this unit holds, so the symbol
        #: slots do not cross a call.
        _rv32_forget_symbols(state)
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
    without that edge is exactly what the edge does not dominate.

    A block's entry state is the MEET OVER ALL its predecessors' settled
    exit states, recomputed from scratch each time one of them moves, not a
    running fold of whichever predecessor arrived first.  That is what
    makes the result independent of block layout and of the order the
    worklist happens to pop ([R0] MAJOR on PR #241)."""
    blocks, order, edges = rv32_blocks(body)
    if cut is not None:
        edges = dict(edges)
        edges[cut[0]] = [edge for edge in edges[cut[0]] if edge[1] != cut[1]]
    entry = order[0]
    preds = {block: [] for block in order}
    for block in order:
        for succ, kind in edges[block]:
            preds[succ].append((block, kind))
    seed, exits = Rv32State(entry_regs or {}), {}

    def joined(block):
        """The meet over every predecessor that is REACHABLE, plus the
        function's own entry state for the entry block.  An unreachable
        predecessor contributes nothing, which is exactly what `cut` needs:
        removing an edge must remove what flowed along it.  Each
        predecessor's exit state arrives REFINED by the edge it flows
        along, so a conditional branch's own comparison is a fact on the
        side that took it."""
        parts = [rv32_edge_refined(exits[at], blocks[at], kind)
                 for at, kind in preds[block] if at in exits]
        if block == entry:
            parts.append(seed)
        return rv32_meet(parts)

    states = {entry: joined(entry)}
    work, budget = [entry], 0
    while work and budget < 20000:
        budget += 1
        block = work.pop()
        state = states[block].copy()
        for mnem, ops in blocks[block]:
            rv32_step(state, mnem, ops, data, tags or {})
        exits[block] = state
        for succ, _kind in edges[block]:
            entering = joined(succ)
            if succ not in states or \
                    states[succ].frozen() != entering.frozen():
                states[succ] = entering
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
                name, value = payload
                seen["symstores"].add(name)
                seen["stores"].append((block, (Rv32Where("sym", name), value)))
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


RV32_ARG_REGS = ("a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7")
#: Every name that can only be a REGISTER.  A transfer whose target operand
#: is one of these is INDIRECT: this interpreter reads the emitted operand,
#: and a register it cannot tie to a symbol is a call edge it cannot place.
RV32_REG_NAMES = frozenset(
    ("zero", "ra", "sp", "gp", "tp", "fp") +
    tuple(f"x{n}" for n in range(32)) +
    tuple(f"t{n}" for n in range(7)) +
    tuple(f"s{n}" for n in range(12)) + RV32_ARG_REGS)


def _rv32_forget_symbols(state):
    """Drop every symbol slot the state holds.

    Called wherever a write this resolver CANNOT place may have landed on
    one of this unit's statics: any call, and any store whose base did not
    resolve.  A resolved numeric address and a stack address are not in that
    class -- statics are symbolic in this model and the stack is a different
    object -- so those two leave the slots alone."""
    for key in [key for key in state.mem if key[0] == "sym"]:
        del state.mem[key]


#: Every spelling in which the emitted code takes a symbol's ADDRESS: the
#: `%hi`/`%lo`/`%pcrel` relocations, the `la`/`lla` pseudo-instructions, and
#: a symbol emitted as a data word.  A function whose address is taken can
#: be called from somewhere this unit cannot see, so its arguments may not
#: be resolved from the call sites this unit does see.
RV32_ADDRESS_TAKEN_RE = re.compile(
    r"%(?:hi|lo|pcrel_hi|pcrel_lo|got_pcrel_hi|tprel_hi|tprel_lo)"
    r"\(\s*([A-Za-z_.$][\w.$]*)"
    r"|\b(?:lla|la|lui)\s+[a-z0-9]+\s*,\s*([A-Za-z_.$][\w.$]*)"
    r"|^\s*\.(?:word|4byte|long|dword|8byte|quad)\s+([A-Za-z_.$][\w.$]*)\s*$")


def rv32_address_taken(assembly):
    """Every symbol whose address the emitted code forms."""
    taken = set()
    for line in assembly.splitlines():
        for found in RV32_ADDRESS_TAKEN_RE.finditer(line):
            taken.add(next(name for name in found.groups() if name))
    return taken


def rv32_defined(assembly):
    """Every symbol this translation unit DEFINES: a label it emits, or an
    object it reserves with `.comm`/`.lcomm`.

    The store census needs this to place a store through a symbol's address.
    `extern volatile uint32_t r; r = 1;` also stores through a symbol, and
    where that symbol LANDS is the linker's decision, not this unit's -- so
    a symbol this unit does not define is not one it may place."""
    defined = set()
    for line in assembly.splitlines():
        label = re.match(r"^([A-Za-z_.$][\w.$]*):", line)
        if label:
            defined.add(label.group(1))
            continue
        reserved = re.match(r"^\s*\.l?comm\s+([\w.$]+)", line)
        if reserved:
            defined.add(reserved.group(1))
    return defined


def rv32_call_seeds(runs, private):
    """The entry registers a PRIVATE function can be resolved with: for
    each argument register, the value every call site in this unit hands
    it, or nothing when the sites disagree.

    This is the interprocedural half of the store census.  `parse_u64()`
    and `seconds_to_ns()` write through a caller's pointer, and intra-
    procedurally that pointer is simply unknown -- which under the rule
    that an unplaceable store is a REFUSAL would red the shipping
    firmware.  Resolved from the call sites it becomes a stack address,
    which is a class the census can PLACE."""
    sites = {}
    for run in runs.values():
        for _at, (callee, handed) in run["calls"]:
            if callee in private:
                sites.setdefault(callee, []).append(handed)
    seeds = {}
    for name, handed in sites.items():
        agreed = {}
        for reg in RV32_ARG_REGS:
            values = {site.get(reg) for site in handed}
            if len(values) == 1:
                value = values.pop()
                if value is not None:
                    agreed[reg] = value
        seeds[name] = agreed
    return seeds


def rv32_unit(assembly):
    """Resolve the whole translation unit the census compiled.

    Two passes: the first finds every static the code STORES through, the
    second resolves loads only from statics nothing writes.  A static the
    firmware assigns at run time has no compile-time value, and reporting
    one would be an invented fact rather than a resolved one.

    Then the arguments.  A function this unit does not export and whose
    address it never forms is reached ONLY from the call sites in this
    unit, so the values those sites agree on are the values it starts
    with.  Iterated to a fixpoint, meeting the seeds each round so a
    disagreement can only ever lose precision, and refusing outright if it
    has not settled -- a partial walk is not a measurement."""
    data, functions = rv32_data(assembly), rv32_functions(assembly)
    written = set()
    for body in functions.values():
        written |= rv32_run(body, data)["symstores"]
    data = {name: value for name, value in data.items() if name not in written}
    exported = set(re.findall(r"^\s*\.globa?l\s+([\w.$]+)", assembly,
                              re.MULTILINE))
    addressed = rv32_address_taken(assembly)
    private = {name for name in functions
               if name not in exported and name not in addressed}
    seeds, runs, rounds = {}, None, 0
    while rounds < 8:
        rounds += 1
        runs = {name: rv32_run(body, data, entry_regs=seeds.get(name))
                for name, body in functions.items()}
        found = rv32_call_seeds(runs, private)
        merged = {name: {reg: value
                         for reg, value in found.get(name, {}).items()
                         if name not in seeds or
                         seeds[name].get(reg) == value}
                  for name in functions}
        merged = {name: agreed for name, agreed in merged.items() if agreed}
        if merged == seeds:
            break
        seeds = merged
    else:
        raise AssertionError(
            "the RV32 resolver's interprocedural argument seeding did not "
            "settle, so its answer would depend on how many rounds it was "
            "given rather than on the code")
    return {"data": data, "functions": functions, "runs": runs,
            "private": private, "seeds": seeds, "exported": exported,
            "addressed": addressed, "defined": rv32_defined(assembly)}


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
    """Gate 1b: every tracked config uses the one product CPU contract."""
    for name, path in CONFIGS.items():
        result = eb.build(path, OUT)
        cfg = result["cfg"]
        argv = _canon(result["argv"])
        assert cfg["soc"]["software_profile"] == "baremetal", name
        assert cfg["soc"]["cpu"] == "vexiiriscv", name
        assert cfg["soc"]["xlen"] == 32 and cfg["soc"]["cpu_count"] == 1, name
        assert cfg["soc"]["full"] is True, name
        assert cfg["constraints"]["l2_bytes"] == 0, name
        assert cfg["constraints"]["flashboot"] in ("none", "baremetal"), name
        assert cfg["soc"]["scala_args"] == [], name
        assert cfg["features"]["fabric_gptp"] is True, name
        assert argv["--software-profile"] == ["baremetal"], name
        assert argv["--xlen"] == [32.0] and argv["--l2-bytes"] == [0.0], name
        assert "--full" in argv, name
        assert "--fabric-gptp" in argv, name
        assert "gptp_ucode" in result["paths"], name
        assert "pp_mem" in result["platform"], name

    def set_soc(key, value):
        return lambda cfg: cfg.setdefault("soc", {}).__setitem__(key, value)

    cases = (
        ("RV64", set_soc("xlen", 64)),
        ("two harts", set_soc("cpu_count", 2)),
        ("alternate CPU", set_soc("cpu", "naxriscv")),
        ("cache", lambda cfg: cfg["board"]["constraints"].__setitem__(
            "l2_bytes", 8192)),
        ("scala override", set_soc("scala_args", ["--lsu-l1-ways=2"])),
        ("unknown flash manifest", lambda cfg: cfg["board"]["constraints"].__setitem__(
            "flashboot", "unsupported")),
        ("unknown software profile", set_soc("software_profile", "hosted")),
        ("missing clock attributes", lambda cfg: cfg.pop("gptp", None)),
        ("unknown SoC key", set_soc("unknown_option", True)),
        ("partial SoC", set_soc("full", False)),
        ("unknown constraint key", lambda cfg:
         cfg["board"]["constraints"].__setitem__("unknown_option", True)),
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
    print(f"  [gate 1b] {len(CONFIGS)} product configs and "
          f"{len(cases)} refusal arms pass")


def test_gptp_product_default_and_legacy_option():
    """Gate 1c: fabric ownership is the product default and only config value."""
    default_cfg = _variant(
        CONFIGS["ax7101_1x1_tdm8"],
        lambda cfg: cfg["board"]["features"].pop("fabric_gptp", None))
    try:
        with tempfile.TemporaryDirectory() as out:
            result = eb.build(default_cfg, out)
            assert result["cfg"]["features"]["fabric_gptp"] is True
            assert "--fabric-gptp" in result["argv"]
            assert "--no-fabric-gptp" not in result["argv"]
            assert "gptp_ucode" in result["paths"]
    finally:
        os.unlink(default_cfg)

    disabled = _variant(
        CONFIGS["ax7101_1x1_tdm8"],
        lambda cfg: cfg["board"]["features"].__setitem__("fabric_gptp", False))
    try:
        try:
            eb.load_config(disabled)
        except eb.ConfigError as exc:
            assert "verification-only" in str(exc)
        else:
            raise AssertionError("option-off product configuration was accepted")
    finally:
        os.unlink(disabled)

    soc_source = open(os.path.join(ROOT, "sw/litex/milan_soc.py")).read()
    assert "p_GPTP_PLANE_EN_P=int(bool(gptp_plane))" in soc_source
    assert 'ap.set_defaults(fabric_gptp=None)' in soc_source
    assert 'self._gptp_owner = "software"' not in soc_source
    for launcher in ("sw/litex/sweep.sh", "sw/litex/build.sh",
                     "sw/litex/sweep_extra.sh"):
        source = open(os.path.join(ROOT, launcher)).read()
        assert "--fabric-gptp" in source
        assert "--no-fabric-gptp" not in source
    print("  [gate 1c] fabric ownership is the only product configuration")


def test_qspi_owner_transition_completed_write_prefixes():
    """Gate 1e: every supported persistent write prefix has one owner.

    #259: the one supported persistent image set is the fabric-owned
    bare-metal {bitstream, aem} pair and the one transition is its refresh.
    Unsupported owners and malformed layouts refuse with zero programmer
    I/O, and the compiled CPU-width binding fails closed."""
    with tempfile.TemporaryDirectory() as td:
        fake_bin = os.path.join(td, "bin")
        os.makedirs(fake_bin)
        qspi = os.path.join(td, "qspi.bin")
        log = os.path.join(td, "programmer.log")
        count = os.path.join(td, "programmer.count")
        deploy_tmp = os.path.join(td, "deploy-tmp")
        os.makedirs(deploy_tmp)

        fake_ofl = os.path.join(fake_bin, "openFPGALoader")
        with open(fake_ofl, "w", encoding="utf-8") as stream:
            stream.write(r'''#!/usr/bin/env python3
import os, struct, sys

args = sys.argv[1:]
qspi = os.environ["OFL_QSPI"]
log = os.environ["OFL_LOG"]
count_path = os.environ["OFL_COUNT"]

def value(flag, default=None):
    try:
        return args[args.index(flag) + 1]
    except (ValueError, IndexError):
        return default

def bit_payload(path):
    raw = open(path, "rb").read()
    pos = 2 + struct.unpack_from(">H", raw, 0)[0]
    pos += 2
    while True:
        kind = raw[pos]; pos += 1
        if kind == ord("e"):
            size = struct.unpack_from(">I", raw, pos)[0]; pos += 4
            return raw[pos:pos + size]
        size = struct.unpack_from(">H", raw, pos)[0]; pos += 2 + size

serial = value("--ftdi-serial")
if serial != os.environ.get("OFL_EXPECT_SERIAL", serial):
    raise SystemExit(88)

if "--dump-flash" in args:
    size = int(value("--file-size"), 0)
    off = int(value("-o", "0"), 0)
    out = args[-1]
    with open(qspi, "rb") as source, open(out, "wb") as sink:
        source.seek(off)
        sink.write(source.read(size))
    with open(log, "a", encoding="utf-8") as trace:
        trace.write(f"DUMP\t{off}\t{size}\n")
    mutate = os.environ.get("OFL_MUTATE_BIT")
    replacement = os.environ.get("OFL_MUTATE_FROM")
    if mutate and replacement:
        with open(replacement, "rb") as source, open(mutate, "wb") as sink:
            sink.write(source.read())
    raise SystemExit(0)

is_bit = "-f" in args or "--write-flash" in args and value("-o") is None
is_raw = "--write-flash" in args and value("-o") is not None
if not (is_bit or is_raw):
    raise SystemExit(89)
old_count = int(open(count_path).read()) if os.path.exists(count_path) else 0
index = old_count + 1
if int(os.environ.get("OFL_FAIL_BEFORE", "0")) == index:
    with open(log, "a", encoding="utf-8") as trace:
        trace.write(f"FAIL_BEFORE\t{index}\n")
    raise SystemExit(91)
if "--verify" not in args:
    with open(log, "a", encoding="utf-8") as trace:
        trace.write(f"NO_VERIFY\t{index}\n")
    raise SystemExit(90)
off = 0 if is_bit else int(value("-o"), 0)
source_path = args[-1]
data = bit_payload(source_path) if is_bit else open(source_path, "rb").read()
with open(qspi, "r+b") as flash:
    flash.seek(off)
    flash.write(data)
with open(count_path, "w", encoding="utf-8") as state:
    state.write(str(index))
with open(log, "a", encoding="utf-8") as trace:
    trace.write(f"WRITE\t{index}\t{off}\tverify\t{os.path.basename(source_path)}\n")
if int(os.environ.get("OFL_FAIL_AFTER", "0")) == index:
    raise SystemExit(92)
''')
        os.chmod(fake_ofl, 0o755)

        # This gate intentionally has no LiteX dependency. Implement only the
        # crcfbigen output boundary and delegate every checker/planner command
        # to the real interpreter.
        fake_python = os.path.join(fake_bin, "fixture-python")
        with open(fake_python, "w", encoding="utf-8") as stream:
            stream.write(f'''#!{sys.executable}
import binascii, os, struct, sys
if sys.argv[1:3] == ["-m", "litex.soc.software.crcfbigen"]:
    source = sys.argv[3]
    output = sys.argv[sys.argv.index("-o") + 1]
    data = open(source, "rb").read()
    with open(output, "wb") as sink:
        sink.write(struct.pack("<II", len(data), binascii.crc32(data) & 0xffffffff))
        sink.write(data)
    raise SystemExit(0)
os.execv({sys.executable!r}, [{sys.executable!r}] + sys.argv[1:])
''')
        os.chmod(fake_python, 0o755)

        def make_build(name, owner, serial_payload, manifest="baremetal",
                       extra_rows=(), cpu_xlen=32):
            build = os.path.join(td, name)
            os.makedirs(os.path.join(build, "gateware"))
            bit = os.path.join(build, "gateware", "alinx_ax7101.bit")
            payload = (b"\xff" * 16 + b"\xaa\x99\x55\x66" + serial_payload)
            qspi_transition._fake_bit(bit, payload, name.encode())
            layout = os.path.join(build, "flashboot_layout.json")
            images = [
                {"name": "bitstream", "offset": 0, "budget": 0x400000},
                {"name": "aem", "offset": 0x400000, "budget": 0x10000},
            ] + [dict(row) for row in extra_rows]
            body = {"manifest": manifest, "gptp_owner": owner,
                    "complete": False, "images": images}
            if cpu_xlen is not None:
                body["cpu_xlen"] = cpu_xlen
            aem = os.path.join(build, "aem_desc.bin")
            with open(aem, "wb") as out:
                out.write(b"AEMI" + serial_payload)
            body.update(qspi_transition.bitstream_binding(bit))
            body.update(qspi_transition.aem_image_binding(aem))
            with open(layout, "w", encoding="utf-8") as out:
                json.dump(body, out)
            return {"dir": build, "layout": layout, "bit": bit,
                    "owner": owner, "payload": payload}

        fabric = make_build("fabric", "fabric", b"FABRIC-OWNER-A")
        fabric2 = make_build("fabric2", "fabric", b"FABRIC-OWNER-B")
        mutable_target = make_build(
            "mutable-target", "fabric", b"MUTABLE-TARGET")
        replacement_target = make_build(
            "replacement-target", "fabric", b"UNVALIDATED-REPLACEMENT")
        none_owner = make_build("none-owner", "none", b"NONE-OWNER")
        malformed = make_build("malformed", "fabric", b"MALFORMED-LAYOUT")
        with open(malformed["layout"], encoding="utf-8") as source:
            malformed_layout = json.load(source)
        malformed_layout["images"][1]["offset"] = 0
        with open(malformed["layout"], "w", encoding="utf-8") as out:
            json.dump(malformed_layout, out)
        reserved_collision = make_build(
            "reserved-collision", "fabric", b"RESERVED-COLLISION")
        with open(reserved_collision["layout"], encoding="utf-8") as source:
            reserved_layout = json.load(source)
        reserved_layout["reserved"] = {
            "journal": {"offset": 0x400000, "size": 0x10000}}
        with open(reserved_collision["layout"], "w", encoding="utf-8") as out:
            json.dump(reserved_layout, out)

        base_env = dict(os.environ)
        base_env.update({
            "PATH": fake_bin + os.pathsep + base_env.get("PATH", ""),
            "PYTHON": fake_python,
            "SERIAL": "TEST-SERIAL", "AX_FTDI": "TEST-SERIAL",
            "CABLE": "ft232", "FPGA_PART": "xc7a100tfgg484",
            "OFL_QSPI": qspi, "OFL_LOG": log, "OFL_COUNT": count,
            "OFL_EXPECT_SERIAL": "TEST-SERIAL",
            "TMPDIR": deploy_tmp,
        })

        def reset_flash(source):
            with open(qspi, "wb") as flash:
                flash.truncate(16 * 1024 * 1024)
                flash.seek(0)
                flash.write(source["payload"])
                with open(os.path.join(source["dir"], "aem_desc.bin"),
                          "rb") as artifact:
                    flash.seek(0x400000)
                    flash.write(artifact.read())
            for path in (log, count):
                try:
                    os.unlink(path)
                except FileNotFoundError:
                    pass

        def env_for(source, target, fail_kind=None, fail_index=0):
            env = dict(base_env)
            env.update({"INSTALLED_LAYOUT": source["layout"],
                        "INSTALLED_BIT": source["bit"],
                        "LAYOUT": target["layout"], "BIT": target["bit"],
                        "EXPECTED_GPTP_OWNER": target["owner"]})
            env.pop("OFL_FAIL_BEFORE", None)
            env.pop("OFL_FAIL_AFTER", None)
            env.pop("OFL_MUTATE_BIT", None)
            env.pop("OFL_MUTATE_FROM", None)
            if fail_kind:
                env[f"OFL_FAIL_{fail_kind.upper()}"] = str(fail_index)
            return env

        deploy = os.path.join(SOC_DIR, "deploy.sh")

        def invoke_deploy(argv, env):
            result = subprocess.run(argv, cwd=SOC_DIR, env=env, text=True,
                                    capture_output=True)
            leaked = os.listdir(deploy_tmp)
            assert not leaked, (
                f"deploy transaction leaked staged artifacts after rc "
                f"{result.returncode}: {leaked}\n{result.stdout}{result.stderr}")
            return result

        def run_pair(source, target, fail_kind=None, fail_index=0,
                     reset=True, named=False, env_over=None):
            if reset:
                reset_flash(source)
            env = env_for(source, target, fail_kind, fail_index)
            if env_over:
                env.update(env_over)
            if named:
                argv = [BUILD_SH, "flash", f"ax7101:{target['dir']}"]
            else:
                argv = [deploy, "flash-pair"]
            return invoke_deploy(argv, env)

        def writes():
            if not os.path.exists(log):
                return []
            rows = []
            for line in open(log, encoding="utf-8"):
                fields = line.rstrip("\n").split("\t")
                if fields[0] == "WRITE":
                    rows.append((int(fields[1]), int(fields[2]),
                                 fields[3], fields[4]))
            return rows

        def live_bit(source, target):
            with open(qspi, "rb") as flash:
                live = flash.read(max(len(source["payload"]),
                                      len(target["payload"])))
            old = live[:len(source["payload"])] == source["payload"]
            new = live[:len(target["payload"])] == target["payload"]
            assert old ^ new, (
                f"live bit must identify exactly one owner: "
                f"{source['dir']} old={old}, {target['dir']} new={new}, "
                f"prefix={live[:48].hex()}")
            return source if old else target

        # The one supported transition: a fabric refresh, aem verified first
        # and the target bit committed last, so every completed write prefix
        # boots exactly one fabric owner.
        wanted_offsets = [0x400000, 0]
        total = len(wanted_offsets)
        clean = run_pair(fabric, fabric2)
        assert clean.returncode == 0, clean.stdout + clean.stderr
        assert [row[1] for row in writes()] == wanted_offsets
        assert all(row[2] == "verify" for row in writes())
        assert live_bit(fabric, fabric2) is fabric2

        # The validated source path is deliberately replaced after the live
        # dump and before identify/write. The transaction must still program
        # the immutable staged copy, never reopen the rebuilt source path.
        swapped = run_pair(
            fabric, mutable_target,
            env_over={"OFL_MUTATE_BIT": mutable_target["bit"],
                      "OFL_MUTATE_FROM": replacement_target["bit"]})
        assert swapped.returncode == 0, swapped.stdout + swapped.stderr
        assert live_bit(fabric, mutable_target) is mutable_target, \
            "flash-pair programmed a bitstream replaced after validation"

        checked_prefixes = 0
        for kind in ("before", "after"):
            for index in range(1, total + 1):
                failed = run_pair(fabric, fabric2, kind, index)
                assert failed.returncode != 0, failed.stdout + failed.stderr
                prefix = writes()
                expected = index - 1 if kind == "before" else index
                assert len(prefix) == expected, (kind, index, prefix)
                assert [row[1] for row in prefix] == wanted_offsets[:expected]
                live_bit(fabric, fabric2)     # exactly one owner, always
                checked_prefixes += 1
                resumed = run_pair(fabric, fabric2, reset=False)
                assert resumed.returncode == 0, \
                    resumed.stdout + resumed.stderr
                assert live_bit(fabric, fabric2) is fabric2

        # The named launcher must delegate to the same live-proof transaction.
        named = run_pair(fabric, fabric2, named=True)
        assert named.returncode == 0, named.stdout + named.stderr
        assert [row[1] for row in writes()] == wanted_offsets

        # A live target bit with a stale AEM beside it is safely repaired:
        # the autonomous fabric commit bit owns gPTP independently of AEM.
        reset_flash(fabric)
        with open(qspi, "r+b") as flash:
            flash.seek(0)
            flash.write(fabric2["payload"])
        repair = run_pair(fabric, fabric2, reset=False)
        assert repair.returncode == 0, repair.stdout + repair.stderr
        assert [row[1] for row in writes()] == [0x400000], \
            "AEM repair beside a live fabric commit bit must write AEM only"
        assert live_bit(fabric, fabric2) is fabric2

        # Whole-set preparation happens before even read-only programmer I/O.
        reset_flash(fabric)
        missing_env = env_for(fabric, fabric2)
        missing_env["AEM"] = os.path.join(td, "missing-aem.bin")
        missing = invoke_deploy([deploy, "flash-pair"], missing_env)
        assert missing.returncode != 0
        assert not writes(), "missing AEM artifact caused a programmer write"
        assert not os.path.exists(log), \
            "missing AEM artifact caused read-only programmer I/O"

        def refuse_before_io(label, source, target, needle):
            reset_flash(source)
            refused = invoke_deploy(
                [deploy, "flash-pair"], env_for(source, target))
            output = refused.stdout + refused.stderr
            assert refused.returncode != 0, f"{label}: accepted\n{output}"
            assert needle in output, f"{label}: no {needle!r}\n{output}"
            assert not os.path.exists(log), \
                f"{label} reached programmer I/O"

        refuse_before_io("ownerless bare-metal target", fabric, none_owner,
                         "not flashable")

        # A manifest-row parser failure must propagate before the live dump.
        refuse_before_io("malformed image offsets", fabric, malformed,
                         "unique")
        refuse_before_io("image/reservation collision", fabric,
                         reserved_collision, "reserved")

        # The two opt-in recovery primitives use the same staged custody and
        # must clean it on a nested preflight exit too. This is the dynamic
        # shell-scope case that a RETURN-only trap missed: do_check_images()
        # has its own local `tmp` while refusing the malformed row set.
        for recovery_step in ("flash", "flash-images"):
            reset_flash(fabric)
            recovery_env = env_for(fabric, malformed)
            recovery_env["ALLOW_NONATOMIC_FLASH"] = "1"
            refused = invoke_deploy([deploy, recovery_step], recovery_env)
            assert refused.returncode != 0, (
                f"{recovery_step}: malformed layout accepted\n"
                f"{refused.stdout}{refused.stderr}")
            assert not os.path.exists(log), \
                f"{recovery_step}: malformed layout reached programmer I/O"

        # The compiled CPU width binds fail-closed ([R0] on PR #228): a
        # layout that does not state it, or states an impossible one, refuses
        # before any programmer I/O.
        for label, mutate_xlen in (("missing cpu_xlen",
                                    lambda body: body.pop("cpu_xlen")),
                                   ("invalid cpu_xlen",
                                    lambda body: body.update(cpu_xlen=16))):
            with open(fabric2["layout"], encoding="utf-8") as source:
                unbound_body = json.load(source)
            mutate_xlen(unbound_body)
            unbound_layout = os.path.join(fabric2["dir"],
                                          "unbound-layout.json")
            with open(unbound_layout, "w", encoding="utf-8") as out:
                json.dump(unbound_body, out)
            reset_flash(fabric)
            env = env_for(fabric, fabric2)
            env["LAYOUT"] = unbound_layout
            refused = invoke_deploy([deploy, "flash-pair"], env)
            output = refused.stdout + refused.stderr
            assert refused.returncode != 0, f"{label}: accepted\n{output}"
            assert "compiled CPU width" in output, f"{label}\n{output}"
            assert not os.path.exists(log), f"{label} reached programmer I/O"
            os.unlink(unbound_layout)

        # Persistent targets are identity evidence, never an mtime-selected
        # convenience default.  Omission must fail before live QSPI access.
        for omitted in ("BIT", "LAYOUT"):
            reset_flash(fabric)
            omitted_env = env_for(fabric, fabric2)
            omitted_env.pop(omitted)
            refused = invoke_deploy([deploy, "flash-pair"], omitted_env)
            assert refused.returncode != 0
            assert not os.path.exists(log), \
                f"missing target {omitted} caused programmer I/O"

        # A mutable owner string cannot substitute for exact live QSPI proof.
        reset_flash(fabric)
        with open(qspi, "r+b") as flash:
            flash.write(b"\x00" * len(fabric["payload"]))
        mismatch = invoke_deploy(
            [deploy, "flash-pair"], env_for(fabric, fabric2))
        assert mismatch.returncode != 0
        assert not writes(), "unidentified live bitstream caused a write"

        # An identical-payload refresh is ambiguous and refused.
        refuse_before_io("identical payloads", fabric, fabric, "identical")

    print(f"  [gate 1e] {checked_prefixes} injected before/after-write "
          "prefixes across the fabric-baremetal refresh retain one live "
          "owner and every prefix resumes; all writes verify; a live target "
          "bit gets an AEM-only repair; a source BIT replaced after live "
          "identification cannot replace the validated staged copy; every "
          "success/refusal (including both recovery primitives) cleans its "
          "staged transaction set; the "
          "ownerless owner, malformed/collision layouts, missing artifacts, "
          "missing cpu_xlen x2 and an unidentified live bit all refuse "
          "before programmer I/O")




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
            cm.setdefault("pools", {"pilot": True, "loopback": 4})
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
        # validate_features rightly refuses next to a declared DAC.
        # The replacement feature map keeps the mandatory fabric owner.
        c["board"]["features"] = {"fabric_gptp": True}
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
        m = re.search(r'^OPTS="([^"]*)"\n(?:NS=\d+\n)?L2=(\d+)\n',
                      txt, re.M)
        assert m, f"{p}: fragment lacks OPTS/L2"
        frag[board] = (m.group(1), m.group(2), p)
    for board, (opts, l2, p) in frag.items():
        want_opts, want_l2 = sweep_inline(board)
        assert opts == want_opts, (f"{board}: fragment OPTS != sweep.sh inline\n"
                                   f" frag   {opts!r}\n inline {want_opts!r}")
        assert l2 == want_l2, f"{board}: fragment L2 {l2} != inline {want_l2}"
        print(f"  [gate 9] {board}: generated OPTS/L2 byte-match sweep.sh "
              f"inline table ({len(opts)} chars)")
    for path in [SWEEP] + [p for (_o, _l, p) in frag.values()]:
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

    # #259: the 8x8's listeners are empty-handed (0 physical),
    # so the input face carries eight zero-cluster ports and the 1-key
    # placeholder engine - the same retired posture the 1x1 leg below pins.
    # The output face is the 9-cluster geometry: pilot (13'h1400) then the
    # eight fabric-disabled loopback templates, idxh = the talker's own rx
    # stream so the eight ports stay distinct.
    ax8 = eb.load_config(CONFIGS["ax7101_8x8"])
    h8 = eb.emit_adp_shape_svh(ax8, eb.emit_aem_overlay(ax8))
    assert scalar(h8, "ADP_DMAP_IN_KEYS_C") == 1
    assert array(h8, "ADP_DMAP_IN_PBASE_C") == [0] * 8
    assert array(h8, "ADP_DMAP_IN_PCLS_C") == [0] * 8
    assert array(h8, "ADP_DMAP_IN_PNMAPS_C") == [0] * 8
    assert array(h8, "ADP_DMAP_IN_RPHYS_C") == [0]
    assert array(h8, "ADP_DMAP_OUT_PCLS_C") == [9] * 8
    assert array(h8, "ADP_DMAP_OUT_PCBASE_C") == list(range(0, 72, 9))
    c8 = array(h8, "ADP_DMAP_OUT_CSRC_C")
    assert c8[:9] == [0x1400, 0x0500, 0x0D00, 0x0501,
                      0x0D01, 0x0502, 0x0D02, 0x0503, 0x0D03]
    assert c8[9:18] == [0x1400, 0x0510, 0x0D10, 0x0511,
                        0x0D11, 0x0512, 0x0D12, 0x0513, 0x0D13]

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
    import gen_aem_store as aem_store

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
        # silence. The ship config declares loopback_lane false, and its
        # source topology contains only the live fabric pools, so:
        #   - the identity must be the PILOT tone, the one pool this build
        #     can feed: {valid, src=4 TONE} = 13'h1400
        #   - reserved source encoding 3 may not survive at all
        #     (its old template encoding would be 13'h13xx)
        #   - the loopback templates must still be EMITTED (the clusters
        #     exist and a controller may map to them) but fabric-disabled,
        #     bit 12 clear, so 13'h05xx, never 13'h15xx
        # INIT carries {valid[5], cluster offset[4:0]}; pilot is offset 0
        # and ONE cluster wide, so key 0 of each port reads 6'h20 and the
        # other seven keys wake NOT MAPPED (6'h00) - Milan v1.2 5.3.9.1
        # allows a Stream Output channel to be unmapped, and an unbacked
        # source would be the exact defect this gate exists to refuse.
        assert "13'h1400" in svh, "power-on identity is not the pilot tone"
        assert "13'h13" not in svh, \
            "reserved source encoding 3 survived the #259 cleanup"
        assert "13'h15" not in svh, \
            "a VALID loopback template survived with the lane switched off"
        assert "13'h05" in svh, \
            "loopback templates vanished; the clusters must still be offered"
        assert "AEM_ODMAP_INIT_C [0:63] = '{6'h20, 6'h00, 6'h00, 6'h00, " \
               "6'h00, 6'h00, 6'h00, 6'h00, 6'h20" in svh, \
            "power-on map does not wake on the pilot pool alone"
        print("  [gate 17d] ax7101_8x8 ALL streams dynamic: 8 output ports "
              "n_maps=0, zero AUDIO_MAPs, `AEM_ODYNMAP keys=64 slotb 0..28")
        print("  [gate 17e] lane OFF: power-on identity = PILOT (13'h1400), "
              "reserved source 3 absent (#259), loopback templates emitted "
              "fabric-disabled (13'h05xx) and protocol-mappable")

        # and the OTHER direction: declaring the lane must hand the pool
        # back. ONE fact drives the argv and the map, so they cannot drift.
        def dyn_everything_lane(c):
            dyn_everything(c)
            c["audio_interface"]["cluster_mapping"]["fabric"] = {
                "loopback_lane": True}
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
            # #259: the retired pool is absent, so the old preference has no
            # subject left on this shape - the walk lands on the
            # BACKED loopback pool (offset 1: pilot holds offset 0), which
            # is the D8 point this arm exists for: declaring the lane
            # hands the pool back. INIT co runs 1..8 on every port.
            assert "AEM_ODMAP_INIT_C [0:63] = '{6'h21, 6'h22, 6'h23, " \
                   "6'h24, 6'h25, 6'h26, 6'h27, 6'h28, 6'h21" in svh2, \
                "the power-on map must claim the backed loopback pool"
            assert "--loopback-lane" in eb.emit_design_opts(
                eb.load_config(p2)), \
                "lane declared but milan_soc was never told to build it"
            assert all(q["primary_role"] == "loopback"
                       for q in r2["overlay"]["stream_ports"]["output"])
            print("  [gate 17e] lane ON: loopback valid (13'h1500), "
                  "primary_role/INIT move onto it (6'h21..6'h28) - "
                  "declaring the lane hands the pool back")
        finally:
            os.unlink(p2)
    finally:
        os.unlink(p)

    # gate 17f (#259): the legacy cluster-count policy still carries an
    # explicit physical/virtual source pool when an OUTPUT becomes dynamic.
    # A schema-2.x overlay with that pool missing is stale or hand-mutated;
    # counts cannot reconstruct its source topology. Both consumers must
    # refuse it instead of reviving reserved source encoding 3 as a fallback.
    def dyn_legacy_output(c):
        for s in c["streams"]["talkers"]:
            s["map_mode"] = "dynamic"
    p = _variant(CONFIGS["arty_current"], dyn_legacy_output)
    try:
        r = eb.build(p, OUT)
        cfg = eb.load_config(p)
        ovl = r["overlay"]
        pout = ovl["stream_ports"]["output"][0]
        assert pout["pool"] == [
            {"role": "physical", "offset": 0, "width": 2},
            {"role": "virtual", "offset": 2, "width": 6},
        ]
        spec = aem_store.spec_from_overlay(ovl)
        srcs = spec["ports_out"][0]["cluster_sources"]
        assert [s["src"] for s in srcs] == [2, 2, 0, 0, 0, 0, 0, 0]
        assert [s["valid"] for s in srcs] == \
            [True, True, False, False, False, False, False, False]
        rom_svh = aem_store.emit_svh_text(aem_store.build_model(spec))
        adp_svh = eb.emit_adp_shape_svh(cfg, ovl)
        assert "13'h13" not in rom_svh and "13'h13" not in adp_svh, \
            "reserved source encoding 3 survived a valid legacy-policy map"

        for label, remove_pool in (("missing", True), ("empty", False)):
            bad = copy.deepcopy(ovl)
            if remove_pool:
                del bad["stream_ports"]["output"][0]["pool"]
            else:
                bad["stream_ports"]["output"][0]["pool"] = []
            try:
                aem_store.spec_from_overlay(bad)
            except ValueError as e:
                msg = str(e)
                assert "output[0]" in msg and "pool" in msg, \
                    f"{label} pool: unclear generator refusal: {msg}"
            else:
                raise AssertionError(
                    f"dynamic output with {label} source pool reached the "
                    "descriptor generator")
            try:
                eb.emit_adp_shape_svh(cfg, bad)
            except eb.ConfigError as e:
                msg = str(e)
                assert "output[0]" in msg and "pool" in msg, \
                    f"{label} pool: unclear builder refusal: {msg}"
            else:
                raise AssertionError(
                    f"dynamic output with {label} source pool reached the "
                    "ADP include emitter")

        # Exercise build_model's boundary independently of the overlay
        # helper so deleting that second defence makes this arm fail.
        bad_spec = copy.deepcopy(spec)
        bad_spec["ports_out"][0]["cluster_sources"] = None
        try:
            aem_store.build_model(bad_spec)
        except ValueError as e:
            msg = str(e)
            assert "ports_out[0]" in msg and "source topology" in msg, \
                f"unclear build_model refusal: {msg}"
        else:
            raise AssertionError(
                "dynamic output without cluster_sources reached build_model")
        print("  [gate 17f] dynamic legacy-policy output: explicit physical/"
              "virtual source pool accepted; missing/empty topology refused "
              "by descriptor, model, and ADP consumers")
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
          "mixed output map modes, and missing dynamic-output source "
          "topology raise ConfigError")


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
    ("sw/litex/milan_soc.py", r"\"hdl/common/csr\""),
    ("syn/yosys/run.sh", r"INCDIRS=\([^)]*\"\$R/hdl/common/csr\""),
)

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


def test_platform_gateware_shape():
    """Gate 19: publish only the memory reservation gateware consumes."""
    import json

    for name, path in CONFIGS.items():
        result = eb.build(path, OUT)
        shape = json.load(open(result["paths"]["platform_shape"]))
        assert shape == result["platform"], name
        assert set(shape) == {
            "_schema", "_schema_version", "_generated_by",
            "_source_config", "pp_mem",
        }, f"{name}: platform shape grew an unconsumed field: {set(shape)}"
        assert shape["_schema"] == eb.PLATFORM_SCHEMA_ID
        assert shape["_schema_version"] == "2.0.0"
        assert set(shape["pp_mem"]) == {"phys", "bytes"}
        base = int(shape["pp_mem"]["phys"], 16)
        size = int(shape["pp_mem"]["bytes"], 16)
        assert base == result["cfg"]["platform"]["pp_mem_phys"]
        assert base > 0 and base % 0x1000 == 0
        assert size == eb.PP_MEM_BYTES and size % 0x1000 == 0

    for label, mutate in (
            ("unknown key", lambda cfg: cfg["platform"].__setitem__("mystery", 1)),
            ("retired CSR mirror",
             lambda cfg: cfg["platform"].__setitem__("csr_base", 0x90000000)),
            ("retired interrupt mirror",
             lambda cfg: cfg["platform"].__setitem__("interrupt", 3)),
            ("unaligned processor window",
             lambda cfg: cfg["platform"].__setitem__("pp_mem_phys", 0x12345))):
        path = _variant(CONFIGS["ax7101_1x1_tdm8"], mutate)
        try:
            try:
                eb.load_config(path)
            except eb.ConfigError:
                pass
            else:
                raise AssertionError(f"{label}: invalid platform was accepted")
        finally:
            os.unlink(path)
    print(f"  [gate 19] {len(CONFIGS)} gateware memory reservations contain "
          "only pp_mem; unknown/retired/unaligned inputs are refused")


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

    # REQ-CBS-02: EVERY queue powers up UNSHAPED.
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
    declares `board.features.render_lpf: false`, the only Vivado-priced
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
                         if not cfg["features"].get(key, True)}
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
        ("filter pruned, promiscuous input declared explicitly",
         dict(rx_mac_filter=False),
         lambda c: c.setdefault("platform", {}).update(
             rx_address_filter="promiscuous"), False),
        # the mirror-image lie: a filter with nothing behind it.
        ("playback pruned but the render LPF kept",
         dict(i2s_playback=False, render_lpf=True),
         lambda c: None, True),
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

      * A misspelled optional-block Instance parameter was passed for weeks.
        LiteX does not diagnose a parameter the module does not have - it
        drops it - so the flag pruned nothing and every gate stayed green.
        Gate 23d closed that for the six prune parameters; this one closes it
        for `AUDIO_IF_MASTER_P` / `AUDIO_IF_CLK_HZ_P`.
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
             f"DROPPED, reproducing the silent optional-parameter no-op "
             f"class")

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
    ("optional-parameter class: the SoC passes a name the RTL does not have",
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
    shipped as a bitstream with KL_maap still in it. That is the same silent
    optional-parameter class, so a keyword `**kwargs` would swallow MUST fail
    closed here.
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

    # Every ordinary --no-* flag main() DECLARES must be one main() also READS,
    # and it must stay an off-by-default store_true. `--no-fabric-gptp` is the
    # deliberate exception: it is the negative member of a mutually-exclusive
    # owner group and therefore uses store_false on the shared fabric_gptp
    # destination; gates 1c/1e grade both of its polarities and every carrier.
    # `default=True` on an ordinary --no-* flag inverts the lever in silence
    # (an UNFLAGGED build takes the pruned path), and a flag nothing reads is
    # decorative ABI wearing a CLI hat.
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
        if flag == "--no-fabric-gptp":
            continue
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
        "does not have IS the silent optional-parameter defect: "
        f"{', '.join(sorted(routes))}")
    assert isinstance(out.value, ast.Constant) and out.value.value == 0, (
        f"add_milan_datapath: `{ast.unparse(out)}` - only 0 prunes, any other "
        "value leaves the generate arm elaborated (AREA_BUDGET rule 1)")
    return routes


def _module_source(module):
    """Return the text of the .sv file that declares `module`, or None.

    The datapath's source list is curated in milan_soc.py, but a module's file
    is found here by NAME across hdl/ so this helper cannot be fooled by a
    stale list - a module that exists is found, a module that does not is not.
    """
    for path in sorted(pathlib.Path(ROOT, "hdl").rglob("*.sv")):
        text = path.read_text(errors="replace")
        if re.search(r"^\s*module\s+%s\b" % re.escape(module), text, re.M):
            return text
    return None


def _prune_guard_site(param, rtl):
    """Find the source text that carries `param`'s `generate if`, and the name
    the guard uses there.

    Two shapes are legitimate, and only two:
      * the datapath guards the block itself -> (rtl, param);
      * the datapath binds the parameter into a child module's own parameter,
        `Child #(.CHILD_P (PARAM))`, and the child guards it -> (child, CHILD_P).

    Anything else - including a parameter that is passed to a child which does
    not guard it either - returns (None, param) and fails the gate.
    """
    if re.search(r"generate if \(%s != 0\) begin : \w+" % re.escape(param), rtl):
        return rtl, param

    #: `Module #( .A (X), .B (Y) ) inst (` - the parameter block, balanced
    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*#\s*\(", rtl):
        start = m.end()
        depth, i = 1, start
        while i < len(rtl) and depth:
            if rtl[i] == "(":
                depth += 1
            elif rtl[i] == ")":
                depth -= 1
            i += 1
        params = rtl[start:i - 1]
        bind = re.search(r"\.\s*(\w+)\s*\(\s*%s\s*\)" % re.escape(param), params)
        if not bind:
            continue
        child = _module_source(m.group(1))
        if child is None:
            continue
        if re.search(r"generate if \(%s != 0\) begin : \w+"
                     % re.escape(bind.group(1)), child):
            return child, bind.group(1)
    return None, param


def test_optional_block_names_reach_the_rtl():
    """gate 23d - the DECORATIVE-ABI gate, and the reason it exists is on the
    record: `milan_soc.py` once passed a misspelled optional-block Instance
    parameter, so LiteX silently no-oped it and the flag pruned nothing.
    Nothing caught it because no CI job runs LiteX. This gate parses the three
    files as TEXT and pins them together:

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
        #    the same lie in a different costume.
        #
        #    The guard may be ONE HOP AWAY. When a block is extracted into its
        #    own module the datapath keeps the parameter and binds it to the
        #    child's own name (`.ENABLE_P (LTAP_P)`), and the generate lives in
        #    the child. Following that binding is not a relaxation: the pruned
        #    arm still has to exist and still has to tie its outputs off, just
        #    in the file that now owns the logic. Refusing to follow it would
        #    make the gate forbid extraction rather than forbid a decorative
        #    parameter.
        where, guard = _prune_guard_site(param, rtl)
        assert where is not None, (
            f"{param} guards no `generate if`, in milan_datapath.sv or in any "
            f"module the datapath binds it to")
        g = re.search(r"generate if \(%s != 0\) begin : (\w+)"
                      % re.escape(guard), where)
        tail = where[g.end():]
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
          "AREA_BUDGET tier-1 table row (the silent optional-parameter "
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
    # like the historical misspelling did: argv would carry --loopback-lane, the
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


def test_prune_guard_hop_gate_bites():
    """gate 23d, the ONE-HOP arm. Following a parameter into a child module is
    only safe if the follow refuses everything except a real guarded generate
    with an inert else arm. Each case below is a mutation of the live LTAP
    shape, and every negative one must leave the site unfound.

    The positives matter as much: an arm that only ever returns None is a ban,
    not a gate, so the datapath-local shape and the real one-hop shape are both
    asserted FOUND, with the guard name the site actually uses."""
    local = "generate if (X_P != 0) begin : g_x\n end else begin : g_no_x\n"
    site, guard = _prune_guard_site("X_P", local)
    assert site is local and guard == "X_P", \
        "a datapath-local generate must still be found, under its own name"

    # the live shape: the datapath binds LTAP_P into the bank's ENABLE_P and
    # the bank owns the generate.
    rtl = open(os.path.join(ROOT, "hdl/milan/milan_datapath.sv")).read()
    site, guard = _prune_guard_site("LTAP_P", rtl)
    assert site is not None and guard == "ENABLE_P", (
        "the live one-hop binding .ENABLE_P (LTAP_P) must resolve to the "
        f"bank's own guard, got {guard!r}")
    assert "KL_aaf_latency_tap_bank" in site, \
        "the resolved site must be the bank's source, not some other module"

    # NEGATIVES - each one is a way the follow could be fooled.
    for label, mutant, param in [
        ("no generate anywhere",
         "KL_child #(.ENABLE_P (X_P)) inst (.a(b));", "X_P"),
        ("bound to a module that does not exist",
         "KL_not_a_real_module_at_all #(.ENABLE_P (X_P)) inst (.a(b));", "X_P"),
        ("child exists but guards a DIFFERENT parameter",
         "KL_aaf_latency_tap_bank #(.TIMEOUT_C (X_P)) inst (.a(b));", "X_P"),
        ("parameter never bound at all",
         "KL_aaf_latency_tap_bank #(.ENABLE_P (OTHER_P)) inst (.a(b));", "X_P"),
    ]:
        site, _guard = _prune_guard_site(param, mutant)
        assert site is None, f"one-hop follow accepted {label!r} - it must not"

    # and the else arm is still required AT THE SITE: a child whose generate
    # has no inert arm must not satisfy the gate. Graded on text, because that
    # is what the gate itself reads.
    bank = open(os.path.join(ROOT,
                "hdl/ieee1722/aaf/KL_aaf_latency_tap_bank.sv")).read()
    g = re.search(r"generate if \(ENABLE_P != 0\) begin : (\w+)", bank)
    assert g, "the bank must carry the guarded generate this gate follows to"
    assert re.search(r"end else begin : \w+", bank[g.end():]), \
        "the bank's generate must tie its outputs off in an else arm"
    print("  [gate 23d one-hop] 2 positive site(s) resolved, 4 mutations "
          "refused, inert else arm present at the followed site")


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
                "silent optional-parameter failure reproduced inside the check "
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
#  DEFAULT POLARITY. The seven OPTIONAL_BLOCKS rows default PRESENT and pass
#  their parameter ONLY when pruned, so a default build emits a byte-identical
#  top .v. Fabric gPTP moved to the profile-aware gate 1e when #116 made its
#  RTL default ON.
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
#: profile whose fabric plane is the only time source.
#: time source and no signal.
#:
#: And it was once thought to be the only shape that elaborates anywhere
#: but this bench, which was wrong in both directions (#185): on a stock
#: toolchain NO shape elaborates - this one needs the `baremetal` CPU
#: variant. With the series in sw/litex/patches applied, which apply.sh does
#: and gate 23h proves, every supported shape reaches the datapath Instance.
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
            # Several labels share one command line on purpose; elaborating
            # the same shipping baseline more than once buys nothing.
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



def _why_failed(row):
    """One probe failure as text, with the captured output when there is any.

    LiteX reports through a logger, so several of its refusals arrive as an
    exception whose str() is empty; the reason is in the stream the probe
    redirected.  Both halves are printed or the gate is unactionable.
    """
    err = row.get("error", "no result")
    out = (row.get("output") or "").strip()
    return f"{err}\n      " + out.replace("\n", "\n      ") if out else err


def _prune_contract(got, rows):
    """Every prune-contract violation in one probe result set, as text.

    ONE grader, shared by the gates and by their negative controls, so a
    mutation is proved to turn THE GATE red rather than some weaker
    restatement of it. `rows` are the OPTIONAL_BLOCKS names graded against
    the "present" baseline.
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
    return bad


def _config_argv(name):
    """(cfg, the config's OWN emitted argv, with --entity-gen-dir attached).

    eb.build() writes both the generated include dir the argv points at and
    the processor-memory reservation milan_soc.py reads, so it runs first.
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
    the token under test. The shipping shape declares the gPTP plane, so it is
    also that row's present side; _instance_params elaborates it once.
    """
    cfg, argv = _config_argv(BEHAVIOURAL_CFG)
    flags = {f for f, _p, _w in eb.OPTIONAL_BLOCKS.values()}
    present = [a for a in argv if a not in flags]
    assert "--fabric-gptp" in present, \
        f"{cfg['name']} no longer has the polarity this gate grades " \
        "against"
    runs = [("present", present)]
    runs += [(name, present + [flag])
             for name, (flag, _p, _w) in eb.OPTIONAL_BLOCKS.items()]
    return cfg, runs


def _drop_flag(argv, flag, nargs):
    """argv without `flag` and its nargs values.  Asserts it was there."""
    assert flag in argv, f"{flag} is not on this argv: {' '.join(argv)}"
    i = argv.index(flag)
    return argv[:i] + argv[i + 1 + nargs:]


# =============================================================== gate 1e ====
# The PHC ownership bit crosses four Python call boundaries before it becomes
# p_GPTP_PLANE_EN_P.  Gate 1c proves the public spelling; this gate executes
# the real SoC entry point and observes the parameters handed to
# Instance("milan_datapath").  Both software profiles are graded with the
# option omitted and stated explicitly, plus the shipping build/sweep/deploy
# launchers.  The same grader is reused by mutations that cut each carrier.

GPTP_PROFILE_CASES = (
    ("gptp baremetal default", "ax7101_1x1_tdm8", None, 1),
    ("gptp baremetal explicit", "ax7101_1x1_tdm8", "--fabric-gptp", 1),
    ("gptp ax8x8 default", "ax7101_8x8", None, 1),
    ("gptp ax8x8 fabric explicit", "ax7101_8x8", "--fabric-gptp", 1),
    ("gptp baremetal option-off", "ax7101_1x1_tdm8", "--no-fabric-gptp", 0),
)


def _gptp_without_owner_flag(argv):
    return [a for a in argv
            if a not in ("--fabric-gptp", "--no-fabric-gptp")]


def _launcher_soc_argv(script, args):
    """The milan_soc.py argv printed by a launcher's real dry-run path."""
    proc = subprocess.run(["bash", script] + list(args), cwd=SOC_DIR,
                          text=True, capture_output=True)
    assert proc.returncode == 0, (
        f"{os.path.basename(script)} {' '.join(args)} dry-run failed "
        f"(rc={proc.returncode})\n{proc.stdout[-2000:]}\n"
        f"{proc.stderr[-2000:]}")
    rows = []
    for line in proc.stdout.splitlines():
        if "milan_soc.py" not in line:
            continue
        tokens = shlex.split(line.strip())
        for i, token in enumerate(tokens):
            if os.path.basename(token) == "milan_soc.py":
                argv = tokens[i + 1:]
                if "--output-dir" in argv:
                    j = argv.index("--output-dir")
                    argv[j + 1] = BUILD_OUT_TOKEN
                rows.append(argv)
                break
    assert rows, (f"{os.path.basename(script)} {' '.join(args)} printed no "
                  f"milan_soc.py argv\n{proc.stdout[-2000:]}")
    return rows


def _gptp_instance_runs():
    """Profile/default probes and the three supported shipping entry points."""
    runs, expected = [], {}
    cached = {}
    # Each config's generated directory carries its own fabric microcode.  Do
    # not borrow another configuration's ROM: that would silently break the
    # identity/priority binding this gate is meant to preserve.
    for label, name, flag, want in GPTP_PROFILE_CASES:
        if name not in cached:
            _cfg, base_argv = _config_argv(name)
            cached[name] = _gptp_without_owner_flag(base_argv)
        argv = list(cached[name])
        if flag:
            argv.append(flag)
        argv += ["--output-dir", BUILD_OUT_TOKEN, "--build"]
        runs.append((label, argv))
        expected[label] = want

    build_rows = _launcher_soc_argv(BUILD_SH, ["ax7101", "--dry-run"])
    assert len(build_rows) == 1, \
        f"build.sh ax7101 emitted {len(build_rows)} commands, want 1"
    runs.append(("gptp build.sh shipping", build_rows[0]))
    expected["gptp build.sh shipping"] = 1

    deploy = os.path.join(SOC_DIR, "deploy.sh")
    deploy_rows = _launcher_soc_argv(deploy, ["build", "--dry-run"])
    assert len(deploy_rows) == 1, \
        f"deploy.sh build emitted {len(deploy_rows)} commands, want 1"
    runs.append(("gptp deploy.sh shipping", deploy_rows[0]))
    expected["gptp deploy.sh shipping"] = 1

    sweep_rows = [(label, argv) for label, argv in _recipe_cases()
                  if label == "sweep.sh ax7101"]
    assert len(sweep_rows) == 1, \
        f"sweep.sh ax7101 yielded {len(sweep_rows)} recipes, want 1"
    runs.append(("gptp sweep.sh shipping", sweep_rows[0][1]))
    expected["gptp sweep.sh shipping"] = 1
    return runs, expected


def _gptp_instance_contract(got, expected):
    """Every ownership violation in a probe set, shared with mutations."""
    bad, params = [], {}
    for label, want in expected.items():
        row = got.get(label) or {"error": "case not run"}
        if "params" not in row:
            bad.append(f"{label}: never reached the datapath Instance: "
                       f"{_why_failed(row)}")
            continue
        p = params[label] = row["params"]
        if p.get("p_GPTP_PLANE_EN_P") != want:
            bad.append(
                f"{label}: p_GPTP_PLANE_EN_P="
                f"{p.get('p_GPTP_PLANE_EN_P', '<absent>')!r}, want {want}")
        has_rom = "p_GPTP_UCODE_HEX_P" in p
        if has_rom != bool(want):
            bad.append(f"{label}: gPTP ROM is "
                       f"{'present' if has_rom else 'absent'} with plane "
                       f"{'on' if want else 'off'}")
        if has_rom and not os.path.isabs(p["p_GPTP_UCODE_HEX_P"]):
            bad.append(f"{label}: gPTP ROM path is not absolute")
    for default, explicit in (("gptp baremetal default",
                               "gptp baremetal explicit"),
                              ("gptp ax8x8 default",
                               "gptp ax8x8 fabric explicit")):
        if default in params and explicit in params \
                and params[default] != params[explicit]:
            changed = sorted(k for k in set(params[default]) | set(params[explicit])
                             if params[default].get(k) != params[explicit].get(k))
            bad.append(f"{default}: omission differs from the explicit owner "
                       f"at {changed}")
    return bad


def test_gptp_plane_reaches_the_instance():
    """Gate 1e: both owner states reach the real RTL Instance."""
    python = _litex_or_skip("gate 1e")
    if python is None:
        return
    runs, expected = _gptp_instance_runs()
    got = _instance_params(python, runs)
    bad = _gptp_instance_contract(got, expected)
    assert not bad, "gate 1e:\n  " + "\n  ".join(bad)

    # #259: option-off is VERIFICATION-ONLY hardware on every profile. The
    # bare-metal option-off case above already proves it reaches the real
    # Instance with the plane off; here the soc must have said so out loud
    # (zero gPTP owners, not a supported product image).
    off_run = got.get("gptp baremetal option-off", {})
    assert "params" in off_run, \
        "option-off verification elaboration did not reach the Instance"
    # The out-loud announcement itself is pinned as source text by gate 1c
    # ("VERIFICATION-ONLY" in milan_soc.py, beside the removed coupling).
    print(f"  [gate 1e] {len(runs)} real elaborations: the product fabric "
          "default is identical across product shapes and to explicit ON; "
          "bare-metal option-OFF elaborates as announced verification-only "
          "hardware (#259); build.sh, sweep.sh and deploy.sh ship fabric "
          "ownership")


GPTP_INSTANCE_MUTATIONS = (
    ("main ties the parsed owner off",
     [("gptp_plane=args.fabric_gptp,", "gptp_plane=False,", 1)],
     "gptp baremetal explicit"),
    ("MilanSoC drops its owner carrier",
     [("\n" + " " * 34 + "gptp_plane=gptp_plane,\n",
       "\n" + " " * 34 + "gptp_plane=None,\n", 1)],
     "gptp baremetal explicit"),
    ("MilanNIC drops its owner carrier",
     [("\n" + " " * 27 + "gptp_plane=gptp_plane,\n",
       "\n" + " " * 27 + "gptp_plane=None,\n", 1)],
     "gptp baremetal explicit"),
    ("the emitted parameter is tied on",
     [("p_GPTP_PLANE_EN_P=int(bool(gptp_plane))",
       "p_GPTP_PLANE_EN_P=int(True)", 1)],
     "gptp baremetal option-off"),
    ("the emitted parameter is inverted",
     [("p_GPTP_PLANE_EN_P=int(bool(gptp_plane))",
       "p_GPTP_PLANE_EN_P=int(not gptp_plane)", 1)],
     "gptp baremetal explicit"),
    ("the omission default stops selecting the product owner",
     [('args.fabric_gptp = not args.no_milan',
       'args.fabric_gptp = False', 1)],
     "gptp ax8x8 default"),
)


def test_gptp_plane_instance_gate_bites():
    """Gate 1e negative controls: every Python carrier cut turns it red."""
    python = _litex_or_skip("gate 1e mutation")
    if python is None:
        return
    runs, expected = _gptp_instance_runs()
    cases = dict(runs)
    for why, mutations, label in GPTP_INSTANCE_MUTATIONS:
        got = _instance_params(python, [(label, cases[label])], mutations)
        bad = _gptp_instance_contract(got, {label: expected[label]})
        assert bad, f"gate 1e accepted a tree where {why}"
    print(f"  [gate 1e mutation] {len(GPTP_INSTANCE_MUTATIONS)}/"
          f"{len(GPTP_INSTANCE_MUTATIONS)} owner-carrier cuts rejected")


def test_optional_blocks_reach_the_instance():
    """gate 23f - THE BEHAVIOURAL PRUNE PROOF (issues #130, #154).

    Every OPTIONAL_BLOCKS row is graded on the
    parameters that actually reach Instance("milan_datapath", ...) in a real
    elaboration of the shipping configs.  A prune must land as `p_<PARAM>=0`
    AND MUST CHANGE NOTHING ELSE - a flag that prunes the wrong block is the
    same silent lie as a flag that prunes nothing."""
    python = _litex_or_skip("gate 23f")
    if python is None:
        return
    cfg, runs = _behavioural_runs()
    t0 = time.time()
    got = _instance_params(python, runs)
    bad = _prune_contract(got, list(eb.OPTIONAL_BLOCKS))
    assert not bad, "gate 23f:\n  " + "\n  ".join(bad)
    base = got["present"]["params"]
    print(f"  [gate 23f] {len({tuple(a) for _l, a in runs})} real "
          f"milan_soc.py elaborations of {cfg['name']}, the shipping AX "
          f"shape, in {time.time() - t0:.0f} s: each of the "
          f"{len(eb.OPTIONAL_BLOCKS)} --no-* flags lands as p_<PARAM>=0 in "
          f'the Instance("milan_datapath") parameters and moves NOTHING '
          f"else, a build that prunes nothing passes none of them "
          f"({len(base)} parameters, byte-identical top .v). Fabric gPTP's product "
          f"default is graded separately by gate 1e. This grades what "
          f"elaboration HANDS the module, not "
          f"what the module DOES with it (gate 23d) and not that the "
          f"bitstream places or boots")


def test_optional_block_instance_gate_bites():
    """Gate 23f negative controls - the hops a spelling gate cannot see.

    Each row deletes, renames or inverts ONE link of the argv -> Instance
    chain in milan_soc.py's source and re-runs the gate's OWN grader over the
    same real elaborations, so what is proved is that THE GATE goes red, not
    that some weaker restatement of it does.

    Most controls leave every OTHER gate in this file green, which is the
    whole reason this gate exists.  The controls that do not are gate 23d's
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
    ]
    t0 = time.time()
    for why, mutations, rows, inverted in controls:
        labels = ["present"] + rows
        got = _instance_params(python, [(lbl, cases[lbl]) for lbl in labels],
                               mutations)
        bad = _prune_contract(got, rows)
        assert bad, (f"gate 23f accepted a milan_soc.py in which {why} "
                     f"({mutations[0][0]!r} -> {mutations[0][1]!r})")
        want = rows[0]
        assert any(line.startswith(f"{want}:") for line in bad), \
            f"{why}: gate 23f went red for the wrong row: {bad}"
    print(f"  [gate 23f mutation] {len(controls)}/{len(controls)} broken "
          f"links of the argv -> Instance chain rejected in "
          f"{time.time() - t0:.0f} s: a dropped CLI handoff, two dropped "
          "constructor keywords, a dropped keyword inside "
          "add_milan_datapath, a suppressed parameter, a renamed parameter, "
          "and both prune polarities inverted; gate 1e separately owns the "
          "profile-aware gPTP chain")


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
#        and the one the board-to-board analog loop runs through;
#        endstation_arty_current.yaml streams
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
    assert any("i2s_pads[0]" in b for b in binds), \
        ("no build binds o_i2s_mclk_o to i2s_pads[0] - the Pmod I2S2 "
         "MCLK (pmoda:4, ball D13) feeds the CS5343 ADC; without it the "
         "board's only working audio input is dead")
    for b in binds:
        assert "i2s_pads[0]" in b or "tdm_pads" in b, (
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
     "soc", ('platform.add_extension(_arty_serial_io("tdm", "pmodb"))',
             "pass")),
    # THE (b) HALF: i2s_mclk moved off the Pmod.
    ("i2s_mclk is bound to a bare Signal() - off pmoda:4 (D13), the CS5343 "
     "MCLK, on the board whose I2S path is the project's negative control",
     "soc", ("o_i2s_mclk_o=(i2s_pads[0] if i2s_pads else Signal()),",
             "o_i2s_mclk_o=Signal(),")),
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
     "argv_soc", (('platform.add_extension(_arty_serial_io("tdm", "pmodb"))',
                   "pass"),
                  (True, ["--board", "arty", "--audio-interface", "tdm8",
                          "--audio-interface-master"]))),
]


#: gate 24e: the 8.3b BLEND bindings - (label, which, regex) that must all
#: hold, and each is mutated below to prove it can fail. The blend is three
#: bindings: the parameter NAME reaches the RTL (the silent no-op class),
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
     # _board_audio_ports() returns None when the board has no I2S front end;
     # the blend branch is guarded by that same physical-pad fact.
     r'dp_ports\[\s*["\']o_i2s_mclk_o["\']\s*\]\s*=\s*i2s_pads\[0\]'),
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
    _ARTY_TDM_EXT = 'platform.add_extension(_arty_serial_io("tdm", "pmodb"))'
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
    # (a) the AX shape as shipped since #259: 0 physical, pilot, loopback 8.
    #     Those are the complete live fabric pools. The listeners are
    #     therefore empty-handed: the STREAM_PORT_INPUTs
    #     exist and stay dynamically mapped (Milan 5.3.3.9) but truthfully
    #     own ZERO local AUDIO_CLUSTER descriptors - the retired posture,
    #     pinned.
    r = eb.build(CONFIGS["ax7101_8x8"], OUT)
    ovl = r["overlay"]
    check_port_layout(ovl, 8, 8)
    assert ovl["cluster_policy"] == "role-pools"
    assert ovl["physical_binding"]["physical_channels"] == \
        {"capture": 0, "render": 0}, "the AX routes no audio pins"
    P_in, P_out = ovl["stream_ports"]["input"], ovl["stream_ports"]["output"]
    assert all(p["clusters"] == 0 for p in P_in), P_in         # no pool at all
    assert all(p["pool"] == [] for p in P_in), P_in
    assert all(p.get("map_mode") == "dynamic" for p in P_in), P_in
    assert all(p["clusters"] == 9 for p in P_out), P_out       # 1 + 8
    assert ovl["descriptor_counts"]["AUDIO_CLUSTER"] == 8*0 + 8*9 == 72
    assert all(g["role"] != "physical" for p in P_in + P_out for g in p["pool"]), \
        "a board with 0 routed channels must emit NO physical clusters"
    # (b) the primary segment: an empty-handed listener has none (#259),
    #     and the talkers fall through to the first pool this BUILD can
    #     actually feed (task #65). LOOPBACK is still the pool the USER
    #     asked for (2026-07-28) and it comes back the moment
    #     cluster_mapping.fabric.loopback_lane is declared, which gate 17e
    #     proves in both directions; with the lane off, pointing the power-on
    #     image at it would advertise a source milan_datapath does not carry,
    #     so the identity is the PILOT tone. Since the 08-01 flip the ship
    #     talkers are map_mode dynamic (no AUDIO_MAP descriptors), so the
    #     identity lives in the DYNAMIC engine's power-on image
    #     (AEM_ODMAP_INIT_C).
    assert all(p["primary_role"] is None for p in P_in)
    lane = (eb.load_config(CONFIGS["ax7101_8x8"])["interface"]
            ["cluster_fabric"]["loopback_lane"])
    want = "loopback" if lane else "pilot"
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
        # #259: the want pool is no longer 8 wide on every shape (pilot is
        # ONE cluster), so only its width's worth of keys may arm; the rest
        # of each port's eight keys wake NOT MAPPED, which Milan v1.2
        # 5.3.9.1 makes explicit and legal - never on an unbacked source.
        armed_w = min(seg["width"], 8)
        for k, v in enumerate(vals):
            if k % 8 < armed_w:
                assert v >> 5 == 1, f"identity key {k} not armed"
                assert (v & 0x1F) == seg["offset"] + k % 8, \
                    f"identity key {k} cluster {v & 0x1F} outside {want} pool"
            else:
                assert v == 0, f"identity key {k} armed past the {want} pool"
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
    print(f"  [gate 24a] ax7101_8x8 role-pools: 72 AUDIO_CLUSTERs "
          f"(8x empty-handed in, #259; 8x pilot1+loopback8 out), 0 physical "
          f"because the board routes none, talker map -> {want} (fabric lane "
          f"{'on' if lane else 'off'}), 8 distinct loopback sources offered")

    # (d) physical pool APPEARS when the platform declares routed channels
    p = _pools_variant("ax7101_8x8", {"capture": 16, "render": 16},
                       {"pilot": True, "loopback": 2})
    try:
        r = eb.build(p, os.path.join(OUT, "_pools"))
        P = r["overlay"]["stream_ports"]["output"][0]
        assert [g["role"] for g in P["pool"]] == \
            ["physical", "pilot", "loopback"], P
        assert P["clusters"] == 16 + 1 + 2
        # With physical present the static map still does NOT go to loopback -
        # that was and remains the point of this assertion. The 0x0043
        # old preference order lost its subject when the retired pool was
        # removed (#259), so the identity lands on PHYSICAL (this variant is
        # not the shipped
        # AX, whose declared truth stays 0 routed channels), and the
        # UNBACKED loopback pool is never a candidate (task #65).
        assert P["primary_role"] == "physical", P["primary_role"]
        assert [g["role"] for g in P["pool"]][0] == "physical", \
            "cluster numbering must stay physical-first"
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

    # (e) BOUNDARY: an over-wide loopback pool is the shape D8 sketches and
    #     D6 predicted could not be stored - it must VALIDATE and be marked,
    #     not crash and not silently wrap the 16-bit ROM address space.
    #     With only live fabric roles, loopback widens 64 -> 72 so the
    #     per-output-port total stays 89
    #     and the deliberate overflow is preserved (840 clusters at 90 B
    #     put the ROM at 80873 B, still past the 65536 B store).
    p = _pools_variant("ax7101_8x8", {"capture": 16, "render": 16},
                       {"pilot": True, "loopback": 72})
    try:
        r = eb.build(p, os.path.join(OUT, "_pools"))
        assert r["overlay"]["descriptor_counts"]["AUDIO_CLUSTER"] == \
            8*16 + 8*(16+1+72), r["overlay"]["descriptor_counts"]
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
    print("  [gate 24a] the over-wide (72) D8 loopback pool VALIDATES, "
          "exceeds the 16-bit AEM store address space, is marked rather "
          "than emitted, and --write-rtl REFUSES it (D6 is the owner)")


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
             "pools", {"pilot": True, "tdm": 8})),
        # every pool zero: empty-handed STREAM_PORT_INPUTs are legal since
        # #259, but a STREAM_PORT_OUTPUT with no cluster block still is not
        # - a talker needs a source, so the refusal stands
        ("all pools zero", "ax7101_8x8",
         lambda c: c["audio_interface"]["cluster_mapping"].__setitem__(
             "pools", {"pilot": False, "loopback": 0})),
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
        # Role and name must agree; a pilot label on any other role would be
        # exactly the lie D10 exists to remove.
        cnames = r["cfg"]["interface"].get("channel_names") or []
        for c in cl:
            if c["role"] == "pilot":
                assert c["name"] == "Pilot Tone", c
            elif c["role"] == "loopback":
                assert c["name"].startswith("Loopback S"), c
                # channel_names reach the loopback suffix too
                if cnames:
                    assert c["name"].split()[-1] in cnames, c
            elif c["role"] == "virtual":
                assert c["name"].startswith("Virtual "), c
            else:
                assert c["role"] == "physical", c
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
    # (loopback 4 against the base's 8 - one width apart is enough)
    p = _pools_variant("ax7101_8x8", {"capture": 0, "render": 0},
                       {"pilot": True, "loopback": 4})
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
    # shipped input dynamic and removed its forbidden AUDIO_MAP,
    # then -> 0x001BC5B17E3D155F when #259 stated the fabric owner's gptp:
    # section on the retired Arty configs (the section joins model_shape by
    # design; its values restate the historical descriptor constants
    # byte-exactly, and the served id itself stays pinned),
    # then -> 0x001BC5D471D5A5E1 when the gptp: section stopped restating
    # the historical clock_accuracy 0x21 / log_sync_interval 0 and derives
    # the engine's announced 0xFE / -3 instead ([R-parallel] on #228):
    # AVB_INTERFACE clock fields are descriptor content, so 6.2.2.8 obliges
    # the move, while the served id itself stays pinned.
    assert eb.load_config(CONFIGS["arty_current"])["model_id"]["hash"] == \
        "0x001BC5D471D5A5E1"
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
    # went 2 -> 3 and AUDIO_CLUSTER grew from the 2013 87 octets to 2021's 90,
    # and a SEVENTH -> 0x001BC565D9B48CD0 when #259 stated the fabric owner's
    # gptp: section on the retired Arty configs (the section joins
    # model_shape by design; its values restate the historical descriptor
    # constants byte-exactly), and an EIGHTH -> 0x001BC5E53D97FC91 when that
    # restatement was itself retired: clock_accuracy 0x21 / log_sync_interval
    # 0 are deleted and the builder derives the engine's announced 0xFE / -3
    # ([R-parallel] on #228), which is descriptor content per 7.2.8.
    # `interface.kind`, the descriptor set and
    # the byte layout are all model-shaping, so a shape change SHOULD move a
    # hash-derived id - that is the mechanism working. What must NOT move is
    # arty_current's PINNED id above, and it has not: it was re-pinned by hand
    # with the reflash, which is the only way a pin is allowed to move.
    assert eb.load_config(CONFIGS["arty_4x4"])["model_id"]["hash"] == \
        "0x001BC5E53D97FC91"
    print("  [gate 24c] every cluster named for its ROLE; renaming leaves "
          "entity_model_id frozen (1722.1 6.2.2.8 exclusion list) while a "
          "pool width moves it; pre-D8 hashes stay explicitly pinned to "
          "their current model")


def cluster_name_census(name):
    """Every cluster name the builder produces for config `name`: per
    direction, one list per STREAM_PORT in port order, names in offset order.
    Read off the overlay, which is what gen_aem_store turns into descriptor
    bytes, so a name is counted where it ships rather than where it is made."""
    ovl = eb.build(CONFIGS[name], OUT)["overlay"]
    census = {}
    for direction in ("input", "output"):
        ports = ovl["stream_ports"][direction]
        slot = {p["index"]: k for k, p in enumerate(ports)}
        rows = [[] for _ in ports]
        for c in sorted(ovl["audio_clusters"],
                        key=lambda c: (c["port_index"], c["offset"])):
            if c["direction"] == direction:
                rows[slot[c["port_index"]]].append(c["name"])
        assert [len(r) for r in rows] == [p["clusters"] for p in ports], name
        census[direction] = rows
    return census


def write_cluster_names_golden():
    """Regenerate cluster_names_golden.json from the current builder."""
    golden = {
        "_generated_by": "python3 sw/builder/test_builder.py --write-cluster-golden",
        "_what": "gate 24d: every AUDIO_CLUSTER object_name the builder "
                 "produces, per config, direction and STREAM_PORT, in offset "
                 "order; regenerate only for a deliberate naming change",
    }
    for name in CLUSTER_NAMES_GOLDEN_CONFIGS:
        golden[name] = cluster_name_census(name)
    with open(CLUSTER_NAMES_GOLDEN, "w") as f:
        json.dump(golden, f, indent=1)
        f.write("\n")
    print(f"wrote {CLUSTER_NAMES_GOLDEN}")


def test_d10_cluster_namer_paths():
    """gate 24d - the cluster namers: the two paths a live config does not
    reach, and the moved logic pinned name by name.

    Rule 2 (docs/development/CODE_QUALITY.md) turned an `if/elif/elif/else`
    chain nested inside two loops into a named table. Two of its paths were
    only ever reachable through that nesting and had no arm:

      * the loopback namer with an EMPTY receive channel space. A talker whose
        entity declares no listener has nothing to walk, and the cluster is
        named by its own offset instead. The old shape reached this with a
        `continue` five levels deep, so nothing graded it.
      * a pool role with no namer. The old shape's bare `else` swallowed any
        unknown role and named it as a loopback channel; the table refuses it
        by name. The set is closed today, which is exactly why the refusal
        needs an arm - an unreachable path with no test is how the next role
        gets silently mislabelled.

    Those two arms grade the paths; the golden below grades what the refactor
    MOVED. The talker-t -> rx-stream-t walk, the `+ n` channel step and the
    channel_names mapping survive only as names, and gate 24c checks loopback
    names by prefix and physical names by label, so `rx_index() -> 0`,
    dropping `+ n`, and a physical namer that ignores channel_names each
    moved 56, 63 and 8 real names past every builder gate. Every name the
    builder produces for the loopback-bearing ax7101_8x8 (both directions:
    its listeners are headless, and the golden records those empty ports
    too) and for the channel_names config ax7101_1x1_tdm8 is therefore pinned
    in cluster_names_golden.json, generated from the implementation that a
    replay of every cluster_names() call proved byte-identical to the
    pre-refactor chain. Each of those three mutations fails here.
    """
    cfg = eb.load_config(CONFIGS["ax7101_8x8"])

    # -- the empty-rx loopback path -----------------------------------------
    headless = dict(cfg, listeners=[])
    port = {"index": 0, "clusters": 3,
            "pool": [{"role": "loopback", "width": 3, "first": 0, "offset": 0}]}
    got = eb.cluster_names(headless, port, "output")
    assert got == ["Loopback ch 0", "Loopback ch 1", "Loopback ch 2"], got

    # and with a receive space present the SAME pool names real sources, so
    # the arm above is not passing because the namer is inert
    live = eb.cluster_names(cfg, port, "output")
    assert live != got and all(n.startswith("Loopback S") for n in live), live

    # -- the unknown-role refusal -------------------------------------------
    bogus = {"index": 0, "clusters": 1,
             "pool": [{"role": "teleport", "width": 1, "first": 0, "offset": 0}]}
    try:
        eb.cluster_names(cfg, bogus, "output")
    except eb.ConfigError as e:
        assert "teleport" in str(e) and "loopback" in str(e), str(e)
    else:
        assert False, ("an unknown pool role must be refused by name, not "
                       "silently named as a loopback channel")

    # -- every known role still has a namer, and the table IS the dispatch ---
    assert set(eb.CLUSTER_NAMERS) == {"physical", "virtual", "pilot", "loopback"}, \
        eb.CLUSTER_NAMERS
    for direction, roles in eb.PRIMARY_ROLE_ORDER.items():
        for role in roles:
            assert role in eb.CLUSTER_NAMERS, (
                f"{role} is a primary role for {direction} but has no namer")

    # -- the moved logic itself, name by name --------------------------------
    with open(CLUSTER_NAMES_GOLDEN) as f:
        golden = json.load(f)
    pinned = 0
    for name in CLUSTER_NAMES_GOLDEN_CONFIGS:
        got = cluster_name_census(name)
        for direction in ("input", "output"):
            want = golden[name][direction]
            assert len(got[direction]) == len(want), (
                f"{name}: builds {len(got[direction])} STREAM_PORT_"
                f"{direction.upper()}s, the golden pins {len(want)}")
            for pi, (w, g) in enumerate(zip(want, got[direction])):
                assert g == w, (
                    f"{name} STREAM_PORT_{direction.upper()} {pi}: cluster "
                    f"names moved\n  golden: {w}\n  built:  {g}\n"
                    "a deliberate naming change regenerates the golden with "
                    "`python3 sw/builder/test_builder.py --write-cluster-golden`"
                    " and the diff of that file is the review")
                pinned += len(w)
    # the golden must pin the two behaviours it exists for, so an emptied or
    # truncated file cannot pass by matching nothing
    flat = [n for name in CLUSTER_NAMES_GOLDEN_CONFIGS
            for ports in golden[name].values() for p in ports for n in p]
    assert sum(1 for n in flat if n.startswith("Loopback S")) >= 64, \
        "the golden pins no loopback walk"
    cnames = eb.load_config(CONFIGS["ax7101_1x1_tdm8"])["interface"]["channel_names"]
    assert cnames and all(any(n.endswith(" " + c) for n in flat) for c in cnames), \
        "the golden pins no channel_names mapping"
    print("  [gate 24d] empty-rx loopback names by offset (and by source when "
          "a receive space exists), an unknown role is refused by name, "
          "every primary role in PRIMARY_ROLE_ORDER has a namer, and "
          f"{pinned} cluster names across {len(CLUSTER_NAMES_GOLDEN_CONFIGS)} "
          "configs match the tracked golden name for name")


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



def test_gptp_domain_is_one_source():
    """Gate 26: Milan domain 0 is a structural protocol fact.

    A non-zero configuration must be refused with the governing clause. The
    one legal value still reaches the normalized fabric configuration, but it
    must not create a generated reset constant or mutable CSR shadow: the
    public CSR readback and the protocol-facing output are literal zero in
    both fabric-on and verification option-off shapes.
    """
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
    legal = _variant(CONFIGS["ax7101_1x1_tdm8"],
                     lambda c: c["gptp"].__setitem__("domain", DOM))
    try:
        r = eb.build(legal, OUT)
    finally:
        os.unlink(legal)

    # 1. The legal config value survives normalization and reaches the fabric
    # configuration artifact. It does not generate a second RTL authority.
    assert r["cfg"]["gptp"]["domain"] == DOM
    assert r["overlay"]["gptp"]["domain"] == DOM
    assert "ADP_GPTP_DOMAIN_C" not in r["adp_shape_svh"], \
        "the retired generated domain shadow has returned"

    # 2. CSR readback and the protocol-facing output are structural zero.
    # Neither expression is conditional on GPTP_PLANE_EN_P, so both supported
    # elaboration shapes expose the same Milan domain.
    csr = open(MILAN_CSR_SV).read()
    assert re.search(r"A_ADP_DOMAIN\s*:\s*live_mux\s*=\s*32'd0\s*;", csr), \
        "A_ADP_DOMAIN readback is not structural domain 0"
    assert re.search(r"assign\s+o_adp_gptp_domain\s*=\s*8'd0\s*;", csr), \
        "the protocol-facing domain is not structural domain 0"
    assert not re.search(r"\badp_domain\s*(?:<=|=)", csr), \
        "a mutable ADP domain shadow has returned"

    # 3. Walk the public output into the protocol plane by name. The byte-48
    # placement lives in the pinned submodule; this repository owns the chain
    # to that boundary.
    dp = open(os.path.join(ROOT, "hdl/milan/milan_datapath.sv")).read()
    assert re.search(r"\.o_adp_gptp_domain\s*\(\s*cfg_adp_gptp_domain\s*\)",
                     dp), "milan_datapath does not take the CSR's domain"
    assert re.search(r"\.gptp_domain_i\s*\(\s*cfg_adp_gptp_domain\s*\)", dp), \
        "the ADP advertiser is not fed the CSR's domain"
    print(f"  [gate 26] gptp.domain 3 REFUSED with the 802.1AS-2011 "
          f"8.1 clause; legal domain {DOM} reaches fabric configuration; "
          f"CSR readback and protocol output are structural 0 in both shapes; "
          f"the chain reaches the advertising plane's gptp_domain_i")


def test_gptp_dataset_matches_engine_announce():
    """Gate 26b: the AVB_INTERFACE clock dataset IS the engine's Announce.

    THE DEFECT THIS GATE CLOSES ([R-parallel] on #228).  The builder
    accepted nine gptp fields and published all of them in AVB_INTERFACE,
    but ROM generation forwarded only MAC, priority1 and the clock
    frequency; the pinned engine hardcodes priority2, clockQuality and
    every logMessageInterval octet and transmits THOSE.  So the ax7101
    configs advertised offset_scaled_log_variance 0xFFFF while the engine
    announced 0x436A, and the arty configs advertised clock_accuracy 0x21
    while it announced 0xFE - a controller comparing the descriptor with
    the wire saw two different clocks.  The fix is DERIVATION: the builder
    parses the generator's live constants, fills every non-consumed field
    from them, and refuses a config that states anything else (gate 1b
    owns the refusal arms; this gate owns the bytes and the parser).

    Read here as well as in the builder: the expected values below come
    from this test's OWN parse of gptp-processor/hdl/ucode/
    gen_gptp_ucode.py, so a removed or cross-wired mapping in
    endstation_builder fails byte-for-byte instead of comparing the
    builder's derivation with itself."""
    gen = open(os.path.join(
        ROOT, "gptp-processor/hdl/ucode/gen_gptp_ucode.py")).read()
    live = [ln.split("#", 1)[0] for ln in gen.splitlines()]

    def one(pat, what):
        hits = [m.group(1) for ln in live for m in [re.match(pat, ln)] if m]
        assert len(hits) == 1, \
            f"{what}: {len(hits)} live matches in gen_gptp_ucode.py, need 1"
        return int(hits[0], 0)

    p2 = one(r"P1_C\s*,\s*P2_C\s*=\s*\d+\s*,\s*(\d+)\s*$", "P2_C")
    cq = one(r"CQ_C\s*=\s*(0[xX][0-9A-Fa-f]+)\s*$", "CQ_C")
    n = r"(?:0[xX][0-9A-Fa-f]+|\d+)"
    logints = {}
    for mtype, name in (("0x0", "Sync"), ("0xB", "Announce"),
                        ("0x2", "Pdelay_Req")):
        v = one(rf"\s*e_hdr\(p,\s*{mtype},\s*{n},\s*\w+,\s*({n}),\s*\d+\)\s*$",
                f"{name} e_hdr")
        logints[name] = v - 256 if v >= 128 else v
    wire = dict(priority2=p2,
                clock_class=(cq >> 24) & 0xFF,
                clock_accuracy=(cq >> 16) & 0xFF,
                offset_scaled_log_variance=cq & 0xFFFF,
                log_sync_interval=logints["Sync"],
                log_announce_interval=logints["Announce"],
                log_pdelay_interval=logints["Pdelay_Req"])

    # 1. the builder's derivation agrees with this parse, field for field
    assert eb.gptp_engine_pins() == wire, (
        f"endstation_builder.gptp_engine_pins() {eb.gptp_engine_pins()} != "
        f"this gate's own parse {wire} - one of the two readers of "
        f"gen_gptp_ucode.py has rotted")
    #! The consumed set is priority1 alone (--p1; MAC and clock frequency
    #! ride --mac/--clk-hz from platform/constraints).  If the engine grows
    #! an argument for a pinned field, the field must MOVE to the consumed
    #! path, not stay refused.
    assert eb.GPTP_ENGINE_CONSUMED == ("priority1",)
    assert re.search(r'add_argument\("--p1"', gen), \
        "the engine generator no longer consumes --p1"

    # 2. every config's AVB_INTERFACE bytes 86..96 are BYTE-EXACT the wire
    #    dataset (priority1, clockQuality, priority2, domain, intervals)
    for name in sorted(CONFIGS):
        cfg = eb.load_config(CONFIGS[name])
        overlay = eb.emit_aem_overlay(cfg)
        blob = eb._entity_model_image(cfg, overlay)["aem_desc.bin"]
        avbi = image_descriptor(blob, 0x0009)
        want = (bytes([cfg["gptp"]["priority1"], wire["clock_class"]])
                + wire["offset_scaled_log_variance"].to_bytes(2, "big")
                + bytes([wire["clock_accuracy"], wire["priority2"], 0,
                         wire["log_sync_interval"] & 0xFF,
                         wire["log_announce_interval"] & 0xFF,
                         wire["log_pdelay_interval"] & 0xFF]))
        assert avbi[86:96] == want, (
            f"{name}: AVB_INTERFACE clock dataset {avbi[86:96].hex()} != "
            f"the engine's Announce dataset {want.hex()} (1722.1-2021 "
            f"7.2.8 bytes 86..96) - the descriptor claims a clock the "
            f"wire does not carry ([R-parallel] on #228)")

    # 3. a config OMITTING every pinned key is filled from the engine
    thin = _variant(CONFIGS["ax7101_1x1_tdm8"],
                    lambda c: [c["gptp"].pop(k, None) for k in wire])
    cfg = eb.load_config(thin)
    os.unlink(thin)
    for k, v in wire.items():
        assert cfg["gptp"][k] == v, \
            f"omitted gptp.{k} resolved to {cfg['gptp'][k]}, engine says {v}"

    # 4. the parser derives (it does not mirror): a fixture with OTHER
    #    values comes back with those values, a commented-out duplicate
    #    does not count, and a missing or twice-declared constant REFUSES
    fixture = ("P1_C, P2_C = 248, 247\n"
               "CQ_C = 0xF7FD436B\n"
               "# CQ_C = 0x11111111 commented copies are stripped\n"
               "    e_hdr(p, 0x0, 0x0208, RA, 0xFC, 44)\n"
               "    e_hdr(p, 0x2, 0x0000, RA, 0x00, 54)\n"
               "    e_hdr(p, 0xB, 0x0008, RA, 0x01, 76)\n")
    got = eb.gptp_engine_pins(fixture)
    assert got == dict(priority2=247, clock_class=0xF7, clock_accuracy=0xFD,
                       offset_scaled_log_variance=0x436B,
                       log_sync_interval=-4, log_announce_interval=1,
                       log_pdelay_interval=0), got
    for label, broken in (
            ("missing CQ_C", fixture.replace("CQ_C = 0xF7FD436B\n", "")),
            ("duplicate CQ_C", fixture + "CQ_C = 0x12345678\n"),
            ("missing Announce TX",
             fixture.replace("    e_hdr(p, 0xB, 0x0008, RA, 0x01, 76)\n",
                             "")),
            ("duplicate Announce TX",
             fixture + "    e_hdr(p, 0xB, 0x0008, RA, 0x02, 76)\n")):
        try:
            eb.gptp_engine_pins(broken)
            raise AssertionError(f"{label}: the derivation invented a value "
                                 f"instead of refusing")
        except eb.ConfigError as e:
            assert "gen_gptp_ucode.py" in str(e), \
                f"{label}: refused without naming the authority: {e}"
    #! and the fixture path never poisons the real cache
    assert eb.gptp_engine_pins() == wire

    print(f"  [gate 26b] AVB_INTERFACE == wire Announce for all "
          f"{len(CONFIGS)} configs: priority2 {wire['priority2']}, "
          f"clockQuality 0x{cq:08X}, log intervals "
          f"{wire['log_sync_interval']}/{wire['log_announce_interval']}/"
          f"{wire['log_pdelay_interval']}; omitted keys fill from the "
          f"engine; the parser refuses a missing or twice-declared "
          f"constant ([R-parallel] on #228)")


def test_pp_window_contract():
    """Gate 27: config and gateware share one processor-memory window."""
    import json
    for name, path in CONFIGS.items():
        result = eb.build(path, OUT)
        shape = json.load(open(result["paths"]["platform_shape"]))
        published = shape["pp_mem"]
        cfg = result["cfg"]["platform"]
        assert int(published["phys"], 16) == cfg["pp_mem_phys"], name
        assert int(published["bytes"], 16) == cfg["pp_mem_bytes"], name

    soc = open(MILAN_SOC_PY).read()
    assert re.search(r"^\s*_shape\s*=\s*_platform_shape\(", soc, re.M)
    assert '_shape["pp_mem"]["phys"]' in soc
    assert '_shape["pp_mem"]["bytes"]' in soc
    print(f"  [gate 27] {len(CONFIGS)} processor-memory windows are single-sourced")


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
    against the artifact that owns it: the builder's derived identifiers,
    the gateware's adp_shape_defaults.svh for the counts and capability words,
    pp_adp_pkg.sv for entity_capabilities, and the config for the MAC. It fails
    both ways round: an unbaked image and a baked image that disagrees with ADP.
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
        want_eid = eb.derive_entity_id(cfg)
        want_mid = int(cfg["entity"]["entity_model_id"], 16)
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
    if "--write-cluster-golden" in sys.argv:
        write_cluster_names_golden()
        sys.exit(0)
    for fn in (test_all_configs_build, test_baremetal_profile_contract,
               test_gptp_product_default_and_legacy_option,
               test_qspi_owner_transition_completed_write_prefixes,
               test_gptp_plane_reaches_the_instance,
               test_gptp_plane_instance_gate_bites,
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
               test_platform_gateware_shape,
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
               test_prune_guard_hop_gate_bites,
               test_d10_cluster_names, test_d10_cluster_namer_paths,
               test_d10_names_reach_the_rom,
               test_gptp_domain_is_one_source,
               test_gptp_dataset_matches_engine_announce,
               test_pp_window_contract,
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
