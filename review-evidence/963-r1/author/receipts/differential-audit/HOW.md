# Interim strict observable differential

No bytes are masked. Frames retain their per-channel/interface order. Only the trace's
wall-clock/cycle timestamp columns are excluded from comparison. Each publication word's
writes, transmit counts, probe status and grading verdicts are compared too.

All five applicable `aecp-largest-notice` point/arm groups are exact. The other raw
byte differences are explicitly DIFF, not silently promoted to an exact match.
This interim snapshot precedes the complete save-window measurement.
