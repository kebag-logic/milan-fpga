# R894-1 F5: the round-1 receipt index against the bytes as published at evidence commit 4ee921e6

Published blobs compared: 81 files under review-evidence/584-r1/author-r1/receipts (INDEX.md included).

Before (the index as published): three rows differ from their blobs, as R894-1 found:
- gates/builder-leg-1.json: indexed 16621 B, published 16615 B
- gates/builder-leg0.txt: indexed 50280 B, published 50272 B
- gates/builder-leg1.txt: indexed 42954 B, published 42948 B

Cause: publication normalized one path form, '<scratch><home-path>' and '<scratch><home-path>' to '<scratch><home-path>', in those three files after the index was written. No measurement, result or return code differs.

Fix: the three local copies now hold the published bytes, and round1-INDEX-corrected.md was regenerated from them (its header states the normalization).

After: 80 indexed rows checked against the published blobs: 80 match, 0 differ.
