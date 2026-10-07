[R529] Static examination at 938497af1dffd8a87edebf3ab93663914bf85e5e

This receipt records review conclusions, not a reasoning transcript.

Conformance
- IEEE 1722-2016 B.2.1 / Figure B.1: maap.c:73-100 encodes the source/destination, subtype, message type, MAAP version, 16-byte control-data length, zero stream ID, requested range, conflict range and minimum-frame padding. maap.c:262-302 accepts the documented compatible versions and checks the relevant complete fields before use. DEFEND echoes the request and sends the intersection to the triggering source.
- Table B.7: INITIAL Begin reserves; active Begin has no protocol action. Release stops the applicable timer, discards obsolete queued output and withdraws. Restart generates and reserves. Reserve initializes three retransmissions, starts a probe timer and sends immediately. PROBE receives DEFEND/ANNOUNCE as unconditional conflicts, with reversed-MAC priority only for PROBE. DEFEND answers a conflicting PROBE; received DEFEND/ANNOUNCE uses priority. Probe expiry sends/decrements, and zero count sends ANNOUNCE after the final PROBE. Announce expiry rearms and announces. Operational-link events restart active state. Internal Restart/Reserve/probeCount actions implement their table cells without exposing synchronous callbacks.
- Table B.7 note a: maap.c:185 retains an accepted preference while down, maap.c:230 consumes it on first operational reserve, and maap.c:105 clears it before later conflict restarts. Invalid Begin does not replace it. Release followed by a fresh Begin overwrites it.
- B.3.3/B.3.4: constants and strict timer bounds agree. Test software timestamps advance to real requested timer deadlines. Parent frame timestamps expose the 500..627 ms and delayed-three-probe deltas. These deviations are explicitly tracked in #686 and comment 6029233665; the parent remains a comparison subject.
- B.3.6.1/B.3.6.4/B.4: low MAC-plus-clock seed, nonzero full-period generator, rejection sampling, six reversed octets, and final-fitting pool boundary were examined. Fixed-seed retry and each deciding octet are tested.

RTL and interfaces
- The F2-only db9aa8c9..HEAD diff changes no RTL, register definition, shipping configuration, placement glue or submodule pin. The assigned wider range includes the FC follow-up. Its classification moves to byte 15, stores subtype at byte 14, and retains the last-byte decision for a frame ending at byte 14. The four-word queue can hold bytes 0..15 before drain; the new subtype register resets with the same synchronous reset. No new clock or CDC is introduced. Generated SV/C/doc masks agree with YAML.
- ctrl_app.c:55-58 now writes RX bits for ADP and MAAP plus event enable before opening the composed channels. ctrl_loop_step and the host wait port are traversed by the wake test; servicing depends on the observed IRQ, rather than an unconditional manual service call.
- maap_mbx.c:13-33 maintains distinct timer slot/tag state; :94-115 rejects foreign interfaces and suppresses duplicate link levels; :119-127 polls every interface, even after another reports pending output. The shared range filter covers live-range envelopes; each indexed core performs exact overlap checks.
- maap_csr.c:42-69 uses the register map's offsets and packing, closes enables, disables the old allocator, writes destinations, restores stream selection, then restores the requested controls. milan_csr.sv:1834-1866 gates indexed DMAC writes on talker direction and selects the correct TCTX words. The model now implements the relevant read-only listener behavior.
- KL_pp_maap_shim.sv:82 and milan_datapath.sv:1999,5326,7066 confirm the documented allocation-to-declaration dependency. This opt-in output is not an integrated streaming path until the default-flip obligation is satisfied. No firmware-only destination write proves media quiescence.

Robustness
- Static queue bound, maximum two sends, deferred expiry, stale timer tags, integer wrap, adjacent/disjoint/zero ranges, malformed/truncated input, rejected configurations, release/link loss and no synchronous reentry were reviewed and exercised by the focused positive arms.
- Overflow is counted as failed service; delayed recovery does not restart the input budget. The focused late-TX and late-ignored-input mutations both fail their named timing checks. Interface 1's five-millisecond stall is included in the measured 5,004,400 ns elapsed time.
- Wake tests cover one/two interfaces and retain ADP/event enables. The missing-MAAP bit fails the actual wait/IRQ/service chain at both sizes. These are host-model checks, not physical WFI/interrupt hardware measurements.

Tests
- The reviewer-selected production defects operate on wake masks, reservation choice, retry choice, comparison width, CSR direction/order and interface polling. Eighteen controls were built and required to fail a named assertion; compilation failures were not counted.
- The full differential self-test independently ran its 12 positive cases and 16 controls. The new timing case tests strict endpoint predicates and actual timer-driven intervals; 1, 500 and 600 ms production mutations fail it. Wrong parent-bound and parent-count expectations fail the same named case.
- Generator drift checks and its positive/planted controls passed. The scoped RTL mailbox suite runs both bus adapters from an exact-head source export. Firmware coverage is independently measured at the final head; no ratchet or exclusion was edited.

Docs
- The README's six parent deviations agree with #686 body plus 6029233665. Its supplied-range API, IRQ composition, CSR dependency, no-callback rule, release-only object-build limit and host-time assumptions match code and executable observations.
- PR #687 repeats the integration dependency and explicitly defers the #683/#685 dev integration. Public author-r2/HANDOFF.md distinguishes final-head firmware measurements from earlier unchanged bank inputs. It supplies command/exit/hash tables; underlying author logs are not all in the public archive and were not independently hash-verified here.
- Full source-bank passes are separate from a final live-dev merge candidate. Field skips, absent vendor analysis and historical calibration NOT RUN are not hardware proof.
