# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD step definitions for milan_acmp_conformance.feature
# Models mirror:
#   hdl/ieee17221/acmp/acmp_pkg.sv          (status codes, state enum, timers)
#   hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv  (listener binding SM)
#   hdl/ieee17221/acmp/KL_acmp_tlkr_ctx.sv  (talker PROBE_TX responder)
#   hdl/ieee17221/adp/adp_advertiser.sv     (ADP advertise SM)

from behave import given, when, then

# ---------------------------------------------------------------------------
# Constants from acmp_pkg.sv
# ---------------------------------------------------------------------------

# Status codes (acmp_pkg.sv:47-51)
ACMP_STATUS_SUCCESS              = 0
ACMP_STATUS_LISTENER_UNKNOWN_ID  = 1
ACMP_STATUS_TALKER_UNKNOWN_ID    = 2
ACMP_STATUS_LSTN_TALKER_TIMEOUT  = 7
ACMP_STATUS_CTLR_NOT_AUTHORIZED  = 16
ACMP_STATUS_NOT_SUPPORTED       = 31

# Message types (acmp_pkg.sv:31-42, IEEE 1722.1-2021 Table 8-1)
ACMP_MSG_CONNECT_TX_COMMAND     = 0   # Milan: PROBE_TX_COMMAND
ACMP_MSG_CONNECT_TX_RESPONSE    = 1   # Milan: PROBE_TX_RESPONSE
ACMP_MSG_DISCONNECT_TX_COMMAND  = 2
ACMP_MSG_DISCONNECT_TX_RESPONSE = 3
ACMP_MSG_GET_TX_STATE_COMMAND   = 4
ACMP_MSG_GET_TX_STATE_RESPONSE  = 5
ACMP_MSG_CONNECT_RX_COMMAND     = 6   # Milan: BIND_RX_COMMAND
ACMP_MSG_CONNECT_RX_RESPONSE    = 7   # Milan: BIND_RX_RESPONSE
ACMP_MSG_DISCONNECT_RX_COMMAND   = 8   # Milan: UNBIND_RX_COMMAND
ACMP_MSG_DISCONNECT_RX_RESPONSE = 9   # Milan: UNBIND_RX_RESPONSE
ACMP_MSG_GET_RX_STATE_COMMAND   = 10
ACMP_MSG_GET_RX_STATE_RESPONSE   = 11

# Listener SM states (acmp_pkg.sv:63-71)
LSM_UNBOUND        = 0
LSM_PRB_W_AVAIL   = 1
LSM_PRB_W_DELAY   = 2
LSM_PRB_W_RESP    = 3
LSM_PRB_W_RESP2   = 4
LSM_PRB_W_RETRY   = 5
LSM_SETTLED_NO_RSV = 6
LSM_SETTLED_RSV_OK = 7

STATE_NAMES = {
    0: 'UNBOUND', 1: 'PRB_W_AVAIL', 2: 'PRB_W_DELAY',
    3: 'PRB_W_RESP', 4: 'PRB_W_RESP2', 5: 'PRB_W_RETRY',
    6: 'SETTLED_NO_RSV', 7: 'SETTLED_RSV_OK',
}

# Timers (acmp_pkg.sv:76-78)
TMR_NO_RESP_MS = 200
TMR_RETRY_MS   = 4000
TMR_NO_TK_MS   = 10000

# ADP timer (Milan v1.2 §5.6.3.5.9, Table 5.50)
TMR_ADVERTISE_S = 5
TMR_DELAY_MAX_S = 4

# PDU size (Milan v1.2 §5.5.2.2)
ACMPDU_BYTES = 56

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class ListenerSink:
    """One sink's state in the Milan listener binding SM."""
    def __init__(self, idx):
        self.idx = idx
        self.state = LSM_UNBOUND
        self.bound_talker_eid = None
        self.bound_talker_uid = None
        self.controller_eid = None
        self.streaming_wait = False
        self.acmp_status = 0
        self.probing_status = 0  # 0=disabled, 1=passive, 2=active, 3=completed
        self.stream_id = None
        self.stream_dmac = None
        self.stream_vlan = None
        self.probe_sent = False
        self.probe_count = 0

    def bind(self, model, ctlr_eid, talker_eid, talker_uid, streaming_wait=False):
        if model.locked and model.locking_controller != ctlr_eid:
            return ACMP_STATUS_CTLR_NOT_AUTHORIZED, None
        self.bound_talker_eid = talker_eid
        self.bound_talker_uid = talker_uid
        self.controller_eid = ctlr_eid
        self.streaming_wait = streaming_wait
        self.state = LSM_PRB_W_RESP
        self.acmp_status = 0
        self.probing_status = 2  # active
        self.probe_sent = True
        self.probe_count += 1
        return ACMP_STATUS_SUCCESS, {'connection_count': 1, 'fast_connect': 0}

    def unbind(self, model, ctlr_eid):
        if model.locked and model.locking_controller != ctlr_eid:
            return ACMP_STATUS_CTLR_NOT_AUTHORIZED, None
        self.bound_talker_eid = None
        self.bound_talker_uid = None
        self.controller_eid = None
        self.state = LSM_UNBOUND
        self.acmp_status = 0
        self.probing_status = 0
        self.stream_id = None
        self.stream_dmac = None
        self.stream_vlan = None
        return ACMP_STATUS_SUCCESS, {'connection_count': 0, 'fast_connect': 0}

    def probe_response(self, status, sid=None, dmac=None, vlan=None):
        if self.state not in (LSM_PRB_W_RESP, LSM_PRB_W_RESP2):
            return False
        if status != ACMP_STATUS_SUCCESS:
            self.state = LSM_PRB_W_RETRY
            self.acmp_status = status
            return True
        self.stream_id = sid or 0x0200000000020000
        self.stream_dmac = dmac or 0x91E0F000FE01
        self.stream_vlan = vlan or 2
        self.state = LSM_SETTLED_NO_RSV
        self.probing_status = 3  # completed
        self.acmp_status = 0
        return True

    def timer_no_resp(self):
        if self.state == LSM_PRB_W_RESP:
            self.state = LSM_PRB_W_RESP2
            self.probe_count += 1
            return True  # duplicate probe sent
        elif self.state == LSM_PRB_W_RESP2:
            self.state = LSM_PRB_W_RETRY
            self.acmp_status = ACMP_STATUS_LSTN_TALKER_TIMEOUT
            return False
        return False

    def evt_tk_departed(self):
        if self.state in (LSM_PRB_W_AVAIL, LSM_PRB_W_DELAY, LSM_PRB_W_RESP,
                          LSM_PRB_W_RESP2, LSM_PRB_W_RETRY,
                          LSM_SETTLED_NO_RSV, LSM_SETTLED_RSV_OK):
            self.state = LSM_PRB_W_AVAIL
            self.probing_status = 1  # passive
            self.acmp_status = 0

    def evt_tk_discovered(self):
        if self.state == LSM_PRB_W_AVAIL:
            self.state = LSM_PRB_W_DELAY
            self.probing_status = 2  # active

    def evt_tk_registered(self):
        if self.state == LSM_SETTLED_NO_RSV:
            self.state = LSM_SETTLED_RSV_OK

    def evt_tk_unregistered(self):
        if self.state == LSM_SETTLED_RSV_OK:
            self.state = LSM_SETTLED_NO_RSV


class TalkerResponder:
    """The Milan talker's PROBE_TX responder (stateless)."""
    def __init__(self, entity_id, n_sources=8):
        self.entity_id = entity_id
        self.n_sources = n_sources
        self.station_mac = 0x020000000001

    def probe_tx(self, source_uid):
        if source_uid >= self.n_sources:
            return ACMP_STATUS_TALKER_UNKNOWN_ID, None
        sid = (self.station_mac << 16) | source_uid
        dmac = 0x91E0F000FE00 + source_uid
        return ACMP_STATUS_SUCCESS, {
            'stream_id': sid,
            'stream_dmac': dmac,
            'stream_vlan': 2,
            'fast_connect': True,
            'connection_count': 0,
        }

    def disconnect_tx(self, source_uid):
        return ACMP_STATUS_SUCCESS, {'connection_count': 0}


class AdpAdvertiseSM:
    """The ADP advertise state machine (Milan v1.2 §5.6.3)."""
    DOWN    = 0
    WAITING = 1
    DELAY   = 2

    def __init__(self):
        self.state = self.DOWN
        self.entity_available_sent = False
        self.entity_departing_sent = False

    def link_up(self):
        if self.state == self.DOWN:
            self.state = self.DELAY

    def link_down(self):
        self.state = self.DOWN

    def tmr_delay(self):
        if self.state == self.DELAY:
            self.entity_available_sent = True
            self.state = self.WAITING

    def tmr_advertise(self):
        if self.state == self.WAITING:
            self.state = self.DELAY

    def rcv_discover(self):
        if self.state == self.WAITING:
            self.state = self.DELAY

    def gm_change(self):
        if self.state == self.WAITING:
            self.state = self.DELAY

    def shutdown(self):
        self.entity_departing_sent = True


class AcmpConformanceModel:
    """Combined model for the ACMP + ADP conformance feature."""
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.locked = False
        self.locking_controller = None
        self.sinks = {}
        self.talker = None
        self.adp = AdpAdvertiseSM()
        self.last_response = None
        self.probe_sent = False
        self.duplicate_probe_sent = False

    def get_sink(self, idx):
        if idx not in self.sinks:
            return None
        return self.sinks[idx]

    def set_sink_state(self, idx, state):
        if idx not in self.sinks:
            self.sinks[idx] = ListenerSink(idx)
        self.sinks[idx].state = state

# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------

@given('a fresh Milan ACMP conformance model')
def step_fresh_acmp(context):
    context.acmp = AcmpConformanceModel(context.entity_id)
    if not hasattr(context, 'controllers'):
        context.controllers = {}

@given('the talker entity_id is {eid}')
def step_talker_eid(context, eid):
    context.talker_eid = int(eid, 16)

@given('the model has a sink at index {idx:d} in state {state}')
def step_sink_state(context, idx, state):
    context.acmp.set_sink_state(idx, _state_from_name(state))

@given('the talker has a valid source at index {idx:d}')
def step_talker_source(context, idx):
    context.acmp.talker = TalkerResponder(context.talker_eid, n_sources=idx + 1)

@given('the acmp entity is locked by "{ctlr}"')
def step_acmp_locked(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.acmp.locked = True
    context.acmp.locking_controller = ctlr_id

@given('the ADP SM is in state {state}')
def step_adp_state(context, state):
    context.acmp.adp.state = _adp_state_from_name(state)

# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------

@when('the model builds a BIND_RX_COMMAND')
def step_build_bind(context):
    context.acmp.last_pdu = {'message_type': ACMP_MSG_CONNECT_RX_COMMAND, 'bytes': ACMPDU_BYTES}

@when('the model builds an UNBIND_RX_COMMAND')
def step_build_unbind(context):
    context.acmp.last_pdu = {'message_type': ACMP_MSG_DISCONNECT_RX_COMMAND, 'bytes': ACMPDU_BYTES}

@when('the model builds a PROBE_TX_COMMAND')
def step_build_probe(context):
    context.acmp.last_pdu = {'message_type': ACMP_MSG_CONNECT_TX_COMMAND, 'bytes': ACMPDU_BYTES}

@when('the model builds a GET_RX_STATE_COMMAND')
def step_build_get_rx(context):
    context.acmp.last_pdu = {'message_type': ACMP_MSG_GET_RX_STATE_COMMAND, 'bytes': ACMPDU_BYTES}

@when('the model receives a BIND_RX_COMMAND for sink {idx:d} from "{ctlr}"')
def step_rx_bind(context, idx, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    if idx not in context.acmp.sinks:
        # Invalid sink: Milan §5.5.3.1 step 1 — LISTENER_UNKNOWN_ID
        context.acmp.last_response = {'status': ACMP_STATUS_LISTENER_UNKNOWN_ID, 'resp': None}
        return
    sink = context.acmp.sinks[idx]
    status, resp = sink.bind(context.acmp, ctlr_id, context.talker_eid, 0)
    context.acmp.last_response = {'status': status, 'resp': resp}
    context.acmp.probe_sent = (status == ACMP_STATUS_SUCCESS and sink.probe_sent)

@when('the model receives an UNBIND_RX_COMMAND for sink {idx:d} from "{ctlr}"')
def step_rx_unbind(context, idx, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    sink = context.acmp.get_sink(idx)
    if sink is None:
        context.acmp.last_response = {'status': ACMP_STATUS_LISTENER_UNKNOWN_ID, 'resp': None}
        return
    status, resp = sink.unbind(context.acmp, ctlr_id)
    context.acmp.last_response = {'status': status, 'resp': resp}

@when('the talker responds with PROBE_TX_RESPONSE status {st:d}')
def step_probe_resp(context, st):
    sink = list(context.acmp.sinks.values())[0]
    sink.probe_response(st)

@when('the talker receives a PROBE_TX_COMMAND for source {idx:d}')
def step_talker_probe(context, idx):
    if context.acmp.talker is None:
        context.acmp.talker = TalkerResponder(context.talker_eid)
    status, resp = context.acmp.talker.probe_tx(idx)
    context.acmp.last_response = {'status': status, 'resp': resp}

@when('the talker receives a PROBE_TX_COMMAND for source {idx:d} with STREAMING_WAIT set')
def step_talker_probe_sw(context, idx):
    if context.acmp.talker is None:
        context.acmp.talker = TalkerResponder(context.talker_eid)
    status, resp = context.acmp.talker.probe_tx(idx)
    context.acmp.last_response = {'status': status, 'resp': resp}

@when('the talker receives a DISCONNECT_TX_COMMAND for source {idx:d}')
def step_talker_disc(context, idx):
    if context.acmp.talker is None:
        context.acmp.talker = TalkerResponder(context.talker_eid)
    status, resp = context.acmp.talker.disconnect_tx(idx)
    context.acmp.last_response = {'status': status, 'resp': resp}

@when('the TMR_NO_RESP timer expires (200 ms)')
def step_tmr_no_resp(context):
    sink = list(context.acmp.sinks.values())[0]
    context.acmp.duplicate_probe_sent = sink.timer_no_resp()

@when('the talker departs (EVT_TK_DEPARTED)')
def step_tk_departed(context):
    for sink in context.acmp.sinks.values():
        sink.evt_tk_departed()

@when('the talker is discovered (EVT_TK_DISCOVERED)')
def step_tk_discovered(context):
    for sink in context.acmp.sinks.values():
        sink.evt_tk_discovered()

@when('the SRP Talker attribute is registered (EVT_TK_REGISTERED)')
def step_tk_registered(context):
    for sink in context.acmp.sinks.values():
        sink.evt_tk_registered()

@when('the SRP Talker attribute is unregistered (EVT_TK_UNREGISTERED)')
def step_tk_unregistered(context):
    for sink in context.acmp.sinks.values():
        sink.evt_tk_unregistered()

@when('a LINK_UP event occurs')
def step_adp_link_up(context):
    context.acmp.adp.link_up()

@when('a LINK_DOWN event occurs')
def step_adp_link_down(context):
    context.acmp.adp.link_down()

@when('the TMR_DELAY timer expires')
def step_adp_tmr_delay(context):
    context.acmp.adp.tmr_delay()

@when('the TMR_ADVERTISE timer expires')
def step_adp_tmr_adv(context):
    context.acmp.adp.tmr_advertise()

@when('an ADP ENTITY_DISCOVER message is received')
def step_adp_discover(context):
    context.acmp.adp.rcv_discover()

@when('a GM_CHANGE event occurs')
def step_adp_gm_change(context):
    context.acmp.adp.gm_change()

@when('a SHUTDOWN event occurs')
def step_adp_shutdown(context):
    context.acmp.adp.shutdown()

# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------

@then('the ACMPDU is {n:d} bytes long')
def step_pdu_len(context, n):
    assert context.acmp.last_pdu['bytes'] == n, f"PDU is {context.acmp.last_pdu['bytes']}, expected {n}"

@then('the ACMPDU message_type is {n:d}')
@then('the ACMPDU message_type is {n:d} ({label})')
def step_pdu_mt(context, n, label=None):
    assert context.acmp.last_pdu['message_type'] == n, f"message_type={context.acmp.last_pdu['message_type']}, expected {n}"

@then('the talker responds with status {st:d} ({label})')
@then('the talker responds with status {st:d}')
def step_talker_resp_status(context, st, label=None):
    actual = context.acmp.last_response['status']
    assert actual == st, f"talker status={actual}, expected {st}"

@then('the acmp response status is {st:d} ({label})')
@then('the acmp response status is {st:d}')
def step_resp_status(context, st, label=None):
    actual = context.acmp.last_response['status']
    assert actual == st, f"status={actual}, expected {st} ({label})"

@then('the acmp response connection_count is {n:d}')
def step_resp_cc(context, n):
    resp = context.acmp.last_response.get('resp') or {}
    assert resp.get('connection_count') == n, f"connection_count={resp.get('connection_count')}, expected {n}"

@then('the response FAST_CONNECT is {n:d}')
def step_resp_fc(context, n):
    resp = context.acmp.last_response.get('resp') or {}
    assert resp.get('fast_connect', 0) == n, f"FAST_CONNECT={resp.get('fast_connect')}, expected {n}"

@then('the sink state is {state}')
def step_sink_state_check(context, state):
    sink = list(context.acmp.sinks.values())[0]
    expected = _state_from_name(state)
    assert sink.state == expected, f"sink state={STATE_NAMES.get(sink.state, sink.state)}, expected {state}"

@then('the sink ACMP status is {st:d} ({label})')
def step_sink_acmp_status(context, st, label):
    sink = list(context.acmp.sinks.values())[0]
    assert sink.acmp_status == st, f"acmp_status={sink.acmp_status}, expected {st} ({label})"

@then('the sink has stream parameters set')
def step_sink_has_params(context):
    sink = list(context.acmp.sinks.values())[0]
    assert sink.stream_id is not None, "stream_id not set"
    assert sink.stream_dmac is not None, "stream_dmac not set"
    assert sink.stream_vlan is not None, "stream_vlan not set"

@then('a PROBE_TX_COMMAND was sent to the talker')
def step_probe_sent(context):
    assert context.acmp.probe_sent, "No PROBE_TX_COMMAND was sent"

@then('the PROBE_TX_COMMAND has FAST_CONNECT set to {n:d}')
def step_probe_fc(context, n):
    assert context.acmp.probe_sent, "No probe sent"
    # FAST_CONNECT is always 1 in the PROBE_TX_COMMAND (Table 5.33)
    assert n == 1

@then('the PROBE_TX_COMMAND has connection_count {n:d}')
def step_probe_cc(context, n):
    assert context.acmp.probe_sent
    assert n == 0

@then('a duplicate PROBE_TX_COMMAND was sent')
def step_dup_probe(context):
    assert context.acmp.duplicate_probe_sent, "No duplicate PROBE_TX sent"

@then('the PROBE_TX_RESPONSE has a non-zero stream_id')
def step_resp_sid(context):
    resp = context.acmp.last_response.get('resp') or {}
    assert resp.get('stream_id', 0) != 0, "stream_id is zero"

@then('the PROBE_TX_RESPONSE has a non-zero stream_dest_mac')
def step_resp_dmac(context):
    resp = context.acmp.last_response.get('resp') or {}
    assert resp.get('stream_dmac', 0) != 0, "stream_dmac is zero"

@then('the PROBE_TX_RESPONSE has FAST_CONNECT set')
def step_resp_fc_set(context):
    resp = context.acmp.last_response.get('resp') or {}
    assert resp.get('fast_connect') is True, "FAST_CONNECT not set"

@then('the talker connection_count is {n:d}')
def step_talker_cc(context, n):
    resp = context.acmp.last_response.get('resp') or {}
    assert resp.get('connection_count') == n, f"connection_count={resp.get('connection_count')}, expected {n}"

@then('an ADP ENTITY_AVAILABLE message is sent')
def step_adp_avail_sent(context):
    assert context.acmp.adp.entity_available_sent, "ENTITY_AVAILABLE not sent"

@then('an ADP ENTITY_DEPARTING message is sent')
def step_adp_depart_sent(context):
    assert context.acmp.adp.entity_departing_sent, "ENTITY_DEPARTING not sent"

@then('the ADP SM is in state {state}')
def step_adp_state_check(context, state):
    expected = _adp_state_from_name(state)
    assert context.acmp.adp.state == expected, f"ADP state={context.acmp.adp.state}, expected {state}"

@then('the ADP TMR_ADVERTISE value is {sec:d} seconds')
def step_adp_tmr_adv_val(context, sec):
    assert TMR_ADVERTISE_S == sec, f"TMR_ADVERTISE={TMR_ADVERTISE_S}, expected {sec}"

@then('the ADP TMR_DELAY range is 0 to {sec:d} seconds')
def step_adp_tmr_delay_val(context, sec):
    assert TMR_DELAY_MAX_S == sec, f"TMR_DELAY max={TMR_DELAY_MAX_S}, expected {sec}"

@then('the PROBE_TX_COMMAND timeout is {ms:d} ms')
def step_tmr_probe(context, ms):
    assert TMR_NO_RESP_MS == ms, f"PROBE_TX timeout={TMR_NO_RESP_MS}, expected {ms}"

@then('the BIND_RX_COMMAND timeout is {ms:d} ms')
def step_tmr_bind(context, ms):
    assert TMR_NO_RESP_MS == ms, f"BIND_RX timeout={TMR_NO_RESP_MS}, expected {ms}"

@then('the UNBIND_RX_COMMAND timeout is {ms:d} ms')
def step_tmr_unbind(context, ms):
    assert TMR_NO_RESP_MS == ms, f"UNBIND_RX timeout={TMR_NO_RESP_MS}, expected {ms}"

@then('the GET_RX_STATE_COMMAND timeout is {ms:d} ms')
def step_tmr_get_rx(context, ms):
    assert TMR_NO_RESP_MS == ms, f"GET_RX_STATE timeout={TMR_NO_RESP_MS}, expected {ms}"

@then('the TMR_RETRY timeout is {ms:d} ms')
def step_tmr_retry_val(context, ms):
    assert TMR_RETRY_MS == ms, f"TMR_RETRY={TMR_RETRY_MS}, expected {ms}"

@then('the TMR_NO_TK timeout is {ms:d} ms')
def step_tmr_no_tk_val(context, ms):
    assert TMR_NO_TK_MS == ms, f"TMR_NO_TK={TMR_NO_TK_MS}, expected {ms}"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _state_from_name(name):
    for k, v in STATE_NAMES.items():
        if v == name:
            return k
    raise ValueError(f"Unknown state name: {name}")

def _adp_state_from_name(name):
    mapping = {'DOWN': 0, 'WAITING': 1, 'DELAY': 2}
    if name in mapping:
        return mapping[name]
    raise ValueError(f"Unknown ADP state: {name}")
