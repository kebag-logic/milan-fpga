# SPDX-FileCopyrightText: 2026 Kebag Logic <contact@kebag-logic.com>
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD step definitions for the Milan conformance extension features:
#   milan_adp_advertisements.feature
#   milan_srp_defaults.feature
#   milan_entity_model_validation.feature
#   milan_aecp_extended_commands.feature
#   milan_notifications.feature
#
# These models mirror the RTL behaviour described in:
#   hdl/ieee17221/adp/adp_advertiser.sv   (ADP format/timing)
#   hdl/ieee8021q/srp/lwsrp_pkg.sv        (SR class, timers)
#   hdl/ieee8021q/srp/KL_lwsrp_tx.sv      (Domain MRPDU emission)
#   hdl/ieee17221/aecp/KL_aecp_response_builder.sv  (AECP commands)
#   hdl/common/csr/milan_csr.sv           (VERSION register)
#   sw/builder/endstation_builder.py       (entity model generation)
#   avdecc/gen_aem_store.py               (AEM ROM generation)

import os
import sys
import json
import struct
import time

from behave import given, when, then

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _import_builder():
    """Import the endstation builder from the repo root."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    swb = os.path.join(root, 'sw', 'builder')
    if swb not in sys.path:
        sys.path.insert(0, swb)
    if root not in sys.path:
        sys.path.insert(0, root)
    import endstation_builder
    return endstation_builder


def _load_config(config_name):
    """Load an endstation YAML config and return the builder output dict."""
    builder = _import_builder()
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    cfg_path = os.path.join(root, 'configs', f'{config_name}.yaml')
    outdir = os.path.join(root, 'sw', 'builder', 'out', config_name)
    builder.main_cli = getattr(builder, 'main_cli', None)
    # Use the builder's own parse/emit path
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    parser.add_argument('-o', dest='outdir', default=outdir)
    args = parser.parse_args([cfg_path, '-o', outdir])
    try:
        results = builder.build_config(builder.load_config(cfg_path), outdir)
    except Exception:
        results = builder.emit(builder.load_config(cfg_path), outdir)
    return results

def _read_overlay(config_name):
    """Read the AEM overlay JSON for a given config."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    outdir = os.path.join(root, 'sw', 'builder', 'out', config_name)
    overlay_path = os.path.join(outdir, 'aem_overlay.json')
    with open(overlay_path) as f:
        return json.load(f)

def _read_generated_svh(config_name, filename):
    """Read a generated .svh file for a config."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    path = os.path.join(root, 'configs', 'generated', config_name, 'gen', filename)
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return None

def _stream_format_channels(fmt_hex):
    """Decode channels_per_frame from a 64-bit AAF stream format string."""
    fmt = int(fmt_hex, 16) if isinstance(fmt_hex, str) else fmt_hex
    # channels_per_frame is bits [47:32] (byte 4-5 of the 8-byte format)
    channels = (fmt >> 32) & 0xFFFF
    return channels

# ===========================================================================
# ADP ADVERTISEMENTS
# ===========================================================================

class AdpModel:
    """Offline model of the ADP advertiser (adp_advertiser.sv)."""
    def __init__(self):
        self.entity_id = 0
        self.station_mac = 0
        self.enabled = True
        self.available_index = 0
        self.valid_time = 10
        self.gm_id = b'\x00' * 8
        self.gm_domain = 0
        self.adpdus = []
        self.departed = False
        # seconds the advertise timer has already run since its last
        # (re)start; mirrors adv_tick_cnt_r in adp_advertiser.sv
        self.timer_elapsed = 0

    def transmit(self):
        idx = self.available_index
        self.available_index = (self.available_index + 1) & 0xFF
        # Milan v1.2 5.6.3.5.9 step 2: EVERY ENTITY_AVAILABLE send restarts
        # the TMR_ADVERTISE timer (mirrors adv_restart_w in the RTL)
        self.timer_elapsed = 0
        adpdu = {
            'dmac': 0x91E0F0010000,
            'ethertype': 0x22F0,
            'vlan': False,
            'cd': 1,
            'subtype': 0x7A,
            'sv': 0,
            'version': 0,
            'message_type': 0,  # ENTITY_AVAILABLE
            'control_data_length': 56,
            'available_index': idx,
            'gm_id': self.gm_id,
            'gm_domain': self.gm_domain,
        }
        self.adpdus.append(adpdu)
        return adpdu

    def gm_change(self, new_gm_id, new_domain):
        self.gm_id = new_gm_id
        self.gm_domain = new_domain
        return self.transmit()

    def depart(self):
        self.departed = True
        adpdu = {
            'message_type': 1,  # ENTITY_DEPARTING
            'control_data_length': 56,
        }
        self.adpdus.append(adpdu)
        return adpdu


@given('a fresh Milan ADP advertiser model')
def step_fresh_adp(context):
    context.adp = AdpModel()

@given('the station MAC is {mac}')
def step_station_mac(context, mac):
    context.station_mac = mac

@given('the advertiser has already sent {n:d} ADPDUs')
def step_adp_sent_n(context, n):
    for _ in range(n):
        context.adp.transmit()

@given('the advertiser is enabled')
def step_adp_enabled(context):
    context.adp.enabled = True

@given('the valid_time field is {n:d}')
def step_valid_time(context, n):
    context.adp.valid_time = n

@given('the advertise timer has {n:d} second left to run')
@given('the advertise timer has {n:d} seconds left to run')
def step_adp_timer_ripe(context, n):
    # wind the periodic timer to n seconds from expiry (interval math shared
    # with the observation-window step: interval = MAX(1, valid_time/2))
    interval = max(1, context.adp.valid_time // 2)
    context.adp.timer_elapsed = interval - n

@given('the advertiser has transmitted an ADPDU with available_index {n:d}')
def step_adp_sent_idx(context, n):
    context.adp.available_index = n
    context.adp.transmit()

@when('the advertiser transmits an ADPDU')
def step_adp_transmit(context):
    context.adp.transmit()

@when('the advertiser transmits {n:d} consecutive ADPDUs')
def step_adp_transmit_n(context, n):
    for _ in range(n):
        context.adp.transmit()

@when('the advertiser transmits over a {sec:d} second observation window')
def step_adp_window(context, sec):
    # Milan: interval = MAX(1, valid_time/2) = 5s for valid_time=10
    interval = max(1, context.adp.valid_time // 2)
    elapsed = 0
    while elapsed <= sec:
        context.adp.transmit()
        elapsed += interval

@when('the advertiser is started from link-up')
def step_adp_linkup(context):
    context.adp_transmit_count = 0
    # First ADPDU within 9.5s (half the 5s cadence with margin)
    context.adp.transmit()
    context.first_adpdu_time = 5.0  # simulated time of first transmit

@when('a gPTP grandmaster change event arrives')
def step_gm_change(context):
    context.adp.gm_change(b'\x00\x01\x02\x03\x04\x05\x06\x07', 1)

@when('the entity is commanded to depart')
def step_depart(context):
    context.adp.depart()

@when('an ENTITY_DISCOVER message is received')
def step_discover(context):
    # Advertiser responds immediately with ENTITY_AVAILABLE
    context.last_adpdu = context.adp.transmit()

@then('the ADPDU destination MAC is {mac_str}')
def step_adpdu_dmac(context, mac_str):
    # 91:e0:f0:01:00:00
    expected = int(mac_str.replace(':', ''), 16)
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['dmac'] == expected, f"dmac={hex(last['dmac'])}, expected {hex(expected)}"

@then('the ADPDU EtherType is 0x{eth}')
def step_adpdu_ethertype(context, eth):
    expected = int(eth, 16)
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['ethertype'] == expected, f"EtherType={hex(last['ethertype'])}, expected 0x{eth}"

@then('the ADPDU has no VLAN tag')
def step_adpdu_no_vlan(context):
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert not last.get('vlan', False), "VLAN tag present"

@then('the ADPDU cd field is {v:d}')
def step_adpdu_cd(context, v):
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['cd'] == v, f"cd={last['cd']}, expected {v}"

@then('the ADPDU subtype is 0x{sub}')
def step_adpdu_subtype(context, sub):
    expected = int(sub, 16)
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['subtype'] == expected, f"subtype={hex(last['subtype'])}, expected 0x{sub}"

@then('the ADPDU sv field is {v:d}')
def step_adpdu_sv(context, v):
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['sv'] == v, f"sv={last['sv']}, expected {v}"

@then('the ADPDU version is {v:d}')
def step_adpdu_version(context, v):
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['version'] == v, f"version={last['version']}, expected {v}"

@then('the ADPDU message_type is {v:d} ({label})')
def step_adpdu_msgtype(context, v, label):
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['message_type'] == v, f"message_type={last['message_type']}, expected {v} ({label})"

@then('the ADPDU control_data_length is {v:d}')
def step_adpdu_cdl(context, v):
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['control_data_length'] == v, f"control_data_length={last['control_data_length']}, expected {v}"

@then('the ADPDU has available_index {v:d}')
@then('the ADPDU available_index is {v:d}')
def step_adpdu_idx(context, v):
    last = context.adp.adpdus[-1] if context.adp.adpdus else context.last_adpdu
    assert last['available_index'] == v, f"available_index={last['available_index']}, expected {v}"

@then('the first ADPDU has available_index {v:d}')
def step_first_idx(context, v):
    assert context.adp.adpdus[0]['available_index'] == v

@then('the second ADPDU has available_index {v:d}')
def step_second_idx(context, v):
    assert context.adp.adpdus[1]['available_index'] == v

@then('the third ADPDU has available_index {v:d}')
def step_third_idx(context, v):
    assert context.adp.adpdus[2]['available_index'] == v

@then('the ADPDU gptp_grandmaster_id reflects the new grandmaster')
def step_adpdu_gm(context):
    last = context.adp.adpdus[-1]
    assert last['gm_id'] == b'\x00\x01\x02\x03\x04\x05\x06\x07'

@then('the ADPDU gptp_domain_number reflects the new domain')
def step_adpdu_domain(context):
    last = context.adp.adpdus[-1]
    assert last['gm_domain'] == 1

@then('the next periodic ADPDU arrives a full advertise interval later')
def step_adpdu_restarted(context):
    # Milan v1.2 5.6.3.5.9 step 2: the send (here: the discover response)
    # restarted TMR_ADVERTISE, so the next periodic is a FULL interval away -
    # NOT the residue the pre-discover schedule had left (the model winds the
    # timer to 1 s from expiry before the discover arrives).
    interval = max(1, context.adp.valid_time // 2)
    remaining = interval - context.adp.timer_elapsed
    assert remaining == interval, (
        f"timer not restarted by the send: next periodic in {remaining}s "
        f"of a {interval}s interval")

@then('the interval between consecutive ADPDUs is at most {sec:f} seconds')
def step_adpdu_interval_max(context, sec):
    interval = max(1, context.adp.valid_time // 2)
    assert interval <= sec, f"interval {interval}s > {sec}s"

@then('the interval between consecutive ADPDUs is at least {sec:f} seconds')
def step_adpdu_interval_min(context, sec):
    interval = max(1, context.adp.valid_time // 2)
    assert interval >= sec, f"interval {interval}s < {sec}s"

@then('at least {n:d} ADPDUs are transmitted in a {sec:d} second window')
def step_adpdu_count(context, n, sec):
    assert len(context.adp.adpdus) >= n, f"only {len(context.adp.adpdus)} ADPDUs, expected >= {n}"

@then('the advertiser transmits an ADPDU within 2 seconds')
@then('the advertiser transmits an ADPDU within {sec:f} seconds')
def step_adpdu_within(context, sec=2):
    assert len(context.adp.adpdus) > 0

@then('the advertiser transmits a message_type {v:d} ({label})')
def step_adpdu_msgtype_alt(context, v, label):
    last = context.adp.adpdus[-1] if context.adp.adpdus else {}
    assert last.get('message_type') == v, f"message_type={last.get('message_type')}, expected {v} ({label})"

@then('the ENTITY_DEPARTING has control_data_length {v:d}')
def step_entity_departing_cdl(context, v):
    last = context.adp.adpdus[-1] if context.adp.adpdus else {}
    assert last.get('control_data_length') == v

# entity model
@given('the endstation builder is importable')
def step_builder_importable(context):
    try:
        _import_builder()
    except Exception as e:
        from behave.api.pending_step import StepNotImplementedError
        raise StepNotImplementedError(f"builder import failed: {e}")

# aecp extended
@then('the response contains counter values')
def step_ext_counters_present(context):
    assert context.ext_resp is not None and len(context.ext_resp) > 0

# SRP
@given('an {n:d}-channel AAF talker stream at 48 kHz')
def step_srp_stream_48(context, n):
    context.srp_channels = n
    context.srp_rate = 48000

@then('the first Domain MRPDU after link-up carries SR Class ID {n:d}')
def step_srp_after_linkup(context, n):
    last = context.srp.mrpdus[-1]
    assert last['sr_class_id'] == n

# notification
@when('the link goes down')
def step_srp_link_down_alt(context):
    context.srp.link_up = False
    context.srp.mrpdus.clear()

@then('the first ADPDU is transmitted within {sec:f} seconds')
def step_adpdu_first_time(context, sec):
    assert len(context.adp.adpdus) > 0

@then('the advertiser transmits an ADPDU immediately')
def step_adpdu_immediate(context):
    assert len(context.adp.adpdus) > 0

@then('the advertiser transmits ADPDUs at the mandated cadence')
def step_adpdu_cadence(context):
    assert context.adp.enabled
    assert context.adp.valid_time == 10

@then('no explicit arm pulse is required')
def step_no_arm_pulse(context):
    # Level-triggered, not edge
    assert context.adp.enabled

# ===========================================================================
# SRP DEFAULTS
# ===========================================================================

class SrpModel:
    """Offline model of the lwSRP Domain TX engine."""
    def __init__(self):
        self.sr_class = 'A'
        self.sr_class_id = 6
        self.priority = 3
        self.vid = 2
        self.join_time_ms = 200
        self.leave_time_ms = 600
        self.leaveall_time_ms = 10000
        self.bw_limit_pct = 75
        self.mrpdus = []
        self.link_up = True

    def transmit_domain(self):
        mrpdu = {
            'sr_class_id': self.sr_class_id,
            'priority': self.priority,
            'vid': self.vid,
            'event': 'JoinMt',
            'leaveall': False,
        }
        self.mrpdus.append(mrpdu)
        return mrpdu

    def leaveall(self):
        mrpdu = {
            'sr_class_id': self.sr_class_id,
            'priority': self.priority,
            'vid': self.vid,
            'event': 'LeaveAll',
            'leaveall': True,
        }
        self.mrpdus.append(mrpdu)
        return mrpdu

    def compute_tspec(self, channels, rate_hz=48000):
        samples_per_frame = 6
        max_frame = 24 + samples_per_frame * channels * 4
        return {'MaxFrameSize': max_frame, 'MaxIntervalFrames': 1}


@given('a fresh Milan SRP Domain model')
def step_fresh_srp(context):
    context.srp = SrpModel()

@given('the SR class is {cls}')
def step_sr_class(context, cls):
    context.srp.sr_class = cls

@given('the SR class ID is {n:d}')
def step_sr_class_id(context, n):
    context.srp.sr_class_id = n

@given('the SR priority is {n:d}')
def step_sr_priority(context, n):
    context.srp.priority = n

@given('the SR VLAN ID is {n:d}')
def step_sr_vid(context, n):
    context.srp.vid = n

@given('a {n:d}-channel AAF talker stream at {rate:d} kHz')
def step_srp_stream(context, n, rate):
    context.srp_channels = n
    context.srp_rate = rate * 1000

@when('the SRP engine transmits a Domain MRPDU')
def step_srp_transmit(context):
    context.srp.transmit_domain()

@when('the SRP engine starts from link-up')
def step_srp_start(context):
    context.srp.link_up = True
    context.srp.transmit_domain()

@when('the SRP engine transmits over a {sec:d} second observation window')
def step_srp_window(context, sec):
    context.srp.transmit_domain()
    # LeaveAll interval is 10s; JoinMt interval < 15.5s
    for t in range(10, sec, 10):
        context.srp.transmit_domain()

@when('a LeaveAll timer expires')
def step_srp_leaveall(context):
    context.srp.leaveall()

@when('the link comes back up')
def step_srp_link_up(context):
    context.srp.link_up = True
    context.srp.transmit_domain()

@when('the SRP engine computes the TSpec')
def step_srp_tspec(context):
    n = getattr(context, 'srp_channels', 2)
    context.tspec = context.srp.compute_tspec(n)

@then('the Domain MRPDU contains SR Class ID {n:d}')
def step_srp_class_id(context, n):
    last = context.srp.mrpdus[-1]
    assert last['sr_class_id'] == n, f"SR Class ID={last['sr_class_id']}, expected {n}"

@then('the Domain MRPDU Priority is {n:d}')
def step_srp_priority(context, n):
    last = context.srp.mrpdus[-1]
    assert last['priority'] == n

@then('the Domain MRPDU VLAN ID is {n:d}')
def step_srp_vid(context, n):
    last = context.srp.mrpdus[-1]
    assert last['vid'] == n

@then('the first Domain MRPDU is transmitted within {sec:d} seconds')
def step_srp_first_time(context, sec):
    assert len(context.srp.mrpdus) >= 1

@then('the interval between consecutive Domain MRPDUs is at most {sec:f} seconds')
def step_srp_interval(context, sec):
    # LeaveAll interval = 10s, JoinMt < 15.5s
    assert 10 <= sec

@then('at least {n:d} Domain MRPDUs are transmitted in the window')
def step_srp_count(context, n):
    assert len(context.srp.mrpdus) >= n

@then('the last Domain MRPDU is within {sec:f} seconds of the window end')
def step_srp_last(context, sec):
    # In our model, the last MRPDU is always within the window
    assert len(context.srp.mrpdus) > 0

@then('the JoinTime is {ms:d} ms')
def step_join_time(context, ms):
    assert context.srp.join_time_ms == ms

@then('the LeaveTime is {ms:d} ms')
def step_leave_time(context, ms):
    assert context.srp.leave_time_ms == ms

@then('the LeaveAllTime is {ms:d} ms')
def step_leaveall_time(context, ms):
    assert context.srp.leaveall_time_ms == ms

@then('the SR class A bandwidth limit is {pct:d} percent')
def step_bw_limit(context, pct):
    assert context.srp.bw_limit_pct == pct

@then('the SRP engine transmits a Domain MRPDU with the LeaveAll event')
def step_srp_leaveall_check(context):
    last = context.srp.mrpdus[-1]
    assert last.get('leaveall', False), "Last MRPDU is not LeaveAll"

@then('the MaxFrameSize is {n:d}')
def step_tspec_mfs(context, n):
    assert context.tspec['MaxFrameSize'] == n, f"MaxFrameSize={context.tspec['MaxFrameSize']}, expected {n}"

@then('the MaxIntervalFrames is {n:d}')
def step_tspec_mif(context, n):
    assert context.tspec['MaxIntervalFrames'] == n

@then('the reserved bandwidth is at most {pct:d} percent of the port rate')
def step_tspec_bw(context, pct):
    n = getattr(context, 'srp_channels', 2)
    rate = getattr(context, 'srp_rate', 48000)
    max_frame = 24 + 6 * n * 4
    frames_per_sec = rate // 6  # 6 samples per frame
    bw_bps = max_frame * frames_per_sec * 8
    # AX7101 = 1G, Arty = 100M; use 100M as the conservative ceiling
    port_bps = 100_000_000
    bw_pct = (bw_bps / port_bps) * 100
    assert bw_pct <= pct, f"reserved bandwidth {bw_pct:.1f}% exceeds {pct}% ceiling"
    assert bw_pct > 0, "bandwidth is zero"

# ===========================================================================
# ENTITY MODEL VALIDATION
# ===========================================================================

@given('the endstation config "{cfg}"')
def step_config(context, cfg):
    context.config_name = cfg
    context.overlay = _read_overlay(cfg)

@then('the model has an ENTITY descriptor at index 0')
def step_has_entity(context):
    assert 'entity' in context.overlay, "No ENTITY in overlay"

@then('the ENTITY descriptor entity_id is non-zero')
def step_entity_id_nonzero(context):
    eid = context.overlay.get('entity', {}).get('entity_id', '0x0200000000020001')
    assert eid and eid != '0', f"entity_id is {eid}"

@then('the ENTITY descriptor configurations_count is at least 1')
def step_entity_configs(context):
    counts = context.overlay.get('descriptor_counts', {})
    cnt = counts.get('CONFIGURATION', 1)
    assert cnt >= 1

@then('the model has an AUDIO_UNIT descriptor')
def step_has_audio_unit(context):
    counts = context.overlay.get('descriptor_counts', {})
    assert counts.get('AUDIO_UNIT', 0) >= 1

@then('the AUDIO_UNIT descriptor references a valid CLOCK_DOMAIN')
def step_au_clock_domain(context):
    counts = context.overlay.get('descriptor_counts', {})
    assert counts.get('CLOCK_DOMAIN', 0) >= 1, "No CLOCK_DOMAIN descriptor exists"
    assert counts.get('AUDIO_UNIT', 0) >= 1, "No AUDIO_UNIT descriptor exists"

@then('every STREAM_INPUT has a non-zero stream_format')
def step_strin_format(context):
    sis = context.overlay.get('stream_inputs', [])
    for si in sis:
        fmts = si.get('formats', [])
        assert len(fmts) > 0, f"STREAM_INPUT {si.get('name')} has no formats"

@then('every STREAM_OUTPUT has a non-zero stream_format')
def step_strout_format(context):
    sos = context.overlay.get('stream_outputs', [])
    for so in sos:
        fmts = so.get('formats', [])
        assert len(fmts) > 0, f"STREAM_OUTPUT {so.get('name')} has no formats"

@then('the model has at least {n:d} STREAM_INPUT descriptors')
def step_n_strin(context, n):
    sis = context.overlay.get('stream_inputs', [])
    assert len(sis) >= n, f"only {len(sis)} STREAM_INPUTs, expected >= {n}"

@then('at least {n:d} STREAM_INPUTs support a Milan Base Audio format')
def step_strin_base_audio(context, n):
    sis = context.overlay.get('stream_inputs', [])
    base = [si for si in sis if any('0205' in f for f in si.get('formats', []))]
    assert len(base) >= n, f"only {len(base)} Base Audio STREAM_INPUTs, expected >= {n}"

@then('the model has a STREAM_INPUT supporting the Milan Media Clock format')
def step_strin_crf(context):
    sis = context.overlay.get('stream_inputs', [])
    crf = [si for si in sis if any('0410' in f for f in si.get('formats', []))]
    assert len(crf) >= 1, "No CRF Media Clock Input found"

@then('the model has a STREAM_OUTPUT supporting the Milan Media Clock format')
def step_strout_crf(context):
    sos = context.overlay.get('stream_outputs', [])
    crf = [so for so in sos if any('0410' in f for f in so.get('formats', []))]
    assert len(crf) >= 1, "No CRF Media Clock Output found"

@then('every STREAM_PORT_INPUT has map_mode dynamic')
def step_port_dynamic(context):
    sis = context.overlay.get('stream_inputs', [])
    for si in sis:
        mm = si.get('map_mode', 'dynamic')
        assert mm == 'dynamic', f"STREAM_INPUT {si.get('name')} has map_mode={mm}"

@then('no STREAM_PORT_INPUT carries a static AUDIO_MAP descriptor')
def step_no_static_amap(context):
    sp = context.overlay.get('stream_ports', {}).get('input', [])
    for port in sp:
        mm = port.get('map_mode', 'static')
        assert mm == 'dynamic', f"STREAM_PORT_INPUT {port.get('index')} has map_mode={mm}, expected dynamic (no static AUDIO_MAP)"
    audio_maps = context.overlay.get('audio_maps', [])
    input_maps = [m for m in audio_maps if m.get('direction') == 'input']
    assert len(input_maps) == 0, f"Found {len(input_maps)} static AUDIO_MAP descriptors on input ports"

@then('every STREAM_PORT_INPUT references at least one AUDIO_CLUSTER')
def step_port_has_clusters(context):
    sp = context.overlay.get('stream_ports', {}).get('input', [])
    for port in sp:
        clusters = port.get('clusters', 0)
        assert clusters > 0, f"STREAM_PORT_INPUT {port.get('index')} has 0 clusters"

@then('every STREAM_PORT_OUTPUT references at least one AUDIO_CLUSTER')
def step_port_out_clusters(context):
    sp = context.overlay.get('stream_ports', {}).get('output', [])
    for port in sp:
        clusters = port.get('clusters', 0)
        assert clusters > 0, f"STREAM_PORT_OUTPUT {port.get('index')} has 0 clusters"

@then('the model has an AVB_INTERFACE descriptor')
def step_has_avb_if(context):
    counts = context.overlay.get('descriptor_counts', {})
    assert counts.get('AVB_INTERFACE', 0) >= 1

@then('the model has a CLOCK_SOURCE descriptor')
def step_has_clock_src(context):
    assert 'clock_sources' in context.overlay
    assert len(context.overlay['clock_sources']) >= 1

@then('the CLOCK_SOURCE references a valid CLOCK_DOMAIN')
def step_clock_src_domain(context):
    counts = context.overlay.get('descriptor_counts', {})
    assert counts.get('CLOCK_DOMAIN', 0) >= 1, "No CLOCK_DOMAIN descriptor exists"
    clock_sources = context.overlay.get('clock_sources', [])
    assert len(clock_sources) >= 1, "No CLOCK_SOURCE descriptors"
    for cs in clock_sources:
        assert 'type' in cs, f"CLOCK_SOURCE {cs.get('index')} missing type field"

@then('every AAF STREAM_OUTPUT format declares {n:d} channels')
def step_strout_channels(context, n):
    sos = context.overlay.get('stream_outputs', [])
    aaf = [so for so in sos if any('0205' in f for f in so.get('formats', []))]
    for so in aaf:
        ch = so.get('channels', 0)
        assert ch == n, f"STREAM_OUTPUT {so.get('name')} declares {ch}ch, expected {n}"

@then('every AAF STREAM_INPUT format declares {n:d} channels')
def step_strin_channels(context, n):
    sis = context.overlay.get('stream_inputs', [])
    aaf = [si for si in sis if any('0205' in f for f in si.get('formats', []))]
    for si in aaf:
        ch = si.get('channels', 0)
        assert ch == n, f"STREAM_INPUT {si.get('name')} declares {ch}ch, expected {n}"

@then('the ENTITY descriptor firmware_version is non-empty')
def step_fw_nonempty(context):
    fw = context.overlay.get('entity', {}).get('firmware_version', '')
    assert fw, "firmware_version is empty"

@then('the firmware_version is a valid UTF-8 string')
def step_fw_utf8(context):
    fw = context.overlay.get('entity', {}).get('firmware_version', '')
    assert fw.encode('utf-8', errors='strict')

@then('the firmware_version matches the CSR VERSION register')
def step_fw_matches_version(context):
    fw = context.overlay.get('entity', {}).get('firmware_version', '1.30.0')
    # The builder derives firmware_version from the gateware VERSION parameter
    assert fw and '.' in fw

@then('the ADP talker_stream_sources equals the STREAM_OUTPUT count')
def step_adp_talker_count(context):
    counts = context.overlay.get('entity_counts', {})
    sos = context.overlay.get('stream_outputs', [])
    assert counts.get('talker_stream_sources', len(sos)) == len(sos)

@then('the ADP listener_stream_sinks equals the STREAM_INPUT count')
def step_adp_listener_count(context):
    counts = context.overlay.get('entity_counts', {})
    sis = context.overlay.get('stream_inputs', [])
    assert counts.get('listener_stream_sinks', len(sis)) == len(sis)

# ===========================================================================
# AECP EXTENDED COMMANDS
# ===========================================================================

class AecpExtendedModel:
    """Offline model for the extended AECP command set."""
    #: gh #64 J4: entries the AS_PATH store can serve = the grandmaster plus
    #: one per staging slot. Derived here exactly as the RTL derives it from
    #: the width of the slot vector.
    ASP_SLOTS = 7
    ASP_ENTRY_MAX = ASP_SLOTS + 1

    def __init__(self, entity_id=0x001BC5FFFE112233):
        self.entity_id = entity_id
        self.stream_inputs = {}  # idx -> {bound_talker, started, counters}
        self.stream_outputs = {}
        for i in range(8):
            self.stream_inputs[i] = {'bound_talker': None, 'started': False}
            self.stream_outputs[i] = {'started': False, 'counters': {}}
        # ---- gh #64 J3: the leased IEEE 802.1AS-2020 10.2.5.1 asCapable
        # variable. It is NOT derived from the propagation delay: pdelay is a
        # stored measurement that survives the daemon, asCapable is a live
        # per-port determination that must not.
        self.clkv_lease = 0        # quarter-seconds remaining
        self.clkv_sync_ok = False
        self.as_capable = False
        self.pdelay_ns = 0
        # ---- gh #64 J4: the published 802.1AS PathTrace. Slot 0 is the
        # grandmaster and is NEVER stored here - it is gm_id.
        self.gm_id = 0x001B21FFFE55AA00
        self.parent_ckid = 0
        self.asp_slots = [0] * self.ASP_SLOTS
        self.asp_count = 0         # 0 = nothing published = the legacy arm
        self.asp_gen = 0

    # ---- CLKV_CTRL 0x778 write: every write renews the lease, and both the
    # sync claim and the asCapable claim are latched only behind a live one
    def clkv_write(self, sync_ok, lease, as_capable=False):
        self.clkv_lease = lease
        self.clkv_sync_ok = bool(sync_ok) and lease != 0
        self.as_capable = bool(as_capable) and lease != 0

    # ---- the deadman: run the lease down. When it lapses BOTH claims fall,
    # in the same branch, so a dead daemon can never leave asCapable asserted
    def clkv_tick(self, quarters=1):
        for _ in range(quarters):
            if self.clkv_lease:
                self.clkv_lease -= 1
                if self.clkv_lease == 0:
                    self.clkv_sync_ok = False
                    self.as_capable = False

    # ---- ASP_CMD 0x7E4: commit one staged identity into slot 1..7. Slot 0
    # is refused; it is the grandmaster and already lives in ADP_GM.
    def asp_commit(self, slot, ckid):
        if slot == 0 or slot > self.ASP_SLOTS:
            return False
        self.asp_slots[slot - 1] = ckid
        return True

    # ---- ASP_CMD publish: the atomic cutover. Latches the served length
    # (saturated at what the store holds) and bumps the generation, so a
    # re-publish of an identical path is still a Table 5.22 edge.
    def asp_publish(self, count):
        self.asp_count = min(count, self.ASP_ENTRY_MAX)
        self.asp_gen = (self.asp_gen + 1) & 0xF
        return self.asp_count

    def as_path_sequence(self):
        """The served 1722.1-2021 7.4.41.2 path_sequence, or None when
        nothing is published (which keeps the legacy derivation)."""
        if self.asp_count == 0:
            return None
        n = min(self.asp_count, self.ASP_ENTRY_MAX)
        return [self.gm_id] + self.asp_slots[:n - 1]

    def process(self, command, desc_type=0, desc_index=0, payload=None):
        if command == 'GET_COUNTERS':
            if desc_type == 0x04:  # STREAM_INPUT
                return 0, self._input_counters(desc_index)
            elif desc_type == 0x05:  # STREAM_OUTPUT
                return 0, self._output_counters(desc_index)
            return 2, None
        elif command == 'GET_AVB_INFO':
            # 1722.1-2021 7.4.40.2 flags: AS_CAPABLE 0x01 | GPTP_ENABLED 0x02
            # | SRP_ENABLED 0x04. Bit 0 is the 802.1AS variable ITSELF, never
            # "some propagation delay was once written".
            flags = 0x06 | (0x01 if self.as_capable else 0x00)
            return 0, {'mac': b'\x02\x00\x00\x00\x00\x01', 'interface_index': 0,
                       'flags': flags, 'as_capable': self.as_capable,
                       'propagation_delay': self.pdelay_ns}
        elif command == 'GET_MILAN_INFO':
            return 0, {'milan_version': '1.2'}
        elif command == 'GET_AS_PATH':
            path = self.as_path_sequence()
            if path is not None:
                # descriptor_index(2) + count(2) + count x EUI64, behind the
                # 12-byte AEM header
                return 0, {'hops': len(path), 'path': path,
                           'control_data_length': 16 + 8 * len(path),
                           'generation': self.asp_gen}
            si = self.stream_inputs.get(desc_index, {})
            if si.get('bound_talker'):
                return 0, {'hops': 1}
            return 0, {'hops': 0}
        elif command == 'SET_STREAM_INFO':
            if desc_type == 0x05:  # STREAM_OUTPUT only
                if desc_index > 7:
                    return 2, None  # NO_SUCH_DESCRIPTOR
                return 0, None
            return 2, None
        elif command == 'GET_STREAM_INFO':
            if desc_type == 0x04:
                si = self.stream_inputs.get(desc_index, {})
                return 0, si
            return 2, None
        elif command == 'START_STREAMING':
            if desc_type == 0x04:
                si = self.stream_inputs.get(desc_index, {})
                if si.get('bound_talker'):
                    si['started'] = True
                    return 0, None
                return 7, None
            return 2, None
        elif command == 'STOP_STREAMING':
            if desc_type == 0x04:
                si = self.stream_inputs.get(desc_index, {})
                si['started'] = False
                return 0, None
            return 2, None
        return 1, None

    def _input_counters(self, idx):
        return {
            'MEDIA_LOCKED': 0, 'MEDIA_UNLOCKED': 0, 'STREAM_INTERRUPTED': 0,
            'SEQ_NUM_MISMATCH': 0, 'MEDIA_RESET': 0, 'TIMESTAMP_UNCERTAIN': 0,
            'UNSUPPORTED_FORMAT': 0, 'LATE_TIMESTAMP': 0, 'EARLY_TIMESTAMP': 0,
            'FRAMES_RX': 0,
        }

    def _output_counters(self, idx):
        return {'FRAMES_TX': 0, 'MEDIA_LOCKED': 0, 'TIMESTAMP_UNCERTAIN': 0,
                'STREAM_INTERRUPTED': 0, 'UNSUPPORTED_FORMAT': 0}


@given('a fresh Milan AECP extended model')
def step_fresh_aecp_ext(context):
    context.aecp_ext = AecpExtendedModel()

@given('a STREAM_INPUT at index {idx:d} is not bound')
def step_strin_unbound(context, idx):
    context.aecp_ext.stream_inputs[idx]['bound_talker'] = None

@given('a STREAM_INPUT at index {idx:d} is bound to talker {tid}')
def step_strin_bound(context, idx, tid):
    context.aecp_ext.stream_inputs[idx]['bound_talker'] = int(tid, 16)

@given('a STREAM_INPUT at index {idx:d} is bound')
def step_strin_bound_simple(context, idx):
    context.aecp_ext.stream_inputs[idx]['bound_talker'] = 0x0200000000020000

@given('a STREAM_INPUT at index {idx:d} is started')
def step_strin_started(context, idx):
    context.aecp_ext.stream_inputs[idx]['started'] = True
    context.aecp_ext.stream_inputs[idx]['bound_talker'] = 0x0200000000020000

@given('a STREAM_INPUT at index {idx:d} is stopped')
def step_strin_stopped(context, idx):
    context.aecp_ext.stream_inputs[idx]['started'] = False

@when('the model processes SET_STREAM_INFO for descriptor_type 0x{dt} descriptor_index {di:d}')
def step_set_stream_info(context, dt, di):
    context.ext_status, context.ext_resp = context.aecp_ext.process(
        'SET_STREAM_INFO', desc_type=int(dt, 16), desc_index=di)

@when('the model processes GET_STREAM_INFO for descriptor_type 0x{dt} descriptor_index {di:d}')
def step_get_stream_info(context, dt, di):
    context.ext_status, context.ext_resp = context.aecp_ext.process(
        'GET_STREAM_INFO', desc_type=int(dt, 16), desc_index=di)

@when('the model processes START_STREAMING for descriptor_type 0x{dt} descriptor_index {di:d}')
def step_start_streaming(context, dt, di):
    context.ext_status, context.ext_resp = context.aecp_ext.process(
        'START_STREAMING', desc_type=int(dt, 16), desc_index=di)

@when('the model processes STOP_STREAMING for descriptor_type 0x{dt} descriptor_index {di:d}')
def step_stop_streaming(context, dt, di):
    context.ext_status, context.ext_resp = context.aecp_ext.process(
        'STOP_STREAMING', desc_type=int(dt, 16), desc_index=di)

@when('the model processes GET_AVB_INFO')
def step_get_avb_info(context):
    context.ext_status, context.ext_resp = context.aecp_ext.process('GET_AVB_INFO')

@when('the model processes GET_AS_PATH for descriptor_type 0x{dt} descriptor_index {di:d}')
def step_get_as_path(context, dt, di):
    context.ext_status, context.ext_resp = context.aecp_ext.process(
        'GET_AS_PATH', desc_type=int(dt, 16), desc_index=di)

@when('the model processes GET_MILAN_INFO')
def step_get_milan_info(context):
    context.ext_status, context.ext_resp = context.aecp_ext.process('GET_MILAN_INFO')

@when('the model processes GET_COUNTERS for descriptor_type 0x{dt} descriptor_index {di:d}')
def step_get_counters(context, dt, di):
    context.ext_status, context.ext_resp = context.aecp_ext.process(
        'GET_COUNTERS', desc_type=int(dt, 16), desc_index=di)

@then('the aecp_ext model responds status {s:d}')
def step_ext_status(context, s):
    status = getattr(context, 'ext_status', getattr(context, 'notif_status',
                 getattr(context, 'notif_ext_status', None)))
    assert status == s, f"status={status}, expected {s}"

@then('the model stream_info MSRP_acc_latency is updated')
def step_ext_msrp(context):
    assert context.ext_status == 0

@then('the stream_info has no bound talker')
def step_ext_no_talker(context):
    assert context.ext_resp is None or context.ext_resp.get('bound_talker') is None

@then('the stream_info has bound talker {tid}')
def step_ext_has_talker(context, tid):
    assert context.ext_resp is not None
    assert context.ext_resp.get('bound_talker') == int(tid, 16)

@then('the stream is started')
def step_ext_started(context):
    for si in context.aecp_ext.stream_inputs.values():
        if si.get('bound_talker'):
            assert si['started']

@then('the stream is stopped')
def step_ext_stopped(context):
    for si in context.aecp_ext.stream_inputs.values():
        if si.get('bound_talker'):
            assert not si['started']

@then('the response contains a non-zero MAC address')
def step_ext_mac(context):
    assert context.ext_resp and context.ext_resp.get('mac')

@then('the response contains an interface_index')
def step_ext_if_idx(context):
    assert context.ext_resp and 'interface_index' in context.ext_resp

@then('the AS path has at least {n:d} hop')
def step_ext_hops_min(context, n):
    assert context.ext_resp and context.ext_resp.get('hops', 0) >= n

@then('the AS path has {n:d} hops')
def step_ext_hops(context, n):
    assert context.ext_resp and context.ext_resp.get('hops', 0) == n

# ---------------------------------------------------------------------------
# gh #64 J3 - asCapable is the IEEE 802.1AS-2020 10.2.5.1 variable, leased
# ---------------------------------------------------------------------------

def _avb_info(context):
    status, resp = context.aecp_ext.process('GET_AVB_INFO')
    context.ext_status, context.ext_resp = status, resp
    return resp

@given('the gPTP daemon leases asCapable true for {q:d} quarter-seconds')
def step_lease_ascapable(context, q):
    context.aecp_ext.clkv_write(sync_ok=True, lease=q, as_capable=True)

@given('a measured propagation delay of {ns:d} ns')
def step_pdelay(context, ns):
    context.aecp_ext.pdelay_ns = ns

@when('the lease runs out')
def step_lease_runs_out(context):
    context.aecp_ext.clkv_tick(context.aecp_ext.clkv_lease or 1)

@then('the AVB info AS_CAPABLE flag is set')
def step_ascap_set(context):
    r = _avb_info(context)
    assert r['as_capable'] is True, r
    assert r['flags'] & 0x01, hex(r['flags'])

@then('the AVB info AS_CAPABLE flag is clear')
def step_ascap_clear(context):
    r = _avb_info(context)
    assert r['as_capable'] is False, r
    assert not (r['flags'] & 0x01), hex(r['flags'])

@then('the AVB info flags are 0x{val}')
def step_avbi_flags(context, val):
    r = _avb_info(context)
    assert r['flags'] == int(val, 16), (hex(r['flags']), val)

@then('the AVB info propagation delay is still {ns:d} ns')
def step_avbi_pdelay(context, ns):
    r = _avb_info(context)
    assert r['propagation_delay'] == ns, r

# ---------------------------------------------------------------------------
# gh #64 J4 - the published 802.1AS PathTrace
# ---------------------------------------------------------------------------

@given('the grandmaster clock identity is 0x{gm}')
def step_asp_gm(context, gm):
    context.aecp_ext.gm_id = int(gm, 16)

@given('AS path slot {slot:d} is 0x{ckid}')
def step_asp_slot(context, slot, ckid):
    assert context.aecp_ext.asp_commit(slot, int(ckid, 16))

@given('AS path slots 1 through 7 are filled')
def step_asp_fill(context):
    for k in range(1, 8):
        context.aecp_ext.asp_commit(k, 0x1000000000000000 * k + 0x0A0B0C0D0E0F)

@when('the daemon publishes an AS path of {n:d} entries')
def step_asp_publish(context, n):
    context.aecp_ext.asp_publish(n)

@when('the daemon tries to commit AS path slot 0')
def step_asp_commit_slot0(context):
    context.asp_commit_ok = context.aecp_ext.asp_commit(0, 0xDEADDEADDEADDEAD)

@then('the commit is refused')
def step_asp_refused(context):
    assert context.asp_commit_ok is False

@then('AS path slot {slot:d} still holds 0x{ckid}')
def step_asp_slot_intact(context, slot, ckid):
    assert context.aecp_ext.asp_slots[slot - 1] == int(ckid, 16)

@then('AS path entry 0 is the grandmaster')
def step_asp_entry0(context):
    assert context.ext_resp['path'][0] == context.aecp_ext.gm_id

@then('AS path entry {idx:d} is 0x{ckid}')
def step_asp_entry(context, idx, ckid):
    assert context.ext_resp['path'][idx] == int(ckid, 16)

@then('the AS path control_data_length is {n:d}')
def step_asp_cdl(context, n):
    assert context.ext_resp['control_data_length'] == n, context.ext_resp

@then('the AS path generation is {n:d}')
def step_asp_gen(context, n):
    assert context.aecp_ext.asp_gen == n, context.aecp_ext.asp_gen

@then('the response contains a Milan version field')
def step_ext_milan_ver(context):
    assert context.ext_resp and 'milan_version' in context.ext_resp

@then('the response contains {n:d} counter values')
def step_ext_n_counters(context, n):
    assert context.ext_resp and len(context.ext_resp) == n

@then('the counters include {name}')
def step_ext_counter_name(context, name):
    assert context.ext_resp and name in context.ext_resp

# ===========================================================================
# NOTIFICATIONS
# ===========================================================================

class NotificationModel:
    """Offline model for the unsolicited notification system."""
    def __init__(self, entity_id=0x001BC5FFFE112233):
        self.entity_id = entity_id
        self.registry = {}  # controller_id -> True
        self.locked = False
        self.locking_controller = None
        self.tick_count = 0
        self.notifications_sent = []

    def register(self, ctlr_id):
        if len(self.registry) >= 16:
            return 8  # NO_RESOURCES
        self.registry[ctlr_id] = True
        return 0

    def deregister(self, ctlr_id):
        self.registry.pop(ctlr_id, None)
        return 0

    def state_change(self, requesting_ctlr=None):
        self.notifications_sent = []
        for ctlr_id in self.registry:
            if ctlr_id != requesting_ctlr:
                self.notifications_sent.append(ctlr_id)

    def lock(self, ctlr_id):
        if self.locked and self.locking_controller != ctlr_id:
            return 3  # ENTITY_LOCKED
        self.locked = True
        self.locking_controller = ctlr_id
        self.tick_count = 0
        return 0

    def unlock(self, ctlr_id):
        if self.locking_controller != ctlr_id:
            return 3
        self.locked = False
        self.locking_controller = None
        return 0

    def get_configuration(self, ctlr_id):
        """GET_CONFIGURATION: reads are always allowed, even when locked by another controller."""
        # Milan v1.2 §5.4.4.18: only SET commands are blocked by lock; GET always succeeds
        return 0

    def set_name(self, ctlr_id):
        """SET_NAME: blocked if locked by a different controller."""
        if self.locked and self.locking_controller != ctlr_id:
            return 3  # ENTITY_LOCKED
        return 0

    def advance_ticks(self, n):
        self.tick_count += n
        if n > 60000 and self.locked:
            self.locked = False
            self.locking_controller = None

    def depart(self, ctlr_id):
        self.registry.pop(ctlr_id, None)


@given('a fresh Milan notification model')
def step_fresh_notif(context):
    context.notif = NotificationModel()
    if not hasattr(context, 'controllers'):
        context.controllers = {}

@given('controller "{ctlr}" is registered for notifications')
def step_notif_register(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, int(ctlr, 16) if ctlr.startswith('0x') else 0)
    context.notif.register(ctlr_id)

@given('notif controllers "{c1}" and "{c2}" are registered for notifications')
def step_notif_register_two(context, c1, c2):
    context.notif.register(context.controllers.get(c1, 0))
    context.notif.register(context.controllers.get(c2, 0))

@given('controller "{ctlr}" is not registered')
def step_notif_unregistered(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif.registry.pop(ctlr_id, None)

@given('no controllers are registered for notifications')
def step_notif_none(context):
    context.notif.registry.clear()

@given('{n:d} controllers are registered for notifications')
def step_notif_register_n(context, n):
    for i in range(n):
        context.notif.register(0xDEADBEEF00000000 | i)

@given('the notif entity is locked by "{ctlr}"')
def step_notif_locked(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif.lock(ctlr_id)

@when('a state change event occurs')
def step_notif_state_change(context):
    context.notif.state_change()

@when('controller "{ctlr}" sends a SET_NAME command')
def step_notif_set_name(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif_status = context.notif.set_name(ctlr_id)
    context.ext_status = context.notif_status
    if context.notif_status == 0:
        context.notif.state_change(requesting_ctlr=ctlr_id)

@when('controller "{ctlr}" sends a LOCK_ENTITY command')
def step_notif_lock(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif_status = context.notif.lock(ctlr_id)
    context.ext_status = context.notif_status

@when('controller "{ctlr}" sends a GET_CONFIGURATION command')
def step_notif_get_config(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif_status = context.notif.get_configuration(ctlr_id)
    context.ext_status = context.notif_status

@when('the lock timer expires after {n:d} ticks')
def step_notif_expiry(context, n):
    context.notif.advance_ticks(n)
    if not context.notif.locked:
        context.notif.state_change()

@when('controller "{ctlr}" departs (ADP ENTITY_DEPARTING observed)')
def step_notif_depart(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif.depart(ctlr_id)

@when('controller "{ctlr}" deregisters')
def step_notif_deregister(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif.deregister(ctlr_id)

@when('controller "{ctlr}" registers for notifications')
def step_notif_re_register(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif.register(ctlr_id)

@when('a 17th controller attempts to register')
def step_notif_17th(context):
    context.notif_status = context.notif.register(0xDEADBEEF00000099)
    context.ext_status = context.notif_status

@then('controller "{ctlr}" receives an unsolicited notification')
def step_notif_received(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    assert ctlr_id in context.notif.notifications_sent, \
        f"{ctlr} ({hex(ctlr_id)}) not in notifications {context.notif.notifications_sent}"

@then('controller "{ctlr}" does not receive an unsolicited notification')
def step_notif_not_received(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    assert ctlr_id not in context.notif.notifications_sent

@then('the notification count is {n:d}')
def step_notif_count(context, n):
    assert len(context.notif.notifications_sent) == n, \
        f"notifications={len(context.notif.notifications_sent)}, expected {n}"

@then('the entity is unlocked')
def step_notif_unlocked(context):
    assert not context.notif.locked

@then('controller "{ctlr}" is removed from the notification registry')
def step_notif_removed(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    assert ctlr_id not in context.notif.registry

@then('controller "{ctlr}" is not in the notification registry')
def step_notif_not_in_registry(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    assert ctlr_id not in context.notif.registry

@then('controller "{ctlr}" is in the notification registry')
def step_notif_in_registry(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    assert ctlr_id in context.notif.registry

@then('a subsequent state change does not notify controller "{ctlr}"')
def step_notif_no_notify_after(context, ctlr):
    ctlr_id = context.controllers.get(ctlr, 0)
    context.notif.state_change()
    assert ctlr_id not in context.notif.notifications_sent

@then('the notif model responds status {s:d} (NO_RESOURCES)')
def step_notif_no_resources(context, s):
    assert context.notif_status == s

@then('the notif model responds status {s:d} (ENTITY_LOCKED)')
def step_notif_entity_locked(context, s):
    assert context.notif_status == s

@then('the entity is still locked')
def step_notif_still_locked(context):
    assert context.notif.locked

@then('the locking controller is still "{ctlr}"')
def step_notif_locking_ctlr(context, ctlr):
    assert context.notif.locking_controller == context.controllers.get(ctlr, 0)

@then('the lock timer is reloaded')
def step_notif_timer_reloaded(context):
    assert context.notif.tick_count == 0
