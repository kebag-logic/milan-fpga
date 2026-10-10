[A589] REVIEW READY
Commit: `49b437f445e34b558106c8799c1ffc0a5dc844cf` (branch `711-lwsrp-bump`, two commits on dev `e8454e27`; not pushed: this lane may not push)
Changed:
- `third_party/lwSRP` `9197193e` to `08ee86e8`, the only lwSRP change; `ctrl_arms.py` pin check follows.
- `sw/firmware/ctrl/test/srp_latency.cpp:76-84`: the MVRP LeaveAll walk reads every VectorAttribute to the Message's EndMark (IEEE 802.1Q-2018 10.8.1.2 d; vector size per 10.8.2.8, 10.8.2.10.1), and each walk must end on the MRPDU EndMark (10.8.1.2 b, 10.8.2.9). This is the only byte-level SRP expectation the grouped layout changes. The old walk with the new assertion fails at `08ee86e8` at IF=1 and IF=2; the new walk passes at both pins.
- Re-recorded through its generator: the submodule boundary diagram and `PNG_MANIFEST.json` (`submodule_boundaries.gen.py`); the `SUBMODULES.md` ledger row is checked by `check_submodule_docs.py`. Pin prose and contract permalinks in four documents.
Validation (base `e8454e27` against head, every command rc 0, clean scratch clones):
- Firmware unit job, all six steps: 59 arms `ok` both sides, identical verdict lines; 1,191 cases; coverage 30 files at 100 %, table and denominators identical; planted defects 784 of 784 caught both sides (control 471, AECP 74, SRP 169 + 68, pin 2). F4 SRP set `ok` at IF=1 and IF=2.
- Decoded SRP behaviour: every SRP-channel frame of 28 arm executables, decoded by an independent 802.1Q 10.8 / 35.2.2 / 11.2.3.1 decoder: 4,186 MRPDUs, 2,201 byte-identical, 1,985 layout-only, 0 decoded differently; every head MRPDU is grouped. Planted-change controls fail as they should.
- Saved-state capture at the receipt's recipe: all nine `capture.log` files (six arms, three controls) byte-identical between base and head; bounds pass; `check_nvm_capture.py` rc 0.
- All-fabric shipping image: firmware ROM identical at base, head and a second base export (1x1 `a14e34e7…`, 8x8 `cf2c371f…`). `route-1x1`, base and head: LUT 50,267, FF 54,413, SLICE 15,779, RAMB36 74, RAMB18 27, DSP 14, WNS 0.299 ns, WHS 0.031 ns, fully routed; `pp_resource_gate.py check` PASS with zero delta at both. The census, utilization, timing and route-status reports are identical apart from their `Date` line.
- Gates: all 81 `docs.yml` commands; 19 rtl-fast static gates; ROM-digest generator self-tests; Yosys 58 of 58 tops; Verilator sweep 61 suites, 0 failed (2,185,848 checks); `tsn_fuzz` with the CI-pinned field oracle; `xvlog_gate.py --check` PASS.
Acceptance criteria: 1-5 met.
- 3: lwSRP is not compiled into the capture firmware, so its digest does not move; the re-measure found no difference to attribute. The receipt's existing staleness against dev is #621's (open PR #707) and is not re-recorded here.
- 5: no tracked record documents the shipping ROM digest; the digests above are now documented, measured identical at base and head.
Open risks/questions: none blocking. `act_ci.py --pr` was not run, because it needs a pushed head. The control firmware's `.text` grows by +588 linked octets (grouped encoder), with storage unchanged.
