# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The chmap64 render-crossbar binding contract, offline.

WHAT THIS IS, AND WHAT IT IS NOT.  This module carries the dynamic audio-map
model that used to live in tests/steps/tsn_gen_steps.py. The protocol processor
serves READ_DESCRIPTOR, GET_AUDIO_MAP, ADD_AUDIO_MAPPINGS, and
REMOVE_AUDIO_MAPPINGS. Their wire behavior and transactional live-RAM writes
are tested in the processor and milan_dp harnesses, not in this offline model.

What SURVIVES is the fabric half - the render crossbar KL_chan_map_render and
its capture twin KL_chan_map_capture - and the WORD FORMAT a mapping projects
to: {en[6], stream[5:3], ch[2:0]} at the GLOBAL cluster key (base_cluster +
port-relative offset), which is the map-RAM address.  Those scenarios keep
running against this model because the crossbar still ships and the key-space
law (Milan v1.2 5.3.3.9: dynamic mappings on ALL Stream Port Inputs, each with
its own base_cluster) is what addresses it.

The model is driven DIRECTLY here.  It is no longer fed from generated frames,
so nothing in this module needs the tsn_gen packet generator - and nothing
here skips when that binary is absent.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from behave import given, then, when

if TYPE_CHECKING:  # behave is a test-only dependency; the annotation is lazy
    from behave.runner import Context

#: One ADD/REMOVE record as 1722.1-2021 Table 7-33 orders it:
#: (stream_index, stream_channel, cluster_offset, cluster_channel).
Mapping = tuple[int, int, int, int]

#: IEEE 1722.1-2021 7.4.44/7.4.45/7.4.46 command codes, kept so the model's
#: ADD / REMOVE / GET arms stay separable and self-describing.
CMD_GET_AUDIO_MAP = 43
CMD_ADD_AUDIO_MAPPINGS = 44
CMD_REMOVE_AUDIO_MAPPINGS = 45

#: 1722.1-2021 Table 7-2 descriptor types
DESC_STREAM_PORT_INPUT = 0x0E
DESC_STREAM_PORT_OUTPUT = 0x0F

#: 1722.1-2021 Table 7-5 AEM status codes
STATUS_SUCCESS = 0
STATUS_NO_SUCH_DESCRIPTOR = 2
STATUS_BAD_ARGUMENTS = 7
STATUS_NOT_SUPPORTED = 11


class MapShape:
    """The AEM_DMAP_* generics one audio-map model is shaped by.

    Four facts that describe the FABRIC the model stands in for, and that only
    ever move together: which cluster block each STREAM_PORT_INPUT owns
    (`ports`, as (base_cluster, clusters) pairs - AEM_DMAP_PBASE_C /
    AEM_DMAP_PCLS_C), how many mappings a GET page carries (`page` -
    AEM_DMAP_PAGE_C), the current format of each STREAM_INPUT
    (`stream_channels`, with None marking an unmappable CRF input), and how
    deep the render crossbar physically reaches (`phys` - AEM_DMAP_PHYS_C,
    milan_datapath CHMAP_PHYS_C).

    `ports=None` asks for the single-port default shape, which the model then
    derives from its own `keys`/`nmaps` declaration.

    `rphys` is the generated ADP_DMAP_IN_RPHYS_C table, one 7-bit word
    {valid[6], render_key[5:0]} per GLOBAL cluster key. It decides which keys
    reach a PHYSICAL render channel and which do not - a separate question
    from whether a mapping is legal. `None` keeps the identity projection
    every scenario written before it assumed: key k reaches render channel k
    while k < `phys`.
    """

    def __init__(self, ports=None, page=4, stream_channels=8, phys=10,
                 rphys=None):
        self.ports = ports
        self.page = page
        self.stream_channels = stream_channels
        self.phys = phys
        self.rphys = rphys


class MilanAudioMapModel:
    """Dynamic audio-map store for EVERY map_mode-dynamic STREAM_PORT_INPUT,
    and the chmap64 render words it projects.

    Milan v1.2 5.3.3.9 is why this is plural: "The Stream Port Input of a
    Configuration shall not contain any AUDIO_MAP descriptor. Note: this
    means that a PAAD-AE implements dynamic mappings on all of its Stream
    Port Inputs."

    Milan 5.4.2.26 mono clusters: one store key IS one Audio-Cluster channel
    (at most one dynamic mapping each). A mapping record is (stream_index,
    stream_channel, cluster_offset, cluster_channel), and the offset is
    PORT-RELATIVE (1722.1-2021 Table 7-33 - "the offset from the base_cluster
    of the STREAM_PORT_INPUT") while the store key is the GLOBAL cluster
    index base_cluster + offset, which is also the render crossbar's map-RAM
    address.

      * ADD is all-or-nothing (5.4.2.27): any invalid record -> BAD_ARGUMENTS
        and NOTHING is written; one key naming two different stream channels
        in one command is the mandated conflict. Exact duplicates are safe.
      * REMOVE validates ALL first (7.4.46.1: "If any of the mappings in the
        command are invalid or not present then the command shall fail with a
        BAD_ARGUMENTS status and none of the mappings shall be removed").

    Each accepted record projects to a chmap64 render map word
    {en, stream[2:0], ch[2:0]} at the GLOBAL cluster key (physical-channel)
    address; each cleared record disables that word. That projection IS the
    executable chmap64 binding contract (docs/CHMAP64_AEM_BINDING.md).
    """

    def __init__(self, shape=None, keys=8, nmaps=2):
        """`shape` is the fabric (`MapShape`); `keys`/`nmaps` are the
        single-port DEFAULT, kept apart from it because they are not a shape
        the caller picks but the declaration this model asserts its own
        derivation against when no ports are given."""
        shape = MapShape() if shape is None else shape
        self.page = shape.page        # AEM_DMAP_PAGE_C: mappings per page
        #: (base_cluster, clusters) per STREAM_PORT_INPUT — AEM_DMAP_PBASE_C
        #: / AEM_DMAP_PCLS_C. Default = the single-port shape.
        self.ports = ([tuple(p) for p in shape.ports] if shape.ports
                      else [(0, keys)])
        self.keys = max(b + n for b, n in self.ports)   # AEM_DMAP_KEYS_C
        #: AEM_DMAP_PNMAPS_C: per-port fixed partition count (5.4.2.26)
        self.nmaps = [-(-n // self.page) for _, n in self.ports]
        assert shape.ports is not None or self.nmaps == [nmaps], \
            f'single-port shape: derived nmaps {self.nmaps} != {nmaps}'
        #: channels in the CURRENT format of each STREAM_INPUT; None marks an
        #: unmappable (CRF) input. A bare int is the legacy 1-stream shape.
        self.stream_channels = (list(shape.stream_channels)
                                if isinstance(shape.stream_channels,
                                              (list, tuple))
                                else [shape.stream_channels])
        #: render-crossbar DEPTH (AEM_DMAP_PHYS_C = milan_datapath
        #: CHMAP_PHYS_C): the size of the physical key space
        self.phys = shape.phys
        #: PROTOCOL VALIDITY AND PHYSICAL PROJECTION ARE SEPARATE. The
        #: generated ADP_DMAP_IN_RPHYS_C table says which global cluster keys
        #: are BACKED by a render channel and which key each reaches; a
        #: cluster with no projection is a legal, protocol-visible mapping
        #: that changes no physical destination. The identity default is the
        #: shape every scenario written before this table assumed.
        self.rphys = (list(shape.rphys) if shape.rphys is not None
                      else [0x40 | k for k in range(self.phys)])
        self.store = {}               # global key -> (stream_index, stream_ch)
        self.fabric_map = {}          # global key -> {en,stream,ch} word
        self.last_get = None          # rows returned by the last GET page

    # -- port lookup --------------------------------------------------------
    def _port(self, di):
        return self.ports[di] if 0 <= di < len(self.ports) else None

    # -- validity (5.4.2.27) ------------------------------------------------
    def _shape_ok(self, port, si, sc, co, cc):
        # mono cluster (cluster_channel 0), offset inside THIS port's own
        # cluster block, and a mappable (non-CRF) Stream Input.
        #
        # A MISSING PHYSICAL PROJECTION IS NOT A REFUSAL, and this model used
        # to say it was. The fabric accepts an ADD on a dynamic
        # STREAM_PORT_INPUT from the cluster bound, the stream bound and the
        # mono-cluster rule alone; it consults the projection table only when
        # deciding whether to write the render RAM. The generated headers say
        # the same in words - "non-physical clusters remain protocol-visible
        # mappings without aliasing a physical pin" - and a preserved tracked
        # shape (Arty 4x4) ships exactly that: port 0 offsets 2 and 3, and
        # ports 1 to 3 entirely, are legal clusters with no pin behind them.
        # A cluster offset past the addressed port's own block is a different
        # defect class and stays BAD_ARGUMENTS below.
        del sc                              # graded by _ch_ok
        base, n = port
        del base
        return (cc == 0 and co < n and 0 <= si < len(self.stream_channels)
                and self.stream_channels[si] is not None)

    def _ch_ok(self, si, sc):
        # stream_channel inside the current format of THAT Stream Input
        # (Milan 5.3.10.1); the render word carries ch[2:0]
        return sc < self.stream_channels[si] and sc < 8

    # -- fabric projection --------------------------------------------------
    def phys_key(self, key: int) -> int | None:
        """The render channel global cluster `key` reaches, or None when the
        cluster is legal but has no physical destination."""
        if not 0 <= key < len(self.rphys):
            return None
        word = self.rphys[key]
        return (word & 0x3F) if (word & 0x40) else None

    def _project_add(self, si, sc, key):
        pk = self.phys_key(key)
        if pk is None:
            return                       # legal, stored, reaches no pin
        self.fabric_map[pk] = {'en': 1, 'stream': si, 'ch': sc}

    def _project_remove(self, key):
        pk = self.phys_key(key)
        if pk is None:
            return
        self.fabric_map[pk] = {'en': 0, 'stream': 0, 'ch': 0}

    def word(self, key: int) -> int:
        """The 7-bit chmap64 map word {en[6], stream[5:3], ch[2:0]}."""
        m = self.fabric_map.get(key, {'en': 0, 'stream': 0, 'ch': 0})
        return ((m['en'] & 1) << 6) | ((m['stream'] & 0x7) << 3) | (m['ch'] & 0x7)

    def enabled_words(self) -> int:
        """How many map-RAM words currently drive a channel. A removal writes
        a disabled word rather than dropping the entry, so this counts the
        enable bits and not the size of the projection."""
        return sum(1 for m in self.fabric_map.values() if m['en'])

    # -- command processing -------------------------------------------------
    def process_mappings(self, cmd: int, dt: int, di: int,
                         mappings: Sequence[Mapping]) -> int:
        """The AEM status one ADD or REMOVE command earns, having applied all
        of its records or none of them.

        Both arms validate the whole command before writing anything, so a
        caller that reads only the status can still trust the store: a
        BAD_ARGUMENTS return means the model is exactly as it was.
        """
        if dt == DESC_STREAM_PORT_OUTPUT and di == 0:
            return STATUS_NOT_SUPPORTED          # static output maps
        port = self._port(di)
        if dt != DESC_STREAM_PORT_INPUT or port is None:
            return STATUS_NO_SUCH_DESCRIPTOR
        # IEEE 1722.1-2021 9.2.2.6 limits a command's control_data_length to
        # 524 octets. Figure 7-71 uses 20 + 8*N, so N is at most 63. Milan
        # v1.2 5.4.1 lifts this limit for responses, not commands.
        if len(mappings) > 63:
            return STATUS_BAD_ARGUMENTS
        if not mappings:
            return STATUS_SUCCESS                # empty edit, no change
        base, _ = port

        if cmd == CMD_ADD_AUDIO_MAPPINGS:
            claim = {}                           # key -> command-local row
            for si, sc, co, cc in mappings:      # validate pass
                key = base + co
                if (not self._shape_ok(port, si, sc, co, cc)
                        or not self._ch_ok(si, sc)
                        or (key in claim and claim[key] != (si, sc))):
                    return STATUS_BAD_ARGUMENTS  # all-or-nothing
                claim[key] = (si, sc)
            for si, sc, co, cc in mappings:      # commit pass (replace allowed)
                self.store[base + co] = (si, sc)
                self._project_add(si, sc, base + co)
            return STATUS_SUCCESS

        # REMOVE — validate ALL first, then commit. 7.4.46.1 verbatim: "If
        # any of the mappings in the command are invalid or not present then
        # the command shall fail with a BAD_ARGUMENTS status and none of the
        # mappings shall be removed." Milan 5.4.2.28 overrides that for
        # DUPLICATES only ("shall ignore duplicate mappings"), and duplicates
        # survive precisely because nothing is committed during validation.
        for si, sc, co, cc in mappings:
            if not (self._shape_ok(port, si, sc, co, cc) and sc < 16
                    and self.store.get(base + co) == (si, sc)):
                return STATUS_BAD_ARGUMENTS
        for si, sc, co, cc in mappings:
            if base + co in self.store:          # 2nd copy of a dup: no-op
                del self.store[base + co]
                self._project_remove(base + co)
        return STATUS_SUCCESS

    def process_get(self, dt: int, di: int, map_index: int) -> int:
        """The AEM status one GET_AUDIO_MAP page earns, leaving the page
        itself in `last_get`.

        Every refusal clears `last_get` first, so a scenario cannot read a
        stale page after a failed GET and call it a response.
        """
        if dt == DESC_STREAM_PORT_OUTPUT and di == 0:
            self.last_get = None
            return STATUS_NOT_SUPPORTED
        port = self._port(di)
        if dt != DESC_STREAM_PORT_INPUT or port is None:
            self.last_get = None
            return STATUS_NO_SUCH_DESCRIPTOR
        if map_index >= self.nmaps[di]:          # 7.4.44.1 paging
            self.last_get = None
            return STATUS_BAD_ARGUMENTS
        base, n = port
        lo = map_index * self.page
        hi = min(lo + self.page, n)              # last partition is short
        #: rows carry the PORT-RELATIVE offset, never the global key
        self.last_get = [(self.store[base + k][0], self.store[base + k][1],
                          k, 0)
                         for k in range(lo, hi) if base + k in self.store]
        return STATUS_SUCCESS


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------

@given('a fresh Milan audio-map model')
def step_fresh_audiomap(context: Context) -> None:
    """The single-port default shape: 8 clusters, page 4, one 8-channel
    Stream Input - the smallest fabric that can show a paging boundary."""
    context.amap = MilanAudioMapModel()


@given('a Milan audio-map model with {n:d} dynamic ports of {cl:d} clusters '
       'and page {page:d}')
def step_fresh_audiomap_ports(context: Context, n: int, cl: int,
                              page: int) -> None:
    """Milan 5.3.3.9: dynamic mappings on ALL Stream Port Inputs. Ports own
    contiguous cluster blocks, so port p's base_cluster is p*clusters, and
    the last Stream Input is the unmappable CRF sink."""
    context.amap = MilanAudioMapModel(MapShape(
        page=page, ports=[(p * cl, cl) for p in range(n)],
        stream_channels=[8] * n + [None]))


#: The generated ADP_DMAP_IN_RPHYS_C tables of two TRACKED shapes, named so a
#: scenario says WHICH fabric it stands in rather than spelling seven-bit
#: words. Words are {valid[6], render_key[5:0]}; 0x00 is a legal cluster with
#: no physical destination.
#:
#:   arty 4x4      the preserved shape that already separates the two
#:                 questions: four ports of four clusters, and only port 0
#:                 offsets 0 and 1 are backed - by the stereo DAC lane.
#:   shipping tdm8 the AX7101 1x1 shape: one port of eight clusters, every one
#:                 backed by the TDM lane at render keys 2..9. The lane BASE
#:                 (2) and the COUNT (8) are separate quantities.
PROJECTION_TABLES = {
    'arty 4x4': dict(
        ports=[(0, 4), (4, 4), (8, 4), (12, 4)], page=4,
        stream_channels=[8, 8, 8, 8, None],
        rphys=[0x40, 0x41] + [0x00] * 14),
    'shipping tdm8': dict(
        ports=[(0, 8)], page=8, stream_channels=[8, None],
        rphys=[0x42 + n for n in range(8)]),
}


@given('a Milan audio-map model on the {name} render projection')
def step_amap_projection(context: Context, name: str) -> None:
    """A model shaped by a TRACKED generated projection table, so a scenario
    can tell a cluster-bound refusal apart from a missing physical
    destination instead of conflating the two."""
    spec = PROJECTION_TABLES.get(name)
    assert spec is not None, (
        f'unknown render projection {name!r}; '
        f'known: {", ".join(sorted(PROJECTION_TABLES))}')
    context.amap = MilanAudioMapModel(MapShape(**spec))


@then('the render crossbar physical key {pk:d} is en {en:d} stream {s:d} '
      'ch {ch:d}')
def step_phys_key_word(context: Context, pk: int, en: int, s: int,
                       ch: int) -> None:
    """Grade a word at a PHYSICAL render key, which is the address the
    crossbar RAM actually has - not the global cluster key the protocol
    command names. On a projected shape the two differ by the lane base."""
    m = context.amap.fabric_map.get(pk, {'en': 0, 'stream': 0, 'ch': 0})
    assert (m['en'], m['stream'], m['ch']) == (en, s, ch), \
        (f'physical key {pk}: fabric word {m}, '
         f'expected en={en} stream={s} ch={ch}')


@then('the global cluster key {key:d} has no physical destination')
def step_key_unprojected(context: Context, key: int) -> None:
    """Assert a cluster is legal but reaches no pin - the state a refusal
    would hide and an aliasing projection would break."""
    assert context.amap.phys_key(key) is None, \
        (f'global cluster key {key} projects to render key '
         f'{context.amap.phys_key(key)}, expected none')


@then('the global cluster key {key:d} projects to physical key {pk:d}')
def step_key_projected(context: Context, key: int, pk: int) -> None:
    """Assert the derived projection itself, so the lane base is under test
    and not only the words a command happened to write."""
    assert context.amap.phys_key(key) == pk, \
        (f'global cluster key {key} projects to '
         f'{context.amap.phys_key(key)}, expected {pk}')


@when('I ADD mapping stream_channel {sc:d} at cluster_offset {co:d}')
def step_amap_add(context: Context, sc: int, co: int) -> None:
    """ADD one record on the default port, and keep only its status: the
    scenario grades the store and the fabric words separately."""
    context.amap_status = context.amap.process_mappings(
        CMD_ADD_AUDIO_MAPPINGS, DESC_STREAM_PORT_INPUT, 0, [(0, sc, co, 0)])


@when('I ADD {n:d} copies of stream_channel {sc:d} at cluster_offset {co:d}')
def step_amap_add_copies(context: Context, n: int, sc: int, co: int) -> None:
    """ADD the same record n times in ONE command - the exact-duplicate case
    5.4.2.27 allows, as distinct from two records claiming one key."""
    context.amap_status = context.amap.process_mappings(
        CMD_ADD_AUDIO_MAPPINGS, DESC_STREAM_PORT_INPUT, 0,
        [(0, sc, co, 0)] * n)


@when('I REMOVE mapping stream_channel {sc:d} at cluster_offset {co:d}')
def step_amap_remove(context: Context, sc: int, co: int) -> None:
    """REMOVE one record on the default port, keeping only its status."""
    context.amap_status = context.amap.process_mappings(
        CMD_REMOVE_AUDIO_MAPPINGS, DESC_STREAM_PORT_INPUT, 0, [(0, sc, co, 0)])


@when('on input port {di:d} I ADD stream {si:d} channel {sc:d} at '
      'cluster_offset {co:d}')
def step_amap_add_port(context: Context, di: int, si: int, sc: int,
                       co: int) -> None:
    """ADD across the multi-port shape, where cluster_offset is relative to
    THIS port's base_cluster - the distinction Milan 5.3.3.9 forces."""
    context.amap_status = context.amap.process_mappings(
        CMD_ADD_AUDIO_MAPPINGS, DESC_STREAM_PORT_INPUT, di, [(si, sc, co, 0)])


@when('on input port {di:d} I REMOVE stream {si:d} channel {sc:d} at '
      'cluster_offset {co:d}')
def step_amap_remove_port(context: Context, di: int, si: int, sc: int,
                          co: int) -> None:
    """REMOVE across the multi-port shape, at a port-relative offset."""
    context.amap_status = context.amap.process_mappings(
        CMD_REMOVE_AUDIO_MAPPINGS, DESC_STREAM_PORT_INPUT, di,
        [(si, sc, co, 0)])


@when('the audio-map model GETs input port {di:d} page {mi:d}')
def step_amap_get_port(context: Context, di: int, mi: int) -> None:
    """Fetch one GET_AUDIO_MAP page, leaving both its status and its rows
    on the model for the Then steps to read."""
    context.amap_status = context.amap.process_get(
        DESC_STREAM_PORT_INPUT, di, mi)


@then('the audio-map model responds status {code:d}')
def step_amap_status(context: Context, code: int) -> None:
    """Grade the last command's AEM status against Table 7-5."""
    assert context.amap_status == code, \
        f'audio-map status {context.amap_status}, expected {code}'


@then('the fabric map word at cluster_offset {co:d} is en {en:d} stream {s:d} ch {ch:d}')
def step_fabric_word_fields(context: Context, co: int, en: int, s: int,
                            ch: int) -> None:
    """Grade the projected word field by field, which says WHICH field is
    wrong when a packing change would only show as a wrong number."""
    m = context.amap.fabric_map.get(co, {'en': 0, 'stream': 0, 'ch': 0})
    assert (m['en'], m['stream'], m['ch']) == (en, s, ch), \
        f'cluster_offset {co}: fabric word {m}, expected en={en} stream={s} ch={ch}'


@then('the fabric map word at cluster_offset {co:d} equals {val}')
def step_fabric_word_value(context: Context, co: int, val: str) -> None:
    """Grade the packed 7-bit word itself, so the bit ORDER {en, stream, ch}
    is under test and not just the three values."""
    v = int(val, 0)
    assert context.amap.word(co) == v, \
        f'cluster_offset {co}: word {context.amap.word(co):#04x}, expected {v:#04x}'


@then('the fabric render crossbar has {n:d} enabled words')
def step_fabric_enabled(context: Context, n: int) -> None:
    """Count enabled crossbar words - the check that catches an all-or-
    nothing violation writing rows a status-only assertion would miss."""
    assert context.amap.enabled_words() == n, \
        f'{context.amap.enabled_words()} enabled words, expected {n}'


@then('the last GET lists {n:d} mappings')
def step_get_count(context: Context, n: int) -> None:
    """Size the last GET page, refusing to grade one that was never taken;
    the final partition is short, so the count is not always `page`."""
    assert context.amap.last_get is not None, 'no GET page captured'
    assert len(context.amap.last_get) == n, \
        f'GET page has {len(context.amap.last_get)} mappings, expected {n}'


@then('the last GET contains stream {si:d} channel {sc:d} at cluster_offset '
      '{co:d}')
def step_get_contains_port(context: Context, si: int, sc: int,
                           co: int) -> None:
    """Assert one row is on the page, spelled with the PORT-RELATIVE offset
    the response carries rather than the global key the store uses."""
    assert context.amap.last_get is not None, 'no GET page captured'
    assert (si, sc, co, 0) in context.amap.last_get, \
        f'(si={si}, sc={sc}, co={co}) not in GET page {context.amap.last_get}'
