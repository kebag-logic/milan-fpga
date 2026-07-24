# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD step definitions driving the tsn-gen packet_gen binary (the same tool
# used for the AM65x TI board validation): seeded frame generation from the
# protocol YAMLs, bit-exact field patching cross-checked through packet_gen
# --decode, and Milan v1.2 semantic models mirroring the RTL contract
# (KL_aecp_response_builder / KL_acmp_listener — themselves verified by the
# tb/verilator suites).
#
# Every scenario is skipped cleanly when the tsn-gen checkout/binary is not
# present (TSAGEN_DIR), so CI without the tool stays green.

import json
import os
import subprocess

from behave import given, when, then

# ---------------------------------------------------------------------------
# tsn-gen PDU layouts (bit-packed MSB-first from message_type — the tsn-gen
# convention; subtype/sv/version ride the AVTP control layer). Field order
# and widths MUST mirror the protocol YAMLs.
# ---------------------------------------------------------------------------

LAYOUTS = {
    'SET_CLOCK_SOURCE': {
        'yaml_dir': '{tsn}/protocols/application/1722_1/aecp',
        'interface': ('atdecc_aecp_set_clock_source::AECP_SET_CLOCK_SOURCE::'
                      'AECP_SET_CLOCK_SOURCE_IF'),
        'fields': [('message_type', 4), ('status', 5),
                   ('control_data_length', 11), ('target_entity_id', 64),
                   ('controller_entity_id', 64), ('sequence_id', 16),
                   ('u', 1), ('command_type', 15), ('descriptor_type', 16),
                   ('descriptor_index', 16), ('clock_source_index', 16),
                   ('reserved', 16)],
    },
    'SET_CONTROL': {
        'yaml_dir': '{tsn}/protocols/application/1722_1/aecp',
        'interface': ('atdecc_aecp_set_control::AECP_SET_CONTROL::'
                      'AECP_SET_CONTROL_IF'),
        'fields': [('message_type', 4), ('status', 5),
                   ('control_data_length', 11), ('target_entity_id', 64),
                   ('controller_entity_id', 64), ('sequence_id', 16),
                   ('u', 1), ('command_type', 15), ('descriptor_type', 16),
                   ('descriptor_index', 16), ('control_values', 64)],
    },
    'SET_SAMPLING_RATE': {
        'yaml_dir': '{tsn}/protocols/application/1722_1/aecp',
        'interface': ('atdecc_aecp_set_sampling_rate::AECP_SET_SAMPLING_RATE::'
                      'AECP_SET_SAMPLING_RATE_IF'),
        'fields': [('message_type', 4), ('status', 5),
                   ('control_data_length', 11), ('target_entity_id', 64),
                   ('controller_entity_id', 64), ('sequence_id', 16),
                   ('u', 1), ('command_type', 15), ('descriptor_type', 16),
                   ('descriptor_index', 16), ('sampling_rate', 32)],
    },
    'ACMP': {
        'yaml_dir': '{repo}/tests/protocols/acmp',
        'interface': 'milan_acmp::MILAN_ACMP::MILAN_ACMP_IF',
        'fields': [('message_type', 4), ('status', 5),
                   ('control_data_length', 11), ('stream_id', 64),
                   ('controller_entity_id', 64), ('talker_entity_id', 64),
                   ('listener_entity_id', 64), ('talker_unique_id', 16),
                   ('listener_unique_id', 16), ('stream_dest_mac', 48),
                   ('connection_count', 16), ('sequence_id', 16),
                   ('flags', 16), ('stream_vlan_id', 16), ('reserved', 16)],
    },
}

def _layout(context, key):
    lay = LAYOUTS[key]
    tsn = os.path.dirname(os.path.dirname(context.packet_gen))
    tsn = os.path.dirname(tsn)          # .../tsn-gen/build/traffic-gen -> tsn-gen
    repo = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
    yaml_dir = lay['yaml_dir'].format(tsn=tsn, repo=os.path.normpath(repo))
    return yaml_dir, lay['interface'], lay['fields']


# ---- bit helpers (MSB-first packing, identical to packet_gen) -------------

def _field_offset(fields, name):
    off = 0
    for n, w in fields:
        if n == name:
            return off, w
        off += w
    raise KeyError(name)


def extract_field(hexstr, fields, name):
    off, w = _field_offset(fields, name)
    raw = int.from_bytes(bytes.fromhex(hexstr), 'big')
    total = len(hexstr) * 4
    return (raw >> (total - off - w)) & ((1 << w) - 1)


def patch_field(hexstr, fields, name, value):
    off, w = _field_offset(fields, name)
    raw = int.from_bytes(bytes.fromhex(hexstr), 'big')
    total = len(hexstr) * 4
    mask = ((1 << w) - 1) << (total - off - w)
    raw = (raw & ~mask) | ((value & ((1 << w) - 1)) << (total - off - w))
    return raw.to_bytes(len(hexstr) // 2, 'big').hex()


# ---- packet_gen wrappers ---------------------------------------------------

def pg_generate(context, key, seed):
    yaml_dir, iface, _ = _layout(context, key)
    out = subprocess.run(
        [context.packet_gen, '--yaml-dir', yaml_dir, '--interface', iface,
         '--seed', str(seed), '--output', 'json'],
        capture_output=True, timeout=15, check=True)
    return json.loads(out.stdout.decode().strip().splitlines()[-1])


def pg_decode(context, key, hexstr):
    yaml_dir, iface, _ = _layout(context, key)
    out = subprocess.run(
        [context.packet_gen, '--yaml-dir', yaml_dir, '--interface', iface,
         '--decode', '--hex', hexstr],
        capture_output=True, timeout=15, check=True)
    return json.loads(out.stdout.decode().strip().splitlines()[-1])['fields']


# ---------------------------------------------------------------------------
# Milan v1.2 AECP semantic model — mirrors KL_aecp_response_builder for the
# commands under test (the RTL itself is verified by tb/verilator/aecp).
# ---------------------------------------------------------------------------

STATUS_SUCCESS, STATUS_NO_SUCH_DESCRIPTOR, STATUS_BAD_ARGUMENTS = 0, 2, 7
DESC_CLOCK_DOMAIN, DESC_CONTROL = 0x24, 0x1A
CMD_SET_CLOCK_SOURCE, CMD_SET_CONTROL = 22, 24
CMD_SET_SAMPLING_RATE, CMD_GET_SAMPLING_RATE = 20, 21
DESC_AUDIO_UNIT = 0x0002
VALID_RATES = {44100, 48000, 96000}
CMD_GET_CLOCK_SOURCE = 23   # 0x0017


class MilanAecpModel:
    """clock_source_index in 0..2 on CLOCK_DOMAIN[0]; IDENTIFY control is
    LINEAR_UINT8 with step 255 (only 0 / 255 legal) on CONTROL[0]."""

    def __init__(self):
        self.clock_source_index = 0
        self.identify = 0
        self.sampling_rate = 48000

    def process(self, fields):
        cmd = fields['command_type']
        dt, di = fields['descriptor_type'], fields['descriptor_index']
        if cmd == CMD_SET_SAMPLING_RATE:
            if dt != DESC_AUDIO_UNIT or di != 0:
                return STATUS_NO_SUCH_DESCRIPTOR
            if fields['sampling_rate'] not in VALID_RATES:
                return STATUS_BAD_ARGUMENTS
            self.sampling_rate = fields['sampling_rate']
            return STATUS_SUCCESS
        if cmd == CMD_GET_SAMPLING_RATE:
            if dt != DESC_AUDIO_UNIT or di != 0:
                return STATUS_NO_SUCH_DESCRIPTOR
            return STATUS_SUCCESS        # getter: response carries sampling_rate
        if cmd == CMD_GET_CLOCK_SOURCE:
            if dt != DESC_CLOCK_DOMAIN or di != 0:
                return STATUS_NO_SUCH_DESCRIPTOR
            return STATUS_SUCCESS        # getter: no state change; response carries clock_source_index
        if cmd == CMD_SET_CLOCK_SOURCE:
            if dt != DESC_CLOCK_DOMAIN or di != 0:
                return STATUS_NO_SUCH_DESCRIPTOR
            if fields['clock_source_index'] >= 3:
                return STATUS_BAD_ARGUMENTS
            self.clock_source_index = fields['clock_source_index']
            return STATUS_SUCCESS
        if cmd == CMD_SET_CONTROL:
            if dt != DESC_CONTROL or di != 0:
                return STATUS_NO_SUCH_DESCRIPTOR
            value = (fields['control_values'] >> 56) & 0xFF  # first byte
            if value not in (0, 255):
                return STATUS_BAD_ARGUMENTS
            self.identify = value
            return STATUS_SUCCESS
        return None


# ---------------------------------------------------------------------------
# Milan v1.2 ACMP LISTENER model — mirrors KL_acmp_listener (states, response
# field rules; timer/ADP events surface as explicit steps).
# ---------------------------------------------------------------------------

ACMP_CONNECT_RX_CMD, ACMP_DISCONNECT_RX_CMD, ACMP_GET_RX_STATE_CMD = 6, 8, 10
ACMP_STATUS_LISTENER_UNKNOWN_ID = 1
FLAG_FAST_CONNECT, FLAG_STREAMING_WAIT, FLAG_SRP_REG_FAILED = 0x2, 0x8, 0x40

LSM = ['UNBOUND', 'PRB_W_AVAIL', 'PRB_W_DELAY', 'PRB_W_RESP', 'PRB_W_RESP2',
       'PRB_W_RETRY', 'SETTLED_NO_RSV', 'SETTLED_RSV_OK']


class MilanListenerModel:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.state = 'UNBOUND'
        self.talker = 0
        self.tuid = 0
        self.flags = 0
        self.sid = 0
        self.dmac = 0
        self.vlan = 0
        self.active = False
        self.ta_registered = False
        self.tk_avail = False
        self.probe_seq = 0
        self.probes = []          # emitted PROBE_TX commands

    # -- helpers ------------------------------------------------------------
    def _probe(self, controller):
        self.probes.append({
            'message_type': 0, 'controller_entity_id': controller,
            'talker_entity_id': self.talker, 'listener_entity_id': self.entity_id,
            'talker_unique_id': self.tuid, 'listener_unique_id': 0,
            'sequence_id': self.probe_seq, 'stream_id': 0,
            'stream_dest_mac': 0, 'stream_vlan_id': 0,
            'flags': self.flags & ~(FLAG_STREAMING_WAIT | FLAG_SRP_REG_FAILED)})
        self.probe_seq += 1

    # -- frame events ---------------------------------------------------------
    def handle(self, f):
        """Returns the response fields dict, or None (frame ignored)."""
        if f['message_type'] not in (ACMP_CONNECT_RX_CMD,
                                     ACMP_DISCONNECT_RX_CMD,
                                     ACMP_GET_RX_STATE_CMD):
            return None
        if f['listener_entity_id'] != self.entity_id:
            return None            # not accessible: ignored (acmp.c gate)
        resp = dict(f)
        resp['message_type'] = f['message_type'] + 1
        resp['status'] = 0

        if f['listener_unique_id'] != 0:
            resp['status'] = ACMP_STATUS_LISTENER_UNKNOWN_ID
            return resp

        if f['message_type'] == ACMP_CONNECT_RX_CMD:
            same = (self.state != 'UNBOUND'
                    and f['talker_entity_id'] == self.talker
                    and f['talker_unique_id'] == self.tuid
                    and ((f['flags'] & self.flags & FLAG_STREAMING_WAIT) != 0
                         or ((f['flags'] | self.flags)
                             & FLAG_STREAMING_WAIT) == 0))
            # Table 5.32 response
            resp['connection_count'] = 1
            resp['flags'] = f['flags'] & ~(FLAG_FAST_CONNECT
                                           | FLAG_SRP_REG_FAILED)
            resp['stream_id'] = 0
            resp['stream_dest_mac'] = 0
            resp['stream_vlan_id'] = 0
            if not same:
                if self.state in ('SETTLED_NO_RSV', 'SETTLED_RSV_OK'):
                    self.active = False
                self.talker = f['talker_entity_id']
                self.tuid = f['talker_unique_id']
                self.flags = f['flags']
                self.sid = ((self.talker & 0xFFFFFFFFFFFF0000) | self.tuid
                            if ((self.talker >> 24) & 0xFFFF) != 0xFFFE else
                            (((self.talker >> 40) << 40)
                             | ((self.talker & 0xFFFFFF) << 16) | self.tuid))
                self._probe(f['controller_entity_id'])
                self.state = 'PRB_W_RESP'
            return resp

        if f['message_type'] == ACMP_DISCONNECT_RX_CMD:
            # Table 5.36 response
            resp['talker_entity_id'] = 0
            resp['talker_unique_id'] = self.tuid
            resp['connection_count'] = 0
            resp['flags'] = f['flags'] & ~(FLAG_STREAMING_WAIT
                                           | FLAG_FAST_CONNECT
                                           | FLAG_SRP_REG_FAILED)
            resp['stream_id'] = 0
            resp['stream_dest_mac'] = 0
            resp['stream_vlan_id'] = 0
            self.state = 'UNBOUND'
            self.talker = self.tuid = self.flags = self.sid = 0
            self.dmac = self.vlan = 0
            self.active = False
            return resp

        # GET_RX_STATE — Table 5.37
        bound = self.state != 'UNBOUND'
        resp['talker_entity_id'] = self.talker if bound else 0
        resp['talker_unique_id'] = self.tuid
        resp['connection_count'] = 1 if bound else 0
        resp['stream_dest_mac'] = 0          # reference zeroes it
        if not bound:
            resp['flags'] = 0
        elif self.state in ('SETTLED_NO_RSV', 'SETTLED_RSV_OK'):
            resp['flags'] = self.flags & FLAG_STREAMING_WAIT
        else:
            resp['flags'] = FLAG_STREAMING_WAIT
        return resp

    # -- non-frame events -----------------------------------------------------
    def probe_response(self, status, sid, dmac, vlan):
        assert self.state in ('PRB_W_RESP', 'PRB_W_RESP2')
        if status == 0:
            self.sid, self.dmac, self.vlan = sid, dmac, vlan
            self.active = True
            self.state = 'SETTLED_NO_RSV'
        else:
            self.state = 'PRB_W_RETRY'

    def ta_event(self, registered):
        self.ta_registered = registered
        if registered and self.state == 'SETTLED_NO_RSV':
            self.state = 'SETTLED_RSV_OK'
        elif not registered and self.state == 'SETTLED_RSV_OK':
            self.active = False
            self.state = 'PRB_W_DELAY' if self.tk_avail else 'PRB_W_AVAIL'


# ---------------------------------------------------------------------------
# Steps — common
# ---------------------------------------------------------------------------

@given('the tsn_gen packet generator is available')
def step_tsn_gen_available(context):
    if not getattr(context, 'has_packet_gen', False):
        context.scenario.skip('tsn-gen packet_gen binary not present')
        return


@given('tsn_gen generated a {key} frame with seed {seed:d}')
def step_generate(context, key, seed):
    pkt = pg_generate(context, key, seed)
    context.frame_key = key
    context.frame_hex = pkt['hex']
    context.frame_fields = pkt['fields']


@when('I patch field "{name}" to {value}')
def step_patch(context, name, value):
    val = int(value, 0)
    _, _, fields = _layout(context, context.frame_key)
    context.frame_hex = patch_field(context.frame_hex, fields, name, val)
    context.frame_fields[name] = val


@then('tsn_gen decodes every patched field back')
def step_decode_back(context):
    decoded = pg_decode(context, context.frame_key, context.frame_hex)
    for name, expect in context.frame_fields.items():
        assert decoded[name] == expect, \
            f'{name}: tsn_gen decoded {decoded[name]}, expected {expect}'


@then('our field extractor agrees with tsn_gen on every field')
def step_extractor_agrees(context):
    _, _, fields = _layout(context, context.frame_key)
    decoded = pg_decode(context, context.frame_key, context.frame_hex)
    for name, _w in fields:
        ours = extract_field(context.frame_hex, fields, name)
        assert ours == decoded[name], \
            f'{name}: extractor {ours} != tsn_gen {decoded[name]}'


@then('field "{name}" equals {value}')
def step_field_equals(context, name, value):
    val = int(value, 0)
    actual = context.frame_fields[name]
    assert actual == val, f'{name}={actual}, expected {val}'


@then('the tsn_gen control_data_length overshoots the Milan wire CDL {milan:d} by 8')
def step_cdl_deviation(context, milan):
    # tsn-gen counts target_entity_id into the CDL (known model deviation,
    # pinned so nobody "fixes" a drill against the wrong oracle again)
    cdl = context.frame_fields['control_data_length']
    assert cdl == milan + 8, \
        f'tsn_gen CDL {cdl}: expected the Milan value {milan} + 8'


# ---------------------------------------------------------------------------
# Steps — Milan AECP semantics
# ---------------------------------------------------------------------------

@given('a fresh Milan AECP model')
def step_fresh_model(context):
    context.aecp_model = MilanAecpModel()


@when('the Milan AECP model processes the frame')
def step_model_process(context):
    context.model_status = context.aecp_model.process(context.frame_fields)


@then('the model responds status {code:d}')
def step_model_status(context, code):
    assert context.model_status == code, \
        f'model status {context.model_status}, expected {code}'


@then('the model clock_source_index is {v:d}')
def step_model_csi(context, v):
    assert context.aecp_model.clock_source_index == v


@then('the model identify level is {v:d}')
def step_model_identify(context, v):
    assert context.aecp_model.identify == v


@when('the model processes {n:d} SET_CLOCK_SOURCE frames from seeds {a:d} to {b:d}')
def step_model_fuzz(context, n, a, b):
    assert b - a + 1 == n
    context.fuzz_results = []
    for seed in range(a, b + 1):
        pkt = pg_generate(context, 'SET_CLOCK_SOURCE', seed)
        f = pkt['fields']
        status = context.aecp_model.process(f)
        context.fuzz_results.append((f, status))


@then('every SUCCESS was a valid CLOCK_DOMAIN write and nothing else mutated state')
def step_fuzz_invariant(context):
    for f, status in context.fuzz_results:
        legal = (f['descriptor_type'] == DESC_CLOCK_DOMAIN
                 and f['descriptor_index'] == 0
                 and f['clock_source_index'] < 3)
        if status == STATUS_SUCCESS:
            assert legal, f'model accepted an illegal write: {f}'
        else:
            assert not legal or status is None, \
                f'model rejected a legal write with {status}: {f}'
    csi = context.aecp_model.clock_source_index
    assert csi < 3, f'state corrupted: clock_source_index={csi}'


# ---------------------------------------------------------------------------
# Steps — Milan ACMP listener
# ---------------------------------------------------------------------------

@given('the Milan listener model adopts the frame\'s listener entity id')
def step_listener_adopt(context):
    context.listener = MilanListenerModel(
        context.frame_fields['listener_entity_id'])


@given('a Milan listener model with entity id {eid}')
def step_listener_with_eid(context, eid):
    context.listener = MilanListenerModel(int(eid, 0))


@when('the frame is delivered to the listener model')
def step_deliver(context):
    context.acmp_resp = context.listener.handle(context.frame_fields)


@then('the listener ignores the frame')
def step_ignored(context):
    assert context.acmp_resp is None, \
        f'expected the frame to be ignored, got {context.acmp_resp}'


@then('the listener responds message_type {mt:d} with status {st:d}')
def step_acmp_resp(context, mt, st):
    r = context.acmp_resp
    assert r is not None, 'no response emitted'
    assert r['message_type'] == mt, f"message_type={r['message_type']}"
    assert r['status'] == st, f"status={r['status']}"


@then('the response connection_count is {n:d}')
def step_resp_count(context, n):
    assert context.acmp_resp['connection_count'] == n


@then('the response stream fields are zero')
def step_resp_stream_zero(context):
    r = context.acmp_resp
    assert r['stream_id'] == 0 and r['stream_dest_mac'] == 0 \
        and r['stream_vlan_id'] == 0, f'stream fields not zeroed: {r}'


@then('the response clears FAST_CONNECT and SRP_REGISTRATION_FAILED')
def step_resp_flags_cleared(context):
    fl = context.acmp_resp['flags']
    assert (fl & (FLAG_FAST_CONNECT | FLAG_SRP_REG_FAILED)) == 0, hex(fl)


@then('the response talker entity id is zero')
def step_resp_talker_zero(context):
    assert context.acmp_resp['talker_entity_id'] == 0


@then('the response talker matches the bound talker')
def step_resp_talker_bound(context):
    assert context.acmp_resp['talker_entity_id'] == context.listener.talker


@then('the response flags carry STREAMING_WAIT')
def step_resp_flags_sw(context):
    assert context.acmp_resp['flags'] & FLAG_STREAMING_WAIT, \
        hex(context.acmp_resp['flags'])


@then('the listener state is {state}')
def step_listener_state(context, state):
    assert context.listener.state == state, \
        f'state={context.listener.state}, expected {state}'


@then('a PROBE_TX command was emitted to the bound talker')
def step_probe_emitted(context):
    assert context.listener.probes, 'no probe emitted'
    p = context.listener.probes[-1]
    assert p['message_type'] == 0
    assert p['talker_entity_id'] == context.listener.talker
    assert p['listener_entity_id'] == context.listener.entity_id
    assert p['stream_id'] == 0 and p['stream_dest_mac'] == 0
    assert (p['flags'] & (FLAG_STREAMING_WAIT | FLAG_SRP_REG_FAILED)) == 0


@then('the probe sequence id was {n:d}')
def step_probe_seq(context, n):
    assert context.listener.probes[-1]['sequence_id'] == n


@when('the talker answers the probe with status {st:d} stream_id {sid} dmac {dmac} vlan {vlan:d}')
def step_probe_answer(context, st, sid, dmac, vlan):
    context.listener.probe_response(st, int(sid, 0), int(dmac, 0), vlan)


@when('the TalkerAdvertise registrar reports {what}')
def step_ta_event(context, what):
    context.listener.ta_event(what == 'registered')


@then('the listener sink is {onoff}')
def step_sink(context, onoff):
    assert context.listener.active == (onoff == 'active'), \
        f'active={context.listener.active}'


@then('the bound stream vlan is {v:d}')
def step_bound_vlan(context, v):
    assert context.listener.vlan == v


@when('I deliver {n:d} tsn_gen ACMP frames with seeds {a:d} to {b:d} to the listener model')
def step_acmp_fuzz(context, n, a, b):
    assert b - a + 1 == n
    context.fuzz_acmp = []
    for seed in range(a, b + 1):
        pkt = pg_generate(context, 'ACMP', seed)
        f = pkt['fields']
        resp = context.listener.handle(f)
        context.fuzz_acmp.append((f, resp))


@then('only listener commands addressed to the model were answered')
def step_acmp_fuzz_invariant(context):
    for f, resp in context.fuzz_acmp:
        addressed = (f['listener_entity_id'] == context.listener.entity_id
                     and f['message_type'] in (6, 8, 10))
        if resp is None:
            assert not addressed, f'addressed frame ignored: {f}'
        else:
            assert addressed, f'unaddressed frame answered: {f}'
            assert resp['message_type'] == f['message_type'] + 1
    assert context.listener.state in LSM


@then('the model sampling_rate is {v:d}')
def _model_sr(context, v):
    assert context.aecp_model.sampling_rate == v, f"sr={context.aecp_model.sampling_rate}"
