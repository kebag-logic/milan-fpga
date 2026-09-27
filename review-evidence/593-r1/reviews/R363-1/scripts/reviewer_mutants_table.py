"""Survivors of reviewer_mutants.py at 95bea7cf (generated from its table)."""
SURVIVORS = [
    ('M06 MEDIA_RESET read stream filter removed', 'reads = [read for read in media_reset_reads if read["stream_id"] == stream_id]', 'reads = media_reset_reads'),
    ('M12 PDU timestamp order check removed', '                or current["timestamp_s"] < previous["timestamp_s"]):\n            return "NOT RUN", {"why": "ordered, contiguous', '                or False):\n            return "NOT RUN", {"why": "ordered, contiguous'),
    ('M13 read order check removed', 'if after["timestamp_s"] <= before["timestamp_s"]:', 'if False:'),
    ('M14 counter wrap decoding removed', 'delta = (after["value"] - before["value"]) % 2**32', 'delta = (after["value"] - before["value"])'),
    ('M15 single counter read accepted', 'if len(reads) < 2:', 'if len(reads) < 1:'),
    ('M19 counter value range unchecked', 'if type(read.get("value")) is not int or not 0 <= read["value"] < 2**32:', 'if type(read.get("value")) is not int:'),
    ('M20 cause kind type unchecked', 'if not isinstance(event.get("kind"), str):', 'if False:'),
    ('M22 MEDIA_RESET upper bound drops R', 'upper_s = Decimal(str(after["timestamp_s"])) + Decimal(str(resolution_s))', 'upper_s = Decimal(str(after["timestamp_s"]))'),
    ('M24 MEDIA_RESET consumes latest', 'for event_s in matches_s[:delta]:', 'for event_s in (matches_s[-delta:] if delta else []):'),
    ('M26 tu GM change at clear counted', 'gm_events_s = [event_s for event_s in gm_changes_s if event_s < clear_s]', 'gm_events_s = [event_s for event_s in gm_changes_s if event_s <= clear_s]'),
    ('M28 tu any holdover bound accepted', 'clear_s <= observed_start_s or holdover_bound_s != 0.5', 'clear_s <= observed_start_s or holdover_bound_s <= 0'),
    ('M29 tu zero-length interval accepted', 'clear_s <= observed_start_s or holdover_bound_s != 0.5', 'clear_s < observed_start_s or holdover_bound_s != 0.5'),
    ('M32 release evidence text drops NOT RUN', 'missing, NOT RUN, SKIP, INFO, ', 'missing, SKIP, INFO, '),
    ('M34 mr assertion drops interval counting', '"MEDIA_RESET counts observation intervals, not packets; "', '""'),
]
