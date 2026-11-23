# Exact target-group wire differential

All five applicable point/arm combinations of `aecp-largest-notice` have identical complete
wire-frame sequences between `dd163e41` and the tested firmware `e9627b31`. No byte is masked;
these files omit only the WIRE trace's cycle timestamp. All channels and interfaces retain
one global order. The full original logs' sizes and SHA-256 values are in `summary.json`.
The broader strict comparison also holds publication writes, probe statuses and verdicts,
transmit counts, RESULT and refusal lines equal for these five groups.

The 8x8/1if target is defined in answering-ports and declaring-outputs. Both have zero
work passes over THE SHARE at the head; strict grading and the base negative controls
are in `share/strict-regrade-e9627b31.md`.
