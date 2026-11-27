#!/usr/bin/env python3
"""Reviewer falsification probes: reuse the shipped plant harness with reviewer-chosen plants.

Usage: probe_plants.py <clone>/tb/verilator/usbaudio/transport_mutations.py <harness args...>
The harness reads the clone's hdl sources and writes only under --out; sources are never edited.
"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("tm", sys.argv[1])
tm = importlib.util.module_from_spec(spec); spec.loader.exec_module(tm)
tm.PLANTS = (
 # q2: status epoch tracks the applied epoch continuously, not latched at the snapshot.
 ('q2_status_epoch_live', 'epochs', 'bridge',
  (('if (bus_ack_valid_w) applied_epoch_r <= bus_ack_epoch_w;',
    'if (bus_ack_valid_w) applied_epoch_r <= bus_ack_epoch_w; status_epoch_r <= applied_epoch_r;'),),
  'BRIDGE_SNAPSHOT_ACK_BEFORE_CAPTURE'),
 # q3: publish the epoch on any status beat instead of on the record's last beat.
 ('q3_publish_first_beat', 'epochs', 'bridge',
  (('if (status_valid_o && status_ready_i && status_last_o) published_epoch_r',
    'if (status_valid_o && status_ready_i) published_epoch_r'),),
  'BRIDGE_SNAPSHOT_ACK_BEFORE_CAPTURE'),
 # q4: the guard only holds playback while deferred; it consumes on the application cycle.
 ('q4_consume_on_apply', 'media', 'media',
  (('assign playback_ready_o = !playback_changed_w &&', 'assign playback_ready_o = !(playback_changed_w && !state_boundary_w) &&'),),
  'MEDIA_DEFERRED_FRAME_RETAINED'),
 # q6: a playback epoch change keeps the old prime, so no reprefill.
 ('q6_no_reprime', 'media', 'media',
  (('          primed_r <= 0;\n          emit_r <= 0;', '          emit_r <= 0;'),),
  'MEDIA_DEFERRED_FRAME_RETAINED'),
)
sys.argv = [sys.argv[0]] + sys.argv[2:]
raise SystemExit(tm.main())
