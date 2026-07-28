# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Steps for audio_map_port_binding.feature.

These walk the REAL generated entity model (avdecc/gen_aem_store.py) and the
REAL controller-grade predicate (tb/tools/hive_compliance.py C10), not a second
implementation of either. A behave suite that re-derives the rule it is
checking is two tools written from one reading of the spec agreeing with each
other - the failure mode that let fifteen Hive findings through on 2026-07-27.
"""
import importlib.util
import os
import sys

from behave import given, then

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))
sys.path.insert(0, os.path.join(ROOT, "sw", "builder"))

import gen_aem_store as G                                        # noqa: E402

#: hive_compliance.py is a script, not an importable package member (it is
#: named for what it does on the wire); load it by path so the SAME predicate
#: the bench tool runs is the one asserted here.
_spec = importlib.util.spec_from_file_location(
    "hive_compliance", os.path.join(ROOT, "tb", "tools", "hive_compliance.py"))
HC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(HC)

STREAM_PORT_INPUT, STREAM_PORT_OUTPUT = 0x000E, 0x000F
AUDIO_MAP = 0x0017

TRACKED = ["endstation_arty_current", "endstation_arty_4x4",
           "endstation_ax7101_8x8"]


def _model_for(name):
    """Build the entity model for a tracked config through the SAME path the
    build uses: config YAML -> endstation_builder overlay -> gen_aem_store."""
    import endstation_builder as B
    cfg = os.path.join(ROOT, "configs", name + ".yaml")
    r = B.build(cfg, outdir=None)
    return G.build_model(G.spec_from_overlay(r["overlay"]))


def _ports(M):
    """-> [(label, port_index, descriptor_bytes)] for both directions."""
    out = []
    for t, i, base, ln in M["directory"]:
        if t in (STREAM_PORT_INPUT, STREAM_PORT_OUTPUT):
            nm = "STREAM_PORT_INPUT" if t == STREAM_PORT_INPUT \
                else "STREAM_PORT_OUTPUT"
            out.append((nm, i, M["rom"][base:base + ln]))
    return out


def _be16(b, o):
    return (b[o] << 8) | b[o + 1]


def _maps(M):
    """-> {index: (base, len, declared_n, rows)} for every AUDIO_MAP."""
    d = {}
    for t, i, base, ln in M["directory"]:
        if t != AUDIO_MAP:
            continue
        img = M["rom"][base:base + ln]
        n = _be16(img, 6)
        rows = [tuple(_be16(img, 8 + 8 * k + 2 * f) for f in range(4))
                for k in range(min(n, (ln - 8) // 8))]
        d[i] = (base, ln, n, rows)
    return d


# ------------------------------------------------------------------ given ---
@given("the generated AEM models for every tracked end-station config")
def step_models_all(context):
    context.models = {n: _model_for(n) for n in TRACKED}


@given('the generated AEM model for config "{name}"')
def step_model_one(context, name):
    context.models = {name: _model_for(name)}


@given("the deployed AEM model spec")
def step_deployed_spec(context):
    context.spec = G.builtin_spec()


MUTATIONS = {
    # a GLOBAL AUDIO_CLUSTER index written where 7.2.19 wants an offset from
    # the port's own base_cluster - the exact shape of the wire defect
    "global_cluster_idx": lambda s: s["audio_maps"].__setitem__(
        1, [[0, c, 8 + c, 0] for c in range(8)]),
    "missing_base_map": lambda s: s["ports_out"][0].update(base_map=7),
    "two_maps_one_port": lambda s: s["ports_out"][0].update(maps=2),
    "cluster_channel_oob": lambda s: s["audio_maps"][0].__setitem__(
        0, [0, 0, 0, 1]),
    "stream_index_oob": lambda s: s["audio_maps"][0].__setitem__(
        0, [9, 0, 0, 0]),
    "duplicate_cluster": lambda s: s["audio_maps"][0].__setitem__(
        1, [0, 0, 0, 0]),
    "map_onto_crf": lambda s: s["audio_maps"][0].__setitem__(0, [1, 0, 0, 0]),
    # 1722.1-2021 Table 7-32: "The maximum value of this field is 62 for this
    # version of AEM."
    "too_many_mappings": lambda s: s["audio_maps"].__setitem__(
        0, [[0, c % 8, c, 0] for c in range(63)]),
    # 7.2.19 STREAM_PORT_OUTPUT: "at most one entry for each
    # mapping_stream_index and mapping_stream_channel across the entire
    # Configuration"
    "output_dup_stream": lambda s: s["audio_maps"].__setitem__(
        1, [[0, 0, 0, 0], [0, 0, 1, 0]]),
    # ...but the SAME paragraph permits repeating a cluster offset, which is
    # exactly what the INPUT rule forbids. Applying the input rule to both
    # directions would refuse this conformant model.
    "output_dup_cluster": lambda s: s["audio_maps"].__setitem__(
        1, [[0, 0, 0, 0], [0, 1, 0, 0]]),
}

#: the served rows of the deployed 8x8 output port (its own map) and of the
#: input port the pre-fix RTL actually read instead
OWN2 = [(0, 0, 0, 0), (0, 1, 1, 0)]
OTHER8 = [(1, c, c, 0) for c in range(8)]
AM_HDR = 12

C10_CASES = {
    "own_map": (OWN2, 2, AM_HDR + 16, OWN2, 24, None),
    "own_map_reordered": (OWN2[::-1], 2, AM_HDR + 16, OWN2, 24, None),
    "other_ports_map": (OTHER8, 8, AM_HDR + 64, OWN2, 24, None),
    "declares_more_than_it_carries": (OWN2, 8, AM_HDR + 16, OWN2, 24, None),
    "descriptor_overdeclares": (OWN2, 2, AM_HDR + 16, OWN2, 24, 8),
    "no_descriptor_dynamic": (OWN2, 2, AM_HDR + 16, None, None, None),
}


@given('a served GET_AUDIO_MAP response described by "{case}"')
def step_c10_case(context, case):
    assert case in C10_CASES, f"unknown C10 case {case}"
    context.c10 = C10_CASES[case]


# ------------------------------------------------------------------- when ---
@given('the audio map is mutated by "{mutation}"')
def step_mutate_given(context, mutation):
    step_mutate(context, mutation)


def step_mutate(context, mutation):
    assert mutation in MUTATIONS, f"unknown mutation {mutation}"
    MUTATIONS[mutation](context.spec)
    context.mutation = mutation


try:
    from behave import when

    @when('the audio map is mutated by "{mutation}"')
    def step_mutate_when(context, mutation):
        step_mutate(context, mutation)
except ImportError:                                       # pragma: no cover
    pass


# ------------------------------------------------------------------- then ---
@then("every STREAM_PORT base_map names an AUDIO_MAP the model defines")
def step_base_map_exists(context):
    for name, M in context.models.items():
        maps = _maps(M)
        for nm, i, d in _ports(M):
            n_maps, base_map = _be16(d, 16), _be16(d, 18)
            if n_maps == 0:
                continue                 # 7.2.13 dynamic-mapping signal
            assert base_map in maps, \
                f"{name} {nm}[{i}] base_map={base_map} not in the model"


@then("every AUDIO_MAP holds exactly the mappings it declares")
def step_map_self_consistent(context):
    for name, M in context.models.items():
        for i, (base, ln, n, rows) in _maps(M).items():
            assert ln == 8 + 8 * n, \
                (f"{name} AUDIO_MAP[{i}] declares {n} mappings but is {ln} B "
                 f"(7.2.19: 8 B header + 8 B per mapping = {8 + 8 * n})")
            assert len(rows) == n, \
                f"{name} AUDIO_MAP[{i}] declares {n} rows, holds {len(rows)}"


@then("every mapping is inside its own port's number_of_clusters")
def step_port_relative_bounds(context):
    for name, M in context.models.items():
        maps = _maps(M)
        for nm, i, d in _ports(M):
            n_clusters, n_maps, base_map = _be16(d, 12), _be16(d, 16), \
                _be16(d, 18)
            if n_maps == 0:
                continue
            for (si, sc, co, cc) in maps[base_map][3]:
                assert co < n_clusters, \
                    (f"{name} {nm}[{i}] AUDIO_MAP[{base_map}] cluster_offset "
                     f"{co} >= its own number_of_clusters {n_clusters} "
                     "(7.2.19: the offset is PORT-RELATIVE)")


@then("the static serving table addresses each port's own base_map descriptor")
def step_smap_addresses(context):
    for name, M in context.models.items():
        maps, sm = _maps(M), M["SMAP"]
        for nm, i, d in _ports(M):
            n_maps, base_map = _be16(d, 16), _be16(d, 18)
            key = "OUT_ADDR" if nm.endswith("OUTPUT") else "IN_ADDR"
            got = sm[key][i]
            want = 0 if n_maps == 0 else maps[base_map][0]
            assert got == want, \
                (f"{name} {nm}[{i}] serving address {got}, its own "
                 f"AUDIO_MAP[{base_map}] is at {want}")


@then("the static serving table row count is that descriptor's own "
      "number_of_mappings")
def step_smap_rows(context):
    for name, M in context.models.items():
        maps, sm = _maps(M), M["SMAP"]
        for nm, i, d in _ports(M):
            n_maps, base_map = _be16(d, 16), _be16(d, 18)
            key = "OUT_ROWS" if nm.endswith("OUTPUT") else "IN_ROWS"
            want = 0 if n_maps == 0 else maps[base_map][2]
            assert sm[key][i] == want, \
                (f"{name} {nm}[{i}] serves {sm[key][i]} mappings, its own "
                 f"AUDIO_MAP[{base_map}] declares {want}")


@then("AUDIO_MAP index {idx:d} belongs to STREAM_PORT_INPUT {pi:d}, not to an "
      "output port")
def step_map1_is_input(context, idx, pi):
    M = list(context.models.values())[0]
    owners = [(nm, i) for nm, i, d in _ports(M)
              if _be16(d, 16) and _be16(d, 18) == idx]
    assert owners == [("STREAM_PORT_INPUT", pi)], \
        f"AUDIO_MAP[{idx}] is owned by {owners}"


@then("STREAM_PORT_OUTPUT {pi:d} is served from a different address than "
      "AUDIO_MAP index {idx:d}")
def step_out_not_map1(context, pi, idx):
    M = list(context.models.values())[0]
    maps, sm = _maps(M), M["SMAP"]
    assert sm["OUT_ADDR"][pi] != maps[idx][0], \
        (f"STREAM_PORT_OUTPUT[{pi}] is served from AUDIO_MAP[{idx}] "
         "- that is the defect, not the fix")


@then('building the model is refused naming "{clause}"')
def step_refused(context, clause):
    try:
        G.build_model(context.spec)
    except ValueError as e:
        assert clause in str(e), \
            f"refused, but the message does not cite {clause}: {e}"
        return
    raise AssertionError(
        f"mutation {context.mutation} built without complaint - the gate is "
        "not asserting anything (methodology R2)")


@then("building the model is accepted")
def step_accepted(context):
    try:
        G.build_model(context.spec)
    except ValueError as e:
        raise AssertionError(
            f"mutation {context.mutation} was REFUSED, but 1722.1-2021 7.2.19 "
            f"permits it on this direction: {e}")


@then("the open AUDIO_MAP deviations are exactly the recorded list")
def step_deviations_recorded(context):
    M = G.build_model(context.spec)
    got = G.assert_no_map_deviations(M)
    context.deviations = got
    assert got, "the recorded deviation list is empty - if it was fixed, " \
                "delete KNOWN_MAP_DEVIATIONS and this scenario"


@then("an empty allowlist makes that deviation FAIL")
def step_allowlist_load_bearing(context):
    M = G.build_model(context.spec)
    try:
        G.assert_no_map_deviations(M, allow=set())
    except ValueError:
        return
    raise AssertionError("the allowlist is not load-bearing")


@then("the C10 over-read rule reports {n:d} violation(s)")
def step_c10(context, n):
    got = HC.audio_map_overreads(*context.c10)
    assert len(got) == n, f"expected {n} violation(s), got {len(got)}: {got}"
