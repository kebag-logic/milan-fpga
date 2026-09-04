#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_aem_store.py - generate descriptor bytes and a legacy SVH rendering.

The end-station builder supplies the current model through an overlay. The
default compatibility model contains ENTITY, CONFIGURATION, AUDIO_UNIT,
STREAM_INPUT x2 (AAF + CRF), STREAM_OUTPUT, AVB_INTERFACE, CLOCK_SOURCE x3,
CLOCK_DOMAIN, CONTROL (IDENTIFY), LOCALE, STRINGS, STREAM_PORT_IN/OUT,
AUDIO_CLUSTER x16, AUDIO_MAP x2.

The historical JSON snapshot declares eight AUDIO_UNIT external ports but no
EXTERNAL_PORT descriptors. The compatibility model keeps both counts at zero
so the tree remains closed during controller enumeration.

Byte layouts mirror IEEE 1722.1-2021 clause 7.2 and are checked against the
controller-visible descriptor contract.

The ENTITY descriptor's firmware_version (7.2.1 Table 7-2, offset 116, 64
octets) is DERIVED from the gateware's own VERSION parameter, not declared -
see firmware_version_string() for why that is not a style preference.

Since the endstation-builder round (gaps item 4) the model can also be built
from a builder-emitted AEM overlay (sw/builder/endstation_builder.py):
  python3 avdecc/gen_aem_store.py --overlay <aem_overlay.json> [--out-dir D]

NO RTL ROM CONSUMES THIS MODEL DIRECTLY (2026-08-16). The repository-local
IEEE 1722.1 control plane that used to compile it into
hdl/ieee17221/aecp/** is deleted. The protocol processor is the control plane
now and serves READ_DESCRIPTOR from a main-memory image built from this model.
The model is therefore still controller-visible after the builder packs it and
software loads the resulting aem_desc.bin before entity enable:

  * the two file targets that made it RTL are gone with the plane.  The
    default run no longer writes hdl/ieee17221/aecp/gen/aecp_aem_rom.svh
    (the directory does not exist) and no longer writes
    tb/verilator/aecp/aem_golden.h (that whole suite is deleted).  A code
    path whose only destination is a deleted directory is worse than no
    path: it fails at runtime, or worse, resurrects the directory.
  * what the model IS used for: it is the single declarative entity
    definition the ADP shape counts (talker_stream_sources /
    listener_stream_sinks) and the ADP capability words are DERIVED from,
    and the builder's own self-consistency gates read it. Those counts reach
    the gateware through hdl/common/gen/adp_shape_defaults.svh, while the
    builder packs the descriptor bytes into the processor's DRAM image.

Outputs (all generated, do not edit):
  avdecc/aem_rom.json             - the model for the Python measurement
                                    controller. The default target.
  <out-dir>/aecp_aem_rom.svh      - only under --out-dir, only for a caller
  <out-dir>/aem_rom.json            that wants the text in a scratch
                                    directory (the builder gates do).  This
                                    is NOT installed into any RTL tree.

THE AUDIO_MAP BOUNDS GATE (2026-07-28, defect B).  build_model() now REFUSES a
model whose AUDIO_MAPs leave the bounds of the ports that own them, and emits
the per-port serving tables (AEM_SMAP_*) the RTL needs to answer GET_AUDIO_MAP
from the ADDRESSED PORT's own base_map instead of a hardcoded descriptor index.
The two are one change: the tables cannot be built without checking that each
port's base_map names a descriptor that exists and holds what it claims, and
without the tables the RTL had nothing to select by but a constant.
See static_map_tables() for the clause behind each bound.

  python3 avdecc/gen_aem_store.py --self-test   # prove the gate bites


WHERE THE CODE LIVES (2026-09-03).  This module passed 2 400 lines and Rule 12
(docs/development/CODE_QUALITY.md) refuses a module over a thousand, so it is
now the FACADE over five siblings in this directory, split along what each one
produces:

  avdecc/aem_descriptors.py  clause 7.2 field layouts - one descriptor's
                             octets - plus the gateware version the ENTITY
                             descriptor's firmware_version field carries.
  avdecc/aem_maps.py         the AUDIO_MAP bounds refusal and the per-port
                             AEM_SMAP_* serving tables it produces.
  avdecc/aem_specs.py        the two declarative shapes a model is built
                             from: builtin_spec() and spec_from_overlay().
  avdecc/aem_assemble.py     build_model() - where every descriptor sits, the
                             ROM image, the overlay/write-back spans and the
                             dynamic tables.  Importing it builds the builtin
                             model, exactly as importing this file always did.
  avdecc/aem_emit.py         the renderings: emit_svh_text(), emit_svh(),
                             emit_json().  Nothing here decides a byte.

Every name those modules define is re-exported below, so
`gen_aem_store.build_model`, `.directory`, `.FORMATS`, `.emit_svh_text` and
the rest still resolve for the four importers that use them
(sw/builder/endstation_builder.py, sw/builder/test_builder.py,
scripts/check_entity_shape.py, avdecc/gen_aemi_image.py).  What stayed here is
the self-test and the CLI: the two things that are ABOUT the generator rather
than part of it.
"""
import argparse
import json
from pathlib import Path
from typing import Any

from aem_assemble import (CHMAP_PHYS_DEPTH, NAMED, OVERLAYS, ROM_SIZE,
                          SRC_IDS, WB, _M, base_of, build_model, check_named,
                          check_two_level, directory, named_structure, rom,
                          two_level_directory)
from aem_descriptors import (AUDIO_CLUSTER, AUDIO_MAP, AUDIO_UNIT,
                             AVB_INTERFACE, CLOCK_DOMAIN, CLOCK_SOURCE,
                             CONFIGURATION, CONTROL, CRF_FORMATS,
                             CTRL_LINEAR_UINT8, CTRL_TYPE_IDENTIFY, ENTITY,
                             FORMATS, HERE, LOCALE, MILAN_CSR_SV, NO_STRING,
                             OUT_FORMATS, RATES, ROOT, STREAM_INPUT,
                             STREAM_OUTPUT, STREAM_PORT_INPUT,
                             STREAM_PORT_OUTPUT, STRINGS, PortMapBounds, be16,
                             be32, be64, clock_source_shape, cstr,
                             d_audio_cluster, d_audio_map, d_audio_unit,
                             d_avb_interface, d_clock_domain, d_clock_source,
                             d_configuration, d_control_identify, d_entity,
                             d_locale, d_stream, d_stream_port, d_strings,
                             firmware_version_string, rtl_version)
from aem_emit import emit_json, emit_svh, emit_svh_text
from aem_maps import (KNOWN_MAP_DEVIATIONS, MILAN_BASE_CHANNELS,
                      SMAP_CLUSTER_CHANNELS, SMAP_MAX_PORTS, SMAP_MAX_ROWS,
                      MapDirection, assert_no_map_deviations,
                      base_channel_cover, fmt_channels, static_map_tables)
from aem_specs import _out_cluster_sources, builtin_spec, spec_from_overlay

#: Re-exported so `from gen_aem_store import *` and a reader both see that
#: this module's surface is its siblings' surface plus the self-test and the
#: CLI.  Nothing here is defined twice: a name is owned by exactly one file.
__all__ = [
    "AUDIO_CLUSTER", "AUDIO_MAP", "AUDIO_UNIT", "AVB_INTERFACE",
    "CHMAP_PHYS_DEPTH", "CLOCK_DOMAIN", "CLOCK_SOURCE", "CONFIGURATION",
    "CONTROL", "CRF_FORMATS", "CTRL_LINEAR_UINT8", "CTRL_TYPE_IDENTIFY",
    "ENTITY", "FORMATS", "HERE", "KNOWN_MAP_DEVIATIONS", "LOCALE",
    "MILAN_BASE_CHANNELS", "MILAN_CSR_SV", "NAMED", "NO_STRING",
    "OUT_FORMATS", "OVERLAYS", "PortMapBounds", "RATES", "ROM_SIZE", "ROOT",
    "SMAP_CLUSTER_CHANNELS", "SMAP_MAX_PORTS", "SMAP_MAX_ROWS", "SRC_IDS",
    "STREAM_INPUT", "STREAM_OUTPUT", "STREAM_PORT_INPUT",
    "STREAM_PORT_OUTPUT", "STRINGS", "MapDirection", "WB",
    "assert_no_map_deviations", "base_channel_cover", "base_of", "be16",
    "be32", "be64", "build_model", "builtin_spec", "check_named",
    "check_two_level", "clock_source_shape", "cstr", "d_audio_cluster",
    "d_audio_map", "d_audio_unit", "d_avb_interface", "d_clock_domain",
    "d_clock_source", "d_configuration", "d_control_identify", "d_entity",
    "d_locale", "d_stream", "d_stream_port", "d_strings", "directory",
    "emit_json", "emit_svh", "emit_svh_text", "firmware_version_string",
    "fmt_channels", "named_structure", "rom", "rtl_version", "self_test",
    "spec_from_overlay", "static_map_tables", "two_level_directory",
]

def _selftest_map_bounds():
    """The AUDIO_MAP bounds gate: every vector is a model that must be refused.

    Methodology R2 - a check that cannot fail is not a check - so the arm
    ends by proving the recorded-deviation allowlist is load-bearing too.
    """
    ok = [True]

    def refuses(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        """Assert `mutate`'s model is REFUSED by build_model()."""
        spec = builtin_spec()
        mutate(spec)
        try:
            build_model(spec)
        except ValueError as e:
            print(f"  [ok  ] {name}\n         -> {str(e)[:150]}")
            return
        ok[0] = False
        print(f"  [FAIL] {name}: built without complaint")

    def accepts(name: str,
                mutate: Callable[[dict[str, Any]], None] = lambda s: None) -> None:
        """Assert `mutate`'s model still BUILDS - the gate's negative control."""
        spec = builtin_spec()
        mutate(spec)
        try:
            build_model(spec)
            print(f"  [ok  ] {name}")
        except ValueError as e:
            ok[0] = False
            print(f"  [FAIL] {name}: refused - {e}")

    print("=== gen_aem_store AUDIO_MAP bounds gate self-test ===")
    # POSITIVE control first: the gate must not refuse what ships.
    accepts("the deployed model still builds")

    def global_index(s: dict[str, Any]) -> None:
        """Rewrite the output map with GLOBAL cluster indices - defect A."""
        #! THE defect A shape at the model tier: a global AUDIO_CLUSTER index
        #! written where 7.2.19 wants an offset from the port's base_cluster.
        #! The output port's clusters are 8..15 globally and 0..7 relative.
        s["audio_maps"][1] = [[0, c, 8 + c, 0] for c in range(8)]
    refuses("global cluster index where 7.2.19 wants a port-relative offset",
            global_index)
    refuses("base_map naming an AUDIO_MAP the model does not define",
            lambda s: s["ports_out"][0].update(base_map=7))
    refuses("number_of_maps != 1 on a static port (pages it cannot answer)",
            lambda s: s["ports_out"][0].update(maps=2))
    refuses("cluster_channel past the cluster's channel_count (7.2.16)",
            lambda s: s["audio_maps"][0].__setitem__(0, [0, 0, 0, 1]))
    refuses("stream_index past the descriptors this direction has (7.2.13)",
            lambda s: s["audio_maps"][0].__setitem__(0, [9, 0, 0, 0]))
    refuses("INPUT: two mappings onto the SAME cluster channel (7.2.19)",
            lambda s: s["audio_maps"][0].__setitem__(1, [0, 0, 0, 0]))
    refuses("a mapping onto the CRF sink, which carries no audio channels",
            lambda s: s["audio_maps"][0].__setitem__(0, [1, 0, 0, 0]))
    #! 7.2.19's two directions are DIFFERENT rules, and this pair is the
    #! negative control for that: the first version of this gate applied the
    #! INPUT rule to both and would have refused the second model, which the
    #! OUTPUT paragraph explicitly permits.
    refuses("OUTPUT: the same (stream_index, stream_channel) twice (7.2.19 "
            "\"across the entire Configuration\")",
            lambda s: s["audio_maps"].__setitem__(
                1, [[0, 0, 0, 0], [0, 0, 1, 0]]))
    accepts("OUTPUT: the same cluster_offset twice IS allowed (7.2.19 "
            "\"there may be multiple entries for each mapping_cluster_"
            "offset\")",
            lambda s: s["audio_maps"].__setitem__(
                1, [[0, 0, 0, 0], [0, 1, 0, 0]]))
    refuses("more mappings in one AUDIO_MAP than Table 7-32 allows (62)",
            lambda s: s["audio_maps"].__setitem__(
                0, [[0, c % 8, c, 0] for c in range(63)]))

    # ...and the recorded deviation is exactly the recorded one, no more.
    M = build_model(builtin_spec())
    got = M["SMAP"]["DEVIATIONS"]
    try:
        assert_no_map_deviations(M)
        print(f"  [ok  ] the {len(got)} open stream_channel deviation(s) are "
              "exactly the recorded ones")
    except ValueError as e:
        ok[0] = False
        print(f"  [FAIL] a NEW deviation appeared: {e}")
    # ...and that allowlist is not vacuous either: drop it and it must fail.
    try:
        assert_no_map_deviations(M, allow=set())
        ok[0] = False
        print("  [FAIL] the deviation allowlist is not asserting anything")
    except ValueError:
        print("  [ok  ] with an empty allowlist the deviation FAILS "
              "(the list is load-bearing)")
    return ok[0]


def _selftest_two_level():
    """The two-level directory gate: layouts the direct-indexed RTL would
    mis-serve, each of which must be refused, plus the NAMED 1:1 split."""
    ok = [True]

    # Two-level directory gate: every vector is a layout the direct-indexed
    # accessor would silently mis-serve, so each MUST be a refusal (a check
    # that cannot fail is not a check).
    print("\n=== two-level directory gate self-test ===")

    def dir_refuses(name: str,
                    tamper: Callable[[list[tuple[int, int, int, int]]], None]) -> None:
        """Assert `tamper`'s directory layout is REFUSED before it reaches RTL."""
        d = list(build_model(builtin_spec())["directory"])
        tamper(d)
        try:
            l1t = two_level_directory(d)
            check_two_level(l1t, d)
        except ValueError as e:
            print(f"  [ok  ] {name}\n         -> {str(e)[:150]}")
            return
        ok[0] = False
        print(f"  [FAIL] {name}: accepted without complaint")

    def swap(d: list[tuple[int, int, int, int]], x: int, y: int) -> None:
        """Exchange two directory rows in place."""
        d[x], d[y] = d[y], d[x]
    # row 0 is ENTITY, rows 3/4 the STREAM_INPUT run: parking SI[0] at row 0
    # splits that run around the descriptors between them
    dir_refuses("a shuffled directory entry (contiguity)",
                lambda d: swap(d, 0, 3))
    # STREAM_INPUT[0]/[1] swapped: contiguous but not ascending
    dir_refuses("same-type entries out of index order",
                lambda d: swap(d, 3, 4))
    # ...and the equivalence check itself bites on a corrupt level-1 row
    # base even when the directory is pristine (the "shuffle one entry"
    # bite at the TABLE tier)
    Mtl = build_model(builtin_spec())
    l1b = dict(Mtl["L1"], ROW=list(Mtl["L1"]["ROW"]))
    l1b["ROW"][STREAM_INPUT] += 1
    try:
        check_two_level(l1b, Mtl["directory"])
        ok[0] = False
        print("  [FAIL] an off-by-one level-1 row base was accepted")
    except ValueError as e:
        print(f"  [ok  ] an off-by-one level-1 row base is refused\n"
              f"         -> {str(e)[:150]}")
    # name split: a mask bit on an unnamed type claims names that do not
    # exist - the 1:1 gate must catch it
    try:
        check_named(Mtl["L1"], Mtl["directory"], Mtl["NAMED"],
                    Mtl["NAME_MASK"] | (1 << STRINGS), Mtl["NAME_EXC"])
        ok[0] = False
        print("  [FAIL] a mask bit on the unnamed STRINGS type was accepted")
    except ValueError as e:
        print(f"  [ok  ] a mask bit on an unnamed type is refused\n"
              f"         -> {str(e)[:150]}")
    return ok[0]


def _selftest_base_formats():
    """Milan v1.2 6.4 over the BUILTIN model's own FORMATS constant."""
    ok = [True]

    # Milan v1.2 6.4 over the BUILTIN model's own FORMATS constant, which no
    # config and no overlay reaches: the config-driven path has its family
    # derived (endstation_builder.base_format_complete) and gated by
    # test_builder gate 29, so the constants in this file are the one
    # advertised formats list in the tree with no owner but this check.
    print("\n=== Milan 6.4 Base format family (builtin model) ===")
    for label, fmts in (("FORMATS (STREAM_INPUT)", FORMATS),):
        missing = sorted(set(MILAN_BASE_CHANNELS) - base_channel_cover(fmts))
        if missing:
            ok[0] = False
            print(f"  [FAIL] {label}: 48 kHz Base channel count(s) {missing} "
                  f"unadvertised - Milan 6.4 wants the whole family")
        else:
            print(f"  [ok  ] {label}: all {len(MILAN_BASE_CHANNELS)} 48 kHz "
                  f"Base channel counts {list(MILAN_BASE_CHANNELS)} covered "
                  f"by {len(fmts)} entries (6.5's ut string does the family)")
    # negative control: the ut entry is what carries the family, so dropping
    # it must be REPORTED and not shrugged at
    short = sorted(set(MILAN_BASE_CHANNELS) - base_channel_cover(FORMATS[:1]))
    if short:
        print(f"  [ok  ] without the ut entry the family check REPORTS "
              f"{short} missing")
    else:
        ok[0] = False
        print("  [FAIL] the family check passes without the ut entry - it has "
              "stopped being able to say no")
    return ok[0]


def self_test() -> int:
    """Negative control for the AUDIO_MAP bounds gate (methodology R2: a check
    that cannot fail is not a check). Every vector below is a model that used
    to build silently, and the deployed model passing is not evidence that the
    gate bites - only a refused model is."""
    ok = _selftest_map_bounds()
    ok = _selftest_two_level() and ok
    ok = _selftest_base_formats() and ok
    print("\ngen_aem_store self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="generate the HW AEM descriptor store")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the AUDIO_MAP bounds gate refuses "
                         "out-of-bounds models, and exit (no files written)")
    ap.add_argument("--overlay", default=None,
                    help="build the model from a builder-emitted "
                         "aem_overlay.json instead of the builtin shape")
    ap.add_argument("--out-dir", default=None,
                    help="write aecp_aem_rom.svh + aem_rom.json into this "
                         "SCRATCH directory instead of avdecc/aem_rom.json. "
                         "Nothing is installed into an RTL tree: the AEM plane "
                         "this ROM described is deleted (see the module "
                         "docstring), so the .svh is a readable rendering of "
                         "the declarative model, not a build input")
    args = ap.parse_args()
    if args.self_test:
        raise SystemExit(self_test())
    if args.overlay:
        M = build_model(spec_from_overlay(
            json.loads(Path(args.overlay).read_text())))
    else:
        M = _M
    # The tracked-RTL destinations (hdl/ieee17221/aecp/gen/aecp_aem_rom.svh and
    # tb/verilator/aecp/aem_golden.h) are DELETED along with the plane that
    # compiled them.  Only --out-dir renders the .svh now, and only into a
    # directory the caller names.
    if args.out_dir:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        p_json = out_dir / "aem_rom.json"
        emit_svh(M, out_dir / "aecp_aem_rom.svh")
    else:
        p_json = HERE / "aem_rom.json"
    emit_json(M, p_json)
    print(f"[gen_aem_store] {len(M['directory'])} descriptors, "
          f"ROM {M['ROM_SIZE']} B"
          + (f" (overlay {args.overlay})" if args.overlay else "")
          + (f" -> {args.out_dir}" if args.out_dir
             else " -> avdecc/aem_rom.json (no RTL target: the AEM plane is "
                  "deleted)"))
    for t, i, b, l in M["directory"]:
        print(f"  type 0x{t:04X} idx {i}: base {b:4d} len {l}")
