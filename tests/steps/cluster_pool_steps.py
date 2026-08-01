# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
Conformance steps for the D8 role-pool / D10 role-named cluster model.

WHAT THESE COVER THAT A MODULE TB CANNOT. The unit TBs prove the RTL answers
the frames it is given. These scenarios walk the model a CONTROLLER
enumerates - STREAM_PORT geometry, every AUDIO_CLUSTER in the block, every
AUDIO_MAP row - straight out of the artifact the build actually ships
(`sw/builder/endstation_builder.py` -> `aem_overlay.json` ->
`avdecc/gen_aem_store.py` -> `aecp_aem_rom.svh`). A config that emits a
model no controller can enumerate fails HERE, before a bitstream exists.

Clause basis, cited per step:
  * IEEE 1722.1-2021 7.2.13 (Table 7-23) - STREAM_PORT_INPUT/OUTPUT carry
    number_of_clusters/base_cluster and number_of_maps/base_map; an entity
    that does dynamic mapping "set[s] the number_of_maps field to zero (0)".
  * IEEE 1722.1-2021 7.2.16 / 7.2.16.1 - AUDIO_CLUSTER, mono MBLA.
  * IEEE 1722.1-2021 7.2.19 - an AUDIO_MAP maps stream channels to channels
    of the AUDIO_CLUSTERs "contained in the same" port, and
    mapping_cluster_offset is "the offset from the base_cluster of the
    STREAM_PORT_INPUT or STREAM_PORT_OUTPUT" - i.e. PORT-RELATIVE. Its
    uniqueness rules: input - at most one entry per cluster channel; output -
    at most one entry per stream channel across the Configuration.
  * IEEE 1722.1-2021 6.2.2.8 - object_name is NOT part of "the structure of
    an ATDECC Entity data model", so renaming clusters must not move
    entity_model_id.
  * Milan v1.2 5.4.2.27/28 - ADD/REMOVE_AUDIO_MAPPINGS are required only for
    stream ports that have NO Audio Map; a port WITH Audio Maps answers
    NOT_SUPPORTED. That NOT_SUPPORTED is CONFORMANCE, not a gap, and these
    scenarios assert it rather than flag it.
"""
import os
import sys

from behave import given, then, when

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "sw", "builder"))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))

import endstation_builder as eb        # noqa: E402
import gen_aem_store as gas            # noqa: E402

STATUS_SUCCESS = 0
STATUS_NO_SUCH_DESCRIPTOR = 2
STATUS_NOT_SUPPORTED = 11

DESC_STREAM_PORT_INPUT = 0x000E
DESC_STREAM_PORT_OUTPUT = 0x000F
DESC_AUDIO_CLUSTER = 0x0014
DESC_AUDIO_MAP = 0x0017


class EnumerationModel:
    """A read-only controller's view of one built end-station config: the
    descriptors it can address, and the status each request returns."""

    def __init__(self, config_stem):
        path = os.path.join(ROOT, "configs", f"endstation_{config_stem}.yaml")
        self.cfg = eb.load_config(path)
        self.ovl = eb.emit_aem_overlay(self.cfg)
        self.ports = {
            DESC_STREAM_PORT_INPUT: self.ovl["stream_ports"]["input"],
            DESC_STREAM_PORT_OUTPUT: self.ovl["stream_ports"]["output"],
        }
        self.clusters = sorted(self.ovl["audio_clusters"],
                               key=lambda c: c["index"])
        self.maps = {m["index"]: m for m in self.ovl["audio_maps"]}

    # -- READ_DESCRIPTOR (1722.1 7.4.5) ---------------------------------
    def read_descriptor(self, dtype, index):
        if dtype in self.ports:
            ports = self.ports[dtype]
            if index >= len(ports):
                return STATUS_NO_SUCH_DESCRIPTOR, None
            return STATUS_SUCCESS, ports[index]
        if dtype == DESC_AUDIO_CLUSTER:
            if index >= len(self.clusters):
                return STATUS_NO_SUCH_DESCRIPTOR, None
            return STATUS_SUCCESS, self.clusters[index]
        if dtype == DESC_AUDIO_MAP:
            if index not in self.maps:
                return STATUS_NO_SUCH_DESCRIPTOR, None
            return STATUS_SUCCESS, self.maps[index]
        return STATUS_NO_SUCH_DESCRIPTOR, None

    # -- Milan 5.4.2.27/28 posture --------------------------------------
    def add_audio_mappings(self, dtype, index):
        st, port = self.read_descriptor(dtype, index)
        if st != STATUS_SUCCESS:
            return st
        # "For each Stream Port Input and for each Stream Port Output that
        # has no Audio Map, the PAAD-AE shall implement the
        # ADD_AUDIO_MAPPINGS command"; a port WITH maps answers
        # NOT_SUPPORTED (Milan 5.4.2.27/28, 1722.1 7.2.13).
        return STATUS_NOT_SUPPORTED if port["maps"] > 0 else STATUS_SUCCESS


@given('the end-station config "{stem}" is built')
def step_build_config(context, stem):
    context.model = EnumerationModel(stem)
    context.stem = stem


@then('the entity advertises {n:d} AUDIO_CLUSTER descriptors')
def step_cluster_count(context, n):
    got = context.model.ovl["descriptor_counts"]["AUDIO_CLUSTER"]
    assert got == n, f"AUDIO_CLUSTER count {got} != {n}"


@then('the cluster policy is "{policy}"')
def step_policy(context, policy):
    got = context.model.ovl["cluster_policy"]
    assert got == policy, f"cluster policy {got!r} != {policy!r}"


@then('the board routes {cap:d} capture and {rend:d} render physical channels')
def step_physical(context, cap, rend):
    ph = context.model.ovl["physical_binding"]["physical_channels"]
    assert ph == {"capture": cap, "render": rend}, ph


@then('no AUDIO_CLUSTER carries the "{role}" role')
def step_no_role(context, role):
    bad = [c for c in context.model.clusters if c["role"] == role]
    assert not bad, (f"{len(bad)} cluster(s) still claim role {role!r} on a "
                     f"board that routes none: {bad[:3]}")


@then('every AUDIO_CLUSTER in every STREAM_PORT block answers READ_DESCRIPTOR')
def step_clusters_addressable(context):
    """1722.1 7.2.13: the port declares number_of_clusters/base_cluster; an
    entity that advertises clusters it cannot serve contradicts itself
    between two commands."""
    m = context.model
    seen = set()
    for dtype, ports in m.ports.items():
        for p in ports:
            for off in range(p["clusters"]):
                idx = p["base_cluster"] + off
                st, _ = m.read_descriptor(DESC_AUDIO_CLUSTER, idx)
                assert st == STATUS_SUCCESS, (
                    f"port type 0x{dtype:04X}[{p['index']}] advertises "
                    f"cluster {idx} but READ_DESCRIPTOR answers status {st}")
                assert idx not in seen, (
                    f"cluster {idx} claimed by two ports (blocks must not "
                    f"overlap - 7.2.13)")
                seen.add(idx)
    assert len(seen) == m.ovl["descriptor_counts"]["AUDIO_CLUSTER"], (
        f"{len(seen)} clusters reachable through ports but "
        f"{m.ovl['descriptor_counts']['AUDIO_CLUSTER']} advertised")


@then('the AUDIO_CLUSTER one past the last block answers NO_SUCH_DESCRIPTOR')
def step_cluster_boundary(context):
    m = context.model
    n = m.ovl["descriptor_counts"]["AUDIO_CLUSTER"]
    st, _ = m.read_descriptor(DESC_AUDIO_CLUSTER, n)
    assert st == STATUS_NO_SUCH_DESCRIPTOR, f"status {st} for cluster {n}"


@then('every AUDIO_MAP a STREAM_PORT declares answers READ_DESCRIPTOR')
def step_maps_addressable(context):
    """1722.1 7.2.13: number_of_maps/base_map. A port that names a map it
    cannot serve is the same self-contradiction as the cluster case."""
    m = context.model
    for dtype, ports in m.ports.items():
        for p in ports:
            for k in range(p["maps"]):
                st, _ = m.read_descriptor(DESC_AUDIO_MAP, p["base_map"] + k)
                assert st == STATUS_SUCCESS, (
                    f"port 0x{dtype:04X}[{p['index']}] declares map "
                    f"{p['base_map'] + k}, status {st}")


@then('every AUDIO_MAP row is port-relative and inside its own cluster block')
def step_rows_port_relative(context):
    """1722.1 7.2.19: mapping_cluster_offset is 'the offset from the
    base_cluster of the STREAM_PORT_INPUT or STREAM_PORT_OUTPUT'. A model
    that wrote GLOBAL cluster indices would pass every count check and be
    wrong on the wire - this is the check that catches it."""
    m = context.model
    for dtype, ports in m.ports.items():
        for p in ports:
            if not p["maps"]:
                continue
            amap = m.maps[p["base_map"]]
            for (si, sc, off, cc) in amap["mappings"]:
                assert 0 <= off < p["clusters"], (
                    f"map {amap['index']} row offset {off} outside its port's "
                    f"{p['clusters']}-cluster block (7.2.19 offsets are "
                    f"port-relative, not global)")
                assert si == p["stream_index"], (
                    f"map {amap['index']} references stream {si}, port owns "
                    f"{p['stream_index']}")
                assert cc == 0, "mono MBLA clusters have channel 0 only (7.2.16.1)"


@then('no AUDIO_MAP violates the 7.2.19 uniqueness rules')
def step_uniqueness(context):
    """Input: at most one entry per cluster channel. Output: at most one
    entry per stream channel across the entire Configuration."""
    m = context.model
    out_keys = set()
    for dtype, ports in m.ports.items():
        for p in ports:
            if not p["maps"]:
                continue
            amap = m.maps[p["base_map"]]
            in_keys = set()
            for (si, sc, off, cc) in amap["mappings"]:
                if dtype == DESC_STREAM_PORT_INPUT:
                    key = (off, cc)
                    assert key not in in_keys, (
                        f"map {amap['index']}: two entries for cluster "
                        f"channel {key} (7.2.19 input uniqueness)")
                    in_keys.add(key)
                else:
                    key = (si, sc)
                    assert key not in out_keys, (
                        f"map {amap['index']}: stream channel {key} mapped "
                        f"twice in the Configuration (7.2.19 output "
                        f"uniqueness)")
                    out_keys.add(key)


@then('every talker AUDIO_MAP row lands in the "{role}" pool')
def step_map_lands_in_pool(context, role):
    m = context.model
    for p in m.ports[DESC_STREAM_PORT_OUTPUT]:
        seg = next((g for g in p["pool"] if g["role"] == role), None)
        assert seg, f"talker port {p['index']} has no {role} pool"
        if p["maps"] == 0:
            # USER 08-01: the ship talkers are map_mode dynamic - the
            # power-on identity moved from static AUDIO_MAP rows into the
            # dynamic engine's reset image, whose origin is the PRIMARY
            # pool segment (builder gate 24a checks the image bytes land
            # inside it; here the overlay-level fact is the origin itself)
            assert p["primary_role"] == role, (
                f"dynamic talker port {p['index']} identity origin "
                f"{p['primary_role']!r}, expected {role!r}")
            continue
        amap = m.maps[p["base_map"]]
        for (_, _, off, _) in amap["mappings"]:
            assert seg["offset"] <= off < seg["offset"] + seg["width"], (
                f"talker port {p['index']} map offset {off} is outside its "
                f"{role} segment {seg}")


@then('each talker port offers a distinct "{role}" source set')
def step_distinct_sources(context, role):
    m = context.model
    byport = {}
    for c in m.clusters:
        if c["role"] == role and c["direction"] == "output":
            byport.setdefault(c["port_index"], []).append(c["name"])
    assert byport, f"no {role} clusters emitted"
    sets = {tuple(v) for v in byport.values()}
    assert len(sets) == len(byport), (
        f"{len(byport)} talker ports share only {len(sets)} distinct {role} "
        "source sets - the talkers would all carry the same audio")


@then('no AUDIO_CLUSTER is named "{placeholder}"')
def step_no_placeholder_name(context, placeholder):
    bad = [c for c in context.model.clusters if c["name"] == placeholder]
    assert not bad, (f"{len(bad)} cluster(s) still named {placeholder!r} - "
                     "a controller operator cannot tell them apart")


@then('every AUDIO_CLUSTER object_name matches its role')
def step_names_match_roles(context):
    prefix = {"pilot": "Pilot Tone", "loopback": "Loopback S",
              "host": "Host ", "virtual": "Virtual "}
    for c in context.model.clusters:
        if c["role"] in prefix:
            assert c["name"].startswith(prefix[c["role"]]), c
        else:                                   # physical: "<IFACE> In/Out n"
            assert c["name"].split()[0] in eb.IFACE_LABEL.values(), c
        assert len(c["name"].encode()) <= 63, \
            f"object_name {c['name']!r} does not fit the 64-byte field (7.2.16)"


@when('a controller sends ADD_AUDIO_MAPPINGS to every STREAM_PORT')
def step_add_mappings_all(context):
    m = context.model
    context.add_status = {}
    for dtype, ports in m.ports.items():
        for p in ports:
            context.add_status[(dtype, p["index"])] = \
                m.add_audio_mappings(dtype, p["index"])


@then('every port with Audio Maps answers NOT_SUPPORTED')
def step_static_posture(context):
    """Milan v1.2 5.4.2.27/28. This is CONFORMANCE: the dynamic commands are
    required only where number_of_maps == 0."""
    m = context.model
    n = 0
    for (dtype, idx), st in context.add_status.items():
        port = m.ports[dtype][idx]
        if port["maps"] > 0:
            assert st == STATUS_NOT_SUPPORTED, (
                f"port 0x{dtype:04X}[{idx}] has {port['maps']} Audio Map(s) "
                f"and answered {st}, not NOT_SUPPORTED (Milan 5.4.2.28)")
            n += 1
        else:
            assert st != STATUS_NOT_SUPPORTED, (
                f"port 0x{dtype:04X}[{idx}] has NO Audio Map, so Milan "
                "5.4.2.27 REQUIRES ADD_AUDIO_MAPPINGS")
    assert n, "no port with Audio Maps in this shape - nothing was proven"


@then('every port serves the dynamic commands (no Audio Maps anywhere)')
def step_all_dynamic_posture(context):
    """Milan v1.2 5.4.2.27/28, the other posture (USER 08-01): a fully
    dynamic shape has NO port that may answer NOT_SUPPORTED - the dynamic
    commands are a SHALL on every one of its stream ports."""
    m = context.model
    assert context.add_status, "no ports were exercised"
    for (dtype, idx), st in context.add_status.items():
        port = m.ports[dtype][idx]
        assert port["maps"] == 0, (
            f"port 0x{dtype:04X}[{idx}] still has {port['maps']} Audio "
            "Map(s) in a shape declared fully dynamic")
        assert st != STATUS_NOT_SUPPORTED, (
            f"port 0x{dtype:04X}[{idx}] has NO Audio Map, so Milan "
            "5.4.2.27/28 REQUIRE the dynamic commands")


@then('the entity_model_id is {eid}')
def step_model_id(context, eid):
    got = context.model.cfg["model_id"]["value"]
    assert got.lower() == eid.lower(), f"entity_model_id {got} != {eid}"


@then('renaming an AUDIO_CLUSTER leaves the entity_model_id unchanged')
def step_rename_keeps_id(context):
    """1722.1 6.2.2.8 lists object_name among the fields that do NOT
    constitute the structure of the data model, so a name change must keep
    the id (and controllers re-read names via GET_NAME)."""
    m = context.model
    before = m.cfg["model_id"]["hash"]
    shape_before = eb.model_shape(m.cfg)
    # the names are not in the shape at all - that IS the mechanism
    flat = repr(shape_before)
    for c in m.clusters[:8]:
        assert c["name"] not in flat, (
            f"cluster name {c['name']!r} leaked into the model-id shape - "
            "6.2.2.8 excludes object_name from the model structure")
    assert eb.derive_model_id(shape_before) == int(before, 16)


@then('the AEM descriptor ROM generates from the overlay')
def step_rom_generates(context):
    """The overlay is only a contract if the ROM consumer can actually build
    it - a shape whose descriptor set cannot be generated is a shape that
    cannot be built."""
    M = gas.build_model(gas.spec_from_overlay(context.model.ovl))
    n = sum(1 for (t, _, _, _) in M["directory"] if t == DESC_AUDIO_CLUSTER)
    assert n == context.model.ovl["descriptor_counts"]["AUDIO_CLUSTER"]
    context.rom_bytes = M["ROM_SIZE"]


@then('the descriptor ROM fits the 16-bit AEM store address space')
def step_rom_fits(context):
    assert context.rom_bytes + 64 <= 0x10000, (
        f"ROM {context.rom_bytes} B + 64 B MVU scratch exceeds 65536 - the "
        "store svh addresses itself with 16-bit words throughout")
