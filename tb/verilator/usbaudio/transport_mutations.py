#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant transport defects and require named runtime failures of the same tests.

Each selected test first passes without a defect. Build failures, timeouts and
unrelated assertions are failures of this campaign, never caught defects.
Completed builds can be removed after their paths are durably logged.
Output directories must be new; sources, logs and verdicts are retained.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess

# name, test, source leaf, edits, named detection
PLANTS = (
 ('bridge_applied_epoch', 'epochs', 'bridge',
  (('&& applied_epoch_r == bus_capture_epoch_r && published_epoch_r == bus_capture_epoch_r',
    '&& published_epoch_r == bus_capture_epoch_r'),), 'BRIDGE_MEDIA_APPLIED_GATE'),
 ('bridge_capture_abort', 'epochs', 'bridge',
  (('assign capture_abort_o = apply_w && capture_epoch_w != bus_capture_epoch_r;',
    "assign capture_abort_o = 1'b0;"),), 'BRIDGE_CAPTURE_ABORT'),
 ('bridge_packet_fence', 'epochs', 'bridge',
  (('.fence_i(capture_abort_o)', ".fence_i(1'b0)"),),
  'BRIDGE_CAPTURE_CHANNEL_ZERO_RESTART'),
 ('bridge_status_epoch', 'epochs', 'bridge',
  (('.capture_epoch_i(applied_epoch_r)', '.capture_epoch_i(bus_capture_epoch_r)'),),
  'BRIDGE_ACK_AFTER_MEDIA_APPLY'),
 ('bridge_published_epoch', 'epochs', 'bridge',
  (('&& applied_epoch_r == bus_capture_epoch_r && published_epoch_r == bus_capture_epoch_r',
    '&& applied_epoch_r == bus_capture_epoch_r'),), 'BRIDGE_PUBLISHED_ACK_GATE'),
 ('media_grid_transition', 'media', 'media',
  (('if (media_tick_i && emit_r == 0) begin',
    'if (media_tick_i && emit_r == 0 && !playback_changed_w) begin'),),
  'MEDIA_EVERY_GRID_SNAPSHOT'),
 ('media_walk_transition', 'media', 'media',
  (('!playback_changed_w || (emit_r == 0 && !media_tick_i)', "1'b1"),),
  'MEDIA_EVERY_GRID_SNAPSHOT'),
 ('levels_clock_launch', 'levels', 'bridge',
  (('lock_r <= {lock_r[0], media_levels_r[2]};',
    'lock_r <= {lock_r[0], media_locked_i};'),), 'LEVEL_CLOCK_GLITCH'),
 ('levels_playback_launch', 'levels', 'bridge',
  (('running_meta_r <= media_levels_r[1:0];',
    'running_meta_r <= {media_running_w[1], media_levels_r[0]};'),), 'LEVEL_PLAYBACK_GLITCH'),
 ('levels_capture_launch', 'levels', 'bridge',
  (('running_meta_r <= media_levels_r[1:0];',
    'running_meta_r <= {media_levels_r[1], media_running_w[0]};'),), 'LEVEL_CAPTURE_GLITCH'),
 ('reference_magic',
  'reference',
  'ingress',
  (("data_i != 16'h5549", "1'b0"), ("reference_r[15:0] == 16'h5549", "1'b1")),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_length',
  'reference',
  'ingress',
  (('reference_r[31:16] == 20', "1'b1"),),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_version',
  'reference',
  'ingress',
  (("reference_r[47:32] == 16'h0801", 'reference_r[47:40] == 8'),),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_period',
  'reference',
  'ingress',
  (("reference_r[47:32] == 16'h0801", 'reference_r[39:32] == 1'),),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_count_reserved',
  'reference',
  'ingress',
  (('reference_r[63:62] == 0', "1'b1"),),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_count_alignment',
  'reference',
  'ingress',
  (('reference_r[50:48] == 0', "1'b1"),),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_raw_count',
  'reference',
  'ingress',
  (('reference_r[109:96] == reference_r[61:48]', "1'b1"),),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_raw_reserved',
  'reference',
  'ingress',
  (('reference_r[127:123] == 0', "1'b1"),),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_flags',
  'reference',
  'ingress',
  (('reference_r[143:129] == 0', "1'b1"),),
  'REFERENCE_FIELDS_REJECTED'),
 ('reference_digest', 'reference', 'ingress', (('data_i == DIGEST_P', "1'b1"),), 'REFERENCE_FIELDS_REJECTED'),
 ('reference_first_word',
  'reference',
  'ingress',
  (('stamp_r <= media_ticks_i', "stamp_r <= media_ticks_i+48'd512"),),
  'REFERENCE_FIRST_WORD_TIMESTAMP'),
 ('reference_sequence_gap',
  'reference',
  'reference',
  (("sequence_i == sequence_r+32'd1", "1'b1"),),
  'REFERENCE_SEQUENCE_GAP'),
 ('reference_duplicate',
  'reference',
  'reference',
  (("sequence_i == sequence_r+32'd1", "(sequence_i == sequence_r || sequence_i == sequence_r+32'd1)"),),
  'REFERENCE_SEQUENCE_DUPLICATE'),
 ('reference_count_step', 'reference', 'reference', (('count_step_w == 8', "1'b1"),), 'REFERENCE_COUNT_GAP'),
 ('reference_loss_flag',
  'reference',
  'reference',
  (('discontinuity_i || delta_i', "1'b0 || delta_i"),),
  'REFERENCE_DISCONTINUITY'),
 ('reference_watchdog_early',
  'reference',
  'reference',
  (('(BUS_HZ_P/1000)*3', 'BUS_HZ_P/500'),),
  'REFERENCE_WATCHDOG_2P9MS_ACCEPTED'),
 ('reference_watchdog_late',
  'reference',
  'reference',
  (('(BUS_HZ_P/1000)*3', '(BUS_HZ_P/1000)*3+1'),),
  'REFERENCE_WATCHDOG_3MS_REFUSED'),
 ('reference_watchdog',
  'reference',
  'reference',
  (('malformed_i || expired_w', "malformed_i || 1'b0"),),
  'REFERENCE_WATCHDOG_3MS_REFUSED'),
 ('reference_watchdog_early_output',
  'reference',
  'reference',
  (('.locked_i(healthy_r)', '.locked_i(healthy_r && !bad_w)'),),
  'REFERENCE_WATCHDOG_BEFORE_3MS'),
 ('reference_watchdog_requires_record',
  'reference',
  'reference',
  (('malformed_i || expired_w', 'malformed_i || (expired_w && reference_i)'),),
  'REFERENCE_WATCHDOG_3MS_NO_REFERENCE'),
 ('reference_early', 'reference', 'reference', (('delivery_ticks_w >= 18432', "1'b1"),), 'REFERENCE_BUNCHED'),
 ('reference_late', 'reference', 'reference', (('delivery_ticks_w <= 30720', "1'b1"),), 'REFERENCE_LATE'),
 ('reference_delta_range', 'reference', 'reference', (('delta_i >= 7500', "1'b0"),), 'REFERENCE_DELTA_RANGE'),
 ('reference_delta_units',
  'reference',
  'reference',
  (("(32'(delta_i)*256)/625", "32'd0"),),
  'REFERENCE_DELTA_UNITS'),
 ('reference_physical_bound',
  'reference',
  'reference',
  (('&& latency_qualified_i;', ';'),),
  'REFERENCE_PHYSICAL_BOUND'),
 ('reference_window_stride',
  'reference',
  'reference',
  (('.INTERVAL_LOG2_P(3)', '.INTERVAL_LOG2_P(2)'),),
  'SELECTED_REFERENCE_RATE'),
 ('media_capture_only_epoch',
  'media',
  'media',
  (('if (playback_epoch_r != state_i[34:3])',
    'if (playback_epoch_r != state_i[34:3] || capture_epoch_r != state_i[66:35])'),),
  'MEDIA_PLAYBACK_BITS'),
 ('media_partial_frame',
  'media',
  'media',
  (('render_tick_i && render_complete_r', 'render_tick_i'),),
  'MEDIA_PARTIAL_HIDDEN'),
 ('media_epoch_trailing',
  'media',
  'media',
  (('if (render_discard_r)', "if (1'b0)"),),
  'MEDIA_EPOCH_TRAILING_BEATS_CLEAN'),
 ('media_capture_low_bits',
  'media',
  'media',
  (('return {value[7:0], value[15:8], value[23:16], value[31:24]};',
    "return {value[7:0], value[15:8], value[23:16], 8'd0};"),),
  'MEDIA_CAPTURE_BITS'),
 ('media_underflow_count',
  'media',
  'media',
  (("gaps_o <= gaps_o+1'b1", 'gaps_o <= gaps_o'),),
  'MEDIA_UNDERFLOW_FRAME_COUNT'),
 ('media_overflow_count',
  'media',
  'media',
  (("if (drops_o != 32'hffffffff)", "if (drops_o != 32'hffffffff && !render_complete_r)"),),
  'MEDIA_OVERFLOW_FRAME_COUNT'),
 ('media_prefill',
  'media',
  'media',
  (("playback_level_i >= 7'(PREFILL_FRAMES_P)", 'playback_level_i >= 1'),),
  'MEDIA_PLAYBACK_BITS'),
 ('packet_stall',
  'packet',
  'packet',
  (('if (valid_o && ready_i)', 'if (valid_o)'),),
  'PACKET_STALL_POSITION'),
 ('packet_fence', 'packet', 'packet', (('if (fence_i)', "if (1'b0)"),), 'PACKET_EPOCH_ABANDON'),
 ('packet_prefill', 'packet', 'packet', (('level_i >= 12', 'level_i >= 1'),), 'PACKET_PREFILL'),
 ('packet_maximum',
  'packet',
  'packet',
  (("level_i >= 7 ? 3'd7", "level_i >= 6 ? 3'd6"),),
  'PACKET_LAST_BOUNDARY'),
 ('packet_final_word',
  'packet',
  'packet',
  (("{frames_r, 4'b0}-1'b1", "{frames_r, 4'b0}-2'd2"),),
  'PACKET_WHOLE_FRAME'),
 ('gpif_address', 'gpif', 'gpif',
  (('address_o <= next_address_w;',
    'address_o <= next_address_w == 0 ? 2 : next_address_w;'),), 'GPIF_AUDIO_ADDRESSES'),
 ('gpif_blocked_status',
  'gpif',
  'gpif',
  (('status_age_r >= BUS_HZ_P/2000 && status_turn_r', 'status_age_r >= BUS_HZ_P/2000'),),
  'GPIF_BLOCKED_STATUS_FAIRNESS'),
 ('gpif_settle', 'gpif', 'gpif', (('delay_r <= 6;', 'delay_r <= 0;'),), 'GPIF_READ_OWNERSHIP'),
 ('gpif_commit',
  'gpif',
  'gpif',
  (('pktend_n_o <= !(selected_status_w ? status_last_i : capture_last_i);', 'pktend_n_o <= 1;'),),
  'GPIF_CAPTURE_COMMIT'),
 ('gpif_reset',
  'gpif',
  'gpif',
  (('posedge clk_i or negedge rst_n_w) begin : bus_schedule', 'posedge clk_i) begin : bus_schedule'),),
  'GPIF_ASYNC_PAD_RESET'))


def main() -> int:
    """Compile each selected plant and require its named runtime finding."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--cleanup-ledger", required=True, type=Path)
    parser.add_argument("--temporary-suffix", required=True)
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--discard-builds", action="store_true")
    args = parser.parse_args()
    if args.jobs < 1 or "/" in args.temporary_suffix:
        parser.error("invalid jobs or temporary suffix")
    args.out.mkdir(parents=True, exist_ok=False)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    here = Path(__file__).resolve().parent
    originals = {p.name: p.read_text() for p in (here.parents[2] / "hdl/milan/usbaudio").glob("*.sv")}
    selected = [p for p in PLANTS if not args.only or p[0] in args.only]
    if not selected:
        parser.error("no selected plants")
    cases = [("baseline_"+test, test, "", (), "") for test in sorted({p[1] for p in selected})] + selected
    results = []
    for name, test, leaf, edits, expected in cases:
        if shutil.disk_usage(args.out).free < 19*1024**3:
            raise RuntimeError("free-space guard: campaign deferred")
        case = args.out / name
        case.mkdir()
        sources = []
        for filename, original in originals.items():
            content = original
            if filename == f"KL_usbaudio_{leaf}.sv":
                for old, new in edits:
                    required = 1
                    if content.count(old) != required:
                        raise RuntimeError(f"{name}: expected {required} plant locations")
                    content = content.replace(old, new)
            source = case / filename
            source.write_text(content)
            sources.append(str(source))
        obj = case / "build"
        top = "V"+test+"_tb"
        with args.cleanup_ledger.open("a") as ledger:
            ledger.write(f"Planned generated temporary removal: {obj / (top+args.temporary_suffix)}\n")
            ledger.flush()
            os.fsync(ledger.fileno())
        command = [args.engine, "--binary", "--timing", "--top-module", test+"_tb",
                   "-Wall", "-Wno-fatal", "-Wno-TIMESCALEMOD", "--build-jobs", str(args.jobs),
                   "--Mdir", str(obj), *sources,
                   str(here.parents[2] / "third_party/verilog-axis/rtl/axis_async_fifo.v"),
                   str(here / (test+"_tb.sv"))]
        with (case / "compile.log").open("w") as log:
            compiled = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
        result = {"plant": name, "check": expected}
        if compiled.returncode:
            result["result"] = "BUILD_FAILED"
        else:
            run = subprocess.run([str(obj/top)], text=True, capture_output=True, timeout=120, check=False)
            output = run.stdout+run.stderr
            (case / "run.log").write_text(output)
            if not expected:
                result["result"] = "PASS" if run.returncode == 0 and "PASS " in output else "BASELINE_FAILED"
            else:
                result["result"] = "CAUGHT" if run.returncode != 0 and "CHECK "+expected in output else "NOT_CAUGHT"
        results.append(result)
        (args.out/"results.json").write_text(json.dumps(results, indent=2)+"\n")
        print(json.dumps(result), flush=True)
        if args.discard_builds and obj.is_dir():
            with args.cleanup_ledger.open("a") as ledger:
                ledger.write(f"Planned completed build removal: {obj.resolve()}\n")
                ledger.flush()
                os.fsync(ledger.fileno())
            shutil.rmtree(obj)
        if not expected and result["result"] != "PASS":
            break
    return 0 if all(row["result"] in ("PASS", "CAUGHT") for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
