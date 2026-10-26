#!/usr/bin/env python3
"""Digest the emitted release plan and extract the audio step's round-3 contract.

Usage: python3 -I plan_audit.py <plan.json> <out.json>

The plan is `torture_campaign.py --plan --areas soak,audio,power --json`.
Writes its SHA-256, size and step count, and the audio.integrity arguments
that state what a counter verdict proves.
"""
import hashlib
import json
import sys
from pathlib import Path

raw = Path(sys.argv[1]).read_bytes()
plan = json.loads(raw)
steps = plan["steps"] if isinstance(plan, dict) and "steps" in plan else plan
audio = next(step for step in steps if step["sid"] == "audio.integrity")
control = next(step for step in steps if step["sid"] == "audio.control.planted-drop")
keys = ("counter_grader", "counter_grader_required_s", "counter_classes", "qualification", "counter_limits",
        "planted_placement", "capture_start", "capture_losses", "pass_rule", "window_rule")
Path(sys.argv[2]).write_text(json.dumps({
    "plan_sha256": hashlib.sha256(raw).hexdigest(), "plan_bytes": len(raw), "steps": len(steps),
    "audio_integrity": {key: audio["args"][key] for key in keys},
    "audio_asserts": audio["asserts"],
    "control_fixture_required_s": control["args"]["fixture"]["required_s"],
}, indent=2) + "\n")
print("steps", len(steps), "sha256", hashlib.sha256(raw).hexdigest())
