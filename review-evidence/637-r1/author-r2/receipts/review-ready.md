[A656] REVIEW READY
Commit: `63a187e1579474bca562d85304b9a91466877c33` (branch `637-map-records`, local, not pushed; 11 commits on dev `e9cbb676`; processor pin `2cbed0a9` unchanged)

Changed:
- `hdl/milan/KL_pp_shadow.sv`: a 2:1 arbiter on `KL_nvm_backend`'s device face, shared by the processor's NVM port and the parent's map writer. A side keeps the face while it asks, a command stays with its side until done or err, an abandoned read is drained, and an abandoned write is never padded. `pend_i` takes the map writer's dirty bits, the sticky source keeps names only, and the map alarm joins `nvm_alarm`.
- `hdl/milan/milan_datapath.sv` (`amr_*`): the writer and restore of records `0x60` + port and `0x70` + port.
  - Writer: the trigger is the actual phase-5 change, with the 500 ms first-dirty window, a one-clock latch with no edit open, taint, and the clear at the untainted WRITE's done; DR2c's three attempts 500 ms apart, then the alarm.
  - Restore: after the D3 COMPLETE terminal only. A well-formed record replaces the reset set through the existing ADD/REMOVE server (the ADD rule is the value rule). Erased, unframed, torn, corrupt or malformed records keep the default.
  - Roll-back: every map goes back to its reset set on a transport failure (20 ms per wait, 1,000 ms aggregate), and nothing is restored on `restore_rb_o`.
  - Holds: the edit face, CSR writer, GET_AUDIO_MAP, format judge and entity enable wait until the map restore ends.
- The record format is unchanged: the empty list is a framed record of UNUSED entries (D3 8.3 V3g).
- No processor register-map, top-level port or parameter change.
- `scripts/check_nvm_record_space.py` check 15 holds the parent's layout literal to the donor's `LAYOUT_VER_P`.
- `tb/verilator/milan_dp` dynmap leg `[MAPREC]`: a planted power cycle keeps the window memory across a reset, and the repository's codec frames every expected record.
- `tb/verilator/pp_shadow` P2 waits, within a bound, for the map restore's blank reads.
- Docs: SAVED_STATE_MATERIALIZATION (status, 1, 5.2, 8.4, 8.6, 10, 15 item 2, 18.4 implementation record), FASTCONNECT, SNAPSHOT_OWNERSHIP, REGISTER_MAP, MILAN_COMPLIANCE_MATRIX, TESTING, and the READMEs.

Validation (all rc 0, unpiped):
- `scripts/run_all_suites.sh` at the head: 63 of 63 suites, 2,186,578 checks, 0 failures.
- `make -C tb/verilator/milan_dp dynmap`: 331 checks, 0 failures.
- `make -C tb/verilator/milan_dp dynmap-mutants`: 37 of 37 planted controls caught, 24 of them new, each clean leg passing. The new pp_shadow check has a planted control too, caught.
- `syn/yosys/run.sh`: 58 of 58 tops. `scripts/xvlog_gate.py --check` and `--selftest`: rc 0, 0.
- `scripts/lint_rtl.py --check --self-test` and the docs, record-space (`--self-test`: 22 controls), capture and rtl-fast self-test gates.
- route-1x1: LUT +289, FF +262 (DR4 maps ceiling 1,250 / 600), WNS +0.215 -> +0.316 ns, WHS +0.036 -> +0.015 ns, route complete.
- ooc-1x1: LUT +52, FF +2. ooc-8x8: LUT +71, FF 0. Every base equals the accepted record.

Acceptance criteria:
- Item 1: met. One read pass instead of the processor's two; reasoning in D3 18.4.
- Item 2: met. The processor's `07_memory_maps.md` 5.1 at the pin already matches.
- Item 3: met (empty, saved and torn cases).
- Item 4: met, census and timing unchanged (`check_nvm_capture.py`).
- #763: the EMPTY list in both directions and a non-empty non-default list survive the planted power cycle, and the format is kept.
- NOT met: the on-board cold cycle. This lane has no bench access.

Open risks/questions:
- The one-pass deviation may want a ruling.
- The faces' hold measured 553 to 635 clocks on a zero-latency window model; DDR latency adds to it, against the processor's 4,096-clock gather watchdog.
- The side-port image-window lock now follows the enable released after the map restore.
- The sweep ran under CPython 3.14: the local 3.12.3 build lacks `os.pidfd_open`, which its process-ownership preflight needs.
- Step 0 found lane 3 (names) not adopted in the parent. It did not block this lane, and the name sticky pending stays.
