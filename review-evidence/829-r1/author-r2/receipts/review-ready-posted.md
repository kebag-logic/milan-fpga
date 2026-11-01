[A725c] REVIEW READY
Commit: 2d534bec9348557a9407d3024c0b199c0ebc8bce on 829-mii-gptp, round 2 of PR #831, 10 commits on 4cda0aa0 (local; the push is the manager's).
Changed: every finding and residue of R761-1 and R762-1. No RTL behaviour moves. The MII plane text and changelog pass the style gate with their facts unchanged, and the MII build's flag group satisfies the idiom ratchet at 0. The statement that GMII `ready` is a constant is corrected everywhere: it is a flop that is 1 from the first clock after reset, whose reset the observer's own covers, so no octet is held on GMII. The fragment check reads the shape's own distance, with an MII control. The PHC window arm loads on the first symbol, the timestamp point of IEEE 802.1AS-2020 11.3.9 (the earlier citation of 11.3.2 was wrong), and holds the guard's reload, with controls at 170 and 202 cycles. The bias check's name states each shape's limit. New builder gate 1h holds the datapath's shape wiring, with planted cuts.
Correction to my predecessor's REVIEW READY, comment 6561285235, which stays as posted: "14 planted controls" was the bench branch's figure at 7fa8332e. `4cda0aa0` had 10, and this head has 13. "All 126 implementation checksums" compares `4cda0aa0` with the bench branch at b474b534, key off. It does not compare this PR with `dev`; no route of `dev` exists, so the routed effect of this PR alone on the AX7101 is unknown. "The documentation gates" there meant three steps of docs.yml, and two others were red.
Validation, on this commit:
- docs.yml: 64 `run:` steps rc 0 on clean clones, from the workflow's own list; 31 hosted-only or package-install steps not run, each with its reason. A check over the workflow fails if any step has neither.
- Full sweep, four shards, no rerun: 65 of 65 suites, 2,192,435 checks, 0 in-suite failures, lifecycle test passed.
- `make -C tb/verilator/gptp_txts`: 95 of 95 in each of 3 runs, 13 of 13 controls caught.
- `cd tests && behave`: 508 scenarios, 0 failed. `lint_rtl.py --check --self-test`: PASS, 89 at ratchet 89. Both builder legs rc 0, as docs.yml runs them and again where the SoC can elaborate. `gptp_shadow`, `gptp_plane`, `milan_dp gptp`, `gptp-lat`, `test_gptp_tx_timestamp.py`, `git diff --check` against the merge base: rc 0 each.
- Comment-only RTL shown, not asserted: preprocessed RTL, converted plane and exported AX7101 SoC top with comments removed are byte-identical to `4cda0aa0`'s, so no route was repeated.
- Not run: hosted workflows and the local replica, which need the pushed head; rtl-fast's Yosys elaboration, publication census and firmware jobs; candidate merge validation.
Acceptance criteria:
- Root cause in simulation at MII byte timing, failing signal named: met, as reported at `4cda0aa0`, and reproduced by both reviews.
- Fix with a regression test that fails without it, GMII behaviour unchanged: met. The observer takes a real `ready` flop on GMII, which never held an octet in either review's full GMII run. The netlist is not shown unchanged against `dev`.
- asCapable and sync to the bench grandmaster (IEEE 802.1AS-2020 11.2, 10.2): met on the bench branch through the inline tap under a compensation, as reported. Not re-run: this round changes no logic.
Open risks/questions:
- The tap-out check and the physical calibration stay owed through #583.
- AX7101 slices are 15841 of 15850 on one placement, and the routed effect of this PR alone is unmeasured.
- Two findings go to the manager, neither fixed here: queued frames leave the MII pads 480 ns apart against the 960 ns of IEEE 802.3 4.4.2, from LiteEth and predating this PR, and the bench stream was unaffected; and the `gptp_shadow` lifecycle test's cleanup deadline can expire under heavy load, on `dev` too, with its cause not established.
