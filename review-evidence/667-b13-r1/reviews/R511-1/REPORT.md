[R511] POSITIVE - exact head afa4e687234b80e9474aa6dd0dc756de16a241bd

Round R511-1, external independent review of issue #667 / PR #676.
Tree: `2f113aa1eda3744db77e9ea49818ef49309b63de`.
Source base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.

This verdict approves the scoped bench findings record. It does not approve
the observed startup defect or claim that issue #667 is fixed.
No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION finding remains from this review.

The [B13 assignment](https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6009837251)
defines this lane: identity, two-hour bidirectional AAF/CRF soak, 100 two-second
talker binds, first-ten-header evidence, counter observations and restoration.
The issue body's investigation and simulation work are broader.
The [separate repair assignment](https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6011846710)
owns the RTL reproduction and fix. This PR correctly uses `Refs #667`.

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue and
public scope decisions, REQUIREMENTS.md, the architecture and time-sync
contracts, relevant register mappings, the exact diff and its one-commit
history, then the
[published evidence](https://github.com/kebag-logic/milan-fpga/tree/b2bb3c89096c8fd4712a39677bae96e5987ccbbd/review-evidence/667-b13-r1).
No private lane material or other review report informed this verdict or ledger.

Acceptance evidence:

| Assigned outcome | Examined evidence and result |
|---|---|
| Identity before action | `author/identity.json` records all four matches; `soc-readonly.json` records VERSION and AEM CRC. The serial is deliberately redacted. PASS as a recorded operator observation. |
| Two-hour bidirectional AAF and CRF soak | `run-events.jsonl`, `soak-controller-receipts.json` and 145 `soak-*-wire.json` files record four bound streams and 7203.971 seconds. All four listener/talker format pairs match. |
| Every supported DUT counter and bound peer input | Independently decoded 1,160 successful payloads in 1,305 responses. The remaining 145 are DUT ENTITY NOT_SUPPORTED. All 61 counter rows match the page. No assigned error-class count rises or decreases between samples. |
| Sampling and timing | All 145 checkpoint rows match events and the page. Maximum checkpoint interval is 55.727 seconds. Individual counter-response intervals remain below 55.710 seconds; timing-response intervals remain below 55.726 seconds. All 580 timing responses retain GM/path and asCapable. |
| Rolling captures and gaps | Checked four streams across every segment and successive overlap boundaries. All nine gap-recovery chains join identical endpoints with consecutive header sequence numbers. One missing kernel-drop statistic is disclosed; the other 734 capture receipts report zero. |
| 100 startup binds and first ten PDUs | Recomputed all 1,000 retained raw headers, 100 rows and the histogram. First-ten sequences are consecutive modulo 256, with tv=1 and tu=0. Exactly 14 cycles pair EARLY=1 with a negative first step; all LATE values are zero. |
| Two-second hold and pre-unbind attribution | All bind/unbind responses succeed. Observed holds span 2002.714-2004.055 ms. Every positive EARLY observation precedes unbind submission, with minimum lead 1900.062 ms. |
| Restore as found | Independently compared 42 effective-state observations and two inventories: 18 formats, 18 zero bindings, two sources and four map fingerprints. Console bytes match. Three successful NVM commits and the sequence advance remain explicit residual bookkeeping. Cleanup receipts record deregistration, process exit and lock release. |

[R511] PASS Conformance - `docs/findings/667_TALKER_START_BENCH.md:18`, `:176`, `:431`, `:466`; B13 assignment; REQUIREMENTS.md sections 4 and 8 - Scoped observation deliverables are supported. The report distinguishes presentation-time differences from an absolute presentation window and leaves gPTP correlation NOT RUN. It makes no seven-day release-campaign or completed-repair claim. Authority mappings were checked against repository requirements and interface documentation.

[R511] PASS RTL - exact base-to-head diff and commit `afa4e687234b80e9474aa6dd0dc756de16a241bd`; `docs/overview/ARCHITECTURE.md:57`; `docs/design/TIME_SYNC.md:644` - The only added artifact is the 503-line findings page. No RTL, firmware, clock/reset/CDC path, interface, register map, configuration, build input, test or submodule pin changes. Wording preserves fabric time ownership and does not assert a register-level root cause from uncorrelated captures.

[R511] PASS Robustness - public `author/decode_capture.py`, `check_receipts.py`, `compare_restore.py`, `run_b13.py`, `probe.cpp:568`, `overlap-recovery.json`; `receipts/offline-probes.log` - Checked signed timestamp rollover, sequence rollover, tagged/plain decoding, truncated input rejection, error-class controls, missing/duplicate/failed restoration rows and changed bindings/sources/maps. Inspected bounded waits, format readback before binding and soak stop-on-error behavior. Actual counter samples contain no decreases that could conceal an error rise through reset. Missing capture statistics remain disclosed.

[R511] PASS Tests - `audit_evidence.py`, `offline_probes.py`, `receipts/evidence-audit.log`, `receipts/offline-probes.log` - Independent arithmetic reproduces the figures. All 1,015 solicited DUT counter responses also match retained wire payloads/status, including ENTITY status 11. All 22 published adverse controls pass with only their temporary directory relocated. Additional synthetic plain/tagged captures check tap-word ordering, sequence and timestamp wraps, a negative startup jump and packet truncation. RTL reproduction belongs to the separate repair lane.

[R511] PASS Docs - `docs/findings/667_TALKER_START_BENCH.md:6`, `:35`, `:270`, `:452`, `:478`, `:495`; PR body; `receipts/checks.json` - Scope, image identity, B12 comparison, all tables, absolute-correlation limit, capture limitation and NVM residuals agree with public records. All seven listed receipt sizes and hashes match. Documentation, style, contents, em-dash, path, bare-metal and whitespace gates pass. No wording-only residue was identified.

Reviewer-owned completion ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | B13 public scope; REQUIREMENTS.md; findings page:18,176,431,466; public identity/startup/soak/restoration receipts | R511-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |
| RTL | CLEAN | Exact diff/history; architecture:57; time-sync:644; parent and required-submodule byte/index/mode audit | R511-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |
| Robustness | CLEAN | Public decoder, runner, probe, restoration comparator; overlap recovery; offline adverse/synthetic probes | R511-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |
| Tests | CLEAN | 1,000 startup headers; 1,305 counter responses; 580 timing responses; wire cross-check; 22 controls; independent scripts | R511-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |
| Docs | CLEAN | Findings page and PR body; seven receipt hashes; all documentation/whitespace gates | R511-1 | afa4e687234b80e9474aa6dd0dc756de16a241bd |

Prior-public-findings reconciliation: no earlier public review findings exist
in the fetched PR records. There are two manager review-start comments, zero
submitted reviews and zero inline review comments. Nothing needs resolution
or retention. `receipts/prior-findings.json` records the read and the preceding
report hash; the independent verdict and ledger were written first.

Reproduction uses the portable scripts in this packet. From a clean exact-head
clone, run `fetch_public.py <packet>/scratch/public`, then
`audit_evidence.py <clone> <packet>/scratch/public`,
`offline_probes.py <packet>`, and `check_tree_bytes.py <clone>` with Python.
`run_checks.py <clone> <packet> <docs-python>` runs the seven repository checks
and independent audit concurrently, waits for completion and records individual
logs and return codes. The documentation interpreter needs the repository's
pinned Markdown dependencies. There were no source edits or GitHub writes.

Real limits and pending manager duties:

- The bench image is dev `28f9666f`, seed `asl`; source review is the exact
  head above. Neither substitutes for a later merge-candidate validation.
- Identity and physical restoration are assessed through published receipts.
  Full raw captures and binaries are hash-indexed but absent from the public
  packet. This review checks retained raw headers and payloads, not every
  packet in those full captures.
- No physical calibration, tap-to-gPTP mapping, hardware rerun, release soak,
  power-cut campaign, or RTL startup reproduction was performed here.
  Physical calibration is NOT RUN. Field skips are not hardware proof.
- Full licensed standard texts were not independently obtained in this session;
  clause application was checked through repository authorities and public
  field evidence. No new full-protocol conformance conclusion is asserted.
- The manager reports passing source static/builder and native banks. Those
  banks were not repeated here. Hosted/act acceptance remains manager-owned;
  this review does not count skipped hosted contexts as executed jobs.
- The manager must publish this report and listed receipts, reconcile the
  independent review, publish/accept exact-head source evidence, validate the
  final current-dev candidate, and complete authorized merge and containment.
  Issue #667 remains open for repair and subsequent bench verification.

Final byte verification covers 1,110 parent entries and required submodule
entries: protocol-processor 558, gptp-processor 104 and verilog-axis 214.
Disk blob bytes, executable/symlink modes, stage-zero indexes and required
gitlinks match their real pinned trees. Parent status is clean.

R511-1 FINISHED
