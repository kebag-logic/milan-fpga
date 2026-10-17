[R634] R634-2 independent pass, written before the round-1 review reports were read

Head 75853d80c22893448936bd1890e782bd0a0ce642, delta 867fb945..75853d80 (docs/findings/117_AUDIO_CONTINUITY.md only).

Preliminary result of the independent pass over the delta and the published packet:

- Packet author-r2 (evidence commit 68f0200e): 447 of 447 files match published_sha256 in MANIFEST.json.
- Cold-archive inputs: all 12 hashes named on the page and in pr2/REPRODUCE.txt match.
- Every PR round 2 analysis re-run from the published tools reproduces its published output byte for byte
  (dA-transit-crf.json differs only in the masked capture names).
- Restart upper bound recomputed by an independent script (no author code): 27.511 / 33.502 / 100.725 ms,
  20 of 20 under 1 s, identical per cycle to the tool.
- The cycle driver stamps its binding-rule event with time.time() before writing the CONNECT_RX request;
  the capture reader stamps realtime after each read returns; both run on the bench host
  (restart_run_b21.sh). Realtime minus monotonic spans 29.56 us over the capture.
- No AAF packet on the peer-link tap between any CONNECT_RX command and its response, none in any hold.
- Docs gates rc 0 at the head (docs_check, doc style, TOC, em dash, doc paths, git diff --check x2).

Preliminary findings: no BLOCKER, MAJOR or MINOR.
- RESIDUE: line 667, "So the 17 losses with a shortfall" (two of the other three also have a positive
  shortfall); exact fix "So the 17 losses whose shortfall exceeds the control maximum".
- SUGGESTION: b21_floor_groups.py prints wake spacing at 0.1 s; the page's 1.02 to 1.04 s is correct
  (receipts/sampler_spacing.txt) but not printed by the published tool.

Preliminary ledger: Conformance, RTL (not applicable, no RTL in the diff), Robustness, Tests, Docs all CLEAN
at 75853d80, pending resolution of the named round-1 findings.
