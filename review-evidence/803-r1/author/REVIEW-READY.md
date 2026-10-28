[A693] REVIEW READY
Commit: fb182b19925b9ea24443d48d0e71b656de52b8ae (branch 803-adopt-gptp-f97c1803, on dev 5fcec84b; not pushed)
Changed:
- gptp-processor gitlink 55680bff -> f97c1803 (FPGA-gPTP PRs 92 and 93). The engine's one port change: `pub_path_o` carries eight entries from entry 0.
- Companions applied in order, each whole with `git apply --index`, clean, no fuzz: b53944d5 (PR 92 parent test patch), then 3a3db518 (PR 93: `KL_gptp_shadow` eight-entry path, `milan_datapath` GET_AS_PATH entry 0 from the engine head per IEEE 1722.1-2021 7.4.41.2 with the Table 5.22 comparator on entry 0, REGISTER_MAP 0x7DC and CLASSES, tsn_fuzz fixtures, TEST_RESULTS.md).
- Reviewed as milan-fpga code. No RTL defect found. Fixed the statements the companions left on the retired rules: the loss page (Sync timeout by gmPresent, fifth lost response), the feature ledger's AS_PATH trigger, the milan_dp README (five intervals; the physical leg's deadline projection re-scaled), a CSR harness comment, the tsn_fuzz README tally (675).
- Pin-derived records through their generators: ROM ledger row (`gptp_ucode.hex` b21b244f, equal to the donor's image), pin table, both diagrams, 18 donor links, port census header. Adoption recorded on the pin page and the CHANGELOG.
Validation (all rc 0 at this head, each unpiped with its own log):
- Full sweep, 4 shard units: 64/64 suites, 2,191,417 checks, 0 failures, 0 timed out. Shard 2 was OOM-killed at its 10 GB cap in capture_coherence and re-run with VERILATOR_JOBS=2: 16/16.
- milan_dp gptp and gptp-lat legs 200/200 each; milan_dp_gm_steps 202; tsn_fuzz ptp 675 pass, artifact fresh; gptp_shadow 325.
- milan_dp_gptp (physical): 205 checks, 0 failures, 17.992742740 simulated s. It took 5,494 s with SUITE_TIMEOUT=14400 on this loaded host.
- rtl-fast replica: all 12 jobs success, behave 495 scenarios. Yosys 60/60 tops. RTL lint at ratchet; xvlog 0 findings. sv/C++/Python/shell idiom gates pass.
- Docs workflow under GNU Make 4.3: 44 steps, 42 run all rc 0, 2 skipped by rule. Plus the LiteX builder leg, the Markdown gates on CPython 3.12 and the no-git gates.
- Vivado 2026.1, one run at a time under the lock, against the current record: route-1x1 PASS, LUT 51,259 -> 51,740 (+481, +0.94 %, tolerance 500), WNS +0.333 ns; ooc-1x1 PASS (+17); ooc-8x8 PASS (+63).
- Against dev's own route, this adoption adds +310 LUT, +155 FF and +20 slices. The ooc moves are dev's drift: their top instantiates none of the changed RTL.
- Every new parent check fails under a planted defect: 23 (defect, suite) rows, all killed on every named check. Five parent RTL reverts, the #207 arm's control, and the donor's own planted texts for gPTP 87, 88, 89 and 90, two of them in the physical leg.
Acceptance criteria: all consumer gates rc 0: met. gPTP 87-91 close after an image passes the in-house scenarios on the test machine: outside this lane.
Open risks/questions:
1. Decision needed: `docs/design/AREA_BUDGET.md` says the next shipping-image growth needs its own owner decision (15 free slices). This head leaves 7 of 15,850. The gate passes and the 2 % STOP is not reached, so no record was rewritten.
2. The physical leg's hosted projection is now 99.0-101.6 % of its 5,400 s budget (stated in the suite README; scheduling is already a CI follow-up).
