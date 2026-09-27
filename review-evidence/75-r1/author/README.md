[A386] Reconnect measurement packet

Refs #75. HANDOFF.md gives current state and one row per cycle.
PR-BODY.md is the prepared publication description.

Acquisition sources are under tools. Each cycle directory contains:

- result.json: live tap timing and disconnect hold;
- analysis.json: offline timing, binding checks, and sender counts;
- msrp.tsv: every decoded type, event, and listener value;
- integrity.json: tap continuity, burst bounds, and processor deltas;
- console-before.txt and console-after.txt: direct readbacks;
- snapshot-before.jsonl and snapshot-after.jsonl: controller counters;
- cycle.jsonl: disconnect and reconnect transaction responses;
- events.jsonl: recorder timestamps and action return codes;
- capture.txt: complete capture statistics;
- raw-artifacts.json: private raw capture path, bytes, and SHA-256.

Full captures remain under /tmp/a386; never copy them here.
The complete raw index is RAW-ARTIFACTS.json.
The root MANIFEST.sha256 authenticates packet-level files and
directory manifests. Each child manifest authenticates that directory.
This hierarchy keeps every retained file below 200,000 bytes.

Recompute a cycle with python3 -B tools/analyze.py listener-001.
The controller and tap endpoint arguments are site-local inputs.
The acquisition runner requires its caller to hold the bench lock.
It joins every capture child before returning.
Every numbered cycle has its own lock window.
The series stops after ten consecutive bound failures in one direction.
The initial bind is never counted as a reconnect cycle.

Recompute continuity and diagnostics with tools/integrity.py.
Generate the public page with tools/report.py.
The public page is the only repository change.
No package, environment, dependency tree, binary capture, or large file
belongs in this packet. The temporary capture driver is removed at restore.

Verify existing hashes without rewriting them: python3 -B tools/verify_packet.py.
